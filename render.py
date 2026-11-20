# render.py — builds entry.png (1024x1024) for news-image-20261119 v3.
# Run: python3 render.py  (writes entry.png next to this file)
# Uses Pillow at BUILD time only. The entry program (main.py) is stdlib-only
# and copies the pre-rendered entry.png byte-for-byte; it never imports this.
# All text is rendered with real Liberation glyphs (see FONTS below).
# All drawings are original flat-colour illustrations drawn in code.

import math
from PIL import Image, ImageDraw, ImageFont

from coast import CONTINENTS, ISLANDS, MAP_DOTS

W, H = 1024, 1024
PAPER = (247, 241, 222)
INK = (26, 26, 26)
RED = (176, 30, 36)
DARKRED = (138, 22, 28)
BLUE = (31, 78, 121)
TEAL = (15, 118, 110)
GREEN = (46, 125, 50)
PURPLE = (107, 63, 160)
BROWN = (163, 60, 31)
GREY = (85, 85, 85)
LIGHTBLUE = (168, 205, 230)
LAND = (232, 205, 150)
SEA = (178, 212, 232)
CARD_BG = (255, 252, 244)
GOLD = (201, 162, 39)

FDIR = "/usr/share/fonts/truetype/liberation/"


def F(name, size):
    return ImageFont.truetype(FDIR + name, size)


SERIF_B = lambda s: F("LiberationSerif-Bold.ttf", s)
SERIF_I = lambda s: F("LiberationSerif-Italic.ttf", s)
SERIF_R = lambda s: F("LiberationSerif-Regular.ttf", s)
SANS_B = lambda s: F("LiberationSans-Bold.ttf", s)
SANS_R = lambda s: F("LiberationSans-Regular.ttf", s)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, max_w, fill, leading=None):
    lines = wrap(draw, text, font, max_w)
    lh = leading if leading is not None else int(font.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y, len(lines)


def fit_lines(draw, text, font, max_w, max_lines):
    """Wrap text; if it exceeds max_lines, shorten with ellipsis."""
    lines = wrap(draw, text, font, max_w)
    while len(lines) > max_lines and len(text) > 10:
        text = text.rsplit(" ", 1)[0] + " …"
        lines = wrap(draw, text, font, max_w)
    return lines


def text_lines(draw, x, y, lines, font, fill, leading=None):
    lh = leading if leading is not None else int(font.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- flags
def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 34, 52), outline=INK, width=1)
    for i in range(1, 7, 2):
        d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                    fill=(255, 255, 255))
    d.rectangle([x, y, x + w * 0.4, y + h * 0.54], fill=(31, 60, 120))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16), outline=INK, width=1)
    d.text((x + 2, y), "★", font=SANS_B(int(h * 0.6)), fill=(255, 222, 0))


def flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle([x, y, x + w, y + h // 3], fill=(255, 255, 255))
    d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
    d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 50))


def flag_kr(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK, width=1)
    d.ellipse([x + w * 0.38, y + h * 0.28, x + w * 0.62, y + h * 0.72],
              fill=(205, 0, 0))
    d.ellipse([x + w * 0.38, y + h * 0.5, x + w * 0.62, y + h * 0.72],
              fill=(0, 71, 160))


def flag_dk(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(198, 12, 48), outline=INK, width=1)
    d.rectangle([x + w * 0.32, y, x + w * 0.42, y + h], fill=(255, 255, 255))
    d.rectangle([x, y + h * 0.42, x + w, y + h * 0.58], fill=(255, 255, 255))


def flag_us_small(d, x, y, w, h):
    flag_us(d, x, y, w, h)


