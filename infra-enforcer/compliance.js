// compliance.js — Pure compliance-evaluation logic for infra-enforcer.
//
// Extracted from index.js so it has NO dependency on the openclaw plugin SDK
// and can be unit-tested in isolation with plain `node`. index.js re-exports
// these for the plugin runtime; test-verify.js imports them directly.

// ─── Scoring deltas ──────────────────────────────────────────────────
export const DELTA = {
  noToolCall: -0.5,      // no Skill tool call at all → hard reject
  matchedRouter: +0.5,   // invoked a skill the router recommended → pass
  wrongSkill: -0.3,      // invoked a skill but none matched router recommendation
  usedButNoRouter: +0.2, // invoked some skill, but no router block emitted
};

// Markers that indicate a router recommendation block follows in the reply.
const ROUTER_MARKERS = [
  "專項強制",
  "推薦技能",
  "強制載入",
  "required_skills",
  "推薦：",
  "Router",
];

// ─── Extract REAL Skill tool calls from the transcript ───────────────
//
// Tool calls live inside AssistantMessage.content blocks:
//   { type: "toolCall", name: "Skill", arguments: { skill: "..." } }
// Legacy/external agents may emit { type: "tool_use", input: {...} }; we
// accept both (mirrors the headroom plugin's defensive handling).
export function extractSkillCalls(messages) {
  const called = new Set();
  if (!Array.isArray(messages)) return called;
  for (const msg of messages) {
    if (msg?.role !== "assistant") continue;
    const blocks = Array.isArray(msg.content) ? msg.content : [];
    for (const block of blocks) {
      const isToolCall = block?.type === "toolCall" || block?.type === "tool_use";
      if (!isToolCall) continue;
      const name = block.name;
      // The Skill tool; also tolerate "skill" (case-insensitive exact).
      if (name !== "Skill" && name !== "skill") continue;
      const args = block.type === "toolCall" ? block.arguments : block.input;
      const skillName = args?.skill || args?.name;
      if (typeof skillName === "string" && skillName.trim()) {
        called.add(skillName.trim());
      }
    }
  }
  return called;
}

// Extract the assistant's final reply as a string (for router-block parsing).
export function getReplyText(messages) {
  if (!Array.isArray(messages)) return "";
  for (let i = messages.length - 1; i >= 0; i--) {
    const m = messages[i];
    if (m?.role !== "assistant") continue;
    const c = m.content;
    if (typeof c === "string") return c;
    if (Array.isArray(c)) {
      return c
        .filter((b) => b?.type === "text" && typeof b.text === "string")
        .map((b) => b.text)
        .join("\n");
    }
    return "";
  }
  return "";
}

// Parse the router recommendation block from the reply text.
// skill-router emits lines like:
//   🔀 Router v3.0：[類別] × [階段]
//     → 專項強制：[skill-A, skill-B, skill-C]
// We collect any backtick-quoted or bracket-listed token that looks like a
// skill name appearing after a router marker.
export function extractRouterRecommended(replyText) {
  const recommended = new Set();
  if (!replyText) return recommended;
  // Only look at text AFTER the first router marker appears, so we don't grab
  // unrelated backtick tokens from earlier in the reply.
  let cut = replyText.length;
  for (const marker of ROUTER_MARKERS) {
    const idx = replyText.indexOf(marker);
    if (idx !== -1 && idx < cut) cut = idx;
  }
  // If no marker at all, there's nothing to cross-check against.
  if (cut === replyText.length) return recommended;
  const tail = replyText.slice(cut, cut + 400); // bound the scan window
  // Backtick-quoted skill names: `skill-name`
  for (const m of tail.matchAll(/`([a-z][a-z0-9-]{1,60})`/gi)) {
    recommended.add(m[1].toLowerCase());
  }
  // Bracketed list form: [skill-A, skill-B]
  for (const m of tail.matchAll(/\[([^\]]+)\]/g)) {
    for (const piece of m[1].split(/[,，|]/)) {
      const t = piece.trim().replace(/[`'"]/g, "").toLowerCase();
      if (/^[a-z][a-z0-9-]{1,60}$/.test(t)) recommended.add(t);
    }
  }
  // Filter out obvious non-skills the router line carries ("v3.0", etc.)
  for (const noise of ["v3.0", "v2.0", "router"]) recommended.delete(noise);
  return recommended;
}

// ─── Core: pure compliance evaluation ────────────────────────────────
//
// Returns { verdict, delta, reason, detail }.
//   verdict ∈ {"pass", "weak_pass", "reject"}
//   delta   — signed score change to apply
export function evaluateCompliance(messages) {
  const called = extractSkillCalls(messages);
  const replyText = getReplyText(messages);
  const recommended = extractRouterRecommended(replyText);

  const detail = {
    called_skills: [...called],
    router_recommended: [...recommended],
  };

  // 1. No real Skill tool call at all → hard reject. (This is the fix for
  //    "pretending": writing "🛠️ 使用技能" no longer counts.)
  if (called.size === 0) {
    return {
      verdict: "reject",
      delta: DELTA.noToolCall,
      reason: "no_skill_tool_call",
      detail: {
        ...detail,
        note: "reply text is irrelevant; only real Skill tool calls count",
      },
    };
  }

  // 2. Router emitted a recommendation → cross-check.
  if (recommended.size > 0) {
    const matched = [...called].filter((s) =>
      recommended.has(s.toLowerCase()),
    );
    if (matched.length > 0) {
      return {
        verdict: "pass",
        delta: DELTA.matchedRouter,
        reason: "used_router_recommended_skill",
        detail: { ...detail, matched },
      };
    }
    return {
      verdict: "reject",
      delta: DELTA.wrongSkill,
      reason: "skill_called_but_not_router_recommended",
      detail: {
        ...detail,
        note: "called skills did not intersect router recommendation",
      },
    };
  }

  // 3. Used a skill but emitted no router block → weak pass.
  return {
    verdict: "weak_pass",
    delta: DELTA.usedButNoRouter,
    reason: "used_skill_no_router_block",
    detail,
  };
}
