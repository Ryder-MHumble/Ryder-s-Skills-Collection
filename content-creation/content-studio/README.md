# Content Studio v4.6

> **2 平台爆款内容生产 + 视觉卡片生成**。
> 从「写一条帖子」升级到「建一个 IP」。

## 核心范式（v4.6）

**封面支持两种模式**，**用户只选这两种**：

| 模式 | 默认 | 元素数 | 适合场景 |
|------|------|--------|---------|
| **simple** | ✅ | 5 元素 | 日常推文、KOL 库更新 |
| **complex** |  | 12+ 元素（brutalist 杂志风） | 重要发布、爆款冲量 |

内页 = 1 套信纸留白模板（用户 P 图用）。

## 快速开始

```bash
# 简易模式封面（默认）
python scripts/card_generator.py \
  --type cover --mode simple \
  --hook "高段位 AI\n决策者都应该有\nKOL 情报库" \
  --sub "2 小时访谈 → 5 分钟笔记" \
  -o cover.png

# 复杂 brutalist 模式封面
python scripts/card_generator.py \
  --type cover --mode complex \
  --hook "高段位 AI\n决策者都应该有\nKOL 情报库" \
  --sub "2 小时访谈 → 5 分钟笔记" \
  -o cover.png

# 内页（信纸版）
python scripts/card_generator.py --type inside --page 2 --total 5 -o inside.png
```

## 文件结构

```
content-studio/
├── SKILL.md                          # 详细规范
├── README.md                         # 本文件
├── scripts/
│   └── card_generator.py             # 卡片生成器
├── references/                       # 参考文档
│   ├── implementation-notes.md       # CJK 字体实现
│   ├── visual/avatar-driven-design.md
│   ├── platforms/{x,xiaohongshu}.md
│   └── frameworks/{personal-ip,psychological-hooks}.md
├── templates/                        # 文案模板
│   └── {x_thread,xiaohongshu_post}.md
└── assets/
    ├── avatar.png                    # 主头像（黑皮夹克）
    └── fonts/README.md
```

## 平台支持

- **X**（Twitter）：独狼帖 + Thread
- **小红书**：标题 + 正文 + 标签

## 输出位置

默认：`~/Downloads/social-platform-references/`

详见 `SKILL.md`。
