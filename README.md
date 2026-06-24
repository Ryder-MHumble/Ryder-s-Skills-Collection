# Ryder's Skills Collection

个人 AI Agent 技能库。收录我用着顺手、反复验证过的 skill——有的从开源社区收集改造，有的从零自建。

> **怎么用这个仓库**：按下面的分类找到你需要的 skill → clone 仓库 → 把 skill 目录复制到你的 agent skills 路径（Hermes: `~/.hermes/skills/`，Codex: `~/.codex/skills/`）→ 新 session 自动加载。

---

## 目录结构

```
Ryder-s-Skills-Collection/
├── research-intelligence/     调研与情报（8 个）
├── ZGCI/                      研究院内部技能（3 个）
├── video-motion/              视频与动画（4 个）
├── content-creation/          内容创作（5 个）
├── personal-insights/         自我洞察（1 个）
├── frontend-dev/              前端开发（1 个）
├── README.md                  中文版（本文件）
└── README_EN.md               English version
```

---

## Skill 总览

### research-intelligence/ — 调研与情报

深度调研、开源项目分析、AI 行业情报、KOL 内容挖掘。适合产品经理、研究者、行业分析师。

| Skill | 版本 | 体积 | 一句话 | 适合谁 |
|---|---|---|---|---|
| **deep-research** | 1.3.2 | 1.3MB | 企业级深度调研，5 场景模版 + .docx 麦肯锡风输出 | 需要出调研报告的人 |
| **github-deep-analysis** | 9.0.0 | 102KB | GitHub 开源项目战略分析（不是技术评估，是商业洞察）| 看项目值不值得跟/投/用的人 |
| **aihot** | — | 24KB | AI HOT 中文 AI 综合资讯查询 | 每天跟 AI 动态的人 |
| **aihot-ai-models** | — | 4KB | AI HOT 模型发布/更新情报（OpenAI/Anthropic/Google...）| 跟模型发布的人 |
| **aihot-ai-papers** | — | 4KB | AI HOT 论文研究情报（arXiv/突破/架构...）| 跟学术进展的人 |
| **aihot-ai-products** | — | 4KB | AI HOT 产品发布/更新情报（SaaS/工具/功能...）| 跟产品动态的人 |
| **twitter-ai-kol-fetcher** | — | 38KB | 抓取 Twitter AI KOL 动态 + 识别热门话题 + 生成内参 | 做 AI 行业内参的人 |
| **kol-interview-to-wiki** | 3.0 | 30KB | YouTube KOL 访谈 → 结构化深度分析 → Obsidian wiki | 从 KOL 访谈里挖情报的人 |

### ZGCI/ — 研究院内部技能

中关村人工智能研究院内部工作相关技能。包含成果转化/产孵问答，以及情报引擎 API。

| Skill | 版本 | 体积 | 一句话 | 适合谁 |
|---|---|---|---|---|
| **chanfu-external-qa** | — | 16KB | 成果转化办公室对外创业咨询问答（外部安全口径）| 面向研究员、创业团队、合作方的问题答复 |
| **chanfu-internal-qa** | — | 12KB | 成果转化办公室对内领导问答（项目进展/风险/决策支持）| 内部管理和领导决策支持 |
| **intelligence-engine-api** | — | 104KB | 情报引擎后端 API 查询/导出/排名/可视化 | 用情报引擎做二次开发的人 |

### video-motion/ — 视频与动画

社媒视频制作、视频后处理、视频下载剪辑。适合内容创作者、社媒运营。

| Skill | 版本 | 体积 | 一句话 | 适合谁 |
|---|---|---|---|---|
| **vibe-remotion-animator** | 2.0.0 | 4.0MB | 社媒视频统一入口，7 组件 + Disney 12 原则 + 3 平台规格 | 做抖音/B站/视频号讲解视频的人 |
| **Video-Wrapper-Skills** | — | 89KB | 访谈视频综艺特效（花字/卡片/人物条/章节标题）| 做访谈视频后处理的人 |
| **Youtube-clipper-skill** | — | 100KB | YouTube 智能剪辑 + 双语字幕 + 烧录 + 总结文案 | 从 YouTube 做短视频素材的人 |
| **video-downloader** | — | 2KB | YouTube 等平台视频下载 | 需要下载视频的人 |

### content-creation/ — 内容创作

PPT 生成、社媒 IP 内容、文档配图、文档处理、文本去 AI 味。适合内容生产者。

