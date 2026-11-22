#!/usr/bin/env python3
"""The picture that tastes of one ingredient.

A close-up bowl of steaming ramen built around ONE perfect soft egg:
glistening runny yolk, glossy broth, wavy noodles, warm light.
Pure Python 3 stdlib, no network. Writes /output/entry.png (1024x1024).
"""
import math
import os
import struct
import zlib

W = H = 1024
buf = bytearray(W * H * 3)


def lerp(a, b, t):
    return a + (b - a) * t


def blend(x, y, r, g, b, a):
    """Blend colour (r,g,b) with alpha a (0..1) onto pixel (x,y)."""
    if x < 0 or x >= W or y < 0 or y >= H or a <= 0:
        return
    i = (y * W + x) * 3
    if a >= 1:
        buf[i] = r
        buf[i + 1] = g
        buf[i + 2] = b
        return
    ia = 1 - a
    buf[i] = int(buf[i] * ia + r * a)
    buf[i + 1] = int(buf[i + 1] * ia + g * a)
    buf[i + 2] = int(buf[i + 2] * ia + b * a)


def hrect(y0, y1, c0, c1):
    """Fill rows y0..y1 with a vertical gradient between c0 and c1."""
    n = max(1, y1 - y0)
    for y in range(max(0, y0), min(H, y1)):
        t = (y - y0) / n
        r = int(lerp(c0[0], c1[0], t))
        g = int(lerp(c0[1], c1[1], t))
        b = int(lerp(c0[2], c1[2], t))
        i = (y * W) * 3
        row = bytes((r, g, b)) * W
        buf[i:i + W * 3] = row


def disc(cx, cy, r, col, a=1.0):
    r2 = r * r
    y0 = max(0, int(cy - r))
    y1 = min(H - 1, int(cy + r) + 1)
    for y in range(y0, y1 + 1):
        dy = y - cy
        dx = int(math.sqrt(max(0, r2 - dy * dy)))
        x0 = max(0, int(cx - dx))
        x1 = min(W - 1, int(cx + dx))
        i = (y * W + x0) * 3
        for x in range(x0, x1 + 1):
            blend(x, y, col[0], col[1], col[2], a)


def ellipse(cx, cy, rx, ry, col, a=1.0):
    y0 = max(0, int(cy - ry))
    y1 = min(H - 1, int(cy + ry) + 1)
    for y in range(y0, y1 + 1):
        dy = (y - cy) / ry
        dx = rx * math.sqrt(max(0.0, 1 - dy * dy))
        x0 = max(0, int(cx - dx))
        x1 = min(W - 1, int(cx + dx))
        for x in range(x0, x1 + 1):
            blend(x, y, col[0], col[1], col[2], a)


def ring(cx, cy, rx, ry, thick, col, a=1.0):
    """Elliptical ring outline, drawn as a stroked ellipse."""
    ellipse(cx, cy, rx, ry, col, a)
    ellipse(cx, cy, rx - thick, ry - thick * ry / rx, (222, 138, 42), a)


def poly(points, col, a=1.0):
    """Scanline fill of a simple polygon."""
    if len(points) < 3:
        return
    ys = [p[1] for p in points]
    y0 = max(0, int(min(ys)))
    y1 = min(H - 1, int(max(ys)) + 1)
    n = len(points)
    for y in range(y0, y1 + 1):
        xs = []
        for k in range(n):
            x1, y1p = points[k]
            x2, y2p = points[(k + 1) % n]
            if (y1p <= y < y2p) or (y2p <= y < y1p):
                t = (y - y1p) / (y2p - y1p)
                xs.append(x1 + t * (x2 - x1))
        xs.sort()
        for j in range(0, len(xs) - 1, 2):
            x0 = max(0, int(xs[j]))
            x1 = min(W - 1, int(xs[j + 1]))
            for x in range(x0, x1 + 1):
                blend(x, y, col[0], col[1], col[2], a)


def thick_line(x0, y0, x1, y1, w, col, a=1.0):
    d = math.hypot(x1 - x0, y1 - y0)
    steps = max(2, int(d / max(2.0, w * 0.45)))
    for s in range(steps + 1):
        t = s / steps
        disc(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, w / 2, col, a)


def bezier(p0, p1, p2, w, col, a=1.0, steps=40):
    px, py = p0
    for s in range(1, steps + 1):
        t = s / steps
        mt = 1 - t
        x = mt * mt * p0[0] + 2 * mt * t * p1[0] + t * t * p2[0]
        y = mt * mt * p0[1] + 2 * mt * t * p1[1] + t * t * p2[1]
        thick_line(px, py, x, y, w, col, a)
        px, py = x, y


def wavy(x0, x1, ybase, amp, waves, w, col, a=1.0):
    """A horizontal wavy noodle strand."""
    px, py = x0, ybase
    steps = 60
    for s in range(1, steps + 1):
        t = s / steps
        x = x0 + (x1 - x0) * t
        y = ybase + amp * math.sin(t * waves * math.pi * 2)
        thick_line(px, py, x, y, w, col, a)
        px, py = x, y


