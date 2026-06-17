# Word (.docx) 报告生成技术指南

> 2025年6月整理，源自外骨骼劳工保护调研报告v1-v3迭代

## 适用场景

当用户要求生成可编辑Word文档（而非PDF），或需要：
- 可点击超链接来源
- 封面页+目录
- 复杂表格样式（表头颜色、交替行底色）
- 企业条目按"概述段+KV表格"格式排版

## 依赖

```bash
pip install python-docx
# 当前版本: python-docx 1.2.0
# 路径: ~/.local/lib/python3.12/site-packages/ 或 venv中
```

## 核心工具函数

### 1. 可点击超链接

python-docx原生不支持超链接，需通过OxmlElement手动构建：

```python
def add_hyperlink(paragraph, text, url):
    """在段落中添加可点击蓝色下划线超链接"""
    part = paragraph.part
    r_id = part.relate_to(
        url,
        'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',
        is_external=True
    )
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    c = OxmlElement('w:color')
    c.set(qn('w:val'), '0563C1')  # Word默认超链接蓝
    rPr.append(c)
    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), '19')  # 9.5pt
    rPr.append(sz)
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return paragraph
```

使用方式：
```python
p = doc.add_paragraph()
run = p.add_run('1. ')  # 编号
run.font.size = Pt(9)
add_hyperlink(p, '来源标题', 'https://example.com')
```

⚠️ **陷阱**：`add_hyperlink` 必须在段落已加入document后调用（需要`paragraph.part`），不能在游离段落上使用。

### 2. 表格样式工具

#### 单元格底色

```python
def set_cell_shading(cell, color_hex):
    """设置单元格背景色，color_hex如'1F4E79'（不带#）"""
    shading_elm = OxmlElement('w:shd')
    shading_elm.set(qn('w:fill'), color_hex)
    shading_elm.set(qn('w:val'), 'clear')
    cell._tc.get_or_add_tcPr().append(shading_elm)
```

#### 通用表格格式化

```python
def format_table(table, header_color='1F4E79'):
    """应用标准样式：深色表头白字+交替行底色+字号"""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # 表头：深色底+白色粗体字
    for cell in table.rows[0].cells:
        set_cell_shading(cell, header_color)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.color.rgb = RGBColor(255, 255, 255)
                r.font.bold = True
                r.font.size = Pt(10)
    # 数据行：交替浅灰底+10pt字
    for i, row in enumerate(table.rows[1:], 1):
        for cell in row.cells:
            if i % 2 == 0:
                set_cell_shading(cell, 'F2F2F2')
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)
```

#### KV表格（企业条目专用）

企业条目标准格式：2列表（维度+详情），用此helper避免行数计算错误：

```python
def make_kv_table(doc, data_rows, headers=None):
    """创建KV表格。data_rows = [(key, value), ...]"""
    if headers is None:
        headers = ['维度', '详情']
    t = doc.add_table(rows=1 + len(data_rows), cols=2)
    t.style = 'Table Grid'
    t.rows[0].cells[0].text = headers[0]
    t.rows[0].cells[1].text = headers[1]
    for i, (k, v) in enumerate(data_rows):
        t.rows[i+1].cells[0].text = k
        t.rows[i+1].cells[1].text = v
    format_table(t)
    return t
```

#### 多列数据表格

```python
def make_data_table(doc, headers, data_rows):
    """创建多列表格。headers=['列1','列2',...], data_rows=[[v1,v2,...], ...]"""
    t = doc.add_table(rows=1 + len(data_rows), cols=len(headers))
    t.style = 'Table Grid'
    for j, h in enumerate(headers):
        t.rows[0].cells[j].text = h
    for i, row in enumerate(data_rows):
        for j, val in enumerate(row):
            t.rows[i+1].cells[j].text = val
    format_table(t)
    return t
```

⚠️ **行数计算bug**：`doc.add_table(rows=N, ...)` 的N必须 = 1（header）+ len(data_rows)。常见错误：8行数据写了`rows=8`但忘加header那行，导致`IndexError: list index out of range`。用`make_kv_table`和`make_data_table`可以避免此问题。

### 3. 封面页

```python
for _ in range(6):
    doc.add_paragraph()  # 空行撑开

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('报告标题')
run.font.size = Pt(28)
run.font.bold = True
run.font.color.rgb = RGBColor(31, 78, 121)

doc.add_paragraph()  # 空行

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('English Subtitle')
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(89, 89, 89)

doc.add_page_break()
```

### 4. 目录页（手动）

Word自动目录需要打开文档后按Ctrl+A→F9刷新，对用户不便。改用手动目录：

```python
toc_items = ['一、章节1', '二、章节2', ...]
for item in toc_items:
    p = doc.add_paragraph()
    run = p.add_run(item)
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(31, 78, 121)
doc.add_page_break()
```

### 5. 中文字体设置

```python
style = doc.styles['Normal']
font = style.font
font.name = 'SimSun'
font.size = Pt(10.5)
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'SimSun')
```

### 6. 特定单元格着色（如红色标注最快增速）

```python
t = make_data_table(doc, [...], [...])
# 对第一行数据着红色
for cell in t.rows[1].cells:
    for p in cell.paragraphs:
        for r in p.runs:
            r.font.color.rgb = RGBColor(192, 0, 0)
            r.font.bold = True
```

## 完整报告结构模板

```python
doc = Document()
# 1. 中文字体设置
# 2. 封面页（6空行+标题+英文副标题+日期+分页）
# 3. 目录页（手动目录+分页）
# 4. 正文各章（heading→段落→表格→分页）
#    - 企业条目：概述段(2-3句) → make_kv_table
#    - 市场数据：make_data_table
#    - 核心结论：红色加粗
# 5. 参考来源（编号+add_hyperlink）
# 6. doc.save(path)
```

## 与PDF管线的选择

| 维度 | Word (python-docx) | PDF (md-to-pdf) |
|------|-------------------|-----------------|
| 可编辑性 | ✅ 用户可编辑 | ❌ 只读 |
| 超链接 | ✅ 可点击 | ✅ 可点击 |
| 中文排版 | ⚠️ 需手动设字体 | ✅ CSS字体回退链 |
| 复杂表格 | ✅ 底色/合并/对齐 | ⚠️ 需写HTML |
| 封面/目录 | ✅ 原生支持 | ⚠️ 需CSS分页 |
| 文件大小 | 50-100KB | 200-500KB |

**建议**：调研报告优先Word（用户常需编辑/调整），正式交付可用PDF。

## 常见陷阱

1. **行数计算错误**：`add_table(rows=N)` 的N必须含header行（N=1+len(data)）
2. **超链接在游离段落上报错**：必须先`doc.add_paragraph()`再加入超链接
3. **中文字体不生效**：需同时设`font.name`和`rPr.rFonts.set(qn('w:eastAsia'), ...)`
4. **表格无Table Grid样式**：必须显式设`table.style = 'Table Grid'`，否则无边框
5. **来源编号重排**：删除某条来源后需全部重新编号，Markdown和Word同步更新
