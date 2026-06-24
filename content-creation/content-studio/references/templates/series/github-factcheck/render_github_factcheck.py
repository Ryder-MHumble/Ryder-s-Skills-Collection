#!/usr/bin/env python3
"""Render Xiaohongshu cards for the series: 一分钟打假一个 GitHub 热门项目.

Input: JSON spec with cards. Output: 1080x1440 PNG cards + contact sheet.
This template intentionally uses measured PIL text flow instead of browser
absolute positioning, so overflow fails fast instead of clipping silently.
"""
from __future__ import annotations

import argparse
import json
import pathlib
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont, ImageOps

W, H = 1080, 1440
FOOTER_H = 78
SAFE_BOTTOM = H - FOOTER_H - 36
MX = 58
CONTENT_W = W - MX * 2

PAPER = "#F4EBDD"
PAPER_2 = "#FFF9ED"
INK = "#090909"
RED = "#E93B45"
MUTED = "#6C6256"
GRID = "#E2D8C7"
YELLOW = "#FFD748"
GREEN = "#E9FFE8"

SKILL_ROOT = pathlib.Path(__file__).resolve().parents[4]
DEFAULT_AVATAR = SKILL_ROOT / "assets" / "avatar.png"
FONT_CN = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_CN_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_MONO = "/System/Library/Fonts/SFNSMono.ttf"
FONT_UI = "/System/Library/Fonts/Avenir Next.ttc"


def fnt(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_MONO if mono else (FONT_CN_BOLD if bold else FONT_CN)
    try:
        return ImageFont.truetype(path, size=size)
    except OSError:
        return ImageFont.load_default(size=size)


def size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    b = draw.textbbox((0, 0), str(text), font=font)
    return b[2] - b[0], b[3] - b[1]


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    for para in str(text).split("\n"):
        cur = ""
        for ch in para:
            trial = cur + ch
            if not cur or size(draw, trial, font)[0] <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
        if para == "":
            lines.append("")
    return lines


def line_height(font: ImageFont.FreeTypeFont, gap: int) -> int:
    a, d = font.getmetrics()
    return a + d + gap


def fit_font(draw: ImageDraw.ImageDraw, text: str, start_size: int, min_size: int, width: int) -> tuple[ImageFont.FreeTypeFont, int, int]:
    """Shrink one-line text until it fits; fail rather than clip silently."""
    for font_size in range(start_size, min_size - 1, -2):
        font = fnt(font_size, True)
        tw, _ = size(draw, text, font)
        if tw <= width:
            return font, font_size, tw
    raise RuntimeError(f"Text does not fit cover line: {text!r}")


def para_h(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, width: int, gap: int = 7) -> int:
    lines = wrap(draw, text, font, width)
    if not lines:
        return 0
    return len(lines) * line_height(font, gap) - gap


def draw_wrap(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.FreeTypeFont, width: int, fill: str, gap: int = 7) -> int:
    x, y = xy
    for line in wrap(draw, text, font, width):
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height(font, gap)
    return y


def avatar(path: pathlib.Path, diameter: int) -> Image.Image:
    src = Image.open(path).convert("RGB")
    src = ImageOps.fit(src, (diameter, diameter), method=Image.Resampling.LANCZOS)
    mask = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, diameter - 1, diameter - 1), fill=255)
    out = Image.new("RGBA", (diameter, diameter), (0, 0, 0, 0))
    out.paste(src, (0, 0), mask)
    return out


def rect(draw: ImageDraw.ImageDraw, box, fill: str, outline: str = INK, width: int = 3):
    draw.rectangle(box, fill=fill, outline=outline, width=width)


