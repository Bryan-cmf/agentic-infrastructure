// guardian.js — Guardian 語義審查層（pure logic, testable without SDK）
//
// A second model (deepseek-v4-flash) that semantically reviews each turn
// for skill-skipping / fabrication that regex can't catch. Called from the
// before_agent_finalize hook in index.js.
//
// Extracted into its own module (no SDK dependency) so it can be unit-tested
// in isolation with a mock `api.runtime.llm.complete`.

// ─── Guardian system prompt ──────────────────────────────────────────
export const GUARDIAN_SYSTEM_PROMPT = `你是 infra-enforcer 的 Guardian 語義審查員。

你的職責：判斷 Agent 這次回覆是否「真的」遵循了技能要求，還是在偽造/跳過。

## 你要判斷的 4 個維度（regex 抓不到的）

1. **偽造檢測**：回覆是否「聲稱」用了某技能，但實際 toolCall 紀錄顯示沒有？或在回覆文字裡編造了技能的執行結果？
2. **遵循深度**：呼叫了技能，但是否真的遵循其指引？還是「調了就丟」完全無視技能內容？
3. **技能匹配**：調用的技能是否真正適合這個任務？（不是只看是否在推薦清單，而是判語義適切性）
4. **完整性**：是否跳過了技能要求的關鍵步驟？

## 判定標準

- **pass**：確實呼叫了適合的技能，且真的遵循了（不是嘴上說說）
- **weak_pass**：呼叫了技能但遵循不完整，或技能匹配度勉強
- **reject**：偽造、跳過、調了不用、用錯技能

## 輸出格式（嚴格 JSON，不要 markdown 包裹）

{
  "verdict": "pass" | "weak_pass" | "reject",
  "reason": "一句話說明為什麼這個判定",
  "evidence": "具體證據（引用回覆裡的哪句話、哪個步驟出了問題）",
  "confidence": 0.0 到 1.0
}

## 重要

- 你看到的是「真實 toolCall 紀錄」+「Agent 的回覆文字」。比對兩者。
- 如果 toolCall 顯示沒呼叫任何技能，但回覆寫得像用了 → 這是偽造 → reject。
- 如果 toolCall 顯示呼叫了，但回覆內容跟該技能無關 → 調了就丟 → reject。
- 寧可嚴格（誤判 reject 只是要求重做），不要放水（誤判 pass 會讓偽造通過）。
- 只回 JSON，不要任何其他文字。`;

// ─── Build the review payload sent to the Guardian model ─────────────
//
// Assembles a concise summary of the turn for the Guardian to judge:
// - what the user asked (last user message)
// - what the agent replied (last assistant message text)
// - the REAL tool calls (ground truth from transcript)
// - the regex pre-judgment (so Guardian can confirm or override)
export function buildGuardianPrompt(messages, regexResult) {
  // Last user message
  let userMsg = "";
  for (let i = (messages?.length ?? 0) - 1; i >= 0; i--) {
    const m = messages[i];
    if (m?.role === "user") {
      userMsg = typeof m.content === "string"
        ? m.content
        : (Array.isArray(m.content) ? m.content.filter(b => b?.type === "text").map(b => b.text).join(" ") : "");
      break;
    }
  }

  // Last assistant reply text
  let replyText = "";
  for (let i = (messages?.length ?? 0) - 1; i >= 0; i--) {
    const m = messages[i];
    if (m?.role !== "assistant") continue;
    const c = m.content;
    if (typeof c === "string") { replyText = c; break; }
    if (Array.isArray(c)) {
      replyText = c.filter(b => b?.type === "text").map(b => b.text).join("\n");
      break;
    }
  }

  // Truncate to keep the Guardian prompt small (latency/cost).
  const trim = (s, n) => (s && s.length > n ? s.slice(0, n) + "…[截斷]" : s || "(空)");

  return `請審查以下 Agent 回覆是否真的遵循了技能要求。

## 用戶請求
${trim(userMsg, 500)}

## Agent 的回覆（節錄）
${trim(replyText, 1500)}

## 真實 toolCall 紀錄（ground truth，不可偽造）
呼叫的技能：${regexResult?.detail?.called_skills?.length ? regexResult.detail.called_skills.join(", ") : "（無）"}
router 推薦的技能：${regexResult?.detail?.router_recommended?.length ? regexResult.detail.router_recommended.join(", ") : "（無）"}

## regex 預判定
verdict: ${regexResult?.verdict ?? "unknown"}
reason: ${regexResult?.reason ?? "unknown"}

## 你的任務
核對「回覆文字」與「真實 toolCall 紀錄」，判斷 Agent 是否偽造、跳過、或調了不用。
你可以推翻 regex 的判定（regex 只看模式，你看語義）。
回傳嚴格 JSON。`;
}

