# 🩺 Agentic Infrastructure 技能自查指南

> **每個技能都有一個「自查提示詞」。複製 → 貼給你的 Agent → 它會自動檢查該技能是否正確安裝、初始化、適配你的系統。**

---

## 使用方法

1. 安裝八件套後，打開你的 Agent
2. 從下方挑選你想檢查的技能，複製該技能的自查提示詞
3. 貼給 Agent → 它會執行檢查並回報結果
4. 建議首次使用時，按順序從 ⑧ 到 ① 全部檢查一遍

---

## ⑧ agentic-infra — 統一入口

```markdown
## 自查：Agentic Infra（統一入口）

請執行以下檢查：

### 安裝檢查
1. 確認 `skills/agentic-infra/SKILL.md` 存在
2. 讀取該文件，確認包含「Bootstrap Pipeline」和「6-Step」字樣
3. 驗證 description 欄位包含中文關鍵詞（初始化/bootstrap/基礎建設）

### 初始化檢查
1. 確認 `skills/skill-curator/SKILL.md` 存在且可讀取
2. 確認 `skills/skill-router/SKILL.md` 存在且可讀取
3. 確認 `skills/skills-triggering/SKILL.md` 存在且可讀取
4. 確認 `skills/vector-memory/SKILL.md` 存在且可讀取
5. 確認 `skills/skill-reporting/SKILL.md` 存在且可讀取
6. 確認 `skills/agent-evolver/SKILL.md` 存在且可讀取

### 適配檢查
1. 掃描你的技能庫目錄，列出所有已安裝的技能
2. 檢查技能數量是否 > 0
3. 如果已安裝全部 7 子技能，回報「Agentic Infrastructure 完整安裝」

### 通過標準
- 全部 7 子技能可讀取 → ✅ 通過
- 有缺失 → 列出缺失清單 + 安裝指令
```

---

## ⑦ agent-previsor — 事前預判

```markdown
## 自查：Agent Previsor（事前預判）

### 安裝檢查
1. 確認 `skills/agent-previsor/SKILL.md` 存在
2. 讀取該文件，確認包含「Pre-mortem」和「多情境路徑預判」字樣

### 功能檢查
1. 模擬場景：你接到一個複雜任務「遷移數據庫從 MySQL 到 PostgreSQL」
2. 載入 agent-previsor → 展開 3 條執行路徑
3. 每條路徑列出：瓶頸、踩坑、浪費、風險評分
4. 輸出最優路徑推薦

### 通過標準
- 能展開 ≥3 條路徑 → ✅ 通過
- 每條路徑都有風險評分 → ✅ 完整
```

---

## ⑥ agent-evolver — 自我進化

```markdown
## 自查：Agent Evolver（自我進化）

### 安裝檢查
1. 確認 `skills/agent-evolver/SKILL.md` 存在
2. 讀取該文件，確認包含「月度自省」和「核心文件範圍」

### 初始化檢查
1. 檢查是否有月度進化排程（cron job）
2. 如果沒有，建立一個（每月 1 號執行）

### 功能檢查
1. 掃描你的核心文件（AGENTS.md / RULES.md / SOUL.md / PERMANENT-RULES.md）
2. 檢查是否有過時規則（>90 天未更新且與當前方向衝突）
3. 列出建議：保留 / 更新 / 刪除

### 通過標準
- 月度排程已建立 → ✅
- 核心文件掃描完成 → ✅
```

---

## ⑤ skill-curator — 技能策展

```markdown
## 自查：Skill Curator（技能策展）

### 安裝檢查
1. 確認 `skills/skill-curator/SKILL.md` 存在
2. 確認 `skills/skill-curator/scripts/scan_all.py` 存在（可選）

### 功能檢查
1. 掃描你技能庫中的所有技能
2. 按三級健康度分類：🔴致命 / 🟡警告 / 🟢健康
3. 對於缺少中文關鍵詞的技能，自動注入
4. 輸出健康報告

### 通過標準
- 技能掃描完成 → ✅
- 健康報告輸出 → ✅
- 缺少中文關鍵詞的技能已修復 → ✅
```

---

## ④ vector-memory — 向量記憶

```markdown
## 自查：Vector Memory（向量記憶）

### 安裝檢查
1. 確認 `skills/vector-memory/SKILL.md` 存在
2. 確認 `skills/vector-memory/setup.sh` 存在
3. 確認 Qdrant 已安裝（檢查 `curl http://localhost:6333/`）

### 初始化檢查
1. 如果 Qdrant 未運行 → 執行 setup.sh
2. 檢查 collection 是否存在
3. 嘗試寫入一條測試記憶 → 搜索驗證

### 適配檢查
1. 檢查你的技能目錄中是否有記憶文件（memory/daily/ 等）
2. 如果有 → 建議執行 auto_sync 建立初始索引
3. 如果沒有 → 系統會在運行後自動建立