# ---------------------------------------------------------------- lead art
def art_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 62, 110))
    d.rectangle([x, y, x + w, y + 22], fill=(176, 30, 36))
    d.text((x + 8, y + 3), "APEC 2026 · SHENZHEN", font=SANS_B(13),
           fill=(255, 255, 255))
    # flags behind the three seats
    flag_us(d, x + 28, y + 34, 44, 26)
    flag_cn(d, x + w // 2 - 22, y + 34, 44, 26)
    flag_ru(d, x + w - 72, y + 34, 44, 26)
    # table
    d.rounded_rectangle([x + 10, y + 96, x + w - 10, y + h - 8], radius=8,
                        fill=(232, 205, 150), outline=INK, width=2)
    d.rectangle([x + 10, y + 96, x + w - 10, y + 104], fill=(255, 255, 255))
    # three seated figures
    for cx, suit, tie in ((x + 55, (30, 30, 30), (176, 30, 36)),
                          (x + w // 2, (20, 20, 20), (176, 30, 36)),
                          (x + w - 55, (40, 40, 40), (31, 78, 121))):
        d.ellipse([cx - 16, y + 62, cx + 16, y + 94], fill=(235, 200, 170),
                  outline=INK, width=1)
        d.ellipse([cx - 8, y + 74, cx - 4, y + 78], fill=INK)
        d.ellipse([cx + 4, y + 74, cx + 8, y + 78], fill=INK)
        d.polygon([(cx - 24, y + 96), (cx + 24, y + 96), (cx + 18, y + 122),
                   (cx - 18, y + 122)], fill=suit)
        d.polygon([(cx - 4, y + 96), (cx + 4, y + 96), (cx, y + 116)],
                  fill=tie)
    # name strip across the table front, drawn last so no name is hidden
    d.rectangle([x + 10, y + h - 28, x + w - 10, y + h - 8], fill=(24, 62, 110))
    for cx, name in ((x + 55, "TRUMP"), (x + w // 2, "XI"),
                     (x + w - 55, "PUTIN")):
        tw = d.textlength(name, font=SANS_B(11))
        d.text((cx - tw / 2, y + h - 25), name, font=SANS_B(11),
               fill=(255, 255, 255))


def art_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    # courthouse
    d.polygon([(x + 30, y + 58), (x + w // 2, y + 22), (x + w - 30, y + 58)],
              fill=(150, 80, 50), outline=INK, width=2)
    d.rectangle([x + 30, y + 58, x + w - 30, y + h - 6], fill=(196, 120, 70),
                outline=INK, width=2)
    for i in range(5):
        cx = x + 52 + i * (w - 104) // 4
        d.rectangle([cx - 7, y + 62, cx + 7, y + h - 14], fill=(245, 235, 210),
                    outline=INK, width=1)
    d.rectangle([x + w // 2 - 14, y + h - 34, x + w // 2 + 14, y + h - 14],
                fill=(90, 50, 30))
    # scales of justice, right side
    sx, sy = x + w - 62, y + 26
    d.line([sx, sy, sx, sy + 44], fill=INK, width=3)
    d.line([sx - 26, sy + 6, sx + 26, sy + 6], fill=INK, width=3)
    d.line([sx - 26, sy + 6, sx - 34, sy + 26], fill=INK, width=2)
    d.line([sx - 26, sy + 6, sx - 18, sy + 26], fill=INK, width=2)
    d.line([sx + 26, sy + 6, sx + 18, sy + 26], fill=INK, width=2)
    d.line([sx + 26, sy + 6, sx + 34, sy + 26], fill=INK, width=2)
    d.arc([sx - 40, sy + 20, sx - 12, sy + 34], 0, 180, fill=GOLD, width=3)
    d.arc([sx + 12, sy + 20, sx + 40, sy + 34], 0, 180, fill=GOLD, width=3)
    # 9-6 badge
    d.rounded_rectangle([x + 8, y + 8, x + 64, y + 34], radius=4,
                        fill=RED, outline=(255, 255, 255), width=2)
    d.text((x + 14, y + 10), "9 – 6", font=SANS_B(17), fill=(255, 255, 255))


def art_climate(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 110, 105))
    # globe, left
    gx, gy, gr = x + 52, y + 62, 38
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(60, 140, 220),
              outline=(255, 255, 255), width=2)
    d.ellipse([gx - 22, gy - 26, gx - 2, gy - 6], fill=(80, 180, 90))
    d.ellipse([gx - 6, gy + 8, gx + 22, gy + 30], fill=(80, 180, 90))
    d.ellipse([gx + 6, gy - 24, gx + 24, gy - 8], fill=(80, 180, 90))
    # thermometer, right edge
    tx = x + w - 40
    d.rounded_rectangle([tx, y + 14, tx + 16, y + 86], radius=8,
                        fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([tx + 5, y + 26, tx + 11, y + 82], fill=RED)
    d.ellipse([tx - 6, y + 78, tx + 22, y + 106], fill=RED, outline=INK, width=2)
    # struck-through text panel between globe and thermometer
    d.rectangle([x + 98, y + 20, x + w - 50, y + 50], fill=(255, 252, 244))
    d.text((x + 104, y + 24), "FOSSIL FUELS", font=SANS_B(12), fill=INK)
    d.line([x + 102, y + 35, x + w - 52, y + 35], fill=RED, width=3)
    d.text((x + 104, y + 56), "$120BN ADAPTATION AID", font=SANS_B(11),
           fill=(255, 255, 255))
    # CUT stamp below the panel
    d.rounded_rectangle([x + 104, y + 80, x + 168, y + 112], radius=4,
                        outline=RED, width=3)
    d.text((x + 114, y + 85), "CUT", font=SANS_B(20), fill=RED)


# ---------------------------------------------------------------- grid art
def art_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 205, 230))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(120, 150, 180))
    d.polygon([(x, y + h - 22), (x + w // 2, y + 12), (x + w, y + h - 22)],
              fill=(200, 200, 200))
    d.arc([x + 18, y + 2, x + w - 18, y + h - 6], 180, 360, fill=INK, width=3)
    d.line([x, y + h - 26, x + w, y + h - 26], fill=INK, width=3)
    for i in range(5):
        cx = x + 20 + i * (w - 40) // 4
        d.line([cx, y + h - 26, cx, y + h - 40], fill=INK, width=2)
    # explosion star
    ex, ey = x + w - 34, y + 16
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([ex, ey, ex + 13 * math.cos(a), ey + 13 * math.sin(a)],
               fill=(255, 140, 0), width=3)
    d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 60, 0))


def art_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 64))
    for i, bh in enumerate((34, 48, 28, 44, 38)):
        bx = x + 10 + i * (w - 20) // 5
        bw = (w - 20) // 5 - 6
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(40, 60, 110),
                    outline=(120, 150, 200), width=1)
        for wy in range(3):
            d.rectangle([bx + 3, y + h - bh + 5 + wy * 10, bx + 8,
                         y + h - bh + 9 + wy * 10], fill=(255, 220, 100))
    # missile trail
    d.line([x + w - 20, y + 8, x + w - 48, y + 34], fill=(255, 200, 60), width=3)
    d.ellipse([x + w - 24, y + 4, x + w - 16, y + 12], fill=(255, 120, 0))
    d.ellipse([x + 14, y + 6, x + 20, y + 12], fill=(255, 255, 255))


