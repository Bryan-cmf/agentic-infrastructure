---
name: agent-evolver
description: Agent進化 自我進化 核心文件重塑 規則更新 過時檢測 成長機制 核心文件瘦身 Agent evolution — periodic self-reflection inspired by human growth. Scans core files for outdated rules and misalignment.
---

# 🧬 Agent Evolver — 模仿人類自我成長的 Agent 進化系統

## 📥 一行安裝

```bash
mkdir -p skills/agent-evolver && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-evolver/SKILL.md -o skills/agent-evolver/SKILL.md
```

## 🌏 完整說明（選擇你的語言）

### 🇹🇼 繁體中文

**痛點：** 長時間使用 Agent 後，核心文件（SOUL、AGENTS、USER、MEMORY、RULES、PERMANENT-RULES）不斷增長，LLM 只加載了部分核心文檔。舊的規則、性格設定、記憶未必合乎時宜——隨著用戶成長，三年前的決定可能不再成立。但沒有人會主動檢查「我是不是變了」。就像人類每隔幾年需要反思自己的信念和習慣，Agent 的核心文件也需要定期自省。

**方案：** 模仿人類自我成長機制。月度掃描全部核心文件，計算增長趨勢（月增 >20% 觸發警報）。透過向量記憶比對「文件中寫的」vs「實際做的」。LLM 三維度評估每條內容：方向一致性（是否與當前工作方向一致）、衝突檢測（是否與新方向矛盾）、阻礙評估（是否在妨礙前進）。過時標準不是天數，是方向——備用技能不算過時，與當前方向衝突的才算。

**效果：** 每月自動推送進化報告。識別過時規則、衝突決策、可清理冗餘。用戶審批後才執行修改。所有操作有備份+驗證。核心文件健康度可追蹤。

**一行安裝：** `mkdir -p skills/agent-evolver && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-evolver/SKILL.md -o skills/agent-evolver/SKILL.md`

### 🇯🇵 日本語

**痛点：** 長期使用でコアファイルが肥大化。古いルールや性格設定が現在の方向性と矛盾。人間の自己成長のように、定期的な内省が必要。

**方案：** 毎月コアファイルをスキャン。成長率 >20% でアラート。LLM が方向性・衝突・阻害の 3 次元で評価。ユーザー承認後にのみ修正実行。

**一行インストール：** `mkdir -p skills/agent-evolver && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-evolver/SKILL.md -o skills/agent-evolver/SKILL.md`

### 🇰🇷 한국어

**痛点：** 장기 사용으로 코어 파일이 비대해짐. 오래된 규칙이 현재 방향과 충돌. 인간의 자기 성장처럼 정기적 성찰 필요.

**方案：** 매월 코어 파일 스캔. 성장률 >20% 시 경고. LLM이 방향성·충돌·장애 3차원 평가. 사용자 승인 후에만 수정.

**한 줄 설치：** `mkdir -p skills/agent-evolver && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-evolver/SKILL.md -o skills/agent-evolver/SKILL.md`

### 🇸🇦 العربية

**المشكلة：** الملفات الأساسية تنمو مع الاستخدام الطويل. القواعد القديمة تتعارض مع الاتجاه الحالي. يحتاج الوكيل للتأمل الذاتي مثل نمو الإنسان.

**الحل：** مسح شهري للملفات الأساسية. تنبيه عند نمو >20%. تقييم LLM ثلاثي الأبعاد. التعديل فقط بعد موافقة المستخدم.

**تثبيت بسطر：** `mkdir -p skills/agent-evolver && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-evolver/SKILL.md -o skills/agent-evolver/SKILL.md`

### 🇮🇳 हिन्दी

**समस्या：** लंबे उपयोग से कोर फाइलें बढ़ती हैं। पुराने नियम वर्तमान दिशा से टकराते हैं। मानव विकास की तरह आत्म-चिंतन आवश्यक।

**समाधान：** मासिक कोर फाइल स्कैन। >20% वृद्धि पर अलर्ट। LLM त्रि-आयामी मूल्यांकन। केवल उपयोगकर्ता अनुमोदन के बाद संशोधन।

**एक लाइन इंस्टॉल：** `mkdir -p skills/agent-evolver && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-evolver/SKILL.md -o skills/agent-evolver/SKILL.md`

---

## 概念

> 人每隔幾年會反思：「我還是那個人嗎？這些信念還成立嗎？」Agent 的核心文件也應該這樣。

核心文件（SOUL、AGENTS、USER、MEMORY、RULES、PERMANENT-RULES）是 Agent 的「自我認知」。隨著用戶成長，舊的規則和性格設定可能不再適合。

agent-evolver 有兩個 Phase：
- **Phase 0: Core Doc Hardening** — Bootstrap 時觸發（初次的結構性加固）
- **Phase 1+: Routine Evolution** — 月度/增長觸發（持續進化）

