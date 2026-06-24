# 头像驱动的视觉设计（Avatar-Driven Visual Design）

> 适用于所有 Ryder 个人 IP 相关的视觉设计场景。
> **核心原则**：视觉风格 = 头像调性 + 钩子句文案 + 5 主题配色体系。

## 为什么需要这个范式

**v4.1 失败教训**：早期尝试用"暗色 Cyberpunk + 荧光"调性做 Ryder 的视觉，但用户的实际头像（米黄背景 + 橙白蓝条纹毛衣 + 黑发戴眼镜温和笑容）是**暖色调产品经理/独立创作者**调性——**和暗色 Cyberpunk 完全冲突**。

用户原话："调性和头像不匹配"、"效果特别特别差"、"同质化太强"。

**结论**：视觉调性必须从用户的**头像/角色**派生，不能套用通用"科技感"调性。

## 头像调性分析（Ryder 二次元头像）

| 元素 | 特征 | 调性暗示 |
|------|------|---------|
| 背景 | 米黄渐变 | 暖、温和、友好 |
| 服饰 | 橙白蓝条纹毛衣 | 知性、稳重、不张扬 |
| 发型 | 黑发、刘海 | 邻家、专业 |
| 配饰 | 眼镜 | 产品经理/独立创作者 |
| 表情 | 温和自信微笑 | 信任、亲和 |
| 整体 | "温暖的产品经理" | **不冷、不酷、不极客** |

→ **派生调性**：温暖的科技感 / 知性产品经理 / 独立创作者

## 5 主题配色体系（基于头像暖色调）

所有主题从**头像调性**派生，**全部暖色调**。**禁止用暗色/赛博朋克/霓虹调性**。

| 主题 | 背景 | accent | accent2 | 调性 | 推荐 |
|------|------|--------|---------|------|------|
| ⭐ **cream** | #F5E6D3 奶油 | #D62828 深红 | #003049 深蓝 | 克制专业 | **主推**（IP/知识/咨询/产品） |
| warm | #FFE8B0 暖米黄 | #FF6B35 暖橙 | #1F4E79 深蓝 | 友好生活化 | 工具/教程 |
| peach | #FFD4B8 桃粉 | #E63946 红 | #1F4E79 深蓝 | 女性向 | 美妆/生活 |
| coral | #FF8B6B 珊瑚 | #FFD60A 亮黄 | #1F4E79 深蓝 | 活泼 | 年轻向/兴趣 |
| olive | #C7D580 暖橄榄 | #FF6B35 暖橙 | #1F4E79 深蓝 | 知性 | 文学/哲学/独立 |

**配色原则**：
- 背景 = 头像调性的近邻色（warm/cream/peach 接近头像米黄）
- accent = 头像服饰色（橙、红、深红等）
- accent2 = Ryder 品牌主色 #1F4E79（深蓝）

**色温检测**：所有主题都应该是"暖色温"——色相 < 60° 或 > 300° + 低饱和度。**禁止用冷色温**（青/紫/深绿 + 高饱和度）。

## 视觉锚点：头像 ≠ 角标

**反 v4.1 范式**：v4.1 把头像当作"小角标"（"R monogram"），仅占画面 1-5%。这浪费了 IP 资产。

**v4.2 范式**：头像 = 视觉锚点，占画面 30-50%。

### 封面用法（大头像）

- 尺寸：`w * 0.40`（1200×1600 → 480px 直径）
- 处理：圆形 + 10px 黑边 + 10px 硬投影
- 位置：中央偏下（让出顶部标题区）

### 内页用法（小头像）

- 尺寸：80px 直径
- 处理：圆形 + 4px 黑边
- 位置：顶 header 左上角（伴随标题）

### 视觉实现（card_generator.py）

```python
def make_circular_avatar(avatar_path, size, border_color="#0A0A0A", border_width=8):
    """裁剪成圆形 + 黑边 + 硬投影"""
    img = Image.open(avatar_path).convert("RGBA")
    img.thumbnail((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([(0,0),(size,size)], fill=255)
    avatar = Image.new("RGBA", (size,size), (0,0,0,0))
    offset = ((size-img.width)//2, (size-img.height)//2)
    avatar.paste(img, offset, img.split()[3] if img.mode=="RGBA" else None)
    avatar.putalpha(mask)
    return avatar
```

**重要**：从 `<skill>/assets/avatar.png` 读取，**不依赖外部路径**。换头像不需要改代码。

## 封面 = 标题替代品

**核心认知**：用户原话"封面可以替代标题...因为很多人其实会最先看到封面图，因此封面图的内容有时候甚至比标题还重要"。

**封面 5 元素**（v4.2 标准结构）：

```
┌────────────────────────────────────┐
│ [叫我 Ryder 即可]   [KOL 情报库]   │  ← 角标区
│                                    │
│     {主钩子句（2-3 行）}            │  ← 钩子区（最关键）
│     [副钩子标签]                   │  ← 副钩子区
│                                    │
│           [头像大圆]                │  ← 锚点区
│                                    │
│     Ryder's KOL Intelligence        │  ← 底部副标
└────────────────────────────────────┘
```

