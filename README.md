# 🧰 Agentic Infrastructure — Agent 基礎建設七件套

> **七個獨立技能，解決 AI Agent 生態系統的七個結構性問題。**
> 一鍵安裝，立即生效。支持任何 AI Agent 平台。

---

## 🎯 七個問題 · 七個方案

| # | 問題 | 技能 | 安裝命令 |
|---|------|------|--------|
| 1 | 非英語用戶找不到技能 | 🌐 Skills Triggering | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/openclaw-agent-toolkit/main/skills-triggering/SKILL.md) `-o skills/skills-triggering/SKILL.md` |
| 2 | Agent 有技能但不知道用哪個 | 🔀 Skill Router | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/openclaw-agent-toolkit/main/skill-router/SKILL.md) `-o skills/skill-router/SKILL.md` |
| 3 | Agent 做了什麼無人知 | 📊 Skill Reporting | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/openclaw-agent-toolkit/main/skill-reporting/SKILL.md) `-o skills/skill-reporting/SKILL.md` |
| 4 | Agent 重啟後完全失憶 | 🧠 Vector Memory | `curl -sSL` [`setup.sh`](https://raw.githubusercontent.com/Bryan-cmf/openclaw-agent-toolkit/main/vector-memory/setup.sh) `\| bash` |
| 5 | 技能越裝越多越來越亂 | 🎨 Skill Curator | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/openclaw-agent-toolkit/main/skill-curator/SKILL.md) `-o skills/skill-curator/SKILL.md` |
| 6 | 核心文件越來越臃腫 | 🧬 Agent Evolver | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/openclaw-agent-toolkit/main/agent-evolver/SKILL.md) `-o skills/agent-evolver/SKILL.md` |
| 7 | 每次都在事後才發現問題 | 🔮 Agent Previsor | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/openclaw-agent-toolkit/main/agent-previsor/SKILL.md) `-o skills/agent-previsor/SKILL.md` |

---

## 📥 單獨安裝 · Individual Install

```bash
# ① Skills Triggering — 多語言技能觸發
mkdir -p skills/skills-triggering && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skills-triggering/SKILL.md -o skills/skills-triggering/SKILL.md

# ② Skill Router — 任務技能路由
mkdir -p skills/skill-router && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-router/SKILL.md -o skills/skill-router/SKILL.md

# ③ Skill Reporting — 技能使用透明度
mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md

# ④ Vector Memory — 向量記憶持久化（含 Qdrant + BGE-m3 一鍵部署）
curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/vector-memory/setup.sh | bash

# ⑤ Agent Evolver — 核心文件自我進化
mkdir -p skills/agent-evolver && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-evolver/SKILL.md -o skills/agent-evolver/SKILL.md

# ⑥ Skill Curator — 技能全生命週期策展
mkdir -p skills/skill-curator && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-curator/SKILL.md -o skills/skill-curator/SKILL.md
mkdir -p skills/agent-previsor && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-previsor/SKILL.md -o skills/agent-previsor/SKILL.md
```

## 📋 全部一鍵安裝 · Install All

把這段話發給任何 AI Agent 即可：

```
請安裝 Agentic Infrastructure 六件套：

mkdir -p skills/skills-triggering && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skills-triggering/SKILL.md -o skills/skills-triggering/SKILL.md
mkdir -p skills/skill-router && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-router/SKILL.md -o skills/skill-router/SKILL.md
mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md
curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/vector-memory/setup.sh | bash
mkdir -p skills/agent-evolver && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-evolver/SKILL.md -o skills/agent-evolver/SKILL.md
mkdir -p skills/skill-curator && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-curator/SKILL.md -o skills/skill-curator/SKILL.md
mkdir -p skills/agent-previsor && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-previsor/SKILL.md -o skills/agent-previsor/SKILL.md
```

---

