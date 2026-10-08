import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
"""Asset drawing for shots 6-9 (flat vector, INK outlines)."""
from lib import *
import math, random, cairo

def tone(c, k): return tuple(max(0, min(1, v*k)) for v in c)

def serif(ctx, s, x, y, size, c, anchor="c", bold=True):
    ctx.save()
    ctx.select_font_face("DejaVu Serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size); e = ctx.text_extents(s)
    ox = {"c": -e.width/2 - e.x_bearing, "l": 0, "r": -e.width}[anchor]
    ctx.move_to(x+ox, y); ctx.set_source_rgb(*c); ctx.show_text(s); ctx.restore()

# ====================== SHOT 6 ======================
LEAF = [(0, -1.0), (0.10, -0.66), (0.27, -0.76), (0.25, -0.48), (0.58, -0.62), (0.50, -0.30), (1.0, -0.22),
        (0.74, 0.02), (0.84, 0.30), (0.40, 0.22), (0.38, 0.50), (0.07, 0.34)]  # right half incl. 6 tips (top + 5)

def maple_leaf(ctx, x, y, s, c=hexc('#d52b1e'), line_c=None):
    """11-point maple leaf (flag shape); s = half height."""
    right = LEAF
    pts = [(px*s*0.95, py*s) for px, py in right]
    left = [(-px*s*0.95, py*s) for px, py in reversed(right[1:])]
    stem = [(-0.06*s, 0.34*s), (-0.05*s, 1.0*s), (0.05*s, 1.0*s), (0.07*s, 0.34*s)]
    # assemble: top, right side..., (0.07,0.34) stem right, stem bottom, stem left, left side
    outline = pts[:-1] + [(0.07*s, 0.34*s), (0.05*s, 1.0*s), (-0.05*s, 1.0*s), (-0.07*s, 0.34*s)] + left[1:]
    # left list reversed starts with (-0.07,0.34); drop it since stem has it
    outline = [(x+px, y+py) for px, py in outline]
    poly(ctx, outline, c, line_c, 2.5 if line_c else 0)

def pine(ctx, x, base, h, snow=True, c=hexc('#1f5a38')):
    w = h*0.5
    box(ctx, x-h*0.04, base-h*0.14, h*0.08, h*0.14, hexc('#5b3a22'))
    for i in range(3):
        top = base - h*(0.95 - i*0.0) + i*h*0.0
        yb = base - h*0.12 - i*h*0.26
        yt = yb - h*0.46
        ww = w*(1.0 - i*0.27)/2*1.0
        poly(ctx, [(x, yt), (x+ww, yb), (x-ww, yb)], c, INK, 2)
        poly(ctx, [(x, yt), (x+ww, yb), (x+ww*0.15, yb)], tone(c, 0.78))
        if snow:
            poly(ctx, [(x, yt), (x+ww*0.38, yt+(yb-yt)*0.38), (x+ww*0.15, yt+(yb-yt)*0.3), (x, yt+(yb-yt)*0.42),
                       (x-ww*0.2, yt+(yb-yt)*0.32), (x-ww*0.38, yt+(yb-yt)*0.38)], (0.97, 0.98, 1.0))
        poly(ctx, [(x, yt), (x+ww, yb), (x-ww, yb)], None, INK, 2) if False else None

def mountain(ctx, x0, x1, px, py, base, c, snow=True):
    poly(ctx, [(x0, base), (px, py), (x1, base)], c, None)
    poly(ctx, [(px, py), (x1, base), (px+(x1-px)*0.1, base), (px-(px-x0)*0.02, py+(base-py)*0.45)], tone(c, 0.82))
    if snow:
        f = 0.40
        lx, ly = lerp(px, x0, f), lerp(py, base, f)
        rx, ry = lerp(px, x1, f), lerp(py, base, f)
        pts = [(px, py), (rx, ry), (lerp(px, rx, 0.72), ry-18), (lerp(px, rx, 0.45), ry+22), (px+4, ry-20),
               (lerp(px, lx, 0.35), ly+24), (lerp(px, lx, 0.7), ly-14), (lx, ly)]
        poly(ctx, pts, (0.96, 0.98, 1.0))
        poly(ctx, [(px, py), (rx, ry), (lerp(px, rx, 0.72), ry-18), (lerp(px, rx, 0.45), ry+22), (px+4, ry-20)], (0.80, 0.87, 0.95))
    line(ctx, [(x0, base), (px, py), (x1, base)], INK, 2.5)

def airliner(ctx, x, y, s=1.0, flip=False):
    ctx.save(); ctx.translate(x, y); ctx.scale(-s if flip else s, s)
    white = (0.97, 0.97, 0.98); gray = hexc('#c9d1da'); red = hexc('#d63a2f'); dark = hexc('#8a95a3')
    # far wing + far stabiliser
    poly(ctx, [(12, -24), (-28, -26), (-92, -58), (-70, -60)], dark, INK, 2.5)
    poly(ctx, [(-168, -20), (-132, -18), (-150, -40)], dark, INK, 2)
    # tail fin
    poly(ctx, [(-180, -30), (-146, -112), (-116, -112), (-108, -24)], red, INK, 3)
    poly(ctx, [(-180, -30), (-146, -112), (-134, -112), (-160, -26)], tone(red, .82))
    # fuselage
    ctx.new_path(); ctx.move_to(-182, -36); ctx.curve_to(-120, -26, -50, -32, 70, -32)
    ctx.curve_to(135, -32, 180, -14, 186, 5); ctx.curve_to(182, 22, 150, 30, 110, 30)
    ctx.curve_to(0, 32, -100, 22, -184, -10); ctx.close_path()
    ctx.set_source_rgb(*white); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3.5); ctx.stroke()
    # belly shade
    ctx.save(); ctx.new_path(); ctx.move_to(-182, -36); ctx.curve_to(-120, -26, -50, -32, 70, -32)
    ctx.curve_to(135, -32, 180, -14, 186, 5); ctx.curve_to(182, 22, 150, 30, 110, 30)
    ctx.curve_to(0, 32, -100, 22, -184, -10); ctx.close_path(); ctx.clip()
    box(ctx, -200, 12, 420, 30, gray)
    line(ctx, [(-200, 6), (-100, 8), (60, 8), (190, 2)], red, 6)
    ctx.restore()
    # windows
    for i in range(14):
        circle(ctx, -118 + i*14.5, -12, 3.6, hexc('#37506e'))
    poly(ctx, [(128, -20), (162, -14), (166, -6), (132, -8)], hexc('#37506e'), INK, 2)
    # near wing, swept back
    poly(ctx, [(34, 6), (-22, 8), (-118, 66), (-88, 68)], gray, INK, 3)
    poly(ctx, [(-22, 8), (-118, 66), (-104, 66), (-10, 8)], dark)
    # near tailplane
    poly(ctx, [(-170, -8), (-118, 0), (-152, 14)], gray, INK, 2.5)
    # engine on pylon
    poly(ctx, [(-36, 28), (-12, 28), (-14, 44), (-40, 44)], dark, INK, 2)
    ellipse(ctx, -26, 52, 30, 14, white); ellipse(ctx, -26, 52, 30, 14, (0, 0, 0), a=0)
    ctx.new_path(); ctx.save(); ctx.translate(-26, 52); ctx.scale(30, 14); ctx.arc(0, 0, 1, 0, 2*math.pi); ctx.restore()
    ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    ellipse(ctx, 0, 52, 9, 11, hexc('#5c6773')); ellipse(ctx, 0, 52, 4, 6, INK)
    ctx.restore()

