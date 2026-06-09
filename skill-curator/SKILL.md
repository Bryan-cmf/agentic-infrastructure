---
name: skill-curator
description: 技能策展 技能管理 技能調適 技能掃描 技能診斷 技能維護 關鍵詞注入 多語言技能 Skill curator — full lifecycle skill management: scan, diagnose, adapt, test, and report.
---

# 🎨 Skill Curator — 技能全生命週期策展人

## 📥 一行安裝

```bash
mkdir -p skills/skill-curator && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-curator/SKILL.md -o skills/skill-curator/SKILL.md
```

## 🌏 完整說明（選擇你的語言）

### 🇹🇼 繁體中文

**痛點：** 用戶大量下載技能但從不調適——缺中文關鍵詞無法觸發、格式損壞無法使用、功能重疊互相干擾、從未測試不知好壞。就像一個圖書館買了幾百本書但從不整理、不編目、不檢查——書雖多，一本也找不到。我們對 125 個技能的首次掃描發現：6 個致命（無 description）、55 個警告（缺中文關鍵詞）、只有 51% 健康。

**方案：** 六階段全生命週期管理。(1) 全量掃描：提取所有技能的 description 語言覆蓋、frontmatter 完整性、觸發詞覆蓋率。(2) 三層診斷：🔴致命（無法觸發）🟡警告（缺多語言）🟢建議（可合併/卸載）。(3) 自動調適：注入中文+六語言關鍵詞、修復格式損壞。(4) 場景生成：為每個技能生成「你應該這樣用我」的提示詞。(5) 匯報：飛書推送策展報告。(6) 執行：卸載/合併等用戶審批。

**效果：** 首次策展將 125 技能從 51% 健康提升至 99.2% 健康。6 致命→1（幽靈），55 警告→0，64 健康→124。自動注入 61 個技能的中文關鍵詞。

**一行安裝：** `mkdir -p skills/skill-curator && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-curator/SKILL.md -o skills/skill-curator/SKILL.md`

### 🇯🇵 日本語

**痛点：** ユーザーが多数のスキルをダウンロードするが、調整しない——中国語キーワード不足でトリガー不可、フォーマット破損、機能重複。125 スキルの初回スキャンで 6 致命的、55 警告、51% のみ健全。

**方案：** 6 フェーズ管理。(1) 全量スキャン (2) 3 層診断 (3) 自動適応（多言語キーワード注入）(4) シナリオ生成 (5) レポート (6) 実行（承認後）。

**効果：** 125 スキルが 51%→99.2% 健全に。6 致命的→1、55 警告→0。

**一行インストール：** `mkdir -p skills/skill-curator && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-curator/SKILL.md -o skills/skill-curator/SKILL.md`

### 🇰🇷 한국어

**痛点：** 사용자가 많은 스킬을 다운로드하지만 조정하지 않음——중국어 키워드 부족, 포맷 손상, 기능 중복. 125개 스킬 초기 스캔 결과 6개 치명적, 55개 경고, 51%만 정상.

**方案：** 6단계 관리. (1) 전량 스캔 (2) 3계층 진단 (3) 자동 적응(다국어 키워드 주입) (4) 시나리오 생성 (5) 보고 (6) 실행.

**効果：** 125개 스킬 51%→99.2% 정상. 6 치명적→1, 55 경고→0.

**한 줄 설치：** `mkdir -p skills/skill-curator && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-curator/SKILL.md -o skills/skill-curator/SKILL.md`

### 🇸🇦 العربية

**المشكلة：** تحميل مهارات كثيرة بدون تكييف——نقص الكلمات المفتاحية الصينية، تنسيق تالف، تداخل وظيفي. مسح 125 مهارة: 6 حرجة، 55 تحذير، 51% سليمة فقط.

**الحل：** إدارة من 6 مراحل: مسح ← تشخيص ← تكييف ← سيناريوهات ← تقرير ← تنفيذ.

**التأثير：** 125 مهارة من 51%→99.2% سليمة. 6 حرجة→1، 55 تحذير→0.

**تثبيت بسطر：** `mkdir -p skills/skill-curator && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-curator/SKILL.md -o skills/skill-curator/SKILL.md`

### 🇮🇳 हिन्दी

**समस्या：** बहुत सारी स्किल्स डाउनलोड लेकिन अनुकूलित नहीं——चीनी कीवर्ड की कमी, फॉर्मेट क्षति। 125 स्किल्स का स्कैन: 6 क्रिटिकल, 55 चेतावनी, केवल 51% स्वस्थ।

**समाधान：** 6-चरण प्रबंधन: स्कैन → निदान → अनुकूलन → परिदृश्य → रिपोर्ट → निष्पादन।

**प्रभाव：** 125 स्किल्स 51%→99.2% स्वस्थ। 6 क्रिटिकल→1, 55 चेतावनी→0।

**एक लाइन इंस्टॉल：** `mkdir -p skills/skill-curator && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-curator/SKILL.md -o skills/skill-curator/SKILL.md`

---

## 解決的三大痛點

| 痛點 | 症狀 | 方案 |
|------|------|------|
| 技能未調適 | 缺關鍵詞、無法觸發、格式損壞 | 自動注入關鍵詞 + 修復格式 |
| 技能過多 | Token 消耗大、互相干擾 | 健康掃描 + 去重合併 + 卸載建議 |
| 技能未測試 | 不知好壞、不知何時用 | 場景生成 + 觸發驗證 |

## 六階段流程

1. **掃描** — 全量技能健康盤點（語言覆蓋/格式/觸發詞）
2. **診斷** — 🔴致命 🟡警告 🟢建議 三層分類
3. **調適** — 自動注入關鍵詞 + 修復格式（備份原文件）
4. **場景生成** — 每技能生成 3-5 個「你應該這樣用我」
5. **匯報** — 飛書推送策展報告
6. **執行** — 卸載/合併等用戶審批

## 功能矩陣（包括但不限於）

| 功能 | 自動/確認 |
|------|---------|
| 🔍 全量掃描 | 自動 |
| 🩺 格式診斷 | 自動 |
| 🌏 關鍵詞注入（六語言） | 自動 |
| 🧹 去重合併 | 建議→確認 |
| 🗑️ 卸載建議 | 建議→確認 |
| 🧪 場景生成 | 自動 |
| 🚫 路由管理 | 建議→確認 |

## 檔案結構

```
skills/skill-curator/
├── SKILL.md
└── scripts/scan_all.py
```

## 授權 · License

MIT
