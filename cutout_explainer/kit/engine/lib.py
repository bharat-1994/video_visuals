"""Cut-out puppet animation engine (cairo). 1280x720 @30fps.
Style: flat vector, round heads, dot eyes, swap-set brows/mouths, rubber-hose limbs,
handwritten captions (Caveat Brush), pop-in with overshoot, smoke puffs, camera push/pull."""
import cairo, math, random

W, H, FPS = 1280, 720, 30
FONT = "Caveat Brush"
INK = (0.08, 0.08, 0.1)
SKIN = (0.96, 0.84, 0.70)
SKIN_LINE = (0.55, 0.40, 0.30)

def hexc(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))

# ---------------- easing / timing ----------------
def clamp(x, a=0, b=1): return max(a, min(b, x))
def lerp(a, b, t): return a + (b - a) * t
def ease_io(t): t = clamp(t); return t*t*(3-2*t)
def ease_out(t): t = clamp(t); return 1-(1-t)**3
def back(t, s=1.9):
    t = clamp(t) - 1; return t*t*((s+1)*t + s) + 1
def pop(t, start, dur=0.35):
    """scale factor for pop-in: 0 before start, overshoot to 1."""
    if t < start: return 0.0
    return back((t-start)/dur)

# ---------------- primitives ----------------
def fill(ctx, c, a=1):
    ctx.set_source_rgba(*c, a) if len(c) == 3 else ctx.set_source_rgba(*c); ctx.fill()
def rrect(ctx, x, y, w, h, r):
    r = min(r, w/2, h/2)
    ctx.new_sub_path()
    ctx.arc(x+w-r, y+r, r, -math.pi/2, 0); ctx.arc(x+w-r, y+h-r, r, 0, math.pi/2)
    ctx.arc(x+r, y+h-r, r, math.pi/2, math.pi); ctx.arc(x+r, y+r, r, math.pi, 1.5*math.pi)
    ctx.close_path()
def box(ctx, x, y, w, h, c, r=0, line=None, lw=3):
    rrect(ctx, x, y, w, h, r); ctx.set_source_rgb(*c)
    if line: ctx.fill_preserve(); ctx.set_source_rgb(*line); ctx.set_line_width(lw); ctx.stroke()
    else: ctx.fill()
def circle(ctx, x, y, r, c, line=None, lw=3, a=1):
    ctx.new_sub_path(); ctx.arc(x, y, r, 0, 2*math.pi); ctx.set_source_rgba(*c, a)
    if line: ctx.fill_preserve(); ctx.set_source_rgb(*line); ctx.set_line_width(lw); ctx.stroke()
    else: ctx.fill()
def ellipse(ctx, x, y, rx, ry, c, a=1):
    ctx.save(); ctx.translate(x, y); ctx.scale(rx, ry); ctx.arc(0, 0, 1, 0, 2*math.pi); ctx.restore()
    ctx.set_source_rgba(*c, a); ctx.fill()
def poly(ctx, pts, c, line=None, lw=3, a=1):
    ctx.move_to(*pts[0]); [ctx.line_to(*p) for p in pts[1:]]; ctx.close_path()
    ctx.set_source_rgba(*c, a)
    if line: ctx.fill_preserve(); ctx.set_source_rgb(*line); ctx.set_line_width(lw); ctx.stroke()
    else: ctx.fill()
def line(ctx, pts, c=INK, lw=6, a=1):
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(*pts[0]); [ctx.line_to(*p) for p in pts[1:]]
    ctx.set_source_rgba(*c, a); ctx.set_line_width(lw); ctx.stroke()
def hose(ctx, p0, p1, bend=0.25, lw=9, c=INK):
    """rubber-hose limb: curved stroke from p0 to p1; bend>0 bows to the right of travel."""
    mx, my = (p0[0]+p1[0])/2, (p0[1]+p1[1])/2
    dx, dy = p1[0]-p0[0], p1[1]-p0[1]
    cx, cy = mx - dy*bend, my + dx*bend
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(*p0); ctx.curve_to(lerp(p0[0], cx, .66), lerp(p0[1], cy, .66), lerp(p1[0], cx, .66), lerp(p1[1], cy, .66), *p1)
    ctx.set_source_rgb(*c); ctx.set_line_width(lw); ctx.stroke()

