import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from lib import *
from assets_b import *
import math

EXPR["asleep"] = dict(brow=(0, 4), eyes="closed", mouth="o_small")

def kw(ctx, s, t, start, x, y, size=72, rot=-3, c=(1, 1, 1)):
    k = pop(t, start, 0.35)
    if k <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(k, k)
    text(ctx, s, 0, 0, size, c, rot=rot*math.pi/180, outline=INK); ctx.restore()

def caption_tw(ctx, s, t, start, x, y, size=54, speed=14.0):
    r = clamp((t-start)*speed/len(s))
    if r > 0: text(ctx, s, x, y, size, (1, 1, 1), anchor="l", reveal=r, outline=INK)

def lp(a, b, k): return (lerp(a[0], b[0], k), lerp(a[1], b[1], k))

# ============================ SHOT 6 : Canada 1989 ============================
def shot6(ctx, t, dur):
    p = ease_io(t/dur)
    ctx.save(); camera(ctx, lerp(1.0, 1.08, p), lerp(620, 660, p), lerp(380, 400, p), t=t)
    ctx.set_source_rgb(*hexc('#a9dcf2')); ctx.paint()
    box(ctx, -300, -300, W+600, 300, hexc('#a9dcf2'))
    for (x, y, s) in [(160, 250, 1.0), (760, 70, 1.2), (1100, 190, 0.9)]:
        for dx, r in [(-40, 26), (0, 38), (42, 28)]: circle(ctx, x+dx*s, y, r*s, (1, 1, 1), a=.9)
    # mountains
    mountain(ctx, 220, 760, 470, 190, 520, hexc('#6f8fb8'))
    mountain(ctx, 600, 1240, 900, 150, 520, hexc('#5f7fa9'))
    mountain(ctx, 1000, 1700, 1300, 210, 520, hexc('#7898bd'))
    mountain(ctx, -300, 330, 20, 230, 520, hexc('#7898bd'))
    # grass + sidewalk + curb + road
    box(ctx, -300, 500, W+600, 80, hexc('#7fae6b'))
    box(ctx, -300, 560, W+600, 110, hexc('#d8d6d0'))
    for gx in range(-300, W+300, 120): line(ctx, [(gx, 560), (gx, 670)], hexc('#b9b6af'), 2)
    box(ctx, -300, 560, W+600, 6, hexc('#bcb9b1'))
    box(ctx, -300, 668, W+600, 14, hexc('#f1c232'), 0, INK, 2.5)
    box(ctx, -300, 682, W+600, 140, hexc('#4a4e57'))
    for dx in range(-300, W+300, 160): box(ctx, dx, 740, 80, 8, hexc('#e8e8e8'))
    # pines behind sign/walker line
    for (px, h) in [(430, 150), (520, 190), (600, 140), (700, 175), (800, 150), (1290, 185), (1190, 150), (1380, 160)]:
        pine(ctx, px, 556, h)
    terminal(ctx, -120, 400, 560)
    welcome_sign(ctx, 985, 590)
    for (px, h) in [(1190, 120), (760, 105)]:
        pine(ctx, px, 590, h)
    # plane
    px = lerp(-260, 1560, clamp(t/dur*1.05))
    py = 150 + math.sin(t*1.2)*3
    airliner(ctx, px, py, 0.8)
    # teen walking right, pulling suitcase
    x = lerp(300, 790, clamp(t/dur))
    ground = 640
    wy = ground-150*0.85
    teen = cast('elon_teen', 0.85)
    walk = t*1.8
    # suitcase trails behind: handle socket -> hand
    sx = x-190
    sock = rolling_suitcase(ctx, sx, ground, t)
    info = teen.draw(ctx, x, wy, t, 'determined', facing=0.8, armL=(-52, 112), armR=(30, 110), legs=True, walk=walk, blink_seed=1)
    hand = info['handL']
    line(ctx, [sock, hand], hexc('#5b616d'), 5)
    line(ctx, [sock, hand], hexc('#aeb4be'), 2)
    circle(ctx, hand[0], hand[1], 9, SKIN, INK, 2.5)
    ctx.restore()
    caption_tw(ctx, "1989 · Age 17", t, 0.25, 50, 62, 58)

