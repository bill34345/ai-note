---
title: Codex 与 Agent Skills 生态检索
category: references
tags: [codex, agent-skills, obsidian, skills]
sources:
  - https://skills.sh/
  - https://github.com/Ar9av/obsidian-wiki
summary: 本机已安装的 LLM Wiki、Obsidian 和可视化 skills，以及 skills.sh 外部候选的可用性与重复关系。
provenance: {extracted: 0.88, inferred: 0.12, ambiguous: 0.0}
base_confidence: 0.83
lifecycle: draft
lifecycle_changed: 2026-07-15
tier: supporting
created: 2026-07-15T21:52:04+08:00
updated: 2026-07-16T00:07:55+08:00
---

# Codex 与 Agent Skills 生态检索

## 已验证层级

- `obsidian-wiki 2026.7.3` CLI 可运行，bundled skills 检查通过；对当前 vault 显式执行 `cache-check` 成功。
- AnySearch 已完成 general、code、social_media 搜索与真实 Reddit 结果读取，属于端到端可用。
- `npx skills find` 已完成 `obsidian`、`knowledge graph`、`academic research`、`diagram visualization`、`spaced repetition` 五组查询。
- `obsidian-markdown` 已实际用于生成本批符合 Obsidian 语法、frontmatter、callout、wikilink 和 Mermaid 的页面。
- 其他 skill 的“已安装”不等于本次已完成端到端测试；没有输入样本或会产生额外制品的能力保持为“可触发、未在本轮执行”。

## 已安装且直接适合学习的 skills

| Skill | 典型触发 | 产出/写入 | 外部服务 | 与 Obsidian 插件分工 |
|---|---|---|---|---|
| `llm-wiki` | “按 LLM Wiki 组织这批知识” | 结构和规则 | 无 | 定义来源→知识页→schema，不是 UI 插件。 |
| `wiki-research` | `/wiki-research <主题>` | references/concepts/entities/synthesis | 搜索阶段联网 | 多轮调研并编译进 vault。 |
| `wiki-ingest` | “把这个 URL/PDF/文档入库” | 更新相关知识页 | 依来源而定 | 避免只生成孤立摘要。 |
| `wiki-query` | “基于 vault 回答……” | 只读答案/查询日志 | 可选 QMD | 替代大部分 Obsidian 内 AI 问答插件。 |
| `wiki-status` | `/wiki-status` | delta、token footprint、健康建议 | 无 | 替代单纯的“知识库统计”插件。 |
| `wiki-lint` | `/wiki-lint` | 链接、frontmatter、重复与矛盾报告 | 无 | 做内容健康审计。 |
| `wiki-synthesize` | “跨这些页面综合” | synthesis 页面 | 无 | 负责跨来源连接，不依赖 Graph 自动猜测。 |
| `cross-linker` | “补全合理双链” | wikilinks/relationships | 无 | 维护链接语义。 |
| `obsidian-markdown` | 创建或编辑 Obsidian `.md` | 标准 Markdown | 无 | 负责语法正确性。 |
| `obsidian-bases` | “为这些笔记建一个 Base” | `.base` | 无 | 与核心 Bases 配合，不需要 Dataview。 |
| `json-canvas` | “把这些概念做成 Canvas” | `.canvas` | 无 | 配合核心 Canvas。 |
| `excalidraw-diagram` | “生成可编辑手绘架构图” | Excalidraw 文件 | 无；查看需插件 | Codex 生成，Excalidraw 插件负责查看和手工编辑。 |
| `mermaid-visualizer` | “生成流程图/时序图” | Mermaid Markdown | 无 | Obsidian 原生渲染，无需 Mermaid Tools。 |
| `imagegen` | “为页面生成概念插图” | raster image | OpenAI 图像服务 | 只用于插图，不应用来表达需要精确版本控制的逻辑图。 |
| `anysearch` | 搜索、核实、读取 URL | 来源包 | AnySearch API | 负责外部事实，不替代 vault 内检索。 |
| `find-skills` | “找一个能做 X 的 skill” | skills.sh 候选 | npm/skills.sh | 只发现，不自动证明质量。 |

PDF、Documents、Presentations skills 在当前 Codex 会话中由 bundled primary runtime 提供，但不位于普通 `~/.codex/skills` 或 `~/.agents/skills` 目录；它们是可用会话能力，不应被误报为本地目录缺失。

## 外部 skills 检索结论

- `kepano/obsidian-skills` 的 `obsidian-markdown`、`obsidian-bases`、`json-canvas` 已安装，无需重复安装。
- `kepano/obsidian-skills@obsidian-cli` 的版本前提已因 Obsidian 更新到 1.12.7 而满足，但尚未验证 CLI 是否已启用、skill 是否安装以及端到端调用，因此仍只列为待评估能力。
- `defuddle` 可作为网页正文清洗备选，但 AnySearch 已具备 URL extraction，当前不是缺口。
- 外部 academic-research、knowledge-graph、diagram skills 多数与 `wiki-research`、`wiki-status`、`cross-linker` 和现有三种可视化 skills 重叠；仅凭 skills.sh installs 不建议安装。^[inferred]
- spaced-repetition 类 agent skills 采用量和证据较弱；真正的复习调度更适合使用成熟 Obsidian Spaced Repetition 插件或专门的 Anki，而不是让 Agent 自行维护时间表。^[inferred]

## 配置边界

`obsidian-wiki doctor` 当前仍读取全局 vault 配置；本项目的 `.env` 是 Codex skills 按 walk-up 规则解析的项目本地边界。调用 CLI 子命令时应继续显式传入当前 vault 路径，不能依据 doctor 的全局 vault 报告。 

## Sources

- [skills.sh](https://skills.sh/)
- [Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki)
- [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