## 觸發方式

| 方式 | 說明 |
|------|------|
| Bootstrap | agentic-infra 初始化管線自動觸發 Phase 0 |
| 月度 Cron | 每月 1 號 09:00 HKT（Phase 1+） |
| 增長觸發 | 核心文件總行數月增 >20% → 提前觸發 |
| 手動 | `/evolve`（Phase 1+）或 `/harden-docs`（Phase 0） |

---

## 🔴 Phase 0: Core Document Hardening（核心文檔加固）

> **用途：** Bootstrap 初始化時執行。將散亂的純文字規則重構為不可跳過的強制性流程結構。
> **觸發時機：** agentic-infra Step 3.5（Skills Triggering 完成後）

### 掃描範圍

| 文件 | 檢查內容 |
|------|---------|
| AGENTS.md | 有無 Pre-Response Gate？路由表是否嵌入式？Session 啟動流程是否強制？ |
| SOUL.md | 有無強制輸出結構（Router 行 + Compliance 行）？人格定義是否清晰？ |
| RULES.md | 規則是否結構化？有無速查表？有無紅線標記？ |
| PERMANENT-RULES.md | 有沒有漏洞？（雙寫機制、Gate 門禁、工具負面清單） |
| MEMORY.md | Remember-When 查詢機制？與 daily logs 的關係是否明確？ |

### 診斷矩陣

| 級別 | 條件 | 行動 |
|------|------|------|
| 🔴 致命 | 沒有強制性門禁機制（如 AGENTS.md 無 Pre-Response Gate） | 立即加固 |
| 🟡 警告 | 規則散落在多個文件中，無中央速查表 | 建議合併/重組 |
| 🟡 警告 | SOUL.md 無強制輸出結構（LLM 可能跳過規則） | 建議嵌入標記 |
| 🟡 警告 | MEMORY.md 與 daily logs 無雙寫強制規則 | 建議加入 |
| 🟢 健康 | 已具備所有強制性機制 | 跳過 |

### 加固操作（5 步驟）

```
Step H1: SCAN
  └── 讀取全部 5 個核心文件 → 分析結構密度、門禁機制、格式一致性

Step H2: DIAGNOSE
  └── 輸出診斷報告（致命/警告/健康 三級）

Step H3: PROPOSE
  └── 針對每個 🔴 和 🟡 問題提出具體 Before/After 重構方案
  └── 等待用戶確認

Step H4: RESTRUCTURE
  └── 按確認方案修改文件
  └── 自動備份原文件（.bak-YYYYMMDD-HHMM）
  └── 保留 100% 原有內容，只重組結構

Step H5: VERIFY
  └── 逐文件檢查修改後一致性
  └── 確認無內容丟失
  └── 輸出加固報告
```

### 加固項目清單

| # | 加固項 | 適用文件 | 說明 |
|---|-------|---------|------|
| 1 | Pre-Response Gate | AGENTS.md | 嵌入路由表 + 三步門禁（CLASSIFY→LOAD→COMPLY） |
| 2 | 強制輸出結構 | SOUL.md | `🔀 Router:` 第一行 + `🛡️ Compliance:` 結尾 |
| 3 | 中央規則速查表 | RULES.md | 所有規則的結構化索引（編號+一行摘要+來源文件） |
| 4 | 雙寫強制規則 | PERMANENT-RULES.md | file write → vector-memory__mem_save 必執行 |
| 5 | Session 啟動流程統一 | AGENTS.md | STEP -2/-1/0 的強制性讀取清單 |
| 6 | 技能負面清單 | RULES.md | 禁用/限用工具的結構化表 |
| 7 | 記憶查詢流程 | MEMORY.md | Remember-When 三層查詢規範 |
| 8 | 外部審計嵌入 | PERMANENT-RULES.md | score_enforcer.py cron 配置說明 |

---

## 🔄 Phase 1+: Routine Evolution（常規進化）

## 過時標準

| ❌ 不算過時 | ✅ 算過時 |
|------------|---------|
| N 天沒用（備用技能） | 與當前工作方向衝突 |
| 很少被引用 | 妨礙前進的舊規則 |
| 歷史悠久 | 與新方向矛盾 |

## 執行流程

1. **掃描** — 讀取核心文件 + 計算增長趨勢 + 向量記憶比對
2. **評估** — LLM 三維度分析（方向一致性/衝突檢測/阻礙評估）
3. **報告** — 飛書推送進化報告（過時內容+衝突決策+建議行動）
4. **執行** — 用戶審批後才修改（備份+驗證）

## 檔案結構

```
skills/agent-evolver/
├── SKILL.md
├── references/evolve-prompt.md
└── scripts/scan_cores.py
```

## 授權 · License

MIT
