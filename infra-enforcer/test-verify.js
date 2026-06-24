// test-verify.js — Verification tests for infra-enforcer v2.0
// Run: node /Users/Claw/.openclaw/infra-enforcer/test-verify.js
//
// These tests prove the three compliance verdicts behave correctly, i.e. that
// "pretending to use skills" (writing 🛠️ in the reply with no real tool call)
// is now REJECTED, and that real Skill tool calls + router cross-check gate
// the score. Pure-function tests against evaluateCompliance().

import { evaluateCompliance, extractSkillCalls, extractRouterRecommended } from "./compliance.js";

let pass = 0;
let fail = 0;
function assert(name, cond, detail) {
  if (cond) {
    pass++;
    console.log(`  ✅ ${name}`);
  } else {
    fail++;
    console.error(`  ❌ ${name}`);
    if (detail !== undefined) console.error(`     got: ${JSON.stringify(detail)}`);
  }
}

console.log("\n=== infra-enforcer v2.0 verification ===\n");

// ─── Case A: FABRICATION — reply has 🛠️ text but NO real Skill tool call ──
// This is THE regression test for the bug we fixed. Before the fix, this case
// was awarded +0.5 (the emoji substring matched). It MUST now be rejected.
console.log("Case A — 偽造：回覆有 🛠️ 但無真實工具呼叫（應 REJECT -0.5）");
{
  const messages = [
    { role: "user", content: "幫我做個網站" },
    {
      role: "assistant",
      content: [
        {
          type: "text",
          text:
            "🔀 Router: 💻代碼 × 🎨設計\n→ 專項強制：[frontend-design, design-taste-frontend]\n\n這是您的網站...\n\n🛠️ 使用技能：frontend-design",
        },
      ],
      stopReason: "stop",
    },
  ];
  const r = evaluateCompliance(messages);
  assert("verdict is reject", r.verdict === "reject", r.verdict);
  assert("reason is no_skill_tool_call", r.reason === "no_skill_tool_call", r.reason);
  assert("delta is -0.5", r.delta === -0.5, r.delta);
  assert("called_skills is empty", r.detail.called_skills.length === 0, r.detail.called_skills);
}

// ─── Case B: HONEST PASS — real Skill tool call matching router recommendation
console.log("\nCase B — 真實通過：呼叫 Skill 工具且符合 router 推薦（應 PASS +0.5）");
{
  const messages = [
    { role: "user", content: "幫我做個網站" },
    {
      role: "assistant",
      content: [
        { type: "text", text: "🔀 Router: 💻代碼 × 🎨設計\n→ 專項強制：[frontend-design]" },
        {
          type: "toolCall",
          id: "call_1",
          name: "Skill",
          arguments: { skill: "frontend-design" },
        },
        { type: "text", text: "已載入 frontend-design，開始設計..." },
      ],
      stopReason: "stop",
    },
  ];
  const r = evaluateCompliance(messages);
  assert("verdict is pass", r.verdict === "pass", r.verdict);
  assert("reason is used_router_recommended_skill", r.reason === "used_router_recommended_skill", r.reason);
  assert("delta is +0.5", r.delta === 0.5, r.delta);
  assert("frontend-design detected as called", r.detail.called_skills.includes("frontend-design"), r.detail.called_skills);
  assert("frontend-design detected as recommended", r.detail.router_recommended.includes("frontend-design"), r.detail.router_recommended);
  assert("matched includes frontend-design", r.detail.matched && r.detail.matched.includes("frontend-design"), r.detail.matched);
}

// ─── Case C: WRONG SKILL — called a skill but not what router recommended ──
console.log("\nCase C — 技能不符：呼叫了 Skill 但不是 router 推薦的（應 REJECT -0.3）");
{
  const messages = [
    { role: "user", content: "幫我做個網站" },
    {
      role: "assistant",
      content: [
        { type: "text", text: "🔀 Router: 💻代碼 × 🎨設計\n→ 專項強制：[frontend-design]" },
        {
          type: "toolCall",
          id: "call_1",
          name: "Skill",
          arguments: { skill: "dcf-valuation" },
        },
        { type: "text", text: "已載入..." },
      ],
      stopReason: "stop",
    },
  ];
  const r = evaluateCompliance(messages);
  assert("verdict is reject", r.verdict === "reject", r.verdict);
  assert("reason is skill_called_but_not_router_recommended", r.reason === "skill_called_but_not_router_recommended", r.reason);
  assert("delta is -0.3", r.delta === -0.3, r.delta);
}