def text(ctx, s, x, y, size=48, c=(1, 1, 1), anchor="c", reveal=1.0, rot=0, outline=None):
    """handwritten text; reveal 0..1 = typewriter."""
    n = int(round(len(s)*clamp(reveal)))
    s2 = s[:n]
    ctx.save(); ctx.select_font_face(FONT); ctx.set_font_size(size)
    full = ctx.text_extents(s)
    ox = {"c": -full.width/2, "l": 0, "r": -full.width}[anchor]
    ctx.translate(x, y); ctx.rotate(rot); ctx.move_to(ox, full.height/2 - 4)
    ctx.text_path(s2)
    if outline: ctx.set_source_rgb(*outline); ctx.set_line_width(size/8); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
    ctx.set_source_rgb(*c); ctx.fill(); ctx.restore()
    return full.width

def dialogue(ctx, s, x, y, to, size=40, reveal=1.0, c=(1, 1, 1), ink=INK):
    """reference style: white handwritten line, dark outline, tiny tick pointing at speaker mouth."""
    lines = s.split("\n")
    for i, l in enumerate(lines):
        text(ctx, l, x, y + i*size*1.05, size, c, reveal=reveal*1.15, outline=ink)
    # tick
    tx, ty = to
    ax, ay = lerp(x, tx, .78), lerp(y, ty, .78)
    bx, by = lerp(x, tx, .92), lerp(y, ty, .92)
    if reveal > 0.05:
        line(ctx, [(ax, ay), (bx, by)], ink, 9); line(ctx, [(ax, ay), (bx, by)], (1, 1, 1), 4)

def smoke(ctx, x, y, t, size=60, seed=1):
    """puff cloud: t in 0..1 lifetime."""
    if t <= 0 or t >= 1: return
    rnd = random.Random(seed)
    a = 1 - ease_io((t-.4)/.6) if t > .4 else 1
    for i in range(9):
        ang = rnd.uniform(0, 2*math.pi); d = rnd.uniform(.2, .8)*size*ease_out(t*1.6)
        r = size*rnd.uniform(.28, .5)*(0.4 + ease_out(t*2))
        cx, cy = x+math.cos(ang)*d, y+math.sin(ang)*d*.7
        circle(ctx, cx, cy, r, (0.75, 0.75, 0.78), a=a)
        circle(ctx, cx-r*.12, cy-r*.12, r*.85, (1, 1, 1), a=a)

def popped(ctx, t, start, x, y, draw, dur=0.35, puff=True, seed=3):
    """draw(ctx) around origin, scaled in with overshoot at time start, with smoke puff."""
    s = pop(t, start, dur)
    if puff: smoke(ctx, x, y, (t-start)/0.7, 70, seed)
    if s <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s); draw(ctx); ctx.restore()

# ---------------- backgrounds ----------------
def bg_flat(ctx, c):
    ctx.set_source_rgb(*c); ctx.paint()
def bg_spotlight(ctx, base=(0.13, 0.13, 0.15), cx=W/2, floor_y=620):
    ctx.set_source_rgb(*base); ctx.paint()
    g = cairo.LinearGradient(0, 0, 0, floor_y)
    poly(ctx, [(cx-90, -10), (cx+90, -10), (cx+330, floor_y), (cx-330, floor_y)], (1, 1, 1), a=0)
    ctx.move_to(cx-90, -10); ctx.line_to(cx+90, -10); ctx.line_to(cx+330, floor_y); ctx.line_to(cx-330, floor_y); ctx.close_path()
    g.add_color_stop_rgba(0, 1, 1, 1, .16); g.add_color_stop_rgba(1, 1, 1, 1, .05); ctx.set_source(g); ctx.fill()
    ellipse(ctx, cx, floor_y, 330, 46, (1, 1, 1), a=.12)
def bg_sky_ground(ctx, sky=hexc('#9fd8f0'), ground=hexc('#7cc06a'), horizon=520):
    ctx.set_source_rgb(*sky); ctx.paint(); box(ctx, 0, horizon, W, H-horizon, ground)
    for (x, y, s) in [(180, 110, 1), (900, 80, 1.3), (1150, 170, .8)]:
        for dx, r in [(-40, 30), (0, 42), (40, 32)]:
            circle(ctx, x+dx*s, y, r*s, (1, 1, 1))
def bg_sunset(ctx):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc('#e2675b')); g.add_color_stop_rgb(.55, *hexc('#f2a65e')); g.add_color_stop_rgb(1, *hexc('#f6c77d'))
    ctx.set_source(g); ctx.paint()
def bg_room(ctx, wall=hexc('#e9e4d8'), floor=hexc('#b98a5e'), floor_y=560):
    ctx.set_source_rgb(*wall); ctx.paint(); box(ctx, 0, floor_y, W, H-floor_y, floor)
    line(ctx, [(0, floor_y), (W, floor_y)], (0, 0, 0), 3, .25)
