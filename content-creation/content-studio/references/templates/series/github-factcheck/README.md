# 一分钟打假一个 GitHub 热门项目｜专题模板

Use this template when a 小红书 post fact-checks a popular GitHub repo using code, issues, benchmarks, docs, or local tests.

## Positioning

- 系列名固定露出：`一分钟打假一个 GitHub 热门项目`
- 语气：不要反复喊“打假”。核心是“大家都在吹的时候，先冷静复核它是不是真的那么神”。
- 结构：封面 1 张 + 6-7 张证据卡 + References 1 张
- 每张证据卡只讲 1 个复核点：`claim -> evidence -> implication`
- 帖子正文先写刷到热门项目时的真实体感，再给一句明确判断，最后给读者可复用的三问法：数字适用什么场景、边界在哪里、issue 里在吵什么。

## Visual Rules

- 画布：1080×1440，小红书 3:4
- 风格：forensic dossier（米黄纸面、黑色证据块、红色 verdict、黄色测试标签）
- 封面固定结构：主标题放系列名；副标题放本期强钩子；下方放 GitHub 项目主页首屏截图；页脚保留 issue 编号
- 内容页必须有：红色 kicker、强标题、证据块或指标条、1-2 个解释块
- 禁止把大段终端输出当正文；终端块只放 3-5 行关键证据
- Renderer 使用 PIL 测量文本；封面标题会自动缩字号适配，其他溢出直接报错，避免浏览器截图裁切

## Data Schema

Run:

```bash
python capture_github_project_page.py \
  --repo headroomlabs-ai/headroom \
  --out ./assets/headroom-github-project-page.png

python render_github_factcheck.py \
  --data spec.json \
  --out ./png
```

Minimal cover fields:

```json
{
  "series_name": "一分钟打假一个 GitHub 热门项目",
  "cards": [
    {"type":"cover","slug":"cover","cover_style":"series_github_project","main_title":"一分钟打假一个 GitHub 热门项目","subtitle":"号称省70%Token，实测大失所望","project_screenshot":"./assets/repo-page.png"},
    {"type":"finding","slug":"verdict","kicker":"测试结论","title":"高星不是假，神话有水分","metrics":[{"label":"Stars","value":"46,640"}],"body":[{"tag":"结论","text":"..."}]},
    {"type":"references","slug":"references","refs":["[1] ..."]}
  ]
}
```

See `cover_spec.example.json` for a single-card cover smoke spec.

## Scripts

| Script | Purpose |
|---|---|
| `capture_github_project_page.py` | Capture the first viewport of a GitHub repo page. Uses Chrome DevTools Protocol with Python stdlib. |
| `render_github_factcheck.py` | Render 1080x1440 cover/content/reference PNGs from JSON. Fails fast on overflow. |

`capture_github_project_page.py` needs local Chrome/Chromium. On macOS it uses `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`; otherwise set `CHROME_BIN`.

## Topic Slots

- `AI时代的碎碎念`：观点/社会观察型，图集主打体感与机制解释。
- `一分钟打假一个 GitHub 热门项目`：证据/测试报告型，图集主打 repo 数据、代码证据、issue、benchmark。
- `Ryder的工具集推荐`：工具推荐型，图集主打使用场景、替代选择、真实体验。
