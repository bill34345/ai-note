---
title: Obsidian 核心功能与版本基线
category: references
tags: [obsidian, core-plugins, baseline, version]
aliases: [Obsidian baseline]
sources:
  - https://obsidian.md/help/bases
  - https://obsidian.md/help/plugins/canvas
  - https://obsidian.md/help/web-clipper
  - https://help.obsidian.md/linking+notes+and+files/embedding+files
  - https://obsidian.md/changelog/
summary: 当前 AI-wiki 的 Obsidian 版本、已启用核心能力及其足以覆盖的学习工作流基线。
provenance: {extracted: 0.92, inferred: 0.08, ambiguous: 0.0}
base_confidence: 0.93
lifecycle: draft
lifecycle_changed: 2026-07-16
tier: supporting
created: 2026-07-15T21:52:04+08:00
updated: 2026-07-16T00:31:15+08:00
---

# Obsidian 核心功能与版本基线

## 本机状态

- 当前运行的 Obsidian：**1.12.7**，路径 `H:\Obsidian\Obsidian.exe`；版本已从运行中程序的文件元数据核实。
- 初始调研在 2026-07-15 核实到公共版 **1.12.4**；随后本机已更新到 1.12.7，因此 1.12.4 只保留为历史调研快照。
- 当前 vault 已安装并启用一个社区插件：Excalidraw 2.25.3；另已启用浏览器扩展 Web Clipper 1.7.0。
- 已启用：File Explorer、Search、Graph、Backlinks、Canvas、Outgoing Links、Properties、Templates、Daily Notes、Bookmarks、File Recovery、Sync、Bases 等。
- 未启用但属于核心能力：Web Viewer、Workspaces、Slides、Audio Recorder 等。

> [!warning] 版本约束
> 不应把某插件“仓库仍活跃”理解为本机可直接安装其最新版。QuickAdd 和 Templater 的调研时 manifest 要求 Obsidian 1.13.0，因此本机 1.12.7 仍不满足；Copilot 要求 1.11.4，版本门已满足，但与 Codex 重叠和联网隐私风险仍使其不进入推荐栈。

## 原生能力已经覆盖什么

| 需求 | 原生能力 | 当前结论 |
|---|---|---|
| 结构化元数据 | Properties + Bases | 新 vault 先用 Bases；只有遇到行内字段、任务查询或 DataviewJS 才考虑 Dataview。 |
| 流程与架构说明 | Mermaid fenced block | Codex 可直接生成，Obsidian 原生渲染，不需要 Mermaid 插件。 |
| 空间化整理 | Canvas | 适合摆放笔记卡片、附件和网页，先验证原生限制再加 Advanced Canvas。 |
| PDF 阅读 | 内置 PDF viewer + `![[file.pdf#page=N]]` | 已能嵌入和定位页码；需要高亮回链时再加 PDF++。 |
| 检索 | Search、Quick Switcher、Graph、Backlinks | fresh vault 足够；规模增大或 PDF/OCR 检索成为瓶颈时再加 Omnisearch。 |
| 模板 | Templates | Codex 主导写入时足够；只有需要在 Obsidian 内动态脚本化创建时才需要 Templater。 |
| 网页采集 | 官方 Web Clipper 浏览器扩展 | 本地保存 Markdown、无厂商锁定，是最符合当前隐私边界的采集入口。 |

## 核心原则

原生能力优先并不是拒绝社区插件，而是降低长期依赖面：当一个插件停止维护时，纯 Markdown、Properties、wikilinks、Mermaid 和 JSON Canvas 仍可被其他工具读取。^[inferred]

## Sources

- [Introduction to Bases](https://obsidian.md/help/bases)
- [Canvas core plugin](https://obsidian.md/help/plugins/canvas)
- [Obsidian Web Clipper](https://obsidian.md/help/web-clipper)
- [Embed files and PDFs](https://help.obsidian.md/linking+notes+and+files/embedding+files)
- [Obsidian changelog](https://obsidian.md/changelog/)
