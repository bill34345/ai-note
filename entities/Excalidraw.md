---
title: Excalidraw for Obsidian
category: entities
tags: [obsidian, visualization, diagram, local-first]
aliases: [Obsidian Excalidraw, Excalidraw]
sources: [https://community.obsidian.md/plugins/obsidian-excalidraw-plugin, https://github.com/zsviczian/obsidian-excalidraw-plugin]
summary: 在 Obsidian 中创建和编辑可链接的自由绘图、架构草图和视觉说明，默认本地离线。
relationships:
  - target: "[[synthesis/Obsidian-Codex-AI学习知识库工具链调研]]"
    type: uses
provenance: {extracted: 0.86, inferred: 0.14, ambiguous: 0.0}
base_confidence: 0.84
lifecycle: draft
lifecycle_changed: 2026-07-16
tier: core
created: 2026-07-15T21:52:04+08:00
updated: 2026-07-16T00:31:15+08:00
---

# Excalidraw for Obsidian

## 适合场景

- AI Agent 架构草图、组件关系、比较图和需要手工调整的概念图。
- 将 drawing 内元素与 Markdown 笔记互相链接。
- 配合 Codex 的 `excalidraw-diagram`：Codex 生成初稿，用户在 Obsidian 内审阅和修改。

## 不应承担的场景

- 需要精确 diff 的流程图或时序图优先 Mermaid。
- 只是摆放现有笔记卡片时优先核心 Canvas。
- 不要默认开启 AI、Taskbone OCR、远程字体或外部图片等联网功能。

## 风险

插件由单一主要开发者维护且功能面很大；源码说明某些导出、缓存和高级功能会使用 IPC、动态代码或可选网络能力。只启用实际需要的本地绘图功能。^[inferred]

## 结论

**评分 88/100，首批采用，现已启用。** 当前安装版本 2.25.3 的最低 Obsidian 版本为 1.8.7，兼容本机 Obsidian 1.12.7。

## 本机验收

- 社区插件清单已启用 `obsidian-excalidraw-plugin`，manifest 版本为 2.25.3。
- 已创建包含矩形和中文文本“Excalidraw 验收测试”的绘图。
- 绘图已保存、关闭并重新打开，Obsidian 能继续渲染和编辑。
- 验收文件保存在 `Excalidraw/`；联网 AI/OCR 功能未作为本轮验收范围。

## Sources

- [Plugin page](https://community.obsidian.md/plugins/obsidian-excalidraw-plugin)
- [Official repository and privacy disclosure](https://github.com/zsviczian/obsidian-excalidraw-plugin)
