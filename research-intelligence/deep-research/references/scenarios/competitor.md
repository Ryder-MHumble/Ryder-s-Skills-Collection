# 场景模版：competitor（竞品对比）

## 适用 query 类型

- 「A vs B」「A vs B vs C」「A 和 B 怎么选」
- 「XX 赛道玩家对比」「XX 产品阵营」
- 关键词：对比/比较/vs/versus/区别/差异/选哪个/怎么选/玩家/阵营

## 报告骨架（严格 6 章）

```
## 1. Quick Verdict（一句话选型建议）
## 2. <Entity A>（按 entity 重复）
## 3. <Entity B>
## ...（每个 entity 一章）
## N-1. Head-to-Head 对比矩阵
## N. The Bottom Line（选型决策树 + 不确定项）
```

**章节数 = 实体数 + 3（Quick Verdict + Head-to-Head + Bottom Line）**

注意：实体数过多（≥5）时合并 entity 章节为「主要玩家」+「长尾玩家」两章，保持总章节数 ≤ 7。

## 章节内容指引

### 1. Quick Verdict

- 一句话选型建议（针对典型场景）
- 适用前提（什么场景下这个建议成立）
- 格式：**选型建议** + **适用前提** + **窗口期**

例：
```markdown
**Quick Verdict**：在 2026-Q2 时点，对企业级 LLM API 选型，推荐 **Anthropic Claude 3.7**（长上下文/复杂推理）+ **OpenAI GPT-4o**（多模态/工具调用）的组合，而非单选。

**适用前提**：企业级、需要 Function Calling、预算充足。**不适用**：消费级 C 端、成本敏感型场景。
```

### 2-4. <Entity X>（每个 entity 一章）

每个 entity 章节严格 4 个要素：

```markdown
## 2. Anthropic Claude 3.7

**定位** - Anthropic 的旗舰多模态 LLM，2024-10 发布，定位企业级长上下文与复杂推理。

**核心能力** - 200K 上下文、Computer Use、Artifacts、Tool Use。SWE-bench 62.3% [L1, 2024-10-22]。

**定价** - Input $3/MTok, Output $15/MTok；Batch 5 折 [L1, 2026-04-15]。

**局限** - 中文支持弱 [L5 多源, 2026-04-15]；视觉理解偶有错误 [L3, Stratechery 2026-04-22]。
```

### N-1. Head-to-Head 对比矩阵

**用文字段落呈现，不用 markdown 表格**（便于信源标注和上下文）：

```markdown
**能力维度对比**：

- **长上下文**：Claude 3.7 200K [L1] > GPT-4o 128K [L1] > Gemini 2.0 2M [L1]。Claude 在 100K+ 场景表现最优 [L3, Stratechery 2026-04-22]。

- **Function Calling**：GPT-4o 工具调用最稳 [L5, Reddit r/OpenAI 2026-04-15]；Claude 3.7 Tool Use 在复杂工作流中错误率更高 [L3, 2026-04-20]。

- **多模态**：GPT-4o > Claude 3.7 > Gemini 2.0 > Llama 3.3（图像理解）[L3, 2026-04-25]；视频理解 Gemini 2.0 领先 [L1, 2026-04-15]。

- **价格**：Llama 3.3（自托管） < Gemini 2.0 Flash < Claude 3.5 Haiku < GPT-4o Mini < Claude 3.7 < GPT-4o < Claude 3.7 Opus [L1, 各家定价页 2026-04-15]。

- **中文支持**：Qwen 2.5 > DeepSeek V3 > 智谱 GLM-4 > Llama 3.3 (中文微调) > Claude 3.7 > GPT-4o [L3 多源, 2026-04-15]。国产模型中文明显领先。

- **生态/SDK**：OpenAI 生态最成熟（Assistants API、Fine-tuning、Vector Store）[L1]；Anthropic 生态追赶中 [L3, 2026-04-20]；开源生态 Llama 最丰富。
```

### N. The Bottom Line

- **选型决策树**（按场景给推荐）
- **关键不确定项**（可能影响选型的变量）
- 格式：
  ```markdown
  **选型决策树**：
  - 场景 1：长上下文 + 复杂推理 → Claude 3.7
  - 场景 2：多模态 + 工具调用生态 → GPT-4o
  - 场景 3：成本敏感 + 中文为主 → Qwen 2.5 / DeepSeek V3
  - 场景 4：自托管 + 私有化 → Llama 3.3
  - 场景 5：视频理解 → Gemini 2.0

  **关键不确定项**：
  - Claude 4 发布时间未定 [L3, 2026-04-22] — 可能改变对比格局
  - OpenAI o-series 与 GPT 系列合并策略不明 [L3, 2026-04-25]
  ```

## 信源调度

### L1 必调（每家厂商都要）
- 每家厂商的官网、定价页、文档、博客、GitHub Release
- 每家厂商最近的官方发布/版本更新

### L2 可选
- 各模型相关学术论文（如 Llama、Mistral、DeepSeek 的技术报告）
- OpenAlex 找高引对比工作（如 LMSYS Chatbot Arena Leaderboard 论文）

### L3 必调
- LMSYS Chatbot Arena Leaderboard（公认权威基准）
- 中文：36氪/晚点搜 query 关键词
- 英文：TechCrunch/The Verge/Stratechery/Information 搜 query 关键词

### L4 可选
- KOL 对各家的评价（kol-interview-to-wiki 目录）

### L5 必调
- X 搜各家官方账号 + query 关键词
- Reddit r/LocalLLaMA、r/MachineLearning、r/OpenAI、r/ClaudeAI
- HN 搜 query 关键词

## 强约束自检清单

- [ ] 章节数 = 实体数 + 3（实体 ≥5 时合并为「主要/长尾」2 章）
- [ ] 每个 entity 章节严格 4 要素（定位/能力/定价/局限）
- [ ] Head-to-Head 矩阵用文字段落，不用 markdown 表格
- [ ] 至少 5 个对比维度（能力/价格/中文/生态/速度/可靠性等）
- [ ] Bottom Line 给具体决策树
- [ ] 不确定项明确列出
- [ ] 至少 3 个信源层级（L1+L3 必到）
- [ ] 同一对比维度下所有 entity 都有数据，缺数据时显式标「N/A」