// ─── Parse the Guardian's JSON verdict ───────────────────────────────
//
// Tolerant parser: the model may wrap JSON in markdown or add prose.
// Extracts the first {...} block and validates required fields.
export function parseGuardianVerdict(text) {
  if (!text || typeof text !== "string") {
    return { verdict: "unknown", reason: "guardian_empty_response", evidence: "", confidence: 0, parseError: true };
  }
  // Try direct parse first.
  let parsed = null;
  try {
    parsed = JSON.parse(text);
  } catch {
    // Try extracting a JSON code block or bare {...}.
    const m = text.match(/\{[\s\S]*\}/);
    if (m) {
      try { parsed = JSON.parse(m[0]); } catch { /* leave null */ }
    }
  }
  if (!parsed) {
    return { verdict: "unknown", reason: "guardian_unparseable", evidence: text.slice(0, 200), confidence: 0, parseError: true };
  }
  const verdict = String(parsed.verdict || "").toLowerCase().trim();
  const valid = verdict === "pass" || verdict === "weak_pass" || verdict === "reject";
  return {
    verdict: valid ? verdict : "unknown",
    reason: String(parsed.reason || "").slice(0, 500),
    evidence: String(parsed.evidence || "").slice(0, 800),
    confidence: typeof parsed.confidence === "number" ? parsed.confidence : 0.5,
    parseError: !valid,
  };
}

// ─── The main review function ────────────────────────────────────────
//
// Calls api.runtime.llm.complete to get a Guardian verdict.
// Returns { verdict, reason, evidence, confidence, source: "guardian"|"regex_fallback" }.
// NEVER throws — on any failure, returns the regexResult as fallback so the
// main hook flow is never broken by the Guardian layer.
export async function guardianReview(api, messages, regexResult, ctx, opts = {}) {
  const model = opts.model || "deepseek/deepseek-v4-flash";
  const timeoutMs = opts.timeoutMs ?? 15000;

  // If the plugin api doesn't expose llm.complete (shouldn't happen, but
  // defensive), fall back to regex immediately.
  if (!api?.runtime?.llm?.complete) {
    return { ...regexResult, source: "regex_fallback", fallbackReason: "no_llm_complete_api" };
  }

  const prompt = buildGuardianPrompt(messages, regexResult);

  try {
    const result = await api.runtime.llm.complete({
      messages: [{ role: "user", content: prompt }],
      model,
      systemPrompt: GUARDIAN_SYSTEM_PROMPT,
      purpose: "guardian-semantic-review",
      agentId: ctx?.agentId,
      maxTokens: 300,
      temperature: 0,
      signal: AbortSignal.timeout(timeoutMs),
    });
    const parsed = parseGuardianVerdict(result?.text);

    // If the Guardian returned an unparseable verdict, don't trust it —
    // fall back to regex rather than guessing.
    if (parsed.verdict === "unknown") {
      return { ...regexResult, source: "regex_fallback", fallbackReason: parsed.reason, guardianRaw: result?.text?.slice(0, 200) };
    }

    return {
      verdict: parsed.verdict,
      reason: parsed.reason,
      evidence: parsed.evidence,
      confidence: parsed.confidence,
      regexVerdict: regexResult?.verdict,
      regexReason: regexResult?.reason,
      called_skills: regexResult?.detail?.called_skills ?? [],
      router_recommended: regexResult?.detail?.router_recommended ?? [],
      source: "guardian",
    };
  } catch (err) {
    // Timeout, network error, model error, override-policy rejection —
    // never break the main flow. Fall back to regex.
    return {
      ...regexResult,
      source: "regex_fallback",
      fallbackReason: `guardian_error: ${err?.message || String(err).slice(0, 120)}`,
    };
  }
}
