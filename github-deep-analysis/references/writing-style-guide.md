# 写作风格参考：海外技术深度分析文章的手法拆解

基于对5篇参考文章的结构化分析，提炼可复用的写作模式。

---

## 参考文章列表

1. [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — Jay Alammar
2. [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Anthropic Engineering
3. [The State of LLMs 2025](https://magazine.sebastianraschka.com/p/state-of-llms-2025) — Sebastian Raschka
4. [Scaling Laws for LLMs: From GPT-3 to o3](https://cameronrwolfe.substack.com/p/llm-scaling-laws) — Cameron Wolfe
5. [Which Multi-AI Agent Framework is Best?](https://medium.com/data-science-in-your-pocket/magentic-one-autogen-langgraph-crewai-or-openai-swarm-which-multi-ai-agent-framework-is-best-6629d8bd9509) — Medium

---

## 三种写作范式

### 范式A：工程实操型（Anthropic 风格）

代表作：Anthropic Engineering Blog

开头：问题驱动——以一个实践痛点切入，开篇即点明核心论点
结构：定义→构建→运行→迭代（工程方法论递进）
引用：嵌入式——在叙述中自然插入链接，不阻断阅读流
语气：工程师对话式。"We found that..." / "The key insight is..."。不用数学公式，但用词精准
视觉：代码块为主，高亮框标记关键建议或常见错误，图表较少
收尾：行动号召——给读者"从今天开始做"的具体步骤 + Further Reading

适用于：有明确实操指导意义的分析

### 范式B：领域全景型（Raschka 风格）

代表作：Sebastian Raschka 的年度 LLM 状态报告

开头：时间锚定——"一年前 vs 现在"的对比，列出主题地图让读者各取所需
结构：按技术栈从底到顶排列（基建→训练→后训练→应用→趋势）
引用：学术综述式——每段2-3篇论文引用，点到为止+链接。这是引用密度最高的写法
语气：学术综述+有态度的评论。用"值得注意的是"、"有趣的是"暗示选择性视角。对争议话题给出平衡观点
视觉：图表驱动——对比表格、架构示意图、趋势折线图。信息密度大
收尾：展望式——列未来方向，标注不确定性，不提供行动清单

适用于：需要覆盖大范围、对比多个项目的分析

### 范式C：思想史叙事型（Cameron Wolfe 风格）

代表作：Cameron Wolfe 的 Substack 深度技术文章

开头：叙事钩子——从一个具体历史事件切入，建立"旧认知 vs 新认知"的张力
结构：按认知演进排列——经典理论→颠覆理论→修正理论→新范式。每个章节都是对前一个的"推翻/修正/扩展"
引用：论文精读式——选3-5篇核心论文深度解读，包含公式推导、关键图表复现
语气：学术叙事，自信且权威。像"讲一个知识演进的故事"，每篇论文是一个"角色"
视觉：数学公式+论文图表截图+自制示意图
收尾：理论→实践→前瞻三层收尾，附 Key Takeaways 列表

适用于：需要讲清楚"为什么是这个方向"的深度分析

---

## 五个共性手法（所有范式共享）

### 1. 渐进聚焦结构
从宏观到微观、从定义到实操、从事实到观点，层层递进聚焦。不是上来就给细节，而是先给框架再填内容。

### 2. 锚点+展开写法
每个章节以一个核心概念/论文/事件为锚点，围绕锚点展开分析。锚点是"这一章在讲什么"的快速定位标记。

### 3. 张力驱动叙事
文章不是平铺直叙，而是制造"旧认知 vs 新认知"、"问题 vs 解决方案"的张力。有张力的文章让人想读下去，没张力的文章是流水账。

### 4. 可验证性原则
每个关键论断都有出处，读者可以沿着链接验证。没有出处的论断要明确标注为作者观点。

### 5. 信息密度控制
不是每段同等密度。关键段落高密度（图表/公式/引用），过渡段落低密度（纯叙述）。密度交替制造节奏感。

---

## 用于 GitHub 项目分析的融合策略

三种范式各有适用场景，GitHub 项目分析应该融合使用：

| 章节 | 适用范式 | 原因 |
|------|---------|------|
| 开头钩子 | 范式C（叙事钩子）| 项目都有"创始人为什么做这个"的故事 |
| 项目定位 | 范式A（工程实操）| 快速建立理解 |
| 技术架构 | 范式A + 范式C | 既要有实操细节，也要讲"为什么这样设计" |
| 关键设计决策 | 范式C（思想史）| 每个决策都有"旧做法 vs 新做法"的张力 |
| 亮点与风险 | 范式A（工程实操）| 配对呈现，对比鲜明 |
| 进化脉络 | 范式C（思想史）| 这就是认知演进叙事 |
| 团队与商业 | 范式C（叙事）| 人和商业的故事性 |
| 中国市场 | 范式B（全景扫描）| 多维度快速覆盖 |
| README营销力 | 范式A（实操）| 可学习的具体手法 |
| 升维视角 | 范式B（全景）+ 范式C | 站在高处看赛道演进 |

---

## 参考信源库

写文章时优先使用以下海外信源，避免使用国内转载：

### AI 大厂工程博客
- [Anthropic Engineering](https://www.anthropic.com/engineering)
- [Google DeepMind Blog](https://deepmind.google/blog/)
- [OpenAI Blog](https://openai.com/blog)
- [Meta AI Blog](https://ai.meta.com/blog/)

### 技术深度分析
- [Sebastian Raschka](https://magazine.sebastianraschka.com/) — LLM 状态报告、训练技术
- [Cameron Wolfe](https://cameronrwolfe.substack.com/) — LLM scaling laws、训练优化
- [Jay Alammar](https://jalammar.github.io/) — 可视化技术解读
- [Simon Willison](https://simonwillison.net/) — LLM 工具生态
- [Lilian Weng](https://lilianweng.github.io/) — AI 技术综述

### 投资与行业视角
- [a16z AI coverage](https://a16z.com/ai/) — 投资视角
- [Sequoia Capital](https://www.sequoiacap.com/) — 行业判断
- [Emergence Capital](https://www.emcap.com/) — 企业软件视角

### 学术论文
- [arXiv cs.AI / cs.CL](https://arxiv.org/) — 最新研究
- [Papers With Code](https://paperswithcode.com/) — 带代码的论文

### 社区讨论
- [Hacker News](https://news.ycombinator.com/) — 技术社区反馈
- [Reddit r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) — 本地模型社区
- [Reddit r/MachineLearning](https://www.reddit.com/r/MachineLearning/) — ML 社区