// ─── Case D: USED SKILL, NO ROUTER BLOCK — weak pass ───────────────────────
console.log("\nCase D — 弱通過：呼叫了 Skill 但沒輸出 router 區塊（應 weak_pass +0.2）");
{
  const messages = [
    { role: "user", content: "hi" },
    {
      role: "assistant",
      content: [
        {
          type: "toolCall",
          id: "call_1",
          name: "Skill",
          arguments: { skill: "vector-memory" },
        },
        { type: "text", text: "完成了。" },
      ],
      stopReason: "stop",
    },
  ];
  const r = evaluateCompliance(messages);
  assert("verdict is weak_pass", r.verdict === "weak_pass", r.verdict);
  assert("delta is +0.2", r.delta === 0.2, r.delta);
}

// ─── Case E: legacy tool_use / input shape still detected ──────────────────
console.log("\nCase E — 相容性：legacy tool_use/input 格式仍應被偵測（應 PASS）");
{
  const messages = [
    { role: "user", content: "x" },
    {
      role: "assistant",
      content: [
        { type: "text", text: "→ 專項強制：[frontend-design]" },
        { type: "tool_use", id: "u1", name: "Skill", input: { skill: "frontend-design" } },
      ],
      stopReason: "stop",
    },
  ];
  const r = evaluateCompliance(messages);
  assert("verdict is pass (legacy shape)", r.verdict === "pass", r.verdict);
  assert("delta is +0.5", r.delta === 0.5, r.delta);
}

// ─── Unit: router recommendation parser ────────────────────────────────────
console.log("\nCase F — router 解析器：多種格式都應抓到推薦技能");
{
  const a = extractRouterRecommended("→ 專項強制：[frontend-design, design-taste-frontend]");
  assert("bracket form parsed", a.has("frontend-design") && a.has("design-taste-frontend"), [...a]);

  const b = extractRouterRecommended("推薦技能：`ak-hk-stock-dd` `tavily-search`");
  assert("backtick form parsed", b.has("ak-hk-stock-dd") && b.has("tavily-search"), [...b]);

  const c = extractRouterRecommended("完全沒有 router 標記的普通回覆");
  assert("no-marker returns empty", c.size === 0, [...c]);
}

// ─── Unit: skill-call extraction ignores non-Skill tools ───────────────────
console.log("\nCase G — 只抓 Skill 工具，忽略其他工具呼叫");
{
  const messages = [
    {
      role: "assistant",
      content: [
        { type: "toolCall", id: "1", name: "Bash", arguments: { command: "ls" } },
        { type: "toolCall", id: "2", name: "Read", arguments: { file_path: "/x" } },
        { type: "toolCall", id: "3", name: "Skill", arguments: { skill: "critique" } },
      ],
      stopReason: "stop",
    },
  ];
  const c = extractSkillCalls(messages);
  assert("only Skill tool extracted", c.size === 1 && c.has("critique"), [...c]);
}

// ─── Case H: revise decision — reject verdicts should trigger revise ──────
// The before_agent_finalize hook only revises on hard reject (no tool call
// or wrong skill); weak_pass is allowed through. This encodes that policy.
console.log("\nCase H — revise 決策：reject 應重做，weak_pass 應放行");
{
  // Fabricated → reject → would revise
  const fab = evaluateCompliance([
    { role: "assistant", content: [{ type: "text", text: "🛠️ 使用技能" }] },
  ]);
  const fabShouldRevise = fab.verdict === "reject";
  assert("fabricated → reject (revise)", fabShouldRevise, fab.verdict);

  // Used a skill but no router block → weak_pass → would NOT revise
  const weak = evaluateCompliance([
    {
      role: "assistant",
      content: [
        { type: "toolCall", id: "1", name: "Skill", arguments: { skill: "critique" } },
        { type: "text", text: "done" },
      ],
    },
  ]);
  const weakShouldNotRevise = weak.verdict === "pass" || weak.verdict === "weak_pass";
  assert("used-skill-no-router → not hard reject (no revise)", weakShouldNotRevise, weak.verdict);

  // Wrong skill → reject → would revise
  const wrong = evaluateCompliance([
    {
      role: "assistant",
      content: [
        { type: "text", text: "→ 專項強制：[frontend-design]" },
        { type: "toolCall", id: "1", name: "Skill", arguments: { skill: "dcf-valuation" } },
      ],
    },
  ]);
  assert("wrong skill → reject (revise)", wrong.verdict === "reject", wrong.verdict);
}

