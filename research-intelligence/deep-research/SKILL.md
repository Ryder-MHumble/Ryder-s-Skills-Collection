---
name: deep-research
version: 1.3.2
description: "【企业级深度调研】基于权威信源分层（官方/学术/行业媒体/KOL/社区），5 类场景模版（技术趋势/产品调研/竞品对比/行业市场/工业硬件To B），输入 query → Step 1.5 scenario-fit check（删除非目标场景产品）→ 自动编排信源抓取 → 按场景模版聚类合并 → 9 条强约束 LAWs 自检（含结构同质化 + scenario-fit）→ 生成结构化中文报告。**默认输出 .docx（麦肯锡风，scripts/word_output.py，单页信息密集型首页 v5.2）+ Markdown 备份到 Obsidian Vault**。工业硬件调研支持 Walmart-style 市场容量测算 + 🔴/🟡/⚪ 数据强度颜色。"
author: Ryder + Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [research, deep-research, tech-trend, product-research, competitor-analysis, industry-market, authoritative-sources, multi-source, chinese]
    related_skills: [arxiv, openalex, openreview, firecrawl, xurl, blogwatcher, kol-interview-to-wiki, ai-daily-report, ocr-and-documents]
prerequisites:
  commands: [python3]
---

# Deep Research — 企业级深度调研

> 不复制 last30days 的 50+ vendor 库；只参考它的 plan→多源抓取→聚类→强约束输出架构，按中文企业级调研场景从零设计。

## 何时使用

- **技术趋势追踪**：「过去 N 天/月/年的 XX 技术演进」「XX 框架最新论文」「XX 路线图」 → `--type tech-trend`
- **单产品深度调研**：「调研一下 XX 产品」「XX 怎么样」「XX 的定价/功能/技术架构」 → `--type product-deep`
- **竞品对比**：「A vs B vs C」「A 和 B 怎么选」「XX 赛道玩家对比」 → `--type competitor`
- **行业市场调研**：「XX 行业格局」「XX 赛道融资/政策」「XX 市场玩家」 → `--type industry-market`
- **工业硬件 / To B 产品调研**：「调研 XX 工业产品」「XX 行业 + XX 产品」「XX 产品 + 目标客户」 → `--type industrial-tob`（**详见 `references/scenarios/industrial-tob.md`**——含 scenario-fit check、employer-first 结构、Walmart-style 市场容量测算、🔴/🟡/⚪ 数据强度颜色）
- **不适合**：
  - 日级快讯（用 ai-daily-report）
  - KOL 访谈内容深挖（用 kol-interview-to-wiki）
  - 短问题快查（直接对话回答即可，不必调 skill）

## 与现有 skills 的关系

| 已有 skill | 定位 | deep-research 与之关系 |
|------------|------|---------------------|
| ai-daily-report | 日级 AI 信号快讯，PDF → 飞书 | **互补**：日报自动推送，调研手动深挖 |
| kol-interview-to-wiki | YouTube KOL 访谈 → 飞书 wiki | **互补**：KOL 观点是 industry-market/tech-trend 的可选信源 |
| arxiv / openalex / openreview | 学术 API 单点查询 | **复用**：作为 deep-research 学术信源层 |
| firecrawl | 网页抓取 | **复用**：作为 deep-research 通用抓取底座 |
| xurl | X/Twitter API | **复用**：作为 deep-research 社区/产品反馈信源 |
| blogwatcher | RSS 博客监控 | **复用**：作为 deep-research 持续追踪信源 |

## 6. 机构署名论文追踪 (Institution Paper Tracking)

不同于上面 5 个**叙事性报告**场景，这是个**结构化数据追踪**工作流——输入"某机构 + 时间窗"，输出按**两院署名论文**模板格式的 xlsx 表格。适合"中关村人工智能研究院 3-6 月发了哪些论文"、"某高校近 90 天 paper 清单"之类的查询。

### 触发场景

- 「查中关村人工智能研究院 3-6 月发了哪些论文」
- 「某高校 / 实验室 / 研究院近 N 月署名论文清单」
- 「两院署名论文追踪」

### 工作流

#### Step 1: 解析用户请求

从 query 提取：
- **机构名**（中英文都给，如"中关村人工智能研究院/Zhongguancun Institute of Artificial Intelligence"）
- **时间窗**：start_date, end_date（默认当月或用户指定）
- **人员分类**：哪些名字是"学生"vs"导师"（用户没说就先标"学生"待 review）

#### Step 2: 三大 API 串行查询（最大化覆盖）

**2a. CrossRef API（PRIMARY——机构匹配最准）**
```
GET https://api.crossref.org/works?query.affiliation={encoded_name}&filter=from-pub-date:{start},{end}&rows=50
```
- `query.affiliation` 直接搜索作者机构字符串，最精确
- 对每条结果遍历 `author[].affiliation[]` 匹配机构名
- 提取：title, DOI, date, author names + affiliations

**2b. OpenAlex API（SUPPLEMENTARY——arXiv 覆盖好）**
```
GET https://api.openalex.org/works?search={encoded_name}&filter=from_publication_date:{start}&per_page=25&sort=publication_date:desc&select=id,title,publication_date,doi
```
- ⚠️ OpenAlex **不支持** `raw_affiliation_string.search` 过滤——只能走 full-text `search`，需要后过滤
- 对每条结果拉详情，校验 `authorships[].raw_affiliation_strings[]` 是否含目标机构关键词
- **Pitfall**：新成立/小型机构（ZIAI、ZA）**没有** OpenAlex institution ID——别依赖 `institutions[].id` 匹配，必须走 `raw_affiliation_strings[]`

**2c. arXiv API（特定作者名已知时）**
```
GET http://export.arxiv.org/api/query?search_query=au:{author_name}&start=0&max_results=50&sortBy=submittedDate&sortOrder=descending
```
- XML 格式，`xml.etree.ElementTree` 解析
- arXiv ID 从 `entry.id` 提取（`http://arxiv.org/abs/2603.20611v1` → `2603.20611`）

#### Step 3: 机构名匹配 + 假阳性过滤

```python
def is_affiliation_match(aff_string, institution_keywords):
    """机构名匹配：所有关键词都必须在 affiliation 字符串里。"""
    aff_lower = aff_string.lower()
    return all(kw.lower() in aff_lower for kw in institution_keywords)
```

**假阳性过滤清单**（这些是地址/不同机构，必须排除）：
- "Zhongguancun East Road" / "Zhongguancun South Street" = **地址**，不是机构
- "Chinese Academy of Sciences, Zhongguancun" = CAS 地址，除非"Zhongguancun Academy"作为机构名出现
- "Zhongguancun Laboratory" = 另一个机构，仅在用户明确要求时包含

#### Step 4: 去重 + 分类 + 生成 xlsx

