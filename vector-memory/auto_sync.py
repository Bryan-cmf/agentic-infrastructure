#!/usr/bin/env python3
"""
記憶自動同步腳本 — 檔案層 ↔ 向量層
檢測檔案變更 → 增量分塊 → embedding → upsert 到 Qdrant
支援：新增、修改（自動覆蓋）、刪除（可選清理）

v2.0 — 使用 memory_utils 共享模塊
修復：短段落丟失 Bug / 原子寫入 / Markdown-Aware 分塊
"""

import os
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer

from memory_utils import (
    chunk_text, should_skip, get_tags_from_path, collect_files,
    load_state, save_state, generate_content_id,
    WORKSPACE, MEMORY_DIR, MEMORY_MD, PROJECT_ROOT,
)

# ── Config ──────────────────────────────────────────
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
COLLECTION = os.getenv("COLLECTION", "openclaw_mem")
STATE_FILE = PROJECT_ROOT / "sync_state.json"


def main():
    start_time = datetime.now(timezone.utc)
    print(f"🔄 記憶自動同步 v2.0 — {start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 50)

    # ── Load model ──
    print("📥 載入 Embedding 模型...")
    model = SentenceTransformer(MODEL_NAME, device="mps")

    # ── Connect Qdrant ──
    client = QdrantClient(url=QDRANT_URL)

    # Ensure collection with dynamic embedding dimension
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION not in collections:
        vector_size = model.get_sentence_embedding_dimension()
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE, on_disk=True)
        )
        print(f"📦 Created collection {COLLECTION} ({vector_size}dim)")

    # ── Load state ──
    old_state = load_state(STATE_FILE)
    old_paths = set(old_state.keys())

    # ── Scan files ──
    files = collect_files()
    new_state = {}
    new_paths = set()

    changed_files = []
    for f in files:
        rel = str(f.relative_to(WORKSPACE))
        mtime = f.stat().st_mtime
        new_state[rel] = mtime
        new_paths.add(rel)
        if rel not in old_state or old_state[rel] != mtime:
            changed_files.append(f)

    # ── Detect deletions ──
    deleted_paths = old_paths - new_paths
    deleted_count = 0
    if deleted_paths:
        for del_path in deleted_paths:
            try:
                results = client.scroll(
                    collection_name=COLLECTION,
                    scroll_filter=Filter(
                        must=[FieldCondition(key="source", match=MatchValue(value=del_path))]
                    ),
                    limit=200,
                )
                point_ids = [p.id for p in results[0]]
                if point_ids:
                    client.delete(collection_name=COLLECTION, points_selector=point_ids)
                    deleted_count += len(point_ids)
            except Exception as e:
                print(f"  ⚠️  刪除失敗 {del_path}: {e}")

    if not changed_files:
        print(f"\n✅ 無變更（{len(files)} 個文件已同步）")
        if deleted_count:
            print(f"🗑️  已清理 {deleted_count} 條已刪除文件的向量")
        save_state(STATE_FILE, new_state)
        print(f"💾 狀態已保存")
        return

    # ── Process changed files ──
    print(f"\n📝 檢測到 {len(changed_files)} 個變更文件...")
    all_chunks = []
    for f in changed_files:
        try:
            content = f.read_text(encoding="utf-8")
        except Exception as e:
            print(f"  ⚠️  讀取失敗: {f.name}: {e}")
            continue
        rel = str(f.relative_to(WORKSPACE))
        # Remove old chunks for this file first
        try:
            results = client.scroll(
                collection_name=COLLECTION,
                scroll_filter=Filter(
                    must=[FieldCondition(key="source", match=MatchValue(value=rel))]
                ),
                limit=200,
            )
            old_ids = [p.id for p in results[0]]
            if old_ids:
                client.delete(collection_name=COLLECTION, points_selector=old_ids)
        except Exception:
            pass

        # Use markdown-aware chunking
        chunks = chunk_text(content, rel, markdown_aware=True)
        tags = get_tags_from_path(f)
        for c in chunks:
            c["tags"] = tags
            c["filename"] = f.name
        all_chunks.extend(chunks)
        print(f"  📄 {f.name}: {len(chunks)} chunks")

    if not all_chunks:
        print("⚠️  無有效 chunks")
        save_state(STATE_FILE, new_state)
        return

    # ── Embed & Upsert ──
    print(f"\n🧠 Embedding + 寫入 {len(all_chunks)} chunks...")
    BATCH_SIZE = 50
    imported = 0
    for i in range(0, len(all_chunks), BATCH_SIZE):
        batch = all_chunks[i:i + BATCH_SIZE]
        texts = [c["content"] for c in batch]
        embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)

        points = []
        for j, chunk in enumerate(batch):
            cid = generate_content_id(chunk["source"], chunk["content"], prefix="sync")
            points.append(PointStruct(
                id=cid,
                vector=embeddings[j].tolist(),
                payload={
                    "content": chunk["content"],
                    "source": chunk["source"],
                    "filename": chunk.get("filename", ""),
                    "tags": chunk.get("tags", []),
                    "section_path": chunk.get("section_path", ""),
                    "char_length": chunk.get("char_length", len(chunk["content"])),
                    "synced_at": datetime.now().isoformat(),
                    "access_count": 0,
                    "last_accessed": datetime.now().isoformat(),
                }
            ))
        client.upsert(collection_name=COLLECTION, points=points)
        imported += len(points)
        pct = min(100, int((i + BATCH_SIZE) / len(all_chunks) * 100))
        print(f"   [{pct:3d}%] {imported}/{len(all_chunks)}", end="\r")

    # ── Save state (atomic) ──
    save_state(STATE_FILE, new_state)

    # ── Summary ──
    stats = client.get_collection(COLLECTION)
    elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
    print(f"\n\n{'=' * 50}")
    print(f"✅ 同步完成！")
    print(f"   變更文件: {len(changed_files)} 個")
    print(f"   新增/更新 chunks: {imported} 個")
    if deleted_count:
        print(f"   清理向量: {deleted_count} 條")
    print(f"   向量總數: {stats.points_count} 條")
    print(f"   耗時: {elapsed:.1f}s")
    print(f"   💾 狀態已保存到 {STATE_FILE}")


if __name__ == "__main__":
    main()
