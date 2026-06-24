// infra-enforcer/index.js
// Infrastructure Enforcement Plugin for OpenClaw
// 3 Hook injection points: before_prompt_build, before_agent_run, agent_end
//
// v2.0 (2026-06-23) — Root-cause rewrite.
//   FIX 1: handlers now take (event, ctx); workspaceDir read from ctx.workspaceDir
//          (the old code read event.context.*, which does not exist in the SDK,
//           so the block gate short-circuited and NEVER fired).
//   FIX 2: compliance is now judged by REAL Skill tool calls (AssistantMessage
//          content blocks with type==="toolCall" && name==="Skill"), NOT by the
//          presence of "🛠️" / "使用技能" strings in the reply. The old emoji
//          substring check actively rewarded fabrication ("pretending to use
//          skills"). See evaluateCompliance() in ./compliance.js.
//   FIX 3: when a router recommendation is emitted in the reply, the skills
//          actually invoked are cross-checked against it.
//
// The pure evaluation logic lives in ./compliance.js (no SDK dependency) so it
// can be unit-tested in isolation. This file wires it into the plugin runtime.

import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";
import { readFileSync, existsSync, writeFileSync, mkdirSync, appendFileSync, statSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { execFile } from "node:child_process";
import {
  DELTA,
  evaluateCompliance,
} from "./compliance.js";
import { guardianReview } from "./guardian.js";

// Re-export so existing imports keep working.
export { evaluateCompliance, extractSkillCalls, extractRouterRecommended } from "./compliance.js";

// ─── Plugin config ───────────────────────────────────────────────────
// The SDK does not surface per-plugin config through hook signatures in this
// version, so defaults are constants overridable via INFRA_ENFORCER_* env vars.
const CONFIG = {
  bootstrapScorePath:
    process.env.INFRA_ENFORCER_SCORE_PATH || "memory/skill-compliance/score.json",
  deathThreshold: Number(process.env.INFRA_ENFORCER_DEATH_THRESHOLD ?? 0),
  injectChecklist: process.env.INFRA_ENFORCER_INJECT_CHECKLIST !== "false",
  blockUncompliant: process.env.INFRA_ENFORCER_BLOCK !== "false",
  initialScore: Number(process.env.INFRA_ENFORCER_INITIAL_SCORE ?? 5.0),
  maxScore: 10,
  historyLimit: Number(process.env.INFRA_ENFORCER_HISTORY_LIMIT ?? 20),
  auditMaxBytes: Number(process.env.INFRA_ENFORCER_AUDIT_MAX_BYTES ?? 500_000),
  auditKeepLines: Number(process.env.INFRA_ENFORCER_AUDIT_KEEP_LINES ?? 2000),
  reviseMaxAttempts: Number(process.env.INFRA_ENFORCER_REVISE_MAX ?? 2),
  // IM reject-notification (openclaw message send). Disabled by default to
  // avoid surprises; enable via env. Set to "off" to suppress.
  notifyChannel: process.env.INFRA_ENFORCER_NOTIFY_CHANNEL || "feishu",
  notifyTarget: process.env.INFRA_ENFORCER_NOTIFY_TARGET || "ou_142d6f44476f17b38709ed86dfe7dc3b",
  notifyEnabled: process.env.INFRA_ENFORCER_NOTIFY !== "off",
  notifyDangerScore: Number(process.env.INFRA_ENFORCER_NOTIFY_DANGER_SCORE ?? 2.0),
  notifyDailyCap: Number(process.env.INFRA_ENFORCER_NOTIFY_DAILY_CAP ?? 3),
  // Guardian semantic review (second-model check for fabrication/skipping).
  guardianModel: process.env.INFRA_ENFORCER_GUARDIAN_MODEL || "qwen/qwen3-max-2026-01-23",
  guardianTimeoutMs: Number(process.env.INFRA_ENFORCER_GUARDIAN_TIMEOUT ?? 15000),
  // agentId allowlist: enforce ONLY for these agents (default-exempt policy
  // was trigger-based, but external-supervisor shares agentId=main with user
  // turns, so trigger alone misfires). Whitelist the conversation agent(s)
  // that should be subject to skill enforcement.
  enforceAgentIds: (process.env.INFRA_ENFORCER_AGENT_IDS || "main")
    .split(",").map(s => s.trim()).filter(Boolean),
};

// ─── Bootstrap Enforcement Context (injected into system prompt) ─────
//
// Built DYNAMICALLY per workspace so the injected skill list + routing table
// never go stale. Reads the ten-piece SKILL.md frontmatter and the router's
// matrix from disk at call time (cheap; cached by the prompt-cache layer).

const INFRA_SKILLS = [
  "agentic-infra",
  "skill-router",
  "infra-watchdog",
  "skill-curator",
  "agent-evolver",
  "agent-previsor",
];

// Core routing matrix excerpt (kept compact; full table lives in skill-router).
// Matches skill-router/SKILL.md "專項技能層" so the model can route without
// loading the skill first. ~2KB, well under any prompt budget.
const ROUTER_TABLE = `
| 類別 | 階段 | 關鍵詞 | 強制載入的專項技能 |
|------|------|--------|------------------|
| 💻 代碼 | 📋 規劃 | 設計/架構/規劃 | software-architect, architecture-patterns |
| 💻 代碼 | 💻 開發 | 寫代碼/開發/實現 | karpathy-guidelines, tdd |
| 💻 代碼 | 🧪 診斷 | Bug/報錯/審查/重構 | software-architect, agent-previsor |
| 💻 代碼 | 🚀 部署 | 部署/上線/Vercel | deploy-vercel |
| 💰 金融 | 🔍 搜索 | 港股/股票/調研/DD | ak-hk-stock-dd, tavily-search |
| 💰 金融 | 📊 分析 | 估值/財務/DCF | ak-financial-analyst, dcf-valuation |
| 🛠️ 日常 | 📋 規劃 | 規劃/下一步/討論 | agent-previsor, idea-refine |
| 🛠️ 日常 | ⚙️ 維運 | 配置/修復/同步 | agent-previsor |
| 🛠️ 日常 | 📊 分析 | 報告/總結/審計 | agent-previsor, software-architect |
| 🎨 設計 | 🎨 設計 | UI/網站/前端/PPT | frontend-design, ui-ux-pro-max |
| 🎨 設計 | 🔍 審查 | UX審查/設計審查 | design-taste-frontend, ui-ux-pro-max |
`;

// Read a skill's description (first paragraph of frontmatter) for the list.
function readSkillBlurb(ws, skillName) {
  for (const rel of [`skills/${skillName}/SKILL.md`, `.zcode/skills/${skillName}/SKILL.md`]) {
    const p = resolve(ws, rel);
    try {
      if (!existsSync(p)) continue;
      const txt = readFileSync(p, "utf8");
      const m = txt.match(/^---\n([\s\S]*?)\n---/);
      if (!m) return { name: skillName, desc: "" };
      const desc = (m[1].match(/^description:\s*(.+)$/m)?.[1] || "").replace(/^["']|["']$/g, "");
      // Keep the part before any " — " and trim to one line.
      const short = desc.split("—")[0].trim().slice(0, 90);
      return { name: skillName, desc: short };
    } catch {
      /* skip */
    }
  }
  return { name: skillName, desc: "" };
}

// Build the full enforcement context. Memoized per-workspace for the process
// lifetime; skills don't change mid-session often, and the watcher refreshes
// on the next session anyway.
const _ctxCache = new Map();
function buildEnforcementContext(ws) {
  if (_ctxCache.has(ws)) return _ctxCache.get(ws);

  const skills = INFRA_SKILLS.map((n) => readSkillBlurb(ws, n)).filter((s) => s.desc);
  const skillList = skills
    .map((s) => `  - \`${s.name}\` — ${s.desc}`)
    .join("\n");

  const ctx = `🧰 [SYSTEM ENFORCEMENT — 基礎設施強制載入 v3]

在執行任何任務前，這是系統層面的架構強制要求，不可跳過。

## 🔴 回合起手式（每次收到訊息的第一個動作）

\`\`\`
收到訊息
  → Step 1: 用 Skill 工具呼叫 skill-router（分類當前任務）
  → Step 2: 依下方路由表，用 Skill 工具呼叫推薦的專項技能（至少一個）
  → Step 3: 執行任務
  → Step 4: 回覆末尾附 🛠️ 使用技能（僅供人類查看，不參與評分）
\`\`\`

## 📋 基礎設施十件套（可用 Skill 工具呼叫）

${skillList || "  （讀取失敗，請 read skills/skill-router/SKILL.md 查看完整清單）"}

## 🔀 核心路由表（不需先載入 skill-router 即可查表）

${ROUTER_TABLE}

## 🔴 合規判定規則（由 infra-enforcer 程式執行，不可作弊）

合規在每次回覆後由 infra-enforcer **核對真實的 Skill 工具呼叫紀錄**判定
（讀取 AssistantMessage.content 裡 type==="toolCall" && name==="Skill" 的區塊）。
**不是**看回覆文字有沒有「🛠️」。寫這些文字不會得分。

- 完全沒有 Skill 工具呼叫 → 分數 ${DELTA.noToolCall}（REJECT）+ 系統會要求你 revise 重答
- 呼叫了 router 推薦的技能 → 分數 ${DELTA.matchedRouter}（PASS）
- 呼叫了技能但不符合 router 推薦 → 分數 ${DELTA.wrongSkill}（REJECT）
- 呼叫了技能但沒輸出 router 區塊 → 分數 ${DELTA.usedButNoRouter}（弱 PASS）
- 累積分數 ≤ ${CONFIG.deathThreshold} → 下一次 turn 硬性 block，必須 /reset

## 🚫 禁止的合理化藉口

- ❌ 「這只是簡單任務」
- ❌ 「我已經知道了」
- ❌ 「先回覆，事後補」
- ❌ 打「🛠️ 使用技能」就以為可以過關（程式只認真實 toolCall）`;

  _ctxCache.set(ws, ctx);
  return ctx;
}

// ─── Helpers ──────────────────────────────────────────────────────────

// FIX 1: workspaceDir lives on the second hook argument (ctx), NOT on
// event.context. Fall back to the env var the 2026-06-18 install relied on.
function getWorkspace(ctx) {
  return ctx?.workspaceDir || process.env.OPENCLAW_WORKSPACE;
}

// Should this turn be subject to skill enforcement?
//
// TWO conditions must BOTH hold:
//   1. ctx.agentId is in the enforceAgentIds allowlist (default: ["main"])
//   2. ctx.trigger === "user" (a real user-initiated conversation)
//
// This replaces the earlier trigger-only gate, which misfired because
// external-supervisor (a cron job) shares agentId="main" with user turns but
// carried a non-"cron" trigger. With the AND condition, supervisor turns
// (trigger != "user") are exempt even though they share the agentId, AND
// turns from non-enforced agents (e.g. coder-*, ecc) are exempt even if
// triggered by a user.
//
// Also: turns that FAILED (model error/timeout) are never the model's fault
// and must not be scored — that's punishing infra outages, not skill-skipping.
function shouldEnforce(ctx, event) {
  // Condition 1: agent allowlist
  if (!CONFIG.enforceAgentIds.includes(ctx?.agentId)) return false;
  // Condition 2: must be a real user turn
  if (ctx?.trigger !== "user") return false;
  return true;
}

// A failed turn (model error/timeout/rate-limit) must never be scored.
// The agent didn't "skip" skills — it couldn't reply at all. Scoring these
// drains the score during outages and blocks recovery.
function isFailedTurn(event) {
  if (event?.success === false) return true;
  if (event?.error) return true;
  return false;
}

function getScorePath(ws) {
  return resolve(ws, CONFIG.bootstrapScorePath);
}

// FIX 2b: missing score.json now returns the configured initial score
// (default 5.0) instead of always 5, and never 0 — registering the plugin
// must not instantly lock every session out.
function readScore(filePath) {
  try {
    if (existsSync(filePath)) {
      const data = JSON.parse(readFileSync(filePath, "utf8"));
      // Tolerate both { score } and the richer skill-compliance schema.
      const s = data?.score;
      return typeof s === "number" ? s : CONFIG.initialScore;
    }
  } catch {
    /* fall through */
  }
  return CONFIG.initialScore;
}

function writeScore(filePath, score, reason, detail) {
  try {
    const dir = dirname(filePath);
    if (!existsSync(dir)) mkdirSync(dir, { recursive: true });

    // Merge semantics: preserve an existing history[] (e.g. legacy skill-compliance
    // entries) and append the new verdict, capped at HISTORY_LIMIT entries.
    let history = [];
    try {
      if (existsSync(filePath)) {
        const prev = JSON.parse(readFileSync(filePath, "utf8"));
        if (Array.isArray(prev?.history)) history = prev.history;
      }
    } catch {
      /* corrupt or missing — start fresh */
    }
    history.push({
      ts: new Date().toISOString(),
      verdict: detail?.verdict,
      reason,
      delta: detail?.delta,
      score_after: score,
      called_skills: detail?.called_skills ?? [],
      router_recommended: detail?.router_recommended ?? [],
    });
    if (history.length > CONFIG.historyLimit) {
      history = history.slice(-CONFIG.historyLimit);
    }

    writeFileSync(
      filePath,
      JSON.stringify(
        {
          score,
          maxScore: CONFIG.maxScore,
          reason,
          detail,
          history,
          scorer: "infra-enforcer",   // provenance: only this plugin may write here
          last_updated: new Date().toISOString(),
        },
        null,
        2,
      ),
      "utf8",
    );
  } catch {
    /* best-effort; never let scoring crash a run */
  }
}

// Append one structured line to audit.jsonl (the tamper-proof, machine-written
// record of every turn's real skill usage). Auto-rotates when it grows too long.
function appendAudit(scoreDir, entry) {
  try {
    const auditPath = resolve(scoreDir, "audit.jsonl");
    if (!existsSync(scoreDir)) mkdirSync(scoreDir, { recursive: true });
    appendFileSync(auditPath, JSON.stringify(entry) + "\n", "utf8");
    // Rotate: if the file exceeds the line budget, keep only the tail.
    try {
      const stat = statSync(auditPath);
      if (stat.size > CONFIG.auditMaxBytes) {
        const lines = readFileSync(auditPath, "utf8").split("\n").filter(Boolean);
        const kept = lines.slice(-CONFIG.auditKeepLines);
        writeFileSync(auditPath, kept.join("\n") + "\n", "utf8");
      }
    } catch {
      /* rotation is best-effort */
    }
  } catch {
    /* audit must never crash a run */
  }
}

// ─── IM reject-notification ──────────────────────────────────────────
// Spawns `openclaw message send` to push a heads-up to the operator when a
// turn is rejected or the score drops into the danger zone. Fire-and-forget:
// a delivery failure must NEVER break the agent_end hook. Daily rate-limited
// (default 3/day) so a stuck agent can't spam the chat.
const _notifySentToday = new Map(); // dateStr → count
function notifyReject(ws, scoreBefore, scoreAfter, reason) {
  if (!CONFIG.notifyEnabled) return;
  const danger = scoreAfter <= CONFIG.notifyDangerScore;
  // Only notify on reject OR when score crosses into the danger zone.
  // (score_after <= danger threshold counts as worth alerting.)
  if (!danger) return;

  // Daily cap per process.
  const today = new Date().toISOString().slice(0, 10);
  const sent = _notifySentToday.get(today) ?? 0;
  if (sent >= CONFIG.notifyDailyCap) return;

  const msg =
    `⚠️ [infra-enforcer] 合規警告\n` +
    `分數：${scoreBefore} → ${scoreAfter}（危險區 ≤ ${CONFIG.notifyDangerScore}）\n` +
    `原因：${reason}\n` +
    `連續失敗將導致下次 turn 被 block，需 /reset。`;

  const bin = process.env.OPENCLAW_BIN || "openclaw";
  execFile(
    bin,
    [
      "message", "send",
      "--channel", CONFIG.notifyChannel,
      "--target", CONFIG.notifyTarget,
      "--message", msg,
    ],
    { timeout: 30_000, cwd: ws || undefined },
    () => {
      // best-effort: ignore errors entirely (logged nowhere to avoid noise)
      _notifySentToday.set(today, sent + 1);
    },
  );
}

// ─── Plugin entry ────────────────────────────────────────────────────
export default definePluginEntry({
  id: "infra-enforcer",
  name: "Infrastructure Enforcer",
  description:
    "Forces infra bootstrap before every task; judges compliance by real Skill tool calls",

  register(api) {
    // ─── Hook #1: before_prompt_build ────────────────────────────────
    // Inject enforcement context into the SYSTEM prompt (cacheable).
    api.on(
      "before_prompt_build",
      async (_event, ctx) => {
        if (CONFIG.injectChecklist) {
          const ws = getWorkspace(ctx);
          return { prependSystemContext: buildEnforcementContext(ws) };
        }
      },
      { priority: 100 },
    );

    // ─── Hook #2: before_agent_run ───────────────────────────────────
    // Block the run if compliance score has hit the death threshold.
    // This is the ONLY hard gate. (Previously never fired due to the
    // event.context bug — now reads ctx.workspaceDir correctly.)
    api.on(
      "before_agent_run",
      async (_event, ctx) => {
        if (!CONFIG.blockUncompliant) return { outcome: "pass" };

        // Enforce ONLY for allowlisted agents on user-initiated turns.
        // (external-supervisor shares agentId=main but trigger != "user".)
        if (!shouldEnforce(ctx, _event)) return { outcome: "pass" };

        const ws = getWorkspace(ctx);
        if (!ws) {
          console.warn("[infra-enforcer] no workspace resolved; skipping block gate");
          return { outcome: "pass" };
        }

        const score = readScore(getScorePath(ws));
        if (score <= CONFIG.deathThreshold) {
          return {
            outcome: "block",
            reason: `compliance_score_${score}_below_threshold_${CONFIG.deathThreshold}`,
            message:
              `❌ [System Enforcement] Compliance score (${score}) hit the death threshold. ` +
              `The previous turns did not make real Skill tool calls. ` +
              `Please /reset the session and start with the proper infrastructure bootstrap ` +
              `(read PRE-TASK-CHECKLIST.md → agentic-infra Bootstrap → skill-router → Skill tool).`,
          };
        }
        return { outcome: "pass" };
      },
      { priority: 90 },
    );

    // ─── Hook #3: agent_end ──────────────────────────────────────────
    // Inspect the REAL tool-call transcript and update the compliance score.
    api.on(
      "agent_end",
      async (event, ctx) => {
        // Don't score maintenance turns OR failed turns.
        // - Non-enforced agents / non-user triggers: skip (default-exempt).
        // - Failed turns (model error/timeout/rate-limit): the agent couldn't
        //   reply at all — that's an outage, not skill-skipping. Scoring it
        //   drains the score during outages and blocks recovery.
        if (!shouldEnforce(ctx, event)) return;
        if (isFailedTurn(event)) return;

        const ws = getWorkspace(ctx);
        if (!ws) return;

        const scorePath = getScorePath(ws);
        const scoreDir = dirname(scorePath);
        const score = readScore(scorePath);
        const result = evaluateCompliance(event?.messages);

        const next = Math.max(
          Math.min(score + result.delta, CONFIG.maxScore),
          0,
        );
        writeScore(scorePath, next, result.reason, {
          ...result.detail,
          previous_score: score,
          delta: result.delta,
          verdict: result.verdict,
        });
        // Tamper-proof audit trail: every turn's real skill usage, written by
        // the program (never by the model). Single source of truth for watchdog.
        appendAudit(scoreDir, {
          ts: new Date().toISOString(),
          runId: event?.runId ?? null,
          trigger: ctx?.trigger ?? null,
          verdict: result.verdict,
          reason: result.reason,
          delta: result.delta,
          score_before: score,
          score_after: next,
          called_skills: result.detail?.called_skills ?? [],
          router_recommended: result.detail?.router_recommended ?? [],
          matched: result.detail?.matched ?? [],
        });
        // Push an IM heads-up if the score landed in the danger zone.
        notifyReject(ws, score, next, result.reason);
      },
      { priority: 100 },
    );

    // ─── Hook #4: before_agent_finalize ─────────────────────────────
    // Mid-strength gate: if the reply that's about to ship has NO real Skill
    // tool call, demand another model pass (revise) instead of accepting it.
    // Uses the SDK's native retry cap (maxAttempts) — the harness itself stops
    // revising after maxAttempts, so no infinite-token risk. This is the layer
    // between "nudge via prompt" (hook #1) and "block the next turn" (hook #2).
    api.on(
      "before_agent_finalize",
      async (event, ctx) => {
        // Enforce ONLY for allowlisted agents on user-initiated turns.
        if (!shouldEnforce(ctx, event)) return { action: "continue" };

        const messages = event?.messages;
        if (!Array.isArray(messages)) return { action: "continue" };

        // Stage 1: regex pre-judgment (fast, catches "no tool call at all").
        const regexResult = evaluateCompliance(messages);

        // Stage 2: Guardian semantic review (v4-flash). Runs EVERY user turn
        // (per user's "最嚴" choice). Guardian can override the regex verdict
        // — it catches fabrication, "called-but-ignored", wrong-fit skills
        // that regex structurally cannot see. On any Guardian failure, falls
        // back to the regex verdict (never breaks the main flow).
        const finalResult = await guardianReview(api, messages, regexResult, ctx, {
          model: CONFIG.guardianModel,
          timeoutMs: CONFIG.guardianTimeoutMs,
        });

        // Pass / weak_pass → accept the reply.
        if (finalResult.verdict === "pass" || finalResult.verdict === "weak_pass") {
          return { action: "continue" };
        }

        // Reject → revise. Build an instruction that includes the Guardian's
        // specific diagnosis (reason + evidence) when available, so the model
        // gets actionable feedback instead of a generic "use a skill" nudge.
        const calledList = finalResult.called_skills?.length
          ? finalResult.called_skills.join(", ")
          : "（沒有任何 Skill 工具呼叫）";

        const guardianDetail =
          finalResult.source === "guardian" && finalResult.evidence
            ? `\n\n🔍 Guardian 診斷：${finalResult.reason}\n證據：${finalResult.evidence}`
            : "";

        return {
          action: "revise",
          reason: `compliance_${finalResult.reason}`,
          retry: {
            maxAttempts: CONFIG.reviseMaxAttempts,
            instruction:
              `⚠️ [infra-enforcer + Guardian] 本回合合規檢查 REJECT（${finalResult.reason}）。` +
              `已核對真實 toolCall 紀錄：本回合 ${calledList}。` +
              `（評分來源：${finalResult.source}${finalResult.fallbackReason ? `, fallback: ${finalResult.fallbackReason}` : ""}）` +
              `infra-enforcer 只認真實的 Skill 工具呼叫，打「🛠️」文字不算；Guardian 會核對你是否真的遵循技能指引。` +
              `請重新作答：先用 Skill 工具呼叫 skill-router 分類任務，` +
              `再用 Skill 工具呼叫路由推薦的專項技能，然後切實遵循技能內容執行任務。` +
              guardianDetail,
          },
        };
      },
      { priority: 100 },
    );
  },
});
