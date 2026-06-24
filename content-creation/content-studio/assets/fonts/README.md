# Fonts

本目录说明 content-studio skill 使用的字体策略。

## 策略：智能系统字体 fallback

**不内嵌字体文件**（避免版权 + 仓库体积）。脚本 `scripts/card_generator.py` 自动 fallback 到 macOS/Linux/Windows 系统字体。

## 字体优先级链

### 中文（CJK）字体

| 优先级 | macOS | Linux | Windows |
|--------|-------|-------|---------|
| 1 | Hiragino Sans GB.ttc | Noto Sans CJK SC | Microsoft YaHei |
| 2 | STHeiti Medium.ttc | WenQuanYi Micro Hei | SimHei |
| 3 | PingFang.ttc | Source Han Sans | 微软雅黑 |
| Fallback | Arial Unicode.ttf | DejaVu Sans | Arial |

### 英文 Display / Sans

| 优先级 | macOS | Linux | Windows |
|--------|-------|-------|---------|
| 1 | Helvetica.ttc | DejaVu Sans Bold | Arial |
| 2 | Avenir.ttc | Liberation Sans | Calibri |
| 3 | SFNS.ttf | Ubuntu | Segoe UI |

### 英文 Serif

| 优先级 | macOS | Linux | Windows |
|--------|-------|-------|---------|
| 1 | Times.ttc | Liberation Serif | Times New Roman |
| 2 | Palatino.ttc | DejaVu Serif | Cambria |
| 3 | NewYork.ttf | URW Bookman | Constantia |

### Monospace

| 优先级 | macOS | Linux | Windows |
|--------|-------|-------|---------|
| 1 | Menlo.ttc | DejaVu Sans Mono | Consolas |
| 2 | SFNSMono.ttf | Liberation Mono | Courier New |
| 3 | Courier.ttc | Ubuntu Mono | Cascadia Mono |

## 推荐字体升级（可选）

如果想让卡片视觉效果更接近 web 设计，可以下载并安装：

| 字体 | 用途 | 来源 |
|------|------|------|
| **Inter** | Swiss Grid 首选 | https://rsms.me/inter/ |
| **Playfair Display** | McKinsey 标题 | Google Fonts |
| **Archivo Black** | Neo-Brutalism 标题 | Google Fonts |
| **Plus Jakarta Sans** | 通用 sans | Google Fonts |
| **JetBrains Mono** | 数据 / telemetry | JetBrains |

下载后放到 `~/Library/Fonts/`（macOS）或 `~/.local/share/fonts/`（Linux），再运行 `fc-cache -fv`（Linux）。

**但本 skill 不强制要求**——智能 fallback 已经能渲染出 OK 的效果。

## 测试当前字体

```bash
python -c "
from PIL import ImageFont
import os
# macOS
for path in ['/System/Library/Fonts/Helvetica.ttc',
             '/System/Library/Fonts/Hiragino Sans GB.ttc']:
    if os.path.exists(path):
        try:
            f = ImageFont.truetype(path, 24)
            print(f'OK: {path}')
        except Exception as e:
            print(f'FAIL: {path}: {e}')
"
```

## 如果字体显示方框

1. **检查中文字体**是否在系统里
2. **修改字体优先级链**（`scripts/card_generator.py` 的 `FONT_FALLBACK_CHAIN`）
3. **下载并安装中文字体**（见上）

## 字体不会显示 emoji

Apple Color Emoji.ttc 是 emoji 专用字体。本 skill 不主动调用它，所以 emoji 在卡片中可能显示为方框。

**解决**：把 `Apple Color Emoji.ttc` 加到 `FONT_FALLBACK_CHAIN` 的 `cjk_regular` 之后，作为 emoji fallback。
