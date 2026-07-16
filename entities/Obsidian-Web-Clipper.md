---
title: Obsidian Web Clipper
category: entities
tags: [obsidian, capture, web, local-first]
aliases: [Web Clipper]
sources: [https://obsidian.md/help/web-clipper, https://github.com/obsidianmd/obsidian-clipper]
summary: Obsidian 官方浏览器扩展，将网页和高亮以本地 Markdown 保存到 vault，不收集使用数据。
relationships:
  - target: "[[synthesis/Obsidian-Codex-AI学习知识库工具链调研]]"
    type: uses
provenance: {extracted: 0.94, inferred: 0.06, ambiguous: 0.0}
base_confidence: 0.93
lifecycle: draft
lifecycle_changed: 2026-07-16
tier: core
created: 2026-07-15T21:52:04+08:00
updated: 2026-07-16T00:31:15+08:00
---

# Obsidian Web Clipper

## 适合本 vault 的原因

- 官方扩展，网页内容保存为本地、耐久的 Markdown。
- 官方声明不收集数据或使用统计。
- 可用模板保留 URL、标题、作者、发布时间和高亮，正好补齐“来源入口”。
- 与 Codex 分工清晰：Clipper 捕获原始材料，Codex 负责核实、蒸馏、交叉链接和综合。

## 结论

**评分 98/100，首批采用，现已启用。** 它不是 Obsidian 社区插件，而是浏览器扩展。

## 本机验收

- Web Clipper 1.7.0 已由用户安装并启用。
- 已将目标 vault 明确设置为 `AI-wiki`，目标目录设置为 `_raw`。
- 端到端测试已生成约 20 KB 的 Markdown：标题、原始 GitHub URL、描述、标签、正文、代码块和外部链接均已保存。
- 文件本体为有效 UTF-8；破折号和箭头等 Unicode 字符未损坏。
- 当前测试只覆盖整页剪藏；高亮剪藏和本地图片附件仍需在真实需要出现时另行验收。

## Sources

- [Official documentation](https://obsidian.md/help/web-clipper)
- [Official open-source repository](https://github.com/obsidianmd/obsidian-clipper)
