# Complex 模式设计规范（brutalist）

> 直接从 `~/Documents/Daily Work/xhs-brutalist-cards/html/style.css` (11.4KB) 翻译为 PIL 坐标。
> 修改 complex 模式时，对照此表的 token 调整即可，**不需要重读 CSS**。

## 1. 设计 token（v4.6 baseline，1200×1600 画布）

| Token | 值 | 来源 | 备注 |
|-------|-----|------|------|
| 卡片尺寸 | 1240×1654 (参考) → 1200×1600 (实际) | `--card-w/h` | 当前画布 1200×1600（3:4） |
| 厚黑边框 | 16px | `border: 16px solid ink` | 全周 |
| 右下斜切角 | 200px (黑色) | `clip-path: 100% 0, 100% 100%, 0 100%` | 原来是 260px，缩到 200 不再覆盖 footer |
| 顶部红方块 | 206×126 | `.card-red-corner` | 紧贴左上 16px 黑边 |
| ID 卡片 | 690×104 @ (46, 46) | `.identity` | 头像 76×76 + 文字 |
| ID 头像偏移 | 头像 76×76 @ 卡片内 (10, (h-76)/2) | `.logo-slot` | 红底+黑边+黑投影 |
| KOL INTEL 角标 | w≈330, h=72 @ (w-54-330, 34) | `.top-badge` | 黑底白字 35px Arial Black |
| meta-rail 横线 | y=202, x=46 → w-46, 6px | `.meta-rail` | + 4 tick 标记 @ 260px 间距 |
| title-1 (米白) | y=302, h=162, 字号 92 | `.title-1` | 居中，红投影 (+14, +14) |
| title-2 (黑) | y=496 (=302+162+32), h=162, 字号 92 | `.title-2` | 白字+红投影 |
| title-3 (红) | y=690 (=496+162+32), h=186, 字号 112 | `.title-3` | 黑字+**黄**投影 |
| 副标题 | y=930, h=112, 字号 45 | `.subtitle-bar` | 米白+红边+红投影 |
| 红条纹 | y=1090, h=34, x=46→w-46 | `.stripe` | 黑(0-36%) + 红(36-56%) + 黑(57-100%) |
| 01 stamp | (46, h-184-220), 350×220 | `.page-stamp` | 红底+黑边+黑投影，数字 130px |
| stamp 文字 | COVER / 5 MIN / XHS @ 34px | `.stamp-meta` | 居右 144px 列 |
| RYDER 卡 | (w-54-626, 同 stamp_y), 626×266 | `.support-card` | 米白+黑边+红投影 |
| 条形码 | 卡右上 (w-26-140, 26), 140×94 | `.barcode` | 20 根竖条 |
| AI PM chip | (34, 96), min-w 356, h=48 | `.support-chip` | 黑底白字 25px |
| KOL 情报库 | @ (34, 156), 32px | `.support-copy` | 黑字 |
| HIGH-STAKES | @ (34, 200), 18px | 红色 | |
| footer | y = h-60, 字号 25 | `.footer-note` | "REDESIGNED BRUTAL CARD SYSTEM / TEXT NEVER OVERLAPS / 1240x1654" |
| + 标记 | 字号 58, 4 个位置 | `.plus-marker` | (w-156, 280) / (w-180, 960) / (126, 1126) / (480, h-170) |

## 2. 配色（CSS variables）

```python
COMPLEX_COLORS = {
    "paper": "#F1E2CC",     # 米黄信纸底
    "soft": "#FFF9ED",      # 米白卡片
    "ink": "#080808",       # 黑色
    "red": "#F0442E",       # 橙红（投影 + stamp）
    "yellow": "#FFD72E",    # 黄（仅 title-3 投影）
}
```

**注意**：brutalist 模式的橙红 `#F0442E` 比 simple 模式的 `#E63946` 更红、饱和度更高。不要混用。

## 3. 硬投影规律（brutalist 美学核心）

所有"装饰块"用 **box-shadow 14px 14px 0** 风格的硬投影（**无模糊**），颜色二选一：
- 红 (`#F0442E`) — 主要投影色
- 黄 (`#FFD72E`) — 仅 title-3 用作强调

**尺寸规律**：投影偏移 14px（标题级）/ 12px（副标题级）/ 10px（ID 卡级）/ 8px（角标级）。**投影大小 = 元素重要性**。

## 4. 信纸背景（paper overlay）

CSS 原版用 `repeating-linear-gradient(0deg, transparent 0 20px, rgba(8,8,8,.13) 20px 21px)` + 两层 `radial-gradient` 噪点。

**PIL 等价**：
```python
# 横线：每 22px 一条 1px 黑色 alpha=42
# 噪点：random.seed(42) 固定种子，约 w*h/300 个 2×2 椭圆 alpha=80
```

固定 random seed（42）保证每次输出**像素级一致**。

## 5. 修改时检查清单

调 complex 模式任何 token 之前：
- [ ] 改了 y 坐标？看是否影响 footer 切边（h-60 是底线）
- [ ] 改了投影偏移？看是否被 16px 厚黑边截断
- [ ] 改了 title 字号？看 hook 拆 3 行后第 1 行是否能放进画布
- [ ] 改了条形码宽度？看是否越过 626px RYDER 卡右边界
- [ ] 改了 4 个 + 标记位置？看是否与其他元素重叠

