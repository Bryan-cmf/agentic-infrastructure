# Core Doc Hardening Reference — INFRA-MANDATE Pattern

> **agent-evolver Phase 0 執行結果範例**
> 
> 此文件展示如何將基礎設施十件套的強制性加載提示嵌入每一個核心文檔。
> 策略：在所有核心文檔的最頂部插入統一的 INFRA-MANDATE 區塊。

## 加固前 vs 後

| 文件 | 加固前 infra 引用 | 加固後 infra 引用 | 強制標記 |
|------|-----------------|-----------------|---------|
| AGENTS.md | 13 | 19 | ✅ INFRA-MANDATE |
| SOUL.md | 2 | 7 | ✅ INFRA-MANDATE |
| RULES.md | 11 | 12 | ✅ INFRA-MANDATE |
| PERMANENT-RULES.md | 19 | 20 | ✅ INFRA-MANDATE |
| MEMORY.md | 25 | 26 | ✅ INFRA-MANDATE |

## INFRA-MANDATE 模板

```markdown
## 🔴 INFRA-MANDATE — 基礎設施十件套常態化加載（全文件第一行規則）

每條訊息前: skill-router（查路由表）→ skill-compliance（合規檢查）→ skill-reporting（回報）
複雜任務前: + agent-previsor（多路徑預判）
寫入後:     + vector-memory（雙寫強制，mem_save）
每日自動:   infra-watchdog（巡檢）
每月自動:   agent-evolver（自省）+ skill-curator（策展）
初始化:     agentic-infra（Bootstrap 統一入口）
技能觸發:   skills-triggering（跨語言關鍵詞注入）

⚠️ 以上十件套是基礎設施，不是「可選技能」。跳過任一件 = 違反 INFRA-MANDATE。
```

## 設計原則

1. **每個核心文檔頂部都有** — 無論 LLM 先讀到哪個文件，第一眼就看到
2. **不可跳過的語氣** — "INFRA-MANDATE"，不是 "建議"、"可選"
3. **具體的技能名稱** — 不是抽象描述，是實際的工具/技能名
4. **觸發場景明確** — 每條訊息/複雜任務/寫入後/每日/每月

## agent-evolver Phase 0 觸發

```
agentic-infra bootstrap
  → Step 3: Skills Triggering
  → Step 3.5: agent-evolver Phase 0「Core Doc Hardening」
      ├── SCAN 5 核心文件
      ├── DIAGNOSE 致命/警告/健康
      ├── PROPOSE INFRA-MANDATE 插入方案
      ├── RESTRUCTURE（用戶確認後）
      └── VERIFY
  → Step 4: Vector Memory
```
