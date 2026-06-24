# Ryder's Skills Collection

A personal AI Agent skill library. Contains skills I use regularly and have validated through repeated use — some collected and adapted from the open-source community, some built from scratch.

> **How to use this repo**: Find the skill you need in the categories below → clone the repo → copy the skill directory to your agent's skills path (Hermes: `~/.hermes/skills/`, Codex: `~/.codex/skills/`) → start a new session to auto-load.

---

## Directory Structure

```
Ryder-s-Skills-Collection/
├── research-intelligence/     Research & Intelligence (9 skills)
├── video-motion/              Video & Motion (4 skills)
├── content-creation/          Content Creation (5 skills)
├── personal-insights/         Personal Insights (1 skill)
├── frontend-dev/              Frontend Development (1 skill)
├── README.md                  Chinese version
└── README_EN.md               English version (this file)
```

---

## Skill Catalog

### research-intelligence/ — Research & Intelligence

Deep research, open-source project analysis, AI industry intelligence, KOL content mining. For PMs, researchers, and analysts.

| Skill | Version | Size | One-liner | Who it's for |
|---|---|---|---|---|
| **deep-research** | 1.3.2 | 1.3MB | Enterprise-grade deep research, 5 scenario templates + McKinsey-style .docx output | Anyone producing research reports |
| **github-deep-analysis** | 9.0.0 | 102KB | GitHub open-source project strategic analysis (business insight, not tech assessment) | Anyone evaluating projects for adoption/investment |
| **aihot** | — | 24KB | AI HOT Chinese AI comprehensive news query | Anyone tracking AI daily |
| **aihot-ai-models** | — | 4KB | AI HOT model release/update intelligence (OpenAI/Anthropic/Google...) | Anyone tracking model releases |
| **aihot-ai-papers** | — | 4KB | AI HOT paper research intelligence (arXiv/breakthroughs/architectures...) | Anyone tracking academic progress |
| **aihot-ai-products** | — | 4KB | AI HOT product launch/update intelligence (SaaS/tools/features...) | Anyone tracking product updates |
| **intelligence-engine-api** | — | 91KB | Intelligence engine backend API query/export/rank/visualize | Developers building on the intelligence engine |
| **twitter-ai-kol-fetcher** | — | 38KB | Fetch Twitter AI KOL activity + identify trending topics + generate briefings | Anyone producing AI industry briefings |
| **kol-interview-to-wiki** | 3.0 | 30KB | YouTube KOL interview → structured deep analysis → Obsidian wiki | Anyone mining KOL interviews for insights |

### video-motion/ — Video & Motion

Social media video production, video post-processing, video download/clipping. For content creators and social media operators.

| Skill | Version | Size | One-liner | Who it's for |
|---|---|---|---|---|
| **vibe-remotion-animator** | 2.0.0 | 4.0MB | Social media video unified entry, 7 components + Disney 12 principles + 3 platform specs | Anyone making Douyin/Bilibili/WeChat explainer videos |
| **Video-Wrapper-Skills** | — | 89KB | Interview video variety effects (captions/cards/character bars/chapter titles) | Anyone doing interview video post-processing |
| **Youtube-clipper-skill** | — | 100KB | YouTube smart clipping + bilingual subtitles + burn-in + summary copy | Anyone making short clips from YouTube |
| **video-downloader** | — | 2KB | Download videos from YouTube and other platforms | Anyone needing to download videos |

### content-creation/ — Content Creation

PPT generation, social media IP content, document illustration, document processing, AI-text de-identification. For content producers.

| Skill | Version | Size | One-liner | Who it's for |
|---|---|---|---|---|
| **NanoBanana-PPT-Skills** | — | 160KB | PPT visual generation + transition videos (style selection + image gen + video composition) | Anyone making PPTs |
| **Document-illustrator-skill** | — | 183KB | Auto-generate document illustrations (AI analyzes structure + generates style-matched images) | Anyone needing illustrations for documents |
| **content-studio** | — | 6.5MB | Personal social media IP content studio (Xiaohongshu/X/Douyin/Bilibili copy + card templates + reusable series templates) | Anyone building a personal IP or social content system |
| **document-skills** | — | 2.4MB | Document processing toolkit | Anyone processing various documents |
| **Humanizer-zh** | — | 26KB | Remove AI traces from Chinese text (exaggerated symbolism/promotional language/rule-of-three...) | Anyone polishing AI-generated text |

### personal-insights/ — Personal Insights

Understand yourself through work traces — where fun meets depth.

| Skill | Version | Size | One-liner | Who it's for |
|---|---|---|---|---|
| **work-selfie** | — | 27MB | WorkSelfie workplace personality analysis + Fauvism card (DingTalk data → self-analysis report + PNG card) | Anyone wanting to understand themselves through work traces |

### frontend-dev/ — Frontend Development

React component selection and integration. For frontend developers.

| Skill | Version | Size | One-liner | Who it's for |
|---|---|---|---|---|
| **react-bits-selector** | — | 21MB | React Bits animated component selection/config/integration (1325-component local catalog) | Anyone adding animations to React frontends |

---

## How to Choose: By Scenario

| I want to... | Recommended Skill |
|---|---|
| Produce a research report | `deep-research` |
| Analyze a GitHub open-source project | `github-deep-analysis` |
| Track daily AI industry updates | `aihot` (general) / `aihot-ai-models` (models) / `aihot-ai-papers` (papers) / `aihot-ai-products` (products) |
| Mine KOL interview content | `kol-interview-to-wiki` (YouTube) + `twitter-ai-kol-fetcher` (Twitter) |
| Make Douyin/Bilibili explainer videos | `vibe-remotion-animator` |
| Add effects to interview videos | `Video-Wrapper-Skills` |
| Clip short videos from YouTube | `Youtube-clipper-skill` |
| Make PPTs | `NanoBanana-PPT-Skills` |
| Create personal IP social posts | `content-studio` |
| Add illustrations to documents | `Document-illustrator-skill` |
| Remove AI tone from text | `Humanizer-zh` |
| Understand yourself through work traces | `work-selfie` |
| Add animated components to React | `react-bits-selector` |

---

## Installation

```bash
# 1. Clone
git clone https://github.com/Ryder-MHumble/Ryder-s-Skills-Collection.git

# 2. Copy the skill you need to your agent's skills directory
# Hermes Agent:
cp -r Ryder-s-Skills-Collection/<category>/<skill-name> ~/.hermes/skills/creative/

# Codex CLI:
cp -r Ryder-s-Skills-Collection/<category>/<skill-name> ~/.codex/skills/

# 3. Start a new session — the agent auto-loads the skill
```

> **Note**: Some skills have script dependencies (python3 / node / npm / ffmpeg / puppeteer). See each skill's SKILL.md `prerequisites` field for details.

---

## Skill Source Labels

| Label | Meaning |
|---|---|
| `author: Ryder + Hermes Agent` | Built by Ryder or heavily modified |
| `author: —` | Collected from open-source community, possibly adapted but author unchanged |
| Has version number | Version-managed (see CHANGELOG.md) |
| Version `—` | Single version, no CHANGELOG |

---

## Maintenance Rules

- Local `~/.hermes/skills/` is the **primary copy**; GitHub repo is a **mirror**
- When upgrading a skill, update local first, then sync to repo
- New skills must be categorized into the appropriate directory
- Use environment variables (`$HERMES_HOME` / `$HERMES_OUTPUT`) for paths — no hardcoding

---

## License

Each skill is independently licensed — see each SKILL.md's `license` field. Unlabeled skills default to MIT.