## 6. v4.6 已知偏差

| 偏差 | 原版 | v4.6 | 原因 |
|------|------|------|------|
| 画布尺寸 | 1240×1654 | 1200×1600 (3:4 默认) | 适配小红书 |
| 斜切角 | 260px | 200px | 原 260 覆盖 footer |
| 角标文字 | "KOL INTEL / 04" | 保留 | 4 = 第 4 期 |
| 条形码密度 | 28px 周期 | 7px 周期 | PIL 渲染精度差异 |

如要还原原版 1240×1654 严格 1:1，改 `--aspect` 为 1240×1654（当前未支持，需在 `ASPECT_RATIOS` 加）。

---

## 7. KOL 卡片变体（v4.7 · 标题居中 + 边缘不对称）

> 区别于 complex 模式：complex 是「3 个不对称的 box 块堆叠」；KOL 卡片是「3 行**居中**的 box 块 + 边缘装饰保持张力」。
> 文件：`references/visual/kol-card-template.html` + `kol-card-style.css` + `kol-04-cover.html`（实例）

### 设计 token（1240×1654 画布）

| Token | 值 | 来源 | 备注 |
|-------|-----|------|------|
| 卡片尺寸 | 1240×1654 | `--card-w/h` | 与 complex 一致 |
| 厚黑边框 | 16px | `border: 16px solid ink` | 全周 |
| 右下斜切角 | 220px（黑色） | `clip-path` | 略小于 complex（220 vs 200） |
| **顶部左 ID 卡** | 690×104 @ (46, 46) | `.identity` | 米白底+红 LOGO+账号名 |
| **顶部右 KOL 角标** | 320×130 @ (w-54-320, 34) | `.kol-badge` | 黑底+红数字 86px+KOL INTEL 标签 |
| 红线分隔 | y=200, x=46 → w-46, 6px | `.red-divider` | 端点各有一个 6×30 黑色 tick |
| **头部左 头像** | 240×280 @ (80, 260) | `.head-avatar` | 粗黑边 8px+红硬投影 |
| **头部右 装饰方块** | 360×280 @ (w-54-360, 260) | `.head-deco` | 黄底+NEW 黑 chip+No.04 大字 |
| title-line-1 | y=600, w=980, h=130, 字号 78 | `.title-line-1` | 米白底+红投影（**居中**） |
| title-line-2 | y=760, w=880, h=130, 字号 78 | `.title-line-2` | 黑底+白字+红投影（**居中**） |
| title-line-3 | y=920, w=1080, h=150, 字号 92 | `.title-line-3` | 红底+黑字+**黄**投影（**居中**，视觉最重） |
| 副标题盒 | y=1100, w=880, h=100, 字号 42 | `.subtitle-box` | 米白+黑边+红投影（**居中**） |
| **底部左 stamp** | (46, h-184-200), 350×200 | `.stamp-card` | 红底+黑边+黑投影，数字 130px |
| **底部中 条形码** | bottom=220, w=240, h=110 | `.barcode-block` | 居中于水平中线 |
| **底部右 RYDER 卡** | (w-54-460, h-184-240), 460×240 | `.ryder-card` | 米白+黑边+红投影 |
| footer | y = h-60, 字号 22 | `.footer-note` | 英文签名档 |

### 与 complex 模式的核心差异

| 维度 | complex | KOL 卡片 |
|------|---------|----------|
| **标题布局** | 3 个左对齐 box（不对称堆叠） | 3 个**居中** box（宽度递减 1080→980→880→1080 形成节奏） |
| **顶部装饰** | meta-rail 横线 + 4 tick | 红线分隔（端点 2 tick） |
| **头部装饰** | 无 | **左头像 + 右装饰方块**（形成左右张力） |
| **底部 3 元素** | 2 元素（stamp + RYDER 卡） | **3 元素**（stamp + 条形码 + RYDER 卡，水平不对称分布） |
| **副标题位置** | y=930，独立分隔 | y=1100，紧贴 title-3 下方 |
| **使用方式** | PIL 脚本生成 PNG | HTML+CSS 模板（浏览器内 contenteditable 编辑） |

### 修改 checklist

调 KOL 卡片任何 token 之前：
- [ ] 改了 y 坐标？看是否影响副标题盒和 stamp 的垂直间距（min 30px）
- [ ] 改了标题字号？看 hook 3 行是否还能放进 880-1080 宽的居中 box
- [ ] 改了头部装饰方块？看是否和顶部 KOL 角标（y=34-164）有垂直重叠
- [ ] 改了 RYDER 卡宽度？看是否和水平居中的条形码块（w=240）有水平重叠
- [ ] 改了 logo 文字（默认 "RYDER" 5 字符）？超过 6 字符需调小 font-size 到 12px 或换 2 行布局

### 头像路径 3 种方案（按稳定性排序）

1. **同目录放 `avatar.png`**：`<img src="./avatar.png">` ← 模板默认
2. **base64 嵌入**：`<img src="data:image/png;base64,...">` ← 最稳，文件大
3. **绝对 `file://` 路径**：仅本机预览用，跨机器失效 ← 实例用此方案

详见 `SKILL.md` § 失败模式 #10。
