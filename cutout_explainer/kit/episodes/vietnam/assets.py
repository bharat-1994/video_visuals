"""Vietnam episode: cast + recurring assets. Built by the director. Builders REUSE these; never redraw them.
Import from a batch module (cwd = kit root):  from episodes.vietnam.assets import *
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "engine"))
from lib import *

# ---------------- palette ----------------
PADDY, PADDY_D, WATER, EARTH = hexc('#86b85f'), hexc('#5e9447'), hexc('#a9d6df'), hexc('#c49a6c')
STRAW, STRAW_D, STRAW_L = hexc('#e6c97f'), hexc('#c4a258'), hexc('#f3e2ad')
PAPER, STAMP = hexc('#efe5c4'), hexc('#7b3f8c')
NOTE_G, NOTE_G_D = hexc('#b7d3a2'), hexc('#7fa66b')
NIGHT, SOV, SOV_D, SOV_L, RED = hexc('#1c1c24'), hexc('#8d9299'), hexc('#676c74'), hexc('#b3b7bd'), hexc('#c0392b')
MAP_C, MAP_D = hexc('#e9b949'), hexc('#c48f2c')

# ---------------- cast ----------------
# Signature look: farmer + mother + kid wear the non la (conical straw hat). Clerk: olive state-store uniform + cap.
_VC = {
    "farmer": dict(hair="short", hair_c=hexc('#1f1a17'), shirt=hexc('#7d8c6a'), jaw=0.45, nose=True, collar=False),
    "mother": dict(hair="wavy", hair_c=hexc('#1a1614'), shirt=hexc('#d9cfb8'), jaw=0.1, collar=True),
    "kid":    dict(kid=True, hair="fringe", hair_c=hexc('#1a1614'), shirt=hexc('#f0f0e8'), collar=False),
    "clerk":  dict(hair="slick", hair_c=hexc('#1a1614'), shirt=hexc('#6f7a4a'), jaw=0.6, glasses=True, nose=True),
}
_HAT = {"farmer": "non_la", "mother": "non_la", "kid": None, "clerk": "cap"}

class VPuppet:
    """Same draw() signature as Puppet; adds the character's hat. Hat is skipped with hat=False."""
    def __init__(self, who, scale=1.0):
        self.who = who; self.p = Puppet(scale=scale, seed=sum(map(ord, who)) % 97, **_VC[who])
    def __getattr__(self, k): return getattr(self.p, k)
    def draw(self, ctx, x, y, t, expr="neutral", talking=False, facing=0.0, hat=True, **kw):
        info = self.p.draw(ctx, x, y, t, expr, talking, facing, **kw)
        hx, hy = info['head']; R = info['R']; hx += facing*R*0.12
        if hat and _HAT[self.who] == "non_la": non_la(ctx, hx, hy - R*0.55, R)
        if hat and _HAT[self.who] == "cap": state_cap(ctx, hx, hy - R*0.62, R, facing)
        return info

def vcast(who, scale=1.0):
    """who: farmer | mother | kid | clerk"""
    return VPuppet(who, scale)

def non_la(ctx, x, y, R):
    """Conical palm-leaf hat. (x,y) = brim centre. Signature: wide shallow cone, radial weave lines, chin string."""
    w, h = R*1.45, R*1.0
    poly(ctx, [(x-w, y+R*0.06), (x, y-h), (x+w, y+R*0.06)], STRAW, INK, max(2, R*0.04))
    poly(ctx, [(x, y-h), (x+w, y+R*0.06), (x+w*0.35, y+R*0.06)], STRAW_D)        # shadow side
    for k in (-0.62, -0.3, 0.02, 0.34):
        line(ctx, [(x, y-h), (x+w*k, y+R*0.06)], STRAW_D, max(1, R*0.022), .8)
    for k in (0.33, 0.62):
        line(ctx, [(x-w*k, y-h*(1-k)+R*0.06*k), (x+w*k, y-h*(1-k)+R*0.06*k)], STRAW_L, max(1, R*0.025), .9)
    line(ctx, [(x-w, y+R*0.06), (x+w, y+R*0.06)], INK, max(2, R*0.045))

