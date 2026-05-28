# Feishu Docx Block Types — 实测可用映射

通过 lark-cli api GET 读取已有文档的实际 block 结构，再通过 create children API 验证可写入性。

## 已验证可创建的 block 类型

| block_type | 字段名 | 用途 | 示例 |
|-----------|--------|------|------|
| 2 | `text` | 正文段落 | `{"block_type": 2, "text": {"elements": [{"text_run": {"content": "..."}}], "style": {}}}` |
| 3 | `heading1` | H1 标题 | `{"block_type": 3, "heading1": {"elements": [{"text_run": {"content": "一、..."}}], "style": {}}}` |
| 4 | `heading2` | H2 标题 | `{"block_type": 4, "heading2": {"elements": [{"text_run": {"content": "1.1 ..."}}], "style": {}}}` |
| 14 | `code` | 代码块/逐字稿原文 | `{"block_type": 14, "code": {"elements": [{"text_run": {"content": "..."}}], "style": {"language": 1, "wrap": true}}}` |
| 15 | `quote` | 引用块/金句 | `{"block_type": 15, "quote": {"elements": [{"text_run": {"content": "..."}}], "style": {}}}` |
| 22 | `divider` | 分隔线 | `{"block_type": 22, "divider": {"style": {}}}` |

## 不可用的 block 类型

| block_type | 说明 |
|-----------|------|
| 23 | 常被误认为是 code block，实际 create children API 返回 1770001 invalid param |

## 关键发现

- Code block 是 **type 14**（不是 23），字段名 `"code"`
- Quote block 是 **type 15**，字段名 `"quote"`（不是 `"callout"`）
- `text_element_style` 支持: `bold`, `italic`, `inline_code`, `strikethrough`, `underline`
- Code block 的 `style.language` 值 1 = 默认语言
- Code block 的 `style.wrap` = true 启用自动换行

## 写入命令

```bash
cd /tmp && lark-cli api POST \
  "/open-apis/docx/v1/documents/DOC_ID/blocks/DOC_ID/children" \
  --as user --data @batch_file.json
```

⚠️ `--data @file` 必须用相对路径（先 cd /tmp），不支持绝对路径。
⚠️ 每批 3-5 个 block，验证返回 `"code": 0`。
⚠️ 必须用 `--as user`，bot 身份对 user-owned wiki 返回 1770032 forbidden。
