# 📋 Agentic Infrastructure — 一鍵一鍵初始化提示詞

> ⚠️ **v2 更新（2026-06-24）**：本文檔反映 v1 十件套結構。v2 已精簡為**七件套 + infra-enforcer 插件**：`skills-triggering`（併入 curator）、`skill-compliance` + `skill-reporting`（併入 infra-enforcer）已移除。本文檔中提及這三個技能的部分請以 [`README.md`](./README.md) 的 v2 結構為準。


> **每個方框都是一段提示詞。複製 → 貼給 Agent → 看結果 → 下一段。**
>
> **10 段跑完，你的 Agent 基礎建設就完成了。**

---

## 前置：安裝全部技能文件

```
請執行以下指令，下載全部 10 個技能文件：

mkdir -p skills/skills-triggering && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skills-triggering/SKILL.md -o skills/skills-triggering/SKILL.md
mkdir -p skills/skill-router && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-router/SKILL.md -o skills/skill-router/SKILL.md
mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md
mkdir -p skills/vector-memory && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/vector-memory/SKILL.md -o skills/vector-memory/SKILL.md
mkdir -p skills/skill-curator && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-curator/SKILL.md -o skills/skill-curator/SKILL.md
mkdir -p skills/agent-evolver && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-evolver/SKILL.md -o skills/agent-evolver/SKILL.md
mkdir -p skills/agent-previsor && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-previsor/SKILL.md -o skills/agent-previsor/SKILL.md
mkdir -p skills/agentic-infra && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agentic-infra/SKILL.md -o skills/agentic-infra/SKILL.md
mkdir -p skills/skill-compliance && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-compliance/SKILL.md -o skills/skill-compliance/SKILL.md
mkdir -p skills/infra-watchdog && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/infra-watchdog/SKILL.md -o skills/infra-watchdog/SKILL.md

安裝完成後，列出所有已安裝的技能目錄。
```

---

## 1️⃣ 技能健康掃描 + 中文關鍵詞注入

```
載入 skills/skill-curator/SKILL.md，執行技能庫健康掃描：

1. 列出 skills/ 目錄下所有技能
2. 對每個技能，檢查 SKILL.md 的 description 是否包含中文關鍵詞
3. 分類：🔴致命（無 description）| 🟡警告（缺中文關鍵詞）| 🟢健康
4. 對 🟡 的技能，推斷合適的中文關鍵詞，用 edit tool 注入
5. 輸出健康報告
```

---

## 2️⃣ 技能路由矩陣分類

```
載入 skills/skill-router/SKILL.md，將技能庫中所有技能分類：

1. 閱讀 SKILL.md 中的「4類×10階段」路由表
2. 把每個技能填入對應的類別和階段格子
3. 輸出路由矩陣
4. 計算覆蓋率
```

---

## 3️⃣ 部署技能合規檢查器（門禁對）

```
載入 skills/skill-compliance/SKILL.md，部署合規檢查器：

1. 理解合規檢查是「行為」而非「文件讀取」
2. 與 skill-router 組成門禁對：
   - 任務前：skill-router 路由 → 輸出強制技能清單
   - 任務後：skill-compliance 內聯檢查 → PASS/REJECT
3. 確認已理解，輸出「合規檢查器就緒」
```

---

## 4️⃣ 啟動向量記憶系統

```
載入 skills/vector-memory/SKILL.md，啟動向量記憶：

1. curl -s http://localhost:6333/healthz → 檢查 Qdrant
2. 如果 Qdrant 未運行，用 Docker 啟動
3. 檢查 collection 狀態
4. 輸出：記憶系統狀態報告
```

---

## 5️⃣ 啟動技能使用追蹤

```
載入 skills/skill-reporting/SKILL.md：

從現在開始，你的每次回覆末尾必須附帶：
> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）

現在就用這個格式回覆我，證明追蹤已啟動。
```

---

## 6️⃣ 設定自我進化排程

```
載入 skills/agent-evolver/SKILL.md：

1. 為我建立每月 1 號的自我進化排程
2. 檢查核心文件（AGENTS.md/RULES.md/SOUL.md/PERMANENT-RULES.md）是否有過時規則
3. 如果平台支援 cron，建立 cron job；否則建立記憶提醒
```

---

## 7️⃣ 規則持久化

```
將以下規則寫入我的啟動文件（CLAUDE.md 或 AGENTS.md 或 RULES.md）。
如果文件不存在就創建，如果已存在就追加到末尾：

# Agentic Infrastructure 常駐規則

## 每次回覆強制執行
1. 回覆前：載入 skill-router → 分類任務 → 輸出 required_skills
2. 回覆末：內聯執行 skill-compliance 檢查 → 輸出 PASS/REJECT
3. 回覆末：附帶技能使用信息（🛠️ 使用技能：...）

完成後確認寫入正確。
```

---

## 8️⃣ 設定定時巡查

```
載入 skills/infra-watchdog/SKILL.md：

1. 建立每週巡查排程（週一 09:00）
2. 立即執行第一次巡查，檢查全部 10 個技能
3. 輸出巡查報告
4. 不要自動修復——有問題只報告，讓我決定
```

---

## 9️⃣ 全面自查

```
對 Agentic Infrastructure 全部 10 個技能執行自查：

檢查每個技能的 SKILL.md 是否存在且內容完整：
- skills-triggering（技能觸發）
- skill-router（技能路由 · 常駐）
- skill-compliance（技能合規 · 常駐）
- skill-reporting（技能追蹤）
- vector-memory（向量記憶）
- skill-curator（技能策展）
- agent-evolver（自我進化）
- agent-previsor（事前預判）
- agentic-infra（統一入口）
- infra-watchdog（定時巡查）

輸出自查報告。
```

---

## 🔟 完成

```
Agentic Infrastructure 十件套全部初始化完成。

總結：
- 門禁對：skill-router（每任務前路由）+ skill-compliance（每任務後檢查）
- 記憶：vector-memory 持久化
- 追蹤：skill-reporting 記錄每次技能使用
- 維護：skill-curator 技能健康 + agent-evolver 月度進化
- 巡查：infra-watchdog 每週檢查一切正常
- 預判：agent-previsor 複雜任務前預判風險

一切就緒。現在你可以正常對話——基礎設施在後台自動運行。
```
