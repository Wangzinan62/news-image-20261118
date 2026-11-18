#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page as a single 1024x1024 PNG.

Everything is drawn with PIL vector shapes and real Noto fonts -- no AI
image generation, so no text can come out garbled. Layout is measured with
PIL's own text metrics; every block asserts it stays inside its panel.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
CX0, CX1 = MARGIN, W - MARGIN          # content box: 28..996 (968 wide)
PAPER = (246, 241, 229)                # #f6f1e5
INK = (22, 24, 29)                     # #16181d
RED = (179, 49, 42)                    # #b3312a
NAVY = (36, 66, 92)                    # #24425c
CREAM = (246, 241, 229)

FONT_DIR = "/usr/share/fonts/truetype/noto/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_BLACK = "NotoSerif-Black.ttf"
SERIF_BOLD = "NotoSerif-Bold.ttf"
SANS_BLACK = "NotoSans-Black.ttf"
SANS_BOLD = "NotoSans-Bold.ttf"
SANS_REG = "NotoSans-Regular.ttf"
COND_BOLD = "NotoSans-CondensedBold.ttf"


def wrap(draw, text, fnt, width):
    """Greedy word wrap measured with real glyph widths."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, text, fnt, lh, width, fill=INK):
    """Draw a wrapped left-aligned block; return the y just past it."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def hrule(draw, y, x0=CX0, x1=CX1, wdt=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=wdt)


# ---------------------------------------------------------------- icons
def icon_chip(d, x, y):
    """Computer chip with circuit pins, in a ~66x26 box at (x, y)."""
    d.rectangle([x + 2, y + 3, x + 30, y + 23], outline=NAVY, width=3)
    d.rectangle([x + 12, y + 9, x + 20, y + 17], fill=NAVY)
    for py in (7, 13, 19):
        d.line([(x - 6, y + py), (x + 2, y + py)], fill=NAVY, width=3)
        d.line([(x + 30, y + py), (x + 40, y + py)], fill=NAVY, width=3)
    d.line([(x + 40, y + 7), (x + 56, y + 7)], fill=NAVY, width=3)
    d.line([(x + 40, y + 19), (x + 50, y + 19), (x + 50, y + 24)],
           fill=NAVY, width=3)
    d.ellipse([x + 53, y + 4, x + 59, y + 10], fill=RED)


def icon_bridge(d, x, y):
    """Bridge silhouette with an explosion starburst, ~66x26 box."""
    deck_y = y + 20
    d.line([(x, deck_y), (x + 42, deck_y)], fill=NAVY, width=3)
    for tx in (x + 10, x + 32):
        d.line([(tx, y + 5), (tx, deck_y)], fill=NAVY, width=3)
    # main suspension cable as a shallow parabola through the tower tops
    pts = []
    for i in range(21):
        t = i / 20.0
        px = x + 2 + t * 38
        py = (y + 12) - 7 * (1 - (2 * t - 1) ** 2) + 0 * t
        pts.append((px, py + 5))
    d.line(pts, fill=NAVY, width=2)
    for sx in (x + 16, x + 21, x + 26):
        d.line([(sx, y + 13), (sx, deck_y)], fill=NAVY, width=2)
    d.line([(x + 2, y + 24), (x + 40, y + 24)], fill=NAVY, width=2)
    cx, cy = x + 54, y + 10
    for ang in range(0, 360, 45):
        r0, r1 = 3, 8 if ang % 90 == 0 else 6
        d.line([(cx + r0 * math.cos(math.radians(ang)),
                 cy + r0 * math.sin(math.radians(ang))),
                (cx + r1 * math.cos(math.radians(ang)),
                 cy + r1 * math.sin(math.radians(ang)))], fill=RED, width=2)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)


def icon_cyclone(d, x, y):
    """Cyclone spiral over waves, ~66x26 box."""
    cx, cy = x + 16, y + 11
    pts = []
    for i in range(60):
        t = i / 59.0
        ang = t * 4.2 * math.pi
        r = 1.5 + t * 10.5
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang) * 0.78))
    d.line(pts, fill=NAVY, width=3, joint="curve")
    for wx in range(x + 34, x + 64, 15):
        d.arc([wx, y + 16, wx + 12, y + 26], start=180, end=360,
              fill=NAVY, width=3)


def icon_dish(d, x, y):
    """Probe / dish with signal arcs among stars, ~66x26 box."""
    d.arc([x, y + 2, x + 26, y + 26], start=300, end=120, fill=NAVY, width=3)
    d.line([(x + 13, y + 14), (x + 24, y + 4)], fill=NAVY, width=3)
    d.ellipse([x + 23, y + 2, x + 27, y + 6], fill=RED)
    d.line([(x + 8, y + 20), (x + 13, y + 13), (x + 18, y + 20)],
           fill=NAVY, width=3)
    for r in (7, 12):
        d.arc([x + 30, y - 2, x + 30 + 2 * r, y - 2 + 2 * r],
              start=270, end=360, fill=NAVY, width=2)
    for sx, sy in ((x + 52, y + 16), (x + 60, y + 6), (x + 46, y + 22)):
        d.line([(sx - 2, sy), (sx + 2, sy)], fill=NAVY, width=2)
        d.line([(sx, sy - 2), (sx, sy + 2)], fill=NAVY, width=2)


