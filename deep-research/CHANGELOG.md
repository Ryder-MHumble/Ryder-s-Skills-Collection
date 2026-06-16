# Changelog

`deep-research` skill 的版本演进记录。

---

## v1.3.2（2026-06-11）— 当前版本

**核心改动**：`.docx` 报告默认采用「信息密集型单页首页」（v5.2 首页重构）

### 新增

- **`add_dense_cover(doc, params)`**——`scripts/word_output.py` 新增函数，把封面页从硬编码改为参数化
  - 单页承载：顶部 brand 条 + 主标题 + 副标题 + 英文 + 5 条核心判断 + 4 个关键数据 + 6 项元信息（2 列布局表） + 缩小 Banner 图 + 底部 brand 条
  - 总高度 ≈ 13.6cm < A4 可用 24.7cm，单页所有信息
  - 详见 `references/cover-page-design.md`

- **`references/cover-page-design.md`**——v5.2 信息密集型首页设计参考
  - 设计原则（麦肯锡风 + 单页所有信息）
  - 布局结构图（ASCII）
  - params dict 字段规范
  - 字号 / 颜色 / 间距规范
  - 5 条核心判断的提炼方法
  - 4 个关键数据的选择标准

### 修改

- **`scripts/word_output.py` 封面页**——从硬编码 102 行改为参数化 45 行
  - 旧设计：banner 占 30% + 标题 + 5 行空 + 5 项元信息（**2 页**）
  - 新设计：brand 条 + 标题 + 5 核心判断 + 4 数据 + 6 元信息（2 列布局）+ 缩小 banner（**单页**）
- **`word_output.py` 文件头注释**——v5.1 → v5.2

### 升级方式

下次跑任何 deep-research 报告时，**默认走 v5.2 首页**。需要换报告主题只需改 `build_report()` 中的 `COVER` 字典。

---

## v1.3.1（2026-06-10）



**核心改动**：5 个场景模版 + 9 条 LAWs + 11 个失败模式 + industrial-tob 最高优先级

### 新增

- **5th 场景 `industrial-tob`**——工业硬件 / To B 产品专用模版
  - 详见 `references/scenarios/industrial-tob.md`
  - 含 scenario-fit check + employer-first 结构 + Walmart-style 市场容量测算 + 🔴/🟡/⚪ 数据强度颜色
  - 优先级最高（当 query 同时含"行业 + 产品"时按 industrial-tob 处理）

- **Step 1.5 scenario-fit check**（最高优先级前置检查）
  - 提取目标场景 → 列出场景特征 → 列出删除清单 → 报告开篇"包含/不包含"段 → 后续每家公司/产品先验证
  - 适用：query 含明确目标场景描述时（"劳工保护" / "工业装卸" / "消费级" / "工厂"）

- **LAW 8「结构同质化」**——每章节保持单一视角（市场/雇主 OR 产品/企业）
  - 禁止混合（如"监管章节里夹带公司产品介绍"）
  - 对应工业 To B 报告 3 部分严格分离：① 市场/雇主视角 ② 产品/企业视角 ③ 趋势/不确定项

- **LAW 9「Scenario-fit 强制执行」**
  - 目标场景边界明示 + 后续每家公司/产品先验证
  - 禁止"顺手"加入 query 未要求的场景产品

- **失败模式 10（Scenario scope creep）+ 失败模式 11（数据强度未标色 / 法规章节 auto-expand）**

- **`references/market-sizing-methodology.md`**——Walmart-style 5% 渗透率 × 员工数 × 单价 的市场容量测算方法
  - 独立方法论 + 计算模板 + 风险提示 + 实战教训

- **auto-detection 优先级调整**：`industrial-tob` > competitor > product-deep > tech-trend > industry-market

### 修改

