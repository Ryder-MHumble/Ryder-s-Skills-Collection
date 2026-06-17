# Deep Research Search Protocol

用于把一次调研变成可复核的检索工程，而不是边搜边写。

## 1. 检索计划 JSON schema

复杂任务先写 `research_plan.json`：

```json
{
  "topic": "industrial exoskeleton labor protection market",
  "decision_question": "Should we enter this market and which segment should be prioritized?",
  "as_of_date": "2026-06-10",
  "time_window": "2024-01-01 to 2026-06-10; last 30 days for live signals",
  "geography": ["United States", "United Kingdom", "France", "Germany"],
  "languages": ["en", "zh"],
  "include": ["labor protection", "warehouse", "manufacturing", "construction"],
  "exclude": ["medical rehab", "consumer hiking unless relevant to crossover entrants"],
  "source_mix": {
    "A": ["government", "SEC/IR", "official statistics", "papers"],
    "B": ["Reuters", "industry research", "credible vertical media"],
    "C": ["company websites", "product pages", "conference pages"],
    "Social": ["Reddit", "X", "YouTube", "HN", "GitHub", "Polymarket"]
  },
  "subqueries": [
    {
      "id": "Q1",
      "question": "What is the current market size and growth rate?",
      "search_query": "industrial exoskeleton market size labor protection warehouse manufacturing",
      "target_sources": ["A", "B"],
      "evidence_needed": "market size, CAGR, segmentation, source methodology"
    }
  ],
  "entity_resolution": {
    "companies": ["German Bionic", "Ottobock Paexo", "HeroWear"],
    "official_sites": [],
    "social_handles": [],
    "communities": [],
    "github_repos": []
  },
  "stop_condition": "Every core judgment has 2 independent evidence items or is explicitly marked unavailable."
}
```

## 2. 查询质量预检

避免把搜索引擎带偏：

- 不把“近30天/recent/latest”塞进所有关键词；能用时间过滤就用时间过滤。
- 年龄、数字、Top N 等容易劫持检索的词，只在语义必要时保留。
- 把教程式问题改成讨论式问题：`how to use X` → `X workflows pain points alternatives`。
- 把宽主题拆成 4-8 个子查询：市场规模、用户痛点、玩家、价格、政策、负面证据、最新动态。
- 对命名实体先解析别名、母公司、子品牌、创始人、官网、社媒账号、GitHub repo、社区，再检索。

## 3. last30days 适配

适用：用户问最近30天、社媒舆情、真实用户怎么说、产品/竞品热度、开源项目近期活跃度、创始人/公司最新动作。

优先路径：如果本机安装了 `last30days` skill，先读它的 `SKILL.md`，按其 contract 运行主脚本。不要只用普通 Web 搜索替代。

可用发现方式：

```bash
find "$HOME/.codex/skills" "$HOME/.agents/skills" "$HOME/.claude/plugins/cache" \
  -path '*/last30days*/SKILL.md' -o -path '*/last30days*/scripts/last30days.py' 2>/dev/null
```

调用前先诊断：

```bash
python3 /path/to/last30days/scripts/last30days.py --diagnose
python3 /path/to/last30days/scripts/last30days.py --help
```

典型命令形态：

```bash
python3 /path/to/last30days/scripts/last30days.py "$TOPIC" \
  --days 30 \
  --emit md \
  --plan research_plan.json \
  --subreddits "SaaS,Entrepreneur,startups" \
  --github-repo "owner/repo" \
  --save-dir ./research_raw
```

从 last30days 输出中只吸纳这些字段进入本 skill 的证据账本：

| 字段 | 写入方式 |
|------|----------|
| source/platform | `type=Social` |
| title/author/community | source 标题 |
| URL | source URL |
| published_at | date |
| engagement | note：upvotes/likes/views/comments/stars |
| quoted finding | claim 或 note |
| uncertainty | confidence |

限制：Social 证据可证明“有人这样讨论/热度/争议”，不能单独证明市场规模、收入、市占、融资、法规事实。

## 4. 手工替代路径

如果没有 last30days 或缺少 API key：

1. 做实体解析：官网、X/微博/LinkedIn、GitHub、YouTube、Reddit/HN、App Store/电商、媒体库。
2. 对每个平台用 2-4 个查询：`品牌 + pain points`、`品牌 + alternative`、`品类 + recommendation`、`品类 + complaints`。
3. 记录时间窗和样本量，不把零结果解释为不存在。
4. 对事实性社媒爆料必须找 A/B/C 源二次确认。

## 5. 证据账本格式

Markdown：

```markdown
| evidence_id | claim | source | url | type | date | supports | confidence | note |
|-------------|-------|--------|-----|------|------|----------|------------|------|
| E01 | German Bionic sells powered industrial exoskeletons | Company product page | https://... | C | accessed 2026-06-10 | yes | medium | product page confirms category, not sales volume |
```

CSV：

```csv
evidence_id,claim,source,url,type,date,supports,confidence,note
E01,"...","...","https://...",C,2026-06-10,yes,medium,"..."
```

## 6. 反向检索和负面证据

每个重大判断至少做一次反向检索：

- `company lawsuit`, `company bankruptcy`, `product discontinued`, `recall`, `complaints`, `Reddit alternative`, `site:reddit.com/r/...`。
- 中文：`公司名 投诉`、`公司名 停产`、`公司名 融资 失败`、`产品名 负面`。
- 没找到负面不是“没有风险”，写“未在本轮公开检索中发现”。