- 按 DOI 或 arXiv ID 去重
- 分类（学生/导师）根据用户输入或推断，默认"学生"标 flag
- **生成脚本**：`scripts/gen_xlsx.py`（openpyxl）
- **运行方式**：MUST 写到 `/tmp/gen_xlsx.py` 然后 `python3 /tmp/gen_xlsx.py`（hermes sandbox python 可能没 openpyxl，系统 python3 已装）

#### xlsx 模板规范

匹配 `~/Desktop/2026／3月～6月两院署名论文.xlsx`：

| Column | Header | 说明 |
|--------|--------|------|
| A | 人员类型 | "学生" or "导师" |
| B | 姓名 | 中文（无则英文） |
| C | 原高校/机构 | 作者原高校/机构 |
| D | 论文标题 | 完整，不截断 |
| E | 提交日期 | YYYY-MM-DD |
| F | arXiv ID | 2603.20611 形式，无则空 |
| G | arXiv链接 | `https://arxiv.org/abs/{ID}` 形式，无则空 |
| H | 作者列表 | 全部作者用 `; ` 分隔 |

**视觉规范**：
- Header row: `1F4E78` 深蓝底 + 白色加粗
- Freeze pane at `A2`
- 数据行：size 11，无 fill
- Sheet name: 描述性中文
- 排序：人员类型（学生→导师）→提交日期降序
- 列宽：A=8, B=10, C=16, D=55, E=12, F=12, G=35, H=55

#### Pitfalls

1. **OpenAlex institution IDs**：新机构没入库，别用 `institutions[].id` 匹配——走 `raw_affiliation_strings[]`
2. **OpenAlex search 噪声**：full-text `search` 会匹配摘要/地址里提及的论文——必须后过滤 `raw_affiliation_strings`
3. **响应大小**：OpenAlex 完整 authorships 可超 20KB/work——列表查询用 `select=id,title,publication_date,doi`，按 ID 单独拉详情
4. **CrossRef 精度**：`query.affiliation` 最准，但还是要手动过滤（如 "Zhongguancun South Street" 是地址）
5. **日期格式**：OpenAlex 用 `from_publication_date:YYYY-MM-DD`，CrossRef 用 `from-pub-date:YYYY-MM`
6. **中文名**：API 返回基本是英文名；用户给中英对照时按对照表转换
7. **openpyxl 可用性**：hermes sandbox Python 可能没装 openpyxl，**必须**用系统 python3（已装）
8. **arXiv ID 提取**：有些论文有 DOI 但没 arXiv ID——F/G 列只在有 arXiv 数据时填充，否则空

### 复用 deep-research 的脚手架

- **信源分级思路**：和 deep-research 一样，CrossRef (PRIMARY) > OpenAlex (SUPPLEMENTARY) > arXiv (SPECIFIC)
- **多源去重**：DOI/arXiv ID 为主键
- **错误兜底**：见 `references/source-fetch-fallbacks.md`
- **obsidian 输出**：可选的 xlsx 备份到 obsidian vault（用 `obsidian` skill）

---

# 工作流（v1：LLM 直接编排，不依赖 Python 引擎）

## Step 1: 解析 query，确定 4 要素

```yaml
topic: <核心主题，必填>
type: <tech-trend | product-deep | competitor | industry-market | industrial-tob>  # 自动判定或用户指定
window: <时间窗口，默认 90 天；可选 7/30/90/180/365/all>  # 学术和深度调研建议 180+
entities: <涉及的具体实体列表，必填；竞品对比时多个>
target_scenario: <目标场景描述，必填；如"劳工保护"/"工业装卸"/"消费级户外"等>
exclude_categories: <非目标场景产品/品类，列出后自动剔除>
```

**自动判定规则**（用户未指定时按 query 关键词判定）：

| 关键词 | 判定 |
|--------|------|
| 趋势/演进/论文/框架/路线图/综述/技术路线/突破 | `tech-trend` |
| 调研/产品/功能/定价/评测/体验/架构/技术细节 | `product-deep` |
| 对比/比较/vs/versus/区别/差异/选哪个/怎么选 | `competitor` |
| 行业/市场/融资/财报/监管/政策/玩家/格局/赛道 | `industry-market` |
| **工业/工厂/工地/物流/仓储/To B/企业/装配线/装卸/搬运/PPE/安全/介护/劳工/工伤/产线** | **`industrial-tob`**（v1.2 新增）|
| 同时匹配多个 | 优先级：`industrial-tob` > competitor > product-deep > tech-trend > industry-market |

**`industrial-tob` 优先级最高的理由**：当 query 同时含"行业"+ "产品" 时（如"调研外骨骼市场"），按 industrial-tob 处理——先做 employer 视角市场分析 + scenario-fit check + Walmart-style 容量测算，再做产品分析。其他 4 个场景退化为子能力。

用户可在 query 里加 `--type <类型>` 强制指定，覆盖自动判定。

### Step 1.1: 5W2H 主动反问机制（v1.3 新增，**user 给宽泛主题时触发**）

**核心原则**：当用户给"宽泛主题"或"几个关键词"时（如"AI 调研"、"工业外骨骼"、"机器人市场"），**必须主动反问补齐 5W2H context**，再开始检索。这避免跑出"形式完整但内容空泛"的报告。**这是 Ryder 硬性要求**——他要的是"GPT Deep Research 风格的 5W2H 反问"。

**触发条件（任一满足即触发）**：
- 用户 query 只有 1-2 个宽泛词
- 用户没说明决策目的（投资 / 竞品对比 / 产品立项 / 兴趣探索）
- 用户没说明受众（自己 / 团队 / 领导 / 投资人 / 客户）
- 用户没说明地域边界
- 用户没说明时间窗

**反问清单**（7 个核心问题）：

```
为了把这个调研做到最贴近你真实需求，我需要先对齐几个关键点：

1. 决策目的：这份报告主要用途是什么？
   - 投资判断（VC/PE/二级市场）
   - 产品立项（你自己或团队做这个方向）
   - 竞品对比（已有产品，对标对手）
   - 内部汇报（给领导/团队看）
   - 兴趣探索（个人了解行业）
   - 其他：____

2. 受众与交付物：
   - 谁会读这份报告？你自己 / 团队 / 领导 / 投资人 / 客户 / 其他？
   - 报告长度预期：一页纸 / 5-10 页 / 20+ 页深度 / 不限？
   - 输出格式：Markdown（默认 Obsidian 备份）/ Word .docx（麦肯锡风）/ PDF / PPT / 不指定？

3. 地域边界：
   - 全球 / 中国 / 美国 / 欧洲 / 特定国家 / 不限？
   - 是否包含海外市场（如国内看海外机会）？

4. 品类/场景边界：
   - 工业 To B / 消费 To C / 医疗 / 金融 / 教育 / 其他？
   - 包含哪些场景 / 排除哪些场景（如不要消费级、不要医疗康复）？

5. 时间窗：
   - 最近 30 天 / 最近 3 个月 / 最近 12 个月 / 3-5 年趋势 / 不限？

6. 重点关注维度（可多选）：
   - 市场容量与增速 / 主要玩家与竞争格局 / 技术路线与产品对比
   - 客户画像与需求 / 商业模式与定价 / 法规与合规
   - 投资 / 融资 / 并购动态 / 行业进入壁垒与机会点

7. 已有材料（可选）：
   - 你已经有任何参考资料、报告、数据、品牌名单吗？优先作为候选池。

回复后我会基于这些 context 写一份 research_plan.json 并开始检索。
```

