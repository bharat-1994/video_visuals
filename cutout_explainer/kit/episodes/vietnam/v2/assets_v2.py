"""Vietnam v2: cast, backgrounds and props (REVISION_v2.md sections 5-7).
Cast: the family (lan, minh) + bunny / us_official / cn_official, built like assets.py's VPuppet.
Backgrounds and props follow the house rules: flat colours, 2-3 tones per material, INK outlines,
detail via loops, no gradients, no real logos/emblems/flags/seals (brand colour + plain lettering only)."""
import sys, os, math, random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "engine")))
from lib import *
import lib
from episodes.vietnam.assets_ind import skyline
from episodes.vietnam.assets import vcast, VPuppet, non_la, toque, state_cap, coin, RED, PAPER, NIGHT, MAP_C

def _mix(a, b, t): return tuple(lerp(x, y, t) for x, y in zip(a, b))
def _dk(c, k=0.25): return _mix(c, (0, 0, 0), k)
def _lt(c, k=0.3): return _mix(c, (1, 1, 1), k)
def _C(c): return hexc(c) if isinstance(c, str) else c

# ================= CAST v2 (section 5) =================
# The family: Ba = v1 farmer; Lan = the S08 kid grown up (same black hair, similar face); Minh = Lan's son.
_V2C = {
    "lan":        dict(hair="wavy", hair_c=hexc('#1a1614'), shirt=hexc('#8fc1e3'), jaw=0.15, collar=True),
    "minh":       dict(hair="short", hair_c=hexc('#1a1614'), shirt=(1, 1, 1), jaw=0.3, collar=True, glasses=True, nose=True),
    "bunny":      dict(hair="bald", hair_c=(0.93, 0.94, 0.96), shirt=(0.95, 0.96, 0.98), jaw=0.15, collar=False),
    "us_official": dict(hair="part", hair_c=hexc('#a8794f'), shirt=(1, 1, 1), jacket=hexc('#232b45'), tie=hexc('#b23a3a'), jaw=0.85, nose=True, brow_w=7),
    "cn_official": dict(hair="part", hair_c=hexc('#1a1614'), shirt=(1, 1, 1), jacket=hexc('#3d4248'), tie=hexc('#4a5568'), jaw=0.35, glasses=True, nose=True),
}

class V2Puppet:
    """Same draw() signature as VPuppet; adds per-character extras (bun + cap, lanyard, cleanroom hood/mask/gloves)."""
    def __init__(self, who, scale=1.0):
        self.who = who
        self.p = Puppet(scale=scale, seed=sum(map(ord, who)) % 97, **_V2C[who])
    def __getattr__(self, k): return getattr(self.p, k)

    def draw(self, ctx, x, y, t, expr="neutral", talking=False, facing=0.0, hat=True, **kw):
        info = self.p.draw(ctx, x, y, t, expr, talking, facing, **kw)
        hx, hy = info['head']; R = info['R']; hx += facing*R*0.12
        s = self.p.scale
        if self.who == "lan":
            # low bun at the side of the jaw (tied strand), small work cap on the crown when hat=True
            bx, by = hx - R*1.10, hy + R*0.40          # low bun peeking from behind the nape, outside the face
            line(ctx, [(hx - R*0.88, hy + R*0.22), (bx + R*0.10, by - R*0.08)], hexc('#1a1614'), max(3, R*0.14))
            circle(ctx, bx, by, R*0.24, hexc('#1a1614'), INK, 2.5)
            line(ctx, [(bx - R*0.04, by - R*0.22), (bx + R*0.12, by - R*0.10)], hexc('#c9504f'), max(2, R*0.06))
            if hat:
                cx0 = hx + facing*R*0.10
                ctx.save(); ctx.translate(cx0, hy - R*0.10)
                ctx.arc(0, 0, R*1.28, math.pi, 2*math.pi); ctx.close_path(); ctx.clip()
                box(ctx, -R*1.4, -R*1.5, R*2.8, R*1.07, hexc('#6fa8cc'))
                ctx.restore()
                ctx.save(); ctx.translate(cx0, hy - R*0.10)
                ctx.new_path(); ctx.arc(0, 0, R*1.28, math.pi, 2*math.pi)
                ctx.set_source_rgb(*INK); ctx.set_line_width(max(2, R*0.035)); ctx.stroke(); ctx.restore()
                line(ctx, [(cx0 - R*1.18, hy - R*0.53), (cx0 + R*1.18, hy - R*0.53)], INK, max(2, R*0.04))
                line(ctx, [(cx0 - R*0.9, hy - R*0.62), (cx0 + R*0.9, hy - R*0.62)], hexc('#5d97bd'), max(2, R*0.05))
        elif self.who == "minh":
            # blue lanyard with a white badge
            ty_ = y + (-190 + 34)*s
            line(ctx, [(x - 42*s, ty_), (x, y + (-190 + 118)*s), (x + 42*s, ty_)], hexc('#2f6db5'), max(3, 7*s))
            box(ctx, x - 16*s, y + (-190 + 112)*s, 32*s, 26*s, (1, 1, 1), 3*s, INK, max(2, 2.5*s))
            box(ctx, x - 16*s, y + (-190 + 112)*s, 32*s, 7*s, hexc('#2f6db5'), 3*s)
        elif self.who == "bunny":
            # cleanroom hood: a white ring framing the face (eyes stay visible), mask over the mouth, white gloves
            ctx.save()
            ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
            ctx.new_path(); ctx.arc(hx, hy - R*0.06, R*1.30, 0, 2*math.pi)
            ctx.new_sub_path(); ctx.arc(hx, hy - R*0.06, R*0.96, 0, 2*math.pi)
            ctx.set_source_rgb(*hexc('#eef0f4')); ctx.fill()
            ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
            ctx.new_path(); ctx.arc(hx, hy - R*0.06, R*1.30, 0, 2*math.pi); ctx.set_source_rgb(*INK); ctx.set_line_width(max(2, R*0.03)); ctx.stroke()
            ctx.new_path(); ctx.arc(hx, hy - R*0.06, R*0.96, 0, 2*math.pi); ctx.stroke()
            ctx.restore()
            f = facing
            fx = hx + f*R*0.30
            my = hy + R*0.42
            ctx.save(); ctx.translate(fx, my + R*0.10); ctx.rotate(f*0.12)
            rrect(ctx, -R*0.60, -R*0.26, R*1.20, R*0.72, R*0.24); ctx.set_source_rgb(1, 1, 1)
            ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(max(2, R*0.035)); ctx.stroke()
            for yy in (R*0.04, R*0.20): line(ctx, [(-R*0.48, yy), (R*0.48, yy)], hexc('#c9ced6'), max(1.5, R*0.025))
            ctx.restore()
            line(ctx, [(fx + R*0.58, my - R*0.02), (hx - f*R*0.85, hy - R*0.1)], (1, 1, 1), max(2, R*0.05))
            for hd in ("handL", "handR"):
                gx, gy = info[hd]; circle(ctx, gx, gy, 8.5*s, (1, 1, 1), INK, 2.5)
        return info

def v2cast(who, scale=1.0):
    """v2 cast ids (lan minh bunny us_official cn_official); falls back to the v1 cast for every other id."""
    return V2Puppet(who, scale) if who in _V2C else vcast(who, scale)

# ================= BACKGROUNDS (section 6; merged from _bg_draft.py) =================

"""SCRATCH DRAFT (_bg_draft.py): P1 full-frame cartoon backgrounds for Vietnam v2.
A lead engineer merges this into assets_v2.py. All randomness is seeded; all motion is t-deterministic.
Signature: def bg_NAME(ctx, t=0.0, **kv) — canvas 1280x720, ground band y~560-640, nothing important below y=630.
"""

# ---------------- shared helpers ----------------
C = lambda c: hexc(c) if isinstance(c, str) else c
def _abox(ctx, x, y, w, h, c, a=1):
    """Flat rectangle with alpha (box() has no alpha)."""
    poly(ctx, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], C(c), a=a)

def _tree(ctx, x, y, s=1.0, leaf='#4f7a3a'):
    """Leafy street tree. (x,y)=base."""
    lc, ld, tl = C(leaf), _dk(C(leaf), .22), hexc('#6b4b2a')
    box(ctx, x - 5*s, y - 74*s, 10*s, 74*s, tl, 0, INK, 2)
    for dx, dy, r in ((-26, -84, 24), (24, -86, 22), (0, -108, 27), (-14, -66, 19), (16, -64, 19)):
        circle(ctx, x + dx*s, y + dy*s, r*s, lc, INK, 2)
    for dx, dy, r in ((-10, -112, 12), (14, -92, 10), (-28, -88, 9)):
        circle(ctx, x + dx*s, y + dy*s, r*s, _lt(lc, .22))
    for dx, dy, r in ((-20, -70, 10), (8, -70, 9)):
        circle(ctx, x + dx*s, y + dy*s, r*s, ld)

