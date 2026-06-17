"""
飞书文档写入器 — Phase 3 成文专用

用法:
    from feishu_writer import FeishuWriter
    writer = FeishuWriter(title="文章标题")
    writer.add_h2("1. 章节标题")
    writer.add_p("正文段落")
    writer.add_p("带链接段落", links={"显示文本": "https://url"})
    writer.add_bullet_list(["项目A", "项目B"])
    writer.add_numbered_list(["步骤1", "步骤2"])
    writer.add_quote("引用文本")
    writer.publish()

已知飞书 API 兼容问题：
- block_type 12 (ordered) 和 13 (bullet) 返回 invalid param，用段落模拟替代
- block_type 22 (divider) 必须带 "divider": {} 才能写入，空 dict 不行
- link 必须放在 text_element_style 内部，放在 text_run 根级别会静默丢失
- 无法原地更新已有文档：飞书 docx API 没有可靠的 update/delete block 端点，迭代时只能创建新文档
"""

import sys, os
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/productivity/feishu-docs/scripts"))
from feishu_api import call, create_doc, append_doc_blocks


class FeishuWriter:
    def __init__(self, title="Untitled"):
        self.title = title
        self.blocks = []
        self.doc_id = None
        self.doc_url = None

    def _text_element(self, content, link=None):
        """构建单个 text_run element
        
        飞书 API 的 link 必须放在 text_element_style 内部：
        {"text_run": {"content": "...", "text_element_style": {"link": {"url": "..."}}}}
        """
        style = {}
        if link:
            style["link"] = {"url": link}
        elem = {"text_run": {"content": content}}
        if style:
            elem["text_run"]["text_element_style"] = style
        return elem

    def _build_text_elements(self, text, links=None):
        """构建 elements 列表，支持内嵌链接
        
        links: {"显示文本": "url", ...}
        如果文本中包含链接文本，会被替换为带链接的 element
        """
        if not links:
            return [self._text_element(text)]
        
        elements = []
        remaining = text
        # 按 links 字典中的 key 在文本中出现的位置依次分割
        while remaining and links:
            # 找最早出现的 link key
            earliest_pos = len(remaining)
            earliest_key = None
            for key in list(links.keys()):
                pos = remaining.find(key)
                if pos != -1 and pos < earliest_pos:
                    earliest_pos = pos
                    earliest_key = key
            
            if earliest_key is None:
                break
            
            # 前面的普通文本
            if earliest_pos > 0:
                elements.append(self._text_element(remaining[:earliest_pos]))
            
            # 链接文本
            elements.append(self._text_element(earliest_key, links[earliest_key]))
            
            remaining = remaining[earliest_pos + len(earliest_key):]
            del links[earliest_key]
        
        # 剩余普通文本
        if remaining:
            elements.append(self._text_element(remaining))
        
        return elements

    def add_h1(self, text):
        self.blocks.append({
            "block_type": 3,
            "heading1": {"elements": [self._text_element(text)]}
        })
        return self

    def add_h2(self, text):
        self.blocks.append({
            "block_type": 4,
            "heading2": {"elements": [self._text_element(text)]}
        })
        return self

    def add_h3(self, text):
        self.blocks.append({
            "block_type": 5,
            "heading3": {"elements": [self._text_element(text)]}
        })
        return self

    def add_p(self, text, links=None):
        """添加段落，可选内嵌链接"""
        elements = self._build_text_elements(text, links.copy() if links else None)
        self.blocks.append({
            "block_type": 2,
            "text": {"elements": elements}
        })
        return self

    def add_quote(self, text, links=None):
        elements = self._build_text_elements(text, links.copy() if links else None)
        self.blocks.append({
            "block_type": 15,
            "quote": {"elements": elements}
        })
        return self

    def add_bullet_list(self, items, links_per_item=None):
        """添加无序列表（用段落模拟，飞书 API block_type 13 格式不兼容）"""
        for i, item in enumerate(items):
            item_links = links_per_item[i] if links_per_item and i < len(links_per_item) else None
            elements = self._build_text_elements(f"• {item}", item_links.copy() if item_links else None)
            self.blocks.append({
                "block_type": 2,
                "text": {"elements": elements}
            })
        return self

    def add_numbered_list(self, items, links_per_item=None):
        """添加有序列表（用段落模拟，飞书 API block_type 12 格式不兼容）"""
        for i, item in enumerate(items):
            item_links = links_per_item[i] if links_per_item and i < len(links_per_item) else None
            elements = self._build_text_elements(f"{i+1}. {item}", item_links.copy() if item_links else None)
            self.blocks.append({
                "block_type": 2,
                "text": {"elements": elements}
            })
        return self

    def add_divider(self):
        """添加分割线（必须带 "divider": {}）"""
        self.blocks.append({"block_type": 22, "divider": {}})
        return self

    def add_table_from_data(self, headers, rows):
        """用段落模拟简单表格（飞书表格 API 复杂，段落更稳定）
        
        headers: ["列1", "列2"]
        rows: [["值1", "值2"], ...]
        """
        # 表头
        header_text = " | ".join(headers)
        self.add_p(header_text)
        # 分隔
        sep_text = " | ".join(["---"] * len(headers))
        self.add_p(sep_text)
        # 数据行
        for row in rows:
            row_text = " | ".join(str(c) for c in row)
            self.add_p(row_text)
        return self

    def publish(self):
        """创建文档并写入所有内容，返回文档信息"""
        # 创建文档
        doc = create_doc(title=self.title)
        self.doc_id = doc["document_id"]
        
        # 写入内容（分批，每批最多 50 个 block）
        batch_size = 50
        for i in range(0, len(self.blocks), batch_size):
            batch = self.blocks[i:i+batch_size]
            append_doc_blocks(self.doc_id, batch)
        
        self.doc_url = f"https://zvwp0lbu2oh.feishu.cn/docx/{self.doc_id}"
        return {
            "doc_id": self.doc_id,
            "doc_url": self.doc_url,
            "block_count": len(self.blocks)
        }

    def attach_to_wiki(self, space_id, parent_node_token):
        """尝试将文档挂到 wiki 节点下（需要空间权限）"""
        try:
            result = call("POST", f"/wiki/v2/spaces/{space_id}/nodes", {
                "parent_node_token": parent_node_token,
                "node_type": "origin",
                "obj_type": "docx",
                "obj_token": self.doc_id
            })
            if result.get("code") == 0:
                return {"success": True, "node_token": result["data"]["node"]["node_token"]}
            else:
                return {"success": False, "error": result.get("msg"), "code": result.get("code")}
        except Exception as e:
            return {"success": False, "error": str(e)}