# ---------------------------------------------------------------- background
# Warm cream backdrop fading to amber, then a dark wooden table.
hrect(0, 560, (250, 226, 176), (238, 183, 110))
hrect(560, H, (122, 74, 40), (74, 44, 24))
# Soft warm light glow behind the bowl.
for rr, aa in ((430, 0.10), (340, 0.12), (250, 0.14)):
    disc(512, 520, rr, (255, 214, 140), aa)
# Table grain: a few soft dark streaks.
for gy, gw in ((700, 5), (790, 4), (880, 6), (960, 4)):
    thick_line(0, gy, W, gy + 18, gw, (60, 35, 18), 0.25)

# ------------------------------------------------------------------- steam
# Three rising columns of translucent steam, drawn before the bowl rim
# so the lowest wisps sit behind the toppings.
for cx0, phase in ((380, 0.0), (512, 1.3), (650, 2.6)):
    for s in range(46):
        t = s / 45
        y = 500 - t * 330
        x = cx0 + math.sin(t * 5.2 + phase) * (14 + t * 30)
        r = 16 + t * 26
        disc(x, y, r, (255, 250, 240), 0.055)

# -------------------------------------------------------------------- bowl
# Bowl body: deep lacquered bowl, wide and low, centred low in frame.
ellipse(512, 660, 392, 300, (28, 20, 18))
ellipse(512, 640, 392, 285, (52, 30, 26))
# Red lacquer band around the bowl.
ellipse(512, 700, 392, 262, (158, 32, 22))
ellipse(512, 690, 392, 250, (52, 30, 26))
# Bowl foot shadow on the table.
ellipse(512, 940, 330, 42, (40, 22, 12), 0.55)
# Rim: pale ceramic ring with a warm light catch on its upper edge.
ellipse(512, 560, 380, 148, (245, 232, 210))
bezier((180, 500), (380, 430), (620, 432), 10, (255, 246, 222), 0.8)
ellipse(512, 560, 356, 132, (222, 138, 42))  # broth surface
# Broth shading: darker at the far edge, glossy pool near the front.
ellipse(512, 540, 330, 108, (196, 116, 30), 0.55)
ellipse(512, 600, 300, 92, (242, 178, 80), 0.5)
# Chilli-oil sheen: glossy orange-red swirls on the broth.
for cx, cy, rx in ((330, 520, 90), (700, 540, 80), (560, 500, 60)):
    ellipse(cx, cy, rx, rx * 0.32, (214, 84, 20), 0.35)
# Broth highlight arc (light from upper left).
bezier((250, 520), (380, 470), (560, 478), 14, (255, 214, 130), 0.5)

# ------------------------------------------------------------------ noodles
NOODLE_COLS = [(245, 201, 92), (238, 182, 62), (250, 220, 122), (232, 172, 52)]
strands = [
    (210, 540, 26, 2.2, 0), (230, 570, 22, 2.6, 1), (260, 600, 20, 2.0, 2),
    (300, 620, 18, 2.4, 3), (420, 630, 20, 2.2, 0), (520, 635, 18, 2.6, 1),
    (600, 620, 22, 2.0, 2), (660, 600, 18, 2.4, 3), (700, 570, 20, 2.2, 0),
    (250, 520, 24, 2.8, 1), (480, 545, 16, 2.4, 2), (640, 545, 16, 2.6, 3),
]
for i, (x0, yb, amp, wv, ci) in enumerate(strands):
    x1 = min(x0 + 190 + (i % 3) * 30, 830)  # keep noodles inside the broth
    wavy(x0, x1, yb, amp, wv, 15, NOODLE_COLS[ci % 4])
    wavy(x0, x1, yb - 4, amp, wv, 5, (255, 232, 150), 0.7)

# ------------------------------------------------------- toppings: chashu
# Two overlapping slices of glistening chashu pork, left side.
for cx, cy, r in ((330, 585, 92), (430, 610, 78)):
    disc(cx, cy, r, (226, 158, 132))
    disc(cx, cy, r - 14, (198, 110, 84))
    disc(cx, cy, r - 34, (232, 168, 140))
    disc(cx, cy, r - 52, (196, 104, 78))
    disc(cx - r * 0.35, cy - r * 0.4, r * 0.28, (255, 214, 186), 0.55)
# Narutomaki fish cake, right side: white disc, pink spiral.
disc(730, 590, 62, (250, 244, 232))
for rr in range(52, 6, -8):
    disc(730, 590, rr, (238, 120, 140), 0.85)
    disc(730, 590, rr - 4, (250, 244, 232), 0.85)
disc(730, 590, 8, (238, 120, 140))

