#!/usr/bin/env python3
"""全量技能掃描引擎 — 掃描所有 SKILL.md，提取健康指標。"""
import re, json, os
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw/workspace"))

SKILLS_DIRS = [WORKSPACE / "skills", WORKSPACE / ".agents" / "skills"]

LANGUAGES = {
    "zh": "[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]",
    "ja": "[\u3040-\u309f\u30a0-\u30ff]",
    "ko": "[\uac00-\ud7af]",
    "ar": "[\u0600-\u06ff]",
    "hi": "[\u0900-\u097f]",
    "en": "[a-zA-Z]",
}


def extract_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter from SKILL.md."""
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return None
    fm = {}
    for line in m.group(1).split("\n"):
        kv = re.match(r"^(\w+):\s*(.*)", line)
        if kv:
            fm[kv.group(1)] = kv.group(2).strip()
    return fm


def detect_languages(text: str) -> list[str]:
    """Detect which languages are present in text."""
    found = []
    for lang, pattern in LANGUAGES.items():
        if re.search(pattern, text):
            found.append(lang)
    return found


def scan_skill(skill_dir: Path) -> dict | None:
    """Scan a single skill directory."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None

    content = skill_md.read_text(encoding="utf-8")
    fm = extract_frontmatter(content)

    if not fm:
        return {
            "name": skill_dir.name,
            "path": str(skill_dir),
            "status": "critical",
            "issue": "NO_FRONTMATTER",
            "description_langs": [],
        }

    desc = fm.get("description", "")
    has_name = bool(fm.get("name"))
    has_desc = bool(desc)

    desc_langs = detect_languages(desc)

    # Determine status
    if not has_desc or len(desc) < 3:
        status = "critical"
        issue = "EMPTY_DESCRIPTION" if not has_desc else "BROKEN_DESCRIPTION"
    elif "zh" not in desc_langs:
        status = "warning"
        issue = "NO_CHINESE"
    elif len(desc_langs) < 2:
        status = "healthy"
        issue = None  # Has Chinese, that's the minimum requirement
    else:
        status = "healthy"
        issue = None

    return {
        "name": fm.get("name", skill_dir.name),
        "dir": skill_dir.name,
        "path": str(skill_dir),
        "status": status,
        "issue": issue,
        "description": desc[:120],
        "description_langs": desc_langs,
        "has_name": has_name,
        "has_desc": has_desc,
        "size": len(content),
    }


def scan_all() -> list[dict]:
    """Scan all skills across all directories."""
    results = []
    for skills_dir in SKILLS_DIRS:
        if not skills_dir.exists():
            continue
        for skill_dir in sorted(skills_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            result = scan_skill(skill_dir)
            if result:
                result["source"] = str(skills_dir)
                results.append(result)
    return results


def summary(results: list[dict]) -> dict:
    """Generate scan summary."""
    return {
        "total": len(results),
        "critical": sum(1 for r in results if r["status"] == "critical"),
        "warning": sum(1 for r in results if r["status"] == "warning"),
        "healthy": sum(1 for r in results if r["status"] == "healthy"),
    }


if __name__ == "__main__":
    results = scan_all()
    s = summary(results)
    print(f"總計: {s['total']} | 🔴致命 {s['critical']} | 🟡警告 {s['warning']} | 🟢健康 {s['healthy']}")
    for r in results:
        if r["status"] != "healthy":
            print(f"  {r['status'].upper()}: {r['name']} — {r['issue']}")
