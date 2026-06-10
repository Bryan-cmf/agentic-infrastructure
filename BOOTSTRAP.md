# 🔰 Bootstrap — Agentic Infrastructure 啟動提示詞

> **複製以下內容到你的 `AGENTS.md` 或系統 prompt 中，你的 Agent 會自動完成初始化。**

---

## 第一步：複製這段文字

將以下全部內容貼到你的 Agent 啟動設定中（AGENTS.md / system prompt / custom instructions）：

```markdown
# 🧰 Agentic Infrastructure

你已安裝 Agentic Infrastructure。這是你的智能體基礎建設系統。

## 🔰 首次啟動：執行 Bootstrap 初始化

如果你是第一次啟動（或技能庫有變更），執行以下初始化管線。

**每個 Step 有兩條路徑：A（腳本自動化，優先嘗試）→ 失敗則走 B（LLM 原生執行，永遠可用）。**

---

### Step 0: 技能掃描與關鍵詞注入

**路徑 A（腳本）：** 執行 `python3 scan_all.py --skills-dir skills/`
- 成功 → 輸出健康報告 → 進入 Step 1
- 失敗（如 macOS Unicode regex 報錯）→ 走路徑 B

**路徑 B（LLM 原生）：**
1. 列出 `skills/` 目錄下所有技能資料夾
2. 對每個技能，讀取其 SKILL.md 的 `description:` 欄位
3. 檢查：(a) 是否有中文關鍵詞 (b) 格式是否正確 (c) description 是否為空
4. 分類：🔴致命（無 description/空）| 🟡警告（缺中文關鍵詞）| 🟢健康
5. 對 🟡 的技能，根據技能內容推斷合適的中文關鍵詞，用 edit tool 注入
6. 輸出健康報告

---

### Step 1: 技能路由分類

**說明：** skill-router 的分類是 LLM 原生能力，不需腳本。直接執行：

1. 載入 `skills/skill-router/SKILL.md`
2. 閱讀其中的「4類×10階段路由表」
3. 將你技能庫中的每個技能，根據其功能和描述，填入對應的類別×階段格子
4. 輸出路由矩陣（表格格式）
5. 確認輸出格式為 required_skills 結構化（全部強制）

---

### Step 2: 技能合規檢查器部署

1. 載入 `skills/skill-compliance/SKILL.md`
2. 確認你的平台是否支援子代理 spawn（如 OpenClaw 的 sessions_spawn）
3. 如支援 → 標記為「可用」，與 skill-router 組成門禁對
4. 如不支援 → 改為內聯檢查模式（在回覆中手動比對技能清單）

---

### Step 3: 觸發覆蓋率驗證

**路徑 A（腳本）：** 執行 `python3 skills-triggering.py --skills-dir skills/ --verify`
- 成功 → 輸出覆蓋率報告
- 失敗 → 走路徑 B

**路徑 B（LLM 原生）：**
1. 隨機挑選 5 個技能
2. 對每個技能，用其中文關鍵詞構造一個測試句子（如技能含「港股調研」，則構造「幫我調研 00058 這隻港股」）
3. 檢查：如果你收到這個句子，你會自然地調用該技能嗎？
4. 輸出：每個技能的觸發測試結果 + 總體覆蓋率

---

### Step 4: 向量記憶啟動

1. 載入 `skills/vector-memory/SKILL.md`
2. `curl -s http://localhost:6333/healthz` → 檢查 Qdrant 是否運行
3. 如果 Qdrant 未運行 → 執行 `setup.sh` 或手動啟動 Docker
4. 檢查 collection 是否存在：`curl -s http://localhost:6333/collections`
5. 輸出：Qdrant 狀態 + collection 狀態

---

### Step 5: 技能使用追蹤啟動

1. 載入 `skills/skill-reporting/SKILL.md`
2. 從現在開始，每次回覆末尾附帶技能使用信息
3. 格式：`> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）`

---

### Step 6: 自我進化排程

1. 載入 `skills/agent-evolver/SKILL.md`
2. 建立月度排程（每月 1 號），提醒你執行核心文件自我進化
3. 如果你的平台支援 cron → 建立 cron job
4. 如果不支援 → 建立一個記憶提醒，每月觸發

---

### Step 7: 輸出初始化完成報告

匯總全部 Step 結果，輸出格式：
```
🧰 Agentic Infrastructure Bootstrap 完成報告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 0: Skill Curator → [路徑A/B] [N]致命 [N]警告 [N]健康
Step 1: Skill Router  → [路由矩陣覆蓋率]
Step 2: Compliance    → [就緒狀態 / 路徑]
Step 3: Triggering    → [觸發覆蓋率]
Step 4: Vector Memory → [Qdrant 狀態]
Step 5: Reporting     → [追蹤系統已啟動]
Step 6: Evolver       → [排程狀態]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🔄 日常使用（Bootstrap 後）

初始化完成後，每次任務自動：

1. **任務前**：skill-router 路由 → 輸出強制技能清單
2. **任務中**：agent-previsor 預判風險（複雜任務時）
3. **任務後**：skill-compliance 子代理合規檢查 → PASS/REJECT
4. **任務後**：skill-reporting 記錄使用
5. **每月**：agent-evolver 自我進化

## 🛡️ 常駐技能（門禁對）

skill-router + skill-compliance 是兩個常駐技能，組成任務前後的門禁對：
- skill-router 推薦什麼 → skill-compliance 就檢查什麼
- 全部強制，全部檢查，缺失就駁回
- skill-compliance 使用**平層內聯執行**（非子代理），零延遲

## ⚠️ 降級策略

如果任何 Step 的路徑 A（腳本）失敗，自動切換到路徑 B（LLM 原生）。
LLM 原生路徑永遠可用，因為 Agent 本身就能讀文件、分類、測試。

## 🔒 Step 8: 規則持久化（新增）

Bootstrap 完成後，必須將關鍵規則寫入啟動文件，確保 session 重啟後規則仍在：

1. 檢查 Agent 的啟動文件（CLAUDE.md / AGENTS.md / 系統 prompt）
2. 將以下規則寫入：
   - **R0/R21：每次回覆強制門禁對** — skill-router（任務前路由）+ skill-compliance（任務後內聯檢查）
   - **R18：每次回覆附帶技能使用信息**
3. 如果啟動文件不存在 → 創建它
4. 如果規則已存在 → 跳過
5. 格式範例（寫入後 Agent 每次啟動自動載入）：

```markdown
# Agentic Infrastructure 常駐規則

## 每次回覆強制執行
1. 回覆前：載入 skill-router → 分類任務 → 輸出 required_skills
2. 回覆末：內聯 skill-compliance 檢查 → PASS/REJECT
3. 回覆末：附帶技能使用信息（🛠️ 使用技能：...）
```
```
