# Contributing to Agentic Infrastructure

感謝你考慮貢獻！這個項目旨在解決 AI Agent 生態系統的結構性問題。

## 🎯 貢獻方向

### 1. 技能改進
- 改進現有技能的 SKILL.md
- 添加更多語言支持
- 優化技能觸發關鍵詞

### 2. 代碼貢獻
- 修復 bug（見 Issues）
- 添加測試
- 改進文檔

### 3. 新技能
- 如果你解決了一個新的結構性問題，歡迎提交新技能

## 📝 提交規範

### Commit Message 格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Type:**
- `feat`: 新功能
- `fix`: 修復 bug
- `docs`: 文檔更新
- `style`: 代碼格式（不影響邏輯）
- `refactor`: 重構
- `test`: 添加測試
- `chore`: 構建/工具鏈

**Scope:**
- `skills-triggering`
- `skill-router`
- `skill-reporting`
- `vector-memory`
- `skill-curator`
- `agent-evolver`
- `agent-previsor`

**示例:**
```
feat(vector-memory): 添加記憶衰減系統

- 實現 decay.py 模塊
- 支持自定義衰減曲線
- 添加單元測試

Closes #42
```

## 🧪 測試

提交前請確保：
```bash
# 1. 安裝依賴
cd vector-memory
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. 運行測試
python3 -m pytest tests/

# 3. 驗證安裝腳本
bash setup.sh --dry-run
```

## 📖 文檔

- 更新 README.md（如果涉及功能變更）
- 更新 CHANGELOG.md（遵循 Keep a Changelog 格式）
- 更新 USAGE-GUIDE.md（如果涉及使用流程）

## 🔍 代碼審查

所有提交都需要通過代碼審查。審查重點：
- 代碼質量
- 測試覆蓋
- 文檔完整性
- 向後兼容性

## 💬 溝通

- 開 Issue 討論新功能
- 在 PR 中詳細說明變更
- 及時回應審查意見

## 📄 許可

貢獻的代碼將遵循 MIT 許可證。

---

感謝你的貢獻！🙏
