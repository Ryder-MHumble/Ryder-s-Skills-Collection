# 样例输出：deep-research 跑完的样子

> **本样例仅展示输出格式**。URL 和日期均为占位（用 `[URL]/[DATE]` 表示），实际跑 deep-research 时会被真实抓取数据填充。

---

**Demo Query**：`调研 Anthropic Computer Use 过去 90 天的技术演进和竞品对比 --type competitor --window 90`

**自动解析**：
- topic: `Anthropic Computer Use`
- type: `competitor`（"对比"关键词命中）
- window: 90 天
- entities: `[Anthropic Computer Use, OpenAI Operator]`

---

## 报告正文（按 competitor 模版，6 章）

```markdown
# Anthropic Computer Use 90 天技术演进 vs OpenAI Operator

## 1. Quick Verdict

**Quick Verdict**：在 2026-Q2 时点，企业级 GUI Agent（图形用户界面智能体）选型，**Anthropic Computer Use** 在工具调用稳定性和企业级 API 完整性上领先；**OpenAI Operator** 在 C 端用户体验和浏览器原生集成上更优。两者尚未形成绝对替代关系，按场景组合使用更合理。

**适用前提**：企业级、API 集成、自动化脚本场景。**不适用**：纯 C 端消费场景、零代码用户。

**窗口期**：YYYY-MM-DD ~ YYYY-MM-DD

## 2. Anthropic Computer Use

**定位** - Anthropic 于 [DATE, L1] 发布的 GUI 操作能力，让 Claude 直接控制桌面/浏览器完成多步任务，定位企业级自动化。

**核心能力** - 多步任务规划、屏幕截图理解、坐标定位、键盘鼠标操作。SWE-bench Verified 得分 62.3% [L1, DATE]。支持 Windows/macOS/Linux 三大桌面系统 [L1, 文档]。

**定价** - 通过 Claude API 调用，按 input/output token 计费；Computer Use 调用单价为普通对话的 1.5x [L1, DATE]。

**局限** - 中文场景识别率低于英文 15% [L3 多源, DATE]；复杂嵌套 UI 偶发误点击 [L5, Reddit r/ClaudeAI DATE]；长任务执行稳定性待提升 [L3, Stratechery DATE]。

## 3. OpenAI Operator

**定位** - OpenAI 于 [DATE, L1] 发布的浏览器原生 Agent，内置于 ChatGPT Pro，定位 C 端用户的网页任务自动化。

**核心能力** - 浏览器内自动化操作、视觉理解、Takeover Mode（关键步骤人工接管）、多任务并行。WebArena 基准 87% [L1, DATE]。

**定价** - ChatGPT Pro 订阅 $200/月 [L1, DATE]；暂未开放独立 API [L1, DATE]。

**局限** - 仅限浏览器场景（不支持桌面应用）[L1, 文档]；API 缺失阻碍企业集成 [L3, DATE]；与 ChatGPT 深度耦合，独立部署困难 [L3, DATE]。

## 4. Head-to-Head 对比

**能力维度对比**：

- **场景覆盖**：Computer Use 桌面+浏览器 > Operator 仅浏览器 [L1, 各家文档 DATE]。
- **任务稳定性**：Computer Use 在长任务（>20 步）场景优于 Operator [L3, 36氪 DATE]；Operator 在 5 步内短任务响应更快 [L3, The Verge DATE]。
- **视觉理解**：双方均基于自研多模态大模型，差距不显著 [L3, Stratechery DATE]。
- **价格**：Computer Use 按 token 计费（重度使用约 $50-200/月）vs Operator 固定 $200/月 [L1, DATE]。轻度使用 Operator 更便宜，重度使用 Computer Use 灵活。
- **生态集成**：Computer Use 开放 API + Claude Agent SDK [L1, DATE]；Operator 暂无独立 API，集成困难 [L3, DATE]。
- **中文支持**：Computer Use 弱于 Operator（均弱，但 Operator 略好）[L5 多源, DATE]。

**典型场景选型**：
- 企业 SaaS 自动化、桌面应用脚本化 → Computer Use
- C 端用户网页任务（订票、购物、表单）→ Operator
- 多任务并行批处理 → Operator
- 复杂长链路工作流 → Computer Use

## 5. The Bottom Line

**选型决策树**：
- 场景 A：企业内部自动化、桌面/浏览器混合、需要 API → **Computer Use**
- 场景 B：消费级网页任务、预算固定、不需要集成 → **Operator**
- 场景 C：研究/实验用途、两个都要试 → 都用，按需切换

**关键不确定项**：
- Operator 何时开放独立 API [L3, DATE] — 改变企业选型格局
- Computer Use 中文能力提升计划 [L3, DATE] — 影响国内企业
- 两家是否会互相渗透（Computer Use 进 C 端 / Operator 进企业）[L3, DATE]

## 6. 信源清单

### L1 官方一手（4 条）
- Anthropic Blog (Computer Use 发布): [URL] (抓取于 DATE)
- Anthropic Docs (Computer Use API): [URL] (抓取于 DATE)
- OpenAI Blog (Operator 发布): [URL] (抓取于 DATE)
- OpenAI Help Center (Operator 文档): [URL] (抓取于 DATE)

### L2 学术权威（2 条）
- arXiv:XXXX.XXXXX (GUI Agent Survey): [URL] (抓取于 DATE)
- arXiv:XXXX.XXXXX (Computer Use Benchmark): [URL] (抓取于 DATE)

### L3 行业媒体（3 条）
- 36氪: [URL] (抓取于 DATE)
- Stratechery: [URL] (抓取于 DATE)
- The Verge: [URL] (抓取于 DATE)

### L4 KOL（1 条）
- KOL情报/<KOL名>- <视频标题>.md: Obsidian 路径 (抓取于 DATE)

### L5 社区（2 条）
- Reddit r/ClaudeAI: [URL] (抓取于 DATE)
- X @AnthropicAI: [URL] (抓取于 DATE)
```

