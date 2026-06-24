# Grid + Screenshot Pitfalls — content-studio v4.7

> 从 v4.7 复杂模式重设计实战中踩到的两个坑。HTML/CSS 模版阶段 + Playwright 预览阶段必读。

## §1 CSS Grid + display:flex + line-height 隐式 margin 陷阱

### 症状

HTML 模版里把一个 box 放进 `display: grid` 容器作为 grid item，box 自己用 `display: flex; align-items: center; justify-content: center; line-height: 0.92;` 居中单行文字。**结果 box 的 bounding box 比 CSS `height` 高 60-100px，整张卡片垂直布局完全错乱。**

实测 162px 高的 box，computed `marginTop: 61.64px, marginBottom: 61.64px`（用 `getComputedStyle().marginTop` 可见），中心舞台整体高度膨胀到 1448px（期望 942px）。

### 根因

Grid item 的"intrinsic size"计算时，**浏览器把 flex/grid 容器内单行文字的 line-box 算作 padding 之外的"min-content"**，导致 grid layout 给该 item 多分配上下空间。`place-items: center` 又把这个 line-box 居中。

**具体行为**：
- `line-height: 0.92` × `font-size: 92px` = `lineHeight: 84.64px`
- box height 162, 期望 line-box 居中 = top 38.68
- 实际 computed marginTop: 61.64 ≈ 162/2 - 84.64/2 + 一些浏览器特定 baseline 偏移

### 修复（必用）

**不要**用 `display: flex; align-items: center` 居中已知高度 box 里的单行文字。**改用**：

```css
.title-block {
  display: block;        /* 不要 flex/grid */
  text-align: center;
  margin: 0;            /* 显式清零，防 computed margin 注入 */
  line-height: 1;       /* 不要用 ratio 触发 line-box 计算 */
}
.title-1 {
  height: 162px;
  padding: 35px 0;      /* 手动算: (height - lineHeight) / 2 = (162 - 92) / 2 = 35 */
  font-size: 92px;
}
```

**验证 computed margin**：
```javascript
// 在 Playwright evaluate 里跑
const cs = getComputedStyle(document.querySelector('.title-1'));
console.log(cs.marginTop, cs.marginBottom, cs.lineHeight);
// 期望 marginTop: 0px, marginBottom: 0px
```

如果 `marginTop` 不是 0 — 说明还有 flex/grid 残留，立刻排查 `display` 和 `line-height`。

### 适用范围

任何**已知高度 + 单行文字 + 居中需求**的 box 都应该用 `display: block + padding` 而不是 `display: flex + align-items: center`。这一条规则适用于 content-studio 未来所有的 HTML 模版（封面、内页、信纸等）。

## §2 Playwright `element.screenshot()` vs `page.screenshot(clip=...)`

### 症状

调用 `page.query_selector('.xhs-card').screenshot(path=...)` 截一张 1654px 高的卡片，**结果图只到卡片中部（avatar 和 support 卡完全缺失）**，但 `bounding_box()` 返回的 height 是完整 1654px。

### 根因

`element.screenshot()` **滚动元素到视口 + 截 viewport 可见部分**，不截溢出 viewport 的部分。如果元素比 viewport 大，**底部被截掉**。`bounding_box()` 返回的是 layout 尺寸（不依赖 viewport 可见性），但 `screenshot()` 用 viewport 截图。

### 修复

**用 `page.screenshot(clip={x, y, width, height})` 精确裁剪**：

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    page = browser.new_page(viewport={"width": 1400, "height": 1900})  # viewport 调大
    page.goto(f"file://{template_path}")
    page.wait_for_load_state("networkidle")

    # 读 element 的 layout rect
    rect = page.evaluate("""() => {
        const r = document.querySelector('.xhs-card').getBoundingClientRect();
        return {x: r.x, y: r.y, width: r.width, height: r.height};
    }""")

    # 用 page.screenshot 精确裁剪
    page.screenshot(
        path=str(out_path),
        clip={"x": rect["x"], "y": rect["y"], "width": rect["width"], "height": rect["height"]}
    )
```

**关键参数**：
- `viewport` height 必须 >= element height（否则就算用 clip 也会被 viewport 截掉）
- `clip` 坐标用 `getBoundingClientRect()` 拿 viewport-relative 坐标
- **不要用** `full_page=True`（会把 body 背景和 padding 都拍进去，污染结果）

### 适用范围

这个 pattern 适用于所有"截图高于 viewport 的 HTML 元素"场景：content-studio 模版预览、KOL 情报库卡片截图、未来其他生成式 HTML 模版的验证。**通用模式**：

```python
# 通用 helper
def screenshot_element(page, selector, out_path, headroom=100):
    page.set_viewport_size({"width": 1400, "height": 2000})  # 给够高
    page.goto(...)
    rect = page.evaluate(f"""() => {{
        const r = document.querySelector('{selector}').getBoundingClientRect();
        return {{x: r.x, y: r.y, width: r.width, height: r.height}};
    }}""")
    page.screenshot(path=out_path, clip=rect)
```

### 顺便记录

- `element.is_visible()` 返回 True 不代表元素完整可见，**只能验证 layout box 非空**，不能验证 viewport 可见性
- `bounding_box()` 返回 viewport-relative 坐标，不是 page-relative — 滚动会改变坐标
