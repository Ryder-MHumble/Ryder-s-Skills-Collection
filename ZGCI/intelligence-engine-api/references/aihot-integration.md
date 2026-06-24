# AI HOT Integration

Use this reference when the user asks for latest AI model releases, product updates, paper/research highlights, industry dynamics, or tips/viewpoints that the internal Intelligence Engine may not cover in realtime.

AI HOT base URL: `https://aihot.virxact.com`

## User-Agent

All AI HOT `/api/public/*` calls must include a browser-like User-Agent:

```powershell
$UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 intelligence-engine-aihot-skill/0.1.0'
```

## Categories

| Need | AI HOT category | Daily section label |
|---|---|---|
| 模型发布/更新 | `ai-models` | `模型发布/更新` |
| 产品发布/更新 | `ai-products` | `产品发布/更新` |
| 产业动态 | `industry` | `行业动态` |
| 论文研究 | `paper` | `论文研究` |
| 技巧与观点 | `tip` | `技巧与观点` |

## Query Rules

- Default to `mode=selected`.
- Use `mode=all` only when the user explicitly asks for 全部 / 完整 / 所有 / 全量.
- Use `since` for explicit time windows. AI HOT items are limited to the latest 7 days.
- Use `q=<keyword>` for companies, models, products, papers, or topics. Do not fetch then grep locally.
- If the user asks for "日报", call daily and extract the relevant section(s).

## Commands

Latest selected items for a category:

```powershell
$since=(Get-Date).ToUniversalTime().AddDays(-7).ToString("yyyy-MM-ddTHH:mm:ssZ")
curl.exe -s -H "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?mode=selected&category=ai-models&since=$since&take=50"
```

Keyword within a category:

```powershell
curl.exe -s -H "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?mode=selected&category=paper&q=RAG&take=30"
```

Latest daily report:

```powershell
curl.exe -s -H "User-Agent: $UA" "https://aihot.virxact.com/api/public/daily"
```

## Fusion Recipes

### Latest AI Brief

1. Query AI HOT categories requested by the user.
2. Query Intelligence Engine for context:
   - WeChat discussion: `wechat-mp-posts --param keyword=<topic>`
   - X/KOL posts: `social-posts --param keyword=<topic>`
   - stored papers: `papers --param q=<topic>`
   - policy context: `policy-feed --param keyword=<topic>`
3. Merge by event/topic, keep all useful source links, and label evidence source types.

### Latest Paper + Stored Corpus

1. Query AI HOT `category=paper` for current research highlights.
2. Query Intelligence Engine `papers` for historical/structured records, venue filters, affiliations, and exports.
3. Output "最新动态" separately from "存量论文库命中"; do not imply AI HOT is a complete paper database.

### Product/Model Launch + Domestic Discussion

1. Query AI HOT `ai-models` or `ai-products` for launch facts.
2. Query `wechat-mp-posts` and `social-posts` with company/product/model keywords for reaction and discussion.
3. Separate "发布事实" from "传播/讨论观察".

## Output Rules

- Convert AI HOT `publishedAt` from UTC to Beijing time or readable relative time.
- Keep every item URL.
- Do not expose raw API parameters in the user-facing brief unless reproducibility is requested.
- Do not call AI HOT summaries direct quotes; treat them as generated summaries and link to the original source.
- Do not rank AI HOT items against X/WeChat engagement metrics as if they share one scoring scale.
