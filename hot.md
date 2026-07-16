---
title: Hot Cache
updated: 2026-07-16T14:47:14+08:00
---

# Hot Cache

*近期活动的语义快照。*

## Recent Activity

- [2026-07-15T22:09:23+08:00] 完成 Obsidian × Codex 工具链调研，推广 9 个已审阅页面。
- [2026-07-16T00:07:55+08:00] 完成 Obsidian 1.12.7、Web Clipper 1.7.0 与 Excalidraw 2.25.3 的本机主路径验收。
- [2026-07-16T00:28:33+08:00] 完成首个 Raw Mode 学习闭环：将 claude-video 剪藏编译为来源、实体、概念和技能四个页面。
- [2026-07-16T14:47:14+08:00] 按第三方 Agent 项目工作流完成 last30days-skill v3.16.0 固定提交采集，新增来源、实体、概念和技能四个页面。

## Active Threads

- Web Clipper 与 Excalidraw 已进入实际使用观察期；PDF++ 仍等待真实论文阅读需求触发。
- `watch` skill 已完成资料审计但尚未安装；只有用户决定实际分析视频时才进入隔离安装与运行验收。
- `last30days` 已完成 v3.16.0 来源审计但尚未安装或运行；下一门槛是安装后先跑只读 preflight，再决定 cookie、外部 API 与最小研究验收。

## Key Takeaways

- 原生 Bases、Canvas、Mermaid、Properties 和 Search 应先于社区插件。
- 首批候选 Web Clipper、Excalidraw 已启用并通过主路径验收；PDF++ 仅在论文阅读明确时加入。
- Obsidian 已升级到 1.12.7；未来新增插件仍逐项检查 `minAppVersion`。
- 视频理解应把转录与视觉帧作为两条互补证据流，并把“视频声称什么”与“事实是否成立”分开。
- Claude Video 无字幕时的 Whisper 回退可能上传提取音频；敏感视频应优先 `--no-whisper`。
- Last30Days 是 Skill 合约与 Python Engine 的双层系统；只做普通 Web 搜索不等于运行该 Skill。
- Last30Days 的“来源支持”取决于本次配置、CLI、cookie/API 与逐来源 outcome；无结果不能和来源失败混为一谈。
- 本机 Python 3.11.9 低于其 3.12+ 要求；`uv` 存在但自动供应路径尚未运行验证，Digg/arXiv/Techmeme/Trustpilot CLI 也尚未发现。

## Flagged Contradictions

- Zotero Integration 是否值得采用，取决于用户是否选择 Zotero + Better BibTeX 作为主论文库。
- Spaced Repetition 是否值得采用，取决于用户是否明确需要记忆测验，而不是仅做理解型笔记。
- claude-video 的性能表和准确性描述来自作者测试，本机尚未安装运行，不能视为已验证能力。
- last30days 的 zero-config、无追踪、密钥不入输出等属于上游规范与静态代码声明；本机尚未通过 preflight、最小研究和输出文件检查验证。