# ============================ SHOT 7 : Stanford 1995 ============================
def shot7(ctx, t, dur):
    p = ease_io(t/dur)
    ctx.save(); camera(ctx, lerp(1.0, 1.1, p), 640, lerp(330, 360, p), t=t)
    ctx.set_source_rgb(*hexc('#8fd0ee')); ctx.paint()
    box(ctx, -300, -300, W+600, 300, hexc('#8fd0ee'))
    for (x, y, s) in [(190, 90, 1.0), (1050, 70, 1.1)]:
        for dx, r in [(-40, 24), (0, 36), (42, 26)]: circle(ctx, x+dx*s, y, r*s, (1, 1, 1), a=.9)
    # foothills
    poly(ctx, [(-300, 430), (100, 330), (400, 400), (700, 320), (1000, 390), (1300, 330), (1600, 430)], hexc('#c8b57a'))
    # ground
    box(ctx, -300, 495, W+600, 400, hexc('#ddc9a0'))
    base = 495
    arcade(ctx, 120, 515, base, 56)
    arcade(ctx, 765, 1160, base, 56)
    arcade(ctx, -260, 120, base, 56)
    arcade(ctx, 1160, 1540, base, 56)
    church_facade(ctx, 640, base)
    # lawn oval + path
    ellipse(ctx, 640, 553, 640, 58, hexc('#4fa25a'))
    ellipse(ctx, 640, 548, 600, 48, hexc('#5fb468'))
    ctx.new_path(); ctx.save(); ctx.translate(640, 553); ctx.scale(640, 58); ctx.arc(0, 0, 1, 0, 2*math.pi); ctx.restore()
    ctx.set_source_rgb(*INK); ctx.set_line_width(2); ctx.stroke()
    poly(ctx, [(606, 497), (674, 497), (760, 606), (520, 606)], hexc('#efe0bc'), None)
    line(ctx, [(606, 497), (520, 606)], hexc('#c9b88f'), 3); line(ctx, [(674, 497), (760, 606)], hexc('#c9b88f'), 3)
    # front walkway (foreground)
    box(ctx, -300, 606, W+600, 200, hexc('#efe0bc'))
    box(ctx, -300, 606, W+600, 5, hexc('#c9b88f'))
    # palms
    palm(ctx, 62, 570, 430, 20, t, 1)
    palm(ctx, 1218, 570, 430, -20, t, 2)
    palm(ctx, 440, 580, 290, -16, t, 3)
    palm(ctx, 840, 580, 290, 14, t, 4)
    # plinth sign
    box(ctx, 150, 575, 300, 36, BUFF_D, 3, INK, 3)
    box(ctx, 142, 553, 316, 32, BUFF, 4, INK, 3)
    box(ctx, 150, 560, 300, 14, BUFF_L)
    serif(ctx, "Stanford University", 300, 578, 28, hexc('#8c1515'))
    # calendar
    calendar_post(ctx, 990, 624, t, 1.55)
    # Elon: walk in, pause, walk out fast
    x_in = lerp(-120, 600, clamp(t/1.25))
    x = x_in
    walking = t < 1.25
    exit_k = clamp((t-2.35)/0.9)
    if t >= 2.35: x = lerp(600, 1650, exit_k*exit_k*(3-2*exit_k) if False else exit_k**1.6)
    facing = 0.8 if (t < 1.25 or t >= 2.5) else lerp(0.8, 0.0, ease_io((t-1.25)/0.3)) if t < 1.6 else (0.0 if t < 2.2 else lerp(0.0, 0.8, ease_io((t-2.2)/0.3)))
    moving = walking or t >= 2.35
    walk = t*2.0 if (t < 1.2) else (t*3.4 if t >= 2.35 else 0)
    ex = "tired" if 1.6 < t < 2.35 else ("worried" if t >= 2.35 else "neutral")
    el = cast('elon_adult', 0.68)
    wy = 630-0.68*150
    armL = (-26, 125); armR = (26, 125)
    if 1.6 < t < 2.35: armR = (60, -10)   # points at calendar
    el.draw(ctx, x, wy, t, ex, facing=facing, armL=armL, armR=armR, legs=True, walk=walk, blink_seed=3)
    # backpack on his back (drawn after body, sticks out at left side)
    bpx = x - 0.68*88*(1 if facing >= 0 else -1) * (0.9 if abs(facing) > 0.3 else 0.6)
    ctx.save(); ctx.translate(bpx - 8, wy - 0.68*120)
    box(ctx, -26, -52, 52, 100, hexc('#d9533d'), 14, INK, 3)
    box(ctx, -22, -2, 44, 36, hexc('#b8402d'), 8, INK, 2); box(ctx, -18, -52, 36, 12, hexc('#b8402d'), 6)
    ctx.restore()
    ctx.restore()
    kw(ctx, "2 days.", t, 2.4, 300, 150, 92, -4)

