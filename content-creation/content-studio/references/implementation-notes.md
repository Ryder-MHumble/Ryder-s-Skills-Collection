# Implementation Notes — content-studio 卡片生成器

> v4.0 实战中遇到的关键实现坑 + 修复路径。PIL 渲染 + CJK 字体处理经验。

## §1 CJK 字体 Fallback（最关键）

### 问题

PIL `ImageFont.truetype()` 不会自动 fallback 字符集。直接 `load_font("display_bold", size)` 用 `Helvetica.ttc` 渲染中文 = **方框（□）**。

### 解决

`scripts/card_generator.py` 提供 `select_font(role, text, size)` 函数：

```python
def has_cjk(text: str) -> bool:
    """检测 CJK 字符。"""
    for ch in text:
        cp = ord(ch)
        if (0x4E00 <= cp <= 0x9FFF or  # CJK Unified
            0x3400 <= cp <= 0x4DBF or  # Extension A
            0x3040 <= cp <= 0x30FF or  # Hiragana/Katakana
            0xAC00 <= cp <= 0xD7AF or  # Hangul
            0x3000 <= cp <= 0x303F or  # CJK Symbols
            0xFF00 <= cp <= 0xFFEF):   # Fullwidth
            return True
    return False


def select_font(role: str, text: str, size: int) -> ImageFont.FreeTypeFont:
    if has_cjk(text):
        if "bold" in role or "display" in role:
            return load_font("cjk_bold", size)
        return load_font("cjk_regular", size)
    return load_font(role, size)
```

**所有 render 函数的字体加载必须用 `select_font(role, text, size)`，不能用 `load_font(role, size)`**。否则中文 = 方框。

### 字体优先级链

`scripts/card_generator.py` 顶部 `FONT_FALLBACK_CHAIN` 定义：

| role | macOS 优先级 | Linux 优先级 | Windows 优先级 |
|------|------------|------------|----------------|
| `display_bold` | Arial Unicode → Helvetica → Avenir | DejaVu Bold → Liberation | Arial |
| `serif_bold` | Times → Palatino → NewYork | Liberation Serif → DejaVu Serif | Times New Roman |
| `sans_regular` | HelveticaNeue → Avenir → SFNS | DejaVu Sans → Liberation | Calibri |
| `mono` | Menlo → SFNSMono → Courier | DejaVu Mono → Liberation Mono | Consolas |
| `cjk_bold` | Hiragino Sans GB → STHeiti Medium → PingFang | Noto Sans CJK SC → WenQuanYi | Microsoft YaHei |
| `cjk_regular` | Hiragino Sans GB → STHeiti Light | Noto Sans CJK SC | SimHei |

详见 `assets/fonts/README.md`。

## §2 不要内嵌字体文件

**反模式**：把 .ttf/.otf 文件复制到 `assets/fonts/` 内嵌到 skill。

**理由**：
- 版权风险（大多数字体不允许再分发）
- 仓库体积膨胀（每个字体 1-5MB，5 个字体 = 25MB+）

**正确做法**：智能 fallback 到系统已装字体。skill 跨机器可用，体积小。

**macOS 测试**：
```python
import os
for path in ["/System/Library/Fonts/Helvetica.ttc",
             "/System/Library/Fonts/Hiragino Sans GB.ttc"]:
    print(f"{'OK' if os.path.exists(path) else 'MISSING'}: {path}")
```

**Linux 装中文字体**（如 fallback 失败）：
```bash
sudo apt install fonts-noto-cjk fonts-noto-cjk-extra
# 或
sudo yum install google-noto-sans-cjk-fonts
```

## §3 PIL 渲染的尺寸选择

**最大 1600px 基准**：所有 aspect ratio 都以最长边 = 1600px 算，避免过大文件。

| aspect | 输出像素 | 文件大小（典型） |
|--------|---------|----------------|
| 1:1 | 1600×1600 | 50-100KB |
| 3:4 | 1200×1600 | 40-90KB |
| 9:16 | 1080×1920 | 50-130KB |
| 16:9 | 1600×900 | 30-80KB |
| 2:3 | 1200×1800 | 50-110KB |