| Skill | 版本 | 体积 | 一句话 | 适合谁 |
|---|---|---|---|---|
| **NanoBanana-PPT-Skills** | — | 160KB | PPT 画面生成 + 转场视频（风格选择 + 图片生成 + 视频合成）| 做 PPT 的人 |
| **Document-illustrator-skill** | — | 183KB | 文档自动配图（AI 分析结构 + 生成符合风格的配图）| 写文档要配图的人 |
| **content-studio** | — | 6.5MB | 个人社媒 IP 内容工作室（小红书/X/抖音/B站文案 + 图文卡片模板 + 固定专题模板）| 做个人 IP 和社媒内容的人 |
| **document-skills** | — | 2.4MB | 文档处理工具集 | 处理各类文档的人 |
| **Humanizer-zh** | — | 26KB | 中文文本去 AI 痕迹（夸大象征/宣传性语言/三段式...）| 用 AI 写完要润色的人 |

### personal-insights/ — 自我洞察

从工作痕迹中认识自己，趣味与深度并存。

| Skill | 版本 | 体积 | 一句话 | 适合谁 |
|---|---|---|---|---|
| **work-selfie** | — | 27MB | WorkSelfie 职场人格分析 + 野兽派名片（钉钉数据 → 自我分析报告 + PNG 名片）| 想从工作痕迹里认识自己的人 |

### frontend-dev/ — 前端开发

React 组件选择与集成。适合前端开发者。

| Skill | 版本 | 体积 | 一句话 | 适合谁 |
|---|---|---|---|---|
| **react-bits-selector** | — | 21MB | React Bits 动画组件选择/配置/集成（1325 个组件本地目录）| 做 React 前端要加动效的人 |

---

## 怎么选：按场景

| 我要做... | 推荐 Skill |
|---|---|
| 出一份调研报告 | `deep-research` |
| 分析一个 GitHub 开源项目 | `github-deep-analysis` |
| 每天 AI 行业动态 | `aihot`（综合）/ `aihot-ai-models`（模型）/ `aihot-ai-papers`（论文）/ `aihot-ai-products`（产品）|
| 查询/导出情报引擎数据 | `intelligence-engine-api` |
| 做成果转化办公室问答 | `chanfu-external-qa`（对外）/ `chanfu-internal-qa`（对内）|
| 从 KOL 访谈里挖内容 | `kol-interview-to-wiki`（YouTube）+ `twitter-ai-kol-fetcher`（Twitter）|
| 做抖音/B站讲解视频 | `vibe-remotion-animator` |
| 给访谈视频加特效 | `Video-Wrapper-Skills` |
| 从 YouTube 剪短视频 | `Youtube-clipper-skill` |
| 做 PPT | `NanoBanana-PPT-Skills` |
| 做个人 IP 社媒图文 | `content-studio` |
| 给文档配图 | `Document-illustrator-skill` |
| 去掉文本的 AI 味 | `Humanizer-zh` |
| 从工作痕迹认识自己 | `work-selfie` |
| React 项目加动画组件 | `react-bits-selector` |

---

## 安装方式

```bash
# 1. Clone
git clone https://github.com/Ryder-MHumble/Ryder-s-Skills-Collection.git

# 2. 复制你需要的 skill 到 agent skills 目录
# Hermes Agent:
cp -r Ryder-s-Skills-Collection/<category>/<skill-name> ~/.hermes/skills/creative/

# Codex CLI:
cp -r Ryder-s-Skills-Collection/<category>/<skill-name> ~/.codex/skills/

# 3. 新建 session，agent 自动加载
```

> **注意**：部分 skill 含脚本依赖（python3 / node / npm / ffmpeg / puppeteer），具体见各 skill 的 SKILL.md `prerequisites` 字段。

---

## Skill 来源标记

| 标记 | 含义 |
|---|---|
| `author: Ryder + Hermes Agent` | Ryder 自建或深度改造 |
| `author: —` | 从开源社区收集，可能做过适配但未改 author |
| 版本号有 | 经过版本管理（CHANGELOG.md 可查）|
| 版本号 `—` | 单版本，无 CHANGELOG |

---

## 维护规则

- 本地 `~/.hermes/skills/` 为**主版本**，GitHub 仓库为**镜像**
- 升级 skill 时先改本地，再同步到仓库
- 新增 skill 必须归类到对应分类目录
- 路径用环境变量（`$HERMES_HOME` / `$HERMES_OUTPUT`），不硬编码

---

## License

各 skill 独立授权，见各 SKILL.md 的 `license` 字段。未标 license 的默认 MIT。
