---
name: agentic-infra
description: Agent基礎建設 智能體基礎設施 技能管理 記憶系統 技能路由 自我進化 事前預判 bootstrap 初始化 infra infrastructure agent-toolkit 系統優化 技能初始化 啟動設定 agentic-infrastructure — Unified entry skill that bootstraps and orchestrates the 7-piece Agentic Infrastructure suite. Triggers on "bootstrap", "初始化", "infra", "基礎建設", "啟動基礎設施".
---

# 🧰 Agentic Infra — Agentic Infrastructure 統一入口（7 件套 v2）

## 概念

> 七件套各自獨立。這個技能把它們串成一條完整管線。
> v2（2026-06-24）：精簡自十件套——skills-triggering（被 curator 覆蓋）、
> skill-compliance + skill-reporting（被 infra-enforcer 插件取代）已移除。

Agentic Infra 是七件套的統一入口——編排層。當它被觸發時，自動按正確順序加載和執行子技能。

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
🧰 Agentic Infra Bootstrap Pipeline（7 件套）
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
├── Step 2: Core Document Hardening（核心文檔加固）
│   ├── 由 agent-evolver Phase 0 執行
│   ├── 掃描 AGENTS.md / RULES.md / SOUL.md / PERMANENT-RULES.md / MEMORY.md
│   ├── 診斷：致命（缺門禁）/ 警告（散落規則）/ 健康（已完備）
│   ├── 對 🔴 問題自動加固（嵌入路由器表、門禁、雙寫規則）
│   ├── 對 🟡 問題提案 → 等用戶確認 → 執行
│   └── 輸出：加固報告（8 項檢查清單）
│
├── Step 3: Vector Memory 啟動
│   ├── 載入 skills/vector-memory/SKILL.md
│   ├── 檢查 Qdrant 是否運行
│   ├── 若無 → 嘗試啟動
│   └── 輸出：記憶系統健康狀態
│
├── Step 4: Agent Evolver 排程
│   ├── Phase 0 已在 Step 2 完成（核心文檔加固）
│   ├── 建立 Phase 1+ 月度自我進化排程（cron）
│   └── 輸出：進化排程已設定（月度 + 增長觸發）
│
└── Step 5: 輸出初始化報告
    └── 格式：
        🧰 Agentic Infrastructure Bootstrap 完成（7 件套）
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        Curator:      [N] 致命 [N] 警告 [N] 健康
        Router:       覆蓋率 XX%
        Hardening:    [N] 致命加固 [N] 警告提案
        Memory:       健康 ✅
        Evolver:      月度排程已設定 ✅
        Enforcer:     插件已啟用（合規/評分/擋截由它負責）
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🔴 鐵律

- **啟動時必須按順序執行 5 個 Step，不可跳步**
- **每個 Step 必須載入對應 SKILL.md（用 read tool 或等效機制）**
- **每個 Step 完成後必須輸出驗證結果**
- **Step 5 必須產出匯總報告**

## 🔄 日常使用（Bootstrap 後）

Bootstrap 完成後，Agent 在日常運作中自動：

```
每次任務：
  ① skill-router → 路由分類 + 輸出強制技能清單（任務前）
  ② agent-previsor → 複雜任務時預判風險
  ③ infra-enforcer（插件）→ 程式評分 + revise 重做 + audit 紀錄（任務後，自動）

每月：
  ④ agent-evolver → 自我進化檢查（cron 自動觸發）
```

> **合規與匯報不再由技能負責**——`infra-enforcer` 插件（gateway hook）
> 自動在每次回合評分、寫 audit.jsonl、必要時推 IM 通知、score 歸零時 block。
> 模型不需手動「打 🛠️」或「自評」，enforcer 讀真實 toolCall 紀錄判定。

## 與子技能的關係（7 件套 + 1 插件）

```
agentic-infra (編排層 · 統一入口)
    │
    ├── Step 0 → skill-curator     (策展人 · 掃描+注入+去重)
    ├── Step 1 → skill-router      (路由器 · 常駐)
    ├── Step 2 → agent-evolver     (進化者 · 核心文檔加固 Phase 0)
    ├── Step 3 → vector-memory     (記憶庫 · Qdrant)
    └── Step 4 → agent-evolver     (進化者 · 月度排程)

agent-previsor → 不屬於初始化管線，日常任務時獨立調用
infra-watchdog → 定期巡查（每周），獨立調用

infra-enforcer（gateway 插件，非技能）→
    全權負責：合規評分 + audit 紀錄 + revise 重做 + score 擋截 + IM 通知
    + 每回合注入技能清單/路由表/規則到 system prompt
```

## 📋 v2 精簡說明（為什麼從 10 件變 7 件）

| 被移除 | 原因 | 功能由誰接手 |
|--------|------|-------------|
| skills-triggering | skill-curator 的嚴格子集（掃描+注入關鍵詞 curator 全包） | skill-curator |
| skill-compliance | 模型自評會作弊；enforcer 程式評分更可靠 | infra-enforcer |
| skill-reporting | 🛠️ 文字匯報可被偽造；enforcer 的 audit.jsonl 不可作弊 | infra-enforcer |
