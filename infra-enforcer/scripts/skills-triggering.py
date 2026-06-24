#!/usr/bin/env python3
"""skills-triggering.py — Multilingual keyword audit & injection for SKILL.md.

Checks whether each skill's `description` frontmatter contains CJK keywords
(Traditional/Simplified Chinese, Japanese, Korean) so non-English users can
trigger the skill. Skills lacking CJK keywords are invisible to those users.

Modes:
  (default)  Dry-run audit: report which skills lack CJK keywords, suggest
             what to inject. Writes nothing.
  --apply    Actually rewrite the description fields (backs up each file to
             <file>.bak-<ts> first). Use sparingly; review the dry-run first.

Usage:
  python3 skills-triggering.py                              # audit ~/.zcode/skills
  python3 skills-triggering.py --skills-dir /path/to/skills
  python3 skills-triggering.py --skills-dir DIR --apply     # rewrite + backup

This is the "Path A" script referenced by the skills-triggering skill and
agentic-infra Step 3. It complements scan_all.py (which reports health) by
offering to *fix* the CJK-coverage gap.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
# Languages we consider "trigger-capable" for non-English users.
CJK_RE = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]")

# Minimal canonical keyword packs per domain. Used only to SUGGEST keywords
# when a description is purely English — we never inject blindly; the dry-run
# shows the proposal for human review.
SUGGESTED_KEYWORDS = {
    "default": "技能 技能觸發 多語言",
    "code": "代碼 開發 程式",
    "design": "設計 前端 UI",
    "finance": "金融 股票 估值",
    "writing": "寫作 文案 報告",
}


def parse_frontmatter(text):
    """Return (fm_text, body_text, desc_line_tuple). desc_line_tuple =
    (start_offset_in_fm, raw_value) or None if no description line."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text, None
    fm = m.group(1)
    # Find the description line within frontmatter, recording its offset.
    for i, line in enumerate(fm.split("\n")):
        kv = re.match(r"^(\s*description\s*:\s*)(.*)$", line)
        if kv:
            return fm, text[m.end() - len(fm):], (i, kv.group(2), kv.group(1))
    return fm, text, None


def detect_domain(desc):
    d = desc.lower()
    if any(w in d for w in ("code", "develop", "frontend", "backend", "deploy", "bug")):
        return "code"
    if any(w in d for w in ("design", "ui", "ux", "css", "web")):
        return "design"
    if any(w in d for w in ("finance", "stock", "valuation", "dcf", "financial")):
        return "finance"
    if any(w in d for w in ("write", "blog", "report", "essay", "content")):
        return "writing"
    return "default"


def audit_skill(skill_dir):
    """Audit one skill. Returns a report dict."""
    skill_md = skill_dir / "SKILL.md"
    name = skill_dir.name
    report = {"name": name, "path": str(skill_md)}
    if not skill_md.exists():
        report["status"] = "missing"
        return report
    text = skill_md.read_text(encoding="utf-8")
    fm, body, desc_info = parse_frontmatter(text)
    if not fm:
        report["status"] = "no_frontmatter"
        return report
    if not desc_info:
        report["status"] = "no_description"
        return report
    _, raw_desc, _ = desc_info
    desc = raw_desc.strip().strip('"').strip("'")
    has_cjk = bool(CJK_RE.search(desc))
    report["description"] = desc[:100]
    report["has_cjk"] = has_cjk
    if has_cjk:
        report["status"] = "ok"
        return report
    report["status"] = "lacks_cjk"
    domain = detect_domain(desc)
    report["suggested_domain"] = domain
    report["suggested_keywords"] = SUGGESTED_KEYWORDS.get(domain, SUGGESTED_KEYWORDS["default"])
    return report


def apply_injection(skill_dir):
    """Rewrite the description to append suggested CJK keywords. Returns
    True if changed, False if skipped (already has CJK / no description)."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False
    text = skill_md.read_text(encoding="utf-8")
    fm, body, desc_info = parse_frontmatter(text)
    if not fm or not desc_info:
        return False
    line_idx, raw_desc, prefix = desc_info
    desc = raw_desc.strip().strip('"').strip("'")
    if CJK_RE.search(desc):
        return False  # already has CJK
    domain = detect_domain(desc)
    kws = SUGGESTED_KEYWORDS.get(domain, SUGGESTED_KEYWORDS["default"])
    # Preserve quoting style: if original was quoted, keep quotes.
    was_quoted = raw_desc.strip().startswith(('"', "'"))
    q = raw_desc.strip()[0] if was_quoted else ""
    new_desc = f"{desc} {kws}".strip()
    if was_quoted:
        new_raw = f'{q}{new_desc}{q}'
    else:
        new_raw = new_desc
    fm_lines = fm.split("\n")
    fm_lines[line_idx] = prefix + new_raw
    new_fm = "\n".join(fm_lines)
    new_text = f"---\n{new_fm}\n---\n{body}"
    # Backup then write.
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = skill_md.with_suffix(f".md.bak-{ts}")
    shutil.copy2(skill_md, backup)
    skill_md.write_text(new_text, encoding="utf-8")
    return True


def main():
    ap = argparse.ArgumentParser(description="Audit/inject CJK trigger keywords in SKILL.md descriptions.")
    ap.add_argument("--skills-dir", default=os.path.expanduser("~/.zcode/skills"))
    ap.add_argument("--apply", action="store_true", help="Rewrite descriptions (backs up first). Default is dry-run.")
    ap.add_argument("--json", action="store_true", help="Emit JSON report.")
    args = ap.parse_args()

    root = Path(args.skills_dir)
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        sys.exit(2)

    reports = []
    applied = 0
    for child in sorted(root.iterdir()):
        if not child.is_dir() or child.name.startswith("."):
            continue
        r = audit_skill(child)
        reports.append(r)
        if args.apply and r.get("status") == "lacks_cjk":
            if apply_injection(child):
                applied += 1
                r["applied"] = True

    lacks = [r for r in reports if r.get("status") == "lacks_cjk"]
    if args.json:
        out = {
            "skills_dir": str(root),
            "scanned": len(reports),
            "lacks_cjk": len(lacks),
            "applied": applied if args.apply else None,
            "mode": "apply" if args.apply else "dry-run",
            "reports": reports,
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(f"掃描 {len(reports)} 個技能 | 缺 CJK 關鍵詞: {len(lacks)} | 模式: {'apply(已改寫 '+str(applied)+')' if args.apply else 'dry-run'}")
        for r in lacks:
            sug = r.get("suggested_keywords", "")
            print(f"  ⚠️ {r['name']}: 缺 CJK → 建議加 [{sug}]")
            print(f"     現況: {r.get('description','')[:80]}")
    # Exit non-zero if any lack CJK, so callers (watchdog) can gate on it.
    sys.exit(1 if lacks else 0)


if __name__ == "__main__":
    main()