def art_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(232, 205, 150))
    cx, cy = x + w // 2, y + h // 2 - 4
    for r in (8, 16, 24, 32):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(31, 78, 121),
              width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(176, 30, 36))
    d.text((x + 6, y + 2), "ODISHA", font=SANS_B(10), fill=INK)


def art_gavel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 230, 200))
    # gavel head, tilted, with handle down to the sound block
    d.polygon([(x + 52, y + 12), (x + 132, y + 28), (x + 128, y + 44),
               (x + 48, y + 28)], fill=(120, 72, 30), outline=INK, width=2)
    d.line([x + 92, y + 32, x + 148, y + 52], fill=(120, 72, 30), width=6)
    d.ellipse([x + 88, y + 48, x + 112, y + 60], fill=(90, 50, 30),
              outline=INK, width=1)
    flag_kr(d, x + 8, y + 8, 30, 18)
    d.text((x + 118, y + 8), "OVERTURNED", font=SANS_B(11), fill=RED)


def art_greenland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 205, 230))
    d.polygon([(x, y + h), (x + 40, y + 14), (x + 80, y + h)],
              fill=(240, 240, 240), outline=INK, width=1)
    d.polygon([(x + 60, y + h), (x + 120, y + 6), (x + 180, y + h)],
              fill=(220, 230, 240), outline=INK, width=1)
    flag_dk(d, x + 10, y + 8, 30, 18)
    flag_us_small(d, x + 46, y + 8, 30, 18)
    d.rounded_rectangle([x + w - 56, y + 6, x + w - 6, y + 26], radius=3,
                        fill=RED)
    d.text((x + w - 52, y + 9), "109–0", font=SANS_B(11), fill=(255, 255, 255))


