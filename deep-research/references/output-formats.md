# 输出格式与交付（v1.3.1 更新）

**v1.3.1 重大变更**：`.docx` 麦肯锡风报告**升级为默认主交付物**（不需 `--word` 标志），Markdown 降为可选（需 `--with-md` 标志）。**根因**：用户 2 次反馈"为什么没给 Word"和"报告和 word 不一样"——.docx 不是"可选"是"默认"。

deep-research 任务完成后，按以下顺序交付（前 3 种默认，后 2 种可选）。

## 输出 1: .docx 麦肯锡风报告（**v1.3.1 默认主交付物**）

**位置**：`~/Documents/Obsidian Vault/深度调研/<主题中文>DeepResearch报告-<核心结论简写>-<窗口期>.docx`

**文件名规范**：
- ✅ 格式：`<主题中文>DeepResearch报告-<核心结论简写>-<窗口期>.docx`
- ✅ 例：`外骨骼劳工保护DeepResearch报告-玩家格局商业模式与切入机会-2024-2026.docx`
- ❌ 不要 v1/v2/v3 后缀（迭代历史归档到 `.archive/`）
- ❌ 不要纯英文文件名（如 `ai-product-evolution-2024-2026.docx`）

**实现**：`scripts/word_output.py`（麦肯锡风 .docx 渲染器）—— 含 banner 图 + 9 章正文 + 4 附录 + 内联超链接 + evidence_id。

**麦肯锡风样式系统**：详见 `references/mckinsey-style-guide.md`（v5.1 沉淀的 8 条设计原则 + 2 色配色 + 7 个 Pitfall）。

**报告标题 vs 文件名 vs Obsidian 索引 3 类区分**：详见 `references/report-title-conventions.md`。

**v1.3.1 强化要点**：
- **不要结尾页**（LAW 10 #4）—— 报告在最后一个附录自然结束
- **国别旗 emoj 也要替换**（LAW 10 #1 强化）—— `🇺🇸 🇨🇳` 改为"美国""中国"或"（美国）""（中国）"
- **Obsidian 索引 < 30 行**——不复制报告全文

## 输出 2: 对话中显示（必选）

直接在 chat 里展示：
- 报告核心结论（执行摘要级别的 3-5 条）
- 关键数据 + evidence_id 链接
- 跳转 Obsidian .docx 的指引
- **不展示**完整报告全文（避免 chat 刷屏）

**为什么不直接在对话显示完整报告**：报告 60-150KB / 400+ 段，对话中显示会被截断；.docx 才是真正的报告载体，对话只显示摘要 + 链接。

## 输出 2: Obsidian Vault 备份（必选）

**默认路径**：`/Users/rydersun/Documents/Obsidian Vault/深度调研/`

⚠️ 文件夹不存在时需先创建：`mkdir -p "/Users/rydersun/Documents/Obsidian Vault/深度调研"`

**文件名格式**：`<topic>-<YYYY-MM-DD>.md`
- topic 用连字符替换空格和特殊字符
- 例：`anthropic-computer-use-2026-04-15.md`
- 例：`llm-api-competitor-2026-04-15.md`

**文件结构**（frontmatter + 完整报告）：

```markdown
---
title: "<topic> 深度调研"
type: <tech-trend | product-deep | competitor | industry-market>
generated: <YYYY-MM-DD>
window: <window description>
tags:
  - 深度调研
  - <场景类型>
sources_count:
  L1: <N>
  L2: <N>
  L3: <N>
  L4: <N>
  L5: <N>
---

[完整报告内容，对话中显示的版本]

## 信源清单

[按 L1-L5 分类的完整信源清单，每条带 URL 和抓取日期]
```

**写入方式**：用 `write_file` 工具直接写入。

⚠️ **不要用 Obsidian CLI 写入**——`obsidian append` 会在 ~1500 字符处截断，长报告会丢尾部（kol-interview-to-wiki 已踩坑）。

**写入后告知用户**：
```
📁 已备份到 Obsidian: ~/Documents/Obsidian Vault/深度调研/<topic>-<YYYY-MM-DD>.md
```

## 输出 3: 飞书 wiki 写入（可选，需 `--feishu` 标志）

仅当用户 query 含 `--feishu` 时执行。参考 kol-interview-to-wiki 的飞书 wiki 写入链路：

### 步骤

1. **创建飞书 wiki 子节点**：用 `lark-cli doc create --title "<topic> 深度调研" --parent-node <parent_token>` 创建一个子文档
2. **写入报告内容**：用 `lark-cli doc update --content <markdown>` 把完整报告写入
3. **返回 wiki URL**：告知用户

### Markdown → 飞书 block 转换

参考 kol-interview-to-wiki 的 `references/feishu-block-types.md`（如需进一步定制，可借鉴 kol-interview-to-wiki 的实现）。

