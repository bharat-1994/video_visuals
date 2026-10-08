import math, random
from lib import *

def L2(a, b, k): return (lerp(a[0], b[0], k), lerp(a[1], b[1], k))

# ---------------- shot 6 ----------------
def shot6(ctx, t, dur):
    bg_sunset(ctx)
    k = t/dur
    ctx.save(); camera(ctx, lerp(1.0, 1.08, ease_io(k)), lerp(600, 680, ease_io(k)), 360)
    circle(ctx, 640, 400, 125, hexc('#ffd36b'))
    for (pts, c) in [([(-200, 460), (130, 150), (460, 460)], hexc('#8a4a6b')),
                     ([(300, 470), (700, 90), (1100, 470)], hexc('#6b3560')),
                     ([(800, 470), (1130, 180), (1500, 470)], hexc('#8a4a6b')),
                     ([(-100, 520), (330, 280), (760, 520)], hexc('#4a2748')),
                     ([(650, 520), (1040, 300), (1450, 520)], hexc('#4a2748'))]:
        poly(ctx, pts, c)
    box(ctx, -300, 520, 1900, 300, hexc('#2f1c36'))
    # sign
    sx = 1010
    box(ctx, sx-8, 440, 16, 100, hexc('#7a4a25'), 0, INK, 3)
    poly(ctx, [(sx-110, 400), (sx+80, 400), (sx+120, 430), (sx+80, 460), (sx-110, 460)], hexc('#c48a4f'), INK, 4)
    text(ctx, "CANADA", sx-12, 431, 38, INK)
    text(ctx, "→", sx+78, 431, 30, INK)
    # elon
    p = cast("elon_teen", 0.78)
    ex = lerp(180, 640, ease_io(k*0.95))
    wy = 478
    ph = t*1.6
    sw = math.sin(ph*2*math.pi)
    armL = (-25-12*sw, 115)
    armR = (30, 105)
    info = p.draw(ctx, ex, wy, t, "determined", facing=0.9, armL=armL, armR=armR, walk=ph)
    hx, hy = info['handR']
    # suitcase hangs from hand
    ctx.save(); ctx.translate(hx, hy); ctx.rotate(0.05*sw)
    box(ctx, -14, 18, 28, 8, hexc('#4a2c14'), 3)
    box(ctx, -48, 24, 96, 70, hexc('#a0602f'), 8, INK, 4)
    box(ctx, -48, 54, 96, 6, hexc('#6b3f1d'))
    box(ctx, -8, 52, 16, 12, hexc('#e0b94a'), 2, INK, 2)
    ctx.restore()
    ctx.restore()
    text(ctx, "1989 · Age 17", 50, 70, 54, (1, 1, 1), anchor="l", reveal=clamp(t/1.0), outline=INK)

