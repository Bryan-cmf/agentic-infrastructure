# 🧰 Agentic Infrastructure — Agent 基礎建設七件套 + Enforcer

> **七個獨立技能 + 一個 gateway 插件，解決 AI Agent 生態系統的結構性問題。**
>
> **Seven standalone skills + one gateway plugin solving structural problems in the AI agent ecosystem.**

> **v2（2026-06-24）**：精簡自十件套。`skills-triggering`（被 curator 覆蓋）、
> `skill-compliance` + `skill-reporting`（被 `infra-enforcer` 插件取代）已移除。
> 合規評分、匯報、技能觸發三項收斂到單一可靠的程式入口，不再靠模型自評。

---

## 🚀 快速開始 · Quick Start

### 👉 一鍵一鍵初始化：打開 [`INIT-PROMPTS.md`](./INIT-PROMPTS.md)

### 或：一次性安裝七件套技能

複製以下整段給你的 Agent：

```
請執行以下安裝指令：

mkdir -p skills/skill-router && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-router/SKILL.md -o skills/skill-router/SKILL.md
mkdir -p skills/skill-curator && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-curator/SKILL.md -o skills/skill-curator/SKILL.md
mkdir -p skills/agent-evolver && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-evolver/SKILL.md -o skills/agent-evolver/SKILL.md
mkdir -p skills/agent-previsor && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-previsor/SKILL.md -o skills/agent-previsor/SKILL.md
mkdir -p skills/agentic-infra && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agentic-infra/SKILL.md -o skills/agentic-infra/SKILL.md
mkdir -p skills/infra-watchdog && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/infra-watchdog/SKILL.md -o skills/infra-watchdog/SKILL.md
mkdir -p skills/vector-memory && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/vector-memory/SKILL.md -o skills/vector-memory/SKILL.md

安裝完成後列出所有已安裝的技能。
```

### 🔧 安裝 infra-enforcer 插件（OpenClaw gateway）

enforcer 是 gateway 插件，提供程式級合規評分、revise 重試、audit 紀錄、IM 推送、score 擋截。
技能安裝後，把 `infra-enforcer/` 目錄加入 OpenClaw 的 `plugins.load.paths`，並在 `plugins.entries` 設
`allowConversationAccess: true`（詳見 [`infra-enforcer/README.md`](./infra-enforcer/)）。

然後打開 [`INIT-PROMPTS.md`](./INIT-PROMPTS.md)，從第 1 步開始，一段一段貼。

---

## 🎯 痛點 · 方案（七件套 + Enforcer）

| # | 痛點 | 方案 | 一句話 |
|---|------|------|--------|
| 🧰 | 技能各自獨立，缺少統一入口 | **Agentic Infra** | 一鍵 Bootstrap 初始化。安裝→啟動→完成 |
| 🩺 | 裝完就忘了，不知道技能還能不能用 | **Infra Watchdog** | 每週定時巡查，報告退化，不自動修復 |
| 🔀 | 技能太多，不知道該用哪個 | **Skill Router** | 類別×階段矩陣自動路由 |
| 🛡️ | Agent 知道要用技能但會跳過、會作弊 | **Infra Enforcer**（插件） | 程式核對真實 toolCall，revise 重做 + score 擋截 + audit 紀錄 |
| 🧠 | 重啟後完全失憶，從零開始 | **Vector Memory** | Qdrant+BGE-m3 持久化 |
| 🎨 | 技能越裝越多，越來越亂 | **Skill Curator** | 掃描→診斷→調適（含 CJK 關鍵詞注入） |
| 🧬 | 核心文件臃腫，舊規則過時 | **Agent Evolver** | 月度自省，識別過時內容 |
| 🔮 | 每次都在事後才發現問題 | **Agent Previsor** | Pre-mortem 多路徑預判。動手之前預見所有坑 |

> **v2 變更**：合規（舊 skill-compliance）、匯報（舊 skill-reporting）、
> 觸發詞注入（舊 skills-triggering）三項已收斂到 `infra-enforcer` 插件 +
> `skill-curator`，不再作為獨立技能。原因：模型自評會作弊、文字匯報可偽造、
> 關鍵詞注入是 curator 的子功能。詳見各被移除技能的 `agentic-infra/SKILL.md` v2 說明。

---

## 🇹🇼🇨🇳 中文

| # | 痛點 · Pain Point | 技能 · Skill | 解決方案 · Solution |
|---|------|------|------|
| 0 | 技能各自獨立，缺少統一入口和初始化管線 — 用戶安裝後不知道下一步 | 🧰 Agentic Infra | 一鍵 Bootstrap 五步初始化管線：掃描→路由→加固→記憶→進化 |
| 1 | Agent 有技能但不知道用哪個 — 40% AI 專案因協調失敗被取消 | 🔀 Skill Router | 類別×階段矩陣路由，多階段自動展開完整管線 |
| 2 | Agent 知道要用技能但會跳過、會作弊 — 模型自評不可靠 | 🛡️ Infra Enforcer（插件） | 程式核對真實 toolCall 紀錄，revise 重做 + score 擋截 + audit 紀錄 |
| 3 | Agent 重啟後完全失憶 — 狀態失憶是 #1 生產殺手 | 🧠 Vector Memory | Qdrant+BGE-m3，四層記憶架構，中文搜尋 >78% |
| 4 | 技能越裝越多越來越亂 — 125 技能僅 51% 健康 | 🎨 Skill Curator | 六階段全生命週期：掃描→診斷→調適（含 CJK 關鍵詞注入）→場景→報告→執行 |
| 5 | 核心文件越來越臃腫，舊規則過時 | 🧬 Agent Evolver | 月度自省，三維度評估（方向一致性/衝突檢測/阻礙評估） |
| 6 | 每次都在事後才發現問題 | 🔮 Agent Previsor | Pre-mortem 多情境路徑預判，事前識別瓶頸/踩坑/浪費 |