- **`SKILL.md`** 升级到 402 行 / 27.7KB
- **5 个场景模版**（`references/scenarios/*.md`）—— 替换 v1.0 的 4 场景
- **5 个 reference 文档**（`references/source-priority.md` / `source-fetch-fallbacks.md` / `output-formats.md` / `market-sizing-methodology.md` / `derivation-notes.md`）

### 实战验证

外骨骼劳工保护调研（v1.2.0 第二次实战）：

- ✅ 严格执行 scenario-fit check，删除消费级 / 医疗 / 老年外骨骼
- ✅ 工业 To B 报告 3 部分结构严格执行
- ✅ 30 个 evidence_id 全部用 [L?, 日期] 标注
- ✅ 5 条核心判断每条 ≥ 2 个独立信源交叉验证
- ✅ 19 个独立信源（14 已采纳 + 4 备份 + 2 不可达）
- ⚠️ 工业子市场 CAGR 公开摘要未披露（缺口诚实声明）
- ⚠️ 国内 6 家厂商官网 firecrawl 抓取失败（改 L3 兜底）

---

## v1.1.0（2026-06-10）

**核心改动**：LAW 7 实抓 vs 训练知识 + 失败模式 7-9 + 抓取实战经验

### 新增

- **LAW 7「实抓 vs 训练知识」二分类标注**
  - 每条事实必标 `[实抓, YYYY-MM-DD]` 或 `[训练知识, 截止 2025-01]`
  - 严禁把训练知识伪装成实抓
  - 报告开头必须有"数据来源声明"段
  - **为什么要这条 LAW**：Ryder 硬要求"信源权威性"——但 LLM 训练知识截止（2025-01）与实时（2026-06）有 17 个月 gap。**第一次实战证明**：仅靠训练知识会导致"程天科技是外骨骼公司"这种错分类（实抓后发现主营是电动轮椅）

- **失败模式 7：信源抓取失败默默跳过**
  - 显式抓取失败清单
  - 不补训练知识时显式声明
  - 失败率 > 30% 时降级报告

- **失败模式 8：公司状态变更未发现**
  - 抓 news/press/about 兜底
  - 跳转 URL 是关键信号（sarcos.com/news/ → palladyneai.com）

- **失败模式 9：跨场景 query 章节混乱**
  - 主场景优先 + 副线内嵌到主场景第 2 章

- **「实战经验与抓取量控制」section**：
  - sweet spot（5-8 公司 / 8-12 tool call / 30-50K 字符）
  - 国内网站特别说明
  - 跨 skill 协同图

- **详细设计决策记录**（含 Keep/Redesign 决策矩阵 + 普适 forking+redesigning 工作流）见 `references/derivation-notes.md`

- **信源抓取失败模式与 fallback 链**（5 类失败 + 工具对比表 + 信源抓取声明模板）见 `references/source-fetch-fallbacks.md`

### 实战验证

外骨骼劳工保护调研（v1.1.0 第一次实战）：

- 实抓 16 个 URL（firecrawl 备端点）
- 发现 Sarcos 主体业务 2023-12 已并入 Palladyne AI（跳转 URL 证据）
- 程天科技错分类为工业外骨骼 → 实抓后发现主营是电动轮椅
- 国内 6 家厂商官网 firecrawl 抓取失败（Cloudflare/超时/500）→ 改 L3 兜底

---

## v1.0.0（2026-06-10）

**核心改动**：从 last30days-skill 改造初版

### 起源

不复制 last30days 的 50+ vendor 库；只参考它的 plan→多源抓取→聚类→强约束输出架构，按中文企业级调研场景从零设计。

### 4 个场景模版（v1.0）

- `tech-trend`（技术趋势）
- `product-deep`（单产品深度）
- `competitor`（竞品对比）
- `industry-market`（行业市场）

### 6 条 LAWs（v1.0）

- LAW 1：禁幻觉引用
- LAW 2：禁"听说"式表达
- LAW 3：强制时间戳
- LAW 4：禁滥用 ## 小标题
- LAW 5：必标信源置信度
- LAW 6：关键术语必给英文原名

