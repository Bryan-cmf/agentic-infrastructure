#!/usr/bin/env python3
"""
Vector Memory MCP Server v2.0
==============================
本地向量記憶系統 — Qdrant + BGE-m3

新增功能：
  - 記憶衰減系統 (Memory Decay)
  - 語義去重引擎 (Semantic Dedup)
  - 矛盾檢測 (Contradiction Detector)
  - 時間旅行查詢 (Time-Travel Query)
  - 跨 Collection 聯邦搜索 (Federated Search)
  - 知識圖譜 (Memory Graph)
  - 並發安全 (Thread-safe)
  - 修復工具描述錯誤

Tools:
  mem_save / mem_search / mem_delete / mem_stats / mem_list_collections
  mem_decay          — 執行記憶衰減計算
  mem_dedup          — 語義去重
  mem_contradict     — 矛盾檢測
  mem_time_travel    — 時間旅行查詢
  mem_federated      — 跨 Collection 搜索
  mem_graph          — 知識圖譜構建
  mem_health         — 健康度報告
"""

import asyncio
import json
import sys
import os
import uuid
import threading
from typing import Optional
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import math

# Qdrant & Embedding
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue, SearchRequest,
    ScrollRequest, PointIdsList
)
from sentence_transformers import SentenceTransformer

# MCP Protocol
import mcp.types as types
from mcp.server import Server

# ── Configuration ──────────────────────────────────
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
DEFAULT_COLLECTION = os.getenv("DEFAULT_COLLECTION", "openclaw_mem")
MAX_RESULTS = 10
SIMILARITY_THRESHOLD = 0.6
DEDUP_THRESHOLD = 0.92
CONTRADICTION_THRESHOLD = 0.75
DECAY_LAMBDA = 0.01  # Decay rate per day

# ── Initialize components ──────────────────────────
print(f"🔄 Loading embedding model: {MODEL_NAME}...", file=sys.stderr)
embedding_model = SentenceTransformer(MODEL_NAME, device="mps")
EMBEDDING_DIM = embedding_model.get_sentence_embedding_dimension()
print(f"✅ Model loaded ({EMBEDDING_DIM}dim)", file=sys.stderr)

qdrant_client = QdrantClient(url=QDRANT_URL)
print(f"✅ Connected to Qdrant at {QDRANT_URL}", file=sys.stderr)

# Thread-safe lock for concurrent operations
_lock = threading.Lock()

app = Server("vector-memory")


# ── Helper Functions ──────────────────────────────────

def get_embedding(text: str) -> list[float]:
    """Generate embedding vector for text"""
    return embedding_model.encode(text, normalize_embeddings=True).tolist()


def ensure_collection(collection_name: str):
    """Create collection if not exists, using model's actual embedding dimension"""
    with _lock:
        collections = [c.name for c in qdrant_client.get_collections().collections]
        if collection_name not in collections:
            qdrant_client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIM,
                    distance=Distance.COSINE,
                    on_disk=True
                )
            )
            print(f"📦 Created collection: {collection_name} ({EMBEDDING_DIM}dim)", file=sys.stderr)


def get_all_collection_names() -> list[str]:
    """Get all collection names"""
    return [c.name for c in qdrant_client.get_collections().collections]


def scroll_all_points(collection: str, limit: int = 1000) -> list:
    """Scroll all points in a collection (for batch operations)"""
    points = []
    offset = None
    while True:
        result = qdrant_client.scroll(
            collection_name=collection,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False
        )
        points.extend(result[0])
        offset = result[1]
        if offset is None or len(points) >= limit:
            break
    return points[:limit]


