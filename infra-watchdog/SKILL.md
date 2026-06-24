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

每次巡查按以下清單逐項檢查 7 件套 + enforcer 插件：

| # | 組件 | 檢查方式 | 通過標準 | 失敗時建議 |
|---|------|---------|---------|-----------|
| ① | skill-router | SKILL.md 存在 + 路由矩陣完整 | 文件可讀 + 含4類×10階段 | 重新安裝 |
| ② | vector-memory | curl localhost:6333/healthz | HTTP 200 | 見 STEP-BY-STEP 第 4 步 |
| ③ | skill-curator | 技能 description 含 CJK 比例 | >80% | 見 STEP-BY-STEP 第 1 步 |
| ④ | agent-evolver | 進化排程存在 | cron 或提醒已設定 | 見 STEP-BY-STEP 第 6 步 |
| ⑤ | agent-previsor | SKILL.md 存在 | 文件可讀 | 重新安裝 |
| ⑥ | agentic-infra | BOOTSTRAP.md 或 STEP-BY-STEP.md 存在 | 文件可讀 | 重新安裝 |
| ⑦ | infra-watchdog | 本 SKILL.md 存在 | 文件可讀 | 重新安裝 |
| ⑧ | infra-enforcer（插件） | `memory/skill-compliance/audit.jsonl` 最近 24h 有記錄 | 有近期 verdict 記錄 | 重啟 gateway；查 enforcer 是否載入 |

> v2（2026-06-24）：巡查對象從 9 項精簡為 7 件套 + enforcer。
> skills-triggering（併入 curator 的 CJK 檢查）、skill-compliance + skill-reporting
>（併入 enforcer 的 audit.jsonl 檢查）已移除。

---

## 📊 輸出格式

巡查完成後輸出以下格式的報告：

```
🩺 Infra Watchdog 巡查報告（7 件套 + enforcer）
📅 日期：YYYY-MM-DD
━━━━━━━━━━━━━━━━━━━━━━━━━━
① skill-router:      ✅ 正常
② vector-memory:     ✅ 正常 (Qdrant alive, 399 pts)
③ skill-curator:     🔴 需關注 — CJK 覆蓋率 53%（目標 >80%）
④ agent-evolver:     ✅ 正常
⑤ agent-previsor:    ✅ 正常
⑥ agentic-infra:     ✅ 正常
⑦ infra-watchdog:    ✅ 正常
⑧ infra-enforcer:    ✅ audit.jsonl 近 24h 有 5 筆記錄
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 建議修復：
  ③ → 執行 STEP-BY-STEP 第 1 步（技能健康掃描）
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
