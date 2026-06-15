#!/usr/bin/env python3
"""
score_enforcer.py — 外部獨立合規審計器（LLM 無法干預）

功能：
  1. 掃描當前 session 的最新回覆
  2. 檢查每條回覆是否包含 🔀 Router 行 + 🛡️ Compliance 行
  3. 缺失 → 自動更新 score.json 扣分
  4. 連續 3 次 PASS → +0.1 分
  5. 分數 ≤ 0 → 💀 DEATH → 觸發 Bootstrap

用法：
  python3 scripts/score_enforcer.py              # 單次掃描
  python3 scripts/score_enforcer.py --cron        # cron 模式（只檢查新回覆）
  python3 scripts/score_enforcer.py --reset       # 重置分數到 10.0
  python3 scripts/score_enforcer.py --status      # 只顯示當前分數
  python3 scripts/score_enforcer.py --omlx-check  # OMLX L3 外部驗證：掃描 system-health STATE.json
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

HKT = timezone(timedelta(hours=8))

WORKSPACE = Path(__file__).resolve().parent.parent
SCORE_PATH = WORKSPACE / "memory" / "skill-compliance" / "score.json"
STATE_PATH = WORKSPACE / "memory" / "skill-compliance" / "audit_state.json"
SESSION_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"

# OMLX L3 外部驗證
LOOP_ENGINEERING = Path.home() / "Desktop" / "UltraClaw_Project" / "loop-engineering"
SYSTEM_HEALTH_STATE = LOOP_ENGINEERING / "loops" / "system-health" / "STATE.json"
OMLX_ALERT_PATH = WORKSPACE / "memory" / "omlx_alerts.json"
OMLX_UNHEALTHY_THRESHOLD = 2  # OMLX status ≠ healthy 超過 2 次巡檢 → 觸發告警

# 合規標記
ROUTER_MARKER = "🔀 Router:"
COMPLIANCE_MARKER = "🛡️ Compliance:"

# 分數規則
INITIAL_SCORE = 10.0
MAX_SCORE = 10.0
MIN_SCORE = 0.0
DEDUCTION_PER_VIOLATION = -0.5
REWARD_PER_STREAK = 0.1
STREAK_REQUIRED = 3
DEATH_RESET_SCORE = 5.0


def load_score():
    """載入分數文件"""
    if SCORE_PATH.exists():
        with open(SCORE_PATH, "r") as f:
            return json.load(f)
    return {
        "agent": "main",
        "score": INITIAL_SCORE,
        "maxScore": MAX_SCORE,
        "minScore": MIN_SCORE,
        "deductionPerReject": DEDUCTION_PER_VIOLATION,
        "rewardPerStreak": REWARD_PER_STREAK,
        "streakRequired": STREAK_REQUIRED,
        "history": [],
        "deaths": 0,
        "created": datetime.now(HKT).isoformat(),
        "updated": datetime.now(HKT).isoformat(),
        "streak": 0,  # 連續 PASS 計數
    }


def save_score(data):
    """保存分數文件"""
    SCORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    data["updated"] = datetime.now(HKT).isoformat()
    with open(SCORE_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_audit_state():
    """載入審計狀態（記錄上次檢查到哪裡）"""
    if STATE_PATH.exists():
        with open(STATE_PATH, "r") as f:
            return json.load(f)
    return {"last_checked_session": None, "last_checked_message_index": 0}


def save_audit_state(state):
    """保存審計狀態"""
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def get_latest_session_file():
    """獲取最新的 session JSONL 文件"""
    if not SESSION_DIR.exists():
        return None
    jsonl_files = sorted(SESSION_DIR.glob("*.jsonl"), key=os.path.getmtime, reverse=True)
    return jsonl_files[0] if jsonl_files else None


def extract_assistant_replies(session_path, start_index=0):
    """從 session JSONL 提取 assistant 回覆（含 tool call 信息）"""
    replies = []
    if not session_path or not session_path.exists():
        return replies

    recent_tool_calls = []  # 追蹤最近的 tool call（用於 Gate 2 檢查）

    with open(session_path, "r") as f:
        for i, line in enumerate(f):
            if i < start_index:
                continue
            try:
                msg = json.loads(line.strip())
                msg_type = msg.get("type", "")
                message = msg.get("message", {})

                # 追蹤 tool_use / tool_call (v2 nested format)
                if msg_type == "message" and isinstance(message, dict):
                    role = message.get("role", "")
                    if role == "assistant":
                        content_list = message.get("content", [])
                        if isinstance(content_list, list):
                            for c in content_list:
                                if isinstance(c, dict) and c.get("type") == "tool_use":
                                    tool_name = c.get("name", "")
                                    tool_input = c.get("input", {})
                                    recent_tool_calls.append({
                                        "name": tool_name,
                                        "path": str(tool_input.get("path", "")),
                                        "index": i,
                                    })

                is_assistant = False
                content = ""

                # v1: flat format
                if msg_type == "assistant":
                    is_assistant = True
                    if isinstance(message, str):
                        content = message
                    elif isinstance(message, dict):
                        content = message.get("content", "")
                    elif msg.get("content"):
                        content = str(msg.get("content", ""))

                # v2: nested format
                elif msg_type == "message" and isinstance(message, dict) and message.get("role") == "assistant":
                    is_assistant = True
                    raw_content = message.get("content", "")
                    if isinstance(raw_content, list):
                        text_parts = [c.get("text", "") for c in raw_content if isinstance(c, dict) and c.get("type") == "text"]
                        content = "".join(text_parts)
                    else:
                        content = str(raw_content)

                if is_assistant and content:
                    replies.append({
                        "index": i,
                        "content": content,
                        "tool_calls_before": list(recent_tool_calls),  # snapshot
                    })
            except (json.JSONDecodeError, KeyError):
                continue
    return replies


def check_gate2(reply):
    """
    Gate 2: 檢查是否真的 read 了技能文件
    從 tool_calls_before 中檢查是否有 read tool 調用且路徑含 SKILL.md
    """
    tool_calls = reply.get("tool_calls_before", [])
    # 檢查是否有 read 了任何 SKILL.md 文件
    skills_read = [
        tc for tc in tool_calls
        if tc.get("name") == "read" and "SKILL.md" in tc.get("path", "")
    ]
    return {
        "has_read_skills": len(skills_read) > 0,
        "skills_read": [s["path"] for s in skills_read],
    }


def check_reply(reply_content):
    """檢查單條回覆的合規性（含 Gate 1, 3）"""
    has_router = ROUTER_MARKER in reply_content
    has_compliance = COMPLIANCE_MARKER in reply_content
    return {
        "has_router": has_router,           # Gate 1
        "has_compliance": has_compliance,    # Gate 3
        "passes": has_router and has_compliance,
        "violations": [
            v for v, flag in [
                ("Gate 1: Router line missing", not has_router),
                ("Gate 3: Compliance line missing", not has_compliance),
            ] if flag
        ],
    }


def process_replies(replies, score_data):
    """處理回覆列表，更新分數（含 Gate 1/2/3 完整檢查）"""
    session_streak = 0
    violations_found = []

    for reply in replies:
        result = check_reply(reply["content"])
        gate2 = check_gate2(reply)

        # 合併 Gate 1+2+3 結果
        all_pass = result["passes"] and gate2["has_read_skills"]
        all_violations = list(result["violations"])

        if not gate2["has_read_skills"]:
            all_violations.append("Gate 2: No skill SKILL.md loaded (no read tool call)")

        if all_pass:
            session_streak += 1
            if session_streak >= STREAK_REQUIRED and session_streak % STREAK_REQUIRED == 0:
                old_score = score_data["score"]
                score_data["score"] = min(score_data["score"] + REWARD_PER_STREAK, MAX_SCORE)
                score_data["history"].append({
                    "task": f"Streak reward (reply index {reply['index']})",
                    "result": "PASS",
                    "reason": f"連續 {session_streak} 次 FULL PASS (Gate 1+2+3)，+{REWARD_PER_STREAK}",
                    "deduction": REWARD_PER_STREAK,
                    "time": datetime.now(HKT).isoformat(),
                })
                score_data["streak"] = session_streak
        else:
            session_streak = 0
            score_data["score"] = max(score_data["score"] + DEDUCTION_PER_VIOLATION, MIN_SCORE)
            reason = "; ".join(all_violations)
            score_data["history"].append({
                "task": f"Reply index {reply['index']}",
                "result": "REJECT",
                "reason": reason,
                "deduction": DEDUCTION_PER_VIOLATION,
                "time": datetime.now(HKT).isoformat(),
                "snippet": reply["content"][:200],
                "gate2_skills": gate2.get("skills_read", []),
            })
            violations_found.append({
                "index": reply["index"],
                "reason": reason,
                "snippet": reply["content"][:200],
            })
            score_data["streak"] = 0

        if score_data["score"] <= MIN_SCORE:
            score_data["deaths"] = score_data.get("deaths", 0) + 1
            score_data["score"] = DEATH_RESET_SCORE
            score_data["history"].append({
                "task": "💀 DEATH",
                "result": "DEATH",
                "reason": f"分數歸零，強制 Bootstrap，重置為 {DEATH_RESET_SCORE}",
                "deduction": None,
                "time": datetime.now(HKT).isoformat(),
            })

    return violations_found


def check_omlx_l3():
    """
    OMLX L3 外部驗證規則
    掃描 system-health STATE.json，檢查 OMLX 服務狀態。
    規則：OMLX status ≠ healthy 超過 2 次巡檢，且無 escalation 記錄 → 觸發外部告警。
    此函數獨立運行，LLM agent 無法干預。
    """
    if not SYSTEM_HEALTH_STATE.exists():
        print("⚠️ OMLX L3: system-health STATE.json 不存在，跳過檢查")
        return None

    try:
        with open(SYSTEM_HEALTH_STATE) as f:
            sh_state = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ OMLX L3: 無法讀取 system-health STATE.json: {e}")
        return None

    # 載入 OMLX 告警歷史
    omlx_alerts = {}
    if OMLX_ALERT_PATH.exists():
        try:
            with open(OMLX_ALERT_PATH) as f:
                omlx_alerts = json.load(f)
        except json.JSONDecodeError:
            omlx_alerts = {}

    # 提取 OMLX 檢查歷史
    history = sh_state.get("history", [])
    alerts = sh_state.get("alerts", [])

    # 分析最近的 OMLX 狀態
    recent_omlx_statuses = []
    for entry in history[-10:]:  # 檢查最近 10 次巡檢
        time_str = entry.get("time", "")
        summary = entry.get("summary", "")
        # 從 summary 中提取 OMLX 狀態
        if "OMLX" in summary or "omlx" in summary.lower():
            is_healthy = "healthy" in summary.lower() and "not running" not in summary.lower() and "non-critical" not in summary.lower()
            recent_omlx_statuses.append({
                "time": time_str,
                "healthy": is_healthy,
                "summary": summary,
            })

    # 如果 history 中沒有 OMLX 信息，檢查 checks 字段
    if not recent_omlx_statuses:
        checks = sh_state.get("checks", {})
        omlx_check = checks.get("4_omlx", checks.get("omlx", {}))
        if omlx_check:
            is_healthy = omlx_check.get("status") == "healthy"
            recent_omlx_statuses.append({
                "time": sh_state.get("last_run", ""),
                "healthy": is_healthy,
                "summary": omlx_check.get("details", ""),
            })

    if not recent_omlx_statuses:
        print("ℹ️ OMLX L3: 無 OMLX 數據，跳過檢查")
        return None

    # 計算連續 unhealthy 次數
    consecutive_unhealthy = 0
    for status in reversed(recent_omlx_statuses):
        if not status["healthy"]:
            consecutive_unhealthy += 1
        else:
            break

    # 檢查是否有 escalation 記錄
    has_escalation = any(
        "omlx" in alert.get("message", "").lower() and alert.get("level") in ["critical", "escalated"]
        for alert in alerts
    )

    result = {
        "checked_at": datetime.now(HKT).isoformat(),
        "omlx_consecutive_unhealthy": consecutive_unhealthy,
        "threshold": OMLX_UNHEALTHY_THRESHOLD,
        "has_escalation": has_escalation,
        "alert_triggered": False,
        "action": "none",
    }

    if consecutive_unhealthy > OMLX_UNHEALTHY_THRESHOLD and not has_escalation:
        result["alert_triggered"] = True
        result["action"] = "external_alert"
        result["message"] = (
            f"🔴 OMLX L3 ALERT: OMLX 服務連續 {consecutive_unhealthy} 次巡檢狀態非 healthy，"
            f"且無 escalation 記錄。超過閾值 {OMLX_UNHEALTHY_THRESHOLD} 次。\n"
            f"觸發外部告警 — OMLX 是關鍵生產服務，不可忽略。\n"
            f"最後檢查時間：{recent_omlx_statuses[-1].get('time', 'unknown')}"
        )

        # 記錄告警歷史
        omlx_alerts[datetime.now(HKT).strftime("%Y-%m-%dT%H:%M:%S")] = result
        OMLX_ALERT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(OMLX_ALERT_PATH, "w") as f:
            json.dump(omlx_alerts, f, indent=2, ensure_ascii=False)

        print(result["message"])
    else:
        status_msg = f"OMLX L3: 連續 {consecutive_unhealthy} 次 unhealthy（閾值 {OMLX_UNHEALTHY_THRESHOLD}）"
        if has_escalation:
            status_msg += " — 已有 escalation 記錄，不重複告警"
        else:
            status_msg += " — 未達告警閾值"
        print(f"✅ {status_msg}")

    return result


def main():
    mode = "scan"
    if "--omlx-check" in sys.argv:
        result = check_omlx_l3()
        if result and result.get("alert_triggered"):
            sys.exit(1)  # 非零退出碼表示有告警
        return
    if "--cron" in sys.argv:
        mode = "cron"
    elif "--reset" in sys.argv:
        mode = "reset"
    elif "--status" in sys.argv:
        mode = "status"

    if mode == "status":
        score_data = load_score()
        print(f"📊 當前分數：{score_data['score']}/{score_data['maxScore']}")
        print(f"💀 死亡次數：{score_data.get('deaths', 0)}")
        print(f"📋 歷史記錄：{len(score_data.get('history', []))} 條")
        return

    if mode == "reset":
        score_data = load_score()
        score_data["score"] = INITIAL_SCORE
        score_data["history"] = []
        score_data["deaths"] = 0
        score_data["streak"] = 0
        save_score(score_data)
        print(f"🔄 分數已重置為 {INITIAL_SCORE}/{MAX_SCORE}")
        return

    # scan / cron mode
    session_path = get_latest_session_file()
    if not session_path:
        print("⚠️ 找不到 session 文件")
        return

    audit_state = load_audit_state()
    start_index = 0

    if mode == "cron":
        # cron 模式：從上次檢查位置繼續
        if audit_state.get("last_checked_session") == str(session_path):
            start_index = audit_state.get("last_checked_message_index", 0)

    # 提取 assistant 回覆
    replies = extract_assistant_replies(session_path, start_index)

    if not replies:
        print("ℹ️ 沒有新的 assistant 回覆需要檢查")
        return

    # 載入分數並處理
    score_data = load_score()
    violations = process_replies(replies, score_data)
    save_score(score_data)

    # 更新審計狀態
    last_index = max(r["index"] for r in replies) + 1
    audit_state["last_checked_session"] = str(session_path)
    audit_state["last_checked_message_index"] = last_index
    save_audit_state(audit_state)

    # 輸出結果
    total = len(replies)
    passed = total - len(violations)
    print(f"📊 審計完成：檢查 {total} 條回覆，{passed} PASS，{len(violations)} REJECT")
    print(f"📊 當前分數：{score_data['score']}/{score_data['maxScore']} | 💀 死亡：{score_data.get('deaths', 0)}")

    if violations:
        print(f"\n🔴 違規詳情：")
        for v in violations:
            print(f"  Reply #{v['index']}: {v['reason']}")
            print(f"    Content: {v['snippet'][:150]}...")

    if score_data["score"] <= MIN_SCORE:
        print(f"\n💀💀💀 DEATH #{score_data.get('deaths', 0)} 觸發！需要 Bootstrap 重置 💀💀💀")


if __name__ == "__main__":
    main()
