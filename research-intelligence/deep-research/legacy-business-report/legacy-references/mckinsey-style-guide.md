# 麦肯锡风设计系统（McKinsey Style System）

> **来源**：从 v5.0 → v5.1 实战反馈迭代而来。5+ 轮用户反馈后固化的视觉样式系统。
> **实现位置**：`scripts/generate_report.py`（1595 行 Python）
> **本文件目的**：把"为什么这样设计"和"具体规则"从脚本中抽出来，让未来用本 skill 的人能直接读规则。

---

## 1. 配色系统（Color Tokens）

```python
# 麦肯锡风 - 2 色收敛
COLOR_PRIMARY   = RGBColor(31, 78, 121)    # #1F4E79 深蓝 - 标题/表头/链接
COLOR_SECONDARY = RGBColor(89, 89, 89)     # #595959 中灰 - 副标题/辅助
COLOR_TERTIARY  = RGBColor(127, 127, 127)   # #7F7F7F 浅灰 - 注释/来源
COLOR_BODY      = RGBColor(0, 0, 0)        # #000000 黑色 - 正文
COLOR_ACCENT    = RGBColor(192, 0, 0)      # #C00000 深红 - 仅关键数字
COLOR_WHITE     = RGBColor(255, 255, 255)   # #FFFFFF 纯白
COLOR_TABLE_ALT = 'F2F2F2'                  # 浅灰 - 表格交替行
COLOR_TABLE_HEADER = '1F4E79'               # 深蓝 - 表头背景
```

**配色原则**：
- **2 色收敛**：主色（深蓝）+ 中性灰（最多 3 个灰度）。**禁止**引入第 3 种主色。
- **红色只用数字**：深红 `#C00000` 仅用于 16-18pt 粗体大数字，**不**用作背景色 / 边框。
- **背景纯白**：页面与表格主底色，不要任何彩色背景。

---

## 2. 排版元素（Typography）

| 元素 | 字号 | 字重 | 颜色 | 备注 |
|------|------|------|------|------|
| 一级标题（H1 章节） | 22pt | bold | 深蓝 | 章节封面顶部 |
| 二级标题（H2） | 14pt | bold | 深蓝 | "1.1 市场概览" |
| 三级标题（H3） | 11.5pt | bold | 中灰 | 小节内 |
| 关键判断（段首） | 10.5pt | bold | 深蓝 | "判断 1." 开头 |
| 关键数字 | 16-18pt | bold | 深红或深蓝 | 单点数字 |
| 正文 | 10.5pt | normal | 黑色 | 行距 1.5 |
| 表格表头 | 10.5pt | bold | 白色 | 深蓝底色 |
| 表格数据 | 10pt | normal | 黑色 | 白底 / 灰交替 |
| 注释 / 来源 | 8.5pt | normal | 浅灰 | 链接/脚注 |

**字体**：中文用 SimSun（系统内置，跨平台兼容）。

---

## 3. 表格规则

### 标准表格
- **表头**：深蓝底 + 白字加粗 + 左对齐
- **数据行**：白底 / 浅灰交替
- **边框**：细灰线（#DDD）
- **对齐**：左对齐（不要居中）
- **列宽**：手动设置或自动

### KV 表格（2 列）
- **左列**（维度）：加粗 + 深蓝色
- **右列**（详情）：常规黑色
- **用途**：企业条目、产品参数、ROI 测算

### 多列数据表格
- **表头**：深蓝底 + 白字加粗
- **数据行**：交替白/灰
- **列宽**：根据内容手动设置
- **行高**：适中（不要过紧）

### 表格里**不要**：
- ❌ 彩色行（用蓝/白/灰交替）
- ❌ emoj（用文字）
- ❌ 表情符号替代评级（用"极强/强/中/弱"）
- ❌ 居中（用左对齐）

---

## 4. 关键判断段落（Insight Block）

**替代 callout 块的麦肯锡风方案**：

```python
def add_insight(doc, label, text):
    """关键判断 - 粗体段首 + 黑色正文（无背景）"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.3)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(6)
    
    # 段首（深蓝加粗）
    run = p.add_run(f'{label} ')
    run.font.size = Pt(10.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY
    
    # 正文（黑色）
    run = p.add_run(text)
    run.font.size = Pt(10.5)
    run.font.color.rgb = COLOR_BODY
```

**使用示例**：
```
判断 1. 国外劳工保护外骨骼是最大单一细分市场，但增速并非最快赛道
       （医疗 45% > 工业 29.4%）。切入逻辑应转为"最大容量 + To B 稳定"
       而非"最快增速"。
```

