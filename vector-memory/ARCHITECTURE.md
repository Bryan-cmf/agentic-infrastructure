# 🧠 向量記憶系統 — 完整技術架構

> **Version 2.0 | 2026-06-15 | UltraClaw Production**

---

## 目錄

1. [設計哲學](#設計哲學)
2. [雙引擎架構](#雙引擎架構)
3. [Engine A: 內建記憶搜尋](#engine-a-內建記憶搜尋)
4. [Engine B: MCP 向量記憶](#engine-b-mcp-向量記憶)
5. [雙寫強制層](#雙寫強制層)
6. [自動化 Cron 層](#自動化-cron-層)
7. [可視化層 MemoryHub v6.0](#可視化層-memoryhub-v60)
8. [記憶文件體系](#記憶文件體系)
9. [部署與維運](#部署與維運)
10. [歷史演進](#歷史演進)

---

## 設計哲學

### 核心原則

| 原則 | 說明 |
|------|------|
| **雙引擎冗餘** | 兩套獨立搜尋系統，互為備援 |
| **完全本地** | 零 API Key、零網路依賴、零成本 |
| **雙寫強制** | 文件寫入必同步向量，不能只寫一個 |
| **自動化兜底** | Cron 安全網確保遺漏自動補齊 |
| **可觀測性** | Dashboard + 健康報告 + 統計面板 |

### 為什麼雙引擎？

1. **Engine A (內建 memory_search)**: 搜尋 MEMORY.md + daily logs，混合搜尋（向量 + BM25），適合精確召回
2. **Engine B (MCP vector-memory)**: 搜尋 Qdrant 中的所有向量化記憶，純語義搜尋，適合模糊匹配

兩者搜尋範圍不同、embedding 模型不同、算法不同 → 互補而非重複。

---

## 雙引擎架構

```
User Query
    │
    ├──→ Engine A: memory_search
    │    ├── Embedding: embeddinggemma-300m (GGUF, 600MB, 全本地)
    │    ├── 索引源: MEMORY.md + memory/*.md
    │    ├── 搜尋: 混合 (向量 70% + BM25 30%)
    │    └── 延遲: ~4 秒
    │
    └──→ Engine B: vector-memory__mem_search
         ├── Embedding: BAAI/bge-m3 (1024-dim, MPS 加速)
         ├── 索引源: Qdrant openclaw_mem (10,131 pts)
         ├── 搜尋: 純向量 Cosine
         └── 延遲: ~0.5 秒
```

---

## Engine A: 內建記憶搜尋

### 技術棧

| 組件 | 技術 |
|------|------|
| 索引引擎 | OpenClaw built-in (SQLite FTS5 + sqlite-vec) |
| Embedding 模型 | embeddinggemma-300m-qat-Q8_0 (GGUF) |
| 執行環境 | node-llama-cpp (Node.js native) |
| 搜尋算法 | 混合 (Vector 70% + BM25 30%) |
| 索引範圍 | MEMORY.md + memory/*.md (遞歸) |
| 模型大小 | ~600 MB |

### 配置

```json5
// openclaw.json → agents.defaults.memorySearch
{
  "provider": "local",
  "query": {
    "hybrid": {
      "vectorWeight": 0.7,
      "textWeight": 0.3,
      "mmr": { "enabled": true, "lambda": 0.7 },
      "temporalDecay": { "enabled": true, "halfLifeDays": 30 }
    }
  }
}
```

### 搜尋流程

```
查詢 "自媒體平台"
    ↓
1. Tokenize → BM25 關鍵詞搜尋 (FTS5)
    ↓
2. GGUF Embedding → 512-dim 向量
    ↓
3. sqlite-vec 向量搜尋 (Cosine)
    ↓
4. 加權合併 (0.7 × vector + 0.3 × BM25)
    ↓
5. MMR 多樣性重排 + 時間衰減
    ↓
6. 返回 Top-N 結果 (含 Source 引用)
```

### 安裝

```bash
# 1. 安裝 node-llama-cpp
cd /opt/homebrew/lib/node_modules/openclaw
npm install node-llama-cpp

# 2. 配置 provider
# openclaw.json: agents.defaults.memorySearch.provider = "local"

# 3. 重建索引
openclaw memory index --force --agent main
```

---

## Engine B: MCP 向量記憶

### 技術棧

| 組件 | 技術 |
|------|------|
| 向量數據庫 | Qdrant v1.18.1 (Docker) |
| Embedding 模型 | BAAI/bge-m3 (1024-dim) |
| 執行環境 | Python 3.13 + sentence-transformers |
| 硬體加速 | Apple MPS (Metal Performance Shaders) |
| MCP 協議 | stdio-based JSON-RPC |
| 集合 | openclaw_mem (UltraClaw 專用) |

### MCP Server 架構

```python
# mcp_server.py 核心結構
class VectorMemoryMCP:
    def __init__(self):
        self.embedder = SentenceTransformer('BAAI/bge-m3', device='mps')
        self.qdrant = QdrantClient(url='http://localhost:6333')
        self.collection = 'openclaw_mem'

    # 工具: mem_search, mem_save, mem_stats, mem_health,
    #       mem_decay, mem_dedup, mem_graph, mem_contradict,
    #       mem_time_travel, mem_federated, mem_list_collections
```

### 搜尋流程

```
查詢 "自媒體平台"
    ↓
1. BGE-m3 encode → 1024-dim 向量 (MPS)
    ↓
2. Qdrant search (Cosine, top_k=10)
    ↓
3. 返回: {point_id, score, content, tags, metadata}
    ↓
延遲: ~0.5 秒 (MPS 加速)
```

### 部署

```bash
# Qdrant
docker run -d -p 6333:6333 \
  -v /Users/Claw/qdrant_storage:/qdrant/storage \
  qdrant/qdrant

# MCP Server (via OpenClaw config or standalone)
/Users/Claw/Desktop/Projects/vector-memory/.venv/bin/python \
  /Users/Claw/Desktop/Projects/vector-memory/mcp_server.py
```

---

## 雙寫強制層

### 寫入流程

```
Agent 完成任務
    ↓
write tool → 寫入 memory/daily/YYYY-MM-DD.md
    ↓ (強制，不可跳過)
vector-memory__mem_save → Qdrant openclaw_mem
    ├── content: 完整段落 (80-1500 字)
    ├── tags: [分類, date:YYYY-MM-DD]
    └── collection: openclaw_mem
    ↓ (安全網)
auto_sync.py 每小時增量掃描 → 補齊遺漏
```

### 雙寫規則 (寫入 AGENTS.md + PERMANENT-RULES.md)

| 規則 | 內容 |
|------|------|
| 🔴 觸發條件 | 每個有意義任務完成後 |
| 🔴 Collection | 永遠用 openclaw_mem |
| 🔴 Tags | 分類 tag + date:YYYY-MM-DD |
| 🔴 內容長度 | 80-1500 字完整段落 |
| 🟡 auto_sync | Cron 每小時，僅後備 |

---

## 自動化 Cron 層

### 定時任務矩陣

| 時間 | 任務 | 腳本 | 用途 |
|------|------|------|------|
| 每分鐘 | 存活監控 | guard.sh | Qdrant + MCP 進程守護 |
| 每小時 | 增量同步 | auto_sync.py | 文件→向量補齊 |
| 每 2 小時 | 預載入 | memory_preload.py | 熱數據快取 |
| 每 10 分鐘 | Watcher | sync_watcher.py | 事件驅動同步 |
| 每天 04:00 | 一致性檢查 | consistency_check.py | 雙系統比對 |
| 每天 08:00 | 記憶摘要 | morning_brief.py | 每日記憶概覽 |
| 每週日 03:00 | Qdrant 備份 | qdrant_backup.py | 全量備份 |
| 每月 1 日 03:30 | Qdrant 緊湊化 | qdrant_backup.py --optimize | 空間回收 |

### 監控指標

- Qdrant 存活狀態
- 集合點數變化趨勢
- 雙系統一致性比率
- 記憶衰減分佈
- 去重候選數

---

## 可視化層 MemoryHub v6.0

### 架構

```
Browser (memhub.best-thinktank.com)
    ↓ Cloudflare Tunnel
Python api_server.py (:3872)
    ├── templates/dashboard.html (DOM API, 零轉義)
    ├── /api/memories → Qdrant REST API
    └── /api/stats → 即時統計
```

### v6.0 核心改進 (DOM API 重構)

| 版本 | 按鈕實現 | 穩定性 |
|------|---------|--------|
| v3-v5.1 | JS 字串拼接 onclick | 🔴 反覆炸 (四層轉義) |
| **v6.0** | **DOM API: btn.onclick = function(){}** | 🟢 **永不炸** |

### 功能

- 四主題 (暗夜/暖陽/森林/海洋)
- 全中文界面
- 即時搜尋
- 回憶錄內置目錄
- 多集合切換
- 統計面板

---

## 記憶文件體系

```
~/.openclaw/workspace/
├── MEMORY.md                    ← 長期記憶 (Evergreen, 79KB)
├── memory/
│   ├── daily/
│   │   ├── YYYY-MM-DD.md       ← 每日工作日志
│   │   └── YYYY-MM-DD-lessons.md ← 每日踩坑反思
│   ├── weekly/
│   │   └── YYYY-WXX.md         ← 週報
│   ├── projects/
│   │   └── PROJECT.md          ← 專案記憶
│   ├── lessons/
│   │   └── index.md            ← 踩坑索引
│   ├── procedures/
│   │   └── *.md               ← SOP 文檔
│   └── articles/
│       └── *.md               ← 技術文章
│
├── MEMORY-SYSTEM.md            ← 記憶系統機制規則
├── SOUL.md                     ← Agent 人格定義
├── USER.md                     ← 用戶檔案
├── AGENTS.md                   ← Agent 行為規則
├── RULES.md                    ← 規則速查表
└── PERMANENT-RULES.md          ← 永久規則
```

### 檔案 → 向量映射

| 檔案類別 | Collection | Tags |
|---------|-----------|------|
| MEMORY.md | openclaw_mem | memory, evergreen |
| daily/*.md | openclaw_mem | daily, date:YYYY-MM-DD |
| daily/*-lessons.md | openclaw_mem | lessons, date:YYYY-MM-DD |
| projects/*.md | openclaw_mem | projects, project:NAME |
| weekly/*.md | openclaw_mem | weekly, week:YYYY-WXX |

---

## 部署與維運

### 系統需求

| 組件 | 最低 | 推薦 |
|------|------|------|
| RAM | 8 GB | 16 GB+ |
| 磁盤 | 5 GB | 20 GB (for Qdrant + models) |
| Python | 3.11+ | 3.13 |
| Node.js | 22+ | 26 |
| Docker | (Qdrant only) | Colima / Docker Desktop |

### 健康檢查

```bash
# Qdrant
curl http://localhost:6333/

# MCP Server
ps aux | grep mcp_server

# 記憶統計
python3 -c "
from qdrant_client import QdrantClient
c = QdrantClient('localhost', port=6333)
info = c.get_collection('openclaw_mem')
print(f'Points: {info.points_count}')
"

# 內建索引
openclaw memory status --agent main
```

### 故障恢復

| 故障 | 恢復步驟 |
|------|---------|
| Qdrant 離線 | `docker restart qdrant` |
| MCP Server 掛掉 | 重啟 mcp_server.py |
| 向量不同步 | `python3 auto_sync.py --force` |
| 內建索引損壞 | `openclaw memory index --force --agent main` |
| 記憶體洩漏 | 清理重複 MCP 進程，重啟 Gateway |

---

## 歷史演進

| 日期 | 里程碑 |
|------|--------|
| 2026-05-16 | Qdrant 部署，首批 1,156 條向量導入 |
| 2026-05-17 | 雙寫強制規則建立，auto_sync.py 上線 |
| 2026-05-19 | MemoryHub v2.0 部署，10 數據庫統一管線 |
| 2026-05-21 | MemoryHub v3.0，Dashboard 互動 |
| 2026-05-23 | 內建記憶搜尋 (memory_search) 投入使用 |
| 2026-05-30 | Qdrant Docker Volume 陷阱修復 (4,133 pts 恢復) |
| 2026-06-11 | MemoryHub v6.0 DOM API 重構 |
| **2026-06-15** | **Engine A 切換為本地 GGUF ($0 成本)** |
| 2026-06-15 | 雙引擎全面恢復上線 |

---

## 相關倉庫

- [agentic-infrastructure](https://github.com/Bryan-cmf/agentic-infrastructure) — 十件套主倉庫
- [MemoryHub](https://github.com/Bryan-cmf/MemoryHub) — Dashboard 獨立倉庫
- [vector-memory](https://github.com/Bryan-cmf/vector-memory) — MCP Server 倉庫

---

_Last updated: 2026-06-15 · UltraClaw Production_
