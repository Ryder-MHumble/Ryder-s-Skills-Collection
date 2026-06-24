# Poster and Briefing Data Recipe

Use this reference when the user asks for a poster, elevator screen, weekly intelligence board, leadership brief, or realistic sample content.

## Recommended API Mix

1. `daily-metrics?target_date=YYYY-MM-DD`
   - Use `article_count`, `dimension_counts`, and `metric_cards` for the main numeric card.
   - If unavailable for today, state the fallback date explicitly.
2. `sources-catalog?page_size=1&include_facets=true`
   - Use `total_sources`, `facets.source_platforms`, `facets.health_statuses`, and `facets.dimensions` for coverage proof.
3. `policy-feed?limit=5`
   - Use recent important policy or policy opportunity cards.
4. `tech-signals?limit=6`
   - Use technology/industry/KOL signal cards.
5. `articles` with `dimension=industry|technology|universities|beijing_policy` plus `date_from/date_to`
   - Use for direct article examples when enriched feeds are too verbose.
6. `social-posts?page_size=5&sort_by=published_at&order=desc`
   - Use for X/KOL observations. Avoid comparing its engagement metrics with non-social sources.
7. `papers?page_size=5&sort_by=publication_date&order=desc`
   - Use for recent paper cards.
8. `paper-sources`
   - Use for paper warehouse coverage numbers.

## Poster Copy Rules

- Prefer ??? AI ?????, ????????, or ???????? over ranking language.
- Avoid `Top10`, `???`, likes, comments, views, fire icons, and cross-source popularity ranking unless explicitly requested.
- Lead with fresh time-bounded counts: ?????? X ? AI ??? or ??? 7 ????.
- Show platform value through dimensions: policy, industry, technology, university, talent/personnel, papers, social/KOL.
- Mention ?????? ? ????? only if the user confirms it is still true.
- Use ?????????? for QR copy unless a different CTA is provided.

## Quality Caveats

- `daily-today` may return yesterday's generated narrative. Prefer `daily-metrics` for current-day numbers.
- Some event/deadline sources have future `published_at` values. Always set `date_to` for recent-news posters.
- `sentiment-feed` may include test records; verify title/content before public display.
- Top journals/conferences are valuable for coverage proof, but not all are crawled daily.

## Minimal Poster Snapshot Command

```powershell
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py poster-snapshot --date 2026-05-14 --days 7
```

The snapshot returns a compact JSON object with metrics, source coverage, social totals, paper totals, and candidate cards.