**为什么不用 callout 块**：
- 麦肯锡年报分析显示彩色背景块显得花里胡哨
- 视觉层级靠字号/粗细/颜色对比，不用色块
- 黑白正文更专业

---

## 5. 关键数字展示（Key Metric）

**单个关键数据**的展示方式：

```python
def add_key_metric(doc, label, value, source_eid=None, source_url=None):
    """关键数据 - 粗体大字 + 灰色标签 + 链接来源"""
    # 标签（浅灰小字）
    p = doc.add_paragraph()
    run = p.add_run(label)
    run.font.size = Pt(10)
    run.font.color.rgb = COLOR_SECONDARY
    
    # 数字（深红/深蓝粗体大字）
    p2 = doc.add_paragraph()
    run = p2.add_run(value)
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY
    
    # 来源（带超链接）
    if source_eid and source_url:
        p3 = doc.add_paragraph()
        run = p3.add_run('来源: ')
        run.font.size = Pt(8.5)
        run.font.color.rgb = COLOR_TERTIARY
        add_hyperlink(p3, f'[{source_eid}]', source_url, size=8.5)
```

**视觉示例**：
```
外骨骼总市场 2025
$0.56B
来源: [E10] MarketsandMarkets
```

**3 列并列展示**（关键数据矩阵）：
```python
table = doc.add_table(rows=2, cols=3)
# 行 1：标签（浅灰小字）
# 行 2：数据（深蓝 16pt 粗体大字）
```

---

## 6. 内联 evidence_id 超链接

**正文中每个 evidence_id 必须可点击**（不是只在底部参考列表）：

```python
def add_evidence_para(doc, lead_text, body_text, evidence_id, url, label=None):
    p = doc.add_paragraph()
    
    # 段首（深蓝加粗）
    if lead_text:
        run = p.add_run(lead_text)
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
    
    # 正文
    if body_text:
        run = p.add_run(body_text)
        run.font.size = Pt(10.5)
        run.font.color.rgb = COLOR_BODY
    
    # 内联超链接 evidence_id
    if evidence_id and url:
        run = p.add_run(' ')
        add_hyperlink(p, f'[{evidence_id}]', url, size=9.5)
```

**为什么内联**：
- 读者遇到"80 磅举升"想验证时直接点 `[E01]` 跳转
- 不用翻到附录再手动找 URL
- 阅读效率显著提升

---

## 7. 章节封面（Section Cover）

**简洁的章节分隔**（不是大色块）：

```python
def add_section_cover(doc, chapter_num, chapter_title, subtitle=None):
    # 顶部细蓝横线
    add_hr_line(doc)
    
    # 章节号（小灰字）
    p = doc.add_paragraph()
    run = p.add_run(f'第 {chapter_num} 章')
    run.font.size = Pt(11)
    run.font.color.rgb = COLOR_TERTIARY
    
    # 章节标题（大蓝字）
    p2 = doc.add_paragraph()
    run = p2.add_run(chapter_title)
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY
    
    # 副标题（可选，浅灰斜体）
    if subtitle:
        p3 = doc.add_paragraph()
        run = p3.add_run(subtitle)
        run.font.size = Pt(11)
        run.font.italic = True
        run.font.color.rgb = COLOR_SECONDARY
    
    # 底部细蓝横线
    add_hr_line(doc)
```

**为什么不要大色块**：
- 麦肯锡风要求克制
- 章节封面是结构提示，不是视觉冲击
- 横线 + 字号已足够区分

---

## 8. 封面 Banner 图（matplotlib）

**深蓝科技感 banner** 设计原则：

```python
def render_banner(output_path):
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    mpl.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'STHeiti', 'Songti SC', 'sans-serif']
    mpl.rcParams['axes.unicode_minus'] = False
    
    # 配色
    PRIMARY = '#1F4E79'
    DARK = '#0E2D4A'
    LIGHT = '#4A7BA8'
    GOLD = '#C9A961'
    WHITE = '#FFFFFF'
    
    # 画布：9:3 比例（适合 Word 顶部通栏）
    fig, ax = plt.subplots(figsize=(9, 3), dpi=150)
    
    # 背景：深蓝渐变
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    cmap = LinearSegmentedColormap.from_list('mckinsey', [PRIMARY, DARK])
    ax.imshow(gradient, extent=[0, 100, 0, 33], aspect='auto', cmap=cmap)
    
    # 元素：
    # - 细网格底纹（alpha 0.06）
    # - 3 条数据线（白色主 + 浅蓝辅 + 金色）
    # - 关键数据点（白色圆圈）
    # - 顶部金色装饰条
    # - 左下文字 / 右上品牌 / 右下关键数字
    
    plt.savefig(output_path, dpi=150, bbox_inches='tight', pad_inches=0, facecolor=DARK)
```

