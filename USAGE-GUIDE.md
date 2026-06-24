# 🚀 Agentic Infrastructure 十件套 — 完整使用指南

> ⚠️ **v2 更新（2026-06-24）**：本文檔反映 v1 十件套結構。v2 已精簡為**七件套 + infra-enforcer 插件**：`skills-triggering`（併入 curator）、`skill-compliance` + `skill-reporting`（併入 infra-enforcer）已移除。本文檔中提及這三個技能的部分請以 [`README.md`](./README.md) 的 v2 結構為準。


> **從安裝到體驗，一步步引導你與 Agent 建立深度協作。**

---

## 🔰 Phase 0: Agentic Infra — 一鍵 Bootstrap 初始化（新增 ⭐）

### 為什麼要有 Phase 0？

以前用戶安裝十件套後，每個技能各自獨立，用戶不知道下一步。**現在有了統一入口。**

### 0.1 安裝

```bash
mkdir -p skills/agentic-infra && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agentic-infra/SKILL.md -o skills/agentic-infra/SKILL.md
```

### 0.2 初始配置提示詞

將 [`BOOTSTRAP.md`](./BOOTSTRAP.md) 的全部內容複製到你的 `AGENTS.md` 中。

### 0.3 體驗提示詞

> **執行 Bootstrap 初始化**

Agent 會自動執行 7-Step 初始化管線：

```
Step 0: Skill Curator      → 掃描技能庫 + 注入中文關鍵詞 + 修復格式
Step 1: Skill Router       → 將技能分類到 4類×10階段 路由矩陣
Step 2: Skill Compliance   → 部署合規檢查器
Step 3: Skills Triggering  → 測試關鍵詞覆蓋率 + 補強觸發盲區
Step 3.5: Core Doc Hardening → 加固5個核心文檔（嵌入 INFRA-MANDATE 門禁）🆕
Step 4: Vector Memory      → 啟動 Qdrant + 建立初始索引
Step 5: Skill Reporting    → 掛載技能使用追蹤
Step 6: Agent Evolver      → 建立月度自我進化排程
Step 7: 輸出初始化完成報告
```

**一分鐘內，你的 Agent 基礎建設完成。**

---

## 📋 手動安裝順序（如需逐個安裝）

```
Phase 0: 編排層 → Bootstrap 初始化 + 統一入口（🆕 十件套新增）
Phase 1: 基礎層 → 讓 Agent 記住一切
Phase 2: 發現層 → 讓技能能被觸發
Phase 3: 路由層 → 讓任務匹配技能
Phase 4: 透明度層 → 讓每一步可見
Phase 5: 維護層 → 清理和調適現有技能
Phase 6: 進化層 → 核心文件自我進化（含加固）
Phase 7: 預判層 → 事前預見所有坑
```

**為什麼是這個順序？**

- **沒有編排**（Phase 0），各技能各自獨立，用戶不知道下一步 → 🆕 Agentic Infra 解決
- **沒有記憶**（Phase 1），Agent 每次從零開始，其他技能都白搭
- **沒有觸發**（Phase 2），技能裝了也用不上
- **沒有路由**（Phase 3），Agent 不知道什麼時候用哪個技能
- **沒有透明度**（Phase 4），你不知道 Agent 做了什麼
- **沒有維護**（Phase 5），技能越裝越多但越來越亂
- **沒有進化**（Phase 6），核心文件越來越臃腫
- **沒有預判**（Phase 7），每次都在事後才發現問題

---

## Phase 1: Vector Memory — 讓 Agent 記住一切

### 1.1 安裝

```bash
curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/vector-memory/setup.sh | bash
```

### 1.2 初始配置提示詞

**複製貼給 Agent：**

```
請幫我配置 Vector Memory 技能。

1. 確認 Qdrant 已啟動（docker ps | grep qdrant）
2. 測試記憶寫入：mem_save("測試記憶", collection="openclaw_mem")
3. 測試記憶搜尋：mem_search("測試", collection="openclaw_mem")
4. 如果都成功，告訴我「Vector Memory 已就緒」
```

### 1.3 體驗提示詞

**讓 Agent 展示記憶能力：**

```
請用 Vector Memory 記住以下三件事：
1. 我最喜歡的顏色是藍色
2. 我討厭重複性工作
3. 我希望 Agent 主動預判風險

然後搜尋「我最喜歡什麼」，看看你能不能找到。
```

