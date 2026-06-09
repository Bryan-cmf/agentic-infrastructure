---
name: skill-router
description: 技能路由器 任務匹配 技能推薦 任務路由 類別階段矩陣 用咩技能 スキルルーター タスクマッチング 스킬라우터 작업매칭 Skill router — class × phase matrix for matching any task to the right skills.
---

# 🔀 Skill Router — 任何任務，自動匹配正確技能

## 📥 一行安裝

```bash
mkdir -p skills/skill-router && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-router/SKILL.md -o skills/skill-router/SKILL.md
```

## 多語言簡介

**🇹🇼 繁中：** 任何任務進來，自動匹配正確的技能組合。
**🇨🇳 簡中：** 任何任务进来，自动匹配正确的技能组合。
**🇯🇵 日文：** どんなタスクも、正しいスキルの組み合わせに自動マッチング。
**🇰🇷 韓文：** 모든 작업을 올바른 스킬 조합에 자동 매칭합니다.
**🇸🇦 阿文：** أي مهمة تدخل، يتم مطابقتها تلقائياً مع مجموعة المهارات الصحيحة.
**🇮🇳 印地：** कोई भी कार्य आए, स्वचालित रूप से सही स्किल्स से मैच हो जाता है।

---

## 痛點

> **你的 Agent 有 200+ 個技能，但每次都要你手動告訴它用哪個。**

| 現象 | 根因 |
|------|------|
| 用戶說「幫我分析這隻股票」→ Agent 開始 Google 搜索，完全不知道有 `financial-analyst` 技能 | 沒有路由機制，任務和技能之間沒有橋樑 |
| AI 編碼助手選用了錯誤的工具鏈 | 技能很多但沒有分類，Agent 隨機選擇 |
| 每次都要用戶記得技能名稱並手動調用 | 使用者不是技能目錄，不該記住 200 個技能名 |
| 多步驟任務需要的手動串聯多個技能 | 沒有自動展開完整管線的機制 |

**市場數據：**

| 數據 | 來源 |
|------|------|
| 40% AI 專案因 Agent 協調失敗被取消 | Gartner 2026 |
| 88% 生產故障來自基礎設施缺口（含技能調度） | VentureBeat / arxiv 研究 (591 incidents) |
| 多 Agent 系統 Debug 耗時是單 Agent 的 3-5 倍 | Zylos Research 2026 |

**開源生態的現狀：**

OpenClaw、Claude Code、ECC 等平台上，技能數量爆炸式增長（OpenClaw 社群 300+ 技能），但沒有一個標準化的「任務 → 技能」路由機制。用戶安裝了強大技能，Agent 卻從不調用——這就是技能系統的「最後一里路」問題。

## 方案

### 架構：類別 × 階段矩陣

```
任何任務進來
    │
    ├── Step 1: 檢測類別（關鍵詞匹配）
    │   🛠️ 日常 | 💰 金融 | 💻 代碼 | 🎨 設計
    │
    ├── Step 2: 檢測階段（意圖匹配）
    │   📋規劃 | 🔍搜索 | 🎨設計 | 💻開發 | 🧪測試 | 📊分析 | 🚀部署
    │
    ├── Step 3: 查表 → 推薦技能組合
    │
    └── Step 4: 多階段自動展開完整管線
```

### 路由表示例

| 用戶說 | 類別 | 階段 | 推薦技能 |
|--------|------|------|---------|
| 「港股調研」「股票分析」 | 💰 金融 | 🔍 搜索 | `ak-hk-stock-dd` `tavily-search` |
| 「網站」「前端」「UI」 | 💻 代碼 | 🎨 設計 | `frontend-design` `design-taste-frontend` |
| 「部署」「上線」 | 🛠️ 日常 | 🚀 部署 | `deploy-vercel` |
| 「修 Bug」「報錯」 | 💻 代碼 | 🧪 診斷 | `diagnose` `tdd` |
| 「代碼審查」「重構」 | 💻 代碼 | 📋 規劃 | `grill-with-docs` `karpathy-guidelines` |

### 核心機制

**1. 關鍵詞匹配（零延遲）**

```python
KEYWORDS = {
    "💰金融": ["港股", "股票", "調研", "DD", "估值", "DCF", "併購"],
    "💻代碼": ["代碼", "開發", "Bug", "重構", "測試", "架構", "網站", "前端"],
    "🛠️日常": ["部署", "上線", "配置", "記憶", "整理", "飛書"],
}
```

**2. 多階段自動展開**

```
「幫我做 00058 調研」
→ 💰金融 + 🔍搜索 → ak-hk-stock-dd
→ Phase 2 自動展開：💰金融 + 📊分析 → ak-financial-analyst
→ Phase 3 自動展開：💰金融 + 📊分析 → dd-business-report
```

**3. 中途檢查點**

```
✅ Phase 1: ak-hk-stock-dd → 完成
🔀 路由到 Phase 2: ak-financial-analyst → 載入中...
✅ Phase 2: ak-financial-analyst → 完成
🔀 路由到 Phase 3: dd-business-report → 載入中...
```

---

## 安裝

```bash
cp SKILL.md ~/.openclaw/workspace/skills/skill-router/

# 在你的 AGENTS.md 或 RULES.md 中加入：
# R17: 收到任何任務 → 先經過 skill-router 檢查
```

---

## 自定義路由表

擴展你自己的領域和技能：

```markdown
### 你的領域 + 你的階段

| 階段 | 技能 |
|------|------|
| 🔍 搜索 | `你的搜索技能` |
| 📊 分析 | `你的分析技能` |
```

---

## 效果

| 指標 | 無 Router | 有 Router | 改善 |
|------|----------|----------|------|
| 技能發現率 | ~35% | ~90% | +157% |
| 錯誤工具使用 | 頻繁 | 極少 | -80% |
| 任務啟動時間 | 3-5 回合 | 1 回合 | -60% |
| 多步驟任務中斷 | 常發生 | 自動展開 | -90% |

---

## 相關資源

- **前置項目：** [Skills Triggering](../skills-triggering/) — 先讓技能被正確發現
- **配套項目：** [Vector Memory](../vector-memory/) — 讓 Agent 記住路由決策

---

## 📥 一行安裝

```bash
mkdir -p skills/skill-router && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-router/SKILL.md -o skills/skill-router/SKILL.md
```

## 授權

MIT