def state_cap(ctx, x, y, R, f=0.0):
    """Olive peaked cap (state employee). No badge/insignia."""
    box(ctx, x-R*0.82, y-R*0.42, R*1.64, R*0.5, hexc('#5f6a3c'), R*0.2, INK, max(2, R*0.04))
    poly(ctx, [(x-R*0.6+f*R*0.5, y+R*0.06), (x+R*0.6+f*R*0.5, y+R*0.06), (x+R*0.75+f*R*0.7, y+R*0.24), (x-R*0.45+f*R*0.7, y+R*0.24)],
         hexc('#2e3320'), INK, max(2, R*0.04))

# ---------------- backgrounds ----------------
def bg_paddy(ctx, t=0.0, karst=True):
    """Northern countryside: pale sky, limestone karst peaks, flooded paddy rows reflecting sky, coconut palms.
    Horizon at y=400. Free ground for characters: y 430-640."""
    box(ctx, 0, 0, W, 400, hexc('#cfe6ea'))
    if karst:
        for x0, w, h, c in [(-40, 260, 230, '#9db8a8'), (180, 200, 300, '#8aa897'), (900, 240, 260, '#9db8a8'), (1080, 260, 190, '#8aa897')]:
            ctx.move_to(x0, 400); ctx.curve_to(x0+w*0.1, 400-h, x0+w*0.45, 400-h*1.08, x0+w*0.55, 400-h*0.9)
            ctx.curve_to(x0+w*0.7, 400-h*0.7, x0+w*0.85, 400-h*0.5, x0+w, 400); ctx.close_path()
            ctx.set_source_rgb(*hexc(c)); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
    box(ctx, 0, 400, W, 320, PADDY)
    for i, y0 in enumerate([400, 432, 472, 524, 590]):   # flooded strips (perspective rows)
        hh = 10 + i*7
        box(ctx, 0, y0+4, W, hh, WATER)
        for k in range(14):                              # rice tufts
            xx = (k*97 + i*41 + 20) % (W+40) - 20
            for d in (-1, 0, 1):
                line(ctx, [(xx+d*4, y0+4+hh), (xx+d*7, y0+hh-6-i*2)], PADDY_D, 2+i*0.4)
    for px, s in [(70, 1.0), (1210, 0.85)]: palm(ctx, px, 470, s)

def palm(ctx, x, y, s=1.0):
    """Coconut palm. (x,y) = base."""
    pts = [(x, y), (x+8*s, y-90*s), (x+22*s, y-180*s)]
    line(ctx, pts, INK, 15*s); line(ctx, pts, hexc('#8b6b45'), 10*s)
    tx, ty = x+22*s, y-180*s
    for a in (-2.6, -2.0, -1.2, -0.5, 0.2, 0.9):
        ex, ey = tx+math.cos(a)*85*s, ty+math.sin(a)*55*s+30*s
        poly(ctx, [(tx, ty), (tx+math.cos(a-0.25)*50*s, ty+math.sin(a-0.25)*35*s), (ex, ey), (tx+math.cos(a+0.2)*45*s, ty+math.sin(a+0.2)*30*s+12*s)],
             hexc('#4f8a3c'), INK, 2)
    for d in (-8, 4): circle(ctx, tx+d*s, ty+10*s, 8*s, hexc('#6b4b2a'), INK, 2)

def bg_dark(ctx):
    """Emotional/abstract beats: near-black with a soft spotlight."""
    bg_spotlight(ctx, base=NIGHT)

# ---------------- map (RECURRING MOTIF: the country as an object) ----------------
_VN = [(102.14, 22.40), (102.5, 22.75), (103.0, 22.6), (103.97, 22.5), (104.5, 22.82), (105.3, 23.35), (106.0, 22.98), (106.7, 22.8),
       (107.35, 21.8), (108.0, 21.55), (107.4, 21.2), (106.9, 20.85), (106.55, 20.3), (106.0, 19.9), (105.75, 19.1), (105.7, 18.7),
       (106.1, 18.1), (106.6, 17.47), (107.2, 16.75), (107.6, 16.4), (108.2, 16.05), (108.8, 15.3), (109.2, 13.8), (109.45, 12.6),
       (109.15, 11.6), (108.6, 11.15), (108.0, 10.7), (107.1, 10.4), (106.7, 9.8), (105.9, 8.85), (105.1, 8.6), (104.8, 9.0),
       (104.9, 10.0), (104.5, 10.4), (105.1, 10.9), (106.15, 11.1), (106.4, 11.7), (107.5, 12.3), (107.55, 13.4), (107.5, 14.6),
       (107.6, 15.4), (107.2, 15.9), (106.6, 16.5), (106.0, 17.3), (105.55, 18.15), (104.85, 18.8), (104.2, 19.25), (104.0, 19.65),
       (104.6, 20.3), (104.25, 20.8), (103.2, 20.85), (102.9, 21.4), (102.3, 21.8)]

