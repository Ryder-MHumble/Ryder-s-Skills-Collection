---
name: kol-interview-to-wiki
version: 3.0
trigger: 当用户提供 YouTube 视频 URL 并要求分析/提炼/写入文档时自动激活；或每日自动扫描信源频道时激活
description: YouTube KOL 访谈 → 结构化深度分析 → 飞书 wiki 子文档。支持两种触发：手动给 URL 或每日自动扫描信源。纯 API 获取逐字稿和元信息，按内容流分章节而非观点清单，逐字稿原文用 code block 佐证。
---

# KOL 访谈 → 飞书 Wiki 全流程

## 前置条件

| 依赖 | 路径 | 用途 |
|------|------|------|
| youtube-transcript-api | `/opt/anaconda3/bin/python3` | 获取逐字稿 |
| yt-dlp | `/opt/anaconda3/bin/yt-dlp` | 获取元信息 + 频道扫描 |
| lark-cli | `/opt/homebrew/bin/lark-cli` | 飞书 wiki 创建子节点 + 写入文档内容 |
| scan_youtube.py | `scripts/scan_youtube.py` | 信源频道扫描脚本 |

---

## 模式 A：手动触发（用户给 URL）

用户发送 YouTube URL → 跳到 Step 2。

## 模式 B：每日自动扫描

### Step 0: 扫描信源频道

```bash
/opt/anaconda3/bin/python3 ~/.hermes/skills/research/kol-interview-to-wiki/scripts/scan_youtube.py 2>&1
```

读取 `/tmp/youtube_scanner_results.json` 获取结构化结果。

**三层漏斗**：

| 层级 | 条件 | 动作 |
|------|------|------|
| Tier 1 🔴 | 大佬名字命中（≥5min，非新闻评论） | 自动跑全流程（Step 2-7），优先级最高 |
| Tier 2 🟡 | AI关键词命中 OR 高信噪比频道+长视频(≥15min) | 自动跑全流程（Step 2-7），优先级次之 |
| Tier 3 | <5min / 无命中 | 跳过 |

**每日全流程上限 = 3 个**（Tier 1 + Tier 2 合计），避免 cron 超时或限流。Tier 1 优先处理，Tier 2 其次。超出部分记入待处理队列（pending_queue），次日优先处理。

对每个 Tier 1/Tier 2 视频（already_wiki=false），按 Step 2-7 执行。

⚠️ **关键：Tier 2 也要自动跑全流程**，不要停在推荐列表。整个 cron 流程必须是 扫描→发现→获取逐字稿→深度分析→写飞书wiki 一条龙完成。

---

## Step 1: 解析 YouTube ID

从 URL 提取 video ID（11位字符）。支持格式：
- `https://www.youtube.com/watch?v=XXXXX`
- `https://youtu.be/XXXXX`
- `https://www.youtube.com/watch?v=XXXXX&t=15s`

## Step 2: 获取逐字稿

```python
/opt/anaconda3/bin/python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
ytt = YouTubeTranscriptApi()
transcript = ytt.fetch('VIDEO_ID')
with open('/tmp/transcript_VIDEO_ID.txt', 'w') as f:
    for entry in transcript:
        mins = int(entry.start // 60)
        secs = int(entry.start % 60)
        f.write(f'[{mins:02d}:{secs:02d}] {entry.text}\n')
"
```

**错误处理**：
- `NoTranscriptFound` → 尝试：`ytt.fetch('VIDEO_ID', languages=['en', 'zh-Hans', 'zh-Hant'])`
- `VideoUnavailable` → 私人/删除视频，告知用户
- 无任何字幕 → 终止流程，标注"无字幕"
- `ImportError: cannot import name 'fetch'` → API 已升级，必须用 `YouTubeTranscriptApi().fetch()` 而非直接 `from youtube_transcript_api import fetch`

## Step 3: 获取元信息

```bash
/opt/anaconda3/bin/yt-dlp --dump-json --no-download URL 2>/dev/null | /opt/anaconda3/bin/python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'Title: {d[\"title\"]}')
print(f'Channel: {d[\"channel\"]}')
print(f'Duration: {d[\"duration\"]//60}min')
print(f'Upload: {d[\"upload_date\"]}')
print(f'Description: {d[\"description\"][:500]}')
"
```

## Step 4: 深度分析逐字稿

**读取全文** → 用 read_file 分批读（每批 2000 行），全部加载到上下文。

**分析原则**：
1. **按内容流分章节**（一、二、三…），不按「观点 1、观点 2…」流水账
2. 每个章节标题从内容矛盾/主题中产生，不用维度标签
3. 每个核心判断必须附带逐字稿原文佐证（带时间戳 `[MM:SS]`）
4. 顶部用一句话核心判断概括整场访谈的赌注
5. 叙事有弧线，章节之间有过渡