**社媒平台原生尺寸**（可选适配）：

| 平台 | 比例 | 像素 |
|------|------|------|
| 小红书封面 | 3:4 | 1080×1440 |
| 抖音封面 | 9:16 | 1080×1920 |
| X 首图 | 16:9 | 1200×675 |
| B 站封面 | 16:9 | 1920×1080 |

## §4 文字 wrap 算法

`wrap_text(text, font, max_width, draw)` 按字符逐个加，超出 max_width 就换行。**注意**：

- 中英文混排时**按字符切**（不是按 word），所以每个 CJK 字符独立换行
- macOS 系统 `Helvetica.ttc` + CJK 字符 → 走 `select_font` 切到 CJK 字体，否则宽度估算错误导致 wrap 错位
- 长串英文 + CJK 混排容易算错 wrap 位置。**测试时务必用真实文本**（不要用纯英文 placeholder）

## §5 已知 Bug

### emoji 🟠 显示为方框

**症状**：`🟠` 这种彩色 emoji 在卡片上显示为 □。

**原因**：CJK 字体（Hiragino Sans GB）不含 emoji glyph，Apple Color Emoji.ttc 也没在 fallback 链里。

**临时修复**（v4.0.1+ 待实现）：
```python
FONT_FALLBACK_CHAIN["cjk_regular"].append(
    "/System/Library/Fonts/Apple Color Emoji.ttc"
)
```

**或**用 🟠 的近似 ASCII：`[ORANGE]` / `●`（黑色实心圆）。

### Swiss Grid 在 3:4 比例下文字 wrap 错位

**症状**：`"看 2 小时 KOL"` 在 3:4 卡片中"KOL"被切成 "K\nOL"。

**原因**：Swiss Grid 用了 `int(col_w * 9)` 作为 max_text_w，3:4 比例下 col_w 偏小，9 列不够放下 "KOL"。

**临时修复**（v4.0.1+ 待实现）：在 wrap_text 之前先用更宽松的 max_text_w（如 `int(col_w * 11)`）。

**或**：社媒场景默认用 16:9 比例做 Swiss Grid。

## §6 Patch 文件时的语法保护

**问题**（v4.0 实战）：用 `patch` 工具注释掉 render_neo_brutalism 中的工业标记代码块时，**漏了函数结尾的 `)`**，导致 SyntaxError。

**正确做法**：
1. 用 `read_file` 看完目标段（不要只看部分行）
2. patch 时把 `old_string` 的范围覆盖到 `return img` 之前
3. patch 后必须跑 lint 或执行一次测试（如 `--help`）验证

**自动检测**：在 scripts/ 加一个 `validate.py`，import 所有 module，确保无 syntax error。

## §7 性能

**单张卡片**：1-2 秒生成（取决于字体加载和 wrap_text）。

**批量（platform_pack.py）**：每个平台 1 张 cover + 1-3 张 cards = 5-15 秒。

**字体缓存**：`_loaded_fonts: dict` 缓存已加载字体，避免重复 IO。同一 size + role 只加载一次。

## §8 测试覆盖

**手工测试矩阵**（每个 style × 每个 aspect × 中文/英文 = 50+ 组合）：

```python
import subprocess
from pathlib import Path

gen = Path.home() / ".hermes/skills/creative/content-studio/scripts/card_generator.py"
out = Path("/tmp/cs_test")
out.mkdir(exist_ok=True)

styles = ["neo-brutalism", "mckinsey", "swiss-grid", "notion-minimal", "cyber-neon"]
aspects = ["1:1", "3:4", "9:16", "16:9"]
texts = [
    ("中文测试", "副标题"),  # CJK
    ("English test", "subtitle"),  # ASCII
    ("混合 Mixed 中英", "subtitle"),  # mixed
]

for style in styles:
    for aspect in aspects:
        for text, sub in texts:
            cmd = ["python3", str(gen), "--style", style,
                   "--text", text, "--subtitle", sub,
                   "--aspect", aspect, "--output", str(out / f"{style}_{aspect}.png")]
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            assert r.returncode == 0, f"FAIL: {style}/{aspect}/{text}: {r.stderr}"
print("All tests passed")
```
