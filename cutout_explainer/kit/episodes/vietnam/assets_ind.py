import sys, os, math; sys.path.insert(0, os.getcwd())
from episodes.vietnam.assets import *
import random

"""Industry / electronics / logistics props for the Vietnam episode (flat cut-out style, no logos)."""

# ---------------- small helpers ----------------
def _mix(a, b, t): return tuple(lerp(x, y, t) for x, y in zip(a, b))
def _dk(c, k=0.25): return _mix(c, (0, 0, 0), k)
def _lt(c, k=0.3): return _mix(c, (1, 1, 1), k)

STEEL, STEEL_D, STEEL_L = hexc('#8d97a3'), hexc('#5f6a77'), hexc('#b9c2cc')
GOLD, GOLD_D = hexc('#e6b830'), hexc('#b88a1c')
_CONT = [hexc('#c0392b'), hexc('#2e6fb0'), hexc('#e0a82e'), hexc('#3f9a5a'), hexc('#d9732b')]
_APP = [hexc(c) for c in ('#ef5350', '#ffb300', '#43a047', '#29b6f6', '#ab47bc', '#ff7043', '#26c6da', '#ec407a')]


def _clip_rr(ctx, x, y, w, h, r):
    rrect(ctx, x, y, w, h, r); ctx.clip()


# ---------------- factory ----------------
def factory(ctx, x, y, s=1.0, t=0.0, label="FACTORY"):
    """Anchor: bottom-centre. ~520x300 at s=1. Brick wall in 2 tones, sawtooth roof (4 teeth, glazed vertical faces),
    row of windows, roll-up loading door, brick chimney with a slow looping smoke puff (t), plain red sign band."""
    brick, brick_d = hexc('#d9a066'), hexc('#b97f4c')
    roof, roof_d = hexc('#7d8794'), hexc('#5b6470')
    glass, glass_d = hexc('#9fd4e8'), hexc('#6fb0cc')
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    # chimney (behind roof)
    cb = hexc('#a85a43')
    box(ctx, 170, -318, 34, 172, cb, 0, INK, 3)
    box(ctx, 190, -316, 12, 168, _dk(cb, .22))
    for k in range(7): line(ctx, [(171, -300 + k*24), (190, -300 + k*24)], _dk(cb, .3), 1.5)
    box(ctx, 164, -330, 46, 14, _dk(cb, .15), 2, INK, 3)
    for k in range(3):                                   # looping smoke puff
        ph = ((t/4.0) + k/3.0) % 1.0
        px = 187 + ph*55 + math.sin(ph*7 + k*2)*7; py = -340 - ph*120; r = 12 + ph*26
        a = min(1.0, ph*5)*(1 - ph)
        circle(ctx, px, py, r, (0.72, 0.73, 0.78), a=a*.9)
        circle(ctx, px - r*.12, py - r*.14, r*.82, (0.97, 0.97, 0.98), a=a)
    # wall
    box(ctx, -260, -150, 520, 150, brick, 0, INK, 3)
    box(ctx, -260, -22, 520, 22, brick_d, 0, INK, 3)
    box(ctx, 232, -150, 28, 128, brick_d)
    for r_ in range(6):                                  # brick courses hint
        for k in range(26):
            if (k + r_) % 2: continue
            line(ctx, [(-255 + k*20, -118 + r_*16), (-241 + k*20, -118 + r_*16)], _mix(brick, brick_d, .6), 1.5)
    box(ctx, -260, -150, 520, 30, hexc('#c0392b'), 0, INK, 3)                     # sign band
    box(ctx, -260, -126, 520, 6, hexc('#8f2a1f'))
    text(ctx, label, 0, -137, 28, (1, 1, 1))
    # sawtooth roof: 4 teeth, slope tone + glazed vertical face
    for i in range(4):
        x0 = -260 + i*100
        poly(ctx, [(x0, -150), (x0 + 100, -232), (x0 + 100, -150)], roof, INK, 3)
        poly(ctx, [(x0 + 12, -150), (x0 + 100, -232), (x0 + 100, -150)], roof_d)
        for k in range(1, 5):                            # roof ribs
            xx = x0 + k*19; line(ctx, [(xx, -150 - (xx - x0)*0.82 + 2), (xx, -150)], _dk(roof_d, .25), 1.5, .8)
        quad = [(x0 + 78, -214), (x0 + 100, -232), (x0 + 100, -150), (x0 + 78, -150)]
        poly(ctx, quad, glass, INK, 2.5)
        poly(ctx, [(x0 + 90, -222), (x0 + 100, -232), (x0 + 100, -150), (x0 + 90, -150)], glass_d)
        for k in range(1, 4):
            yy = -150 - k*20; line(ctx, [(x0 + 78, yy), (x0 + 100, yy)], INK, 1.5)
        line(ctx, [(x0, -150), (x0 + 100, -232), (x0 + 100, -150)], INK, 3)
    box(ctx, 140, -156, 120, 8, roof_d, 0, INK, 3)                                  # flat roof edge
    # windows
    for k in range(4):
        wx = -238 + k*60
        box(ctx, wx - 4, -108, 56, 56, hexc('#e8dcc4'), 2, INK, 2.5)
        box(ctx, wx, -104, 48, 48, glass, 0, INK, 2)
        poly(ctx, [(wx + 28, -104), (wx + 48, -104), (wx + 48, -90), (wx + 12, -56 + 0), (wx + 0, -56), (wx, -56)], glass_d, a=.0)
        poly(ctx, [(wx + 30, -104), (wx + 48, -104), (wx + 48, -88)], glass_d)
        line(ctx, [(wx + 24, -104), (wx + 24, -56)], INK, 2); line(ctx, [(wx, -80), (wx + 48, -80)], INK, 2)
    box(ctx, 188, -108, 56, 56, hexc('#e8dcc4'), 2, INK, 2.5); box(ctx, 192, -104, 48, 48, glass, 0, INK, 2)
    line(ctx, [(216, -104), (216, -56)], INK, 2); line(ctx, [(192, -80), (240, -80)], INK, 2)
    # roll-up door
    box(ctx, 8, -106, 156, 106, hexc('#4a4f58'), 0, INK, 3)
    ctx.save(); ctx.rectangle(14, -100, 144, 100); ctx.clip()
    box(ctx, 14, -100, 144, 100, hexc('#c9ced6'))
    for k in range(11):
        box(ctx, 14, -100 + k*9.6, 144, 9, hexc('#c9ced6') if k % 2 else hexc('#aeb5bf'), 0, INK, 1.5)
    ctx.restore()
    box(ctx, 76, -14, 20, 8, STEEL_D, 3, INK, 2)
    ctx.restore()