def city_window(ctx, x, y, w, h, night=False):
    sky = hexc('#22305a') if night else hexc('#bfe6f5')
    box(ctx, x-10, y-10, w+20, h+20, hexc('#6d7480'), 6)
    box(ctx, x, y, w, h, sky)
    ctx.save(); rrect(ctx, x, y, w, h, 0); ctx.clip()
    rnd = random.Random(7); bx = x
    while bx < x+w:
        bw = rnd.randint(50, 110); bh = rnd.randint(int(h*.35), int(h*.9))
        col = hexc('#4a5578') if night else rnd.choice([hexc('#8fb8cf'), hexc('#a9c8d8'), hexc('#7aa3bd')])
        box(ctx, bx, y+h-bh, bw-8, bh, col)
        for wy in range(int(y+h-bh+12), int(y+h), 22):
            for wx in range(int(bx+8), int(bx+bw-16), 18):
                box(ctx, wx, wy, 9, 11, hexc('#f7d774') if (night and rnd.random() < .5) else ((1, 1, 1) if not night else hexc('#38406a')))
        bx += bw
    ctx.restore()
    line(ctx, [(x+w/2, y), (x+w/2, y+h)], hexc('#6d7480'), 10)

# ---------------- camera ----------------
def camera(ctx, zoom=1.0, cx=W/2, cy=H/2, shake=0.0, t=0):
    """apply camera: zoom about (cx,cy)."""
    sx = math.sin(t*61)*shake; sy = math.cos(t*53)*shake
    ctx.translate(W/2+sx, H/2+sy); ctx.scale(zoom, zoom); ctx.translate(-cx, -cy)

# ---------------- puppet ----------------
EXPR = {  # brow (inner_dy, outer_dy, tilt) , eyes, idle mouth
    "neutral":    dict(brow=(0, 0), eyes="dot", mouth="line"),
    "happy":      dict(brow=(-4, -4), eyes="dot", mouth="smile"),
    "sad":        dict(brow=(-10, 6), eyes="dot", mouth="frown"),
    "angry":      dict(brow=(12, -8), eyes="dot", mouth="frown"),
    "worried":    dict(brow=(-12, 4), eyes="dot", mouth="wobble"),
    "shocked":    dict(brow=(-16, -16), eyes="wide", mouth="o"),
    "smug":       dict(brow=(4, -2), eyes="half", mouth="smirk"),
    "tired":      dict(brow=(-2, 6), eyes="half", mouth="line"),
    "determined": dict(brow=(9, -3), eyes="dot", mouth="line"),
}
VISEMES = ["o_small", "open", "wide", "line", "open", "ee", "o_small", "open"]

def smooth(ctx, pts, start=True):
    """Catmull-Rom spline through pts (continues current path unless start)."""
    if start: ctx.move_to(*pts[0])
    for i in range(len(pts)-1):
        p0 = pts[max(i-1, 0)]; p1 = pts[i]; p2 = pts[i+1]; p3 = pts[min(i+2, len(pts)-1)]
        ctx.curve_to(p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6, p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6, *p2)

def head_path(ctx, hx, hy, R, jaw=0.0):
    k = 0.552; cy = R*(1+0.12*jaw)
    ctx.new_path(); ctx.move_to(hx-R, hy)
    ctx.curve_to(hx-R, hy-k*R, hx-k*R, hy-R, hx, hy-R); ctx.curve_to(hx+k*R, hy-R, hx+R, hy-k*R, hx+R, hy)
    ctx.curve_to(hx+R, hy+(k+0.3*jaw)*R, hx+(k+0.35*jaw)*R, hy+cy, hx, hy+cy)
    ctx.curve_to(hx-(k+0.35*jaw)*R, hy+cy, hx-R, hy+(k+0.3*jaw)*R, hx-R, hy); ctx.close_path()