**何时不反问（直接动手）**：
- 用户已明确给出 5W2H 中至少 5 项（如"我想做工业外骨骼劳工保护美国市场调研，目的是投资判断，重点看玩家格局和商业模式"）
- 用户在已有报告上追问（如"再深挖一下 German Bionic 的客户案例"）
- 用户要求"快速扫描"或"先给我看一版"（按默认假设走：全球 / 工业 To B / 最近 12 个月 / Markdown 输出）

**反问不是"形式主义"**：反问的目的是让用户参与定义问题。如果用户嫌烦，可以一句话回答（"投资判断、Word、全球、工业 To B、最近 1 年"）就足够。

**反问的最大价值**：避免跑出"形式完整但内容空泛"的报告。Ryder 实战案例：第一次给"AI 调研"这种宽泛词时，**直接动手跑会得到通用综述**（哪类 AI 都讲、哪国都讲、最近 5 年都讲），对决策毫无帮助。

**与 Step 1 自动判定的关系**：Step 1.1（5W2H 反问）→ Step 1 自动判定 → Step 1.5（Scenario-fit check）→ Step 2 加载场景模版。如果 5W2H 反问已明确给出 4 要素，Step 1 自动判定可以加速。

## Step 1.5: Scenario-fit check（v1.2 新增，**最高优先级前置检查**）

**适用场景**：当 query 含明确的目标场景描述时（"劳工保护" / "工业装卸" / "消费级" / "工厂" 等），或 query 同时含 "行业 + 产品" 时，**必须**先做 scenario-fit check 再动笔。

**操作流程**：
1. 从 query 提取**目标场景**（如"劳工保护 / 工业 To B"）
2. 列出该场景的**明确特征**（如：体力密集型 / MSD 高发 / 雇主采购 / 法规驱动）
3. 列出**删除清单**（非目标场景子品类）—— 例：劳工保护场景下删除消费级户外、医疗康复、老年助行、军用外骨骼
4. 报告开篇写"场景边界声明"段（包含 / 不包含）
5. 后续每提到一家公司 / 一款产品，先验证是否在边界内

**典型 query 触发**：
- "调研国内外 XX 工业产品" → target_scenario = 工业
- "XX 行业 + XX 产品"（如"外骨骼市场 + 劳工保护"）→ target_scenario = 劳工保护
- "XX 产品 + 目标客户"（如"外骨骼 + 国外物流公司"）→ target_scenario = 国外物流
- "对比 A 和 B 在 XX 场景" → target_scenario = XX 场景

**对应场景模版**：`references/scenarios/industrial-tob.md`（完整 scenario-fit check 流程 + 删除清单范例）

**违反后果**（按 Ryder 实战反馈）：
- ❌ 把"工业外骨骼"等同于"所有外骨骼" → 错分类
- ❌ 调研中"顺手"加入其他场景产品（消费级 / 医疗） → 报告冗余、读者困惑
- ❌ 自动扩展法规章节到未指定国家 → 噪音

## Step 2: 加载场景模版

按 `--type` 读取 `references/scenarios/<type>.md`，获取：
- 报告骨架（章节顺序、必含要素）
- 信源调度清单（必调/可选/忽略）
- 强约束自检清单

## Step 3: 信源编排抓取（按信源分层顺序）

读取 `references/source-priority.md`，按 5 层信源优先级顺序抓取：

| 层级 | 信源类型 | 调用的现有 tools |
|------|----------|----------------|
| **L1 官方一手** | 公司官网/产品页/技术博客/GitHub Release/官方公告/财报/监管文件 | `firecrawl` + `web_extract` |
| **L2 学术权威** | arXiv 论文、顶会论文、机构智库、OpenAlex 高引工作 | `arxiv` skill + `openalex` skill |
| **L3 行业权威媒体** | 36氪/晚点/虎嗅/财新（中文）；TechCrunch/The Verge/Wired/Stratechery（英文） | `firecrawl` + `blogwatcher`（如已订阅）|
| **L4 KOL/Newsletter** | 已监控的 YouTube KOL、Newsletter、Substack | `kol-interview-to-wiki` 的信源清单 + `blogwatcher` |
| **L5 社区讨论** | X/Reddit/Hacker News | `xurl` + `web_extract` |

**抓取原则**：
- **L1-L3 是核心，必须有数据；缺失时报告必须显式声明「该信源无近期数据」**
- **L4-L5 是补充，用于交叉验证或舆情参考**
- 每个场景模版有具体的"必调/可选/忽略"清单，参见对应模版

**信源标注规则**（在报告中每个事实后用 `[L1]`/`[L2]`/`[L3]`/`[L4]`/`[L5]` 标记）：
```
例：根据 Anthropic 2026-04-15 官方博客 [L1]，Claude 3.7 Sonnet 在 SWE-bench 上得分 62.3%...
例：arXiv 论文 2402.03300 [L2] 提出 GRPO 算法...
```

## Step 4: 聚类合并

LLM 自己做聚类：
- 按主题/时间线/实体分组
- 去重（同一事实出现在多个信源时，优先用 L1 信源表述，其他信源标"印证"）
- 识别时间序列（关键技术节点、产品迭代节点）
- 识别分歧（不同信源对同一事件的矛盾描述，标「冲突：X 信源说 A，Y 信源说 B」）

## Step 5: 按场景模版渲染

每个场景模版定义了：
- 必含章节（不可省略）
- 可选章节（视数据丰富度决定）
- 章节顺序（不可调换）
- 每个章节的内容指引

**严格按模版渲染**——这是 LAW 4 的核心。

## Step 6: 4 条强约束 LAWs 自检

**LAW 1: 禁幻觉引用。** 每个事实必带 URL 或可追溯的 L1-L5 信源标注。无信源的事实在报告里**不存在**。自检：在终稿中搜索「听说」「据传」「有人认为」「普遍认为」「业内观点」等无信源表达，全部删除或补信源。

**LAW 2: 禁"听说"式表达。** 不用「据传」「可能」「有人认为」「普遍认为」「有观点指出」等无信源表达。改用「[L1] Anthropic 2026-04-15 官方博客称……」「[L2] arXiv:2402.03300 提出……」。