# ============================ SHOT 8 : Zip2 office ============================
def shot8(ctx, t, dur):
    p = ease_io(t/dur)
    ctx.save(); camera(ctx, lerp(1.0, 1.07, p), lerp(650, 690, p), 360, t=t)
    wallc = hexc('#2b3552'); floorc = hexc('#3e3338')
    ctx.set_source_rgb(*wallc); ctx.paint(); box(ctx, -300, -300, W+600, 300, wallc)
    FL = 590
    box(ctx, -300, FL, W+600, 400, floorc)
    box(ctx, -300, FL-14, W+600, 14, hexc('#232b44'))
    for fx in range(-300, W+300, 110): line(ctx, [(fx, FL), (fx-30, FL+140)], tone(floorc, .8), 2)
    office_door(ctx, 40, FL-14, 320, 160)
    night_window(ctx, 290, 110, 250, 230, t)
    # window light pool on wall
    # chair + towel (behind Elon)
    seat_y = 512
    chair_with_towel(ctx, 515, FL, seat_y)
    # Elon seated, facing right
    el = cast('elon_adult', 0.85)
    ex, ey = 640, 520
    kb_x = 770; desk_y = 500
    typing = 0.6 + (math.sin(t*22) * 0.5)
    hL = (kb_x-18, desk_y-6 + math.sin(t*25)*3)
    hR = (kb_x+22, desk_y-6 + math.sin(t*25+2)*3)
    shL = (ex - 0.85*65, ey - 0.85*156); shR = (ex + 0.85*65, ey - 0.85*156)
    armL = ((hL[0]-shL[0])/0.85, (hL[1]-shL[1])/0.85)
    armR = ((hR[0]-shR[0])/0.85, (hR[1]-shR[1])/0.85)
    el.draw(ctx, ex, ey, t, 'determined', facing=0.8, armL=armL, armR=armR, legs=False, blink_seed=5, look=1)
    # screen glow on his face and body (cone from monitor)
    mon_x = 960
    scr = (mon_x-52, desk_y-124)
    poly(ctx, [(scr[0], scr[1]-60), (scr[0], scr[1]+60), (ex+40, ey-120), (ex+60, ey-250)], hexc('#5ec8ff'), None, 0, a=.10)
    ellipse(ctx, ex+22, ey-215, 54, 66, hexc('#5ec8ff'), a=.07)
    # desk (in front of his lap)
    dtop = desk_y
    box(ctx, 540, dtop, 520, 22, hexc('#9a6a3e'), 4, INK, 3)
    box(ctx, 552, dtop+22, 496, 70, hexc('#7f5432'), 0, INK, 3)
    box(ctx, 560, dtop+92, 20, FL-dtop-92+4, hexc('#7f5432'), 0, INK, 3)
    box(ctx, 1020, dtop+92, 20, FL-dtop-92+4, hexc('#7f5432'), 0, INK, 3)
    box(ctx, 820, dtop+34, 150, 46, hexc('#6c4527'), 4, INK, 2.5); circle(ctx, 895, dtop+57, 6, hexc('#d9c46a'), INK, 2)
    keyboard_side(ctx, kb_x, dtop)
    # hands on keys (over keyboard)
    circle(ctx, hL[0], hL[1], 8, SKIN, INK, 2.5); circle(ctx, hR[0], hR[1], 8, SKIN, INK, 2.5)
    crt_side(ctx, mon_x, dtop)
    # glow cone over desk surface
    # papers + mug
    box(ctx, 600, dtop-16, 44, 16, (1, 1, 1), 2, INK, 2)
    box(ctx, 1000, dtop-30, 26, 30, hexc('#e4572e'), 4, INK, 2.5)
    # Kimbal asleep on beanbag in the corner
    kx = 1150
    beanbag(ctx, kx, FL+30, 250, 120, hexc('#c0562f'))
    ctx.save(); ctx.translate(kx+6, FL-20); ctx.rotate(-0.12)
    kim = cast('kimbal', 0.78)
    kim.draw(ctx, 0, -10, t, 'asleep', facing=0.2, armL=(-14, 100), armR=(14, 100), legs=False, blink_seed=2)
    ctx.restore()
    blanket(ctx, kx-120, FL-72, 240, 70)
    # beanbag front lip
    ctx.new_path(); ctx.move_to(kx-125, FL+30); ctx.curve_to(kx-100, FL-8, kx+100, FL-8, kx+125, FL+30)
    ctx.curve_to(kx+60, FL+44, kx-60, FL+44, kx-125, FL+30); ctx.set_source_rgb(*tone(hexc('#c0562f'), .92)); ctx.fill_preserve()
    ctx.set_source_rgb(*INK); ctx.set_line_width(4); ctx.stroke()
    zzz(ctx, kx+44, FL-250, t)
    ctx.restore()
    # dim vignette
    g = cairo.RadialGradient(W/2, H/2, 300, W/2, H/2, 800); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0.03, 0.1, .45)
    ctx.set_source(g); ctx.paint()
    kw(ctx, "Zip2", t, 0.5, 300, 520, 0) if False else None