**语言检测**：
- 逐字稿为英文 → 中文分析 + 英文原文佐证
- 逐字稿为中文 → 中文分析 + 中文原文佐证
- 混合 → 以逐字稿主体语言为准

## Step 5: 创建飞书 wiki 子文档

```bash
cd /tmp && lark-cli wiki +node-create \
  --parent-node-token Pkf4wt3SgiSCxXk4gufceNIpnBe \
  --title "KOL名: 视频标题" \
  --as user
```

记录返回的 `obj_token`（即 doc_id）和 wiki `node_token`。

## Step 6: 写入文档内容

用 lark-cli api 分批写入，每批 3-5 个 block。

**飞书 docx block 类型速查**：

| 类型 | block_type | 字段名 | 用途 |
|------|-----------|--------|------|
| 文本 | 2 | `text` | 正文段落 |
| H1 | 3 | `heading1` | 章节标题（一、二、三…） |
| H2 | 4 | `heading2` | 子标题（1.1、1.2…） |
| Code | 14 | `code` | 逐字稿原文佐证（**必须设 `style.wrap: true`**） |
| Quote | 15 | `quote` | 核心判断/金句 |
| Divider | 22 | `divider` | 分隔线 |

**写入 API**：
```bash
cd /tmp && lark-cli api POST \
  "/open-apis/docx/v1/documents/DOC_ID/blocks/DOC_ID/children" \
  --as user --data @batch_file.json
```

⚠️ `--data @file` 必须用**相对路径**，先 `cd /tmp`。

## Step 7: 更新状态

将视频 ID 记入 wiki_ids：
```python
/opt/anaconda3/bin/python3 -c "
import json
from pathlib import Path
state_file = Path('/Users/sunminghao/.hermes/cache/youtube_scanner_state.json')
state = json.loads(state_file.read_text())
if 'wiki_ids' not in state: state['wiki_ids'] = []
state['wiki_ids'].append('VIDEO_ID')
state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2))
"
```

---

## 文档结构模板

```
[Quote] 核心判断一句话（含赌注描述）
[Quote] —— KOL名, 来源+年份
[Text] 视频链接：https://www.youtube.com/watch?v=XXX
[Text] 概述：时间、场合、对话者、核心赌注
[Text] 主题脉络：4-6 个核心章节线索

[H1] 一、章节标题（从内容矛盾中产生）
  [H2] 1.1 子标题
  [Text] 分析段落（中文）
  [Code] [MM:SS] 逐字稿原文（不翻译）
  ...

[Divider]
[Text] 元信息（加粗）
[Code] 标题 / 频道 / 发布时间 / 时长 / YouTube链接 / 分析时间
```

---

## 每日汇报格式（模式 B 专用）

```
📡 KOL Intelligence — YYYY-MM-DD

🔴 Tier 1 已处理（N个）
  • 视频标题 — 飞书wiki链接
  ...

🟡 Tier 2 已处理（N个）
  • 视频标题 — 飞书wiki链接
  ...

⏳ 待处理队列（N个，次日优先）
  • 标题 (Xmin) — 频道
    https://youtube.com/watch?v=XXX
  ...
```

## 用户反馈与改进（2025-05-27）

用户对技能改进提出以下建议，已部分采纳：

1. **逐字稿质量门控**：用户指出 YouTube 自动生成字幕的技术内容术语可能不准，目前测试只有手动点击 Obsidian web clipper 导出的逐字稿质量较好。暂时保持现状，未来可考虑质量检查（条目数/总时长比）。

2. **跨频道去重**：用户认为当前监控的 13 个信源频道出现内容重复的概率较低，暂不需要 YouTube 全网检索去重。

3. **Tier 2 → Tier 1 升级路径**：用户建议将自动扫描与 wiki 生成流程更紧密集成。已实现：Tier 2 推荐列表中的视频，用户回复视频 ID 即可触发深度分析。

4. **Cron prompt 精简**：用户同意将冗长的流程描述从 cron prompt 中移除，改为引用 skill 文件。已优化：cron prompt 仅保留 `load skill → 执行模式 B` 指令。

5. **每日全流程上限**：用户确认上限合理，建议分批次处理。已实现：超出部分写入 `pending_queue`，次日优先处理。**2026-05-28 修正**：Tier 2 也必须自动跑全流程不停在推荐列表，上限从 Tier 1 单独 2 个调整为 Tier 1+Tier 2 合计 3 个

