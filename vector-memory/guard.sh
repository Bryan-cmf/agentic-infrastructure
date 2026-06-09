#!/bin/bash
# Vector Memory 存活守護腳本 v2.0
# ==================================
# 確保 Qdrant 響應 + MCP Server 進程存在
# 由 crontab 每 60 秒呼叫一次
#
# v2.0 新增：
#   - 自動重啟 MCP Server
#   - 重啟頻率限制（最多 3 次/小時）
#   - 更好的日誌格式

LOG="/tmp/vector_memory_guard.log"
MAX_LOG_LINES=500
STATE_FILE="/tmp/vector_memory_guard_state"
RESTART_COUNT_FILE="/tmp/vector_memory_guard_restarts"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"
MCP_SERVER="$SCRIPT_DIR/mcp_server.py"

# Max restarts per hour
MAX_RESTARTS_PER_HOUR=3

STATUS="OK"
DETAILS=""

# ── Check Qdrant ──
if curl -sf http://localhost:6333/ > /dev/null 2>&1; then
    QDRANT_STATUS="UP"
else
    QDRANT_STATUS="DOWN"
    STATUS="QDRANT_DOWN"
    DETAILS="Qdrant not responding on :6333"
fi

# ── Check MCP Server process ──
MCP_PID=$(pgrep -f "mcp_server.py" | head -1)
if [ -n "$MCP_PID" ]; then
    MCP_STATUS="UP (PID: $MCP_PID)"
else
    MCP_STATUS="DOWN"
    if [ "$STATUS" = "OK" ]; then
        STATUS="MCP_DOWN"
    else
        STATUS="BOTH_DOWN"
    fi
fi

# ── Auto-restart MCP if down ──
if [ "$MCP_STATUS" = "DOWN" ]; then
    # Check restart rate limit
    NOW=$(date +%s)
    HOUR_AGO=$((NOW - 3600))
    
    # Clean old restart records
    if [ -f "$RESTART_COUNT_FILE" ]; then
        # Keep only timestamps from last hour
        TEMP_FILE=$(mktemp)
        while read -r ts; do
            if [ "$ts" -gt "$HOUR_AGO" ] 2>/dev/null; then
                echo "$ts" >> "$TEMP_FILE"
            fi
        done < "$RESTART_COUNT_FILE"
        mv "$TEMP_FILE" "$RESTART_COUNT_FILE"
    fi
    
    RESTART_COUNT=$(wc -l < "$RESTART_COUNT_FILE" 2>/dev/null || echo 0)
    
    if [ "$RESTART_COUNT" -lt "$MAX_RESTARTS_PER_HOUR" ]; then
        # Attempt restart
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🔄 Auto-restarting MCP Server..." >> "$LOG"
        
        # Kill any zombie processes
        pkill -9 -f "mcp_server.py" 2>/dev/null
        sleep 1
        
        # Start MCP server in background
        nohup "$VENV_PYTHON" "$MCP_SERVER" > /tmp/mcp_server_stdout.log 2>&1 &
        NEW_PID=$!
        
        # Verify it started
        sleep 2
        if pgrep -f "mcp_server.py" > /dev/null 2>&1; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ MCP Server restarted (PID: $NEW_PID)" >> "$LOG"
            STATUS="${STATUS}_RECOVERED"
        else
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ MCP Server restart failed" >> "$LOG"
        fi
        
        # Record restart timestamp
        echo "$NOW" >> "$RESTART_COUNT_FILE"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  MCP down but restart limit reached ($RESTART_COUNT/$MAX_RESTARTS_PER_HOUR)" >> "$LOG"
        STATUS="${STATUS}_RATE_LIMITED"
    fi
fi

# ── Log only on status change ──
PREV_STATUS=$(cat "$STATE_FILE" 2>/dev/null || echo "UNKNOWN")

if [ "$STATUS" != "$PREV_STATUS" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $STATUS (was: $PREV_STATUS) | Qdrant: $QDRANT_STATUS | MCP: $MCP_STATUS" >> "$LOG"
    echo "$STATUS" > "$STATE_FILE"
fi

# ── Log rotation ──
if [ -f "$LOG" ]; then
    LINE_COUNT=$(wc -l < "$LOG" 2>/dev/null || echo 0)
    if [ "$LINE_COUNT" -gt "$MAX_LOG_LINES" ]; then
        tail -200 "$LOG" > "${LOG}.tmp" && mv "${LOG}.tmp" "$LOG"
    fi
fi
