---
name: skill-reporting
description: 技能匯報 技能透明度 使用了咩技能 回覆附帶技能信息 技能使用追蹤 Skill usage reporting — append skill usage summary to every agent reply for transparency. Use when users can't see what skills/tools the agent used, when debugging agent behavior is opaque, or when building trust through transparency.
---

# 📊 Skill Reporting — 讓 Agent 的每一步都透明可見

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

## 授權

MIT