def vietnam_pts(x, y, h):
    """Outline points; (x,y) = centre of the map's bounding box, h = height in px."""
    k = h/(23.35-8.6); kx = k*0.96
    return [(x+(lo-105.8)*kx, y-(la-15.97)*k) for lo, la in _VN]

def vietnam_map(ctx, x, y, h, c=MAP_C, cracks=0.0, star=False, seed=1):
    """S-shaped silhouette with shadow edge. cracks 0..1 grows 3 jagged cracks. Bounding box ~0.48h wide."""
    pts = vietnam_pts(x, y, h)
    poly(ctx, [(px+h*0.012, py+h*0.015) for px, py in pts], MAP_D)
    poly(ctx, pts, c, INK, max(2, h*0.008))
    k = h/(23.35-8.6)
    for i, path in enumerate([[(105.4, 21.6), (105.9, 20.9), (105.5, 20.4), (106.0, 19.9)],
                              [(107.0, 16.6), (107.4, 16.2), (107.6, 15.4), (108.3, 14.9)],
                              [(106.6, 11.6), (106.2, 11.0), (106.4, 10.5), (105.7, 9.9)]]):
        f = clamp(cracks*3 - i)
        if f <= 0: continue
        P = [(x+(lo-105.8)*k*0.96, y-(la-15.97)*k) for lo, la in path]
        n = 1 + f*(len(P)-1); i0 = min(int(n), len(P)-1); fr = n - int(n)
        seg = P[:i0] + ([(lerp(P[i0-1][0], P[i0][0], fr), lerp(P[i0-1][1], P[i0][1], fr))] if fr > 0 else [])
        if len(seg) < 2: continue
        line(ctx, seg, INK, max(3, h*0.012))

