# 卡片模版 — 双模式（Simple + Complex）

> v2 重设计（2026-06-17）：Simple 保持极简、Complex 重新设计（14→10 元素，删纯装饰）。
> 每个模式包含 3 种卡片：**封面 / 内容卡 / 结尾卡**。
> 所有模版内嵌头像，通过 `contenteditable` 槽位编辑文字。

## 文件结构

```
templates/
├── simple/                # 极简模式（日常高频）
│   ├── style.css          # 样式（米黄底 + 黑字 + 橙红强调）
│   ├── cover.html         # 封面（ID标签 + 3行钩子 + 副标题 + 大圆头像）
│   ├── content.html       # 内容卡（页眉 + section块 + 页脚）
│   ├── ending.html        # 结尾卡（收尾语 + 头像 + CTA + ID标签）
│   └── avatar.png         # 头像（同目录引用）
├── complex/               # Brutalist 杂志风（重要发布）
│   ├── style.css          # 样式（信纸底 + 黑厚边框 + 硬投影）
│   ├── cover.html         # 封面（ID卡+角标+3行标题+stamp+Ryder卡）
│   ├── content.html       # 内容卡（黑底页眉 + callout块 + section块）
│   ├── ending.html        # 结尾卡（box标题 + 头像 + CTA + ID底栏）
│   └── avatar.png
├── cover-template.html    # [旧] v1 PIL 对齐版（保留备查）
├── style.css              # [旧] v1 共享样式
└── README.md              # 本文件
```

## 用法

### 1. 浏览器编辑（推荐）

```bash
# Simple 封面
open references/templates/simple/cover.html

# Complex 封面
open references/templates/complex/cover.html
```

所有 `contenteditable="true"` 区域双击即可改文字。CSS 不用动，视觉自动重排。

### 2. HTML → PNG 渲染

```bash
# macOS Chrome headless（skill 自带脚本）
./scripts/render-html-to-png.sh references/templates/simple/cover.png 1200 1600
./scripts/render-html-to-png.sh references/templates/complex/cover.html complex_cover.png 1200 1600
```

### 3. PIL CLI（最终 PNG 输出）

```bash
# Simple 封面
python scripts/card_generator.py --type cover --mode simple \
  --hook "高段位 AI\n决策者都应该有\nKOL 情报库" --sub "2 小时访谈 → 5 分钟笔记" -o cover.png

# Complex 封面
python scripts/card_generator.py --type cover --mode complex \
  --hook "高段位 AI\n决策者都应该有\nKOL 情报库" --sub "2 小时访谈 → 5 分钟笔记" -o cover.png
```

## 设计对比

| 维度 | Simple | Complex |
|------|--------|---------|
| 底纹 | 米黄 + 淡网格 | 信纸横线 + 噪点 |
| 边框 | 无 | 16px 黑色厚边框 |
| 标题 | 纯文字（KOL 红色高亮） | 3 行 box 块（米白/黑/红底 + 硬投影） |
| 副标题 | 红底白字框 | 白底黑边 + 红硬投影 |
| 头像 | 中央大圆（直径 384px） | ID 卡小圆（72px） |
| 装饰 | 红色分隔线 | meta-rail + stamp + Ryder 支持卡 |
| ID | 左上白底标签 | 左上 ID 卡（头像+名）+ 右上角标 |
| 结尾 | 居中文字 + 头像 + CTA | box 标题 + 头像 + CTA + ID 底栏 |
| 适合 | 日常高频（周 3-5 条） | 重要发布（月 1-2 条） |

## Complex v2 重设计要点

**删除的元素**（v1 的纯装饰，无信息价值）：
- 顶部红方块 — 纯色块，不承载信息
- 右下斜切角 — 纯装饰
- 4 个 + 标记 — 纯符号装饰
- 黑红条纹 — 纯装饰

**保留的 10 个元素**（每个都承载信息或结构功能）：
1. 16px 黑色厚边框 — 容器边界
2. 信纸底纹 — 手作感
3. ID 卡（左上）— 头像 + 账号名
4. KOL 角标（右上）— 系列编号
5. Meta-rail 横线 — 主题标签 + 期数
6. 3 行标题（居中）— 核心信息
7. 副标题（居中）— 补充信息
8. Stamp（左下）— 期号 + 元数据
9. Ryder 支持卡（右下）— 签名 + 标签
10. Footer — 底部署名

## 槽位对照表

### Simple

| 槽位 | 文件 | 占位文字 | 替换为 |
|------|------|---------|--------|
| `.cover-id` | cover.html | `叫我 Ryder 就好` | 账号名 |
| `.cover-hook .line` | cover.html | `高段位 AI` 等 | 3 行钩子句 |
| `.cover-sub .box` | cover.html | `2 小时访谈 → 5 分钟笔记` | 副标题 |
| `.content-id` | content.html | `叫我 Ryder 就好` | 账号名 |
| `.content-page` | content.html | `02 / 05` | 页码 |
| `.content-section-title` | content.html | `核心洞察` | section 标题 |
| `.content-text` | content.html | 正文占位 | 正文内容 |
| `.ending-text .main` | ending.html | `关注 Ryder` | 收尾语 |
| `.ending-cta .label` | ending.html | `点赞 · 收藏 · 关注` | CTA |

### Complex

| 槽位 | 文件 | 占位文字 | 替换为 |
|------|------|---------|--------|
| `.cover-id .name` | cover.html | `叫我 Ryder 就好` | 账号名 |
| `.cover-badge` | cover.html | `KOL INTEL / 04` | 系列编号 |
| `.cover-meta .row span` | cover.html | `DECISION SIGNALS` 等 | 主题标签 |
| `.title-1/2/3` | cover.html | `高段位 AI` 等 | 3 行标题 |
| `.cover-sub` | cover.html | `2 小时访谈 → 5 分钟笔记` | 副标题 |
| `.cover-stamp .num` | cover.html | `04` | 期号 |
| `.cover-stamp .meta div` | cover.html | `COVER/5 MIN/XHS` | 元数据 |
| `.cover-ryder .ryder-title` | cover.html | `RYDER` | 签名 |
| `.cover-ryder .ryder-chip` | cover.html | `AI PM / INTEL NOTES` | 标签 |
| `.cover-ryder .ryder-desc` | cover.html | `KOL 情报库` | 栏目名 |
| `.cover-ryder .ryder-tag` | cover.html | `HIGH-STAKES DECISIONS` | 副标 |
| `.cover-footer` | cover.html | `BRUTAL CARD SYSTEM / ...` | 底部署名 |
