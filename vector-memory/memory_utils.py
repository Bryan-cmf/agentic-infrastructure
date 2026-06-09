#!/usr/bin/env python3
"""
向量記憶系統 — 共享工具模塊
=============================
抽取 auto_sync / batch_import / consistency_check 的公共邏輯。

包含：
  - chunk_text()         智能分塊（支持 Markdown-Aware）
  - should_skip()        文件過濾
  - get_tags_from_path() 自動標籤
  - collect_files()      文件收集
  - atomic_write_json()  原子寫入
  - load_state()         狀態讀取
  - save_state()         狀態保存（原子）
"""

import os
import re
import json
import uuid
from pathlib import Path
from typing import Optional

# ── Config ──────────────────────────────────────────
WORKSPACE = Path(os.getenv("MEMORY_WORKSPACE", str(Path.home() / ".openclaw" / "workspace")))
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_MD = WORKSPACE / "MEMORY.md"
PROJECT_ROOT = Path(__file__).parent

MIN_CHUNK_CHARS = 80
TARGET_CHUNK_CHARS = 800
MAX_CHUNK_CHARS = 1500

SKIP_PATTERNS = [
    "emails", "email", "cc_notifications", "dream-log.md",
    "archive", "episodes", "procedures", "follow_up",
    "notification", "heartbeat-state", "task-status",
    "checker-review", "checker-approval", "research-analyst",
    "main-heartbeat", "task-handover", "dreams", ".dreams",
    "email_notification", "email_drafts",
]

# Markdown heading regex
MD_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def should_skip(path: Path) -> bool:
    """Check if path matches any skip pattern"""
    path_str = str(path).lower()
    for pat in SKIP_PATTERNS:
        if pat in path_str:
            return True
    return False


def get_tags_from_path(path: Path) -> list[str]:
    """Generate tags from file path — supports all coder-* agents sharing workspace"""
    tags = []
    try:
        rel = path.relative_to(WORKSPACE).parts
    except ValueError:
        return ["format:" + path.suffix.lstrip(".")]

    if "memory" in rel:
        idx = rel.index("memory")
        sub = rel[idx + 1:] if idx + 1 < len(rel) else []
        if sub:
            cat = sub[0].replace(".md", "").replace(".json", "")
            tags.append(cat)
            # Sub-category for deeper paths
            if len(sub) > 1:
                subcat = sub[1].replace(".md", "").replace(".json", "")
                tags.append(f"sub:{subcat}")

    # Date tag from filename
    name = path.stem
    date_match = re.match(r"(\d{4}-\d{2}-\d{2})", name)
    if date_match:
        tags.append(f"date:{date_match.group(1)}")

    # Project tag
    if "projects" in str(path):
        tags.append(f"project:{name}")

    # Agent tag (coder-qwen, main, ecc, etc.)
    try:
        agent_rel = path.relative_to(Path.home() / ".openclaw" / "agents")
        agent_name = agent_rel.parts[0]
        tags.append(f"agent:{agent_name}")
    except ValueError:
        pass

    # File type tag
    tags.append(f"format:{path.suffix.lstrip('.')}")

    return tags


def _extract_markdown_sections(text: str) -> list[dict]:
    """
    將 Markdown 文本按標題拆分為 sections。
    每個 section 包含 heading_level, heading_text, content。
    用於 Markdown-Aware Chunking。
    """
    sections = []
    lines = text.split("\n")
    current_section = {"level": 0, "heading": "", "content": ""}

    for line in lines:
        m = re.match(r"^(#{1,6})\s+(.+)$", line)
        if m:
            # Save previous section
            if current_section["content"].strip():
                sections.append(current_section)
            level = len(m.group(1))
            heading = m.group(2).strip()
            current_section = {"level": level, "heading": heading, "content": line + "\n"}
        else:
            current_section["content"] += line + "\n"

    # Last section
    if current_section["content"].strip():
        sections.append(current_section)

    return sections


def chunk_text(text: str, source: str, markdown_aware: bool = True) -> list[dict]:
    """
    智能分塊 — 支持 Markdown-Aware 模式。

    策略：
    1. 如果有 Markdown 標題 → 按標題分 section
    2. 每個 section 再按段落長度合併/拆分
    3. 每個 chunk 附帶 section_path metadata
    """
    text = text.strip()
    if not text:
        return []

    if markdown_aware and re.search(r"^#{1,6}\s+", text, re.MULTILINE):
        return _chunk_markdown(text, source)
    else:
        return _chunk_plain(text, source)


