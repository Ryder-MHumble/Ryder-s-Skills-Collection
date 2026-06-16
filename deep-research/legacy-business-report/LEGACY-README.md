# Business Report

> **一句话定位**：从"宽泛关键词"到"麦肯锡风业务研究报告"——一次跑出深度、可追溯、单一 .docx 交付。

---

## 是什么

`business-report` 是一个 Hermes skill，把"市场调研 / 竞品分析 / 行业研究 / 技术趋势"这类宽泛主题，跑成**结构化、可点击信源、单一 .docx 文件**的业务报告。

**核心特征**：

- **5W2H 主动反问**——用户给宽泛关键词时，skill 会先反问 7 个关键点（决策目的 / 受众 / 地域 / 品类 / 时间窗 / 重点维度 / 已有材料）补齐 context，再开始检索
- **麦肯锡风样式**——2 色收敛（深蓝 #1F4E79 + 中性灰 #7F7F7F）、白底 + 蓝头条表格、关键判断用粗体段首、关键数字用粗体大字
- **证据全程可追溯**——每个关键判断有 `evidence_id`、正文中 evidence_id 直接可点击跳转、附录有完整信源透明度报告
- **单一 .docx 交付**——不产生 plan/ledger/sources 等独立文件，全部嵌入 Word 附录 A-D
- **9 章正文 + 4 附录结构**——执行摘要 → 市场概览 → 客户需求 → 玩家分析 → 波特五力 → 市场容量 → 商业模式 → 机会点 → 风险 → 行动路径 → 附录

---

## 案例：外骨骼劳工保护市场调研（2026 H1）

`examples/exoskeleton-report/` 目录下的完整案例。

### 报告页面预览

| 封面 + Banner | 执行摘要 | 玩家深度分析 |
|:---:|:---:|:---:|
| ![cover](assets/page-1-cover.png) | ![exec](assets/page-2-exec-summary.png) | ![players](assets/page-3-players.png) |
| **市场容量测算** | **行动路径** | **附录·信源透明度** |
| ![sizing](assets/page-4-market-sizing.png) | ![action](assets/page-5-action-plan.png) | ![appendix](assets/page-6-appendix.png) |

### 报告核心数据

| 指标 | 数值 | 来源 |
|------|------|------|
| 外骨骼总市场 2025 | $0.56B | MarketsandMarkets |
| 总市场 CAGR 2025-2030 | 29.4% | MarketsandMarkets |
| 医疗子市场 CAGR 2021-2026 | 45% | MarketsandMarkets Medical |
| 美欧 5% 渗透市场空间 | $3.35B – $6.75B | 自测算 |
| 报告独立信源数 | 19（14 已采纳 + 4 备份 + 2 不可达） | — |
| 报告关键判断 | 5 条（每条 ≥ 2 个独立信源交叉验证） | — |
| 最终交付物大小 | 143.1KB | — |

### 报告 9 章正文 + 4 附录结构

| 章节 | 标题 | 核心内容 |
|------|------|----------|
| 摘要 | 执行摘要 | 5 条核心判断 + 1 句核心建议 + 3 个关键数据 |
| 第 1 章 | 市场概览与驱动因素 | 产业定义分类、4 类驱动因素、价值链分析 |
| 第 2 章 | 核心需求与客户画像 | 谁买单三角驱动、4 类客户画像、ROI 测算 |
| 第 3 章 | 主要玩家深度分析 | 6 家第一梯队 + 4 家第二梯队 + 玩家对比矩阵 + 竞争格局 |
| 第 4 章 | 竞争格局：波特五力 | 5 力完整分析 + 整体竞争强度判断 |
| 第 5 章 | 市场容量测算 | 美国 / 欧洲 / 5% 渗透合计 |
| 第 6 章 | 商业模式与定价 | 5 种商业模式 + 定价策略 + 渠道销售 |
| 第 7 章 | 机会点与切入策略 | 产品定位决策树 + 地域切入路径 + 5 个机会点 |
| 第 8 章 | 风险评估 | 技术 / 商业 / 法规 / 竞争 4 类风险 |
| 第 9 章 | 行动建议与下一步 | 短期 0-3 月 / 中期 3-12 月 / 长期 1-3 年 |
| 附录 A | 检索计划 | research_plan.json 表格化 |
| 附录 B | 证据账本 | 30 个 evidence_id 表格化 |
| 附录 C | 信源透明度报告 | 19 个信源的最终采纳情况 |
| 附录 D | 参考来源 | 30 个可点击超链接 URL 列表 |

---

## 快速开始

### 1. 给一个宽泛关键词

```
"工业外骨骼劳工保护市场调研"
"AI Agent 投资判断"
"中国 SaaS 行业研究"
"机器人产业链分析"
```

### 2. Skill 会先反问 5W2H