# hair: (top height, outline pts of fringe edge from RIGHT temple to LEFT temple, in R units; y up negative)
HAIR = {
  "short":  (1.30, [(0.99,-0.05),(0.85,-0.38),(0.55,-0.5),(0.2,-0.42),(-0.08,-0.66),(-0.45,-0.5),(-0.8,-0.42),(-0.99,-0.05)]),
  "fringe": (1.28, [(0.99,-0.02),(0.9,-0.3),(0.6,-0.36),(0.3,-0.32),(0.0,-0.38),(-0.3,-0.33),(-0.6,-0.37),(-0.9,-0.3),(-0.99,-0.02)]),
  "part":   (1.42, [(0.99,-0.12),(0.9,-0.42),(0.6,-0.52),(0.25,-0.5),(-0.05,-0.62),(-0.35,-0.78),(-0.62,-0.7),(-0.86,-0.45),(-0.99,-0.12)]),
  "wavy":   (1.40, [(0.99,0.05),(0.9,-0.35),(0.55,-0.46),(0.25,-0.56),(-0.1,-0.5),(-0.45,-0.58),(-0.8,-0.4),(-0.99,0.05)]),
  "slick":  (1.18, [(0.99,-0.15),(0.8,-0.6),(0.4,-0.74),(0.0,-0.76),(-0.4,-0.74),(-0.8,-0.6),(-0.99,-0.15)]),
}
def draw_hair(ctx, hx, hy, R, style, hc, f=0.0):
    top, fr = HAIR[style]
    sh = f*0.18
    P = lambda x, y: (hx + (x + sh*(1-abs(x)))*R, hy + y*R)
    ctx.new_path()
    # outer cap: left temple -> over top -> right temple
    if style == "wavy":
        outer = [(-0.99,0.05),(-1.1,-0.5),(-0.95,-0.95),(-0.6,-1.25),(-0.2,-1.38),(0.2,-1.36),(0.6,-1.24),(0.95,-0.95),(1.1,-0.5),(0.99,0.05)]
    else:
        outer = [(-0.99,fr[-1][1]),(-1.07,-0.6),(-0.8,-1.08),(-0.3,-top),(0.25,-top+0.02),(0.75,-1.12),(1.06,-0.6),(0.99,fr[0][1])]
    smooth(ctx, [P(*p) for p in outer])
    smooth(ctx, [P(*p) for p in fr], start=False)
    ctx.close_path(); ctx.set_source_rgb(*hc); ctx.fill()
    if style == "wavy":
        for x in (-0.7, -0.25, 0.2, 0.65):
            circle(ctx, *P(x, -1.22 + abs(x)*0.18), R*0.2, hc)
    if style == "part":  # part line + lighter swoop strand
        smooth(ctx, [P(-0.42, -1.3), P(-0.38, -1.0), P(-0.32, -0.8)])
        ctx.set_source_rgba(1, 1, 1, .18); ctx.set_line_width(3); ctx.stroke()
        smooth(ctx, [P(-0.2, -1.2), P(0.25, -1.05), P(0.7, -0.75)])
        ctx.set_source_rgba(1, 1, 1, .14); ctx.set_line_width(4); ctx.stroke()

_WARNED = set()

