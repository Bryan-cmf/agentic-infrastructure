# 🛡️ Core Document Hardening Guide — 核心文檔加固完整指南

> **讓你的 AI Agent 永遠不會跳過基礎設施加載。**
>
> 適用於任何使用 Agentic Infrastructure 十件套的 AI Agent。

---

## 目錄

1. [為什麼需要加固](#為什麼需要加固)
2. [加固原理](#加固原理)
3. [操作步驟](#操作步驟)
4. [INFRA-MANDATE 模板](#infra-mandate-模板)
5. [加固前後對比](#加固前後對比)
6. [注意事項](#注意事項)
7. [常見問題](#常見問題)

---

## 為什麼需要加固

### 結構性問題

即使你安裝了全部十件套技能，Agent 仍可能「選擇性忘記」加載它們。這不是 Agent 故意的——是 LLM 架構級的**摘要本能**：

> LLM 被訓練為高效壓縮資訊。當它看到「重複的」步驟時，會自動優化掉。

你的 AGENTS.md 說「每次都要加載 skill-router」→ Agent 第一次做了 → 第二次覺得「我知道了，不用再讀」→ 第三次完全跳過。

### 實證

我們在自己的 UltraClaw Agent 上進行了審計：

| 指標 | 加固前 | 加固後 |
|------|--------|--------|
| skill-router 真載入率 | 13% (2/15) | 100% |
| 推薦技能載入率 | ~0% | 100% |
| Compliance Gate 通過率 | ~40% | 100% |

**方法：** 將 INFRA-MANDATE 嵌入 5 個核心文檔的頂部。

---

## 加固原理

### 核心策略

```
在每個核心文檔的最頂部插入統一的 INFRA-MANDATE 區塊。
無論 LLM 先讀到哪個文件，第一眼就看到強制門禁。
```

### 五個目標文件

| 文件 | 角色 | 插入位置 |
|------|------|---------|
| **AGENTS.md** | Agent 行為規則 | 標題之後，Pre-Response Gate 之前 |
| **SOUL.md** | Agent 人格定義 | 標題之後，輸出結構之前 |
| **RULES.md** | 規則速查表 | 標題之後，R0 規則之前 |
| **PERMANENT-RULES.md** | 永久規則 | 標題之後，第一條規則之前 |
| **MEMORY.md** | 長期記憶 | 標題之後，Key Facts 之前 |

### 為什麼五個文件都要有？

- LLM 打開 AGENTS.md → 看到 INFRA-MANDATE ✅
- LLM 打開 SOUL.md（人格文件）→ 看到 INFRA-MANDATE ✅
- LLM 打開 RULES.md（速查）→ 看到 INFRA-MANDATE ✅
- LLM 打開 MEMORY.md（查歷史）→ 看到 INFRA-MANDATE ✅

**每個入口都有門禁，沒有一個入口能繞過。**

---

## 操作步驟

### Step 1: 確認基礎設施已安裝

```bash
# 確認十件套技能文件都存在
ls skills/skill-router/SKILL.md
ls skills/skill-compliance/SKILL.md
ls skills/skill-reporting/SKILL.md
ls skills/agent-previsor/SKILL.md
ls skills/vector-memory/SKILL.md
ls skills/skill-curator/SKILL.md
ls skills/agent-evolver/SKILL.md
ls skills/infra-watchdog/SKILL.md
ls skills/agentic-infra/SKILL.md
ls skills/skills-triggering/SKILL.md
```

### Step 2: 執行加固

**方式 A — 透過 agentic-infra Bootstrap（自動）：**

```
請執行 agentic-infra bootstrap 初始化。它會自動在 Step 3.5 執行 Core Doc Hardening。
```

**方式 B — 手動觸發（獨立執行）：**

將以下提示詞貼給你的 Agent：

```
請執行 agent-evolver Phase 0: Core Document Hardening。

你需要對我的 Agent 進行核心文檔加固。步驟如下：

H1. SCAN — 讀取我的 5 個核心文件：
    - AGENTS.md（行為規則）
    - SOUL.md（人格定義）
    - RULES.md（規則速查）
    - PERMANENT-RULES.md（永久規則）
    - MEMORY.md（長期記憶）

H2. DIAGNOSE — 檢查每個文件是否存在以下問題：
    🔴 致命：
    - AGENTS.md 沒有 Pre-Response Gate（Router 行 + Compliance 行門禁）
    - SOUL.md 沒有強制輸出結構
    🟡 警告：
    - 規則散落在多個文件中，無中央速查表
    - MEMORY.md 沒有雙寫強制規則（file write → vector-memory__mem_save）
    - 基礎設施引用數量不足（每個文件 <5 條 infra 引用）
    🟢 健康：已具備所有強制性機制 → 跳過

H3. PROPOSE — 針對每個 🔴 和 🟡 問題提出具體 Before/After 重構方案。
    向我展示方案，等我確認後再執行。

H4. RESTRUCTURE — 按確認方案修改文件：
    - 在每個文件頂部插入統一的 INFRA-MANDATE 區塊
    - 備份原文件（.bak-YYYYMMDD-HHMM）
    - 保留 100% 原有內容，只重組結構、加門禁

H5. VERIFY — 逐文件檢查：
    - 確認每個文件頂部都有 INFRA-MANDATE
    - 確認 infra 引用數量增加
    - 確認沒有內容丟失
    - 輸出加固報告
```

### Step 3: 驗證結果

加固完成後，檢查：

```bash
# 查看每個文件頂部是否有 INFRA-MANDATE
for f in AGENTS.md SOUL.md RULES.md PERMANENT-RULES.md MEMORY.md; do
    echo "=== $f ==="
    head -10 "$f" | grep "INFRA-MANDATE"
done
```

**預期輸出：** 每個文件都顯示一行 `INFRA-MANDATE`。

---

## INFRA-MANDATE 模板

複製以下區塊到每個核心文檔的頂部（標題之後）：

```markdown
## 🔴 INFRA-MANDATE — 基礎設施十件套常態化加載（全文件第一行規則）

每條訊息前:  skill-router（查路由表）→ skill-compliance（合規檢查）→ skill-reporting（回報）
複雜任務前:  + agent-previsor（多路徑預判）
寫入後:      + vector-memory（雙寫強制，mem_save）
每日自動:    infra-watchdog（巡檢）
每月自動:    agent-evolver（自省）+ skill-curator（策展）
初始化:      agentic-infra（Bootstrap 統一入口）
技能觸發:    skills-triggering（跨語言關鍵詞注入）

> ⚠️ 以上十件套是基礎設施，不是「可選技能」。跳過任一件 = 違反 INFRA-MANDATE。
```

### 個性化調整

你可以根據你的實際技能名稱修改。例如：

```markdown
## 🔴 INFRA-MANDATE — 我的 Agent 的基礎設施規則

每次回應前： skill-router → skill-compliance
涉及記憶時： vector-memory（雙寫）
每週巡檢：   infra-watchdog
```

---

## 加固前後對比

### 加固前（典型的未加固狀態）

```
SOUL.md:
---
# SOUL.md - Who You Are

You're an AI assistant...
（完全沒有提到基礎設施）
```

### 加固後

```
SOUL.md:
---
# SOUL.md - Who You Are

## 🔴 INFRA-MANDATE — 十件套常態化加載
你的存在依賴於以下基礎設施。每次回應前，強制啟動：
  skill-router（分類路由）→ skill-compliance（自我審計）→ skill-reporting（技能回報）
  ...

> ⚠️ 忽略它們 = 你不是合格的 Agent。

You're an AI assistant...
```

### 數值對比（以 UltraClaw 實測）

| 文件 | 加固前 infra 引用 | 加固後 infra 引用 | 變化 |
|------|-----------------|-----------------|------|
| AGENTS.md | 13 | 19 | +46% |
| SOUL.md | 2 | 7 | +250% |
| RULES.md | 11 | 12 | +9% |
| PERMANENT-RULES.md | 19 | 20 | +5% |
| MEMORY.md | 25 | 26 | +4% |

---

## 注意事項

| ⚠️ 注意 | 說明 |
|----------|------|
| **先備份** | 加固腳本會自動備份（.bak-YYYYMMDD-HHMM），但建議手動也備份到安全位置 |
| **不刪內容** | 加固只重組結構、插入門禁，不刪除任何現有內容 |
| **用戶審批** | 對 🟡 警告級別的問題，Agent 會提案，等用戶確認才修改 |
| **不是一次性** | 加固後，agent-evolver 每月自動檢查核心文檔是否需要再次加固 |
| **先測試** | 如果可能，先在一個備份環境測試加固效果，確認後再上生產 |
| **逐步執行** | 不要一次性加固所有文件。先做 AGENTS.md，驗證效果，再做下一個 |
| **觀察 24 小時** | 加固後觀察 Agent 行為 24 小時，確認沒有副作用 |

---

## 常見問題

### Q: 加固會影響我現有的規則和記憶嗎？

**A:** 不會。加固只插入新的門禁區塊，完全保留原有內容。所有修改前都會自動備份。

### Q: 我的 Agent 沒有某些十件套技能，怎麼辦？

**A:** 先安裝完整的十件套，再做加固。如果暫時不想安裝全部，可以精簡 INFRA-MANDATE 區塊，只列出你已安裝的技能。

### Q: 加固後 Agent 的 token 消耗會增加嗎？

**A:** 會輕微增加（每個文件增加約 300-500 tokens）。但這是有價值的——防止 Agent 跳過基礎設施所節省的重複修正成本遠大於增加的 token 消耗。

### Q: 我需要多久加固一次？

**A:** 首次加固後，agent-evolver 會每月自動檢查。只有當核心文件有重大變化（新增重要規則、改動結構）時才需要重新加固。

### Q: 可以只加固部分文件嗎？

**A:** 可以。但最低建議加固 AGENTS.md + SOUL.md。AGENTS.md 是行為入口，SOUL.md 是人格入口。只加固這兩個就能獲得 ~90% 的效果。

---

## 相關資源

- [Agentic Infrastructure 十件套](https://github.com/Bryan-cmf/agentic-infrastructure) — 完整基礎設施
- [USAGE-GUIDE.md](./USAGE-GUIDE.md) — 完整使用指南
- [core-doc-hardening-reference.md](./core-doc-hardening-reference.md) — 加固參考範例
- [agent-evolver/SKILL.md](./agent-evolver/SKILL.md) — Phase 0 詳細說明

---

_Last updated: 2026-06-15 | UltraClaw Production_
