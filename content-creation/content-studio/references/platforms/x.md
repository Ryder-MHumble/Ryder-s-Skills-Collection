# X (Twitter) 平台方法论

> **核心**：X 有自己的**科技文化 sub-style**，**不是中文翻译成英文**。
> 选 sub-style → 选心理钩子 → 写独狼帖或 Thread。

## 1. 平台调性速查

| 维度 | 数值 |
|------|------|
| 单帖上限 | **280 字符**（Premium 25,000） |
| Thread 长度 | 3-4 条（不要 > 7） |
| 钩子位置 | 1/n **前 10 字符** |
| 视觉资产 | 16:9 首图（建议） |
| 主导心理钩子 | 反认知 / 对比冲击 / 圈层暗号 |
| 调性 | 极简、硬核、hacker 文化、英文优先 |

## 2. 6 种 sub-style（必选 1 种）

X 有 6 种科技风 sub-style，**不许混用超过 2 种**，**不许简单中译英**。

### 2.1 Indie Hacker（@levelsio 风格）

- **适合**：个人开源 / side project / 全栈独立开发者
- **公式**：`Built [工具] that [能力 1], [能力 2], and [能力 3].` + `No [烂大街 1]. No [烂大街 2].` + `Just [核心价值].` + `github.com/...`
- **例子**：
  ```
  Built a CLI that reads your DingTalk chat via `dws`, classifies you into one of 4 archetypes, and outputs a 4:5 identity card.

  No LLM in the loop. No MBTI. No astrology.

  Just behavior → visual identity.

  github.com/Ryder-MHumble/work-selfie
  ```
- **关键**：英文 + 极简 + 工程师文化感 + GitHub 链接必带

### 2.2 Terminal Output（@jxmnop 风格）

- **适合**：CLI / 命令行工具 / 系统级
- **公式**：`$ [tool] [args]` + 输出 + 解释
- **例子**：
  ```
  $ workselfie run --provider dws --days 365
  Loading 12,847 messages...
  Analyzing behavior signals...
  Output: 🟠 glasses thinker

  Reason: "long messages, abstract words, system diagrams in your head"

  Open source. github.com/Ryder-MHumble/work-selfie
  ```
- **关键**：terminal monospace 风格 + 数字具体 + reason 一句到位

### 2.3 Tech Declaration（@swyx 风格）

- **适合**：技术架构 / 性能指标 / 兼容矩阵
- **公式**：一行总述 + `- [metric]: [value]` 列表
- **例子**：
  ```
  Wrote a CLI that maps 12k DingTalk messages → one of 4 archetypes.

  - Provider: dws (DingTalk) / lark-cli (Lark)
  - Avg runtime: 30s for 10k messages
  - LLM in the loop: zero
  - Privacy: default local, no auto-publish

  github.com/Ryder-MHumble/work-selfie
  ```
- **关键**：技术细节硬核 + 数字 + 兼容性矩阵

### 2.4 Hot Take（@bentossell 风格）

- **适合**：反共识 / 行业吐槽
- **公式**：`[Hot take: 争议观点].` + `Built something better.` + 一行解决方案 + 链接
- **例子**：
  ```
  Hot take: MBTI is astrology for engineers.

  Built something better.

  An Agent Skill that reads your actual work traces (DingTalk, Lark) and maps you to one of 4 archetypes based on behavior.

  No LLM in the loop. Open source.

  github.com/Ryder-MHumble/work-selfie
  ```
- **关键**：必须真的"hot"——敢说"X 是垃圾"才有人看

### 2.5 OS Announcement（GitHub release 风格）

- **适合**：项目 launch / 首发 / 版本发布
- **公式**：`Just [open-sourced/launched] [项目名].` + 一段能力描述 + 兼容性 + 链接
- **例子**：
  ```
  Just open-sourced WorkSelfie.

  An Agent Skill that reads your work traces (DingTalk, Lark), maps you to 1 of 4 archetypes based on behavior, and outputs a 4:5 identity card.

  Works with Codex, Claude Code, any agent with local skills.

  github.com/Ryder-MHumble/work-selfie
  ```
- **关键**：中性专业 + launch day / 重大版本时用

### 2.6 One-liner（@paulg 风格）

- **适合**：极简 + 视觉化
- **公式**：`I [动作] that [能力].` + 4-6 个 emoji 列表 + 链接
- **例子**：
  ```
  I built a CLI that reads your DingTalk and tells you which of 4 archetypes you are at work.

  🟠 glasses thinker
  🟢 mood explainer
  🟣 execution engine
  🔵 info radar

  Open source 👇
  github.com/Ryder-MHumble/work-selfie
  ```
- **关键**：视觉强 + 极简 + 列表感

## 3. sub-style 选用决策