# ---------------- props ----------------
def ration_coupon(ctx, x, y, s=1.0, rot=0.0, rows=(("RICE", "13 kg"), ("PORK", "0.5 kg"), ("KEROSENE", "1 L"), ("SUGAR", "0.5 kg")),
                  torn=0, stamped=1.0):
    """Coupon sheet (centre x,y). Signature: cream paper, perforated grid of stubs, item + ration amount, purple ink stamp.
    torn = number of stubs missing from the bottom-right (0..len(rows)*2)."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    w, hh = 300, 70*len(rows)+60
    box(ctx, -w/2+6, -hh/2+8, w, hh, hexc('#b7aa82'))
    box(ctx, -w/2, -hh/2, w, hh, PAPER, 6, INK, 3)
    text(ctx, "RATION BOOK  1986", 0, -hh/2+28, 30, hexc('#5a4632'))
    n = 0
    for r, (item, amt) in enumerate(rows):
        for c in range(2):
            n += 1
            if n > len(rows)*2 - torn: continue
            bx, by = -w/2+12+c*(w-24)/2, -hh/2+50+r*70
            box(ctx, bx, by, (w-24)/2-6, 62, hexc('#f7f0d8'), 3, hexc('#9a8a6a'), 2)
            text(ctx, item, bx+(w-24)/4-3, by+22, 22, hexc('#4a3a2a'))
            text(ctx, amt, bx+(w-24)/4-3, by+46, 24, hexc('#8a2f2f'))
    for r in range(len(rows)+1):  # perforations
        yy = -hh/2+47+r*70
        for k in range(24): circle(ctx, -w/2+10+k*12.3, yy, 1.6, hexc('#9a8a6a'))
    if stamped > 0:
        ctx.save(); ctx.translate(w*0.22, hh*0.18); ctx.rotate(-0.25); ctx.scale(pop(stamped, 0, 1.0) if stamped < 1 else 1, pop(stamped, 0, 1.0) if stamped < 1 else 1)
        ctx.arc(0, 0, 44, 0, 6.283); ctx.set_source_rgba(*STAMP, .75); ctx.set_line_width(5); ctx.stroke()
        ctx.arc(0, 0, 34, 0, 6.283); ctx.set_line_width(2); ctx.stroke()
        text(ctx, "STATE", 0, -4, 20, STAMP); text(ctx, "STORE", 0, 16, 20, STAMP)
        ctx.restore()
    ctx.restore()

def dong_note(ctx, x, y, s=1.0, rot=0.0, value="100", wither=0.0):
    """Generic banknote, NO portrait/seal/emblem: green paper, guilloche ovals, value in corners, plain 'DONG'.
    wither 0..1: shrinks, greys and curls (value draining away)."""
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot + wither*0.25); sc = s*(1-0.55*wither); ctx.scale(sc, sc*(1-0.25*wither))
    g = tuple(lerp(a, b, wither) for a, b in zip(NOTE_G, hexc('#b9b4a6'))); gd = tuple(lerp(a, b, wither) for a, b in zip(NOTE_G_D, hexc('#8e897c')))
    box(ctx, -150, -70, 300, 140, g, 6, INK, 3)
    box(ctx, -138, -58, 276, 116, g, 4, gd, 2)
    for r in (40, 30, 20): ctx.save(); ctx.translate(55, 0); ctx.scale(1, 0.8); ctx.arc(0, 0, r, 0, 6.283); ctx.restore(); ctx.set_source_rgb(*gd); ctx.set_line_width(2); ctx.stroke()
    for k in range(6): line(ctx, [(-125, -30+k*12), (-20, -30+k*12)], gd, 2, .6)
    text(ctx, value, -112, -38, 30, hexc('#2f4a2a'), "l"); text(ctx, value, 125, 44, 30, hexc('#2f4a2a'), "r")
    text(ctx, "DONG", 55, 6, 34, hexc('#2f4a2a'))
    ctx.restore()

def rice_sack(ctx, x, y, s=1.0, label="RICE"):
    """Burlap sack, (x,y) = bottom centre. Tied neck, stitched seam, grains spilling."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    poly(ctx, [(-70, 0), (-80, -90), (-45, -150), (45, -150), (80, -90), (70, 0)], hexc('#d8c08e'), INK, 3)
    poly(ctx, [(30, -150), (45, -150), (80, -90), (70, 0), (35, 0)], hexc('#bfa472'))
    poly(ctx, [(-30, -150), (-42, -185), (42, -185), (30, -150)], hexc('#d8c08e'), INK, 3)
    line(ctx, [(-34, -152), (34, -152)], hexc('#7a5a32'), 6)
    for k in range(7): line(ctx, [(-60+k*20, -20), (-55+k*20, -12)], hexc('#9a8058'), 2)
    text(ctx, label, 0, -80, 32, hexc('#6a4a28'))
    for gx, gy in [(-90, -4), (-100, -2), (85, -3), (95, -5), (-82, -10)]: ellipse(ctx, gx, gy, 5, 3, (1, 1, .95))
    ctx.restore()

def rice_bowl(ctx, x, y, s=1.0, fill_=1.0):
    """Small bowl with a heap of rice (fill_ 0..1), (x,y) = bottom centre. Use for 'grams of rice' / tiny portions."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if fill_ > 0:
        ctx.save(); ctx.scale(1, fill_); ctx.arc(0, -40/max(fill_, .01) + 0, 60, math.pi, 0); ctx.restore(); fill(ctx, (1, 1, .97)); ctx.restore(); ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    poly(ctx, [(-75, -45), (75, -45), (55, -5), (25, 0), (-25, 0), (-55, -5)], hexc('#e8eef2'), INK, 3)
    line(ctx, [(-65, -30), (65, -30)], hexc('#3a6fb0'), 5)
    ctx.restore()

def pork(ctx, x, y, s=1.0):
    """Cut of pork belly (layered fat/meat stripes), centre x,y."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    poly(ctx, [(-90, 45), (-80, -50), (85, -55), (95, 42)], hexc('#d9776b'), INK, 3)
    for k, c in enumerate(['#fbe4dc', '#c45e52', '#fbe4dc', '#c45e52']):
        yy = -28 + k*18; line(ctx, [(-84, yy), (90, yy-3)], hexc(c), 9)
    poly(ctx, [(-80, -50), (85, -55), (87, -40), (-79, -36)], hexc('#f3c9a8'), INK, 2)
    poly(ctx, [(95, 42), (85, -55), (110, -45), (118, 40)], hexc('#b9544a'), INK, 3)
    ctx.restore()

