---
name: vector-memory
description: 向量記憶 語義記憶 Agent記憶 持久記憶 記憶系統 跨Session記憶 ベクトルメモリ エージェント記憶 벡터메모리 에이전트기억 Vector memory — persistent semantic memory for AI agents. Never lose context again.
---

# 🧠 Vector Memory — 讓你的 Agent 不再失憶

## 📥 一行安裝

```bash
curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/vector-memory/setup.sh | bash
```

## 多語言簡介

**🇹🇼 繁中：** Qdrant 向量資料庫 + BGE-m3 嵌入——讓 Agent 記住一切，永不失憶。
**🇨🇳 簡中：** Qdrant 向量数据库 + BGE-m3 嵌入——让 Agent 记住一切，永不失忆。
**🇯🇵 日文：** QdrantベクトルDB + BGE-m3埋め込み——エージェントがすべてを記憶し、決して忘れない。
**🇰🇷 韓文：** Qdrant 벡터DB + BGE-m3 임베딩——에이전트가 모든 것을 기억하고 절대 잊지 않습니다.
**🇸🇦 阿文：** قاعدة بيانات Qdrant المتجهة + تضمين BGE-m3——الوكيل يتذكر كل شيء ولا ينسى أبداً.
**🇮🇳 印地：** Qdrant वेक्टर DB + BGE-m3 एम्बेडिंग——एजेंट सब कुछ याद रखता है, कभी नहीं भूलता।

---

## 痛點

> **Agent 重啟後完全失憶。每一次對話都從零開始。**

| 現象 | 根因 |
|------|------|
| Agent 每次都問「你是誰」「之前做到哪了」 | Session 隔離，沒有跨 Session 記憶 |
| 做了 6 小時的工作，第二天 Agent 完全不記得 | 對話上下文不持久化 |
| 用戶重複回答相同的問題 | Agent 不記得上次的對話 |
| Debug 困難——不知道 Agent 之前做了什麼決定 | 沒有審計追蹤 |

**市場數據：**

| 數據 | 來源 |
|------|------|
| 狀態失憶是 Agent 生產環境 #1 殺手 | VentureBeat Pulse Q2 2026 |
| 77% 團隊花 >30% 時間在基礎設施管道而非智能開發 | VentureBeat 企業 AI 調查 |
| 24% 故障來自幻覺傳播（Agent 忘記前面步驟的上下文） | VentureBeat Agentic Reckoning Report |
| 40% 專案因基礎設施問題在 2027 前被取消 | Gartner |
| 多 Agent Debug 耗時 3-5 倍於單 Agent | Zylos Research |

**開源生態的現狀：**

現有的 agentmemory 等方案主要為 Claude Code 等 Coding Agent 設計，對中文支援幾乎為零（我們實測 0% 檢索成功率）。社區缺乏一個**通用、輕量、多語言、開箱即用**的 Agent 記憶方案。

## 方案

### 架構

```
┌──────────────────────────────────────────────┐
│              向量記憶系統                      │
├──────────────────────────────────────────────┤
│                                              │
│  寫入層                                       │
│  ├─ Agent 對話自動捕獲 (MCP Server)            │
│  ├─ 文件系統掃描 (增量同步)                     │
│  └─ 雙寫強制 (file + vector 同步寫入)           │
│                                              │
│  存儲層                                       │
│  ├─ Qdrant 向量資料庫 (1024-dim COSINE)        │
│  ├─ BGE-m3 嵌入模型 (193MB, 中英文最優)         │
│  └─ 三層去重 (UUID5 + Offset + Jaccard)        │
│                                              │
│  檢索層                                       │
│  ├─ mem_search (語義搜尋)                      │
│  ├─ mem_federated (跨 Collection 搜尋)         │
│  ├─ mem_graph (知識圖譜)                       │
│  ├─ mem_time_travel (時間旅行)                 │
│  └─ mem_health (系統健康報告)                   │
│                                              │
│  固化層                                       │
│  ├─ auto-dream (夜間合併整理)                  │
│  ├─ mem_decay (遺忘曲線)                       │
│  ├─ mem_dedup (去重)                          │
│  └─ mem_contradict (矛盾檢測)                  │
│                                              │
└──────────────────────────────────────────────┘
```

### 一鍵部署

```bash
# 1. 啟動 Qdrant
docker compose up -d

# 2. 安裝依賴
pip install sentence-transformers qdrant-client

# 3. 啟動記憶服務
python3 mcp_server.py

# 4. 配置 OpenClaw Gateway（將 vector-memory MCP 加入 plugins）
```

---

## 功能矩陣

| 功能 | 工具 | 用途 |
|------|------|------|
| 語義搜尋 | `mem_search` | 「我們上週做的 OCR 項目進展如何？」 |
| 跨庫搜尋 | `mem_federated` | 一次搜尋所有 Collection |
| 知識圖譜 | `mem_graph` | 發現記憶之間的隱含關聯 |
| 時間旅行 | `mem_time_travel` | 「3 個月前我們在做什麼？」 |
| 記憶寫入 | `mem_save` | 保存新記憶（支援 Tags） |
| 自動去重 | `mem_dedup` | 合併重複記憶 |
| 遺忘曲線 | `mem_decay` | 自動降低舊記憶權重 |
| 矛盾檢測 | `mem_contradict` | 發現衝突記憶 |
| 健康報告 | `mem_health` | 系統全面體檢 |

---

## 實戰數據（UltraClaw 自用）

| 指標 | 數值 |
|------|------|
| 總記憶條數 | 6,675 |
| 索引向量數 | 6,009 |
| 嵌入維度 | 1024 (BGE-m3) |
| 距離算法 | COSINE |
| Collection 數 | 5（openclaw / deepseek / claude / hermes / shared） |
| 中文搜尋精確度 | >78% |
| 硬碟佔用 | ~150MB（含模型） |
| 每日寫入量 | ~50-100 條 |

---

## 與 agentmemory 的對比

| 維度 | agentmemory | Vector Memory |
|------|------------|---------------|
| 設計場景 | Coding Agent（Claude Code） | 通用 AI 助理 |
| 中文檢索成功率 | 0%（實測） | >78% |
| 嵌入模型 | 英文優化 | BGE-m3（中英文最優） |
| 部署複雜度 | 高（多容器） | 低（單容器 + Python） |
| 數據主權 | 依賴外部索引 | 100% 本地 |
| 知識圖譜 | 有 | 有 |
| 時間旅行 | 無 | 有 |
| 適合平台 | Claude Code | OpenClaw / Claude Code / 通用 |

---

## 為什麼選擇 Qdrant？

| 對比 | Qdrant | Chroma | Weaviate | Milvus |
|------|--------|--------|----------|--------|
| 語言 | Rust | Python | Go | C++ |
| 單機性能 | 極佳 | 中 | 佳 | 極佳 |
| 資源佔用 | 低 (~50MB) | 低 | 高 (~500MB) | 高 (~1GB) |
| 安裝難度 | 極低（Docker） | 低 | 中 | 高 |
| 適合場景 | 個人/小團隊 | 原型 | 企業 | 大規模 |

---

## 相關資源

- **前置項目：** [Skills Triggering](../skills-triggering/) — 讓技能被發現
- **配套項目：** [Skill Router](../skill-router/) — 讓記憶輔助路由決策

---

## 📥 一行安裝

```bash
curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/vector-memory/setup.sh | bash
```

## 授權

MIT
