#!/usr/bin/env python3
"""批量為缺失中文關鍵詞的技能自動注入觸發詞。支援 auto-detect 模式。"""
import re, sys
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
SKILLS_DIRS = [WORKSPACE / "skills", WORKSPACE / ".agents" / "skills"]

# Auto-detect keywords from skill name
def auto_detect_keywords(name: str) -> list[str]:
    patterns = {
        "software-architect": ["架構設計", "系統設計", "軟件架構"],
        "architecture": ["設計模式", "架構模式", "系統模式"],
        "caveman": ["簡化設計", "降級方案", "最簡單方案"],
        "diagnose": ["故障診斷", "根因分析", "Debug"],
        "grill": ["文檔審查", "設計挑戰", "方案質疑"],
        "tdd": ["測試驅動開發", "單元測試"],
        "handoff": ["任務交接", "轉交任務"],
        "triage": ["問題分類", "問題分級"],
        "prototype": ["原型設計", "快速原型"],
        "evolver": ["自我進化", "核心文件重塑"],
        "curator": ["技能管理", "技能策展"],
        "report": ["報告生成", "數據匯報"],
        "agent-": ["Agent管理", "自動化"],
        "qwen": ["Qwen服務", "阿里雲"],
        "memory": ["記憶管理", "記憶系統"],
        "trigger": ["技能觸發", "關鍵詞", "多語言"],
        "router": ["路由", "任務匹配"],
        "previsor": ["預判", "風險分析", "路徑推演"],
        "finance": ["財務分析", "金融分析"],
        "deploy": ["部署", "上線", "發布"],
        "docker": ["容器管理", "Docker"],
        "react": ["React開發", "前端框架"],
    }
    for key, kws in patterns.items():
        if key in name:
            return kws
    return []

def fix_skills(auto_detect=False, dry_run=False):
    fixed = 0
    for base in SKILLS_DIRS:
        if not base.exists():
            continue
        for skill_dir in sorted(base.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            content = skill_md.read_text(encoding="utf-8")
            m = re.match(r"^(---\n.*?\n---)", content, re.DOTALL)
            if not m:
                continue
            fm = m.group(1)
            rest = content[len(fm):]
            dm = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
            if not dm:
                continue
            old = dm.group(1).strip()
            if re.search(r'[\u4e00-\u9fff]', old):  # Already has Chinese
                continue
            kws = auto_detect_keywords(skill_dir.name) if auto_detect else None
            if not kws:
                continue
            kw_str = " ".join(kws)
            new_desc = f"{kw_str} {old}"
            new_fm = fm.replace(f"description: {old}", f"description: {new_desc}", 1)
            if not dry_run:
                skill_md.rename(str(skill_md) + ".bak")
                skill_md.write_text(new_fm + rest, encoding="utf-8")
            fixed += 1
    print(f"{'[DRY RUN] ' if dry_run else ''}Fixed: {fixed} skills")
    return fixed

if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    auto = "--auto-detect" in sys.argv
    fix_skills(auto_detect=auto, dry_run=dry)
