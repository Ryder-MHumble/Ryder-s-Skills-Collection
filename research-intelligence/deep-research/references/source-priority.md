# 信源优先级与编排规则

## 5 层信源分层

| 层级 | 类型 | 调用的现有 tool | 典型来源 | 抓取成本 |
|------|------|---------------|---------|---------|
| **L1 官方一手** | 公司官网、产品页、定价页、技术博客、官方公告、GitHub Release、官方文档、监管文件、SEC 财报、官方白皮书 | `firecrawl` + `web_extract` | anthropic.com, openai.com, blog.google, 36kr.com/information/... | 高（需逐 URL 抓）|
| **L2 学术权威** | arXiv 论文、顶会论文（NeurIPS/ICML/ICLR/CVPR/ACL/CHI/UIST/CHI）、OpenAlex 高引工作、机构智库报告 | `arxiv` skill + `openalex` skill | arxiv.org, openalex.org, distill.pub, 各高校/智库 | 中（API 查询）|
| **L3 行业权威媒体** | 中文：36氪/晚点 LatePost/虎嗅/财新/钛媒体；英文：TechCrunch/The Verge/Wired/Stratechery/Casey Newton Platformer | `firecrawl` + `blogwatcher`（如已订阅）| 36kr.com, latpost.com, huxiu.com, techcrunch.com, theverge.com | 中（站点抓取）|
| **L4 KOL/Newsletter** | 已监控的 YouTube KOL、Newsletter、Substack | `kol-interview-to-wiki` 信源清单 + `blogwatcher` | 用户 Vault/KOL情报 目录 | 低（已扫描）|
| **L5 社区讨论** | X/Reddit/Hacker News/知乎/即刻 | `xurl` + `web_extract` | twitter.com, reddit.com, news.ycombinator.com, zhihu.com | 中（API 限流）|

## 抓取原则

### 必调与可选（按场景）

| 场景 | L1 必调 | L2 必调 | L3 必调 | L4 可选 | L5 可选 |
|------|--------|--------|--------|--------|--------|
| **tech-trend** | 关键技术领导方官方博客/论文 | ✅ 必调（核心）| ✅ 必调 | KOL 观点 | 社区讨论 |
| **product-deep** | ✅ 必调（核心）| 可选（看技术深度）| ✅ 必调 | 可选 | 评测/反馈 |
| **competitor** | ✅ 必调（每家都要）| 学术论文（看技术）| ✅ 必调 | KOL 评测 | 社区选型讨论 |
| **industry-market** | ✅ 必调（监管/财报/公告）| 智库报告 | ✅ 必调 | KOL 行业观点 | 社区舆情 |

### 缺数据处理

| 情况 | 处理 |
|------|------|
| L1 某官方源 404/403/超时 | 尝试 archive.org / Google Cache / 改用 L2 论文 |
| L1 全部失败 | **主动告知用户**，降级到 L2+L3+ 显式标 `[L1 缺失, 用 L2/L3 替代]` |
| L2 arXiv 无相关论文 | 扩大关键词；用 Semantic Scholar 搜；用 OpenAlex 找高引 |
| L3 某站点无内容 | 改用其他行业媒体；用 Firecrawl 搜同主题 |
| L4 KOL 列表无相关内容 | 跳过 L4，不强求 |
| L5 全部缺失 | 不影响报告有效性，L5 是补充 |

### 跨源印证规则

- 同一事实出现 2+ 信源印证时：主陈述用最高优先级信源（L1 > L2 > L3 > L4 > L5），标 `[L1, L3 印证, 2026-04-15]`
- 同一事实出现矛盾描述时：标「**冲突**：[L1, Anthropic 2026-04-15] 称 A；[L3, 36氪 2026-04-12] 称 B」，不擅自选边
- 单一信源孤证：标 `[L3 单源, 2026-04-15]`，在「不确定项」section 单列

## 信源标注格式

### 在报告正文里

```markdown
- 根据 Anthropic 2026-04-15 官方博客 [L1, 2026-04-15]，Claude 3.7 Sonnet 在 SWE-bench 上得分 62.3%。
- arXiv 论文 2402.03300 [L2, 2024-02-05] 提出 GRPO 算法，Hugging Face 团队 [L3, 2024-02-20] 跟进实现。
- 36氪 2026-04-10 报道 [L3, 2026-04-10] 称国内某厂商已上线 Computer Use 类功能。
```

### 在信源清单 section 里（报告末尾）

```markdown
## 信源清单

### L1 官方一手（5 条）
- Anthropic Blog: https://www.anthropic.com/news/... (抓取于 2026-04-15)
- OpenAI Blog: https://openai.com/blog/... (抓取于 2026-04-15)
- GitHub Release: https://github.com/.../releases/tag/... (抓取于 2026-04-15)
...

### L2 学术权威（3 条）
- arXiv:2402.03300: https://arxiv.org/abs/2402.03300 (抓取于 2026-04-15)
- arXiv:2501.12345: https://arxiv.org/abs/2501.12345 (抓取于 2026-04-15)
- OpenAlex W2741809807: https://openalex.org/W2741809807 (抓取于 2026-04-15)
...

### L3 行业媒体（4 条）
- 36氪: https://36kr.com/... (抓取于 2026-04-15)
- 晚点 LatePost: https://latpost.com/... (抓取于 2026-04-15)
...

### L4 KOL（2 条）
- KOL情报/Demis Hassabis- AGI 路线.md: Obsidian 路径 (抓取于 2026-04-15)
...

### L5 社区（3 条）
- X: https://x.com/.../status/... (抓取于 2026-04-15)
- Reddit: https://reddit.com/r/.../comments/... (抓取于 2026-04-15)
...
```

## 信源白名单（推荐默认）

### L1 通用白名单（根据 query 主题动态筛选）
- AI/ML 公司：anthropic.com/news, openai.com/blog, blog.google, deepmind.google, x.ai, huggingface.co/blog
- 中国公司：qwen.alibaba-inc.com, tech.meituan.com, blog.csdn.net (官方认证号), 各大厂 aihub
- 产品官网：直接搜 `<产品名> official site`

### L3 中文媒体优先级
1. 36氪（综合性，含融资/产品）
2. 晚点 LatePost（深度报道）
3. 虎嗅（产业分析）
4. 财新（政策/财经）
5. 钛媒体（行业新闻）

### L3 英文媒体优先级
1. TechCrunch（产品发布）
2. The Verge（产品评测）
3. Stratechery / Casey Newton Platformer（深度分析，订阅制）
4. Wired（产业趋势）
5. Ars Technica（技术深度）

### 避免使用的信源（黑名单）
- 内容农场（百家号、头条号低质内容）
- 未注明作者的中文聚合站
- 超过 6 个月未更新的博客
- SEO 站群（典型特征：URL 含大量关键词、模板化内容）
