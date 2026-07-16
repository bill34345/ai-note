---
title: 使用 Claude Video 分析视频
category: skills
tags: [ai, codex, video, agent-skill]
aliases: [使用 watch skill, Codex 视频分析]
sources:
  - https://github.com/bradautomates/claude-video
relationships:
  - target: "[[entities/Claude-Video]]"
    type: uses
  - target: "[[concepts/Agent-视频理解管线]]"
    type: uses
  - target: "[[skills/Codex学习工作流]]"
    type: related_to
summary: 在 Codex 中评估、安装和使用 Claude Video watch skill 的实操指南，包含触发语法、detail 选择、隐私边界及写入 AI-wiki 的后续步骤。
provenance: {extracted: 0.58, inferred: 0.42, ambiguous: 0.00}
base_confidence: 0.54
lifecycle: draft
lifecycle_changed: 2026-07-16
tier: supporting
created: 2026-07-16T00:24:06+08:00
updated: 2026-07-16T00:31:15+08:00
---

# 使用 Claude Video 分析视频

> [!warning] 当前状态
> 本机具备 `python`、`ffmpeg`、`ffprobe`、`yt-dlp`、`node` 和 `npx`，但 **尚未安装 `watch` skill**。以下安装命令来自上游仓库，本轮没有执行；也没有上传任何视频或配置 Whisper API Key。

## Codex 中如何触发

安装后优先使用 Codex 的 skill 触发形式：

```text
$watch <视频 URL 或本地路径> <你想了解的问题>
```

也可以明确写成自然语言：

```text
使用 watch skill 分析这个视频，重点解释 02:10–03:00 的 Agent 工具调用流程。
```

上游 README 大量使用 `/watch`，那是 Claude Code 风格的统一命令名；在 Codex 中应以实际出现的 `$watch` skill 或明确点名 skill 为准。^[inferred]

## 安装方式（尚未执行）

只安装到 Codex、对当前用户全局可用的候选命令：

```powershell
npx skills add bradautomates/claude-video -g -a codex
```

上游最简命令是：

```powershell
npx skills add bradautomates/claude-video -g
```

后者会让 Agent Skills CLI 自行检测多个宿主。安装前应先用 `-l` 查看将要安装的 skill，并确认目标路径与来源：

```powershell
npx skills add bradautomates/claude-video -l
```

## detail 选择

| 目标 | 建议起点 | 原因 |
|---|---|---|
| 先判断视频值不值得深入 | `--detail transcript` | 有字幕时无需下载视频，成本最低 |
| 快速查看画面主线 | `--detail efficient` | 关键帧提取快，最多 50 帧 |
| 教程、产品演示、屏幕录制 | `--detail balanced` | 场景变化与 100 帧上限之间折中 |
| 视觉变化非常密集 | `--detail token-burner` | 不设硬上限，但 token 成本可能很高 |

对十分钟以上的视频，先跑 transcript，再用 `--start`、`--end` 聚焦真正需要视觉核对的片段，通常比直接扫描全片更有效。^[inferred]

## AI 学习视频的建议流程

1. **先提出具体问题**：不要只说“总结”，而要问核心观点、演示步骤、证据和仍不理解的点。
2. **先读转录结构**：用 `transcript` 找章节、术语和关键时间点。
3. **再补视觉证据**：对代码、架构图、UI 操作所在时段使用 `balanced` 与聚焦区间。
4. **区分内容与事实**：先记录“视频声称什么”，再到官方文档、代码仓库或论文核实。
5. **写入知识库**：把原始分析作为来源材料，再按 [[skills/Codex学习工作流]] 编译为实体、概念和技能页面。

## 隐私决策

> [!danger] 敏感本地视频
> 没有原生字幕时，默认 Whisper 回退可能把提取音频发送到 Groq 或 OpenAI。处理内部会议、私人录屏或含个人数据的视频时，应明确加 `--no-whisper`，或先获得上传授权。

- 公共视频仍会被 `yt-dlp` 从来源网站请求。
- 视频、帧、音频和中间转录会暂存在系统临时目录；完成后应清理。
- `--out-dir` 会保留工作文件，适合需要复核，但也增加本地残留风险。
- API Key 应保存在 `~/.config/watch/.env`，不要写入 vault 或聊天记录。

## 最小验收方案

如果以后决定安装，不应以“目录里出现了 SKILL.md”为完成：

1. 检查 skill 目录同时包含 `SKILL.md` 与 `scripts/`。
2. 用一个短、公开、带字幕的视频运行 `transcript`。
3. 用同一视频的 20–30 秒区间运行 `balanced`，确认帧时间戳和画面可读。
4. 对照原视频抽查至少三个时间点，判断回答是否忠实。
5. 确认未配置 Whisper 时不会在无授权情况下上传音频。
6. 把结果经 [[concepts/Agent-视频理解管线]] 和 Wiki ingest 流程写入 Obsidian，验证来源回链。

## Related

- [[entities/Claude-Video]] — 工具本身及运行边界。
- [[concepts/Agent-视频理解管线]] — 为什么需要转录与视觉双流。
- [[references/Claude-Video-GitHub仓库]] — 安装与行为的上游证据。
- [[skills/Codex学习工作流]] — 分析结果进入 AI-wiki 的后续步骤。

## Sources

- [[references/Claude-Video-GitHub仓库]]
- [`skills/watch/SKILL.md`](https://github.com/bradautomates/claude-video/blob/main/skills/watch/SKILL.md)