def welcome_sign(ctx, x, base):
    """x = center, base = ground y. Roadside sign on two posts."""
    w, h = 400, 190
    top = base - 118 - h
    for px in (x-w*0.32, x+w*0.32):
        box(ctx, px-9, top+h-10, 18, 128, hexc('#7d8794'), 0, INK, 3)
        box(ctx, px-16, base-6, 32, 10, hexc('#6b7480'), 3, INK, 2)
    box(ctx, x-w/2, top, w, h, hexc('#1d4f91'), 16, INK, 4)
    box(ctx, x-w/2+9, top+9, w-18, h-18, None if False else hexc('#1d4f91'), 10, (1, 1, 1), 3)
    # leaf panel
    box(ctx, x-w/2+22, top+26, 120, h-52, (1, 1, 1), 12, INK, 2.5)
    maple_leaf(ctx, x-w/2+82, top+h/2-6, 50, hexc('#d52b1e'), INK)
    text(ctx, "Welcome to", x+62, top+62, 46, (1, 1, 1))
    text(ctx, "Canada", x+62, top+128, 92, (1, 1, 1))
    # small light strip
    box(ctx, x-w/2+8, top-6, w-16, 6, hexc('#12335e'))

def terminal(ctx, x0, x1, base):
    wall = hexc('#e7ebef'); glass = hexc('#7fa6c4')
    top = base - 230
    box(ctx, x0, top, x1-x0, 230, wall, 0, INK, 3)
    box(ctx, x0, top, x1-x0, 26, hexc('#c4ccd4'), 0, INK, 3)
    # glass band
    bx = x0+20
    while bx < x1-60:
        box(ctx, bx, top+56, 62, 120, glass, 0, INK, 2.5)
        box(ctx, bx, top+56, 62, 30, tone(glass, 1.15))
        line(ctx, [(bx+31, top+56), (bx+31, top+176)], INK, 2)
        bx += 72
    # entrance door pair
    # canopy
    box(ctx, x0-10, base-100, x1-x0+60, 14, hexc('#4c5a69'), 0, INK, 3)
    for cx in (x0+40, x1-10, x1+40):
        box(ctx, cx-6, base-86, 12, 86, hexc('#9aa6b2'), 0, INK, 2.5)
    # sign
    box(ctx, x0+40, top-62, 250, 62, hexc('#1f3d7a'), 8, INK, 3)
    text(ctx, "ARRIVALS", x0+150, top-31, 50, (1, 1, 1))
    poly(ctx, [(x0+262, top-45), (x0+262, top-17), (x0+282, top-31)], hexc('#f5c518'), INK, 2)

