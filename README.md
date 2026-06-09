# 🧰 Agentic Infrastructure — Agent 基礎建設系列

> **四個獨立項目，解決 AI Agent 生態系統的四個結構性問題。**

---

## 🎯 四個問題，四個方案

| # | 問題 | 技能 | 一句話 |
|---|------|------|--------|
| 1 | 非英語用戶找不到技能 | [🌐 Skills Triggering](./skills-triggering/) | 用使用者的語言定義技能觸發詞 |
| 2 | Agent 有技能但不知道用哪個 | [🔀 Skill Router](./skill-router/) | 類別×階段矩陣，自動匹配任務到技能 |
| 3 | Agent 做了什麼無人知 | [📊 Skill Reporting](./skill-reporting/) | 每條回覆附帶技能使用摘要 |
| 4 | Agent 重啟後完全失憶 | [🧠 Vector Memory](./vector-memory/) | Qdrant 持久化 + 語義檢索 + 一鍵部署 |

---

## 📊 市場痛點對照

| 痛點 | 數據 | 來源 | 我們的方案 |
|------|------|------|----------|
| Agent 協調失敗 | 40% 專案被取消 | Gartner 2026 | Skill Router |
| 技能對非英語用戶隱形 | 75% 用戶非英語，95% 技能只有英文 | 內部審計 242 技能 | Skills Triggering |
| Agent 黑箱不透明 | 透明度是企業採用 AI 第三大障礙 | Deloitte 2026 | Skill Reporting |
| 狀態失憶 | #1 生產殺手 | VentureBeat Q2 2026 | Vector Memory |
| 基建管道吞噬開發時間 | 77% 團隊花 >30% 時間 | VentureBeat 企業 AI 調查 | 四件套整體 |

---

## 🏗️ 四層互補

```
🌐 Skills Triggering（發現層）
    │  讓技能被正確發現
    │
    ▼
🔀 Skill Router（路由層）
    │  讓任務匹配正確技能
    │
    ▼
📊 Skill Reporting（透明度層）
    │  讓每一步都透明可見
    │
    ▼
🧠 Vector Memory（基礎層）
    │  讓 Agent 記住一切
    │
```

---

## 🚀 快速開始

每個項目都是獨立技能，可單獨安裝使用。見各項目 SKILL.md。

---

## 📊 綜合效果（UltraClaw 自用數據）

| 指標 | 無四件套 | 有四件套 | 改善 |
|------|---------|---------|------|
| 技能發現率 | ~35% | ~90% | +157% |
| 中文用戶匹配率 | ~20% | ~95% | +375% |
| Agent 透明度 | 0% | 100% | ∞ |
| 跨 Session 記憶保留 | 0% | >95% | ∞ |
| 任務啟動回合數 | 3-5 | 1 | -60% |

---

## 📄 授權

MIT — 自由使用、修改、分發。

## 🌟 關於

這四個項目來自 **UltraClaw**——一個在實戰中迭代了 6 個月的 AI 助理系統。每個方案都經歷過踩坑、修復、驗證的完整循環。

我們相信：**好工具來自真實的痛點，而非憑空設計。**