def _chunk_markdown(text: str, source: str) -> list[dict]:
    """Markdown-Aware chunking — 按標題結構分塊"""
    sections = _extract_markdown_sections(text)
    chunks = []
    section_path = []

    for sec in sections:
        # Track section hierarchy
        while section_path and section_path[-1][0] >= sec["level"]:
            section_path.pop()
        if sec["level"] > 0:
            section_path.append((sec["level"], sec["heading"]))

        # Build section path string
        sec_path = " > ".join([h for _, h in section_path]) if section_path else ""

        # Chunk the section content
        section_chunks = _chunk_plain(sec["content"], source)
        for c in section_chunks:
            c["section_path"] = sec_path
            c["section_heading"] = sec["heading"]

        chunks.extend(section_chunks)

    return chunks


def _chunk_plain(text: str, source: str) -> list[dict]:
    """Plain text chunking — 按段落分塊（修復短段落丟失 Bug）"""
    text = text.strip()
    if not text:
        return []

    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # FIX: 短段落處理 — 無論 current_chunk 是否為空都累積
        if len(para) < MIN_CHUNK_CHARS:
            if current_chunk:
                if len(current_chunk) + len(para) + 2 < MAX_CHUNK_CHARS:
                    current_chunk += "\n\n" + para
                    continue
                else:
                    # current_chunk is full, save it first
                    if len(current_chunk) >= MIN_CHUNK_CHARS:
                        chunks.append({"content": current_chunk, "char_length": len(current_chunk)})
                    current_chunk = para
                    continue
            else:
                # 無前文 → 累積短段落
                current_chunk = para
                continue

        # current_chunk 有足夠內容 → 保存
        if len(current_chunk) >= MIN_CHUNK_CHARS:
            chunks.append({"content": current_chunk, "char_length": len(current_chunk)})

        # 處理超長段落
        if len(para) > MAX_CHUNK_CHARS:
            sentences = re.split(r"(?<=[。！？.!?\n])\s*", para)
            sub_chunk = ""
            for sent in sentences:
                if len(sub_chunk) + len(sent) > TARGET_CHUNK_CHARS and len(sub_chunk) >= MIN_CHUNK_CHARS:
                    chunks.append({"content": sub_chunk.strip(), "char_length": len(sub_chunk)})
                    sub_chunk = sent
                else:
                    sub_chunk += " " + sent if sub_chunk else sent
            current_chunk = sub_chunk.strip()
        else:
            current_chunk = para

    # 最後一個 chunk（即使 < MIN_CHUNK_CHARS 也保留，避免丟失內容）
    if current_chunk.strip():
        if len(current_chunk) >= MIN_CHUNK_CHARS or not chunks:
            chunks.append({"content": current_chunk.strip(), "char_length": len(current_chunk)})

    for c in chunks:
        c["source"] = source
        if "section_path" not in c:
            c["section_path"] = ""

    return chunks


def collect_files(extra_paths: Optional[list[Path]] = None) -> list[Path]:
    """收集所有記憶文件"""
    files = []

    if MEMORY_MD.exists():
        files.append(MEMORY_MD)

    if MEMORY_DIR.exists():
        for path in MEMORY_DIR.rglob("*"):
            if not path.is_file():
                continue
            if should_skip(path):
                continue
            if path.suffix not in (".md", ".json", ".yaml", ".yml", ".txt"):
                continue
            if path.name.startswith("."):
                continue
            if path.stat().st_size > 500_000:
                continue
            files.append(path)

    # Extra paths (e.g., agent-specific memory dirs)
    if extra_paths:
        for p in extra_paths:
            if p.exists() and p.is_file() and p not in files:
                files.append(p)

    return sorted(files)


def atomic_write_json(path: Path, data: dict):
    """原子寫入 JSON — 防止 crash 導致狀態文件損壞"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    tmp.rename(path)  # atomic on macOS/APFS


def load_state(state_file: Path) -> dict:
    """Load sync state {filepath: mtime}"""
    if state_file.exists():
        try:
            return json.loads(state_file.read_text())
        except json.JSONDecodeError:
            # Corrupted state file — start fresh
            return {}
    return {}


def save_state(state_file: Path, state: dict):
    """Save sync state (atomic)"""
    atomic_write_json(state_file, state)


def generate_content_id(source: str, content: str, prefix: str = "") -> str:
    """Generate deterministic UUID for content — 避免碰撞"""
    seed = f"{prefix}:{source}:{content[:200]}" if prefix else f"{source}:{content[:200]}"
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, seed))