### 5 层信源（L1-L5）

- L1 官方一手（firecrawl + web_extract）
- L2 学术权威（arxiv + openalex + openreview）
- L3 行业权威媒体（36氪/晚点 + TechCrunch/The Verge）
- L4 KOL/Newsletter（kol-interview-to-wiki + blogwatcher）
- L5 社区讨论（xurl + web_extract）

### 3 种交付物

1. 对话中显示（必选）
2. Obsidian Vault 备份（必选）
3. 飞书 wiki 写入（可选 `--feishu`）

### 4 个失败模式（v1.0）

- 失败 1：信源单层依赖
- 失败 2：幻觉引用
- 失败 3：时间漂移
- 失败 4：场景模版被无视

---

## 关键设计决策（跨版本）

| 决策 | 决定 | 原因 |
|------|------|------|
| 默认输出 | Markdown + Obsidian 备份 | 用户常用 Obsidian + 飞书 wiki |
| 可选 .docx 输出 | `scripts/word_output.py`（麦肯锡风） | 满足给领导/投资人看 Word 的需求 |
| 场景模版 | 5 个（v1.0 4 + v1.2 加 industrial-tob） | 工业 To B 是高频且最复杂的场景 |
| LAWs 数量 | 9 条（v1.0 6 + v1.1 加 1 + v1.2 加 2） | 实战中暴露的隐藏幻觉需要强制约束 |
| 信源分层 | L1-L5（不是 A/B/C） | 学术/官方/媒体/社区分层更清晰 |
| 数据强度颜色 | 🔴/🟡/⚪（v1.2 新增） | 读者一眼判断"能不能证明" |
| Scenario-fit check | 最高优先级前置检查 | 防止 scenario scope creep |
| 结构同质化 | LAW 8 强制 | 防止章节视角混乱 |

---

## 配套资产演进

| 资产 | 路径 | 状态 |
|------|------|------|
| 主文档 | `SKILL.md` | 27.7KB / 402 行 / v1.2.0 |
| 案例 | `examples/exoskeleton-report/` | industrial-tob 场景完整案例 |
| 工具脚本 | `scripts/verify_sources.py` | URL 验证 |
| Word 工具（可选）| `scripts/word_output.py` | 麦肯锡风 .docx 渲染器 |
| 截图预览 | `assets/page-*.png` | 6 张麦肯锡风页面预览 |
| 5 个场景模版 | `references/scenarios/*.md` | tech-trend / product-deep / competitor / industry-market / industrial-tob |
| 5 个 reference | `references/*.md` | source-priority / source-fetch-fallbacks / market-sizing-methodology / output-formats / derivation-notes |
| 历史归档 | `legacy-business-report/` | v2.0.0 business-report 改造版（已废弃，作为参考保留） |

---

## 致谢

- last30days-skill（mvanhorn）—— 架构思想来源（plan→多源抓取→聚类→强约束输出）
- phuryn/pm-skills（v2.0.0）—— 跨 skill 协同方法论
- MarketsandMarkets / TechCrunch / IEEE Spectrum / Walmart IR / CYBERDYNE 官网 / DGUV 官网 / OSHA 官网—— 关键信源
- python-docx / matplotlib / Firecrawl / arXiv API / OpenAlex API / xurl—— 工具栈
- Ryder 实战反馈——驱动 v1.1 → v1.2 的 LAW 8 / 9 与失败模式 10 / 11

---

**当前版本**：v1.2.0（2026-06-10）
**下次迭代方向**：
- 解决 firecrawl 备端点余额/超时问题
- 加更多行业场景模版（金融 / 教育 / 医疗）
- 加 PDF 输出标准化（vs 当前 `--pdf` 标志借用 ai-daily-report）
- 加更多数据强度维度的判断（不仅"能不能证明"，还有"时效性"）