| 项目特征 | 选哪个 |
|----------|--------|
| CLI 工具 / 命令行 | Terminal Output |
| 性能 / 架构亮点 | Tech Declaration |
| 个人项目 / side project | Indie Hacker |
| 项目 launch / 重大版本 | OS Announcement |
| 反共识 / 颠覆叙事 | Hot Take |
| 视觉化强（4 个原型这种） | One-liner |
| 拿不准 | Indie Hacker（最安全） |

## 4. 7 大心理钩子在 X 的应用

| 钩子 | 公式 | 例子 |
|------|------|------|
| **痛点共鸣** | 痛点场景 + 具体数字 + 软性 CTA | "Spent 3 years saving the chat group. 12,000+ '收到's. Boss thought I was just replying." |
| **身份贩卖** | 高段位身份 + 揭晓 + 软性 CTA | "The smartest worker in any team is the one who says '收到' the most. 🟠" |
| **反认知震撼** | 我以为 X + 都是错的 + 数字证据 | "I thought I was an INTJ. 3 years of work traces told me I'm a 🟠 systems thinker." |
| **群体认同** | 身份标签 + 共同特征 + 软性 CTA | "Every group has one: the one who always says '收到' but actually runs everything." |
| **对比冲击** | 对比项 + 结果 | "16 MBTI tests: generic. 1 AI reading my work trace: 'system diagrams in your head.'" |
| **圈层暗号** | 圈层黑话 + 揭晓 + 软性 CTA | "12,000 '收到's. 480 meetings. 17 firefights. The 🟠 archetype hits different." |
| **生活方式** | 生活方式 + 软性 CTA | "Want to be the one who 'sees through everything' at work? Read your own work trace." |

## 5. 营销号 listicle（X 上的营销号）

英文 X 圈不像中文那么"震惊体"——营销号在 X 上是 **listicle 风格**：

```
5 things your DingTalk group knows about you that you don't:

1. You're not an INTJ
2. Your "收到"s are not laziness
3. You draw architecture diagrams in your head
4. You're a 🟠 systems thinker
5. 1 year of chat logs can prove it

Open source. github.com/Ryder-MHumble/work-selfie
```

## 6. 1/n 钩子必含 3 选 1

- 心理钩子关键词（"I thought" / "The one who" / "Want to"）
- 数字（"12,000+" / "16"）
- 反转（"An AI read..." / "But actually..."）

## 7. Thread 结构（4 条标准）

```
1/n：心理钩子 + 反转（1 段，1 个核心事实）
2/n：具体数字证据（3-5 个 bullet）
3/n：对号入座清单（3-4 条，让用户"被点名"）
4/n：开放问题 + 软性 CTA
```

## 8. 反模式

- ❌ 自我介绍
- ❌ "首先...其次..."
- ❌ 强推产品
- ❌ emoji 开头
- ❌ Thread > 7 条
- ❌ 呼吁关注
- ❌ tag 堆
- ❌ 写"怎么用"（不是产品文档）
- ❌ **把中文 X 钩子直接翻译成英文**（v3.2 警告：英文 X 文化完全不同）

## 9. 卡片图建议

- **16:9 比例**（1200×675 是 X 推荐）
- **sub-style 视觉匹配**：
  - indie hacker / terminal → Swiss Grid 或 Cyber Neon
  - tech declaration → McKinsey Business
  - hot take → Neo-Brutalism
  - OS announcement → McKinsey Business
  - one-liner → Swiss Grid

## 10. 分析第三方项目的帖子模式

当分享对**别人项目**的深度分析（而非自己的项目 launch）时，帖子策略不同于 OS Announcement：

| 维度 | 自己的项目 | 第三方分析 |
|------|-----------|-----------|
| Sub-style | OS Announcement / Indie Hacker | **Hot Take** |
| 链接 | 必带 GitHub 链接 | **不带链接**（纯观点帖互动更高，算法不降权） |
| 形式 | Thread 4 条（能力→数字→对比→CTA） | **独狼帖优先**（核心观点≤3句时） |
| 钩子 | 圈层暗号 / 对比冲击 | **反认知震撼** |
| KPI | 关注转化 | 点赞/转发 |

**独狼帖模板（分析第三方项目）**：
```
[反认知判断：X 看起来像 Y，但 Z 反转了认知]

[3-5 个数字证据，bullet 或行内]

[一句话可迁移视角]
```

**关键原则**：
- 核心洞察能 3 句说清 → 独狼帖，不要硬撑 Thread
- 不带链接——分享分析观点 ≠ 帮别人引流，纯观点帖在 X 算法里互动率更高
- 机构身份做隐含背书——简介里已有 ZGCI，帖子正文不需要再提"我是XX院的"

## 11. KPI 速查

| 钩子 | 主导 KPI |
|------|----------|
| 痛点共鸣 | 评论 |
| 身份贩卖 | 收藏 |
| 反认知震撼 | 点赞/转发 |
| 群体认同 | 转发 |
| 对比冲击 | 互动（投票） |
| 圈层暗号 | 收藏 |
| 生活方式 | 关注 |