# ── MCP Tool Definitions ──────────────────────────────

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        # ── Core Tools ──
        types.Tool(
            name="mem_save",
            description="Save a memory entry to vector database. "
                        "Args: collection (str, optional, default: openclaw_mem), content (str), "
                        "tags (list[str], optional), metadata (dict, optional)",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection": {"type": "string", "description": "Collection name (default: openclaw_mem)"},
                    "content": {"type": "string", "description": "Memory content to save"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for categorization"},
                    "metadata": {"type": "object", "description": "Additional metadata"}
                },
                "required": ["content"]
            }
        ),
        types.Tool(
            name="mem_search",
            description="Search memories by semantic similarity. "
                        "Args: query (str), collection (str, optional, default: openclaw_mem), "
                        "limit (int, default 10), tags (list[str], optional)",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection": {"type": "string", "description": "Collection name (default: openclaw_mem)"},
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "description": "Max results (default: 10)"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Filter by tags"}
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="mem_list_collections",
            description="List all memory collections",
            inputSchema={"type": "object", "properties": {}}
        ),
        types.Tool(
            name="mem_delete",
            description="Delete a memory entry by ID. "
                        "Args: collection (str), point_id (str)",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection": {"type": "string", "description": "Collection name"},
                    "point_id": {"type": "string", "description": "UUID of the memory to delete"}
                },
                "required": ["collection", "point_id"]
            }
        ),
        types.Tool(
            name="mem_stats",
            description="Get statistics for a collection. "
                        "Args: collection (str)",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection": {"type": "string", "description": "Collection name"}
                },
                "required": ["collection"]
            }
        ),
        # ── Advanced Tools ──
        types.Tool(
            name="mem_decay",
            description="Execute memory decay calculation. "
                        "Reduces weight of memories not accessed recently. "
                        "Args: collection (str, optional), dry_run (bool, default false)",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection": {"type": "string", "description": "Collection name (default: openclaw_mem)"},
                    "dry_run": {"type": "boolean", "description": "If true, only report, no changes"}
                }
            }
        ),
        types.Tool(
            name="mem_dedup",
            description="Semantic deduplication — find and merge duplicate memories. "
                        "Args: collection (str, optional), threshold (float, default 0.92), dry_run (bool)",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection": {"type": "string", "description": "Collection name (default: openclaw_mem)"},
                    "threshold": {"type": "number", "description": "Similarity threshold (default: 0.92)"},
                    "dry_run": {"type": "boolean", "description": "If true, only report duplicates"}
                }
            }
        ),
        types.Tool(
            name="mem_contradict",
            description="Detect contradictory memories. "
                        "Args: collection (str, optional), content (str, optional — new memory to check)",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection": {"type": "string", "description": "Collection name (default: openclaw_mem)"},
                    "content": {"type": "string", "description": "New memory content to check for contradictions"}
                }
            }
        ),
        types.Tool(
            name="mem_time_travel",
            description="Query memories as they existed at a specific date. "
                        "Args: date (str, YYYY-MM-DD), query (str), collection (str, optional)",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Target date (YYYY-MM-DD)"},
                    "query": {"type": "string", "description": "Search query"},
                    "collection": {"type": "string", "description": "Collection name (default: openclaw_mem)"}
                },
                "required": ["date", "query"]
            }
        ),
        types.Tool(
            name="mem_federated",
            description="Search across ALL collections simultaneously. "
                        "Args: query (str), limit (int, default 10)",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "description": "Max results per collection (default: 10)"}
                },
                "required": ["query"]
            }
        ),
        types.Tool(
            name="mem_graph",
            description="Build memory knowledge graph — find related memories. "
                        "Args: collection (str, optional), point_id (str, optional — specific memory)",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection": {"type": "string", "description": "Collection name (default: openclaw_mem)"},
                    "point_id": {"type": "string", "description": "Specific memory ID to find relations for"}
                }
            }
        ),
        types.Tool(
            name="mem_health",
            description="Get memory system health report. "
                        "Returns: collection stats, decay distribution, dedup candidates, consistency.",
            inputSchema={"type": "object", "properties": {}}
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        handlers = {
            "mem_save": tool_mem_save,
            "mem_search": tool_mem_search,
            "mem_list_collections": tool_list_collections,
            "mem_delete": tool_mem_delete,
            "mem_stats": tool_mem_stats,
            "mem_decay": tool_mem_decay,
            "mem_dedup": tool_mem_dedup,
            "mem_contradict": tool_mem_contradict,
            "mem_time_travel": tool_mem_time_travel,
            "mem_federated": tool_mem_federated,
            "mem_graph": tool_mem_graph,
            "mem_health": tool_mem_health,
        }
        handler = handlers.get(name)
        if handler:
            return await handler(arguments)
        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"❌ Error: {str(e)}")]


# ── Core Tool Implementations ──────────────────────────

