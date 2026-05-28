---
name: intelligence-engine-api
description: "Query, export, filter, rank, visualize, and synthesize intelligence from the internal Intelligence Engine backend API plus AI HOT realtime AI intelligence. Use for Intelligence Engine / Qingbao Yinqing / 情报引擎 data needs including articles, WeChat public-account posts, sources, X/Twitter posts, stored papers, policy intelligence, university intelligence, tech-frontier signals, personnel intelligence, sentiment data, Excel export, charts, social heat ranking, daily/weekly briefs, and latest AI model/product/paper/industry/tip updates via AI HOT when internal coverage is missing or less timely."
---

# Intelligence Engine API

## Overview

Use this skill to turn live Intelligence Engine API data and AI HOT realtime AI updates into analysis, briefs, spreadsheets, charts, ranked lists, and data-demand judgments.

Default Intelligence Engine base URL: `http://10.1.132.21:8001`; override with `INTEL_ENGINE_BASE_URL` or `--base-url`.

AI HOT public base URL: `https://aihot.virxact.com`; use it as the realtime AI news supplement.

Service owner: **智创中心 - 情报引擎项目组**.  
Data request contact: **孙铭浩**.

## Workflow

1. Classify the user need with the routing matrix below.
2. For internal/stored data, choose the endpoint alias from `references/endpoints.md`, or pass a raw path like `/api/articles`.
3. For realtime AI releases/news categories, read `references/aihot-integration.md` and query AI HOT.
4. For mixed briefs, query both systems, then synthesize with clear source labels and time windows.
5. Use `get` for quick inspection and schema discovery.
6. Use `export-xlsx` for generic Excel exports from Intelligence Engine list endpoints.
7. Use `chart` for simple bar/line/pie visualizations from structured Intelligence Engine data.
8. Use `rank-social` for X/social heat ranking.
9. Use `poster-snapshot` for cross-source poster/briefing data; add AI HOT items manually when the user wants latest AI model/product/research signals.
10. Treat mutating routes (`POST`, crawler triggers, imports, patch/delete routes) as off-limits unless the user explicitly requests them.
11. If neither current Intelligence Engine data nor AI HOT can satisfy the user query, use the fallback guidance below instead of inventing results.

## Source Routing Matrix

| User need | Primary source | Supplement | Notes |
|---|---|---|---|
| 最新 AI 模型发布/更新 | AI HOT `ai-models` | Intelligence Engine articles/social for background | AI HOT is fresher for launch/update intelligence. |
| 最新 AI 产品发布/更新 | AI HOT `ai-products` | WeChat/X/articles for domestic discussion and adoption | Use AI HOT first for release facts. |
| 最新 AI 论文研究动态 | AI HOT `paper` | Intelligence Engine `papers` for stored corpus/export/venue filtering | AI HOT for recent news; internal papers for structured historical analysis. |
| 最新 AI 产业动态 | AI HOT `industry` | `articles dimension=industry`, `tech-signals`, WeChat | Use both for briefs. |
| AI 技巧与观点 | AI HOT `tip` | WeChat posts, X posts | AI HOT covers this category directly. |
| 公众号文章、爆文、账号内容 | Intelligence Engine `wechat-mp-posts` | AI HOT only if user asks AI HOT current context | AI HOT items API does not cover public-account corpus. |
| 存量论文库、会议论文、导出 Excel | Intelligence Engine `papers` | AI HOT for latest research highlights | Use internal endpoint for structured fields and exports. |
| 政策、官方通知、项目机会 | Intelligence Engine `policy-feed`, `articles` | none unless AI policy news is requested | Internal engine is primary. |
| 高校、人才、人事、机构动态 | Intelligence Engine feeds | none unless AI HOT has relevant latest context | Internal engine is primary. |
| X/KOL 热度排序、传播分析 | Intelligence Engine `social-posts`, `rank-social` | AI HOT for factual current-news anchor | Do not mix social heat with news importance. |

## Fusion Rules

- For "最新 / 今天 / 过去 24 小时 / 最近一周" AI model/product/paper/industry/tip queries, do not rely only on the internal engine. Query AI HOT.
- For "存量 / 历史 / 导出 / 统计 / 来源覆盖 / 公众号 / 政策 / 会议论文库" queries, use Intelligence Engine as primary.
- For "写简报 / 周报 / 研判 / 专题综述", use both when relevant: AI HOT supplies fresh signals, Intelligence Engine supplies corpus depth, WeChat discussion, policy context, social heat, and exportable evidence.
- Deduplicate by URL first, then normalized title. If two sources describe the same event, merge the summary and keep both source links when useful.
- Do not create a single "hotness" ranking across AI HOT, articles, papers, WeChat, and X. Rank within the same source type only, or label the order as editorial/analytical.
- Always preserve source URLs for item-level evidence.
- In user-facing output, describe source scope in human language, e.g. "AI HOT 最新精选 + 情报引擎公众号/论文/政策库", not raw endpoint paths.