### 通過標準
- Qdrant alive → ✅
- Collection 存在 → ✅
- 讀寫測試通過 → ✅
```

---

## ③ skill-reporting — 技能使用追蹤

```markdown
## 自查：Skill Reporting（技能使用追蹤）

### 安裝檢查
1. 確認 `skills/skill-reporting/SKILL.md` 存在
2. 讀取該文件，確認追蹤機制說明

### 功能檢查
1. 回到本對話的開頭，檢查你的回覆末尾是否附帶了技能使用信息
2. 格式應為：`> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）`
3. 如果沒有 → 從現在開始，每次回覆末尾附加

### 通過標準
- 每次回覆都附帶技能使用信息 → ✅ 已啟動
```

---

## ② skill-router — 技能路由

```markdown
## 自查：Skill Router（技能路由）

### 安裝檢查
1. 確認 `skills/skill-router/SKILL.md` 存在
2. 讀取該文件，確認包含「4類×10階段」路由矩陣

### 功能檢查
1. 模擬場景：我說「幫我寫一個網站」
2. 你必須：① 讀取 skill-router → ② 分類為 💻代碼 + 🎨設計 → ③ 推薦 frontend-design + design-taste-frontend
3. 模擬場景：我說「幫我調研一隻港股」
4. 你必須：① 讀取 skill-router → ② 分類為 💰金融 + 🔍搜索 → ③ 推薦 ak-hk-stock-dd

### 通過標準
- 兩個場景都正確路由 → ✅ 通過
- 任何一個跳過路由 → ❌ 不通過，需強制執行 R0 規則
```

---

## ① skills-triggering — 技能觸發

```markdown
## 自查：Skills Triggering（技能觸發）

### 安裝檢查
1. 確認 `skills/skills-triggering/SKILL.md` 存在
2. 讀取該文件，確認包含「三層關鍵詞策略」

### 功能檢查
1. 列出你技能庫中所有技能的 description
2. 檢查每個技能是否至少有 3 個中文關鍵詞
3. 標記缺少中文關鍵詞的技能
4. 對於缺失的，推斷合適的中文關鍵詞並建議注入

### 通過標準
- 全部技能掃描完成 → ✅
- 缺失清單已列出 → ✅
- 修復建議已生成 → ✅
```

---

## 🆕 skill-compliance — 技能合規檢查（常駐技能 · 門禁對）

```markdown
## 自查：Skill Compliance Checker（技能合規檢查）

### 安裝檢查
1. 確認 `skills/skill-compliance/SKILL.md` 存在
2. 讀取該文件，確認包含「子代理隔離」和「字串比對」字樣

### 功能檢查
1. 執行一次模擬任務
2. skill-router 輸出 required_skills = [skill-A, skill-B]
3. spawn skill-compliance 子代理
4. 輸入 required_skills 和 actual_calls
5. 驗證：只輸出 PASS 或 REJECT，無其他內容

### 通過標準
- 子代理 spawn 成功 → ✅
- 輸出只有 PASS 或 REJECT → ✅
- 缺失技能時正確 REJECT → ✅
```

---

## 🔄 全部技能一鍵自查

複製以下全部內容給你的 Agent，一次檢查全部 9 個技能：

<details>
<summary>📋 一鍵全部自查（點擊展開）</summary>

```
請對 Agentic Infrastructure 所有已安裝的技能執行全面自查：

對以下每個技能，依次執行：
1. 安裝檢查：確認 SKILL.md 存在且可讀取
2. 初始化檢查：確認必要的依賴和配置
3. 適配檢查：確認技能與當前系統兼容

技能清單（按優先級）：
⑧ agentic-infra     — 統一入口
② skill-router      — 技能路由（常駐）
🆕 skill-compliance — 技能合規（常駐）
④ vector-memory     — 向量記憶
① skills-triggering — 技能觸發
⑤ skill-curator     — 技能策展
③ skill-reporting   — 技能使用追蹤
⑥ agent-evolver     — 自我進化
⑦ agent-previsor    — 事前預判

輸出格式：
```
🩺 Agentic Infrastructure 自查報告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⑧ agentic-infra:     ✅ 通過 / ❌ [問題]
② skill-router:      ✅ 通過 / ❌ [問題]
🆕 skill-compliance: ✅ 通過 / ❌ [問題]
④ vector-memory:     ✅ 通過 / ❌ [問題]
① skills-triggering: ✅ 通過 / ❌ [問題]
⑤ skill-curator:     ✅ 通過 / ❌ [問題]
③ skill-reporting:   ✅ 通過 / ❌ [問題]
⑥ agent-evolver:     ✅ 通過 / ❌ [問題]
⑦ agent-previsor:    ✅ 通過 / ❌ [問題]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
未通過項目修復建議：[...]
```
```
</details>