**預期體驗：** Agent 能準確回憶你剛才告訴它的三件事，證明記憶系統運作正常。

---

## Phase 2: Skills Triggering — 讓技能能被觸發

### 2.1 安裝

```bash
mkdir -p skills/skills-triggering && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skills-triggering/SKILL.md -o skills/skills-triggering/SKILL.md
```

### 2.2 初始配置提示詞

```
請幫我執行 Skills Triggering 的批量修復。

1. 讀取 skills/skills-triggering/SKILL.md
2. 執行批量關鍵詞注入腳本（如果有的話）
3. 或者手動為以下技能加入中文關鍵詞：
   - software-architect → 架構設計 系統設計 軟件架構
   - caveman → 簡化設計 降級方案 最簡單方案
   - diagnose → 故障診斷 根因分析 Debug
4. 完成後告訴我「已修復 N 個技能」
```

### 2.3 體驗提示詞

**測試中文觸發：**

```
幫我設計一個系統架構。

（觀察 Agent 是否自動調用了 software-architect 技能）
```

**預期體驗：** Agent 應該在回覆末尾附帶「> 🛠️ 使用技能：software-architect（系統架構設計）」，證明中文關鍵詞生效。

---

## Phase 3: Skill Router — 讓任務匹配技能

### 3.1 安裝

```bash
mkdir -p skills/skill-router && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-router/SKILL.md -o skills/skill-router/SKILL.md
```

### 3.2 初始配置提示詞

```
請幫我配置 Skill Router。

1. 讀取 skills/skill-router/SKILL.md
2. 確認 AGENTS.md 中已有 Step -2: SKILL-ROUTER PRE-CHECK
3. 確認 RULES.md 中已有 R0: SKILL-ROUTER PRE-CHECK
4. 測試路由：我說「幫我調研 00058」，你應該先經過 skill-router，然後推薦 ak-hk-stock-dd
```

### 3.3 體驗提示詞

**測試路由準確性：**

```
幫我調研 00058 這隻港股。

（觀察 Agent 是否先經過 skill-router，然後推薦 ak-hk-stock-dd 技能）
```

**預期體驗：** Agent 應該在回覆開頭說「🔀 Router：💰金融 + 🔍搜索 → 推薦 ak-hk-stock-dd」，然後開始執行調研。

---

## 🛡️ Phase 3.5: Core Doc Hardening — 核心文檔加固（🆕 新增）

> **為你的 Agent 建立不可跳過的強制性基礎設施門禁。**

### 為什麼需要這個步驟？

即使你安裝了全部十件套，Agent 仍可能「選擇性忘記」加載它們。LLM 有天然的摘要本能——它會優化掉看似重複的步驟。

**解決方案：** 將基礎設施加載提示嵌入每一個核心文檔的頂部，使得無論 Agent 先讀到哪個文件，第一眼就看到強制門禁。

### 3.5.1 觸發方式

| 方式 | 指令 |
|------|------|
| Bootstrap 自動 | agentic-infra Step 3.5 自動執行 |
| 手動 | `請執行核心文檔加固` 或 `請 hardening 我的 agent 文檔` |

### 3.5.2 初始配置提示詞

**複製貼給 Agent：**

```
請執行 agent-evolver Phase 0: Core Document Hardening。

步驟：
1. 掃描我的 5 個核心文檔（AGENTS.md, SOUL.md, RULES.md, PERMANENT-RULES.md, MEMORY.md）
2. 診斷是否存在以下問題：
   - 🔴 致命：沒有強制性門禁機制（如 AGENTS.md 無 Pre-Response Gate）
   - 🟡 警告：規則散落，無中央速查表
   - 🟡 警告：SOUL.md 無強制輸出結構
   - 🟡 警告：MEMORY.md 與 daily logs 無雙寫強制規則
3. 在每個核心文檔頂部插入統一的 INFRA-MANDATE 區塊
4. 備份原文件（.bak-日期）
5. 驗證所有修改，輸出加固報告
```

### 3.5.3 INFRA-MANDATE 模板

這是會插入每個核心文檔頂部的強制門禁區塊：