**LAW 3: 强制时间戳。** 每个事件必标日期（精确到日）或日期范围。技术节点、论文发布、产品迭代、行业事件都必须有具体时间。无时间戳的"近期""最近""不久前"等模糊表达全部改为具体日期。

**LAW 4: 禁滥用 ## 小标题。** 报告结构服从场景模版，不让模型自由发挥新增 `## 章节`。如果模版说"必含 5 个章节"，报告就严格 5 个，不多不少。每个 `## 章节` 内部用 `**关键判断** - 论述` 的"加粗引领句 + 段落"格式，不在章节内嵌套 `###` 子标题。

**LAW 5: 必标信源置信度。** 每条信源必须标 L1-L5 层级 + 抓取日期（格式 `[L1, 2026-04-15]`）。同一事实被多源印证时，标 `[L1, L3 印证, 2026-04-15]`。

**LAW 6: 关键术语必给英文原名。** 首次出现的产品名/技术名/论文标题/方法名，给中英对照（如「强化学习（Reinforcement Learning, RL）」「模型上下文协议（Model Context Protocol, MCP）」）。学术专有名次首次出现时附 arXiv ID 或论文链接。

**LAW 7: 「实抓 vs 训练知识」二分类标注（v1.1 新增）。** 每条事实必须明确标 `[实抓, YYYY-MM-DD]` 或 `[训练知识, 截止 2025-01]`。**严禁把训练知识伪装成实抓**——这是隐藏的幻觉。具体规则：
- **实抓**：来自 firecrawl/curl/browser 当次抓取的真实网页内容，每条标抓取日期
- **训练知识**：AI 训练知识截止前的公开信息，标 `[训练知识]` 提示用户需二次验证
- **混合**：同一事实既有实抓又有训练知识印证时，标 `[实抓, 训练知识印证]`
- 报告开头必须有"数据来源声明"段，列出本次实抓的 N 条 + 训练知识参考的 M 条

**为什么要这条 LAW**：Ryder 的硬要求是"信源权威性"——但 LLM 训练知识截止时间（2025-01）与实时（2026-06）有 17 个月 gap。如果不强制区分，报告里"我知道的"和"我刚抓的"会被读者当成一回事，而前者可能已经过时（公司被合并、产品线停产、人事变动）。第一次实战（外骨骼调研）证明：仅靠训练知识会导致"程天科技是外骨骼公司"这种错分类（实抓后发现主营是电动轮椅）。

**LAW 8: 结构同质化（v1.2 新增）。** 报告每个 `## 章节` 内部必须保持**单一视角**——要么是"市场/雇主视角"（讲市场容量、法规、玩家格局），要么是"产品/企业视角"（讲公司做什么、产品参数、技术、价格）。**禁止在同一章节里混合两种视角**（如"监管章节里夹带公司产品介绍"）。对应工业 To B 场景，**报告结构**必须是：第一部分（市场/雇主视角，3 章）→ 第二部分（产品/企业视角，1 章）→ 第三部分（趋势/不确定项，2 章）—— 三大部分严格分离。

**为什么要这条 LAW**：Ryder 第一次外骨骼调研反馈："我觉得要不然先讲雇主视角，要不然产品，你应该更加结构化一点，现在太分散了。" 失败模式 #10 详述。**这条 LAW 是 deep-research 报告可读性的核心约束**。

**LAW 9: Scenario-fit 强制执行（v1.2 新增）。** 当 query 含明确目标场景（"劳工保护"/"工业 To B"/"消费级"/"工厂"等）时，**必须**先做 Step 1.5 的 scenario-fit check，并在报告开篇明示"包含 / 不包含"边界。后续**每**提到一家公司或一款产品，先验证其是否在目标场景内——**不在的删除**，不"留个尾巴"。**禁止**"顺手"加入 query 未要求的场景产品（如"劳工保护"加消费级外骨骼 / "工厂"加老年助行）。

**为什么要这条 LAW**：Ryder 第一次外骨骼调研反馈："如果他不需要消费级的产品，就删消费级"——明确要求删除非目标场景产品。**也防止**自动扩展法规章节到未指定国家（法规章节的"auto-expand"也是同一类错误）。这条 LAW 是 query 边界尊重的硬性约束。

**LAW 10: 报告视觉样式约束（v1.3 新增，v1.3.1 强化）。** 报告视觉必须克制、专业、麦肯锡风。**这是 Ryder 硬性要求**——他明确指出过 3 类视觉错误（截图反馈）：

1. **禁用 emoj（包括国别旗 emoj）**：macOS Word 在中文系统下不渲染 emoj glyph（显示为方框 □）。所有"🔴💡📌⭐⚠️🎯"等 emoj 改用文字（"关键判断："、"建议："、"小结："、"注意："）。**v1.3.1 新增**：国别旗 emoj 也属于这一类——`🇺🇸 🇬🇧 🇩🇪 🇫🇷 🇨🇳 🇯🇵 🇰🇷` 全部替换为文字（"美国" / "英国" / "德国" / "法国" / "中国" / "日本" / "韩国"），或带括号形式（"（美国）" / "（中国）"）。**例外**：`references/output-formats.md` 中"数据强度颜色"（🔴/🟡/⚪）允许在 Markdown 报告内使用——但**绝不**用于 .docx 输出。

2. **禁用多色 callout 块**：5+ 色的"粉色/蓝色/绿色/黄色" callout 块（带背景色 + 边框）显得花里胡哨。改用"粗体段首 + 黑色正文"——视觉层级靠字号和粗细，不用色块。如确需突出关键判断，用左侧细蓝/红粗线 + 无背景。

3. **避免"段落紧贴表格"**：表格下方若直接接"关键洞察"等段落，**必须加空行/空段**隔开。Word 默认段落间距太小会导致视觉"贴脸"。

4. **v1.3.1 新增**：报告**不要结尾页**。禁止"报 告 结 束" / "本报告共 N 章 + M 附录" / "Generated by Ryder" 等仪式感段落——报告在最后一个附录自然结束即可。**根因**：仪式感结尾页破坏专业感，麦肯锡/BCG/贝恩咨询报告 90% 没有结尾页。

**色彩收敛（强制 2 色）**：
- 主色：深蓝 `#1F4E79`（标题、表头、超链接）
- 辅色：中性灰 `#7F7F7F`（次要文字、注释）
- 背景：纯白 `#FFFFFF` + 浅灰 `#F2F2F2`（表格交替行）
- **强调色（仅关键数字）**：深红 `#C00000`——只用于最关键数字，不用于 callout 块

**完整样式系统**：详见 `references/mckinsey-style-guide.md`（v5.1 沉淀：2 色配色 + 表格样式 + 章节封面模板 + banner 图渲染）。

