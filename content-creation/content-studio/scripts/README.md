# card_generator.py — 卡片生成器 v4.6

> 两种封面模式（simple/complex）+ 1 套内页信纸版。

## 6 种宽高比

```
1:1   (1600x1600)  - 朋友圈方图
3:4   (1200x1600)  - 小红书竖图（默认）
4:3   (1600x1200)  - 公众号横图
9:16  (1080x1920)  - 抖音 / 视频号
16:9  (1600x900)   - X 横图 / B 站封面
2:3   (1200x1800)  - 竖图（带更多内容）
```

## 两种封面模式

### Simple（默认）
- 5 元素：米黄底+网格 / ID 标签 / 3 行主标题 / 副标 / 头像
- 适合日常推文

### Complex（brutalist 杂志风）
- 12+ 元素：参考 `xhs-brutalist-cards/html/style.css`
- 适合重要发布

## CLI 用法

```bash
# 简易模式（默认）
python card_generator.py \
  --type cover --mode simple \
  --hook "高段位 AI\n决策者都应该有\nKOL 情报库" \
  --sub "2 小时访谈 → 5 分钟笔记" \
  --aspect 3:4 -o cover.png

# 复杂模式
python card_generator.py \
  --type cover --mode complex \
  --hook "..." --sub "..." \
  --aspect 3:4 -o cover.png

# 9:16 抖音封面（复杂）
python card_generator.py \
  --type cover --mode complex \
  --hook "..." --sub "..." \
  --aspect 9:16 -o cover.png

# 内页信纸版
python card_generator.py --type inside --page 2 --total 5 \
  --aspect 3:4 -o inside.png
```

## Python API

```python
from card_generator import (
    render_cover_simple,
    render_cover_complex,
    render_inside,
)

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
    hook="...",
    sub_hook="...",
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

## hook 写法

用 `\n` 拆 3 行：
- 第 1 行 5 字符左右（如"高段位 AI"）
- 第 2 行 7-8 字符
- 第 3 行包含"KOL"（自动红色高亮）

## 故障排除

**中文显示为方框**：检查 `load_font` 字体链是否包含 Hiragino Sans GB.ttc
**文字溢出 box**：已用 `true_text_width + 8% buffer` 修复
**footer 被切**：simple 模式无 footer，complex 模式 footer 自动上移
**CLI 单步不显示**：用 `nargs="+"` 一次传多值