> **四個獨立項目，解決 AI Agent 生態系統的四個結構性問題。**
>
> **Four standalone projects solving four structural problems in the AI agent ecosystem.**
>
> **4つの独立プロジェクトで、AIエージェントエコシステムの4つの構造的問題を解決。**
>
> **4개의 독립 프로젝트로 AI 에이전트 생태계의 4가지 구조적 문제를 해결합니다.**
>
> **أربعة مشاريع مستقلة تحل أربع مشاكل هيكلية في النظام البيئي لوكلاء الذكاء الاصطناعي.**
>
> **चार स्वतंत्र परियोजनाएँ जो AI एजेंट इकोसिस्टम की चार संरचनात्मक समस्याओं को हल करती हैं。**

---

## 🌏 多語言介紹 · Multi-Language Intro

### 🇹🇼 繁體中文
你的 AI Agent 有數百個技能卻找不到？非英語用戶的請求無法觸發正確的技能？Agent 重啟後完全失憶？每次回覆都像黑箱，不知道 Agent 用了哪些工具？**Agentic Infrastructure 四件套**為你解決這四個問題——一鍵安裝，立即生效。

### 🇨🇳 简体中文
你的 AI Agent 有数百个技能却找不到？非英语用户的请求无法触发正确的技能？Agent 重启后完全失忆？每次回复都像黑箱？**Agentic Infrastructure 四件套**为你解决这四个问题——一键安装，立即生效。

### 🇯🇵 日本語
AIエージェントに数百のスキルがあるのに見つからない？非英語ユーザーのリクエストが正しいスキルをトリガーできない？再起動のたびに完全に記憶喪失？毎回の応答がブラックボックス？**4つのソリューション**がこれらの問題を解決——ワンラインインストールですぐに使えます。

### 🇰🇷 한국어
AI 에이전트에 수백 개의 스킬이 있는데 찾을 수 없다면? 비영어권 사용자의 요청이 올바른 스킬을 트리거하지 못한다면? 재시작할 때마다 완전히 기억을 잃는다면? 매 응답이 블랙박스 같다면? **네 가지 솔루션**이 이 문제들을 해결합니다.

### 🇸🇦 العربية
وكيل الذكاء الاصطناعي لديك يمتلك مئات المهارات لكنه لا يجدها؟ طلبات المستخدمين غير الناطقين بالإنجليزية لا تُشغّل المهارات الصحيحة؟ الوكيل يفقد ذاكرته بالكامل بعد كل إعادة تشغيل؟ كل رد يشبه الصندوق الأسود؟ **أربعة حلول** تحل هذه المشكلات — جاهزة فوراً.

### 🇮🇳 हिन्दी
आपके AI एजेंट के पास सैकड़ों स्किल्स हैं लेकिन वह उन्हें ढूंढ नहीं पाता? गैर-अंग्रेज़ी उपयोगकर्ताओं के अनुरोध सही स्किल्स को ट्रिगर नहीं कर पाते? हर रीस्टार्ट पर एजेंट पूरी तरह से भूल जाता है? हर जवाब ब्लैक बॉक्स जैसा? **चार समाधान** इन समस्याओं को हल करते हैं।

---

## 🎯 四個問題 · 四個方案 · 四條命令

### 🇹🇼🇨🇳 中文

| # | 問題 | 技能 | 安裝命令 |
|---|------|------|---------|
| 1 | 非英語用戶找不到技能 | 🌐 Skills Triggering | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skills-triggering/SKILL.md) `-o skills/skills-triggering/SKILL.md` |
| 2 | Agent 有技能但不知道用哪個 | 🔀 Skill Router | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-router/SKILL.md) `-o skills/skill-router/SKILL.md` |
| 3 | Agent 做了什麼無人知 | 📊 Skill Reporting | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md) `-o skills/skill-reporting/SKILL.md` |
| 4 | Agent 重啟後完全失憶 | 🧠 Vector Memory | `curl -sSL` [`setup.sh`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/vector-memory/setup.sh) `| bash` |

### 🇯🇵 日本語