简化的转换规则：
- `##` → `[H1]` 块
- `**加粗**` → `[Text]` 块 + `<b>` 标签
- `>` 引用 → `[Quote]` 块
- `-` 列表 → `[Bullet]` 块
- ` ``` ` 代码块 → `[Code]` 块
- 普通段落 → `[Text]` 块

### 飞书 wiki MOC 更新

**默认不更新 MOC**（避免污染 kol-interview-to-wiki 的 KOL 情报 MOC）。如需汇总，在 Obsidian 目录里另建 `深度调研 MOC.md` 维护索引。

## 用户标志说明

| 标志 | 含义 | 默认值 |
|------|------|--------|
| `--type <type>` | 强制场景类型 | 自动判定 |
| `--window <N>` | 时间窗口（7/30/90/180/365/all） | 90 |
| `--feishu` | 额外写入飞书 wiki 子节点 | 否 |
| `--no-obsidian` | 跳过 Obsidian 备份 | 否（默认备份） |
| `--pdf` | 额外生成 PDF | 否 |
| `--word` / `--docx` | 额外生成麦肯锡风 .docx（v1.3 新增） | 否 |
| `--entities <A,B,C>` | 显式指定实体（竞品对比时） | 自动提取 |

## 输出 4: Word .docx 输出（可选，需 `--word` 标志，v1.3 新增）

**适用场景**：用户明确要 Word 格式——给领导/投资人看、打印分享、需要可编辑+可点击超链接+复杂表格。

**实现方式**：`scripts/word_output.py`（麦肯锡风 .docx 渲染器，82KB / 含 banner 图渲染 + 9 章正文 + 4 附录结构）。

**触发方式**：
- 用户在 query 里加 `--word` 或 `--docx` 标志
- 或用户明确说"我要 Word 报告"/"给领导看"/"打印版"

**Word 输出特性（对比默认 Markdown）**：

| 维度 | Markdown（默认） | Word .docx（可选）|
|------|-----------------|-------------------|
| 可编辑性 | ⚠️ 排版弱 | ✅ 用户可编辑 |
| 超链接 | ✅ 可点击 | ✅ 可点击 |
| 复杂表格 | ⚠️ 需写 HTML | ✅ 底色/对齐/合并 |
| 封面 Banner | ❌ 无 | ✅ matplotlib 渲染深蓝科技感 |
| 章节封面 | ❌ 无 | ✅ 细蓝线 + 章节号 + 标题 |
| 文件大小 | 15-30KB | 60-150KB（含 banner 图）|
| 适用 | Obsidian 笔记 / 自己看 | 给领导/投资人 / 打印分享 |

**麦肯锡风样式系统**：详见 `references/mckinsey-style-guide.md`（v5.1 沉淀：2 色配色 + 表格样式 + 章节封面模板 + banner 图渲染）。

**重要说明**：
- Word 输出**不影响**默认 Markdown 流程——只是额外生成
- Markdown 报告仍按 v1.2.0 流程走（数据来源声明 + 9 LAWs 自检 + Obsidian 备份）
- Word 输出要遵守 **LAW 10 视觉样式约束**（emoj / callout 块 / 表格紧贴的 pitfall）

## 进度反馈

多步任务（>3 步）应在每完成一个关键节点时主动给用户简短反馈：

```
📡 Deep Research 启动
   主题: <topic>
   场景: <type>
   时间窗口: <window>
   预计 3-5 分钟

🔍 Step 3: 抓取信源
   ✅ L1: Anthropic 博客 (3 篇), OpenAI 博客 (2 篇)
   ✅ L2: arXiv (5 篇), OpenAlex (2 篇)
   ⚠️ L3: 36氪仅 1 篇相关内容（数据稀疏）
   ⏭️ L4: 无相关内容
   ✅ L5: X 5 条, Reddit 3 条

🧩 Step 4-5: 聚类合并 + 渲染
   报告章节数: 5/5（符合模版）

✅ Step 6: 4 条 LAWs 自检全部通过

📁 Step 7: 交付
   ✅ 对话显示
   ✅ Obsidian: ~/Documents/Obsidian Vault/深度调研/<topic>-<YYYY-MM-DD>.md
   ⏭️ 飞书 wiki: 未启用（无 --feishu 标志）
```

## 与已有 skills 的协同交付

- **ai-daily-report**：日报自动 cron 推送飞书 PDF；深度调研手动输出 Markdown → Obsidian。两者互补
- **kol-interview-to-wiki**：KOL 访谈是 deep-research 的可选信源（L4），KOL 的观点可被 industry-market/tech-trend 引用
- **blogwatcher**：持续追踪某个主题的 RSS 更新，是 deep-research 的"长期监控"补充（手动 deep-research 是"一次性深挖"）