def fit_image_top(src: Image.Image, target: tuple[int, int]) -> Image.Image:
    """Fill target size, anchoring the crop to the top of a webpage screenshot."""
    tw, th = target
    src = src.convert("RGB")
    scale = max(tw / src.width, th / src.height)
    rw, rh = int(src.width * scale), int(src.height * scale)
    resized = src.resize((rw, rh), Image.Resampling.LANCZOS)
    left = max(0, (rw - tw) // 2)
    top = 0
    return resized.crop((left, top, left + tw, top + th))


def contain_image_top(src: Image.Image, target: tuple[int, int], bg: str = PAPER_2) -> Image.Image:
    """Show the whole screenshot, top-aligned, without cropping repo UI."""
    tw, th = target
    src = src.convert("RGB")
    scale = min(tw / src.width, th / src.height)
    rw, rh = int(src.width * scale), int(src.height * scale)
    resized = src.resize((rw, rh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (tw, th), bg)
    canvas.paste(resized, ((tw - rw) // 2, 0))
    return canvas


@dataclass
class CardCanvas:
    idx: int
    total: int
    spec: dict
    avatar_path: pathlib.Path

    def __post_init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.draw = ImageDraw.Draw(self.img)
        self.grid()
        self.header()
        self.footer()

    def grid(self):
        for x in range(0, W + 1, 50):
            self.draw.line((x, 0, x, H), fill=GRID, width=1)
        for y in range(0, H + 1, 50):
            self.draw.line((0, y, W, y), fill=GRID, width=1)
        self.draw.rectangle((26, 26, W - 26, H - 26), outline=INK, width=0)

    def header(self):
        av = avatar(self.avatar_path, 42)
        x, y = MX, 52
        rect(self.draw, (x, y, x + 288, y + 70), PAPER_2, width=3)
        self.img.paste(av, (x + 16, y + 14), av)
        self.draw.ellipse((x + 16, y + 14, x + 58, y + 56), outline=INK, width=3)
        self.draw.text((x + 76, y + 18), "叫我 Ryder 就好", font=fnt(27, True), fill=INK)
        page = f"{self.idx:02d}/{self.total:02d}"
        pf = fnt(29, True, mono=True)
        tw, _ = size(self.draw, page, pf)
        px, py = W - MX - tw - 36, 58
        rect(self.draw, (px, py, px + tw + 36, py + 54), INK, outline=INK, width=0)
        self.draw.text((px + 18, py + 12), page, font=pf, fill=PAPER_2)

    def footer(self):
        left = self.spec.get("footer_left", "GITHUB FACTCHECK")
        right = self.spec.get("footer_right", "REPORT CARD")
        top = H - FOOTER_H
        self.draw.rectangle((0, top, W, H), fill=PAPER)
        self.draw.line((0, top, W, top), fill=RED, width=4)
        ff = fnt(22, True, mono=True)
        self.draw.text((MX, top + 26), left, font=ff, fill=INK)
        tw, _ = size(self.draw, right, ff)
        self.draw.text((W - MX - tw, top + 26), right, font=ff, fill=INK)

    def kicker(self, text: str, y: int) -> int:
        font = fnt(29, True)
        tw, _ = size(self.draw, text, font)
        rect(self.draw, (MX, y, MX + tw + 34, y + 56), RED, width=3)
        self.draw.text((MX + 17, y + 10), text, font=font, fill=PAPER_2)
        return y + 76

    def title(self, text: str, y: int, font_size: int = 58) -> int:
        font = fnt(font_size, True)
        lines = wrap(self.draw, text, font, CONTENT_W - 50)
        h = len(lines) * line_height(font, 4) + 24
        widest = min(CONTENT_W, max(size(self.draw, line, font)[0] for line in lines) + 48)
        rect(self.draw, (MX, y, MX + widest, y + h), PAPER_2, width=4)
        ty = y + 11
        for line in lines:
            self.draw.text((MX + 24, ty), line, font=font, fill=INK)
            ty += line_height(font, 4)
        return y + h + 28

    def metric_strip(self, metrics: list[dict], y: int) -> int:
        if not metrics:
            return y
        cols = min(4, len(metrics))
        gap = 14
        box_w = (CONTENT_W - gap * (cols - 1)) // cols
        box_h = 128
        for i, metric in enumerate(metrics[:4]):
            x = MX + i * (box_w + gap)
            rect(self.draw, (x, y, x + box_w, y + box_h), INK, outline=INK, width=0)
            self.draw.text((x + 16, y + 14), metric.get("label", ""), font=fnt(19, True), fill=YELLOW)
            draw_wrap(self.draw, (x + 16, y + 48), metric.get("value", ""), fnt(28, True), box_w - 32, fill=PAPER_2, gap=3)
        return y + box_h + 24

    def evidence(self, label: str, lines: list[str], y: int, font_size: int = 23) -> int:
        lab_f = fnt(21, True)
        lab_w, _ = size(self.draw, label, lab_f)
        rect(self.draw, (MX, y, MX + lab_w + 28, y + 42), YELLOW, width=3)
        self.draw.text((MX + 14, y + 9), label, font=lab_f, fill=INK)
        y += 42
        mono = fnt(font_size, True, mono=True)
        all_lines: list[str] = []
        for line in lines:
            all_lines.extend(wrap(self.draw, line, mono, CONTENT_W - 48))
        h = 28 + len(all_lines) * line_height(mono, 5) + 20
        rect(self.draw, (MX, y, MX + CONTENT_W, y + h), INK, outline=INK, width=0)
        ty = y + 20
        for line in all_lines:
            self.draw.text((MX + 24, ty), line, font=mono, fill=GREEN)
            ty += line_height(mono, 5)
        return y + h + 24

    def note(self, tag: str, text: str, y: int, font_size: int = 29, compact: bool = False) -> int:
        pad = 20 if compact else 23
        tag_f = fnt(21 if compact else 23, True)
        body_f = fnt(font_size, True)
        inner_w = CONTENT_W - pad * 2
        tag_w, tag_h = size(self.draw, tag, tag_f)
        body_h = para_h(self.draw, text, body_f, inner_w, gap=7)
        h = pad + tag_h + 14 + body_h + pad
        rect(self.draw, (MX, y, MX + CONTENT_W, y + h), PAPER_2, width=3)
        rect(self.draw, (MX + pad, y + pad, MX + pad + tag_w + 24, y + pad + tag_h + 12), INK, outline=INK, width=0)
        self.draw.text((MX + pad + 12, y + pad + 6), tag, font=tag_f, fill=PAPER_2)
        draw_wrap(self.draw, (MX + pad, y + pad + tag_h + 26), text, body_f, inner_w, fill=INK, gap=7)
        return y + h + (14 if compact else 18)

    def quote(self, text: str, y: int) -> int:
        font = fnt(35, True)
        h = para_h(self.draw, text, font, CONTENT_W - 48, gap=8) + 38
        rect(self.draw, (MX, y, MX + CONTENT_W, y + h), RED, width=4)
        draw_wrap(self.draw, (MX + 24, y + 18), text, font, CONTENT_W - 48, fill=PAPER_2, gap=8)
        return y + h + 18

    def render_cover(self):
        if self.spec.get("cover_style") in {"series_github_project", "series_readme"}:
            return self.render_series_github_project_cover()

        y = 158
        self.draw.text((MX, y), self.spec.get("series_name", "一分钟打假一个 GitHub 热门项目"), font=fnt(32, True), fill=RED)
        y += 72
        headline = self.spec.get("headline", [])
        for i, line in enumerate(headline):
            start_size = 94 if len(line) > 8 else 106
            font, font_size, tw = fit_font(self.draw, line, start_size, 62, CONTENT_W - 54)
            fill = RED if i == len(headline) - 1 else PAPER_2
            text_fill = PAPER_2 if fill == RED else INK
            h = line_height(font, 4) + 18
            rect(self.draw, (MX, y, MX + tw + 54, y + h), fill, width=4)
            self.draw.text((MX + 26, y + 7), line, font=font, fill=text_fill)
            y += h + 18
        subtitle = self.spec.get("subtitle", "")
        if subtitle:
            sub_font = fnt(35, True)
            sub_h = para_h(self.draw, subtitle, sub_font, CONTENT_W - 48, gap=8) + 44
            if y + 6 + sub_h > SAFE_BOTTOM - 260:
                raise RuntimeError(f"Cover subtitle overflows: {subtitle!r}")
            rect(self.draw, (MX, y + 6, MX + CONTENT_W, y + 6 + sub_h), INK, outline=INK, width=0)
            draw_wrap(self.draw, (MX + 24, y + 28), subtitle, sub_font, CONTENT_W - 48, fill=PAPER_2, gap=8)
        chips = self.spec.get("chips", [])
        cy = SAFE_BOTTOM - 150
        cx = MX
        for chip in chips[:3]:
            cf = fnt(23, True)
            tw, _ = size(self.draw, chip, cf)
            if cx + tw + 28 > W - MX:
                raise RuntimeError(f"Cover chips overflow near: {chip!r}")
            rect(self.draw, (cx, cy, cx + tw + 28, cy + 48), YELLOW, width=3)
            self.draw.text((cx + 14, cy + 11), chip, font=cf, fill=INK)
            cx += tw + 44
        av = avatar(self.avatar_path, 230)
        ax, ay = W - MX - 235, SAFE_BOTTOM - 225
        self.draw.ellipse((ax + 10, ay + 10, ax + 240, ay + 240), fill=INK)
        self.img.paste(av, (ax, ay), av)
        self.draw.ellipse((ax, ay, ax + 230, ay + 230), outline=INK, width=8)

    def render_series_github_project_cover(self):
        y = 150
        title = self.spec.get("main_title", self.spec.get("series_name", "一分钟打假一个 Github热门项目"))
        title_font = fnt(52, True)
        title_lines = wrap(self.draw, title, title_font, CONTENT_W - 64)
        title_h = len(title_lines) * line_height(title_font, 4) + 34
        rect(self.draw, (MX, y, MX + CONTENT_W, y + title_h), PAPER_2, width=4)
        ty = y + 17
        for line in title_lines:
            self.draw.text((MX + 26, ty), line, font=title_font, fill=INK)
            ty += line_height(title_font, 4)
        y += title_h + 22

        subtitle = self.spec.get("subtitle", "")
        if subtitle:
            sub_font = fnt(48, True)
            sub_lines = wrap(self.draw, subtitle, sub_font, CONTENT_W - 56)
            sub_h = len(sub_lines) * line_height(sub_font, 5) + 28
            rect(self.draw, (MX, y, MX + CONTENT_W, y + sub_h), RED, width=4)
            sy = y + 13
            for line in sub_lines:
                self.draw.text((MX + 28, sy), line, font=sub_font, fill=PAPER_2)
                sy += line_height(sub_font, 5)
            y += sub_h + 28

        shot_path = self.spec.get("project_screenshot") or self.spec.get("readme_screenshot")
        if not shot_path:
            raise RuntimeError("series_github_project cover requires project_screenshot")
        shot = Image.open(pathlib.Path(shot_path).expanduser())
        label_f = fnt(23, True, mono=True)
        label = self.spec.get("screenshot_label", "GITHUB PROJECT PAGE")
        label_w, _ = size(self.draw, label, label_f)
        rect(self.draw, (MX, y, MX + label_w + 30, y + 46), YELLOW, width=3)
        self.draw.text((MX + 15, y + 10), label, font=label_f, fill=INK)
        y += 52

        box_h = min(755, SAFE_BOTTOM - y - 24)
        if box_h < 520:
            raise RuntimeError("Cover screenshot area is too small")
        fitted = contain_image_top(shot, (CONTENT_W, box_h))
        self.img.paste(fitted, (MX, y))
        self.draw.rectangle((MX, y, MX + CONTENT_W, y + box_h), outline=INK, width=5)

        project = self.spec.get("project", "Headroom")
        chip = self.spec.get("screenshot_chip", f"{project} / GitHub")
        chip_f = fnt(24, True)
        chip_w, _ = size(self.draw, chip, chip_f)
        rect(self.draw, (MX + 18, y + box_h - 58, MX + chip_w + 52, y + box_h - 12), INK, outline=INK, width=0)
        self.draw.text((MX + 34, y + box_h - 49), chip, font=chip_f, fill=PAPER_2)

    def render_finding(self):
        y = 160
        y = self.kicker(self.spec.get("kicker", "测试报告"), y)
        y = self.title(self.spec.get("title", ""), y, self.spec.get("title_size", 58))
        y = self.metric_strip(self.spec.get("metrics", []), y)
        for ev in self.spec.get("evidence", []):
            y = self.evidence(ev.get("label", "证据"), ev.get("lines", []), y, ev.get("font_size", 23))
        for item in self.spec.get("body", []):
            y = self.note(item.get("tag", "结论"), item.get("text", ""), y, item.get("font_size", 29), item.get("compact", False))
        if self.spec.get("quote"):
            y = self.quote(self.spec["quote"], y + 2)
        if y > SAFE_BOTTOM:
            raise RuntimeError(f"Card {self.idx} overflows: y={y}, safe={SAFE_BOTTOM}, title={self.spec.get('title')}")

    def render_refs(self):
        y = 160
        y = self.kicker(self.spec.get("kicker", "参考材料"), y)
        y = self.title(self.spec.get("title", "REFERENCES"), y, 58)
        for ref in self.spec.get("refs", []):
            y = self.note("REF", ref, y, 24, True)
        if self.spec.get("quote"):
            y = self.quote(self.spec["quote"], y)
        if y > SAFE_BOTTOM:
            raise RuntimeError(f"References overflow: y={y}, safe={SAFE_BOTTOM}")

    def render(self) -> Image.Image:
        card_type = self.spec.get("type", "finding")
        if card_type == "cover":
            self.render_cover()
        elif card_type == "references":
            self.render_refs()
        else:
            self.render_finding()
        return self.img


def render_spec(spec: dict, out_dir: pathlib.Path, avatar_path: pathlib.Path) -> list[pathlib.Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    cards = spec["cards"]
    paths: list[pathlib.Path] = []
    for idx, card in enumerate(cards, 1):
        card.setdefault("series_name", spec.get("series_name", "一分钟打假一个 GitHub 热门项目"))
        canvas = CardCanvas(idx, len(cards), card, avatar_path)
        img = canvas.render()
        slug = card.get("slug", f"card-{idx:02d}")
        path = out_dir / f"{idx:02d}-{slug}.png"
        img.save(path)
        paths.append(path)
    make_contact_sheet(paths, out_dir / "contact-sheet.png")
    return paths


def make_contact_sheet(paths: list[pathlib.Path], out: pathlib.Path):
    thumbs = []
    for path in paths:
        im = Image.open(path).convert("RGB")
        im.thumbnail((270, 360))
        canvas = Image.new("RGB", (270, 360), PAPER)
        canvas.paste(im, ((270 - im.width) // 2, (360 - im.height) // 2))
        thumbs.append((path, canvas))
    cols = 3
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (270 * cols + 32 * (cols + 1), 360 * rows + 54 * (rows + 1)), INK)
    d = ImageDraw.Draw(sheet)
    lf = fnt(14, True, mono=True)
    for idx, (path, thumb) in enumerate(thumbs):
        row, col = divmod(idx, cols)
        x = 32 + col * (270 + 32)
        y = 42 + row * (360 + 54)
        sheet.paste(thumb, (x, y))
        d.text((x, y - 25), path.stem[:30], fill=PAPER_2, font=lf)
    sheet.save(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, type=pathlib.Path)
    parser.add_argument("--out", required=True, type=pathlib.Path)
    parser.add_argument("--avatar", type=pathlib.Path, default=DEFAULT_AVATAR)
    args = parser.parse_args()
    spec = json.loads(args.data.read_text(encoding="utf-8"))
    paths = render_spec(spec, args.out, args.avatar)
    for path in paths:
        im = Image.open(path)
        if im.size != (W, H):
            raise RuntimeError(f"Bad size: {path} {im.size}")
    print(f"rendered={len(paths)} out={args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