---

## 🇯🇵 日本語

| # | 痛点 · Pain Point | スキル · Skill | 解決策 · Solution |
|---|------|------|------|
| 0 | スキルがバラバラで統一入り口がない | 🧰 Agentic Infra | ワンクリックBootstrap 5ステップ初期化パイプライン |
| 1 | スキルが多すぎてどれを使うか分からない | 🔀 Skill Router | クラス×フェーズマトリックス自動ルーティング |
| 2 | スキルを使うと分かってるのに飛ばす、ズルする | 🛡️ Infra Enforcer（プラグイン） | 実際のtoolCall記録を照合、revise再実行 + scoreブロック + audit記録 |
| 3 | 再起動のたびに完全に記憶喪失 | 🧠 Vector Memory | Qdrant+BGE-m3、4層メモリアーキテクチャ |
| 4 | スキルが増えすぎて管理不能 | 🎨 Skill Curator | 6フェーズ管理：スキャン→診断→適応（CJKキーワード注入含む）→シナリオ→報告→実行 |
| 5 | コアファイルが肥大化、古いルールが残る | 🧬 Agent Evolver | 毎月の自己内省、3次元評価（方向性/衝突/阻害） |
| 6 | 実行後に初めて問題に気づく | 🔮 Agent Previsor | Pre-mortemマルチパス予測、事前に全リスクを特定 |

---

## 🇰🇷 한국어

| # | 문제 · Pain Point | 스킬 · Skill | 해결책 · Solution |
|---|------|------|------|
| 0 | 스킬이 각각 분리되어 통합 진입점 부재 | 🧰 Agentic Infra | 원클릭 Bootstrap 5단계 초기화 파이프라인 |
| 1 | 스킬이 너무 많아 어떤 것을 쓸지 모름 | 🔀 Skill Router | 클래스×페이즈 매트릭스 자동 라우팅 |
| 2 | 스킬을 쓴다고 알면서도 건너뛰거나 속임 | 🛡️ Infra Enforcer（플러그인） | 실제 toolCall 기록 대조, revise 재실행 + score 차단 + audit |
| 3 | 재시작할 때마다 완전히 기억 상실 | 🧠 Vector Memory | Qdrant+BGE-m3, 4계층 메모리 아키텍처 |
| 4 | 스킬이 너무 많아 관리 불가 | 🎨 Skill Curator | 6단계 관리: 스캔→진단→적응(CJK 키워드 주입 포함)→시나리오→보고→실행 |
| 5 | 코어 파일 비대, 오래된 규칙 잔존 | 🧬 Agent Evolver | 월간 자기성찰, 3차원 평가(방향성/충돌/장애) |
| 6 | 실행 후에야 문제를 발견 | 🔮 Agent Previsor | Pre-mortem 다중 경로 예측, 사전 위험 식별 |

---

## 🏗️ 架構 · Architecture

```
🧰 Agentic Infra        →  編排層：統一入口，一鍵 Bootstrap
🩺 Infra Watchdog       →  巡查層：每週定時，只報告不自動修復
🔀 Skill Router         →  路由層：任務匹配技能（常駐）
🛡️ Infra Enforcer       →  強制層：程式評分 + revise + block + audit（gateway 插件）
🧠 Vector Memory        →  基礎層：永不失憶
🎨 Skill Curator        →  維護層：技能健康管理（含 CJK 關鍵詞注入）
🧬 Agent Evolver        →  進化層：與你一起成長
🔮 Agent Previsor       →  預判層：動手之前，預見所有坑
```

---

## 📊 市場痛點對照 · Market Validation

| 痛點 · Pain Point | 數據 · Data | 來源 · Source | 方案 · Solution |
|------|------|------|------|
| Agent 協調失敗 | 40% 專案被取消 | Gartner 2026 | Skill Router |
| 缺少初始化引導 | 用戶安裝後不知下一步，技能閒置率 65% | 內部審計 242 技能 | Agentic Infra |
| Agent 跳過技能/作弊 | 模型自評不可靠，文字匯報可偽造 | 實測：9 連 REJECT 仍自評 PASS | Infra Enforcer |
| 狀態失憶 | #1 生產殺手 | VentureBeat Q2 2026 | Vector Memory |
| 技能管理失控 | 125 技能僅 51% 健康 | UltraClaw 實測 | Skill Curator |
| 核心文件臃腫 | 長期使用後核心文件月增 >20% | UltraClaw 實測 | Agent Evolver |
| 缺乏事前預判 | 80% 時間花在勘探而非建設 | UltraClaw 實測 | Agent Previsor |

---

## 📊 綜合效果 · Results

| 指標 | 使用前 | 使用後 | 改善 |
|------|--------|--------|------|
| 技能發現率 | ~35% | ~90% | +157% |
| 非英語匹配率 | ~20% | ~95% | +375% |
| Agent 透明度 | 0% | 100% | ∞ |
| 跨 Session 記憶保留 | 0% | >95% | ∞ |
| 技能健康度 | ~51% | ~99% | +94% |
| 初始化時間 | N/A | <1 分鐘 | ∞ |
| 任務啟動回合數 | 3-5 | 1 | -60% |

---

## 📄 授權 · License

MIT

## 🌟 關於 · About

來自 **UltraClaw**——一個在實戰中迭代了 6 個月的 AI 助理系統。每個方案都經歷過踩坑、修復、驗證的完整循環。**好工具來自真實的痛點。**
