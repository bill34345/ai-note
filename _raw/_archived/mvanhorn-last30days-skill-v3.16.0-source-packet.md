---
title: "mvanhorn/last30days-skill v3.16.0 source packet"
source: "https://github.com/mvanhorn/last30days-skill"
source_type: repository-source-packet
retrieved: 2026-07-16
commit: 249c7a4c040558a903d6838dee31012980d4946d
release: v3.16.0
license: MIT
tags:
  - clippings
  - github
  - agent-skill
  - research
---

# mvanhorn/last30days-skill v3.16.0 source packet

本文件是 2026-07-16 对官方仓库固定提交 `249c7a4c040558a903d6838dee31012980d4946d` 的不可变来源包。采集方式为浅克隆官方 `main`、核对最新 release、读取核心说明与 Skill 规范，并对固定提交中的文件做 SHA-256 校验。它不是对本机安装或运行结果的证明。

## 仓库快照

| 字段 | 值 |
|---|---|
| 仓库 | `mvanhorn/last30days-skill` |
| 固定提交 | `249c7a4c040558a903d6838dee31012980d4946d` |
| tag / package version | `v3.16.0` / `3.16.0` |
| release 发布时间 | `2026-07-16T00:21:39Z` |
| 默认分支 | `main` |
| 许可证 | MIT |
| GitHub 快照 | 52,376 stars；4,579 forks；65 open issues |
| 代码结构快照 | 85 个 Python `lib` 模块；199 个测试文件；3,115 个 `test_*` 函数 |

GitHub 数字是采集时点快照，会继续变化。

## 核心文件与哈希

| 文件 | SHA-256 | 字节数 |
|---|---|---:|
| `README.md` | `6C4F981307007D980487578963D6371D9BEF77072C5067C689A164F606A159E9` | 32,442 |
| `skills/last30days/SKILL.md` | `8043D3BF8426F256E42EEFED085E8A9A8C9F45CDBD7A63530B58493895267668` | 209,798 |
| `CONFIGURATION.md` | `496A05B9A346A36D6A30184542ED19E047FB87923CE24C6C8EEE53ECB49F50CF` | 54,299 |
| `CONCEPTS.md` | `F70A1397FF07FB3385AA9B05EB25B5B022202696E0101F3CD7E79474C4780C78` | 6,315 |
| `docs/how-search-works.md` | `CB3C513EEC67996E88FF88BDBBB43DD3DA4C4472E2CA0CCEF62C71D3FCCA9AF4` | 6,370 |
| `CHANGELOG.md` | `413BC8ACD681EF9163F5E0956A1915C6CF0D93BC207518BFCEA1D4EA54D34AE3` | 97,614 |
| `pyproject.toml` | `E88A0A03CBD05B40A8008F4469DE1725EBC7123C121F60C3E5DA44DDE388F436` | 999 |
| `.codex-plugin/plugin.json` | `255CF67F40EE4E0DAEBADDDD3863CFE8E6C9E14DB5267ED4FDC4663B025791D3` | 1,505 |

## 官方定义的组件

- **Skill**：`SKILL.md` 加同级 `scripts/` 的可分发 Agent Skills 包。
- **Engine**：`scripts/last30days.py` 及 `scripts/lib/`，负责检索、归一化、排序、聚类、渲染、健康检查和本地库。
- **Harness**：加载 Skill 的宿主，包括 Codex、Claude Code、Cursor、Copilot、Gemini CLI 等。
- **Agent contract**：Skill 规范要求宿主先做意图解析、实体/账号/社区解析和查询规划，再调用 Engine；不能用普通网页搜索冒充完整运行。

## 官方定义的研究管线

1. 解析主题类型、时间窗、目标实体和用户意图。
2. 对命名实体解析 X handle、GitHub 用户或仓库、subreddit、TikTok hashtag/creator、Instagram creator 等上下文。
3. 由宿主模型生成 2–4 个查询子计划，或在无宿主搜索能力时使用 `--auto-resolve`。
4. Engine 并行调用可用来源，归一化字段并执行日期过滤、相关性/互动量评分、去重和跨来源聚类。
5. Engine 输出证据簇、来源覆盖状态、固定格式 footer 和原始结果文件；宿主再按 Skill 的输出契约综合。
6. 可选地把结果保存为 Markdown、JSON、HTML、SQLite 趋势库、Atom feed 或本地全文检索库。

## 来源与启用条件

- 无密钥或公开路径：Reddit 公开路径、Hacker News、Polymarket、StockTwits（金融主题）、部分 GitHub 与 keyless web 路径。
- 本地 CLI：`yt-dlp`、`digg-pp-cli`、`arxiv-pp-cli`、`techmeme-pp-cli`、可选 `trustpilot-pp-cli`。
- 凭据或 cookie：X/Twitter、TikTok、Instagram、Threads、Pinterest、LinkedIn、Bluesky、Truth Social、Perplexity 等。
- 请求式本地服务：小红书需要已登录的本地浏览器会话服务，并要求显式选择该来源。
- 本地私有语料：`--corpus` / `LAST30DAYS_CORPUS_DIRS`；官方规范声明默认不把语料结果放进托管发布或稳定 Agent JSON。

## v3.16.0 变更摘要

- YouTube 评论优先由 `yt-dlp` 免费获取，ScrapeCreators 仅作为失败回退。
- `GITHUB_TOKEN` 接入配置、setup 与 doctor 流程。
- 新增可覆盖的逐来源结果上限、`OPENROUTER_BASE_URL` 和更宽容的 MCP timeout 解析。
- 修复 DuckDuckGo 异常拦截时的 keyless web 回退、Reddit 二次抓取失败污染整个 web 来源、Windows/Node 24 Bird 输出、超长主题文件名、空值排序和非 ASCII URL 等问题。

## 权限与数据流摘录

- 默认把研究文件写到 `~/Documents/Last30Days`；Windows 对应用户 Documents 下的 `Last30Days`，可用环境变量或 `--save-dir` 改写。
- `--preflight` 用于在研究前报告配置来源、cookie 计划、计划写入、可选命令和 endpoint override；规范声称它不会读取 cookie 值、写配置/报告或执行研究。
- 首次 setup 必须先获得 cookie 读取许可；不同来源可能把查询发送到 ScrapeCreators、xAI、Xquik、OpenAI、Brave、Perplexity、Polymarket、HN Algolia 等服务。
- `--publish` 才会发布到 `ht-ml.app`；公开是默认发布可见性，密码保护需要另行选择。
- 官方规范要求 API Key 不进入报告输出，但该声明仍需本机运行和文件检查才能验证。

## 官方来源

- [Repository](https://github.com/mvanhorn/last30days-skill)
- [README at fixed commit](https://github.com/mvanhorn/last30days-skill/blob/249c7a4c040558a903d6838dee31012980d4946d/README.md)
- [Runtime SKILL.md at fixed commit](https://github.com/mvanhorn/last30days-skill/blob/249c7a4c040558a903d6838dee31012980d4946d/skills/last30days/SKILL.md)
- [Configuration at fixed commit](https://github.com/mvanhorn/last30days-skill/blob/249c7a4c040558a903d6838dee31012980d4946d/CONFIGURATION.md)
- [How search works](https://github.com/mvanhorn/last30days-skill/blob/249c7a4c040558a903d6838dee31012980d4946d/docs/how-search-works.md)
- [v3.16.0 release](https://github.com/mvanhorn/last30days-skill/releases/tag/v3.16.0)

