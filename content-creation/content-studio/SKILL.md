---
name: content-studio
description: "Use when producing social media content (X / 小红书 / 抖音 / B站) for personal IP building or project marketing. Generates 4-platform content packs with copy text, video scripts, and HTML/CSS card templates with Ryder's avatar (黑色皮夹克二次元男性) integrated as the visual anchor. Two visual modes: simple (极简) and complex (brutalist 杂志风, 8 元素中心+边缘张力). Each mode has 3 templates: cover + content + ending. 4 content types: AI产品推荐 / GitHub深度分析 / 热点事件讲解 / 日常感悟. HTML templates are contenteditable, browser-editable, render to PNG via Chrome headless."
version: 4.9.3
author: Ryder
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [social-media, content, marketing, personal-ip, xiaohongshu, twitter, card-generator, ip-branding, brutalist, magazine]
    related_skills: [brandkit, high-end-visual-design, industrial-brutalism-ui, popular-web-designs, baoyu-infographic, humanizer]
---
> **Codex Adaptation Notes**: This skill was originally designed for Hermes Agent. When running in Codex CLI, map Hermes tools to shell equivalents:
> - `write_file(path, content)` → `cat > path << 'HEREDOC' ... HEREDOC` or Python `Path(path).write_text(content)`
> - `read_file(path)` → `cat path` or Python `Path(path).read_text()`
> - `search_files(pattern, path)` → `grep -rn "pattern" path/` or `find path/ -name "*pattern*"`
> - `patch(path, old, new)` → `sed -i 's/old/new/g' path` or Python string replace
> - `terminal(command)` → run shell commands directly
> - `delegate_task(goal)` → do the work directly in the main session (no subagent delegation in Codex)
> - `browser_navigate/click/type` → use `curl` for HTTP requests; browser interaction not available
> - `send_message` → not applicable; output to stdout/files instead
> - Hermes memory → use `~/.codex/memories/` or project AGENTS.md
> - Paths: `~/.hermes/skills/` → `~/.codex/skills/` (this skill's own directory)



# Content Studio v4.8.0 — 4 平台 + 4 内容类型 + 双模式卡片模版

> **从「写一条帖子」升级到「建一个 IP」**。4 平台内容生产（图文+视频）+ HTML/CSS 卡片模版。
> 核心：**个人 IP 长期运营**（不是单次项目宣传）。
> **v4.8**：4 平台（X/小红书/抖音/B站）+ 4 内容类型方法论 + 平台画像分析。Complex 模版 v2 重设计（8 元素，删 6 个纯装饰）。快手已移除（用户画像不匹配）。

## v4.6 双模式范式（核心）

封面 = 标题替代品（用户先看封面，再决定点不点）。
**封面有两种模式，默认用 simple，复杂用 complex。**

| 模式 | 触发 | 元素数 | 适合场景 | 实现 |
|------|------|--------|---------|----------|
| **simple**（默认） | 日常推文、快节奏 | 5 元素（米黄底+网格 / ID 标签 / 3 行主标题 / 副标 / 头像） | KOL 库日常更新、临场感内容、个人 IP 软广 | `render_cover_simple()` |
| **complex** | 重要发布、爆款冲量 | 8 元素（brutalist 杂志风 v2：16px 厚黑边 / 3 行多色 box / ID 卡+角标 / stamp / RYDER 卡 / 条形码） | 项目首发、产品 launch、需要"看起来很专业"的内容 | `render_cover_complex()` |
| **KOL 卡片（v4.7 新增）** | KOL 库定期发布 | 10 元素（标题居中 + 边缘装饰保留 brutalist 不对称） | KOL INTEL 周报、IP 长期运营的可复用模板 | HTML+CSS 模板（`references/visual/kol-card-template.html`） |

**关键认知**：
- 封面在信息流里 3 秒定生死，**封面比标题还重要**
- simple 模式适合**日常高频**（一周 3-5 条），视觉清爽不疲劳
- complex 模式适合**重要发布**（一月 1-2 条），杂志 brutalist 风冲量
- KOL 卡片适合**KOL 库周报**（一期一卡，长期 IP 沉淀）
- 内页 = **信纸留白**（两种模式共用），用户后续自己 P 图

> **用户决定（2026-06-17）**：KOL 卡片模板的设计方向——**「标题居中 + 边缘装饰保留 brutalist 不对称」**。区别于 complex 模式：complex 是「3 个不对称的 box 块堆叠」，KOL 卡片是「3 行居中的 box 块 + 边缘装饰保持张力」。两种模式不混淆，按场景选。

> **用户决定（2026-06-17）**："现在这个可以做成一个简易模式的模版，复杂模式可以参考 xhs-brutalist-cards 的相关 html、css，默认用简易模式，在 skill 中规范好，其他风格可以先不要，就要两种模式的这一套模版就好"

## v4.7 双模版定稿（2026-06-17）

> **状态**：✅ 已完成。simple + complex 两套 HTML/CSS 模版定稿，每套 3 张（封面/内容卡/结尾卡）。Ryder 视觉确认通过后可同步 PIL。

**核心改动**：complex 模式从 14 元素砍到 **8 元素**，解决 v4.6「全部贴边堆叠 = 视觉过满 + 毫无审美」的问题。

**模版目录结构（v4.7 定稿）**：

```
references/templates/
├── simple/                    # 简易版（保持 v4.6 设计语言）
│   ├── style.css              # 共享样式（米黄底+网格）
│   ├── cover.html             # 封面（ID标签 + 3行钩子 + 副标题 + 大圆头像）
│   ├── content.html           # 内容卡（页眉ID+页码 / 正文区 / 底部签名）
│   ├── ending.html            # 结尾卡（收尾语 + 头像 + CTA + ID标签）
│   └── avatar.png             # 头像（已复制到目录内）
├── complex/                   # 复杂版（重新设计）
│   ├── style.css              # 共享样式（信纸底+厚黑边）
│   ├── cover.html             # 封面（8 元素，见下）
│   ├── content.html           # 内容卡（黑条页眉 / 正文+引用框 / 底部签名）
│   ├── ending.html            # 结尾卡（收尾语 + 头像 + CTA + 底部签名行）
│   └── avatar.png
└── (旧 cover-template.html / style.css 保留，未删)
```

**complex 封面 8 元素清单**（v4.7 定稿）：

| # | 元素 | 位置 | 功能 |
|---|------|------|------|
| 1 | ID 卡片 | 左上贴边 | 头像+账号名（红投影） |
| 2 | KOL 编号角标 | 右上贴边 | 黑底红编号（04 KOL INTEL） |
| 3 | 主标题 3 行 | 居中 | 米白/黑/红 box，硬投影，视觉重心 |
| 4 | 副标题 | 居中 | 米白+黑边+红投影 |
| 5 | 头像 | 居中偏下 | 圆形，黑色硬投影 |
| 6 | 期号 stamp | 左下贴边 | 红底+编号+元数据 |
| 7 | RYDER 签名卡 | 右下贴边 | 米白+黑边+红投影 |
| 8 | 条形码 | 底部居中 | 纯装饰 |

**删除的 6 个元素**（v4.6 有 → v4.7 删）：红方块左上、斜切角右下、4 个 + 标记、meta-rail 横线+tick、黑红条纹、footer 文字行。删除原因：重复装饰无功能价值，堆砌导致凌乱。

**设计原则**：
- 内容（标题/副标题/头像）= 居中 → 视觉重心稳
- 装饰（ID 卡/角标/stamp/RYDER 卡）= 贴边不对称 → brutalist 节奏感
- 硬投影无 blur：红/黄/黑三色，按重要性递减
- 每个元素都有明确功能，**无重复无意义元素**
- 标题与底部之间大量留白 → 呼吸感

## 设计/内容分离：HTML 模版工作流（v4.6+）

**核心理念**：PIL 端 `render_cover_complex` / `render_inside` 输出是 **基准视觉**，HTML/CSS 模版是 **可编辑设计稿**，两者**视觉一致**。

**触发场景**（用户原话常带这些词）：
- "重新设计排版布局" — 实际指"做设计稿（HTML/CSS 模版）"，**不是**改设计
- "做成可复用的模版" — 指 `contenteditable` 槽位化的 HTML
- "提取内容往里加" — 未来新主题时只改 HTML 文字，不动 CSS / PIL
- "参考 xhs-brutalist-cards 那种 html/css" — 要的是设计稿形式，不是改 PIL

**工作流**：
1. **以 PIL 端输出为基准** — 不要改 `card_generator.py`
2. **写 HTML 模版**（`references/templates/cover-template.html`）— 用 `contenteditable="true"` 标注所有可编辑槽位
3. **写 CSS**（`references/templates/style.css`）— 视觉规范 1:1 对齐 PIL 坐标（1200×1600 卡片尺寸直接对应 `ASPECT_RATIOS["3:4"]`）
4. **跑 HTML 截图对比 PIL 输出** — Playwright `page.screenshot(clip=...)` 精确裁剪，验证视觉一致
5. **更新 README** — 列出槽位对照表（class 名 → 占位文字 → 用户替换内容）

**brutalist 风格硬性约束**（complex 模式 v2，8 元素 baseline）：
- 3 行主标题 + 副标题：水平居中
- 其他元素**贴边 / 错位 / 不居中**：
  - ID 卡（左贴）+ KOL 角标（右贴）
  - stamp（左下贴）+ RYDER 签名卡（右下贴）
  - 条形码（底部居中）
- **不要自动居中**副标题 / 头像 / 装饰元素
- **v4.8 删除的 6 个纯装饰元素**（红方块左上、斜切角右下、4 个 + 标记、meta-rail 横线+tick、黑红条纹、footer 文字行）—— Ryder 原话：「页面中禁止出现重复的以及无意义的元素」
- **每个元素必须有明确功能**，无重复无意义元素

## When to Use

- 用户要发 **X / 小红书 / 抖音 / B站** 的内容
- 用户要为某个项目做**多平台内容包**（图文 + 视频）
- 用户要**个人 IP 长期运营**
- 用户要基于一段文字**生成卡片截图**用于社媒
- 用户要做**短视频/长视频脚本**（抖音/B站）

**不要用**：
- HTML 网页 / Slide Deck → `claude-design` 或 `doc-to-slide`
- 单张大信息图 → `baoyu-infographic`
- 品牌 VI 系统 → `brandkit`
- 已有内容去 AI 味 → `humanizer`

## 三大能力模块

### 1. 内容生产（文案 + 视频脚本）

**图文平台**：
- **X**：独狼帖（≤ 280 字符，6 sub-style 选 1）+ Thread（4 条）→ `references/platforms/x.md`
- **小红书**：标题（≤ 20 字，A/B/C 候选）+ 正文（≤ 300 字）+ 5 标签 → `references/platforms/xiaohongshu.md`

**视频平台**：
- **抖音**：15-60s 短视频口播脚本（黄金3秒 + 价值密度 + CTA）→ `references/platforms/douyin.md`
- **B站**：5-15min 长视频分镜脚本（开场白 + 深度分析 + 弹幕互动）→ `references/platforms/bilibili.md`

**4 种内容类型**（跨平台适配）：
- AI产品推荐 / GitHub深度分析 / 热点事件讲解 / 日常感悟 → `references/content-types.md`

**通用框架**：
- **心理钩子**：7 大钩子 → `references/frameworks/psychological-hooks.md`
- **个人 IP**：IP 打造框架 → `references/frameworks/personal-ip.md`
- **平台画像 + 账号定位**：4 平台用户画像分析 + ID/简介/视觉风格/内容策略建议 → `references/platform-audit.md`
- **反模式**：7 大原则，不说"我能做什么"、不堆功能、不写"怎么用"

### 2. 视觉卡片生成（`scripts/card_generator.py` + HTML/CSS 模版）

| 类型 | 模式 | 模版文件 | 输出 |
|------|------|---------|------|
| cover | simple | `references/templates/simple/cover.html` | `cover.png` |
| cover | complex | `references/templates/complex/cover.html` | `cover_complex.png` |
| content | simple | `references/templates/simple/content.html` | `cards/02-05.png` |
| content | complex | `references/templates/complex/content.html` | `cards/02-05.png` |
| ending | simple | `references/templates/simple/ending.html` | `cards/end.png` |
| ending | complex | `references/templates/complex/ending.html` | `cards/end.png` |

**支持 6 种宽高比**：1:1 / 3:4 / 4:3 / 9:16 / 16:9 / 2:3

### 2.1 专题模板（Series Templates）

当用户提到固定栏目/系列名时，优先使用专题模板，而不是通用 simple/complex 卡片。

| 专题 | 模板目录 | 内容定位 |
|------|----------|----------|
| AI时代的碎碎念 | `references/templates/series/`（观点型，沿用图集证据卡规范） | AI 时代社会观察、机制解释、观点输出 |
| 一分钟打假一个 GitHub 热门项目 | `references/templates/series/github-factcheck/` | GitHub 热门项目事实核查：repo 数据、issue、代码证据、benchmark、测试报告 |
| Ryder的工具集推荐 | `references/templates/series/`（待扩展） | 工具推荐、真实使用体验、适用/不适用边界 |

**GitHub 打假专题硬性要求**：
- 封面固定为栏目模板：主标题放系列名 `一分钟打假一个 GitHub 热门项目`，副标题放本期强钩子，下方放 GitHub 项目主页首屏截图，页脚保留期号和 `GITHUB FACTCHECK`。
- 内页采用 `claim → evidence → implication`：每张卡只讲一个复核点。
- 证据必须来自 repo 数据、issue、代码 grep、benchmark、docs 或本地测试报告。
- 不要把大段终端输出当正文；终端块只放 3-5 行关键证据。
- 先用 `capture_github_project_page.py` 截 GitHub 项目主页首屏，再用 `render_github_factcheck.py` 的 PIL 模板渲染；内容溢出时直接报错，避免浏览器截图裁切。
- 小红书正文不要围绕“打假”这个词写；写成“大家都在吹的时候，我帮你慢半拍看一眼”：先给刷到热门项目的体感，再给明确判断，再给读者可复用的三问法。

## 快速开始

### HTML/CSS 模版（v4.7 推荐）

```bash
# 浏览器直接编辑（双击 contenteditable 区域改文字）
open references/templates/simple/cover.html
open references/templates/complex/cover.html

# 渲染为 PNG（见下方「Chrome headless 渲染实战」节）
```

模版槽位对照表见 `references/templates/v4.7-template-guide.md`。

### CLI 用法（PIL 渲染，v4.6 baseline）

```bash
# 简易模式封面（默认）
python card_generator.py \
  --type cover --mode simple \
  --hook "高段位 AI\n决策者都应该有\nKOL 情报库" \
  --sub "2 小时访谈 → 5 分钟笔记" \
  --aspect 3:4 -o cover.png

# 复杂 brutalist 模式封面
python card_generator.py \
  --type cover --mode complex \
  --hook "高段位 AI\n决策者都应该有\nKOL 情报库" \
  --sub "2 小时访谈 → 5 分钟笔记" \
  --aspect 3:4 -o cover.png

# 内页（信纸版）
python card_generator.py --type inside --page 2 --total 5 \
  --aspect 3:4 -o inside.png
```

### Python API

```python
from card_generator import render_cover_simple, render_cover_complex, render_inside

# 简易模式
img = render_cover_simple(
    w=1200, h=1600,
    hook="高段位 AI\n决策者都应该有\nKOL 情报库",
    sub_hook="2 小时访谈 → 5 分钟笔记",
    avatar_path="assets/avatar.png",
)
img.save("cover.png", "PNG")

# 复杂模式
img = render_cover_complex(
    w=1200, h=1600,
    hook="高段位 AI\n决策者都应该有\nKOL 情报库",
    sub_hook="2 小时访谈 → 5 分钟笔记",
    avatar_path="assets/avatar.png",
)
img.save("cover_complex.png", "PNG")

# 内页
img = render_inside(
    w=1200, h=1600,
    avatar_path="assets/avatar.png",
    page_num=2, total_pages=5,
)
img.save("inside.png", "PNG")
```

## 视觉规范

### Simple 模式（`references/templates/simple/`）

**配色**：BG `#F5F0E1` / FG `#0A0A0A` / WHITE `#FFFFFF` / RED `#E63946`

**封面 5 元素**：米黄底+网格 → ID标签（左上）→ 3行钩子句（KOL红色高亮+红下划线）→ 红框副标题 → 大圆头像（居中，双层黑色硬投影）

**内容卡**：顶部页眉（ID+页码，黑横条+红线）→ 正文区（红色左边框 section title + 正文 + 高亮 + 引用框）→ 底部签名（黄线+签名+期号）

**结尾卡**：居中收尾语（红色高亮）→ 红色分隔线 → 头像 → CTA 红框 → ID 标签

### Complex 模式（`references/templates/complex/`，v4.7 重新设计）

**配色**：paper `#F1E2CC` / soft `#FFF9ED` / ink `#080808` / red `#F0442E` / yellow `#FFD72E`

**封面 8 元素**（v4.7 从 14 砍到 8）：
1. ID 卡片（左上贴边，红投影）
2. KOL 编号角标（右上贴边，黑底）
3. 主标题 3 行（居中，米白/黑/红 box，硬投影）
4. 副标题（居中，米白+黑边+红投影）
5. 头像（居中偏下，圆形硬投影）
6. 期号 stamp（左下贴边，红底）
7. RYDER 签名卡（右下贴边，米白+红投影）
8. 条形码（底部居中，纯装饰）

**内容卡**：黑条页眉（头像+ID+页码）→ 正文区（section title + 引用框 + 高亮）→ 底部签名行

**结尾卡**：居中收尾语 → 红色分隔线 → 头像 → CTA 红框 → 底部签名行（END stamp + RYDER chip）

**v4.7 删除的 6 个元素**：红方块左上、斜切角右下、4 个 + 标记、meta-rail 横线+tick、黑红条纹、footer 文字行。原因：重复装饰无功能价值，堆砌导致凌乱。

### 内页（信纸版）

**元素**：
1. 米黄底 + 网格（`#D4CCB8`，50px spacing）
2. 左侧 4 个装订孔（白边红圆）
3. 顶部 header（黑横条 + 红线）+ ID 标签 + 页码 "KOL 情报库 | 02/05"
4. 主体 100% 留白（**不画任何内容**，用户 P 图）
5. 底部 footer（黄线 + Ryder's KOL Intelligence + 期号）

### KOL 卡片（v4.7 新增 · 标题居中 + 边缘不对称）

**设计核心**：标题居中（视觉重心）+ 边缘装饰保留 brutalist 不对称（节奏感）。区别于 complex 模式的「3 个不对称 box 块堆叠」——KOL 卡片是「3 行**居中**的 box 块 + 周边装饰保持张力」。

**文件**：
- `references/visual/kol-card-template.html` — 通用模板（contenteditable + 注释占位符）
- `references/visual/kol-card-style.css` — 独立样式（CSS 变量驱动）
- `references/visual/kol-04-cover.html` — KOL 04 实例（首期）

**元素清单**（10 个）：
1. 顶部左 ID 卡（米白底+红 LOGO+账号名）
2. 顶部右 KOL 编号角标（黑底+红数字 04+KOL INTEL 标签）
3. 红线分隔条
4. 头部左 头像（粗黑边+红硬投影）
5. 头部右 装饰方块（黄底+NEW 标签+No.04 大字）
6. 主标题 1（米白底+红投影，居中）
7. 主标题 2（黑底+白字+红投影，居中）
8. 主标题 3（红底+黑字+黄投影，居中，视觉最重）
9. 副标题盒（米白+黑边+红投影，居中）
10. 底部三元素：左 01 stamp + 中 条形码 + 右 RYDER 卡（不对称分布）

**画布**：1240×1654（3:4 竖图）

**使用方式**：
```bash
# 浏览器内直接编辑（contenteditable）
open references/visual/kol-card-template.html

# 或复制模板 → 重命名 → 替换内容
cp kol-card-template.html my-kol-cover.html
# 替换文字 + 改 src="./avatar.png"（同目录放头像）

# 导出 PNG（用 skill 自带的 macOS Chrome headless 脚本）
chmod +x scripts/render-html-to-png.sh
./scripts/render-html-to-png.sh my-kol-cover.html my-kol-cover.png 1240 1654
```

**配色变量**（`kol-card-style.css` `:root`）：
```css
--paper: #f1e2cc;   --soft: #fff9ed;   --ink: #080808;
--red: #f0442e;     --yellow: #ffd72e; --muted: #6d6255;
```

**与 complex 模式对比**：

| 维度 | complex | KOL 卡片 |
|------|---------|----------|
| 标题布局 | 3 个居中 box 块 | 3 个**居中** box 块 |
| 装饰元素 | 条形码（底部） | 头像+装饰方块（顶部不对称） |
| 用途 | 项目首发、爆款冲量 | KOL 周报、IP 长期运营 |
| 模板 | PIL 脚本 + HTML 模版 | HTML+CSS 模板（可复用） |

## CJK 字体处理

**核心问题**：PIL 的 `draw.textbbox()` 和 `font.getlength()` 对中文字符宽度估算不准（特别是 CJK + Latin 混排），容易导致文字溢出 box 右边。

**解决方案**：
```python
def true_text_width(text, font_size):
    """手算宽度：CJK=字号, Latin=字号*0.6, 空格=字号*0.4"""
    w = 0
    for c in text:
        if 0x4E00 <= ord(c) <= 0x9FFF or 0x3000 <= ord(c) <= 0x303F:
            w += font_size
        elif 0xFF00 <= ord(c) <= 0xFFEF:
            w += font_size
        elif c == " ":
            w += font_size * 0.4
        else:
            w += font_size * 0.6
    return int(w * 1.08)  # + 8% buffer

def text_size(draw, text, font, size):
    tw = true_text_width(text, size)
    try:
        fl = int(font.getlength(text))
    except:
        fl = 0
    w = max(tw, fl)  # 取较大值
    # 高度用 textbbox
    ...
```

**字体优先级**：
1. `Hiragino Sans GB.ttc`（macOS 系统 CJK）
2. `ArialHB.ttc`（macOS 系统）
3. `Helvetica.ttc`（macOS 系统）

详见 `references/implementation-notes.md` 和 `references/complex-mode-design-spec.md`（complex 模式设计 token 速查表）。

## 头像规范

**当前主头像**：`assets/avatar.png`（黑皮夹克、黑发戴眼镜、温柔帅气的二次元男性，1104×1072，1.7MB）
**旧版备份**：`assets/avatar.backup-二次元-Avatar.png`（橙毛衣生活化版）

**头像在封面中的作用**：
- simple 模式：中央大圆（直径 = 0.32 × 卡片宽），带 2 层黑色硬投影
- complex 模式：顶部 ID 卡片小圆（76×76），红底黑边黑投影
- 内页：装订孔同列，左上 ID 标签内置

**为什么头像在 IP 长期运营中至关重要**：
- 视觉锚点：用户刷信息流时，**头像比品牌名更易识别**
- 一致性：所有平台、所有内容都带同一头像 = 强 IP 印象
- 温度感：二次元头像比真人照更"温暖"，比抽象 logo 更"亲切"

详见 `references/visual/avatar-driven-design.md`。

## 持久化策略

**默认输出位置**：`~/workspace/hermes-output/content-studio/<主题名>/`

```
~/workspace/hermes-output/content-studio/
└── <主题名>/
    ├── xhs/
    │   ├── cover.png                    # 简易/复杂模式封面
    │   ├── cover_complex.png
    │   └── cards/
    │       ├── 02.png                   # 内容卡
    │       ├── 03.png
    │       ├── end.png                  # 结尾卡
    ├── x/
    │   └── thread.md                    # X 独狼帖/Thread
    ├── douyin/
    │   └── script.md                    # 抖音脚本
    └── bilibili/
        └── script.md                    # B站脚本
```

## 文件结构

```
content-studio/
├── SKILL.md                          # 本文件
├── README.md                         # 快速开始
├── scripts/
│   ├── card_generator.py             # 卡片生成器（PIL，simple+complex+inside）
│   ├── render-html-to-png.sh         # HTML→PNG 渲染脚本（macOS Chrome headless）
│   └── README.md                     # CLI 详细文档
├── references/
│   ├── implementation-notes.md       # CJK 字体实现笔记
│   ├── complex-mode-design-spec.md   # complex 模式设计 token 速查表
│   ├── grid-and-screenshot-pitfalls.md # CSS Grid + Playwright 截图坑
│   ├── content-types.md              # 4 内容类型 × 4 平台适配矩阵
│   ├── platform-audit.md             # 平台用户画像 + 账号定位策略
│   ├── visual/
│   │   ├── avatar-driven-design.md   # 头像驱动设计
│   │   ├── html-template-to-png.md   # HTML→PNG 渲染指南
│   │   ├── kol-card-template.html    # KOL 卡片模板（contenteditable）
│   │   ├── kol-card-style.css        # KOL 卡片独立样式
│   │   ├── kol-04-cover.html         # KOL 04 实例
│   │   └── kol-04-cover.png          # KOL 04 渲染结果
│   ├── platforms/
│   │   ├── x.md                      # X 平台规范（6 sub-style）
│   │   ├── xiaohongshu.md            # 小红书平台规范（风格钩子 + 图集文案）
│   │   ├── douyin.md                 # 抖音平台规范（短视频口播脚本）
│   │   └── bilibili.md               # B站平台规范（长视频分镜 + 弹幕互动）
│   ├── frameworks/
│   │   ├── personal-ip.md            # IP 长期运营框架
│   │   └── psychological-hooks.md    # 7 大心理钩子
│   └── templates/                    # HTML/CSS 模版（v4.7 定稿）
│       ├── simple/                   # 极简模式（封面+内容卡+结尾卡+avatar.png）
│       ├── complex/                  # Brutalist 杂志风（封面+内容卡+结尾卡+avatar.png）
│       ├── v4.7-template-guide.md   # 模版槽位对照表
│       ├── cover-template.html       # [旧] v1 PIL 对齐版（保留参考）
│       ├── style.css                 # [旧] v1 共享样式（保留参考）
│       └── README.md                 # 旧版模版说明
├── templates/                        # 文案/脚本模板
│   ├── x_thread.md                   # X 文案模板
│   ├── xiaohongshu_post.md           # 小红书文案模板
│   ├── douyin_script.md              # 抖音短视频脚本模板
│   └── bilibili_script.md            # B站长视频脚本模板
└── assets/
    ├── avatar.png                    # 主头像（黑皮夹克二次元）
    ├── avatar.backup-二次元-Avatar.png  # 旧版备份
    ├── colors.json                   # 配色（保留历史）
    └── fonts/
        └── README.md                 # 字体说明
```

## 反模式（v4 原则）

**7 大原则**：
1. **不说"我能做什么"** — 用户不关心工具，关心自己能不能解决问题
2. **不堆功能** — 一条帖子只讲 1 个核心数字 / 1 个反直觉点
3. **不写"怎么用"** — 工具上手难 = 工具问题，不是用户问题
4. **不强推产品** — 3 行内带 GitHub 链接，多了 = 油腻
5. **不讲原理** — 4 层维度分析 = 黑盒，不解释方法论
6. **不用形容词** — "高段位 AI 决策者"是定位词，"超厉害无敌好用"是形容词
7. **不预设人设** — Ryder 是 IP，不演"专家" / "老师" / "导师"

详见 `references/frameworks/personal-ip.md` 和 `psychological-hooks.md`。

### 8. 机构身份 = 信任锚点（v4.8 沉淀）

> **Ryder 原话**：「最好亮明一些身份，我是中关村人工智能研究院的AI产品经理...让人家知道这个人所在的单位是ai行业的顶级机构，那我的很多论点都更容易被相信」

- **社媒简介第一行 = 机构身份**（不是"热爱分享"也不是"全网同名"）
- 国家人工智能研究院在职 AI 产品经理 = 信任锚点。中文平台用"国家人工智能研究院在职AI产品经理"，英文平台用"AI PM at a national AI research institute"
- 4 平台简介模板（含机构身份）详见 `references/platform-audit.md` § 三 + `social-critique/references/persona-guide.md`
- **反模式**：简介不写机构 = 白白浪费信任锚点；写"研究员/产品经理"但不写单位 = 没有背书力

### 9. 人设指南 = 语言风格统一约束（v4.9 新增）

**生成任何社媒内容（文案/口播稿/视频脚本）前，必须读取 `social-critique/references/persona-guide.md`。** 该文件是 Ryder 社媒人设的 single source of truth，约束语言风格、标志性表达、禁用词汇、各平台语气微调。

**核心语言基调**：严谨但不冷漠，更不傲慢。展现的是专业性，不是优越感。

**关键约束**（详见 persona-guide.md §2-§5）：
- 禁用词汇清单（破冰话术/赋能/降维打击/无耻/求三连/不吹不黑等）—— 生成内容后必须 grep 自检 0 命中
- 标志性表达（"这不是你的错觉""省下的时间不归你归KPI"等）—— 偶尔自然使用，不刻意堆
- 各平台语气微调（B站亮身份+理论口语化，小红书砍理论+痛点共鸣，抖音1数据1金句，X英文独狼帖）
- 两种内容类型适配（§3）：①社会现象批判 ②前沿发现与预测（后者是 Ryder 核心竞争力，skill 不介入预测本身）

**与 social-critique 的协作**：当 social-critique 生成调研报告后调用 content-studio 生成口播稿时，content-studio 必须同时加载 persona-guide.md，确保口播稿的人设一致性。

**自检**：内容生成后过 persona-guide.md §6 的 8 项自检清单。

### 10. Deep Research → 小红书图集的证据卡规范（v4.9.1 新增）

当输入是 deep research / social-critique / 长报告 / 调研报告 / 学术资料汇总，并要求生成小红书卡片或图集时，默认启用本规范。

**核心原则**：小红书正文仍然保持痛点共鸣和口语化，但卡片图集必须更像「可收藏的证据链」——不是只写大字金句。

**图集结构**：
- 默认 7-9 张：封面 1 张 + 内容卡 5-7 张 + References 1 张。
- 最后一页必须是 `References` / `参考材料`，不放 URL，只列明确资料名称。
- References 页只列被卡片实际使用的资料，优先 4-8 条；不要把报告附录全搬进去。
- 每条资料分配编号：`[1]`、`[2]`、`[3]`，后续内容卡用同一编号引用。

**卡片内引用编号**：
- 每张数据卡、案例卡、机制卡都必须出现参考材料号，例如 `[1]`、`[2][5]`。
- 引用编号放在句末、数据旁、引用框角标或页脚位置均可，但要清晰可见。
- 封面和 CTA 结尾页可以不放引用；只要有事实判断、数据、案例，就必须放。
- 不在卡片中显示 URL；URL 可以保存在 Markdown 或源报告里，但社媒图上只出现资料名称编号。

**信息密度要求**：
- 内容卡不再只放一句金句。每张卡至少包含 `1 个主判断 + 2-3 个支撑点`，或 `1 个数据 + 1 个解释 + 1 个影响`。
- 竖屏 1080×1440 内容卡建议正文 90-160 个汉字；重点卡可以到 180 字，但必须分块排版。
- 每屏保留 2-3 个信息点：例如「结论 / 数据 / 为什么重要」「现象 / 机制 / 结果」。
- 可以继续用强标题和大数字，但标题下面必须补足证据、机制或案例，不输出只有标题的空卡。

**References 页格式**：
```
REFERENCES
[1] Humlum et al. (2025). Large Language Models, Small Labor Market Effects. NBER Working Paper No. 33777.
[2] Brynjolfsson, Rock & Syverson (2017). Artificial Intelligence and the Modern Productivity Paradox. NBER Working Paper No. 24001.
[3] Raisch & Krakowski (2021). Artificial Intelligence and Management: The Automation-Augmentation Paradox. Academy of Management Review.
[4] Fortune (2026-03-10). AI productivity paradox: Workers are doing more, not less.
```

**生成顺序**：
1. 先从报告提取 `source_registry`：编号、资料名称、年份、类型、与哪张卡有关。
2. 再写图集脚本：每张卡明确 `claim`、`evidence`、`ref_ids`。
3. 最后做 HTML/PNG：内容卡渲染引用编号；尾页渲染 References。
4. QA 时检查：内容卡引用号是否都能在 References 页找到；References 页是否没有 URL。

### 11. 小红书「图集主载体，正文辅助」规范（v4.9.3 修订）

当已经生成了小红书图集/卡片时，帖子正文不是报告摘要，也不是把卡片再复述一遍。**图片负责承载核心信息和证据链，正文负责把用户拉进图集、制造共鸣、引导评论。**

**定位**：
- 图片 = 主内容：核心判断、数据、案例、参考材料号、References。
- 正文 = 辅助文案：情绪入口、场景共鸣、阅读引导、开放问题。
- 标题 = 信息流钩子：先让用户停下来，再让图片完成说服。

**标题学习的是风格，不是句式**：
- 不要固化标题模板；不要把某个 case 的标题结构当公式复用。
- 学习的是「像人刷到会停一下」的表达：口语、反差、共鸣、轻微冒犯感、明确痛点。
- 标题要先命中用户体感，再让图片完成论证；不要先摆研究结论。
- 同一主题输出标题候选时，要覆盖不同情绪角度：吐槽感、扎心感、反差感、追问感、冷静点破感。
- 每个标题必须像一个真实用户会转述的话，而不是一个内容运营模板。

**标题风格校准**：
| 维度 | 要做到 | 避免 |
|------|--------|------|
| 口语感 | 像朋友突然说出一句扎心话 | 学术摘要、报告题目 |
| 反差 | 承诺 vs 现实、工具变强 vs 人更累 | 平铺直叙 |
| 体感 | 先写“我/你真的遇到过” | 先写宏观趋势 |
| 情绪 | 有一点不爽、怀疑、被戳中 | 情绪宣泄或骂街 |
| 可信 | 不骗点击，图里能兑现标题 | 标题党、夸大事实 |

**风格参考只作为 taste，不作为模板**：如果用户给出某个标题例子，提炼其风格特征（例如“反问 + 戳破承诺”“趋势反差 + 群体共鸣”），不要在后续机械套用同一结构。

**正文文笔要求（图片辅助型）**：
1. 开头先写体感，不要写结论；让用户觉得“这说的不就是我吗”。
2. 用具体动作带出场景：写 prompt、补上下文、查幻觉、改输出、被追问“AI不是很快吗”。
3. 句子要有节奏：短句停顿 + 关键句单独成段；不要一整段报告腔。
4. 中段点出核心矛盾，但不展开证据；证据留给图片。
5. 结尾抛一个用户愿意回答的问题，避免“快来评论”式乞求互动。

**正文风格校准**：
| 维度 | 要做到 | 避免 |
|------|--------|------|
| 入口 | 先接住具体痛感 | “本报告显示” |
| 画面 | 写工作动作和对话 | 抽象概念堆叠 |
| 信息 | 只抛核心矛盾 | 复述每张卡 |
| 节奏 | 短句、停顿、单独成段 | 长段落、总结腔 |
| 互动 | 问真实处境 | 要赞要关注 |

**正文不要这样写**：
- 不要写成“本报告显示/本研究发现/本文整理了……”的摘要腔。
- 不要把每个数据、论文、案例都塞进正文；这些放图片里。
- 不要重复 References；正文只提示“最后一页放了参考材料”即可。
- 不要过度解释理论；小红书正文砍理论，图集里通过编号和 References 保留可信度。

**正文长度**：
- 常规图集：180-280 字。
- 深度调研图集：220-350 字也可以，但必须像人话，不像报告前言。
- 每段 1-3 行，移动端阅读优先；允许短句、反问、停顿。

## 失败模式（已记录）

1. **CJK 字体宽度估算** — draw.textbbox 偏短 → 改用 true_text_width + getlength max
2. **中文字符切边** — 长句不拆 3 行 → 强制用 `\n` 拆 3 行
3. **复杂模式 footer 被切** — 16px 黑边 + 斜切角覆盖 → 缩小斜切角到 200px，footer 上移
4. **emoji 方框** — macOS 默认字体不支持 `🟠` → 改用纯文字配色，不依赖 emoji
5. **CLI nargs bug** — `--steps nargs="*"` 只保留最后一个值 → 改 `nargs="+"`
6. **avatar 路径** — `~/Downloads/image/`（单数）vs `images/`（复数）→ 内嵌到 skill assets
7. **AI 生图回退** — v4.0 试 Midjourney/DALL-E/SD + overlay 失败 → v4.6 撤销，纯 PIL 路线
8. **5 套主题散乱** — v4.3 orange_blk/peach_yellow/cream_red 等 5 套 → v4.6 砍到 simple+complex 2 模式
9. **bash CLI `\n` 是字面字符** — `python card_generator.py --hook "高段位 AI\n决策者"` 中 `\n` 不会变成真换行，**`hook.split("\n")` 失败**，结果只显示一行，所有元素被压成单行 box。**修复**：在 `main()` 入口加 `hook = _normalize_newlines(hook)` 把字面 `\n` 替换为真 `\n`。任何需要多行输入的 CLI 字段都加这一层。

10. **"重新设计卡片"歧义（v4.7 起）** — Ryder 说"重新设计卡片"时**默认指 HTML/CSS 模版**（`references/templates/` 下的设计源文件），不是 PIL 渲染代码（`scripts/card_generator.py`）。参考架构：xhs-brutalist-cards 三层模式（HTML 用 `contenteditable` 槽位 + CSS 控样式 + PIL/render_cards.py 作为最终 PNG 输出）。**工作流**：先动 `references/templates/` 写出设计稿 → 跑 Playwright 截图给 Ryder 确认 → 通过后再同步改 `scripts/card_generator.py`。反向（先动 PIL 改 HTML）会被打断纠正。

11. **对称审美陷阱（v4.7 起）** — Ryder 不要对称设计（"毫无设计感"）。提布局方向时**不要给 3 个对称选项让 Ryder 选**。新设计原则："**中心稳定 + 边缘张力**"——核心信息（标题/副标题/头像）居中形成视觉重心，装饰元素（ID 卡、KOL 角标、stamp、RYDER 卡）贴边不对称制造张力。简单模式已做到；复杂模式 v4.6 失败（14 个元素全部贴边堆叠看着像 brute force），v4.7 重做。

12. **沟通节奏（v4.7 起）** — 不要问太多问题。问 1-2 个关键的就动手做，做完发图让 Ryder 反馈。Ryder 偏好"**做出来看效果 > 反复对齐文字描述**"。给 3 个文字选项让 Ryder 选 = 强迫他做设计判断；做 1 个方案 + 渲染图让他视觉反馈 = 高效迭代 10×。

13. **HTML 预览渲染 vs PIL 渲染是两件事（v4.7 起）** — `references/templates/*.html` 是设计源（用 Playwright 截图验证视觉），`scripts/card_generator.py` 是最终输出工具（生成社媒 PNG）。两者**独立验证**：HTML 用 Playwright `page.screenshot(clip=...)` 截；PIL 用 `card_generator.py` CLI 直接输出。**不要混淆**——HTML 截图只验证设计稿是否好看，PIL 截图才验证最终产物是否对齐设计稿。

14. **HTML 模板里 `<img src="./avatar.png">` file:// 协议下相对路径 broken** — Chromium 严格模式下 file:// 加载相对资源时，路径解析到当前文件目录外会失败，显示 broken image。**修复**：① 同目录放 avatar.png ② base64 嵌入（最稳）③ 绝对 file:// 路径（仅本机预览）。模板注释里写明 3 种方式。

15. **"标题居中" ≠ "整体对称"** — 用户说"标题居中"时，指**主标题内容在水平方向居中对齐**（视觉重心），**不是指整体布局对称**。brutalist 美学的核心是"不对称的张力"，整体对称会破坏杂志感。**正确做法**：标题居中 + 边缘装饰保留不对称分布。**判断口诀**：内容（C位）= 居中，装饰（边缘）= 不对称。

16. **"模板" ≠ "单次输出"** — 用户让做卡片时，默认需求是**可复用模板**（存在 `references/` 下，浏览器内 contenteditable 编辑 + CSS 变量化 + HTML 注释占位），不是一次性 PIL/HTML 输出。**判断时机**：用户描述需求时若带"下周/下次/不同主题/换内容"等措辞 → 100% 是模板需求。

17. **brutalist 居中陷阱**（complex 模式硬性约束）— 自动把副标题 / 头像也居中会破坏 brutalist 风格。brutalist 要求"**除了标题都贴边/错位**"。**v4.8 注**：红方块、斜切角、+ 标记、meta-rail、条纹、footer 已删除，不再是 brutalist 必需元素。

18. **CSS Grid 隐式 marginTop bug** — `display: grid/flex` 父容器 + 子元素 `display: grid; place-items: center; line-height: <1` → 浏览器计算子元素 marginTop 为非 0，撑高父容器导致布局错乱。**修复**：子元素改用 `display: block; text-align: center; margin: 0; padding: 35px 0`，或 `line-height: 1` + `display: flex; align-items: center; justify-content: center`。

19. **Playwright `card.screenshot()` 不可靠** — 元素高于 viewport 时截不完整。**修复**：用 `page.screenshot(clip={x, y, width, height})` 配合 `el.getBoundingClientRect()` 精确裁剪。

20. **PIL v1 14 元素 baseline 已推翻**（v4.8）— 14 元素中 6 个无功能价值的装饰元素已删除（红方块、斜切角、+标记、meta-rail、条纹、footer），砍到 8 元素。新 baseline = 8 元素。**核心判断标准**：每个元素必须有明确功能，无重复无意义元素。

21. **Chrome headless 渲染 macOS 实战坑**（v4.7）— ① `--headless=old` 比 `--headless=new` 稳定；② 每次渲染后必须 `pkill -f "Google Chrome"` + sleep 1-2s；③ macOS 没有 `timeout` 命令，用 `--virtual-time-budget=5000` 替代；④ `--virtual-time-budget` <3000 会导致 avatar.png 未加载完就截图。详见 SKILL.md「Chrome headless 渲染实战」节。

22. **多次 patch 叠加导致 SKILL.md 内部矛盾**（v4.8 审计）— 跨 session 的多次 patch 会导致：①文件结构段被重复粘贴 3 遍；②失败模式编号重复（10-12 出现三次）；③元素数量在不同段落不一致（description 写 10、正文写 8）；④已删元素的引用残留（对比表引用 +标记/meta-rail/stripe）。**修复**：每次大版本迭代后做一次全文审计（grep 关键词 + 检查编号连续性 + 检查元素数量一致性）。**预防**：patch 前先 read_file 确认上下文，不要盲打 old_string。

## 设计原则（brutalist 范式）

> 这些原则是从 v4.7 迭代中沉淀的，比具体的 token 表更稳定。

### 1. 中心 + 边缘张力
- **中心（C 位）**：核心信息（标题、副标题）**居中**——视觉重心稳
- **边缘（装饰）**：装饰元素（ID 卡、角标、头像、stamp、RYDER 卡）**不对称分布**——brutalist 节奏感
- **判断口诀**：内容居中，装饰错位
- **反例**：整体对称 = 普通海报，不是 brutalist

### 2. 硬投影（box-shadow）规律
- 投影偏移 = 元素重要性：标题级 14px / 副标级 12px / ID 卡级 10px / 角标级 8px
- 颜色二选一：红（`#F0442E`，主要） / 黄（`#FFD72E`，仅 title-3 强调）
- **绝对不能**用 blur 模糊投影——brutalist 的核心是"硬切"质感

### 3. 视觉重量二件套（v4.8 修订）
- 黑色厚边框（16px 全周）= 容器边界
- 信纸底纹理（横线 + 噪点）= 手作感
- **v4.8 删除**：右下斜切角（200-260px）—— 纯装饰，无信息承载功能，Ryder 要求删除无意义元素
- 二件套已足够 brutalist，不需要第三件

### 4. 模板优先于输出
- 用户让做卡片时，**默认做模板**（references/ 下，CSS 变量化 + contenteditable + 注释占位）
- 单次输出 = 浪费，每次新主题都要重新设计
- 模板要做成"换内容就能用"，不要做"换内容还要再调坐标"

### 5. 无意义元素零容忍（v4.8 硬性原则）
- Ryder 原话：「页面中禁止出现重复的以及无意义的元素」
- **每个元素必须承载信息或结构功能**——纯装饰元素（色块、符号、条纹）一律删除
- **判断标准**：删掉这个元素，卡片信息量是否减少？如果不减少 = 该删
- v4.8 删除的 4 个元素（红方块/斜切角/+标记/条纹）都是"删了不影响信息传达"的纯装饰
- 这条原则适用于所有模式（simple + complex）和所有卡片类型（封面/内容卡/结尾卡）

## Chrome headless 渲染实战（2026-06-17 定稿）

> 用 `scripts/render-html-to-png.sh` 或直接 Chrome headless 渲染 HTML 模版为 PNG。

**关键经验**：

1. **`--headless=old` 比 `--headless=new` 更稳定**：`--headless=new`（新版默认）频繁超时/不输出；`--headless=old` 每次都能渲染。
2. **每次渲染后 `pkill -f "Google Chrome"`**：Chrome headless 进程不自动退出，累积后导致后续渲染超时。渲染完一个 → kill → sleep 1-2s → 渲染下一个。
3. **macOS 没有 `timeout` 命令**：不要在脚本里用 `timeout 30 chrome ...`，会报 `command not found`。用 `--virtual-time-budget=5000` 控制渲染等待时间即可。
4. **必加 flags**：`--no-first-run --disable-extensions --disable-background-networking`（减少 Chrome 启动时的网络请求干扰）。
5. **批量渲染脚本模板**：
   ```bash
   CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
   render() {
     local html="$1" png="$2"
     "$CHROME" --headless=old --disable-gpu --hide-scrollbars --no-sandbox \
       --no-first-run --disable-extensions --disable-background-networking \
       --virtual-time-budget=5000 --window-size="1200,1600" \
       --screenshot="$png" "file://$(cd $(dirname $html) && pwd)/$(basename $html)" 2>/dev/null
     pkill -f "Google Chrome" 2>/dev/null; sleep 1
   }
   ```

**已知坑**：
- Chrome 启动时报 `installwebapp failed` 错误（Gmail/Docs webapp 安装），可忽略，不影响截图。
- `--virtual-time-budget` <3000 可能导致图片未加载完就截图（avatar.png 显示不全）。5000ms 够用。

## 已知局限

- **emoji 不支持** — `🟠` 等 emoji 在 macOS 默认字体链外显示为方框
- **复杂模式只支持 1 种配色** — brutalist 红黑米黄，不分支。simple 模式也是固定配色（米黄+黑+橙红）
- **内页不留任何内容** — 必须用户 P 图，工具不自动填充（设计原则）
- **4 平台覆盖** — X / 小红书（图文）+ 抖音 / B站（视频）。快手/公众号暂不覆盖（用户画像不匹配）
- **4 内容类型各有结构** — AI产品推荐/GitHub分析/热点讲解/日常感悟不是同一套模板套不同文字，各有独立结构。详见 `references/content-types.md`
- **字体仅 macOS** — Linux 需额外配置字体路径

## 平台选择原则（v4.8 沉淀）

> **教训**：v4.8 初版曾加入快手平台（标题党风格），Ryder 实际查看后发现在快手无人关注——用户画像完全不匹配（快手核心用户偏下沉市场，与 AI 产品经理专业内容定位矛盾）。

**平台选择硬性原则**：
1. **先验证用户画像匹配度，再建平台方法论** — 不能凭"这个平台流量大"就加入，要看目标用户在不在这个平台上
2. **内容调性 vs 平台调性** — 专业/硬核内容不适合下沉市场平台；标题党风格不适合专业社区
3. **宁可少平台，不要错平台** — 4 个精准匹配的平台 > 6 个硬做的平台
4. **平台画像分析是前置步骤** — 详见 `references/platform-audit.md`，每个平台要有用户画像 + 匹配度评估 + 账号定位

**当前 4 平台定位**（详见 `references/platform-audit.md`）：

| 平台 | 角色定位 | 匹配度 | 投入比例 |
|------|---------|--------|---------|
| X | AI tech voice（行业判断+项目发现） | ⭐⭐⭐⭐⭐ | 30% |
| 小红书 | AI 工具种草官（实用工具+痛点解决） | ⭐⭐⭐⭐ | 30% |
| B站 | AI 深度分析（专业护城河） | ⭐⭐⭐⭐ | 25% |
| 抖音 | AI 知识速览（曝光扩大器） | ⭐⭐⭐ | 15% |
