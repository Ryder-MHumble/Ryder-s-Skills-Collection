# HTML 模板 → PNG 渲染（macOS Chrome headless）

> **何时用**：需要把 HTML/CSS 模板渲染成 PNG 发布到社媒，但不想装 Playwright / Puppeteer。
> **适用场景**：content-studio 的 KOL 卡片模板、xhs-brutalist-cards 系列、未来其他 HTML 模板。

## 1. 一键命令

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HTML="$1"   # 输入 HTML 绝对路径
OUT="$2"    # 输出 PNG 绝对路径
W="${3:-1240}"
H="${4:-1654}"

"$CHROME" --headless --disable-gpu --hide-scrollbars --no-sandbox \
  --window-size="${W},${H}" --screenshot="$OUT" \
  "file://$HTML" 2>&1 | tail -3
```

**实际调用示例**（KOL 04）：
```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless --disable-gpu --hide-scrollbars --no-sandbox \
  --window-size=1240,1654 \
  --screenshot=/Users/rydersun/.hermes/skills/creative/content-studio/references/visual/kol-04-cover.png \
  file:///Users/rydersun/.hermes/skills/creative/content-studio/references/visual/kol-04-cover.html
```

## 2. 关键 flags（缺一不可）

| Flag | 作用 | 不加的后果 |
|------|------|----------|
| `--headless` | 无头模式 | 打开完整 Chrome 窗口（GUI） |
| `--disable-gpu` | 禁用 GPU 加速 | 报 GPU 错误（在 headless 模式无意义） |
| `--hide-scrollbars` | 隐藏滚动条 | 截图里出现滚动条（默认 800×600 时尤其明显） |
| `--no-sandbox` | 关闭沙盒 | macOS 沙盒下报 "Failed to move to new namespace" |
| `--window-size=W,H` | 设定视口尺寸 | **默认 800×600**，必须显式指定目标尺寸 |
| `--screenshot=OUT` | 输出 PNG 路径 | 不指定就不输出 |

## 3. 已知坑（v4.7 实测）

### 坑 1：默认 800×600 截图
**症状**：输出 PNG 只有 800×600，不是设计的 1240×1654
**原因**：`--window-size` 必须显式指定
**修复**：`--window-size=1240,1654`

### 坑 2：网络图片未加载完
**症状**：头像/外部图片显示 broken 或空
**原因**：Chrome 截图时机早于 `load` 事件
**修复**：加 `--virtual-time-budget=5000`（5 秒虚拟时间）
```bash
"$CHROME" --headless ... --virtual-time-budget=5000 --screenshot=... file://...
```

### 坑 3：file:// 协议下相对路径 broken
**症状**：HTML 里的 `<img src="./avatar.png">` 显示 broken
**原因**：Chromium 严格模式下 file:// 加载相对资源失败
**修复**（按稳定性排序）：
1. 同目录放 `avatar.png`（最简，模板默认）
2. base64 嵌入（`<img src="data:image/png;base64,...">`，最稳）
3. 绝对 file:// 路径（`<img src="file:///Users/.../avatar.png">`，仅本机预览用）

### 坑 4：中文显示方框
**症状**：中文字符渲染成方框
**原因**：HTML 里没显式指定中文字体链
**修复**：CSS 加 `font-family: "STHeiti", "Heiti SC", "PingFang SC", "Microsoft YaHei", sans-serif;`

### 坑 5：滚动条影响构图
**症状**：右侧/底部出现灰色滚动条
**修复**：`--hide-scrollbars`（必须）

## 4. 何时不用

- **需要交互测试**（点击、表单填写）→ 用 Playwright
- **需要等 JS 异步加载完成** → 用 Playwright + `waitForLoadState`
- **需要批量截图多页面** → 用 Playwright 脚本
- **Linux 服务器**（无 GUI）→ 装 headless Chrome 或 Playwright

## 5. 性能数据（实测）

- 启动 Chrome headless: ~1.5s
- 渲染 1240×1654 单页: ~0.5s
- 输出 PNG: ~200-300KB
- **总计**: 2-3s/张（比 Playwright 快 50%，因为无 Node.js 开销）

## 6. 可重用的脚本

详见 `scripts/render-html-to-png.sh`（已封装上述命令）。