def _shutter(ctx, x, y, w, h, open_=0.0, c='#8a8f96'):
    """Roll-down shop shutter. (x,y)=top-left of opening. open_: 0 closed .. 1 fully rolled up."""
    cc = C(c)
    box(ctx, x - 4, y - 4, w + 8, h + 8, _dk(cc, .45), 0, INK, 2)         # frame
    box(ctx, x, y, w, h, _lt(cc, .55))                                     # opening behind
    rh = max(0.0, h * (1 - open_))
    for k in range(int(rh // 7) + 1):                                      # slats
        line(ctx, [(x, y + 3 + k*7), (x + w, y + 3 + k*7)], _dk(cc, .28), 1.6)
    box(ctx, x, y, w, rh, cc) if False else None
    box(ctx, x - 2, y + rh - 5, w + 4, 8, _dk(cc, .35), 2, INK, 2)         # bottom bar
    box(ctx, x - 2, y - 10, w + 4, 10, _dk(cc, .5), 2, INK, 2)             # roll housing

def _bicycle(ctx, x, y, s=1.0, c='#43608a'):
    """Parked bicycle, side view. (x,y)=ground centre."""
    r = 15*s
    for wx in (-24*s, 24*s):
        ctx.new_sub_path(); ctx.arc(x + wx, y - r, r, 0, 6.283)
        ctx.set_source_rgb(*INK); ctx.set_line_width(3*s); ctx.stroke()
        for k in range(4):
            a = k * math.pi / 4 + 0.4
            line(ctx, [(x + wx, y - r), (x + wx + math.cos(a)*r*.78, y - r + math.sin(a)*r*.78)], (0.72, 0.72, 0.75), 1.4*s)
    line(ctx, [(x - 24*s, y - r), (x - 4*s, y - 2.05*r), (x + 11*s, y - 2.05*r), (x + 24*s, y - r)], C(c), 3.2*s)
    line(ctx, [(x - 24*s, y - r), (x + 2*s, y - r), (x + 11*s, y - 2.05*r)], C(c), 3.2*s)
    line(ctx, [(x - 4*s, y - 2.05*r), (x + 2*s, y - r)], C(c), 3.2*s)
    line(ctx, [(x + 11*s, y - 2.05*r), (x + 14*s, y - 2.6*r)], INK, 3*s)
    line(ctx, [(x + 9*s, y - 2.62*r), (x + 19*s, y - 2.55*r)], INK, 3*s)     # handlebar
    line(ctx, [(x - 4*s, y - 2.1*r), (x - 8*s, y - 2.5*r)], INK, 3*s)
    line(ctx, [(x - 14*s, y - 2.55*r), (x - 3*s, y - 2.5*r)], INK, 4*s)      # saddle
    circle(ctx, x + 2*s, y - r, 5*s, (0.5, 0.5, 0.55), INK, 1.6*s)

def _wire_bundle(ctx, x0, y0, x1, y1, n=5, sag=26, c=None, lw=1.6):
    """A bundle of drooping overhead wires between two points."""
    cc = c or INK
    for k in range(n):
        a, b = y0 + k*6, y1 + k*6
        mx = (x0 + x1) / 2; my = max(a, b) + sag + k*7
        ctx.move_to(x0, a); ctx.curve_to(mx, my, mx, my, x1, b)
        ctx.set_source_rgb(*cc); ctx.set_line_width(lw); ctx.stroke()

def _pole(ctx, x, base, top, c='#9a948a'):
    """Concrete utility pole with cross-arm + insulators."""
    cc = C(c)
    box(ctx, x - 5, top, 10, base - top, cc, 0, INK, 2)
    box(ctx, x - 5, top, 4, base - top, _lt(cc, .18))
    box(ctx, x - 42, top + 16, 84, 6, _dk(cc, .25), 0, INK, 2)
    box(ctx, x - 34, top + 34, 68, 5, _dk(cc, .25), 0, INK, 2)
    for dx in (-36, -12, 12, 36): circle(ctx, x + dx, top + 12, 3.2, hexc('#4a5a4a'), INK, 1.5)

def _banner(ctx, x, y, w, h, c):
    """Plain cloth banner (no emblem), scalloped bottom, hanging from a rod."""
    cc = C(c)
    line(ctx, [(x - 6, y), (x + w + 6, y)], INK, 3)
    poly(ctx, [(x, y), (x + w, y), (x + w, y + h), (x + w*.75, y + h - 9), (x + w*.5, y + h),
               (x + w*.25, y + h - 9), (x, y + h)], cc, INK, 2)
    box(ctx, x + w*.68, y + 2, w*.32 - 2, h - 12, _dk(cc, .16))
    for k in range(3): line(ctx, [(x + 3 + k*(w/3), y + 2), (x + 3 + k*(w/3), y + h - 14)], _dk(cc, .22), 1.2, .5)

def _sign(ctx, x, y, w, h, c, word, tc=(1, 1, 1), size=None):
    """Plain shop sign: coloured board + generic word, no logo."""
    cc = C(c)
    box(ctx, x, y, w, h, cc, 3, INK, 2.5)
    box(ctx, x + 2, y + h - 7, w - 4, 5, _dk(cc, .28))
    box(ctx, x + 2, y + 2, w - 4, 4, _lt(cc, .3))
    text(ctx, word, x + w/2, y + h/2 + 2, size or int(h*.66), C(tc) if isinstance(tc, str) else tc)

def _tube_house(ctx, x, w, top, fc, open_=0.0, sign=None, sc=None, tc=(1, 1, 1),
                balcony=False, awning=None, shutter_c='#8a8f96'):
    """Narrow 3-storey tube house, facade from `top` down to base=560."""
    base = 560
    fd = _dk(fc, .18)
    box(ctx, x, top, w, base - top, fc, 0, INK, 2.5)
    box(ctx, x + w*.82, top + 2, w*.18 - 2, base - top - 4, fd)
    box(ctx, x - 5, top - 12, w + 10, 14, _dk(fc, .42), 0, INK, 2.5)      # roof slab
    box(ctx, x - 5, top - 12, w + 10, 4, _dk(fc, .28))
    # window rows (upper floors)
    nrow = 0
    for wy in (top + 26, top + 108, top + 190):
        if wy + 44 > 466: continue
        for k in range(2):
            wx = x + 14 + k*(w*.44)
            ww, wh = w*.34, 42
            box(ctx, wx - 3, wy - 3, ww + 6, wh + 6, _dk(fc, .35), 0, INK, 2)
            box(ctx, wx, wy, ww, wh, hexc('#3d3a34'))
            poly(ctx, [(wx + ww*.45, wy), (wx + ww, wy), (wx + ww, wy + wh*.55)], hexc('#71685a'))
            line(ctx, [(wx + ww/2, wy), (wx + ww/2, wy + wh)], hexc('#8b8578'), 2)
            for gy in range(1, 3): line(ctx, [(wx, wy + gy*wh/3), (wx + ww, wy + gy*wh/3)], hexc('#8b8578'), 1.2)
        nrow += 1
    if balcony and nrow >= 2:
        by = top + 150
        box(ctx, x + 6, by, w - 12, 8, _dk(fc, .3), 0, INK, 2)
        for k in range(int((w - 12)//9)):
            line(ctx, [(x + 10 + k*9, by), (x + 10 + k*9, by - 26)], hexc('#6a6459'), 2)
        box(ctx, x + 6, by - 30, w - 12, 5, hexc('#6a6459'), 0, INK, 2)
    # ground floor: doorway + shuttered shop opening
    ox, ow = x + w*.42, w*.5
    box(ctx, x + 8, 486, w*.28, 74, hexc('#4a3a28'), 0, INK, 2.5)         # doorway
    for k in range(3): line(ctx, [(x + 10 + k*w*.09, 488), (x + 10 + k*w*.09, 558)], hexc('#5a4630'), 2)
    _shutter(ctx, ox, 484, ow, 76, open_, shutter_c)
    if sign:
        _sign(ctx, x + 4, 448, w - 8, 30, sc or '#b03a2e', sign, tc, size=22)
    if awning:
        ac = C(awning)
        poly(ctx, [(x + 4, 448), (x + w - 4, 448), (x + w + 4, 470), (x - 4, 470)], ac, INK, 2)
        for k in range(5):
            if k % 2: line(ctx, [(lerp(x + 4, x + w + 4, k/5), 448), (lerp(x - 4, x - 4 + 8, 0) , 470)], _lt(ac, .5), 0)
        for k in range(6):
            x0 = lerp(x + 2, x + w - 2, k/5); x1 = lerp(x - 2, x + w + 2, k/5)
            line(ctx, [(x0, 448), (x1, 470)], _lt(ac, .45), 4)

# ============================================================
# 1. bg_hanoi_1986 — muted pre-Đổi Mới street
# ============================================================
def bg_hanoi_1986(ctx, t=0.0, **kv):
    """1986 Hanoi street: faded ochre tube houses, closed shutters, tangled wires, bicycles, plain banners."""
    pal = [C('#cbb27e'), C('#c2a266'), C('#d2bd92'), C('#b89a68'), C('#c9ab7c'),
           C('#bfae87'), C('#c7a878'), C('#b69f74')]
    box(ctx, 0, 0, W, 560, C('#b7bfb9'))                                   # muted sky
    for cx, cw, ch in ((150, 300, 90), (700, 420, 110), (1080, 260, 80)):  # flat cloud bands
        ellipse(ctx, cx, ch*0.7, cw/2, 26, C('#c9d0c9'), a=.85)
    spec = [(-30, 165, 150), (135, 120, 186), (255, 170, 158), (425, 128, 200),
            (553, 158, 168), (711, 122, 190), (833, 168, 152), (1001, 140, 184), (1141, 170, 166)]
    for i, (hx, hw, ht) in enumerate(spec):
        _tube_house(ctx, hx, hw, ht, pal[i % len(pal)],
                    open_=(0.0 if i % 3 == 1 else (0.85 if i % 4 == 0 else 0.0)),
                    balcony=(i % 3 == 0))
        if i % 4 == 1:                                                     # rooftop water tank
            box(ctx, hx + hw*.5, ht - 40, 26, 28, hexc('#5a5f66'), 3, INK, 2)
        if i % 5 == 2:                                                     # rooftop tuft
            for dx in (0, 7, -6): line(ctx, [(hx + hw*.3 + dx, ht - 12), (hx + hw*.3 + dx*1.6, ht - 26)], C('#5f7a44'), 2)
    _banner(ctx, 300, 200, 40, 130, '#b0483a'); _banner(ctx, 875, 210, 36, 118, '#c9a23e')
    # poles + tangled overhead wires
    _pole(ctx, 208, 560, 96); _pole(ctx, 1052, 560, 84)
    _wire_bundle(ctx, -10, 118, 208, 108, n=6, sag=34)
    _wire_bundle(ctx, 208, 104, 1052, 92, n=7, sag=52)
    _wire_bundle(ctx, 1052, 100, 1290, 128, n=6, sag=30)
    _wire_bundle(ctx, 208, 138, 640, 126, n=3, sag=44)                     # second tangle layer
    for px, hx in ((208, 255), (208, 425), (1052, 711), (1052, 1001)):     # service drops
        _wire_bundle(ctx, px, 150, hx, 196, n=2, sag=8)
    circle(ctx, 208, 176, 5, hexc('#3a3f4a'), INK, 1.5)                    # transformer can
    box(ctx, 200, 182, 16, 26, hexc('#4a5058'), 2, INK, 1.5)
    # sidewalk + road
    box(ctx, 0, 560, W, 40, C('#a49e90')); line(ctx, [(0, 560), (W, 560)], INK, 2.5, .5)
    for k in range(11): line(ctx, [(60 + k*118, 562), (48 + k*118, 598)], C('#8f897c'), 2)
    box(ctx, 0, 600, W, 120, C('#7b7873')); line(ctx, [(0, 600), (W, 600)], INK, 2.5, .5)
    for px, py, pr in ((300, 668, 26), (860, 690, 30), (1180, 650, 20)):   # patched asphalt (below 630 = plain)
        ellipse(ctx, px, py, pr, pr*.4, C('#6c6a66'), a=.6)
    _bicycle(ctx, 355, 598, .95, '#4a5f7a'); _bicycle(ctx, 725, 598, .9, '#5a4a58'); _bicycle(ctx, 1010, 598, .95, '#42604c')
    _tree(ctx, 62, 598, 1.05, '#54713e'); _tree(ctx, 1238, 598, .95, '#4f7a3a')

# ============================================================
# 2. bg_hanoi_street_1990 — P2 cheap variant (brighter, shops reopening)
# ============================================================
def bg_hanoi_street_1990(ctx, t=0.0, **kv):
    """1990 Hanoi street: same grammar as 1986 but brighter, more shutters rolled up, a couple of plain signs."""
    pal = [C('#dcc48e'), C('#d4b478'), C('#e4cfa0'), C('#caab76'), C('#d9bc8a'),
           C('#d2c096'), C('#ddb986'), C('#cab082'), C('#d9c294')]
    box(ctx, 0, 0, W, 560, C('#c6d6da'))
    for cx, cw in ((150, 300), (700, 420), (1080, 260)):
        ellipse(ctx, cx, 60, cw/2, 24, (1, 1, 1), a=.55)
    spec = [(-30, 165, 150), (135, 120, 186), (255, 170, 158), (425, 128, 200),
            (553, 158, 168), (711, 122, 190), (833, 168, 152), (1001, 140, 184), (1141, 170, 166)]
    for i, (hx, hw, ht) in enumerate(spec):
        _tube_house(ctx, hx, hw, ht, pal[i % len(pal)],
                    open_=(0.9 if i % 2 == 0 else 0.15), balcony=(i % 3 == 1),
                    sign=("CAFE" if i == 2 else "SHOP" if i == 5 else None), sc='#7a8f5a')
    _banner(ctx, 300, 200, 40, 130, '#c05a44'); _banner(ctx, 875, 210, 36, 118, '#d8b04e')
    _pole(ctx, 208, 560, 96); _pole(ctx, 1052, 560, 84)
    _wire_bundle(ctx, -10, 118, 208, 108, n=5, sag=34)
    _wire_bundle(ctx, 208, 104, 1052, 92, n=6, sag=52)
    _wire_bundle(ctx, 1052, 100, 1290, 128, n=5, sag=30)
    box(ctx, 0, 560, W, 40, C('#b0aa9c')); line(ctx, [(0, 560), (W, 560)], INK, 2.5, .5)
    box(ctx, 0, 600, W, 120, C('#84817c')); line(ctx, [(0, 600), (W, 600)], INK, 2.5, .5)
    _bicycle(ctx, 480, 598, .95, '#4a5f7a'); _bicycle(ctx, 940, 598, .95, '#6a4a4a')
    _tree(ctx, 62, 598, 1.05, '#5c7f42'); _tree(ctx, 1238, 598, .95, '#57823f')

# ============================================================
# 3. bg_hanoi_today — bright street + motorbike stream
# ============================================================
def _moto(ctx, x, y, s=1.0, flip=1, body='#b03a2e', rider='#3a4a6a'):
    """Small motorbike+rider, side view. (x,y)=ground centre between wheels."""
    bc, rc = C(body), C(rider)
    ctx.save(); ctx.translate(x, y); ctx.scale(s * flip, s)
    for wx in (-24, 24):
        circle(ctx, wx, -11, 11, hexc('#23262c'), INK, 2); circle(ctx, wx, -11, 4.5, hexc('#9aa0a8'))
    box(ctx, -18, -30, 36, 12, bc, 5, INK, 2)
    poly(ctx, [(14, -30), (26, -46), (22, -30)], bc, INK, 2)
    line(ctx, [(24, -46), (18, -54)], INK, 3)
    box(ctx, -24, -36, 16, 8, _dk(bc, .3), 3, INK, 2)
    poly(ctx, [(-10, -34), (6, -34), (10, -60), (-6, -62)], rc, INK, 2)    # rider torso
    circle(ctx, 2, -70, 8, SKIN, INK, 2)                                   # head
    circle(ctx, 2, -72, 9, hexc('#e8e8e4'), INK, 2, a=.95)                 # helmet
    line(ctx, [(4, -56), (16, -50)], rc, 5)                                # arm to bars
    ctx.restore()

def bg_hanoi_today(ctx, t=0.0, **kv):
    """Today's Hanoi: bright shophouses with generic signs, glass towers behind, motorbike stream animated by t."""
    pal = [C('#f0d79e'), C('#e8c48c'), C('#f2dfae'), C('#dfc09a'), C('#eed2a2'),
           C('#e2cba4'), C('#f4d9a8'), C('#e6c496'), C('#f0dda8')]
    box(ctx, 0, 0, W, 560, C('#c3e2f0'))
    ellipse(ctx, 220, 70, 120, 26, (1, 1, 1), a=.8); ellipse(ctx, 940, 52, 150, 28, (1, 1, 1), a=.8)
    # glass towers behind the roofline
    for tx, tw, th, tc in ((280, 96, 470, '#9fc4dc'), (620, 120, 505, '#8fb6d2'), (950, 90, 455, '#a6cbe0')):
        tcol = C(tc)
        box(ctx, tx, 560 - th, tw, th, tcol, 0, INK, 2.5)
        box(ctx, tx + tw*.76, 560 - th + 2, tw*.24 - 2, th - 4, _dk(tcol, .16))
        for r_ in range(int(th // 26)):
            for c_ in range(int(tw // 16)):
                box(ctx, tx + 6 + c_*16, 560 - th + 10 + r_*26, 11, 18, _lt(tcol, .38) if (r_ + c_) % 3 else _dk(tcol, .28))
        box(ctx, tx + tw*.3, 560 - th - 14, tw*.4, 14, _dk(tcol, .25), 0, INK, 2)
    spec = [(-30, 165, 150), (135, 120, 186), (255, 170, 158), (425, 128, 200),
            (553, 158, 168), (711, 122, 190), (833, 168, 152), (1001, 140, 184), (1141, 170, 166)]
    signs = [(1, "PHO", '#c0392b'), (3, "CAFE", '#3f7a4a'), (5, "MOBILE", '#2e6fb0'), (7, "NAILS", '#b0487a')]
    sd = {i: (w, c) for i, w, c in signs}
    for i, (hx, hw, ht) in enumerate(spec):
        op = 0.9 if i % 3 else 0.25
        _tube_house(ctx, hx, hw, ht, pal[i % len(pal)], open_=op, balcony=(i % 3 == 1),
                    sign=sd.get(i, (None, None))[0], sc=sd.get(i, (None, '#888'))[1],
                    awning=(C('#e0a82e') if i % 4 == 2 else None))
    _pole(ctx, 150, 560, 108); _pole(ctx, 1130, 560, 96)
    _wire_bundle(ctx, 150, 116, 1130, 104, n=4, sag=40)
    _wire_bundle(ctx, -10, 130, 150, 120, n=3, sag=24); _wire_bundle(ctx, 1130, 112, 1290, 138, n=3, sag=24)
    box(ctx, 0, 560, W, 40, C('#c2bcae')); line(ctx, [(0, 560), (W, 560)], INK, 2.5, .5)
    for k in range(11): line(ctx, [(60 + k*118, 562), (48 + k*118, 598)], C('#a9a296'), 2)
    box(ctx, 0, 600, W, 120, C('#8b8883')); line(ctx, [(0, 600), (W, 600)], INK, 2.5, .5)
    for k in range(-1, 7): box(ctx, ((k*210 + t*60) % (W + 210)) - 105, 652, 60, 5, (0.95, 0.95, 0.92), 2)
    # motorbike stream (deterministic in t)
    bodies = ['#b03a2e', '#2e6fb0', '#e8e8e4', '#3f7a4a', '#c9a23e', '#5a5f6a', '#a04a7a', '#d9732b']
    for i in range(8):
        sp = 120 + (i % 3) * 55
        if i % 2:
            x = W + 140 - ((t * sp + i * 217) % (W + 280)); yy, ss, fl = 648, .62, -1
        else:
            x = ((t * sp + i * 173) % (W + 280)) - 140; yy, ss, fl = 668, .78, 1
        _moto(ctx, x, yy, ss, fl, bodies[i % len(bodies)], ['#3a4a6a', '#5a4636', '#2e4a3a', '#54405a'][i % 4])
    _tree(ctx, 40, 598, .9, '#5c8a44'); _tree(ctx, 1250, 598, .85, '#54823f')

# ============================================================
# 4. bg_market — open-air market
# ============================================================
def _umbrella(ctx, x, y, r, c1, c2):
    """Big striped market parasol. (x,y)=canopy centre top-ish."""
    a1, a2 = C(c1), C(c2)
    n = 12
    for k in range(n):
        a0, a1r = math.pi * k / n, math.pi * (k + 1) / n
        poly(ctx, [(x, y), (x + math.cos(a0)*r, y + math.sin(a0)*r*.55), (x + math.cos(a1r)*r, y + math.sin(a1r)*r*.55)],
             a1 if k % 2 else a2)
    ctx.arc(x, y, r, 0, math.pi); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
    ctx.arc(x, y, r, 0, math.pi); ctx.set_source_rgb(*_dk(a1, .3)); ctx.set_line_width(2.5); ctx.stroke()
    for k in range(1, n):
        a0 = math.pi * k / n
        line(ctx, [(x, y), (x + math.cos(a0)*r, y + math.sin(a0)*r*.55)], _dk(a2, .25), 1.4)
    circle(ctx, x, y - 4, 6, _dk(a1, .35), INK, 2)
    line(ctx, [(x, y), (x, y + 190)], hexc('#7a5a38'), 5)

def _basket(ctx, x, y, w, h, c='#b8853f'):
    """Produce basket (trapezoid, weave lines). (x,y)=bottom centre."""
    cc = C(c)
    poly(ctx, [(x - w/2, y - h), (x + w/2, y - h), (x + w*.38, y), (x - w*.38, y)], cc, INK, 2.5)
    for k in range(1, 4): line(ctx, [(x - w/2 + k*2, y - h*k/4 - 2), (x + w/2 - k*2, y - h*k/4 - 2)], _dk(cc, .25), 2)
    for k in range(4): line(ctx, [(x - w*.32 + k*w*.22, y - h + 2), (x - w*.24 + k*w*.17, y - 2)], _dk(cc, .2), 1.5)
    box(ctx, x - w/2 - 3, y - h - 5, w + 6, 7, _dk(cc, .35), 3, INK, 2)

def _fruit_pile(ctx, x, y, w, c, n=7, r=9):
    cc = C(c)
    rows = (n + 2) // 3
    for ri in range(rows):
        cnt = n - ri*3 if ri == 0 else max(2, n - ri*3)
        for k in range(min(5, max(2, 5 - ri))):
            fx = x - w/2 + (k + .5)*w/5 + ri*4
            fy = y - ri*r*1.4
            circle(ctx, fx, fy, r, cc, INK, 1.6)
            circle(ctx, fx - r*.3, fy - r*.3, r*.3, _lt(cc, .4))

def bg_market(ctx, t=0.0, **kv):
    """Open-air market: striped parasols, stall tables with produce baskets, rice sacks, hanging bananas, ground mats."""
    box(ctx, 0, 0, W, 300, C('#cfe3e6'))
    for hx, hw, hh in ((-40, 320, 120), (300, 380, 150), (720, 300, 120), (1000, 320, 150)):
        ctx.move_to(hx, 300); ctx.curve_to(hx + hw*.3, 300 - hh, hx + hw*.7, 300 - hh, hx + hw, 300); ctx.close_path()
        ctx.set_source_rgb(*C('#8fae8a')); ctx.fill()
    box(ctx, 0, 300, W, 420, C('#c9b28e'))                                 # dusty ground
    box(ctx, 0, 300, W, 26, C('#a8a29a'))                                  # far wall
    for k in range(16): line(ctx, [(40 + k*80, 302), (40 + k*80, 324)], C('#8f8a82'), 2)
    # back stall row with awnings
    for i, sx in enumerate((-40, 210, 460, 710, 960, 1170)):
        box(ctx, sx, 330, 230, 130, C('#8f6b42') if i % 2 else C('#7a5a38'), 0, INK, 2.5)
        ac = (C('#c0392b'), C('#e8e4d2')) if i % 2 else (C('#2e6fb0'), C('#e8e4d2'))
        for k in range(8):
            box(ctx, sx - 8 + k*30, 316, 30, 26, ac[0] if k % 2 == 0 else ac[1], 0, INK, 1.5)
        poly(ctx, [(sx - 8, 342), (sx + 232, 342), (sx + 232, 348), (sx - 8, 348)], _dk(ac[0], .3))
    _umbrella(ctx, 250, 300, 190, '#c0392b', '#efe6d0')
    _umbrella(ctx, 660, 288, 210, '#2e6fb0', '#efe6d0')
    _umbrella(ctx, 1060, 306, 180, '#3f7a4a', '#efe6d0')
    # hanging bananas from a frame (left)
    line(ctx, [(60, 380), (60, 560)], hexc('#6a4a2c'), 5); line(ctx, [(200, 380), (200, 560)], hexc('#6a4a2c'), 5)
    line(ctx, [(52, 380), (208, 380)], hexc('#6a4a2c'), 6)
    for k in range(4):
        bx = 78 + k*34
        line(ctx, [(bx, 382), (bx, 402)], hexc('#4a5a2c'), 3)
        for j in range(5):
            poly(ctx, [(bx, 402), (bx - 12 + j*6, 402 + 26 + abs(2 - j)*-6), (bx - 8 + j*6, 430 + abs(2 - j)*-5), (bx + 2, 406)],
                 C('#e8c832'), INK, 1.6)
    # front stall tables
    for sx in (330, 780):
        box(ctx, sx - 130, 508, 260, 14, C('#a8703f'), 3, INK, 2.5)
        box(ctx, sx - 130, 522, 260, 8, C('#8b5a33'))
        for lx in (-118, 106): box(ctx, sx + lx, 530, 12, 62, C('#6e4524'), 0, INK, 2)
    _basket(ctx, 260, 508, 66, 46); _fruit_pile(ctx, 260, 462, 56, '#e08a2e')
    _basket(ctx, 340, 508, 66, 46, '#9a6a3a'); _fruit_pile(ctx, 340, 462, 56, '#c0392b')
    _basket(ctx, 420, 508, 66, 46); _fruit_pile(ctx, 420, 462, 56, '#7aa64a')
    _basket(ctx, 700, 508, 66, 46); _fruit_pile(ctx, 700, 462, 56, '#e8c832')
    _basket(ctx, 790, 508, 66, 46, '#9a6a3a'); _fruit_pile(ctx, 790, 462, 56, '#8a4a2e')
    _basket(ctx, 870, 508, 66, 46); _fruit_pile(ctx, 870, 462, 56, '#4a8a5a')
    # rice sacks (right)
    for px, py, ss in ((1080, 592, .8), (1160, 592, .8), (1120, 566, .72), (1226, 592, .7)):
        ctx.save(); ctx.translate(px, py); ctx.scale(ss, ss)
        poly(ctx, [(-52, 0), (-60, -66), (-34, -108), (34, -108), (60, -66), (52, 0)], C('#d8c08e'), INK, 2.5)
        poly(ctx, [(22, -108), (34, -108), (60, -66), (52, 0), (26, 0)], C('#bfa472'))
        poly(ctx, [(-22, -108), (-30, -130), (30, -130), (22, -108)], C('#d8c08e'), INK, 2.5)
        line(ctx, [(-24, -110), (24, -110)], C('#7a5a32'), 4)
        text(ctx, "GAO", 0, -56, 24, C('#6a4a28'))
        ctx.restore()
    # ground mat stalls (front, kept low + sides clear of centre)
    for mx, mc in ((150, '#b0483a'), (560, '#3f7a4a')):
        poly(ctx, [(mx - 120, 640), (mx + 120, 640), (mx + 150, 700), (mx - 150, 700)], C(mc), INK, 2.5)
        for k in range(5): _fruit_pile(ctx, mx - 90 + k*45, 656, 34, ['#e08a2e', '#c0392b', '#e8c832', '#7aa64a', '#8a4a2e'][k], n=4, r=7)
    _basket(ctx, 1210, 640, 70, 44); _basket(ctx, 60, 648, 76, 48, '#9a6a3a')
    ellipse(ctx, 640, 668, 130, 20, C('#b09a76'), a=.5)                    # worn ground patch centre

# ============================================================
# 5. bg_meeting_room — boardroom with wall screen
# ============================================================
def bg_meeting_room(ctx, t=0.0, **kv):
    """Boardroom: long table front edge y=600, dark wall screen showing screen= text, city window, potted plant."""
    screen = str(kv.get('screen', 'WHY VIETNAM?')).replace("→", "»")     # Caveat Brush has no arrow glyph
    box(ctx, 0, 0, W, 620, C('#e7e1d2'))                                   # wall
    box(ctx, 0, 0, W, 46, C('#f2efe6')); line(ctx, [(0, 46), (W, 46)], C('#c9c2b2'), 3)
    for lx in (300, 980): box(ctx, lx - 60, 12, 120, 16, (1, 1, 1), 6, C('#c9c2b2'), 2)   # ceiling lights
    box(ctx, 0, 600, W, 120, C('#b3a58a'))                                 # floor behind/below table
    line(ctx, [(0, 600), (W, 600)], C('#8f8470'), 3, .5)
    city_window(ctx, 84, 130, 360, 250, night=bool(kv.get('night', False)))
    # wall screen
    box(ctx, 556, 118, 560, 300, C('#23262e'), 10, INK, 4)
    box(ctx, 572, 132, 528, 272, C('#141a26'), 6)
    box(ctx, 572, 132, 528, 10, C('#1d2636'), 4)
    words = screen.split()
    if len(screen) > 13 and len(words) > 1:
        mid = (len(words) + 1) // 2
        lns = [" ".join(words[:mid]), " ".join(words[mid:])]
    else:
        lns = [screen]
    for i, l in enumerate(lns):
        text(ctx, l, 836, 268 + (i - (len(lns) - 1) / 2) * 74, 60 if len(lns) == 1 else 56, (1, 1, 1))
    box(ctx, 578, 402, 90, 6, C('#3a6fb0'), 2)                             # plain underline accent
    # clock + shelf detail
    circle(ctx, 1180, 170, 26, C('#efece2'), INK, 3); line(ctx, [(1180, 170), (1180, 152)], INK, 3); line(ctx, [(1180, 170), (1194, 174)], INK, 2.5)
    # potted plant (right)
    box(ctx, 1140, 520, 68, 60, C('#a5502e'), 6, INK, 2.5); box(ctx, 1140, 520, 68, 12, C('#8a3f24'), 4, INK, 2)
    for a, ln in ((-1.9, 90), (-1.2, 105), (-0.5, 95), (2.6, 92), (3.6, 100), (4.6, 88)):
        ex, ey = 1174 + math.cos(a)*ln, 520 + math.sin(a)*ln
        line(ctx, [(1174, 520), (ex, ey)], C('#3f7a4a'), 5)
        ellipse(ctx, ex, ey, 17, 8, C('#4f8a3c'), a=1)
        ctx.save(); ctx.translate(ex, ey); ctx.rotate(a); ellipse(ctx, 0, 0, 17, 8, C('#5c9a48')); ctx.restore()
    # long table: front edge at y=600
    box(ctx, 0, 600, W, 26, C('#8a5a33'), 0, INK, 3)
    box(ctx, 0, 600, W, 8, C('#a8703f'))
    box(ctx, 0, 626, W, 94, C('#6e4524'), 0, INK, 3)
    for k in range(9): line(ctx, [(70 + k*140, 634), (70 + k*140, 716)], C('#5a3820'), 3)

# ============================================================
# 6/7. bg_assembly_hall + bg_samsung_hall
# ============================================================
VPX, VPY = 640, 440
def _pp(x, y, s):
    """One-point perspective projection toward vanishing point; s=1 near plane."""
    return (VPX + (x - VPX) * s, VPY + (y - VPY) * s)

def bg_assembly_hall(ctx, t=0.0, **kv):
    """Factory hall in one-point perspective: converging workstation rows, ceiling lights, lane lines, tiny workers."""
    uni = C(kv.get('uniform', '#8fc1e3'))
    pal = kv.get('palette', 'grey')
    if pal == 'samsung':
        wall, wall2, floor, floor2, bench, bench2, ceil = (C('#e9eef3'), C('#d9e2ea'), C('#cfd8e2'), C('#bcc8d4'),
                                                           C('#c2cfd9'), C('#a4b4c2'), C('#dfe7ee'))
    else:
        wall, wall2, floor, floor2, bench, bench2, ceil = (C('#d8dcdd'), C('#c3c8ca'), C('#aeb3b5'), C('#989ea1'),
                                                           C('#8d949a'), C('#6f767c'), C('#c6cbcd'))
    box(ctx, 0, 0, W, H, wall)
    b = _pp(0, 0, .12); e = _pp(0, H, .12); f = _pp(W, 0, .12); g = _pp(W, H, .12)
    poly(ctx, [(0, 0), (W, 0), f, b], ceil)                                # ceiling
    poly(ctx, [(0, H), (W, H), g, e], floor)                               # floor
    poly(ctx, [(0, 0), b, e, (0, H)], wall2)                               # left wall
    poly(ctx, [(W, 0), f, g, (W, H)], wall2)
    box(ctx, b[0], b[1], f[0] - b[0], e[1] - b[1], C('#e6e9ea'), 0, INK, 2)  # back wall
    box(ctx, 612, 402, 56, 72, C('#7a8288'), 0, INK, 2)                    # far door
    box(ctx, 566, 396, 40, 22, C('#c0392b'), 2, INK, 2); text(ctx, "SAFETY FIRST", 586, 407, 11, (1, 1, 1))
    # ceiling light rows converging
    for s in (.18, .3, .48, .74, 1.0):
        for lx in (300, 980):
            p1 = _pp(lx - 90, 60, s); p2 = _pp(lx + 90, 110, s)
            box(ctx, p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1], C('#f4f2d8'), 0, INK, 2 * s + .5)
            line(ctx, [(p1[0], p1[1] + (p2[1] - p1[1]) / 2), (p2[0], p1[1] + (p2[1] - p1[1]) / 2)], C('#d8d4b0'), 1.5)
    # pipes along side walls
    for s0, s1 in ((.12, 1.0),):
        for wy, wc in ((150, C('#8a9298')), (170, C('#a4adb3'))):
            p1 = _pp(0, wy, s1); p2 = _pp(b[0], wy, s0)
            line(ctx, [p1, p2], wc, 5 * s1, .9)
            line(ctx, [(_pp(W, wy, s1)), (_pp(f[0], wy, s0))], wc, 5 * s1, .9)
    # floor lane lines converging to VP
    for fx in (170, 470, 810, 1110):
        line(ctx, [(fx, H), _pp(fx, H, .12)], C('#d9b23a'), 4, .55)
    # workstation rows (far -> near), centre aisle kept clear
    depths = [(.15, .19), (.22, .28), (.34, .42), (.5, .62), (.72, .9)]
    for i, (s_far, s_near) in enumerate(reversed(depths)):
        pass
    for (s_far, s_near) in reversed(depths):
        for side, (x0, x1) in ((-1, (30, 430)), (1, (850, 1250))):
            a1 = _pp(x0, 585, s_near); a2 = _pp(x1, 585, s_near)
            b1 = _pp(x0, 640, s_far); b2 = _pp(x1, 640, s_far)
            poly(ctx, [a1, a2, b2, b1], bench, INK, 2)                     # bench top
            f1 = _pp(x0, 640, s_far); f2 = _pp(x1, 640, s_far)
            g1 = _pp(x0, 690, s_near); g2 = _pp(x1, 690, s_near)
            poly(ctx, [f1, f2, g2, g1], bench2, INK, 2)                    # bench front
            for mx in (0.25, 0.62):                                        # machine boxes on the bench
                p = _pp(lerp(x0, x1, mx), 560, (s_near + s_far) / 2)
                mw = (x1 - x0) * .17 * (s_near + s_far) / 2
                box(ctx, p[0] - mw/2, p[1] - mw*.8, mw, mw*.8, C('#5f6a72'), 2 * s_near + .5, INK, 2 * s_near + .5)
                box(ctx, p[0] - mw/2, p[1] - mw*.8, mw, mw*.22, C('#78838c'))
    # tiny workers far back + along rows
    for (s_far, s_near) in depths[1:]:
        for x0, x1 in ((230, 230), (1050, 1050)):
            p = _pp(x0, 560, s_far * 1.05)
            ss = max(.18, s_far * 1.6)
            _tiny_worker(ctx, p[0], p[1], ss, uni)
    for wx, ss in ((600, .3), (680, .28), (640, .22)):
        p = _pp(wx, 520, ss * .55)
        _tiny_worker(ctx, p[0], p[1] + 4, .2, uni)

def _tiny_worker(ctx, x, y, s=1.0, uni=(0.56, 0.76, 0.89)):
    """Tiny distant factory worker. (x,y)=feet."""
    u = C(uni) if isinstance(uni, str) else uni
    box(ctx, x - 7*s, y - 30*s, 14*s, 20*s, u, 5*s, INK, 1.8)
    circle(ctx, x, y - 36*s, 6.5*s, SKIN, INK, 1.8)
    box(ctx, x - 7*s, y - 41*s, 14*s, 5*s, _dk(u, .3), 2.5*s, INK, 1.5)    # cap
    line(ctx, [(x - 3*s, y - 10*s), (x - 3*s, y)], INK, 3*s)
    line(ctx, [(x + 3*s, y - 10*s), (x + 3*s, y)], INK, 3*s)

def bg_samsung_hall(ctx, t=0.0, **kv):
    """Samsung-flavoured assembly hall: white/blue palette, blue wall band reading SAMSUNG (plain letters, no logo)."""
    kv['palette'] = 'samsung'; kv.setdefault('uniform', '#2f6db5')
    bg_assembly_hall(ctx, t, **kv)
    box(ctx, 470, 300, 340, 64, C('#cfe0f2'), 0, INK, 3)                   # plain blue wall band
    box(ctx, 470, 300, 340, 10, C('#e8f1fa'))
    box(ctx, 470, 354, 340, 10, C('#9dbbdd'))
    text(ctx, "SAMSUNG", 640, 332, 44, C('#1428a0'))

# ============================================================
# 8. bg_white_studio — seamless cyclorama
# ============================================================
def bg_white_studio(ctx, t=0.0, **kv):
    """Seamless white cyclorama: flat wall, soft grey floor-shadow bands, one flat light band at top."""
    box(ctx, 0, 0, W, H, C('#fbfbfc'))
    box(ctx, 0, 0, W, 74, C('#ffffff'))                                    # flat glow band
    box(ctx, 0, 74, W, 16, C('#f6f8fa'))
    box(ctx, 0, 556, W, 164, C('#f0f0f2'))                                 # floor
    box(ctx, 0, 520, W, 36, C('#f5f5f7'))                                  # cove bands (flat, no gradient)
    box(ctx, 0, 540, W, 16, C('#f2f2f4'))
    line(ctx, [(0, 556), (W, 556)], C('#dcdce0'), 2, .5)
    ellipse(ctx, 640, 636, 330, 40, C('#c9ccd2'), a=.20)                   # soft floor shadow
    ellipse(ctx, 640, 638, 220, 26, C('#bfc3ca'), a=.16)
    ellipse(ctx, 640, 640, 120, 14, C('#b6bac2'), a=.12)

# ============================================================
# 9. bg_port_day / bg_port_night
# ============================================================
def _container(ctx, x, y, w, h, c, night=False):
    """One shipping container, (x,y)=top-left. Corrugation + door end."""
    cc = C(c); cn = _dk(cc, .42) if night else cc
    cd = _dk(cn, .28)
    box(ctx, x, y, w, h, cn, 2, INK, 2.5)
    box(ctx, x, y, w, 6, _lt(cn, .22), 1)
    box(ctx, x, y + h - 6, w, 6, cd, 1)
    for k in range(7): line(ctx, [(x + 12 + k*(w - 24)/6, y + 7), (x + 12 + k*(w - 24)/6, y + h - 7)], cd, 2, .8)
    box(ctx, x + w - 26, y + 6, 22, h - 12, cd, 1, INK, 1.5)
    for k in range(2): line(ctx, [(x + w - 20 + k*8, y + 8), (x + w - 20 + k*8, y + h - 8)], _dk(cd, .3), 2)

def _gantry(ctx, x, y, s, night, t, seed=0.0):
    """Quay gantry crane. (x,y)=rail point at quay top, s=scale."""
    yc = C('#3a4258') if night else C('#d9a13a')
    yd = _dk(yc, .3)
    hgt = 250 * s
    top = y - hgt
    for lx, w in ((-120, 14), (120, 14), (-58, 10), (58, 10)):
        box(ctx, x + lx*s - w*s/2, top + 40*s, w*s, hgt - 40*s, yc, 0, INK, 2.5)
        for k in range(int((hgt - 40*s)//(26*s))):
            line(ctx, [(x + lx*s - w*s/2, top + 44*s + k*26*s), (x + lx*s + w*s/2, top + 66*s + k*26*s)], yd, 2)
    box(ctx, x - 138*s, top + 26*s, 276*s, 18*s, yc, 0, INK, 2.5)          # portal beam
    poly(ctx, [(x - 128*s, top + 26*s), (x - 66*s, top - 46*s), (x + 66*s, top - 46*s), (x + 128*s, top + 26*s)], yc, INK, 2.5)
    box(ctx, x - 20*s, top - 66*s, 40*s, 22*s, yc, 3, INK, 2.5)            # apex house
    bx0, bx1 = x - 330*s, x + 150*s                                        # boom over water
    box(ctx, bx0, top - 6*s, bx1 - bx0, 12*s, yc, 0, INK, 2.5)
    box(ctx, bx0, top + 6*s, bx1 - bx0, 5*s, yd)
    line(ctx, [(x - 18*s, top - 64*s), (bx0 + 30*s, top - 8*s)], INK if not night else C('#8a93b5'), 2.5)
    line(ctx, [(x + 18*s, top - 64*s), (bx1 - 30*s, top - 8*s)], INK if not night else C('#8a93b5'), 2.5)
    box(ctx, x + 96*s, top - 26*s, 46*s, 26*s, C('#5a6270') if night else C('#e8e4d8'), 3, INK, 2.5)  # cab
    box(ctx, x + 102*s, top - 22*s, 22*s, 12*s, C('#233246') if night else C('#9fd4e8'), 2)
    tx = x - 120*s + math.sin(t * 0.22 + seed) * 150 * s                   # trolley drift
    box(ctx, tx - 16*s, top - 14*s, 32*s, 10*s, yd, 2, INK, 2)
    dy = top + 60*s + (math.sin(t * 0.35 + seed) * 0.5 + 0.5) * 60 * s
    line(ctx, [(tx - 10*s, top - 4*s), (tx - 10*s, dy)], INK, 2)
    line(ctx, [(tx + 10*s, top - 4*s), (tx + 10*s, dy)], INK, 2)
    box(ctx, tx - 26*s, dy, 52*s, 9*s, C('#c0392b') if not night else _dk(C('#c0392b'), .35), 2, INK, 2)  # spreader
    if night:
        for lx, ly in ((bx0 + 12*s, top - 10*s), (bx1 - 12*s, top - 10*s), (x, top - 70*s), (x - 128*s, top + 30*s), (x + 128*s, top + 30*s)):
            circle(ctx, lx, ly, 3.4*s, C('#ffd86b')); circle(ctx, lx, ly, 7*s, C('#ffd86b'), a=.22)

def _port(ctx, t, night):
    sky = C('#141c38') if night else C('#bcd8e8')
    w1 = C('#1b2c4a') if night else C('#3f7fae')
    w2 = C('#16243d') if night else C('#2d6a97')
    quay = C('#2a2f3c') if night else C('#9a9e98')
    box(ctx, 0, 0, W, 320, sky)
    if night:
        for i in range(26):                                                # faint stars
            circle(ctx, (i*197 + 60) % W, 20 + (i*83) % 220, 1.4, (1, 1, 1), a=.5)
        circle(ctx, 1120, 70, 26, C('#e8e6d4')); circle(ctx, 1110, 62, 22, sky)
    else:
        ellipse(ctx, 300, 90, 130, 24, (1, 1, 1), a=.7); ellipse(ctx, 950, 60, 150, 26, (1, 1, 1), a=.7)
    box(ctx, 0, 320, W, 160, w1)                                           # water
    box(ctx, 0, 400, W, 80, w2)
    box(ctx, 0, 320, W, 4, _lt(w1, .4))
    for r_ in range(5):                                                    # wave strokes
        for k in range(9):
            x0 = (k*160 + r_*67 + t*(14 + r_*4)) % (W + 150) - 75
            yy = 340 + r_*26
            line(ctx, [(x0, yy), (x0 + 26, yy + 2), (x0 + 52, yy)], C('#7fc2e8') if night else C('#e8f6ff'), 2.5, .5)
    # distant harbour lights + reflections (night)
    if night:
        for i in range(9):
            lx = 40 + i*150
            circle(ctx, lx, 318, 2.6, C('#ffd86b'))
            for k in range(3): line(ctx, [(lx - 8 + k*8, 330 + k*14), (lx - 4 + k*8, 344 + k*14)], C('#ffd86b'), 2, .3)
    box(ctx, 0, 470, W, 250, quay)                                         # quay
    line(ctx, [(0, 470), (W, 470)], INK, 3, .6)
    box(ctx, 0, 470, W, 8, _lt(quay, .25))
    for k in range(8): line(ctx, [(90 + k*160, 478), (90 + k*160, 720)], _dk(quay, .18), 3, .5)   # slab joints
    for bx in (60, 640, 1215):                                             # bollards
        box(ctx, bx - 7, 486, 14, 22, C('#3a4048') if not night else C('#1f2430'), 4, INK, 2)
    cols = ['#c0392b', '#2e6fb0', '#e0a82e', '#3f9a5a']
    stacks = [(60, 3, 2), (620, 2, 3), (930, 3, 2)]
    for sx, ncol, nrow in stacks:
        for r_ in range(nrow):
            for c_ in range(ncol):
                _container(ctx, sx + c_*150, 470 + 8 - (r_ + 1)*58, 142, 54, cols[(r_*2 + c_ + sx) % 4], night)
    if night:                                                              # lit windows on a stack + glow
        circle(ctx, 700, 452, 4, C('#ffd86b')); ellipse(ctx, 700, 470, 40, 10, C('#ffd86b'), a=.1)
    _gantry(ctx, 400, 470, 1.0, night, t, 0.0)
    _gantry(ctx, 1010, 470, .85, night, t, 2.2)

def bg_port_day(ctx, t=0.0, **kv):
    """Day port: quay edge, 4-colour container stacks, 2 gantry cranes, water with wave lines."""
    _port(ctx, t, night=False)

def bg_port_night(ctx, t=0.0, **kv):
    """Night port: navy sky, moon, crane lights, water reflections."""
    _port(ctx, t, night=True)

# ============================================================
# 10. bg_warehouse
# ============================================================
def _carton(ctx, x, y, w, h, c='#c9a06a', open_=False):
    """Cardboard carton, (x,y)=bottom-left."""
    cc = C(c)
    box(ctx, x, y - h, w, h, cc, 2, INK, 2)
    box(ctx, x + w*.44, y - h, w*.12, h, _dk(cc, .16))                     # tape seam
    line(ctx, [(x + 2, y - h + 5), (x + w - 2, y - h + 5)], _lt(cc, .3), 2)
    if open_:
        poly(ctx, [(x, y - h), (x + w*.42, y - h - 10), (x + w*.42, y - h)], _dk(cc, .2), INK, 1.6)
        poly(ctx, [(x + w*.58, y - h), (x + w, y - h - 12), (x + w, y - h)], _dk(cc, .2), INK, 1.6)
    else:
        box(ctx, x + w*.14, y - h*.62, w*.24, h*.2, _dk(cc, .3), 1)        # stamped label

def bg_warehouse(ctx, t=0.0, **kv):
    """Warehouse: tall racking full of cartons (loops), yellow forklift, floor lane markings."""
    box(ctx, 0, 0, W, 560, C('#d5d2c8'))                                   # back wall
    box(ctx, 0, 0, W, 60, C('#c2bfb4'))
    for wx in (140, 480, 820, 1160):                                       # high windows
        box(ctx, wx - 44, 20, 88, 34, C('#eef4f6'), 2, INK, 2.5)
        line(ctx, [(wx, 20), (wx, 54)], C('#9aa2a8'), 3); line(ctx, [(wx - 44, 37), (wx + 44, 37)], C('#9aa2a8'), 2)
    box(ctx, 0, 560, W, 160, C('#a8a8a2'))                                 # concrete floor
    line(ctx, [(0, 560), (W, 560)], C('#8a8a84'), 3)
    # racking: 5 bays x 4 levels, cartons looped with deterministic gaps
    rx0, rx1, ry_top, ry_bot = 40, 1240, 110, 560
    cols, rows = 5, 4
    bw = (rx1 - rx0) / cols; bh = (ry_bot - ry_top) / rows
    for r_ in range(rows + 1):                                             # beams
        yy = ry_top + r_ * bh
        box(ctx, rx0 - 8, yy - 6, rx1 - rx0 + 16, 10, C('#2e6fb0'), 0, INK, 2)
        box(ctx, rx0 - 8, yy - 6, rx1 - rx0 + 16, 3, C('#4a8ac4'))
    for c_ in range(cols + 1):                                             # uprights
        xx = rx0 + c_ * bw
        box(ctx, xx - 7, ry_top - 16, 14, ry_bot - ry_top + 16, C('#5a6470'), 0, INK, 2.5)
        box(ctx, xx - 7, ry_top - 16, 4, ry_bot - ry_top + 16, C('#79838e'))
        line(ctx, [(xx - 5, ry_top + 30), (xx + 5, ry_bot - 30)], C('#4a525c'), 2, .5)  # brace
    ccyc = ['#c9a06a', '#b8905a', '#c9a06a', '#a87f4e']
    for r_ in range(rows):                                                 # cartons per cell
        for c_ in range(cols):
            seed = r_ * 7 + c_ * 13
            if seed % 11 == 4: continue                                    # empty slot (gaps)
            bx, by = rx0 + c_ * bw + 12, ry_top + (r_ + 1) * bh - 8
            wmax = bw - 30
            k = 0; xx = bx
            while xx < bx + wmax - 30:
                cw = 46 + ((seed + k * 17) % 3) * 16
                chh = bh - 26 - ((seed + k * 29) % 2) * 8
                _carton(ctx, xx, by, cw, chh, ccyc[(seed + k) % 4], open_=((seed + k) % 7 == 3))
                if (seed + k) % 5 == 2:
                    _carton(ctx, xx + 6, by - chh, cw - 12, 18, ccyc[(seed + k + 1) % 4])
                xx += cw + 8; k += 1
    # floor markings: lane lines + hatch zone
    box(ctx, 0, 606, W, 6, C('#d9b23a'), 2, None); box(ctx, 0, 690, W, 6, C('#d9b23a'), 2, None)
    for k in range(14):
        poly(ctx, [(940 + k*26, 640), (952 + k*26, 640), (940 + k*26, 686), (928 + k*26, 686)], C('#d9b23a'), a=.75)
    # pallet + cartons right
    box(ctx, 1000, 640, 150, 10, C('#8b5a33'), 2, INK, 2)
    for k in range(3): box(ctx, 1006 + k*50, 650, 12, 8, C('#6e4524'))
    _carton(ctx, 1010, 640, 60, 46); _carton(ctx, 1076, 640, 60, 46, '#b8905a'); _carton(ctx, 1040, 594, 60, 44)
    # yellow forklift (left, facing right)
    fx, fy = 250, 668
    box(ctx, fx - 60, fy - 120, 14, 120, C('#5a6470'), 0, INK, 2.5)        # mast
    box(ctx, fx - 40, fy - 120, 10, 120, C('#5a6470'), 0, INK, 2.5)
    box(ctx, fx - 62, fy - 22, 92, 10, C('#3a3f48'), 2, INK, 2)            # forks
    box(ctx, fx - 62, fy - 60, 66, 40, C('#c9a06a'), 2, INK, 2.5)          # load on forks
    yc = C('#e0a82e')
    box(ctx, fx - 26, fy - 86, 118, 62, yc, 8, INK, 3)                     # body
    box(ctx, fx - 26, fy - 40, 118, 16, _dk(yc, .22), 4)
    box(ctx, fx + 26, fy - 132, 58, 48, yc, 6, INK, 3)                     # cab
    box(ctx, fx + 34, fy - 126, 42, 30, C('#9fd4e8'), 3, INK, 2)
    line(ctx, [(fx + 20, fy - 132), (fx + 20, fy - 168)], INK, 4)          # overhead guard
    line(ctx, [(fx + 92, fy - 132), (fx + 92, fy - 168)], INK, 4)
    box(ctx, fx + 14, fy - 172, 88, 8, _dk(yc, .3), 2, INK, 3)
    for wx in (fx - 6, fx + 74):
        circle(ctx, wx, fy - 18, 26 if wx > fx else 20, C('#23262c'), INK, 2.5)
        circle(ctx, wx, fy - 18, 9, C('#9aa0a8'))
    box(ctx, fx + 96, fy - 70, 10, 16, C('#c0392b'), 2, INK, 1.5)          # rear light

# ============================================================
# 11. bg_construction
# ============================================================
def _tcrane(ctx, x, base, h, t, seed=0.0, night=False):
    """Tower crane with jib swinging slightly with t. (x,base)=mast foot."""
    yc = C('#e0a82e'); yd = _dk(yc, .3)
    mw = 16
    box(ctx, x - mw/2, base - h, mw, h, yc, 0, INK, 2.5)
    for k in range(int(h // 26)):
        line(ctx, [(x - mw/2, base - k*26), (x + mw/2, base - (k + 1)*26)], yd, 2)
        line(ctx, [(x + mw/2, base - k*26), (x - mw/2, base - (k + 1)*26)], yd, 2)
    ty = base - h
    ang = math.sin(t * 0.3 + seed) * 0.05
    box(ctx, x - 13, ty - 26, 26, 26, C('#e8ecf0'), 3, INK, 2.5)           # cab
    box(ctx, x - 8, ty - 20, 14, 10, C('#7ec8e8'), 1)
    poly(ctx, [(x - 6, ty - 26), (x, ty - 66), (x + 6, ty - 26)], yc, INK, 2.5)  # apex
    ctx.save(); ctx.translate(x, ty - 8); ctx.rotate(ang)
    box(ctx, -150, -5, 360, 10, yc, 0, INK, 2.5)                           # jib + counter jib
    for k in range(30): line(ctx, [(-148 + k*12, 5), (-142 + k*12, -5)], yd, 1.8)
    box(ctx, -160, -14, 34, 26, C('#6a707a'), 2, INK, 2.5)                 # counterweight
    line(ctx, [(0, -58), (200, 0)], INK, 2); line(ctx, [(0, -58), (-140, 0)], INK, 2)
    hx = 150 + math.sin(t * 0.45 + seed) * 26
    line(ctx, [(hx, 5), (hx, 96)], INK, 2)
    box(ctx, hx - 8, 96, 16, 8, C('#8d95a2'), 1, INK, 1.5)                 # hook block
    box(ctx, hx - 16, 104, 32, 12, C('#9aa3ad'), 1, INK, 1.5)              # load
    ctx.restore()
    if night: circle(ctx, x, ty - 68, 4, C('#ff5a4a')); circle(ctx, x, ty - 68, 8, C('#ff5a4a'), a=.25)

def bg_construction(ctx, t=0.0, **kv):
    """Construction site: corrugated fence with plain sign, rising steel frame, 2 tower cranes (jibs sway with t), dust piles."""
    box(ctx, 0, 0, W, 470, C('#cfe0e8'))
    ellipse(ctx, 260, 80, 140, 26, (1, 1, 1), a=.7); ellipse(ctx, 900, 60, 160, 28, (1, 1, 1), a=.7)
    box(ctx, 0, 470, W, 250, C('#a5845c'))                                 # dirt ground
    box(ctx, 0, 470, W, 26, C('#8f7350'))
    # rising steel frame (right of centre)
    gx0, gy_base, gx1 = 520, 470, 1080
    for fl in range(4):
        yy = gy_base - 90 - fl * 82
        box(ctx, gx0 - 18, yy, gx1 - gx0 + 36, 12, C('#6a7480'), 0, INK, 2.5)  # beam
        box(ctx, gx0 - 18, yy, gx1 - gx0 + 36, 4, C('#8a94a0'))
    for cx in range(5):
        xx = gx0 + cx * (gx1 - gx0) / 4
        box(ctx, xx - 8, gy_base - 90 - 3 * 82 - 12, 16, 90 + 3 * 82 + 12, C('#5f6a77'), 0, INK, 2.5)
        box(ctx, xx - 8, gy_base - 90 - 3 * 82 - 12, 5, 90 + 3 * 82 + 12, C('#8a94a0'))
    box(ctx, gx0 + 130, gy_base - 350, 120, 350, C('#b8b8b2'), 0, INK, 2.5)  # concrete core
    for k in range(6): line(ctx, [(gx0 + 130, gy_base - 60 - k*58), (gx0 + 250, gy_base - 60 - k*58)], C('#9a9a94'), 2)
    for i in range(3):                                                     # floor decks hint
        line(ctx, [(gx0 + 260, gy_base - 170 - i*82), (gx1 - 10, gy_base - 170 - i*82)], C('#4a525c'), 2, .5)
    # corrugated fence across the back of the ground
    fy = 500
    box(ctx, 0, fy, W, 96, C('#9aa0a0'), 0, INK, 2.5)
    for k in range(43): line(ctx, [(14 + k*30, fy + 2), (14 + k*30, fy + 94)], C('#83898a'), 2.5)
    for k in range(9): box(ctx, 60 + k*150, fy - 6, 8, 108, C('#5a6066'), 0, INK, 2)
    box(ctx, 0, fy, W, 10, C('#b8bcbc')); box(ctx, 0, fy + 88, W, 8, C('#7a8082'))
    for k in range(10):                                                    # hazard stripe band
        box(ctx, k*130, fy + 30, 65, 14, C('#e07a1e')); box(ctx, k*130 + 65, fy + 30, 65, 14, C('#efece2'))
    box(ctx, 880, fy - 74, 240, 60, C('#2e6fb0'), 4, INK, 3)
    text(ctx, "SAFETY FIRST", 1000, fy - 44, 30, (1, 1, 1))
    _tcrane(ctx, 330, 500, 430, t, 0.0); _tcrane(ctx, 940, 500, 470, t, 2.4)
    # dust / material piles (left)
    poly(ctx, [(60, 640), (150, 560), (200, 588), (260, 640)], C('#d9b978'), INK, 2.5)
    for k in range(6): line(ctx, [(90 + k*24, 636 - k*4), (110 + k*24, 620 - k*6)], _dk(C('#d9b978'), .2), 2)
    poly(ctx, [(250, 640), (320, 586), (390, 640)], C('#8f8f8f'), INK, 2.5)
    for k in range(5): circle(ctx, 280 + k*24, 626 - (k % 2)*8, 6, C('#7a7a7a'), INK, 1.5)
    for px in range(3):                                                    # stacked pipes
        circle(ctx, 430 + px*26, 620, 13, C('#9aa0a8'), INK, 2); circle(ctx, 430 + px*26, 620, 6, C('#6a7078'))
    circle(ctx, 443, 596, 13, C('#9aa0a8'), INK, 2); circle(ctx, 443, 596, 6, C('#6a7078'))
    for cxp in (560, 1160):                                                # cones
        poly(ctx, [(cxp - 16, 640), (cxp + 16, 640), (cxp + 12, 632), (cxp - 12, 632)], C('#e07a1e'), INK, 2)
        poly(ctx, [(cxp - 10, 634), (cxp, 596), (cxp + 10, 634)], C('#e07a1e'), INK, 2)
        line(ctx, [(cxp - 6, 616), (cxp + 6, 616)], (1, 1, 1), 5)
    box(ctx, 0, 640, W, 80, C('#96794f'))                                  # foreground dirt (plain, below 630)
    for k in range(10): ellipse(ctx, 60 + k*130, 668 + (k % 3)*14, 26, 7, C('#8a6d46'), a=.7)

# ============================================================
# 12. bg_classroom
# ============================================================
def bg_classroom(ctx, t=0.0, **kv):
    """Classroom: green chalkboard with plain chalk text, rows of wooden desks, sunny window, globe on a shelf."""
    box(ctx, 0, 0, W, 580, C('#efe6cf'))                                   # wall
    box(ctx, 0, 0, W, 36, C('#f6f1e2'))
    box(ctx, 0, 580, W, 140, C('#b98a5e'))                                 # wood floor
    for k in range(9): line(ctx, [(0, 596 + k*14), (W, 594 + k*14)], C('#a3774c'), 2, .7)
    for k in range(13): line(ctx, [(40 + k*100, 580), (20 + k*100, 720)], C('#a3774c'), 2, .4)
    # chalkboard
    box(ctx, 120, 120, 560, 280, C('#8b5a33'), 6, INK, 3)
    box(ctx, 136, 134, 528, 252, C('#2e5c46'), 3, INK, 2)
    box(ctx, 136, 134, 528, 8, C('#3a6e54'), 2)
    box(ctx, 130, 386, 540, 12, C('#a8703f'), 3, INK, 2.5)                 # chalk tray
    for cx in (200, 320, 460): circle(ctx, cx, 392, 4, (1, 1, 1), C('#c9c2ae'), 1.5)
    text(ctx, "1 + 1 = 2", 250, 190, 44, (1, 1, 1), anchor="l")
    text(ctx, "A  B  C", 250, 250, 40, C('#f2e8c8'), anchor="l")
    for k in range(4): line(ctx, [(430, 170 + k*26), (430 + 150 - k*22, 170 + k*26)], (1, 1, 1), 3, .75)  # chalk list
    ctx.arc(560, 320, 34, 0.4, 4.6); ctx.set_source_rgba(1, 1, 1, .8); ctx.set_line_width(3); ctx.stroke()  # erased smudge
    circle(ctx, 190, 320, 3, (1, 1, 1), a=.8); circle(ctx, 210, 330, 2, (1, 1, 1), a=.6)
    # window (far right) + curtains
    box(ctx, 1044, 120, 232, 280, C('#8f9aa6'), 4, INK, 3)
    box(ctx, 1056, 132, 208, 256, C('#bfe0ef'))
    poly(ctx, [(1056, 300), (1120, 244), (1180, 300), (1264, 240), (1264, 388), (1056, 388)], C('#7fae6a'))  # hills outside
    circle(ctx, 1216, 176, 22, C('#f6e58a'))
    line(ctx, [(1160, 132), (1160, 388)], C('#8f9aa6'), 8); line(ctx, [(1056, 260), (1264, 260)], C('#8f9aa6'), 8)
    box(ctx, 1036, 396, 248, 14, C('#a8703f'), 3, INK, 2.5)                # sill
    # shelf + globe + books (left of window)
    box(ctx, 700, 470, 220, 12, C('#a8703f'), 3, INK, 2.5)
    for lx in (712, 900): box(ctx, lx, 482, 10, 40, C('#8b5a33'), 0, INK, 2)
    gx, gy, gr = 760, 428, 40
    circle(ctx, gx, gy, gr, C('#5fa8d9'), INK, 2.5)
    ctx.save(); ctx.arc(gx, gy, gr - 1, 0, 6.283); ctx.clip()
    ellipse(ctx, gx - 12, gy - 10, 14, 10, C('#7cbf5a')); ellipse(ctx, gx + 12, gy + 8, 12, 16, C('#7cbf5a'))
    ellipse(ctx, gx - 6, gy + 22, 10, 6, C('#7cbf5a')); ctx.restore()
    ctx.arc(gx, gy, gr + 6, 2.4, 5.2); ctx.set_source_rgb(*C('#b8861e')); ctx.set_line_width(5); ctx.stroke()  # cradle
    box(ctx, gx - 14, gy + gr + 2, 28, 10, C('#8b5a33'), 3, INK, 2)
    for k, bc in enumerate(('#c0392b', '#2e6fb0', '#3f7a4a')):
        box(ctx, 830 + k*22, 428, 16, 42, C(bc), 2, INK, 2)
        line(ctx, [(832 + k*22, 436), (844 + k*22, 436)], (1, 1, 1), 2, .5)
    # clock
    circle(ctx, 400, 70, 24, C('#efece2'), INK, 3); line(ctx, [(400, 70), (400, 54)], INK, 3); line(ctx, [(400, 70), (412, 74)], INK, 2.5)
    # desks: 2 rows x 3, centre-front kept clear
    for ri, (dy, ss) in enumerate(((470, .8), (560, 1.0))):
        for ci, dx in enumerate((180, 430, 1050) if ri == 0 else (120, 380, 1120)):
            w, h = 150*ss, 18*ss
            ctx.save(); ctx.translate(dx, dy); ctx.scale(ss, ss)
            poly(ctx, [(-75, 0), (75, 0), (88, 26), (-62, 26)], C('#c89a62'), INK, 2.5)   # top (3/4)
            poly(ctx, [(-62, 26), (88, 26), (88, 36), (-62, 36)], C('#a87c48'), INK, 2)
            box(ctx, -58, 36, 10, 66, C('#8b5a33'), 0, INK, 2); box(ctx, 76, 36, 10, 66, C('#8b5a33'), 0, INK, 2)
            poly(ctx, [(-40, -46), (28, -46), (36, -18), (-32, -18)], C('#b8853f'), INK, 2)  # chair back
            box(ctx, -30, -18, 8, 44, C('#8b5a33')); box(ctx, 22, -18, 8, 44, C('#8b5a33'))
            if (ri + ci) % 3 == 0:
                paper(ctx, 10, 8, 44, 30, rot=.06, c=(1, 1, 1), lines_=3)
            ctx.restore()

# ============================================================
# 13. bg_lab — R&D lab
# ============================================================
def bg_lab(ctx, t=0.0, **kv):
    """R&D lab: white benches, monitors facing their benches (backs to camera; one angled showing a waveform), microscope silhouette, ceiling cable trays."""
    box(ctx, 0, 0, W, 560, C('#eef1f4'))                                   # wall
    box(ctx, 0, 0, W, 70, C('#dfe4e9'))                                    # ceiling strip
    for ty, tc in ((34, C('#9aa2ac')), (58, C('#8a929c'))):                # cable trays + cables
        box(ctx, 0, ty, W, 14, tc, 0, INK, 2)
        for k in range(43): circle(ctx, 16 + k*30, ty + 7, 2, _dk(tc, .4))
        for k in range(9): line(ctx, [(70 + k*150, ty - 2), (90 + k*150, ty - 12), (120 + k*150, ty - 2)], C('#3a4048'), 2)
    for dx in (260, 900): line(ctx, [(dx, 70), (dx, 200)], C('#6a727c'), 6)  # conduit drops
    box(ctx, 0, 560, W, 160, C('#c8ccd0'))                                 # floor
    for k in range(8): line(ctx, [(k*170, 560), (k*170 - 30, 720)], C('#b4b8bd'), 2, .6)
    _abox(ctx, 0, 606, W, 5, '#d9b23a', .8)
    # back counter/bench along the wall
    box(ctx, 40, 430, 1200, 16, C('#f4f6f8'), 4, INK, 2.5)
    box(ctx, 40, 446, 1200, 116, C('#dfe3e8'), 0, INK, 2.5)
    for k in range(10): line(ctx, [(140 + k*120, 450), (140 + k*120, 558)], C('#c2c8cf'), 2)
    box(ctx, 40, 552, 1200, 10, C('#c2c8cf'))
    # upper shelf with bottles/boxes
    box(ctx, 80, 250, 520, 12, C('#e8ebee'), 3, INK, 2.5)
    for k in range(4):
        bx = 110 + k*120
        box(ctx, bx, 200, 46, 50, C('#dfe3e8'), 3, INK, 2)
        box(ctx, bx + 8, 190, 30, 12, C('#aeb6c0'), 2, INK, 2)
    for k, bc in enumerate(('#7fb2d9', '#d9a066', '#8fc79a', '#d98f8f', '#cbb2e0')):
        box(ctx, 340 + k*46, 208, 26, 42, C(bc), 4, INK, 2)
        box(ctx, 348 + k*46, 198, 10, 12, C('#e8ebee'), 2, INK, 2)
    # monitors seen from behind (screens face their benches); one angled showing a green waveform
    for mx in (700, 830):
        box(ctx, mx, 330, 96, 78, C('#3a3f47'), 6, INK, 3)                 # back of monitor
        box(ctx, mx + 10, 340, 76, 58, C('#2e333a'), 4)
        line(ctx, [(mx + 30, 350), (mx + 30, 390)], C('#454b54'), 3); line(ctx, [(mx + 66, 350), (mx + 66, 390)], C('#454b54'), 3)
        box(ctx, mx + 34, 408, 28, 16, C('#4a5058'), 2, INK, 2)            # stand
        box(ctx, mx + 16, 424, 64, 6, C('#4a5058'), 3, INK, 2)
    ctx.save(); ctx.translate(1010, 380); ctx.rotate(-0.28)
    box(ctx, -60, -56, 120, 92, C('#23262c'), 6, INK, 3)                   # angled monitor: sliver of screen visible
    box(ctx, -52, -48, 104, 76, C('#0c1410'), 3)
    pts = [(-46 + k*10, -10 + math.sin(k*1.3)*22) for k in range(11)]
    line(ctx, pts, C('#4ce07a'), 3)
    for k in range(5): box(ctx, -46 + k*20, 18, 12, 4, C('#2e6a44'), 1)
    box(ctx, -18, 36, 36, 12, C('#4a5058'), 2, INK, 2)
    ctx.restore()
    # microscope silhouette on the bench (right)
    ctx.save(); ctx.translate(1130, 430); ctx.scale(1.0, 1.0)
    mc = C('#2a2e34')
    poly(ctx, [(-34, 0), (34, 0), (26, -14), (-26, -14)], mc, INK, 2)      # base
    box(ctx, 12, -96, 16, 84, mc, 4, INK, 2)                               # arm/back post
    ctx.arc(0, -70, 30, -1.9, 1.2); ctx.set_source_rgb(*mc); ctx.set_line_width(14); ctx.stroke()  # curved arm
    box(ctx, -30, -108, 14, 40, mc, 3, INK, 2)
    ctx.save(); ctx.translate(-24, -110); ctx.rotate(-0.5); box(ctx, -6, -34, 12, 34, mc, 3, INK, 2); ctx.restore()  # eyepiece
    box(ctx, -40, -60, 34, 8, mc, 2, INK, 2)                               # stage
    box(ctx, -34, -52, 8, 18, mc, 2); ctx.restore()
    # bench items: beaker + flasks + laptop back
    box(ctx, 150, 372, 40, 58, C('#dfeef4'), 4, INK, 2.5); box(ctx, 156, 396, 28, 34, C('#9fd4e8'), 2)
    line(ctx, [(150, 384), (190, 384)], INK, 2, .6)
    ctx.save(); ctx.translate(260, 430)
    poly(ctx, [(-8, -60), (8, -60), (8, -34), (26, 0), (-26, 0), (-8, -34)], C('#dfeef4'), INK, 2.5)
    poly(ctx, [(-20, -10), (20, -10), (26, 0), (-26, 0)], C('#8fc79a')); ctx.restore()
    box(ctx, 420, 402, 120, 26, C('#4a5058'), 3, INK, 2.5)                 # equipment box
    for k in range(4): circle(ctx, 440 + k*28, 415, 5, C('#7ec8e8'), INK, 1.5)
    circle(ctx, 556, 412, 4, C('#e07a1e'))

# ============================================================
# 14. bg_cleanroom — yellow-tinted semiconductor fab
# ============================================================
def bg_cleanroom(ctx, t=0.0, **kv):
    """Semiconductor fab: yellow-tinted light, white panels, overhead rails with carriage, wafer racks, a tool with an orange status light."""
    box(ctx, 0, 0, W, 560, C('#f3ecc4'))                                   # yellow-tinted walls
    box(ctx, 0, 0, W, 120, C('#efe6b4'))                                   # ceiling
    for k in range(17): line(ctx, [(k*80, 0), (k*80, 120)], C('#ddd2a0'), 2)  # ceiling grid
    for r_ in range(2):                                                    # light panels
        for k in range(6):
            px = 60 + k*210
            box(ctx, px, 26 + r_*56, 150, 34, C('#fbf5b8'), 3, C('#d8c878'), 2)
            _abox(ctx, px + 8, 32 + r_*56, 134, 8, (1, 1, 1), .8)
    # white wall panels
    box(ctx, 0, 120, W, 440, C('#f7f3df'))
    for k in range(9): line(ctx, [(60 + k*150, 120), (60 + k*150, 560)], C('#ddd6ba'), 3)
    box(ctx, 0, 120, W, 8, C('#cfc8a8')); box(ctx, 0, 548, W, 12, C('#cfc8a8'))
    # glossy yellow floor with flat reflection bands
    box(ctx, 0, 560, W, 160, C('#e8dca4'))
    line(ctx, [(0, 560), (W, 560)], C('#c8bc82'), 3)
    for k in range(6):
        px = 60 + k*210
        _abox(ctx, px + 20, 560, 110, 160, '#f2e8b8', .5)               # reflection columns
    _abox(ctx, 0, 640, W, 6, '#d9cf98', .8)
    # overhead rails + carriage
    for ry in (150, 186):
        box(ctx, 0, ry, W, 12, C('#cfc9ae'), 0, INK, 2.5)
        box(ctx, 0, ry + 4, W, 4, C('#a8a288'))
        for k in range(32): line(ctx, [(20 + k*40, ry), (20 + k*40, ry + 12)], C('#b8b298'), 2)
    for hx in (240, 760): line(ctx, [(hx, 120), (hx, 150)], C('#8f8a72'), 6); line(ctx, [(hx + 80, 120), (hx + 80, 150)], C('#8f8a72'), 6)
    box(ctx, 430, 196, 96, 26, C('#e4e8ec'), 4, INK, 3)                    # carriage
    circle(ctx, 448, 222, 7, C('#8f949c'), INK, 2); circle(ctx, 508, 222, 7, C('#8f949c'), INK, 2)
    line(ctx, [(478, 222), (478, 252)], C('#6a6f78'), 6)
    box(ctx, 462, 252, 32, 16, C('#aeb4bc'), 3, INK, 2.5)
    # central tool (white box) with orange status light
    box(ctx, 540, 300, 300, 260, C('#f2f4f6'), 6, INK, 3)
    box(ctx, 540, 300, 300, 34, C('#dfe4ea'), 6, INK, 2)
    box(ctx, 566, 356, 120, 90, C('#2a3138'), 4, INK, 2.5)                 # dark window
    poly(ctx, [(576, 366), (676, 366), (676, 386), (576, 400)], C('#3a4a58'), a=.9)
    box(ctx, 712, 356, 100, 40, C('#cfd6de'), 3, INK, 2)
    for k in range(3): box(ctx, 722 + k*30, 408, 20, 8, C('#8f949c'), 2, INK, 1.5)
    circle(ctx, 800, 318, 9, C('#e07a1e'), INK, 2)                         # orange status light
    poly(ctx, [(788, 300), (812, 300), (826, 236), (774, 236)], C('#e07a1e'), a=.14)
    box(ctx, 560, 470, 260, 60, C('#dfe4ea'), 4, INK, 2.5)                 # tool base
    line(ctx, [(540, 500), (840, 500)], C('#c2c8d0'), 3)
    # wafer racks left + right: open shelving with cassette slots
    for rx in (60, 900):
        box(ctx, rx, 300, 220, 260, C('#eceff2'), 0, INK, 3)
        box(ctx, rx, 300, 220, 12, C('#cfd6de'))
        for r_ in range(4):
            yy = 330 + r_*58
            box(ctx, rx + 6, yy + 40, 208, 8, C('#c2c8d0'), 0, INK, 1.5)
            for k in range(9):                                             # wafer cassettes
                wx = rx + 14 + k*22
                box(ctx, wx, yy - 4, 14, 44, C('#dfe6ee'), 2, INK, 1.5)
                for s_ in range(4): line(ctx, [(wx + 2, yy + 6 + s_*9), (wx + 12, yy + 6 + s_*9)], C('#9aa6b2'), 1.5)
        for k in range(3): circle(ctx, rx + 40 + k*66, yy + 20, 12, C('#c8d2dc'), INK, 1.5)  # loose wafers
    # pass-through window in back wall
    box(ctx, 250, 330, 180, 120, C('#cfd6de'), 4, INK, 3)
    box(ctx, 262, 342, 156, 96, C('#b8c4cc'), 2)
    poly(ctx, [(262, 400), (360, 342), (418, 342), (262, 438)], C('#cfdce4'), a=.8)
    # bunny-suited worker far right hint (small, generic)
    bx, by = 1150, 560
    box(ctx, bx - 26, by - 130, 52, 96, C('#f4f6f8'), 12, INK, 2.5)
    circle(ctx, bx, by - 148, 24, C('#f4f6f8'), INK, 2.5)
    box(ctx, bx - 14, by - 156, 28, 16, C('#c8d2dc'), 4)                   # goggles band
    box(ctx, bx - 12, by - 138, 24, 12, C('#eef2f6'), 4)
    line(ctx, [(bx - 12, by - 34), (bx - 12, by)], C('#dfe4ea'), 10); line(ctx, [(bx + 12, by - 34), (bx + 12, by)], C('#dfe4ea'), 10)
    line(ctx, [(bx - 12, by - 34), (bx - 12, by)], INK, 2, .4); line(ctx, [(bx + 12, by - 34), (bx + 12, by)], INK, 2, .4)

# ============================================================
# 15. bg_foxconn_campus — huge campus from above at 3/4
# ============================================================
def bg_foxconn_campus(ctx, t=0.0, **kv):
    """Aerial 3/4 campus: identical long blue-grey factory blocks receding, dorm towers, gate with plain sign, shuttle buses, tiny worker crowd streaming with t."""
    box(ctx, 0, 0, W, 96, C('#cfe0e8'))                                    # thin sky
    for hx, hw, hh in ((-60, 420, 60), (380, 500, 74), (920, 460, 58)):    # far hills
        ctx.move_to(hx, 96); ctx.curve_to(hx + hw*.3, 96 - hh, hx + hw*.7, 96 - hh, hx + hw, 96); ctx.close_path()
        ctx.set_source_rgb(*C('#8fae8a')); ctx.fill()
    box(ctx, 0, 96, W, H - 96, C('#9aa48c'))                               # ground (3/4 plane)
    box(ctx, 0, 96, W, 26, C('#8a947e'))
    # long roads converging slightly (grass strips between blocks)
    for i, (gy, gh) in enumerate(((150, 26), (268, 34), (410, 44), (588, 58))):
        box(ctx, 0, gy, W, gh, C('#7f847c'))
        for k in range(16): _abox(ctx, 30 + k*82, gy + gh/2 - 2, 34, 4, '#c8cabc', .7)
    # identical factory blocks, far -> near (top face + front face)
    blocks = [(120, 118, 640, 30, .5), (60, 176, 760, 44, .72), (20, 296, 880, 66, 1.0), (-40, 448, 1010, 92, 1.35)]
    for bx, by, bw, bh, s in blocks:
        tf, ff = C('#a8b6c2'), C('#7d8fa0')
        poly(ctx, [(bx, by), (bx + bw, by), (bx + bw + 40*s, by - 34*s), (bx + 40*s, by - 34*s)], tf, INK, 2)   # roof
        box(ctx, bx, by, bw, bh, ff, 0, INK, 2.5)                          # facade
        for k in range(int(bw // (46*s))):
            line(ctx, [(bx + 20 + k*46*s, by + 6), (bx + 20 + k*46*s, by + bh - 6)], _dk(ff, .22), 2.5*s + 1)  # bay seams
        box(ctx, bx, by, bw, 7, _lt(tf, .25))
        for k in range(int(bw // 130) + 1):                                # roof vents
            box(ctx, bx + 40 + k*130*s + (1 - s)*60, by - 26*s, 26*s, 10*s, C('#8fa0ae'), 1, INK, 1.5)
        for k in range(3):                                                 # loading doors on nearest blocks
            if s < .7: continue
            box(ctx, bx + 80 + k*260*s, by + bh - 22*s, 34*s, 22*s, C('#4a5560'), 0, INK, 1.5)
    # dormitory towers (right, mid distance)
    for tx, tw, th in ((1020, 74, 210), (1112, 66, 240), (1196, 70, 190)):
        box(ctx, tx, 300 - th + 120, tw, th, C('#93a2b0'), 0, INK, 2.5)
        box(ctx, tx + tw*.74, 300 - th + 122, tw*.26 - 2, th - 4, C('#75848f'))
        poly(ctx, [(tx, 300 - th + 120), (tx + tw, 300 - th + 120), (tx + tw + 10, 300 - th + 106), (tx + 10, 300 - th + 106)], C('#aebcc8'), INK, 2)
        for r_ in range(int(th // 26)):
            for c_ in range(int(tw // 15)):
                box(ctx, tx + 6 + c_*15, 300 - th + 132 + r_*26, 9, 15, C('#c8d6e0') if (r_ + c_) % 4 else C('#5f6e7a'), 1)
    # perimeter fence + gate with plain sign (front band)
    box(ctx, 0, 560, W, 6, C('#6a7068'))
    for k in range(32): line(ctx, [(20 + k*40, 530), (20 + k*40, 566)], C('#8a9088'), 3)
    line(ctx, [(0, 532), (W, 532)], C('#8a9088'), 3)
    box(ctx, 470, 500, 340, 66, C('#5a6470'), 0, INK, 3)                   # gate opening posts
    box(ctx, 470, 500, 26, 66, C('#7d8fa0'), 0, INK, 2.5); box(ctx, 784, 500, 26, 66, C('#7d8fa0'), 0, INK, 2.5)
    box(ctx, 500, 470, 280, 34, C('#2e6fb0'), 3, INK, 2.5)                 # plain sign board
    text(ctx, "ELECTRONICS PARK", 640, 487, 22, (1, 1, 1))
    box(ctx, 505, 556, 270, 10, C('#3a4048'), 2)                           # barrier arm
    # shuttle buses on the front road (deterministic drift)
    for i, sp in enumerate((34, -26)):
        bx = ((t * abs(sp) * (1 if sp > 0 else -1) + i * 700 + (0 if sp > 0 else W)) % (W + 300)) - 150
        byy = 622 if sp > 0 else 656
        ctx.save(); ctx.translate(bx, byy); ctx.scale(1 if sp > 0 else -1, 1)
        box(ctx, -46, -34, 92, 30, C('#eef0ee'), 6, INK, 2.5)
        box(ctx, -46, -14, 92, 8, C('#2e6fb0'), 3)
        for k in range(4): box(ctx, -36 + k*22, -30, 16, 12, C('#9fd4e8'), 2, INK, 1.5)
        for wx in (-26, 26): circle(ctx, wx, -4, 7, C('#23262c'), INK, 2)
        ctx.restore()
    # tiny worker crowd in shift colours streaming to the gate (deterministic in t)
    shift = [C('#2f6db5'), C('#e8e8e8'), C('#3f9a5a'), C('#c9a23e')]
    for i in range(26):
        ph = (t * 0.045 + i / 26.0) % 1.0
        dirn = 1 if i % 2 else -1
        u = ph if dirn > 0 else 1 - ph
        if u < 0.5:
            x = lerp(1240, 860, u * 2); y = 606 + (i % 5) * 5
        else:
            x = lerp(860, 420, (u - 0.5) * 2); y = 616 + (i % 5) * 4
        c = shift[i % 4]
        box(ctx, x - 2.6, y - 9, 5.2, 9, c, 2.4, INK, 1.2)
        circle(ctx, x, y - 12, 3, SKIN, INK, 1.2)
    box(ctx, 0, 668, W, 52, C('#7f847c'))                                  # foreground road (plain below 630+)
    for k in range(9): _abox(ctx, 40 + k*150, 690, 60, 6, '#c8cabc', .6)

# ============================================================
# 16. bg_split2 — vertical split with jagged white divider
# ============================================================
def bg_split2(ctx, t=0.0, **kv):
    """Vertical split: left half left= colour, right half right= colour, white jagged divider, flat paper-texture lines."""
    lc = C(kv.get('left', '#e9d8b0')); rc = C(kv.get('right', '#dfe8ef'))
    box(ctx, 0, 0, 644, H, lc)
    box(ctx, 636, 0, W - 636, H, rc)
    for k in range(38):                                                    # paper texture (flat, low alpha)
        y0 = 12 + k*19
        line(ctx, [(14 + (k*97) % 300, y0), (14 + (k*97) % 300 + 120 + (k*53) % 180, y0)], _dk(lc, .4), 1.4, .08)
        y1 = y0 + 9
        line(ctx, [(680 + (k*89) % 280, y1), (680 + (k*89) % 280 + 110 + (k*61) % 170, y1)], _dk(rc, .4), 1.4, .08)
    n = 26
    le, re_ = [], []
    for i in range(n + 1):
        y = i * H / n
        x = 640 + (16 if i % 2 else -13) + 5 * math.sin(i * 2.7)
        le.append((x - 13, y)); re_.append((x + 13, y))
    poly(ctx, le + list(reversed(re_)), (1, 1, 1), INK, 2)

# ============================================================
# 17. bg_sunrise — layered hills, sun rises with t
# ============================================================
def bg_sunrise(ctx, t=0.0, **kv):
    """Layered hills at dawn: flat warm sky bands, a sun that rises with t, still bird silhouettes."""
    for (y0, y1, c) in ((0, 130, '#6a4a6e'), (130, 240, '#a05e64'), (240, 340, '#d97e52'),
                        (340, 430, '#efa25c'), (430, 500, '#f7cd7c')):
        box(ctx, 0, y0, W, y1 - y0, C(c))
    sy = lerp(520, 250, clamp(t / 8.0))                                    # sun rises with t
    sx = 700
    circle(ctx, sx, sy, 88, C('#f7cd7c'), a=.35)
    circle(ctx, sx, sy, 68, C('#ffdf8e'), a=.5)
    circle(ctx, sx, sy, 50, C('#ffe9a8'), INK, 0)
    circle(ctx, sx, sy, 50, C('#ffd45e'))
    for (hy, hh, c, seed) in ((470, 90, '#b06a54', 1), (500, 110, '#7c5a56', 2), (540, 120, '#4f5a44', 3), (600, 130, '#33492e', 4)):
        ctx.move_to(-20, hy + 60)
        for k in range(7):
            px = -20 + k * (W + 40) / 6
            ctx.curve_to(px + 60, hy - hh * (0.5 + 0.5 * math.sin(seed * 2.1 + k * 1.9)),
                         px + (W + 40) / 6 - 60, hy - hh * (0.5 + 0.5 * math.cos(seed * 1.7 + k * 1.3)),
                         px + (W + 40) / 6, hy - hh * 0.25 * math.sin(k + seed))
        ctx.line_to(W + 20, H); ctx.line_to(-20, H); ctx.close_path()
        ctx.set_source_rgb(*C(c)); ctx.fill()
    box(ctx, 0, 640, W, 80, C('#263a22'))                                  # foreground (plain below 630)
    for bx, by, bs in ((360, 210, 1.0), (430, 240, .8), (300, 260, .7), (980, 190, .9)):  # still birds
        line(ctx, [(bx - 12*bs, by), (bx - 4*bs, by - 6*bs), (bx, by), (bx + 4*bs, by - 6*bs), (bx + 12*bs, by)], C('#3a2e38'), 2.5)

# ============================================================
# 18. bg_coop_yard — collective-yard
# ============================================================
def bg_coop_yard(ctx, t=0.0, **kv):
    """Dusty collective yard: work-points chalk board on posts, horn loudspeaker on a pole, stacked tools, hay pile, mud ground."""
    box(ctx, 0, 0, W, 470, C('#c9c2ac'))                                   # hazy sky
    ellipse(ctx, 300, 90, 160, 24, C('#d6d0bc'), a=.8); ellipse(ctx, 900, 60, 180, 26, C('#d6d0bc'), a=.8)
    for hx, hw, hh in ((-40, 360, 90), (340, 420, 70), (820, 380, 96), (1140, 260, 70)):  # far treeline
        ctx.move_to(hx, 470); ctx.curve_to(hx + hw*.3, 470 - hh, hx + hw*.7, 470 - hh, hx + hw, 470); ctx.close_path()
        ctx.set_source_rgb(*C('#7a7a54')); ctx.fill()
    box(ctx, 0, 470, W, 250, C('#8a6a4a'))                                 # mud ground
    box(ctx, 0, 470, W, 16, C('#7a5c3e'))
    for k in range(12): ellipse(ctx, 40 + k*108, 500 + (k % 4)*44, 34, 8, C('#7a5c3e'), a=.5)
    # thatched shed behind (right)
    box(ctx, 880, 330, 340, 140, C('#9a7a52'), 0, INK, 2.5)
    box(ctx, 880, 330, 340, 140, C('#8a6a44'), 0, None)
    poly(ctx, [(860, 330), (1240, 330), (1190, 268), (910, 268)], C('#a8863e'), INK, 3)
    for k in range(9): line(ctx, [(876 + k*42, 330), (906 + k*40, 270)], C('#8a6a2e'), 2)
    box(ctx, 940, 380, 70, 90, C('#5a4630'), 0, INK, 2.5)                  # dark doorway
    # work-points chalk board (left-centre)
    for px in (180, 520): box(ctx, px, 300, 16, 260, C('#6a4a2c'), 0, INK, 2.5)
    box(ctx, 130, 150, 460, 210, C('#3a4a3e'), 4, INK, 3)                  # board
    box(ctx, 142, 160, 436, 190, C('#2e3f34'), 2)
    text(ctx, "DIEM CONG", 360, 186, 36, (1, 1, 1))
    line(ctx, [(160, 210), (560, 210)], (1, 1, 1), 2.5, .8)
    for r_ in range(4):                                                    # names as ticks + points
        yy = 234 + r_*30
        line(ctx, [(170, yy), (170 + 60 + (r_*37) % 70, yy)], (1, 1, 1), 2.5, .75)
        for k in range(3 + (r_ % 3)): line(ctx, [(360 + k*14, yy - 7), (366 + k*14, yy + 7)], (1, 1, 1), 2.5, .8)
        text(ctx, str(8 + r_*3), 540, yy, 22, C('#f2e8c8'))
    circle(ctx, 560, 350, 4, (1, 1, 1), a=.7)                              # chalk nub
    # loudspeaker pole (centre-right)
    line(ctx, [(700, 560), (700, 150)], C('#6a4a2c'), 12); line(ctx, [(700, 560), (700, 150)], C('#7a5a38'), 7)
    box(ctx, 688, 150, 24, 10, C('#4a4a52'), 2, INK, 2)
    for sy, flip in ((190, 1), (238, -1)):
        ctx.save(); ctx.translate(700, sy); ctx.scale(1, flip)
        poly(ctx, [(0, -8), (0, 8), (54, -22), (54, 22)], C('#5a5f66'), INK, 2.5)
        ellipse(ctx, 54, 0, 6, 22, C('#3a3f46'), a=1)
        ctx.restore()
    line(ctx, [(700, 176), (760, 210), (760, 420), (712, 470)], INK, 2.5, .8)  # wire
    # stacked tools (against shed)
    for k in range(4):                                                     # hoes leaning
        hx0 = 900 + k*30
        line(ctx, [(hx0, 470), (hx0 + 46, 300 + k*8)], C('#8a6a2e'), 6)
        poly(ctx, [(hx0 + 40, 302 + k*8), (hx0 + 64, 292 + k*8), (hx0 + 60, 314 + k*8)], C('#5f6a72'), INK, 2)
    poly(ctx, [(1040, 470), (1096, 452), (1104, 462), (1048, 480)], C('#5f6a72'), INK, 2)  # sickle pile
    line(ctx, [(1050, 466), (1090, 440)], C('#8a6a2e'), 5)
    # hay pile (right foreground) + pitchfork
    poly(ctx, [(1060, 640), (1100, 560), (1160, 540), (1230, 566), (1260, 640)], C('#d9b978'), INK, 3)
    for k in range(16):
        a0 = 0.2 + k * 0.19
        line(ctx, [(1080 + k*11, 636 - (k % 5)*14), (1090 + k*11 + math.cos(a0)*18, 620 - (k % 5)*14 - 16)], C('#c4a258'), 2)
    for k in range(6): line(ctx, [(1120 + k*20, 560 + (k % 2)*10), (1128 + k*20, 540 - (k % 3)*6)], C('#e6c97f'), 2)
    line(ctx, [(1010, 640), (1010, 520)], C('#6a4a2c'), 6)
    for k in range(3): line(ctx, [(1002 + k*8, 520), (1002 + k*8, 546)], C('#5f6a72'), 4)
    box(ctx, 1000, 546, 24, 6, C('#5f6a72'), 1)
    # baskets + sack (left foreground, kept below 630 sparse)
    _basket(ctx, 90, 636, 70, 44, '#9a6a3a')
    ctx.save(); ctx.translate(240, 640); ctx.scale(.6, .6)
    poly(ctx, [(-52, 0), (-60, -66), (-34, -108), (34, -108), (60, -66), (52, 0)], C('#c8b082'), INK, 2.5)
    poly(ctx, [(-22, -108), (-30, -130), (30, -130), (22, -108)], C('#c8b082'), INK, 2.5); ctx.restore()

# ============================================================
# 19. bg_globe_space — starfield
# ============================================================
def bg_globe_space(ctx, t=0.0, **kv):
    """Deep-blue starfield: deterministic twinkling dots, two soft constellations, a few larger stars. Nothing else."""
    box(ctx, 0, 0, W, H, C('#0d1533'))
    box(ctx, 0, 420, W, 300, C('#0a1129'))
    rnd = random.Random(5)
    stars = [(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1.0, 2.6), rnd.uniform(0, 6.28), 1 + rnd.random() * 2)
             for _ in range(100)]
    for i, (sx, sy, sr, ph, sp) in enumerate(stars):
        a = 0.25 + 0.75 * (0.5 + 0.5 * math.sin(t * sp + ph))
        circle(ctx, sx, sy, sr, (0.85, 0.9, 1.0), a=a)
    for cx, cy, sr, ph in ((200, 160, 3.6, 0.4), (1050, 120, 4.2, 1.7), (640, 80, 3.4, 3.1),
                           (380, 520, 3.8, 2.2), (900, 480, 3.4, 5.0), (1180, 320, 3.6, 4.1)):
        a = 0.5 + 0.5 * math.sin(t * 1.3 + ph)
        circle(ctx, cx, cy, sr + a, C('#dfe8ff'), a=.9)
        line(ctx, [(cx - sr*3.2, cy), (cx + sr*3.2, cy)], (0.87, 0.91, 1), 1.6, .25 + .35*a)
        line(ctx, [(cx, cy - sr*3.2), (cx, cy + sr*3.2)], (0.87, 0.91, 1), 1.6, .25 + .35*a)
    cst1 = [(120, 300), (180, 260), (250, 285), (310, 240), (370, 270)]
    cst2 = [(940, 200), (1000, 240), (1070, 220), (1120, 170)]
    for cst in (cst1, cst2):
        line(ctx, cst, (0.75, 0.82, 1), 1.4, .16)
        for px, py in cst: circle(ctx, px, py, 2.4, (0.9, 0.94, 1), a=.85)

# ============================================================
# 20. bg_boxing_ring
# ============================================================
def bg_boxing_ring(ctx, t=0.0, **kv):
    """Boxing ring: crowd silhouettes with camera flashes, flat translucent spotlight cones, corner posts, 3 ropes across."""
    box(ctx, 0, 0, W, 470, C('#1a1e28'))                                   # arena dark
    box(ctx, 0, 0, W, 60, C('#141822'))
    poly(ctx, [(240, 0), (400, 0), (760, 470), (60, 470)], (1, 1, 1), a=.05)   # flat spotlight cones
    poly(ctx, [(880, 0), (1040, 0), (1220, 470), (520, 470)], (1, 1, 1), a=.05)
    poly(ctx, [(560, 0), (720, 0), (900, 470), (380, 470)], (1, 1, 1), a=.04)
    # crowd rows (silhouette blobs)
    for r_, (cy, cs, tone) in enumerate(((300, 13, '#232838'), (350, 15, '#1e2230'), (405, 17, '#171b26'))):
        for k in range(int(W / (cs * 2.4)) + 1):
            px = k * cs * 2.4 + (r_ % 2) * cs + math.sin(k * 3.1 + r_) * 3
            py = cy + math.sin(k * 2.3 + r_ * 1.7) * 5
            circle(ctx, px, py, cs * .62, C(tone))
            poly(ctx, [(px - cs, py + cs * 1.9), (px - cs*.8, py + cs*.5), (px + cs*.8, py + cs*.5), (px + cs, py + cs*1.9)], C(tone))
    for i in range(14):                                                    # camera flashes (deterministic blink)
        if (i * 13 + int(t * 2.5)) % 17 < 1:
            fx = 60 + (i * 197) % 1160; fy = 300 + (i * 83) % 110
            circle(ctx, fx, fy, 3.4, (1, 1, 1))
            circle(ctx, fx, fy, 9, (1, 1, 1), a=.25)
    # ring canvas
    poly(ctx, [(0, 720), (W, 720), (1120, 470), (160, 470)], C('#4a7ab0'))
    poly(ctx, [(160, 470), (1120, 470), (1120, 486), (160, 486)], C('#2d5c92'))
    for k in range(5): line(ctx, [(180 + k*220, 486), (120 + k*260, 720)], C('#3f6da3'), 3, .5)  # canvas seams
    ellipse(ctx, 640, 600, 210, 56, C('#5488c0'), a=.5)                    # centre circle
    ctx.arc(640, 600, 210, 0, 6.283); ctx.set_source_rgb(*C('#e8ecf2')); ctx.set_line_width(4); ctx.stroke()
    # corner posts
    posts = [(150, 470, 1.0), (1130, 470, 1.0), (430, 350, .62), (850, 350, .62)]
    for px, py, ps in posts:
        box(ctx, px - 9*ps, py - 170*ps, 18*ps, 170*ps, C('#8a94a2'), 0, INK, 2.5)
        box(ctx, px - 13*ps, py - 168*ps, 26*ps, 60*ps, C('#c0392b'), 6*ps, INK, 2.5)  # pad
        circle(ctx, px, py - 176*ps, 8*ps, C('#e8ecf2'), INK, 2)
    # 3 ropes across the frame (back pair + front sweep)
    rope = [(C('#c0392b'), 330), (C('#e8ecf2'), 386), (C('#2e6fb0'), 442)]
    for rc, ry in rope:
        line(ctx, [(150, ry + 8), (430, ry - 40), (850, ry - 40), (1130, ry + 8)], INK, 11)
        line(ctx, [(150, ry + 8), (430, ry - 40), (850, ry - 40), (1130, ry + 8)], rc, 7)
    for px, py, ps in posts:
        for rc, ry in rope:
            box(ctx, px - 7*ps, ry - 46*ps - 20 + (1 - ps)*0, 14*ps, 12*ps, rc, 2*ps, INK, 1.5)  # turnbuckle wraps

# ============================================================
# 21. bg_newsroom — TV studio
# ============================================================
def _dot_continent(ctx, cx, cy, rx, ry, px, py):
    return ((px - cx) / rx) ** 2 + ((py - cy) / ry) ** 2 <= 1

def bg_newsroom(ctx, t=0.0, **kv):
    """TV studio: anchor desk front edge y=600, blue backdrop with generic dotted world map, ticker band above y=630."""
    box(ctx, 0, 0, W, 620, C('#1d3a6e'))                                   # backdrop
    box(ctx, 0, 0, W, 40, C('#16294f'))
    blobs = [(330, 220, 60, 90), (360, 330, 46, 70), (620, 200, 50, 70), (640, 320, 70, 100),
             (830, 230, 130, 90), (880, 340, 50, 40), (960, 420, 55, 35)]
    for py in range(120, 470, 24):                                         # dotted world map
        for px in range(120, 1160, 24):
            ox = 12 if (py // 24) % 2 else 0
            for cx, cy, rx, ry in blobs:
                if _dot_continent(ctx, cx, cy, rx, ry, px + ox, py):
                    circle(ctx, px + ox, py, 5, C('#3a5f9a')); break
    box(ctx, 120, 100, 1040, 400, None) if False else None
    rrect(ctx, 100, 96, 1080, 408, 10); ctx.set_source_rgb(*C('#16294f')); ctx.fill_preserve()
    ctx.set_source_rgb(*C('#2e5290')); ctx.set_line_width(4); ctx.stroke()  # frame the map area
    # side screens
    for sx in (30, 1105):
        box(ctx, sx, 130, 145, 110, C('#23262e'), 6, INK, 3)
        box(ctx, sx + 8, 138, 129, 94, C('#2a4a80'), 3)
        text(ctx, "WORLD", sx + 72, 172, 26, (1, 1, 1))
        text(ctx, "NEWS", sx + 72, 204, 30, C('#e0b03a'))
    # studio lamps
    for lx in (220, 1060):
        box(ctx, lx - 40, 14, 80, 26, C('#e8e4d2'), 6, INK, 2.5)
        poly(ctx, [(lx - 40, 40), (lx + 40, 40), (lx + 70, 90), (lx - 70, 90)], (1, 1, 1), a=.06)
    # ticker band (dark strip + light blocks) above y=630
    box(ctx, 0, 540, W, 44, C('#101826'), 0, INK, 2)
    box(ctx, 0, 540, W, 5, C('#2e5290'))
    box(ctx, 14, 548, 130, 28, C('#c0392b'), 3, INK, 2)
    text(ctx, "LIVE", 79, 562, 24, (1, 1, 1))
    for k in range(12):                                                    # scrolling light blocks
        bx = ((k * 120 - t * 90) % (W + 240)) - 120
        box(ctx, bx + 170, 552, 84, 20, C('#dfe6ee'), 3)
        box(ctx, bx + 262, 552, 26, 20, C('#7fa8d9'), 3)
    # anchor desk: front edge ~600
    box(ctx, 200, 584, 880, 22, C('#e8ecf2'), 8, INK, 3)                   # desk top
    box(ctx, 220, 606, 840, 114, C('#2a4a80'), 0, INK, 3)                  # desk front
    box(ctx, 220, 606, 840, 10, C('#16294f'))
    for k in range(4): line(ctx, [(390 + k*160, 616), (390 + k*160, 716)], C('#1d3a6e'), 4)
    box(ctx, 0, 620, W, 100, C('#121a2e'))                                 # studio floor
    # papers + mug on desk (above 600 line, small)
    paper(ctx, 320, 578, 70, 44, rot=.05, lines_=3)
    box(ctx, 900, 560, 26, 24, C('#c0392b'), 4, INK, 2)
    ctx.arc(932, 572, 9, -1.4, 1.4); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()

# ============================================================
# 22. bg_state_store — 1986 ration store, mostly empty shelves
# ============================================================
def bg_state_store(ctx, t=0.0, **kv):
    """1986 state store: mostly EMPTY shelves with a few lone tins, ration poster in plain text, wooden counter front edge y=600, tiled floor."""
    box(ctx, 0, 0, W, 560, C('#d9d3bf'))                                   # wall
    box(ctx, 0, 0, W, 40, C('#c9c3ae'))
    box(ctx, 0, 470, W, 250, C('#cfcabb'))                                 # tiled floor
    for r_ in range(6):
        for c_ in range(14):
            if (r_ + c_) % 2: box(ctx, c_*100 - (50 if r_ % 2 else 0), 478 + r_*42, 96, 38, C('#c2bcab'))
    line(ctx, [(0, 470), (W, 470)], C('#a39d8a'), 3)
    # hanging sign
    box(ctx, 470, 52, 340, 54, C('#b23b2e'), 5, INK, 3)
    box(ctx, 470, 96, 340, 10, C('#8f2a1f'), 2)
    text(ctx, "CUA HANG THUC PHAM", 640, 80, 30, (1, 1, 1))
    line(ctx, [(500, 40), (500, 52)], INK, 3); line(ctx, [(780, 40), (780, 52)], INK, 3)
    # shelves: 4 levels x 6 bays — deliberately mostly empty
    sx0, sx1, sy0 = 60, 860, 150
    bw = (sx1 - sx0) / 6; bh = 78
    box(ctx, sx0 - 10, sy0 - 16, sx1 - sx0 + 20, sy0 + 4*78 + 30 - sy0 + 16, C('#c2b89a'), 0, None)  # dusty back panel
    for c_ in range(7): box(ctx, sx0 + c_*bw - 5, sy0 - 10, 10, 4*78 + 26, C('#8b5a33'), 0, INK, 2)
    for r_ in range(4):
        yy = sy0 + r_ * bh
        box(ctx, sx0 - 10, yy + bh - 10, sx1 - sx0 + 20, 12, C('#a8703f'), 0, INK, 2.5)
        box(ctx, sx0 - 10, yy + bh - 10, sx1 - sx0 + 20, 4, C('#c08a52'))
    def tin(x, y, c='#8a94a2'):
        box(ctx, x - 12, y - 30, 24, 30, C(c), 3, INK, 2)
        ellipse(ctx, x, y - 30, 12, 4, _lt(C(c), .3), a=1)
        box(ctx, x - 12, y - 20, 24, 8, C('#e8e4d2'), 0, INK, 1)
    # the few lone items (scarcity): 4 tins, 1 bottle, 1 small stack
    tin(150, sy0 + 78 - 10); tin(560, sy0 + 2*78 - 10, '#a28a6a'); tin(230, sy0 + 3*78 - 10); tin(760, sy0 + 4*78 - 16)
    box(ctx, 420, sy0 + 78 - 44, 16, 34, C('#5a7a4a'), 4, INK, 2); box(ctx, 424, sy0 + 78 - 52, 8, 10, C('#5a7a4a'), 2, INK, 1.5)
    for k in range(2): box(ctx, 640 + k*26, sy0 + 4*78 - 34, 22, 24, C('#d8c08e'), 2, INK, 2)  # two paper packets
    # price list board (plain text)
    box(ctx, 900, 150, 250, 200, C('#3a4a3e'), 4, INK, 3)
    text(ctx, "GIA", 1025, 180, 30, (1, 1, 1))
    for k, (it, pr) in enumerate((("RICE", "13 kg"), ("PORK", "0.5 kg"), ("SUGAR", "0.5 kg"), ("OIL", "0.25 L"))):
        text(ctx, it, 940, 220 + k*32, 22, C('#e8e4d2'), anchor="l")
        text(ctx, pr, 1120, 220 + k*32, 22, C('#f2e8c8'), anchor="r")
    # ration poster on wall (left)
    ctx.save(); ctx.translate(40, 200); ctx.rotate(-0.03)
    box(ctx, -8, -8, 130, 160, C('#d8d2c0'), 0, INK, 2)
    box(ctx, 0, 0, 114, 144, C('#efe5c4'), 2, INK, 2)
    text(ctx, "TIEU CHUAN", 57, 26, 18, C('#5a4632'))
    text(ctx, "RICE", 57, 62, 22, C('#8a2f2f')); text(ctx, "13 kg", 57, 88, 24, C('#4a3a2a'))
    text(ctx, "THANG 10", 57, 122, 16, C('#5a4632'))
    circle(ctx, 57, 6, 3, C('#8a2f2f')); ctx.restore()
    # window with bars (right wall, above counter)
    box(ctx, 940, 380, 220, 90, C('#8f9aa6'), 3, INK, 2.5)
    box(ctx, 950, 388, 200, 74, C('#b8ccd4'))
    poly(ctx, [(950, 430), (1030, 388), (1150, 388), (950, 462)], C('#cfe0e6'), a=.8)
    for k in range(4): line(ctx, [(985 + k*45, 388), (985 + k*45, 462)], C('#5a6068'), 4)
    # wooden counter, front edge y=600
    box(ctx, 120, 588, 1040, 24, C('#a8703f'), 4, INK, 3)
    box(ctx, 120, 612, 1040, 108, C('#8b5a33'), 0, INK, 3)
    for k in range(8): line(ctx, [(200 + k*130, 620), (200 + k*130, 716)], C('#6e4524'), 3)
    # beam balance on the counter (right)
    bx = 1010
    box(ctx, bx - 30, 560, 60, 10, C('#4a4f58'), 2, INK, 2)
    box(ctx, bx - 4, 470, 8, 92, C('#4a4f58'), 0, INK, 2)
    line(ctx, [(bx - 56, 478), (bx + 56, 486)], C('#6a7078'), 5)
    for ex in (-56, 56):
        line(ctx, [(bx + ex, 482 if ex < 0 else 486), (bx + ex, 510)], INK, 1.5)
        ellipse(ctx, bx + ex, 512, 20, 6, C('#9aa0a8'), a=1)
        ctx.arc(bx + ex, 512, 20, 0, 3.1416); ctx.set_source_rgb(*INK); ctx.set_line_width(2); ctx.stroke()
    circle(ctx, bx, 466, 5, C('#4a4f58'), INK, 1.5)

# ================= P2 BACKGROUNDS (section 6; merged from _p2_draft.py) =================


# ---------- shared little builders ----------
def _win_grid(ctx, x, y, w, h, cols, rows, c, lit=None, t=0.0, seed=3):
    gx, gy = w/cols, h/rows
    for r in range(rows):
        for k in range(cols):
            cc = c
            if lit and (r*cols + k + int(t*2)) % 7 == seed % 7: cc = lit
            box(ctx, x + k*gx + 2, y + r*gy + 2, gx - 5, gy - 5, cc)

def _curtains(ctx, c=hexc('#7a2530')):
    for x0 in (0, 1010):
        for k in range(4):
            poly(ctx, [(x0 + k*68, 0), (x0 + k*68 + 46, 0), (x0 + k*68 + 26, 470), (x0 + k*68 + 2, 470)], _dk(c, 0.1 + 0.06*(k % 2)))

# ---------- office_1980s (S06, S33) ----------
def bg_office_1980s(ctx, t=0.0, **kv):
    """grey filing cabinets, rotary phone, desk lamp, beige wall calendar; ground y=620."""
    bg_room(ctx, hexc('#d9d2bd'), hexc('#8f7a5f'), 620)
    for i in range(3):
        x0 = 60 + i*150
        box(ctx, x0, 330, 130, 290, hexc('#8d949a'), 4, INK, 3)
        for r in range(4):
            box(ctx, x0 + 8, 342 + r*70, 114, 62, hexc('#9aa1a7'), 2, INK, 2)
            box(ctx, x0 + 48, 368 + r*70, 34, 8, hexc('#5c6368'), 3)
    box(ctx, 560, 560, 300, 14, hexc('#6b4f35'), 3, INK, 3)                    # sideboard
    box(ctx, 600, 505, 90, 55, hexc('#2f2f33'), 10, INK, 3)                    # rotary phone body
    ctx.arc(645, 505, 34, math.pi, 0); ctx.set_source_rgb(*INK); ctx.set_line_width(7); ctx.stroke()
    circle(ctx, 645, 528, 15, hexc('#4a4a50'), INK, 2.5)
    line(ctx, [(690, 520), (712, 498), (712, 512)], hexc('#1f1f22'), 5)        # handset rest
    box(ctx, 760, 470, 10, 90, hexc('#3c4248'), 2, INK, 2)                     # lamp stem
    poly(ctx, [(742, 470), (792, 470), (778, 438), (756, 438)], hexc('#2e7d4f'), INK, 3)   # lamp shade
    ellipse(ctx, 767, 472, 26, 7, (1, 0.95, 0.6), a=0.5)
    box(ctx, 1020, 180, 170, 210, (1, 1, 1), 4, INK, 3); box(ctx, 1020, 180, 170, 52, hexc('#b23b2e'), 4, INK, 3)
    text(ctx, "1986", 1105, 206, 34); text(ctx, "DEC", 1105, 300, 46, INK)
    for r in range(3):
        for k in range(4): box(ctx, 1032 + k*38, 240 + r*16, 30, 10, hexc('#e4e0d2'))

# ---------- ruins (S11) ----------
def bg_ruins(ctx, t=0.0, **kv):
    """silhouetted broken walls, smoke columns, dim orange sky. No gore."""
    box(ctx, 0, 0, W, 470, hexc('#c96a3a')); box(ctx, 0, 0, W, 200, hexc('#a34f2e'))
    ellipse(ctx, 300, 150, 130, 46, (0.95, 0.72, 0.5), a=0.5); ellipse(ctx, 900, 90, 170, 52, (0.95, 0.72, 0.5), a=0.4)
    box(ctx, 0, 470, W, 250, hexc('#4a3b33'))
    S = hexc('#3a2e2a')
    for x0, w, h in [(60, 170, 260), (300, 120, 180), (470, 210, 320), (740, 130, 150), (920, 200, 290), (1160, 100, 200)]:
        pts = [(x0, 470), (x0, 470 - h), (x0 + w*0.3, 470 - h - 26), (x0 + w*0.55, 470 - h + 18), (x0 + w, 470 - h*0.62), (x0 + w, 470)]
        poly(ctx, pts, S)
        for r in range(3):
            for k in range(2):
                if (r + k + x0) % 3: box(ctx, x0 + 18 + k*(w*0.45), 470 - h + 40 + r*54, 26, 34, hexc('#241d1a'))
    for x0, s in [(360, 1.0), (560, 1.35), (1010, 0.9)]:                      # smoke columns
        for k in range(6):
            ph = (t*0.12 + k*0.16 + x0*0.01) % 1
            circle(ctx, x0 + math.sin(ph*6 + k)*26, 470 - 60 - ph*330, (16 + ph*38)*s, (0.35, 0.32, 0.3), a=0.30*(1 - ph))

# ---------- engine_room (S41) ----------
def bg_engine_room(ctx, t=0.0, **kv):
    """pipes, valves, big boiler, dim light; ground y=640."""
    bg_room(ctx, hexc('#3c444a'), hexc('#2c3236'), 640)
    box(ctx, 760, 210, 420, 430, hexc('#5a646c'), 18, INK, 4)                  # boiler
    box(ctx, 760, 210, 120, 430, hexc('#4a545c'), 18)
    for r in range(3): box(ctx, 778, 250 + r*130, 384, 16, hexc('#39424a'), 6)
    circle(ctx, 970, 300, 56, hexc('#2f373d'), INK, 4); circle(ctx, 970, 300, 34, hexc('#871f1f')); circle(ctx, 958, 288, 9, (1, 1, 1), a=0.3)
    for i in range(3):                                                          # gauges
        circle(ctx, 830 + i*70, 420, 22, hexc('#d9d2bd'), INK, 3); line(ctx, [(830 + i*70, 420), (830 + i*70 + 12, 408)], INK, 3)
    for y0, x1 in [(120, 760), (170, 520)]:                                     # pipes
        line(ctx, [(0, y0), (x1, y0), (x1, y0 + 90)], hexc('#6d7780'), 26)
        line(ctx, [(0, y0), (x1, y0), (x1, y0 + 90)], hexc('#556068'), 16)
        for k in range(5): box(ctx, 60 + k*140, y0 - 8, 16, 42, hexc('#465057'), 3)
    for vx in (300, 620):                                                       # valves
        circle(ctx, vx, 120, 26, hexc('#8a3a2e'), INK, 3); line(ctx, [(vx - 26, 120), (vx + 26, 120)], INK, 5); line(ctx, [(vx, 94), (vx, 146)], INK, 5)
    box(ctx, 60, 470, 130, 170, hexc('#4d575f'), 6, INK, 3)
    for k in range(4): circle(ctx, 76 + k*36, 486, 5, hexc('#2e363c'))

# ---------- renovation (S44) ----------
def bg_renovation(ctx, t=0.0, **kv):
    """scaffolding on an old house, fresh paint buckets, ladders; ground y=640."""
    bg_sky_ground(ctx, hexc('#cfe6ea'), hexc('#a89a86'), 560)
    box(ctx, 320, 200, 640, 440, hexc('#cdb98f'), 0, INK, 4)                    # house
    poly(ctx, [(290, 200), (960, 200), (625, 70)], hexc('#8f5a3c'), INK, 4)     # roof
    for r in range(2):
        for k in range(3): box(ctx, 380 + k*190, 250 + r*170, 110, 120, hexc('#7d8c9a'), 3, INK, 3)
    box(ctx, 600, 470, 130, 170, hexc('#6b4a2c'), 4, INK, 3)
    box(ctx, 320, 200, 210, 440, hexc('#e3d3a8'))                                # freshly painted strip
    line(ctx, [(530, 200), (530, 640)], INK, 2.5, 0.4)
    for x0 in (360, 700, 1020):                                                  # scaffold uprights
        line(ctx, [(x0, 640), (x0, 150)], hexc('#8a6a3a'), 9)
        line(ctx, [(x0, 640), (x0, 150)], INK, 3, 0.35)
    for y0 in (250, 400, 540):
        line(ctx, [(350, y0), (1030, y0)], hexc('#a8854f'), 10)
        line(ctx, [(350, y0), (1030, y0)], INK, 3, 0.3)
    for dx in (430, 620, 810): line(ctx, [(dx, 250), (dx + 90, 400)], hexc('#8a6a3a'), 6)
    box(ctx, 1080, 560, 60, 80, hexc('#3a7d5c'), 6, INK, 3); box(ctx, 1080, 560, 60, 14, hexc('#e3d3a8'))   # paint bucket
    box(ctx, 1150, 574, 46, 66, hexc('#b23b2e'), 5, INK, 3); box(ctx, 1150, 574, 46, 12, hexc('#e8e4da'))
    line(ctx, [(140, 640), (230, 300)], hexc('#a8854f'), 9); line(ctx, [(190, 640), (280, 300)], hexc('#a8854f'), 9)  # leaning ladder
    for k in range(6): line(ctx, [(152 + k*5.6, 560 - k*44), (202 + k*5.6, 560 - k*44)], hexc('#8a6a3a'), 6)

# ---------- harvest_gold / harvest_poor (S56, S38) ----------
def _field(ctx, sky, far, near, ripe, sparse=False):
    bg_sky_ground(ctx, sky, far, 420)
    box(ctx, 0, 420, W, 300, near)
    for i in range(7):
        y0 = 440 + i*38
        line(ctx, [(0, y0), (W, y0 + 8)], _dk(near, 0.12), 3, 0.7)
    if sparse: return
    for k in range(9):                                                          # sheaves
        x0 = 60 + k*145; y0 = 600 + (k % 3)*14
        for d in (-14, 0, 14): line(ctx, [(x0 + d, y0), (x0 + d*1.9, y0 - 64)], ripe, 5)
        poly(ctx, [(x0 - 20, y0), (x0 + 20, y0), (x0, y0 - 74)], ripe, _dk(ripe, 0.35), 2.5)
def bg_harvest_gold(ctx, t=0.0, **kv):
    """golden ripe field with sheaves."""
    _field(ctx, hexc('#e8d9a8'), hexc('#d8b95c'), hexc('#c9a23f'), hexc('#b8862a'))
def bg_harvest_poor(ctx, t=0.0, **kv):
    """sparse brown field, dry cracks."""
    _field(ctx, hexc('#cfc6b4'), hexc('#a08a62'), hexc('#8f7a55'), hexc('#7a6547'), sparse=True)
    for k in range(7):
        x0 = 90 + k*180
        line(ctx, [(x0, 620), (x0 + 34, 604), (x0 + 70, 618)], _dk(hexc('#8f7a55'), 0.3), 3)

# ---------- beijing_1978 (S61) ----------
def bg_beijing_1978(ctx, t=0.0, **kv):
    """wide avenue, bicycles, grey Soviet-style blocks; no gate, no emblems."""
    bg_sky_ground(ctx, hexc('#cfd8d5'), hexc('#8b8f8a'), 430)
    for i in range(4):                                                          # grey blocks
        x0 = 40 + i*320; hgt = 190 + (i % 2)*60
        box(ctx, x0, 430 - hgt, 250, hgt, hexc('#9aa09b'), 0, INK, 3)
        box(ctx, x0, 430 - hgt, 250, 18, hexc('#7d837e'))
        _win_grid(ctx, x0 + 16, 430 - hgt + 34, 218, hgt - 50, 6, max(2, int(hgt/64)), hexc('#6d746f'))
    box(ctx, 0, 430, W, 210, hexc('#6f6f6a'))                                   # wide avenue
    for k in range(12): line(ctx, [(40 + k*110, 540), (90 + k*110, 540)], (0.9, 0.9, 0.85), 8)
    box(ctx, 0, 640, W, 80, hexc('#84847e'))
    rnd = random.Random(11)
    for i in range(7):                                                          # bicycles
        x0 = (i*190 + 60 + math.sin(t*0.6 + i)*20) % 1280; y0 = 500 + (i % 3)*36; s = 0.75 + (i % 3)*0.12
        c = rnd.choice([hexc('#3a4a6a'), hexc('#4a4a50'), hexc('#2e5a44')])
        circle(ctx, x0 - 26*s, y0, 17*s, hexc('#2e3238'), INK, 3); circle(ctx, x0 + 26*s, y0, 17*s, hexc('#2e3238'), INK, 3)
        line(ctx, [(x0 - 26*s, y0), (x0, y0 - 26*s), (x0 + 26*s, y0), (x0, y0 - 8*s), (x0 - 26*s, y0)], c, 3.5)
        circle(ctx, x0 + 4*s, y0 - 44*s, 9*s, SKIN, INK, 2); line(ctx, [(x0 + 2*s, y0 - 36*s), (x0 - 2*s, y0 - 10*s)], c, 6)

# ---------- formal halls: embassy / government_hall / expo_hall / signing_table / trophy_stage ----------
def _hall_base(ctx, wall, floor, banner_c):
    bg_room(ctx, wall, floor, 560)
    for x0 in (120, 420, 720, 1020):                                            # columns
        box(ctx, x0, 60, 64, 500, _lt(wall, 0.5), 0, INK, 3)
        box(ctx, x0 - 10, 44, 84, 26, _dk(wall, 0.1), 3, INK, 2.5)
        box(ctx, x0 - 10, 548, 84, 20, _dk(wall, 0.1), 3, INK, 2.5)
        for k in range(3): line(ctx, [(x0 + 14 + k*16, 80), (x0 + 14 + k*16, 530)], _dk(wall, 0.12), 3)
    box(ctx, 300, 110, 680, 130, banner_c, 6, INK, 3)
def bg_embassy(ctx, t=0.0, **kv):
    """formal reception hall: columns, dark red curtains, plain gold-trim banner."""
    _hall_base(ctx, hexc('#e8e0cc'), hexc('#8a5f3a'), hexc('#7a2530'))
    text(ctx, "EMBASSY  ·  NORMALIZATION", 640, 176, 40)
    box(ctx, 0, 0, 1280, 46, hexc('#5e1c26'))
    ellipse(ctx, 640, 620, 300, 26, hexc('#a8763f'), a=0.5)
def bg_government_hall(ctx, t=0.0, **kv):
    """columns + plain deep-blue wall band, flag-free."""
    _hall_base(ctx, hexc('#dfe3e6'), hexc('#7d8a8f'), hexc('#28415e'))
    text(ctx, "POLICY  ·  STABILITY  ·  OPENNESS", 640, 176, 40)
    for x0 in (250, 950): box(ctx, x0 - 26, 470, 52, 90, hexc('#9aa1a7'), 4, INK, 3); circle(ctx, x0, 452, 26, hexc('#4f8a3c'), INK, 3)
def bg_expo_hall(ctx, t=0.0, **kv):
    """trade expo: booths with flag-free banners along the back."""
    bg_room(ctx, hexc('#e6e2d4'), hexc('#9a8f7a'), 560)
    box(ctx, 0, 0, W, 90, hexc('#cfd6da'))
    for i in range(4):
        x0 = 70 + i*310
        box(ctx, x0, 180, 240, 300, hexc('#dfe6ea'), 4, INK, 3)
        box(ctx, x0, 150, 240, 46, [hexc('#28415e'), hexc('#7a2530'), hexc('#2e5a44'), hexc('#6b4a8a')][i], 4, INK, 2.5)
        text(ctx, ["TEXTILE", "FOOD", "TECH", "TOURISM"][i], x0 + 120, 172, 26)
        _win_grid(ctx, x0 + 22, 230, 196, 220, 3, 3, hexc('#b8c4ca'))
    line(ctx, [(0, 560), (W, 560)], INK, 3, 0.3)
def bg_signing_table(ctx, t=0.0, **kv):
    """long polished table with pens and folders; two chairs behind."""
    bg_room(ctx, hexc('#e8e0cc'), hexc('#8a5f3a'), 600)
    box(ctx, 0, 60, W, 60, hexc('#5e1c26'))
    for x0 in (300, 900):                                                       # chairs (back)
        box(ctx, x0 - 55, 300, 110, 130, hexc('#3a3f46'), 10, INK, 3); box(ctx, x0 - 45, 250, 90, 70, hexc('#4a5058'), 12, INK, 3)
    box(ctx, 120, 470, 1040, 46, hexc('#6b4a2c'), 8, INK, 4)                    # table top
    box(ctx, 150, 516, 980, 130, hexc('#5a3d24'), 6, INK, 3)
    for x0 in (330, 640, 950): box(ctx, x0 - 60, 452, 120, 20, (1, 1, 1), 3, INK, 2); line(ctx, [(x0 + 30, 448), (x0 + 52, 438)], INK, 4)
def bg_trophy_stage(ctx, t=0.0, **kv):
    """awards stage: steps, curtains, spotlight cones (flat), plain banner."""
    bg_room(ctx, hexc('#2c2f3a'), hexc('#6b5a44'), 560)
    _curtains(ctx)
    box(ctx, 250, 90, 780, 90, hexc('#28415e'), 6, INK, 3)
    poly(ctx, [(500, 180), (780, 180), (900, 560), (380, 560)], (1, 0.95, 0.75), a=0.10)   # spotlight cone
    box(ctx, 320, 470, 640, 90, hexc('#8a6a3a'), 4, INK, 4)                     # stage
    box(ctx, 260, 560, 760, 60, hexc('#7a5c32'), 4, INK, 4)
    for k in range(8): box(ctx, 340 + k*78, 480, 10, 70, _dk(hexc('#8a6a3a'), 0.25))

# ---------- night_city (S23, S122) ----------
def bg_night_city(ctx, t=0.0, **kv):
    """night skyline with lit windows; deep blue, reads as a city at night."""
    bg_flat(ctx, hexc('#141a2e'))
    for i in range(26): circle(ctx, (i*197) % 1280, (i*83) % 300, 1.6 + (i % 3)*0.7, (1, 1, 1), a=0.35 + 0.3*math.sin(t*1.5 + i))
    ellipse(ctx, 1090, 110, 52, 52, hexc('#e8e4c8')); ellipse(ctx, 1072, 98, 44, 44, hexc('#141a2e'))
    skyline(ctx, 560, night=True, t=t)
    box(ctx, 0, 560, W, 160, hexc('#22283a'))
    for k in range(9): ellipse(ctx, 90 + k*140, 600 + (k % 3)*20, 46, 7, hexc('#f7d774'), a=0.16)   # street light pools

# ---------- seoul_hq (S85) ----------
def bg_seoul_hq(ctx, t=0.0, **kv):
    """glass HQ tower with the plain word SAMSUNG; day skyline behind."""
    bg_sky_ground(ctx, hexc('#bcd8e6'), hexc('#8fa3ad'), 560)
    for i, (x0, w, h) in enumerate([(40, 130, 300), (200, 100, 220), (1010, 140, 310), (1170, 90, 230)]):
        box(ctx, x0, 560 - h, w, h, hexc('#a9bfc9'), 0, INK, 3); _win_grid(ctx, x0 + 10, 560 - h + 14, w - 20, h - 28, 4, int(h/52), hexc('#7fa0b0'))
    box(ctx, 430, 90, 420, 470, hexc('#cfe2ec'), 6, INK, 4)                     # main glass tower
    for r in range(9): line(ctx, [(440, 118 + r*50), (840, 118 + r*50)], hexc('#8fb4c6'), 5)
    for k in range(7): line(ctx, [(470 + k*57, 100), (470 + k*57, 552)], hexc('#8fb4c6'), 4)
    box(ctx, 430, 90, 60, 470, hexc('#b8d2de'))
    box(ctx, 520, 150, 240, 66, hexc('#1428a0'), 4); text(ctx, "SAMSUNG", 640, 182, 44)
    box(ctx, 0, 560, W, 160, hexc('#77898f')); line(ctx, [(0, 600), (W, 600)], (1, 1, 1), 4, 0.4)

# ---------- drone_view (S127) ----------
def bg_drone_view(ctx, t=0.0, **kv):
    """top-down: patchwork fields, a river, a highway ribbon."""
    bg_flat(ctx, hexc('#8fae6a'))
    rnd = random.Random(5)
    for i in range(26):
        x0, y0 = (i*233) % 1180, (i*157) % 640
        w, h = 90 + (i % 4)*40, 70 + (i % 3)*50
        c = [hexc('#a3c07a'), hexc('#7ea45c'), hexc('#c9cf7f'), hexc('#6f9a58')][i % 4]
        box(ctx, x0, y0, w, h, c, 6)
        if i % 3 == 0:
            for k in range(4): line(ctx, [(x0 + 8, y0 + 14 + k*16), (x0 + w - 8, y0 + 14 + k*16)], _dk(c, 0.12), 2.5)
    poly(ctx, [(0, 210), (420, 260), (820, 200), (1280, 260), (1280, 320), (830, 262), (410, 322), (0, 272)], hexc('#5f86a8'))   # river
    line(ctx, [(-40, 620), (640, 380), (1320, 520)], hexc('#8d8d88'), 46)       # highway
    line(ctx, [(-40, 620), (640, 380), (1320, 520)], hexc('#a8a8a2'), 36)
    for k in range(14):
        x0 = -20 + k*96; y0 = 615 - 235*math.sin(math.pi*clamp((x0 + 20)/1340))**1.2 + 0*x0
    line(ctx, [(640, 380), (640, 380)], hexc('#e8e4c8'), 2)
    for k in range(12): line(ctx, [(60 + k*105, 592 - k*15 if k < 6 else 400 + (k-6)*18), (120 + k*105, 575 - k*15 if k < 6 else 418 + (k-6)*18)], (1, 1, 1), 5)
    for px, py in [(240, 140), (1040, 120), (180, 520)]:                        # village clusters
        for m in range(4): box(ctx, px + (m % 2)*36, py + (m//2)*30, 28, 22, hexc('#c9b18a'), 2, INK, 1.5)

# ---------- north_vn_hills (S114) ----------
def bg_north_vn_hills(ctx, t=0.0, **kv):
    """layered karst hills with mist bands; ground y=620."""
    bg_sky_ground(ctx, hexc('#d7e6e0'), hexc('#7ba06a'), 560)
    for (x0, w, h, c) in [(-60, 420, 330, '#a9c4ae'), (280, 380, 280, '#93b498'), (620, 460, 360, '#a9c4ae'), (980, 420, 300, '#93b498')]:
        ctx.move_to(x0, 560); ctx.curve_to(x0 + w*0.15, 560 - h, x0 + w*0.45, 560 - h*1.1, x0 + w*0.6, 560 - h*0.85)
        ctx.curve_to(x0 + w*0.75, 560 - h*0.6, x0 + w*0.9, 560 - h*0.35, x0 + w, 560); ctx.close_path()
        ctx.set_source_rgb(*hexc(c)); ctx.fill()
    for k in range(3): ellipse(ctx, 640, 470 + k*36, 620, 26, (1, 1, 1), a=0.35 - k*0.08)     # mist
    box(ctx, 0, 620, W, 100, hexc('#6f9258'))
    for k in range(10): line(ctx, [(60 + k*130, 640), (90 + k*130, 622)], hexc('#557a44'), 4)

# ---------- rice_to_factory (S89) ----------
def bg_rice_to_factory(ctx, t=0.0, **kv):
    """left half: ripe rice field; right half: graded factory site with stakes."""
    bg_sky_ground(ctx, hexc('#cfe6ea'), hexc('#c9a23f'), 420)
    box(ctx, 0, 420, 640, 300, hexc('#c9a23f'))
    for i in range(6): line(ctx, [(0, 440 + i*42), (640, 448 + i*42)], _dk(hexc('#c9a23f'), 0.14), 3, 0.8)
    for k in range(5):
        x0 = 60 + k*120; poly(ctx, [(x0 - 16, 616), (x0 + 16, 616), (x0, 552)], hexc('#b8862a'), _dk(hexc('#b8862a'), 0.3), 2)
    box(ctx, 640, 420, 640, 300, hexc('#b3a288'))                               # graded site
    for i in range(5): line(ctx, [(660 + i*130, 430), (660 + i*130, 700)], _dk(hexc('#b3a288'), 0.18), 3, 0.6)
    for k in range(4):                                                          # survey stakes
        x0 = 720 + k*140; line(ctx, [(x0, 560), (x0, 640)], hexc('#7a5230'), 6); poly(ctx, [(x0, 560), (x0 + 34, 574), (x0, 588)], hexc('#e2553c'), INK, 2)
    line(ctx, [(640, 420), (640, 720)], INK, 3, 0.35)

# ---------- samsung_campus (S96) ----------
def bg_samsung_campus(ctx, t=0.0, **kv):
    """campus of long blocks with blue roofs, plain SAMSUNG band on the main hall."""
    bg_sky_ground(ctx, hexc('#cfe0e8'), hexc('#9aa49a'), 470)
    for i in range(3):                                                          # distant blocks
        x0 = 80 + i*420; box(ctx, x0, 300 - i*10, 300, 180 + i*10, hexc('#c8ccd0'), 0, INK, 3)
        poly(ctx, [(x0 - 8, 300 - i*10), (x0 + 308, 300 - i*10), (x0 + 290, 268 - i*10), (x0 + 10, 268 - i*10)], hexc('#2f6db5'), INK, 3)
        _win_grid(ctx, x0 + 14, 320 - i*10, 272, 140, 6, 3, hexc('#8fa3ad'))
    box(ctx, 380, 380, 520, 190, hexc('#dfe4e8'), 0, INK, 4)                    # main hall
    poly(ctx, [(368, 380), (912, 380), (888, 336), (392, 336)], hexc('#2f6db5'), INK, 3)
    box(ctx, 520, 400, 240, 46, hexc('#1428a0'), 4); text(ctx, "SAMSUNG", 640, 424, 34)
    for k in range(8): box(ctx, 408 + k*62, 480, 40, 60, hexc('#9fb8c4'), 2, INK, 2)
    box(ctx, 0, 570, W, 150, hexc('#8a948a')); line(ctx, [(0, 620), (W, 620)], (1, 1, 1), 5, 0.5)
    for k in range(5): circle(ctx, 120 + k*260, 560, 22, hexc('#4f8a3c'), INK, 2.5)

# ---------- factory_gate (S75) ----------
def bg_factory_gate(ctx, t=0.0, **kv):
    """factory entrance: gatehouse, boom barrier posts (trucks/queue drawn by fn), fence, crowd dots."""
    bg_sky_ground(ctx, hexc('#cfe0e8'), hexc('#9aa49a'), 500)
    box(ctx, 0, 500, W, 220, hexc('#8d948d'))
    box(ctx, 60, 300, 260, 240, hexc('#c8ccd0'), 0, INK, 3); poly(ctx, [(48, 300), (332, 300), (310, 258), (70, 258)], hexc('#2f6db5'), INK, 3)
    _win_grid(ctx, 78, 320, 224, 190, 4, 3, hexc('#8fa3ad'))
    box(ctx, 900, 340, 340, 200, hexc('#c8ccd0'), 0, INK, 3); poly(ctx, [(888, 340), (1252, 340), (1230, 300), (910, 300)], hexc('#2f6db5'), INK, 3)
    for x0 in (430, 830): box(ctx, x0, 430, 26, 130, hexc('#5c6368'), 3, INK, 2.5)
    for k in range(14): line(ctx, [(456 + k*27, 470), (456 + k*27, 556)], hexc('#7d837e'), 7)   # fence bars
    line(ctx, [(452, 470), (834, 470)], hexc('#5c6368'), 8)
    rnd = random.Random(3)
    for i in range(16):                                                         # tiny crowd
        x0 = 380 + (i*47) % 500; y0 = 560 + (i % 4)*16
        circle(ctx, x0, y0 - 16, 7, SKIN, INK, 1.5); box(ctx, x0 - 6, y0 - 9, 12, 22, rnd.choice([hexc('#8fc1e3'), hexc('#2f6db5'), hexc('#d9cfb8')]), 3)

# ---------- garment_hall (S99) ----------
def bg_garment_hall(ctx, t=0.0, **kv):
    """sewing hall: long tables with machine silhouettes, thread spools, fabric rolls."""
    bg_room(ctx, hexc('#e6e2d4'), hexc('#9a8f7a'), 560)
    for i in range(3):                                                          # perspective rows
        y0 = 250 + i*110; sc = 0.6 + i*0.2
        box(ctx, 100 - i*40, y0, 1080 + i*80, 26*sc + 8, hexc('#a8703f'), 3, INK, 2.5)
        for k in range(9):
            x0 = 160 - i*36 + k*(120 + i*18)
            poly(ctx, [(x0, y0), (x0, y0 - 40*sc), (x0 + 34*sc, y0 - 40*sc), (x0 + 44*sc, y0 - 14*sc), (x0 + 30*sc, y0)], hexc('#3a4a58'), INK, 2)
    box(ctx, 60, 90, 300, 130, hexc('#bfe3ef'), 4, INK, 3); line(ctx, [(210, 90), (210, 220)], hexc('#6d7480'), 8)
    for i in range(4):                                                          # fabric rolls
        box(ctx, 880 + i*90, 420, 60, 130, [hexc('#c9504f'), hexc('#4f8a3c'), hexc('#28415e'), hexc('#d9a62e')][i], 8, INK, 3)
    for k in range(5): circle(ctx, 120 + k*230, 585, 9, [hexc('#c9504f'), hexc('#d9a62e'), hexc('#4f8a3c'), hexc('#28415e'), hexc('#7a2530')][k], INK, 2)

# ---------- small_workshop (S136) ----------
def bg_small_workshop(ctx, t=0.0, **kv):
    """garage workshop: roller door, workbench with tools, shelves with parts bins."""
    bg_room(ctx, hexc('#d5d2c8'), hexc('#7d7468'), 560)
    box(ctx, 80, 140, 360, 420, hexc('#aab0b4'), 4, INK, 4)                     # roller door
    for r in range(8): line(ctx, [(88, 168 + r*50), (432, 168 + r*50)], _dk(hexc('#aab0b4'), 0.2), 4)
    box(ctx, 560, 420, 640, 30, hexc('#8a5f3a'), 3, INK, 3); box(ctx, 590, 450, 26, 110, hexc('#6b4a2c'), 0, INK, 2.5); box(ctx, 1140, 450, 26, 110, hexc('#6b4a2c'), 0, INK, 2.5)
    for k in range(5): line(ctx, [(640 + k*90, 420), (640 + k*90, 396)], hexc('#3c4248'), 8)   # hanging tools
    for k, w in enumerate((30, 44, 24, 38, 30)): box(ctx, 626 + k*90, 388 - (k % 2)*10, w, 12, hexc('#5c6368'), 4, INK, 2)
    box(ctx, 1000, 120, 240, 260, hexc('#b8b2a4'), 3, INK, 3)                   # shelf
    for r in range(3):
        line(ctx, [(1004, 200 + r*76), (1236, 200 + r*76)], INK, 4)
        for k in range(3): box(ctx, 1014 + k*78, 152 + r*76, 60, 44, [hexc('#28415e'), hexc('#7a2530'), hexc('#2e5a44')][(r + k) % 3], 3, INK, 2)

# ---------- design_studio (S134) ----------
def bg_design_studio(ctx, t=0.0, **kv):
    """bright studio desk with drawing tablets on stands, pinned sketches on the wall."""
    bg_room(ctx, hexc('#efece4'), hexc('#b8a288'), 560)
    box(ctx, 240, 430, 800, 26, hexc('#d8d4c8'), 4, INK, 3); box(ctx, 280, 456, 22, 104, hexc('#9a948a')); box(ctx, 980, 456, 22, 104, hexc('#9a948a'))
    for x0 in (360, 640, 920):                                                  # drawing tablets on stands
        ctx.save(); ctx.translate(x0, 380); ctx.rotate(-0.12)
        box(ctx, -70, -52, 140, 104, hexc('#2f3338'), 8, INK, 3); box(ctx, -58, -42, 116, 76, hexc('#cfe0ea'), 4)
        ctx.restore(); line(ctx, [(x0 - 26, 430), (x0 + 26, 430)], hexc('#5c6368'), 10)
    for k in range(3): line(ctx, [(90 + k*24, 140 + k*18), (150 + k*24, 120 + k*18)], hexc('#6b6b66'), 3)   # pencils
    for i in range(3):                                                          # pinned sketches
        x0 = 120 + i*470; box(ctx, x0, 90, 220, 150, (1, 1, 1), 3, INK, 2.5); circle(ctx, x0 + 110, 98, 6, hexc('#c9504f'), INK, 2)
        line(ctx, [(x0 + 30, 210), (x0 + 70, 150), (x0 + 120, 190), (x0 + 170, 130)], hexc('#8a8f96'), 3)

# ---------- air_cargo (S97) ----------
def bg_air_cargo(ctx, t=0.0, **kv):
    """cargo apron: pale sky, hangar, control tower, tarmac with painted guide lines."""
    bg_sky_ground(ctx, hexc('#cfe0e8'), hexc('#9aa49a'), 470)
    box(ctx, 0, 470, W, 250, hexc('#8d948d'))
    box(ctx, 60, 260, 380, 210, hexc('#c8ccd0'), 0, INK, 4)                     # hangar
    poly(ctx, [(48, 260), (452, 260), (420, 208), (80, 208)], hexc('#5c6368'), INK, 3)
    box(ctx, 150, 330, 200, 140, hexc('#39424a'), 3, INK, 3)                    # hangar mouth
    box(ctx, 1140, 150, 60, 320, hexc('#b8bdc2'), 0, INK, 3); box(ctx, 1116, 120, 108, 46, hexc('#28415e'), 6, INK, 3)
    for k in range(4): line(ctx, [(1124 + k*26, 128), (1124 + k*26, 158)], hexc('#9fd8f0'), 8)
    for i in range(3):                                                          # guide lines
        y0 = 520 + i*60; line(ctx, [(0, y0), (1280, y0 - 8)], hexc('#e8d98a'), 7, 0.8)
        for k in range(8): box(ctx, 40 + k*160, y0 - 26, 60, 9, hexc('#f2e6a0'), 2)
    box(ctx, 560, 300, 240, 170, hexc('#d8dcdf'), 4, INK, 3); text(ctx, "CARGO TERMINAL", 680, 330, 26, INK)
    for k in range(3): box(ctx, 590 + k*70, 360, 50, 90, hexc('#b3a288'), 3, INK, 2.5)

# ---------- border (S74, S130) ----------
def bg_border(ctx, t=0.0, **kv):
    """border checkpoint: road through a gate arch, hills behind, flag-free signs."""
    bg_sky_ground(ctx, hexc('#d7e2da'), hexc('#8a9a7a'), 460)
    for (x0, w, h, c) in [(-40, 380, 250, '#a9c0a8'), (300, 320, 200, '#93b498'), (860, 420, 260, '#a9c0a8')]:
        ctx.move_to(x0, 460); ctx.curve_to(x0 + w*0.2, 460 - h, x0 + w*0.55, 460 - h*1.05, x0 + w*0.7, 460 - h*0.7)
        ctx.curve_to(x0 + w*0.85, 460 - h*0.4, x0 + w*0.95, 460 - h*0.2, x0 + w, 460); ctx.close_path(); ctx.set_source_rgb(*hexc(c)); ctx.fill()
    poly(ctx, [(520, 720), (760, 720), (700, 460), (580, 460)], hexc('#7d838a'))   # road receding
    for k in range(5): box(ctx, 632 - k*2, 480 + k*46, 12 + k*4, 20, hexc('#e8e4c8'), 2)
    box(ctx, 430, 300, 420, 40, hexc('#28415e'), 4, INK, 3)                     # gate arch beam
    text(ctx, "BORDER GATE", 640, 320, 26)
    for x0 in (440, 820): box(ctx, x0, 330, 34, 300, hexc('#5c6368'), 3, INK, 3)
    box(ctx, 120, 430, 200, 130, hexc('#c8ccd0'), 3, INK, 3); box(ctx, 150, 470, 60, 90, hexc('#39424a'), 2)   # booth
    box(ctx, 950, 470, 260, 16, hexc('#b3a288'), 3, INK, 2)                     # queue curb
    box(ctx, 0, 560, W, 160, hexc('#6f7a64'))

# ---------- sea_lanes (S73) ----------
def bg_sea_lanes(ctx, t=0.0, **kv):
    """open sea top-down-ish: deep blue water, dotted shipping lanes, small islands."""
    bg_flat(ctx, hexc('#2e6d9e'))
    box(ctx, 0, 0, W, 150, hexc('#7fb6d9'))
    for i in range(5): ellipse(ctx, 140 + i*260, 96 + (i % 2)*26, 60, 16, hexc('#5f9a6a'), a=0.9); ellipse(ctx, 140 + i*260, 90 + (i % 2)*26, 34, 12, hexc('#4f8a5a'))
    for r, (yy, amp) in enumerate([(220, 26), (360, 34), (500, 40)]):           # dotted lanes
        pts = [(60 + k*100, yy + math.sin(k*0.9 + r)*amp) for k in range(13)]
        for k in range(12):
            x0, y0 = pts[k]; x1, y1 = pts[k+1]
            for m in range(4):
                f = m/4; circle(ctx, lerp(x0, x1, f) + 6, lerp(y0, y1, f), 5, (1, 1, 1), a=0.75)
    for k in range(9): line(ctx, [(70 + k*150, 640), (110 + k*150, 660)], hexc('#245a86'), 5, 0.8)
    box(ctx, 0, 690, W, 30, hexc('#1f4e76'))

# ---------- race_track (S102) ----------
def bg_race_track(ctx, t=0.0, **kv):
    """speedway: banked curve, start line, grandstand, warm sunset sky."""
    bg_sky_ground(ctx, hexc('#f2a65e'), hexc('#5f7a4f'), 400)
    box(ctx, 0, 400, W, 320, hexc('#8d8d88'))
    ctx.save(); ctx.translate(640, 470); ctx.scale(1, 0.42)
    ctx.arc(0, 0, 430, math.pi, 2*math.pi); ctx.set_source_rgb(*hexc('#3c3f44')); ctx.set_line_width(190); ctx.stroke()
    ctx.arc(0, 0, 430, math.pi, 2*math.pi); ctx.set_source_rgb(*hexc('#55585e')); ctx.set_line_width(150); ctx.stroke()
    ctx.arc(0, 0, 430, math.pi, 2*math.pi); ctx.set_source_rgb(1, 1, 1); ctx.set_line_width(8); ctx.set_dash([26, 22]); ctx.stroke()
    ctx.restore()
    box(ctx, 40, 250, 300, 110, hexc('#28415e'), 6, INK, 3)                     # grandstand
    for r in range(3):
        for k in range(10): circle(ctx, 58 + k*29, 268 + r*30, 7, (1, 1, 1), a=0.75)
    box(ctx, 40, 226, 300, 26, hexc('#7a2530'), 4, INK, 2.5)
    for k in range(8):                                                          # checkered start line
        box(ctx, 560 + (k % 4)*34, 560 + (k//4)*34, 34, 34, (1, 1, 1) if (k + k//4) % 2 else INK)

# ---------- casino_table (S83) ----------
def bg_casino_table(ctx, t=0.0, **kv):
    """green felt table seen from above-front, wood rail, chips stacked at the edges."""
    bg_flat(ctx, hexc('#241f1c'))
    box(ctx, 0, 120, W, 600, hexc('#6b4a2c'), 0, INK, 0)                        # rail
    ctx.save(); ctx.translate(640, 430); ctx.scale(1, 0.62)
    ctx.arc(0, 0, 470, 0, 2*math.pi); ctx.set_source_rgb(*hexc('#1f6b4a')); ctx.fill()
    ctx.arc(0, 0, 470, 0, 2*math.pi); ctx.set_source_rgb(*hexc('#2e8a60')); ctx.set_line_width(26); ctx.stroke()
    ctx.restore()
    for k in range(10): line(ctx, [(140 + k*110, 160), (140 + k*110, 200)], hexc('#e8d98a'), 5, 0.5)   # rail lights
    for x0, c in [(150, hexc('#c9504f')), (1130, hexc('#28415e'))]:             # chip stacks
        for k in range(5):
            ellipse(ctx, x0, 600 - k*14, 34, 12, c); ellipse(ctx, x0, 602 - k*14, 34, 12, _dk(c, 0.25))
            ellipse(ctx, x0, 600 - k*14, 20, 7, (1, 1, 1), a=0.5)

# ---------- vault (S133) ----------
def bg_vault(ctx, t=0.0, **kv):
    """steel vault room: riveted plate walls, floor grate, cold light panel."""
    bg_flat(ctx, hexc('#39414a'))
    for r in range(5):
        for k in range(9):
            x0, y0 = 60 + k*140, 60 + r*120
            box(ctx, x0, y0, 116, 96, hexc('#465057'), 4, INK, 2.5)
            for dx, dy in ((12, 12), (104, 12), (12, 84), (104, 84)): circle(ctx, x0 + dx, y0 + dy, 5, hexc('#2e363c'))
    box(ctx, 0, 620, W, 100, hexc('#2c3238'))
    for k in range(16): line(ctx, [(k*84, 620), (k*84, 720)], hexc('#1f252a'), 5)
    box(ctx, 420, 30, 440, 26, hexc('#cfe0ea'), 6)                       # light panel
    ellipse(ctx, 640, 420, 460, 300, (1, 1, 1), a=0.05)

# ---------- vhs_rewind (S27) ----------
def bg_vhs_rewind(ctx, t=0.0, **kv):
    """VHS rewind look: dark frame, horizontal static stripes drifting, corner PLAY marker."""
    bg_flat(ctx, hexc('#101318'))
    for i in range(26):
        y0 = (i*37 + int(t*220) % 37) % 720
        box(ctx, 0, y0, W, 2 + (i % 3), _mix(hexc('#101318'), (1, 1, 1), 0.05 + 0.05*((i*7) % 3)))
    band = (int(t*9) % 24)*30
    box(ctx, 0, band, W, 16, _mix(hexc("#101318"), (0.6, 0.7, 0.9), 0.12))                           # rolling tracking bar
    for k in range(40): circle(ctx, (k*173) % 1280, (k*97 + int(t*300)) % 720, 1.5, (1, 1, 1), a=0.12)
    box(ctx, 30, 630, 200, 60, hexc('#1f252a'), 6, INK, 3)
    poly(ctx, [(56, 646), (56, 674), (84, 660)], (1, 1, 1)); text(ctx, "REW", 120, 660, 30, (1, 1, 1))
    box(ctx, 1030, 630, 220, 60, hexc('#1f252a'), 6, INK, 3); text(ctx, "SP  1986", 1140, 660, 28, hexc('#cfe0ea'))

# ---------- kitchen_wall (S52) ----------
def bg_kitchen_wall(ctx, t=0.0, **kv):
    """kitchen wall closeup: tiles, shelf with jars, hanging pans; ground y=620."""
    bg_room(ctx, hexc('#e8e4d4'), hexc('#a8703f'), 620)
    for r in range(6):
        for k in range(10):
            box(ctx, 10 + k*128 + (r % 2)*20, 20 + r*66, 118, 58, hexc('#dfe3dc'), 3, hexc('#b8bdb2'), 2)
    box(ctx, 120, 300, 500, 18, hexc('#8a5f3a'), 3, INK, 3)                     # shelf
    for k, (c, h) in enumerate([(hexc('#b8862a'), 70), (hexc('#4f8a3c'), 56), (hexc('#c9504f'), 80), (hexc('#28415e'), 62)]):
        box(ctx, 150 + k*110, 300 - h, 70, h, c, 8, INK, 3); box(ctx, 150 + k*110, 300 - h, 70, 12, _lt(c, 0.25), 8)
    for k in range(3):                                                          # hanging pans
        x0 = 760 + k*140; line(ctx, [(x0, 60), (x0, 130)], hexc('#5c6368'), 5)
        circle(ctx, x0, 170, 42, hexc('#8d949a'), INK, 3); circle(ctx, x0, 170, 30, hexc('#6d747c')); line(ctx, [(x0 + 40, 158), (x0 + 74, 146)], INK, 8)
    box(ctx, 700, 240, 480, 14, hexc('#5c6368'), 3)

# ================= PROPS (section 7; merged from _props_draft.py) =================

"""SCRATCH DRAFT — 22 cartoon props for REVISION_v2 section 7 (flat cut-out style).
A lead engineer merges these into episodes/vietnam/v2/assets_v2.py. Private helpers use a _p_ prefix
so they don't collide with existing module names on merge. No logos, no gradients, 2-3 flat tones
per material + INK outlines, details via loops, seeded randomness only."""

# ---------------- private helpers / palette ----------------
def _p_mix(a, b, t): return tuple(lerp(x, y, t) for x, y in zip(a, b))
def _p_dk(c, k=0.25): return _p_mix(c, (0.05, 0.05, 0.08), k)
def _p_lt(c, k=0.30): return _p_mix(c, (1, 1, 1), k)

def _p_ellpath(ctx, x, y, rx, ry):
    ctx.save(); ctx.translate(x, y); ctx.scale(rx, ry); ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()

def _p_ellfill(ctx, x, y, rx, ry, c, line=None, lw=2.5, a=1):
    _p_ellpath(ctx, x, y, rx, ry); ctx.set_source_rgba(*c, a)
    if line: ctx.fill_preserve(); ctx.set_source_rgb(*line); ctx.set_line_width(lw); ctx.stroke()
    else: ctx.fill()

def _p_pathpoly(ctx, pts, closed=True):
    ctx.new_path(); ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    if closed: ctx.close_path()

def _p_clip_rr(ctx, x, y, w, h, r):
    rrect(ctx, x, y, w, h, r); ctx.clip()

PSTEEL, PSTEEL_D, PSTEEL_L = hexc('#8d97a3'), hexc('#5f6a77'), hexc('#b9c2cc')
PGLASS, PGLASS_D = hexc('#9fd4e8'), hexc('#6fb0cc')


# ==================================================================
def city_card(ctx, x, y, s=1.0, city="newyork", label=None, **kv):
    """Anchor: centre. 300x200 framed postcard at s=1. A city LANDMARK SILHOUETTE inside a bordered picture
    panel + plain city-name lettering under it (no logos, no flags). city= newyork|tokyo|seoul|taipei|
    cupertino|paris|singapore. Signature: cream card, flat sky, recognisable silhouette, stamp-dot row,
    double picture frame."""
    NAME = {"newyork": "NEW YORK", "tokyo": "TOKYO", "seoul": "SEOUL", "taipei": "TAIPEI",
            "cupertino": "CUPERTINO", "paris": "PARIS", "singapore": "SINGAPORE"}
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    box(ctx, -146, -96, 296, 196, hexc('#cbbfa0'), 6, INK, 3)          # drop card
    box(ctx, -146, -100, 296, 196, hexc('#f4ecd8'), 6, INK, 3)         # card
    px, py, pw, ph = -132, -86, 264, 126
    box(ctx, px, py, pw, ph, hexc('#dfe8ee'))
    ctx.save(); _p_clip_rr(ctx, px, py, pw, ph, 2)
    _p_city_scene(ctx, city)
    ctx.restore()
    rrect(ctx, px, py, pw, ph, 2); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
    rrect(ctx, px + 5, py + 5, pw - 10, ph - 10, 2); ctx.set_source_rgb(*hexc('#c2a258')); ctx.set_line_width(1.6); ctx.stroke()
    for k in range(11):
        circle(ctx, px + 12 + k * (pw - 24) / 10, py + 2.5, 1.4, hexc('#b7aa82'))
    lib.text(ctx, (label or NAME.get(city, str(city).upper())), 0, 56, 30, hexc('#4a3a2a'))
    ctx.restore()

def _p_city_scene(ctx, city):
    """Drawn clipped to the picture area; ground line at y=36, top at y=-86."""
    G = 36
    if city == "newyork":
        box(ctx, -140, -90, 280, 126, hexc('#f0b075'))          # dusk sky
        box(ctx, -140, G, 280, 50, hexc('#7a6a92')); box(ctx, -140, G, 280, 5, hexc('#5d4f75'))
        sil, sil2 = hexc('#333d59'), hexc('#242c42')
        for i, (bx, bw, bh) in enumerate([(-132, 34, 48), (-96, 26, 66), (-66, 30, 40), (-30, 26, 84),
                                          (30, 30, 58), (56, 24, 92), (86, 30, 50), (112, 28, 70)]):
            box(ctx, bx, G - bh, bw, bh, sil if i % 2 else sil2, 0, INK, 2)
            for r_ in range(int(bh // 16)):
                for c_ in range(max(1, int(bw // 12))):
                    if (r_ * 5 + c_ * 3 + i) % 3 == 0:
                        box(ctx, bx + 5 + c_ * 12, G - bh + 6 + r_ * 16, 5, 7, hexc('#ffd86b'))
        ex = 2  # Empire State: stepped tower + spire
        box(ctx, ex - 24, G - 44, 48, 44, sil, 0, INK, 2.5)
        box(ctx, ex - 16, G - 76, 32, 32, sil, 0, INK, 2.5)
        box(ctx, ex - 10, G - 96, 20, 20, sil, 0, INK, 2.5)
        box(ctx, ex - 5, G - 108, 10, 12, sil, 0, INK, 2)
        line(ctx, [(ex, G - 108), (ex, G - 124)], INK, 3)
        for r_ in range(3):
            for c_ in range(3):
                if (r_ + c_) % 2: box(ctx, ex - 12 + c_ * 9, G - 72 + r_ * 9, 4, 5, hexc('#ffd86b'))
    elif city == "tokyo":
        box(ctx, -140, -90, 280, 126, hexc('#cfe6ea'))
        box(ctx, -140, G, 280, 50, hexc('#9fb4c4')); box(ctx, -140, G, 280, 4, hexc('#7f94a4'))
        for bx, bw, bh in [(-132, 40, 26), (-88, 30, 36), (52, 34, 30), (96, 40, 24)]:
            box(ctx, bx, G - bh, bw, bh, hexc('#6c859e'), 0, INK, 2)
        red, wt = hexc('#d94b3f'), hexc('#f6f1e4')
        tower = [(-34, G), (34, G), (11, -56), (-11, -56)]
        poly(ctx, tower, red, INK, 2.5)
        ctx.save(); _p_pathpoly(ctx, tower); ctx.clip()
        for k in range(5):
            box(ctx, -36, G - 16 - k * 20, 72, 8, wt)
        ctx.restore()
        box(ctx, -22, -22, 44, 9, red, 1, INK, 2)
        box(ctx, -13, -52, 26, 8, red, 1, INK, 2)
        line(ctx, [(0, -56), (0, -80)], INK, 3)
        circle(ctx, 0, -81, 2.2, red, INK, 1.5)
    elif city == "seoul":
        box(ctx, -140, -90, 280, 126, hexc('#dfe8ef'))
        ctx.save(); ctx.arc(0, 210, 230, math.pi, 0); ctx.close_path()
        ctx.set_source_rgb(*hexc('#5e9447')); ctx.fill()
        ctx.restore()
        ctx.save(); ctx.arc(0, 210, 230, math.radians(215), math.radians(325))
        ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke(); ctx.restore()
        box(ctx, -140, G + 6, 280, 44, hexc('#4f7a3f'))
        hy = -16  # tower on the summit
        box(ctx, -16, hy - 14, 32, 16, hexc('#dfe3e8'), 2, INK, 2.5)
        poly(ctx, [(-9, hy - 14), (9, hy - 14), (6, hy - 38), (-6, hy - 38)], hexc('#cfd5dc'), INK, 2.5)
        _p_ellfill(ctx, 0, hy - 44, 13, 9, hexc('#8fa4b8'), INK, 2.5)
        box(ctx, -3, hy - 60, 6, 14, hexc('#cfd5dc'), 2, INK, 2)
        line(ctx, [(0, hy - 60), (0, hy - 70)], INK, 2.5)
        for k in range(2): line(ctx, [(-11, hy - 44 + k * 5), (11, hy - 44 + k * 5)], hexc('#5f6a77'), 1.3, .7)
        for tx, ty, tr in [(-52, 2, 11), (-78, 14, 9), (56, 4, 11), (82, 16, 9), (-24, 22, 8), (26, 22, 8)]:
            circle(ctx, tx, ty, tr, hexc('#3f7a34'), INK, 2)
    elif city == "taipei":
        box(ctx, -140, -90, 280, 126, hexc('#cfe0ea'))
        box(ctx, -140, G, 280, 50, hexc('#9fb4c4')); box(ctx, -140, G, 280, 4, hexc('#7f94a4'))
        for bx, bw, bh in [(-130, 30, 30), (96, 34, 38), (64, 26, 20)]:
            box(ctx, bx, G - bh, bw, bh, hexc('#7f93a6'), 0, INK, 2)
        jade, jd = hexc('#6ba08e'), hexc('#4f8070')
        for i in range(8):  # 8 stacked modules: each flares wider toward its top (101's bamboo segments)
            wb, wt = 38 - i * 4.2, 46 - i * 4.2
            yb, yt = G - i * 11 - 11, G - i * 11
            poly(ctx, [(-wb, yb), (wb, yb), (wt, yt), (-wt, yt)], jade, INK, 2)
            poly(ctx, [(wb * 0.55, yb), (wb, yb), (wt, yt), (wt * 0.55, yt)], jd)
            line(ctx, [(-wt, yt), (wt, yt)], hexc('#eef3f5'), 2.5, .9)
        ytop = G - 8 * 11
        line(ctx, [(0, ytop), (0, ytop - 18)], INK, 3)  # spire
    elif city == "cupertino":
        box(ctx, -140, -90, 280, 126, hexc('#bfe3f0'))
        box(ctx, -140, G - 20, 280, 70, hexc('#7cc06a')); box(ctx, -140, G - 20, 280, 5, hexc('#5e9447'))
        _p_ellfill(ctx, 0, 6, 116, 34, hexc('#cfdde6'), INK, 2.5)
        _p_ellfill(ctx, 0, 8, 78, 20, hexc('#8fc17a'), INK, 2)
        for k in range(16):
            a = math.pi * 2 * k / 16
            line(ctx, [(math.cos(a) * 80, 8 + math.sin(a) * 20.5), (math.cos(a) * 114, 6 + math.sin(a) * 33)], hexc('#7f93a6'), 1.4, .8)
        for k in range(-2, 3): line(ctx, [(k * 44, 28), (k * 44 + 8, 28)], hexc('#efe9d8'), 2.5, .6)
        for tx, ty, tr in [(-126, 16, 12), (-104, 26, 9), (112, 18, 12), (94, 27, 9), (-28, 30, 8), (38, 31, 9)]:
            circle(ctx, tx, ty, tr, hexc('#4f8a3c'), INK, 2)
    elif city == "paris":
        box(ctx, -140, -90, 280, 126, hexc('#dce4ee'))
        box(ctx, -140, G, 280, 50, hexc('#a9bcc9')); box(ctx, -140, G, 280, 4, hexc('#8aa2b9'))
        irn, ird = hexc('#a8794f'), hexc('#7d5837')
        for sg in (-1, 1):
            poly(ctx, [(sg * 42, G), (sg * 29, G), (sg * 8, -24), (sg * 16, -24)], irn, INK, 2)
        poly(ctx, [(-15, -24), (15, -24), (7, -56), (-7, -56)], irn, INK, 2)
        poly(ctx, [(-4, -56), (4, -56), (1.5, -80), (-1.5, -80)], irn, INK, 2)
        box(ctx, -21, -30, 42, 7, ird, 1, INK, 2)
        box(ctx, -12, -58, 24, 5, ird, 1, INK, 2)
        ctx.arc(0, 24, 22, math.pi, 0); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
        for k in range(1, 4):
            f = k / 4
            line(ctx, [(lerp(-38, -12, f), lerp(G, -24, f)), (lerp(38, 12, f), lerp(G, -24, f))], ird, 1.4, .9)
        line(ctx, [(-9, -44), (9, -44)], ird, 1.4)
    elif city == "singapore":
        box(ctx, -140, -90, 280, 126, hexc('#ffd9a0'))
        box(ctx, -140, G, 280, 50, hexc('#a9d6df')); box(ctx, -140, G, 280, 4, hexc('#7fb8c4'))
        tb, td = hexc('#cfdde6'), hexc('#a4b8c8')
        tops = G - 88
        for i in range(3):
            xb, xt = -74 + i * 50, -68 + i * 44
            poly(ctx, [(xb, G), (xb + 28, G), (xt + 24, tops), (xt, tops)], tb, INK, 2.5)
            poly(ctx, [(xb + 20, G), (xb + 28, G), (xt + 24, tops), (xt + 17, tops)], td)
            for k in range(1, 9):
                f = k / 9
                line(ctx, [(lerp(xt, xb, f), tops + f * (G - tops)), (lerp(xt + 24, xb + 28, f), tops + f * (G - tops))], hexc('#8fa4b8'), 1.2, .8)
        boat = [(-98, tops + 4), (-70, tops - 10), (-40, tops - 12), (64, tops - 12), (92, tops - 2), (64, tops + 9), (-40, tops + 9), (-70, tops + 9)]
        ctx.new_path(); smooth(ctx, boat)
        ctx.set_source_rgb(*hexc('#e8eef4')); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
        box(ctx, 10, tops - 16, 26, 8, hexc('#cfdde6'), 2, INK, 2)
        circle(ctx, -62, tops - 2, 4, hexc('#4f8a3c'), INK, 1.5)
    else:  # fallback generic skyline
        box(ctx, -140, -90, 280, 126, hexc('#cfe6ea'))
        box(ctx, -140, G, 280, 50, hexc('#9fb4c4'))
        for i, (bx, bw, bh) in enumerate([(-120, 40, 60), (-70, 34, 90), (-24, 44, 50), (30, 34, 80), (78, 40, 46)]):
            box(ctx, bx, G - bh, bw, bh, hexc('#6c859e'), 2, INK, 2)


# ==================================================================
def rank_podium(ctx, x, y, s=1.0, labels=("", "VIETNAM", ""), ranks=(1, 2, 3), hl=None, **kv):
    """Anchor: bottom-centre (block feet on y). 3 blocks ~420 wide at s=1. Block i sits left-to-right at
    position i; its HEIGHT and colour come from ranks[i] (1st gold tallest, 2nd silver, 3rd bronze).
    Big rank number painted on each face, plain label above. hl = position index -> soft glow ring.
    Empty-string labels are skipped."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    HGT = {1: 170, 2: 125, 3: 95}
    COL = {1: (hexc('#e6b830'), hexc('#c2921f'), hexc('#f2d074')),
           2: (hexc('#b6bec9'), hexc('#8d97a3'), hexc('#d3dae1')),
           3: (hexc('#c07a44'), hexc('#96592f'), hexc('#d59a63'))}
    bw, gap = 132, 8
    labels = list(labels if labels else ["", "", ""]) + ["", "", ""]
    ranks = list(ranks if ranks else [1, 2, 3]) + [0, 0, 0]
    total = bw * 3 + gap * 2
    for i in range(3):
        r = int(clamp(ranks[i], 1, 3)) if ranks[i] else 3
        h = HGT.get(r, 95)
        bx = -(total / 2) + i * (bw + gap)
        base, shd, hi = COL.get(r, COL[3])
        if hl is not None and int(hl) == i:
            cx, cy = bx + bw / 2, -h / 2
            _p_ellfill(ctx, cx, cy, bw * 0.92, h * 0.86, hexc('#ffd76a'), a=0.13)
            rrect(ctx, cx - bw * 0.66, -h - 14, bw * 1.32, h + 26, 26)
            ctx.set_source_rgba(*hexc('#ffd76a'), 0.28); ctx.set_line_width(10); ctx.stroke()
            rrect(ctx, cx - bw * 0.60, -h - 8, bw * 1.20, h + 14, 22)
            ctx.set_source_rgb(*hexc('#ffd76a')); ctx.set_line_width(4); ctx.stroke()
        box(ctx, bx, -h, bw, h, base, 0, INK, 3)
        box(ctx, bx + bw - 24, -h + 3, 21, h - 6, shd)
        box(ctx, bx + 3, -h + 3, 8, h - 8, hi)
        box(ctx, bx, -h, bw, 9, hi, 0, INK, 2.5)
        lib.text(ctx, str(r), bx + bw / 2, -h * 0.38, 62, _p_dk(base, .55))
        lab = str(labels[i]) if labels[i] is not None else ""
        if lab: lib.text(ctx, lab, bx + bw / 2, -h - 16, 30, INK)
    box(ctx, -total / 2 - 6, -6, total + 12, 8, hexc('#9aa0a8'), 3, INK, 2.5)
    ctx.restore()


# ==================================================================
def shop_front(ctx, x, y, s=1.0, closed=0.0, label="PHO", **kv):
    """Anchor: bottom-centre. 300x300 tube-house shopfront at s=1: living quarters above (grilled windows,
    AC box, eave + antenna), ground-floor opening with warm interior, red sign band with plain `label`,
    roll-down corrugated shutter driven by `closed` 0..1 (0 open, 1 shut) in a roll housing, potted
    plant, step."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    closed = clamp(closed)
    plaster, pl_d = hexc('#e8e0cc'), hexc('#cfc4aa')
    box(ctx, -150, -300, 300, 300, plaster, 0, INK, 3)
    box(ctx, 120, -298, 30, 296, pl_d)
    box(ctx, -158, -312, 316, 16, hexc('#8b5a33'), 3, INK, 3)
    box(ctx, -158, -302, 316, 4, hexc('#6b3f1d'))
    line(ctx, [(60, -312), (60, -344)], INK, 3); line(ctx, [(50, -338), (70, -326)], INK, 2.5)
    for wx in (-92, 12):  # upper windows with grille bars
        box(ctx, wx - 4, -292, 66, 76, hexc('#d8cdb4'), 2, INK, 2.5)
        box(ctx, wx, -288, 58, 68, hexc('#3a5a70'))
        for k in range(1, 4): line(ctx, [(wx + k * 14.5, -288), (wx + k * 14.5, -220)], hexc('#e9e4d8'), 2, .8)
        line(ctx, [(wx, -254), (wx + 58, -254)], hexc('#e9e4d8'), 2, .8)
        poly(ctx, [(wx + 2, -288), (wx + 20, -288), (wx + 2, -266)], (1, 1, 1), a=0.16)
    box(ctx, 118, -282, 22, 30, hexc('#cfd5dc'), 3, INK, 2)
    for k in range(3): line(ctx, [(120, -276 + k * 7), (138, -276 + k * 7)], PSTEEL_D, 1.5)
    ox, oy, ow, oh = -115, -140, 230, 140
    box(ctx, ox, oy, ow, oh, hexc('#2e2620'), 0, INK, 3)
    box(ctx, ox + 4, oy + 4, ow - 8, 34, hexc('#5a4632'))
    box(ctx, ox + 30, oy + oh - 34, 96, 34, hexc('#8b5a33'), 3, INK, 2)
    circle(ctx, 8, oy + 22, 7, hexc('#ffe27a'))
    line(ctx, [(8, oy + 4), (8, oy + 15)], hexc('#c9a24a'), 2)
    _p_ellfill(ctx, 62, oy + oh - 40, 10, 4, hexc('#efe5c4'), INK, 1.5)
    box(ctx, -96, oy + oh - 52, 20, 44, hexc('#c0392b'), 2, INK, 2)
    line(ctx, [(-92, oy + oh - 38), (-80, oy + oh - 38)], (1, 1, 1), 2)
    line(ctx, [(-92, oy + oh - 30), (-80, oy + oh - 30)], (1, 1, 1), 2)
    box(ctx, -125, -216, 250, 36, hexc('#b23b2e'), 4, INK, 3)
    box(ctx, -125, -186, 250, 5, hexc('#8f2a1f'))
    lib.text(ctx, str(label), 0, -196, 30, (1, 1, 1))
    box(ctx, ox - 5, oy - 12, ow + 10, 12, PSTEEL_D, 2, INK, 2.5)  # shutter housing
    hc = oh * closed
    if hc > 1:
        ctx.save(); _p_clip_rr(ctx, ox + 1, oy + 1, ow - 2, oh - 2, 0)
        n = int(hc / 9.5) + 1
        for k in range(n):
            yy = oy + k * 9.5
            if yy > oy + hc - 9.5: break
            box(ctx, ox + 2, yy, ow - 4, 9, PSTEEL if k % 2 else hexc('#aeb5bf'), 0, INK, 1.5)
            for c_ in range(9): circle(ctx, ox + 12 + c_ * 26, yy + 4.5, 1.2, PSTEEL_D)
        box(ctx, ox + 2, oy + hc - 9, ow - 4, 9, PSTEEL_L, 0, INK, 2)  # bottom rail
        box(ctx, -10, oy + hc - 3, 20, 6, hexc('#5f6a77'), 2, INK, 1.5)
        ctx.restore()
    box(ctx, 84, -26, 30, 26, hexc('#b5623a'), 3, INK, 2)
    for dx, dy, r in [(92, -34, 8), (103, -38, 9), (113, -33, 7)]: circle(ctx, dx, dy, r, hexc('#4f8a3c'), INK, 2)
    box(ctx, ox, -4, ow, 5, hexc('#cfc4aa'), 0, INK, 2)
    ctx.restore()



# ==================================================================
def factory_modern(ctx, x, y, s=1.0, label="", **kv):
    """Anchor: bottom-centre. 520x260 modern flat-roof plant at s=1: light wall with a high glass band
    (looped panels + mullions), dark parapet, tilted solar array on the roof, two loading bays with
    roll doors + canopies + bollards + bay numbers, HVAC boxes, personnel door, plain `label` band.
    Replaces the old generic factory."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    wall, wall_d = hexc('#dfe3e8'), hexc('#c2c8d2')
    box(ctx, -260, -230, 520, 230, wall, 0, INK, 3)
    box(ctx, 224, -228, 36, 226, wall_d)
    box(ctx, -268, -244, 536, 16, hexc('#8d97a3'), 2, INK, 3)
    box(ctx, -268, -236, 536, 5, PSTEEL_D)
    for i in range(4):  # roof solar array
        sx = -196 + i * 92
        poly(ctx, [(sx, -244), (sx + 64, -244), (sx + 76, -276), (sx + 12, -276)], hexc('#1f3a5f'), INK, 2.5)
        for k in range(1, 4): line(ctx, [(sx + k * 16 + 2, -246), (sx + 12 + k * 16, -274)], hexc('#4d6f9a'), 1.6)
        line(ctx, [(sx + 32, -244), (sx + 44, -276)], hexc('#4d6f9a'), 1.6)
        box(ctx, sx + 30, -246, 5, 8, PSTEEL_D)
    for hx in (60, 120):  # HVAC
        box(ctx, hx, -258, 40, 14, PSTEEL, 2, INK, 2.5); line(ctx, [(hx + 4, -251), (hx + 36, -251)], PSTEEL_D, 1.5)
    gx, gy, gw, gh = -240, -188, 480, 62  # glass band
    box(ctx, gx, gy, gw, gh, hexc('#3a4450'), 0, INK, 3)
    ctx.save(); _p_clip_rr(ctx, gx + 3, gy + 3, gw - 6, gh - 6, 0)
    box(ctx, gx, gy, gw, gh, PGLASS)
    for k in range(11):
        xx = gx + 4 + k * 44
        box(ctx, xx + 40, gy + 2, 4, gh - 4, PGLASS_D)
        if k % 4 == 1: box(ctx, xx, gy + 2, 40, gh - 4, hexc('#bfe4f4'))
        line(ctx, [(xx, gy), (xx + 30, gy + gh)], (1, 1, 1), 2, .35)
    ctx.restore()
    rrect(ctx, gx, gy, gw, gh, 0); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    box(ctx, -180, -118, 360, 28, hexc('#eef1f4'), 3, INK, 2.5)
    if label: lib.text(ctx, str(label), 0, -103, 26, hexc('#3a4048'))
    for i in range(2):  # loading bays
        bx = -244 + i * 120
        box(ctx, bx, -84, 104, 84, hexc('#4a4f58'), 0, INK, 3)
        ctx.save(); _p_clip_rr(ctx, bx + 4, -80, 96, 80, 0)
        box(ctx, bx + 4, -80, 96, 80, hexc('#c9ced6'))
        for k in range(9): box(ctx, bx + 4, -80 + k * 9, 96, 8, hexc('#c9ced6') if k % 2 else hexc('#aeb5bf'), 0, INK, 1.3)
        ctx.restore()
        box(ctx, bx - 6, -92, 116, 10, hexc('#c0392b'), 2, INK, 2.5)
        box(ctx, bx - 6, -85, 116, 3, hexc('#8f2a1f'))
        for px_ in (bx + 16, bx + 88): box(ctx, px_, -12, 7, 12, hexc('#e0a82e'), 2, INK, 2)
        lib.text(ctx, str(i + 1), bx + 52, -30, 34, hexc('#5a4632'))
    box(ctx, 40, -66, 44, 66, hexc('#3a4450'), 2, INK, 2.5)  # personnel door
    box(ctx, 46, -60, 32, 40, PGLASS, 0, INK, 2)
    for k in range(2): box(ctx, 100 + k * 52, -66, 40, 30, PGLASS, 1, INK, 2)
    box(ctx, -260, -10, 520, 10, hexc('#aeb5bf'), 0, INK, 2.5)
    ctx.restore()


# ==================================================================
def sewing_machine(ctx, x, y, s=1.0, **kv):
    """Anchor: bottom-centre. 200x140 classic industrial sewing machine at s=1: heavy bed, tall column right,
    horizontal arm with head left, handwheel, red thread spool + path, needle + presser foot, gold
    pinstripe, striped fabric with stitch dashes under the needle. 2-tone teal body."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    body, bd, bl = hexc('#2f4a4a'), hexc('#1f3535'), hexc('#4a6a68')
    _p_ellfill(ctx, 0, -4, 102, 12, (0, 0, 0), a=0.15)
    box(ctx, -100, -18, 200, 18, body, 7, INK, 3)
    box(ctx, -100, -8, 200, 8, bd, 7)
    box(ctx, 30, -128, 58, 112, body, 8, INK, 3)
    box(ctx, 70, -126, 18, 108, bd)
    box(ctx, -74, -128, 104, 32, body, 10, INK, 3)
    box(ctx, -74, -104, 104, 8, bd, 3)
    box(ctx, -92, -104, 26, 44, body, 8, INK, 3)
    line(ctx, [(-90, -112), (26, -112)], hexc('#d9a62e'), 2, .85)
    circle(ctx, 92, -96, 15, bd, INK, 3); circle(ctx, 92, -96, 6, bl, INK, 2)
    line(ctx, [(92, -110), (92, -82)], hexc('#122424'), 3)
    box(ctx, 4, -146, 10, 18, hexc('#b23b2e'), 3, INK, 2)
    _p_ellfill(ctx, 9, -146, 9, 3, hexc('#d9736b'), INK, 1.5)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(6, -142); ctx.curve_to(-40, -142, -76, -128, -84, -114)
    ctx.set_source_rgb(*hexc('#d9736b')); ctx.set_line_width(2); ctx.stroke()
    circle(ctx, -84, -110, 4, hexc('#8d97a3'), INK, 2)
    line(ctx, [(-80, -60), (-80, -44)], hexc('#c9ced6'), 3.5)
    line(ctx, [(-80, -46), (-80, -34)], hexc('#e8ecf0'), 2)
    box(ctx, -86, -30, 12, 6, hexc('#aeb5bf'), 2, INK, 2)
    cloth, cd = hexc('#efe5c4'), hexc('#d8c08e')
    poly(ctx, [(-108, -18), (-40, -18), (-34, -9), (-112, -9)], cloth, INK, 2)
    poly(ctx, [(-112, -9), (-108, -18), (-122, -6), (-127, 2), (-115, 2)], cd, INK, 2)  # hanging end
    for k in range(6): line(ctx, [(-104 + k * 12, -17), (-104 + k * 12, -10)], hexc('#c0392b'), 2.5)
    for k in range(7): line(ctx, [(-86 + k * 4, -13.5), (-84 + k * 4, -13.5)], INK, 1.4)
    ctx.restore()


# ==================================================================
def wafer(ctx, x, y, s=1.0, **kv):
    """Anchor: centre. Silicon wafer r=110 at s=1: disc with a chisel flat edge (bottom), metallic 2-tone,
    looped die grid clipped to the disc, a few lit dies, rainbow sheen as 3 flat pastel arcs (no gradient),
    thin rim + top-left glint."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    r = 110
    def wp():
        fy = r * 0.84
        x0 = math.sqrt(r * r - fy * fy)
        a1, a2 = math.atan2(fy, -x0), math.atan2(fy, x0)
        ctx.new_path(); ctx.arc(0, 0, r, a1, a2); ctx.close_path()
    ctx.set_source_rgb(*hexc('#c6ced8')); wp(); ctx.fill()
    ctx.save(); wp(); ctx.clip()
    ctx.translate(7, 6); ctx.set_source_rgba(*hexc('#9aa6b4'), 0.55)
    ctx.arc(0, 0, r + 8, 0, 2 * math.pi); ctx.fill(); ctx.translate(-7, -6)
    for k in range(-6, 7):
        line(ctx, [(k * 18, -120), (k * 18, 120)], hexc('#7f8a99'), 1.5)
        line(ctx, [(-120, k * 18), (120, k * 18)], hexc('#7f8a99'), 1.5)
    for i in range(-5, 6):
        for j in range(-5, 5):
            if (i * 7 + j * 13) % 11 == 0:
                box(ctx, i * 18 + 1, j * 18 + 1, 16, 16, hexc('#aebfe0'))
    for rad, col in ((58, hexc('#b39ddb')), (84, hexc('#81c784')), (104, hexc('#ffe082'))):
        ctx.arc(0, 8, rad, math.radians(195), math.radians(335))
        ctx.set_source_rgba(*col, 0.34); ctx.set_line_width(22); ctx.stroke()
    ctx.arc(-r * 0.42, -r * 0.5, 26, math.radians(200), math.radians(320))
    ctx.set_source_rgba(1, 1, 1, 0.4); ctx.set_line_width(8); ctx.stroke()
    ctx.restore()
    ctx.set_source_rgb(*INK); wp(); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()


# ==================================================================
def microscope(ctx, x, y, s=1.0, **kv):
    """Anchor: bottom-centre. Compound microscope ~230x300 at s=1: dark base with built-in illuminator
    (light dot + faint rays), curved limb column right, stage with slide + clips, nosepiece with 3
    objectives pointing down at the slide, binocular head with two angled eyepieces, focus knobs."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    body, bd, bl = hexc('#8d97a3'), hexc('#5f6a77'), hexc('#b9c2cc')
    dk, dkd = hexc('#3a4450'), hexc('#262b33')
    _p_ellfill(ctx, 0, -4, 92, 12, (0, 0, 0), a=0.16)
    box(ctx, -76, -34, 152, 30, dk, 12, INK, 3)
    box(ctx, -76, -22, 152, 14, dkd, 8)
    box(ctx, -22, -46, 32, 12, dk, 3, INK, 2)
    circle(ctx, -6, -50, 7, hexc('#ffe27a'), INK, 2)
    for a_ in (-0.5, 0, 0.5): line(ctx, [(-6 + math.sin(a_) * 9, -58), (-6 + math.sin(a_) * 15, -70)], hexc('#ffe27a'), 2, .5)
    poly(ctx, [(36, -34), (66, -34), (60, -216), (30, -216)], body, INK, 3)
    poly(ctx, [(58, -34), (66, -34), (60, -216), (52, -216)], bd)
    ctx.arc(30, -196, 30, math.radians(180), math.radians(270))
    ctx.set_source_rgb(*body); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    box(ctx, -88, -128, 128, 12, bd, 2, INK, 3)
    box(ctx, -88, -120, 128, 6, dk, 2)
    box(ctx, -30, -136, 44, 8, hexc('#dfe7ee'), 1, INK, 1.5)
    for cx_ in (-26, 4): box(ctx, cx_, -139, 10, 5, bl, 1, INK, 1.5)
    poly(ctx, [(-10, -156), (26, -156), (20, -168), (-4, -168)], dk, INK, 2.5)
    for ox, oh_ in ((-4, 20), (7, 15), (18, 11)):
        poly(ctx, [(ox, -156), (ox + 5, -156), (ox + 2, -156 + oh_), (ox + 1, -156 + oh_)], bl, INK, 2)
        box(ctx, ox + 0.5, -156 + oh_ + 3, 3, 4, hexc('#5f6a77'), 1, INK, 1.5)
    box(ctx, 2, -232, 28, 66, body, 4, INK, 3)
    box(ctx, 12, -246, 44, 16, body, 6, INK, 3)
    for sg, rot in ((-1, -0.5), (1, 0.5)):
        ctx.save(); ctx.translate(34 + sg * 8, -242); ctx.rotate(rot)
        box(ctx, -9, -44, 18, 44, dk, 4, INK, 3)
        box(ctx, -11, -50, 22, 10, bl, 4, INK, 2.5)
        _p_ellfill(ctx, 0, -50, 8, 3, hexc('#141820'), INK, 1.5)
        ctx.restore()
    circle(ctx, 54, -104, 13, bl, INK, 2.5); circle(ctx, 54, -104, 4, bd)
    circle(ctx, 54, -84, 8, bl, INK, 2)
    ctx.restore()


# ==================================================================
def laptop(ctx, x, y, s=1.0, screen="", **kv):
    """Anchor: bottom-centre. Open laptop ~330x230 at s=1, 3/4 view: silver skewed deck with looped key rows
    and trackpad, screen tilted back on the rear edge (leaning right), dark bezel; screen=code paints a
    code editor: title bar with dots, coloured token lines, cursor."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    al, ad = hexc('#cfd6de'), hexc('#9fb0be')
    F0, F1 = (-150, -10), (150, -10)
    B0, B1 = (-112, -36), (186, -36)
    def deck_pt(t, p):
        lx, ly = lerp(F0[0], B0[0], t), lerp(F0[1], B0[1], t)
        rx, ry = lerp(F1[0], B1[0], t), lerp(F1[1], B1[1], t)
        return (lerp(lx, rx, p), lerp(ly, ry, p))
    poly(ctx, [F0, F1, B1, B0], al, INK, 3)
    poly(ctx, [F0, F1, (F1[0], 2), (F0[0], 2)], ad, INK, 2.5)
    for r_ in range(4):  # key rows
        ta, tb = 0.16 + r_ * 0.2, 0.16 + r_ * 0.2 + 0.15
        for k in range(13):
            p, q = 0.06 + k * 0.068, 0.06 + k * 0.068 + 0.05
            poly(ctx, [deck_pt(ta, p), deck_pt(ta, q), deck_pt(tb, q), deck_pt(tb, p)], hexc('#3a4450'))
    poly(ctx, [deck_pt(0.03, 0.33), deck_pt(0.03, 0.62), deck_pt(0.13, 0.59), deck_pt(0.13, 0.36)],
         hexc('#b7c2cc'), INK, 1.5)  # trackpad
    T0 = (B0[0] + 36, B0[1] - 188)
    T1 = (B1[0] + 36, B1[1] - 188)
    poly(ctx, [B0, B1, T1, T0], hexc('#262a32'), INK, 3)
    def spt(f, g):  # f across, g up the screen
        bx, by = lerp(B0[0], B1[0], f), lerp(B0[1], B1[1], f)
        tx, ty = lerp(T0[0], T1[0], f), lerp(T0[1], T1[1], f)
        return (lerp(bx, tx, g), lerp(by, ty, g))
    bi = [spt(0.045, 0.055), spt(0.955, 0.055), spt(0.945, 0.945), spt(0.055, 0.945)]
    poly(ctx, bi, hexc('#141824'), INK, 2)
    SLOPE = 36.0 / 188.0
    if screen == "code":
        ctx.save(); _p_pathpoly(ctx, bi); ctx.clip()
        cols = [hexc('#7cf26a'), hexc('#4dd2ff'), hexc('#ff8a5c'), hexc('#ffe27a'), hexc('#8fa3c8'), hexc('#c58fff')]
        p1 = spt(0.055, 0.945)
        box(ctx, p1[0], p1[1], 128, 14, hexc('#20242e'))  # title bar
        for k, tc in enumerate(('#ff5f57', '#febc2e', '#28c840')):
            circle(ctx, p1[0] + 9 + k * 13, p1[1] + 7 - 3 * SLOPE, 3.4, hexc(tc))
        for i in range(9):
            ind = (0, 0.06, 0.06, 0.12, 0.06, 0, 0.06, 0.18, 0)[i]
            g = 0.80 - i * 0.08
            if g < 0.09: break
            a, b = spt(0.08 + ind, g), spt(0.92, g)
            xx, yy = a[0], a[1]
            tok = 2 + (i * 5) % 3
            for k in range(tok):
                wln = 20 + ((i * 31 + k * 17) % 40)
                col = hexc('#5a6a80') if (k == 0 and i % 3 == 0) else cols[(i + k) % len(cols)]
                dy = wln * SLOPE
                poly(ctx, [(xx, yy), (xx + wln, yy - dy), (xx + wln, yy + 7 - dy), (xx, yy + 7)], col)
                xx += wln + 8
        box(ctx, a[0] + 34, yy - 6 - 34 * SLOPE, 4, 13, hexc('#e8ecf2'))  # cursor
        ctx.restore()
    else:
        p1 = spt(0.28, 0.55)
        box(ctx, p1[0], p1[1], 120, 10, hexc('#3b6fe0'), 3)
        box(ctx, p1[0] + 20, p1[1] + 20, 80, 8, hexc('#4a5568'), 3)
    ctx.restore()


# ==================================================================
def whiteboard(ctx, x, y, s=1.0, lines=(), at=(), t=0.0, **kv):
    """Anchor: centre (board middle). 420x320 board at s=1: aluminium frame, white tray with eraser + red
    marker, A-frame legs with casters + stabiliser bar. `lines` are written in marker-handwriting from
    left; line i types in over ~0.5 s once t >= at[i]; empty/None `at` -> all lines shown."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for sg in (-1, 1):
        line(ctx, [(sg * 150, 168), (sg * 186, 300)], INK, 12); line(ctx, [(sg * 150, 168), (sg * 186, 300)], PSTEEL, 7)
        line(ctx, [(sg * 150, 168), (sg * 112, 300)], INK, 12); line(ctx, [(sg * 150, 168), (sg * 112, 300)], PSTEEL_D, 7)
        for wx in (sg * 186, sg * 112):
            circle(ctx, wx, 306, 10, hexc('#2a2d34'), INK, 2.5); circle(ctx, wx, 306, 3.5, PSTEEL_L)
    box(ctx, -190, 240, 380, 8, PSTEEL_D, 3, INK, 2.5)
    rrect(ctx, -220, -170, 440, 340, 10); ctx.set_source_rgb(*PSTEEL); ctx.fill_preserve()
    ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    box(ctx, -214, -164, 428, 4, PSTEEL_L, 2)
    box(ctx, -202, -152, 404, 304, hexc('#f8fafb'), 4, INK, 2.5)
    box(ctx, -202, -152, 404, 16, hexc('#eef2f5'), 4)
    box(ctx, -186, 152, 372, 14, hexc('#c9ced6'), 4, INK, 2.5)
    box(ctx, -186, 162, 372, 6, PSTEEL_D, 3)
    box(ctx, -60, 146, 44, 12, hexc('#5a6270'), 3, INK, 2)
    box(ctx, -60, 146, 44, 4, hexc('#7a828f'), 2)
    box(ctx, 30, 150, 54, 7, hexc('#b23b2e'), 3, INK, 2)
    circle(ctx, 82, 153.5, 3, hexc('#e8ecf0'), INK, 1.2)
    lines = list(lines or [])
    at = list(at or [])
    mk = [hexc('#1f3a5f'), hexc('#232323'), hexc('#8a2f2f'), hexc('#1e6b34')]
    for i, ln in enumerate(lines):
        rev = 1.0
        if at:
            a = float(at[i]) if i < len(at) else float(at[-1])
            rev = clamp((t - a) / 0.5)
        if rev <= 0: continue
        col = mk[i % len(mk)]
        ly = -124 + i * 52
        box(ctx, -176, ly - 12, 9, 5, col, 2)
        lib.text(ctx, str(ln), -160, ly + 2, 38, col, anchor="l", reveal=rev * 1.15, rot=-0.02)
    ctx.restore()


# ==================================================================
def chalk_text(ctx, x, y, s=1.0, text="chalk", t=0.0, t0=0.0, size=52, seed=4, **kv):
    """Anchor: centre of the text block. White chalk handwriting, per-letter jitter (seeded), revealed like
    a typewriter at ~0.05 s/char from `t0`. Accepts literal two-char "\\n" sequences as line breaks.
    Draws on transparent background (the chalkboard comes from the bg)."""
    txt = str(text).replace("\\n", "\n")
    rnd = random.Random(seed)
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ls = txt.split("\n")
    lh = size * 1.18
    ctx.select_font_face(FONT); ctx.set_font_size(size)
    wmax = max(sum(ctx.text_extents(ch).x_advance for ch in l) + len(l) * 1.5 for l in ls)
    bw, bh = wmax + 96, len(ls) * lh + 76                       # its own small chalkboard so it always reads as chalk-on-board
    box(ctx, -bw / 2, -bh / 2, bw, bh, hexc('#8b5a33'), 8, INK, 3)
    box(ctx, -bw / 2 + 12, -bh / 2 + 12, bw - 24, bh - 24, hexc('#2e5c46'), 3, INK, 2)
    line(ctx, [(-bw / 2 + 28, bh / 2 - 20), (-bw / 2 + 62, bh / 2 - 20)], (1, 1, 1), 4, .7)  # chalk stub in the frame
    y0 = -((len(ls) - 1) / 2) * lh
    shown = (t - t0) / 0.05
    chalk = hexc('#f2f6f8')
    n = 0
    for li, l in enumerate(ls):
        ctx.select_font_face(FONT); ctx.set_font_size(size)
        widths = [ctx.text_extents(ch).x_advance for ch in l]
        wtot = sum(widths) + len(l) * 1.5
        px, base_y = -wtot / 2, y0 + li * lh
        for ci, ch in enumerate(l):
            n += 1
            if shown < n: continue
            dx, dy = rnd.uniform(-1.5, 1.5), rnd.uniform(-2.2, 2.2)
            if ch != " ":
                lib.text(ctx, ch, px + dx + 1, base_y + dy + 1.2, size, (0.72, 0.78, 0.84), anchor="l")
                lib.text(ctx, ch, px + dx, base_y + dy, size, chalk, anchor="l")
            px += widths[ci] + 1.5
    ctx.restore()


# ==================================================================
def tv_screen(ctx, x, y, s=1.0, headline="VIETNAM EXPORTS SOAR", **kv):
    """Anchor: centre. TV set ~532x330 at s=1: dark bezel with sheen strip + neck/pedestal stand; screen is
    a news page: red BREAKING band, generic 'WORLD NEWS' channel bug, plain `headline` (auto-wrap),
    side story panel with placeholder bars, LIVE ticker. No real channel logos."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    bz, bd = hexc('#3a4049'), hexc('#23262c')
    box(ctx, -14, 138, 28, 26, bd, 0, INK, 3)
    box(ctx, -80, 162, 160, 12, bz, 6, INK, 3)
    box(ctx, -266, -160, 532, 300, bd, 14, INK, 3.5)
    box(ctx, -266, -160, 532, 10, hexc('#4a525e'), 14)
    sx, sy, sw, sh = -252, -146, 504, 272
    box(ctx, sx, sy, sw, sh, hexc('#f2f4f6'), 4, INK, 2)
    ctx.save(); _p_clip_rr(ctx, sx, sy, sw, sh, 4)
    box(ctx, sx, sy, sw, 46, hexc('#c0392b'))
    box(ctx, sx, sy + 46, sw, 6, hexc('#8f2a1f'))
    lib.text(ctx, "BREAKING", sx + 76, sy + 26, 34, (1, 1, 1))
    box(ctx, sx + sw - 150, sy + 8, 140, 30, hexc('#1f2d44'), 4, INK, 2)
    lib.text(ctx, "WORLD NEWS", sx + sw - 80, sy + 24, 20, (1, 1, 1))
    hl = str(headline).replace("\\n", "\n")
    if "\n" not in hl:
        ctx.select_font_face(FONT); ctx.set_font_size(46); lim = sw * 0.62
        words, cur, ls = hl.split(), "", []
        for w_ in words:
            if ctx.text_extents(cur + " " + w_).x_advance > lim and cur: ls.append(cur); cur = w_
            else: cur = (cur + " " + w_).strip()
        if cur: ls.append(cur)
        hl = "\n".join(ls[:2])
    for i, l in enumerate(hl.split("\n")):
        lib.text(ctx, l, sx + sw * 0.36, sy + 96 + i * 48, 44, hexc('#141820'))
    box(ctx, sx + sw - 160, sy + 70, 138, 116, hexc('#dfe6ee'), 4, INK, 2)
    box(ctx, sx + sw - 150, sy + 80, 50, 50, hexc('#7a93ab'), 2)
    for k in range(3): box(ctx, sx + sw - 150, sy + 140 + k * 14, 118 - (k == 2) * 30, 7, hexc('#8d97a3'), 2)
    box(ctx, sx, sy + sh - 34, sw, 34, hexc('#1f2d44'))
    box(ctx, sx, sy + sh - 34, 74, 34, hexc('#c0392b'))
    lib.text(ctx, "LIVE", sx + 37, sy + sh - 16, 24, (1, 1, 1))
    rnd = random.Random(6)
    xx = sx + 88
    while xx < sx + sw - 30:
        wln = rnd.randint(26, 74)
        box(ctx, xx, sy + sh - 22, wln, 8, hexc('#8fa8c8'), 2)
        xx += wln + 12
    ctx.restore()
    rrect(ctx, sx, sy, sw, sh, 4); ctx.set_source_rgb(*INK); ctx.set_line_width(2); ctx.stroke()
    circle(ctx, 250, 128, 4, hexc('#5fd35f'), INK, 1.5)
    ctx.restore()



# ==================================================================
def carton(ctx, x, y, s=1.0, label="FRAGILE", **kv):
    """Anchor: bottom-centre. 180x140 cardboard box at s=1: front face in 2 tones, top face in perspective
    with flap seam, tape seam over top + down the front, stamped red double-border plain `label`,
    a small sticker block and up-arrow hints."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    cb, cd = hexc('#d8b98a'), hexc('#c0a071')
    box(ctx, -90, -112, 180, 112, cb, 0, INK, 3)
    box(ctx, 62, -110, 26, 108, cd)
    poly(ctx, [(-90, -112), (-64, -138), (66, -138), (90, -112)], hexc('#c9a878'), INK, 3)
    line(ctx, [(-60, -131), (62, -131)], hexc('#b2905f'), 2.5)
    poly(ctx, [(-16, -112), (16, -112), (12, -138), (-12, -138)], hexc('#e8d8a8'), INK, 1.5)
    box(ctx, -16, -112, 32, 112, hexc('#e8d8a8'), 0, INK, 1.5)
    box(ctx, 12, -112, 4, 112, hexc('#d2c08c'))
    lab = str(label).replace("\\n", "\n").split("\n")
    ctx.save(); ctx.translate(2, -52); ctx.rotate(-0.08)
    ink = hexc('#b3261e')
    ctx.select_font_face(FONT); ctx.set_font_size(22)
    w_ = max(ctx.text_extents(l).width for l in lab) + 26
    h_ = 24 * len(lab) + 14
    rrect(ctx, -w_ / 2, -h_ / 2, w_, h_, 6); ctx.set_source_rgb(*ink); ctx.set_line_width(2.5); ctx.stroke()
    rrect(ctx, -w_ / 2 + 4, -h_ / 2 + 4, w_ - 8, h_ - 8, 4); ctx.set_line_width(1.2); ctx.stroke()
    for i, l in enumerate(lab):
        lib.text(ctx, l, 0, (i - (len(lab) - 1) / 2) * 22 + 4, 22, ink, anchor="c")
    ctx.restore()
    for ax in (44, 58):
        poly(ctx, [(ax, -98), (ax + 8, -98), (ax + 4, -106)], cd, a=0.9)
        box(ctx, ax + 2.5, -90, 3, 10, cd)
    ctx.restore()


# ==================================================================
def cargo_plane(ctx, x, y, s=1.0, **kv):
    """Anchor: centre (fuselage middle). Wide-body cargo jet ~700 wide at s=1 facing LEFT: white tube with grey
    belly + cheatline, raised hinged nose door, dark front hold opening, swept wing + one big engine, tall
    tail, gear down; a loader ramp with cartons at the nose. Plain livery, 'CARGO' lettering only."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    body, bd, bl = hexc('#eef1f4'), hexc('#c9d2da'), hexc('#f8fafc')
    dk = hexc('#16181d')
    poly(ctx, [(240, -60), (330, -92), (342, -86), (262, -52)], bd, INK, 2.5)  # far stabiliser
    poly(ctx, [(212, -58), (268, -196), (306, -196), (316, -58)], body, INK, 3)  # tail fin
    poly(ctx, [(268, -196), (306, -196), (316, -58), (292, -58)], bd)
    line(ctx, [(272, -170), (302, -170)], hexc('#9fb0c4'), 8)
    fu = [-296, -66, 596, 132]
    ctx.save(); rrect(ctx, *fu, 58); ctx.clip()
    box(ctx, -300, -70, 610, 60, bl)
    box(ctx, -300, -14, 610, 12, hexc('#9fb0c4'))
    box(ctx, -300, 14, 610, 80, bd)
    box(ctx, -300, -52, 62, 108, dk)  # front hold opening
    for k in range(3): line(ctx, [(-296, -34 + k * 30), (-242, -34 + k * 30)], hexc('#3a4049'), 2)
    box(ctx, -300, 52, 70, 8, PSTEEL_D)
    ctx.restore()
    rrect(ctx, *fu, 58); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    lib.text(ctx, "CARGO", -60, -26, 34, hexc('#4a5a70'))
    for k in range(3):
        poly(ctx, [(-262 + k * 16, -48), (-250 + k * 16, -48), (-254 + k * 16, -36), (-266 + k * 16, -36)], dk, a=0.9)
    for k in range(3): circle(ctx, -180 + k * 16, -40, 3.5, hexc('#3a4450'), INK, 1.2)
    ctx.save(); ctx.translate(-248, -60); ctx.rotate(1.45)  # nose door swung up over the nose
    door = [(0, -4), (-24, 0), (-42, 22), (-46, 52), (-32, 76), (-6, 86), (2, 86)]
    poly(ctx, door, bl, INK, 3)
    poly(ctx, [(-24, 0), (-42, 22), (-46, 52), (-32, 76), (-26, 50), (-18, 14)], bd)
    line(ctx, [(-10, 16), (-34, 38)], PSTEEL_D, 2); line(ctx, [(-8, 56), (-28, 66)], PSTEEL_D, 2)
    ctx.restore()
    line(ctx, [(-240, -66), (-308, -72)], INK, 3)  # hold-open strut
    poly(ctx, [(-64, 26), (96, 26), (216, 106), (56, 106)], hexc('#cfd8e0'), INK, 3)  # wing
    poly(ctx, [(-64, 26), (24, 26), (140, 106), (56, 106)], hexc('#b7c2cc'))
    box(ctx, 60, 26, 16, 34, hexc('#9fb0c4'), 0, INK, 2.5)  # pylon
    rrect(ctx, 24, 58, 130, 58, 25); ctx.set_source_rgb(*hexc('#8d97a3')); ctx.fill_preserve()
    ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    box(ctx, 24, 96, 130, 20, hexc('#6f7a88'), 10)
    circle(ctx, 28, 87, 21, dk, INK, 3)
    circle(ctx, 28, 87, 11, hexc('#3a4049'))
    for k in range(6): line(ctx, [(52, 68 + k * 8), (140, 64 + k * 8)], hexc('#5f6a77'), 2, .5)
    for gx, gr in ((-232, 15), (170, 18), (202, 18)):  # gear
        line(ctx, [(gx, 66), (gx, 106)], hexc('#5f6a77'), 7); line(ctx, [(gx, 66), (gx, 106)], INK, 2)
        circle(ctx, gx, 116, gr, hexc('#23262c'), INK, 3); circle(ctx, gx, 116, gr * 0.45, hexc('#aeb5bf'))
    line(ctx, [(-486, 128), (-262, 52)], INK, 12)  # loader ramp
    line(ctx, [(-486, 128), (-262, 52)], PSTEEL, 7)
    line(ctx, [(-486, 140), (-262, 64)], INK, 12)
    line(ctx, [(-486, 140), (-262, 64)], PSTEEL_D, 7)
    for k in range(9):
        f = k / 8
        rx, ry = lerp(-486, -262, f), lerp(134, 58, f)
        line(ctx, [(rx - 4, ry - 6), (rx + 4, ry + 6)], PSTEEL_D, 2)
    box(ctx, -518, 118, 76, 34, hexc('#e0a82e'), 4, INK, 3)  # loader body
    box(ctx, -518, 142, 76, 10, hexc('#b8861e'), 3)
    for wx in (-498, -460): circle(ctx, wx, 152, 11, hexc('#23262c'), INK, 2.5); circle(ctx, wx, 152, 4, PSTEEL_L)
    for f in (0.18, 0.44, 0.7):  # cartons on the ramp
        rx, ry = lerp(-486, -270, f), lerp(134, 58, f)
        ctx.save(); ctx.translate(rx, ry - 20); ctx.rotate(-0.35)
        box(ctx, -20, -18, 40, 34, hexc('#d8b98a'), 2, INK, 2.5)
        box(ctx, -4, -18, 8, 34, hexc('#e8d8a8'), 1)
        line(ctx, [(-20, -4), (20, -4)], hexc('#c0a071'), 2)
        ctx.restore()
    ctx.restore()


# ==================================================================
def road_sign(ctx, x, y, s=1.0, text="BAC NINH 30 km", **kv):
    """Anchor: bottom-centre (post feet at y). Green highway sign ~328x122 panel on two steel posts at s=1:
    white inset border, plain white `text` (two lines allowed, literal "\\n" handled), bolt row, shadow."""
    txt = str(text).replace("\\n", "\n").split("\n")
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    _p_ellfill(ctx, 0, -2, 130, 8, (0, 0, 0), a=0.15)
    for px_ in (-70, 70):
        box(ctx, px_ - 6, -190, 12, 190, hexc('#7f8a99'), 0, INK, 3)
        box(ctx, px_ + 1, -188, 5, 186, PSTEEL_D)
        for k in range(3): circle(ctx, px_, -182 + k * 4, 1.8, hexc('#4a5060'))
    box(ctx, -164, -306, 328, 122, hexc('#1e6b34'), 10, INK, 3)
    box(ctx, -164, -306, 328, 10, hexc('#2e8146'), 10)
    rrect(ctx, -154, -296, 308, 102, 6); ctx.set_source_rgb(1, 1, 1); ctx.set_line_width(3.5); ctx.stroke()
    if len(txt) == 1:
        lib.text(ctx, txt[0], 0, -240, 40, (1, 1, 1))
    else:
        for i, l in enumerate(txt[:2]):
            lib.text(ctx, l, 0, -260 + i * 44, 38, (1, 1, 1))
    for k in range(5): circle(ctx, -120 + k * 60, -190, 2.4, hexc('#4a5060'))
    ctx.restore()


# ==================================================================
def trophy(ctx, x, y, s=1.0, **kv):
    """Anchor: centre. Gold cup ~190x230 at s=1: wide rim ellipse, U bowl with highlight arc and engraved
    star, two scroll handles, stem, tiered black base with a gold plaque."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    gd, gdd, gl = hexc('#e6b830'), hexc('#c2921f'), hexc('#f2d074')
    for sg in (-1, 1):
        a0, a1 = (math.radians(-40), math.radians(160)) if sg > 0 else (math.radians(20), math.radians(220))
        ctx.new_path(); ctx.arc(sg * 62, -48, 30, a0, a1)
        ctx.set_source_rgb(*INK); ctx.set_line_width(14); ctx.stroke()
        ctx.new_path(); ctx.arc(sg * 62, -48, 30, a0, a1)
        ctx.set_source_rgb(*gd); ctx.set_line_width(9); ctx.stroke()
    bowl = lambda c: (c.move_to(-58, -80), c.line_to(58, -80),
                      c.curve_to(56, -18, 30, 6, 0, 6), c.curve_to(-30, 6, -56, -18, -58, -80), c.close_path())
    bowl(ctx); ctx.set_source_rgb(*gd); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    ctx.save(); bowl(ctx); ctx.clip()
    poly(ctx, [(30, -80), (58, -80), (34, 4), (16, 2)], gdd)
    ctx.new_path(); ctx.arc(-34, -40, 40, math.radians(195), math.radians(255))
    ctx.set_source_rgb(*gl); ctx.set_line_width(9); ctx.stroke()
    ctx.restore()
    _p_ellfill(ctx, 0, -80, 58, 11, gl, INK, 3)
    _p_ellfill(ctx, 0, -80, 48, 7, gd, INK, 1.5)
    star = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = 13 if k % 2 == 0 else 5.5
        star.append((math.cos(a) * rr, -42 + math.sin(a) * rr))
    poly(ctx, star, gdd, INK, 2)
    box(ctx, -10, 6, 20, 26, gd, 3, INK, 3)
    box(ctx, -26, 30, 52, 14, gdd, 3, INK, 3)
    box(ctx, -46, 44, 92, 22, hexc('#26292f'), 5, INK, 3)
    box(ctx, -46, 60, 92, 10, hexc('#14171b'), 4)
    box(ctx, -26, 48, 52, 12, gdd, 2, INK, 2)
    circle(ctx, 0, 54, 2.4, hexc('#7a5a10'))
    ctx.restore()


# ==================================================================
def vault_door(ctx, x, y, s=1.0, open_=0.0, **kv):
    """Anchor: centre. Round steel vault r=200 at s=1: concrete wall ring with rivets + side keypad, dark
    opening with a gold-bar shelf behind, sliding door disc (retracting deadbolts, 8 spokes, hub wheel
    that spins as it opens). open_ 0..1 slides the door right into the wall pocket."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    open_ = clamp(open_)
    wall, wd = hexc('#6f757d'), hexc('#4a4f58')
    circle(ctx, 0, 0, 204, wall, INK, 3.5)
    circle(ctx, 0, 0, 196, hexc('#7d838c'), INK, 2.5)
    for k in range(24):
        a = math.pi * 2 * k / 24
        circle(ctx, math.cos(a) * 190, math.sin(a) * 190, 5, wd, INK, 2)
    box(ctx, 168, 60, 34, 60, hexc('#3a4049'), 4, INK, 2.5)
    for r_ in range(3):
        for c_ in range(2): box(ctx, 174 + c_ * 13, 68 + r_ * 15, 9, 9, hexc('#8d97a3'), 1)
    ctx.save(); ctx.new_path(); ctx.arc(0, 0, 184, 0, 2 * math.pi); ctx.clip()
    circle(ctx, 0, 0, 184, hexc('#101418'))
    for k in range(3): circle(ctx, 0, 0, 168 - k * 14, hexc('#181d24') if k % 2 else hexc('#14181e'))
    box(ctx, -70, 30, 120, 8, hexc('#3a4049'), 2)  # shelf
    for k in range(4):  # gold bars
        box(ctx, -52 + (k % 2) * 34, 16 - (k // 2) * 14, 30, 12, hexc('#d9a62e'), 2, INK, 2)
    dx = open_ * 380
    ctx.save(); ctx.translate(dx, 0)  # door
    circle(ctx, 0, 0, 178, hexc('#aeb8c4'), INK, 3)
    ctx.save(); ctx.new_path(); ctx.arc(0, 0, 176, 0, 2 * math.pi); ctx.clip()
    ctx.new_path(); ctx.arc(-50, -50, 150, math.radians(90), math.radians(270))
    ctx.set_source_rgb(*hexc('#c3ccd6')); ctx.set_line_width(30); ctx.stroke()
    poly(ctx, [(60, -176), (176, -176), (176, 176), (60, 176)], hexc('#8d97a3'), a=0.5)
    ctx.restore()
    circle(ctx, 0, 0, 152, hexc('#9aa6b4'), INK, 2.5)
    for k in range(16):  # deadbolts retract as it opens
        a = math.pi * 2 * k / 16
        bl_ = lerp(14, 3, min(1.0, open_ * 3))
        x1, y1 = math.cos(a) * 168, math.sin(a) * 168
        x2, y2 = math.cos(a) * (168 + bl_), math.sin(a) * (168 + bl_)
        line(ctx, [(x1, y1), (x2, y2)], hexc('#5f6a77'), 9)
        circle(ctx, x2, y2, 4.5, PSTEEL_L, INK, 1.5)
    for k in range(8):  # spokes
        a = math.pi * 2 * k / 8 + 0.2
        line(ctx, [(math.cos(a) * 60, math.sin(a) * 60), (math.cos(a) * 148, math.sin(a) * 148)], INK, 16)
        line(ctx, [(math.cos(a) * 60, math.sin(a) * 60), (math.cos(a) * 148, math.sin(a) * 148)], PSTEEL, 11)
    circle(ctx, 0, 0, 58, hexc('#7d8794'), INK, 3)
    ctx.save(); ctx.rotate(open_ * 2.6)  # spinning wheel
    circle(ctx, 0, 0, 40, hexc('#c8862e'), INK, 3)
    for k in range(5):
        a = math.pi * 2 * k / 5
        line(ctx, [(0, 0), (math.cos(a) * 40, math.sin(a) * 40)], INK, 8)
        line(ctx, [(0, 0), (math.cos(a) * 40, math.sin(a) * 40)], hexc('#b8861e'), 5)
    for k in range(5):
        a = math.pi * 2 * (k + 0.5) / 5
        circle(ctx, math.cos(a) * 52, math.sin(a) * 52, 6, hexc('#e6b830'), INK, 2)
    circle(ctx, 0, 0, 12, hexc('#e6b830'), INK, 2.5)
    ctx.restore()
    ctx.restore()
    ctx.restore()                                                          # release the opening clip
    ctx.new_path(); ctx.arc(0, 0, 184, 0, 2 * math.pi)
    ctx.set_source_rgb(*hexc('#4a4f58')); ctx.set_line_width(8); ctx.stroke()  # gasket rim
    ctx.restore()


# ==================================================================
def food_stall(ctx, x, y, s=1.0, label="COM TAM", **kv):
    """Anchor: bottom-centre. Vietnamese street cart ~300x290 at s=1: wooden cart with plank lines + two
    spoked wheels, counter with pots (lids), stacked bowls, striped scalloped umbrella on a leaning pole,
    hanging menu flag with plain `label`, glass display box."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    pole = [(66, -92), (48, -236)]
    line(ctx, pole, INK, 8); line(ctx, pole, hexc('#8b5a33'), 4)
    cx, cy = 44, -196  # striped dome canopy: apex above a shallow drooping rim
    apex = (cx, cy - 58)
    rim = lambda t: (cx + (t - 0.5) * 264, cy + 6 + 16 * (2 * t - 1) ** 2)
    for i in range(8):
        x0, y0 = rim(i / 8); x1, y1 = rim((i + 1) / 8)
        poly(ctx, [apex, (x0, y0), (x1, y1)], hexc('#c0392b') if i % 2 == 0 else hexc('#f4ecd8'), INK, 2)
    for i in range(8):  # scalloped hem
        mx, my = rim((i + 0.5) / 8)
        circle(ctx, mx, my + 6, 9, hexc('#c0392b') if i % 2 else hexc('#f4ecd8'), INK, 2)
    x0, y0 = rim(0); x1, y1 = rim(1)
    line(ctx, [(x0, y0), apex, (x1, y1)], INK, 2.5)
    circle(ctx, apex[0], apex[1] - 3, 5, hexc('#d9a62e'), INK, 2)
    wd, wdd = hexc('#c48a4a'), hexc('#a06a32')
    box(ctx, -96, -92, 192, 68, wd, 3, INK, 3)
    box(ctx, -96, -38, 192, 14, wdd, 3)
    for k in range(5): line(ctx, [(-86 + k * 38, -88), (-86 + k * 38, -28)], wdd, 2)
    box(ctx, -102, -102, 204, 12, hexc('#d8a866'), 3, INK, 3)
    box(ctx, -60, -78, 70, 36, hexc('#a06a32'), 2, INK, 2)
    circle(ctx, -25, -60, 3, hexc('#5a4632'))
    for px_, pw, ph_ in ((-84, 44, 40), (-30, 36, 32), (26, 30, 26)):
        box(ctx, px_ - pw / 2, -102 - ph_, pw, ph_, hexc('#8d97a3'), 5, INK, 2.5)
        box(ctx, px_ + pw * 0.18, -102 - ph_ + 3, pw * 0.28, ph_ - 6, hexc('#6f7a88'), 3)
        _p_ellfill(ctx, px_, -102 - ph_ - 3, pw * 0.56, 6, hexc('#c9ced6'), INK, 2.5)
        circle(ctx, px_, -102 - ph_ - 9, 3.5, hexc('#5f6a77'), INK, 1.5)
    for k in range(3):
        _p_ellfill(ctx, 74, -106 - k * 7, 13, 5, hexc('#eef2f5'), INK, 1.8)
    box(ctx, -18, -134, 44, 32, hexc('#bfe4f4'), 3, INK, 2)
    for dx in (0, 10, 20): circle(ctx, -8 + dx, -120, 4, hexc('#e0a82e'))
    line(ctx, [(-18, -118), (26, -118)], (1, 1, 1), 2, .6)
    box(ctx, -124, -86, 8, 40, hexc('#8b5a33'), 0, INK, 2)
    ctx.save(); ctx.translate(-120, -50); ctx.rotate(0.06)
    box(ctx, -34, -20, 68, 40, hexc('#efe5c4'), 3, INK, 2.5)
    lib.text(ctx, str(label), 0, -4, 19, hexc('#8a2f2f'))
    box(ctx, -26, 6, 52, 4, hexc('#b7aa82'), 1)
    ctx.restore()
    for wx in (-58, 58):
        circle(ctx, wx, -18, 22, hexc('#3a4450'), INK, 3)
        circle(ctx, wx, -18, 6, hexc('#8d97a3'), INK, 2)
        for k in range(6):
            a = math.pi * 2 * k / 6 + 0.3
            line(ctx, [(wx, -18), (wx + math.cos(a) * 19, -18 + math.sin(a) * 19)], hexc('#6f7a88'), 2.5)
    ctx.restore()



# ==================================================================
def empty_chairs(ctx, x, y, s=1.0, **kv):
    """Anchor: bottom-centre. Three empty chairs (~90 wide each, 190 tall at s=1) with jackets draped over
    the backrests (no-shows) and a small 'Zzz' above the middle chair. Wood 2-tone + INK; fixed slight
    tilts by index math (deterministic)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    wood, woodd = hexc('#a8703f'), hexc('#8b5a33')
    jacket = [hexc('#3a4a63'), hexc('#6b3a3a'), hexc('#2f5240')]
    tilt = (-0.05, 0.0, 0.05)
    sc = (0.96, 1.0, 0.98)
    for i in range(3):
        cx = -120 + i * 120
        ctx.save(); ctx.translate(cx, 0); ctx.rotate(tilt[i]); ctx.scale(sc[i], sc[i])
        _p_ellfill(ctx, 0, -2, 48, 6, (0, 0, 0), a=0.15)
        for a_, b_ in (((-38, -60), (-44, 0)), ((38, -60), (44, 0)), ((-30, -60), (-34, -14)), ((30, -60), (34, -14))):
            line(ctx, [a_, b_], INK, 8)
            line(ctx, [a_, b_], woodd, 4)
        box(ctx, -44, -70, 88, 12, wood, 3, INK, 3)
        box(ctx, -44, -64, 88, 6, woodd, 3)
        for bx in (-38, 30):
            box(ctx, bx, -182, 10, 118, wood, 2, INK, 3)
        for sy in (-176, -150):
            box(ctx, -34, sy, 70, 12, wood, 2, INK, 2.5)
            box(ctx, -34, sy + 8, 70, 4, woodd, 2)
        jc = jacket[i]
        poly(ctx, [(-42, -186), (42, -186), (46, -150), (30, -110), (10, -120), (-10, -120), (-30, -110), (-46, -150)], jc, INK, 2.5)
        poly(ctx, [(42, -186), (46, -150), (30, -110), (18, -118), (26, -150), (12, -180)], _p_dk(jc, .25))
        poly(ctx, [(-10, -186), (0, -168), (10, -186)], _p_lt(jc, .35))
        for sg in (-1, 1):
            poly(ctx, [(sg * 44, -170), (sg * 54, -168), (sg * 56, -116), (sg * 46, -114)], jc, INK, 2)
        ctx.restore()
    for zx, zy, zs in [(18, -206, 26), (40, -232, 34), (64, -260, 42)]:
        lib.text(ctx, "Z", zx, zy, zs, hexc('#e8ecf0'), anchor="l", outline=INK, rot=0.15)
    ctx.restore()


# ==================================================================
def loudspeaker_pole(ctx, x, y, s=1.0, **kv):
    """Anchor: bottom-centre. Village PA pole ~330 tall at s=1: 2-tone wooden pole with a crossbar, two horn
    speakers facing outward (metal throat + flared mouth + dark rim ellipse), junction box on top, a
    sagging wire looping off left and short leads to the speaker backs."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    _p_ellfill(ctx, 0, -3, 26, 6, (0, 0, 0), a=0.16)
    wood, woodd = hexc('#8b5a33'), hexc('#6b3f1d')
    box(ctx, -9, -306, 18, 306, wood, 0, INK, 3)
    box(ctx, 3, -304, 6, 300, woodd)
    for k in range(6): line(ctx, [(-9, -40 - k * 52), (9, -46 - k * 52)], woodd, 2, .6)
    box(ctx, -74, -292, 148, 10, hexc('#5f6a77'), 2, INK, 2.5)
    for sg in (-1, 1):
        ctx.save(); ctx.translate(sg * 78, -286)
        box(ctx, -14, -12, 28, 24, hexc('#4a4f58'), 4, INK, 2.5)
        poly(ctx, [(0, -14), (sg * 26, -20), (sg * 26, 20), (0, 14)], hexc('#8d97a3'), INK, 2.5)
        poly(ctx, [(sg * 26, -20), (sg * 58, -34), (sg * 58, 34), (sg * 26, 20)], hexc('#b9c2cc'), INK, 2.5)
        poly(ctx, [(sg * 40, -27), (sg * 58, -34), (sg * 58, 34), (sg * 40, 27)], hexc('#8d97a3'))
        _p_ellfill(ctx, sg * 58, 0, 7, 34, hexc('#5f6a77'), INK, 2.5)
        _p_ellfill(ctx, sg * 58, 0, 4, 26, hexc('#2a2d34'))
        ctx.restore()
    box(ctx, -16, -330, 32, 20, hexc('#3a4450'), 3, INK, 2.5)
    for k in range(4): circle(ctx, -8 + (k % 2) * 16, -325 + (k // 2) * 8, 2, PSTEEL_L)
    ctx.new_path(); ctx.move_to(0, -334); ctx.curve_to(-60, -400, -140, -360, -190, -392)
    ctx.set_source_rgb(*INK); ctx.set_line_width(4); ctx.stroke()
    ctx.new_path(); ctx.move_to(0, -334); ctx.curve_to(-60, -400, -140, -360, -190, -392)
    ctx.set_source_rgb(*hexc('#2a2d34')); ctx.set_line_width(2); ctx.stroke()
    for sg in (-1, 1):
        p0, c, p1 = (sg * 8, -322), (sg * 40, -300), (sg * 68, -288)
        ctx.new_path(); ctx.move_to(*p0)
        ctx.curve_to(p0[0] + 2 / 3 * (c[0] - p0[0]), p0[1] + 2 / 3 * (c[1] - p0[1]),
                     p1[0] + 2 / 3 * (c[0] - p1[0]), p1[1] + 2 / 3 * (c[1] - p1[1]), *p1)
        ctx.set_source_rgb(*hexc('#2a2d34')); ctx.set_line_width(2.5); ctx.stroke()
    circle(ctx, 0, -306, 5, hexc('#5a4632'), INK, 2)
    ctx.restore()


# ==================================================================
def compass(ctx, x, y, s=1.0, **kv):
    """Anchor: centre. Nautical compass rose r=150 at s=1: parchment ring with tick marks, 8-point star
    (light/dark split cardinal points + shorter diagonals), gold hub, plain N/E/S/W lettering
    (N on top)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    navy, lt, pk = hexc('#22304e'), hexc('#f7f2e2'), hexc('#efe3c0')
    circle(ctx, 0, 0, 150, hexc('#d8cdaa'), INK, 3)
    circle(ctx, 0, 0, 138, pk, INK, 2.5)
    for k in range(60):
        a = math.pi * 2 * k / 60
        r1, lw_ = (118, 2.5) if k % 5 == 0 else (126, 1.4)
        line(ctx, [(math.cos(a) * r1, math.sin(a) * r1), (math.cos(a) * 136, math.sin(a) * 136)], navy, lw_)
    circle(ctx, 0, 0, 112, lt, INK, 2.5)
    for k in range(8):
        a = -math.pi / 2 + k * math.pi / 4
        lng = k % 2 == 0
        tip = (math.cos(a) * (104 if lng else 64), math.sin(a) * (104 if lng else 64))
        for f, flip in ((-1, True), (1, False)):
            pa = a + math.pi / 2
            bx, by = math.cos(pa) * 14 * f, math.sin(pa) * 14 * f
            dark = flip if lng else not flip
            poly(ctx, [(0, 0), (bx, by), tip], navy if dark else lt, INK, 1.6)
    for k in range(4):
        a = -math.pi / 2 + k * math.pi / 2 + math.pi / 4
        line(ctx, [(math.cos(a) * 30, math.sin(a) * 30), (math.cos(a) * 44, math.sin(a) * 44)], hexc('#b8861e'), 2)
    circle(ctx, 0, 0, 11, hexc('#e6b830'), INK, 2.5)
    circle(ctx, 0, 0, 4, navy)
    lib.text(ctx, "N", 0, -127, 40, navy)
    lib.text(ctx, "E", 128, 6, 22, navy)
    lib.text(ctx, "S", 0, 134, 22, navy)
    lib.text(ctx, "W", -128, 6, 22, navy)
    ctx.restore()


# ==================================================================
def sneaker(ctx, x, y, s=1.0, **kv):
    """Anchor: centre. Side-view trainer ~270x150 at s=1 facing right: thick white sole with toe upturn +
    tread ticks, 2-tone blue upper with heel counter / toe cap / eyestay overlays, generic diagonal
    white side band (no brand mark), criss-cross laces, tongue, collar opening, heel pull tab."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ub, ud = hexc('#3f8ec9'), hexc('#2c6690')
    sole, soled = hexc('#f4f4f2'), hexc('#cfd0c8')
    ctx.new_path()
    ctx.move_to(-128, 30); ctx.line_to(104, 30)
    ctx.curve_to(126, 28, 136, 16, 134, 4); ctx.line_to(-120, 4)
    ctx.curve_to(-126, 12, -128, 20, -128, 30); ctx.close_path()
    ctx.set_source_rgb(*sole); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    box(ctx, -122, 4, 250, 10, soled, 4)
    for k in range(11): line(ctx, [(-116 + k * 22, 40), (-112 + k * 22, 31)], hexc('#9aa0a8'), 2.5)
    line(ctx, [(-120, 15), (128, 12)], hexc('#b9c2cc'), 3)
    ctx.new_path()
    ctx.move_to(-118, 6); ctx.line_to(-118, -52)
    ctx.curve_to(-112, -74, -86, -78, -70, -70)
    ctx.line_to(-18, -22); ctx.line_to(34, -34)
    ctx.curve_to(76, -44, 104, -26, 122, 2); ctx.line_to(126, 6); ctx.close_path()
    ctx.set_source_rgb(*ub); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    poly(ctx, [(-118, 6), (-118, -52), (-96, -62), (-88, -2), (-96, 6)], ud, INK, 2)
    poly(ctx, [(70, -30), (104, -20), (122, 2), (126, 6), (76, 6)], ud, INK, 2)
    poly(ctx, [(-16, -26), (36, -36), (40, -28), (-12, -18)], ud, INK, 2)  # eyestay strip
    poly(ctx, [(-38, -8), (64, -2), (62, 4), (-44, -1)], (1, 1, 1), INK, 2)  # generic side band
    poly(ctx, [(-66, -64), (-26, -30), (-34, -22), (-74, -56)], hexc('#7fbae8'), INK, 2)  # tongue
    ctx.new_path(); ctx.arc(-86, -56, 13, math.radians(115), math.radians(325))
    ctx.set_source_rgb(*hexc('#23262c')); ctx.set_line_width(6); ctx.stroke()
    poly(ctx, [(-102, -64), (-90, -72), (-86, -58)], ud, INK, 1.6)  # pull tab
    for k in range(3):  # criss-cross laces along the throat
        x0, y0 = -12 + k * 16, -25 - k * 4
        line(ctx, [(x0, y0), (x0 + 11, y0 - 9)], INK, 3.5)
        line(ctx, [(x0 + 11, y0), (x0, y0 - 9)], INK, 3.5)
        line(ctx, [(x0, y0), (x0 + 11, y0 - 9)], hexc('#eef1f4'), 2)
        line(ctx, [(x0 + 11, y0), (x0, y0 - 9)], hexc('#eef1f4'), 2)
        circle(ctx, x0, y0 + 1, 1.8, hexc('#23262c')); circle(ctx, x0 + 11, y0 + 1, 1.8, hexc('#23262c'))
    ctx.restore()


# ==================================================================
def solar_panel(ctx, x, y, s=1.0, **kv):
    """Anchor: bottom-centre. Ground-mounted PV array ~340 wide at s=1: tilted panel with aluminium frame,
    12x4 dark cell grid + lighter busbars, two support legs + cross bar and feet, flat white sun-glint
    bands across the cells and one small diamond sparkle (static)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    _p_ellfill(ctx, 20, -2, 120, 8, (0, 0, 0), a=0.16)
    for lx, tx in ((-70, -52), (66, 96)):
        line(ctx, [(lx, -6), (tx, -118)], INK, 12); line(ctx, [(lx, -6), (tx, -118)], hexc('#7f8a99'), 7)
        box(ctx, lx - 14, -8, 28, 8, hexc('#5f6a77'), 2, INK, 2.5)
    box(ctx, -40, -70, 90, 7, hexc('#8d97a3'), 3, INK, 2.5)
    ctx.save(); ctx.translate(20, -150); ctx.rotate(-0.30)
    box(ctx, -160, -52, 320, 104, hexc('#b9c2cc'), 6, INK, 3)
    box(ctx, -150, -44, 300, 88, hexc('#1f3a5f'), 3, INK, 2)
    ctx.save(); _p_clip_rr(ctx, -150, -44, 300, 88, 3)
    for k in range(12):
        xx = -150 + k * 25
        box(ctx, xx + 1.5, -42, 22, 84, hexc('#2a4a77'))
        box(ctx, xx + 12, -42, 1.4, 84, hexc('#7f9fc4'))
    for yy in (-20, 0, 20): line(ctx, [(-150, yy), (150, yy)], hexc('#7f9fc4'), 1.3)
    poly(ctx, [(-40, -46), (10, -46), (-40, 46), (-90, 46)], (1, 1, 1), a=0.20)
    poly(ctx, [(-14, -46), (4, -46), (-46, 46), (-64, 46)], (1, 1, 1), a=0.12)
    ctx.restore()
    rrect(ctx, -160, -52, 320, 104, 6); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()
    poly(ctx, [(128, -208), (134, -196), (146, -190), (134, -184), (128, -172), (122, -184), (110, -190), (122, -196)],
         (1, 1, 1), hexc('#b9c2cc'), 1.5)
    ctx.restore()