def art_market(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 64, 40))
    d.text((x + 8, y + 4), "ANT  NASDAQ", font=SANS_B(11), fill=(255, 255, 255))
    d.text((x + w - 62, y + 4), "IPO $83", font=SANS_B(11), fill=(255, 220, 100))
    pts = [(x + 10, y + 52), (x + 45, y + 44), (x + 80, y + 48),
           (x + 115, y + 30), (x + 150, y + 34), (x + 182, y + 14)]
    d.line(pts, fill=(120, 220, 120), width=3, joint="curve")
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 220, 100))
    for i, bh in enumerate((10, 16, 12, 22, 18, 28)):
        bx = x + 12 + i * 28
        d.rectangle([bx, y + h - 4 - bh, bx + 12, y + h - 4],
                    fill=(60, 160, 90))


def art_games(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 20, 90))
    for i, bh in enumerate((22, 34, 26, 40, 30)):
        bx = x + 8 + i * 36
        d.rectangle([bx, y + h - 18 - bh, bx + 24, y + h - 18],
                    fill=(120, 60, 160), outline=(255, 120, 200), width=1)
        for wy in range(2):
            d.rectangle([bx + 4, y + h - 14 - bh + wy * 8, bx + 9,
                         y + h - 10 - bh + wy * 8], fill=(255, 220, 100))
    d.ellipse([x + w - 58, y + 6, x + w - 22, y + 42], fill=(255, 150, 60))
    d.text((x + w - 56, y + 12), "VI", font=SANS_B(16), fill=(255, 255, 255))
    # controller
    d.rounded_rectangle([x + 8, y + h - 16, x + 62, y + h - 2], radius=6,
                        fill=(240, 240, 240), outline=INK, width=1)
    d.ellipse([x + 16, y + h - 13, x + 24, y + h - 5], fill=(60, 20, 90))
    d.ellipse([x + 44, y + h - 13, x + 52, y + h - 5], fill=(176, 30, 36))


def art_strike(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 235, 200))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 140, 90))
    for i in range(7):
        cx = x + 14 + i * (w - 28) // 6
        d.ellipse([cx - 7, y + 18, cx + 7, y + 32], fill=(235, 200, 170),
                  outline=INK, width=1)
        d.polygon([(cx - 9, y + 32), (cx + 9, y + 32), (cx + 7, y + h - 26),
                   (cx - 7, y + h - 26)],
                  fill=((176, 30, 36), (31, 78, 121), (46, 125, 50))[i % 3])
    d.rectangle([x + 30, y + 2, x + w - 30, y + 14], fill=(255, 255, 255),
                outline=INK, width=1)
    d.text((x + 36, y + 3), "PARO NACIONAL", font=SANS_B(9), fill=INK)


def art_runner(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    d.line([x, y + h - 14, x + w, y + h - 14], fill=(176, 30, 36), width=3)
    # runner: head, torso, limbs
    cx, cy = x + 70, y + 30
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(235, 200, 170),
              outline=INK, width=1)
    d.line([cx, cy + 8, cx + 6, cy + 26], fill=INK, width=4)
    d.line([cx, cy + 12, cx - 14, cy + 4], fill=INK, width=3)
    d.line([cx, cy + 12, cx + 16, cy + 18], fill=INK, width=3)
    d.line([cx + 6, cy + 26, cx - 8, cy + 44], fill=INK, width=3)
    d.line([cx + 6, cy + 26, cx + 20, cy + 40], fill=INK, width=3)
    d.rectangle([x + 120, y + 8, x + w - 8, y + 30], fill=RED)
    d.text((x + 124, y + 11), "BANNED", font=SANS_B(12), fill=(255, 255, 255))


