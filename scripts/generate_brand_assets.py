#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent.parent
BRAND_DIR = ROOT / "assets" / "brand"

PAPER = (244, 241, 234, 255)
PAPER_STRONG = (255, 250, 240, 255)
INK = (23, 21, 19, 255)
GRAPHITE = (38, 34, 31, 255)
RED = (216, 52, 42, 255)
TEAL = (22, 132, 122, 255)
AMBER = (240, 165, 27, 255)
LINE = (216, 208, 196, 255)
MUTED = (104, 96, 90, 255)
WHITE = (255, 255, 255, 255)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)

    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=face)
    return box[2] - box[0], box[3] - box[1]


def draw_grid(draw: ImageDraw.ImageDraw, width: int, height: int, step: int, alpha: int = 46) -> None:
    color = (38, 34, 31, alpha)
    for x in range(0, width + 1, step):
        draw.line((x, 0, x, height), fill=color, width=1)
    for y in range(0, height + 1, step):
        draw.line((0, y, width, y), fill=color, width=1)


def draw_mark(base: Image.Image, box: tuple[int, int, int, int], with_background: bool = False) -> None:
    draw = ImageDraw.Draw(base, "RGBA")
    x1, y1, x2, y2 = box
    width = x2 - x1
    height = y2 - y1
    unit = min(width, height)
    cx = x1 + width / 2
    cy = y1 + height / 2

    if with_background:
        radius = int(unit * 0.17)
        draw.rounded_rectangle((x1, y1, x2, y2), radius=radius, fill=PAPER_STRONG, outline=LINE, width=max(2, unit // 80))

    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow, "RGBA")
    glow_draw.arc(
        (cx - unit * 0.34, cy - unit * 0.34, cx + unit * 0.34, cy + unit * 0.34),
        start=38,
        end=320,
        fill=(216, 52, 42, 120),
        width=max(6, int(unit * 0.07)),
    )
    glow_draw.arc(
        (cx - unit * 0.25, cy - unit * 0.25, cx + unit * 0.25, cy + unit * 0.25),
        start=210,
        end=70,
        fill=(22, 132, 122, 110),
        width=max(5, int(unit * 0.055)),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(radius=max(2, int(unit * 0.025))))
    base.alpha_composite(glow)

    outer = (cx - unit * 0.34, cy - unit * 0.34, cx + unit * 0.34, cy + unit * 0.34)
    inner = (cx - unit * 0.22, cy - unit * 0.22, cx + unit * 0.22, cy + unit * 0.22)
    draw.arc(outer, start=35, end=318, fill=GRAPHITE, width=max(8, int(unit * 0.095)))
    draw.arc(outer, start=322, end=386, fill=RED, width=max(8, int(unit * 0.095)))
    draw.arc(inner, start=205, end=28, fill=TEAL, width=max(7, int(unit * 0.07)))

    node_size = unit * 0.095
    nodes = [
        (cx + unit * 0.25, cy - unit * 0.2, RED),
        (cx - unit * 0.27, cy + unit * 0.11, TEAL),
        (cx + unit * 0.14, cy + unit * 0.29, AMBER),
    ]
    for nx, ny, color in nodes:
        draw.ellipse((nx - node_size / 2, ny - node_size / 2, nx + node_size / 2, ny + node_size / 2), fill=color)
        draw.ellipse(
            (nx - node_size * 0.2, ny - node_size * 0.2, nx + node_size * 0.2, ny + node_size * 0.2),
            fill=PAPER_STRONG if with_background else PAPER,
        )

    diagonal = [
        (cx - unit * 0.04, cy - unit * 0.36),
        (cx + unit * 0.12, cy - unit * 0.36),
        (cx - unit * 0.08, cy + unit * 0.36),
        (cx - unit * 0.24, cy + unit * 0.36),
    ]
    draw.polygon(diagonal, fill=(240, 165, 27, 230))
    draw.line((cx - unit * 0.29, cy + unit * 0.39, cx + unit * 0.32, cy + unit * 0.39), fill=LINE, width=max(2, unit // 70))


def create_logo_mark() -> None:
    image = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    draw_mark(image, (88, 88, 936, 936), with_background=True)
    image.save(BRAND_DIR / "logo-mark.png")


def create_wordmark() -> None:
    image = Image.new("RGBA", (1400, 360), (0, 0, 0, 0))
    draw_mark(image, (28, 40, 300, 312), with_background=True)
    draw = ImageDraw.Draw(image, "RGBA")
    title_font = font(88, bold=True)
    sub_font = font(28, bold=False)
    micro_font = font(20, bold=True)

    draw.text((342, 78), "CHINAPLAS.LOL", font=title_font, fill=INK)
    draw.text((348, 172), "NON-OFFICIAL GUIDE", font=micro_font, fill=TEAL)
    draw.line((348, 214, 1132, 214), fill=LINE, width=4)
    draw.text((348, 240), "2026 SHANGHAI PLASTICS & RUBBER EXHIBITION NOTES", font=sub_font, fill=MUTED)
    image.save(BRAND_DIR / "logo-wordmark.png")


def create_favicons() -> None:
    favicon = Image.new("RGBA", (256, 256), PAPER)
    draw_mark(favicon, (16, 16, 240, 240), with_background=True)
    favicon.save(BRAND_DIR / "favicon.png")
    favicon.save(BRAND_DIR / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    favicon.resize((180, 180), Image.Resampling.LANCZOS).save(BRAND_DIR / "apple-touch-icon.png")


def create_hero() -> None:
    width, height = 1400, 1100
    image = Image.new("RGBA", (width, height), PAPER_STRONG)
    draw = ImageDraw.Draw(image, "RGBA")
    draw_grid(draw, width, height, 70, alpha=34)

    draw.rounded_rectangle((64, 64, width - 64, height - 64), radius=38, outline=LINE, width=4)
    draw.rectangle((64, 236, width - 64, 242), fill=GRAPHITE)
    draw.rectangle((64, 858, width - 64, 864), fill=GRAPHITE)

    routes = [
        ((150, 352, 1210, 352), RED, 18),
        ((210, 524, 1148, 524), TEAL, 18),
        ((170, 696, 1230, 696), AMBER, 18),
    ]
    for line, color, stroke in routes:
        draw.line(line, fill=color, width=stroke)
        draw.ellipse((line[0] - 18, line[1] - 18, line[0] + 18, line[1] + 18), fill=color)
        draw.ellipse((line[2] - 18, line[3] - 18, line[2] + 18, line[3] + 18), fill=color)

    machine_boxes = [
        (236, 286, 472, 418, "RAW"),
        (598, 458, 836, 590, "MOLD"),
        (934, 630, 1170, 762, "LOOP"),
        (514, 760, 770, 906, "NECC"),
    ]
    label_font = font(38, bold=True)
    small_font = font(22, bold=True)
    for x1, y1, x2, y2, label in machine_boxes:
        draw.rounded_rectangle((x1, y1, x2, y2), radius=18, fill=(244, 241, 234, 238), outline=GRAPHITE, width=4)
        tw, th = text_size(draw, label, label_font)
        draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2 - 4), label, font=label_font, fill=INK)
        draw.rectangle((x1 + 16, y2 - 22, x2 - 16, y2 - 16), fill=LINE)

    for x in range(130, 1240, 104):
        draw.line((x, 936, x + 42, 978), fill=(38, 34, 31, 95), width=3)
        draw.line((x + 42, 978, x + 84, 936), fill=(38, 34, 31, 95), width=3)

    draw.text((110, 112), "CHINAPLAS 2026", font=font(70, bold=True), fill=INK)
    draw.text((114, 194), "MATERIALS / MACHINERY / CIRCULAR SYSTEMS", font=small_font, fill=TEAL)
    draw.text((104, 992), "2026.4.21-24 · NECC HONGQIAO SHANGHAI · NON-OFFICIAL GUIDE", font=small_font, fill=MUTED)

    image.save(BRAND_DIR / "hero-industrial-map.png")


def create_social_card() -> None:
    width, height = 1200, 630
    image = Image.new("RGBA", (width, height), PAPER)
    draw = ImageDraw.Draw(image, "RGBA")
    draw_grid(draw, width, height, 60, alpha=30)
    draw.rounded_rectangle((36, 36, width - 36, height - 36), radius=32, outline=LINE, width=4)
    draw_mark(image, (70, 96, 410, 436), with_background=True)

    title_font = font(72, bold=True)
    sub_font = font(31, bold=False)
    micro_font = font(21, bold=True)
    draw.text((470, 124), "CHINAPLAS 2026", font=title_font, fill=INK)
    draw.text((474, 220), "Shanghai plastics & rubber exhibition guide", font=sub_font, fill=MUTED)
    draw.line((474, 292, 1040, 292), fill=GRAPHITE, width=5)
    draw.text((474, 330), "Dates · Venue · Scale · Themes · Official Links", font=sub_font, fill=TEAL)
    draw.text((474, 424), "NON-OFFICIAL REFERENCE · chinaplas.lol", font=micro_font, fill=RED)
    image.save(BRAND_DIR / "social-card.png")


def main() -> None:
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    create_logo_mark()
    create_wordmark()
    create_favicons()
    create_hero()
    create_social_card()
    print(f"Brand assets generated in {BRAND_DIR}")


if __name__ == "__main__":
    main()