def kerosene_lamp(ctx, x, y, s=1.0, lit=True, t=0.0):
    """Hurricane lantern, (x,y) = bottom centre. Tin tank, glass globe with wire guards, top cap + bail handle."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if lit: circle(ctx, 0, -95, 70, (1, .85, .4), a=0.18)
    box(ctx, -45, -40, 90, 40, hexc('#b23b2e'), 8, INK, 3)                       # tank
    ctx.save(); ctx.translate(0, -95); ctx.scale(1, 1.25); ctx.arc(0, 0, 38, 0, 6.283); ctx.restore()
    fill(ctx, (0.95, 0.97, 1.0), .55); ctx.save(); ctx.translate(0, -95); ctx.scale(1, 1.25); ctx.arc(0, 0, 38, 0, 6.283); ctx.restore()
    ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    if lit:
        fl = 1 + 0.08*math.sin(t*20)
        poly(ctx, [(-8, -80), (0, -80-34*fl), (8, -80)], hexc('#ffb52e'), INK, 2)
    for dx in (-44, 44): line(ctx, [(dx*0.9, -45), (dx, -95), (dx*0.9, -145)], INK, 4)
    box(ctx, -32, -160, 64, 16, hexc('#b23b2e'), 4, INK, 3)
    ctx.arc(0, -160, 46, math.pi, 0); ctx.set_source_rgb(*INK); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()

def calendar(ctx, x, y, s=1.0, top="1986", big="MONTH", flip=0.0):
    """Tear-off wall calendar, centre x,y. flip 0..1 animates the top page tearing away upward."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    box(ctx, -90, -110, 180, 220, (1, 1, 1), 6, INK, 3); box(ctx, -90, -110, 180, 55, RED, 6, INK, 3)
    text(ctx, top, 0, -82, 34); text(ctx, big, 0, 20, 44 if len(big) > 3 else 80, INK)
    for k in (-50, 0, 50): circle(ctx, k, -110, 7, hexc('#555555'), INK, 2)
    if flip > 0:
        ctx.save(); ctx.translate(0, -55 - flip*160); ctx.rotate(-flip*0.8)
        box(ctx, -90, 0, 180, 165, (1, 1, 1), 6, INK, 3); ctx.restore()
    ctx.restore()

def cage(ctx, x, y, w, h, lock_label="EMBARGO", bars=7, lock=1.0):
    """Bird-cage style trap, (x,y) = bottom centre. Dome top, ring, vertical bars, base rail, padlock on front.
    RECURRING MOTIF: planted S12, reused S13-S15; opens later in the film."""
    lw = 7
    ctx.save()
    ctx.move_to(x-w/2, y-h*0.72); ctx.curve_to(x-w/2, y-h*1.02, x+w/2, y-h*1.02, x+w/2, y-h*0.72)
    ctx.set_source_rgb(*INK); ctx.set_line_width(lw+4); ctx.stroke_preserve(); ctx.set_source_rgb(*hexc('#9aa0a8')); ctx.set_line_width(lw); ctx.stroke()
    for i in range(bars):
        bx = x - w/2 + i*w/(bars-1)
        top = y - h*0.72 - (h*0.22)*math.sin(math.pi*i/(bars-1))
        line(ctx, [(bx, y), (bx, top)], INK, lw+4); line(ctx, [(bx, y), (bx, top)], hexc('#9aa0a8'), lw)
    for yy in (y, y-h*0.72):
        line(ctx, [(x-w/2-6, yy), (x+w/2+6, yy)], INK, 16); line(ctx, [(x-w/2-6, yy), (x+w/2+6, yy)], hexc('#6f757d'), 11)
    ctx.arc(x, y-h*0.95-16, 16, 0, 6.283); ctx.set_source_rgb(*INK); ctx.set_line_width(lw); ctx.stroke()
    if lock > 0: padlock(ctx, x, y-h*0.36, lock*min(1.0, w/340), lock_label)
    ctx.restore()

