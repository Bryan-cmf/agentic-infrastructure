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

## 觸發方式

| 方式 | 說明 |
|------|------|
| 月度 Cron | 每月 1 號 09:00 HKT |
| 增長觸發 | 核心文件總行數月增 >20% → 提前觸發 |
| 手動 | `/evolve` |

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