def rolling_suitcase(ctx, x, ground, t=0):
    """x = center, ground = y of wheel contact. returns handle socket position."""
    w, h = 96, 132
    jit = math.sin(t*38)*0.8
    y0 = ground-16-h + jit
    c = hexc('#c43d3d')
    # wheels
    for wx in (x-w/2+12, x+w/2-12):
        circle(ctx, wx, ground-8, 8, hexc('#2c2f36'), INK, 2.5)
        circle(ctx, wx, ground-8, 3, hexc('#99aaaa'), None)
    box(ctx, x-w/2, y0, w, h, c, 12, INK, 4)
    box(ctx, x-w/2, y0, 22, h, tone(c, .82), 12)
    box(ctx, x-w/2+2, y0+2, w-4, h-4, None if False else c, 11) if False else None
    for gx in (x-12, x+10, x+32):
        line(ctx, [(gx, y0+14), (gx, y0+h-14)], tone(c, .72), 3)
    box(ctx, x-w/2+8, y0+h-34, 30, 20, hexc('#f4e3b0'), 3, INK, 2)  # tag
    box(ctx, x+w/2-2, y0+h*0.55, 9, 26, hexc('#3a3d45'), 3, INK, 2)  # side handle
    # top handle socket
    box(ctx, x+w/2-26, y0-6, 18, 8, hexc('#3a3d45'), 2, INK, 2)
    return (x+w/2-17, y0-6)

def curb_scene(ctx):
    pass

# ====================== SHOT 7 ======================
BUFF = hexc('#e2bd86'); BUFF_D = hexc('#c79a62'); BUFF_L = hexc('#f2d9a8'); TILE = hexc('#c4552f'); TILE_D = hexc('#9c3e22')

def arch_opening(ctx, cx, ybase, w, h, c=hexc('#6c4c34')):
    """round-arched opening: base y, total height h, width w"""
    r = w/2
    ctx.new_path(); ctx.move_to(cx-r, ybase); ctx.line_to(cx-r, ybase-h+r)
    ctx.arc(cx, ybase-h+r, r, math.pi, 2*math.pi); ctx.line_to(cx+r, ybase); ctx.close_path()
    ctx.set_source_rgb(*c); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(2); ctx.stroke()

def tile_roof(ctx, x0, x1, ytop, ybot, overhang=8):
    poly(ctx, [(x0-overhang, ybot), (x0+4, ytop), (x1-4, ytop), (x1+overhang, ybot)], TILE, INK, 2.5)
    n = int((x1-x0)/14)
    for i in range(n+1):
        px = lerp(x0, x1, i/n)
        line(ctx, [(lerp(x0+4, x1-4, i/n), ytop+1), (px + (px-(x0+x1)/2)*0.03, ybot)], TILE_D, 1.6)
    for k in (0.4, 0.75):
        yy = lerp(ytop, ybot, k); line(ctx, [(lerp(x0+4, x0-overhang, k), yy), (lerp(x1-4, x1+overhang, k), yy)], TILE_D, 1.4)
    box(ctx, x0-overhang, ybot, x1-x0+2*overhang, 5, TILE_D, 0, INK, 2)

def arcade(ctx, x0, x1, base, step=52):
    """one wing: arcade on short columns + upper wall + tile roofs. x0<x1"""
    h_arc = 96
    # upper wall + windows
    box(ctx, x0, base-h_arc-58, x1-x0, 58, BUFF, 0, INK, 2.5)
    n = int((x1-x0)/step)
    for i in range(n):
        cx = x0 + (i+0.5)*(x1-x0)/n
        arch_opening(ctx, cx, base-h_arc-12, 14, 34, hexc('#5a4332'))
    tile_roof(ctx, x0, x1, base-h_arc-84, base-h_arc-58, 8)
    # arcade wall
    box(ctx, x0, base-h_arc, x1-x0, h_arc, BUFF_D, 0, INK, 2.5)
    for i in range(n):
        bx = x0 + i*(x1-x0)/n; bw = (x1-x0)/n
        cx = bx + bw/2
        arch_opening(ctx, cx, base-6, bw-26, h_arc-16, hexc('#5a4332'))
        # arch keystone ring
        ctx.new_path(); ctx.arc(cx, base-6-(h_arc-16)+(bw-26)/2, (bw-26)/2+4, math.pi, 2*math.pi)
        ctx.set_source_rgb(*BUFF_L); ctx.set_line_width(4); ctx.stroke()
    # roof slab over arcade + columns
    box(ctx, x0-4, base-h_arc-8, x1-x0+8, 12, BUFF_L, 0, INK, 2.5)
    for i in range(n+1):
        cx = x0 + i*(x1-x0)/n
        box(ctx, cx-6, base-h_arc+4, 12, h_arc-4, BUFF_L, 0, INK, 2)
        box(ctx, cx-9, base-h_arc+2, 18, 6, BUFF, 0, INK, 1.5)
        box(ctx, cx-9, base-8, 18, 8, BUFF, 0, INK, 1.5)
    box(ctx, x0-4, base-2, x1-x0+8, 6, hexc('#b8a37e'), 0, INK, 2)  # plinth