6. **执行时间偏好**：用户明确要求定时任务改为**每天早上北京时间十点**运行。已在 cron job 中设置 `0 10 * * *`。

7. **信源筛选确认**：用户确认使用提供的 13 个 YouTube 频道/播放列表作为信源，无需额外筛选。

---

## 关键约束

1. **逐字稿原文不翻译**——英文逐字稿就用英文原文放进 code block
2. **code block 必须带时间戳**——格式 `[MM:SS]` 放在原文开头
3. **code block 用 block_type 14**（不是 23），字段名 `"code"`，**style 必须包含 `"wrap": true` 以启用换行**
4. **quote block 用 block_type 15**，字段名 `"quote"`（不是 `"callout"`）
5. **lark-cli 必须用 `--as user`**
6. **分批写入**——每批 3-5 个 block，验证 `"code": 0`
7. **叙事弧线**——章节之间有逻辑递进，不是并列清单
8. **章节标题从矛盾中产生**——不用维度标签
9. **每日全流程上限 = 3**——Tier 1 + Tier 2 合计，超出降级为待处理队列，次日优先。Tier 2 也必须自动跑全流程（Step 2-7），不停在推荐列表
10. **执行时间偏好**——每日自动扫描在**北京时间早 10:00**运行，符合用户明确要求

## ⛔ 反模式（用户明确纠正过）

1. **观点清单流水账** — "观点1: xxx / 观点2: xxx" 是错的。按内容流分章节，章节有叙事弧线
2. **逐字稿用 text block 加引号** — 必须用 code block (type 14)
3. **block_type 23** — 不可用，code block 是 type 14
4. **quote block 字段名** — 是 `"quote"`，不是 `"callout"`
5. **heading 字段名错误** — block_type 3 的字段是 `heading1`（不是 `heading2`），block_type 4 才是 `heading2`。用错会报 invalid param

## 已知坑

- **一级标题**: `{"block_type": 3, "heading1": {"elements": [{"text_run": {"content": "一、..."}}], "style": {}}}`
- **二级标题**: `{"block_type": 4, "heading2": {"elements": [{"text_run": {"content": "1.1 ..."}}], "style": {}}}`
- ⚠️ block_type 3 字段名是 `heading1`（不是 heading2），block_type 4 字段名是 `heading2`。之前因用错字段名导致 API 报 invalid param
- **Code block 必须带 wrap 换行**：`{"block_type": 14, "code": {"elements": [{"text_run": {"content": "[MM:SS] ..."}}], "style": {"language": 1, "wrap": true}}}` — `wrap: true` 让逐字稿自动换行渲染，不设则默认单行溢出隐藏
- **divider 必须带空 body** — `{"block_type": 22, "divider": {}}`
- **每批最多 4-5 个 block**，批次间 sleep 1.2s，避免 API 超时
- **推荐用 delegate_task subagent 执行写入**，避免主对话超时
- **Python 字符串中的引号**：中文引号用「」而非 ""，避免转义问题；code block 中的英文引号保留原样
- `youtube_transcript_api` 和 `yt-dlp` 不在 hermes venv 中，必须用 `/opt/anaconda3/bin/python3`
- lark-cli `--data @file` 不支持绝对路径，必须用相对路径
- wiki 节点删除用 `lark-cli wiki +node-delete --node-token TOKEN --obj-type wiki --as user --yes`
- 逐字稿条目可能很大（900+），先保存到文件再分批读取
- **逐字稿质量门控**：youtube-transcript-api 抓取的是自动生成字幕，技术内容术语可能不准，质量不稳定。用户反馈目前只有 Obsidian web clipper 导出的逐字稿质量较好。未来可考虑添加质量检查（如条目数/总时长比 < 5 条/分钟则跳过）
- scanner `--flat-playlist` 拉频道所有历史视频，靠 days=3 + processed_ids 去重
- **youtube_transcript_api 版本变更**：旧版 `from youtube_transcript_api import fetch` 已不可用，必须改为 `from youtube_transcript_api import YouTubeTranscriptApi; ytt = YouTubeTranscriptApi(); transcript = ytt.fetch('VIDEO_ID')`。直接 import fetch 会报 ImportError
- **cron 代理依赖**：yt-dlp 和飞书 API 都可能走系统代理（127.0.0.1:7890），如果代理未运行则全部失败。cron 执行前需确认代理可用，或在 yt-dlp 配置中设置 `--no-proxy`（但飞书 API 可能仍需代理）

## Cron Job

- **Job ID**: `0d5ca3142ca6`
- **Schedule**: `0 10 * * *`（每天早 10:00 北京时间）
- **触发**: 加载本 skill → 执行模式 B 全流程