def padlock(ctx, x, y, s=1.0, label="EMBARGO"):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.arc(0, -30, 26, math.pi, 0); ctx.set_source_rgb(*INK); ctx.set_line_width(14); ctx.stroke()
    ctx.arc(0, -30, 26, math.pi, 0); ctx.set_source_rgb(*hexc('#b0b5bb')); ctx.set_line_width(8); ctx.stroke()
    box(ctx, -48, -32, 96, 72, hexc('#d9a62e'), 8, INK, 3); box(ctx, 14, -32, 34, 72, hexc('#b8861e'), 6)
    circle(ctx, 0, -6, 7, INK); poly(ctx, [(-4, -4), (4, -4), (2, 12), (-2, 12)], INK)
    if label:
        ctx.save(); ctx.translate(0, 64); ctx.rotate(-0.06)
        box(ctx, -78, -20, 156, 40, PAPER, 4, INK, 2.5); text(ctx, label, 0, 1, 28, hexc('#8a2f2f'))
        line(ctx, [(0, -20), (0, -54)], INK, 2)
        ctx.restore()
    ctx.restore()

def ussr_pillar(ctx, x, y, h=460, crumble=0.0, t=0.0, label="USSR"):
    """Tall grey stone column of stacked blocks, (x,y) = bottom centre. Plain 'USSR' lettering, no emblem.
    crumble 0..1: blocks crack, slide and fall in order top->bottom with rotation (use with shake + dust)."""
    n = 7; bh = h/n; w = 150
    for i in range(n):                              # i=0 bottom
        f = clamp(crumble*1.6 - (n-1-i)*0.12)       # top blocks go first
        dx = (i % 2 * 2 - 1) * f * (60 + i*25); dy = f*f*(h*0.9 - i*bh*0.4)*1.0 + 0
        rot = (i % 2 * 2 - 1) * f * (0.5 + i*0.1)
        cx, cy = x + dx, y - bh*(i+0.5) + dy*(1 if i > 0 else 0.1)
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot)
        ww = w - (i == n-1)*0 + (i == 0)*40
        box(ctx, -ww/2, -bh/2, ww, bh, SOV, 3, INK, 3)
        box(ctx, ww/2-ww*0.22, -bh/2+3, ww*0.22-3, bh-6, SOV_D)
        box(ctx, -ww/2+4, -bh/2+4, ww*0.12, bh-8, SOV_L)
        if crumble > 0.05 + i*0.03 and f < 0.98:
            line(ctx, [(-ww*0.1, -bh/2), (ww*0.02, -bh*0.1), (-ww*0.06, bh*0.15), (ww*0.08, bh/2)], INK, 3)
        ctx.restore()
    if crumble < 0.35:
        ctx.save(); ctx.translate(x, y - h*0.55); ctx.rotate(-math.pi/2)
        text(ctx, label, 0, 4, 64, hexc('#3e4248'))
        ctx.restore()

