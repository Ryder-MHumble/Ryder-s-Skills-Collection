#!/usr/bin/env python3
"""
COVER 字典模板 — v5.2 信息密集型单页首页

用 5 场景各 1 套示例值。复用方式：
1. 复制本文件到目标报告目录
2. 改 COVER 字典字段（title / judgments / metrics / metas）
3. 在 build_report() 中调用 `add_dense_cover(doc, COVER)`

详细设计原则 + 字段规范 + 字号/颜色/间距：见 references/cover-page-design.md
"""

# ============================================================
# 模板 1: industrial-tob（工业 To B）— 外骨骼劳工保护
# ============================================================
COVER_INDUSTRIAL_TOB = {
    'brand_top':   'RYDER AI SIGNAL  ·  深度调研报告  ·  v5.2',
    'title':       '国内外劳工  外骨骼市场',
    'title_line2': '玩家格局 · 商业模式 · 切入机会',
    'subtitle_en': 'Global Industrial Exoskeleton for Labor Protection (2024-2026)',
    'judgments':   [
        ('① 劳工刚需',   '工伤/缺员/法规三重压力下加速渗透'),
        ('② 头部 4 国',   '美/英/法/德占全球 ~80% 工业外骨骼市场'),
        ('③ 上肢主导',   '上肢辅助占 ~60%（肩/腰），下肢占 ~30%'),
        ('④ 切入机会',   '渠道 + 工种绑定 + 区域代理'),
        ('⑤ 商业模式',   'B2B 销售 + RaaS 订阅并行'),
    ],
    'metrics':     [
        ('$5.6B',  '全球工业外骨骼 2026 估值'),
        ('21.8%',  '北美 CAGR 2018-2026'),
        ('30',     'evidence_id 数量（L1-L5 分层）'),
        ('24+',    '玩家分布（已验证）'),
    ],
    'metas':       [
        ('研究时间窗', '2024-01-01 ~ 2026-06-10 (30 月)'),
        ('场景类型',   'industrial-tob (工业 To B)'),
        ('地理范围',   '美国 · 英国 · 法国 · 德国'),
        ('品类范围',   '工业外骨骼 (劳工保护)'),
        ('报告版本',   'v5.2  ·  2026-06-10'),
        ('出品方',     'Ryder AI Signal  ·  深度调研'),
    ],
    'footer':      '本报告共 9 章正文 + 4 附录  ·  30 evidence_id  ·  麦肯锡风 v5.2  ·  决策导向  /  Decision-Oriented',
}


# ============================================================
# 模板 2: tech-trend（技术趋势）— AI 产品演变
# ============================================================
COVER_TECH_TREND = {
    'brand_top':   'RYDER AI SIGNAL  ·  深度调研报告  ·  v5.2',
    'title':       'AI 产品演变  Deep Research 报告',
    'title_line2': '玩家格局  ·  技术路线  ·  商业化加速',
    'subtitle_en': 'Global AI Product Evolution: Players, Roadmaps, and Commercial Acceleration (2024-2026)',
    'judgments':   [
        ('① 范式跃迁',     '对话 → reasoning → agentic'),
        ('② 头部 3 家',     'OpenAI / Anthropic / Google'),
        ('③ DeepSeek 震惊', 'R1 $6M 训出 → NVDA -$600B'),
        ('④ Computer Use',  '端到端 GUI Agent 开启'),
        ('⑤ OpenAI IPO',    '2026-06-08 提交 S-1'),
    ],
    'metrics':     [
        ('$200B+',  '全球 AI 工具 TAM 2026 H1 估算'),
        ('70-90%',  '头部推理模型 CAGR 区间'),
        ('23',      '关键产品节点（24 月内）'),
        ('30',      'evidence_id 数量（L1-L5 分层）'),
    ],
    'metas':       [
        ('研究时间窗', '2024-07-01 ~ 2026-06-11 (24 月)'),
        ('场景类型',   'tech-trend (技术趋势)'),
        ('地域范围',   '全球 (中美欧 / 5 国)'),
        ('品类范围',   'AI 产品 (5 大类)'),
        ('报告版本',   'v5.2  ·  2026-06-11'),
        ('出品方',     'Ryder AI Signal  ·  深度调研'),
    ],
    'footer':      '本报告共 9 章正文 + 4 附录  ·  30 evidence_id  ·  麦肯锡风 v5.2  ·  决策导向  /  Decision-Oriented',
}


# ============================================================
# 模板 3: product-deep（单产品深度）— Anthropic Computer Use
# ============================================================
COVER_PRODUCT_DEEP = {
    'brand_top':   'RYDER AI SIGNAL  ·  深度调研报告  ·  v5.2',
    'title':       'Anthropic Computer Use',
    'title_line2': '产品深度调研 · 能力边界 · 商业化路径',
    'subtitle_en': 'Anthropic Computer Use: Capability, Limits, and Go-to-Market (2024-2026)',
    'judgments':   [
        ('① 范式',       '端到端 GUI Agent 2024-10 开端'),
        ('② 能力边界',   'OSWorld 14.9% → Claude 4.x 提升至 ~40%'),
        ('③ 竞品差距',   'OpenAI Operator 同期 ~38%, Google Astra 25%'),
        ('④ 商业模式',   '按 token 计费 + Claude Code IDE 集成'),
        ('⑤ 企业渗透',   'Box / Asana / Canva 已 PoC'),
    ],
    'metrics':     [
        ('$3 / MTok',  'Computer Use API 价格'),
        ('40%',        'OSWorld 最新得分 (Claude 4.5)'),
        ('12',         '对比的同类产品数量'),
        ('30',         'evidence_id 数量（L1-L5 分层）'),
    ],
    'metas':       [
        ('研究时间窗', '2024-10-22 ~ 2026-06-11 (20 月)'),
        ('场景类型',   'product-deep (单产品深度)'),
        ('地域范围',   '全球 (主要美国)'),
        ('品类范围',   'Computer Use / GUI Agent'),
        ('报告版本',   'v5.2  ·  2026-06-11'),
        ('出品方',     'Ryder AI Signal  ·  深度调研'),
    ],
    'footer':      '本报告共 9 章正文 + 4 附录  ·  30 evidence_id  ·  麦肯锡风 v5.2  ·  决策导向  /  Decision-Oriented',
}