# ============================ SHOT 9 : payoff ============================
def shot9(ctx, t, dur):
    p = ease_io(t/dur)
    bg_spotlight(ctx, floor_y=640)
    ctx.save(); camera(ctx, lerp(1.0, 1.08, p), 640, 380, t=t)
    # money rain BEHIND characters
    if t > 2.2: money_rain(ctx, t, 2.2)
    sc = 0.95
    ey0 = 505
    # Elon moves toward centre once the banker leaves
    ex = lerp(360, 560, ease_io((t-2.5)/0.7))
    by = ey0
    # banker exit
    bx = 920 if t < 2.2 else lerp(920, 1700, clamp((t-2.2)/0.9)**1.15)
    bk = cast('banker', sc); el = cast('elon_adult', sc)
    shR_e = (ex + 59*sc/0.95, ey0 - 156*sc)  # (kept for clarity)
    # --- check 1 (big)
    c1_c = (640, 360)
    # arm targets
    sh_eR = (360 + 65*sc, ey0 - 156*sc)
    sh_bL = (920 - 65*sc, ey0 - 156*sc)
    # draw check behind hands? characters first, check pops, hands re-drawn on top
    banker_walk = 0.0
    bf = -0.6
    b_arm_L = ((c1_c[0]+160-sh_bL[0])/sc, (c1_c[1]-sh_bL[1])/sc)
    b_arm_R = (26, 125)
    e_arm_R = ((c1_c[0]-160-sh_eR[0])/sc, (c1_c[1]-sh_eR[1])/sc)
    e_arm_L = (-26, 125)
    ex_expr = 'smug'
    if t < 2.2:
        k1 = pop(t, 0.5, 0.4)
        bk.draw(ctx, bx, by, t, 'happy', talking=False, facing=-0.6, armL=b_arm_L if k1 > 0 else (-26, 125), armR=b_arm_R, legs=True, blink_seed=1)
        el.draw(ctx, 360, by, t, 'happy' if k1 > 0 else 'neutral', facing=0.6, armL=e_arm_L, armR=e_arm_R if k1 > 0 else (26, 125), legs=True, blink_seed=4)
        if k1 > 0:
            smoke(ctx, c1_c[0], c1_c[1], (t-0.5)/0.7, 80, 5)
            ctx.save(); ctx.translate(*c1_c); ctx.scale(k1, k1); ctx.rotate(-0.03)
            big_check(ctx, 340, 160, "$307,000,000"); ctx.restore()
            ha = (c1_c[0]+160*k1, c1_c[1]); hb = (c1_c[0]-160*k1, c1_c[1])
            # hands over the check edges
            circle(ctx, c1_c[0]-166, c1_c[1], 9, SKIN, INK, 2.5); circle(ctx, c1_c[0]+166, c1_c[1], 9, SKIN, INK, 2.5)
    else:
        # big check shrinks away with puff, banker turns and walks off
        k = 1 - clamp((t-2.2)/0.25)
        # banker leaves facing right
        bk.draw(ctx, bx, by, t, 'happy', facing=0.8, armL=(-26, 125), armR=(26, 125), legs=True, walk=t*3.2, blink_seed=1)
        if k > 0:
            ctx.save(); ctx.translate(*c1_c); ctx.scale(k, k); ctx.rotate(k*0.0); big_check(ctx, 340, 160, "$307,000,000"); ctx.restore()
        else:
            pass
        smoke(ctx, c1_c[0], c1_c[1], (t-2.2)/0.7, 90, 8)
        # elon with check 2
        c2 = (ex + 22, ey0 - 156*sc + 88)
        sh_L = (ex - 65*sc, ey0 - 156*sc); sh_R = (ex + 65*sc, ey0 - 156*sc)
        kk = pop(t, 2.25, 0.4)
        up = ease_out(clamp((t-2.25)/0.4))
        armL2 = lp((-26, 125), ((c2[0]-130-sh_L[0])/sc, (c2[1]-sh_L[1])/sc), up)
        armR2 = lp((26, 125), ((c2[0]+130-sh_R[0])/sc, (c2[1]-sh_R[1])/sc), up)
        el.draw(ctx, ex, by, t, 'happy' if t > 2.3 else 'smug', facing=0.0, armL=armL2, armR=armR2, legs=True, blink_seed=4)
        if kk > 0:
            smoke(ctx, c2[0], c2[1], (t-2.25)/0.7, 80, 9)
            ctx.save(); ctx.translate(*c2); ctx.scale(kk, kk); ctx.rotate(0.02)
            big_check(ctx, 270, 130, "$22,000,000", payto="Pay to: Elon Musk"); ctx.restore()
            circle(ctx, c2[0]-136*kk, c2[1], 9, SKIN, INK, 2.5); circle(ctx, c2[0]+136*kk, c2[1], 9, SKIN, INK, 2.5)
        # sparkles around the new check
        if t > 2.3:
            for i in range(5):
                a = t*2 + i*1.26; r = 150 + 12*math.sin(t*5+i)
                sx, sy = c2[0]+math.cos(a)*r*1.1, c2[1]-30+math.sin(a)*r*0.7
                s = 7 + 3*math.sin(t*9+i*2)
                if sy < 330 or True:
                    poly(ctx, [(sx, sy-s*2), (sx+s*.5, sy-s*.5), (sx+s*2, sy), (sx+s*.5, sy+s*.5), (sx, sy+s*2), (sx-s*.5, sy+s*.5), (sx-s*2, sy), (sx-s*.5, sy-s*.5)], hexc('#ffe27a'), None, 0, a=.9)
    ctx.restore()
    kw(ctx, "$22M at 27", t, 3.4, 640, 62, 84, -2, hexc('#ffe27a'))