async def tool_mem_save(args: dict) -> list[types.TextContent]:
    try:
        collection = args.get("collection", DEFAULT_COLLECTION)
        content = args.get("content", "")
        if not content:
            return [types.TextContent(type="text", text="❌ Error: content is required")]
        tags = args.get("tags", [])
        metadata = args.get("metadata", {})

        ensure_collection(collection)

        # Check for semantic duplicates before saving
        query_vector = get_embedding(content)
        results = qdrant_client.query_points(
            collection_name=collection,
            query=query_vector,
            limit=3,
            score_threshold=DEDUP_THRESHOLD
        )
        if results.points:
            existing = results.points[0]
            return [types.TextContent(type="text", text=json.dumps({
                "status": "duplicate_detected",
                "similarity": round(existing.score, 4),
                "existing_id": str(existing.id),
                "existing_preview": (existing.payload or {}).get("content", "")[:200],
                "message": "A very similar memory already exists. Use force_save to override."
            }, ensure_ascii=False, indent=2))]

        # Generate embedding and save
        with _lock:
            content_id = f"mcp:{collection}:{content[:200]}"
            point = PointStruct(
                id=str(uuid.uuid5(uuid.NAMESPACE_DNS, content_id)),
                vector=query_vector,
                payload={
                    "content": content,
                    "tags": tags,
                    "created_at": datetime.now().isoformat(),
                    "access_count": 0,
                    "last_accessed": datetime.now().isoformat(),
                    "superseded_at": None,
                    **metadata
                }
            )
            qdrant_client.upsert(collection_name=collection, points=[point])

        result = {
            "status": "saved",
            "collection": collection,
            "point_id": point.id,
            "content_preview": content[:100] + "..." if len(content) > 100 else content
        }
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"❌ mem_save failed: {str(e)}")]


async def tool_mem_search(args: dict) -> list[types.TextContent]:
    try:
        collection = args.get("collection", DEFAULT_COLLECTION)
        query = args.get("query", "")
        if not query:
            return [types.TextContent(type="text", text="❌ Error: query is required")]
        limit = min(args.get("limit", MAX_RESULTS), 50)
        tags = args.get("tags", [])

        ensure_collection(collection)

        stats = qdrant_client.get_collection(collection)
        if stats.points_count == 0:
            return [types.TextContent(type="text", text=f"📭 Collection '{collection}' is empty")]

        query_vector = get_embedding(query)

        search_filter = None
        if tags:
            search_filter = Filter(
                should=[FieldCondition(key="tags", match=MatchValue(value=tag)) for tag in tags]
            )

        results = qdrant_client.query_points(
            collection_name=collection,
            query=query_vector,
            query_filter=search_filter,
            limit=limit,
            score_threshold=SIMILARITY_THRESHOLD
        )
        hits = results.points

        if not hits:
            return [types.TextContent(type="text", text=f"🔍 No results found for: {query}")]

        # Update access stats for found memories
        with _lock:
            for hit in hits:
                try:
                    point = qdrant_client.retrieve(
                        collection_name=collection,
                        ids=[hit.id],
                        with_payload=True,
                        with_vectors=False
                    )
                    if point:
                        payload = point[0].payload or {}
                        payload["access_count"] = payload.get("access_count", 0) + 1
                        payload["last_accessed"] = datetime.now().isoformat()
                        qdrant_client.upsert(
                            collection_name=collection,
                            points=[PointStruct(id=hit.id, vector=query_vector, payload=payload)]
                        )
                except Exception:
                    pass

        output = []
        for i, hit in enumerate(hits, 1):
            payload = hit.payload or {}
            output.append({
                "rank": i,
                "score": round(hit.score, 4),
                "point_id": str(hit.id),
                "content": payload.get("content", ""),
                "tags": payload.get("tags", []),
                "section_path": payload.get("section_path", ""),
                "created_at": payload.get("created_at", "unknown"),
                "access_count": payload.get("access_count", 0)
            })

        return [types.TextContent(type="text", text=json.dumps(output, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"❌ mem_search failed: {str(e)}")]


async def tool_list_collections(args: dict) -> list[types.TextContent]:
    try:
        collections = qdrant_client.get_collections().collections
        result = []
        for col in collections:
            stats = qdrant_client.get_collection(col.name)
            result.append({
                "name": col.name,
                "points_count": stats.points_count,
                "indexed_vectors_count": stats.indexed_vectors_count,
                "status": str(stats.status) if stats.status else "active"
            })
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"❌ mem_list_collections failed: {str(e)}")]


