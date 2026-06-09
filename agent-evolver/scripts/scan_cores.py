#!/usr/bin/env python3
"""核心文件掃描引擎 — 讀取全部核心文件，計算行數和增長趨勢。"""
import json, os
from datetime import datetime
from pathlib import Path
from typing import TypedDict

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw/workspace"))
EVOLVER_DIR = WORKSPACE / "memory" / "evolver"

CORE_FILES = {
    "SOUL.md": "性格設定",
    "AGENTS.md": "啟動流程與記憶規則",
    "USER.md": "用戶理解",
    "MEMORY.md": "長期記憶",
    "RULES.md": "規則速查",
    "PERMANENT-RULES.md": "永久規則",
}


class FileStats(TypedDict):
    file: str
    label: str
    lines: int
    chars: int
    growth_pct: float | None
    last_month_lines: int | None


def count_file(filepath: Path) -> tuple[int, int]:
    """Count lines and characters in a file."""
    try:
        content = filepath.read_text(encoding="utf-8")
        return len(content.split("\n")), len(content)
    except FileNotFoundError:
        return 0, 0


def load_last_month() -> dict:
    """Load previous month stats if available."""
    evolver_dir = EVOLVER_DIR
    if not evolver_dir.exists():
        return {}

    files = sorted(evolver_dir.glob("*.json"))
    if not files:
        return {}

    try:
        return json.loads(files[-1].read_text())
    except Exception:
        return {}


def save_stats(stats: list[FileStats]):
    """Save current month stats."""
    evolver_dir = EVOLVER_DIR
    evolver_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    filename = f"{now.year}-{now.month:02d}.json"

    data = {
        "date": now.strftime("%Y-%m-%d"),
        "files": {s["file"]: {"lines": s["lines"], "chars": s["chars"]} for s in stats},
    }
    (evolver_dir / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2))


def scan() -> list[FileStats]:
    """Scan all core files and return stats."""
    last_month = load_last_month()
    stats = []

    for filename, label in CORE_FILES.items():
        filepath = WORKSPACE / filename
        lines, chars = count_file(filepath)
        last_lines = last_month.get("files", {}).get(filename, {}).get("lines")

        if last_lines and last_lines > 0:
            growth_pct = round((lines - last_lines) / last_lines * 100, 1)
        else:
            growth_pct = None
            last_lines = None

        stats.append(
            {
                "file": filename,
                "label": label,
                "lines": lines,
                "chars": chars,
                "growth_pct": growth_pct,
                "last_month_lines": last_lines,
            }
        )

    save_stats(stats)
    return stats


def check_growth_alarm(stats: list[FileStats], threshold: float = 20.0) -> dict:
    """Check if total growth exceeds threshold."""
    total_lines = sum(s["lines"] for s in stats)
    total_last = sum(s["last_month_lines"] or s["lines"] for s in stats)

    if total_last > 0:
        growth = (total_lines - total_last) / total_last * 100
    else:
        growth = 0

    return {
        "triggered": growth > threshold,
        "total_lines": total_lines,
        "total_last": total_last,
        "growth_pct": round(growth, 1),
        "threshold": threshold,
    }


if __name__ == "__main__":
    stats = scan()
    alarm = check_growth_alarm(stats)

    print("=== 核心文件掃描 ===")
    for s in stats:
        growth_str = f"({s['growth_pct']:+.1f}%)" if s["growth_pct"] is not None else "(首次)"
        print(f"  {s['file']}: {s['lines']} 行 {growth_str}")

    print(f"\n總計: {alarm['total_lines']} 行 ({alarm['growth_pct']:+.1f}%)")
    if alarm["triggered"]:
        print(f"🚨 增長過快！月增 >{alarm['threshold']}%")
    else:
        print(f"✅ 增長正常 (<{alarm['threshold']}%)")