**首页设计（v5.2 信息密集型单页）**：详见 `references/cover-page-design.md`——单页承载：顶部 brand 条 + 主标题 + 5 核心判断 + 4 关键数据 + 6 项元信息（2 列布局表） + 缩小 banner + 底部 brand 条，总高度 ≈ 13.6cm。**drop-in 模板**：`templates/cover_params_template.py`（5 场景各 1 套示例值 + 字段填写注释）。

**为什么要这条 LAW**：Ryder 三次截图反馈明确指出——emoj 渲染为方框、多色 callout 显得花、关键洞察紧贴表格。三类问题都来自"装饰过度"和"Word 兼容性"两个根因。这条 LAW 是"克制 > 丰富"原则的硬性约束。

## Step 7: 交付（**默认 3 种输出** + 2 种可选）

**核心原则（v1.3.1 强约束）**：deep-research 是为**对外汇报 / 决策支持**场景设计的——Ryder 反馈过 2 次"为什么没给 Word"和"报告和 word 不一样"。**默认交付 .docx 麦肯锡风报告 + Markdown 索引 + Obsidian 备份**。

详见 `references/output-formats.md` 和 `references/ryder-preferences.md`。

**默认交付物**（每次跑都生成，**不需用户加标志**）：
1. **.docx 麦肯锡风报告**（主交付物）—— 用 `scripts/word_output.py` 渲染，含 banner 图 + 9 章正文 + 4 附录 + 内联超链接 + evidence_id
2. **对话中显示**（必选）—— 报告核心结论 + 关键数据 + 跳转 Obsidian 的指引
3. **Obsidian Vault 备份**（必选）—— 写 1 个 `.md` 索引文件指向 `.docx` 主交付物

**可选交付物**（按需触发）：
4. **Markdown 完整报告源文件**——加 `--with-md` 标志生成完整 `.md` 报告（Obsidian 索引不依赖它），适用场景：用户想在 Obsidian 里全文搜索 Markdown
5. **飞书 wiki 写入**——加 `--feishu` 标志

**用户可在 query 里加的标志**：
- `--type <类型>`：强制场景类型
- `--window <N>`：时间窗口（7/30/90/180/365/all），默认 90
- `--feishu`：额外写入飞书 wiki 子节点
- `--no-obsidian`：跳过 Obsidian 备份
- `--no-docx`：跳过 .docx 输出（仅生成 Markdown），适用场景：用户明确说"我只要 Markdown"
- `--pdf`：额外生成 PDF（用 ai-daily-report 的 Playwright 渲染链路）
- `--with-md`：额外生成完整 Markdown 报告源文件

**`.docx` 主交付物的文件名规范**（v1.3.1 强制）：
- 格式：`<主题中文>DeepResearch报告-<核心结论简写>-<窗口期>.docx`
- 例：`外骨骼劳工保护DeepResearch报告-玩家格局商业模式与切入机会-2026-06-10.docx`
- 例：`AI产品演变DeepResearch报告-玩家格局技术路线与商业化加速-2024-2026.docx`
- **不要**在文件名中加 v1/v2/v3（迭代历史归档到 `.archive/`，主交付物文件名固定）
- **不要**用纯英文文件名或纯 ASCII 简写（中文标题更专业）

**报告标题与文件名分离**（v1.3.1 强约束）：
- 报告内**首页标题** = `<主题> 深度调研报告：<核心结论> (<窗口期>)`（决策导向）
- 报告**文件名** = 机器友好（见上）
- 详见 `references/report-title-conventions.md`

### Step 7.1: Word .docx 输出（v1.3.1+ 默认主交付物）

**v1.3.1 重要变更**：`.docx` 升级为默认主交付物（不需 `--word` 标志），Markdown 降为可选（需 `--with-md` 标志）。新增 `--no-docx` 标志允许用户主动跳过。**根因**：用户 2 次反馈"为什么没给 Word"和"报告和 word 不一样"——`.docx` 不是"可选"是"默认"。

**实现方式**：`scripts/word_output.py`（麦肯锡风 .docx 渲染器，含 `add_dense_cover(doc, params)` 信息密集型单页首页 v5.2 + 9 章正文 + 4 附录结构）。

**触发方法**：
```bash
# v1.3.1+ 默认行为：每次都生成 .docx
"外骨骼劳工保护市场调研"   # 默认输出 .docx（不需任何标志）
"外骨骼劳工保护市场调研 --no-docx"   # 主动跳过 .docx（仅生成 Markdown）
"外骨骼劳工保护市场调研 --with-md"   # 额外生成完整 Markdown 报告源文件
```

**Word 输出特性**（v1.3.2+ 默认行为）：
| 维度 | Markdown（需 `--with-md` 开启）| Word .docx（默认）|
|------|-----------------|-------------------|
| 可编辑性 | ⚠️ 排版弱 | ✅ 用户可编辑 |
| 超链接 | ✅ 可点击 | ✅ 可点击 |
| 复杂表格 | ⚠️ 需写 HTML | ✅ 底色/对齐/合并 |
| 封面（首页 v5.2）| ❌ 无 | ✅ **单页信息密集型**：顶部 brand 条 + 5 核心判断 + 4 数据 + 6 元信息（2 列表格）+ 缩小 banner |
| 章节封面 | ❌ 无 | ✅ 细蓝线 + 章节号 + 标题 |
| 文件大小 | 15-30KB | 60-150KB（含 banner 图）|
| 适用 | Obsidian 笔记 / 自己看 | 给领导/投资人 / 打印分享 |

**首页设计规范（v5.2）**：详见 `references/cover-page-design.md`——单页承载：顶部 brand 条 + 主标题 + 5 核心判断 + 4 关键数据 + 6 项元信息（2 列布局表） + 缩小 banner + 底部 brand 条，总高度 ≈ 13.6cm < A4 可用 24.7cm。**params 模板**：见 `templates/cover_params_template.py`。

**样式系统（麦肯锡风）**：详见 `references/mckinsey-style-guide.md`（v5.1 沉淀的 8 条设计原则 + 2 色配色系统 + 表格样式 + 章节封面模板）。

**重要说明**：Word 输出**不影响**默认 Markdown 流程——只是额外生成。Markdown 报告仍按 v1.2.0 流程走（数据来源声明 + 9 LAWs 自检 + Obsidian 备份）。

## Step 8: 进度透明

每完成一个 Step，主动给用户简短进度：
```
📡 Deep Research 启动
   主题: <topic>
   场景: <type>
   时间窗口: <window>
   必调信源: L1=官网, L2=arXiv×2, L3=36氪
   预计 3-5 分钟
```