# ---------------- shot 7 ----------------
def shot7(ctx, t, dur):
    bg_flat(ctx, hexc('#2b3a67'))
    k = t/dur
    ctx.save(); camera(ctx, 1.05, lerp(700, 600, ease_io(k)), 360)
    box(ctx, -300, 590, 2000, 300, hexc('#1c2749'))
    # building
    box(ctx, 90, 330, 300, 260, hexc('#d9cdb8'), 0, INK, 4)
    poly(ctx, [(70, 330), (240, 270), (410, 330)], hexc('#a05a4a'), INK, 4)
    for wx in (120, 190, 260, 330):
        box(ctx, wx, 440, 40, 50, hexc('#7fb0d4'), 0, INK, 3)
    box(ctx, 215, 520, 50, 70, hexc('#7a4a25'), 0, INK, 3)
    text(ctx, "Stanford", 240, 400, 46, INK)
    # wall calendar
    cx, cy = 840, 130
    box(ctx, cx-90, cy-50, 180, 190, hexc('#f3efe4'), 6, INK, 4)
    box(ctx, cx-90, cy-50, 180, 38, hexc('#c8473d'), 6, INK, 4)
    for i in range(3):
        for j in range(4):
            box(ctx, cx-70+j*38, cy+10+i*34, 24, 20, hexc('#cfc9b8'))
    for i, (lab, st, vx, vy, vr) in enumerate([("DAY 1", 0.3, 520, -460, 9), ("DAY 2", 0.7, 700, -380, -11)]):
        a = t-st
        if a < 0: continue
        e = a
        px = cx + vx*e*0.5 + (-20 if i == 0 else 20)*e
        py = cy + 30 + (vy*e + 520*e*e)
        rot = vr*e
        ctx.save(); ctx.translate(px, py); ctx.rotate(rot)
        s = 1+0.2*e
        ctx.scale(s, s)
        box(ctx, -60, -50, 120, 100, (1, 1, 1), 4, INK, 3)
        text(ctx, lab, 0, 4, 40, hexc('#c8473d'))
        ctx.restore()
    # PhD scroll
    sd = clamp((t-0.9)/0.5)
    if sd > 0:
        sy = lerp(300, 566, sd*sd)
        sxx = lerp(520, 600, sd)
        ctx.save(); ctx.translate(sxx, sy); ctx.rotate(lerp(-1.0, 0.0, sd) + 0.0)
        box(ctx, -70, -22, 140, 44, hexc('#f1e3b5'), 14, INK, 3)
        box(ctx, -72, -26, 18, 52, hexc('#d9c58b'), 8, INK, 3); box(ctx, 54, -26, 18, 52, hexc('#d9c58b'), 8, INK, 3)
        box(ctx, 28, -22, 14, 44, hexc('#c8473d'))
        text(ctx, "PhD", -14, 10, 36, INK)
        ctx.restore()
    # elon sprints
    p = cast("elon_adult", 0.95)
    ex = lerp(560, 1500, ease_in(k))
    ph = t*3.2
    sw = math.sin(ph*2*math.pi)
    info = p.draw(ctx, ex, 410, t, "determined", facing=1.0, armL=(-30+45*sw, 90-30*abs(sw)), armR=(30-45*sw, 90-30*abs(sw)), walk=ph)
    ctx.restore()
    if t > 1.4:
        s = pop(t, 1.4, .35)
        ctx.save(); ctx.translate(430, 150); ctx.scale(s, s)
        text(ctx, "2 DAYS", 0, 0, 84, (1, 1, 1), outline=INK); ctx.restore()

def ease_in(x): x = clamp(x); return x*x

# ---------------- shot 8 ----------------
def shot8(ctx, t, dur):
    bg_room(ctx, hexc('#6f7a94'), hexc('#7a5a42'), 570)
    k = t/dur
    ctx.save(); camera(ctx, lerp(1.0, 1.04, k), 640, 360)
    city_window(ctx, 520, 60, 280, 230, night=True)
    # Zip2 sign taped
    ctx.save(); ctx.translate(660, 175); ctx.rotate(-0.05)
    paper(ctx, 0, 0, 130, 70, 0, (1, 1, 0.92), 0)
    text(ctx, "Zip2", 0, 12, 54, INK)
    box(ctx, -50, -46, 40, 14, (0.95, 0.9, 0.6), 0, None); box(ctx, 10, -46, 40, 14, (0.95, 0.9, 0.6), 0, None)
    ctx.restore()
    # elon at desk
    p = cast("elon_adult", 0.95)
    ty = math.sin(t*14)*8
    info = p.draw(ctx, 200, 545, t, "tired", facing=0.8, armL=(60, 70+ty*0.4), armR=(110, 75-ty*0.4), legs=False)
    desk(ctx, 330, 470, 440)
    def scr(c, tt):
        box(c, 0, 0, 184, 132, hexc('#1d3a2a'))
        for i in range(0, 184, 23): line(c, [(i, 0), (i, 132)], hexc('#2f6b47'), 1.5)
        for j in range(0, 132, 22): line(c, [(0, j), (184, j)], hexc('#2f6b47'), 1.5)
        circle(c, 100, 56-4*abs(math.sin(tt*3)), 11, hexc('#e04040'), INK, 2)
        poly(c, [(92, 62), (108, 62), (100, 82)], hexc('#e04040'), INK, 2)
    crt(ctx, 410, 470, 1.0, draw_screen=scr, t=t)
    # kimbal asleep
    ctx.save(); ctx.translate(1040, 618); ctx.rotate(-math.pi/2)
    kp = cast("kimbal", 0.7)
    kp.draw(ctx, 0, 0, t, "tired", facing=0, armL=(-25, 110), armR=(25, 110), legs=False)
    ctx.restore()
    # sleeping bag
    ctx.save(); ctx.translate(0, 0)
    poly(ctx, [(930, 590), (1260, 585), (1270, 650), (930, 655)], hexc('#3f6e9a'), INK, 4)
    box(ctx, 880, 596, 70, 50, hexc('#f3efe4'), 14, INK, 3)
    line(ctx, [(1000, 595), (1000, 652)], hexc('#2d5278'), 3); line(ctx, [(1100, 592), (1100, 652)], hexc('#2d5278'), 3)
    ctx.restore()
    for i, (zx, zy, s) in enumerate([(760, 520, 40), (800, 480, 50), (850, 435, 60)]):
        a = clamp((t*1.5 - i*0.35) % 1.8)
        text(ctx, "z", zx, zy - 12*a, s, (1, 1, 1), outline=INK)
    # YMCA sign + towel
    def ymca(c):
        box(c, -8, 10, 16, 120, hexc('#7a4a25'), 0, INK, 3)
        poly(c, [(-130, -40), (80, -40), (120, -10), (80, 20), (-130, 20)], hexc('#f5f0dc'), INK, 4)
        text(c, "YMCA showers", -10, -6, 30, INK); text(c, "→", 90, -8, 26, INK)
    popped(ctx, t, 1.0, 1100, 410, ymca, seed=5)
    def towel(c):
        box(c, -28, -22, 56, 44, hexc('#f0a0b0'), 6, INK, 3); box(c, -28, -6, 56, 8, (1, 1, 1))
        box(c, 36, -8, 26, 16, hexc('#9fe0c0'), 6, INK, 3)
    popped(ctx, t, 1.3, 1140, 540, towel, seed=6)
    ctx.restore()
    s = pop(t, 1.9, .35)
    if s > 0:
        ctx.save(); ctx.translate(1000, 120); ctx.scale(s, s)
        text(ctx, "SLEPT AT\nTHE OFFICE" if False else "SLEPT AT", 0, 0, 56, (1, 1, 1), outline=INK)
        text(ctx, "THE OFFICE", 0, 56, 56, (1, 1, 1), outline=INK); ctx.restore()

