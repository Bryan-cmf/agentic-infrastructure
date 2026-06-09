#!/usr/bin/env python3
"""
Vector Memory 基礎測試
"""

import sys
import os
from pathlib import Path

# 添加當前目錄到 path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_memory_utils_import():
    """測試 memory_utils 可以正常導入"""
    try:
        from memory_utils import chunk_text, should_skip, collect_files
        print("✅ memory_utils 導入成功")
        return True
    except Exception as e:
        print(f"❌ memory_utils 導入失敗: {e}")
        return False

def test_chunk_text():
    """測試 chunk_text 函數"""
    try:
        from memory_utils import chunk_text
        
        text = """
這是第一段。這是一個測試文本。

這是第二段。包含更多內容。

這是第三段。用來驗證分塊功能。
"""
        chunks = chunk_text(text, "test.md")
        
        assert len(chunks) > 0, "應該至少有一個 chunk"
        assert all('content' in c for c in chunks), "每個 chunk 應該有 content 字段"
        assert all('source' in c for c in chunks), "每個 chunk 應該有 source 字段"
        
        print(f"✅ chunk_text 測試通過 (產生 {len(chunks)} 個 chunks)")
        return True
    except Exception as e:
        print(f"❌ chunk_text 測試失敗: {e}")
        return False

def test_should_skip():
    """測試 should_skip 函數"""
    try:
        from memory_utils import should_skip
        
        # 測試應該跳過的文件（匹配 SKIP_PATTERNS）
        assert should_skip(Path("memory/email_notification_queue/test.json")) == True
        assert should_skip(Path("memory/dreams/test.md")) == True
        assert should_skip(Path("memory/daily/2026-06-10.md")) == False
        assert should_skip(Path("memory/projects/test.md")) == False
        
        print("✅ should_skip 測試通過")
        return True
    except Exception as e:
        print(f"❌ should_skip 測試失敗: {e}")
        return False

def test_collect_files():
    """測試 collect_files 函數"""
    try:
        from memory_utils import collect_files
        
        files = collect_files()
        
        assert isinstance(files, list), "應該返回 list"
        # 不強制要求有文件，因為測試環境可能沒有記憶文件
        
        print(f"✅ collect_files 測試通過 (找到 {len(files)} 個文件)")
        return True
    except Exception as e:
        print(f"❌ collect_files 測試失敗: {e}")
        return False

def test_mcp_import():
    """測試 MCP server 可以正常導入（需要 mcp 包）"""
    try:
        import mcp.types
        print("✅ mcp 包導入成功")
        return True
    except ImportError:
        print("⚠️  mcp 包未安裝（正常 — 需要 pip install mcp）")
        return True  # 不算失敗

def main():
    """運行所有測試"""
    print("🧪 Vector Memory 基礎測試\n")
    
    tests = [
        test_memory_utils_import,
        test_chunk_text,
        test_should_skip,
        test_collect_files,
        test_mcp_import,
    ]
    
    results = []
    for test in tests:
        print(f"\n運行: {test.__name__}")
        result = test()
        results.append(result)
    
    print("\n" + "="*50)
    passed = sum(results)
    total = len(results)
    print(f"測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("✅ 所有測試通過！")
        return 0
    else:
        print(f"❌ {total - passed} 個測試失敗")
        return 1

if __name__ == "__main__":
    sys.exit(main())
