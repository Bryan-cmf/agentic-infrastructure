---
name: infra-watchdog
description: 基礎設施巡查 技能健康檢查 定時巡查 系統健康監控 技能維護 定期檢查 技能運作狀態 基础设施巡检 定期维护 Infra watchdog — scheduled health monitor for all Agentic Infrastructure skills. Runs weekly, checks all 9 skills, reports degradation, suggests fixes. Does NOT auto-fix — users decide what to repair.
---

# 🩺 Infra Watchdog — 基礎設施定時巡查員

## 概念

> **不是自動修復工具。是定時巡查員——檢查、報告、建議。修不修由你決定。**

每週自動巡查全部基礎設施技能的健康狀態。發現退化就報告，附上修復建議和對應的 STEP-BY-STEP 提示詞。用戶根據報告自己決定要不要修。

## 📥 一行安裝

```bash
mkdir -p skills/infra-watchdog && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/infra-watchdog/SKILL.md -o skills/infra-watchdog/SKILL.md
```

## 🔄 觸發方式

| 方式 | 說明 |
|------|------|
| 定時 | 建議每週一次（週一 09:00），用 cron 或平台排程 |
| 手動 | `巡查`、`健康檢查`、`基礎設施檢查`、`infra check` |

## 🩺 巡查清單

每次巡查按以下清單逐項檢查 9 個技能：

| # | 技能 | 檢查方式 | 通過標準 | 失敗時建議 |
|---|------|---------|---------|-----------|
| ① | skills-triggering | SKILL.md 存在且 description 含中文 | 文件可讀 | 重新安裝：見 STEP-BY-STEP 前置 |
| ② | skill-router | SKILL.md 存在 + 路由矩陣完整 | 文件可讀 + 含4類×10階段 | 重新安裝 |
| ③ | skill-reporting | 最近回覆有技能信息 | 回覆末尾有 `🛠️ 使用技能` | 見 STEP-BY-STEP 第 5 步 |
| ④ | vector-memory | curl localhost:6333/healthz | HTTP 200 | 見 STEP-BY-STEP 第 4 步 |
| ⑤ | skill-curator | 技能 description 含 CJK 比例 | >80% | 見 STEP-BY-STEP 第 1 步 |
| ⑥ | agent-evolver | 進化排程存在 | cron 或提醒已設定 | 見 STEP-BY-STEP 第 6 步 |
| ⑦ | agent-previsor | SKILL.md 存在 | 文件可讀 | 重新安裝 |
| ⑧ | agentic-infra | BOOTSTRAP.md 或 STEP-BY-STEP.md 存在 | 文件可讀 | 重新安裝 |
| ⑨ | skill-compliance | 最近回覆有內聯檢查 | 回覆末尾有 PASS/REJECT | 見 STEP-BY-STEP 第 3 步 |

---

## 📊 輸出格式

巡查完成後輸出以下格式的報告：

```
🩺 Infra Watchdog 巡查報告
📅 日期：YYYY-MM-DD
━━━━━━━━━━━━━━━━━━━━━━━━━━
① skills-triggering:  ✅ 正常
② skill-router:      ✅ 正常
③ skill-reporting:   ⚠️ 退化 — 最近 3 次回覆缺技能信息
④ vector-memory:     ✅ 正常 (Qdrant alive, 399 pts)
⑤ skill-curator:     🔴 需關注 — CJK 覆蓋率 53%（目標 >80%）
⑥ agent-evolver:     ✅ 正常
⑦ agent-previsor:    ✅ 正常
⑧ agentic-infra:     ✅ 正常
⑨ skill-compliance:  ⚠️ 退化 — 最近回覆缺 PASS/REJECT
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 建議修復：
  ⑤ → 執行 STEP-BY-STEP 第 1 步（技能健康掃描）
  ③ → 執行 STEP-BY-STEP 第 5 步（啟動技能追蹤）
  ⑨ → 執行 STEP-BY-STEP 第 3 步（部署合規檢查器）
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📋 定時巡查提示詞

設定每週 cron 時，使用以下提示詞：

```
執行 Infra Watchdog 巡查：

1. 載入 skills/infra-watchdog/SKILL.md
2. 按巡查清單逐一檢查 9 個基礎設施技能
3. 對每個技能：
   - 正常 → ✅
   - 退化 → ⚠️ 附具體症狀
   - 失效 → 🔴 附修復建議（引用 STEP-BY-STEP 對應步驟）
4. 輸出巡查報告（使用上述格式）

巡查完成後，不要自動修復。只報告，讓用戶決定。
```

---

## 🔴 原則

- **只巡查，不自動修** — 用戶決定要不要處理
- **每項都附修復路徑** — 退化項目必須引用 STEP-BY-STEP.md 對應步驟
- **可追溯** — 每次巡查報告保留在 memory 中，可對比歷史
- **不報假警** — 正常就是正常，不要為了「看起來有用」而標記假的警告

---

## 🔗 與其他技能的關係

```
infra-watchdog（巡查員 · 每週）
    │
    ├── 檢查 ①-⑨ 全部技能健康狀態
    ├── 發現退化 → 引用 STEP-BY-STEP 對應修復步驟
    └── 輸出報告 → 用戶決定
```