async def tool_mem_delete(args: dict) -> list[types.TextContent]:
    try:
        collection = args.get("collection", "")
        point_id = args.get("point_id", "")
        if not collection or not point_id:
            return [types.TextContent(type="text", text="❌ Error: collection and point_id are required")]

        try:
            fetched = qdrant_client.retrieve(
                collection_name=collection,
                ids=[point_id],
                with_payload=False,
                with_vectors=False
            )
            if not fetched:
                return [types.TextContent(type="text", text=f"⚠️ Memory not found: {point_id} in {collection}")]
        except Exception:
            return [types.TextContent(type="text", text=f"⚠️ Collection '{collection}' does not exist")]

        qdrant_client.delete(collection_name=collection, points_selector=PointIdsList(points=[point_id]))
        return [types.TextContent(type="text", text=f"✅ Deleted memory {point_id} from {collection}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"❌ mem_delete failed: {str(e)}")]


async def tool_mem_stats(args: dict) -> list[types.TextContent]:
    try:
        collection = args.get("collection", "")
        if not collection:
            return [types.TextContent(type="text", text="❌ Error: collection is required")]

        ensure_collection(collection)
        stats = qdrant_client.get_collection(collection)

        result = {
            "collection": collection,
            "points_count": stats.points_count,
            "indexed_vectors_count": stats.indexed_vectors_count,
            "segments_count": stats.segments_count,
            "status": str(stats.status) if stats.status else "active",
            "config": {
                "vector_size": stats.config.params.vectors.size,
                "distance": str(stats.config.params.vectors.distance)
            }
        }
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"❌ mem_stats failed: {str(e)}")]


# ── Advanced Tool Implementations ──────────────────────────

async def tool_mem_decay(args: dict) -> list[types.TextContent]:
    """Memory Decay — 記憶衰減計算"""
    try:
        collection = args.get("collection", DEFAULT_COLLECTION)
        dry_run = args.get("dry_run", False)

        ensure_collection(collection)
        points = scroll_all_points(collection)
        now = datetime.now()

        decayed_count = 0
        report = []

        for point in points:
            payload = point.payload or {}
            last_accessed = payload.get("last_accessed", payload.get("created_at", now.isoformat()))
            try:
                access_date = datetime.fromisoformat(last_accessed.replace("Z", "+00:00").replace("+00:00", ""))
            except:
                access_date = now

            days_since_access = (now - access_date).total_seconds() / 86400
            decay_factor = math.exp(-DECAY_LAMBDA * days_since_access)
            access_count = payload.get("access_count", 0)
            access_factor = math.log(1 + access_count) / math.log(1 + 100)  # Normalize

            health_score = decay_factor * 0.7 + access_factor * 0.3

            if health_score < 0.3:
                decayed_count += 1
                if len(report) < 10:
                    report.append({
                        "point_id": str(point.id),
                        "content_preview": payload.get("content", "")[:100],
                        "days_since_access": round(days_since_access, 1),
                        "health_score": round(health_score, 3),
                        "decay_factor": round(decay_factor, 3),
                        "access_count": access_count
                    })

            if not dry_run and health_score < 0.1:
                # Mark as superseded (soft delete)
                payload["superseded_at"] = now.isoformat()
                payload["decay_reason"] = "low_health_score"
                with _lock:
                    qdrant_client.upsert(
                        collection_name=collection,
                        points=[PointStruct(id=point.id, vector=[0.0] * EMBEDDING_DIM, payload=payload)]
                    )

        result = {
            "collection": collection,
            "total_memories": len(points),
            "decayed_count": decayed_count,
            "dry_run": dry_run,
            "low_health_examples": report
        }
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"❌ mem_decay failed: {str(e)}")]


