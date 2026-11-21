#!/usr/bin/env python3
"""Paint the picture for the news-image-20261120 bounty.

The design is a picture-editor front page for Friday 20 November
2026, not a dense board of small rows: one dominant hero visual
(the scales of justice over a globe) under one huge headline, one
summit band, one market strip and a thin ticker.  Everything is
drawn with fixed coordinates from Pillow primitives, so the output
is deterministic: two runs produce byte-identical PNG files.

Stories shown (reported Friday 20 November 2026; Just Security
Early Edition, One Turn and Augerton digests, Garuda TV):
  hero    World Court (ICJ) rules Myanmar committed genocide
          against the Rohingya, 9-6, first such finding against
          a state.
  band    Trump, Xi and Putin hold their first three-way summit
          in Shenzhen, at APEC.
  strip   Markets plunge on an AI sell-off (S&P 500 -2 percent,
          Nikkei -4.8 percent) while Anthropic closes +17 percent
          on its Nasdaq debut.
  ticker  Kyiv bridges hit, 8 dead - Riyadh tower struck -
          Kenya Ebola-free - GTA VI tops $2.3bn.
"""

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

PAPER = (247, 243, 234)
INK = (18, 22, 30)
MUTE = (96, 100, 108)
GOLD = (176, 128, 24)
GOLD_DARK = (128, 92, 16)
GLOBE = (33, 58, 86)
GLOBE_LINE = (96, 138, 178)
RED = (178, 34, 44)
GREEN = (24, 122, 66)
BAND = (24, 30, 44)
WHITE = (250, 250, 248)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, size, max_width, min_size=14):
    """Largest font at or below size whose text fits max_width."""
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(path, min_size)


def centred(draw, cx, y, text, f, fill):
    draw.text((cx - draw.textlength(text, font=f) / 2, y), text, font=f, fill=fill)


