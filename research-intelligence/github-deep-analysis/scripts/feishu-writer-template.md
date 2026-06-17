# 飞书文档写入模板脚本

Phase 3 成文时直接 import 使用，避免每次手拼 block 结构。

## 使用方式

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/research/github-deep-analysis/scripts"))
from feishu_writer import FeishuWriter

writer = FeishuWriter(title="MemPalace：存一切，找得到")
writer.add_h1("开篇标题")
writer.add_h2("1. 章节标题")
writer.add_p("正文段落")
writer.add_p("带链接段落", links={"MemPalace": "https://github.com/MemPalace/mempalace"})
writer.add_bullet_list(["项目A", "项目B", "项目C"])
writer.add_numbered_list(["步骤1", "步骤2", "步骤3"])
writer.add_table(headers=["维度", "值"], rows=[["Stars", "44.3k"], ["协议", "MIT"]])
writer.add_quote("引用文本")
writer.publish()  # 创建文档 + 返回链接
```

## Block 构建规则

- H1: block_type=3, heading1 key
- H2: block_type=4, heading2 key
- H3: block_type=5, heading3 key
- 段落: block_type=2, text key
- 引用: block_type=15, quote key
- 有序列表: block_type=12, ordered key
- 无序列表: block_type=13, bullet key
- 表格: 需要独立处理（复杂，建议用段落+文本模拟）

链接格式：
```python
{
    "text_run": {
        "content": "显示文本",
        "link": {"url": "https://..."}
    }
}
```
