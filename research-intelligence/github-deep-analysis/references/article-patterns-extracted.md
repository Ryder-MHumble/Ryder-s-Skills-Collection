# 范文手法拆解：可复制的具体模式

基于对 3 篇顶级技术文章的结构化分析，提炼可直接复制的手法。

---

## 1. Jay Alammar — The Illustrated Transformer

### 开头手法
系列回调 + 里程碑框架。不解释"什么是 Transformer"，而是放在技术演进线上：
> "In the previous post, we covered the high-level architecture of the Transformer model. Now we'll look at each component in detail."

**可复制模式**：用"上一篇→本篇"或"过去→现在"的演进线开头，不从头解释概念。

### 章节过渡
几乎不用显式过渡句。每个小标题本身就是一个自然问题（"How do we calculate attention?"），读者自动知道为什么在读这一段。

**可复制模式**：用问句或悬念做小标题，省掉过渡句。

### 列表 vs 叙述
几乎纯叙述 + 图解。极少的列表。信息密度靠**可视化**承载，不是靠文字罗列。

### 引用嵌入
概念名上挂链接，仅在第一次出现时链接。不用"click here"式指引。

### 收尾
没有总结段。在最后一个技术点自然结束，然后一个 forward pointer 指向下一篇。

**可复制模式**：教程型文章不需要刻意收尾，在自然终止点结束 + "接下来可以看..."

---

## 2. Anthropic — Demystifying Evals for AI Agents

### 开头手法
问题验证 + 交付承诺。两段式：
1. 段1：验证痛点存在（"evals are confusing, here's why"）
2. 段2：承诺具体交付物（"we'll share our framework, show how to build evals, and give you a starter kit"）

**可复制模式**：
```
段1：[痛点] 是真实存在的，因为 [原因]。
段2：这篇文章会给你 [3个具体交付物]。
```

### 章节过渡
显式桥接句。每个章节最后一句点明下一章方向：
> "Now that we've defined what to measure, the question becomes how to actually run these evals."

**可复制模式**：每章结尾用一句话预告下章，制造"我还得接着读"的动力。

### 列表 vs 叙述
- 推理过程 → 叙述段
- 平行枚举 → bullet points
- 对比维度 → 表格

**规则**：3 项以内用叙述，4 项以上用列表，2+ 维度对比用表格。

### 引用嵌入
工具名和先前工作上挂链接。方式自然：不是"参考 [1]"，而是"正如 [Anthropic 的工具使用研究](link) 所示"。

### 收尾
三步法：
1. **Distill**：2-3 句话浓缩核心洞察
2. **Look forward**：指出这个方向还没解决的问题
3. **Call to action**：给读者一个"今天就能做"的具体步骤

**可复制模式**：
```
核心洞察：[2句话]
未解决：[1句话指出空白]
行动：[1个具体步骤]
```

---

## 3. Sebastian Raschka — State of LLMs 2025

### 开头手法
范围声明 + 可信度背书。先说"这篇文章覆盖什么、不覆盖什么"，然后给出自己的分析框架。

**可复制模式**：
```
这篇文章覆盖 [范围A+B+C]，不覆盖 [D]。
基于 [方法论]，我的分析框架是 [框架名称]。
```

### 章节过渡
主题桥接。每章最后的观察自然引出下一章主题：
> "The scaling laws predict certain capabilities, but the real question is whether fine-tuning can close the gap cheaper."

**可复制模式**：用"然而"/"但真正的问题是"制造转折，不是用"接下来我们讨论"。

### 列表 vs 叙述
- 纯叙述 + 行内枚举（"three key trends: X, Y, Z"）
- 表格极其多——每一个对比都用表格
- 很少单独的 bullet list

### 引用嵌入
极高密度——每个命名的实体（论文、模型、公司）都挂链接。这是引用密度最高的写法。

### 收尾
预测 + 个人信念声明：
> "My prediction: [具体预测]. I'm [置信度] about this because [理由]."

**可复制模式**：收尾必须有一个**有态度的判断**，不能"前景光明"式空话。

---

## 跨文章共性与可复制规则

| 手法 | Alammar | Anthropic | Raschka | 我的选择 |
|------|---------|-----------|---------|---------|
| 开头 | 演进线 | 痛点+承诺 | 范围+框架 | Anthropic式（痛点+承诺）|
| 过渡 | 问句标题 | 显式桥接 | 主题转折 | 混合：显式桥接+主题转折 |
| 编号 | 无 | 有(1-6) | 有(1-8) | 有，必须编号 |
| 列表 | 极少 | 枚举用 | 极少 | 推理用叙述，平行项用列表 |
| 引用 | 概念名挂链 | 工具名挂链 | 密度极高 | 密度中等，关键论断必须有 |
| 收尾 | 自然终止 | Distill+CTA | 预测+信念 | Anthropic式（Distill+CTA）|