def church_facade(ctx, cx, base):
    W_ = 250
    x0, x1 = cx-W_/2, cx+W_/2
    # lantern/tower behind gable
    box(ctx, cx-52, base-420, 104, 120, BUFF, 0, INK, 3)
    box(ctx, cx-52, base-420, 22, 120, BUFF_D)
    for dx in (-30, 0, 30):
        arch_opening(ctx, cx+dx, base-322, 16, 54, hexc('#4a3626'))
    box(ctx, cx-60, base-430, 120, 12, BUFF_L, 0, INK, 2.5)
    poly(ctx, [(cx-62, base-428), (cx, base-486), (cx+62, base-428)], TILE, INK, 3)
    poly(ctx, [(cx, base-486), (cx+62, base-428), (cx+10, base-428)], TILE_D)
    line(ctx, [(cx, base-486), (cx, base-508)], INK, 3); line(ctx, [(cx-8, base-498), (cx+8, base-498)], INK, 3)
    # main block
    box(ctx, x0, base-300, W_, 300, BUFF, 0, INK, 3)
    box(ctx, x1-34, base-300, 34, 300, BUFF_D)           # shadow side
    box(ctx, x0, base-300, 12, 300, BUFF_L)
    # gable
    poly(ctx, [(x0-14, base-292), (cx, base-366), (x1+14, base-292)], BUFF, INK, 3)
    poly(ctx, [(cx, base-366), (x1+14, base-292), (cx+20, base-292)], BUFF_D)
    line(ctx, [(x0-14, base-292), (cx, base-366), (x1+14, base-292)], TILE, 8)
    line(ctx, [(x0-14, base-292), (cx, base-366), (x1+14, base-292)], INK, 2)
    # rose window in gable
    circle(ctx, cx, base-322, 15, BUFF_L, INK, 2.5); circle(ctx, cx, base-322, 8, hexc('#4a7aa8'), INK, 2)
    # cornice
    box(ctx, x0-8, base-296, W_+16, 12, BUFF_L, 0, INK, 2.5)
    # mosaic band
    my0, mh = base-282, 74
    box(ctx, x0+10, my0-6, W_-20, mh+12, BUFF_D, 0, INK, 2.5)
    box(ctx, x0+16, my0, W_-32, mh, hexc('#e9b52c'), 0, INK, 2)
    # sky-blue and green strips
    box(ctx, x0+16, my0+mh-14, W_-32, 14, hexc('#4c9a5a'))
    cols = [hexc('#2f5fa8'), hexc('#c8382f'), hexc('#2f8f5a'), hexc('#7a3f9a'), hexc('#f4efe0'), hexc('#2f5fa8'), hexc('#c8382f'), hexc('#2f8f5a'), hexc('#7a3f9a')]
    n = 9; sx0 = x0+30; sp = (W_-60)/(n-1)
    for i in range(n):
        fx = sx0 + i*sp; central = (i == n//2)
        hh = 52 if central else 42
        c = hexc('#2f5fa8') if central else cols[i]
        poly(ctx, [(fx-8 - (3 if central else 0), my0+mh-14), (fx-5, my0+mh-14-hh), (fx+5, my0+mh-14-hh), (fx+8+(3 if central else 0), my0+mh-14)], c, INK, 1.5)
        circle(ctx, fx, my0+mh-14-hh-7, 6.5, hexc('#f2c9a0'), INK, 1.5)
        circle(ctx, fx, my0+mh-14-hh-7, 10, hexc('#fff3b0'), None, a=.0)
        if central: circle(ctx, fx, my0+mh-14-hh-7, 11, (1, 1, 1), hexc('#c8382f'), 2, a=.55)
        # arms
        line(ctx, [(fx-5, my0+mh-14-hh+10), (fx-12, my0+mh-14-hh+24)], INK, 1.5)
        line(ctx, [(fx+5, my0+mh-14-hh+10), (fx+12, my0+mh-14-hh+24)], INK, 1.5)
    # pilasters on both sides of entrance
    ay = base-4
    for sd in (-1, 1):
        box(ctx, cx+sd*86-9, base-206, 18, 206, BUFF_L, 0, INK, 2)
        box(ctx, cx+sd*86-12, base-210, 24, 8, BUFF, 0, INK, 2)
    # grand arch: concentric
    ycen = base-132
    for r, c in ((72, BUFF_L), (62, BUFF_D), (53, BUFF_L)):
        ctx.new_path(); ctx.move_to(cx-r, base-4); ctx.line_to(cx-r, ycen); ctx.arc(cx, ycen, r, math.pi, 2*math.pi); ctx.line_to(cx+r, base-4); ctx.close_path()
        ctx.set_source_rgb(*c); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(2); ctx.stroke()
    ctx.new_path(); ctx.move_to(cx-44, base-4); ctx.line_to(cx-44, ycen); ctx.arc(cx, ycen, 44, math.pi, 2*math.pi); ctx.line_to(cx+44, base-4); ctx.close_path()
    ctx.set_source_rgb(*hexc('#4a2f22')); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
    # doors
    box(ctx, cx-36, base-92, 33, 88, hexc('#6d4630'), 0, INK, 2); box(ctx, cx+3, base-92, 33, 88, hexc('#6d4630'), 0, INK, 2)
    arch_opening(ctx, cx, base-90, 72, 32, hexc('#9fc3d8')) if False else None
    ctx.new_path(); ctx.arc(cx, base-92, 36, math.pi, 2*math.pi); ctx.close_path(); ctx.set_source_rgb(*hexc('#8fb7d2')); ctx.fill_preserve()
    ctx.set_source_rgb(*INK); ctx.set_line_width(2); ctx.stroke()
    line(ctx, [(cx, base-128), (cx, base-92)], INK, 2)
    # steps
    for i in range(3):
        box(ctx, cx-92-i*10, base-6+i*6, 184+i*20, 7, [BUFF_L, BUFF, BUFF_D][i], 0, INK, 2)
    # side windows
    for sd in (-1, 1):
        for dy in (0,):
            arch_opening(ctx, cx+sd*108, base-96, 20, 74, hexc('#4a3626'))

def palm(ctx, x, base, h, lean=0, t=0, seed=1):
    rnd = random.Random(seed)
    sway = math.sin(t*1.3+seed)*4
    topx, topy = x+lean+sway, base-h
    # trunk: tapered curved
    n = 14
    left, right = [], []
    for i in range(n+1):
        k = i/n
        px = lerp(x, topx, k*k) ; py = lerp(base, topy, k)
        wdt = lerp(15, 8, k)
        left.append((px-wdt, py)); right.append((px+wdt, py))
    poly(ctx, left+right[::-1], hexc('#a98a62'), INK, 2.5)
    poly(ctx, [(px+ (rx-px)*0.1, py) for (px, py), (rx, _) in zip([( (l[0]+r[0])/2, l[1]) for l, r in zip(left, right)], right)] + right[::-1], hexc('#8c6f4c'))
    for i in range(1, n):
        l, r = left[i], right[i]
        line(ctx, [l, ((l[0]+r[0])/2, l[1]+5), r], hexc('#6c5237'), 2)
    # crown
    for k in range(10):
        ang = math.radians(-170 + k*(160/9)) + math.sin(t*1.5+k+seed)*0.03
        L = 120 + (k % 3)*14
        dx, dy = math.cos(ang), math.sin(ang)
        ex, ey = topx+dx*L, topy+dy*L*0.55+ (L*0.45 if abs(dx) > .5 else 0)
        mx, my = topx+dx*L*0.55, topy+dy*L*0.55-26
        nx, ny = -(ey-topy), (ex-topx)
        nl = math.hypot(nx, ny) or 1; nx, ny = nx/nl*13, ny/nl*13
        col = hexc('#2f8f4a') if k % 2 else hexc('#3fa65a')
        poly(ctx, [(topx, topy), (mx+nx, my+ny), (ex, ey), (mx-nx, my-ny)], col, INK, 2)
        line(ctx, [(topx, topy), (mx, my), (ex, ey)], tone(col, .7), 2)
    circle(ctx, topx, topy+4, 11, hexc('#6c4a2c'), INK, 2)
    circle(ctx, topx-9, topy+14, 7, hexc('#6c4a2c'), INK, 2); circle(ctx, topx+9, topy+14, 7, hexc('#6c4a2c'), INK, 2)

def calendar_post(ctx, x, base, t, flip_at, flip_dur=0.4, day_a="DAY 1", day_b="DAY 2"):
    """tear-off calendar on a wooden post. x center, base ground y. page hinged at top."""
    bw, bh = 200, 170
    top = base - 130 - bh
    box(ctx, x-8, top+bh-10, 16, 140, hexc('#8a5a2b'), 0, INK, 3)
    box(ctx, x-30, base-8, 60, 10, hexc('#6f4a24'), 3, INK, 2)
    # backing board
    box(ctx, x-bw/2-8, top-8, bw+16, bh+16, hexc('#7a5230'), 8, INK, 3)
    def page(label, sy=1.0, c=(1, 1, 1)):
        ctx.save(); ctx.translate(x, top); ctx.scale(1, sy)
        box(ctx, -bw/2, 0, bw, bh, c, 4, INK, 3)
        box(ctx, -bw/2, 0, bw, 44, hexc('#d63a2f'), 4, INK, 3)
        for rx in (-50, 50): circle(ctx, rx, 12, 7, hexc('#3b2a1f'), INK, 2)
        text(ctx, label, 0, 106, 76, hexc('#1f2a44'))
        text(ctx, "Sept 1995", 0, 24, 26, (1, 1, 1))
        ctx.restore()
    f = clamp((t-flip_at)/flip_dur)
    page(day_b, 1.0, hexc('#fff7d6'))
    if f < 1:
        sy = 1 - ease_io(f)
        page(day_a, max(sy, 0.001))
        if 0 < f < 1:
            # curl shadow under flipping page
            box(ctx, x-bw/2, top + bh*sy, bw, 6, (0, 0, 0), 0)

# ====================== SHOT 8 ======================
def night_window(ctx, x, y, w, h, t=0):
    box(ctx, x-10, y-10, w+20, h+20, hexc('#cfc9bb'), 6, INK, 3)
    box(ctx, x, y, w, h, hexc('#15213f'))
    ctx.save(); rrect(ctx, x, y, w, h, 0); ctx.clip()
    # far buildings
    rnd = random.Random(4); bx = x-10
    while bx < x+w:
        bw = rnd.randint(50, 80); bh = rnd.randint(50, 100)
        box(ctx, bx, y+h-bh-30, bw-6, bh+30, hexc('#232f55'))
        for wy in range(int(y+h-bh-18), int(y+h-40), 20):
            for wx in range(int(bx+8), int(bx+bw-16), 16):
                if rnd.random() < .35: box(ctx, wx, wy, 8, 10, hexc('#f1c75a'))
        bx += bw
    box(ctx, x, y+h-34, w, 34, hexc('#2c3350'))       # street
    box(ctx, x, y+h-36, w, 6, hexc('#4a5272'))        # kerb
    for dx in range(0, int(w), 60): box(ctx, x+dx+10, y+h-14, 30, 4, hexc('#8a90a8'))
    # street lamp
    lx = x + w*0.72
    box(ctx, lx-4, y+h-150, 8, 120, hexc('#3b4258'), 0, INK, 2)
    line(ctx, [(lx, y+h-150), (lx-26, y+h-150)], hexc('#3b4258'), 6)
    ellipse(ctx, lx-26, y+h-146, 70, 62, hexc('#ffe08a'), a=.18)
    ellipse(ctx, lx-26, y+h-146, 38, 34, hexc('#ffe08a'), a=.28)
    box(ctx, lx-42, y+h-156, 24, 10, hexc('#2e3448'), 4, INK, 2)
    ellipse(ctx, lx-30, y+h-143, 11, 5, hexc('#fff3b0'))
    poly(ctx, [(lx-38, y+h-142), (lx-22, y+h-142), (lx+10, y+h-34), (lx-70, y+h-34)], hexc('#ffe08a'), None, 0, a=.12)
    # stars
    for (sx, sy) in ((0.1, 0.1), (0.35, 0.22), (0.55, 0.08), (0.9, 0.2), (0.2, 0.35)):
        circle(ctx, x+w*sx, y+h*sy, 2, (1, 1, 1), a=.8)
    ctx.restore()
    line(ctx, [(x+w/2, y), (x+w/2, y+h)], hexc('#cfc9bb'), 8); line(ctx, [(x, y+h*0.45), (x+w, y+h*0.45)], hexc('#cfc9bb'), 8)
    box(ctx, x-18, y+h+8, w+36, 12, hexc('#bdb6a6'), 3, INK, 3)

def office_door(ctx, x, base, h=330, w=160):
    top = base-h
    box(ctx, x-10, top-10, w+20, h+10, hexc('#8d8678'), 0, INK, 3)
    box(ctx, x, top, w, h, hexc('#a9774a'), 0, INK, 3)
    box(ctx, x+16, top+22, w-32, 110, hexc('#94653b'), 3, INK, 2)
    box(ctx, x+16, top+150, w-32, 150, hexc('#94653b'), 3, INK, 2)
    circle(ctx, x+w-18, top+h*0.55, 8, hexc('#d9c46a'), INK, 2)
    # paper sign
    ctx.save(); ctx.translate(x+w/2, top+70); ctx.rotate(-0.04)
    box(ctx, -52, -34, 104, 68, (1, 1, 1), 2, INK, 2.5)
    box(ctx, -60, -42, 18, 8, hexc('#e8d9a0'), 0, None); box(ctx, 42, -42, 18, 8, hexc('#e8d9a0'), 0, None)
    text(ctx, "Zip2", 0, 0, 56, hexc('#1f2a44'))
    ctx.restore()

def chair_with_towel(ctx, x, floor_y, seat_y):
    """office chair; x = center of backrest-side. towel hangs over backrest."""
    dk = hexc('#3a3f4e')
    # base star + pole + wheels
    box(ctx, x+60-5, seat_y+10, 10, floor_y-seat_y-24, hexc('#555b6b'), 0, INK, 2)
    line(ctx, [(x+10, floor_y-14), (x+60, floor_y-24), (x+110, floor_y-14)], dk, 8)
    for wx in (x+10, x+110): circle(ctx, wx, floor_y-8, 7, hexc('#22252e'), INK, 2)
    # seat
    box(ctx, x-4, seat_y, 140, 16, hexc('#4a5066'), 8, INK, 3)
    # back
    box(ctx, x-14, seat_y-190, 34, 196, hexc('#4a5066'), 12, INK, 3)
    box(ctx, x-14, seat_y-190, 12, 196, tone(hexc('#4a5066'), .8), 12)
    # towel draped over the top
    tc = hexc('#4fb3c4')
    top = seat_y-190
    poly(ctx, [(x-34, top-4), (x+36, top-6), (x+40, top+86), (x+22, top+92), (x+16, top+30), (x-22, top+30), (x-24, top+112), (x-40, top+108)], tc, INK, 2.5)
    for ty in (top+20, top+56):
        line(ctx, [(x-24, ty+2), (x-40, ty)], (1, 1, 1), 3, .8)
    line(ctx, [(x-30, top+42), (x-24, top+42)], (1, 1, 1), 3)
    # note pinned on towel hanging in front (left of back)
    ctx.save(); ctx.translate(x-64, top+80); ctx.rotate(0.08)
    box(ctx, -42, -26, 84, 52, hexc('#fff3a0'), 2, INK, 2.5)
    text(ctx, "YMCA", 0, -8, 24, hexc('#2a2a2a'))
    text(ctx, "showers", 0, 12, 24, hexc('#2a2a2a'))
    circle(ctx, 0, -26, 4, hexc('#d63a2f'), INK, 1.5)
    ctx.restore()

def crt_side(ctx, x, desk_y, t=0):
    """CRT monitor in side profile, screen faces LEFT. x = center of the unit, desk_y = desk surface y.
    returns screen face centre (sx, sy)."""
    beige = hexc('#d9d3bf'); beige_d = hexc('#b8b19b')
    # stand
    box(ctx, x-52, desk_y-14, 100, 14, beige_d, 4, INK, 3)
    box(ctx, x-34, desk_y-30, 60, 18, beige, 3, INK, 3)
    # tube back (tapered)
    poly(ctx, [(x-30, desk_y-205), (x+30, desk_y-190), (x+76, desk_y-146), (x+76, desk_y-70), (x+30, desk_y-34), (x-30, desk_y-44)], beige, INK, 4)
    poly(ctx, [(x+30, desk_y-190), (x+76, desk_y-146), (x+76, desk_y-70), (x+30, desk_y-34)], beige_d)
    for vy in range(-170, -80, 14): line(ctx, [(x+40, desk_y+vy*0.9-10), (x+66, desk_y+vy*0.9-10)], tone(beige_d, .7), 3)
    # front bezel (thin slab, screen pointing left)
    poly(ctx, [(x-30, desk_y-205), (x-52, desk_y-198), (x-52, desk_y-50), (x-30, desk_y-44)], beige, INK, 4)
    # screen edge visible (glowing sliver)
    poly(ctx, [(x-52, desk_y-190), (x-44, desk_y-186), (x-44, desk_y-62), (x-52, desk_y-58)], hexc('#5ec8ff'), None)
    # cable
    ctx.new_path(); ctx.move_to(x+76, desk_y-100); ctx.curve_to(x+110, desk_y-90, x+100, desk_y-10, x+120, desk_y); ctx.set_source_rgb(*INK); ctx.set_line_width(4); ctx.stroke()
    return (x-52, desk_y-124)

def keyboard_side(ctx, x, desk_y):
    """side-ish keyboard (wedge) on desk, x = centre"""
    poly(ctx, [(x-70, desk_y), (x+70, desk_y), (x+66, desk_y-10), (x-62, desk_y-16)], hexc('#cfc9b4'), INK, 3)
    for i in range(8):
        kx = x-58+i*16
        box(ctx, kx, desk_y-20+i*0.3, 11, 5, hexc('#9b9582'), 1, INK, 1)

def beanbag(ctx, x, base, w=230, h=120, c=hexc('#c0562f')):
    ctx.new_path(); ctx.move_to(x-w/2, base); ctx.curve_to(x-w/2-10, base-h*0.9, x-w*0.2, base-h*1.15, x, base-h*1.1)
    ctx.curve_to(x+w*0.25, base-h*1.1, x+w/2+10, base-h*0.8, x+w/2, base)
    ctx.curve_to(x+w*0.2, base+10, x-w*0.2, base+10, x-w/2, base); ctx.close_path()
    ctx.set_source_rgb(*c); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(4); ctx.stroke()
    ellipse(ctx, x-w*0.2, base-h*0.7, 40, 18, tone(c, 1.18), a=.9)

def blanket(ctx, x0, y0, w, h, c=hexc('#3c7a5a')):
    ctx.new_path(); ctx.move_to(x0, y0+10); ctx.curve_to(x0+w*.3, y0-8, x0+w*.7, y0+14, x0+w, y0)
    ctx.line_to(x0+w-6, y0+h); ctx.curve_to(x0+w*.6, y0+h+10, x0+w*.3, y0+h-4, x0+4, y0+h+4); ctx.close_path()
    ctx.set_source_rgb(*c); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3.5); ctx.stroke()
    for k in range(1, 4):
        line(ctx, [(x0+w*k/4, y0+4), (x0+w*k/4-4, y0+h)], tone(c, .75), 3)