def stone_mill(ctx, x, y, s=1.0, ang=0.0, pole_dir=1):
    """Hand rice-grinding mill (side view). (x,y) = bottom centre. Two stone cylinders (wide base, taller top),
    grain hopper hole, chiselled grooves rotate with ang, wooden push-pole from the top stone to the pusher's hands.
    Returns the pole-end point (scene coords) -> put the pusher's hands there."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    def cyl(cx, top, rx, ry, hgt, c, cd, cl):
        def body():
            ctx.move_to(cx-rx, top); ctx.line_to(cx-rx, top+hgt); ctx.curve_to(cx-rx, top+hgt+ry*1.3, cx+rx, top+hgt+ry*1.3, cx+rx, top+hgt)
            ctx.line_to(cx+rx, top); ctx.close_path()
        body(); ctx.set_source_rgb(*c); ctx.fill(); ctx.save(); body(); ctx.clip(); box(ctx, cx+rx*0.45, top, rx*0.6, hgt+ry*2, cd); ctx.restore()
        body(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
        ctx.save(); ctx.translate(cx, top); ctx.scale(1, ry/rx); ctx.arc(0, 0, rx, 0, 6.283); ctx.restore()
        ctx.set_source_rgb(*cl); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    ellipse(ctx, 0, 0, 200, 26, (0, 0, 0), a=.18)
    cyl(0, -70, 175, 34, 60, hexc('#8f897e'), hexc('#77716a'), hexc('#a7a092'))
    cyl(0, -170, 135, 28, 95, hexc('#a39d90'), hexc('#878175'), hexc('#bdb6a8'))
    for k in range(6):                                  # grooves on the visible front, rotating
        a = ang + k*1.047; px = math.sin(a)*120
        if math.cos(a) > 0: line(ctx, [(px, -160), (px*0.97, -82)], hexc('#6f695f'), 4)
    ellipse(ctx, 0, -170, 34, 9, hexc('#4a453e'))
    for gx in (-10, 4, 14): ellipse(ctx, gx, -172, 5, 3, (1, 1, .95))
    pa = math.sin(ang)*95; pb = -170 - math.cos(ang)*6
    end = (pa + pole_dir*300, -125)
    line(ctx, [(pa, pb), end], INK, 20); line(ctx, [(pa, pb), end], hexc('#9b6b3c'), 13)
    box(ctx, pa-9, pb-30, 18, 34, hexc('#7a5230'), 3, INK, 3)
    ctx.restore()
    return (x + end[0]*s, y + end[1]*s)

def state_counter(ctx, x, y, w=520):
    """State store counter: wooden counter top at y, iron grille window above, sign plain text. Centre x."""
    box(ctx, x-w/2, y, w, 180, hexc('#8b5a33'), 0, INK, 3); box(ctx, x-w/2, y-14, w, 20, hexc('#a8703f'), 3, INK, 3)
    for k in range(5): line(ctx, [(x-w/2+20+k*w/5, y+20), (x-w/2+20+k*w/5, y+170)], hexc('#6e4524'), 3)
    box(ctx, x-w/2, y-330, w, 40, hexc('#b23b2e'), 4, INK, 3); text(ctx, "STATE STORE", x, y-309, 34)

def coin(ctx, x, y, r=22):
    circle(ctx, x, y, r, hexc('#f0c24a'), INK, 2.5); circle(ctx, x, y, r*0.66, hexc('#e0ac2c')); text(ctx, "$", x, y+2, r*1.2, hexc('#8a6418'))

def keyword(ctx, t, start, s, x, y, size=72, seed=5):
    """House keyword: white text with ink outline, popped on its word."""
    popped(ctx, t, start, x, y, lambda c: text(c, s, 0, 0, size, (1, 1, 1), outline=INK), seed=seed)

def sticky(ctx, x, y, s, rot=-0.05, c=hexc('#ffe36e'), size=44):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    box(ctx, -95, -60, 190, 120, c, 3, INK, 2.5)
    ls = s.split("\n")                                   # multi-line allowed: 'AVERAGE\nCITIZEN'
    for i, l in enumerate(ls): text(ctx, l, 0, 4 + (i - (len(ls)-1)/2)*size*0.95, size, INK)
    ctx.restore()

def dust(ctx, x, y, t, start, n=5, size=70, seed=1):
    """A burst of smoke puffs (impacts, collapse)."""
    for k in range(n):
        life = clamp((t - start - k*0.05)/0.8)
        if 0 < life < 1: smoke(ctx, x + (k - n/2)*size*0.5, y - (k % 2)*size*0.3, life, size, seed+k)

def arm_to(p, x, y, side, target):
    """Arm offset so the hand of puppet p (waist at x,y) lands on target (scene coords). side -1 = armL, +1 = armR.
    Usage: armR=arm_to(p, x, y, 1, (tx, ty)). Pass cross=True to draw() if the target is across the body midline."""
    s = p.scale*(0.82 if p.kid else 1.0); tw, th = (150, 190) if not p.kid else (130, 150)
    sh = (x + side*(tw/2-10)*s, y + (-th+34)*s)
    return ((target[0]-sh[0])/s, (target[1]-sh[1])/s)

def caged_map(ctx, x, y, h=440, tilt=0.0, lock=1.0, cracks=1.0):
    """RECURRING: the map of Vietnam inside the EMBARGO cage. (x,y) = cage bottom centre, h = cage height.
    tilt in radians rotates the whole thing about its bottom-right corner (for leaning/falling)."""
    w = h*0.82
    ctx.save(); ctx.translate(x + w/2, y); ctx.rotate(tilt); ctx.translate(-(x + w/2), -y)
    vietnam_map(ctx, x, y - h*0.47, h*0.72, cracks=cracks)
    cage(ctx, x, y, w, h, lock=lock)
    ctx.restore()

def rubber_stamp(ctx, x, y, s=1.0):
    """Office rubber stamp, (x,y) = bottom centre of the rubber face. Wooden knob handle + block + purple pad."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    box(ctx, -60, -14, 120, 14, STAMP, 3, INK, 3)
    box(ctx, -66, -52, 132, 40, hexc('#a8703f'), 6, INK, 3); box(ctx, 30, -50, 34, 36, hexc('#8b5a33'))
    box(ctx, -14, -110, 28, 60, hexc('#a8703f'), 6, INK, 3)
    circle(ctx, 0, -125, 30, hexc('#8b5a33'), INK, 3); circle(ctx, -9, -133, 9, hexc('#b98a5e'))
    ctx.restore()

