---
title: Obsidian 社区插件官方元数据
category: references
tags: [obsidian, plugins, github, maintenance, compatibility]
sources:
  - https://github.com/obsidianmd/obsidian-releases/blob/master/community-plugins.json
  - https://github.com/obsidianmd/obsidian-releases/blob/master/community-plugin-stats.json
summary: 依据 Obsidian 官方注册表、插件 manifest 与 GitHub 仓库核实的候选插件版本、兼容性和维护状态。
provenance: {extracted: 0.96, inferred: 0.04, ambiguous: 0.0}
base_confidence: 0.91
lifecycle: draft
lifecycle_changed: 2026-07-15
tier: supporting
created: 2026-07-15T21:52:04+08:00
updated: 2026-07-16T00:07:55+08:00
---

# Obsidian 社区插件官方元数据

以下数据于 2026-07-15 从 Obsidian 官方插件注册表、插件 GitHub 仓库和根目录 `manifest.json` 核实。下载量只表示采用范围，不代表适合本 vault。

| 插件 | 版本 | 最低 Obsidian | 最近发布/推送 | 下载量约 | 关键机械风险 |
|---|---:|---:|---|---:|---|
| Excalidraw | 2.25.3 | 1.8.7 | 2026-07 | 668 万 | 单人维护、功能面大；高级 AI/OCR 或外部资源功能可能联网。 |
| Advanced Canvas | 6.5.0 | 1.7.2 | 2026-07 | 66 万 | 扩展 JSON Canvas 格式；与核心 Canvas 有较大重叠。 |
| Mermaid Tools | 1.4.1 | 1.4.0 | 2026-05 | 31 万 | 主要改善编辑体验；渲染本身已是原生能力。 |
| PDF++ | 0.40.31 | 1.5.8 | 2025-08 | 61 万 | 依赖多项 Obsidian 私有 API，应用更新后存在破坏风险。 |
| Zotero Integration | 3.2.1 | 1.1.1 | release 2024-08；repo 2026-03 有推送 | 52 万 | 桌面端；依赖 Zotero 与 Better BibTeX；文档承认仍不完整。 |
| Spaced Repetition | 1.15.4 | 1.2.8 | 2026-06 | 56 万 | 会把复习语法和调度元数据带入笔记，需要先确定学习法。 |
| Dataview | 0.5.70 | 0.13.11 | release 2025-04 | 456 万 | 维护趋缓、查询为插件依赖语法；复杂查询仍比 Bases 强。 |
| Templater | 2.23.1 | **1.13.0** | 2026-07 | 489 万 | 当前 Obsidian 1.12.7 仍无法使用该调研版本。 |
| QuickAdd | 2.19.1 | **1.13.0** | 2026-07 | 193 万 | 当前 Obsidian 1.12.7 仍无法使用该调研版本；Codex 主导时重叠较大。 |
| Omnisearch | 1.29.3 | 1.7.2 | 2026-05 | 161 万 | Office/PDF/图片索引会增加索引成本；外部 HTTP server 是可选项。 |
| Smart Connections | 4.5.3 | 1.1.0 | 2026-06 | 109 万 | 默认本地 embedding，但与 wiki-query/索引能力重叠；大型 vault 有索引成本。 |
| Copilot | 3.3.3 | **1.11.4** | 2026-05 | 155 万 | 默认工作流常需模型供应商/API；Copilot Plus 明确需要网络；与 Codex 高度重叠。 |
| Text Generator | 0.8.7 | 1.6.0 | 2026-04 | 56 万 | 面向 OpenAI/Gemini/HuggingFace 等外部模型服务；与 Codex 重叠。 |

## 可迁移性事实

- PDF++ 将侧注保存在普通 Markdown，并尽量只增加可选的 PDF link parameters；停用插件后文本仍可读。
- Excalidraw 默认本地离线，但场景文件不是纯正文 Markdown；要保留 SVG/PNG 导出和源文件。
- Advanced Canvas 宣称兼容 JSON Canvas，但扩展特性会写入 Advanced JSON Canvas 元数据。
- Dataview、Templater、QuickAdd 的价值来自可执行查询或脚本；迁出时需要把动态结果编译回静态 Markdown。^[inferred]

## Sources

- [Official community plugin registry](https://github.com/obsidianmd/obsidian-releases/blob/master/community-plugins.json)
- [Official plugin statistics](https://github.com/obsidianmd/obsidian-releases/blob/master/community-plugin-stats.json)
- [Excalidraw repository](https://github.com/zsviczian/obsidian-excalidraw-plugin)
- [PDF++ repository](https://github.com/RyotaUshio/obsidian-pdf-plus)
- [Omnisearch repository](https://github.com/scambier/obsidian-omnisearch)
- [Smart Connections repository](https://github.com/brianpetro/obsidian-smart-connections)
- [Copilot repository](https://github.com/logancyang/obsidian-copilot)