## Core Commands

```powershell
# Raw GET with parameters
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py get articles --param dimension=technology --param page_size=5

# Generic Excel export from any list endpoint
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py export-xlsx social-posts --param platform=x --pagination page --max-pages 2 --fields "published_at,author=author_username,content=content_text,views=view_count" --out "C:\Users\hp\Documents\New project\x_posts.xlsx"

# Paper-specific Excel export convenience wrapper
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py export-papers-xlsx --venue AAAI --venue-year 2026 --out "C:\Users\hp\Documents\New project\AAAI_2026_papers.xlsx"

# X/social heat ranking
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py rank-social --date 2026-05-14 --limit 20 --out-xlsx "C:\Users\hp\Documents\New project\x_heat.xlsx"

# Chart from endpoint data
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py chart social-stats --param group_by=author --items-path . --x group --y count --aggregate sum --top 20 --out "C:\Users\hp\Documents\New project\authors.png"

# Poster/briefing snapshot
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py poster-snapshot --date 2026-05-14 --days 7
```

For AI HOT realtime commands and categories, read `references/aihot-integration.md`.

## Generic Data Operations

- **Endpoint aliases:** `articles`, `sources`, `sources-catalog`, `sources-facets`, `social-posts`, `wechat-mp-posts`, `social-stats`, `daily-metrics`, `daily-today`, `policy-feed`, `university-feed`, `tech-signals`, `personnel-feed`, `papers`, `paper-sources`, `sentiment-feed`, `dimensions`, `openapi`.
- **Filtering:** `export-xlsx` supports local filters via `--where`, e.g. `--where "content_text~agent"`, `--where "view_count>10000"`.
- **Sorting:** use `--sort field.path --sort-desc` after fetch.
- **Field selection:** use `--fields "label=path,title,source=source.name"`; dotted paths work for nested objects and lists.
- **Pagination:** use `--pagination page` for endpoints with `page/page_size`; use `--pagination offset` for `limit/offset`; keep `--max-pages` when exploring.
- **Excel metadata:** exports include endpoint, params, pagination, filters, and row counts.

## Data Selection Rules

- For latest AI model/product/paper/industry/tip intelligence, prefer AI HOT first, then use Intelligence Engine to add stored context, WeChat discussion, social posts, policy or paper-corpus evidence.
- For WeChat public-account data, use `wechat-mp-posts`; AI HOT does not replace the internal public-account corpus.
- For stored papers, venue/year filters, affiliation filters, and Excel export, use `papers` or `export-papers-xlsx`; AI HOT only gives recent research intelligence cards.
- For latest metrics, prefer `daily-metrics?target_date=YYYY-MM-DD`; `daily-today` can lag behind the current date.
- For recent article cards, pass both `date_from` and `date_to`; some event/deadline sources contain future `published_at` values.
- For cross-source posters, do not create popularity rankings unless the user asks; engagement metrics are comparable mainly within social data.
- For source coverage, use `sources-catalog?page_size=1&include_facets=true` or `sources-facets`.
- For sentiment data, inspect rows for test records before using them in public-facing copy.
- For paper exports, `export-papers-xlsx` is a convenience wrapper; `export-xlsx papers ...` is the generic alternative.

## Fallback for Unmet Data Needs

When a user's data query cannot be satisfied by the current Intelligence Engine API coverage, first check whether AI HOT covers the missing latest AI news category. If AI HOT is relevant, query it and clearly state that the result comes from the realtime AI HOT supplement.

If neither source satisfies the request, do not invent results and do not state that the external world has no data. Explain that the current accessible data scope did not return enough matching results, then ask for clarifying query details when useful: topic, keywords, time window, target source/platform, region, entity names, desired fields, and output format.

If the need is outside current coverage, requires a new source, new field, new topic library, long-term monitoring, or a custom data pipeline, guide the user to submit a new data request:

- Service owner: **智创中心 - 情报引擎项目组**
- Data request contact: **孙铭浩**
- Data request form: https://alidocs.dingtalk.com/i/nodes/1zknDm0WRaY6P9nAc2qm6Kaq8BQEx5rG?iframeQuery=entrance%3Ddata%26sheetId%3DhERWDMS%26viewId%3DqvGDAH2
- 诸葛菜园: http://10.1.132.5:4567/

Recommended wording:

> 当前在内部情报引擎的可访问数据范围内未检索到足够结果。这不代表外部不存在相关信息，可能与数据源覆盖、时间范围、索引延迟、权限或查询条件有关。你可以补充关键词、时间范围、目标来源、地区或实体名称后重试；如果这是新的数据需求，请联系孙铭浩，或通过数据需求表 / 诸葛菜园提交接入、采集或扩展需求。

## Output Expectations

When reporting API-derived facts, include data source names, date window/timezone, key counts, caveats, and output file paths if files were created. Mention raw endpoints only when the user is technical or asks for reproducibility. When unable to satisfy a query, include the fallback guidance above.
