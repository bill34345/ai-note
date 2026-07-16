---
title: Obsidian 学习与研究工作流真实用户实践
category: references
tags: [obsidian, user-practice, learning, research, ai]
sources:
  - https://www.reddit.com/r/ObsidianMD/comments/1t4eilr/my_obsidian_plugin_list_in_2026_after_deleting/
  - https://www.reddit.com/r/ObsidianMD/comments/1ul87y2/my_obsidian_setup_for_2_years_of_phd_research/
  - https://www.reddit.com/r/ObsidianMD/comments/1u7iqs0/i_use_my_obsidian_vault_as_a_shared_context_layer/
  - https://forum.obsidian.md/t/dataview-vs-bases/113073
  - https://forum.obsidian.md/t/obsidian-university-workflow-templater-powered-notes-for-students/106984
  - https://forum.obsidian.md/t/zotero-zotfile-mdnotes-obsidian-dataview-workflow/15536
summary: 近期真实用户在技术学习、AI/LLM 研究、PhD 阅读和 Agent 共享上下文中的插件实践、收益与失败模式。
provenance: {extracted: 0.80, inferred: 0.20, ambiguous: 0.00}
base_confidence: 0.72
lifecycle: draft
lifecycle_changed: 2026-07-15
tier: supporting
created: 2026-07-15T21:52:04+08:00
updated: 2026-07-16T00:31:15+08:00
---

# Obsidian 学习与研究工作流真实用户实践

## 重复出现的稳定实践

1. **每篇来源有独立 source/literature note，但综合发生在概念或主题页。** PhD 用户会保留摘要、方法、结果、与自身工作的连接，而不是只存 PDF 或全文转录。
2. **Dataview/Templater 常见，但不是目的。** 用户用它们保持命名、元数据和动态列表一致；当 Bases 足以表达阅读清单和项目追踪时，已有用户迁移到核心 Bases。
3. **Excalidraw 与 Canvas 分工。** Canvas 更适合摆放已有笔记；Excalidraw 更适合架构草图、自由形状和视觉解释。
4. **搜索在规模化后才成为硬需求。** 一个约 3,200 篇笔记、80 篇 AI 论文的用户保留 Omnisearch，理由是 PDF 内搜索真正提高了资料复用率；同一用户把插件总数控制在 15 个以内。
5. **AI 负责采集、整理与草拟，人必须审阅。** 把 vault 作为 Codex/Claude 共享上下文的用户强调：自动化处理的是信息，只有人工复核后才成为知识。

## 常见失败模式

- 因热门清单安装过多插件，最终产生启动、维护和认知税。
- 把 Obsidian 改造成 Notion/GTD/项目管理系统，却不再打开复杂看板。
- 生成大量论文摘要或课堂转录，但没有自己的解释、问题和跨来源综合。
- 让 AI 直接写“结论”且不保留来源、diff 和审核门，导致错误进入长期知识。
- 将 Graph 当作自动发现知识缺口的工具；实践上仍需要稳定的元数据、主题页和有目的的综合。

> [!important] 对本 vault 的含义
> 用户实践支持“小而可替换的插件集 + 明确人工审阅门”，这与 Codex 主导、staged writes 和来源可追溯的方向一致。^[inferred]

## Sources

- [2026 coding/AI knowledge-base plugin list after two cleanups](https://www.reddit.com/r/ObsidianMD/comments/1t4eilr/my_obsidian_plugin_list_in_2026_after_deleting/)
- [Two years of PhD research in Obsidian](https://www.reddit.com/r/ObsidianMD/comments/1ul87y2/my_obsidian_setup_for_2_years_of_phd_research/)
- [Obsidian as shared context for AI tools](https://www.reddit.com/r/ObsidianMD/comments/1u7iqs0/i_use_my_obsidian_vault_as_a_shared_context_layer/)
- [Dataview vs Bases, 2026 user discussion](https://forum.obsidian.md/t/dataview-vs-bases/113073)
- [Templater-powered university workflow](https://forum.obsidian.md/t/obsidian-university-workflow-templater-powered-notes-for-students/106984)
- [Zotero to Obsidian workflow and caveats](https://forum.obsidian.md/t/zotero-zotfile-mdnotes-obsidian-dataview-workflow/15536)