**钩子句公式**（4 种）：

| 钩子类型 | 公式 | 例子 |
|---------|------|------|
| 身份贩卖 | "高段位 [人群] 都应该有 [X]" | 高段位 AI 决策者都应该有 KOL 情报库 |
| 痛点共鸣 | "[时长] [行为], [结果] [情绪]" | 看 2 小时 KOL, 第二天全忘了 |
| 反认知震撼 | "看 [X] ≠ 学习, [N]% 的人搞错了" | 看 KOL≠学习, 99% 的人搞错了 |
| 生活方式 | "我想成为 [那种人], 因为 [X]" | 我想成为有 KOL 情报库的人 |

**视觉技巧**：
- **错位阴影**：钩子句文字 = 黑色主字 + 6% 字号偏移的 accent 色阴影
- **硬投影**：标签 = 4px 黑边 + 4-12px 硬投影偏移
- **不要用反白效果**（`draw.text` 用背景色填充）—— 中文 CJK 字体兼容问题

## 内页 = 辅助说明

**核心认知**：用户原话"其他的图片主要用于放一些辅助的图片，比如如何使用，然后辅之以少量的文本"。

**4 种内页 layout**：

| 函数 | 用途 | 输入格式 |
|------|------|---------|
| `render_inside_steps()` | 4 步操作流程 | `[(title, desc), ...]` |
| `render_inside_data()` | 4 个大数据 | `[(num, unit, desc), ...]` |
| `render_inside_concept("transform")` | 拆解手术（左视频→右笔记） | title + desc |
| `render_inside_concept("layers")` | 4 层金字塔 | title + desc |

**设计原则**：
- 顶部统一 header（小头像 + 标题 + 副标）
- 主体：图为主、文为辅
- 不堆字（每图 ≤ 30 个字核心信息）
- 底部统一 footer（"Ryder's KOL Intelligence"）

## 视觉化技术（实现细节）

### 错位阴影（Offset Shadow）

```python
# 钩子句：黑字 + accent 色阴影
offset = int(font_size * 0.06)
draw.text((x + offset, y + offset), text, font=font, fill=accent_color)
draw.text((x, y), text, font=font, fill=fg_color)
```

### 硬投影标签

```python
def draw_label(draw, text, x, y, font, fg, bg, border):
    tw, th = text_size(draw, text, font)
    pad = 20
    # 硬投影（4px 偏移）
    draw.rectangle([(x+4, y+4), (x+tw+pad*2+4, y+th+pad+4)], fill=border)
    # 主色块 + 4px 黑边
    draw.rectangle([(x, y), (x+tw+pad*2, y+th+pad)], fill=bg, outline=border, width=4)
    draw.text((x+pad, y+pad//2-2), text, font=font, fill=fg)
```

### CJK 字体 fallback（必填）

```python
def _has_cjk(text):
    return any(0x4E00 <= ord(c) <= 0x9FFF or 
               0x3000 <= ord(c) <= 0x303F or 
               0xFF00 <= ord(c) <= 0xFFEF for c in text)

def select_font(role, text, size):
    """CJK 文本自动用 CJK 字体"""
    if _has_cjk(text):
        return load_font("display", size)
    return load_font(role, size)
```

**关键**：PIL `ImageFont.truetype()` **不会自动 fallback 字符集**。加载 `Helvetica.ttc` 渲染中文 = 方框。**必须**用 `select_font()`。

## 反模式（v4.2 实战教训）

1. **❌ 暗色 Cyberpunk / 霓虹调性**（v4.1 失败）—— 和暖色调头像冲突
2. **❌ 头像当小角标**（v4.1 失败）—— 浪费 IP 资产
3. **❌ 封面写描述性文字**（"AI 产品经理的真相"）—— 应该是钩子句
4. **❌ 内页堆字** —— 违反"图为主、文为辅"
5. **❌ 文字用反白效果**（背景色填充）—— CJK 字体兼容问题
6. **❌ emoji 当 ASCII 处理** —— 方框，详见 `references/implementation-notes.md`
7. **❌ 装饰性 emoji** —— 破坏专业调性
8. **❌ 渐变滥用** —— 麦肯锡式的克制更好

## 实战 Checklist（新内容前必查）

- [ ] 头像调性已分析（暖/冷/中性）
- [ ] 主题色基于头像调性（暖色 → 5 主题任选）
- [ ] 封面上有大头像（≥ w * 0.40）
- [ ] 封面文字 = 钩子句（4 种公式任选）
- [ ] 内页 = 辅助说明（图为主）
- [ ] CJK 字体 fallback 已用 `select_font()`
- [ ] 没有暗 Cyberpunk 调性
- [ ] 主题色统一（1 个内容包 = 1 个主题）

## 延伸阅读

- `SKILL.md` §v4.2 范式（核心规则）
- `SKILL.md` §Common Pitfalls #10/11/12/13（v4.2 关键）
- `references/implementation-notes.md`（CJK 字体实现细节）
- `scripts/card_generator.py`（完整实现）