// ─── Case I: router parser handles backtick + bracket + CN comma ──────────
console.log("\nCase I — router 解析器邊界：中文逗號、多種格式混用");
{
  const mixed = extractRouterRecommended(
    "🔀 Router v3.0：💰金融 × 🔍搜索\n  → 專項強制：[ak-hk-stock-dd，tavily-search]",
  );
  assert("CN comma in bracket list parsed", mixed.has("ak-hk-stock-dd") && mixed.has("tavily-search"), [...mixed]);

  const noise = extractRouterRecommended("Router v3.0 says hello world");
  assert("'v3.0' noise filtered out", !noise.has("v3.0"), [...noise]);
}

// ─── Case J: audit record shape (fields the watchdog will read) ───────────
console.log("\nCase J — audit 紀錄欄位完整性（watchdog 依賴的欄位都存在）");
{
  const r = evaluateCompliance([
    {
      role: "assistant",
      content: [
        { type: "text", text: "→ 專項強制：[frontend-design]" },
        { type: "toolCall", id: "1", name: "Skill", arguments: { skill: "frontend-design" } },
      ],
    },
  ]);
  // The audit entry is built from result.detail + result fields in agent_end.
  const auditEntry = {
    ts: new Date().toISOString(),
    verdict: r.verdict,
    reason: r.reason,
    delta: r.delta,
    called_skills: r.detail.called_skills,
    router_recommended: r.detail.router_recommended,
    matched: r.detail.matched ?? [],
  };
  const requiredFields = ["ts", "verdict", "reason", "delta", "called_skills", "router_recommended", "matched"];
  const allPresent = requiredFields.every((f) => auditEntry[f] !== undefined);
  assert("all audit fields present", allPresent, Object.keys(auditEntry));
  assert("audit called_skills is array", Array.isArray(auditEntry.called_skills), typeof auditEntry.called_skills);
}

// ─── Case K: maintenance-turn discrimination ──────────────────────────────
// Enforcement applies ONLY to explicit user turns. Everything else (cron,
// heartbeat, supervisor loops, manual test, undefined) is exempt by default —
// this prevents ANY system/scheduled turn from draining the score, including
// triggers we haven't enumerated. This test pins the "default-exempt" policy.
console.log("\nCase K — 維護任務識別（僅 user turn 被強制，其餘一律豁免）");
{
  const triggers = {
    cron: { trigger: "cron", jobId: "abc-123", workspaceDir: "/tmp/x" },
    heartbeat: { trigger: "heartbeat", workspaceDir: "/tmp/x" },
    user: { trigger: "user", senderId: "ou_1", workspaceDir: "/tmp/x" },
    undefined: { workspaceDir: "/tmp/x" },
    manual: { trigger: "manual", workspaceDir: "/tmp/x" },
    supervisor: { trigger: "supervisor", workspaceDir: "/tmp/x" },
  };
  // Mirror the predicate from index.js: enforce ONLY when trigger === "user".
  const isMaintenance = (ctx) => ctx?.trigger !== "user";
  assert("cron turn is exempt", isMaintenance(triggers.cron) === true);
  assert("heartbeat turn is exempt", isMaintenance(triggers.heartbeat) === true);
  assert("user turn is enforced (NOT exempt)", isMaintenance(triggers.user) === false);
  assert("undefined trigger is exempt (default-off)", isMaintenance(triggers.undefined) === true);
  assert("manual turn is exempt", isMaintenance(triggers.manual) === true);
  assert("supervisor turn is exempt (new trigger auto-covered)", isMaintenance(triggers.supervisor) === true);
}

console.log(`\n=== 結果：${pass} 通過 / ${fail} 失敗 ===\n`);
if (fail > 0) {
  console.error("❌ 有測試失敗，修復未完成。");
  process.exit(1);
}
console.log("✅ 全部通過。合規驗證現在只認真實 Skill 工具呼叫。");
process.exit(0);
