#!/usr/bin/env bash
# render-html-to-png.sh — HTML 模板 → PNG（macOS Chrome headless）
# content-studio · v4.7
#
# 用法：
#   ./render-html-to-png.sh <html-path> <png-path> [width] [height]
#
# 示例：
#   ./render-html-to-png.sh kol-04-cover.html kol-04-cover.png 1240 1654
#   ./render-html-to-png.sh cover.html cover.png           # 默认 1240x1654
#   ./render-html-to-png.sh 9x16.html out.png 1080 1920    # 抖音竖图

set -euo pipefail

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 参数
HTML="${1:?用法: $0 <html-path> <png-path> [width=1240] [height=1654]}"
OUT="${2:?缺少输出 PNG 路径}"
WIDTH="${3:-1240}"
HEIGHT="${4:-1654}"

# 校验
if [ ! -f "$HTML" ]; then
  echo "❌ HTML 文件不存在: $HTML" >&2
  exit 1
fi

# 转绝对路径
HTML_ABS="$(cd "$(dirname "$HTML")" && pwd)/$(basename "$HTML")"
HTML_URL="file://$HTML_ABS"

mkdir -p "$(dirname "$OUT")"

# 渲染
echo "🎨 渲染: $HTML_ABS"
echo "   →   $OUT (${WIDTH}×${HEIGHT})"

"$CHROME" \
  --headless \
  --disable-gpu \
  --hide-scrollbars \
  --no-sandbox \
  --virtual-time-budget=5000 \
  --window-size="${WIDTH},${HEIGHT}" \
  --screenshot="$OUT" \
  "$HTML_URL" 2>&1 | tail -2

# 输出文件大小
if [ -f "$OUT" ]; then
  SIZE=$(du -h "$OUT" | cut -f1)
  echo "✅ 完成 ($SIZE)"
else
  echo "❌ 截图失败" >&2
  exit 1
fi