| # | 問題 | スキル | インストール |
|---|------|------|------|
| 1 | 非英語ユーザーがスキルを見つけられない | 🌐 Skills Triggering | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skills-triggering/SKILL.md) `-o skills/skills-triggering/SKILL.md` |
| 2 | スキルが多すぎてどれを使うか分からない | 🔀 Skill Router | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-router/SKILL.md) `-o skills/skill-router/SKILL.md` |
| 3 | エージェントが何をしたか分からない | 📊 Skill Reporting | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md) `-o skills/skill-reporting/SKILL.md` |
| 4 | 再起動のたびに完全に記憶喪失 | 🧠 Vector Memory | `curl -sSL` [`setup.sh`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/vector-memory/setup.sh) `| bash` |

### 🇰🇷 한국어

| # | 문제 | 스킬 | 설치 |
|---|------|------|------|
| 1 | 비영어 사용자가 스킬을 찾을 수 없음 | 🌐 Skills Triggering | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skills-triggering/SKILL.md) `-o skills/skills-triggering/SKILL.md` |
| 2 | 스킬이 너무 많아 어떤 것을 쓸지 모름 | 🔀 Skill Router | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-router/SKILL.md) `-o skills/skill-router/SKILL.md` |
| 3 | 에이전트가 무엇을 했는지 알 수 없음 | 📊 Skill Reporting | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md) `-o skills/skill-reporting/SKILL.md` |
| 4 | 재시작할 때마다 완전히 기억 상실 | 🧠 Vector Memory | `curl -sSL` [`setup.sh`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/vector-memory/setup.sh) `| bash` |

### 🇸🇦 العربية

| # | المشكلة | المهارة | التثبيت |
|---|------|------|------|
| 1 | المستخدمون غير الناطقين بالإنجليزية لا يجدون المهارات | 🌐 Skills Triggering | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skills-triggering/SKILL.md) `-o skills/skills-triggering/SKILL.md` |
| 2 | المهارات كثيرة ولا يعرف أيها يستخدم | 🔀 Skill Router | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-router/SKILL.md) `-o skills/skill-router/SKILL.md` |
| 3 | لا تعرف ماذا فعل الوكيل | 📊 Skill Reporting | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md) `-o skills/skill-reporting/SKILL.md` |
| 4 | يفقد الذاكرة بالكامل بعد كل إعادة تشغيل | 🧠 Vector Memory | `curl -sSL` [`setup.sh`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/vector-memory/setup.sh) `| bash` |

### 🇮🇳 हिन्दी

| # | समस्या | स्किल | इंस्टॉल |
|---|------|------|------|
| 1 | गैर-अंग्रेज़ी उपयोगकर्ता स्किल्स नहीं ढूंढ पाते | 🌐 Skills Triggering | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skills-triggering/SKILL.md) `-o skills/skills-triggering/SKILL.md` |
| 2 | बहुत सारी स्किल्स, पता नहीं कौन सी इस्तेमाल करें | 🔀 Skill Router | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-router/SKILL.md) `-o skills/skill-router/SKILL.md` |
| 3 | पता नहीं एजेंट ने क्या किया | 📊 Skill Reporting | `curl -sSL` [`SKILL.md`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md) `-o skills/skill-reporting/SKILL.md` |
| 4 | हर रीस्टार्ट पर पूरी तरह भूल जाता है | 🧠 Vector Memory | `curl -sSL` [`setup.sh`](https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/vector-memory/setup.sh) `| bash` |

---

## 📊 市場痛點對照 · Market Pain Points

### 🇹🇼🇨🇳 中文

| 痛點 | 數據 | 來源 | 方案 |
|------|------|------|------|
| Agent 協調失敗 | 40% 專案被取消 | Gartner 2026 | Skill Router |
| 技能對非英語用戶隱形 | 75% 用戶非英語，95% 技能只有英文 | 內部審計 242 技能 | Skills Triggering |
| Agent 黑箱不透明 | 透明度是企業採用 AI 第 3 大障礙 | Deloitte 2026 | Skill Reporting |
| 狀態失憶 | #1 生產殺手 | VentureBeat Q2 2026 | Vector Memory |

### 🇯🇵 日本語

