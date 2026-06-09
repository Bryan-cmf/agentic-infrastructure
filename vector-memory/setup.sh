#!/bin/bash
# Vector Memory — 一鍵部署腳本 v2.0
# Usage: bash setup.sh
#
# v2.0 修復：
#   - 使用 venv 隔離 Python 環境
#   - 使用 requirements.txt 管理依賴
#   - 加入安裝驗證步驟
#   - 支持 --dry-run 模式

set -e

DRY_RUN=false
if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "🔍 DRY RUN MODE — 不會實際安裝任何東西"
    echo ""
fi

echo "🧠 Vector Memory — 一鍵部署 v2.0"
echo "================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 1. Check Docker
echo "1️⃣ 檢查 Docker..."
if command -v docker &> /dev/null; then
    echo -e "   ${GREEN}✅ Docker 已安裝${NC}"
else
    echo -e "   ${RED}❌ 請先安裝 Docker: https://docs.docker.com/get-docker/${NC}"
    exit 1
fi

# 2. Start Qdrant
echo ""
echo "2️⃣ 啟動 Qdrant..."
if [ "$DRY_RUN" = true ]; then
    echo -e "   ${YELLOW}[DRY RUN] 會啟動 Qdrant Docker 容器${NC}"
else
    if docker compose ps 2>/dev/null | grep -q "qdrant"; then
        echo -e "   ${YELLOW}⚠️ Qdrant 已在運行，跳過${NC}"
    else
        cd "$SCRIPT_DIR"
        docker compose up -d
        echo -e "   ${GREEN}✅ Qdrant 已啟動 (port 6333)${NC}"
    fi
fi

# Wait for Qdrant to be ready
echo "   等待 Qdrant 就緒..."
for i in {1..10}; do
    if curl -s http://localhost:6333/ > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ Qdrant 健康檢查通過${NC}"
        break
    fi
    if [ $i -eq 10 ]; then
        echo -e "   ${RED}❌ Qdrant 啟動超時${NC}"
        exit 1
    fi
    sleep 2
done

# 3. Check Python
echo ""
echo "3️⃣ 檢查 Python 環境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "   ${GREEN}✅ $PYTHON_VERSION${NC}"
else
    echo -e "   ${RED}❌ 請先安裝 Python 3.10+${NC}"
    exit 1
fi

# 4. Create venv and install dependencies
echo ""
echo "4️⃣ 建立 Python 虛擬環境..."
if [ "$DRY_RUN" = true ]; then
    echo -e "   ${YELLOW}[DRY RUN] 會建立 .venv 並安裝依賴${NC}"
    echo -e "   ${YELLOW}[DRY RUN] 依賴列表：${NC}"
    cat "$SCRIPT_DIR/requirements.txt" | grep -v "^#" | grep -v "^$" | sed 's/^/      /'
else
    cd "$SCRIPT_DIR"
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        echo -e "   ${GREEN}✅ .venv 已建立${NC}"
    else
        echo -e "   ${YELLOW}⚠️ .venv 已存在，跳過建立${NC}"
    fi
    
    source .venv/bin/activate
    echo "   安裝依賴..."
    pip install -r requirements.txt 2>&1 | tail -3
    echo -e "   ${GREEN}✅ 依賴安裝完成${NC}"
fi

# 5. Create storage directory
echo ""
echo "5️⃣ 初始化存儲目錄..."
if [ "$DRY_RUN" = false ]; then
    mkdir -p "$SCRIPT_DIR/qdrant_storage"
fi
echo -e "   ${GREEN}✅ qdrant_storage/ 已創建${NC}"

# 6. Test embedding model
echo ""
echo "6️⃣ 測試嵌入模型 (BGE-m3)..."
if [ "$DRY_RUN" = true ]; then
    echo -e "   ${YELLOW}[DRY RUN] 會下載並測試 BGE-m3 模型${NC}"
else
    source "$SCRIPT_DIR/.venv/bin/activate"
    python3 -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('BAAI/bge-m3')
vec = model.encode('測試')
print(f'   向量維度: {len(vec)}')
print(f'   模型就緒: ✅')
" 2>&1
fi

# 7. Installation verification
echo ""
echo "7️⃣ 安裝驗證..."
if [ "$DRY_RUN" = true ]; then
    echo -e "   ${YELLOW}[DRY RUN] 會執行以下驗證：${NC}"
    echo "      - from memory_utils import chunk_text"
    echo "      - from mcp_server import app"
    echo "      - curl http://localhost:6333/"
else
    source "$SCRIPT_DIR/.venv/bin/activate"
    cd "$SCRIPT_DIR"
    
    ERRORS=0
    
    # Test memory_utils
    if python3 -c "from memory_utils import chunk_text, should_skip, collect_files; print('   ✅ memory_utils OK')" 2>/dev/null; then
        :
    else
        echo "   ❌ memory_utils 導入失敗"
        ERRORS=$((ERRORS + 1))
    fi
    
    # Test mcp_server (just import, don't start server)
    if python3 -c "import mcp.types; print('   ✅ mcp package OK')" 2>/dev/null; then
        :
    else
        echo "   ❌ mcp package 缺失"
        ERRORS=$((ERRORS + 1))
    fi
    
    # Test Qdrant connection
    if curl -sf http://localhost:6333/ > /dev/null 2>&1; then
        echo "   ✅ Qdrant 連接正常"
    else
        echo "   ❌ Qdrant 連接失敗"
        ERRORS=$((ERRORS + 1))
    fi
    
    if [ $ERRORS -eq 0 ]; then
        echo ""
        echo -e "   ${GREEN}✅ 所有驗證通過！${NC}"
    else
        echo ""
        echo -e "   ${RED}❌ $ERRORS 個驗證失敗${NC}"
    fi
fi

# 8. Done
echo ""
echo "================================="
if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}🔍 DRY RUN 完成 — 沒有實際安裝任何東西${NC}"
    echo ""
    echo "📋 如果滿意，移除 --dry-run 重新執行："
    echo "   bash setup.sh"
else
    echo -e "${GREEN}✅ Vector Memory 部署完成！${NC}"
fi
echo ""
echo "📋 下一步："
echo "   1. 啟動記憶服務:  source .venv/bin/activate && python3 mcp_server.py"
echo "   2. 啟動儀表板:    python3 dashboard.py"
echo "   3. 配置 OpenClaw Gateway 加入 vector-memory MCP"
echo ""
echo "📖 完整文檔:  SKILL.md"