# ---------------- assembly line ----------------
def assembly_line(ctx, x, y, w=900, t=0.0, item=None, gap=170, speed=90):
    """Anchor: x = left end, y = belt TOP. Steel frame + legs, rollers, moving belt stripes (t*speed).
    If item is a function item(ctx, cx, cy) it is called every `gap` px, moving right at `speed` px/s, clipped to the
    belt. cx = item centre-x, cy = belt top (item should treat cy as its BOTTOM; wrap centred props in a lambda)."""
    belt, belt_s = hexc('#2f3238'), hexc('#454a53')
    n = max(2, int(w//170) + 1)
    lxs = [x + 36 + i*(w - 72)/(n - 1) for i in range(n)]
    for lx in lxs:                                       # legs
        box(ctx, lx - 9, y + 58, 18, 104, STEEL, 0, INK, 3); box(ctx, lx + 2, y + 58, 7, 104, STEEL_D)
        box(ctx, lx - 22, y + 158, 44, 9, STEEL_D, 3, INK, 3)
    for a, b in zip(lxs[:-1], lxs[1:]):                  # cross braces
        line(ctx, [(a + 9, y + 70), (b - 9, y + 140)], INK, 5); line(ctx, [(a + 9, y + 70), (b - 9, y + 140)], STEEL_D, 2.5)
    box(ctx, x, y + 30, w, 34, STEEL, 0, INK, 3)         # frame beam
    box(ctx, x, y + 52, w, 12, STEEL_D, 0, INK, 3); box(ctx, x, y + 33, w, 5, STEEL_L)
    for k in range(int(w//30)):                          # rollers peeking under the belt
        circle(ctx, x + 22 + k*30, y + 34, 8, STEEL_L, INK, 2)
        circle(ctx, x + 22 + k*30, y + 34, 2.5, STEEL_D)
    box(ctx, x, y, w, 26, belt, 13, INK, 3)              # belt (pill)
    ctx.save(); _clip_rr(ctx, x, y, w, 26, 13)
    off = (t*speed) % 36
    for k in range(-2, int(w//36) + 3):
        xx = x + k*36 + off
        poly(ctx, [(xx, y), (xx + 14, y), (xx + 4, y + 26), (xx - 10, y + 26)], belt_s)
    ctx.restore()
    line(ctx, [(x + 14, y + 2), (x + w - 14, y + 2)], _lt(belt, .35), 2)
    for hx in (x + 13, x + w - 13):                      # end drums
        circle(ctx, hx, y + 13, 7, STEEL_L, INK, 2.5); circle(ctx, hx, y + 13, 2.5, STEEL_D)
    if item:
        ctx.save(); ctx.rectangle(x, y - 500, w, 500 + 2); ctx.clip()
        off = (t*speed) % gap
        cx = x - gap + off
        while cx < x + w + gap:
            item(ctx, cx, y); cx += gap
        ctx.restore()
        box(ctx, x + 6, y + 0, w - 12, 3, belt, 0, None)


# ---------------- smartphone ----------------
def smartphone(ctx, x, y, s=1.0, rot=0.0, side="front", label=None):
    """Anchor: centre. 120x240 at s=1. Front: rounded black body, thin bezel, punch-hole camera, bright wallpaper
    with a 4x5 grid of coloured app squares + dock. Back: plain colour, square camera bump with 3 lenses; optional
    small plain label centred low."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    if side == "front":
        box(ctx, 59, -60, 4, 34, STEEL_D, 2, INK, 2); box(ctx, 59, -10, 4, 50, STEEL_D, 2, INK, 2)      # side buttons
        box(ctx, -60, -120, 120, 240, hexc('#16181d'), 20, INK, 3)
        ctx.save(); _clip_rr(ctx, -55, -115, 110, 230, 16)
        box(ctx, -55, -115, 110, 230, hexc('#3b6fe0'))
        poly(ctx, [(-55, 20), (55, -30), (55, 115), (-55, 115)], hexc('#8a4fd0'))
        poly(ctx, [(-55, 70), (55, 40), (55, 115), (-55, 115)], hexc('#ff7aa8'))
        circle(ctx, 30, -70, 16, hexc('#ffe27a'))
        ctx.restore()
        for r_ in range(5):
            for c_ in range(4):
                ax, ay = -45 + c_*25, -88 + r_*29
                col = _APP[(r_*4 + c_*3 + r_) % len(_APP)]
                box(ctx, ax, ay, 19, 19, col, 5, INK, 1.8)
                box(ctx, ax + 3, ay + 3, 6, 6, _lt(col, .5), 2)
        box(ctx, -49, 84, 98, 26, (1, 1, 1), 10, None); ctx.set_source_rgba(1, 1, 1, .35)
        for c_ in range(4): box(ctx, -42 + c_*24, 88, 19, 19, _APP[(c_*2 + 1) % len(_APP)], 5, INK, 1.8)
        circle(ctx, 0, -104, 4.5, (0.03, 0.03, 0.05), hexc('#3a3f4b'), 1.5)
        rrect(ctx, -60, -120, 120, 240, 20); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    else:
        c = hexc('#4aa3a0')
        box(ctx, 59, -60, 4, 34, _dk(c), 2, INK, 2); box(ctx, 59, -10, 4, 50, _dk(c), 2, INK, 2)
        box(ctx, -60, -120, 120, 240, c, 20, INK, 3)
        ctx.save(); _clip_rr(ctx, -60, -120, 120, 240, 20)
        box(ctx, 30, -120, 30, 240, _dk(c, .15)); box(ctx, -52, -112, 8, 224, _lt(c, .25))
        ctx.restore()
        rrect(ctx, -60, -120, 120, 240, 20); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
        box(ctx, -48, -108, 58, 58, hexc('#2a2d34'), 12, INK, 2.5)
        box(ctx, -45, -105, 52, 52, hexc('#3a3f4b'), 10)
        for lx, ly in ((-30, -88), (-30 + 0, -68), (-12, -78)):
            pass
        for lx, ly in ((-31, -90), (-31, -68), (-9, -79)):
            circle(ctx, lx, ly, 10, hexc('#14161a'), INK, 2); circle(ctx, lx, ly, 6, hexc('#2d3a66')); circle(ctx, lx - 2, ly - 2, 2, (1, 1, 1))
        circle(ctx, 6, -97, 3.5, hexc('#ffe27a'), INK, 1.5)
        if label: text(ctx, label, 0, 80, 22, (1, 1, 1))
    ctx.restore()


# ---------------- earbuds case ----------------
def earbuds_case(ctx, x, y, s=1.0):
    """Anchor: centre. ~120x150 at s=1. Generic white rounded charging case with open lid (tilted back), inner slot,
    two white stem earbuds standing in it, tiny LED. No logo."""
    W_, WD, WL = (0.97, 0.97, 0.98), hexc('#c9cfd8'), (1, 1, 1)
    ctx.save(); ctx.translate(x, y + 18); ctx.scale(s, s)
    ctx.save(); ctx.translate(0, 0); ctx.rotate(-0.08)                                  # lid, hinged at back
    box(ctx, -58, -100, 116, 90, W_, 24, INK, 3)
    box(ctx, -50, -92, 100, 72, hexc('#aeb6c2'), 18)
    box(ctx, -46, -88, 92, 24, hexc('#c8cfd9'), 12)
    ctx.restore()
    box(ctx, -60, -12, 120, 62, W_, 24, INK, 3)                                         # base back
    ctx.save(); _clip_rr(ctx, -60, -12, 120, 62, 24)
    ctx.restore()
    ellipse(ctx, 0, -6, 52, 12, hexc('#8d95a2'))
    ellipse(ctx, 0, -4, 46, 9, hexc('#5f6672'))
    for ex in (-24, 24):                                                                # earbuds
        d = -1 if ex < 0 else 1
        box(ctx, ex - 6, -50, 12, 56, W_, 6, INK, 2.5)
        box(ctx, ex + 1, -48, 4, 52, WD, 2)
        circle(ctx, ex - d*2, -58, 15, W_, INK, 2.5); circle(ctx, ex - d*2 + d*5, -55, 8, WD)
        circle(ctx, ex - d*2 - d*3, -62, 4, (1, 1, 1))
    ctx.save(); ctx.translate(0, 0)                                                     # front face over bud bottoms
    box(ctx, -60, 0, 120, 50, W_, 22, INK, 3)
    ctx.save(); _clip_rr(ctx, -60, 0, 120, 50, 22)
    box(ctx, 30, 0, 40, 50, WD); box(ctx, -60, 38, 120, 14, WD)
    box(ctx, -52, 6, 10, 28, (1, 1, 1), 4)
    ctx.restore(); rrect(ctx, -60, 0, 120, 50, 22); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    circle(ctx, 0, 26, 4, hexc('#4cd964'), INK, 1.5)
    ctx.restore()
    ctx.restore()


# ---------------- tablet ----------------
def tablet(ctx, x, y, s=1.0, rot=0.0):
    """Anchor: centre. ~260x190 landscape, dark body, bezel, front camera dot, colourful home screen
    (icon grid + big widget)."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    box(ctx, -130, -95, 260, 190, hexc('#262a32'), 16, INK, 3)
    box(ctx, -118, -83, 236, 166, hexc('#0d0f14'), 8)
    ctx.save(); _clip_rr(ctx, -116, -81, 232, 162, 7)
    box(ctx, -116, -81, 232, 162, hexc('#34a8e8'))
    poly(ctx, [(-116, 10), (116, -40), (116, 81), (-116, 81)], hexc('#7a5ae0'))
    poly(ctx, [(-116, 50), (116, 30), (116, 81), (-116, 81)], hexc('#ff8a5c'))
    circle(ctx, 80, -55, 18, hexc('#ffe27a'))
    ctx.restore()
    box(ctx, -100, -66, 90, 50, (1, 1, 1), 8, INK, 2); box(ctx, -92, -58, 50, 8, hexc('#34a8e8'), 3)
    box(ctx, -92, -44, 70, 6, hexc('#c8d3e0'), 3); box(ctx, -92, -32, 40, 6, hexc('#c8d3e0'), 3)
    for r_ in range(3):
        for c_ in range(5):
            ax, ay = -2 + c_*23 - 0, -66 + r_*30
            if c_ > 4: continue
            col = _APP[(r_*5 + c_*2) % len(_APP)]
            box(ctx, ax, ay, 18, 18, col, 5, INK, 1.8); box(ctx, ax + 3, ay + 3, 5, 5, _lt(col, .5), 2)
    for c_ in range(6):
        col = _APP[(c_*3 + 2) % len(_APP)]
        box(ctx, -88 + c_*32, 52, 24, 24, col, 7, INK, 1.8)
    circle(ctx, -124, 0, 3, hexc('#0d0f14'), hexc('#3a3f4b'), 1.5)
    ctx.restore()


# ---------------- smartwatch ----------------
def smartwatch(ctx, x, y, s=1.0):
    """Anchor: centre. Square rounded face (~92x92) showing time digits, orange silicone strap above and below
    with holes, side crown."""
    st, std = hexc('#f07a2a'), hexc('#c25a14')
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for sg in (-1, 1):                                                                   # straps
        y0 = -112 if sg < 0 else 40
        poly(ctx, [(-26, y0 + (0 if sg < 0 else 0)), (26, y0), (26 + (0), y0 + 72), (-26, y0 + 72)], st, INK, 3)
        box(ctx, 8, y0 + 2, 17, 68, std)
        for k in range(4): circle(ctx, 0, y0 + (12 + k*14 if sg > 0 else 14 + k*14 + 2), 3.2, std, INK, 1.5)
        line(ctx, [(-20, y0 + 6), (-20, y0 + 66)], _lt(st, .35), 2.5)
    box(ctx, 44, -14, 10, 24, STEEL_D, 3, INK, 2.5)
    box(ctx, -48, -48, 96, 96, hexc('#2a2d34'), 24, INK, 3)
    box(ctx, -40, -40, 80, 80, hexc('#05070a'), 17)
    text(ctx, "10:09", 0, -4, 36, hexc('#7df9ff'))
    text(ctx, "TUE 14", 0, 24, 15, (0.85, 0.88, 0.9))
    for k, col in enumerate(('#ff4d6d', '#7cf26a', '#4dd2ff')):
        ctx.arc(-18 + k*18, -26, 5, 0, 6.283 * (0.8 - k*.2)); ctx.set_source_rgb(*hexc(col)); ctx.set_line_width(2.5); ctx.stroke()
    ctx.restore()


# ---------------- chip ----------------
def chip(ctx, x, y, s=1.0, label="CHIP"):
    """Anchor: centre. ~160x160. Dark IC package with bevelled edge, 8 gold pins on each of the 4 sides,
    inner die square with grid, pin-1 dot, plain label in the lower part."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for k in range(8):
        p = -49 + k*14
        box(ctx, -78, p - 4.5, 24, 9, GOLD, 2, INK, 2); box(ctx, 54, p - 4.5, 24, 9, GOLD, 2, INK, 2)
        box(ctx, p - 4.5, -78, 9, 24, GOLD, 2, INK, 2); box(ctx, p - 4.5, 54, 9, 24, GOLD, 2, INK, 2)
        box(ctx, -78, p + 0.5, 24, 4, GOLD_D, 1); box(ctx, 54, p + 0.5, 24, 4, GOLD_D, 1)
        box(ctx, p + 0.5, -78, 4, 24, GOLD_D, 1); box(ctx, p + 0.5, 54, 4, 24, GOLD_D, 1)
    box(ctx, -60, -60, 120, 120, hexc('#262a33'), 8, INK, 3)
    poly(ctx, [(-60, -60), (60, -60), (52, -52), (-52, -52), (-52, 52), (-60, 60)], hexc('#3a404c'))
    poly(ctx, [(60, -60), (60, 60), (-60, 60), (-52, 52), (52, 52), (52, -52)], hexc('#171a20'))
    circle(ctx, -42, -42, 4.5, hexc('#0d0f14'), hexc('#4a5060'), 1.5)
    box(ctx, -28, -40, 56, 56, hexc('#4a5568'), 3, INK, 2.5)
    for k in range(1, 4):
        line(ctx, [(-28 + k*14, -40), (-28 + k*14, 16)], hexc('#6d7a90'), 1.5); line(ctx, [(-28, -40 + k*14), (28, -40 + k*14)], hexc('#6d7a90'), 1.5)
    box(ctx, -22, -34, 22, 22, hexc('#6d7a90'), 2)
    text(ctx, label, 0, 38, 22, hexc('#e8ecf2'))
    ctx.restore()


# ---------------- circuit board ----------------
def _mini_chip(ctx, cx, cy, w, h, label=None, pins=6):
    for k in range(pins):
        px = cx - w/2 + (k + .5)*w/pins
        box(ctx, px - 2, cy - h/2 - 5, 4, 7, hexc('#d8dde4'), 0, INK, 1.2); box(ctx, px - 2, cy + h/2 - 2, 4, 7, hexc('#d8dde4'), 0, INK, 1.2)
    box(ctx, cx - w/2, cy - h/2, w, h, hexc('#1e2128'), 3, INK, 2.5)
    box(ctx, cx - w/2 + 3, cy - h/2 + 3, w - 6, 5, hexc('#3a404c'), 1)
    circle(ctx, cx - w/2 + 8, cy - h/2 + 14, 2.5, hexc('#4a5060'))
    if label: text(ctx, label, cx + 4, cy + 4, min(h*0.4, 18), hexc('#d8dde4'))


def circuit_board(ctx, x, y, w=400, h=260):
    """Anchor: top-left. Green PCB with darker border, right-angled light-green traces ending in silver solder dots,
    4 chips (one large), capacitors, resistors, gold edge fingers, mounting holes."""
    G, GD, GL = hexc('#2c8a4f'), hexc('#1d6a3a'), hexc('#5fd08c')
    ctx.save(); ctx.translate(x, y)
    box(ctx, 0, 0, w, h, G, 10, INK, 3)
    box(ctx, 7, 7, w - 14, h - 14, G, 6, GD, 2)
    rnd = random.Random(11)
    ends = []
    for i in range(26):                                                                  # random orthogonal traces
        px, py = rnd.randint(2, w//20 - 2)*20 + 4, rnd.randint(2, (h - 40)//20)*20 + 4
        pts = [(px, py)]; ends.append((px, py))
        for sg in range(rnd.randint(2, 4)):
            if sg % 2 == 0: px = clamp(px + rnd.choice([-1, 1])*rnd.randint(2, 6)*20, 24, w - 24)
            else: py = clamp(py + rnd.choice([-1, 1])*rnd.randint(2, 5)*20, 24, h - 44)
            pts.append((px, py))
        line(ctx, pts, GD, 6); line(ctx, pts, GL, 3.2); ends.append(pts[-1])
    for k in range(7):                                                                   # parallel bus
        yy = h*0.62 + k*5; x0 = w*0.16; x1 = w*0.55
        pts = [(x0, yy), (x1 - k*8, yy), (x1 - k*8, yy + 28 + (6 - k)*3), (w*0.72, yy + 28 + (6 - k)*3)]
        line(ctx, pts, GD, 4.4); line(ctx, pts, GL, 2.2)
    bw = min(w, h)*0.36
    _mini_chip(ctx, w*0.40, h*0.40, bw, bw, "CPU", 8)
    _mini_chip(ctx, w*0.78, h*0.27, w*0.2, h*0.13, None, 5)
    _mini_chip(ctx, w*0.82, h*0.58, w*0.14, h*0.2, "MEM", 4)
    _mini_chip(ctx, w*0.13, h*0.30, w*0.1, h*0.1, None, 3)
    for k in range(6):                                                                   # capacitors
        cx_ = w*0.12 + k*w*0.055; cy_ = h*0.80
        box(ctx, cx_ - 8, cy_ - 22, 16, 24, hexc('#2e6fb0') if k % 2 == 0 else hexc('#34495e'), 3, INK, 2)
        box(ctx, cx_ + 2, cy_ - 22, 6, 24, _dk(hexc('#2e6fb0'), .3) if k % 2 == 0 else hexc('#22303e'), 2)
        ellipse(ctx, cx_, cy_ - 22, 8, 3, hexc('#c8ced6')); line(ctx, [(cx_ - 4, cy_ - 22), (cx_ + 4, cy_ - 22)], INK, 1)
    for k in range(5):                                                                   # resistors
        rx, ry = w*0.62 + k*20, h*0.84
        box(ctx, rx - 7, ry - 4, 14, 8, hexc('#e6d2a0'), 3, INK, 1.8)
        for bx_, bc in ((-3, '#c0392b'), (0, '#2a2a2a'), (3, '#e0a82e')): box(ctx, rx + bx_ - 1, ry - 4, 2, 8, hexc(bc))
    for (ex, ey) in ends[::2]: circle(ctx, ex, ey, 4.5, hexc('#d8dde4'), INK, 1.5)
    for k in range(int((w - 80)//16)):                                                   # gold fingers
        box(ctx, 40 + k*16, h - 20, 9, 14, GOLD, 1, INK, 1.5)
    for (hx, hy) in ((18, 18), (w - 18, 18), (18, h - 18 - 8), (w - 18, h - 26)):
        circle(ctx, hx, hy, 7.5, GOLD, INK, 2); circle(ctx, hx, hy, 4, hexc('#14301e'))
    ctx.restore()


# ---------------- container ----------------
def container(ctx, x, y, s=1.0, c=None, label=None):
    """Anchor: bottom-left. Side view 240x100 at s=1: corrugated vertical ribs (loop), door end at the right with
    4 lock bars + handles, 4 dark corner castings, top/bottom rails. Default colour rust red."""
    c = c or hexc('#b5472f'); cd = _dk(c, .22); cl = _lt(c, .18)
    ctx.save(); ctx.translate(x, y - 100*s); ctx.scale(s, s)
    box(ctx, 0, 0, 240, 100, c, 0, INK, 3)
    for k in range(34):                                                                  # corrugation
        xx = 8 + k*5.3
        box(ctx, xx, 8, 2.6, 84, cd if k % 2 == 0 else cl)
    box(ctx, 196, 0, 44, 100, c, 0, INK, 3)                                              # door end
    box(ctx, 200, 8, 36, 84, _mix(c, cd, .35), 0, INK, 2)
    line(ctx, [(218, 8), (218, 92)], INK, 2.5)
    for dx in (203, 211, 225, 232):
        line(ctx, [(dx, 14), (dx, 86)], STEEL_L, 3); line(ctx, [(dx, 14), (dx, 86)], INK, 1)
        box(ctx, dx - 2.5, 46, 5, 8, STEEL_D, 1, INK, 1.2)
    box(ctx, 0, 0, 240, 7, _dk(c, .12), 0, INK, 2.5); box(ctx, 0, 93, 240, 7, _dk(c, .3), 0, INK, 2.5)
    for cx_, cy_ in ((0, 0), (226, 0), (0, 88), (226, 88)):
        box(ctx, cx_, cy_, 14, 12, hexc('#2a2d34'), 2, INK, 2); circle(ctx, cx_ + 7, cy_ + 6, 2.2, hexc('#8d95a2'))
    if label: text(ctx, label, 100, 52, 30, (1, 1, 1), outline=None)
    ctx.restore()


# ---------------- container ship ----------------
def container_ship(ctx, x, y, s=1.0, t=0.0, label=None):
    """Anchor: waterline centre (x,y). ~800 wide at s=1. Dark navy hull with red bottom stripe and white rail line,
    10 stacks of containers 3-4 tiers high in 4-5 colours (loops), white bridge tower + red funnel at the stern (left),
    bow at the right, gentle bob/roll with t. Plain name on the bow if label. Draw the sea in front/after to hide the keel."""
    hull, hull_d = hexc('#1f2d44'), hexc('#16202f')
    ctx.save(); ctx.translate(x, y + math.sin(t*2.0)*4); ctx.rotate(math.sin(t*1.6)*0.012); ctx.scale(s, s)
    # funnel behind tower
    box(ctx, -352, -218, 38, 70, hexc('#c0392b'), 3, INK, 3); box(ctx, -352, -200, 38, 8, (1, 1, 1)); box(ctx, -332, -217, 16, 68, _dk(hexc('#c0392b'), .25))
    # containers
    rnd = random.Random(5)
    for i in range(10):
        n = 3 + (i*7 + 2) % 2 + (1 if i in (1, 4, 5, 6) else 0)
        n = min(n, 4)
        if i == 9: n = 2
        sx = -268 + i*60
        for j in range(n):
            col = _CONT[rnd.randrange(4)] if (i + j) % 5 else _CONT[4]
            by = -76 - (j + 1)*31
            box(ctx, sx, by, 58, 31, col, 0, INK, 2.2)
            box(ctx, sx + 44, by + 1, 13, 29, _dk(col, .22))
            for k in range(6): line(ctx, [(sx + 5 + k*7, by + 5), (sx + 5 + k*7, by + 26)], _dk(col, .2), 1.4)
            box(ctx, sx, by, 58, 3, _lt(col, .25))
    # hull
    pts = [(-395, -76), (340, -76), (408, -110), (352, 18), (-380, 18)]
    poly(ctx, pts, hull, INK, 3)
    ctx.save(); ctx.move_to(*pts[0]); [ctx.line_to(*p) for p in pts[1:]]; ctx.close_path(); ctx.clip()
    box(ctx, -420, -14, 820, 40, hexc('#b5352a'))
    line(ctx, [(-420, -14), (420, -14)], INK, 2.5)
    box(ctx, -420, -76, 840, 10, hexc('#e8eef4'))
    for k in range(16): line(ctx, [(-360 + k*46, -62), (-360 + k*46, -20)], _lt(hull, .06), 3)
    ctx.restore()
    line(ctx, [(-395, -76), (340, -76), (408, -110)], INK, 3)
    for k in range(40):                                                                  # deck railing at bow
        pass
    # bridge tower
    box(ctx, -388, -118, 100, 42, hexc('#f1f3f6'), 2, INK, 3)
    box(ctx, -382, -148, 88, 30, hexc('#f1f3f6'), 2, INK, 3)
    box(ctx, -376, -176, 76, 28, hexc('#f1f3f6'), 2, INK, 3)
    box(ctx, -370, -202, 64, 26, hexc('#f1f3f6'), 2, INK, 3)
    box(ctx, -300, -118, 12, 42, hexc('#cfd5dc')); box(ctx, -306, -148, 12, 30, hexc('#cfd5dc'))
    box(ctx, -308, -176, 8, 28, hexc('#cfd5dc')); box(ctx, -314, -202, 8, 26, hexc('#cfd5dc'))
    for lv, (wy, x0, n) in enumerate(((-108, -378, 7), (-138, -372, 6), (-166, -366, 5), (-194, -362, 4))):
        for k in range(n): box(ctx, x0 + k*13.5, wy, 9, 10, hexc('#2e4a6b'), 1, INK, 1.2)
    box(ctx, -374, -208, 72, 8, hexc('#2e4a6b'), 2, INK, 2.5)
    line(ctx, [(-338, -208), (-338, -240)], INK, 3); line(ctx, [(-348, -230), (-328, -230)], INK, 2.5)
    # name on bow
    if label: text(ctx, label, 235, -42, 30, (1, 1, 1))
    ctx.restore()


# ---------------- port crane ----------------
def port_crane(ctx, x, y, s=1.0):
    """Anchor: bottom-centre. Ship-to-shore gantry crane ~380 tall x ~460 wide: A-frame legs with X bracing, truss boom
    reaching right (ship side) with back-reach left, apex mast with stay lines, trolley + two cables + spreader holding a
    container. Light blue steel in 3 tones."""
    cb, cd, cl = hexc('#5fa0cc'), hexc('#3f7aa5'), hexc('#a9d0e8')
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    # legs
    for sg in (-1, 1):
        poly(ctx, [(sg*100, 0), (sg*76, 0), (sg*48, -262), (sg*72, -262)], cb, INK, 3)
        poly(ctx, [(sg*90, 0), (sg*76, 0), (sg*48, -262), (sg*58, -262)], cd)
    for yy, hw0, hw1 in ((-90, 88, 78), (-180, 70, 62)):
        pass
    for (ya, yb) in ((0, -90), (-90, -180), (-180, -262)):
        wa = 88 - (-ya)*0 ;
        def hw(yv): return lerp(88, 60, -yv/262)
        xa, xb = hw(ya) - 8, hw(yb) - 8
        line(ctx, [(-xa, ya), (xb, yb)], INK, 5); line(ctx, [(-xa, ya), (xb, yb)], cl, 2.2)
        line(ctx, [(xa, ya), (-xb, yb)], INK, 5); line(ctx, [(xa, ya), (-xb, yb)], cl, 2.2)
        box(ctx, -xb - 6, yb - 4, 2*xb + 12, 8, cd, 0, INK, 2.5)
    for sg in (-1, 1):                                                                   # bogies + wheels
        box(ctx, sg*88 - 24, -14, 48, 12, hexc('#3a3f4b'), 2, INK, 2.5)
        for k in (-14, 14): circle(ctx, sg*88 + k, -5, 6, hexc('#2a2d34'), INK, 2)
    # girder / boom
    xs0, xs1 = -150, 290
    box(ctx, -150, -296, 90, 34, hexc('#d9a62e'), 3, INK, 3)                            # machinery house
    box(ctx, -150, -282, 90, 20, _dk(hexc('#d9a62e'), .2))
    for k in range(3): box(ctx, -140 + k*26, -290, 16, 10, hexc('#7ec8e3'), 1, INK, 1.5)
    for k in range(int((xs1 - xs0)/20)):                                                 # truss zigzag
        xa = xs0 + 70 + k*20
        if xa + 20 > xs1 - 8: break
        tip = (xs1 - xa)/(xs1 - xs0)
        line(ctx, [(xa, -282 + (1 - tip)*0), (xa + 10, -262), (xa + 20, -282)], cd, 3.2)
    poly(ctx, [(-60, -284), (xs1, -276), (xs1 + 14, -270), (xs1, -262), (-60, -262)], cb, INK, 3, a=0.0)
    line(ctx, [(-60, -284), (xs1, -284)], INK, 6); line(ctx, [(-60, -284), (xs1, -284)], cb, 3)
    line(ctx, [(-60, -262), (xs1, -262)], INK, 6); line(ctx, [(-60, -262), (xs1, -262)], cd, 3)
    poly(ctx, [(xs1, -285), (xs1 + 22, -274), (xs1, -261)], cb, INK, 3)
    # A-frame mast + stays
    poly(ctx, [(-50, -284), (0, -382), (50, -284)], cb, INK, 3)
    poly(ctx, [(-24, -284), (0, -382), (50, -284)], cd, a=1)
    poly(ctx, [(-36, -284), (0, -352), (36, -284), (22, -284), (0, -330), (-22, -284)], cb, INK, 2)
    line(ctx, [(0, -382), (xs1 + 8, -280)], INK, 3); line(ctx, [(0, -382), (xs0 + 20, -296)], INK, 3)
    circle(ctx, 0, -382, 5, hexc('#c0392b'), INK, 2)
    # trolley + spreader + container
    tx = 205
    box(ctx, tx - 26, -262, 52, 14, hexc('#c0392b'), 2, INK, 2.5)
    for cx_ in (tx - 18, tx + 18): circle(ctx, cx_, -258, 4, hexc('#2a2d34'))
    for dx in (-22, 22):
        line(ctx, [(tx + dx, -248), (tx + dx*1.4, -164)], INK, 2.5)
    box(ctx, tx - 38, -168, 76, 10, hexc('#3a3f4b'), 2, INK, 2.5)
    box(ctx, tx - 36, -158, 72, 32, hexc('#2e6fb0'), 0, INK, 2.5)
    box(ctx, tx + 20, -157, 15, 30, _dk(hexc('#2e6fb0'), .25))
    for k in range(8): line(ctx, [(tx - 30 + k*8, -153), (tx - 30 + k*8, -130)], _dk(hexc('#2e6fb0'), .2), 1.3)
    ctx.restore()


# ---------------- sea ----------------
def sea(ctx, y, t=0.0):
    """Anchor: full width, from y to the bottom of the frame. Two blue tones (lighter top, deeper lower) plus
    rows of short white wave strokes drifting with t. Draw BEHIND the ship's hull bottom or over it for a bobbing look."""
    top, deep = hexc('#3f95c9'), hexc('#2d78ad')
    hgt = H - y
    box(ctx, 0, y, W, hgt, top)
    box(ctx, 0, y + hgt*0.45, W, hgt*0.55, deep)
    box(ctx, 0, y, W, 5, _lt(top, .45))
    rows = max(2, int(hgt//26))
    for r_ in range(rows):
        yy = y + 18 + r_*26
        for k in range(9):
            x0 = (k*170 + r_*67 + t*(22 + r_*5)) % (W + 160) - 80
            amp = 5 + r_*0.6
            pts = [(x0 + u*8, yy + math.sin(u*0.9 + t*2 + k)*amp*0.6 - math.sin(u*0.45)*amp) for u in range(0, 9)]
            line(ctx, pts, hexc('#e8f6ff') if r_ < rows*0.45 else hexc('#7fc2e8'), 3, .85)


# ---------------- skyline ----------------
def _tower_crane(ctx, x, y, h, t, seed=0, lc=INK):
    yc, yd = hexc('#f0b429'), hexc('#c28a10')
    mw = 16
    box(ctx, x - mw/2, y - h, mw, h, yc, 0, INK, 2.5)
    for k in range(int(h//16)):
        line(ctx, [(x - mw/2, y - k*16), (x + mw/2, y - k*16 - 16)], yd, 2); line(ctx, [(x + mw/2, y - k*16), (x - mw/2, y - k*16 - 16)], yd, 2)
    ty = y - h
    box(ctx, x - 12, ty - 4, 24, 20, hexc('#e8ecf0'), 3, INK, 2.5); box(ctx, x - 8, ty, 12, 9, hexc('#7ec8e3'), 1)
    box(ctx, x - 140, ty - 14, 330, 10, yc, 0, INK, 2.5)
    for k in range(32): line(ctx, [(x - 138 + k*10, ty - 4), (x - 133 + k*10, ty - 14)], yd, 1.8)
    box(ctx, x - 142, ty - 4, 30, 24, hexc('#6a707a'), 2, INK, 2.5)
    poly(ctx, [(x - 6, ty - 14), (x, ty - 54), (x + 6, ty - 14)], yc, INK, 2.5)
    line(ctx, [(x, ty - 54), (x + 186, ty - 14)], lc, 2); line(ctx, [(x, ty - 54), (x - 130, ty - 14)], lc, 2)
    hx = x + 120 + math.sin(t*0.8 + seed)*3
    box(ctx, hx - 8, ty - 4, 16, 6, hexc('#c0392b'), 1, INK, 1.5)
    ln = 110 + math.sin(t*0.5 + seed)*8
    line(ctx, [(hx, ty + 2), (hx, ty + ln)], lc, 2)
    box(ctx, hx - 7, ty + ln, 14, 6, hexc('#8d95a2'), 1, INK, 1.5)
    box(ctx, hx - 16, ty + ln + 6, 32, 12, hexc('#9aa3ad'), 1, INK, 1.5)


def skyline(ctx, y, night=False, t=0.0):
    """Anchor: full width, bottom at y. 12 towers of varied heights in 3 tones (base / mid / shadow), window grids
    (lit yellow at night, pale glass by day), roof steps, antennas, 2 yellow tower cranes with swaying hook."""
    if night:
        tones = [hexc('#2c3550'), hexc('#242c46'), hexc('#1b2138')]; lit, unlit = hexc('#ffd86b'), hexc('#3a4568')
    else:
        tones = [hexc('#a8bccf'), hexc('#8aa2b9'), hexc('#6c859e')]; lit, unlit = hexc('#e6f3fa'), hexc('#7a93ab')
    rnd = random.Random(21)
    spec = []
    xx = -20
    for i in range(12):
        w = rnd.randint(78, 112); h = [190, 300, 240, 380, 220, 330, 270, 200, 360, 250, 310, 210][i]
        spec.append((xx, w, h, i % 3)); xx += w - rnd.randint(0, 14)
    def tower(i, xx, w, h, tn):
        base = tones[tn]; shade = _dk(base, .18)
        ctx.save()
        top = y - h
        box(ctx, xx, top, w, h, base, 0, INK, 3)
        box(ctx, xx + w*0.74, top + 2, w*0.26 - 2, h - 2, shade)
        if i % 3 == 1: box(ctx, xx + w*0.18, top - 20, w*0.64, 20, base, 0, INK, 3); box(ctx, xx + w*0.62, top - 18, w*0.2 - 1, 18, shade)
        if i % 4 == 3: line(ctx, [(xx + w/2, top - (20 if i % 3 == 1 else 0)), (xx + w/2, top - 52)], INK, 3)
        cols = int((w - 16)//17); rows = int((h - 24)//23)
        for r_ in range(rows):
            for c_ in range(cols):
                on = ((r_*7 + c_*13 + i*5) % 10) < (6 if night else 7)
                col = lit if on else unlit
                box(ctx, xx + 9 + c_*17, top + 12 + r_*23, 11, 15, col, 1)
        ctx.restore()
    for i, (xx, w, h, tn) in enumerate(spec):
        tower(i, xx, w, h, tn)
    lc = hexc('#c9d3e6') if night else INK
    _tower_crane(ctx, 300, y, 400, t, 0.0, lc)
    _tower_crane(ctx, 985, y, 430, t, 2.0, lc)


# ---------------- highway ----------------
def _car(ctx, x, y, c):
    cd = _dk(c, .25)
    for wx in (-30, 30):
        pass
    ctx.save(); ctx.translate(x, y)
    poly(ctx, [(-30, -28), (-20, -48), (22, -48), (40, -28)], c, INK, 2.5)
    poly(ctx, [(-24, -30), (-17, -44), (-2, -44), (-2, -30)], hexc('#bfe4f4'), INK, 2)
    poly(ctx, [(2, -30), (2, -44), (20, -44), (32, -30)], hexc('#bfe4f4'), INK, 2)
    box(ctx, -52, -30, 104, 22, c, 8, INK, 2.5)
    box(ctx, -52, -14, 104, 6, cd, 3)
    box(ctx, 44, -26, 7, 6, hexc('#ffe27a'), 2, INK, 1.5); box(ctx, -52, -26, 5, 6, hexc('#ff5a4a'), 2, INK, 1.5)
    for wx in (-30, 30):
        circle(ctx, wx, -8, 11, hexc('#23262c'), INK, 2.5); circle(ctx, wx, -8, 5, hexc('#aeb5bf'))
    ctx.restore()


def highway(ctx, y, t=0.0):
    """Anchor: full width, band from y downward ~140 px. Light kerb strip on top, asphalt, white dashed centre line
    moving with t, solid edge lines, 3 small side-view cars (red, blue, yellow) driving right in two lanes."""
    asp = hexc('#4a4e57')
    box(ctx, 0, y, W, 140, asp)
    box(ctx, 0, y, W, 12, hexc('#b7bcc4'), 0, INK, 3); box(ctx, 0, y + 6, W, 6, hexc('#8f959e'))
    box(ctx, 0, y + 130, W, 10, hexc('#9aa0a8'), 0, INK, 3)
    for k in range(40):
        box(ctx, 0 + k*40 + 8, y + 12, 3, 8, hexc('#7d838c'))
    line(ctx, [(0, y + 28), (W, y + 28)], (0.93, 0.93, 0.9), 3)
    line(ctx, [(0, y + 118), (W, y + 118)], (0.93, 0.93, 0.9), 3)
    off = (t*240) % 100
    for k in range(-1, W//100 + 2):
        box(ctx, k*100 + off, y + 71, 56, 5, (0.96, 0.96, 0.93), 2)
    for cx0, sp, col, ly in ((120, 200, '#c0392b', y + 66), (700, 150, '#2e6fb0', y + 66), (420, 260, '#e0a82e', y + 114)):
        _car(ctx, (cx0 + t*sp) % (W + 240) - 120, ly, hexc(col))


# ---------------- R&D center ----------------
def rd_center(ctx, x, y, s=1.0, label="R&D CENTER"):
    """Anchor: bottom-centre. Modern glass building ~380x320: tall main block + lower wing, curtain-wall grid in 2 blue
    tones with mullions, shaded right face, entrance canopy on posts with glass doors, rooftop sign with label."""
    g1, g2 = hexc('#69b1de'), hexc('#4a8fc2')
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    def wall(x0, y0, w, h, sh):
        ctx.save(); ctx.rectangle(x0, y0, w, h); ctx.clip()
        box(ctx, x0, y0, w, h, hexc('#dfe6ee'), 0, INK, 3)
        cw, ch = 24, 30
        cols, rows = int((w - 6)//cw), int((h - 6)//ch)
        for r_ in range(rows):
            for c_ in range(cols):
                col = g1 if (r_ + c_) % 3 else g2
                if (r_*3 + c_*5) % 7 == 0: col = _lt(g1, .35)
                box(ctx, x0 + 3 + c_*cw, y0 + 3 + r_*ch, cw - 2, ch - 2, col)
        for c_ in range(cols + 1): line(ctx, [(x0 + 2 + c_*cw, y0 + 2), (x0 + 2 + c_*cw, y0 + 4 + rows*ch)], INK, 1.5)
        for r_ in range(rows + 1): line(ctx, [(x0 + 2, y0 + 2 + r_*ch), (x0 + 4 + cols*cw, y0 + 2 + r_*ch)], INK, 1.5)
        poly(ctx, [(x0 + w - 26, y0 + 2), (x0 + w - 2, y0 + 2), (x0 + w - 2, y0 + h - 2), (x0 + w - 26, y0 + h - 2)], (0.05, 0.12, 0.3), a=.28)
        ctx.restore()
        rrect(ctx, x0, y0, w, h, 0); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    wall(-190, -190, 120, 190, 0)
    wall(-70, -290, 260, 290, 0)
    box(ctx, -190, -198, 120, 10, hexc('#8d97a3'), 0, INK, 3); box(ctx, -70, -298, 260, 10, hexc('#8d97a3'), 0, INK, 3)
    # entrance
    box(ctx, -20, -78, 100, 78, hexc('#2a3a4e'), 0, INK, 3)
    for k in range(3): box(ctx, -14 + k*31, -72, 28, 72, hexc('#a6d9f2'), 0, INK, 2); line(ctx, [(-14 + k*31 + 14, -72), (-14 + k*31 + 14, 0)], INK, 1.5)
    box(ctx, -40, -92, 140, 14, hexc('#e8ecf0'), 2, INK, 3); box(ctx, -40, -80, 140, 4, hexc('#8d97a3'))
    for px in (-34, 94): box(ctx, px, -78, 6, 78, hexc('#c9ced6'), 0, INK, 2.5)
    # rooftop sign
    box(ctx, 10, -322, 6, 26, STEEL_D, 0, INK, 2); box(ctx, 160, -322, 6, 26, STEEL_D, 0, INK, 2)
    box(ctx, -30, -354, 240, 40, hexc('#1f2d44'), 6, INK, 3)
    text(ctx, label, 90, -334, 32, (1, 1, 1))
    ctx.restore()


# ---------------- cargo truck ----------------
def cargo_truck(ctx, x, y, s=1.0, label=None, c=None):
    """Anchor: bottom-centre. Side-view box truck ~340x170 facing right: big box body (colour c, default off-white)
    with ribs and optional plain label, red cab with window, bumper, headlight, mirror, 3 wheels with hubcaps."""
    c = c or hexc('#eef0f2'); cd = _dk(c, .14); cab, cabd = hexc('#c0392b'), hexc('#8f2a1f')
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    box(ctx, -172, -52, 344, 14, hexc('#3a3f4b'), 2, INK, 2.5)                          # chassis
    box(ctx, -170, -170, 212, 120, c, 4, INK, 3)                                         # box
    box(ctx, -170, -76, 212, 26, cd, 0, INK, 2.5)
    box(ctx, 26, -168, 14, 116, cd)
    for k in range(5): line(ctx, [(-150 + k*38, -166), (-150 + k*38, -80)], cd, 2)
    box(ctx, -170, -170, 212, 7, _lt(c, .5), 4, INK, 2.5)
    if label: text(ctx, label, -64, -118, 36, hexc('#1f2d44'))
    poly(ctx, [(48, -52), (48, -138), (102, -138), (114, -104), (170, -96), (170, -52)], cab, INK, 3)
    poly(ctx, [(48, -52), (48, -66), (170, -66), (170, -52)], cabd)
    poly(ctx, [(58, -130), (98, -130), (108, -102), (58, -102)], hexc('#bfe4f4'), INK, 2.5)
    line(ctx, [(78, -100), (78, -62)], cabd, 2); box(ctx, 82, -86, 10, 4, cabd, 1)
    box(ctx, 42, -122, 8, 20, STEEL_D, 2, INK, 2)
    box(ctx, 160, -92, 10, 12, hexc('#ffe27a'), 2, INK, 2); box(ctx, 164, -62, 12, 12, hexc('#8d95a2'), 2, INK, 2.5)
    box(ctx, 130, -78, 14, 3, cabd)
    for wx in (-112, -64, 120):
        circle(ctx, wx, -23, 23, hexc('#23262c'), INK, 3); circle(ctx, wx, -23, 11, hexc('#aeb5bf'), INK, 2); circle(ctx, wx, -23, 3.5, STEEL_D)
        poly(ctx, [(wx - 30, -52), (wx + 30, -52), (wx + 24, -44), (wx - 24, -44)], hexc('#2a2d34'), a=0)
    ctx.restore()


# ---------------- stamp ----------------
def stamp_mark(ctx, x, y, text="MADE IN VIETNAM", s=1.0, rot=-0.12):
    """Anchor: centre. Rectangular rubber-stamp impression in red ink: double border, bold lettering, rough worn edges
    and speckle dropouts. Size adapts to the text (~410x104 at s=1 for the default)."""
    txt, size = text, 58
    ctx.save(); ctx.select_font_face(FONT); ctx.set_font_size(size); ext = ctx.text_extents(txt); ctx.restore()
    w, h = ext.width + 60, size + 46
    ink = hexc('#b3261e')
    rnd = random.Random(3)
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.push_group()
    for off, lw in ((0, 6), (9, 2.5)):
        x0, y0, x1, y1 = -w/2 + off, -h/2 + off, w/2 - off, h/2 - off
        pts = [(lerp(x0, x1, u/40), y0) for u in range(41)] + [(x1, lerp(y0, y1, u/20)) for u in range(1, 21)] \
            + [(lerp(x1, x0, u/40), y1) for u in range(1, 41)] + [(x0, lerp(y1, y0, u/20)) for u in range(1, 20)]
        pts = [(a + rnd.uniform(-1.3, 1.3), b + rnd.uniform(-1.3, 1.3)) for a, b in pts]
        ctx.move_to(*pts[0]); [ctx.line_to(*q) for q in pts[1:]]; ctx.close_path()
        ctx.set_source_rgba(*ink, .92); ctx.set_line_width(lw); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
    globals()['text'](ctx, txt, 0, 2, size, ink)
    ctx.set_operator(cairo.OPERATOR_DEST_OUT)                       # worn-ink speckles
    for _ in range(170):
        px, py = rnd.uniform(-w/2 - 4, w/2 + 4), rnd.uniform(-h/2 - 4, h/2 + 4)
        ctx.arc(px, py, rnd.uniform(0.8, 2.6), 0, 6.283); ctx.set_source_rgba(0, 0, 0, rnd.uniform(.6, 1)); ctx.fill()
    for _ in range(14):
        px, py = rnd.uniform(-w/2, w/2), rnd.uniform(-h/2, h/2)
        ctx.move_to(px, py); ctx.line_to(px + rnd.uniform(-14, 14), py + rnd.uniform(-5, 5))
        ctx.set_source_rgba(0, 0, 0, .8); ctx.set_line_width(rnd.uniform(1, 2.2)); ctx.stroke()
    ctx.set_operator(cairo.OPERATOR_OVER)
    p = ctx.pop_group()
    ctx.set_source(p); ctx.paint(); ctx.restore()
