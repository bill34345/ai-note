# AI Note

这是一个以 Obsidian 阅读、链接和审阅，以 Codex 研究与生成内容的 AI 学习知识库。

## 在另一台电脑上使用

1. 安装 Git、Obsidian 和 Codex。
2. 克隆仓库：

   ```powershell
   git clone https://github.com/bill34345/ai-note.git
   cd ai-note
   ```

3. 在 Obsidian 中选择“打开本地仓库”，打开刚克隆的 `ai-note` 文件夹。
4. 如果 Obsidian 询问是否信任此仓库的社区插件，确认后启用 Excalidraw。仓库已包含当前使用的 Excalidraw 插件及配置。
5. 为 Codex 创建本机配置：

   ```powershell
   Copy-Item .env.example .env
   ```

   然后把 `.env` 中的 `OBSIDIAN_VAULT_PATH` 改成这台电脑上的仓库绝对路径。`.env` 不会提交到 GitHub。
6. Obsidian Web Clipper 是浏览器扩展，不属于 vault；每台电脑需要单独安装，并把目标 vault 设为 `ai-note`。

## AI Research Desk

当你要调研、搜索、核实、比较或评分 AI 项目、产品、论文和说法时，可以直接让 Codex 使用 `$ai-research`。它会先在 `_research/<日期>-<主题>/` 建立一份公开可提交的研究包，再把来源、主张、反证、评分和结论分开保存。

也可以从仓库根目录手动初始化：

```powershell
python .agents/skills/ai-research/scripts/init_research_pack.py --topic "Codex-Dream-Skin" --task-type github --question "它是否值得在当前 Windows 环境试用？" --decision-goal "在 Trial、Watch、Reference 或 Reject 中作出可复查判断"
```

完成研究后运行机械校验：

```powershell
python .agents/skills/ai-research/scripts/validate_research_pack.py _research/<研究包目录>
```

校验通过只表示文件结构、证据引用和评分计算一致；Codex 还必须阅读最终结论并抽查来源，做语义验收。研究完成不会自动写入 `_staging/` 或 Wiki。只有你明确批准，并在 `decision.md` 留下批准记录后，才进入单独的 Wiki 晋升流程。详细规则见 `references/research-config.md`。

## 日常同步

开始编辑前：

```powershell
git pull --rebase
```

完成一批笔记后：

```powershell
git add -A
git commit -m "notes: 更新 AI 学习笔记"
git push
```

Git 是版本同步，不是实时协同。不要让两台电脑同时修改同一篇笔记；换电脑前先提交并推送，换到另一台后先拉取。

## 同步范围

会同步：

- Markdown 笔记、来源页、索引和原始剪藏；
- `_research/` 中经过公开清理的研究包与研究索引；
- Excalidraw 图与附件；
- Obsidian 核心插件、社区插件启用清单和 Excalidraw 插件配置；
- LLM Wiki 的公开索引与知识库元数据。

不会同步：

- `.env`：包含每台电脑不同的本地绝对路径；
- `.manifest.json`：LLM Wiki 按本机绝对路径生成的处理状态；
- `.obsidian/workspace*.json`：窗口、标签页和面板布局；
- Obsidian 缓存、回收站以及操作系统临时文件；
- Chrome 扩展自身的设置。
- `_research/` 下的 raw、downloads、cache 和 temp 本地目录。

## 隐私提醒

本仓库是公开仓库。不要在笔记、附件或配置中保存 API Key、密码、私人资料或不适合公开的内容；提交前请检查 `git diff --cached`。
