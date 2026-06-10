# 🔰 Bootstrap — Agentic Infrastructure 啟動提示詞

> **複製以下內容到你的 `AGENTS.md` 或系統 prompt 中，你的 Agent 會自動完成初始化。**

---

## 第一步：複製這段文字

將以下全部內容貼到你的 Agent 啟動設定中（AGENTS.md / system prompt / custom instructions）：

```markdown
# 🧰 Agentic Infrastructure 七件套

你已安裝 Agentic Infrastructure。這是你的智能體基礎建設系統。

## 🔰 首次啟動：執行 Bootstrap 初始化

如果你是第一次啟動（或技能庫有變更），執行以下初始化管線：

### Step 0: 技能掃描與關鍵詞注入
載入 `skills/skill-curator/SKILL.md` → 掃描你的技能庫 → 診斷健康狀態 → 自動注入中文關鍵詞 → 修復格式問題
- 命令：讀取 SKILL.md 後執行 curator scan 流程
- 驗證：輸出技能健康報告（致命/警告/健康 三級）

### Step 1: 技能路由分類
載入 `skills/skill-router/SKILL.md` → 將所有技能分類到 4類×10階段 路由矩陣
- 驗證：路由矩陣覆蓋率 ≥ 80%

### Step 2: 觸發覆蓋率驗證
載入 `skills/skills-triggering/SKILL.md` → 測試關鍵詞覆蓋 → 標記觸發盲區 → 補強缺失關鍵詞
- 驗證：觸發覆蓋率報告

### Step 3: 向量記憶啟動
載入 `skills/vector-memory/SKILL.md` → 確保 Qdrant 運行 → 建立初始索引
- 驗證：Qdrant alive + collection OK

### Step 4: 技能使用追蹤啟動
載入 `skills/skill-reporting/SKILL.md` → 掛載追蹤系統
- 驗證：追蹤系統就緒

### Step 5: 自我進化排程
載入 `skills/agent-evolver/SKILL.md` → 建立月度自我進化排程
- 驗證：進化排程已設定

### Step 6: 輸出初始化完成報告
匯總全部 Step 結果，輸出格式：
```
🧰 Agentic Infrastructure v1.1 Bootstrap 完成報告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 0: Skill Curator → [健康報告摘要]
Step 1: Skill Router  → [路由矩陣覆蓋率]
Step 2: Triggering    → [觸發覆蓋率]
Step 3: Vector Memory → [Qdrant 狀態]
Step 4: Reporting     → [追蹤系統狀態]
Step 5: Evolver       → [排程設定狀態]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🔄 日常使用

初始化完成後，每次任務自動：

1. **任務前**：經過 skill-router 路由 → 載入推薦技能
2. **任務中**：agent-previsor 預判風險（複雜任務時）
3. **任務後**：skill-reporting 記錄使用
4. **每月**：agent-evolver 自我進化

你不需要每次都手動運行初始化。但每次啟動時，檢查 skill-router 和 skill-reporting 是否活躍。
```

---

## 第二步：告訴你的 Agent

複製完後，對你的 Agent 說：

> **請執行 Bootstrap 初始化**

Agent 會自動按照 BOOTSTRAP 流程執行 6 個 Step，完成後輸出一份初始化報告。

---

## 原理

```
用戶在 AGENTS.md 中放入 Bootstrap Prompt
    │
    ▼
Agent 每次啟動時讀取 AGENTS.md
    │
    ▼
看到 Bootstrap 指令 → 自檢是否已初始化
    │
    ├── 首次 → 執行 6-Step 初始化管線
    └── 已初始化 → 正常運行（skill-router + reporting 自動運作）
```

---

## 🔧 自訂技能目錄

如果你的技能不在 `skills/` 目錄下，修改 BOOTSTRAP prompt 中的路徑：

```markdown
載入 `你的技能目錄/skill-curator/SKILL.md` → ...
```