def zzz(ctx, x, y, t):
    for i in range(3):
        k = ((t*0.6 - i*0.33) % 1.0)
        a = 1 - k
        sz = 30 + i*8 + k*10
        zx = x + math.sin(k*5 + i)*8 + k*20 + i*6
        zy = y - k*95
        text(ctx, "z", zx, zy, sz, tuple(lerp(0.35, 1, k) if False else 1 for _ in range(3)), outline=INK) if a > 0.15 else None

# ====================== SHOT 9 ======================
def big_check(ctx, w, h, amount, payto=None, company="Compaq"):
    """check centered on origin"""
    box(ctx, -w/2, -h/2, w, h, hexc('#f6f0d8'), 6, INK, 4)
    box(ctx, -w/2+8, -h/2+8, w-16, h-16, None if False else hexc('#f6f0d8'), 4, hexc('#4c9a5a'), 3)
    # engraved band
    for i in range(5):
        line(ctx, [(-w/2+16, -h/2+22+i*3), (w/2-16, -h/2+22+i*3)], hexc('#cfe4c8'), 1.5)
    if payto:
        text(ctx, payto, -w/2+20, -h/2+36, 26, hexc('#1f2a44'), anchor="l")
        text(ctx, amount, 0, 10, 46, hexc('#1f6b3a'))
    else:
        text(ctx, company, -w/2+20, -h/2+34, 34, hexc('#1f2a44'), anchor="l")
        text(ctx, amount, 0, 6, 62, hexc('#1f6b3a'))
    line(ctx, [(w/2-130, h/2-22), (w/2-24, h/2-22)], INK, 2)
    text(ctx, "~ signed", w/2-78, h/2-32, 18, hexc('#444444'))
    circle(ctx, -w/2+34, h/2-30, 14, hexc('#e9b52c'), INK, 2)

