import sys, os, math; sys.path.insert(0, os.getcwd())
from episodes.vietnam.assets import *
import episodes.vietnam.assets as _A
"""Vietnam episode: political / economic props and backgrounds (second asset module). Reuse, never redraw.
Canvas 1280x720. Flat colours, INK outlines, no emblems."""

WHITE = (1, 1, 1)
CREAM = hexc('#f4ecd2')
WOOD, WOOD_D, WOOD_L = hexc('#a8703f'), hexc('#8b5a33'), hexc('#c48a52')
CURT, CURT_D, CURT_L = hexc('#8c1f26'), hexc('#6a1219'), hexc('#a8303a')
STEEL, STEEL_D, STEEL_L = hexc('#aab2ba'), hexc('#838c96'), hexc('#d3d9de')
BRICK, BRICK_D, BRICK_L, MORTAR = hexc('#b5533c'), hexc('#97412e'), hexc('#cf6c52'), hexc('#d9cdb6')
GOLD, GOLD_D, GOLD_L = hexc('#e5b73b'), hexc('#b8861e'), hexc('#fbe08a')
CHALK = hexc('#f1efe6')


def _mix(c, d, f):
    return tuple(a + (b - a) * f for a, b in zip(c, d))


def _dark(c, f=0.25):
    return _mix(c, (0, 0, 0), f)


def _light(c, f=0.3):
    return _mix(c, (1, 1, 1), f)


def _path(ctx, pts, close=True):
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    if close:
        ctx.close_path()


def _wave(ctx, x, y0, y1, amp, phase, c, lw=3, a=1.0, freq=2.0):
    pts = []
    n = 24
    for i in range(n + 1):
        u = i / n
        pts.append((x + math.sin(u * math.pi * 2 * freq + phase) * amp, lerp(y0, y1, u)))
    line(ctx, pts, c, lw, a)


