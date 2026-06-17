# Browser Harness 深度分析 — 2026-04-30

## 关键数据快照

| 指标 | 值 |
|------|------|
| Stars | 8,604 (13 天) |
| Forks | 769 |
| Watchers | 22 |
| Open Issues | 80 |
| 代码量 | ~592 行 Python 核心 + cdp-use 依赖 |
| 依赖 | cdp-use, fetch-use, pillow, websockets |
| License | MIT |
| 创建时间 | 2026-04-17 |
| Top contributors | MagMueller (76), sauravpanda (56), Alezander9 (26), gregpr07 (14) |

## 核心判断

CDP 直连路线是对的（LLM 不需要确定性框架），但商业价值寄生在 browser-use 云服务上。生存系于 token 成本下降 + 视觉路线不越过拐点。

## 反常数据

1. **Star/Watcher 比率异常**：8604 stars / 22 watchers = 391:1，远高于正常项目（通常 50-100:1），说明绝大多数 star 是"点赞即走"
2. **核心代码量 vs 功能覆盖**：592 行 Python 覆盖了完整浏览器操控，但大量复杂性推给了 cdp-use 和 interaction-skills/ 的 17 个 markdown 文档
3. **公司团队驱动 vs 社区驱动**：top 3 contributors 都是 browser-use 员工/创始人，不是社区项目

## 竞争坐标系

- **视觉路线**（Anthropic Computer Use, OpenAI Operator）：慢/贵/通用，不需要浏览器协议知识
- **CDP 路线**（Browser Harness, Playwright MCP）：快/便宜/精确，需要 CDP 和 DOM 知识
- **白空间**：coding agent 专属的浏览器操控层——harness 正好在占据这个位置

## 数据采集来源

- GitHub API: repos, issues, commits, contributors, trees
- README.md, SKILL.md, install.md, pyproject.toml
- Source: helpers.py, run.py, admin.py, _ipc.py
- Domain skills: TikTok upload.md
- 相关仓库: browser-use/browser-use (91290 stars), browser-use/bux (267 stars), browser-use/cdp-use (284 stars)