---
name: skill-reporting
description: 技能匯報 技能透明度 使用了咩技能 回覆附帶技能信息 スキルレポート 透明性 스킬리포팅 투명성 Skill usage reporting — append skill usage summary to every agent reply for transparency.
---

# 📊 Skill Reporting — 讓 Agent 的每一步都透明可見

## 📥 一行安裝

```bash
mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md
```

## 🌏 完整多語種說明

### 🇹🇼 繁體中文

**問題：** Agent 回覆了你，但你完全不知道它用了哪些技能、走了什麼流程。每次回覆都像黑箱——數據從哪來的？有沒有跳過關鍵步驟？無從得知。這不是性能問題，是信任問題。市場數據：透明度是企業採用 AI Agent 的第三大障礙（Deloitte 2026）。僅 20% 企業有成熟的 Agent 治理機制。可審計性被列為 Agent 生產部署的首要需求（VentureBeat）。「不知道 Agent 做了什麼」是用戶流失的主要原因之一。

**方案：** 在每次回覆末尾自動附加一行技能使用摘要——`> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）`。統一的格式規範，一行搞定。這是一個制度性技能——不需要安裝程式碼，只需在你的 RULES.md 中加入一條永久規則。

**效果：** Agent 透明度從 0% → 100%。用戶可以驗證每個數據的來源。Debug 時間大幅縮短。信任度自然建立。

```bash
mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md
```

### 🇨🇳 简体中文

**问题：** Agent 回复了你，但你完全不知道它用了哪些技能、走了什么流程。每次回复都像黑箱——数据从哪来的？有没有跳过关键步骤？无从得知。这不是性能问题，是信任问题。市场数据：透明度是企业采用 AI Agent 的第三大障碍（Deloitte 2026）。仅 20% 企业有成熟的 Agent 治理机制。

**方案：** 在每次回复末尾自动附加一行技能使用摘要——`> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）`。统一格式规范。这是一个制度性技能——不需要安装代码，只需在 RULES.md 中加入一条永久规则。

**效果：** Agent 透明度从 0% → 100%。用户可以验证每个数据的来源。Debug 时间大幅缩短。

```bash
mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md
```

### 🇯🇵 日本語

**問題：** エージェントが返信したが、どのスキルを使い、どんなプロセスを経たか全くわからない。毎回の応答がブラックボックス——データはどこから？重要なステップをスキップしていないか？これはパフォーマンスの問題ではなく、信頼の問題。透明性は企業の AI エージェント採用における第 3 の障壁（Deloitte 2026）。

**方案：** 毎回の応答末にスキル使用サマリーを 1 行自動付加——`> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）`。統一フォーマット。コードインストール不要の制度的スキル——RULES.md に永続ルールを 1 つ追加するだけ。

**効果：** エージェントの透明性が 0%→100%。全データソースを検証可能に。デバッグ時間が大幅短縮。

```bash
mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md
```

### 🇰🇷 한국어

**문제:** 에이전트가 답변했지만, 어떤 스킬을 사용했고 어떤 프로세스를 거쳤는지 전혀 알 수 없습니다. 매 응답이 블랙박스——데이터는 어디서 왔는지? 중요한 단계를 건너뛰었는지? 이는 성능 문제가 아닌 신뢰 문제입니다. 투명성은 기업의 AI 에이전트 도입에 있어 세 번째 장애물(Deloitte 2026).

**해결책:** 매 응답 말미에 스킬 사용 요약 한 줄 자동 첨부——`> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）`. 통일된 형식. 코드 설치 불필요한 제도적 스킬——RULES.md에 영구 규칙 하나만 추가.

**효과:** 에이전트 투명성 0%→100%. 모든 데이터 소스 검증 가능. 디버그 시간 대폭 단축.

### 🇸🇦 العربية

**المشكلة:** الوكيل يرد عليك، لكنك لا تعرف إطلاقاً المهارات التي استخدمها أو العملية التي مر بها. كل رد يشبه الصندوق الأسود. هذه ليست مشكلة أداء، بل مشكلة ثقة. الشفافية هي ثالث أكبر عقبة أمام تبني المؤسسات لوكلاء الذكاء الاصطناعي (Deloitte 2026).

**الحل:** إضافة سطر واحد تلقائياً في نهاية كل رد يلخص المهارات المستخدمة. تنسيق موحد. مهارة مؤسسية——فقط أضف قاعدة دائمة واحدة إلى RULES.md.

**التأثير:** شفافية الوكيل من 0% → 100%. يمكن التحقق من مصدر كل بيان. وقت التصحيح ينخفض بشكل كبير.

### 🇮🇳 हिन्दी

**समस्या:** एजेंट ने जवाब दिया, लेकिन आपको बिल्कुल नहीं पता कि उसने कौन सी स्किल्स इस्तेमाल कीं, क्या प्रक्रिया अपनाई। हर जवाब ब्लैक बॉक्स जैसा। यह परफॉर्मेंस की नहीं, भरोसे की समस्या है। पारदर्शिता AI एजेंट अपनाने में तीसरी सबसे बड़ी बाधा (Deloitte 2026).

**समाधान:** हर जवाब के अंत में एक लाइन ऑटो-अटैच करें——स्किल उपयोग सारांश। एकीकृत प्रारूप। संस्थागत स्किल——बस RULES.md में एक स्थायी नियम जोड़ें।

