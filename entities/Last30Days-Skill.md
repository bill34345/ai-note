---
title: Last30Days Skill
category: entities
tags: [ai, agent-skill, research, social-search]
aliases: [last30days, /last30days, mvanhorn last30days]
sources:
  - "[[references/Last30Days-Skill-GitHub仓库]]"
relationships:
  - target: "[[concepts/多源时效研究管线]]"
    type: implements
  - target: "[[skills/使用-Last30Days-进行近期研究]]"
    type: related_to
  - target: "[[skills/Codex学习工作流]]"
    type: related_to
summary: Last30Days 是一个多宿主 Agent Skill，把实体解析、多平台近期信号采集、互动量排序、跨来源聚类和证据综合组合成可追溯研究简报。
provenance: {extracted: 0.82, inferred: 0.18, ambiguous: 0.00}
base_confidence: 0.54
lifecycle: draft
lifecycle_changed: 2026-07-16
tier: supporting
created: 2026-07-16T14:47:14+08:00
updated: 2026-07-16T14:47:14+08:00
---

# Last30Days Skill

> [!tldr]
> Last30Days 是一个近期研究 Agent Skill。它的差异不只是“限定最近 30 天”，而是把平台互动量、评论、转录、预测市场赔率、GitHub 活动和普通网页放进同一条证据管线，并明确报告哪些来源本次真的工作、哪些只是未配置或失败。

## 它解决什么问题

通用网页搜索偏向被索引和 SEO 优化的页面，难以同时覆盖 Reddit 评论、X 帖子、YouTube 转录、TikTok/Instagram 内容、预测市场和 GitHub 活动。Last30Days 试图把这些相互隔离的来源桥接起来，用“近期 + 真实互动 + 跨来源印证”回答：

- 最近一个月人们实际上在讨论什么？
- 一个产品的发布节奏与社区评价是否一致？
- 某个人近期在公开账号、GitHub 和视频中做了什么？
- 多个工具的比较是同类竞争，还是位于不同层？
- 某个趋势是否得到多个独立来源支持，还是单点噪声？

## 三个运行层

| 层 | 职责 | 失败时的表现 |
|---|---|---|
| Skill 合约 | 解析用户意图、约束查询计划、决定输出格式与权限交互 | 宿主把它当普通提示词，绕过 Engine 或遗漏必要 flags |
| Python Engine | 采集、归一化、评分、去重、聚类、渲染、缓存、doctor | 来源失败、限流、鉴权缺失、版本或外部 CLI 不兼容 |
| Harness | 提供 WebSearch、Shell、文件和交互能力 | 同一 Skill 在不同宿主上出现安装路径、弹窗和工具能力差异 |

这个结构使 Last30Days 既是软件，也是一个很强的“模型执行协议”；长达两千余行的 `SKILL.md` 本身就是产品行为的一部分。^[inferred]

## 主要模式

- **Named topic**：围绕一个人、项目、公司、概念或新闻主题研究。
- **Comparison**：一次解析多个实体，生成对比视图。
- **Discovery**：无已知主题时先找正在上升的候选话题，并用置信门槛拒绝噪声。
- **Hiring signals**：读取职位页和招聘变化，但要求把结论写成“可能表明”，不能冒充路线图确认。
- **Freshness verification**：对缓存报告中的关键实时数字做再取证，标记 current / stale / contradicted / unsupported。
- **Library / watchlist**：保存跨次研究、全文检索、Atom feed、定时追踪和简报。

## 强项

- 用互动量、评论和跨来源印证补充普通 Web 排名。
- 把“无结果”和“来源没有正常运行”分开，避免把覆盖失败误写成社区沉默。
- 对人和开源项目解析 GitHub 用户/仓库，能把“正在提交什么”与“别人怎么评价”连接起来。
- 输出稳定 JSON、Markdown 和 HTML，并保留原始研究文件供后续审查。
- 对趋势发现设置绝对证据门槛，允许返回“本窗口没有足够强的信号”。

## 限制

- 质量强依赖宿主是否完整遵循长篇 Skill 合约；漏掉实体解析或查询计划，仍可能产生外观合理但覆盖很薄的结果。
- 多数社交平台是封闭花园，需要 cookie、第三方 API、外部 CLI 或本地登录服务；“有适配器”不等于“本次可用”。
- 互动量是注意力信号，不自动等于事实正确或推荐质量；项目在推荐模式中另设 practitioner testimony、专家转向和可测量证据权重来纠正这一点。
- 近 30 天适合追踪变化，不适合代替长期背景、正式文档或系统综述。
- 保存、SQLite、feed 与发布功能扩大了本地数据和外发面，必须先确认写入目录与公开边界。

## 适合放在当前知识库中的位置

Last30Days 可作为 [[skills/Codex学习工作流]] 的“近期舆情与生态证据采集器”，但它不替代官方文档、源码审查和本机验证。更稳妥的组合是：

1. 用 Last30Days 找近期讨论、痛点、使用案例和变化线索。
2. 回到官方文档、release、仓库代码核实关键能力。
3. 把来源声明、本机实验与知识库推断分开记录。
4. 通过 [[concepts/多源时效研究管线]] 保留覆盖状态和反证。

这个定位是根据当前知识库的来源审计规则推导出的使用建议，不是上游官方定位。^[inferred]

## 当前状态

本机尚未安装 Last30Days，也没有运行它的 preflight、setup、doctor 或研究 Engine。当前页面代表对 v3.16.0 固定提交的来源级理解，不代表功能验收。

## Related

- [[references/Last30Days-Skill-GitHub仓库]]
- [[concepts/多源时效研究管线]]
- [[skills/使用-Last30Days-进行近期研究]]
- [[skills/Codex学习工作流]]