| 課題 | データ | 出典 | 解決策 |
|------|------|------|------|
| エージェント調整の失敗 | 40%のプロジェクトがキャンセル | Gartner 2026 | Skill Router |
| 非英語ユーザーにスキルが見えない | 75%が非英語ユーザー、95%のスキルが英語のみ | 242スキルの内部監査 | Skills Triggering |
| エージェントがブラックボックス | 透明性は企業採用の第3の障壁 | Deloitte 2026 | Skill Reporting |
| 状態喪失 | プロダクションの#1キラー | VentureBeat Q2 2026 | Vector Memory |

### 🇰🇷 한국어

| 문제 | 데이터 | 출처 | 해결책 |
|------|------|------|------|
| 에이전트 조정 실패 | 40% 프로젝트 취소 | Gartner 2026 | Skill Router |
| 비영어 사용자에게 스킬이 보이지 않음 | 75% 비영어 사용자, 95% 스킬이 영어만 | 242개 스킬 감사 | Skills Triggering |
| 에이전트 블랙박스 | 투명성은 기업 도입 제3의 장벽 | Deloitte 2026 | Skill Reporting |
| 상태 상실 | 프로덕션 #1 킬러 | VentureBeat Q2 2026 | Vector Memory |

### 🇸🇦 العربية

| المشكلة | البيانات | المصدر | الحل |
|------|------|------|------|
| فشل تنسيق الوكيل | 40% من المشاريع تُلغى | Gartner 2026 | Skill Router |
| المهارات غير مرئية لغير الناطقين بالإنجليزية | 75% مستخدمين غير إنجليز، 95% مهارات بالإنجليزية فقط | تدقيق 242 مهارة | Skills Triggering |
| الوكيل صندوق أسود | الشفافية ثالث أكبر عقبة للتبني | Deloitte 2026 | Skill Reporting |
| فقدان الحالة | القاتل الأول في الإنتاج | VentureBeat Q2 2026 | Vector Memory |

### 🇮🇳 हिन्दी

| समस्या | डेटा | स्रोत | समाधान |
|------|------|------|------|
| एजेंट कोऑर्डिनेशन फेल | 40% प्रोजेक्ट रद्द | Gartner 2026 | Skill Router |
| गैर-अंग्रेज़ी उपयोगकर्ताओं के लिए स्किल्स अदृश्य | 75% गैर-अंग्रेज़ी, 95% स्किल्स सिर्फ अंग्रेज़ी | 242 स्किल ऑडिट | Skills Triggering |
| एजेंट ब्लैक बॉक्स | पारदर्शिता तीसरी सबसे बड़ी बाधा | Deloitte 2026 | Skill Reporting |
| स्टेट लॉस | प्रोडक्शन का #1 किलर | VentureBeat Q2 2026 | Vector Memory |

---

## 🏗️ 四層互補 · Architecture

```
🌐 Skills Triggering（發現層 / Discovery）
    │  讓技能被正確發現
    │
    ▼
🔀 Skill Router（路由層 / Routing）
    │  讓任務匹配正確技能
    │
    ▼
📊 Skill Reporting（透明度層 / Transparency）
    │  讓每一步都透明可見
    │
    ▼
🧠 Vector Memory（基礎層 / Foundation）
    │  讓 Agent 記住一切
    │
    ▼
🎨 Skill Curator（維護層 / Maintenance）
    │  讓技能保持健康
    │
    ▼
🧬 Agent Evolver（進化層 / Evolution）
    │  讓 Agent 與你一起成長
```

---

## 📊 綜合效果 · Results

| 指標 | 無四件套 | 有四件套 | 改善 |
|------|---------|---------|------|
| 技能發現率 | ~35% | ~90% | +157% |
| 非英語匹配率 | ~20% | ~95% | +375% |
| Agent 透明度 | 0% | 100% | ∞ |
| 跨 Session 記憶保留 | 0% | >95% | ∞ |
| 任務啟動回合數 | 3-5 | 1 | -60% |

---

## 📄 授權 · License

MIT

## 🌟 關於 · About

來自 **UltraClaw**——一個在實戰中迭代了 6 個月的 AI 助理系統。每個方案都經歷過踩坑、修復、驗證的完整循環。**好工具來自真實的痛點。**