async def tool_mem_dedup(args: dict) -> list[types.TextContent]:
    """Semantic Deduplication — 語義去重"""
    try:
        collection = args.get("collection", DEFAULT_COLLECTION)
        threshold = args.get("threshold", DEDUP_THRESHOLD)
        dry_run = args.get("dry_run", False)

        ensure_collection(collection)
        points = scroll_all_points(collection, limit=500)  # Limit for performance

        duplicates = []
        processed = set()

        for i, p1 in enumerate(points):
            if str(p1.id) in processed:
                continue

            payload1 = p1.payload or {}
            content1 = payload1.get("content", "")
            if not content1:
                continue

            vec1 = qdrant_client.retrieve(
                collection_name=collection,
                ids=[p1.id],
                with_vectors=True,
                with_payload=False
            )
            if not vec1 or not vec1[0].vector:
                continue

            vector1 = vec1[0].vector
            results = qdrant_client.query_points(
                collection_name=collection,
                query=vector1,
                limit=5,
                score_threshold=threshold
            )

            for hit in results.points:
                if str(hit.id) == str(p1.id) or str(hit.id) in processed:
                    continue

                payload2 = hit.payload or {}
                content2 = payload2.get("content", "")

                # Keep the longer one (more info)
                if len(content1) >= len(content2):
                    keep, remove = p1, hit
                    keep_content, remove_content = content1, content2
                else:
                    keep, remove = hit, p1
                    keep_content, remove_content = content2, content1

                duplicates.append({
                    "keep_id": str(keep.id),
                    "remove_id": str(remove.id),
                    "similarity": round(hit.score, 4),
                    "keep_preview": keep_content[:100],
                    "remove_preview": remove_content[:100]
                })
                processed.add(str(remove.id))

                if not dry_run:
                    with _lock:
                        qdrant_client.delete(
                            collection_name=collection,
                            points_selector=PointIdsList(points=[remove.id])
                        )

        result = {
            "collection": collection,
            "threshold": threshold,
            "total_scanned": len(points),
            "duplicates_found": len(duplicates),
            "dry_run": dry_run,
            "duplicates": duplicates[:20]
        }
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"❌ mem_dedup failed: {str(e)}")]


async def tool_mem_contradict(args: dict) -> list[types.TextContent]:
    """Contradiction Detector — 矛盾檢測"""
    try:
        collection = args.get("collection", DEFAULT_COLLECTION)
        content = args.get("content", "")

        ensure_collection(collection)

        if content:
            # Check new content against existing memories
            query_vector = get_embedding(content)
            results = qdrant_client.query_points(
                collection_name=collection,
                query=query_vector,
                limit=10,
                score_threshold=CONTRADICTION_THRESHOLD
            )

            contradictions = []
            for hit in results.points:
                payload = hit.payload or {}
                existing = payload.get("content", "")

                # Simple heuristic: similar embedding but opposite meaning
                # (In production, use LLM for proper NLI)
                negation_patterns = ["不", "沒", "非", "未", "無", "not", "never", "no"]
                has_negation = any(p in content for p in negation_patterns) != any(p in existing for p in negation_patterns)

                if has_negation and hit.score > CONTRADICTION_THRESHOLD:
                    contradictions.append({
                        "point_id": str(hit.id),
                        "similarity": round(hit.score, 4),
                        "existing_content": existing[:200],
                        "contradiction_type": "negation_detected"
                    })

            result = {
                "status": "checked",
                "contradictions_found": len(contradictions),
                "contradictions": contradictions
            }
        else:
            # Scan all memories for contradictions
            points = scroll_all_points(collection, limit=200)
            contradictions = []

            for i, p in enumerate(points[:50]):  # Limit for performance
                payload = p.payload or {}
                content = payload.get("content", "")
                if not content:
                    continue

                vec_result = qdrant_client.retrieve(
                    collection_name=collection,
                    ids=[p.id],
                    with_vectors=True,
                    with_payload=False
                )
                if not vec_result or not vec_result[0].vector:
                    continue

                results = qdrant_client.query_points(
                    collection_name=collection,
                    query=vec_result[0].vector,
                    limit=5,
                    score_threshold=CONTRADICTION_THRESHOLD
                )

                for hit in results.points:
                    if str(hit.id) == str(p.id):
                        continue
                    hit_payload = hit.payload or {}
                    existing = hit_payload.get("content", "")

                    negation_patterns = ["不", "沒", "非", "未", "無", "not", "never"]
                    has_negation = any(p in content for p in negation_patterns) != any(p in existing for p in negation_patterns)

                    if has_negation:
                        contradictions.append({
                            "point_id_1": str(p.id),
                            "point_id_2": str(hit.id),
                            "similarity": round(hit.score, 4),
                            "preview_1": content[:100],
                            "preview_2": existing[:100]
                        })

            result = {
                "status": "scan_complete",
                "memories_scanned": min(50, len(points)),
                "contradictions_found": len(contradictions),
                "contradictions": contradictions[:10]
            }

        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"❌ mem_contradict failed: {str(e)}")]