# ============================================================
# 模板 4: competitor（竞品对比）— Cursor vs Copilot vs Windsurf
# ============================================================
COVER_COMPETITOR = {
    'brand_top':   'RYDER AI SIGNAL  ·  深度调研报告  ·  v5.2',
    'title':       'AI 编码助手  三家对比',
    'title_line2': 'Cursor · GitHub Copilot · Windsurf',
    'subtitle_en': 'AI Coding Assistant: Cursor vs GitHub Copilot vs Windsurf (2024-2026)',
    'judgments':   [
        ('① Cursor 领先',   'Composer 1.0 2025-07 + ARR $500M+'),
        ('② Copilot 稳固',   '企业市场 130 万付费席位, GitHub 生态'),
        ('③ Windsurf 失速', 'Codeium 整合后流失率上升'),
        ('④ 选型',         '独立开发者 → Cursor, 企业 → Copilot'),
        ('⑤ 价格带',       '$10-60/月, RaaS 模型趋同'),
    ],
    'metrics':     [
        ('$500M+',  'Cursor 2026 ARR 估算'),
        ('1.3M',    'Copilot 企业付费席位'),
        ('3',       '核心对比产品'),
        ('30',      'evidence_id 数量（L1-L5 分层）'),
    ],
    'metas':       [
        ('研究时间窗', '2024-01-01 ~ 2026-06-11 (30 月)'),
        ('场景类型',   'competitor (竞品对比)'),
        ('地域范围',   '全球 (主要北美 / 欧洲)'),
        ('品类范围',   'AI 编码助手 / IDE 插件'),
        ('报告版本',   'v5.2  ·  2026-06-11'),
        ('出品方',     'Ryder AI Signal  ·  深度调研'),
    ],
    'footer':      '本报告共 9 章正文 + 4 附录  ·  30 evidence_id  ·  麦肯锡风 v5.2  ·  决策导向  /  Decision-Oriented',
}


# ============================================================
# 模板 5: industry-market（行业市场）— 全球人形机器人
# ============================================================
COVER_INDUSTRY_MARKET = {
    'brand_top':   'RYDER AI SIGNAL  ·  深度调研报告  ·  v5.2',
    'title':       '全球人形机器人  行业格局',
    'title_line2': '玩家地图 · 资本热度 · 商业化时间表',
    'subtitle_en': 'Global Humanoid Robot Industry: Players, Capital Flows, and Commercialization Timeline (2024-2026)',
    'judgments':   [
        ('① 玩家集中',   'Figure / Tesla / 1X / 宇树 / 智元 头部 5 家'),
        ('② 资本热',     '2025 年人形机器人融资 $4.2B (同比 +180%)'),
        ('③ 量产时间',   'Figure 02 2026 Q1 → Tesla Optimus V3 2026 Q3'),
        ('④ 切入场景',   '工厂搬运 / 汽车装配 / 仓储物流'),
        ('⑤ 中美差距',   '硬件追平, 软件生态落后 12-18 月'),
    ],
    'metrics':     [
        ('$4.2B',  '2025 全球人形机器人融资'),
        ('+180%',  '同比融资增速'),
        ('20+',    '已商业化玩家数'),
        ('30',     'evidence_id 数量（L1-L5 分层）'),
    ],
    'metas':       [
        ('研究时间窗', '2024-01-01 ~ 2026-06-11 (30 月)'),
        ('场景类型',   'industry-market (行业市场)'),
        ('地域范围',   '全球 (中美欧日韩)'),
        ('品类范围',   '人形机器人 / 双足机器人'),
        ('报告版本',   'v5.2  ·  2026-06-11'),
        ('出品方',     'Ryder AI Signal  ·  深度调研'),
    ],
    'footer':      '本报告共 9 章正文 + 4 附录  ·  30 evidence_id  ·  麦肯锡风 v5.2  ·  决策导向  /  Decision-Oriented',
}


# ============================================================
# 在 build_report() 中调用示例：
# ============================================================
# from templates.cover_params_template import COVER_INDUSTRIAL_TOB as COVER
# from scripts.word_output import add_dense_cover
#
# def build_report():
#     doc = Document()
#     # ... 字体 / 边距设置 ...
#     add_dense_cover(doc, COVER)
#     doc.add_page_break()
#     # ... 目录 / 9 章正文 / 4 附录 ...
#
# ============================================================
# 字段填写提示（详见 references/cover-page-design.md § 5/6）：
# ============================================================
# judgments（5 条核心判断）：
#   ① 范式 / 拐点  ② 头部 / 集中度  ③ 意外 / 反共识
#   ④ 机会 / 切入  ⑤ 模式 / 趋势
#   标签 4-8 字, 描述 20-30 字, 含具体数字/玩家/时间
#
# metrics（4 个关键数据）：
#   ① TAM / 市场规模  ② CAGR / 增速
#   ③ 节点 / 事件数  ④ 机会 / 痛点数字
#   big 用数字, desc 12-25 字说明
#
# metas（6 项元信息）：
#   研究时间窗 / 场景类型 / 地域范围 /
#   品类范围 / 报告版本 / 出品方
# ============================================================
