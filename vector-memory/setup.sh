#!/bin/bash
# Vector Memory — 一鍵部署腳本
# Usage: bash setup.sh

set -e

echo "🧠 Vector Memory — 一鍵部署"
echo "============================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

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
if docker compose ps | grep -q "qdrant"; then
    echo -e "   ${YELLOW}⚠️ Qdrant 已在運行，跳過${NC}"
else
    docker compose up -d
    echo -e "   ${GREEN}✅ Qdrant 已啟動 (port 6333)${NC}"
fi

# Wait for Qdrant to be ready
echo "   等待 Qdrant 就緒..."
for i in {1..10}; do
    if curl -s http://localhost:6333/ > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ Qdrant 健康檢查通過${NC}"
        break
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

# 4. Install Python dependencies
echo ""
echo "4️⃣ 安裝 Python 依賴..."
pip3 install sentence-transformers qdrant-client 2>&1 | tail -1
echo -e "   ${GREEN}✅ 依賴安裝完成${NC}"

# 5. Create storage directory
echo ""
echo "5️⃣ 初始化存儲目錄..."
mkdir -p qdrant_storage
echo -e "   ${GREEN}✅ qdrant_storage/ 已創建${NC}"

# 6. Test embedding model
echo ""
echo "6️⃣ 測試嵌入模型 (BGE-m3)..."
python3 -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('BAAI/bge-m3')
vec = model.encode('測試')
print(f'   向量維度: {len(vec)}')
print(f'   模型就緒: ✅')
" 2>&1

# 7. Done
echo ""
echo "============================"
echo -e "${GREEN}✅ Vector Memory 部署完成！${NC}"
echo ""
echo "📋 下一步："
echo "   1. 啟動記憶服務:  python3 mcp_server.py"
echo "   2. 配置 OpenClaw Gateway 加入 vector-memory MCP"
echo "   3. 開始使用:  mem_search('你的問題')"
echo ""
echo "📖 完整文檔:  SKILL.md"
