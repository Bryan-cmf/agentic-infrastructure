---
name: skill-compliance
description: 技能合規檢查 駁回機制 技能審計 合規審查 智能體守門 任務前檢查 任務後檢查 Skill compliance checker — spawns as an isolated sub-agent to verify whether all required skills were actually loaded. Outputs only PASS or REJECT with missing skills list. Zero LLM judgment — pure string matching.
---

# 🛡️ Skill Compliance Checker — 技能合規檢查器

## 概念

> **用 LLM 檢查 LLM 是同一種漏洞。這個技能用子代理隔離 + 機械字串比對來打破這個循環。**

Skill Compliance 是任務後的「門禁」——檢查 skill-router 推薦的技能是否全部被調用。它被 spawn 為獨立子代理，沒有上下文污染，只做一件事：比對兩個名單。

## 📥 一行安裝

```bash
mkdir -p skills/skill-compliance && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-compliance/SKILL.md -o skills/skill-compliance/SKILL.md
```

## 🔴 設計原則

1. **不做判斷，只做比對** — 不判斷技能是否「真的需要」，只看是否被調用
2. **子代理隔離** — 獨立 session，不受主 Agent 的自信偏差污染
3. **二值輸出** — 只有 PASS 或 REJECT，沒有「部分通過」
4. **全部強制** — skill-router 推薦的所有技能都是強制級，無例外

## 🚀 執行流程

### 方式一：平層內聯執行（推薦 · 零延遲）

在每次回覆末尾，內聯執行機械比對：

```
回覆前：skill-router → required_skills: [A, B, C]
回覆中：執行任務
回覆末：
  ① 列出本次實際調用的技能：[A, B]
  ② 對比：required vs actual
  ③ 輸出：✅ PASS 或 🔴 REJECT: [缺失技能]
```

### 方式二：子代理隔離（高風險任務 · 獨立驗證）

當任務涉及寫入/部署/外部操作時，可選用子代理模式：

```
主 Agent 完成任務
    │
    ▼
sessions_spawn("skill-compliance", context="isolated")
    │
    │  輸入：
    │  - required_skills: [idea-refine, spec-driven-development, ...]
    │  - actual_calls: [從對話記錄提取的 tool call / read 記錄]
    │
    │  邏輯：
    │  for each skill in required_skills:
    │      if skill not in actual_calls:
    │          missing.append(skill)
    │
    │  輸出：
    │  if missing is empty → "PASS"
    │  else → "REJECT: [missing skills]"
    │
    ▼
PASS → 任務完成 ✅
REJECT → 主 Agent 收到駁回通知 → 附缺失清單 → 強制重做
```

## 📋 內聯執行 Prompt

在回覆末尾，按以下格式執行：

```markdown
🛡️ Compliance:
  required: [skill-router, skill-compliance, ...]
  actual:   [skill-router, skill-compliance, ...]
  → ✅ PASS
```

如果缺失：

```markdown
🛡️ Compliance:
  required: [skill-router, skill-compliance, ...]
  actual:   [skill-router]
  → 🔴 REJECT: skill-compliance 未調用，強制重做
```

**規則：純字串比對。不做判斷。全部出現=PASS，任何缺失=REJECT。**

當 spawn skill-compliance 子代理時，使用以下 prompt：

```markdown
你是技能合規檢查器。你的唯一任務是進行機械字串比對。

## 輸入
- 強制技能清單：{required_skills}
- 實際調用清單：{actual_calls}

## 規則
1. 清單中的「每個」技能名稱，必須完整出現在實際調用清單中
2. 如果全部出現 → 輸出 "✅ PASS"
3. 如果有任何缺失 → 輸出 "🔴 REJECT"
4. 列出缺失的技能名稱

## 禁止
- 禁止判斷技能是否「真的需要」
- 禁止說「任務簡單所以不需要」
- 禁止說「雖然缺失但不影響結果」
- 禁止輸出任何 PASS/REJECT 以外的判斷
- 禁止討論任務內容

## 輸出格式
```
[PASS 或 REJECT]
[如果是 REJECT，列出缺失的技能名稱，一行一個]
```

現在執行。不要說任何其他話。
```

## 📊 使用方式

### 方式一：手動（用戶觸發）

在任務完成後說：
> 執行技能合規檢查

### 方式二：自動（集成到 agentic-infra）

agentic-infra Bootstrap 管線會自動在每個任務後 spawn skill-compliance。

### 方式三：常駐（與 skill-router 組成門禁對）

```
每次任務：
  任務前 → skill-router（路由 + 輸出強制技能清單）
  任務後 → skill-compliance（子代理比對 + 駁回/通過）
```

## 🔴 鐵律

- **必須用子代理 spawn**（context=isolated），不可內聯
- **只做字串比對**，不做語義判斷
- **只輸出 PASS 或 REJECT**，不輸出其他內容
- **全部強制**，無容忍度，無例外

## 🔗 與其他技能的關係

```
skill-router ──→ 輸出：強制技能清單
                       │
                       ▼
                  主 Agent 執行
                       │
                       ▼
skill-compliance ←── 子代理比對（字串匹配）
    │
    ├── PASS → 任務完成
    └── REJECT → 強制重做
```