```
为了把这个调研做到最贴近你真实需求，我需要先对齐几个关键点：

1. 决策目的：投资判断 / 产品立项 / 竞品对比 / 内部汇报 / 兴趣探索
2. 受众与交付物：自己 / 团队 / 领导 / 投资人 / 客户 + 长度预期 + 格式
3. 地域边界：全球 / 中国 / 美国 / 欧洲 / 特定国家
4. 品类/场景边界：工业 To B / 消费 To C / 医疗 / 金融
5. 时间窗：最近 30 天 / 3 个月 / 12 个月 / 3-5 年趋势
6. 重点关注维度：市场容量 / 玩家 / 技术 / 客户 / 商业模式 / 法规 / 投资
7. 已有材料：参考资料 / 报告 / 品牌名单
```

### 3. 跑出 9 章 + 4 附录 .docx

最终交付：`xxx-核心结论-2026-06-10.docx`（约 100-150KB / 400+ 段落 / 25-30 表格 / 30+ 可点击超链接）

---

## 核心能力

### 5W2H 主动反问机制

- 用户给"宽泛主题"或"几个关键词"时，**必须主动反问补齐 5W2H context**
- 7 个反问题覆盖：决策目的 / 受众 / 地域 / 品类 / 时间窗 / 重点维度 / 已有材料
- 避免"形式完整但内容空泛"报告

### 麦肯锡风样式系统

| 元素 | 规范 |
|------|------|
| 主色 | 深蓝 #1F4E79（标题、表头、链接） |
| 辅色 | 中性灰 #7F7F7F（次要文字） |
| 背景 | 纯白 + 浅灰 #F2F2F2（表格交替行） |
| 强调色 | 深红 #C00000（仅关键数字） |
| 字体 | SimSun（中文）+ 无装饰（去 emoj） |
| callout 块 | **不用**（用粗体段首 + 黑色正文） |
| 表格 | 白底 + 蓝头条 + 灰交替行 |
| Banner | matplotlib 渲染深蓝科技感封面图 |

### 证据全程可追溯

- 30 个 `evidence_id`（E01-E30）绑定每个关键判断
- 正文中 evidence_id 直接可点击跳转（不是底部参考列表）
- 附录 B 完整证据账本（Markdown 表格化）
- 附录 C 信源透明度报告（19 个信源最终采纳情况）
- 附录 D 参考来源 URL 列表（30 个可点击）

### 单一 .docx 交付

- 默认输出：单一 `.docx` 文件
- 不产生独立 `plan.json` / `ledger.md` / `sources.csv` / `verified.csv`
- 工作文件放 `/tmp/<项目名>/`，交付后清理
- Obsidian 目录管理：主目录只保留 `.docx` + `.md` 索引；历史归档到 `.archive/`

### 报告标题与文件名分离

- **报告标题**（Word 文档内）：`<主题>深度调研报告：<核心结论> (<窗口期>)`
- **文件名**（文件系统标识）：`<主题中文>-<核心结论简写>-<YYYY-MM-DD>.docx`
- 不含版本号（v1/v2/v3）——迭代在标题内重写而非文件名累积

---

## 完整工作流

| 步骤 | 动作 | 输出 |
|------|------|------|
| 1. 升维确认 | 5W2H 反问补齐 context | 决策目的 / 受众 / 边界 |
| 2. 写检索计划 | research_plan.json（5-12 行） | 计划文档 |
| 3. 选择检索路径 | 6 种场景模版 | 检索任务列表 |
| 4. 建证据账本 | evidence_id (E01+) 全程绑定 | Markdown / CSV / JSONL |
| 5. 验证 source | verify_sources.py（HTTP 200 + 内容命中） | verified_sources.csv |
| 6. 综合与写作 | 9 章正文 + 4 附录（麦肯锡风） | 单一 .docx |
| 7. 交付前审计 | 9 条 checklist | 通过 / 修正 |

---

## 麦肯锡风设计原则（来源：BCG/麦肯锡年报分析）

1. **2 色收敛**——主色深蓝 + 中性灰；不要 3+ 色
2. **白底 + 蓝头条 + 灰交替**——表格干净专业
3. **关键判断用粗体段首**——不用 callout 块/彩色背景
4. **关键数字用粗体大字**——16-18pt 深蓝/黑色
5. **多留白**——段落间距 1.4-1.6
6. **去 emoj / 去 icon / 去色块**——只用文字
7. **MECE 结构**——执行摘要 → 三大议题 → 详细分析 → 启示
8. **数字突出**——粗体 + 大字 + 蓝/黑，不用红色（红色仅用于警示）

---

## 文件结构

