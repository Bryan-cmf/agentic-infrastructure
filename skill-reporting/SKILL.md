---
name: skill-reporting
description: 技能匯報 技能透明度 スキルレポート 透明性 스킬리포팅 투명성 Skill usage reporting — append skill usage summary to every agent reply for transparency.
---

# 📊 Skill Reporting — 讓 Agent 的每一步都透明可見

## 📥 一行安裝

```bash
mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md
```

---

## 🌏 完整說明（選擇你的語言）

### 🇹🇼 繁體中文

**痛點：** Agent 回覆了你，但你完全不知道它用了哪些技能、走了什麼流程、數據從哪來的。每次回覆都像黑箱——有沒有跳過關鍵步驟？結論是怎麼得出的？無從得知。這不是性能問題，是信任問題。市場數據：透明度是企業採用 AI Agent 的第三大障礙（Deloitte 2026）。僅 20% 企業有成熟的 Agent 治理機制。可審計性被列為 Agent 生產部署的首要需求（VentureBeat）。「不知道 Agent 做了什麼」是用戶流失的主因之一。

**方案：** 在每次回覆末尾自動附加一行技能使用摘要：`> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）+ tool-C（用途）`。統一格式，一行搞定，附帶用途說明。這是一個制度性技能——不需要安裝程式碼，只需在 RULES.md 中加入一條永久規則。支援任何 AI Agent 平台。

**效果：** Agent 透明度從 0% → 100%。用戶可以驗證每個數據的來源。Debug 時間大幅縮短（看最後一行就知道哪個技能漏了）。新用戶對 Agent 的信任度自然建立。間接效果：Agent 必須記錄自己用了什麼 → 減少「跳步」行為。

**一行安裝：** `mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md`

### 🇨🇳 简体中文

**痛点：** Agent 回复了你，但你完全不知道它用了哪些技能、走了什么流程、数据从哪来的。每次回复都像黑箱——有没有跳过关键步骤？结论是怎么得出的？无从得知。这不是性能问题，是信任问题。透明度是企业采用 AI Agent 的第三大障碍（Deloitte 2026）。仅 20% 企业有成熟的 Agent 治理机制。

**方案：** 在每次回复末尾自动附加一行技能使用摘要：`> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）`。统一格式，一行搞定。制度性技能——不需要安装代码，只需在 RULES.md 中加入一条永久规则。

**效果：** Agent 透明度 0%→100%。Debug 时间大幅缩短。信任度自然建立。Agent 必须记录自己用了什么 → 减少跳步。

**一行安装：** `mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md`

### 🇯🇵 日本語

**痛点：** エージェントが返信したが、どのスキルを使い、どんなプロセスを経たか全くわからない。毎回の応答がブラックボックス。重要なステップをスキップしていないか？結論はどう導かれたか？これはパフォーマンスの問題ではなく、信頼の問題。透明性は企業の AI エージェント採用における第 3 の障壁（Deloitte 2026）。

**方案：** 毎回の応答末にスキル使用サマリーを 1 行自動付加：`> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）`。統一フォーマット。制度的スキル——RULES.md に永続ルールを 1 つ追加するだけ。全 AI エージェントプラットフォーム対応。

**効果：** エージェント透明性 0%→100%。全データソース検証可能。デバッグ時間大幅短縮。信頼が自然に構築。

**一行インストール：** `mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md`

### 🇰🇷 한국어

**痛点：** 에이전트가 답변했지만 어떤 스킬을 사용했는지, 어떤 프로세스를 거쳤는지 전혀 알 수 없다. 매 응답이 블랙박스. 중요한 단계를 건너뛰었는지? 결론이 어떻게 도출됐는지? 이는 신뢰 문제다. 투명성은 기업 AI 에이전트 도입의 세 번째 장애물(Deloitte 2026).

**方案：** 매 응답 말미에 스킬 사용 요약 한 줄 자동 첨부：`> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）`. 통일된 형식. 제도적 스킬——RULES.md에 영구 규칙 하나만 추가. 모든 AI 에이전트 플랫폼 지원.

**効果：** 에이전트 투명성 0%→100%. 모든 데이터 소스 검증 가능. 디버그 시간 대폭 단축. 신뢰 자연 구축.

**한 줄 설치：** `mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md`

### 🇸🇦 العربية

**المشكلة:** وكيل الذكاء الاصطناعي يرد عليك، لكنك لا تعرف المهارات التي استخدمها أو العملية التي مر بها. كل رد صندوق أسود. هل تخطى خطوات مهمة؟ كيف توصل إلى الاستنتاج؟ هذه مشكلة ثقة. الشفافية هي ثالث أكبر عقبة (Deloitte 2026).

**الحل:** إضافة سطر واحد تلقائياً في نهاية كل رد يلخص المهارات المستخدمة. تنسيق موحد. مهارة مؤسسية——فقط أضف قاعدة دائمة واحدة إلى RULES.md. يعمل مع جميع منصات وكلاء الذكاء الاصطناعي.

**التأثير:** شفافية الوكيل 0%→100%. يمكن التحقق من كل مصدر بيانات. وقت التصحيح ينخفض بشكل كبير. الثقة تُبنى طبيعياً.

**تثبيت بسطر واحد：** `mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md`

### 🇮🇳 हिन्दी

**समस्या:** एजेंट ने जवाब दिया, लेकिन आपको नहीं पता उसने कौन सी स्किल्स इस्तेमाल कीं, क्या प्रक्रिया अपनाई। हर जवाब ब्लैक बॉक्स। क्या अहम स्टेप्स स्किप किए? निष्कर्ष कैसे निकला? यह भरोसे की समस्या है। पारदर्शिता AI एजेंट अपनाने में तीसरी सबसे बड़ी बाधा (Deloitte 2026)।

**समाधान:** हर जवाब के अंत में एक लाइन ऑटो-अटैच——स्किल उपयोग सारांश। एकीकृत प्रारूप। संस्थागत स्किल——बस RULES.md में एक स्थायी नियम जोड़ें। सभी AI एजेंट प्लेटफ़ॉर्म पर काम करता है।

**प्रभाव:** एजेंट पारदर्शिता 0%→100%। हर डेटा सोर्स सत्यापन योग्य। डिबग समय में भारी कमी। भरोसा स्वाभाविक रूप से बनता है।

**एक लाइन इंस्टॉल：** `mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md`

---

## 🔧 技術細節

### 格式規範

```
> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）+ tool-C（用途）
```

### 安裝方式

在你的 `RULES.md` 中加入永久規則：

```markdown
## R18：每次回覆附帶技能使用信息
每次回覆末尾附帶「> 🛠️ 使用技能：」清單。永久，不可跳過。
```

### 效果

| 場景 | 無 Reporting | 有 Reporting |
|------|-------------|-------------|
| 用戶收到報告 | 「數據哪來的？」 | 「看到了，用了 DI+年報」 |
| Debug 出錯 | 翻 Session JSONL | 看最後一行 |
| 新用戶評估 | 「這東西可靠嗎？」 | 每條回覆透明 |

## 授權

MIT