def art_jobs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 40, 90))
    d.text((x + 8, y + 4), "4.9%", font=SANS_B(20), fill=(255, 220, 100))
    for i in range(5):
        cx = x + 100 + i * 17
        d.ellipse([cx - 5, y + 22, cx + 5, y + 32], fill=(235, 200, 170))
        d.polygon([(cx - 7, y + 33), (cx + 7, y + 33), (cx + 6, y + 50),
                   (cx - 6, y + 50)], fill=(200, 200, 200))
    d.line([(x + 10, y + 56), (x + 60, y + 48), (x + 110, y + 52),
            (x + 170, y + 40)], fill=(255, 100, 100), width=3)


# ---------------------------------------------------------------- map
def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=1)
    lon0, lon1, lat0, lat1 = -170.0, 190.0, -56.0, 83.0

    def proj(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat1 - lat) / (lat1 - lat0) * h
        return px, py

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(150, 120, 70))
    for lon, lat, rx, ry in ISLANDS:
        cx, cy = proj(lon, lat)
        sx = rx / (lon1 - lon0) * w
        sy = ry / (lat1 - lat0) * h
        d.ellipse([cx - sx, cy - sy, cx + sx, cy + sy], fill=LAND,
                  outline=(150, 120, 70))
    for num, lon, lat, grey in MAP_DOTS:
        cx, cy = proj(lon, lat)
        col = (110, 110, 110) if grey else RED
        r = 9
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col,
                  outline=(255, 255, 255), width=2)
        fs = SANS_B(10 if num < 10 else 8)
        tw = d.textlength(str(num), font=fs)
        d.text((cx - tw / 2, cy - 7 if num < 10 else cy - 6), str(num),
               font=fs, fill=(255, 255, 255))


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([2, 2, W - 3, H - 3], outline=INK, width=3)

    # --- masthead bar
    d.text((14, 8), "THE WORLD IN ONE DAY", font=SANS_B(16), fill=RED)
    right = "THURSDAY'S NEWS · ONE PAGE · 36 STORIES"
    d.text((W - 14 - d.textlength(right, font=SANS_R(11)), 11), right,
           font=SANS_R(11), fill=INK)
    d.line([14, 28, W - 14, 28], fill=INK, width=2)

    # --- date
    date_font = SERIF_B(62)
    date = "Thursday 19 November 2026"
    dw = d.textlength(date, font=date_font)
    while dw > W - 28:
        date_font = SERIF_B(date_font.size - 1)
        dw = d.textlength(date, font=date_font)
    d.text(((W - dw) / 2, 32), date, font=date_font, fill=INK)

    # --- subtitle
    sub = ("Trump, Xi and Putin share one table · World Court finds genocide "
           "in Myanmar · COP31's draft drops fossil fuels")
    sf = SERIF_I(19)
    sw = d.textlength(sub, font=sf)
    while sw > W - 28:
        sf = SERIF_I(sf.size - 1)
        sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 100), sub, font=sf, fill=RED)
    d.line([14, 124, W - 14, 124], fill=RED, width=2)

    # --- region strip (y 130-188)
    regions = [
        ("ASIA-PACIFIC 11", BROWN, "3", "leaders, one table"),
        ("EUROPE 7", BLUE, "9–6", "World Court vote"),
        ("AMERICAS 8", PURPLE, "$81.3bn", "record IPO"),
        ("MIDDLE EAST 2", DARKRED, "04:42", "Riyadh sirens"),
        ("AFRICA 2", GREEN, "3 yrs", "marathon ban"),
        ("OCEANIA 2", TEAL, "4.9%", "jobless rate"),
        ("WORLDWIDE 4", GREY, "13 yrs", "GTA VI wait"),
    ]
    rx, rw, gap = 14, 140, 2
    for name, col, big, line in regions:
        d.rectangle([rx, 130, rx + rw, 152], fill=col)
        tw = d.textlength(name, font=SANS_B(10))
        d.text((rx + (rw - tw) / 2, 135), name, font=SANS_B(10),
               fill=(255, 255, 255))
        bw = d.textlength(big, font=SANS_B(22))
        d.text((rx + (rw - bw) / 2, 154), big, font=SANS_B(22), fill=INK)
        lw = d.textlength(line, font=SANS_R(11))
        d.text((rx + (rw - lw) / 2, 180), line, font=SANS_R(11), fill=INK)
        d.rectangle([rx, 130, rx + rw, 192], outline=INK, width=1)
        rx += rw + gap
    # counts: 11+7+8+2+2+2+4 = 36

    # --- 3 lead cards (y 198-468)
    leads = [
        ("1  SHENZHEN · SUMMIT", art_summit,
         "Trump, Xi and Putin hold first three-way summit",
         "The three leaders met beside the APEC summit, with nuclear arms, "
         "Iran and trade on the agenda. A joint statement followed. — Reuters"),
        ("2  THE HAGUE · JUSTICE", art_court,
         "World Court: Myanmar committed genocide",
         "By 9 votes to 6 the ICJ found Myanmar guilty of genocide against "
         "the Rohingya and ordered reparations. — Al Jazeera"),
        ("3  ANTALYA · CLIMATE", art_climate,
         "COP31 draft drops fossil fuels and $120bn aid goal",
         "The slimmer text has no figure for adaptation aid. Talks are due "
         "to end on Friday. — Reuters · AFP"),
    ]
    lx, lw, lgap = 14, 322, 15
    for tag, art, head, deck in leads:
        d.rectangle([lx, 198, lx + lw, 468], fill=CARD_BG, outline=INK, width=1)
        art(d, lx + 1, 199, lw - 2, 138)
        d.text((lx + 8, 342), tag, font=SANS_B(11), fill=RED)
        hl = fit_lines(d, head, SERIF_B(25), lw - 16, 2)
        text_lines(d, lx + 8, 360, hl, SERIF_B(25), INK, leading=28)
        dl = fit_lines(d, deck, SERIF_R(13), lw - 16, 3)
        text_lines(d, lx + 8, 360 + len(hl) * 28 + 4, dl, SERIF_R(13), INK,
                   leading=16)
        lx += lw + lgap

    # --- 10-card grid (y 474-758): 5 cols x 2 rows
    cards = [
        ("4  KERCH · WAR", art_bridge,
         "Crimea bridge hit for third time this week",
         "Rail section targeted overnight; traffic halted. — AP"),
        ("5  RIYADH · GULF", art_riyadh,
         "Saudis shoot down Houthi missiles",
         "Sirens at 04:42; debris fell, no casualties. — Reuters"),
        ("6  ODISHA · STORM", art_cyclone,
         "Cyclone Akvan nears India's coast",
         "Over 200,000 listed for evacuation before Friday's landfall. — IMD"),
        ("7  SEOUL · JUSTICE", art_gavel,
         "Korea's top court clears ex-PM Han",
         "Han Duck-soo's martial law conviction is overturned. — AP"),
        ("8  GREENLAND · SECURITY", art_greenland,
         "Denmark backs Arctic pact with US",
         "Parliament approves the Greenland security deal 109–0. — AP"),
        ("9  NEW YORK · MARKETS", art_market,
         "Anthropic starts trading on Nasdaq",
         "Its record $81.3bn share sale was priced at $83. — AP"),
        ("10  WORLDWIDE · GAMES", art_games,
         "GTA VI goes on sale after 13 years",
         "The midnight launch draws rave reviews. — ABC"),
        ("11  BOGOTÁ · LABOUR", art_strike,
         "Colombia's unions hold national strike",
         "Marches in three cities against an economic rescue bill. — AFP"),
        ("12  NAIROBI · SPORT", art_runner,
         "Marathon champion banned for doping",
         "Kenya's Peres Jepchirchir gets three years. — ABC"),
        ("13  CANBERRA · ECONOMY", art_jobs,
         "Australia's jobless rate hits 4.9%",
         "Highest since 2024; shares and the dollar slide. — ABC"),
    ]
    cw, ch, cgap = 192, 138, 8
    for i, (tag, art, head, deck) in enumerate(cards):
        cx = 14 + (i % 5) * (cw + cgap)
        cy = 474 + (i // 5) * (ch + 8)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD_BG, outline=INK,
                    width=1)
        art(d, cx + 1, cy + 1, cw - 2, 58)
        d.text((cx + 6, cy + 62), tag, font=SANS_B(9), fill=RED)
        hl = fit_lines(d, head, SERIF_B(15), cw - 12, 2)
        text_lines(d, cx + 6, cy + 76, hl, SERIF_B(15), INK, leading=17)
        dl = fit_lines(d, deck, SERIF_R(11), cw - 12, 2)
        text_lines(d, cx + 6, cy + 76 + len(hl) * 17 + 2, dl, SERIF_R(11),
                   INK, leading=13)

    # --- bottom band (y 764-958)
    d.line([14, 764, W - 14, 764], fill=INK, width=1)
    d.text((14, 768), "WHERE IT HAPPENED", font=SANS_B(14), fill=RED)
    d.text((446, 768), "ALSO ON THURSDAY 19 NOVEMBER", font=SANS_B(14),
           fill=RED)
    draw_map(d, 14, 788, 420, 142)
    d.text((14, 934), "Red numbers mark stories 1–13. Grey 10 = worldwide "
           "launch.", font=SANS_R(10), fill=INK)
    d.text((14, 946), "Positions are approximate.", font=SANS_R(10), fill=INK)

    also = [
        "IAEA: N. Korea grew uranium work",
        "Nvidia fades 2.9% post-earnings",
        "Bitcoin slides to about $62,600",
        "Dollar high; gold, metals rout",
        "Alcaraz into ATP semis; Tiafoe wins",
        "Zverev powers into ATP last four",
        "US Democrats fill COP31 halls",
        "India demands climate justice",
        "Pacific shapes COP31 ocean pact",
        "Ethiopia–Eritrea clashes grow",
        "Russian plane crash kills all 19",
        "Myanmar chief rethinks ASEAN",
        "Trump, Marcos hail alliance",
        "India police kill Kashmir rebel",
        "Imran Khan seeks urgent care",
        "Islam largest faith by 2035 — Pew",
        "NASA sets CRS-25 launch cover",
        "Israel says Gaza tank raid is over",
        "Pochettino arrives at Man United",
        "Sri Lanka budget keeps debt path",
        "Florida floods shut schools again",
        "F1 hits Vegas with titles settled",
        "Brunson fires 31 in Knicks win",
    ]
    col_w = 282
    for i, item in enumerate(also):
        col = i // 12
        row = i % 12
        ax = 446 + col * col_w
        ay = 790 + row * 14
        d.ellipse([ax, ay + 4, ax + 6, ay + 10], fill=RED)
        d.text((ax + 10, ay), item, font=SANS_R(11), fill=INK)

    # --- footer (y 964-1016)
    d.rectangle([14, 964, W - 14, 1002], outline=RED, width=2)
    foot = ("DATE CHECK ✓  Every story on this page happened, or was first "
            "reported, on Thursday 19 November 2026.  LEFT OUT AS OTHER "
            "DAYS' NEWS: EU's €45bn Ukraine loan plan (18 Nov) · Iran fires "
            "on Kuwait and Bahrain (18 Nov) · Jeffries named for US Speaker "
            "(Wed 18) · Voyager 1 one light-day out (Wed 18) · Van Gogh sold "
            "for $190.4m (Wed 18).")
    fl = fit_lines(d, foot, SANS_R(11), W - 40, 3)
    text_lines(d, 22, 968, fl, SANS_R(11), INK, leading=13)
    src = ("Sources: Reuters, AP, AFP, BBC, Al Jazeera, Xinhua, Yonhap, ABC, "
           "RNZ, IMD, ICJ, Nature · Pictures and map: original, drawn in "
           "code · 2026-11-19")
    d.text((14, 1006), src, font=SANS_R(10), fill=INK)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    build()