def globe(ctx, x, y, r=150, t=0.0):
    """Generic globe: ocean disc, simple drifting continent blobs, latitude lines. No real-country accuracy needed."""
    circle(ctx, x, y, r, hexc('#5fa8d9'), INK, 3)
    ctx.save(); ctx.arc(x, y, r-2, 0, 6.283); ctx.clip()
    off = (t*30) % (r*4)
    for bx, by, rx, ry in [(-0.5, -0.35, .35, .25), (-0.3, 0.3, .25, .4), (0.35, -0.3, .45, .28), (0.55, 0.35, .2, .2), (1.4, -0.2, .4, .3)]:
        cx = x + bx*r + off - r*2 if bx*r + off > r*2 else x + bx*r + off
        ellipse(ctx, cx, y + by*r, rx*r, ry*r, hexc('#7cbf5a'))
    for k in (-0.5, 0, 0.5): ellipse(ctx, x, y + k*r, r*(1-abs(k)*0.3), r*0.08, hexc('#4f95c6'), a=0.0)
    ctx.restore()
    for k in (-0.45, 0.45):
        ctx.save(); ctx.translate(x, y + k*r); ctx.scale(1, 0.12); ctx.arc(0, 0, r*0.89, 0, 3.1416); ctx.restore()
        ctx.set_source_rgba(1, 1, 1, .5); ctx.set_line_width(2); ctx.stroke()
    circle(ctx, x - r*0.35, y - r*0.4, r*0.18, (1, 1, 1), a=0.25)

def price_tag(ctx, x, y, s=1.0, value="100", walk=None, t=0.0):
    """Shop price tag with optional running legs. (x,y) = tag centre. walk = phase (e.g. t*3) -> rubber-hose legs run."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    if walk is not None:
        for side, off in ((-1, 0), (1, math.pi)):
            sw = math.sin(walk*math.pi*2 + off)*26
            hip = (side*22, 50); foot = (side*20 + sw, 120 - max(0, math.cos(walk*math.pi*2 + off))*14)
            hose(ctx, hip, foot, 0.1*side, 8); line(ctx, [foot, (foot[0]+16, foot[1])], INK, 8)
    poly(ctx, [(-80, -55), (60, -55), (100, 0), (60, 55), (-80, 55)], hexc('#fff6d6'), INK, 3)
    circle(ctx, 70, 0, 9, hexc('#e9e1cf'), INK, 2.5)
    text(ctx, "RICE 1 kg", -10, -26, 26, hexc('#5a4632')); text(ctx, value, -10, 18, 46, RED)
    ctx.restore()