def banknote(ctx, x, y, rot, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    box(ctx, -34, -17, 68, 34, hexc('#7fc77a'), 4, hexc('#2f7a3a'), 2.5)
    circle(ctx, 0, 0, 9, hexc('#a6dfa0'), hexc('#2f7a3a'), 2)
    text(ctx, "$", 0, 0, 18, hexc('#2c6e33'))
    ctx.restore()
def coin(ctx, x, y, s=1.0, ph=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(abs(math.cos(ph))*0.9+0.1, 1);
    circle(ctx, 0, 0, 12*s, hexc('#f2c230'), hexc('#a8760f'), 2.5); circle(ctx, 0, 0, 7*s, hexc('#ffe27a'), None)
    ctx.restore()
def money_rain(ctx, t, t0, seed=5, n=34, ymax=H+40):
    rnd = random.Random(seed)
    for i in range(n):
        x0 = rnd.uniform(20, W-20); delay = rnd.uniform(0, 1.0); v = rnd.uniform(240, 360)
        rot0 = rnd.uniform(-1, 1); sp = rnd.uniform(-2, 2); sw = rnd.uniform(14, 40); kind = rnd.random() < 0.28
        tt = t - t0 - delay
        if tt < 0: continue
        y = -50 + tt*v
        y = (y % (ymax+90)) - 50 if tt*v > ymax else y
        x = x0 + math.sin(tt*2.2+i)*sw
        if kind: coin(ctx, x, y, 1.0, tt*6+i)
        else: banknote(ctx, x, y, rot0 + tt*sp + math.sin(tt*3+i)*0.4, 1.0)
