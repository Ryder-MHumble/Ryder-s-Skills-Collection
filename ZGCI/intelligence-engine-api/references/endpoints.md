# Intelligence Engine API Reference

Base URL: `http://10.1.132.21:8001`

Use `GET /openapi.json` if you need the full live schema. Use the script alias `openapi` for this route.

## Core Discovery

| Alias | Endpoint | Use |
|---|---|---|
| `openapi` | `/openapi.json` | Full API schema. |
| `dimensions` | `/api/dimensions` | Dimension names, total article counts, last update timestamps. |
| `article-stats` | `/api/articles/stats` | Aggregate article counts, default grouped by dimension. |
| `sources-facets` | `/api/sources/facets` | Source counts by dimension, platform, schedule, health, taxonomy. |
| `sources-catalog` | `/api/sources/catalog` | Paginated source list plus optional facets. |

Common source parameters: `dimension`, `dimensions`, `group`, `groups`, `tag`, `tags`, `crawl_method`, `source_type`, `source_platform`, `schedule`, `taxonomy_domain`, `taxonomy_track`, `taxonomy_scope`, `is_enabled`, `health_status`, `keyword`, `page`, `page_size`, `include_facets`.

## Articles and Feeds

| Alias | Endpoint | Important params | Use |
|---|---|---|---|
| `articles` | `/api/articles` | `dimension`, `source_id`, `source_name`, `keyword`, `date_from`, `date_to`, `sort_by`, `order`, `page`, `page_size` | Raw article list across dimensions. |
| `policy-feed` | `/api/intel/policy/feed` | `category`, `importance`, `min_match_score`, `keyword`, `limit`, `offset` | Policy intelligence enriched by rules/LLM. |
| `university-feed` | `/api/intel/university/feed` | `group`, `keyword`, `date_from`, `date_to`, `page`, `page_size` | University and research ecosystem articles. |
| `tech-signals` | `/api/intel/tech-frontier/signals` | `topic_id`, `signal_type`, `keyword`, `limit`, `offset` | Flat technology/industry/KOL signal stream. |
| `personnel-feed` | `/api/intel/personnel/feed` | `importance`, `min_match_score`, `keyword`, `limit`, `offset` | Personnel and appointment intelligence. |

Known dimensions: `national_policy`, `beijing_policy`, `technology`, `talent`, `industry`, `universities`, `events`, `personnel`, `twitter`, `scholars`, `sentiment`.

## Social, Sentiment, Papers

| Alias | Endpoint | Important params | Use |
|---|---|---|---|
| `social-posts` | `/api/social-posts` | `platform`, `username`, `post_type`, `is_kol_author`, `keyword`, `sort_by`, `order`, `page`, `page_size` | Unified social post library, currently useful for X/KOL dynamics. |
| `wechat-mp-posts` | `/api/social-posts/wechat-mp` | `account_name`, `account_names`, `category`, `keyword`, `date_from`, `date_to`, `sort_by`, `order`, `page`, `page_size` | WeChat public-account article list with title, body text, URL, publish/crawl times, and engagement fields. |
| `social-stats` | `/api/social-posts/stats` | `group_by=platform/source/author/post_type/date` | Social aggregates. |
| `sentiment-feed` | `/api/sentiment/feed` | `platform`, `keyword`, `sort_by`, `sort_order`, `page`, `page_size` | Public social/content sentiment feeds; inspect for test data. |
| `papers` | `/api/papers` | `q`, `source_type`, `source_name`, `venue`, `venue_year`, `date_from`, `date_to`, `affiliation`, `has_abstract`, `page`, `page_size`, `sort_by`, `order` | Global paper list. |
| `paper-sources` | `/api/papers/sources` | none usually | Paper source/venue coverage and latest import runs. |

## Daily Briefing

| Alias | Endpoint | Use |
|---|---|---|
| `daily-metrics` | `/api/intel/daily-briefing/metrics` | Metric cards and dimension counts for a target date. Prefer this for latest daily numbers. |
| `daily-today` | `/api/intel/daily-briefing/today` | Generated narrative daily report. It may return the most recently generated report, not necessarily the current calendar date. |

## Request Examples

```powershell
# Today's metric cards
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py get daily-metrics --param target_date=2026-05-14

# Recent technology articles
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py get articles --param dimension=technology --param date_from=2026-05-08 --param date_to=2026-05-14 --param sort_by=published_at --param order=desc --param page_size=5

# Source coverage facets
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py get sources-catalog --param page_size=1 --param include_facets=true

# Recent social posts
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py get social-posts --param page_size=8 --param sort_by=published_at --param order=desc
```

## Excel Export Examples

```powershell
# Export AAAI 2026 papers to Excel
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py export-papers-xlsx --venue AAAI --venue-year 2026 --out "C:\Users\hp\Documents\New project\AAAI_2026_papers.xlsx"
```
