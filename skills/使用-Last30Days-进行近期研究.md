---
title: 使用 Last30Days 进行近期研究
category: skills
tags: [ai, codex, research, agent-skill]
aliases: [使用 last30days, Codex 近期研究, /last30days]
sources:
  - "[[references/Last30Days-Skill-GitHub仓库]]"
relationships:
  - target: "[[entities/Last30Days-Skill]]"
    type: uses
  - target: "[[concepts/多源时效研究管线]]"
    type: uses
  - target: "[[skills/Codex学习工作流]]"
    type: related_to
summary: 在 Codex 中安全评估、安装和验收 Last30Days 的操作指南，强调 preflight、cookie 同意、逐来源覆盖状态、原始结果检查与知识库后续核实。
provenance: {extracted: 0.63, inferred: 0.37, ambiguous: 0.00}
base_confidence: 0.54
lifecycle: draft
lifecycle_changed: 2026-07-16
tier: supporting
created: 2026-07-16T14:47:14+08:00
updated: 2026-07-16T14:47:14+08:00
---

# 使用 Last30Days 进行近期研究

> [!warning] 当前状态
> 本机尚未安装 `last30days` Skill，也未执行上游 Engine。Python 是 3.11.9，低于项目要求的 3.12+；虽然 `uv` 已存在且上游声称可自动供应 3.12，本轮没有运行该路径。以下命令来自 v3.16.0 固定提交，不代表已经验收。

## 什么时候值得用

适合：

- 了解某个人、公司、项目或技术最近一个月的公开动态。
- 比较多个工具近期的发布、社区评价和真实使用摩擦。
- 在正式调研前发现社区用语、争议点、关键账号和高价值来源。
- 建立定期趋势监控或可搜索的近期研究库。

不适合单独承担：

- 法律、医疗、财务等高风险最终结论。
- 长期历史、系统综述或只看官方规范即可回答的问题。
- 需要私密账号操作、发帖、点赞或修改外部内容的任务；该项目定位是只读研究。
- 无法接受第三方 API、cookie 或本地研究文件写入的数据场景。

## 安装前审查

1. 阅读 [[references/Last30Days-Skill-GitHub仓库]] 的版本、数据流和本机准备度。
2. 用 `npx skills add mvanhorn/last30days-skill -l` 查看将安装的技能和目标路径。
3. 确认只保留一种安装方式，避免同一宿主同时出现 marketplace 与 `npx skills` 的重复 Skill。
4. 决定全局还是项目级：研究工具通常适合全局；敏感或实验用途可先项目级隔离。
5. 不要把 API Key 写进公开 vault、项目 `.env` 或聊天记录；上游默认全局配置位置是用户目录下 `.config/last30days/.env`。

上游提供的 Codex 全局安装命令是：

```powershell
npx skills add mvanhorn/last30days-skill -g -a codex
```

本轮没有执行该命令。

## 首次运行的安全顺序

安装后，不要直接开始大型研究。先从已加载 Skill 目录运行只读 preflight：

```powershell
python <SKILL_DIR>\scripts\last30days.py --preflight
```

如果系统 Python 仍是 3.11，应先观察 Skill 的 Python 3.12 解析结果；不要把 `uv` 自动下载解释为已经发生。preflight 应重点检查：

- 实际加载的是哪个 `SKILL.md` 与 Engine 路径。
- 配置来自进程、全局配置还是被信任的项目配置。
- 是否计划读取浏览器 cookie，以及具体浏览器范围。
- 会安装或调用哪些可选 CLI。
- 研究文件和缓存计划写到哪里。
- 是否存在会把研究切换到远端后端的 endpoint override。

只有在用户明确同意后，才进入 setup 的 cookie 读取或 GitHub device-auth 流程。

## 建议的最小验收

1. **版本和文件**：确认 `SKILL.md`、`scripts/` 与 plugin manifest 都是 `3.16.0`，避免旧缓存和新 Engine 混用。
2. **只读 preflight**：保存输出，确认未读取 cookie 值、未写配置或研究报告。
3. **免费来源小样本**：选一个公开、低风险、容易人工核实的项目主题，用 quick 模式运行。
4. **覆盖状态**：检查 `source_status`，区分 `no-results` 与失败/未配置。
5. **原始文件**：确认写入目录、文件名、Markdown/JSON 内容和权限；搜索是否误写 API Key、cookie 或私有 corpus。
6. **事实抽查**：至少抽查一个 Reddit/HN 项目、一个 GitHub 数字和一个网页补充来源。
7. **健康复盘**：运行 `doctor --postmortem`，验证它能解释上次运行中每个来源的真实结果。
8. **发布隔离**：不测试 `--publish`，除非用户明确想把简报发布到公开托管面。

只有这些步骤通过后，才能把页面状态从“来源审计”升级为“本机运行验收”。^[inferred]

## 在 Codex 中提问

安装后可明确点名 Skill，避免宿主把请求当普通搜索：

```text
使用 last30days skill 研究 Codex 最近 30 天的真实用户反馈，先报告每个来源的覆盖状态，再给结论。
```

对开源项目，问题应包含希望区分的证据层：

```text
使用 last30days skill 研究 mvanhorn/last30days-skill：把 GitHub 发布活动、社区使用反馈和作者宣传分开，不要把 stars 当成质量证明。
```

上游大量使用 `/last30days <topic>` 表达调用意图；在 Codex 中应以实际加载的 skill 名称或自然语言明确点名为准。^[inferred]

## 中文主题注意事项

上游 v3.16.0 已有 CJK 分词支持，但 `SKILL.md` 把非拉丁主题列为关键词陷阱：要求使用能覆盖非英文网页的 Web 后端，并提醒 Reddit/HN/GitHub 可能几乎没有同语种结果。中文研究还应：

- 明确中文名、英文名、产品名和官方账号，避免同名污染。
- 小红书只有在本地登录服务已运行且本次显式选择时才会搜索。
- 不要因英文平台无结果就断言中文社区没有讨论。
- 对中文网页的发布日期、转载链和原始来源做额外核实。

## 如何读结果

- 先看时间窗和解析出的实体是否正确。
- 再看每个来源的 outcome，而不是只看条目数。
- 优先读跨来源证据簇，但保留单一来源和薄证据标记。
- 把互动量当作“值得检查”的排序，不当作真伪证明。
- GitHub stars、预测概率、观看量等实时数字需要注明日期，并在高风险输出前刷新。
- 研究结果进入 AI-wiki 时，继续按 [[skills/Codex学习工作流]] 回到官方文档、release 和源码核实。

## 隐私决策表

| 功能 | 需要先确认什么 |
|---|---|
| 浏览器 cookie | 用户是否允许读取；哪一个浏览器；X 账号抓取风险 |
| ScrapeCreators / xAI / Perplexity 等 | 查询和内容会发送到哪一家；费用与配额；Key 存储位置 |
| 本地 corpus | 哪些目录被读；是否包含私密笔记；是否会进入 raw JSON 或缓存 |
| 远端 API backend | `LAST30DAYS_API_BASE` 指向谁；是否会收到完整主题和上下文 |
| 研究文件 | `LAST30DAYS_MEMORY_DIR` 在哪里；是否会被云盘或 Git 同步 |
| HTML publish | 页面默认公开；是否需要密码；是否允许被搜索引擎索引 |

## Related

- [[entities/Last30Days-Skill]]
- [[concepts/多源时效研究管线]]
- [[references/Last30Days-Skill-GitHub仓库]]
- [[skills/Codex学习工作流]]