SCENES = [(3.0, shot6), (3.6, shot7), (3.8, shot8), (4.6, shot9)]

def _tw(shot, start, n, step=0.06): return [(shot, round(start+i*step, 2), "typewriter_tick", -22) for i in range(n)]

CUES = [
    (6, 0.0, "wind_ambience", -16),
    (6, 0.05, "plane_flyby", -12),
    (6, 0.1, "suitcase_roll", -14),
    (6, 1.3, "suitcase_roll", -14),
] + _tw(6, 0.25, 13) + [
    (7, 0.0, "wind_ambience", -18),
    (7, 0.0, "footsteps", -16),
    (7, 0.72, "pop", -10),
    (7, 1.55, "page_flip", -8),
    (7, 2.35, "whoosh", -9),
    (7, 2.4, "pop", -8),
    (8, 0.0, "office_hum", -15),
    (8, 0.0, "night_crickets", -22),
    (8, 0.3, "typing_burst", -10),
    (8, 1.9, "typing_burst", -10),
    (8, 1.0, "snore", -14),
    (8, 3.1, "snore", -14),
    (9, 0.5, "pop", -9),
    (9, 0.55, "sparkle", -14),
    (9, 2.2, "whoosh_short", -12),
    (9, 2.25, "pop", -8),
    (9, 2.25, "cash_register", -8),
    (9, 2.3, "coins", -10),
    (9, 2.3, "money_rain", -12),
    (9, 2.35, "sparkle", -12),
    (9, 3.4, "pop", -8),
]