**प्रभाव:** एजेंट पारदर्शिता 0%→100%। हर डेटा सोर्स सत्यापन योग्य। डिबग समय में भारी कमी।

---

## 痛點

> **Agent 回覆了你，但你完全不知道它用了哪些技能、走了什麼流程。**

| 現象 | 根因 |
|------|------|
| Agent 的回答看起來很好，但不知道是從哪來的 | 沒有來源追蹤，無法驗證 |
| 用戶問「你怎麼得出這個結論的？」→ Agent 無法追溯 | 工具調用過程對用戶不可見 |
| Debug 時不知道 Agent 跳過了哪個關鍵步驟 | 技能使用記錄只在 Session JSONL 中，用戶看不到 |
| 用戶對 Agent 信任度低——感覺像黑箱 | 缺乏透明度機制 |

**這不是性能問題，是信任問題。**

一個醫生告訴你診斷結果，但從不解釋他做了哪些檢查——你會相信他嗎？

**市場數據：**

| 數據 | 來源 |
|------|------|
| 透明度是企業採用 AI Agent 的第三大障礙 | Deloitte State of AI 2026 |
| 僅 20% 企業有成熟的 Agent 治理機制 | Deloitte |
| 可審計性被列為 Agent 生產部署的首要需求 | VentureBeat Agentic Reckoning |
| 「不知道 Agent 做了什麼」是用戶流失的主要原因之一 | 多個社群調查 |

**真實案例：**

```
用戶問：「幫我調研 00058」

❌ 沒有 Skill Reporting：
  Agent 回覆了調研報告 → 用戶不知道用了哪些工具
  → 數據從哪來的？有沒有跳過關鍵步驟？無從得知

✅ 有 Skill Reporting：
  Agent 回覆了調研報告，末尾附帶：
  > 🛠️ 使用技能：ak-hk-stock-dd（港股調研）+ 
  >   tavily-search（市場搜索）+ 
  >   web_fetch（hkexnews 年報下載）+ 
  >   cloakbrowser（DI 披露易查詢）
  
  → 用戶清楚知道每個數據的來源 → 信任度大幅提升
```

## 方案

### 核心機制

在每次 Agent 回覆的末尾，自動附加一行技能使用摘要：

```
> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）+ tool-C（用途）
```

### 格式規範

- **一行搞定**，簡潔不佔空間
- **列出所有使用過的技能和工具**
- **每項附帶用途說明**（括號內一句話）
- **放在回覆最末尾**

### 為什麼需要格式規範？

沒有統一的格式 → 混亂：

```
❌ 「用了 search 和 read」
❌ 「Tools: search, read, write」
❌ （根本沒附）
```

有統一格式 → 可讀、可解析、可審計：

```
✅ > 🛠️ 使用技能：web_search（市場數據）+ firecrawl_scrape（年報提取）+ read（模板讀取）+ write（報告生成）
```

### 安裝方式

#### 方式一：永久規則（推薦）

在你的 `RULES.md` 或 `PERMANENT-RULES.md` 中加入：

```markdown
## 📊 R18：每次回覆附帶技能使用信息

| 觸發條件 | 動作 |
|----------|------|
| 每次回覆用戶（任何內容） | 回覆末尾附帶「> 🛠️ 使用技能：」清單 |
| 🔴 永久 | 不可跳過 |

### 格式規範
> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）+ tool-C（用途）

### 禁止行為
- 覺得「只用咗基本工具唔使列」
- 忘記附加
- 只在部分回覆附加
```

#### 方式二：Hook 注入（進階）

如果你的 Agent 平台支援 hooks，可以在回覆生成後自動注入：

```python
def inject_skill_report(response, skills_used):
    report = " > 🛠️ 使用技能：" + " + ".join(
        f"{s['name']}（{s['purpose']}）" for s in skills_used
    )
    return response + "\n\n" + report
```

---

## 效果

### 透明度對比

| 場景 | 無 Skill Reporting | 有 Skill Reporting |
|------|-------------------|-------------------|
| 用戶收到調研報告 | 「報告不錯，但數據哪來的？」 | 「看到了，用了 DI 披露易 + 年報」 |
| Debug 出錯時 | 翻 Session JSONL | 看最後一行就知道哪個技能漏了 |
| 新用戶評估 Agent | 「這東西可靠嗎？」 | 每條回覆都透明 → 信任自然建立 |

### 間接效果

| 效果 | 說明 |
|------|------|
| 自我紀律 | Agent 必須記錄自己用了什麼 → 減少「跳步」 |
| 技能使用率提升 | 用戶看到技能名稱 → 下次主動要求使用 |
| 審計友好 | 每條回覆都是可追溯的紀錄 |

---

## 與其他三件套的關係

```
🌐 Skills Triggering  →  技能被觸發
🔀 Skill Router       →  技能被正確路由
📊 Skill Reporting    →  技能使用被記錄和展示  ← 你正在看這個
🧠 Vector Memory      →  一切被記住
```

**Skill Reporting 是透明度層——讓前三層的努力被看見。**

---

## 快速開始

1. 將上述 R18 規則寫入你的 `RULES.md` 或 `PERMANENT-RULES.md`
2. 確保每次 Session 啟動時讀取這個規則
3. 開始在每條回覆末尾附加技能使用信息

就這麼簡單。不需要安裝任何程式碼——這是一個**制度性技能**。

---

## 📥 一行安裝

```bash
mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md
```

## 授權

MIT