def icon_cricket(d, x, y, s=96):
    """Cricket stumps, bat and ball in an s-wide box at (x, y)."""
    base = y + s - 8
    for i in range(3):
        sx = x + 14 + i * 11
        d.rounded_rectangle([sx, y + 26, sx + 6, base], radius=3, fill=NAVY)
    d.rectangle([x + 14, y + 22, x + 25, y + 26], fill=NAVY)
    d.rectangle([x + 28, y + 22, x + 39, y + 26], fill=NAVY)
    # bat: tilted handle + blade drawn as plain polygons
    d.polygon([(x + 56, y + 24), (x + 62, y + 25), (x + 66, y + 44),
               (x + 60, y + 43)], fill=NAVY)
    d.polygon([(x + 60, y + 42), (x + 78, y + 47), (x + 80, y + 80),
               (x + 62, y + 78)], fill=NAVY)
    # ball, clear of the bat
    d.ellipse([x + 82, y + 60, x + 96, y + 74], fill=RED)
    d.arc([x + 85, y + 62, x + 93, y + 72], start=100, end=260, fill=CREAM,
          width=2)


# ---------------------------------------------------------------- lead art
def lead_art(d, x0, y0, x1, y1):
    """Rising sun, three summit flags and a skyline in the lead column."""
    # rising sun with rays, top right
    sx, sy, r = x1 - 52, y0 + 42, 25
    for ang in range(0, 360, 30):
        d.line([(sx + (r + 5) * math.cos(math.radians(ang)),
                 sy + (r + 5) * math.sin(math.radians(ang))),
                (sx + (r + 13) * math.cos(math.radians(ang)),
                 sy + (r + 13) * math.sin(math.radians(ang)))],
               fill=RED, width=3)
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=RED)
    # skyline silhouette along the bottom
    base = y1
    buildings = [(0, 44), (26, 66), (54, 36), (78, 78), (108, 52),
                 (134, 88), (162, 48), (186, 68), (210, 40)]
    bw = (x1 - x0) / 9.0
    for i, (_, bh) in enumerate(buildings):
        bx = x0 + i * bw
        d.rectangle([bx + 1, base - bh, bx + bw - 1, base], fill=NAVY)
        for wy in range(int(base - bh) + 8, int(base) - 8, 13):
            d.rectangle([bx + 6, wy, bx + 10, wy + 4], fill=CREAM)
    # three flags on poles in front of the skyline
    pole_top = y0 + 78
    pole_bot = y1 - 30
    flags = []
    for i, fx in enumerate((x0 + 26, x0 + 92, x0 + 158)):
        d.line([(fx, pole_top), (fx, pole_bot)], fill=INK, width=3)
        flags.append((fx + 3, pole_top))
    # United States: red field, navy canton
    fx, fy = flags[0]
    d.rectangle([fx, fy, fx + 40, fy + 24], fill=RED)
    d.rectangle([fx, fy, fx + 17, fy + 12], fill=NAVY)
    # China: red field, cream stars
    fx, fy = flags[1]
    d.rectangle([fx, fy, fx + 40, fy + 24], fill=RED)
    d.ellipse([fx + 4, fy + 4, fx + 10, fy + 10], fill=CREAM)
    for dx, dy in ((13, 3), (15, 8), (13, 13)):
        d.ellipse([fx + dx, fy + dy, fx + dx + 3, fy + dy + 3], fill=CREAM)
    # Russia: white / blue / red thirds
    fx, fy = flags[2]
    d.rectangle([fx, fy, fx + 40, fy + 8], fill=(240, 240, 240))
    d.rectangle([fx, fy + 8, fx + 40, fy + 16], fill=NAVY)
    d.rectangle([fx, fy + 16, fx + 40, fy + 24], fill=RED)
    d.rectangle([fx, fy, fx + 40, fy + 24], outline=INK, width=1)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d._image = img

    # masthead ------------------------------------------------------
    hrule(d, 16, wdt=3)
    hrule(d, 22, wdt=1)
    d.text(((CX0 + CX1) / 2, 28), "THE WORLD IN ONE PICTURE",
           font=font(SERIF_BLACK, 30), fill=INK, anchor="ma")
    hrule(d, 70, wdt=2)

    # the date -- the single most important element ------------------
    d.text(((CX0 + CX1) / 2, 78), "WEDNESDAY",
           font=font(SERIF_BLACK, 88), fill=INK, anchor="ma")
    d.text(((CX0 + CX1) / 2, 168), "18 NOVEMBER 2026",
           font=font(SERIF_BOLD, 45), fill=RED, anchor="ma")
    hrule(d, 222, wdt=5)
    hrule(d, 231, wdt=1)

    # lead story ------------------------------------------------------
    lead_top, lead_bot = 243, 431
    d.text((40, lead_top + 6), "ASIA SUMMITS",
           font=font(SANS_BOLD, 22), fill=RED)
    y = block(d, 40, lead_top + 36,
              "APEC OPENS IN SHENZHEN AS QUAD MEETS IN MANILA",
              font(SANS_BLACK, 38), 43, 700)
    y = block(d, 40, y + 6,
              "Trump, Xi and regional leaders gather in China; tomorrow "
              "brings the first-ever US–China–Russia trilateral summit.",
              font(SANS_REG, 24), 27, 700)
    assert y <= lead_bot, f"lead text overflows: {y} > {lead_bot}"
    lead_art(d, 762, lead_top + 4, 984, lead_bot - 4)
    hrule(d, 441, wdt=2)

    # four panels, 2 x 2 ----------------------------------------------
    panels = [
        ("BUSINESS", "NVIDIA REVENUE DOUBLES TO $115.8BN",
         "First earnings since Jensen Huang's ouster — and the board "
         "says it will not bring him back.", icon_chip),
        ("UKRAINE WAR", "UKRAINE HITS CRIMEAN BRIDGE FOR SECOND DAY",
         "Kyiv strikes the Kerch Bridge again as Russia pounds bridges "
         "in the capital.", icon_bridge),
        ("WEATHER", "CYCLONE AKVAN BEARS DOWN ON INDIA'S COAST",
         "The Bay of Bengal storm intensifies, heading for Andhra "
         "Pradesh by Friday.", icon_cyclone),
        ("SCIENCE", "VOYAGER 1 NEARS ONE LIGHT-DAY FROM EARTH",
         "NASA's farthest probe is about to be a full day's "
         "light-travel from home — a first for any human-made object.",
         icon_dish),
    ]
    grid_top = 453
    row_h, row_gap = 180, 6
    col_w = (CX1 - CX0 - 16) // 2          # 476
    for i, (kicker, head, deck, icon) in enumerate(panels):
        row, col = divmod(i, 2)
        px = CX0 + col * (col_w + 16)
        py = grid_top + row * (row_h + row_gap)
        d.text((px + 12, py + 10), kicker, font=font(SANS_BOLD, 20),
               fill=RED)
        icon(d, px + col_w - 78, py + 8)
        y = block(d, px + 12, py + 32, head, font(SANS_BLACK, 34), 35,
                  col_w - 24)
        y = block(d, px + 12, y + 2, deck, font(SANS_REG, 24), 23,
                  col_w - 24)
        assert y <= py + row_h, f"panel {kicker} overflows: {y}"
    # rules between the grid rows / columns
    hrule(d, grid_top + row_h + row_gap // 2, wdt=1)
    mid_x = CX0 + col_w + 8
    d.line([(mid_x, grid_top + 4), (mid_x, grid_top + 2 * row_h + row_gap - 4)],
           fill=INK, width=1)

    # sport strip -------------------------------------------------------
    sp_top = grid_top + 2 * row_h + 2 * row_gap      # 825
    hrule(d, sp_top - 2, wdt=1)
    icon_cricket(d, CX0 + 8, sp_top + 4, s=92)
    tx = CX0 + 116
    d.text((tx, sp_top + 6), "SPORT", font=font(SANS_BOLD, 20), fill=RED)
    y = block(d, tx, sp_top + 32, "DHONI CALLS TIME ON THE IPL",
              font(SANS_BLACK, 34), 35, CX1 - tx - 12)
    y = block(d, tx, y + 4,
              "India's World Cup-winning captain retires from the league "
              "to become Chennai Super Kings mentor.",
              font(SANS_REG, 24), 24, CX1 - tx - 12)
    assert y <= 944, f"sport strip overflows: {y}"

    # ticker -------------------------------------------------------------
    band_top, band_bot = 948, 1014
    d.rectangle([0, band_top, W, band_bot], fill=INK)
    ticker = ("ALSO TODAY · Kuwait and Bahrain intercept drones as "
              "US–Iran exchanges continue · Gaza ceasefire 'faces "
              "imminent collapse', peace board warns · SpaceX catches "
              "a falling Starship")
    lines = wrap(d, ticker, font(COND_BOLD, 24), 940)
    assert len(lines) <= 2, f"ticker needs {len(lines)} lines"
    ty = band_top + (band_bot - band_top - len(lines) * 28) // 2
    for line in lines:
        d.text((W / 2, ty), line, font=font(COND_BOLD, 24), fill=CREAM,
               anchor="ma")
        ty += 28

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
