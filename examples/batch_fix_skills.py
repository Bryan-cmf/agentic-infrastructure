#!/usr/bin/env python3
"""批量為缺失中文關鍵詞的技能補上 trigger keywords"""
import re
from pathlib import Path

FIXES = {
    # 方法論技能（設計討論時最需要）
    "software-architect": "架構設計 系統設計 軟件架構 技術架構 系統架構 架構師",
    "architecture-patterns": "設計模式 架構模式 系統模式 軟件模式 架構風格",
    "caveman": "簡化設計 降級方案 最簡單方案 砍功能 做減法 極簡設計",
    "grill-with-docs": "文檔審查 需求質疑 設計挑戰 方案壓力測試 文檔驅動審查",
    "grill-me": "設計壓力測試 方案質疑 深度訪談 方案審查 設計面試",
    "diagnose": "故障診斷 根因分析 Debug 排查問題 問題診斷 找原因",
    "prototype": "原型設計 快速原型 先做個demo 原型驗證 試一試",
    "improve-codebase-architecture": "架構改進 代碼重構 架構優化 代碼整理 架構整理",
    "tdd": "測試驅動開發 先寫測試 紅綠重構 單元測試 集成測試",
    "triage": "問題分類 問題分級 Bug分類 任務優先級 問題排序",
    "write-a-skill": "創建技能 寫技能 製作技能 新建技能 技能模板",
    "zoom-out": "全局視角 高層次視角 俯瞰代碼 大局觀 宏觀視角",
    "to-prd": "轉PRD 生成需求文檔 對話轉需求 輸出PRD",
    "to-issues": "生成Issue 轉任務 拆分任務 創建Issue",
    "handoff": "任務交接 交接文檔 轉交任務 交接給其他Agent",
    
    # 系統技能
    "self-improving-agent": "自我改進 持續改進 記錄教訓 錯誤學習 自我優化",
    "agent-analytics": "數據分析 使用分析 統計報告 用量分析",
    "agent-access-control": "訪問控制 權限管理 安全控制 陌生人攔截",
    "agent-rate-limiter": "速率限制 頻率控制 429防護 請求節流",
    "agent-task-tracker": "任務追蹤 任務狀態 進度管理 任務管理",
    "agent-audit": "系統審計 安全審計 代碼審計 合規檢查",
    
    # Claude Code 相關
    "claude-code": "ClaudeCode CC編程 打開CC 啟動CC",
    "react-best-practices": "React最佳實踐 React性能 NextJS優化",
    
    # Media skills (broken format → fix)
    "agnes-ai": "AgnesAI 文字模型 對話模型 免費AI模型",
    "agnes-image": "Agnes圖片 圖片生成 AI繪圖 文生圖",
    "agnes-video": "Agnes影片 影片生成 AI影片 文生影片",
    "skill-analysis": "技能分析 技能評估 技術分析 源碼分析",
    "omp-bridge": "oh-my-pi橋接 OMP橋接 飛書OMP",
}

WORKSPACE = Path.home() / ".openclaw/workspace"
SKILLS_DIRS = [
    WORKSPACE / "skills",
    WORKSPACE / ".agents/skills",
]

def fix_skill(skill_dir, keywords):
    """Add Chinese keywords to a skill's description."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, "NOT FOUND"
    
    content = skill_md.read_text(encoding="utf-8")
    
    # Extract frontmatter
    m = re.match(r"^(---\n.*?\n---)", content, re.DOTALL)
    if not m:
        return False, "NO FRONTMATTER"
    
    frontmatter = m.group(1)
    rest = content[len(frontmatter):]
    
    # Find description line
    desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    if not desc_match:
        return False, "NO DESCRIPTION"
    
    old_desc = desc_match.group(1).strip()
    
    # If already has Chinese, check if our keywords are covered
    has_cn = bool(re.search(r'[\u4e00-\u9fff]', old_desc))
    
    kw_str = " ".join(keywords)
    if has_cn:
        # Already has Chinese - prepend our keywords if missing
        new_desc = f"{kw_str} {old_desc}"
    else:
        # No Chinese at all
        new_desc = f"{kw_str} {old_desc}"
    
    # If nothing changed
    if new_desc == old_desc:
        return True, "ALREADY OK"
    
    # Replace in frontmatter
    new_frontmatter = frontmatter.replace(
        f"description: {old_desc}",
        f"description: {new_desc}",
        1
    )
    
    if new_frontmatter == frontmatter:
        # Try regex replacement for multiline/broken descriptions
        new_frontmatter = re.sub(
            r"(^description:\s*).*$",
            f"\\1{new_desc}",
            frontmatter,
            flags=re.MULTILINE
        )
    
    new_content = new_frontmatter + rest
    
    # Backup
    bak = str(skill_md) + ".bak"
    skill_md.rename(bak)
    skill_md.write_text(new_content, encoding="utf-8")
    
    return True, f"OK ({len(old_desc)}→{len(new_desc)} chars, +{'✅CN' if not has_cn else '🔄CN+'})"


def main():
    fixed = []
    skipped = []
    
    for name, keywords in FIXES.items():
        found = False
        for skills_dir in SKILLS_DIRS:
            skill_dir = skills_dir / name
            if skill_dir.exists():
                ok, msg = fix_skill(skill_dir, keywords)
                if ok:
                    fixed.append(f"✅ {name}: {msg}")
                else:
                    skipped.append(f"❌ {name}: {msg}")
                found = True
                break
        if not found:
            skipped.append(f"🔍 {name}: NOT FOUND in any skills dir")
    
    print(f"修復完成: {len(fixed)} 個")
    for f in fixed:
        print(f"  {f}")
    if skipped:
        print(f"跳過: {len(skipped)} 個")
        for s in skipped:
            print(f"  {s}")

if __name__ == "__main__":
    main()