# ---------------- shot 9 ----------------
def shot9(ctx, t, dur):
    bg_spotlight(ctx, (0.13, 0.13, 0.15), 600, 620)
    k = t/dur
    ctx.save(); camera(ctx, lerp(1.0, 1.08, ease_io(k)), 640, 360)
    # bills rain (behind chars)
    rnd = random.Random(11)
    bills = [(rnd.uniform(60, 1220), rnd.uniform(0, 1), rnd.uniform(-2, 2), rnd.uniform(.6, 1.0)) for _ in range(26)]
    def rain():
        for (bx, ph, rv, s) in bills:
            a = t*0.55 + ph
            yy = -60 + ((a % 1.0))*820
            if t > 0.5 + ph*0.6 - 0.3:
                bill(ctx, bx + math.sin(t*3+ph*9)*25, yy, rv*t + ph*6, s)
    rain()
    p = cast("elon_adult", 1.0)
    pl = p.draw(ctx, 520, 560, t, "smug", facing=0.0,
                armL=L2((-30, 100), (-40, -140), ease_out((t-0.4)/0.6)),
                armR=L2((30, 100), (40, -140), ease_out((t-0.4)/0.6)), legs=False)
    hl, hr = pl['handL'], pl['handR']
    bx, by = (hl[0]+hr[0])/2, (hl[1]+hr[1])/2 - 92
    if t > 0.6: money_bag(ctx, bx, by, 0.8)
    b = cast("banker", 1.0)
    bi = b.draw(ctx, 990, 560, t, "happy", facing=-0.7, armL=(-60, 20), armR=(30, 100), legs=False)
    cxh, cyh = bi['handL']
    def check(c):
        box(c, -170, -75, 340, 150, (1, 1, 1), 6, INK, 4)
        text(c, "Compaq", -90, -35, 40, INK); text(c, "$307,000,000", 0, 22, 48, hexc('#2e7d3a'))
        line(c, [(40, 58), (140, 58)], INK, 3)
    popped(ctx, t, 0.3, cxh+30, cyh+85, check, seed=9)
    ctx.restore()
    if t > 1.4:
        s = pop(t, 1.4, .35)
        ctx.save(); ctx.translate(640, 80); ctx.scale(s, s)
        text(ctx, "$22 million · age 27", 0, 0, 72, (1, 1, 1), outline=INK); ctx.restore()

SCENES = [(3.2, shot6), (3.4, shot7), (3.3, shot8), (3.3, shot9)]
