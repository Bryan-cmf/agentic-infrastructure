# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Agent Previsor skill — pre-mortem analysis for complex tasks
- Scoring rubric for task evaluation (accumulation/reusability/demonstrability)
- Using Agent Skills guide with skill discovery flowchart

### Fixed
- Vector Memory setup.sh now uses venv and requirements.txt
- MCP Server device detection (mps/cuda/cpu auto-detect)
- Docker Compose pins Qdrant version to v1.13.2

## [1.0.0] - 2026-06-10

### Added
- **Skills Triggering** — Multi-language keyword injection for skill discovery
- **Skill Router** — Class × phase matrix for task-to-skill matching
- **Skill Reporting** — Automatic skill usage transparency
- **Vector Memory** — Qdrant + BGE-m3 persistent memory system
  - auto_sync.py — incremental file → vector sync
  - mcp_server.py — MCP protocol server with 13 tools
  - guard.sh — health monitoring with auto-restart
  - setup.sh — one-click deployment
- **Skill Curator** — skill lifecycle management
- **Agent Evolver** — monthly core file self-reflection

### Documentation
- README.md with 6-language support (zh-TW/zh-CN/en/ja/ko/ar/hi)
- USAGE-GUIDE.md with 7-phase onboarding flow
- methodology/ — batch fix skills script and case study

[Unreleased]: https://github.com/Bryan-cmf/openclaw-agent-toolkit/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Bryan-cmf/openclaw-agent-toolkit/releases/tag/v1.0.0