抓取过程中如果某个信源失败或数据稀疏，**主动告知**而非默默跳过：
```
⚠️ L1 抓取失败: Anthropic 官网 503；改用 L2 arXiv 论文摘要补全
⚠️ L3 数据稀疏: 36氪近 90 天仅 2 篇相关文章
```

---

# 完整工作流示例

**用户 query**：「帮我调研一下 Anthropic 的 Computer Use 功能过去 90 天的技术演进和竞品对比」

**自动解析**：
```yaml
topic: "Anthropic Computer Use"
type: competitor  # "对比"关键词命中
window: 90
entities: [Anthropic Computer Use, OpenAI Operator, Google Astra, 阿里通义千问]
```

**信源调度**：
1. L1：Anthropic 博客、Anthropic GitHub Release、OpenAI 博客、阿里通义博客
2. L2：arXiv 搜 "computer use" + "GUI agent" + "screen agent" 2025-2026
3. L3：36氪/晚点 LatePost 搜 "Computer Use" + "GUI Agent"
4. L4：kol-interview-to-wiki 已监控 KOL 中近 90 天涉及 Computer Use 的视频
5. L5：X 搜 "computer use" from:AnthropicAI + from:OpenAI（仅作为补充）

**报告骨架**（按 competitor 模版）：
1. Quick Verdict（一句话选型建议）
2. Anthropic Computer Use（技术路线/版本演进/关键能力/局限性）
3. OpenAI Operator（同上）
4. Google Astra（同上）
5. Head-to-Head 对比表（能力/速度/价格/生态/中文支持）
6. The Bottom Line（选型建议 + 不确定项）
7. 完整信源清单（L1-L5 + 抓取日期）

---

# 验证清单

每次 deep research 任务完成后，**自检以下 8 项**：

- [ ] **LAW 1**：报告中每个事实是否都有 [L?] 信源标注 + URL？`grep -E "(听说|据传|有人认为|普遍认为)"` 应返回 0 命中
- [ ] **LAW 2**：报告是否用「[L1] XX 称……」而非「据传」？
- [ ] **LAW 3**：每个事件是否都有具体日期？`grep -E "(近期|最近|不久前|刚刚)"` 应返回 0 命中
- [ ] **LAW 4**：`##` 章节数是否等于场景模版定义？章节内是否只用「加粗引领句 + 段落」？
- [ ] **LAW 5**：每条信源是否标 [L?, 日期]？多源印证是否标 [L1, L3 印证]？
- [ ] **LAW 6**：中英对照是否齐全？arXiv 论文是否附 ID？
- [ ] **信源多样性**：是否覆盖至少 3 个层级（L1+L2+L3 必到）？单层依赖 = 报告无效
- [ ] **交付完整性**：对话显示 + Obsidian 备份 + （可选）飞书 wiki 是否都完成？

---

# 常见失败模式与规避

## 失败 1: 信源单层依赖
**表现**：报告 80% 内容来自 L5 社区讨论（X/Reddit），L1-L3 缺失。
**根因**：LLM 偷懒，只调了最容易抓的信源。
**规避**：Step 3 显式列必调信源清单，每个信源 L1/L2/L3 失败时主动告知而非默默跳过；Step 6 自检"信源多样性"。

## 失败 2: 幻觉引用
**表现**：报告里有看似合理的引用，但 URL 实际指向无关内容或 404。
**根因**：LLM 编造了看似合理的引用。
**规避**：LAW 1 强制每条引用必须有 URL；自检时抽查 2-3 条引用是否真能打开。

## 失败 3: 时间漂移
**表现**：报告里 2024 年的事件被标"近期"或"最新"。
**根因**：LLM 训练数据截止时间与 query 时间窗口不匹配。
**规避**：LAW 3 强制时间戳；Step 3 抓取时**只取 query 窗口内的数据**（窗口外数据标 [L?, 时间超窗] 单独列出）。

## 失败 4: 场景模版被无视
**表现**：用户要 product-deep，LLM 输出成了通用综述。
**根因**：LLM 没读场景模版就动手。
**规避**：Step 2 强制 `read_file references/scenarios/<type>.md`；Step 6 自检"## 章节数 = 模版定义"。

## 失败 5: 模版章节数不对
**表现**：tech-trend 模版说 5 章，报告 7 章。
**根因**：LLM 在 ## 章节里嵌套了 ### 子标题，统计时算成 7 个。
**规避**：LAW 4 禁止章节内嵌套 ###；自检时用 `grep -E "^## " | wc -l` 数 ## 一级章节数。

## 失败 6: 中文报告混英文
**表现**：报告里"Claude 3.7 Sonnet 实现了 agentic reasoning"没有中文翻译。
**根因**：LLM 默认输出英文。
**规避**：LAW 6 强制中英对照；场景模版在 `references/scenarios/*.md` 给出英文术语的中文翻译约定。

## 失败 7: 信源抓取失败默默跳过（v1.1 新增）
**表现**：5 个 L1 公司官网抓取失败（Cloudflare 拦/超时/500/cookie 拦/robots.txt），LLM 默默用训练知识填充"看起来正常"的报告。
**根因**：LLM 偷懒 + 抓取失败时容易回退到训练知识幻觉。
**规避**：
1. **显式抓取失败清单**：在"信源清单"section 显式列出失败的 URL + 失败原因（Cloudflare 拦截/HTTP 500/超时/cookie 拦/robots 拦）
2. **不补训练知识时显式声明**：当训练知识被用作"实抓失败"后的兜底，必须标 `[训练知识]` 而非省略
3. **失败率 > 30% 时降级报告**：如果 L1 失败率超过 30%，不要硬出报告，告知用户改用其他抓取方式（firecrawl 主端点/browser_navigate/curl with cookies）

## 失败 8: 公司状态变更未发现（v1.1 新增）
**表现**：报告里"X 公司"是 2 年前的状态，但实情是 X 已被收购/合并/转型（如 Sarcos → Palladyne AI）。
**根因**：训练知识截止 2025-01，无法反映后续重大变化。
**规避**：
- 当一个公司主页被 Cloudflare 拦、robots 拦时，**优先尝试抓取其 news 页/press 页/about 页/wiki 页**
- 跳转 URL 是关键信号：sarcos.com/news/ 跳到 palladyneai.com → 重大公司变更
- 报告开头用 1-2 句话声明重大变更（如"Sarcos 主体业务已并入 Palladyne AI"）

## 失败 9: 跨场景 query 章节混乱（v1.1 新增）
**表现**：用户 query 同时涉及"市场全景 + 重点企业对比"（如外骨骼调研），LLM 输出 8 章（行业 5 章 + 对比 3 章），违反模版"严格 N 章"。
**根因**：跨场景 query 没有明确的"主+副"分工。
**规避**：
- **主场景优先**：根据 query 主谓宾判定一个主场景（industry-market/competitor/product-deep/tech-trend），其他作为副线
- **副线内嵌到主场景的第 2 章**"市场结构与玩家格局"里，**不单独成章**
- 例：industry-market(主) + 商业模式分析(副) → 第 2 章"市场结构"内含 1 节"商业模式分析"
- 例：competitor(主) + industry-market(副) → 第 1 章 Quick Verdict + 第 5 章 Bottom Line 内嵌行业背景

