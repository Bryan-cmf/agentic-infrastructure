# 🚀 Agentic Infrastructure — 逐步安裝指南

> **照著以下步驟，每一步複製一段提示詞貼給你的 Agent。它會執行、回報結果，你再進行下一步。**

---

## 前置：安裝全部技能文件

複製這一段給你的 Agent，一次性下載全部技能：

```
請執行以下安裝指令：

mkdir -p skills/agentic-infra && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agentic-infra/SKILL.md -o skills/agentic-infra/SKILL.md
mkdir -p skills/skills-triggering && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skills-triggering/SKILL.md -o skills/skills-triggering/SKILL.md
mkdir -p skills/skill-router && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-router/SKILL.md -o skills/skill-router/SKILL.md
mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md
mkdir -p skills/vector-memory && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/vector-memory/SKILL.md -o skills/vector-memory/SKILL.md
mkdir -p skills/skill-curator && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-curator/SKILL.md -o skills/skill-curator/SKILL.md
mkdir -p skills/agent-evolver && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-evolver/SKILL.md -o skills/agent-evolver/SKILL.md
mkdir -p skills/agent-previsor && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-previsor/SKILL.md -o skills/agent-previsor/SKILL.md
mkdir -p skills/skill-compliance && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-compliance/SKILL.md -o skills/skill-compliance/SKILL.md

安裝完成後，列出已安裝的技能文件，確認全部 9 個都存在。
```

**看到 9 個文件都確認存在後，繼續下一步。**

---

## 第 1 步：技能健康掃描

```
載入 skills/skill-curator/SKILL.md，執行技能庫健康掃描：

1. 列出 skills/ 目錄下所有技能
2. 對每個技能，檢查 SKILL.md 的 description 欄位是否有中文關鍵詞
3. 分類：🔴致命（description 為空或嚴重損壞）| 🟡警告（缺中文關鍵詞）| 🟢健康
4. 對 🟡 的技能，根據其功能推斷合適的中文關鍵詞，用 edit tool 注入到 description 中
5. 輸出健康報告：
   - 總技能數
   - 🔴致命 N 個（列出）
   - 🟡警告 N 個（列出 + 已修復）
   - 🟢健康 N 個
```

**確認報告中 🟡 的技能都已修復後，繼續下一步。**

---

## 第 2 步：技能路由分類

```
載入 skills/skill-router/SKILL.md，將技能庫中的所有技能分類到路由矩陣：

1. 閱讀 SKILL.md 中的「4類×10階段路由表」
2. 把每個技能填入對應的類別和階段格子
3. 輸出路由矩陣（表格格式）
4. 計算覆蓋率：有技能覆蓋的格子數 ÷ 總格子數
```

**確認覆蓋率報告後，繼續下一步。**

---

## 第 3 步：部署技能合規檢查器

```
載入 skills/skill-compliance/SKILL.md，部署合規檢查器：

1. 閱讀 SKILL.md，了解內聯合規檢查的機制
2. 確認理解：每次回覆末尾，比對 required_skills 和 actual_calls
3. 與 skill-router 組成門禁對：
   - 任務前：skill-router 路由 → 輸出強制技能清單
   - 任務後：skill-compliance 內聯檢查 → PASS/REJECT
4. 輸出：合規檢查器部署完成
```

---

## 第 4 步：啟動向量記憶系統

```
載入 skills/vector-memory/SKILL.md，啟動向量記憶：

1. 檢查 Qdrant 是否運行：curl -s http://localhost:6333/healthz
2. 如果未運行：
   - 如果有 Docker：docker run -d -p 6333:6333 qdrant/qdrant
   - 如果沒有 Docker：標記為「需要手動安裝 Qdrant」
3. 檢查 collection 是否存在
4. 輸出：記憶系統狀態
```

---

## 第 5 步：啟動技能使用追蹤

```
載入 skills/skill-reporting/SKILL.md，啟動追蹤：

從現在開始，你的每一次回覆末尾必須附帶：
> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）

現在就用這個格式回覆我，證明你已啟動追蹤。
```

---

## 第 6 步：設定自我進化排程

```
載入 skills/agent-evolver/SKILL.md，建立進化排程：

1. 檢查你的平台是否支援定時任務（cron / scheduler）
2. 如果支援 → 建立每月 1 號的自我進化檢查
3. 如果不支援 → 建立一個記憶提醒，每月提醒執行
4. 輸出：排程狀態
```

---

## 第 7 步：規則持久化

```
將以下規則寫入你的啟動文件（CLAUDE.md / AGENTS.md / RULES.md / 系統 prompt）：

如果啟動文件不存在，創建它。如果已存在且有舊規則，追加到末尾。

要寫入的規則：

# Agentic Infrastructure 常駐規則

## 每次回覆強制執行
1. 回覆前：載入 skill-router → 分類任務 → 輸出 required_skills
2. 回覆末：內聯執行 skill-compliance 檢查 → 輸出 PASS/REJECT
3. 回覆末：附帶技能使用信息（格式：> 🛠️ 使用技能：...）

完成後，確認啟動文件內容正確。
```

---

## 第 8 步：全面自查

```
執行 Agentic Infrastructure 全面自查：

對以下每個技能，檢查 SKILL.md 是否存在且內容完整：
- agentic-infra（統一入口）
- skill-router（技能路由 · 常駐）
- skill-compliance（技能合規 · 常駐）
- vector-memory（向量記憶）
- skills-triggering（技能觸發）
- skill-curator（技能策展）
- skill-reporting（技能追蹤）
- agent-evolver（自我進化）
- agent-previsor（事前預判）

輸出自查報告：
✅ 全部通過 或 ❌ 列出缺失項目
```

---

## ✅ 完成

全部 8 步完成後，你的 Agent 基礎建設已就緒。每次任務都會自動經過門禁對（skill-router + skill-compliance），技能使用會被追蹤，記憶會被持久化。

**日常使用只需正常對話——基礎設施在後台自動運行。**

---

## 第 9 步（建議）：設定定時巡查

基礎設施不是裝完就沒事了。設定每週巡查，讓 Agent 定期檢查一切是否正常：

```
載入 skills/infra-watchdog/SKILL.md，為我建立一個每週巡查排程：

1. 頻率：每週一 09:00
2. 檢查全部 9 個基礎設施技能的健康狀態
3. 有退化就報告，附修復建議（引用 STEP-BY-STEP 對應步驟）
4. 不要自動修復，讓我自己決定

現在執行第一次巡查，讓我看巡查報告的格式。
```