async def tool_mem_time_travel(args: dict) -> list[types.TextContent]:
    """Time-Travel Query — 時間旅行查詢"""
    try:
        target_date = args.get("date", "")
        query = args.get("query", "")
        collection = args.get("collection", DEFAULT_COLLECTION)

        if not target_date or not query:
            return [types.TextContent(type="text", text="❌ Error: date and query are required")]

        try:
            target_dt = datetime.strptime(target_date, "%Y-%m-%d")
        except ValueError:
            return [types.TextContent(type="text", text="❌ Error: date must be YYYY-MM-DD format")]

        ensure_collection(collection)
        query_vector = get_embedding(query)

        # Get all points and filter by time
        points = scroll_all_points(collection, limit=500)
        valid_points = []

        for p in points:
            payload = p.payload or {}
            created_at = payload.get("created_at", "")
            superseded_at = payload.get("superseded_at")

            try:
                created_dt = datetime.fromisoformat(created_at.replace("Z", "").replace("+00:00", ""))
                # Memory was valid at target_date if:
                # 1. Created before or on target_date
                # 2. Not superseded, or superseded after target_date
                if created_dt <= target_dt:
                    if superseded_at:
                        superseded_dt = datetime.fromisoformat(superseded_at.replace("Z", "").replace("+00:00", ""))
                        if superseded_dt > target_dt:
                            valid_points.append(p)
                    else:
                        valid_points.append(p)
            except:
                continue

        # Search within valid points
        results = []
        for p in valid_points:
            vec_result = qdrant_client.retrieve(
                collection_name=collection,
                ids=[p.id],
                with_vectors=True,
                with_payload=True
            )
            if vec_result and vec_result[0].vector:
                search = qdrant_client.query_points(
                    collection_name=collection,
                    query=vec_result[0].vector,
                    limit=1
                )
                if search.points and search.points[0].score > SIMILARITY_THRESHOLD:
                    payload = vec_result[0].payload or {}
                    results.append({
                        "point_id": str(p.id),
                        "score": round(search.points[0].score, 4),
                        "content": payload.get("content", ""),
                        "created_at": payload.get("created_at", ""),
                        "was_valid_at": target_date
                    })

        results.sort(key=lambda x: x["score"], reverse=True)

        result = {
            "target_date": target_date,
            "query": query,
            "valid_memories_at_date": len(valid_points),
            "matching_results": results[:10]
        }
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"❌ mem_time_travel failed: {str(e)}")]


async def tool_mem_federated(args: dict) -> list[types.TextContent]:
    """Federated Search — 跨 Collection 聯邦搜索"""
    try:
        query = args.get("query", "")
        limit = min(args.get("limit", MAX_RESULTS), 20)

        if not query:
            return [types.TextContent(type="text", text="❌ Error: query is required")]

        collections = get_all_collection_names()
        query_vector = get_embedding(query)

        all_results = []
        for col_name in collections:
            try:
                stats = qdrant_client.get_collection(col_name)
                if stats.points_count == 0:
                    continue

                results = qdrant_client.query_points(
                    collection_name=col_name,
                    query=query_vector,
                    limit=limit,
                    score_threshold=SIMILARITY_THRESHOLD
                )

                for hit in results.points:
                    payload = hit.payload or {}
                    all_results.append({
                        "collection": col_name,
                        "score": round(hit.score, 4),
                        "point_id": str(hit.id),
                        "content": payload.get("content", "")[:300],
                        "tags": payload.get("tags", [])
                    })
            except Exception:
                continue

        # Sort by score across all collections
        all_results.sort(key=lambda x: x["score"], reverse=True)

        result = {
            "query": query,
            "collections_searched": len(collections),
            "total_results": len(all_results),
            "results": all_results[:limit * 2]
        }
        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"❌ mem_federated failed: {str(e)}")]