```markdown
## 🔴 INFRA-MANDATE — 基礎設施十件套常態化加載

每條訊息前: skill-router（查路由表）→ skill-compliance（合規檢查）→ skill-reporting（回報）
複雜任務前: + agent-previsor（多路徑預判）
寫入後:     + vector-memory（雙寫強制，mem_save）
每日自動:   infra-watchdog（巡檢）
每月自動:   agent-evolver（自省）+ skill-curator（策展）
初始化:     agentic-infra（Bootstrap 統一入口）
技能觸發:   skills-triggering（跨語言關鍵詞注入）

⚠️ 以上十件套是基礎設施，不是「可選技能」。跳過任一件 = 違反 INFRA-MANDATE。
```

### 3.5.4 加固前後對比

| 文件 | 加固前 | 加固後 |
|------|--------|--------|
| AGENTS.md | Gate 存在但無統一標語 | ✅ INFRA-MANDATE 在頂部 |
| SOUL.md | 僅 Router 結構 | ✅ INFRA-MANDATE 嵌入人格定義 |
| RULES.md | 有規則但無頂部門禁 | ✅ INFRA-MANDATE 在 R0 之前 |
| PERMANENT-RULES.md | 規則詳細但分散 | ✅ INFRA-MANDATE 最高優先級 |
| MEMORY.md | infra 引用分散 | ✅ INFRA-MANDATE 在頂部 |

### 3.5.5 預期效果

加固後，無論 Agent 先打開哪個核心文件，第一眼看到的都是：

> 🔴 INFRA-MANDATE: 基礎設施十件套常態化加載。不能跳過。

這不是建議，是結構性強制。LLM 的摘要本能無法繞過物理上反覆出現的門禁。

### 3.5.6 注意事項

| ⚠️ 注意 | 說明 |
|----------|------|
| **先備份** | 加固腳本會自動備份（.bak-日期），但建議手動也備份 |
| **不刪內容** | 加固只重組結構、插入門禁，不刪除任何現有內容 |
| **用戶審批** | 對 🟡 警告級別的問題，Agent 會提案，等用戶確認才修改 |
| **完成後驗證** | 確保每個文件頂部都有 INFRA-MANDATE，且 infra 引用數增加 |
| **不是一次性** | 加固後，agent-evolver 每月自動檢查核心文檔是否需要再次加固 |

---

## Phase 4: Skill Reporting — 讓每一步可見

### 4.1 安裝

```bash
mkdir -p skills/skill-reporting && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-reporting/SKILL.md -o skills/skill-reporting/SKILL.md
```

### 4.2 初始配置提示詞

```
請幫我配置 Skill Reporting。

1. 讀取 skills/skill-reporting/SKILL.md
2. 確認 RULES.md 中已有 R18: 每次回覆附帶技能使用信息
3. 格式：> 🛠️ 使用技能：skill-A（用途）+ skill-B（用途）
4. 測試：你接下來的每次回覆都應該附帶技能使用信息
```

### 4.3 體驗提示詞

**測試透明度：**

```
幫我分析阿里巴巴的財務狀況。

（觀察 Agent 是否在回覆末尾附帶技能使用信息）
```

**預期體驗：** Agent 回覆末尾應該有「> 🛠️ 使用技能：ak-financial-analyst（財務分析）+ tavily-search（市場搜索）+ web_fetch（年報下載）」，讓你知道它用了哪些工具。

---

## Phase 5: Skill Curator — 清理和調適現有技能

### 5.1 安裝

```bash
mkdir -p skills/skill-curator && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-curator/SKILL.md -o skills/skill-curator/SKILL.md
```

### 5.2 初始配置提示詞

```
請幫我執行 Skill Curator 的全量掃描。

1. 讀取 skills/skill-curator/SKILL.md
2. 執行 scan_all.py 掃描所有技能
3. 告訴我：
   - 總共多少個技能
   - 多少個致命問題（無 description）
   - 多少個警告（缺中文關鍵詞）
   - 多少個健康
4. 然後自動修復所有可以自動修復的問題
```

### 5.3 體驗提示詞

**測試策展能力：**

```
請幫我做一次技能策展。

1. 掃描所有技能
2. 診斷問題
3. 自動修復
4. 生成策展報告
5. 告訴我修復了多少個技能
```

**預期體驗：** Agent 應該輸出類似「📊 總計 125 個技能 | 🔴致命 6 | 🟡警告 55 | 🟢健康 64 → 修復後：🟢健康 124」的報告。

---

## Phase 6: Agent Evolver — 核心文件自我進化

### 6.1 安裝

```bash
mkdir -p skills/agent-evolver && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-evolver/SKILL.md -o skills/agent-evolver/SKILL.md
```

### 6.2 初始配置提示詞