class Puppet:
    def __init__(self, hair="short", hair_c=hexc('#4b2e1c'), shirt=(1, 1, 1), jacket=None, tie=None,
                 skin=SKIN, scale=1.0, glasses=False, mustache=False, kid=False, collar=True, seed=0,
                 jaw=0.0, nose=False, brow_w=6):
        self.__dict__.update(locals()); del self.__dict__['self']

    # pose: dict of arm targets in body-local units (relative to shoulder), e.g. 'L':(dx,dy)
    def draw(self, ctx, x, y, t, expr="neutral", talking=False, facing=0.0, framing="medium",
             armL=(-30, 120), armR=(30, 120), legs=True, walk=0.0, blink_seed=0, look=0.0, mouth_override=None, view="front", cross=False):
        """x,y = base of torso (waist) in scene coords. facing: -1 left .. 0 front .. 1 right.
        armL/armR: hand position relative to that shoulder (px at scale 1)."""
        s = self.scale * (0.82 if self.kid else 1.0)
        bob = math.sin(t*2.4 + blink_seed)*2.5 + (abs(math.sin(walk*math.pi*2))*-6 if walk else 0)
        ctx.save(); ctx.translate(x, y + bob); ctx.scale(s, s)
        R = 88 if not self.kid else 92            # head radius (kids: bigger head ratio)
        tw, th = (150, 190) if not self.kid else (130, 150)
        # legs
        if legs:
            ph = walk*math.pi*2
            for side, off in ((-1, 0), (1, math.pi)):
                sw = math.sin(ph+off)*28 if walk else 0
                hip = (side*28, -6)
                foot = (side*34 + sw, 150)
                hose(ctx, hip, foot, 0.06*side, 10)
                line(ctx, [foot, (foot[0]+ (18 if facing >= 0 else -18) * (1 if abs(facing) > .2 else side), foot[1])], INK, 10)
        # rig constraint: hands may not cross the body midline unless cross=True
        if not cross:
            lim = tw/2 + 10
            nL = (min(armL[0], lim), armL[1]); nR = (max(armR[0], -lim), armR[1])
            for side, a, b in (("armL", armL, nL), ("armR", armR, nR)):
                key = (id(self), side)
                if abs(a[0]-b[0]) > 2 and key not in _WARNED:
                    _WARNED.add(key)
                    print(f"[rig] {side} x={a[0]:.0f} would cross the body midline; clamped to {b[0]:.0f}. "
                          f"Use info['handL'/'handR'] for where the hand really is, or pass cross=True.")
            armL, armR = nL, nR
        if view == "back": self._arms(ctx, tw, th, armL, armR)   # behind torso
        elif facing >= 0.6: self._arms(ctx, tw, th, armL, None)  # far arm behind torso in side view
        elif facing <= -0.6: self._arms(ctx, tw, th, None, armR)
        # torso
        body_c = self.jacket or self.shirt
        ctx.move_to(-tw/2+12, -th); ctx.curve_to(-tw/2-6, -th+40, -tw/2-4, -30, -tw/2+6, 0)
        ctx.line_to(tw/2-6, 0); ctx.curve_to(tw/2+4, -30, tw/2+6, -th+40, tw/2-12, -th); ctx.close_path()
        ctx.set_source_rgb(*body_c); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(4); ctx.stroke()
        fx = facing*22
        if view == "back":
            line(ctx, [(-tw/2+14, -th+40), (0, -th+52), (tw/2-14, -th+40)], INK, 2.5, .45)
            fx = None
        if fx is None: pass
        elif self.jacket:  # shirt V + tie
            poly(ctx, [(-34+fx, -th+2), (34+fx, -th+2), (fx, -th+95)], self.shirt, INK, 3)
            if self.tie: poly(ctx, [(-9+fx, -th+20), (9+fx, -th+20), (12+fx, -th+90), (fx, -th+104), (-12+fx, -th+90)], self.tie, INK, 2)
            line(ctx, [(fx, -th+100), (fx, -12)], INK, 3, .5)
        elif self.collar:
            poly(ctx, [(-40+fx, -th+2), (fx-2, -th+30), (-22+fx, -th+48)], self.shirt, INK, 3)
            poly(ctx, [(40+fx, -th+2), (fx+2, -th+30), (22+fx, -th+48)], self.shirt, INK, 3)
            line(ctx, [(fx, -th+30), (fx, -10)], INK, 2.5, .55)
            for by in range(-th+60, -10, 34): circle(ctx, fx+7, by, 3, INK, a=.6)
            box(ctx, 22+fx*.6, -th+70, 30, 30, self.shirt, 3, INK, 2.5)  # pocket
        # head
        hy = -th - R*0.72
        hx = facing*10
        if view == "back": self._back_head(ctx, hx, hy, R)
        else: self._head(ctx, hx, hy, R, t, expr, talking, facing, blink_seed, look, mouth_override)
        if view != "back":
            self._arms(ctx, tw, th, None if facing >= 0.6 else armL, None if facing <= -0.6 else armR)
        ctx.restore()
        return dict(head=(x + (hx)*s, y + bob + hy*s), R=R*s,
                    handL=(x + (-(tw/2-10)+armL[0])*s, y+bob+(-th+34+armL[1])*s),
                    handR=(x + ((tw/2-10)+armR[0])*s, y+bob+(-th+34+armR[1])*s))

    def _arms(self, ctx, tw, th, armL, armR):
        for side, tgt in ((-1, armL), (1, armR)):
            if tgt is None: continue
            sh = (side*(tw/2-10), -th+34)
            hand = (sh[0]+tgt[0], sh[1]+tgt[1])
            hose(ctx, sh, hand, -0.22*side if tgt[1] > 0 else 0.22*side, 10)
            circle(ctx, hand[0], hand[1], 6.5, INK)

    def _back_head(self, ctx, hx, hy, R):
        for sd in (-1, 1): ellipse(ctx, hx+sd*R*0.98, hy+R*0.08, 12, 18, tuple(c*.93 for c in self.skin))
        head_path(ctx, hx, hy, R, self.jaw); ctx.set_source_rgb(*self.skin); ctx.fill_preserve()
        ctx.set_source_rgb(*SKIN_LINE); ctx.set_line_width(3); ctx.stroke()
        if self.hair == "bald":
            ctx.save(); head_path(ctx, hx, hy, R, self.jaw); ctx.clip()
            box(ctx, hx-R, hy+R*0.05, 2*R, R*0.35, self.hair_c); ctx.restore(); return
        top = HAIR.get(self.hair, HAIR["short"])[0]
        ctx.new_path()
        smooth(ctx, [(hx-R*1.02, hy+R*0.45), (hx-R*1.08, hy-R*0.4), (hx-R*0.6, hy-R*1.12), (hx, hy-R*top), (hx+R*0.6, hy-R*1.12), (hx+R*1.08, hy-R*0.4), (hx+R*1.02, hy+R*0.45)])
        smooth(ctx, [(hx+R*1.02, hy+R*0.45), (hx+R*0.5, hy+R*0.55), (hx, hy+R*0.62), (hx-R*0.5, hy+R*0.55), (hx-R*1.02, hy+R*0.45)], start=False)
        ctx.close_path(); ctx.set_source_rgb(*self.hair_c); ctx.fill()
        if self.hair == "wavy":
            for x in (-0.7, -0.25, 0.2, 0.65): circle(ctx, hx+x*R, hy-R*(1.22-abs(x)*0.18), R*0.2, self.hair_c)

    def _head(self, ctx, hx, hy, R, t, expr, talking, facing, seed, look, mouth_override):
        E = EXPR.get(expr, EXPR["neutral"])
        f = facing
        # back hair
        if self.hair == "long":
            rrect(ctx, hx-R*1.05, hy-R*0.6, R*2.1, R*1.75, R*0.5); fill(ctx, self.hair_c)
        head_path(ctx, hx, hy, R, self.jaw); ctx.set_source_rgb(*self.skin); ctx.fill_preserve()
        ctx.set_source_rgb(*SKIN_LINE); ctx.set_line_width(3); ctx.stroke()
        # ear
        if abs(f) > .3: ellipse(ctx, hx - f*R*0.78, hy+8, 11, 16, tuple(c*.93 for c in self.skin))
        # hair
        hc = self.hair_c
        if self.hair in HAIR:
            draw_hair(ctx, hx, hy, R, self.hair, hc, f)
        elif self.hair == "bald":
            [ellipse(ctx, hx+sd*R*.86, hy-R*.05, R*.13, R*.28, hc) for sd in (-1, 1)]
        # face features
        fx = hx + f*R*(0.30 + 0.22*max(0, abs(f)-0.4)) + look*6
        ey = hy - R*0.02
        sp = R*0.36*(1-abs(f)*0.25)
        # blink
        rnd = random.Random(seed)
        period = 2.6 + rnd.random()*1.5
        blink = ((t + rnd.random()*period) % period) < 0.11
        for side in (-1, 1):
            ex = fx + side*sp
            if blink or E["eyes"] == "closed":
                line(ctx, [(ex-9, ey+2), (ex+9, ey+2)], INK, 4)
            elif E["eyes"] == "wide":
                circle(ctx, ex, ey, 14, (1, 1, 1), INK, 3); circle(ctx, ex+f*3, ey, 6, INK)
            elif E["eyes"] == "half":
                ellipse(ctx, ex, ey+3, 7, 7, INK); line(ctx, [(ex-11, ey-2), (ex+11, ey-2)], self.skin, 7)
                line(ctx, [(ex-11, ey-1), (ex+11, ey-1)], INK, 3.5)
            else:
                ellipse(ctx, ex, ey, 7, 9.5, INK)
            # brows
            inner, outer = E["brow"]
            ix, ox = ex - side*12, ex + side*12
            by = ey - 28
            line(ctx, [(ix, by + inner*0.9), (ox, by + outer*0.9)], hc if self.hair != "bald" else INK, self.brow_w)
        if self.glasses:
            for side in (-1, 1): circle(ctx, fx+side*sp, ey, 19, (1, 1, 1), INK, 3.5, a=.25)
            line(ctx, [(fx-sp+19, ey), (fx+sp-19, ey)], INK, 3.5)
        # nose hint
        my = hy + R*(0.42 + self.jaw*0.07)
        if self.nose:
            nx = fx + f*R*0.10
            ctx.move_to(nx + 2, hy + R*0.10); ctx.curve_to(nx + 6 + f*6, hy + R*0.22, nx + 2 + f*4, hy + R*0.27, nx - 5, hy + R*0.25)
            ctx.set_source_rgb(*SKIN_LINE); ctx.set_line_width(3.5); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.stroke()
        if self.mustache:
            ctx.move_to(fx-34, my-2); ctx.curve_to(fx-20, my-22, fx-4, my-16, fx, my-10)
            ctx.curve_to(fx+4, my-16, fx+20, my-22, fx+34, my-2); ctx.curve_to(fx+16, my-8, fx+4, my-4, fx, my-6)
            ctx.curve_to(fx-4, my-4, fx-16, my-8, fx-34, my-2); fill(ctx, hc)
        # mouth
        m = mouth_override or E["mouth"]
        if talking:
            m = VISEMES[int(t*FPS/3 + seed) % len(VISEMES)]
            if expr in ("happy", "smug") and m == "line": m = "smile"
        self._mouth(ctx, fx, my, m, f)

    def _mouth(self, ctx, x, y, m, f):
        red = hexc('#c9504f')
        if m == "line": line(ctx, [(x-12, y), (x+12, y)], INK, 4)
        elif m == "smile":
            ctx.arc(x, y-10, 18, math.radians(30), math.radians(150)); ctx.set_source_rgb(*INK); ctx.set_line_width(4); ctx.stroke()
        elif m == "frown":
            ctx.arc(x, y+14, 16, math.radians(215), math.radians(325)); ctx.set_source_rgb(*INK); ctx.set_line_width(4); ctx.stroke()
        elif m == "smirk":
            ctx.move_to(x-12, y+2); ctx.curve_to(x, y+6, x+10, y+2, x+16, y-6); ctx.set_source_rgb(*INK); ctx.set_line_width(4); ctx.stroke()
        elif m == "wobble":
            line(ctx, [(x-14, y+2), (x-7, y-2), (x, y+2), (x+7, y-2), (x+14, y+2)], INK, 3.5)
        elif m in ("o", "o_small"):
            r = 10 if m == "o" else 7
            ellipse(ctx, x, y, r, r*1.25, INK); ellipse(ctx, x, y+r*.5, r*.55, r*.4, red)
        elif m == "open":
            ctx.move_to(x-15, y-5); ctx.line_to(x+15, y-5); ctx.curve_to(x+14, y+16, x-14, y+16, x-15, y-5)
            fill(ctx, INK); ellipse(ctx, x, y+7, 8, 4, red)
        elif m == "wide":
            ctx.move_to(x-19, y-6); ctx.line_to(x+19, y-6); ctx.curve_to(x+17, y+22, x-17, y+22, x-19, y-6)
            fill(ctx, INK); box(ctx, x-13, y-5, 26, 5, (1, 1, 1)); ellipse(ctx, x, y+11, 10, 5, red)
        elif m == "ee":
            box(ctx, x-17, y-6, 34, 12, INK, 6); box(ctx, x-13, y-4, 26, 4, (1, 1, 1))

