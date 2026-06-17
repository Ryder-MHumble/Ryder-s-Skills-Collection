---
name: readme-writing
description: Write GitHub README with narrative arc and topic appeal, not feature lists. For open-source projects that need to hook readers, not just inform them.
version: 1.0.0
metadata:
  hermes:
    tags: [writing, open-source, readme, narrative, marketing]
---

# README Writing — Narrative-Driven

## Core Principle

A README is not a manual. It's a pitch. The reader decides in 10 seconds whether to keep reading. Feature lists don't hook — counterintuitive truths do.

## Structure

### 1. One-Line Hook

State the problem, not the solution. Invert expectations.

**Bad**: "A tool that optimizes agent skill routing."
**Good**: "The more you install, the worse your agent picks."

The hook must make the reader think "wait, really?" — then you explain why.

### 2. Expand the Paradox

3-4 sentences that prove the hook is true. Reference structural causes (not user error). Name the mechanism.

Example: "This isn't your agent's fault. It's a structural flaw in Progressive Disclosure — the longer the catalog, the worse LLM retrieval gets."

### 3. "What You Think vs What Actually Happens" Table

Concrete, specific, no abstraction. Each row is an experience the reader has had but couldn't articulate.

### 4. Three Scenarios (Timeline, Not Feature List)

Don't list features. Show the product in action across time:
- **Before** (install time) — what gets caught
- **During** (runtime) — what gets filtered
- **After** (post-run) — what becomes visible

### 5. "What It Isn't"

More powerful than explaining what it is. Each "not" claim is a boundary that makes the "is" sharper.

### 6. vs Competitor Table

Not feature comparison — positioning statement. One line that captures the difference in philosophy.

### 7. Quickstart (5 Minutes Max)

Numbered steps, each one command. No prose.

## Language Rules

- **No "empower", "leverage", "seamless", "powerful"** — these mean nothing
- **Specific numbers over vague claims**: "50 → 5" not "reduces catalog size"
- **Active voice**: "Watchman filters" not "filtering is performed"
- **Chinese for zh-audience projects**: Don't translate an English README. Write natively in Chinese. The sentence structure is different.
- **Bilingual**: Main README in primary audience language. Separate `README.en.md` / `README.zh.md`. Link both from a centered nav line.

## Process

1. Read all source code — understand what's actually built, not what was planned
2. Identify the counterintuitive truth the product reveals
3. Write the hook first — if it doesn't make you rethink, rewrite
4. Build the narrative arc: paradox → proof → solution → boundaries
5. Add technical reference sections (CLI, config, data) after the narrative
6. Write the other language version — don't translate, rewrite with native idiom

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Opening with "X is a Y that does Z" | Describes, doesn't hook | Lead with the problem |
| Feature list as main content | Readers skip these | Embed features in scenarios |
| "Easy to use / Simple / Lightweight" | Everyone says this | Show, don't tell |
| Jargon without explanation | Excludes readers | Explain once, then use |
| Translating instead of rewriting | Feels unnatural | Each version written natively |
| README as thin index to other docs | Wastes the first impression | Full content in README |

## Verification

Before shipping, check:
- [ ] Would someone who's never heard of this problem understand the hook?
- [ ] Does the "vs" table capture a real philosophical difference?
- [ ] Could a reader start using it after reading only the quickstart?
- [ ] Is the bilingual version natively written, not machine-translated?
