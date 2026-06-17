# Institution Paper Tracker — Reference Data

## API Endpoints

| API | Base URL | Affiliation Search | Notes |
|-----|----------|--------------------|-------|
| CrossRef | `https://api.crossref.org/works` | `query.affiliation=` | **Best** for institution matching |
| OpenAlex | `https://api.openalex.org/works` | `search=` (full-text only) | Must post-filter by `raw_affiliation_strings` |
| arXiv | `http://export.arxiv.org/api/query` | `search_query=au:` (by author) | Returns XML; supplementary source |

## Common Institution Names

| Chinese | English | Keywords for matching |
|---------|---------|---------------------|
| 中关村人工智能研究院 | Zhongguancun Institute of Artificial Intelligence | zhongguancun, institute, artificial, intelligence |
| 北京中关村学院 | Zhongguancun Academy | zhongguancun, academy |
| 中关村实验室 | Zhongguancun Laboratory | zhongguancun, laboratory |

## False Positive Patterns

These appear in affiliations but are NOT the target institutions:
- "No. XX, Zhongguancun East Road" → CAS/other institute address
- "No. XX, Zhongguancun South Street" → Chinese Academy of Agricultural Sciences address
- "Zhongguancun North First Street" → Institute of Chemistry, CAS address
- "Zhongguancun Nephrology & Blood Purification Innovation Alliance" → different org