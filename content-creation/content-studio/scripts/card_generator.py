"""
content-studio 卡片生成器 v4.6

两种封面模式：
- simple（默认）：极简版，主标题+副标题+头像+ID 标签
- complex：brutalist 风格，参考 xhs-brutalist-cards

内页：信纸版（用户 P 图用）

用法：
  # 封面（默认 simple）
  python card_generator.py --type cover --hook "高段位 AI\n决策者都应该有\nKOL 情报库" --sub "2 小时访谈 → 5 分钟笔记" -o cover.png

  # 封面（复杂 brutalist 模式）
  python card_generator.py --type cover --mode complex --hook "..." --sub "..." -o cover.png

  # 内页
  python card_generator.py --type inside -o inside.png
"""
import os
import sys
import argparse
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ============== 路径 ==============
SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
AVATAR_PATH = SKILL_DIR / "assets" / "avatar.png"

# ============== 宽高比 ==============
ASPECT_RATIOS = {
    "1:1": (1600, 1600),
    "3:4": (1200, 1600),
    "4:3": (1600, 1200),
    "9:16": (1080, 1920),
    "16:9": (1600, 900),
    "2:3": (1200, 1800),
}

# ============== 字体加载 ==============
def load_font(role, size):
    """按角色加载字体"""
    chains = {
        "display": [
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/System/Library/Fonts/ArialHB.ttc",
            "/System/Library/Fonts/Helvetica.ttc",
        ],
        "ui": [
            "/System/Library/Fonts/ArialHB.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
        ],
    }
    for path in chains.get(role, chains["display"]):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
            except Exception:
                continue
    return ImageFont.load_default()

def has_cjk(text):
    """是否包含 CJK 字符"""
    return any(
        0x4E00 <= ord(c) <= 0x9FFF
        or 0x3000 <= ord(c) <= 0x303F
        or 0xFF00 <= ord(c) <= 0xFFEF
        for c in text
    )

def select_font(role, text, size):
    """智能字体选择（CJK 用 display，否则按 role）"""
    if has_cjk(text):
        return load_font("display", size)
    return load_font(role, size)

def _normalize_newlines(s):
    """把字面 '\\n' 变成真换行（CLI 传 hook 时 bash 不会自动转义）"""
    return s.replace("\\n", "\n") if s else s

def true_text_width(text, font_size):
    """
    手算文字宽度（CJK=字号, Latin=字号*0.6, 空格=字号*0.4）
    + 8% buffer 防 getlength 估短
    """
    w = 0
    for c in text:
        if 0x4E00 <= ord(c) <= 0x9FFF or 0x3000 <= ord(c) <= 0x303F:
            w += font_size
        elif 0xFF00 <= ord(c) <= 0xFFEF:
            w += font_size
        elif c == " ":
            w += font_size * 0.4
        else:
            w += font_size * 0.6
    return int(w * 1.08)

def text_size(draw, text, font, size):
    """取手算 + font.getlength 较大值，高度用 textbbox"""
    tw = true_text_width(text, size)
    try:
        fl = int(font.getlength(text))
    except Exception:
        fl = 0
    w = max(tw, fl)
    try:
        b = draw.textbbox((0, 0), text, font=font)
        h = b[3] - b[1]
    except Exception:
        _, h = draw.textsize(text, font=font)
    return w, h