## 失败 10: Scenario scope creep（v1.2 新增，**工业 To B 场景最高频错误**）
**表现**：用户 query 明确说"劳工保护场景"，LLM 调研中"顺手"加入消费级外骨骼（户外徒步、健身）、医疗康复外骨骼、老年助行外骨骼、军用外骨骼——把"工业外骨骼"等同为"所有外骨骼"，导致报告冗长、读者困惑、不在目标场景的产品被列为"重点企业"。
**根因**：scenario-fit check 缺失；LLM 默认用"上位概念"（如"工业外骨骼"）作为场景边界，把"消费级 / 医疗 / 老年"子品类自动纳入。
**规避**：
- **执行 Step 1.5 scenario-fit check**（**最高优先级前置检查**）
- 报告开篇写"场景边界声明"段：包含 / 不包含
- 后续每提到公司 / 产品，先验证是否在边界
- 参见 `references/scenarios/industrial-tob.md` 的 Step 0 完整流程

**真实案例**：第一次外骨骼调研——"程天科技"被错分类为工业外骨骼公司（实抓后发现主营是电动轮椅）。**如果先做 scenario-fit check，会发现程天的产品线不在目标场景，删除即可**。

## 失败 11: 数据强度未标色 / 法规章节 auto-expand（v1.2 新增）
**表现 A（数据未标色）**：报告结论如"工业外骨骼是外骨骼最大单一细分市场"，但**没有标 🔴/🟡/⚪**——读者无法判断这个判断"能不能证明"。
**表现 B（法规 auto-expand）**：用户说"美国 + 欧洲（英法德）"，LLM 法规章节"顺手"加日本、中国、欧盟其他、加拿大——超过 query 范围。
**根因**：两者都是 query 边界 + 结论强度未做硬性约束。
**规避**：
- **数据强度颜色硬性标**：每条行业判断、数据结论必须标 🔴（多源实抓证实）/ 🟡（单源实抓或训练知识多源）/ ⚪（单源训练知识或推断）
- **法规章节严格按 query 范围**：只写用户明确指定的国家/地区，不"留个尾巴"；未指定时显式询问用户
- 参见 LAW 8（结构同质化）和 LAW 9（Scenario-fit 强制执行）的复合执行

---

# 实战经验与抓取量控制（v1.1 新增）

## Sweet spot

- **公司数量**：5-8 家是 sweet spot。少于 5 覆盖不全；超过 10 个 tool call 容易超时/失败率上升
- **信源分布**：8-12 个 firecrawl 调用（4-6 L1 + 1-2 L2 + 2-3 L3 + 1 L5）
- **总字符量**：30-50K 抓取字符是合适的（够全面但不至于 context 爆炸）
- **并行度**：2-3 批并行抓（每批 4-6 个 URL），避免一次性 10+ 抓导致超时

## 国内网站特别说明

国内公司官网用 firecrawl **备端点**（firecrawl.ihainan.me）抓取成功率明显低于国外站点，常见问题：
- **Cloudflare 拦截**：sarcos.com / palladyneai.com 等
- **HTTP 500**：usbionics.com / mai-bu.com（迈步机器人）等
- **超时**：oymotion.com（傲意智能）等
- **robots 拦**：部分公司 robots.txt 严格

**应对策略**（按优先级）：
1. 试 firecrawl **主端点**（如主端点有余额）
2. 试 firecrawl **备端点**（已默认）
3. 试 **browser_navigate** + browser_console JS 提取（适合 GitHub Trending 那种）
4. 试 **直接 curl** 加 user-agent 头
5. 接受信息缺失，**改用 L3 媒体（36氪/晚点）+ L5 X 搜**作为兜底
6. 在报告中显式标 `[国内 L1 抓取失败, 改用 L3 兜底]`

## 公司状态变更的快速检测

当一个公司 L1 主页抓不到时，按以下顺序试：
1. `https://<公司域名>/news/` 或 `/press/` 或 `/about/`
2. `https://<公司域名>/blog/`
3. 该公司 Wikipedia 页面
4. TechCrunch / Reuters / Bloomberg 搜公司名 + 最近 12 个月
5. SEC EDGAR 搜公司 ticker（如果是美国上市公司）
6. Crunchbase / PitchBook 看公司状态

## 跨 skill 协同图

| deep-research 完成 | 下游用哪个 skill 落地 |
|--------------------|---------------------|
| 技术趋势调研 | pm-skills/product-strategy/skills/tech-trends 或 product-vision |
| 产品/竞品调研 | pm-skills/pm-market-research/skills/competitor-analysis |
| 行业市场调研 | pm-skills/pm-product-strategy/skills/porters-five-forces 或 swot-analysis |
| 单一产品调研 | pm-skills/pm-product-strategy/skills/value-proposition 或 product-strategy |
| 用户/口碑 | pm-skills/pm-market-research/skills/user-personas 或 sentiment-analysis |
| 落地为 PRD | pm-skills/pm-execution/skills/create-prd |
| 落地为 OKR | pm-skills/pm-execution/skills/plan-okrs |
| 长期持续追踪 | blogwatcher（添加 RSS 订阅） |
| 周期性快讯 | ai-daily-report（参考其 GitHub Trending + Product Hunt 抓取链路） |

---

# 调优记录

- **v1.0.0（2026-06-10）**：初版。4 场景 + 5 层信源 + 6 条 LAWs + 3 种输出。基于 last30days 架构思想完全重写（不复制 vendor 库）。
- **v1.1.0（2026-06-10）**：第一次实战（外骨骼市场调研）后迭代。
  - **新增 LAW 7**「实抓 vs 训练知识」二分类标注 —— 防止训练知识幻觉伪装成实抓
  - **新增失败模式 7/8/9**：抓取失败兜底、公司状态变更检测、跨场景 query 章节处理
  - **新增"实战经验与抓取量控制"section**：sweet spot（5-8 公司/8-12 tool call/30-50K 字符）、国内网站特别说明、跨 skill 协同图
  - 详细设计决策记录（含 Keep/Redesign 决策矩阵 + 普适 forking+redesigning 工作流）见 `references/derivation-notes.md`。
  - **信源抓取失败模式与 fallback 链**（5 类失败 + 工具对比表 + 信源抓取声明模板）见 `references/source-fetch-fallbacks.md`。