**关键设计**：
- 渐变方向：左上深 → 右下深
- 数据线：白色（主）+ 浅蓝（辅）+ 金色（机会）
- 关键数字：右下用 22pt 金色大字（如"5%"）
- 顶部金色装饰条：1 行细线，麦肯锡风点缀

---

## 9. 单一 .docx 输出（Single Deliverable）

**不产生独立 plan/ledger/sources 文件**——全部嵌入 Word 附录：

| 附录 | 内容 | 嵌入方式 |
|------|------|----------|
| 附录 A | 检索计划（research_plan.json） | KV 表格 |
| 附录 B | 证据账本（evidence_ledger.md） | 多列数据表格 |
| 附录 C | 信源透明度报告 | 表格化（**不是**机械预筛输出） |
| 附录 D | 参考来源（evidence_id URL 列表） | 编号 + 可点击超链接 |

**工作文件清理**：plan/ledger/sources/verified 放 `/tmp/<项目名>/`，**交付后清理**。

---

## 10. 报告标题与文件名分离

| 类型 | 格式 | 示例 |
|------|------|------|
| 报告标题（Word 内） | `<主题>深度调研报告：<核心结论> (<窗口期>)` | `国内外劳工外骨骼市场深度调研报告：玩家格局、商业模式与切入机会（2026 H1）` |
| 文件名 | `<主题中文>-<核心结论简写>-<YYYY-MM-DD>.docx` | `国内外劳工外骨骼市场深度调研报告-玩家格局商业模式与切入机会-2026-06-10.docx` |

**文件名不含版本号（v1/v2/v3）** —— 迭代在标题内重写而非文件名累积。

---

## 11. 验证清单（Style Checklist）

每次生成 .docx 前自检：

- [ ] 2 色收敛（深蓝 + 中性灰），没有引入第 3 主色
- [ ] 没有 emoj（检查所有字符串）
- [ ] 没有彩色 callout 块（无粉/蓝/绿/红/黄背景）
- [ ] 表格：白底 + 蓝头条 + 灰交替行
- [ ] 关键判断：粗体段首 + 黑色正文（无背景）
- [ ] 关键数字：16-18pt 粗体大字
- [ ] 行距 1.4-1.6
- [ ] 字体 SimSun
- [ ] Banner 图：matplotlib 深蓝科技感
- [ ] 单一 .docx 交付
- [ ] 30+ evidence_id 内联可点击
- [ ] 5W2H 主动反问触发条件满足
- [ ] 报告标题与文件名分离
- [ ] 附录 C 是"信源透明度报告"（不是"机械预筛输出"）
- [ ] 报告无"报告结束"页

---

## 12. 已知问题与边界

| 问题 | 影响 | 缓解 |
|------|------|------|
| 标题与正文同色时，目录条目看不清 | 视觉层级弱 | 目录条目用 Pt(11.5) + bold + 深蓝 |
| Banner 在 4K 屏上可能模糊 | 不影响 Word 显示 | dpi=150 已经足够 |
| 表格超过 8 列时排版拥挤 | 视觉拥挤 | 拆成多张子表或换 K-V 形式 |
| 长 URL 在附录 D 折行 | 不影响可点击 | 不强制处理，Word 自动折行 |
| 中文字体（SimSun）在不同 OS 显示略有差异 | 视觉差异 | SimSun 是 macOS/Windows 都内置的字体 |
| matplotlib 渲染中文需指定字体 | 报"missing glyph"警告 | 设置 `mpl.rcParams['font.sans-serif']` 优先级列表 |

---

## 13. 复用与改造

如果要新写一份同风格的报告，**直接复用** `scripts/generate_report.py`：
- 保留所有 helper 函数（`add_hyperlink`, `make_kv_table`, `make_data_table`, `add_evidence_para`, `add_insight`, `add_section_cover` 等）
- 替换 `build_report()` 函数内的内容（章节、数据、表格）
- 替换 `SOURCES` 字典为新主题的 evidence_id
- 替换 `render_banner()` 内的文字（"DEEP RESEARCH"、"GLOBAL INDUSTRIAL ..."）

**改造不是"重写"** —— 90% 代码可复用，只需替换数据。

---

**版本**：v5.1（2026-06-10）
**作者**：Ryder AI Signal
