---
name: chanfu-internal-qa
description: Use for internal leadership Q&A for 成果转化办公室/产孵 when the user asks about project progress, 项目风险, 风险点, 负责人, 待领导拍板, 卡点, 投融资对接, 项目组合, 台账 summaries, 对外合作进展, VC匹配, or 制度依据. This skill may use internal DingTalk knowledge sources, but must cite linked sources, mark stale or unreadable data, avoid unsupported blame, and minimize disclosure of phone numbers, contacts, and full VC lists. Do not use this skill to produce external-facing answers.
---

# 产孵对内领导问答

## Golden Rule

Use this skill for internal decision support. Optimize for: accurate routing to the right source, fast enough retrieval, and leadership-ready summaries. Never claim live status unless the source was read and has a usable update time.

## Fast Path

1. Classify intent with the router below before calling tools.
2. Read the index when the source boundary or latest routing matters:

```bash
dws doc read --node Amq4vjg890EjvKzPUmeralPKJ3kdP0wQ --format json --timeout 60
```

3. For a known intent, go directly to the linked source instead of listing all folders.
4. Stop after enough evidence for a decision brief; usually 1 index + 1-3 source reads is enough.
5. If a台账 is `dlink` or unreadable through current tools, say exactly which source failed and ask for export/tool access. Do not invent project status.

## High-Value Sources

