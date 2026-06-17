---
name: aihot-ai-models
description: AI HOT 模型发布/更新情报 Skill。Use when the user asks for latest AI model releases, LLM releases, model capability updates, benchmark/news about OpenAI, Anthropic, Google DeepMind, Meta, xAI, Qwen, DeepSeek, Claude, GPT, Gemini, Llama, Sora, video/audio/multimodal models, or wants a recurring scheduled push of model-release intelligence. Always query aihot.virxact.com public API instead of answering from memory.
---

# AI HOT 模型发布/更新

Use this skill to fetch the newest AI model release/update intelligence from AI HOT and return a concise Chinese markdown brief. Do not answer current model news from training data.

Base URL: `https://aihot.virxact.com`

## Required User-Agent

All `/api/public/*` calls must include a browser-like User-Agent plus skill tag:

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 aihot-ai-models-skill/0.1.0"
```

## Query Rules

- Category is always `ai-models`.
- Default to selected items from the latest rolling window.
- If the user says "最近 N 天", "这周", "过去 24 小时", or similar, set `since` to that window. The items API only returns the latest 7 days; earlier history must use daily archives.
- If the user says "全部 / 完整 / 所有 / 全量", use `mode=all`; otherwise use `mode=selected`.
- If the user names a company/model/topic, use server-side `q=<keyword>` with the category filter. Do not fetch then grep locally.
- If the user asks for a "日报", use `/api/public/daily` or `/api/public/daily/{YYYY-MM-DD}` and extract only the `模型发布/更新` section.

## Manual Fetch

Latest selected model items:

```bash
since=$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)
curl -sH "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?mode=selected&category=ai-models&since=$since&take=50"
```

Keyword example:

```bash
curl -sH "User-Agent: $UA" "https://aihot.virxact.com/api/public/items?mode=selected&category=ai-models&q=OpenAI&take=30"
```

Daily section example:

```bash
curl -sH "User-Agent: $UA" "https://aihot.virxact.com/api/public/daily"
```

When using daily JSON, find `sections[]` where `label == "模型发布/更新"`.

## Scheduled Push Mode

When the user asks to create a recurring push, create an actual scheduled job with the scheduling mechanism available in the host environment or agent platform. If no scheduler/push channel exists in the current environment, explain the missing dependency and provide the exact prompt/job body for the user to install elsewhere.

Recommended job prompt:

```text
Use $aihot-ai-models. Run scheduled push mode for the latest AI model releases and updates. Fetch the newest selected model items, deduplicate against the previous run if scheduler state is available, and push a concise Chinese markdown brief with source links.
```

Default cadence: every day at 09:00 Beijing time unless the user specifies another time. For high-signal model launches, daily is enough; do not poll more often than hourly.

Scheduled push output should include:
- Time window in human language.
- New important model releases/updates first.
- Source name and URL for every item.
- "No major model updates found" when there are no new items.

## Output Format

Return user-facing markdown only. Do not expose endpoint paths, raw parameters, HTTP status codes, rate limits, cache details, cursor details, or debug logs.

Use flat numbering because this skill has one category:

```markdown
**AI HOT 模型发布/更新 · 最近一周**（按发布时间倒序）

1. **<标题>** — <来源>
   <北京时间/相对时间>
   <50-100 字中文摘要，说明能力变化、模型类型、适用场景或影响>
   <URL>
```

Convert `publishedAt` from UTC ISO to Beijing time or a readable relative time. Do not display raw ISO timestamps.

If no results match, say plainly that this time window did not find model release/update items, and suggest widening to the latest 7 days.

## Do Not

- Do not mix in product launches, industry dynamics, papers, or tips unless the user explicitly asks for cross-category context.
- Do not omit source URLs.
- Do not treat AI HOT summaries as verbatim source quotes.
- Do not claim a scheduled push was created unless a real scheduler/job was configured.