# ============== 通用工具 ==============
def make_circular_avatar(avatar_path, size, border_color="#0A0A0A", border_width=8):
    """加载头像并裁成圆形"""
    img = Image.open(avatar_path).convert("RGBA")
    img.thumbnail((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([(0, 0), (size, size)], fill=255)
    avatar = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    offset = ((size - img.width) // 2, (size - img.height) // 2)
    avatar.paste(img, offset, img.split()[3] if img.mode == "RGBA" else None)
    avatar.putalpha(mask)
    return avatar

def make_grid_overlay(w, h, color="#E8E4D5", spacing=50, line_width=1):
    """米黄网格背景（简易模式用）"""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    for x in range(0, w, spacing):
        draw.line([(x, 0), (x, h)], fill=color, width=line_width)
    for y in range(0, h, spacing):
        draw.line([(0, y), (w, y)], fill=color, width=line_width)
    return img

def make_paper_overlay(w, h):
    """米黄信纸背景（横线 + 噪点，复杂模式用）"""
    random.seed(42)
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    # 横线
    for y in range(0, h, 22):
        draw.line([(0, y), (w, y)], fill="#08080830", width=1)
    # 噪点
    for _ in range(w * h // 300):
        x = random.randint(0, w - 1)
        y = random.randint(0, h - 1)
        draw.ellipse([(x, y), (x + 2, y + 2)], fill="#08080850")
    return overlay

def save_img(img, out_path):
    """保存图片到指定路径"""
    out = Path(out_path).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", quality=95, optimize=True)
    return str(out)


# ============================================================
# 模式 1: 简易模式（simple）
# ============================================================
def render_cover_simple(w, h, hook, sub_hook, avatar_path):
    """
    简易模式封面：极简风

    元素（按 z-order）：
      1. 米黄底 + 淡网格
      2. 顶部 ID 标签（白底黑字 + 黑边）
      3. 主标题 3 行（KOL 红色高亮 + 红线 underline）
      4. 副标题（红底白字 + 黑投影 + 黑边）
      5. 头像大圆（带黑色硬投影）
    """
    BG = "#F5F0E1"
    FG = "#0A0A0A"
    WHITE = "#FFFFFF"
    ORANGE = "#E63946"

    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    grid = make_grid_overlay(w, h, color="#E8E4D5", spacing=50, line_width=1)
    img.paste(grid, (0, 0), grid)

    # 1) 顶部 ID 标签
    rider_text = "叫我 Ryder 就好"
    rider_size = int(h * 0.025)
    rider_font = select_font("rider", rider_text, rider_size)
    rw, rh = text_size(draw, rider_text, rider_font, rider_size)
    draw.rectangle(
        [(60, 80), (60 + rw + 44, 80 + rh + 28)],
        fill=WHITE, outline=FG, width=2,
    )
    draw.text((82, 80 + 12), rider_text, font=rider_font, fill=FG)

    # 2) 主标题 3 行
    hook_y = int(h * 0.16)
    hook_size = int(h * 0.075)
    hook_font = select_font("hook", hook, hook_size)
    lines = hook.split("\n")
    line_h = int(hook_size * 1.10)
    for i, line in enumerate(lines):
        y = hook_y + i * line_h
        if "KOL" in line:
            # 整行黑色 + "KOL" 红色 + 红线 underline
            draw.text((60, y), line, font=hook_font, fill=FG)
            kol_start = line.find("KOL")
            pre_w, _ = text_size(draw, line[:kol_start], hook_font, hook_size)
            draw.text((60 + pre_w, y), "KOL", font=hook_font, fill=ORANGE)
            kol_w, _ = text_size(draw, "KOL", hook_font, hook_size)
            draw.rectangle(
                [(60 + pre_w, y + hook_size - 8), (60 + pre_w + kol_w, y + hook_size + 4)],
                fill=ORANGE,
            )
        else:
            draw.text((60, y), line, font=hook_font, fill=FG)

    # 3) 红线
    div_y = hook_y + len(lines) * line_h + 30
    draw.rectangle([(60, div_y), (200, div_y + 6)], fill=ORANGE)

    # 4) 副标题（红底白字）
    if sub_hook:
        sub_size = int(h * 0.030)
        sub_font = select_font("sub", sub_hook, sub_size)
        sw, sh = text_size(draw, sub_hook, sub_font, sub_size)
        sub_w, sub_h = sw + 72, sh + 36
        sub_x, sub_y = 60, div_y + 50
        # 黑投影
        draw.rectangle(
            [(sub_x + 8, sub_y + 8), (sub_x + sub_w + 8, sub_y + sub_h + 8)],
            fill=FG,
        )
        # 红底
        draw.rectangle(
            [(sub_x, sub_y), (sub_x + sub_w, sub_y + sub_h)],
            fill=ORANGE, outline=FG, width=4,
        )
        draw.text((sub_x + 36, sub_y + 18), sub_hook, font=sub_font, fill=WHITE)

    # 5) 头像（双层黑色硬投影）
    avatar_size = int(w * 0.32)
    av_x = (w - avatar_size) // 2
    av_y = int(h * 0.55)
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse(
        [(av_x + 18, av_y + 18), (av_x + avatar_size + 18, av_y + avatar_size + 18)],
        fill=(0, 0, 0, 255),
    )
    sd.ellipse(
        [(av_x + 10, av_y + 10), (av_x + avatar_size + 10, av_y + avatar_size + 10)],
        fill=(0, 0, 0, 255),
    )
    img.paste(shadow, (0, 0), shadow)
    if os.path.exists(avatar_path):
        circular = make_circular_avatar(avatar_path, avatar_size, border_color=FG, border_width=10)
        img.paste(circular, (av_x, av_y), circular)

    return img


# ============================================================
# 模式 2: 复杂模式（complex，brutalist 风格）
# ============================================================
# 复杂模式配色
COMPLEX_COLORS = {
    "paper": "#F1E2CC",     # 米黄信纸
    "soft": "#FFF9ED",      # 米白卡片
    "ink": "#080808",       # 黑色
    "red": "#F0442E",       # 橙红
    "yellow": "#FFD72E",    # 黄
    "muted": "#6D6255",
}

def render_cover_complex(w, h, hook, sub_hook, avatar_path):
    """
    复杂模式封面：brutalist 杂志风

    元素（按 z-order，对齐 HTML v2 设计）：
      1. 米黄信纸背景（横线 + 噪点）
      2. 16px 厚黑边框
      3. 顶部 ID 卡片（白底+黑边+红投影+头像+文字）
      4. KOL INTEL/04 黑色角标（右上）
      5. meta-rail 横线 + 4 tick 标记
      6. 3 行主标题（米白/黑/红，box 带硬投影）
      7. 副标题（米白+红边+红投影）
      8. 红色 01 stamp（左下）
      9. RYDER 支持卡（右下）+ 条形码 + AI PM chip + KOL 情报库 + HIGH-STAKES DECISIONS
     10. footer "REDESIGNED BRUTAL CARD SYSTEM / TEXT NEVER OVERLAPS / 1240x1654"

    （已移除纯装饰元素：右下黑色斜切角、顶部红方块、黑红条纹、4 个 + 标记）
    """
    C = COMPLEX_COLORS
    img = Image.new("RGB", (w, h), C["paper"])
    draw = ImageDraw.Draw(img)

    # 1) 信纸背景
    paper = make_paper_overlay(w, h)
    img.paste(paper, (0, 0), paper)

    # 2) 16px 厚黑边框
    bw = 16
    draw.rectangle([(0, 0), (w, h)], outline=C["ink"], width=bw)

    # 3) 顶部 ID 卡片
    id_x, id_y, id_w, id_h = 46, 46, 690, 104
    draw.rectangle(
        [(id_x + 10, id_y + 10), (id_x + id_w + 10, id_y + id_h + 10)],
        fill=C["red"],
    )
    draw.rectangle(
        [(id_x, id_y), (id_x + id_w, id_y + id_h)],
        fill=C["soft"], outline=C["ink"], width=6,
    )
    av_size = 76
    av_x, av_y = id_x + 10, id_y + (id_h - av_size) // 2
    draw.rectangle(
        [(av_x + 8, av_y + 8), (av_x + av_size + 8, av_y + av_size + 8)],
        fill=C["ink"],
    )
    if os.path.exists(avatar_path):
        circular = make_circular_avatar(avatar_path, av_size, border_color=C["ink"], border_width=6)
        img.paste(circular, (av_x, av_y), circular)
    id_text = "叫我 Ryder 就好"
    id_font = select_font("id", id_text, 42)
    draw.text((av_x + av_size + 26, id_y + (id_h - 42) // 2 - 4), id_text, font=id_font, fill=C["ink"])

    # 4) KOL INTEL/04 黑色角标
    badge_text = "KOL INTEL / 04"
    badge_font = select_font("badge", badge_text, 35)
    bbw, bbh = text_size(draw, badge_text, badge_font, 35)
    bx, by = w - 54 - bbw - 56, 34
    draw.rectangle([(bx, by), (bx + bbw + 56, by + 72)], fill=C["ink"])
    draw.text((bx + 28, by + 18), badge_text, font=badge_font, fill=C["soft"])

    # 5) meta-rail
    rail_y = 202
    draw.line([(46, rail_y), (w - 46, rail_y)], fill=C["ink"], width=6)
    for i in range(4):
        x = 46 + i * 260
        draw.line([(x, rail_y - 29), (x, rail_y + 19)], fill=C["ink"], width=5)
    meta_font = select_font("meta", "DECISION SIGNALS", 25)
    draw.text((46, rail_y + 18), "DECISION SIGNALS", font=meta_font, fill=C["ink"])
    m2 = "NO.01 / COVER SYSTEM"
    m2w, _ = text_size(draw, m2, meta_font, 25)
    draw.text((w - 46 - m2w, rail_y + 18), m2, font=meta_font, fill=C["ink"])

    # 6) 3 行主标题
    lines = hook.split("\n")
    if len(lines) < 3:
        lines = lines + ["KOL 情报库"] * (3 - len(lines))
    lines = lines[:3]

    title_size = 92
    title_h = 162
    title_font = select_font("title", "高段位 AI", title_size)

    # title-1 (米白+红投影)
    ty1 = 302
    line1 = lines[0]
    l1w, l1h = text_size(draw, line1, title_font, title_size)
    l1x = (w - l1w) // 2
    draw.rectangle([(l1x + 14, ty1 + 14), (l1x + l1w + 14, ty1 + title_h + 14)], fill=C["red"])
    draw.rectangle([(l1x, ty1), (l1x + l1w, ty1 + title_h)], fill=C["soft"], outline=C["ink"], width=8)
    draw.text((l1x + 28, ty1 + (title_h - l1h) // 2 - 4), line1, font=title_font, fill=C["ink"])

    # title-2 (黑底白字+红投影)
    ty2 = ty1 + title_h + 32
    line2 = lines[1]
    l2w, l2h = text_size(draw, line2, title_font, title_size)
    l2x = (w - l2w) // 2
    draw.rectangle([(l2x + 14, ty2 + 14), (l2x + l2w + 14, ty2 + title_h + 14)], fill=C["red"])
    draw.rectangle([(l2x, ty2), (l2x + l2w, ty2 + title_h)], fill=C["ink"], outline=C["ink"], width=8)
    draw.text((l2x + 28, ty2 + (title_h - l2h) // 2 - 4), line2, font=title_font, fill=C["soft"])

    # title-3 (红底黑字+黄投影,大字)
    ty3 = ty2 + title_h + 32
    title3_h = 186
    title3_size = 112
    title3_font = select_font("title", "KOL 情报库", title3_size)
    line3 = lines[2]
    l3w, l3h = text_size(draw, line3, title3_font, title3_size)
    l3x = (w - l3w) // 2
    draw.rectangle([(l3x + 14, ty3 + 14), (l3x + l3w + 14, ty3 + title3_h + 14)], fill=C["yellow"])
    draw.rectangle([(l3x, ty3), (l3x + l3w, ty3 + title3_h)], fill=C["red"], outline=C["ink"], width=8)
    draw.text((l3x + 28, ty3 + (title3_h - l3h) // 2 - 6), line3, font=title3_font, fill=C["ink"])

    # 7) 副标题
    if sub_hook:
        sub_size = 45
        sub_font = select_font("sub", sub_hook, sub_size)
        sw, sh = text_size(draw, sub_hook, sub_font, sub_size)
        sub_w, sub_h = sw + 70, 112
        sub_x = (w - sub_w) // 2
        sub_y = ty3 + title3_h + 56
        draw.rectangle(
            [(sub_x + 12, sub_y + 12), (sub_x + sub_w + 12, sub_y + sub_h + 12)],
            fill=C["red"],
        )
        draw.rectangle(
            [(sub_x, sub_y), (sub_x + sub_w, sub_y + sub_h)],
            fill=C["soft"], outline=C["ink"], width=7,
        )
        draw.text((sub_x + 35, sub_y + (sub_h - sh) // 2 - 2), sub_hook, font=sub_font, fill=C["ink"])

    # 8) 红色 01 stamp
    stamp_x = 46
    stamp_y = 1140
    stamp_w = 350
    stamp_h = 220
    draw.rectangle(
        [(stamp_x + 12, stamp_y + 12), (stamp_x + stamp_w + 12, stamp_y + stamp_h + 12)],
        fill=C["ink"],
    )
    draw.rectangle(
        [(stamp_x, stamp_y), (stamp_x + stamp_w, stamp_y + stamp_h)],
        fill=C["red"], outline=C["ink"], width=7,
    )
    num_font = select_font("num", "01", 130)
    draw.text((stamp_x + 30, stamp_y + 18), "01", font=num_font, fill=C["soft"])
    draw.line(
        [(stamp_x + 180, stamp_y + 36), (stamp_x + 180, stamp_y + stamp_h - 36)],
        fill=C["ink"], width=6,
    )
    for i, m in enumerate(["COVER", "5 MIN", "XHS"]):
        m_font = select_font("meta", m, 34)
        draw.text((stamp_x + 200, stamp_y + 36 + i * 52), m, font=m_font, fill=C["soft"])

    # 9) RYDER 支持卡
    sup_x = w - 54 - 626
    sup_y = stamp_y
    sup_w = 626
    sup_h = 266
    draw.rectangle(
        [(sup_x + 14, sup_y + 14), (sup_x + sup_w + 14, sup_y + sup_h + 14)],
        fill=C["red"],
    )
    draw.rectangle(
        [(sup_x, sup_y), (sup_x + sup_w, sup_y + sup_h)],
        fill=C["soft"], outline=C["ink"], width=7,
    )
    ryder_font = select_font("ryder", "RYDER", 48)
    draw.text((sup_x + 34, sup_y + 26), "RYDER", font=ryder_font, fill=C["ink"])
    # 条形码
    bcx = sup_x + sup_w - 26 - 140
    bcy = sup_y + 26
    for i in range(20):
        bx = bcx + i * 7
        if i % 3 == 0:
            draw.rectangle([(bx, bcy), (bx + 5, bcy + 94)], fill=C["ink"])
        elif i % 2 == 0:
            draw.rectangle([(bx, bcy), (bx + 3, bcy + 94)], fill=C["ink"])
        else:
            draw.rectangle([(bx, bcy), (bx + 2, bcy + 94)], fill=C["ink"])
    chip_text = "AI PM / INTEL NOTES"
    chip_font = select_font("chip", chip_text, 25)
    cw, ch = text_size(draw, chip_text, chip_font, 25)
    draw.rectangle(
        [(sup_x + 34, sup_y + 96), (sup_x + 34 + cw + 40, sup_y + 96 + 48)],
        fill=C["ink"],
    )
    draw.text((sup_x + 34 + 20, sup_y + 96 + 12), chip_text, font=chip_font, fill=C["soft"])
    kol_font = select_font("kol2", "KOL 情报库", 32)
    draw.text((sup_x + 34, sup_y + 156), "KOL 情报库", font=kol_font, fill=C["ink"])
    hsd_font = select_font("hsd", "HIGH-STAKES DECISIONS", 18)
    draw.text((sup_x + 34, sup_y + 200), "HIGH-STAKES DECISIONS", font=hsd_font, fill=C["red"])

    # 10) footer
    footer_y = h - 60
    footer_text = "REDESIGNED BRUTAL CARD SYSTEM / TEXT NEVER OVERLAPS / 1240x1654"
    footer_font = select_font("footer", footer_text, 25)
    draw.text((46, footer_y), footer_text, font=footer_font, fill=C["ink"])

    return img


# ============================================================
# 内页：信纸版（用户 P 图用）
# ============================================================
def render_inside(w, h, avatar_path, page_num=1, total_pages=5):
    """
    内页信纸版：

    元素：
      1. 米黄底 + 网格
      2. 左侧 4 个装订孔（白边红圆）
      3. 顶部 header（黑横条 + 红线）+ ID 标签 + KOL 情报库 | 02/05
      4. 主体 100% 留白（用户 P 图）
      5. 底部 footer（黄线 + Ryder's KOL Intelligence + 期号）
    """
    BG = "#F5F0E1"
    FG = "#0A0A0A"
    WHITE = "#FFFFFF"
    ORANGE = "#E63946"
    YELLOW = "#FFD72A"

    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)
    grid = make_grid_overlay(w, h, color="#D4CCB8", spacing=50, line_width=1)
    img.paste(grid, (0, 0), grid)

    # 装订孔
    for i in range(4):
        cy = int(h * (i + 1) / 5)
        draw.ellipse([(40 - 12, cy - 12), (40 + 12, cy + 12)], fill=WHITE, outline=FG, width=2)
        draw.ellipse([(40 - 7, cy - 7), (40 + 7, cy + 7)], fill=ORANGE)

    # 顶部 header
    header_h = int(h * 0.06)
    draw.rectangle([(0, 0), (w, header_h)], fill=FG)
    draw.rectangle([(0, header_h), (w, header_h + 6)], fill=ORANGE)

    # ID 标签
    rider_text = "叫我 Ryder 就好"
    rider_size = int(header_h * 0.34)
    rider_font = select_font("rider", rider_text, rider_size)
    rw, rh = text_size(draw, rider_text, rider_font, rider_size)
    ry = (header_h - rh - 28) // 2
    draw.rectangle(
        [(30, ry), (30 + rw + 44, ry + rh + 28)],
        fill=WHITE, outline=FG, width=2,
    )
    draw.text((30 + 22, ry + 12), rider_text, font=rider_font, fill=FG)

    # 页码（右侧）
    page_text = f"{page_num:02d} / {total_pages:02d}"
    page_size = int(header_h * 0.34)
    page_font = select_font("page", page_text, page_size)
    pw, ph = text_size(draw, page_text, page_font, page_size)
    page_x = w - pw - 30
    draw.text((page_x, (header_h - ph) // 2), page_text, font=page_font, fill=YELLOW)

    # 底部 footer
    footer_h = int(h * 0.05)
    footer_y = h - footer_h
    draw.rectangle([(0, footer_y), (w, footer_y + 6)], fill=YELLOW)

    bot_text = "Ryder's KOL Intelligence"
    bot_size = int(footer_h * 0.50)
    bot_font = select_font("bot", bot_text, bot_size)
    bw, bh = text_size(draw, bot_text, bot_font, bot_size)
    draw.text(((w - bw) // 2, footer_y + 14), bot_text, font=bot_font, fill=FG)

    issue_text = "ISSUE 013 · 2025"
    issue_size = int(footer_h * 0.35)
    issue_font = select_font("issue", issue_text, issue_size)
    iw, ih = text_size(draw, issue_text, issue_font, issue_size)
    draw.text(
        (w - iw - 30, footer_y + (footer_h - ih) // 2 + 2),
        issue_text, font=issue_font, fill=FG,
    )

    return img


# ============================================================
# CLI
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="content-studio 卡片生成器 v4.6 — 两种封面模式（simple/complex）+ 内页信纸版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
示例：
  # 简易模式封面（默认）
  python card_generator.py --type cover --hook "高段位 AI\n决策者都应该有\nKOL 情报库" --sub "2 小时访谈 → 5 分钟笔记" -o cover.png

  # 复杂 brutalist 模式封面
  python card_generator.py --type cover --mode complex --hook "..." --sub "..." -o cover.png

  # 内页信纸版
  python card_generator.py --type inside -o inside.png
        """,
    )
    parser.add_argument(
        "--type", default="cover",
        choices=["cover", "inside"],
        help="卡片类型（cover=封面 / inside=内页）",
    )
    parser.add_argument(
        "--mode", default="simple",
        choices=["simple", "complex"],
        help="封面模式（simple=极简 / complex=brutalist 复杂）",
    )
    parser.add_argument("--hook", help="主钩子句（封面用，\\n 分多行）")
    parser.add_argument("--sub", default="", help="副钩子（封面用）")
    parser.add_argument("--avatar", help=f"头像路径（默认 {AVATAR_PATH}）")
    parser.add_argument(
        "--aspect", default="3:4",
        choices=list(ASPECT_RATIOS.keys()),
        help="宽高比",
    )
    parser.add_argument(
        "--page", type=int, default=2,
        help="内页页码（默认 2）",
    )
    parser.add_argument(
        "--total", type=int, default=5,
        help="内页总数（默认 5）",
    )
    parser.add_argument(
        "--output", "-o", required=True,
        help="输出 PNG 路径",
    )

    args = parser.parse_args()
    w, h = ASPECT_RATIOS[args.aspect]
    avatar = args.avatar or str(AVATAR_PATH)

    if not os.path.exists(avatar):
        print(f"⚠️  警告: 头像不存在 {avatar}，将不显示头像")

    try:
        if args.type == "cover":
            if not args.hook:
                parser.error("--hook 必填（封面）")
            hook = _normalize_newlines(args.hook)
            sub_hook = _normalize_newlines(args.sub)
            if args.mode == "simple":
                img = render_cover_simple(w, h, hook, sub_hook, avatar)
            else:
                img = render_cover_complex(w, h, hook, sub_hook, avatar)
        else:  # inside
            img = render_inside(w, h, avatar, page_num=args.page, total_pages=args.total)

        out = save_img(img, args.output)
        print(f"✅ Generated ({args.type} / {args.mode if args.type == 'cover' else 'blank'}): {out}")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