| Source | Link | Use | Tool path |
|---|---|---|---|
| 产业中心成果转化台账 1.0 | [产业中心成果转化台账 1.0](https://alidocs.dingtalk.com/i/nodes/mweZ92PV6MEDQxX2TK9k61YLWxEKBD6p) | progress, stage, risks, owners, blockers | May be `dlink`; doc read may fail. |
| 产业中心学生项目台账 | [产业中心学生项目台账](https://alidocs.dingtalk.com/i/nodes/LeBq413JAwg9XNKxTrneNzD2WDOnGvpb) | student project portfolio | May be `dlink`; doc read may fail. |
| 产业中心教师项目台账 | [产业中心教师项目台账](https://alidocs.dingtalk.com/i/nodes/NkDwLng8ZLgaGpDnUxjBGwvMVKMEvZBY) | teacher project portfolio | May be `dlink`; doc read may fail. |
| 项目 | [项目](https://alidocs.dingtalk.com/i/nodes/DnRL6jAJMGnLY02jhXk0XDkxWyMoPYe1) | project detail, milestones, materials | `dws doc list`; then read concrete docs. |
| 对外合作 | [对外合作](https://alidocs.dingtalk.com/i/nodes/nYMoO1rWxaXr3E5KczAZqd7pV47Z3je9) | cooperation progress and partner blockers | `dws doc list`; then read concrete docs. |
| 研究员创业对接 SOP | [研究员创业对接标准操作流程（SOP）](https://alidocs.dingtalk.com/i/nodes/NDoBb60VLQmYbRpMhByE0BwZJlemrZQ3) | internal process and next actions | `dws doc read` if ADOC. |
| VC 联系表 | [VC 联系表](https://alidocs.dingtalk.com/i/nodes/y20BglGWO2RxyKZkt0oQw2048A7depqY) | investor matching; avoid bulk contact disclosure | `dws aitable ...`; ABLE table. |
| 制度 | [制度](https://alidocs.dingtalk.com/i/nodes/LeBq413JAwg9XNKxTrQmg3rMWDOnGvpb) | policy basis | `dws doc list`; read concrete制度 files. |

## Intent Router

| Internal intent | Query signals | Preferred linked sources | Output focus |
|---|---|---|---|
| Risk scan | 哪些项目有风险, 红黄灯, 风险点, 需要关注 | [成果转化台账](https://alidocs.dingtalk.com/i/nodes/mweZ92PV6MEDQxX2TK9k61YLWxEKBD6p), [学生项目台账](https://alidocs.dingtalk.com/i/nodes/LeBq413JAwg9XNKxTrneNzD2WDOnGvpb), [教师项目台账](https://alidocs.dingtalk.com/i/nodes/NkDwLng8ZLgaGpDnUxjBGwvMVKMEvZBY), [项目目录](https://alidocs.dingtalk.com/i/nodes/DnRL6jAJMGnLY02jhXk0XDkxWyMoPYe1) | Rank by risk/urgency; include source freshness. |
| Pending decisions | 需要我拍板, 本周决策, 待协调 | [成果转化台账](https://alidocs.dingtalk.com/i/nodes/mweZ92PV6MEDQxX2TK9k61YLWxEKBD6p), [项目目录](https://alidocs.dingtalk.com/i/nodes/DnRL6jAJMGnLY02jhXk0XDkxWyMoPYe1), [对外合作](https://alidocs.dingtalk.com/i/nodes/nYMoO1rWxaXr3E5KczAZqd7pV47Z3je9) | Decision list: item, owner, needed action, deadline. |
| Single project status | 某项目进展, 到哪一步, 卡在哪里 | [项目目录](https://alidocs.dingtalk.com/i/nodes/DnRL6jAJMGnLY02jhXk0XDkxWyMoPYe1), [成果转化台账](https://alidocs.dingtalk.com/i/nodes/mweZ92PV6MEDQxX2TK9k61YLWxEKBD6p), [创业对接 SOP](https://alidocs.dingtalk.com/i/nodes/NDoBb60VLQmYbRpMhByE0BwZJlemrZQ3) | Stage, latest progress, blocker, next action. |
| Owner/blocker | 谁负责, 哪个部门卡住, 谁没推进 | [成果转化台账](https://alidocs.dingtalk.com/i/nodes/mweZ92PV6MEDQxX2TK9k61YLWxEKBD6p), [项目目录](https://alidocs.dingtalk.com/i/nodes/DnRL6jAJMGnLY02jhXk0XDkxWyMoPYe1), [对外合作](https://alidocs.dingtalk.com/i/nodes/nYMoO1rWxaXr3E5KczAZqd7pV47Z3je9) | Use source language; avoid unsupported blame. |
| Conversion path | 许可, 转让, 作价入股, 转化路径 | [研究院科技成果转化管理办法](https://alidocs.dingtalk.com/i/nodes/np9zOoBVBYMDpk4xhLrbp9DEW1DK0g6l), [学院科技成果转化管理办法](https://alidocs.dingtalk.com/i/nodes/P0MALyR8klYzXE5AtK6PXkwYW3bzYmDO), [研究院知识产权管理办法](https://alidocs.dingtalk.com/i/nodes/ZQYprEoWon4xZEA2hDKjrnrg81waOeDk) | Compare routes, prerequisites, missing materials. |
| Financing readiness | 哪些项目适合融资, 投资机构, VC匹配 | [项目目录](https://alidocs.dingtalk.com/i/nodes/DnRL6jAJMGnLY02jhXk0XDkxWyMoPYe1), [成果转化台账](https://alidocs.dingtalk.com/i/nodes/mweZ92PV6MEDQxX2TK9k61YLWxEKBD6p), [VC联系表](https://alidocs.dingtalk.com/i/nodes/y20BglGWO2RxyKZkt0oQw2048A7depqY), [孵化项目对外版PPT0526](https://alidocs.dingtalk.com/i/nodes/7QG4Yx2JpLvxaE5eUggMDk3zJ9dEq3XD) | Candidate ranking and fit logic; do not dump contacts. |
| Cooperation progress | 外部合作, 合作方, 对方动作 | [对外合作](https://alidocs.dingtalk.com/i/nodes/nYMoO1rWxaXr3E5KczAZqd7pV47Z3je9), [项目目录](https://alidocs.dingtalk.com/i/nodes/DnRL6jAJMGnLY02jhXk0XDkxWyMoPYe1) | Partner, current stage, next owner, risk. |
| Policy basis | 制度依据, 条款, 流程依据 | [制度](https://alidocs.dingtalk.com/i/nodes/LeBq413JAwg9XNKxTrQmg3rMWDOnGvpb) | Source, applicable scenario, manual confirmation caveat. |

## Tool Commands

```bash
dws doc read --node <doc_node_id> --format json --timeout 60
dws doc list --folder <folder_node_id> --format json --timeout 60

# AI 表格（ABLE），如 VC 联系表：先搜 base，再取表结构，再按需查少量记录。
dws aitable base search --query '<表格名>' --format json --timeout 60
dws aitable base get --base-id <base_id> --format json --timeout 60
dws aitable record query --base-id <base_id> --table-id <table_id> --limit 20 --format json --timeout 60
```

Known tool behavior: `VC联系表` can be located with `dws aitable base search --query 'VC联系表'`. Several project台账 links appear as `dlink`; `dws doc read` may fail. Mark that as a data-access limitation rather than a business conclusion.

## Leadership Answer Template

```text
一句话结论：当前最需要关注的是【项目/事项】的【风险/卡点】。

1. 高风险/重点事项
- 项目：...
- 当前阶段：...
- 风险/卡点：...
- 影响：...
- 责任人/部门：...
- 下一步：...

2. 待领导决策
- ...

3. 需要补充确认
- ...（缺字段/读不到/更新时间不明）

4. 来源与可信度
- [资料名](钉钉链接)，更新时间：...，可信度：高/中/低。
```

## Quality Bar

- Default to Chinese and lead with the decision-relevant conclusion.
- Prefer top 3-5 items over raw dumps.
- Include linked sources and freshness; never cite bare filenames only.
- Say “无法确认最新状态” when the source is unreadable or lacks update time.
- Use “资料显示/台账显示” for responsibility statements; do not infer blame.
- Minimize sensitive disclosure: phone numbers, personal contacts, and full VC lists should not be included unless explicitly necessary and internal.
- If output will be used externally, switch to `chanfu-external-qa` scope.