async def tool_mem_graph(args: dict) -> list[types.TextContent]:
    """Memory Knowledge Graph — 知識圖譜"""
    try:
        collection = args.get("collection", DEFAULT_COLLECTION)
        point_id = args.get("point_id", "")

        ensure_collection(collection)

        if point_id:
            # Find related memories for specific point
            vec_result = qdrant_client.retrieve(
                collection_name=collection,
                ids=[point_id],
                with_vectors=True,
                with_payload=True
            )
            if not vec_result:
                return [types.TextContent(type="text", text=f"⚠️ Memory not found: {point_id}")]

            vector = vec_result[0].vector
            payload = vec_result[0].payload or {}

            results = qdrant_client.query_points(
                collection_name=collection,
                query=vector,
                limit=10,
                score_threshold=0.7
            )

            related = []
            for hit in results.points:
                if str(hit.id) == point_id:
                    continue
                hit_payload = hit.payload or {}
                related.append({
                    "point_id": str(hit.id),
                    "similarity": round(hit.score, 4),
                    "content_preview": hit_payload.get("content", "")[:150],
                    "relation_type": "semantic_similar"
                })

            result = {
                "center": {
                    "point_id": point_id,
                    "content_preview": payload.get("content", "")[:200],
                    "tags": payload.get("tags", [])
                },
                "related_memories": related
            }
        else:
            # Build graph overview — find clusters
            points = scroll_all_points(collection, limit=100)
            clusters = []

            for i, p in enumerate(points[:20]):  # Sample for performance
                vec_result = qdrant_client.retrieve(
                    collection_name=collection,
                    ids=[p.id],
                    with_vectors=True,
                    with_payload=True
                )
                if not vec_result or not vec_result[0].vector:
                    continue

                results = qdrant_client.query_points(
                    collection_name=collection,
                    query=vec_result[0].vector,
                    limit=5,
                    score_threshold=0.85
                )

                if len(results.points) > 1:
                    cluster = {
                        "center_id": str(p.id),
                        "center_preview": (vec_result[0].payload or {}).get("content", "")[:100],
                        "cluster_size": len(results.points),
                        "members": [str(h.id) for h in results.points if str(h.id) != str(p.id)]
                    }
                    clusters.append(cluster)

            result = {
                "collection": collection,
                "total_memories": len(points),
                "clusters_found": len(clusters),
                "clusters": clusters[:10]
            }

        return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"❌ mem_graph failed: {str(e)}")]


async def tool_mem_health(args: dict) -> list[types.TextContent]:
    """Memory Health Report — 健康度報告"""
    try:
        collections = get_all_collection_names()
        now = datetime.now()

        report = {
            "timestamp": now.isoformat(),
            "collections": [],
            "overall_health": "unknown"
        }

        total_memories = 0
        total_issues = 0

        for col_name in collections:
            try:
                stats = qdrant_client.get_collection(col_name)
                points = scroll_all_points(col_name, limit=100)

                # Analyze health distribution
                healthy = 0
                warning = 0
                decayed = 0

                for p in points:
                    payload = p.payload or {}
                    created_at = payload.get("created_at", now.isoformat())
                    access_count = payload.get("access_count", 0)

                    try:
                        created_dt = datetime.fromisoformat(created_at.replace("Z", "").replace("+00:00", ""))
                        days_old = (now - created_dt).total_seconds() / 86400
                    except:
                        days_old = 0

                    # Simple health heuristic
                    if access_count > 5 or days_old < 7:
                        healthy += 1
                    elif access_count == 0 and days_old > 30:
                        decayed += 1
                    else:
                        warning += 1

                col_report = {
                    "name": col_name,
                    "total_points": stats.points_count,
                    "sampled": len(points),
                    "health_distribution": {
                        "healthy": healthy,
                        "warning": warning,
                        "decayed": decayed
                    },
                    "status": str(stats.status) if stats.status else "active"
                }
                report["collections"].append(col_report)
                total_memories += stats.points_count

                if decayed > healthy:
                    total_issues += 1

            except Exception as e:
                report["collections"].append({
                    "name": col_name,
                    "error": str(e)
                })
                total_issues += 1

        report["total_memories"] = total_memories
        report["overall_health"] = "healthy" if total_issues == 0 else f"{total_issues} issues detected"

        return [types.TextContent(type="text", text=json.dumps(report, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"❌ mem_health failed: {str(e)}")]


# ── Server Entry Point ──────────────────────────────────

async def main():
    """Start the MCP server"""
    from mcp.server.stdio import stdio_server
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