---

## 6 条 LAWs 自检结果（自检表）

| LAW | 检查项 | 实际 | 结果 |
|-----|--------|------|------|
| LAW 1 | 禁幻觉引用 - 每条事实有 [L?] + URL | ✅ 全部信源已标 | PASS |
| LAW 2 | 禁"听说"式表达 - 无"据传"/"有观点认为" | ✅ 全文用 [L?] 来源标注 | PASS |
| LAW 3 | 强制时间戳 - 每事件有具体日期 | ✅ 全部事件标 DATE | PASS |
| LAW 4 | 禁滥用 ## - 章节数 = 模版定义 | ✅ 6 章 = 3 (entities) + 3 (Verdict/H2H/Bottom) | PASS |
| LAW 5 | 必标信源置信度 - 每条 [L?, 日期] | ✅ 全部 [L?, DATE] 标注 | PASS |
| LAW 6 | 关键术语中英对照 | ✅ Computer Use / GUI Agent / SWE-bench 均给中英 | PASS |

---

## Obsidian 备份后的 frontmatter

```yaml
---
title: "Anthropic Computer Use 90 天技术演进 vs OpenAI Operator"
type: competitor
generated: YYYY-MM-DD
window: 90 天
tags:
  - 深度调研
  - 竞品对比
sources_count:
  L1: 4
  L2: 2
  L3: 3
  L4: 1
  L5: 2
---
```

**Obsidian 路径**：`~/Documents/Obsidian Vault/深度调研/anthropic-computer-use-vs-openai-operator-YYYY-MM-DD.md`

---

## 关键设计决策回顾

| 维度 | 选择 | 理由 |
|------|------|------|
| 引擎 | LLM 自我编排（无 Python 引擎） | 避免 last30days 50+ vendor 库成本；Hermes skill 哲学 |
| 信源 | 5 层分层，官方/学术优先 | 符合 Ryder "信源权威性" 核心需求 |
| 场景 | 4 类模版（tech-trend/product-deep/competitor/industry-market） | 覆盖技术趋势/产品调研/竞品对比/行业市场四类核心需求 |
| 输出 | Markdown + Obsidian 默认，飞书 wiki 可选 | 与 Ryder 现有 KOL 情报习惯一致；与 ai-daily-report 互补 |
| LAWs | 6 条强约束（禁幻觉/禁听说/强制时间戳/禁小标题滥用/标置信度/中英对照） | 学 last30days 但适配中文+权威场景 |
| Cron | v1 不做，v2 留接口 | 先验证 skill 质量，再加调度 |
