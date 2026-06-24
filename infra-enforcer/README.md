# infra-enforcer — Gateway 合規強制插件

OpenClaw gateway 插件，全權負責基礎設施的合規評分與強制。取代了 v1 的
`skill-compliance`（模型自評，會作弊）和 `skill-reporting`（文字匯報，可偽造）。

## 機制（四個 hook）

| Hook | 觸發時機 | 動作 |
|------|---------|------|
| `before_prompt_build` | 每回合開始 | 把技能清單+路由表+規則注入 system prompt（軟推力） |
| `before_agent_finalize` | 回覆定案前 | 若無真實 Skill 呼叫 → `revise` 要求重答（最多 2 次，中層） |
| `agent_end` | 回合結束 | 程式讀 toolCall 紀錄評分 → 寫 `score.json`(history) + `audit.jsonl`；危險分數推 IM |
| `before_agent_run` | 下一次回合開始 | score ≤ 0 → block 整個 turn（硬閘門） |

**關鍵**：合規只認真實的 `Skill` 工具呼叫（`AssistantMessage.content` 裡
`type==="toolCall" && name==="Skill"` 的區塊），不認回覆文字裡的「🛠️」。

**維護任務豁免**：`trigger: "cron"` / `"heartbeat"` 的 turn（如 auto-memory-dream）
完全跳過強制——它們是系統內部維護，不該被 skill-mandate 約束。

## 安裝

1. 把本目錄加入 OpenClaw 的 `plugins.load.paths`：
   ```json
   "plugins": { "load": { "paths": ["/path/to/infra-enforcer"] } }
   ```
2. 在 `plugins.entries` 啟用並開啟 conversation hook 存取權：
   ```json
   "plugins": { "entries": { "infra-enforcer": {
     "enabled": true,
     "hooks": { "allowConversationAccess": true }
   } } }
   ```
3. 加入 `plugins.allow`：`["...", "infra-enforcer"]`
4. 重啟 gateway：`openclaw gateway restart`

> `allowConversationAccess: true` 是必須的——`before_agent_run` 和 `agent_end`
> 屬於 conversation hook，非 bundled 插件不設此旗標會被靜默丟棄。

## 設定（環境變數，可選）

| 變數 | 預設 | 說明 |
|------|------|------|
| `INFRA_ENFORCER_INITIAL_SCORE` | 5.0 | score.json 不存在時的初始分 |
| `INFRA_ENFORCER_DEATH_THRESHOLD` | 0 | block 閘門閾值 |
| `INFRA_ENFORCER_REVISE_MAX` | 2 | revise 重試上限 |
| `INFRA_ENFORCER_NOTIFY` | (on) | 設 `off` 關閉 IM 推送 |
| `INFRA_ENFORCER_NOTIFY_DANGER_SCORE` | 2.0 | 觸發 IM 推送的危險分數 |
| `INFRA_ENFORCER_NOTIFY_DAILY_CAP` | 3 | 每日 IM 推送上限 |

## 測試

```bash
node infra-enforcer/test-verify.js   # 33 個測試
```

## 檔案

- `index.js` — 插件主體（4 個 hook + IM 推送 + score/audit 寫入）
- `compliance.js` — 純評分邏輯（無 SDK 依賴，可獨立測試）
- `test-verify.js` — 單元測試
- `openclaw.plugin.json` / `package.json` — 插件 manifest
- `scripts/score_enforcer.py` — 唯讀查詢介面（`--status` / `--quick-check`）
- `scripts/skills-triggering.py` — CJK 關鍵詞審計/注入（curator 子功能，獨立可跑）