def globe(draw, cx, cy, r):
    """A lat/long wireframe globe in deep blue with a gold rim."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GLOBE, outline=GOLD, width=5)
    # meridians
    for frac in (0.28, 0.58, 0.86):
        w = r * frac
        draw.ellipse([cx - w, cy - r, cx + w, cy + r], outline=GLOBE_LINE, width=3)
    draw.line([cx, cy - r, cx, cy + r], fill=GLOBE_LINE, width=3)
    # parallels
    for frac in (-0.55, -0.28, 0.0, 0.28, 0.55):
        y = cy + r * frac
        half = r * (1 - frac * frac) ** 0.5
        w = r * 0.32 * (1 - abs(frac))
        draw.ellipse([cx - half, y - w, cx + half, y + w], outline=GLOBE_LINE, width=3)


def scales(draw, cx, top, gold=GOLD):
    """Scales of justice, centred at cx, beam near the top."""
    beam_y = top + 34
    base_y = top + 252
    half = 148
    # post and finial
    draw.line([cx, beam_y, cx, base_y], fill=gold, width=11)
    draw.ellipse([cx - 11, top - 2, cx + 11, top + 20], fill=gold)
    draw.line([cx - 34, base_y, cx + 34, base_y], fill=gold, width=11)
    # beam
    draw.line([cx - half, beam_y, cx + half, beam_y], fill=gold, width=9)
    # chains and pans
    for sx in (cx - half, cx + half):
        pan_y = beam_y + 92
        draw.line([sx, beam_y, sx - 42, pan_y], fill=gold, width=5)
        draw.line([sx, beam_y, sx + 42, pan_y], fill=gold, width=5)
        draw.line([sx, beam_y, sx, pan_y - 6], fill=gold, width=5)
        draw.pieslice([sx - 58, pan_y - 16, sx + 58, pan_y + 40],
                      start=0, end=180, fill=gold)
        draw.rectangle([sx - 58, pan_y - 18, sx + 58, pan_y - 12], fill=gold)


def flag_plate(draw, x, y, w, h, kind):
    """A small simplified flag plate."""
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    if kind == "us":
        for i in range(5):
            yy = y + i * h // 5
            draw.rectangle([x, yy, x + w, yy + h // 5],
                           fill=(178, 34, 52) if i % 2 == 0 else WHITE)
        draw.rectangle([x, y, x + w * 2 // 5, y + h * 3 // 5], fill=(38, 48, 110))
    elif kind == "cn":
        draw.rectangle([x, y, x + w, y + h], fill=(196, 30, 42))
        for dx, dy, r in ((12, 10, 5), (26, 6, 3), (30, 14, 3), (28, 23, 3), (22, 29, 3)):
            draw.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r],
                         fill=(250, 205, 40))
    else:  # ru
        draw.rectangle([x, y, x + w, y + h // 3], fill=WHITE)
        draw.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(30, 64, 160))
        draw.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(196, 30, 42))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead -------------------------------------------------
    draw.text((36, 22), "THE DAY IN ONE IMAGE", font=font(SANS_BOLD, 30), fill=INK)
    right = "FRI 20 NOV 2026"
    f_right = font(SANS, 24)
    draw.text((W - 36 - draw.textlength(right, font=f_right), 26),
              right, font=f_right, fill=MUTE)
    draw.line([36, 68, W - 36, 68], fill=INK, width=3)

    # ---- hero visual ----------------------------------------------
    globe(draw, 512, 272, 168)
    scales(draw, 512, 128)

    # ---- headline ---------------------------------------------------
    y = 452
    for line, size in (("WORLD COURT:", 96),
                       ("MYANMAR COMMITTED", 82),
                       ("GENOCIDE", 96)):
        f = fit(draw, line, SERIF_BOLD, size, W - 60)
        centred(draw, 512, y, line, f, INK)
        y += int(size * 1.04)
    sub = "ICJ rules 9\u20136 \u2014 first genocide finding ever made against a state"
    centred(draw, 512, y + 2, sub, fit(draw, sub, SANS, 29, W - 72), MUTE)

    # ---- summit band --------------------------------------------------
    band_y = 742
    draw.rectangle([0, band_y, W, band_y + 104], fill=BAND)
    fx = 36
    for kind in ("us", "cn", "ru"):
        flag_plate(draw, fx, band_y + 22, 88, 60, kind)
        fx += 104
    tx = fx + 14
    draw.text((tx, band_y + 14), "TRUMP \u00b7 XI \u00b7 PUTIN",
              font=fit(draw, "TRUMP \u00b7 XI \u00b7 PUTIN", SANS_BOLD, 40, W - tx - 30),
              fill=WHITE)
    draw.text((tx, band_y + 62), "FIRST THREE-WAY SUMMIT \u2014 SHENZHEN",
              font=fit(draw, "FIRST THREE-WAY SUMMIT \u2014 SHENZHEN", SANS, 25, W - tx - 30),
              fill=(196, 204, 218))

    # ---- market strip ---------------------------------------------------
    strip_y = 862
    # plunging chart, left
    pts = [(36, strip_y + 8), (86, strip_y + 16), (128, strip_y + 12),
           (172, strip_y + 34), (214, strip_y + 30), (258, strip_y + 58),
           (306, strip_y + 66)]
    draw.line(pts, fill=RED, width=6, joint="curve")
    lx, ly = pts[-1]
    draw.polygon([(lx, ly), (lx - 16, ly - 4), (lx - 4, ly - 16)], fill=RED)
    draw.text((356, strip_y + 2), "MARKETS PLUNGE",
              font=font(SANS_BOLD, 38), fill=RED)
    draw.text((356, strip_y + 46), "AI sell-off: S&P \u22122% \u00b7 Nikkei \u22124.8%",
              font=font(SANS, 24), fill=INK)
    chip = "ANTHROPIC +17% ON DEBUT"
    f_chip = fit(draw, chip, SANS_BOLD, 22, 250)
    cw = draw.textlength(chip, font=f_chip) + 24
    chip_x = 356 + draw.textlength("MARKETS PLUNGE", font=font(SANS_BOLD, 38)) + 18
    draw.rounded_rectangle([chip_x, strip_y + 6, chip_x + cw, strip_y + 42],
                           radius=9, fill=GREEN)
    draw.text((chip_x + 12, strip_y + 13), chip, font=f_chip, fill=WHITE)

    # ---- ticker ----------------------------------------------------------
    tick_y = 962
    draw.rectangle([0, tick_y, W, H], fill=INK)
    ticker = ("KYIV BRIDGES HIT \u00b7 8 DEAD \u2014 RIYADH TOWER STRUCK \u2014 "
              "KENYA EBOLA-FREE \u2014 GTA VI $2.3BN")
    centred(draw, 512, tick_y + 18, ticker,
            fit(draw, ticker, SANS_BOLD, 25, W - 48), (240, 236, 224))

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
