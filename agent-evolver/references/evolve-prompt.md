# Agent Evolver — Monthly Cron Prompt

You are running the Agent Evolver's monthly self-reflection cycle. Language: 繁體中文。

## Pre-flight
1. Create `memory/evolver/` if not exists
2. Read last month's stats from `memory/evolver/` (if exists)
3. Note current month

---

## Phase 1: Scan Core Files

Read all core files and compute stats:

```python
# scan_cores.py logic
files = {
    "SOUL.md": "性格設定",
    "AGENTS.md": "啟動流程",
    "USER.md": "用戶理解",
    "MEMORY.md": "長期記憶",
    "RULES.md": "規則速查",
    "PERMANENT-RULES.md": "永久規則",
}

for file, label in files.items():
    lines = count_lines(file)
    growth = compare_with_last_month(file, lines)
    print(f"{label}: {lines} 行 (上月 {growth:+.1%})")
```

If total growth >20% → 🚨 mark as "增長過快" and add analysis.

---

## Phase 2: Cross-Reference with Vector Memory

Query vector memory for recent behavior patterns:

```
mem_search("近期工作方向 決策 偏好 習慣", limit=20)
mem_search("最近常用的技能和工作流程", limit=20)
```

Compare "what the files say" vs "what the agent actually does":
- Rules that are written but never followed
- Decisions that contradict recent behavior
- Personality traits that no longer match

---

## Phase 3: LLM Evaluation

For each core file, evaluate every significant entry (rules, decisions, personality traits, facts):

**Three dimensions:**

1. **方向一致性**: Does this align with recent behavior patterns and current work direction?
2. **衝突檢測**: Does this contradict newer rules in other files? Does it block progress?
3. **阻礙評估**: Is this an old restriction that no longer serves a purpose?

**Output for each flagged entry:**
```
[文件] [條目摘要]
  過時度: 高/中/低
  原因: [具體說明]
  建議: [保留/修改/移除]
```

---

## Phase 4: Generate Report

Format and send via Feishu message:

```
🧬 Agent 自我進化報告 — {月份}

📈 核心文件增長：
  SOUL.md:    {N} 行 ({growth})
  MEMORY.md:  {N} 行 ({growth})
  總計:       {N} 行 ({growth})
  {"⚠️ 增長過快！月增 >20%，可能原因：..." if triggered}

🕰️ 可能過時的內容：
  {for each flagged entry: number + summary + reason}

🔗 與當前方向衝突的決策：
  {conflicting decisions with explanation}

🧹 可清理的冗餘：
  {redundant entries}

💬 建議行動：
  {numbered, actionable suggestions}

回覆「執行 N」或描述你想如何重塑
```

Save full report to `memory/evolver/{YYYY-MM}.md`.

---

## Phase 5: Wait for Approval

Do NOT modify any core files. Wait for user to say "execute N".

---

## Safety Rules
- 🚫 NEVER auto-modify core files
- ✅ Always backup before modifying
- ✅ Verify line counts after modification
- ✅ Save all evolution records to memory/evolver/
