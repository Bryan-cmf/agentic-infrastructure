# 🧠 Vector Memory — 向量記憶系統

> **Qdrant + BGE-m3 + Local GGUF 雙引擎記憶架構**
> 解決 AI Agent 重啟後完全失憶的結構性問題

---

## 📐 系統架構

```
┌──────────────────────────────────────────────────────────┐
│                    雙引擎記憶架構                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   Engine A: 內建記憶搜尋          Engine B: 向量記憶搜尋   │
│   ┌─────────────────────┐       ┌─────────────────────┐  │
│   │ memory_search       │       │ vector-memory__     │  │
│   │                     │       │ mem_search          │  │
│   ├─────────────────────┤       ├─────────────────────┤  │
│   │ 索引: MEMORY.md     │       │ 索引: Qdrant        │  │
│   │      memory/*.md    │       │       openclaw_mem   │  │
│   ├─────────────────────┤       ├─────────────────────┤  │
│   │ Embedding:          │       │ Embedding:          │  │
│   │ GGUF local          │       │ BGE-m3 (1024-dim)   │  │
│   │ embeddinggemma-300m │       │ 本地 MPS 加速        │  │
│   ├─────────────────────┤       ├─────────────────────┤  │
│   │ 搜尋: 混合           │       │ 搜尋: 純向量          │  │
│   │ (向量 70% + BM25 30%)│      │ Cosine 相似度        │  │
│   ├─────────────────────┤       ├─────────────────────┤  │
│   │ 成本: $0 (完全本地)   │       │ 成本: $0 (完全本地)   │  │
│   └─────────────────────┘       └─────────────────────┘  │
│                                                          │
│   雙寫強制層                                               │
│   ┌─────────────────────────────────────────────────┐    │
│   │ 每次 write file → 同時 vector-memory__mem_save  │    │
│   │ auto_sync.py 每小時增量同步 (後備安全網)           │    │
│   └─────────────────────────────────────────────────┘    │
│                                                          │
│   可視化層 (MemoryHub v6.0)                                │
│   ┌─────────────────────────────────────────────────┐    │
│   │ DOM API 架構 · 四主題 · 全中文 · 回憶錄內置       │    │
│   │ https://memhub.best-thinktank.com                │    │
│   └─────────────────────────────────────────────────┘    │
│                                                          │
│   自動化層                                                 │
│   ┌─────────────────────────────────────────────────┐    │
│   │ auto_sync.py      每小時增量    向量同步          │    │
│   │ guard.sh          每分鐘存活    監控守護          │    │
│   │ consistency_check  每天 04:00   雙系統一致性      │    │
│   │ morning_brief.py   每天 08:00   記憶摘要          │    │
│   │ qdrant_backup.py   每週日 03:00 備份             │    │
│   │ memory_preload.py  每 2 小時    預載入            │    │
│   └─────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

---

## 🚀 快速安裝

### 前置條件

```bash
# Qdrant (Docker)
docker run -d -p 6333:6333 -v /Users/Claw/qdrant_storage:/qdrant/storage qdrant/qdrant

# Python 依賴
pip install sentence-transformers mcp qdrant-client
```

### OpenClaw 配置

**Engine A: 內建記憶搜尋 (本地 GGUF)**

```json5
// openclaw.json → agents.defaults
{
  "memorySearch": {
    "provider": "local"
  }
}
```

安裝 node-llama-cpp：

```bash
cd /opt/homebrew/lib/node_modules/openclaw
npm install node-llama-cpp
```

重建索引：

```bash
openclaw memory index --force --agent main
```

**Engine B: MCP 向量記憶 (BGE-m3 + Qdrant)**

```json5
// openclaw.json → mcp.servers
{
  "vector-memory": {
    "command": "python",
    "args": ["path/to/mcp_server.py"],
    "env": {
      "EMBEDDING_MODEL": "BAAI/bge-m3",
      "QDRANT_URL": "http://localhost:6333"
    }
  }
}
```

---

## 🔧 雙寫強制機制

| 規則 | 內容 |
|------|------|
| 🔴 寫入觸發 | 每次 `write` daily log / MEMORY.md / project .md |
| 🔴 目標集合 | `openclaw_mem` (UltraClaw 專用) |
| 🔴 Tags | 分類 tag (daily/projects/lessons) + 日期 tag (date:YYYY-MM-DD) |
| 🔴 內容 | 完整段落，最少 80 字，最多 1500 字 |
| 🟡 安全網 | auto_sync.py 每小時 crontab 增量同步 |

---

## 📊 記憶統計 (截至 2026-06-15)

| 指標 | 數值 |
|------|------|
| Qdrant 版本 | v1.18.1 |
| openclaw_mem 條目 | 10,131 |
| 向量維度 | 1024 (BGE-m3) |
| 距離函數 | Cosine |
| 內建索引覆蓋 | MEMORY.md + memory/*.md |
| Embedding 模型 (Engine A) | embeddinggemma-300m (GGUF, ~600MB) |
| Embedding 模型 (Engine B) | BAAI/bge-m3 (本地 MPS) |
| GUI Dashboard | MemoryHub v6.0 (DOM API) |

---

## 🛠️ 工具速查

| 工具 | 用途 |
|------|------|
| `memory_search` | 搜尋 MEMORY.md + memory/*.md (混合搜尋) |
| `vector-memory__mem_search` | 搜尋 Qdrant openclaw_mem (純向量) |
| `vector-memory__mem_save` | 寫入向量記憶 |
| `vector-memory__mem_stats` | 集合統計 |
| `vector-memory__mem_health` | 系統健康報告 |
| `vector-memory__mem_decay` | 記憶衰減計算 |
| `vector-memory__mem_dedup` | 語義去重 |
| `vector-memory__mem_graph` | 記憶知識圖譜 |

---

## 📄 相關文件

- `ARCHITECTURE.md` — 完整技術架構
- `scripts/auto_sync.py` — 增量同步腳本
- `scripts/guard.sh` — 存活監控
- `scripts/consistency_check.py` — 雙系統一致性檢查
- `templates/dashboard.html` — MemoryHub v6.0 前端

---

## 🇹🇼 技能元數據

- **名稱**: Vector Memory (向量記憶)
- **版本**: v2.0
- **類別**: 基礎設施
- **依賴**: Qdrant, sentence-transformers, BGE-m3
- **成本**: $0 (完全本地)
- **語言**: 繁體中文 / 简体中文 / English / 日本語 / 한국어 / العربية