# =====================================================================================
def bg_congress(ctx, t=0.0, banner="6TH NATIONAL CONGRESS  ·  1986"):
    """Full-frame party congress hall. Anchor: whole canvas. Deep red curtain with 3-tone vertical folds (y 0-470),
    scalloped valance, cream banner across top (y 40-118) with plain text, long head table: white cloth top at y=470
    (cloth to y=562), 5 plain microphones on it, two rows of delegates seen from behind (y 560-720). No emblems."""
    box(ctx, 0, 0, W, 470, CURT_D)
    fw = 80
    for i in range(-1, W // fw + 2):
        x0 = i * fw
        box(ctx, x0, 0, fw * 0.34, 470, CURT_D)
        box(ctx, x0 + fw * 0.34, 0, fw * 0.36, 470, CURT)
        box(ctx, x0 + fw * 0.70, 0, fw * 0.12, 470, CURT_L)
        box(ctx, x0 + fw * 0.82, 0, fw * 0.18, 470, CURT)
        line(ctx, [(x0, 0), (x0, 470)], _dark(CURT_D, .4), 2, .7)
    # valance swags
    for i in range(0, W // 160 + 2):
        cx = i * 160
        ctx.new_path(); ctx.move_to(cx - 80, 0); ctx.curve_to(cx - 70, 70, cx + 70, 70, cx + 80, 0); ctx.close_path()
        ctx.set_source_rgb(*CURT_L); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
        ctx.move_to(cx - 60, 4); ctx.curve_to(cx - 40, 45, cx + 40, 45, cx + 60, 4)
        ctx.set_source_rgb(*CURT); ctx.set_line_width(5); ctx.stroke()
        for k in (-1, 0, 1):
            line(ctx, [(cx + k * 36, 2), (cx + k * 30, 46 - abs(k) * 6)], CURT_D, 2, .8)
    # banner
    box(ctx, 146, 52, 1000, 78, _dark(CREAM, .3), 8, None)
    box(ctx, 140, 44, 1000, 78, CREAM, 8, INK, 3)
    box(ctx, 150, 54, 980, 58, CREAM, 5, hexc('#c9b98a'), 2)
    text(ctx, banner, 640, 83, 56, hexc('#7a1a20'))
    # floor behind delegates
    box(ctx, 0, 562, W, 158, hexc('#4a2a2e'))
    for yy in (600, 650, 700):
        line(ctx, [(0, yy), (W, yy)], hexc('#3b2024'), 2, .8)
    # head table
    box(ctx, 56, 470, 1168, 16, hexc('#f9f6ec'), 4, INK, 3)
    box(ctx, 64, 486, 1152, 76, WHITE, 0, INK, 3)
    for i in range(0, 1152 // 48 + 1):
        fx = 64 + i * 48
        box(ctx, fx, 486, 14, 76, hexc('#e3e6ea'))
        line(ctx, [(fx + 14, 486), (fx + 14, 562)], hexc('#c9ced4'), 2, .8)
    line(ctx, [(64, 559), (1216, 559)], hexc('#c9ced4'), 4)
    for k in range(7):  # blank name placards
        px = 150 + k * 165
        box(ctx, px - 36, 500, 72, 22, hexc('#f1ede0'), 3, hexc('#9a927c'), 2)
    # microphones
    for mx in (210, 425, 640, 855, 1070):
        ellipse(ctx, mx, 468, 26, 6, hexc('#3a3d44'))
        ellipse(ctx, mx, 466, 22, 4, hexc('#575b64'))
        line(ctx, [(mx, 466), (mx, 420)], INK, 8)
        line(ctx, [(mx, 466), (mx, 420)], hexc('#8c929a'), 4)
        box(ctx, mx - 12, 384, 24, 42, hexc('#2c2f35'), 12, INK, 2.5)
        for k in range(4):
            line(ctx, [(mx - 9, 392 + k * 8), (mx + 9, 392 + k * 8)], hexc('#6a6f78'), 1.8)
        box(ctx, mx - 6, 388, 3, 30, hexc('#8c929a'), 1)
    # delegates from behind
    hairs = [hexc('#1d1715'), hexc('#2a2018'), hexc('#14110f'), hexc('#8a8a86'), hexc('#241b16'), hexc('#1d1715')]
    shirts = [WHITE, hexc('#a9c4dc'), hexc('#d7cfba'), hexc('#7d8c6a'), hexc('#c9ced4'), hexc('#e6d8c0'), hexc('#8aa6c0')]
    for row, (cy, r, step, off, sh_h) in enumerate([(604, 25, 104, 40, 70), (672, 31, 132, 100, 70)]):
        n = int(W // step) + 2
        for i in range(-1, n):
            x = off + i * step + ((i * 37) % 11 - 5)
            by = cy + math.sin(t * 1.4 + i * 1.7 + row) * 1.5
            sc = shirts[(i * 3 + row * 2) % len(shirts)]
            hc = hairs[(i * 5 + row) % len(hairs)]
            # shoulders / jacket back
            sw = r * 2.5
            ctx.new_path()
            ctx.move_to(x - sw / 2, by + r + sh_h); ctx.line_to(x - sw / 2, by + r + 8)
            ctx.curve_to(x - sw / 2, by + r - 4, x - r * 0.6, by + r - 6, x - r * 0.3, by + r - 6)
            ctx.line_to(x + r * 0.3, by + r - 6)
            ctx.curve_to(x + r * 0.6, by + r - 6, x + sw / 2, by + r - 4, x + sw / 2, by + r + 8)
            ctx.line_to(x + sw / 2, by + r + sh_h); ctx.close_path()
            ctx.set_source_rgb(*sc); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
            poly(ctx, [(x + sw * 0.18, by + r + 2), (x + sw / 2 - 1, by + r + 10), (x + sw / 2 - 1, by + r + sh_h), (x + sw * 0.18, by + r + sh_h)], _dark(sc, .12))
            line(ctx, [(x, by + r + 6), (x, by + r + sh_h)], _dark(sc, .25), 2, .8)
            # neck, ears, head
            box(ctx, x - r * 0.32, by + r * 0.5, r * 0.64, r * 0.75, hexc('#d9a77d'), 3, INK, 2)
            for sd in (-1, 1):
                ellipse(ctx, x + sd * r * 0.98, by + r * 0.18, r * 0.16, r * 0.26, hexc('#e3b58a'))
            circle(ctx, x, by, r, hc, INK, 2.5)
            ctx.new_sub_path(); ctx.arc(x, by, r, 0.15, math.pi - 0.15)
            ctx.set_source_rgb(*_light(hc, .0));
            # hairline (nape) and part highlight
            line(ctx, [(x - r * 0.62, by + r * 0.62), (x, by + r * 0.8), (x + r * 0.62, by + r * 0.62)], _dark(hc, .0), 1)
            ctx.new_path()
            ctx.arc(x - r * 0.25, by - r * 0.35, r * 0.45, math.pi * 1.1, math.pi * 1.8)
            ctx.set_source_rgb(*_light(hc, .22)); ctx.set_line_width(3); ctx.stroke()


def podium(ctx, x, y, s=1.0):
    """Wooden lectern, (x,y) = bottom centre. ~150 wide x 220 tall (body 190 + slanted top), front panel, gooseneck mic
    with plain capsule rising ~85 above the top. Wood in 3 tones."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 0, 92, 10, (0, 0, 0), a=.18)
    # body
    poly(ctx, [(-62, 0), (-72, -190), (72, -190), (62, 0)], WOOD, INK, 3)
    poly(ctx, [(34, -190), (72, -190), (62, 0), (30, 0)], WOOD_D)
    poly(ctx, [(-72, -190), (-62, -190), (-52, 0), (-62, 0)], WOOD_L)
    poly(ctx, [(-62, 0), (-72, -190), (72, -190), (62, 0)], (0, 0, 0), INK, 3, a=0)
    # front panel inset
    box(ctx, -46, -165, 92, 130, WOOD_D, 4, INK, 2.5)
    box(ctx, -40, -159, 80, 118, WOOD, 3)
    box(ctx, 8, -159, 32, 118, WOOD_D, 3)
    line(ctx, [(-40, -100), (40, -100)], WOOD_D, 2)
    box(ctx, -68, -12, 136, 12, WOOD_D, 2, INK, 2.5)
    # angled top slab (reading desk)
    poly(ctx, [(-76, -190), (76, -190), (62, -214), (-62, -214)], WOOD_L, INK, 3)
    poly(ctx, [(-76, -190), (76, -190), (76, -180), (-76, -180)], WOOD_D, INK, 3)
    line(ctx, [(-50, -202), (50, -202)], _light(WOOD_L, .3), 2, .8)
    # gooseneck mic
    ctx.new_path(); ctx.move_to(34, -210); ctx.curve_to(38, -260, 20, -290, -4, -296)
    ctx.set_source_rgb(*INK); ctx.set_line_width(8); ctx.stroke_preserve()
    ctx.set_source_rgb(*hexc('#8c929a')); ctx.set_line_width(4); ctx.stroke()
    ctx.save(); ctx.translate(-14, -298); ctx.rotate(-0.35)
    box(ctx, -24, -9, 40, 18, hexc('#2c2f35'), 9, INK, 2.5)
    for k in range(3):
        line(ctx, [(-14 + k * 11, -6), (-14 + k * 11, 6)], hexc('#6a6f78'), 1.8)
    ctx.restore()
    box(ctx, 22, -222, 24, 10, hexc('#3a3d44'), 3, INK, 2)
    ctx.restore()


# =====================================================================================
def bg_kitchen(ctx, t=0.0):
    """Full-frame restaurant kitchen. Anchor: whole canvas. White tile wall (60px grid, y 0-520), steel counter top at
    y=520 (front panel to ~650), black stove with 2 pots and animated rising steam in the centre, hanging rail of
    ladles/pans (y~60-210), warm tiled floor below 650."""
    box(ctx, 0, 0, W, 520, hexc('#f1f3f2'))
    ts = 60
    for r in range(0, 520 // ts + 1):
        for c in range(0, W // ts + 1):
            if (r + c) % 2 == 0:
                box(ctx, c * ts, r * ts, ts, ts, hexc('#e6eae9'))
            box(ctx, c * ts + 4, r * ts + 4, 14, 5, WHITE, 2)
    for c in range(0, W // ts + 1):
        line(ctx, [(c * ts, 0), (c * ts, 520)], hexc('#b9c2c4'), 2)
    for r in range(0, 520 // ts + 1):
        line(ctx, [(0, r * ts), (W, r * ts)], hexc('#b9c2c4'), 2)
    # floor
    box(ctx, 0, 650, W, 70, hexc('#c98f5a'))
    for c in range(0, W // 80 + 2):
        line(ctx, [(c * 80, 650), (c * 80 - 30, 720)], hexc('#a9703f'), 2)
    line(ctx, [(0, 685), (W, 685)], hexc('#a9703f'), 2)
    # counter
    box(ctx, 0, 520, W, 130, STEEL, 0, INK, 3)
    box(ctx, 0, 520, W, 34, STEEL_L, 0, INK, 3)
    box(ctx, 0, 548, W, 8, STEEL_D)
    for c in range(0, 6):
        dx = 20 + c * 212
        box(ctx, dx, 572, 190, 66, STEEL, 4, INK, 2.5)
        box(ctx, dx + 4, 576, 182, 14, STEEL_L, 3)
        box(ctx, dx + 140, 576, 46, 58, STEEL_D, 3)
        box(ctx, dx + 70, 598, 50, 8, STEEL_D, 4, INK, 2)
    line(ctx, [(0, 640), (W, 640)], STEEL_D, 4)
    # stove top unit
    box(ctx, 380, 494, 520, 26, hexc('#2a2c31'), 4, INK, 3)
    box(ctx, 380, 494, 520, 6, hexc('#4a4d55'), 3)
    for bx in (520, 760):
        ellipse(ctx, bx, 497, 66, 8, hexc('#14151a'))
        ellipse(ctx, bx, 494, 48, 5, hexc('#3b3e46'))
    # pots
    def pot(px, w, h, c, cd, lid_off):
        top = 494 - h
        poly(ctx, [(px - w / 2, 494), (px - w / 2 - 4, top), (px + w / 2 + 4, top), (px + w / 2, 494)], c, INK, 3)
        poly(ctx, [(px + w * 0.2, 494), (px + w * 0.2 + 3, top), (px + w / 2 + 4, top), (px + w / 2, 494)], cd)
        box(ctx, px - w / 2 - 6, top - 6, w + 12, 12, _light(c, .2), 5, INK, 3)
        box(ctx, px - w / 2 - 26, top + 12, 24, 10, cd, 4, INK, 2.5)
        box(ctx, px + w / 2 + 2, top + 12, 24, 10, cd, 4, INK, 2.5)
        line(ctx, [(px - w * 0.3, top + 24), (px - w * 0.3, 494 - 14)], _light(c, .45), 4, .9)
        # lid tilted
        ctx.save(); ctx.translate(px + lid_off, top - 10); ctx.rotate(lid_off * 0.011)
        ellipse(ctx, 0, 0, w / 2 + 4, 8, cd)
        ellipse(ctx, 0, -2, w / 2, 6, _light(c, .15))
        circle(ctx, 0, -10, 6, hexc('#2c2f35'), INK, 2)
        ctx.restore()
    pot(520, 150, 118, STEEL, STEEL_D, 30)
    pot(760, 128, 92, hexc('#a5483a'), hexc('#7d3329'), -22)
    # steam (animated)
    for px, ph in ((520, 0.0), (760, 1.7)):
        for k in range(5):
            life = ((t * 0.45 + k / 5 + ph * 0.13) % 1.0)
            yy = 395 - life * 200
            rr = 18 + life * 34
            xx = px + math.sin(life * 7 + k * 2 + ph) * 22
            circle(ctx, xx, yy, rr, WHITE, a=0.75 * (1 - life) ** 0.8)
            circle(ctx, xx, yy, rr, hexc('#cfd8dc'), a=0.0)
    # hanging rail + utensils
    line(ctx, [(70, 62), (1210, 62)], INK, 12)
    line(ctx, [(70, 62), (1210, 62)], STEEL, 7)
    for hx in (70, 1210): line(ctx, [(hx, 62), (hx, 22)], INK, 8)
    items = [(150, 'ladle', 130), (240, 'pan', 0), (350, 'spatula', 120), (450, 'ladle', 160), (560, 'pan', 0), (680, 'whisk', 110),
             (790, 'ladle', 140), (900, 'pan', 0), (1010, 'spatula', 130), (1100, 'ladle', 120), (1170, 'pan', 0)]
    for k, (hx, kind, ln) in enumerate(items):
        sw = math.sin(t * 1.3 + k) * 0.015
        ctx.save(); ctx.translate(hx, 66); ctx.rotate(sw)
        circle(ctx, 0, 0, 5, STEEL_D, INK, 2)
        if kind == 'ladle':
            line(ctx, [(0, 4), (0, ln)], INK, 8); line(ctx, [(0, 4), (0, ln)], STEEL_L, 4)
            ctx.new_path(); ctx.arc(0, ln + 22, 24, 0, math.pi); ctx.close_path()
            ctx.set_source_rgb(*STEEL); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
            ctx.new_path(); ctx.arc(0, ln + 22, 14, 0, math.pi); ctx.set_source_rgb(*STEEL_D); ctx.set_line_width(5); ctx.stroke()
        elif kind == 'spatula':
            line(ctx, [(0, 4), (0, ln - 24)], INK, 8); line(ctx, [(0, 4), (0, ln - 24)], WOOD, 4)
            box(ctx, -16, ln - 28, 32, 50, STEEL, 5, INK, 3)
            for q in range(4): line(ctx, [(-8 + q * 5, ln - 18), (-8 + q * 5, ln + 12)], STEEL_D, 2)
        elif kind == 'whisk':
            line(ctx, [(0, 4), (0, 40)], INK, 8); line(ctx, [(0, 4), (0, 40)], STEEL_L, 4)
            for q in (-18, -9, 0, 9, 18):
                ctx.new_path(); ctx.move_to(0, 40); ctx.curve_to(q * 2.2, 72, q * 1.6, 100, 0, ln); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
        else:
            line(ctx, [(0, 4), (0, 36)], INK, 8)
            ctx.save(); ctx.translate(0, 36)
            line(ctx, [(0, 0), (0, 10)], INK, 8)
            circle(ctx, 0, 62, 54, hexc('#3a3d44'), INK, 3)
            circle(ctx, 0, 62, 40, hexc('#4c5059'), None)
            ctx.new_sub_path(); ctx.arc(-14, 48, 16, math.pi, 1.5 * math.pi); ctx.set_source_rgb(*hexc('#6d727c')); ctx.set_line_width(4); ctx.stroke()
            ctx.restore()
        ctx.restore()


def dish(ctx, x, y, s=1.0, state="fresh", t=0.0):
    """Bowl of pho on a plate, (x,y) = bottom centre. ~300 wide x ~170 tall. Fresh: broth, white noodles, beef slices,
    spring onion, basil + chilli + lime on plate, chopsticks, steam. state='rotten': grey-green food, wilted brown herbs,
    mold spots, wavy green stink lines and 3 small flies circling (t)."""
    rot = (state == "rotten")
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    plate_c = hexc('#f2f4f6'); plate_d = hexc('#cdd4da')
    broth = hexc('#7f8a58') if rot else hexc('#d9a653')
    broth_d = hexc('#64704a') if rot else hexc('#b9852f')
    noodle = hexc('#b9bd9f') if rot else hexc('#fbf6e6')
    noodle_d = hexc('#8f9477') if rot else hexc('#e6dbbb')
    beef = hexc('#7d705a') if rot else hexc('#b9604f')
    beef_d = hexc('#5c5240') if rot else hexc('#8f4638')
    leaf = hexc('#6d6a35') if rot else hexc('#4f9a3c')
    leaf_d = hexc('#4d4b25') if rot else hexc('#3a7a2d')
    # plate
    ellipse(ctx, 0, -14, 154, 30, plate_d);
    ctx.save(); ctx.translate(0, -18); ctx.scale(1, 0.2); ctx.arc(0, 0, 152, 0, 6.283); ctx.restore()
    ctx.set_source_rgb(*plate_c); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    ellipse(ctx, 0, -18, 122, 18, plate_d)
    ellipse(ctx, 0, -20, 118, 15, plate_c)
    # bowl body
    ctx.new_path(); ctx.move_to(-110, -108); ctx.curve_to(-110, -52, -66, -32, -40, -30); ctx.line_to(40, -30)
    ctx.curve_to(66, -32, 110, -52, 110, -108); ctx.close_path()
    ctx.set_source_rgb(*WHITE); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    ctx.save(); ctx.new_path(); ctx.move_to(-110, -108); ctx.curve_to(-110, -52, -66, -32, -40, -30); ctx.line_to(40, -30)
    ctx.curve_to(66, -32, 110, -52, 110, -108); ctx.close_path(); ctx.clip()
    box(ctx, 52, -112, 80, 100, plate_d)
    # blue band + loops pattern
    box(ctx, -120, -92, 240, 7, hexc('#3a6fb0'))
    for k in range(-5, 6):
        circle(ctx, k * 20, -70 + abs(k) * 1.5, 5, hexc('#3a6fb0'), None)
    ctx.restore()
    box(ctx, -42, -34, 84, 8, plate_d, 3, INK, 2.5)
    # rim and broth
    ellipse(ctx, 0, -108, 112, 24, WHITE)
    ctx.new_sub_path(); ctx.save(); ctx.translate(0, -108); ctx.scale(1, 24 / 112); ctx.arc(0, 0, 112, 0, 6.283); ctx.restore()
    ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    ellipse(ctx, 0, -107, 100, 19, broth)
    ellipse(ctx, 18, -103, 70, 11, broth_d, a=0.55)
    # noodles (waves)
    ctx.save(); ctx.new_path(); ctx.save(); ctx.translate(0, -107); ctx.scale(1, 19 / 100); ctx.arc(0, 0, 100, 0, 6.283); ctx.restore(); ctx.clip()
    for k in range(9):
        yy = -121 + k * 3.8
        pts = [(-96 + i * 8, yy + math.sin(i * 0.9 + k * 1.3) * 3.2) for i in range(25)]
        line(ctx, pts, noodle_d, 5)
        line(ctx, [(a, b - 1) for a, b in pts], noodle, 3)
    ctx.restore()
    # beef slices
    for bx, by, br in [(-52, -108, .2), (-8, -112, -.15), (38, -106, .1), (-30, -100, .0), (62, -112, -.25)]:
        ctx.save(); ctx.translate(bx, by); ctx.rotate(br)
        ellipse(ctx, 0, 0, 20, 7.5, beef_d); ellipse(ctx, -1, -1.5, 18, 5.8, beef)
        line(ctx, [(-11, -1.5), (9, -1)], _light(beef, .35), 1.6, .9)
        ctx.restore()
    # spring onion, tiny
    for i in range(14):
        a = i * 2.4
        px, py = math.cos(a) * (14 + (i * 13) % 70), -107 + math.sin(a) * (4 + (i * 7) % 11)
        circle(ctx, px, py, 2.6, leaf_d if rot else hexc('#79c04f'))
    if rot:
        for mx, my, mr in [(-60, -110, 6), (20, -104, 5), (70, -110, 5), (-20, -113, 4)]:
            circle(ctx, mx, my, mr, hexc('#9fb89a'), hexc('#5f7a5c'), 1.5)
            circle(ctx, mx - 1, my - 1, mr * 0.45, hexc('#e8eee4'))
    # herbs sticking out of the right side
    for ang, ln, lf in [(-1.9, 56, 0), (-1.45, 66, 1), (-1.0, 50, 0), (-1.65, 44, 1)]:
        bx, by = 60 + (ang + 1.9) * 24, -112
        ex, ey = bx + math.cos(ang) * ln * 0.55, by + math.sin(ang) * ln
        ctx.save(); ctx.translate(ex, ey); ctx.rotate(ang + math.pi / 2 + (0.5 if rot else 0))
        ctx.new_path(); ctx.move_to(0, 22); ctx.curve_to(-20, 6, -16, -20, 0, -26); ctx.curve_to(16, -20, 20, 6, 0, 22)
        ctx.set_source_rgb(*(leaf if lf else leaf_d)); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
        line(ctx, [(0, 20), (0, -18)], _dark(leaf, .35), 1.8)
        ctx.restore()
        line(ctx, [(bx, by), (ex, ey + 6)], _dark(leaf, .3), 2)
    # lime wedge + chilli on plate
    ctx.save(); ctx.translate(-118, -28); ctx.rotate(-0.2)
    ctx.new_path(); ctx.arc(0, 0, 24, math.pi, 0); ctx.close_path()
    ctx.set_source_rgb(*(hexc('#8a9a50') if rot else hexc('#7fc241'))); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
    ctx.new_path(); ctx.arc(0, 0, 17, math.pi, 0); ctx.close_path(); ctx.set_source_rgb(*(hexc('#b9bf86') if rot else hexc('#d8ef9a'))); ctx.fill()
    for k in range(4):
        a = math.pi + (k + 1) * math.pi / 5
        line(ctx, [(0, 0), (math.cos(a) * 16, math.sin(a) * 16)], _light(leaf, .55), 1.5)
    ctx.restore()
    ctx.save(); ctx.translate(100, -26); ctx.rotate(0.25)
    ctx.new_path(); ctx.move_to(-22, 0); ctx.curve_to(-6, -9, 10, -4, 24, 4); ctx.curve_to(8, 4, -8, 6, -22, 0)
    ctx.set_source_rgb(*(hexc('#7a4a3a') if rot else hexc('#d63a2a'))); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
    ctx.restore()
    # chopsticks
    for dy in (0, 7):
        line(ctx, [(86, -102 + dy), (170, -30 + dy * 0.5)], INK, 5)
        line(ctx, [(86, -102 + dy), (170, -30 + dy * 0.5)], hexc('#d9b97a') if dy else hexc('#c9a35e'), 2.5)
    if not rot:
        for k, ph in enumerate((0.0, 0.33, 0.66)):
            life = (t * 0.5 + ph) % 1
            _wave(ctx, -40 + k * 40, -130 - life * 14, -170 - life * 54, 6, life * 5 + k * 2, WHITE, 4, 0.7 * (1 - life), 1.0)
    else:
        for k, ph in enumerate((0.0, 0.33, 0.66)):
            life = (t * 0.7 + ph) % 1
            _wave(ctx, -60 + k * 60, -140 - life * 10, -200 - life * 40, 9, life * 6 + k * 2.2 + t * 2, hexc('#6a9a3a'), 4, 0.9 * (1 - life * 0.6), 1.5)
        for k in range(3):
            a = t * (4.0 + k * 1.3) + k * 2.1
            fx = math.cos(a) * (80 + k * 22)
            fy = -190 + math.sin(a * 1.7) * (26 + k * 6) + math.sin(a) * 18
            ellipse(ctx, fx - 6, fy - 7, 7, 4, hexc('#dfe8ee'), a=0.9)
            ellipse(ctx, fx + 6, fy - 7, 7, 4, hexc('#dfe8ee'), a=0.9)
            circle(ctx, fx, fy, 6.2, hexc('#2a2a2e'), INK, 1.5)
            circle(ctx, fx + 2, fy - 1, 1.3, hexc('#c04030'))
    ctx.restore()


def price_board(ctx, x, y, s=1.0, locked=False):
    """Chalk menu board, (x,y) = centre. ~300x220: wood frame, dark green board, 'MENU' title, 4 dishes with prices and
    dotted leaders, chalk ledge. locked=True: two heavy chains crossed over it + padlock in the middle."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    box(ctx, -150 + 6, -110 + 8, 300, 220, (0, 0, 0), 10, None)
    ctx.set_source_rgba(0, 0, 0, .15); ctx.fill()
    box(ctx, -150, -110, 300, 220, WOOD, 10, INK, 3)
    box(ctx, -150, 84, 300, 26, WOOD_D, 8, INK, 3)
    box(ctx, -138, -98, 276, 188, hexc('#2f4a3c'), 6, INK, 3)
    box(ctx, -138, -98, 276, 8, hexc('#3c5c4b'), 4)
    box(ctx, 100, 90, 24, 8, CHALK, 3, INK, 2)
    text(ctx, "MENU", 0, -68, 40, CHALK)
    line(ctx, [(-70, -46), (70, -46)], CHALK, 2.5, .8)
    rows = [("PHO", "25"), ("BUN CHA", "30"), ("BANH MI", "12"), ("COFFEE", "18")]
    for i, (nm, pr) in enumerate(rows):
        yy = -22 + i * 30
        text(ctx, nm, -112, yy, 27, CHALK, "l")
        for k in range(8):
            circle(ctx, 14 + k * 9, yy + 8, 1.4, CHALK, a=.7)
        text(ctx, pr + "k", 118, yy, 27, hexc('#ffd86e'), "r")
    if locked:
        def chain(p0, p1):
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            L = math.hypot(dx, dy); ang = math.atan2(dy, dx)
            n = int(L // 26)
            for i in range(n + 1):
                px, py = lerp(p0[0], p1[0], i / n), lerp(p0[1], p1[1], i / n)
                ctx.save(); ctx.translate(px, py); ctx.rotate(ang)
                if i % 2 == 0:
                    rrect(ctx, -17, -10, 34, 20, 10)
                else:
                    rrect(ctx, -14, -5, 28, 10, 5)
                ctx.set_source_rgb(*INK); ctx.set_line_width(12 if i % 2 == 0 else 11); ctx.stroke_preserve()
                ctx.set_source_rgb(*(STEEL if i % 2 == 0 else STEEL_D)); ctx.set_line_width(6.5 if i % 2 == 0 else 6); ctx.stroke()
                ctx.restore()
        chain((-168, -86), (168, 82))
        chain((168, -86), (-168, 82))
        padlock(ctx, 0, -4, 1.05, None)
    ctx.restore()


# =====================================================================================
def coop_farm(ctx, x, y, s=1.0, t=0.0):
    """Collective barn, (x,y) = bottom centre. ~560x300: red plank walls, gable roof with shingle band, plain cream sign
    'COOPERATIVE', open double doors (dark interior), rice sacks piled on the right, long work-points board (tally grid)
    on the left wall, a hen pecking in front (t)."""
    RED, RED_D, RED_L = hexc('#a8473a'), hexc('#873528'), hexc('#c25c4b')
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 2, 330, 14, (0, 0, 0), a=.16)
    wall = [(-280, 0), (-280, -190), (0, -290), (280, -190), (280, 0)]
    poly(ctx, wall, RED, INK, 3)
    ctx.save(); _path(ctx, wall); ctx.clip()
    for i in range(-14, 15):
        line(ctx, [(i * 20, 0), (i * 20, -300)], RED_D, 2, .9)
    poly(ctx, [(200, 0), (200, -300), (300, -300), (300, 0)], RED_D, None, a=.55)
    box(ctx, -300, -16, 600, 16, RED_D)
    ctx.restore()
    poly(ctx, wall, (0, 0, 0), INK, 3, a=0)
    # roof band (shingle)
    for sd in (-1, 1):
        pts = [(sd * 300, -180), (0, -304), (0, -276), (sd * 276, -168)]
        poly(ctx, pts, hexc('#5a3b2a'), INK, 3)
        for k in range(1, 8):
            f = k / 8
            p0 = (sd * 300 * (1 - f), lerp(-180, -304, f)); p1 = (sd * 276 * (1 - f), lerp(-168, -276, f))
            line(ctx, [p0, p1], hexc('#3e281c'), 2)
        for k in range(0, 4):
            f = k / 4
            line(ctx, [(sd * 300 * (1 - f) * 0.98, lerp(-178, -300, f) + 7), (sd * 276 * (1 - f), lerp(-166, -274, f) - 2)], hexc('#7a5440'), 3, .8)
    # hayloft window
    box(ctx, -26, -262, 52, 42, hexc('#2b1d17'), 4, INK, 3)
    box(ctx, -30, -266, 60, 6, hexc('#e8dcc0'), 2, INK, 2)
    line(ctx, [(0, -262), (0, -220)], hexc('#e8dcc0'), 3); line(ctx, [(-26, -241), (26, -241)], hexc('#e8dcc0'), 3)
    # sign
    box(ctx, -156 + 4, -200 + 5, 312, 40, _dark(CREAM, .35), 6)
    box(ctx, -156, -200, 312, 40, CREAM, 6, INK, 3)
    text(ctx, "COOPERATIVE", 0, -180, 36, hexc('#7a1a20'))
    # door opening
    box(ctx, -72, -150, 144, 150, hexc('#2b1d17'), 0, INK, 3)
    line(ctx, [(-72, -30), (72, -30)], hexc('#1c130f'), 3)
    for bx2, bw in ((-40, 36), (-4, 30), (30, 34)):          # hay / sacks inside
        box(ctx, bx2, -62, bw, 32, hexc('#8a6a3a'), 4, INK, 2)
        line(ctx, [(bx2, -46), (bx2 + bw, -46)], hexc('#5f4824'), 2)
    box(ctx, -72, -156, 144, 8, WOOD_D, 0, INK, 3)
    for sd in (-1, 1):                                      # open leaves, swung outward
        hx = sd * 72
        lf = [(hx, 0), (hx, -150), (hx + sd * 38, -140), (hx + sd * 38, -10)]
        poly(ctx, lf, WOOD, INK, 3)
        poly(ctx, [(hx + sd * 20, -145), (hx + sd * 38, -140), (hx + sd * 38, -10), (hx + sd * 20, -5)], WOOD_D)
        for k in (1, 2):
            line(ctx, [(hx + sd * 38 * k / 3, -150 + 10 * k / 3), (hx + sd * 38 * k / 3, -k * 4)], WOOD_D, 1.8)
        line(ctx, [(hx, -30), (hx + sd * 38, -34)], INK, 4); line(ctx, [(hx, -112), (hx + sd * 38, -108)], INK, 4)
        line(ctx, [(hx + sd * 2, -10), (hx + sd * 36, -136)], WOOD_D, 3)
    # work-points board
    box(ctx, -268 + 4, -144 + 4, 150, 90, _dark(RED, .4), 4)
    box(ctx, -268, -144, 150, 90, hexc('#2f4a3c'), 4, INK, 3)
    box(ctx, -268, -144, 150, 16, CREAM, 4, INK, 2.5)
    text(ctx, "WORK POINTS", -193, -135, 15, hexc('#5a3a28'))
    for r in range(4):
        line(ctx, [(-266, -122 + r * 17), (-120, -122 + r * 17)], CHALK, 1.4, .6)
        for c in range(1, 4):
            pass
        n = (r * 3 + 2) % 5 + 3
        for q in range(n):
            gx = -228 + (q // 5) * 36 + (q % 5) * 6
            line(ctx, [(gx, -118 + r * 17), (gx, -108 + r * 17)], CHALK, 1.6)
            if q % 5 == 4: line(ctx, [(gx - 25, -108 + r * 17), (gx + 3, -118 + r * 17)], CHALK, 1.6)
        line(ctx, [(-228 - 3, -125 + r * 17 + 3), (-228 - 3, -125 + r * 17 + 17)], CHALK, 1.4, .6) if False else None
    line(ctx, [(-236, -128), (-236, -54)], CHALK, 1.4, .7)
    # sacks pile
    rice_sack(ctx, 170, 0, 0.5, "RICE"); rice_sack(ctx, 232, 0, 0.5, "RICE")
    rice_sack(ctx, 200, -62, 0.5, "RICE")
    # hen
    hb = math.sin(t * 5.5) * 0.5 + 0.5
    ctx.save(); ctx.translate(-190, 4)
    ellipse(ctx, 0, 0, 22, 4, (0, 0, 0), a=.2)
    line(ctx, [(-4, -10), (-4, 0)], hexc('#d9902a'), 2.5); line(ctx, [(6, -10), (6, 0)], hexc('#d9902a'), 2.5)
    ellipse(ctx, 0, -22, 20, 15, WHITE)
    poly(ctx, [(-20, -26), (-30, -40), (-14, -32)], hexc('#f4efe0'), INK, 2)
    ellipse(ctx, 2, -20, 12, 8, hexc('#e8e2d2'))
    hx, hy = 20 + hb * 6, -28 + hb * 16
    line(ctx, [(14, -30), (hx - 2, hy)], INK, 9); line(ctx, [(14, -30), (hx - 2, hy)], WHITE, 5)
    circle(ctx, hx, hy, 8, WHITE, INK, 2)
    poly(ctx, [(hx + 6, hy - 2), (hx + 14, hy + 1), (hx + 6, hy + 4)], hexc('#e8a028'), INK, 1.5)
    circle(ctx, hx + 2, hy - 2, 1.4, INK)
    circle(ctx, hx - 2, hy - 8, 3, hexc('#d63a2a'))
    ctx.restore()
    ctx.restore()


def land_deed(ctx, x, y, s=1.0, rot=0.0, name="NGUYEN FAMILY"):
    """Land-use-rights certificate, (x,y) = centre, ~260x340, rotatable. Cream paper, title 'LAND USE RIGHTS', name line,
    green field-sketch box with parcel + rows, text bars, blue signature scribble and a red thumbprint (no seal)."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    box(ctx, -130 + 7, -170 + 9, 260, 340, _dark(PAPER, .35), 6)
    box(ctx, -130, -170, 260, 340, PAPER, 6, INK, 3)
    box(ctx, -120, -160, 240, 320, PAPER, 3, hexc('#b3a273'), 2)
    box(ctx, -114, -154, 228, 308, PAPER, 2, hexc('#cdbf92'), 1.5)
    text(ctx, "LAND USE", 0, -130, 36, hexc('#5a3a28'))
    text(ctx, "RIGHTS", 0, -98, 36, hexc('#5a3a28'))
    line(ctx, [(-90, -76), (90, -76)], hexc('#8a7a50'), 2.5); line(ctx, [(-90, -71), (90, -71)], hexc('#8a7a50'), 1.2)
    text(ctx, "HOLDER", -98, -56, 15, hexc('#8a7a50'), "l")
    text(ctx, name, 0, -38, 26, hexc('#2f2a2a'))
    line(ctx, [(-98, -24), (98, -24)], hexc('#5a4632'), 1.8)
    # field sketch
    box(ctx, -98, -14, 196, 92, hexc('#d9e6b5'), 3, hexc('#5a4632'), 2)
    for k in range(9):
        line(ctx, [(-92 + k * 22, -8), (-92 + k * 22 - 18, 72)], hexc('#a8c27a'), 2)
    parcel = [(-62, 0), (40, -4), (74, 30), (50, 62), (-50, 56), (-78, 26)]
    poly(ctx, parcel, hexc('#b7d58a'), None)
    ctx.new_path(); _path(ctx, parcel); ctx.set_source_rgb(*hexc('#5a4632')); ctx.set_line_width(2.2); ctx.set_dash([6, 4]); ctx.stroke(); ctx.set_dash([])
    for k in range(5):
        line(ctx, [(-56 + k * 22, 8 + k % 2 * 4), (-62 + k * 24, 50)], hexc('#7fa66b'), 1.8)
    box(ctx, 52, 36, 16, 12, hexc('#c49a6c'), 1, INK, 1.5); poly(ctx, [(50, 36), (60, 28), (70, 36)], hexc('#a8473a'), INK, 1.5)
    # text lines
    for k in range(4):
        line(ctx, [(-98, 96 + k * 11), (98 - (k == 3) * 60, 96 + k * 11)], hexc('#8c8068'), 2.4, .7)
    # signature
    pts = [(-92 + i * 4, 152 + math.sin(i * 0.9) * 7 * math.sin(i * 0.17 + 0.3)) for i in range(0, 22)]
    line(ctx, pts, hexc('#2a3f7a'), 2.4)
    line(ctx, [(-96, 158), (-20, 158)], hexc('#5a4632'), 1.5)
    # thumbprint
    ctx.save(); ctx.translate(62, 138); ctx.rotate(-0.25)
    ellipse(ctx, 0, 0, 22, 27, hexc('#b8302a'), a=.9)
    for rr in (4, 9, 14, 19):
        ctx.save(); ctx.scale(1, 1.2); ctx.new_path(); ctx.arc(0, 1, rr, 3.4, 6.1); ctx.restore()
        ctx.set_source_rgb(*hexc('#e8d9c4')); ctx.set_line_width(1.8); ctx.stroke()
    ctx.restore()
    text(ctx, "THUMBPRINT", 62, 170, 11, hexc('#8a7a50')) if False else None
    ctx.restore()


# =====================================================================================
def open_doors(ctx, x, y, w=420, h=520, open_=0.0, label="FDI"):
    """Big double doors in a brick/stone frame, (x,y) = bottom centre. Wall block w x h; opening ~0.62w x 0.74h. open_ 0..1
    swings both leaves outward (each leaf narrows toward its hinge, free edge grows taller); warm light floods the gap
    and spills on the ground. Plank doors with iron bands and studs; plain sign above with label."""
    ox = w * 0.31; oh = h * 0.74
    x0 = x - w / 2
    ctx.save()
    # wall
    box(ctx, x0, y - h, w, h, hexc('#b9ac95'), 0, INK, 3)
    bh = 26
    for r in range(int(h // bh) + 1):
        yy = y - h + r * bh
        line(ctx, [(x0, yy), (x0 + w, yy)], hexc('#8f8470'), 2, .8)
        off = (r % 2) * 40
        for k in range(-1, int(w // 80) + 2):
            bx = x0 + off + k * 80
            if x0 <= bx <= x0 + w:
                line(ctx, [(bx, yy), (bx, yy + bh)], hexc('#8f8470'), 2, .8)
            box(ctx, max(x0, bx + 4), yy + 3, 14, 4, hexc('#d3c8b2'), 1) if x0 <= bx + 4 <= x0 + w - 14 else None
    ctx.rectangle(x0, y - h, w, h); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    # arch-less stone surround
    box(ctx, x - ox - 20, y - oh - 20, ox * 2 + 40, oh + 20, hexc('#cfc4ac'), 0, INK, 3)
    for k in range(int(oh // 50) + 1):
        yy = y - oh - 20 + k * 50
        line(ctx, [(x - ox - 20, yy), (x - ox, yy)], hexc('#9d927c'), 2); line(ctx, [(x + ox, yy), (x + ox + 20, yy)], hexc('#9d927c'), 2)
    # interior light
    lit = clamp(open_ * 1.6)
    inner_c = _mix(hexc('#3b2a22'), hexc('#ffe39a'), lit)
    box(ctx, x - ox, y - oh, ox * 2, oh, inner_c, 0, INK, 3)
    if lit > 0.01:
        ctx.save(); ctx.rectangle(x - ox, y - oh, ox * 2, oh); ctx.clip()
        for k in range(-3, 4):
            ctx.new_path(); ctx.move_to(x + k * 6, y - oh * 0.35)
            ctx.line_to(x + k * 150 - 30, y - oh); ctx.line_to(x + k * 150 + 30, y - oh); ctx.close_path()
            ctx.set_source_rgba(1, 1, 0.85, 0.28 * lit); ctx.fill()
        circle(ctx, x, y - oh * 0.38, ox * 0.55 * lit + 4, hexc('#fff6c8'), a=0.8 * lit)
        ctx.restore()
        # spill on ground
        sp = open_
        poly(ctx, [(x - ox, y), (x + ox, y), (x + ox + 120 * sp, y + 38 * sp), (x - ox - 120 * sp, y + 38 * sp)], hexc('#ffe39a'), None, a=0.5 * sp)
    # leaves
    ang = open_ * 1.30
    for sd in (-1, 1):
        hx = x + sd * ox
        lw_ = ox * math.cos(ang)
        fx = hx - sd * lw_
        fh = oh * (1 + 0.16 * math.sin(ang))
        if open_ > 0.001:
            fx = hx - sd * (lw_ - ox * 0.0)
            # outward swing: free edge swings toward the viewer, away from opening centre side -> leaf sits outside frame
            fx = hx + sd * (ox * math.sin(ang) * 0.55) - sd * 0.0
            # keep leaf visible: it occupies [hx, fx] when open (outside), narrowing as it approaches edge-on
            fx = hx + sd * (ox * math.cos(ang) * 0.0)
        wid = lw_
        # closed: leaf covers hinge->centre. open: leaf folds outward, projected width = ox*cos(ang), drawn outside the frame
        if open_ <= 0.001:
            x_a, x_b = hx, hx - sd * ox
        else:
            x_a, x_b = hx, hx + sd * wid * 0.9
        top_a = y - oh; top_b = y - fh
        pts = [(x_a, y), (x_a, top_a), (x_b, top_b), (x_b, y + (fh - oh) * 0.3)]
        poly(ctx, pts, hexc('#8b5a33'), INK, 3)
        # planks
        npl = 5
        for k in range(1, npl):
            f = k / npl
            xa = lerp(x_a, x_b, f)
            ta = lerp(top_a, top_b, f); ba = lerp(y, y + (fh - oh) * 0.3, f)
            line(ctx, [(xa, ta), (xa, ba)], hexc('#6e4524'), 2.2)
            if k % 2:
                poly(ctx, [(xa, ta), (lerp(x_a, x_b, f + 1 / npl), lerp(top_a, top_b, f + 1 / npl)), (lerp(x_a, x_b, f + 1 / npl), lerp(y, y + (fh - oh) * 0.3, f + 1 / npl)), (xa, ba)], hexc('#a8703f'), None, a=0.55)
        for fy in (0.2, 0.75):
            ya = lerp(top_a, y, fy); yb = lerp(top_b, y + (fh - oh) * 0.3, fy)
            line(ctx, [(x_a, ya), (x_b, yb)], INK, 11); line(ctx, [(x_a, ya), (x_b, yb)], hexc('#4a4e56'), 6)
            for k in range(1, 5):
                f = k / 5
                circle(ctx, lerp(x_a, x_b, f), lerp(ya, yb, f), 3.2, hexc('#9aa0a8'), INK, 1.5)
        # ring handle near free edge
        f = 0.88
        hy_ = lerp(lerp(top_a, y, 0.5), lerp(top_b, y, 0.5), f)
        ctx.new_path(); ctx.arc(lerp(x_a, x_b, f), hy_ + 8, 10 * max(0.3, abs(lw_ / ox)), 0, 6.283); ctx.set_source_rgb(*INK); ctx.set_line_width(5); ctx.stroke_preserve()
        ctx.set_source_rgb(*hexc('#9aa0a8')); ctx.set_line_width(2.5); ctx.stroke()
    # sign
    sw = min(w * 0.7, 300)
    box(ctx, x - sw / 2 + 4, y - h + 28 + 4, sw, 64, _dark(hexc('#cfc4ac'), .4), 6)
    box(ctx, x - sw / 2, y - h + 28, sw, 64, hexc('#2f4a7a'), 6, INK, 3)
    box(ctx, x - sw / 2 + 6, y - h + 34, sw - 12, 52, hexc('#2f4a7a'), 4, _light(hexc('#2f4a7a'), .45), 2)
    text(ctx, label, x, y - h + 61, 54, WHITE)
    ctx.restore()


def tariff_wall(ctx, x, y, w=600, h=360, label="25% TARIFF", build=1.0):
    """Brick wall in running bond, (x,y) = bottom centre. Rows (30px) are laid bottom->top as build goes 0..1 (the top
    row slides in brick by brick). Two brick tones + highlight edge, mortar, white painted label on the finished part."""
    x0 = x - w / 2
    bh, bw = 30, 80
    rows = int(math.ceil(h / bh))
    nbuilt = clamp(build) * rows
    ctx.save()
    ctx.rectangle(x0 - 3, y - h - 3, w + 6, h + 6); ctx.clip()
    mh = min(h, math.ceil(nbuilt) * bh)
    box(ctx, x0, y - mh, w, mh, MORTAR)
    for r in range(rows):
        if r >= nbuilt: break
        frac = clamp(nbuilt - r)
        yy = y - (r + 1) * bh
        off = -(r % 2) * (bw / 2)
        nb = int(w // bw) + 2
        for k in range(nb):
            bx = x0 + off + k * bw
            vis = clamp(frac * nb - k)
            if vis <= 0: continue
            ddy = (1 - ease_out(vis)) * -90 if frac < 1 else 0
            tone = ((r * 7 + k * 3) % 5)
            c = BRICK if tone not in (1, 3) else BRICK_D
            if tone == 4: c = _mix(BRICK, BRICK_L, .45)
            ctx.save(); ctx.translate(0, ddy)
            box(ctx, bx + 2, yy + 2, bw - 4, bh - 4, c, 2)
            box(ctx, bx + 2, yy + 2, bw - 4, 5, _light(c, .22), 2)
            box(ctx, bx + 2, yy + bh - 8, bw - 4, 6, _dark(c, .2), 2)
            line(ctx, [(bx + 14, yy + 14), (bx + 22, yy + 15)], _dark(c, .25), 2, .7) if tone % 2 == 0 else None
            ctx.restore()
    ctx.restore()
    # outline of built part
    built_h = min(h, math.ceil(nbuilt) * bh) if nbuilt >= 1 or build > 0 else 0
    if built_h > 2:
        ctx.rectangle(x0, y - built_h, w, built_h); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    # painted label
    if label and build > 0.55:
        a = clamp((build - 0.55) / 0.3)
        ctx.save(); ctx.translate(x, y - h * 0.5); ctx.rotate(-0.04)
        text(ctx, label, 0, 0, min(w / 6.2, h * 0.34), WHITE, outline=hexc('#7a2a1c'))
        ctx.restore()


# =====================================================================================
def handshake(ctx, x, y, s=1.0, sleeveL=None, sleeveR=None):
    """Two forearms meeting in a firm handshake, (x,y) = centre of the clasp. ~520 wide. Left arm has the sleeveL colour
    (default navy), right arm sleeveR (default dark green); white cuffs, mitten hands with thumbs and finger lines."""
    sleeveL = sleeveL or hexc('#34507f'); sleeveR = sleeveR or hexc('#8a3b3b')
    skin, skin_d, skin_l = hexc('#f2c9a0'), hexc('#d9a77d'), hexc('#f9dcbb')
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    def arm(sd, sc):
        ctx.save(); ctx.scale(sd, 1)             # draw as left arm, mirror for right
        ctx.translate(-30, 0)
        # sleeve
        poly(ctx, [(-330, -86), (-120, -58), (-120, 38), (-330, 80)], sc, INK, 3)
        poly(ctx, [(-330, 40), (-120, 12), (-120, 38), (-330, 80)], _dark(sc, .2))
        for q in range(3):
            line(ctx, [(-250 + q * 40, -74 + q * 4), (-258 + q * 40, 70 - q * 4)], _dark(sc, .22), 2, .7)
        line(ctx, [(-280, -40), (-140, -38)], _light(sc, .25), 5, .8)
        poly(ctx, [(-200, -60), (-190, -60), (-190, 52), (-200, 54)], _dark(sc, .15), None, a=.5)
        # cuff
        poly(ctx, [(-124, -56), (-96, -52), (-96, 24), (-124, 34)], WHITE, INK, 3)
        poly(ctx, [(-112, -54), (-96, -52), (-96, 24), (-112, 30)], hexc('#d9dde2'))
        ctx.restore()
    arm(-1, sleeveR)
    arm(1, sleeveL)
    ctx.save(); ctx.scale(1.25, 1.25)
    # left hand (underneath)
    ctx.new_path(); ctx.move_to(-98, -40); ctx.curve_to(-60, -62, 20, -60, 62, -36); ctx.curve_to(90, -14, 84, 24, 56, 38)
    ctx.curve_to(10, 56, -60, 50, -98, 22); ctx.close_path()
    ctx.set_source_rgb(*skin_d); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    # right hand (on top, from the right)
    ctx.new_path(); ctx.move_to(98, -34); ctx.curve_to(60, -60, -10, -52, -50, -30); ctx.curve_to(-70, -10, -62, 22, -34, 34)
    ctx.curve_to(20, 52, 70, 46, 98, 24); ctx.close_path()
    ctx.set_source_rgb(*skin); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    ctx.new_path(); ctx.move_to(98, -34); ctx.curve_to(60, -60, -10, -52, -50, -30); ctx.curve_to(-30, -44, 40, -42, 98, -12); ctx.close_path()
    ctx.set_source_rgb(*skin_l); ctx.fill()
    # fingers of right hand wrapped over (lines), pointing left
    for k in range(4):
        fy = -30 + k * 17
        ctx.new_path(); ctx.move_to(-44 + k * 3, fy + 2); ctx.curve_to(-20, fy + 8, 10, fy + 12, 30, fy + 8)
        ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
    # thumb of right hand across the top
    ctx.new_path(); ctx.move_to(34, -52); ctx.curve_to(0, -78, -50, -80, -78, -56); ctx.curve_to(-84, -46, -70, -38, -58, -44)
    ctx.curve_to(-34, -52, 0, -50, 22, -34); ctx.close_path()
    ctx.set_source_rgb(*skin); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    ctx.new_path(); ctx.move_to(-76, -58); ctx.curve_to(-66, -50, -64, -48, -58, -46); ctx.set_source_rgb(*skin_d); ctx.set_line_width(2); ctx.stroke()
    # left-hand fingertips peeking beneath on the right side + left thumb curling over the right hand's back
    for k in range(3):
        ellipse(ctx, 78 - k * 2, -4 + k * 17, 10, 8, skin_d)
        ctx.new_path(); ctx.arc(78 - k * 2, -4 + k * 17, 9, 0, 6.283)
        ctx.set_source_rgb(*INK); ctx.set_line_width(2); ctx.stroke()
    ctx.new_path(); ctx.move_to(96, -30); ctx.curve_to(110, -52, 84, -66, 60, -56); ctx.curve_to(70, -50, 80, -44, 82, -36)
    ctx.close_path(); ctx.set_source_rgb(*skin_d); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
    ctx.restore()
    # shake lines
    for sd in (-1, 1):
        for k in range(2):
            line(ctx, [(sd * (150 + k * 16), -112 - k * 10), (sd * (166 + k * 16), -128 - k * 12)], INK, 3, .7)
    ctx.restore()


def fta_scroll(ctx, x, y, s=1.0, label="FTA"):
    """Half-unrolled treaty document, (x,y) = centre, ~340x330. Cream sheet between two wooden rods with turned knobs,
    rolled-up lower part, red ribbon with bow, big plain label, text bars and two signature lines with scribbles."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    # shadow
    box(ctx, -158 + 8, -118 + 10, 316, 230, _dark(PAPER, .4), 3)
    # sheet
    box(ctx, -158, -120, 316, 230, PAPER, 3, INK, 3)
    box(ctx, 90, -120, 68, 230, _dark(PAPER, .08), 0)
    ctx.rectangle(-158, -120, 316, 230); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    # top rod
    box(ctx, -190, -140, 380, 24, WOOD, 12, INK, 3)
    box(ctx, -190, -128, 380, 12, WOOD_D, 6)
    line(ctx, [(-170, -134), (170, -134)], WOOD_L, 3, .9)
    for sd in (-1, 1):
        circle(ctx, sd * 200, -128, 17, WOOD_D, INK, 3)
        circle(ctx, sd * 200, -131, 9, WOOD_L)
    # label
    text(ctx, label, 0, -78, 62, hexc('#7a1a20'))
    line(ctx, [(-110, -48), (110, -48)], hexc('#8a7a50'), 2.5); line(ctx, [(-110, -43), (110, -43)], hexc('#8a7a50'), 1.2)
    for k in range(7):
        line(ctx, [(-120, -26 + k * 14), (120 - (k % 3) * 28 - (k == 6) * 40, -26 + k * 14)], hexc('#8c8068'), 2.6, .75)
    # rolled lower part with rod
    ctx.new_path(); ctx.save(); ctx.translate(0, 122); ctx.scale(1, 0.0001); ctx.restore()
    box(ctx, -160, 90, 320, 56, hexc('#e9dfbc'), 24, INK, 3)
    box(ctx, -160, 112, 320, 34, _dark(PAPER, .14), 17)
    rrect(ctx, -160, 90, 320, 56, 24); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    for k in range(5):
        line(ctx, [(-146, 98 + k * 8), (146, 98 + k * 8)], hexc('#c4b88c'), 2, .8)
    box(ctx, -190, 106, 380, 24, WOOD, 12, INK, 3)
    box(ctx, -190, 118, 380, 12, WOOD_D, 6)
    for sd in (-1, 1):
        circle(ctx, sd * 200, 118, 17, WOOD_D, INK, 3)
        circle(ctx, sd * 200, 115, 9, WOOD_L)
    # signatures (on the sheet above the roll)
    for sx in (-64, 66):
        line(ctx, [(sx - 48, 78), (sx + 48, 78)], hexc('#5a4632'), 1.8)
        pts = [(sx - 42 + i * 4.2, 70 + math.sin(i * 0.8 + sx) * 6 * math.sin(i * 0.2 + 0.3)) for i in range(0, 22)]
        line(ctx, pts, hexc('#2a3f7a'), 2.4)
    # ribbon
    RIB, RIB_D = hexc('#c0392b'), hexc('#8f2a20')
    poly(ctx, [(-14, 82), (14, 82), (14, 156), (0, 146), (-14, 156)], RIB, INK, 3) if False else None
    poly(ctx, [(-8, 130), (-30, 190), (-10, 182), (0, 196), (-2, 140)], RIB_D, INK, 3)
    poly(ctx, [(8, 130), (34, 184), (14, 178), (4, 196), (2, 140)], RIB, INK, 3)
    box(ctx, -18, 88, 36, 58, RIB, 4, INK, 3)
    box(ctx, 4, 88, 14, 58, RIB_D, 3)
    for sd in (-1, 1):
        ctx.new_path(); ctx.move_to(0, 112); ctx.curve_to(sd * 30, 78, sd * 56, 86, sd * 52, 112); ctx.curve_to(sd * 56, 138, sd * 30, 146, 0, 112)
        ctx.set_source_rgb(*RIB if sd < 0 else RIB_D); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    circle(ctx, 0, 112, 9, RIB, INK, 3)
    ctx.restore()


# =====================================================================================
def ladder(ctx, x, y, h=500, missing_from=0.65, s=1.0):
    """Tall wooden ladder, (x,y) = bottom centre. Rails converge slightly toward the top. Rungs exist below the fraction
    missing_from of the height; above it only broken stubs poke out of the rails."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    wb, wt = 150, 118
    def rail_x(sd, yy):
        f = -yy / h
        return sd * lerp(wb, wt, f) / 2
    ellipse(ctx, 0, 2, 100, 9, (0, 0, 0), a=.18)
    n = int(h // 46)
    gap = h / (n + 0.5)
    for sd in (-1, 1):
        pts = [(rail_x(sd, 0), 0), (rail_x(sd, -h), -h)]
        wd = 17
        poly(ctx, [(pts[0][0] - wd / 2, 0), (pts[0][0] + wd / 2, 0), (pts[1][0] + wd / 2 * 0.9, -h), (pts[1][0] - wd / 2 * 0.9, -h)], WOOD, INK, 3)
        poly(ctx, [(pts[0][0] + (0 if sd < 0 else 1) * 0 + wd * 0.1, 0), (pts[0][0] + wd / 2, 0), (pts[1][0] + wd / 2 * 0.9, -h), (pts[1][0] + wd * 0.08, -h)], WOOD_D)
        line(ctx, [(pts[0][0] - wd * 0.28, -4), (pts[1][0] - wd * 0.28, -h + 4)], WOOD_L, 2.5, .9)
        for k in range(6):
            yy = -50 - k * (h / 6.5)
            line(ctx, [(rail_x(sd, yy) - 5, yy), (rail_x(sd, yy) + 5, yy - 7)], WOOD_D, 2)
    for i in range(1, n + 1):
        yy = -i * gap
        xr = rail_x(1, yy)
        if -yy <= h * missing_from:
            box(ctx, -xr, yy - 7, xr * 2, 14, WOOD_L, 3, INK, 3)
            box(ctx, -xr, yy + 1, xr * 2, 6, WOOD, 3)
            for sd in (-1, 1): circle(ctx, sd * (xr - 5), yy, 2.2, INK)
        else:
            for sd in (-1, 1):
                ln = 12 + ((i * 7) % 5) * 3
                x1, x2 = sd * (xr - 8), sd * (xr - 8 - ln)
                poly(ctx, [(x1, yy - 7), (x2, yy - 7 - ((i % 3) - 1) * 2), (x2 - sd * 3, yy - 1), (x2 + sd * 2, yy + 4), (x2, yy + 7), (x1, yy + 7)], WOOD_L, INK, 2.5)
                line(ctx, [(x2 - sd * 1, yy - 4), (x2 + sd * 3, yy + 3)], INK, 1.5)
    ctx.restore()


def pit_trap(ctx, x, y, w=420, label="MIDDLE-INCOME TRAP"):
    """Hole in the ground, (x,y) = centre of the opening at ground level. Grass+earth patch, dark elliptical hole (w wide,
    0.3w tall) with visible inner wall and lit rim, rocks around the rim, and a wooden warning sign on a post (plain label,
    two lines, hazard stripe)."""
    ry = w * 0.15
    ctx.save()
    # ground patch
    ellipse(ctx, x, y + 6, w * 0.74, ry * 1.9, hexc('#5e9447'))
    ellipse(ctx, x, y + 6, w * 0.66, ry * 1.6, hexc('#86b85f'))
    # sign (behind hole)
    px, py = x + w * 0.42, y - ry * 0.55
    line(ctx, [(px, py), (px, py - 190)], INK, 16)
    line(ctx, [(px, py), (px, py - 190)], WOOD, 10)
    line(ctx, [(px + 3, py), (px + 3, py - 190)], WOOD_D, 3)
    ellipse(ctx, px, py + 2, 18, 5, (0, 0, 0), a=.2)
    words = label.split()
    half = (len(words) + 1) // 2
    l1, l2 = " ".join(words[:half]), " ".join(words[half:])
    sw_ = max(w * 0.54, 170)
    ctx.save(); ctx.translate(px - 10, py - 205); ctx.rotate(-0.05)
    box(ctx, -sw_ / 2 + 5, -42 + 6, sw_, 88, _dark(WOOD_D, .4), 5)
    box(ctx, -sw_ / 2, -42, sw_, 88, hexc('#f0d56a'), 5, INK, 3)
    for k in range(int(sw_ // 24) + 1):
        poly(ctx, [(-sw_ / 2 + k * 24, -42), (-sw_ / 2 + k * 24 + 12, -42), (-sw_ / 2 + k * 24 + 4, -30), (-sw_ / 2 + k * 24 - 8, -30)], INK) if -sw_ / 2 + k * 24 + 12 <= sw_ / 2 else None
    line(ctx, [(-sw_ / 2, -30), (sw_ / 2, -30)], INK, 2)
    text(ctx, l1, 0, -8, 32, INK)
    text(ctx, l2, 0, 24, 40, hexc('#a8271e'))
    for sd in (-1, 1): circle(ctx, sd * (sw_ / 2 - 8), 36, 3, INK)
    ctx.restore()
    # hole
    ellipse(ctx, x, y, w / 2 + 14, ry + 8, hexc('#c49a6c'))
    ellipse(ctx, x, y + 3, w / 2 + 8, ry + 4, hexc('#9a7248'))
    ctx.new_path(); ctx.save(); ctx.translate(x, y); ctx.scale(1, ry / (w / 2)); ctx.arc(0, 0, w / 2, 0, 6.283); ctx.restore()
    ctx.set_source_rgb(*hexc('#1f1510')); ctx.fill_preserve()
    ctx.save(); ctx.clip()
    # back inner wall = crescent at the top
    ellipse(ctx, x, y - ry * 0.0, w / 2, ry, hexc('#7a5636'))
    for k in range(-6, 7):
        line(ctx, [(x + k * w / 15, y - ry), (x + k * w / 15 * 1.04, y + ry * 0.5)], hexc('#5e4228'), 3, .9)
    for k in range(4):
        ellipse(ctx, x - w * 0.3 + k * w * 0.2, y - ry * 0.55 + (k % 2) * 6, 14, 6, hexc('#9a7248'))
    ellipse(ctx, x, y + ry * 0.45, w / 2 * 1.02, ry * 1.05, hexc('#1f1510'))
    ellipse(ctx, x, y + ry * 0.62, w / 2 * 0.8, ry * 0.8, hexc('#120b08'))
    ctx.restore()
    ctx.save(); ctx.translate(x, y); ctx.scale(1, ry / (w / 2)); ctx.new_path(); ctx.arc(0, 0, w / 2, 0, 6.283); ctx.restore()
    ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    # rocks on rim
    for rx_, ry_, rw, rh in [(-0.50, 0.05, 36, 20), (-0.38, 0.62, 30, 17), (-0.14, 0.95, 26, 14), (0.22, 0.9, 34, 19), (0.46, 0.38, 28, 16), (0.52, -0.2, 22, 13), (-0.53, -0.38, 24, 14)]:
        cx_, cy_ = x + rx_ * w, y + ry_ * ry * 1.15
        poly(ctx, [(cx_ - rw / 2, cy_ + rh * 0.5), (cx_ - rw * 0.42, cy_ - rh * 0.3), (cx_ - rw * 0.1, cy_ - rh * 0.6), (cx_ + rw * 0.35, cy_ - rh * 0.45), (cx_ + rw / 2, cy_ + rh * 0.1), (cx_ + rw * 0.3, cy_ + rh * 0.55)], hexc('#9aa0a8'), INK, 2.5)
        poly(ctx, [(cx_ + rw * 0.1, cy_ - rh * 0.55), (cx_ + rw * 0.35, cy_ - rh * 0.45), (cx_ + rw / 2, cy_ + rh * 0.1), (cx_ + rw * 0.3, cy_ + rh * 0.55), (cx_ + rw * 0.05, cy_ + rh * 0.4)], hexc('#767c84'))
        line(ctx, [(cx_ - rw * 0.3, cy_ - rh * 0.1), (cx_ - rw * 0.05, cy_ - rh * 0.4)], hexc('#c9ced4'), 2.5)
    ctx.restore()


def smile_curve(ctx, x, y, w=820, h=420, progress=1.0, labels=("R&D", "DESIGN", "ASSEMBLY", "BRAND", "SALES")):
    """Smile-curve chart, (x,y) = top-left of the chart area. Axes with arrowheads and 'VALUE' on the vertical one; a U-shaped
    gold curve drawn left to right with progress 0..1; five dots (first two high left, middle one at the bottom, last two
    high right) pop in as the curve reaches them, labelled in plain text."""
    left, right = x + 70, x + w - 30
    top, bot = y + 70, y + h - 100
    axb = y + h - 28
    ctx.save()
    line(ctx, [(left - 20, axb), (left - 20, y + 6)], CHALK if False else hexc('#2c2f35'), 5)
    poly(ctx, [(left - 20, y - 8), (left - 31, y + 16), (left - 9, y + 16)], hexc('#2c2f35'))
    line(ctx, [(left - 20, axb), (x + w, axb)], hexc('#2c2f35'), 5)
    poly(ctx, [(x + w + 12, axb), (x + w - 12, axb - 11), (x + w - 12, axb + 11)], hexc('#2c2f35'))
    ctx.save(); ctx.translate(left - 44, (y + axb) / 2); ctx.rotate(-math.pi / 2)
    text(ctx, "VALUE", 0, 0, 38, hexc('#2c2f35')); ctx.restore()
    f = lambda u: math.exp(-((u - 0.5) / 0.2) ** 2)
    pos = lambda u: (left + u * (right - left), top + (bot - top) * f(u))
    n = 160
    pr = clamp(progress)
    pts = [pos(min(i / n, pr)) for i in range(int(n * pr) + 2)]
    if len(pts) > 1:
        line(ctx, [(a, b + 5) for a, b in pts], _dark(MAP_D, .15), 14, .5)
        line(ctx, pts, INK, 15)
        line(ctx, pts, MAP_C, 9)
        line(ctx, [(a, b - 2) for a, b in pts], _light(MAP_C, .5), 2.5, .8)
    us = [0.04, 0.2, 0.5, 0.8, 0.96]
    for i, (u, lb) in enumerate(zip(us, labels)):
        if pr < u - 0.001: continue
        k = pop(pr, u, 0.12) if pr < 1 else 1.0
        k = max(k, 0.0) if pr < 1 else 1.0
        px, py = pos(u)
        ctx.save(); ctx.translate(px, py); ctx.scale(k, k)
        circle(ctx, 0, 0, 17, hexc('#c0392b'), INK, 3)
        circle(ctx, -4, -5, 5, hexc('#e8776a'))
        yoff = 44 if i == 2 else -34
        text(ctx, lb, 0, yoff, 34, hexc('#2c2f35'), outline=None)
        ctx.restore()
    ctx.restore()


def golden_key(ctx, x, y, s=1.0, rot=0.0):
    """Ornate gold key, (x,y) = centre, ~240 long, horizontal at rot=0 (bow on the left, bit on the right). Trefoil
    ring bow with centre jewel hole, collared shaft with notched bit, 3 tones (base, shadow, highlight)."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    # shaft
    box(ctx, -60, -9, 170, 18, GOLD, 5, INK, 3)
    box(ctx, -60, 1, 170, 8, GOLD_D, 4)
    line(ctx, [(-52, -4), (104, -4)], GOLD_L, 2.5, .9)
    # collars
    for cx_ in (-52, -34, 4):
        box(ctx, cx_, -17, 12, 34, GOLD, 4, INK, 3)
        box(ctx, cx_ + 6, -15, 5, 30, GOLD_D, 2)
        line(ctx, [(cx_ + 3, -13), (cx_ + 3, 13)], GOLD_L, 2, .9)
    # bit
    bit = [(70, 9), (70, 38), (84, 38), (84, 26), (94, 26), (94, 38), (108, 38), (108, 20), (118, 20), (118, 9)]
    poly(ctx, [(70, -9)] + [(70, 9)] + bit[1:] + [(118, -9)], GOLD, INK, 3)
    poly(ctx, [(94, 12), (94, 38), (108, 38), (108, 12)], GOLD_D)
    line(ctx, [(74, 14), (74, 34)], GOLD_L, 2.5, .9)
    # bow: ring with three lobes (top, bottom, left) and a centre hole
    bx_ = -104
    lobes = ((0, -50), (0, 50), (-52, 0))
    for dx, dy in lobes:
        circle(ctx, bx_ + dx, dy, 22, GOLD, INK, 3)
    circle(ctx, bx_, 0, 40, GOLD, INK, 3)
    for dx, dy in lobes:
        circle(ctx, bx_ + dx, dy, 22, GOLD, None)
        circle(ctx, bx_ + dx, dy, 12, GOLD_D, INK, 2.5)
        circle(ctx, bx_ + dx - 3, dy - 3, 4, GOLD_L)
    circle(ctx, bx_, 0, 40, GOLD, None)
    ctx.new_sub_path(); ctx.arc(bx_, 0, 40, 0, 6.283); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    circle(ctx, bx_, 0, 29, GOLD_D, INK, 2.5)
    circle(ctx, bx_ + 2, 2, 19, hexc('#2b1d17'), INK, 2.5)
    ctx.new_sub_path(); ctx.arc(bx_, 0, 35, math.pi * 1.05, math.pi * 1.55); ctx.set_source_rgb(*GOLD_L); ctx.set_line_width(3.5); ctx.stroke()
    for k in range(8):
        a_ = k * math.pi / 4
        circle(ctx, bx_ + math.cos(a_) * 34.5, math.sin(a_) * 34.5, 1.8, GOLD_L)
    ctx.restore()


def books_cap(ctx, x, y, s=1.0):
    """Stack of three textbooks (MATH, SCIENCE, CODE spines facing us, slightly offset) with a graduation cap on top,
    (x,y) = bottom centre. ~280 wide x ~330 tall. Cream page edges on the right of each book, gold bands, plain labels."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 2, 170, 12, (0, 0, 0), a=.18)
    books = [("MATH", hexc('#3a6fb0'), 270, 0), ("SCIENCE", hexc('#3f9a5a'), 250, -14), ("CODE", hexc('#c0392b'), 235, 12)]
    yy = 0
    for lab, c, bw, off in books:
        bh_ = 56
        top = yy - bh_
        cx_ = off
        box(ctx, cx_ - bw / 2, top, bw, bh_, c, 5, INK, 3)
        box(ctx, cx_ - bw / 2, top + bh_ * 0.62, bw, bh_ * 0.38, _dark(c, .22), 5)
        box(ctx, cx_ - bw / 2, top + 3, bw, 8, _light(c, .22), 4)
        # pages (right side)
        box(ctx, cx_ + bw / 2 - 20, top + 6, 22, bh_ - 12, CREAM, 3, INK, 2.5)
        for k in range(4): line(ctx, [(cx_ + bw / 2 - 17, top + 14 + k * 9), (cx_ + bw / 2 + 0, top + 14 + k * 9)], hexc('#c9b98a'), 1.5)
        # spine bands
        for bx_ in (-bw / 2 + 24, bw / 2 - 48):
            box(ctx, cx_ + bx_, top, 10, bh_, GOLD, 0, INK, 2)
        box(ctx, cx_ - 70, top + 12, 140, 32, CREAM, 4, INK, 2.5)
        text(ctx, lab, cx_, top + 29, 30, hexc('#2c2f35'))
        yy = top
    top_y = yy
    # graduation cap
    ctx.save(); ctx.translate(-4, top_y - 2)
    ctx.new_path(); ctx.move_to(-62, -6); ctx.curve_to(-62, 30, 62, 30, 62, -6); ctx.line_to(62, -30); ctx.line_to(-62, -30); ctx.close_path()
    ctx.set_source_rgb(*hexc('#23272e')); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    poly(ctx, [(20, -30), (62, -30), (62, -6), (36, 8)], hexc('#14161a'), None)
    poly(ctx, [(-120, -42), (0, -76), (120, -42), (0, -8)], hexc('#2f343c'), INK, 3)
    poly(ctx, [(0, -8), (120, -42), (120, -36), (0, 2)], hexc('#14161a'), INK, 2.5)
    poly(ctx, [(-120, -42), (0, -76), (30, -67), (-84, -38)], hexc('#454b55'), None, a=.8)
    circle(ctx, 0, -42, 6, GOLD, INK, 2)
    line(ctx, [(0, -42), (88, -34), (96, -4)], GOLD_D, 3.5)
    for q in range(5): line(ctx, [(96, -4), (92 + q * 2, 30 + (q % 2) * 4)], GOLD, 2.2)
    box(ctx, 91, -8, 12, 10, GOLD, 3, INK, 2)
    ctx.restore()
    ctx.restore()


def rice_heap(ctx, x, y, s=1.0):
    """Heap of white rice, (x,y) = bottom centre. ~300 wide x ~165 tall mound drawn as hundreds of tiny rotated grains
    (loop) over a 2-tone mound (cool grey shadow side), thin ink outline."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ellipse(ctx, 0, 2, 175, 14, (0, 0, 0), a=.16)
    def mound():
        ctx.new_path(); ctx.move_to(-150, 0); ctx.curve_to(-140, -34, -92, -62, -40, -108); ctx.curve_to(-18, -140, 18, -140, 40, -108)
        ctx.curve_to(92, -62, 140, -34, 150, 0); ctx.curve_to(80, 12, -80, 12, -150, 0); ctx.close_path()
    mound(); ctx.set_source_rgb(*hexc('#f7f8f6')); ctx.fill()
    ctx.save(); mound(); ctx.clip()
    poly(ctx, [(34, -150), (170, 20), (-20, 20)], hexc('#dfe3e7'), None, a=.8)
    import random
    rnd = random.Random(7)
    for i in range(520):
        gx = rnd.uniform(-150, 150); gy = rnd.uniform(-140, 8)
        a = rnd.uniform(0, math.pi)
        shade = (gx * 0.5 + (gy + 140) * 0.9) > 130
        ctx.save(); ctx.translate(gx, gy); ctx.rotate(a); ctx.scale(1, 0.42)
        ctx.new_path(); ctx.arc(0, 0, 6.5, 0, 6.283)
        ctx.set_source_rgb(*(hexc('#e4e8ec') if shade else hexc('#ffffff'))); ctx.fill_preserve()
        ctx.restore()
        ctx.save(); ctx.translate(gx, gy); ctx.rotate(a); ctx.scale(1, 0.42)
        ctx.new_path(); ctx.arc(0, 0, 6.5, 0, 6.283); ctx.restore()
        ctx.set_source_rgb(*hexc('#b9c2c9')); ctx.set_line_width(1.1); ctx.stroke()
    ctx.restore()
    mound(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()


# =====================================================================================
_CN = [(91, 50), (91, 28.2), (93.5, 28.6), (95.8, 29.2), (97.3, 28.3), (98.7, 27.6), (98.7, 26.0), (98.1, 24.8), (97.6, 23.9),
       (98.8, 24.1), (99.5, 22.9), (100.1, 21.5), (101.2, 21.2), (101.7, 21.2), (102.14, 22.40), (102.5, 22.75), (103.0, 22.6),
       (103.97, 22.5), (104.5, 22.82), (105.3, 23.35), (106.0, 22.98), (106.7, 22.8), (107.35, 21.8), (108.0, 21.55),
       (108.6, 21.55), (109.1, 21.5), (109.7, 21.4), (110.2, 20.9), (110.4, 20.25), (110.9, 20.7), (111.4, 21.4), (112.4, 21.8),
       (113.5, 22.1), (113.6, 22.5), (114.3, 22.3), (115.2, 22.7), (116.5, 22.9), (117.2, 23.5), (118.1, 24.4), (118.9, 25.0),
       (119.5, 25.9), (120.3, 26.8), (120.8, 27.9), (121.4, 28.6), (121.9, 29.7), (121.4, 30.5), (121.9, 31.0), (121.9, 31.8),
       (121.0, 32.2), (120.7, 33.0), (119.9, 34.3), (119.2, 35.1), (120.3, 36.0), (121.4, 36.7), (122.5, 36.9), (122.7, 37.4),
       (121.6, 37.5), (120.7, 37.8), (119.4, 37.2), (118.9, 37.5), (118.1, 38.1), (117.7, 38.8), (118.9, 39.2), (119.6, 39.9),
       (121.0, 40.8), (121.8, 40.95), (122.3, 40.4), (121.9, 39.8), (121.2, 38.9), (122.5, 39.5), (123.5, 39.7), (124.3, 39.9),
       (125.5, 40.5), (126.5, 41.6), (128.0, 42.0), (129.3, 42.4), (130.6, 42.4), (131.0, 43.0), (131.0, 50)]
_RU = [(130.6, 42.4), (131.9, 43.1), (134.0, 44.4), (136.3, 45.0), (136.3, 47), (131.0, 47), (131.0, 43.0)]
_KR = [(124.3, 39.9), (125.5, 40.5), (126.5, 41.6), (128.0, 42.0), (129.3, 42.4), (130.6, 42.4), (129.8, 41.0), (129.4, 40.0), (128.4, 38.6),
       (129.4, 37.0), (129.5, 35.5), (129.0, 35.0), (127.7, 34.7), (126.4, 34.5), (126.4, 35.4), (126.7, 36.0), (126.2, 36.8),
       (126.6, 37.6), (125.5, 37.7), (125.0, 38.4), (125.3, 39.0), (124.9, 39.6)]
_JP = [
    [(130.9, 34.0), (131.6, 34.4), (132.5, 35.5), (133.5, 35.5), (135.0, 35.7), (136.0, 36.0), (136.8, 37.4), (137.3, 37.0),
     (138.5, 37.4), (139.5, 38.5), (140.0, 39.8), (139.9, 40.6), (140.4, 41.2), (140.9, 41.5), (141.4, 41.3), (141.5, 40.0),
     (142.0, 39.4), (141.9, 38.3), (141.0, 38.0), (140.9, 36.9), (140.8, 35.7), (140.3, 35.0), (139.8, 34.9), (139.0, 35.0),
     (138.8, 34.7), (138.2, 34.6), (137.0, 34.6), (136.9, 34.3), (135.8, 33.5), (135.1, 34.2), (135.3, 34.6), (134.0, 34.4),
     (132.5, 34.1), (131.5, 34.0)],
    [(130.0, 33.6), (131.0, 33.9), (131.7, 33.2), (131.9, 32.5), (131.4, 31.4), (130.7, 31.0), (130.2, 31.3), (130.2, 32.5), (129.8, 33.2)],
    [(132.4, 33.5), (132.9, 34.1), (134.2, 34.3), (134.6, 33.8), (134.0, 33.4), (133.0, 32.8)],
    [(140.1, 41.6), (140.4, 42.7), (140.3, 43.3), (141.5, 43.9), (141.7, 45.4), (141.9, 45.5), (143.5, 44.2), (145.3, 43.4), (144.3, 42.9),
     (143.3, 42.0), (142.0, 42.4), (141.0, 42.6), (140.9, 42.3), (140.6, 41.8)]]
_TW = [(121.5, 25.3), (122.0, 24.9), (121.5, 23.2), (121.0, 22.0), (120.7, 22.0), (120.1, 23.0), (120.2, 23.9), (120.8, 25.0)]
_HN = [(108.7, 19.2), (109.5, 20.0), (110.5, 20.1), (111.0, 19.6), (110.5, 18.5), (109.5, 18.2), (108.7, 18.8)]
_PH = [
    [(120.5, 18.5), (121.9, 18.5), (122.3, 17.0), (122.1, 16.0), (121.6, 15.0), (121.7, 14.2), (122.9, 14.1), (123.8, 13.3), (124.1, 12.7),
     (123.5, 12.8), (122.8, 13.2), (121.8, 13.8), (120.9, 13.8), (120.6, 14.2), (120.55, 14.8), (119.9, 15.7), (120.3, 16.3), (120.35, 17.5)],
    [(122.0, 7.0), (123.0, 8.2), (124.0, 8.6), (125.0, 9.8), (126.0, 9.5), (126.5, 8.0), (126.2, 6.6), (125.5, 5.8), (125.3, 6.8),
     (124.2, 6.2), (123.5, 7.3)],
    [(125.0, 12.5), (125.6, 11.5), (125.2, 10.0), (124.6, 10.6), (124.3, 11.8)],
    [(122.0, 11.5), (123.1, 11.5), (122.6, 10.4), (122.0, 10.6)],
    [(122.9, 10.8), (123.5, 10.2), (123.2, 9.2), (122.6, 9.6)],
    [(117.2, 8.3), (117.5, 8.7), (119.6, 11.4), (119.9, 11.2), (118.2, 9.0)],
    [(120.9, 13.5), (121.5, 13.4), (121.2, 12.4), (120.8, 12.7)]]
_IND = [(91, 28.2), (93.5, 28.6), (95.8, 29.2), (97.3, 28.3), (98.7, 27.6), (98.7, 26.0), (98.1, 24.8), (97.6, 23.9), (98.8, 24.1),
        (99.5, 22.9), (100.1, 21.5), (101.2, 21.2), (101.7, 21.2), (102.14, 22.40)]
_BO = [(109.0, 0.0), (109.0, 1.7), (110.3, 2.2), (111.5, 2.9), (113.0, 3.3), (114.5, 4.6), (115.5, 5.4), (116.7, 6.9), (117.2, 6.8),
       (117.7, 6.1), (118.9, 5.6), (119.3, 5.2), (118.3, 4.4), (117.8, 4.2), (117.6, 3.0), (118.0, 1.8), (117.6, 0.9), (117.5, 0.0)]
_SU = [(95.3, 5.6), (97.5, 5.2), (98.7, 4.0), (99.9, 3.0), (100.5, 2.2), (101.4, 2.0), (101.9, 1.5), (102.8, 0.9), (103.8, 0.0),
       (99.0, 0.0), (98.0, 1.5), (97.2, 2.6), (96.0, 3.8)]


def _indochina():
    vn = _A._VN
    i0 = vn.index((104.5, 10.4))
    west_border = list(reversed(vn[i0:]))                      # (102.3,21.8) ... (104.5,10.4) running south
    pts = list(_IND)
    pts += [(102.3, 21.8), (102.9, 21.4), (103.2, 20.85), (104.25, 20.8), (104.6, 20.3), (104.0, 19.65), (104.2, 19.25), (104.85, 18.8),
            (105.55, 18.15), (106.0, 17.3), (106.6, 16.5), (107.2, 15.9), (107.6, 15.4), (107.5, 14.6), (107.55, 13.4), (107.5, 12.3),
            (106.4, 11.7), (106.15, 11.1), (105.1, 10.9), (104.5, 10.4)]
    pts += [(104.0, 10.4), (103.5, 10.6), (102.9, 11.6), (102.3, 12.2), (101.4, 12.65), (100.9, 13.4), (100.4, 13.5), (100.0, 13.3),
            (100.0, 12.5), (99.8, 11.8), (99.2, 10.5), (99.3, 9.2), (100.0, 8.4), (100.6, 7.2), (101.3, 6.9), (102.2, 6.2), (103.2, 5.2),
            (103.4, 3.8), (104.2, 1.7), (103.5, 1.3), (102.9, 1.8), (102.2, 2.3), (101.3, 3.0), (100.6, 4.3), (100.35, 5.4), (100.0, 6.5),
            (99.5, 7.4), (98.4, 8.4), (98.6, 9.9), (98.5, 11.0), (98.2, 14.0), (97.6, 16.4), (96.9, 16.8), (96.2, 16.8), (95.3, 15.8),
            (94.4, 16.0), (94.3, 17.8), (94.5, 18.5), (93.5, 19.3), (92.9, 20.3), (92.3, 21.4), (91.5, 22.2), (91, 22.3)]
    return pts


def asia_map(ctx, x, y, h=600, highlight="VN", labels=True):
    """Stylized East + Southeast Asia, (x,y) = centre of a rounded sea-blue frame covering lon 92-145 E, lat 0-45 N,
    height h (width ~0.85h). Equirectangular like vietnam_pts(): px/deg lat = h/45, lon scale x0.96. Muted beige land
    polygons (China incl. Shandong + Hainan, Korea, Japan, Taiwan, Philippines, Indochina/Myanmar/Malay peninsula,
    Sumatra tip, Borneo top); Vietnam (vietnam_pts at the same scale) in MAP_C gold. Returns a dict:
    {'proj': f(lon,lat)->(x,y), 'k': px per degree lat, 'frame': (x0,y0,w,h)}; highlight may also be CN/KR/JP/TW/PH."""
    k = h / 45.0; kx = k * 0.96
    fw = 53 * kx
    fx0, fy0 = x - fw / 2, y - h / 2
    lon0, lat1 = 92.0, 45.0
    proj = lambda lo, la: (fx0 + (lo - lon0) * kx, fy0 + (lat1 - la) * k)
    sea, sea_d = hexc('#8cc5de'), hexc('#7bb6d2')
    land, land_d, land_o = hexc('#dccfae'), hexc('#bfb08a'), hexc('#8f8266')
    ctx.save()
    rrect(ctx, fx0, fy0, fw, h, h * 0.045)
    ctx.set_source_rgb(*sea); ctx.fill_preserve(); ctx.save(); ctx.clip()
    for i in range(1, 7):                                           # faint sea latitude/longitude bands
        line(ctx, [(fx0, fy0 + h * i / 7), (fx0 + fw, fy0 + h * i / 7)], sea_d, 2, .6)
    def draw(pts, key=None):
        P = [proj(*p) for p in pts]
        hl = (key is not None and key == highlight)
        poly(ctx, [(a + h * 0.006, b + h * 0.008) for a, b in P], MAP_D if hl else land_d)
        poly(ctx, P, MAP_C if hl else land, INK if hl else land_o, max(1.6, h * 0.003), a=1)
    draw(_RU)
    draw(_indochina(), "IND" if False else None)
    draw(_CN, "CN")
    draw(_KR, "KR")
    for p in _JP: draw(p, "JP")
    draw(_TW, "TW"); draw(_HN, "CN")
    for p in _PH: draw(p, "PH")
    draw(_BO); draw(_SU)
    # Vietnam from the shared outline, matching scale and centre
    kv = h / 45.0
    h_vn = kv * (23.35 - 8.6)
    cvx, cvy = proj(105.8, 15.97)
    vpts = vietnam_pts(cvx, cvy, h_vn)
    hl_vn = (highlight == "VN")
    poly(ctx, [(a + h * 0.006, b + h * 0.008) for a, b in vpts], MAP_D if hl_vn else land_d)
    poly(ctx, vpts, MAP_C if hl_vn else land, INK, max(1.8, h * 0.0035))
    if labels:
        fs = max(14, h * 0.032)
        dark = hexc('#5a4a30')
        def lab(s, lo, la, c=dark, size=fs, rot=0.0):
            px, py = proj(lo, la); text(ctx, s, px, py, size, c, rot=rot)
        lab("CHINA", 108.5, 34.0, size=fs * 1.45)
        lab("KOREA", 127.7, 37.2, size=fs * 0.8, rot=0.0)
        lab("JAPAN", 142.4, 31.6, size=fs * 0.9, c=hexc('#f4f8fa'))
        lab("TAIWAN", 124.3, 22.8, size=fs * 0.75, c=hexc('#f4f8fa'))
        lab("SOUTH CHINA SEA", 114.0, 13.6, c=hexc('#f4f8fa'), size=fs * 1.0, rot=0.0)
        vx, vy = proj(112.2, 17.8)
        a, b = proj(107.0, 16.3)
        line(ctx, [(vx - fs * 1.5, vy + fs * 0.5), (a + h * 0.01, b)], INK, 2.2, .8)
        text(ctx, "VIETNAM", vx, vy, fs * 1.15, hexc('#f4f8fa'), outline=INK)
    ctx.restore()
    rrect(ctx, fx0, fy0, fw, h, h * 0.045)
    ctx.set_source_rgb(*INK); ctx.set_line_width(max(3, h * 0.007)); ctx.stroke()
    ctx.restore()
    return {'proj': proj, 'k': k, 'frame': (fx0, fy0, fw, h)}
