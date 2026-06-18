---
name: skill-compliance
description: "技能合規檢查 駁回機制 技能審計 合規審查 智能體守門 扣分系統 技能分數 Compliance checker — inline behavior: compare required vs actual skills, output PASS/REJECT. Penalty system: -0.5 per REJECT, score 0 = DEATH."
---

# 🛡️ Skill Compliance Checker — 技能合規檢查器（含扣分系統）

## 概念

> **合規檢查是一個「行為」，不是一個「文件讀取」。帶著真正的代價。**

## 🩸 扣分系統

```
初始: 10.0 / 10
每次 REJECT: -0.5 分
連續 3 次 PASS: +0.1 分
分數歸零 → 💀 DEATH: 強制 Bootstrap，重置 5.0
```

**分數存儲：** `memory/skill-compliance/score.json`（持久化，不受上下文窗口限制）

## 📊 顯示格式

```
🛡️ Compliance: ✅ PASS | 📊 10.0/10
🛡️ Compliance: 🔴 REJECT | 🩸 9.5/10 [理由]
🛡️ Compliance: 💀 DEATH #1 | 強制 Bootstrap
```

## 什麼叫「調用 skill-compliance」

執行內聯檢查行為（比對 required vs actual + 輸出 PASS/REJECT + 顯示分數）即視為已調用。

## 與扣分系統的整合

```
skill-router → 專項強制清單
     │
     ▼
Agent 執行
     │
     ▼
skill-compliance 內聯檢查
     ├── PASS → 檢查 streak
     │         └── 連續3次 → +0.1 分
     └── REJECT → -0.5 分
              → 分數 ≤ 0 → 💀 DEATH → Bootstrap
```

## 📥 安裝

```bash
mkdir -p skills/skill-compliance && curl -sSL https://raw.githubusercontent.com/Bryan-cmf/agentic-infrastructure/main/skill-compliance/SKILL.md -o skills/skill-compliance/SKILL.md
```