```
請幫我配置 Agent Evolver。

1. 讀取 skills/agent-evolver/SKILL.md
2. 確認 Cron job 已建立（每月 1 號 09:00 HKT）
3. 手動觸發一次進化報告：/evolve
4. 告訴我核心文件的增長趨勢和過時內容
```

### 6.3 體驗提示詞

**測試進化能力：**

```
請幫我執行一次 Agent 自我進化。

1. 掃描所有核心文件（SOUL、AGENTS、USER、MEMORY、RULES、PERMANENT-RULES）
2. 計算增長趨勢
3. 識別過時內容
4. 生成進化報告
5. 告訴我哪些規則可能需要更新
```

**預期體驗：** Agent 應該輸出「🧬 Agent 自我進化報告」，包含核心文件增長趨勢、過時內容清單、建議行動。

---

## Phase 7: Agent Previsor — 事前預見所有坑

### 7.1 安裝

```bash
mkdir -p skills/agent-previsor && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/agent-previsor/SKILL.md -o skills/agent-previsor/SKILL.md
```

### 7.2 初始配置提示詞

```
請幫我配置 Agent Previsor。

1. 讀取 skills/agent-previsor/SKILL.md
2. 確認複雜任務會自動觸發預判
3. 測試：我給一個複雜任務，你應該先做 Pre-mortem 分析
```

### 7.3 體驗提示詞

**測試預判能力：**

```
幫我設計一個完整的港股調研系統，包含：
- 年報自動提取
- 持股數據分析
- 財務指標計算
- 風險評估
- 報告生成

請先做 Pre-mortem 分析，告訴我所有可能的坑和最優路徑。
```

**預期體驗：** Agent 應該先輸出「🔮 Pre-mortem 路徑分析」，展開 3-5 條可能路徑，每條進行瓶頸/踩坑/浪費/風險四維度預判，然後推薦最優路徑。

---

## 🎯 完整體驗流程（一次性測試）

**如果你想一次性測試所有七個技能，複製這段提示詞：**

```
請幫我完成 Agentic Infrastructure 十件套的完整體驗。

1. **Vector Memory** — 記住「我最喜歡的顏色是藍色」，然後搜尋驗證
2. **Skills Triggering** — 幫我設計系統架構（測試中文觸發）
3. **Skill Router** — 幫我調研 00058（測試路由）
4. **Skill Reporting** — 分析阿里巴巴財務（測試透明度）
5. **Skill Curator** — 做一次技能策展（測試維護）
6. **Agent Evolver** — 執行一次自我進化（測試進化）
7. **Agent Previsor** — 設計港股調研系統前先做預判（測試預判）

每個步驟完成後告訴我「✅ Phase N 完成」，最後給我一個總結報告。
```

---

## 📊 預期成果

完成十件套配置後，你的 Agent 將具備：

| 能力 | 說明 |
|------|------|
| 🧠 **永不失憶** | 跨 Session 記憶保留 >95% |
| 🌐 **多語言觸發** | 中文/日文/韓文/阿文/印地文技能觸發率 95%+ |
| 🔀 **智能路由** | 任務→技能匹配準確率 90%+ |
| 📊 **完全透明** | 每次回覆附帶技能使用信息 |
| 🎨 **技能健康** | 技能健康度 99%+ |
| 🧬 **自我進化** | 核心文件月度自省，避免臃腫 |
| 🔮 **事前預判** | 複雜任務先預判所有坑 |

---

## 🆘 常見問題

**Q: 安裝順序可以打亂嗎？**

A: 可以，但建議按順序。Vector Memory 是基礎，沒有它其他技能的記憶功能都無法運作。

**Q: 我可以只安裝其中幾個嗎？**

A: 可以。建議至少安裝 Phase 1-4（記憶+觸發+路由+透明），這是核心體驗。

**Q: 安裝後沒有效果怎麼辦？**

A: 檢查 AGENTS.md 和 RULES.md 是否已更新。如果沒有，重新執行「初始配置提示詞」。

**Q: 十件套會互相衝突嗎？**

A: 不會。它們設計為互補：觸發→路由→透明→記憶→維護→進化→預判，形成完整閉環。

---

## 📚 更多資源

- **GitHub 倉庫：** https://github.com/Bryan-cmf/agentic-infrastructure
- **每個技能的完整文檔：** 見各技能的 SKILL.md
- **問題反饋：** GitHub Issues

---

*最後更新：2026-06-10*