# ------------------------------------------------- hero: the soft egg (x2)
# Two big halved eggs, front and centre — the one ingredient.
def egg(cx, cy, rx, ry, yolk_r):
    # White, slightly glossy, with a soft shadow edge.
    ellipse(cx, cy, rx, ry, (232, 214, 188), 0.9)
    ellipse(cx, cy, rx, ry, (253, 246, 233))
    ellipse(cx, cy, rx - 10, ry - 8, (250, 240, 222))
    # Yolk: deep orange rim to glowing amber centre.
    for rr, col in ((yolk_r, (224, 110, 0)), (yolk_r - 8, (240, 140, 10)),
                    (yolk_r - 20, (248, 168, 20)), (yolk_r - 34, (255, 196, 60))):
        disc(cx, cy, rr, col)
    disc(cx, cy, yolk_r - 48, (255, 214, 90))
    # Gloss highlight on the yolk + a runny drip.
    ellipse(cx - yolk_r * 0.32, cy - yolk_r * 0.42, yolk_r * 0.30, yolk_r * 0.16,
            (255, 240, 180), 0.85)
    disc(cx + yolk_r * 0.15, cy + ry - 6, 16, (255, 190, 40))
    ellipse(cx + yolk_r * 0.15, cy + ry + 12, 12, 20, (255, 190, 40))

egg(470, 640, 148, 108, 74)
egg(660, 665, 132, 96, 64)

# ------------------------------------------------------------- garnish
# Spring-onion rings scattered over broth and noodles.
for cx, cy, r in ((300, 500, 12), (380, 505, 10), (600, 500, 11), (700, 505, 10),
                  (250, 560, 9), (780, 560, 11), (520, 490, 9), (440, 495, 10)):
    disc(cx, cy, r, (46, 130, 62))
    disc(cx, cy, r - 4, (140, 205, 90))
    disc(cx, cy, r - 7, (30, 90, 45))
# Sesame seeds.
for cx, cy in ((350, 640), (560, 640), (740, 640), (420, 560), (640, 610),
               (300, 610), (780, 610), (500, 610)):
    ellipse(cx, cy, 7, 4, (255, 240, 205), 0.95)
# Chilli flakes.
for cx, cy in ((330, 530), (590, 530), (720, 530), (460, 580)):
    disc(cx, cy, 5, (178, 40, 16), 0.9)

# -------------------------------------------------------------- chopsticks
# Resting across the bowl's top-right rim, lifting one noodle strand.
poly([(700, 330), (716, 336), (560, 560), (548, 552)], (96, 58, 30))
poly([(724, 352), (740, 360), (590, 572), (578, 564)], (120, 74, 38))
# Noodle strand lifted by the chopsticks, dripping gloss.
bezier((560, 555), (620, 470), (690, 380), 13, (245, 201, 92))
bezier((560, 555), (620, 470), (690, 380), 5, (255, 232, 150), 0.8)
disc(690, 380, 10, (255, 200, 60))

# ------------------------------------------------------------ front steam
# A few fresh wisps in front of the bowl for depth.
for cx0, phase in ((430, 0.7), (600, 2.0)):
    for s in range(30):
        t = s / 29
        y = 470 - t * 260
        x = cx0 + math.sin(t * 4.6 + phase) * (12 + t * 24)
        disc(x, y, 12 + t * 20, (255, 250, 240), 0.045)

# ------------------------------------------------------------- vignette
# Soft corner shading only — keep it subtle so no hard circles show.
for cx, cy in ((-60, -60), (1084, -60), (-60, 1084), (1084, 1084)):
    disc(cx, cy, 260, (30, 16, 8), 0.10)

# ------------------------------------------------------------------- text
FONT = {
    'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    'G': ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    'I': ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    '-': ["00000", "00000", "00000", "01110", "00000", "00000", "00000"],
    ' ': ["00000"] * 7,
}


def draw_text(text, cx, y, scale, col):
    cw = 6 * scale
    total = len(text) * cw - scale
    x = cx - total // 2
    for ch in text:
        glyph = FONT.get(ch, FONT[' '])
        for gy, row in enumerate(glyph):
            for gx, bit in enumerate(row):
                if bit == '1':
                    for dy in range(scale):
                        for dx in range(scale):
                            blend(x + gx * scale + dx, y + gy * scale + dy,
                                  col[0], col[1], col[2], 1.0)
        x += cw


# Caption band at the bottom: the one ingredient, named for the judge.
poly([(0, 952), (W, 952), (W, H), (0, H)], (28, 18, 12))
draw_text("ONE EGG - STEAMING RAMEN", 512, 972, 4, (255, 214, 140))

# ------------------------------------------------------------------ encode
def write_png(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw.extend(buf[y * W * 3:(y + 1) * W * 3])
    data = zlib.compress(bytes(raw), 6)
    out = bytearray()
    out += b'\x89PNG\r\n\x1a\n'

    def chunk(typ, payload):
        out.extend(struct.pack('>I', len(payload)))
        out.extend(typ)
        out.extend(payload)
        out.extend(struct.pack('>I', zlib.crc32(typ + payload) & 0xFFFFFFFF))

    chunk(b'IHDR', struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0))
    chunk(b'IDAT', data)
    chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(out)
    return len(out)


if __name__ == '__main__':
    n = write_png('/output/entry.png')
    print(f'wrote /output/entry.png {n} bytes, {W}x{H}')
