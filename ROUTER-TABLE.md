# 🔀 Router Table — Pre-Response Gate Engine

> **每條回覆第一步：查此表。這是門禁，不是建議。**
> 嵌入 AGENTS.md 開頭，始終在上下文，零額外讀取成本。

---

## 🔴 三步門禁（每條回覆強制）

```
Gate 1: CLASSIFY → 關鍵詞匹配 → 類別 × 階段
Gate 2: LOAD    → read 推薦專項技能 SKILL.md
Gate 3: COMPLY  → ═══ 線下報告加載了哪些技能 ═══
缺任一步 = REJECT（外部 cron 自動扣分）
```

---

## 🏗️ 基礎設施層（每條回覆必須真載入）

| 技能 | 載入方式 | 說明 |
|------|---------|------|
| `skill-router` | `read skills/skill-router/SKILL.md` | 查此路由表 |
| `skill-compliance` | `read skills/skill-compliance/SKILL.md` | 合規審計 |
| `skill-reporting` | ═══ footer 行 | 技能使用回報 |

---

## 🎯 專項技能層（查表 → 強制 read）

| 類別 | 階段 | 關鍵詞 | 強制載入 |
|------|------|--------|---------|
| 💻代碼 | 📋規劃 | 設計/架構/規劃/討論/方案 | `software-architect` `architecture-patterns` `idea-refine` |
| 💻代碼 | 💻開發 | 寫代碼/開發/實現/構建 | `karpathy-guidelines` `tdd` |
| 💻代碼 | 🧪診斷 | Bug/報錯/審查/審計/重構/排查 | `software-architect` `architecture-patterns` `agent-previsor` |
| 💻代碼 | 🚀部署 | 部署/上線/Vercel/push/git | `deploy-vercel` |
| 💰金融 | 🔍搜索 | 港股/股票/調研/DD/盡調 | `ak-hk-stock-dd` `tavily-search` |
| 💰金融 | 📊分析 | 估值/財務/DCF/報告/融資 | `ak-financial-analyst` `dd-business-report` |
| 🛠️日常 | 📋規劃 | 規劃/下一步/設計機制/方案 | `agent-previsor` `idea-refine` |
| 🛠️日常 | ⚙️維運 | 配置/修復/同步/檢查/排查 | `agent-previsor` |
| 🛠️日常 | 📊分析 | 報告/總結/審查/審計/匯報 | `agent-previsor` `software-architect` |
| 🛠️日常 | 💬通訊 | 打招呼/確認/OK/要/好/早 | (僅基礎設施層) |
| 🎨設計 | 🎨設計 | UI/網站/前端/PPT | `frontend-design` `design-taste-frontend` |
| 🎨設計 | 🔍審查 | UX審查/設計審查/用戶體驗 | `design-taste-frontend` `ui-ux-pro-max` |

---

## 📋 快速路由速查

| 用戶說 | 類別×階段 | 加載 |
|--------|----------|------|
| 早/早晨/hello/hi | 🛠️日常×💬通訊 | 基礎設施層 |
| 跟進/提醒/狀態 | 🛠️日常×📋規劃 | agent-previsor |
| 代碼/開發/網站 | 💻代碼×💻開發 | karpathy-guidelines tdd |
| Bug/報錯/審查 | 💻代碼×🧪診斷 | diagnose software-architect |
| 部署/上線/Vercel | 🛠️日常×🚀部署 | deploy-vercel |
| 港股/股票/調研 | 💰金融×🔍搜索 | ak-hk-stock-dd tavily-search |
| 估值/財務/DCF | 💰金融×📊分析 | ak-financial-analyst |
| 設計/UI/前端 | 🎨設計×🎨設計 | frontend-design design-taste-frontend |
| 配置/修復/排查 | 🛠️日常×⚙️維運 | agent-previsor |
| 審計/報告/總結 | 🛠️日常×📊分析 | agent-previsor software-architect |

---

## ⚠️ 紅旗（以下想法 = 你正在違規）

| 想 | 實際 |
|----|------|
| "這只是簡單回覆" | 簡單回覆也要 Gate 1-3 |
| "我記得路由表" | 必須查當前文件（技能可能更新） |
| "不需要 read 技能，我知道內容" | 沒有 read = 沒有加載 = REJECT |
| "先回覆再補加載" | 加載必須在回覆之前 |

---

_Last updated: 2026-06-15 | Pre-Response Gate Protocol v1.0_
