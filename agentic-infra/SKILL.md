---
name: agentic-infra
description: Agent基礎建設 智能體基礎設施 技能管理 記憶系統 技能觸發 技能路由 自我進化 事前預判 bootstrap 初始化 infra infrastructure agent-toolkit 系統優化 技能初始化 啟動設定 agentic-infrastructure — Unified entry skill that bootstraps and orchestrates all 7 Agentic Infrastructure sub-skills. Triggers on "bootstrap", "初始化", "infra", "基礎建設", "啟動基礎設施".
---

# 🧰 Agentic Infra — Agentic Infrastructure 統一入口

## 概念

> 七個技能各自獨立。這個技能把它們串成一條完整管線。

Agentic Infra 是十件套的統一入口——編排層。當它被觸發時，自動按正確順序加載和執行子技能。

## 📥 一行安裝

```bash
mkdir -p skills/agentic-infra && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agentic-infra/SKILL.md -o skills/agentic-infra/SKILL.md
```

## 觸發方式

| 方式 | 說明 |
|------|------|
| 手動 | `bootstrap`、`初始化`、`基礎建設`、`infra`、`啟動基礎設施` |
| 自動 | 首次安裝後，Agent 讀取 BOOTSTRAP.md → 自動觸發初始化管線 |

## 🚀 Bootstrap 執行流程

當此技能被觸發時，按以下順序強制執行（不可跳步）。

**每個 Step 有兩條路徑：A（腳本優先）→ 失敗則走 B（LLM 原生，永遠可用）。**

```
🧰 Agentic Infra Bootstrap Pipeline
│
├── Step 0: Skill Curator 掃描
│   ├── 路徑A：執行 scan_all.py（如可用）
│   ├── 路徑B：LLM 原生掃描（讀 description → 檢查中英關鍵詞 → 注入）
│   ├── 診斷：致命/警告/健康 三級
│   └── 輸出：健康報告摘要
│
├── Step 1: Skill Router 分類
│   ├── LLM 原生（不需腳本）：讀 SKILL.md → 按路由表分類
│   ├── 將所有技能分類到 4類×10階段 路由矩陣
│   └── 輸出：路由矩陣覆蓋率
│
├── Step 2: Skill Compliance 部署 🆕
│   ├── 檢查平台是否支援子代理 spawn
│   ├── 支援 → 子代理模式 / 不支援 → 內聯檢查模式
│   └── 輸出：合規檢查器就緒
│
├── Step 3: Skills Triggering 驗證
│   ├── 路徑A：執行 skills-triggering.py（如可用）
│   ├── 路徑B：LLM 原生（構造測試句子 → 檢查觸發）
│   └── 輸出：觸發覆蓋率報告
│
├── Step 4: Vector Memory 啟動
│   ├── 載入 skills/vector-memory/SKILL.md
│   ├── 檢查 Qdrant 是否運行
│   ├── 若無 → 嘗試啟動
│   └── 輸出：記憶系統健康狀態
│
├── Step 5: Skill Reporting 掛載
│   ├── 載入 skills/skill-reporting/SKILL.md
│   ├── 確保每次回覆附帶技能使用信息
│   └── 輸出：追蹤系統就緒
│
├── Step 6: Agent Evolver 排程
│   ├── 載入 skills/agent-evolver/SKILL.md
│   ├── 建立月度自我進化排程
│   └── 輸出：進化排程已設定
│
└── Step 7: 輸出初始化報告
    └── 格式：
        🧰 Agentic Infrastructure Bootstrap 完成
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Curator:      [N] 致命 [N] 警告 [N] 健康
        Router:       覆蓋率 XX%
        Compliance:   就緒 ✅
        Triggering:   覆蓋率 XX%
        Memory:       [狀態]
        Reporting:    [狀態]
        Evolver:      [狀態]
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🔴 鐵律

- **啟動時必須按順序執行 6 個 Step，不可跳步**
- **每個 Step 必須載入對應 SKILL.md（用 read tool 或等效機制）**
- **每個 Step 完成後必須輸出驗證結果**
- **Step 6 必須產出匯總報告**

## 🔄 日常使用（Bootstrap 後）

Bootstrap 完成後，Agent 在日常運作中自動：

```
每次任務：
  ① skill-router → 路由分類 + 輸出強制技能清單（任務前）
  ② agent-previsor → 複雜任務時預判風險
  ③ skill-compliance → 子代理合規檢查（任務後）🆕
  ④ skill-reporting → 記錄技能使用

每月：
  ⑤ agent-evolver → 自我進化檢查
```

**skill-router + skill-compliance 是兩個常駐技能，組成任務前後的門禁對。**

---

## 與子技能的關係

```
agentic-infra (第八技能 · 統一入口)
    │
    ├── Step 0 → skill-curator     (策展人)
    ├── Step 1 → skill-router      (路由器 · 常駐)
    ├── Step 2 → skill-compliance  (合規器 · 常駐) 🆕
    ├── Step 3 → skills-triggering (觸發器)
    ├── Step 4 → vector-memory     (記憶庫)
    ├── Step 5 → skill-reporting   (記錄器)
    └── Step 6 → agent-evolver     (進化者)

agent-previsor → 不屬於初始化管線，日常任務時獨立調用

skill-router + skill-compliance = 門禁對（Pre-Gate + Post-Gate）
```
