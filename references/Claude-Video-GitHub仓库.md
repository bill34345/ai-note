---
title: Claude Video GitHub 仓库
category: references
tags: [ai, agent-skill, video, github]
aliases: [claude-video repository, bradautomates/claude-video]
sources:
  - https://github.com/bradautomates/claude-video
source_id: github.com/bradautomates/claude-video
source_type: repository
retrieved: 2026-07-16
relationships:
  - target: "[[entities/Claude-Video]]"
    type: related_to
  - target: "[[skills/使用-Claude-Video-分析视频]]"
    type: related_to
summary: claude-video 上游仓库的来源记录，覆盖 v0.2.0、Codex 安装修复、运行数据流、安全边界及尚未验证的作者声明。
provenance: {extracted: 0.90, inferred: 0.10, ambiguous: 0.00}
base_confidence: 0.54
lifecycle: draft
lifecycle_changed: 2026-07-16
tier: supporting
created: 2026-07-16T00:24:06+08:00
updated: 2026-07-16T00:31:15+08:00
---

# Claude Video GitHub 仓库

> [!tldr]
> `bradautomates/claude-video` 是 `watch` Agent Skill 的上游仓库。它用 `yt-dlp`、`ffmpeg`、字幕或 Whisper，把视频转换为“时间戳转录 + 抽样帧”，再交给支持图像读取的 Agent 回答问题。

## 当前快照

| 项目 | 2026-07-16 核实结果 |
|---|---|
| 仓库 | [bradautomates/claude-video](https://github.com/bradautomates/claude-video) |
| 最新发布 | v0.2.0，2026-07-01 发布 |
| 主要语言 | Python |
| 许可证 | MIT |
| Skill 入口 | `skills/watch/SKILL.md` |
| Codex 安装入口 | `npx skills add bradautomates/claude-video -g` |

v0.2.0 将 `SKILL.md` 与运行脚本重组为自包含的 `skills/watch/` 包。上游 changelog 明确说明，旧版通过 `npx skills add` 安装到 Codex 等非 Claude 宿主时会漏掉脚本，v0.2.0 修复了这一问题。

## 从仓库能够确认的事实

- 输入可以是 `yt-dlp` 支持的公开视频 URL，或本地 `.mp4`、`.mov`、`.mkv`、`.webm` 等文件。
- 原生字幕优先；没有字幕时，可以把抽取出的音频交给 Groq `whisper-large-v3` 或 OpenAI `whisper-1`。
- `transcript`、`efficient`、`balanced`、`token-burner` 四种 detail 模式分别控制是否取帧、取帧引擎和帧上限。
- 默认帧去重把图片缩为 16×16 灰度缩略图，并按与“上一个保留帧”的平均绝对差过滤近重复帧。
- v0.1.3 修复过 Windows UTF-8 读取问题，并针对 URL/路径参数注入强化了子进程调用。
- 上游包含 pytest 测试，但本次只核实了仓库结构与公开说明，没有克隆仓库或运行其测试。

## 作者声明，不等于本机实测

- README 中的速度、帧数、token 估算来自作者选定的一段 49:08 视频，不能外推为所有视频的性能。
- “看过视频后能准确回答”的效果取决于字幕质量、抽帧覆盖、宿主模型视觉能力和问题范围；本次没有实际运行 `watch`，因此不把效果宣传写成已验证结论。
- 仓库的安装命令存在，不代表当前 Codex 已安装；本机检查结果是 `watch` skill **尚未安装**。

## 数据与隐私边界

| 数据 | 默认位置或去向 |
|---|---|
| 视频、帧、音频、中间转录 | 系统临时目录，或用户指定的 `--out-dir` |
| 公共视频请求 | 由 `yt-dlp` 直接访问视频来源站点 |
| 有原生字幕 | 通常不需要 Whisper API |
| 无原生字幕且启用 Whisper | 提取音频发送到 Groq 或 OpenAI |
| API Key | `~/.config/watch/.env` |

对敏感本地视频，应优先使用 `--no-whisper`，否则音频可能离开本机。^[inferred]

## 关联页面

- [[entities/Claude-Video]] — 工具定位、组件和能力边界。
- [[concepts/Agent-视频理解管线]] — “字幕 + 抽样帧”的一般机制。
- [[skills/使用-Claude-Video-分析视频]] — 面向 Codex 的安装、触发和使用策略。
- [[skills/Codex学习工作流]] — 如何把分析结果继续编译为知识库页面。

## Sources

- [Repository README](https://github.com/bradautomates/claude-video)
- [CHANGELOG](https://github.com/bradautomates/claude-video/blob/main/CHANGELOG.md)
- [`skills/watch/SKILL.md`](https://github.com/bradautomates/claude-video/blob/main/skills/watch/SKILL.md)
- [v0.2.0 release](https://github.com/bradautomates/claude-video/releases/tag/v0.2.0)