```
business-report/
├── SKILL.md                              # Skill 主文档（5W2H 反问 + 9 章工作流）
├── README.md                             # 本文档
├── CHANGELOG.md                          # v2.0.0 → v5.1 演进
├── agents/
│   └── openai.yaml                       # Agent 模型配置
├── assets/
│   ├── banner.png                        # 封面 banner 图
│   ├── page-1-cover.png                  # 报告页面预览（6 张）
│   ├── page-2-exec-summary.png
│   ├── page-3-players.png
│   ├── page-4-market-sizing.png
│   ├── page-5-action-plan.png
│   └── page-6-appendix.png
├── examples/
│   └── exoskeleton-report/               # 完整案例
│       ├── exoskeleton-global-labor-market-2026-06-10.docx
│       ├── research_plan.json
│       ├── evidence_ledger.md
│       ├── sources.csv
│       └── verified_sources.csv
├── references/                           # 14 个 reference 文档
│   ├── deep-research-search-protocol.md
│   ├── word-docx-generation.md
│   ├── source-verification.md
│   ├── research-report-legacy-playbook.md
│   ├── report-deliverable-conventions.md
│   ├── exoskeleton-labor-protection-market.md
│   ├── exoskeleton-industry-china-landscape.md
│   ├── exoskeleton-cross-industry-entrants.md
│   ├── stakeholder-interview-outreach.md
│   ├── two-academy-dashboard-example.md
│   ├── ai-breeding-domain-research.md
│   ├── academic-talent-*.md (3 个)
│   └── ...
├── scripts/
│   ├── generate_report.py                # v5.1 麦肯锡风 .docx 生成器（76KB / 1595 行）
│   └── verify_sources.py                 # URL 可达性 + 内容命中验证
└── templates/
    └── research_report_skeleton.py       # 旧版模板（v2.0.0 兼容）
```

---

## 适用场景

| 场景 | 适用 | 输出 |
|------|------|------|
| 投资判断（VC/PE/二级市场） | ✅ | 9 章 + 市场容量 + 玩家矩阵 + 行动建议 |
| 产品立项（自己/团队做这个方向） | ✅ | 9 章 + 客户需求 + 商业模式 + 切入策略 |
| 竞品对比（已有产品，对标对手） | ✅ | 9 章 + 玩家深度 + 波特五力 + SWOT |
| 内部汇报（给领导/团队看） | ✅ | 9 章 + 关键判断 + 数据支撑 + 行动路径 |
| 兴趣探索（个人了解行业） | ✅ | 简版（5 章）+ 关键数据 + 5 条核心判断 |
| 技术趋势（3-5 年长周期） | ✅ | 9 章 + 驱动因素 + 技术分类 + 演化路径 |
| 学术研究 | 部分适用 | 9 章 + 严格信源 + A 源优先 |

---

## 已知局限

1. **中文网页抓取成功率低**——火墙 / Cloudflare / 验证码普遍（国内 6 家厂商官网 firecrawl 抓取失败）
2. **学术论文原文需 arXiv/openalex 渠道**——单机构跟踪能力有限
3. **价格/客户份额多为训练知识**——精确数据需 ABI Research 等付费报告
4. **Word 生成用 python-docx**——复杂图表/嵌入图表支持有限
5. **证据验证是机械预筛**——`verify_sources.py` 只做 HTTP 200 + 关键词命中，最终 claim 是否成立仍需人工判断
6. **依赖 Firecrawl / archive.org**——主端点余额不足时切备用端点（firecrawl.ihainan.me），不支持 screenshot / actions

---

## 设计决策记录

### 为什么不用 callout 块？

麦肯锡年报分析显示：彩色 callout 块（粉/蓝/绿/红）显得花里胡哨，破坏专业感。改用"粗体段首 + 黑色正文"——视觉层级靠字号和粗细，不用色块。

### 为什么去 emoj？

macOS Word 对 emoj 渲染兼容性差（中文系统不含 emoj glyph，显示为方框）。改用文字（"关键判断："、"建议："、"小结："）—— 信息密度更高、更专业。

### 为什么 evidence_id 放在正文而不是底部？

读者看正文时遇到"80 磅举升"想验证来源时，**直接点击 `[E01]` 即可跳转到 TechCrunch**——不用翻到附录再手动找 URL。提升阅读效率。

### 为什么用单一 .docx 而不是 .md？

| 维度 | Word (python-docx) | Markdown |
|------|-------------------|----------|
| 可编辑性 | ✅ 用户可编辑 | ⚠️ 排版弱 |
| 超链接 | ✅ 可点击 | ✅ 可点击 |
| 复杂表格 | ✅ 底色/对齐/合并 | ⚠️ 需写 HTML |
| 封面/目录 | ✅ 原生支持 | ⚠️ 需 CSS |
| 文件大小 | 50-150KB | 20-50KB |

调研报告要给读者**可编辑**和**直接打印/分享**——Word 是最稳妥的载体。

### 为什么用 matplotlib 渲染 banner？

- matplotlib 跨平台、Python 原生、零依赖（除 numpy）
- 可控的配色、几何元素、文字排版
- 1350x450px PNG 嵌入 Word 不失真
- 渲染快（< 2 秒）

替代方案：WPS/Word/Pages 自动 banner（样式不可控）、SVG（Word 兼容性差）、CSS（无法嵌入 Word）

---

## 反馈与迭代

任何问题、改进建议、新增场景需求，可：
- 直接在 SKILL.md / README.md / CHANGELOG.md 上留言
- 在 `references/` 下追加新场景参考
- 在 `examples/` 下追加新案例
- 在 `assets/` 下更新预览图

---

**版本**：v5.1（2026-06-10）
**作者**：Ryder AI Signal
**许可**：MIT
