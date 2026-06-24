# Generic Operations

This skill should stay flexible: endpoint-specific convenience commands are allowed, but default to generic operations.

## Query

Use `get` for inspection:

```powershell
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py get <alias-or-path> --param key=value
```

## Export Any Endpoint to Excel

Use `export-xlsx` for any response with a list. If the response is a list at the root, pass `--items-path .`.

```powershell
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py export-xlsx articles --param dimension=industry --param date_from=2026-05-08 --param date_to=2026-05-14 --pagination page --fields "date=published_at,title,source=source_name,url" --out industry.xlsx
```

Options:

- `--pagination none|page|offset`
- `--items-path items` or `.` for root list
- `--fields "label=path,path2"`
- `--where "field~text"`, `--where "field=value"`, `--where "field>10"`
- `--sort field --sort-desc`
- `--limit N`

## Visualize

Use `chart` for quick bar/line/pie charts.

```powershell
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py chart social-stats --param group_by=author --items-path . --x group --y count --aggregate sum --top 20 --out author_counts.png
```

## Rank X/Social Posts

Use `rank-social` for local heat ranking. Formula:

`likes + replies*1.5 + reposts*2 + quotes*2 + bookmarks*1.5 + views*0.01`

```powershell
python C:\Users\hp\.codex\skills\intelligence-engine-api\scripts\intel_api.py rank-social --date 2026-05-14 --limit 20 --out-xlsx x_heat.xlsx
```

Use this only within social data; do not compare social heat with article, paper, or policy records.