# ---------------- common props ----------------
def money_bag(ctx, x, y, s=1.0, label="$"):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(-22, -62); ctx.curve_to(-70, -10, -66, 50, 0, 50); ctx.curve_to(66, 50, 70, -10, 22, -62); ctx.close_path()
    ctx.set_source_rgb(*hexc('#e2a35a')); ctx.fill_preserve(); ctx.set_source_rgb(*hexc('#8a5a2b')); ctx.set_line_width(3); ctx.stroke()
    poly(ctx, [(-24, -62), (24, -62), (34, -84), (12, -74), (0, -88), (-12, -74), (-34, -84)], hexc('#d0904a'), hexc('#8a5a2b'), 3)
    line(ctx, [(-26, -60), (26, -60)], hexc('#6b3f1d'), 6)
    text(ctx, label, 0, 6, 64, hexc('#2e9e4f'))
    ctx.restore()
def bill(ctx, x, y, rot=0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    box(ctx, -40, -20, 80, 40, hexc('#7fc77a'), 4, hexc('#3f8a45'), 3); circle(ctx, 0, 0, 11, hexc('#5fae5c'))
    text(ctx, "$", 0, 0, 22, hexc('#2c6e33')); ctx.restore()
def crt(ctx, x, y, s=1.0, screen=hexc('#1d2b22'), draw_screen=None, t=0):
    """CRT monitor sitting with base at (x,y)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    box(ctx, -40, -20, 80, 20, hexc('#cfcab8'), 4, INK, 3)
    box(ctx, -110, -190, 220, 170, hexc('#e4dfcc'), 14, INK, 4)
    box(ctx, -92, -174, 184, 132, screen, 10)
    if draw_screen:
        ctx.save(); rrect(ctx, -92, -174, 184, 132, 10); ctx.clip(); ctx.translate(-92, -174); draw_screen(ctx, t); ctx.restore()
    circle(ctx, 88, -32, 5, hexc('#5fd35f'))
    ctx.restore()
def desk(ctx, x, y, w=420, c=hexc('#a8703f')):
    box(ctx, x-w/2, y, w, 26, c, 4, INK, 3); box(ctx, x-w/2+20, y+26, 22, 140, tuple(v*.85 for v in c), 0, INK, 3)
    box(ctx, x+w/2-42, y+26, 22, 140, tuple(v*.85 for v in c), 0, INK, 3)
def paper(ctx, x, y, w, h, rot=0, c=(1, 1, 1), lines_=4, label=None, size=30, ink=INK):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    box(ctx, -w/2, -h/2, w, h, c, 4, INK, 3)
    for i in range(lines_):
        ly = -h/2 + 22 + i*(h-30)/max(lines_, 1)
        if label and i == 0: continue
        line(ctx, [(-w/2+16, ly + (20 if label else 0)), (w/2-16 - (i % 2)*30, ly + (20 if label else 0))], (0.6, 0.6, 0.6), 3)
    if label: text(ctx, label, 0, -h/2+28, size, ink)
    ctx.restore()

# ---------------- render ----------------
def render(scenes, out, preview_every=None, sheet=None):
    """scenes: list of (dur, fn(ctx,t,dur)). Streams raw frames to ffmpeg."""
    import subprocess, os
    S = float(os.environ.get("RENDER_SCALE", "1"))        # 1.5 -> true 1920x1080 (vector drawing, no upscaling)
    RW, RH = int(round(W*S)), int(round(H*S))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{RW}x{RH}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", out],
                         stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, RW, RH)
    shots = []
    for si, (dur, fn) in enumerate(scenes):
        n = int(round(dur*FPS))
        for i in range(n):
            ctx = cairo.Context(surf); ctx.set_source_rgb(1, 1, 1); ctx.paint(); ctx.scale(S, S)
            ctx.save(); fn(ctx, i/FPS, dur); ctx.restore()
            surf.flush(); p.stdin.write(bytes(surf.get_data()))
            if sheet is not None and i == int(n*0.7): surf.write_to_png(f"{sheet}/shot{si+1:02d}.png")
    p.stdin.close(); p.wait()

# ---------------- shared cast (use these; never redefine looks) ----------------
def cast(who, scale=1.0):
    C = {
        "elon_kid":   dict(kid=True, hair="fringe", hair_c=hexc('#b8894f'), shirt=(1, 1, 1), nose=True),
        "elon_teen":  dict(hair="part", hair_c=hexc('#7a5232'), shirt=hexc('#dfe9f2'), jaw=0.3, nose=True),
        "elon_adult": dict(hair="part", hair_c=hexc('#4a3222'), shirt=(1, 1, 1), jaw=0.6, nose=True, brow_w=7),
        "kimbal":     dict(hair="wavy", hair_c=hexc('#3a2a20'), shirt=hexc('#cfe0c8'), jaw=0.35, nose=True),
        "bully":      dict(kid=True, hair="short", hair_c=hexc('#c8862e'), shirt=hexc('#d9534f'), collar=False, jaw=0.4),
        "editor":     dict(hair="bald", hair_c=hexc('#9a9a9a'), shirt=(1, 1, 1), glasses=True, mustache=True, nose=True, jaw=0.2),
        "banker":     dict(hair="slick", hair_c=hexc('#1e1e1e'), shirt=(1, 1, 1), jacket=hexc('#232b45'), tie=hexc('#b23a3a'), jaw=0.5, nose=True),
    }[who]
    return Puppet(scale=scale, seed=sum(map(ord, who)) % 97, **C)


# ---------------- pose presets (hand offsets from each shoulder; use instead of raw numbers) ----------------
POSES = {
    "down":       ((-25, 125), (25, 125)),
    "hips":       ((-45, 70), (45, 70)),
    "hold_front": ((50, 70), (-50, 70)),      # both hands meet in front of belly (holding a sign/book/check)
    "raise_both": ((-40, -130), (40, -130)),
    "wave_R":     ((-25, 125), (45, -120)),
    "point_R":    ((-25, 125), (150, 5)),
    "point_L":    ((-150, 5), (25, 125)),
    "phone_R":    ((-25, 125), (5, -105)),    # right hand at ear
    "think_R":    ((-25, 125), (-35, -55)),   # right hand to chin
    "shrug":      ((-70, -20), (70, -20)),
    "type_R":     ((80, 72), (120, 78)),      # side view facing right, both hands reach forward to a keyboard
    "type_L":     ((-120, 78), (-80, 72)),
    "carry_R":    ((-25, 125), (30, 135)),    # right hand low, carrying a bag/suitcase
}
def pose(name, other=None, t=1.0):
    """pose('wave_R') -> (armL, armR); pose(a, b, t) blends from a to b."""
    a = POSES[name]
    if other is None: return a
    b = POSES[other]; t = clamp(t)
    return tuple((lerp(a[i][0], b[i][0], t), lerp(a[i][1], b[i][1], t)) for i in range(2))
