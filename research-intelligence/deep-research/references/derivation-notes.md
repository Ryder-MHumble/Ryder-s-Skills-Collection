# 设计决策记录 — deep-research v1.0.0

> 本文档记录 deep-research 的设计来源（从 mvanhorn/last30days-skill fork + redesign）、Keep/Redesign 决策矩阵，以及**普适的 forking + redesigning 外部 skill 工作流**（对未来 fork 其他外部 skill 也有参考价值）。

## 来源

基于 [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill)（38.6k star, 3.1k fork）的**架构思想**完全重写，**不复制 50+ vendor 库文件**。

## 为什么 fork + redesign（不 1:1 安装）

**直接 1:1 安装的代价**：
- Python 3.12+ 引擎 50+ 文件 + 多个付费 API key 依赖（Reddit/X/TikTok），移植成本远超收益
- 8 平台 90% 西方社区（Reddit/X/YouTube/TikTok/HN/Polymarket），与"信源权威性"目标错位
- 8 条 LAWs 锁死"英文社区向"输出格式（badge + What I learned 段落）
- 没有中文场景、中文学术 API、飞书/Obsidian 对接

**deep-research 的目标场景**：企业级中文 deep research（技术趋势 / 产品调研 / 竞品对比 / 行业市场），信源权威性优先。

## Keep / Redesign 矩阵

| 维度 | 保留 | 重写 |
|------|------|------|
| 多源计划 → 抓取 → 聚类 → 渲染管线 | ✅ | |
| 强约束 LAWs 防模型漂移（6 条而非 8 条）| ✅ | ✅ |
| 强制信源标注 + 置信度分级 | ✅ | |
| 引擎输出 pass-through | ✅ | |
| **引擎实现**（Python 50+ vendor 库）| | ✅ LLM 自我编排（Hermes skill 哲学）|
| **信源**（8 西方社区）| | ✅ 5 层（官方/学术/媒体/KOL/社区）|
| **时间窗口**（固定 30 天）| | ✅ 7/30/90/180/365/all 可配 |
| **场景**（单一舆情）| | ✅ 4 类模版自动判定 |
| **输出**（英文 badge 段落）| | ✅ 中文 + Markdown + Obsidian/飞书 wiki |
| **依赖**（付费 API）| | ✅ 复用 Hermes 已有 tools（firecrawl/arxiv/xurl 等）|

---

## 普适参考：Forking + Redesigning 外部 skill 的工作流

> 这部分对未来类似任务（fork 其他外部 agent skill）也有参考价值。

### 决策矩阵：什么时候 fork vs 1:1 迁移

| 信号 | 1:1 迁移 | Fork + Redesign |
|------|---------|-----------------|
| 使用场景与原 skill 完全一致 | ✅ | ❌ |
| 架构值得保留（pipeline + 强约束 + LAWs）| — | ✅ |
| 实现层（信源/输出）不匹配 | ❌ | ✅ |
| 原 skill 依赖重（vendor 库多、付费 API 多）| ❌ | ✅ |
| 运行环境/语言不兼容 | ❌ | ✅ |

**Heuristic**：以下 ≥2 项成立时，fork+redesign 比 1:1 迁移更划算：
1. 实现层 >50% 不匹配
2. 原依赖在你的环境不可用
3. 输出格式不符合你的用户
4. 语言/运行时不适合你的工具链

### 8 步 Fork + Redesign 流程

1. **Survey the original** — 读完整 SKILL.md + 目录结构，识别核心**架构** vs **实现层**
2. **Identify use-case gap** — 原 skill 优化什么 vs 你需要什么；列出 use case 错位的具体维度
3. **Keep / Redesign / Drop matrix** — 显式列出每个组件的去向（保留的架构思想 vs 重写的实现 vs 果断 drop 的 vendor 库）
4. **Survey your existing toolchain** — 哪些现有 skill/tool 可替代 vendor 库（这一步是成本节省的关键）
5. **Draft new SKILL.md** — 按 hermes-agent-skill-authoring 的 peer-matched 结构（Overview / When to Use / 流程 / Pitfalls / Verification）
6. **Validate** — 检查 frontmatter（name ≤64 chars, description ≤1024 chars）、size（peer 推荐 8-14K）、YAML 合法
7. **Test with one real query** — 至少跑 1 个真实 query 验证输出符合预期
8. **Iterate** — 根据第一次跑通的结果调整（信源权重、模版章节数、LAWs 强度）

### 常见 pitfalls

1. **忘了 drop vendor 依赖** — 原 skill 50+ vendor 文件如果"以防万一"留着，会变成臃肿怪物。**Aggressive drop**。`scripts/lib/vendor/` 几乎永远不需要。
2. **原 LAWs 不动** — LAWs 是 voice contract。改了输出格式，LAWs 必须重写，否则模型收到冲突指令，输出会自相矛盾。
3. **新引擎 over-engineering** — Hermes skill 哲学是 **"prompt framework, not code framework"**。能用 markdown 表达就别写 Python 引擎。Python 引擎只在需要确定性批处理时才值得。
4. **无视现有 skills** — 设计信源层前先看 firecrawl/arxiv/xurl/blogwatcher 等是否已有。**复用比重写便宜**。原 skill 的 vendor 库大部分可以被你的现有 toolchain 替代。
5. **不真跑一次就宣告完成** — 设计看着好，第一次真 query 暴露边缘情况（rate limit、API cap、关键词歧义）。**永远至少跑 1 个真实 query 再交付**。

### 复盘：本案例（last30days → deep-research）的关键决策

| 决策点 | 选择 | 备选 | 决定理由 |
|--------|------|------|----------|
| 引擎 | LLM 自我编排 | Python 引擎 | Hermes skill 哲学 + 减少 50+ vendor 移植成本 |
| 信源 | 5 层分层 | 沿用 8 平台 | "信源权威性"是用户的硬要求，必须把官方/学术放最前 |
| 场景模版 | 4 类 | 单一通用模版 | 不同调研场景的输出结构差异大，单一模版无法满足 |
| 输出 | Markdown + Obsidian | 沿用 HTML badge | 与 Ryder KOL 情报习惯一致 + 中文友好 + 可二次编辑 |
| LAWs | 6 条 | 沿用 8 条 | 6 条是必要最小集；超 6 条 LLM 记不住会失效 |
| Cron | v1 不做 | v1 就做 | 调度设计（频率/去重/失败重试/手动-周期冲突）工程量大，先打磨核心质量 |
| 配置文件 | v1 不做 | v1 就做 | 配置文件 + 用户可调会增加 v1 复杂度，等用顺了再加 |

---

## 后续调优方向

- **v1.1**：cron 调度（"每周一自动跑 Agent 赛道调研"，复用 ai-daily-report 的 cron 链路）
- **v1.2**：用户可配置文件（信源权重 + 场景自定 + 关键词黑名单）
- **v1.3**：PDF 导出（`--pdf` 标志，借鉴 ai-daily-report 的 Playwright 渲染引擎）
- **v2.0**：根据真实使用数据重构场景模版（哪些章节常被空着、哪些维度常被追问）
