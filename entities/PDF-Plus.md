---
title: PDF++
category: entities
tags: [obsidian, pdf, annotation, research]
aliases: [PDF Plus]
sources: [https://community.obsidian.md/plugins/pdf-plus, https://github.com/RyotaUshio/obsidian-pdf-plus]
summary: 在 Obsidian 原生 PDF viewer 上增加高亮回链、Markdown 侧注和阅读体验增强的本地插件。
relationships:
  - target: "[[synthesis/Obsidian-Codex-AI学习知识库工具链调研]]"
    type: uses
provenance: {extracted: 0.88, inferred: 0.12, ambiguous: 0.00}
base_confidence: 0.8
lifecycle: draft
lifecycle_changed: 2026-07-15
tier: supporting
created: 2026-07-15T21:52:04+08:00
updated: 2026-07-16T00:31:15+08:00
---

# PDF++

## 价值

- 把指向 PDF 文本选择的链接显示为高亮，并让高亮反向连接到 Markdown 侧注。
- 侧注保持为普通 Markdown；插件停止工作后正文仍可读。
- 适合将 AI 论文的原文证据与概念页连接，而不是只保存整篇摘要。

## 风险与边界

- 插件明确依赖多项 Obsidian 私有 API，Obsidian 更新可能破坏功能。
- 当前 release 为 0.40.31（2025-08）；仓库说明正在进行 1.0 大型重构，维护空窗不等于弃用，但增加了不确定性。
- 如果主要阅读在 Zotero 中完成，则应比较 Zotero Integration，避免两套高亮来源。

## 结论

**评分 89/100，论文阅读条件下首批采用。** 当前最低 Obsidian 1.5.8，兼容本机 1.12.7。没有稳定 PDF 阅读习惯时先不装。

## Sources

- [Plugin page](https://community.obsidian.md/plugins/pdf-plus)
- [Official repository](https://github.com/RyotaUshio/obsidian-pdf-plus)