- **v1.2.0（2026-06-10）**：第二次实战（外骨骼 v2 报告，根据 Ryder 反馈迭代）后升级。
  - **新增 5th 场景 `industrial-tob`**——工业硬件 / To B 产品专用模版，详见 `references/scenarios/industrial-tob.md`（含 scenario-fit check + employer-first 结构 + Walmart-style 市场容量测算 + 🔴/🟡/⚪ 数据强度颜色）。
  - **新增 Step 1.5 scenario-fit check**（最高优先级前置检查）—— 删除非目标场景产品。
  - **新增 LAW 8「结构同质化」**——每章节保持单一视角（市场/雇主 OR 产品/企业），禁止混合；对应工业 To B 报告"第一部分市场+第二部分企业+第三部分趋势"严格分离。
  - **新增 LAW 9「Scenario-fit 强制执行」**——目标场景边界明示 + 后续每家公司/产品先验证。
  - **新增失败模式 10/11**——Scenario scope creep（消费级/医疗/老年被错纳入）+ 数据强度未标色/法规章节 auto-expand。
  - **新增 `references/market-sizing-methodology.md`**——Walmart-style 5% 渗透率 × 员工数 × 单价 的市场容量测算方法（独立方法论 + 计算模板 + 风险提示 + 实战教训）。
  - **auto-detection 优先级调整**：`industrial-tob` > competitor > product-deep > tech-trend > industry-market（当 query 同时含"行业 + 产品"时按 industrial-tob 处理）。
- **v1.3.0（2026-06-11）**：第三次实战（AI 产品演变 tech-trend 报告，根据 Ryder 反馈迭代）。
  - **新增 Step 1.1 5W2H 主动反问机制**——Ryder 硬性要求"GPT Deep Research 风格的 5W2H 反问"。当用户给"宽泛主题"或"几个关键词"时，**必须先反问 7 个核心问题**（决策目的 / 受众交付物 / 地域 / 品类场景 / 时间窗 / 重点维度 / 已有材料），再开始检索。**核心价值**：避免跑出"形式完整但内容空泛"的报告。
  - **新增 Step 7.1 可选 Word 输出**——用户明确要 Word 时（或加 `--word` / `--docx` 标志），用 `scripts/word_output.py`（麦肯锡风 .docx 渲染器，82KB）生成 Word 报告。**不影响**默认 Markdown 流程。
  - **新增 LAW 10 报告视觉样式约束**——3 类 pitfall 硬性约束：① 禁 emoj（macOS Word 渲染为方框）② 禁多色 callout 块（5+ 色显得花）③ 禁"段落紧贴表格"。**根因**：装饰过度 + Word 兼容性。
  - **新增 `references/output-formats.md` 输出 4**——可选 Word .docx 输出的详细规范（特性对比表、触发方式、麦肯锡风样式系统引用）。
  - **新增 `references/mckinsey-style-guide.md`**——v5.1 沉淀的 8 条设计原则 + 2 色配色 + 表格样式 + 章节封面模板 + banner 图渲染 + 5 个 Pitfall + 实战案例引用。
- **v1.3.1（2026-06-11）**：第四次实战（AI 产品演变 .docx 补生成）后强化。**根因**：用户反馈"和刚刚那个报告 word 完全不一样"——根因是默认输出仍是 Markdown，.docx 被标为"可选"。本次强化 3 类硬约束：
  - **.docx 升级为默认主交付物**（不需 `--word` 标志），Markdown 降为可选（需 `--with-md` 标志）。新增 `--no-docx` 标志允许用户主动跳过。
  - **LAW 10 新增 2 条 pitfall**——① 国别旗 emoj（🇺🇸 🇨🇳 等）也属于渲染为方框的 emoj 类，全部替换为文字 ② 报告**不要结尾页**（禁止"报 告 结 束" / "本报告共 N 章" / "Generated by XXX"），在最后一个附录自然结束。
  - **新增 `references/report-title-conventions.md`**——报告标题 vs 文件名 vs Obsidian 索引 3 类区分 + 实战案例（外骨骼 + AI 演变）+ 6 项自检清单。**根因**：AI 主题报告用了纯 ASCII 简写文件名和"调研报告"作为首页标题，与外骨骼报告的麦肯锡风标题格式不一致，触发用户"和 word 不一样"反馈。
  - **Obsidian 目录组织规范**——主目录 1 个 .md 索引 + 1 个 .docx 主交付物，迭代历史归档到 `.archive/` 子目录。**硬性规则**：文件名不带 v1/v2/v3。
- **v1.3.2（2026-06-11）**：第五次实战（首页设计迭代）。**根因**：用户反馈"把所有的信息的排版布局都放在第一页首页上"——旧首页 banner 占 30% + 标题 + 5 行空 + 5 项元信息，总高 ≈ 26cm（**两页**），违反"单页决策导向"。本次强化 1 类硬约束：
  - **首页升级为 v5.2 信息密集型单页设计**——`scripts/word_output.py` 新增 `add_dense_cover(doc, params)` 函数，封面页从硬编码 102 行重构为参数化 45 行（改 `COVER` 字典即可换报告主题）
  - **单页承载结构**：顶部 brand 浅蓝条 + 主标题（28pt 紧凑） + 副标题 + 英文 + 5 条核心判断（紧凑横排） + 4 个关键数据 + 6 项元信息（**2 列布局表**） + 缩小 Banner 图（16cm × 5.3cm） + 底部 brand 浅灰条，总高度 ≈ 13.6cm < A4 可用 24.7cm
  - **新增 `references/cover-page-design.md`**（9.7KB）—— 设计原则 + 布局结构图（ASCII） + params 字段规范 + 字号/颜色/间距规范 + 5 条核心判断提炼方法 + 4 个关键数据选择标准 + 与旧版对比
  - **新增 `templates/cover_params_template.py`**——`COVER` 字典的 drop-in 模板（5 场景各 1 套示例值 + 注释），未来任何 deep-research 报告只需 copy + 改字段即可
  - **覆盖更新 `references/mckinsey-style-guide.md` § 10/11**——把"封面页（banner + 标题 + 元信息）"的旧描述改为引用 v5.2 设计；表格对比更新（"封面 Banner"Markdown 一栏改为 ✅ 顶部 brand 条 + 单页所有信息）
  - **修复 `references/output-formats.md` 内部不一致**——文件开头已声明 .docx 是 v1.3.1 默认主交付物，但 "## 输出 4" 一节仍按"可选 + `--word` 标志"旧描述。统一为 v1.3.1+ 后的口径：`.docx` 是默认 Markdown 之外的并行输出，Markdown 备份需 `--with-md` 标志显式开启
  - **`.docx` 渲染器文件头注释**：v5.1 → v5.2
  - **保留向下兼容**：旧 `add_section_cover` / `add_hr_line` / `add_h2` 等 helper 不变；只是 `build_report()` 内的封面页部分被替换为 `add_dense_cover(doc, COVER)` 调用
