"""Vietnam v2: custom shot functions (section 8) and fx layers (section 9).
CUSTOM2 registers into scene_v2.CUSTOM; FX2 into scene_v2.FX (via setup_v2)."""
import sys, os, math, random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "engine")))
from lib import *
import lib
from episodes.vietnam.assets import *
from episodes.vietnam.assets_ind import *
from episodes.vietnam.assets_pol import *
from episodes.vietnam.v2.assets_v2 import *

FX2 = {}

# ================= FX LAYERS (section 9; merged from _fx_draft.py) =================

# ---------------------------------------------------------------------------
# _fx_draft.py — the 11 continuous-motion fx layers allowed by REVISION_v2.md
# section 9 + UPDATE 2 (no decorative motion). Scratch draft: a lead engineer
# merges these into episodes/vietnam/v2/fx_v2.py (registry FX[NAME]).
#
# Contract: def f_NAME(ctx, t, dur, T, **kv)
#   called every frame AFTER the world, BEFORE text overlays, inside the
#   camera transform. t = seconds since layer start, dur = shot duration,
#   T(word) -> seconds (unused here: every layer starts on its own t=0).
# Rules honoured: <= 40 shapes/frame, deterministic (seeded random or index
# math only), no faces covered (face band y 200-560 / x 200-1100 avoided
# except where section 9 grants it: confetti/fireworks may fill the sky),
# top text band y<180 left clear except confetti/fireworks.
# ---------------------------------------------------------------------------

MARGIN = 100  # world-space bleed so full-frame tints still cover at zoom>1


def _num(v, d):
    try:
        return float(v)
    except (TypeError, ValueError):
        return d


def _tint(ctx, x, y, w, h, c, a):
    """flat alpha rectangle (box() has no alpha channel)."""
    if a <= 0.003:
        return
    ctx.rectangle(x, y, w, h)
    ctx.set_source_rgba(c[0], c[1], c[2], a)
    ctx.fill()


def _tw(ctx, s, size):
    """advance width of string s in the house font — used to tile the ticker."""
    ctx.save()
    ctx.select_font_face(FONT)
    ctx.set_font_size(size)
    ext = ctx.text_extents(s)
    ctx.restore()
    return ext.x_advance if ext.x_advance > 1 else len(s) * size * 0.5


# --------------------------------------------------------------- 1. motorbikes
# S16 / S90 / S142 bg hanoi_today — the street really is full of scooters.
_BIKE_COLS = ('#d9504f', '#3f7fbf', '#e8a13c', '#57a05e', '#7a6bb5')
_BIKE_LANES = ((596, 120, 1), (606, 96, -1), (588, 138, 1), (612, 108, -1), (600, 128, 1))


def _scooter(ctx, x, y, c, d):
    """one ~55px scooter at (x, wheel-line y), travel dir d=+1 right / -1 left.
    7 shapes: deck, windscreen, 2 wheels, rider torso, helmeted head, arm."""
    box(ctx, x - 20, y - 12, 40, 10, c, 4, INK, 2)                       # deck
    box(ctx, x + d * 15 - 3, y - 26, 6, 16, tuple(v * 0.78 for v in c))  # windscreen
    circle(ctx, x - 14, y, 5.5, hexc('#26262c'))                         # rear wheel
    circle(ctx, x + 15, y, 5.5, hexc('#26262c'))                         # front wheel
    box(ctx, x - d * 8 - 6, y - 30, 12, 17, (0.93, 0.90, 0.84), 4, INK, 2)  # rider torso
    circle(ctx, x - d * 8 + d * 2, y - 34, 5, hexc('#e8b98a'))            # rider head
    line(ctx, [(x - d * 2, y - 25), (x + d * 12, y - 17)], INK, 2.5)      # arm to bar


def f_motorbikes(ctx, t, dur, T, **kv):
    """stream of scooters crossing at ground level (~y600), seamless modulo loop."""
    y0 = _num(kv.get('y'), 600)
    span = W + 200
    for i, (ly, sp, d) in enumerate(_BIKE_LANES):
        u = (t * sp + 60 + i * 317) % span
        x = u - 100 if d > 0 else (W + 100) - u
        bob = math.sin(t * 9.0 + i * 1.3) * 1.2
        _scooter(ctx, x, y0 + (ly - 600) + bob, hexc(_BIKE_COLS[i]), d)
    # 5 scooters x 7 shapes = 35


# ---------------------------------------------------------------- rice_burst
# S56 harvest field — narration says output "exploded". One ballistic spray.
def f_rice_burst(ctx, t, dur, T, **kv):
    """~24 rice grains spray up from the heap (x=640,y=600 default, kv x/y
    override), burst starts at t=0, settles by ~1.2s, fades to calm by ~2.8s."""
    x = _num(kv.get('x'), 640)
    y = _num(kv.get('y'), 600)
    if t > 3.2:
        return
    rnd = random.Random(56)
    g = 980.0
    # dust ring only in the first 0.4s (the burst moment itself)
    if t < 0.4:
        r = 24 + 74 * ease_out(t / 0.4)
        circle(ctx, x, y - 4, r, hexc('#d9c08a'), a=0.32 * (1 - t / 0.4))
    for i in range(24):
        ang = -math.pi / 2 + rnd.uniform(-1.15, 1.15)
        v = rnd.uniform(210, 470)          # peak height kept below y~490 (no faces)
        vx, vy = math.cos(ang) * v, math.sin(ang) * v
        land = max(0.15, -2 * vy / g)
        tt = min(t, land)
        px = x + vx * tt
        py = y + vy * tt + 0.5 * g * tt * tt
        a = 1.0 if t < land else clamp(1.0 - (t - land) / 0.9)
        if a <= 0.01:
            continue
        rr = rnd.uniform(2.2, 3.4)
        circle(ctx, px, py, rr, hexc('#f5e6b8') if i % 2 else hexc('#e3c98a'), a=a)
    # 1 + 24 = 25 shapes


# --------------------------------------------------------------------- storm
# S106 port at night — "no longer safe", the metaphor shown literally.
def f_storm(ctx, t, dur, T, **kv):
    """rain slanted across the frame, one lightning flash (~t0.4, 2 white
    frames) and a dark tint that fades in over 1.4s and holds."""
    rnd = random.Random(106)
    for i in range(26):
        xi = rnd.uniform(-30, W + 30)
        sp = rnd.uniform(520, 720)
        ln = rnd.uniform(14, 26)
        off = rnd.uniform(0, 800)
        ry = ((t * sp + off) % (H + 90)) - 45
        line(ctx, [(xi, ry), (xi + 5, ry + ln)], (0.78, 0.85, 0.95), 2, a=0.30)
    _tint(ctx, -MARGIN, -MARGIN, W + 2 * MARGIN, H + 2 * MARGIN, (0.04, 0.06, 0.11),
          0.28 * clamp(t / 1.4))
    if 0.40 <= t < 0.434:                       # flash frame 1
        _tint(ctx, -MARGIN, -MARGIN, W + 2 * MARGIN, H + 2 * MARGIN, (1, 1, 1), 0.5)
        line(ctx, [(172, 30), (196, 108), (178, 116), (206, 188)], (1, 1, 1), 5, a=0.9)
    elif 0.467 <= t < 0.50:                     # flash frame 2
        _tint(ctx, -MARGIN, -MARGIN, W + 2 * MARGIN, H + 2 * MARGIN, (1, 1, 1), 0.28)
    # 26 lines + 1 tint + at most 1 tint + 1 bolt = <=29


# --------------------------------------------------------------- solder_sparks
# S132 assembly hall — narration says "soldering".
def f_solder_sparks(ctx, t, dur, T, **kv):
    """tiny radiating spark bursts at 3 bench stations along y~470, staggered
    short cycles. Bench-height only (never reaches the face band)."""
    y = _num(kv.get('y'), 470)
    stations = ((_num(kv.get('x1'), 340), y, 0.00, 0.55),
                (_num(kv.get('x2'), 640), y, 0.35, 0.70),
                (_num(kv.get('x3'), 980), y, 0.62, 0.60))
    for (sx, sy, ph, per) in stations:
        u = (t / per + ph) % 1.0
        if u >= 0.30:
            continue
        life = u / 0.30
        a = 1.0 - life
        reach = 4 + 18 * ease_out(life)
        for k in range(6):
            ang = k * math.pi / 3 + sx * 0.13 - life * 0.35   # splay droops as it dies
            ex = sx + math.cos(ang) * reach
            ey = sy + math.sin(ang) * reach * 0.8 - 4 * (1 - life)
            line(ctx, [(sx + math.cos(ang) * 2, sy + math.sin(ang) * 2), (ex, ey)],
                 hexc('#ffd76a'), 2.5, a=a)
        circle(ctx, sx, sy - 2, 3.0, (1, 1, 0.92), a=a)
    # worst case 3 x (6 lines + 1 dot) = 21


# ---------------------------------------------------------------- smoke_puffs
# S41 engine room — the engine "out of fuel" sputters.
def f_smoke_puffs(ctx, t, dur, T, **kv):
    """dark exhaust puffs rising from the RIGHT edge (~x1190, y300 default,
    kv x/y override) — stays in the right margin, clear of faces and text."""
    x = _num(kv.get('x'), 1190)
    y = _num(kv.get('y'), 300)
    cycle = 2.4
    for k in range(4):
        age = (t - k * 0.60) % cycle
        if age > 2.2:
            continue
        a = 0.42 * clamp(age * 5) * clamp(1.05 - age / 2.2)
        if a <= 0.01:
            continue
        yy = y - age * 52
        xx = max(x - age * 16, 1105) + math.sin(age * 2.4 + k) * 4
        r = 12 + 26 * age
        circle(ctx, xx, yy, r, hexc('#55565c'), a=a)
        circle(ctx, xx - r * 0.45, yy + r * 0.30, r * 0.65, hexc('#484a52'), a=a * 0.8)
        circle(ctx, xx + r * 0.40, yy - r * 0.30, r * 0.55, hexc('#6a6b74'), a=a * 0.7)
        circle(ctx, xx - r * 0.05, yy - r * 0.55, r * 0.45, hexc('#55565c'), a=a * 0.6)
    # worst case 4 x 4 = 16 shapes


# ------------------------------------------------------------------ fireworks
# S123 Hanoi today — "celebrated worldwide". Sky only.
def f_fireworks(ctx, t, dur, T, **kv):
    """3 warm bursts as expanding dot rings, staggered, centres kept at
    y<=155 so the ring (r<=115) never dips below y~260 into the face band."""
    bursts = ((300, 120, '#ffd35c', '#ff8a3d', 0.0),
              (760, 150, '#ff5f4f', '#ffce9e', 1.2),
              (1040, 105, '#ffe9a8', '#fff6e0', 2.4))
    cycle = 4.6
    for (bx, by, c1, c2, s0) in bursts:
        age = (t - s0) % cycle
        if age > 1.1:
            continue
        k = age / 1.1
        r = 115 * ease_out(k)
        a = 0.95 * clamp(1.05 - age / 1.1)
        rr = 4.0 * (1.0 - 0.5 * k)
        if age < 0.12:                     # ignition flash at the burst centre
            circle(ctx, bx, by, 5 + 8 * (1 - age / 0.12), (1, 1, 0.95), a=0.9)
        for d in range(10):
            ang = d * math.pi / 5 + s0
            circle(ctx, bx + math.cos(ang) * r, by + math.sin(ang) * r * 0.92,
                   rr, hexc(c1 if d % 2 else c2), a=a)
    # worst case 3 x 10 = 30 dots


# ------------------------------------------------------------------- confetti
# S110 trophy stage — "the biggest winner".
def f_confetti(ctx, t, dur, T, **kv):
    """26 small flat pieces falling from the top with gentle sin sway and
    spin. Pieces are <=12px so they never mask a face while crossing it."""
    rnd = random.Random(110)
    pal = ('#e94f4f', '#f2b13c', '#4f9ae9', '#57c06a', '#b06ae0', '#f7f1e3')
    for i in range(26):
        x0 = rnd.uniform(-10, W + 10)
        sp = rnd.uniform(80, 150)
        swf = rnd.uniform(0.9, 2.3)
        ph = rnd.uniform(0, 2 * math.pi)
        pw = rnd.uniform(6, 11)
        pd = rnd.uniform(4, 7)
        rot0 = rnd.uniform(0, math.pi)
        spin = rnd.uniform(-3.5, 3.5)
        c = hexc(rnd.choice(pal))
        y = ((t * sp + ph * 90) % (H + 60)) - 30
        xx = x0 + math.sin(t * swf + ph) * 18
        ctx.save()
        ctx.translate(xx, y)
        ctx.rotate(rot0 + t * spin)
        box(ctx, -pw / 2, -pd / 2, pw, pd, c)
        ctx.restore()
    # 26 shapes


# -------------------------------------------------------------- camera_flashes
# S66 embassy (1995 normalization) / S42 congress — press photo-op.
def f_camera_flashes(ctx, t, dur, T, **kv):
    """white bursts at 8 fixed press positions (all outside the face band,
    x<200 / x>1100 or below y560). Deterministic staggered phases; on any
    frame usually 0-1, never more than ~3 are active."""
    pos = ((80, 250), (150, 392), (66, 520), (1186, 242),
           (1102, 384), (1206, 512), (246, 604), (1036, 610))
    for i, (fx0, fy0) in enumerate(pos):
        per = 1.3 + (i % 3) * 0.45
        loc = (t + i * 0.37) % per
        if loc >= 0.14:
            continue
        on = 1.0 - loc / 0.14
        circle(ctx, fx0, fy0, 7 + 10 * on, (1, 1, 1), a=0.85 * on)
        circle(ctx, fx0, fy0, 3 + 5 * on, (1, 1, 0.9), a=0.95 * on)
        ll = 12 + 20 * on
        for k in range(4):
            ang = k * math.pi / 2 + i * 0.4
            line(ctx, [(fx0 + math.cos(ang) * 3, fy0 + math.sin(ang) * 3),
                       (fx0 + math.cos(ang) * ll, fy0 + math.sin(ang) * ll)],
                 (1, 1, 1), 2.5, a=0.75 * on)
    # worst case 3 active x 6 = 18


# ---------------------------------------------------------------------- ticker
# S104 newsroom — a real studio has a bottom ticker. Band y=600..634: below
# the headline zone (kv band= / y= override), clear of faces, and kept above
# the y>630 subtitle line (assets_v2 newsroom bg spec: "ticker band above
# y=630"); since assets_v2 does not exist yet the fx draws its own strip.
def f_ticker(ctx, t, dur, T, **kv):
    """dark strip with one seamless line of small caps scrolling right->left."""
    by = _num(kv.get('band', kv.get('y')), 600)
    bh = _num(kv.get('h'), 34)
    size = _num(kv.get('size'), 22)
    speed = _num(kv.get('speed'), 90)
    box(ctx, -MARGIN, by, W + 2 * MARGIN, bh, hexc('#0e1524'))
    line(ctx, [(0, by), (W, by)], hexc('#c9a24a'), 2)
    line(ctx, [(0, by + bh), (W, by + bh)], hexc('#c9a24a'), 2)
    tile = "MARKETS  \u2022  TRADE  \u2022  SUPPLY CHAINS  \u2022  " * 6
    wt = _tw(ctx, tile, size)
    s = (t * speed) % wt
    x = -s
    while x < W:
        text(ctx, tile, x, by + bh / 2, size, hexc('#f3ecd8'), anchor="l")
        x += wt
    # 1 strip + 2 rules + 2-3 text runs = <=6 draw ops


# ------------------------------------------------------------------ shift_crowd
# S111 foxconn campus — shift change, workers streaming to the gate.
def f_shift_crowd(ctx, t, dur, T, **kv):
    """12 tiny 2-tone workers (uniform tone + skin head, stroked legs)
    converge on the gate at x=640 (kv gate= override) along y=560..600 and
    disappear into it, re-emerging at the far edge. Floor level only."""
    gate = _num(kv.get('gate'), 640)
    u1, u2 = hexc('#2f6db5'), hexc('#52585f')
    sk = hexc('#e8b98a')
    n = 12
    for i in range(n):
        from_left = (i % 2 == 0)
        start = -30.0 if from_left else float(W + 30)
        sp = 0.15 + (i % 4) * 0.03
        pr = ((t * sp) + i / float(n)) % 1.0
        if pr > 0.96:
            continue                      # stepped through the gate
        x = lerp(start, gate, ease_io(pr))
        yy = 558 + (i % 3) * 13 + (i * 5) % 9 - math.sin(t * 7 + i) * 1.2
        sw = math.sin(t * 9 + i * 1.7) * 2.5
        col = u1 if (i % 2) else u2
        line(ctx, [(x - 2.5 + sw, yy + 11), (x, yy + 5), (x + 2.5 - sw, yy + 11)], INK, 2)
        line(ctx, [(x, yy + 5), (x, yy - 1)], col, 5)
        circle(ctx, x, yy - 4, 3, sk)
    # 12 x 3 = <=36


# ----------------------------------------------------------------------- sepia
# S145 paddy flashback — "the 20th century".
def f_sepia(ctx, t, dur, T, **kv):
    """flat warm sepia wash (35% alpha) + 4 flat vignette strips (no
    gradient) + per-frame deterministic specks/scratch that jitter with t.
    Runs before text, so title/caption contrast is preserved."""
    _tint(ctx, -MARGIN, -MARGIN, W + 2 * MARGIN, H + 2 * MARGIN, (0.55, 0.40, 0.17), 0.35)
    dk = (0.10, 0.07, 0.03)
    _tint(ctx, -MARGIN, -MARGIN, W + 2 * MARGIN, 46 + MARGIN, dk, 0.30)         # top
    _tint(ctx, -MARGIN, H - 46, W + 2 * MARGIN, 46 + MARGIN, dk, 0.30)          # bottom
    _tint(ctx, -MARGIN, 46, 54 + MARGIN, H - 92, dk, 0.30)                      # left
    _tint(ctx, W - 54, 46, 54 + MARGIN, H - 92, dk, 0.30)                       # right
    fidx = int(t * FPS)
    for i in range(5):
        rr = random.Random(fidx * 131 + i * 77)
        if rr.random() < 0.45:
            continue
        sx = rr.uniform(0, W)
        sy = rr.uniform(60, H - 60)
        ln = rr.uniform(3, 16)
        if rr.random() < 0.3:                      # hairline scratch
            line(ctx, [(sx, sy), (sx + rr.uniform(-2, 2), sy + ln)], (1, 1, 1), 1, a=0.12)
        else:                                      # dust speck
            box(ctx, sx, sy, 2, 2, (0.98, 0.95, 0.85), 0, None)
    # 5 tints + <=5 specks = <=10


FX2 = {
    "motorbikes": f_motorbikes,
    "rice_burst": f_rice_burst,
    "storm": f_storm,
    "solder_sparks": f_solder_sparks,
    "smoke_puffs": f_smoke_puffs,
    "fireworks": f_fireworks,
    "confetti": f_confetti,
    "camera_flashes": f_camera_flashes,
    "ticker": f_ticker,
    "shift_crowd": f_shift_crowd,
    "sepia": f_sepia,
}

# ================= CUSTOM SHOT FUNCTIONS (section 8; merged from _custom_draft.py) =================
"""v2 custom shot functions — DRAFT (REVISION_v2.md section 8, all 27 functions).
Scratch file: a lead engineer merges these into episodes/vietnam/v2/fx_v2.py and integration-tests them.
Module scope at merge time already contains: everything from engine/lib, episodes/vietnam/assets.py,
assets_ind.py, assets_pol.py, the v2 PROPS spec names, and v2cast. Do NOT import here.
Every function: def c_NAME(ctx, t, dur, T, **kv) registered in CUSTOM["NAME"] at the bottom.
"""

# ---------------- tiny helpers (underscore-private; no name clashes) ----------------
def _T(T, tok, default):
    """safe word resolve: T on a missing token -> default."""
    try:
        return T(tok)
    except Exception:
        return default

def _walk(pts, k):
    """partial polyline of pts up to arc-length fraction k (0..1)."""
    if k <= 0 or len(pts) < 2: return []
    segs = list(zip(pts[:-1], pts[1:])); ls = [math.dist(a, b) for a, b in segs]
    d = clamp(k) * sum(ls); path = [pts[0]]
    for (a, b), l in zip(segs, ls):
        if d >= l: path.append(b); d -= l
        else: path.append((lerp(a[0], b[0], d/l), lerp(a[1], b[1], d/l))); break
    return path

def _qp(p0, pc, p1, u):
    """point on quadratic bezier at u."""
    m = 1 - u
    return (m*m*p0[0] + 2*m*u*pc[0] + u*u*p1[0], m*m*p0[1] + 2*m*u*pc[1] + u*u*p1[1])

def _table(ctx, x, y, w, c=hexc('#a8703f')):
    """plain table strip: top at y (surface), legs down; nothing below y=630 if y<=530."""
    box(ctx, x - w/2, y, w, 18, c, 3, INK, 3)
    for sg in (-1, 1): box(ctx, x + sg*(w/2 - 34), y + 18, 16, 92, tuple(v*.85 for v in c), 0, INK, 2.5)

CHALKW = hexc('#f2f4ee')          # chalk white
GOLD, GOLD_D = hexc('#e9b949'), hexc('#c48f2c')
GLD_L = hexc('#f0c24a')

# ================= 1. zone2 (S04) =================
def c_zone2(ctx, t, dur, T, at="@70"):
    """S04: 10 people in the 1986 street; a grey rain cloud drifts over the left 7 (they turn sad);
    counter 0->70% pops on the word."""
    who = ("farmer", "mother", "kid")
    cx = 430 + 16*math.sin(t*0.55); cy = 195; drift = 9*math.sin(t*0.9)
    for dx, dy, r in [(-230, 4, 44), (-120, -14, 58), (10, -20, 62), (140, -8, 50), (235, 6, 38)]:
        circle(ctx, cx + dx + drift, cy + dy, r, hexc('#9aa0a8'))
    box(ctx, cx - 262 + drift, cy + 22, 530, 34, hexc('#9aa0a8'), 17)     # flat base unifies the blobs
    ellipse(ctx, cx - 70 + drift, cy - 30, 95, 16, hexc('#b3b7bd'))       # single lighter top tone
    ellipse(ctx, cx + drift, cy + 68, 275, 11, hexc('#676c74'), a=0.45)
    for i in range(12):                                    # rain lines under the cloud
        rx = cx + drift - 250 + i*44; ph = (t*105 + i*23) % 74
        y0 = 268 + ph
        if y0 < 360: line(ctx, [(rx, y0), (rx - 6, y0 + 24)], hexc('#7f93b5'), 3)
    for i in range(10):
        x = 135 + i*95
        v2cast(who[i % 3], 0.44 + 0.02*(i % 3)).draw(ctx, x, 520, t, "sad" if i < 7 else "neutral", blink_seed=i)
    t0 = _T(T, at, 1.2)
    if t >= t0: text(ctx, f"{int(70*clamp((t - t0)/0.56))}%", 640, 95, 84, (1, 1, 1), outline=INK)

# ================= 2. priceline_market (S09) =================
def c_priceline_market(ctx, t, dur, T):
    """S09: v1 price line drawn on a dark-green chalk price board in the market; chalk-white line,
    running price tag 100 -> 687 (logic copied from c_priceline)."""
    box(ctx, 90, 100, 1100, 520, hexc('#23412e'), 18, INK, 5)
    box(ctx, 104, 114, 1072, 492, hexc('#23412e'), 12, hexc('#3c5f47'), 2.5)
    for gy in (200, 300, 400, 500): line(ctx, [(140, gy), (1140, gy)], CHALKW, 2, .10)
    text(ctx, "PRICE INDEX", 150, 150, 30, hexc('#dfe7d8'), anchor="l")
    pts = [(150, 570), (250, 540), (320, 555), (430, 470), (510, 492), (645, 395), (725, 415), (880, 305), (960, 325), (1065, 215)]
    tp = _T(T, "@587", 2.4)
    k = clamp((t - 0.4)/max(tp - 0.4, 0.3))
    path = _walk(pts, k)
    if len(path) > 1: line(ctx, path, INK, 14); line(ctx, path, CHALKW, 8)
    tip = path[-1] if path else pts[0]
    tr = _T(T, "@running", 0.2)
    price_tag(ctx, tip[0] - 40, tip[1] - 90, 0.8, value=str(int(lerp(100, 687, k))), walk=(t*3.2 if tr <= t < tp else None))

# ================= 3. ration_queue (S35) =================
def c_ration_queue(ctx, t, dur, T, at="@result"):
    """S35: 8 people shuffle forward 20 px/s in front of a boarded state-store counter with a CLOSED sign."""
    t0 = _T(T, at, 0.5); sp = 82; off = int(max(0.0, t - t0))*20 % sp
    who = ("farmer", "mother", "clerk", "customer", "kid", "farmer", "mother", "worker")
    for i in range(8):
        x = 110 + i*sp + off
        v2cast(who[i], 0.46 + 0.03*(i % 2)).draw(ctx, x, 520, t, "sad" if i % 2 else "tired", facing=0.35, blink_seed=i)
    state_counter(ctx, 1010, 560, w=440)
    for by, rot in ((600, 0.10), (648, -0.09)):             # boarded planks across the counter front
        ctx.save(); ctx.translate(1010, by); ctx.rotate(rot)
        box(ctx, -165, -12, 330, 24, hexc('#b98a5e'), 3, INK, 2.5); ctx.restore()
    line(ctx, [(960, 500), (960, 522)], INK, 2); line(ctx, [(1060, 500), (1060, 522)], INK, 2)
    box(ctx, 920, 522, 180, 58, PAPER, 4, INK, 2.5)
    text(ctx, "CLOSED", 1010, 552, 40, hexc('#8a2f2f'))

# ================= 4/5. sacks_shrink + sacks_grow (S38, S56) =================
def _sack_pos(x, y):
    """15-sack pyramid, ordered bottom->top (row of 5, then 4, 3, 2, 1)."""
    P = []
    for row, n in enumerate((5, 4, 3, 2, 1)):
        for j in range(n):
            P.append((x + (j - (n-1)/2)*76, y - row*88))
    return P

def c_sacks_shrink(ctx, t, dur, T, x=640, y=600, at="@collapsed"):
    """S38: rice-sack pyramid collapses top-down, one sack every ~0.15 s, each with a small puff."""
    t0 = _T(T, at, 1.0); P = _sack_pos(x, y)
    for i, (sx, sy) in enumerate(P):                        # i=0 bottom ... 14 top
        vanish = t0 + (14 - i)*0.15
        if t < vanish: rice_sack(ctx, sx, sy, 0.5)
        elif t < vanish + 0.7: smoke(ctx, sx, sy - 45, (t - vanish)/0.7, 40, seed=i + 2)

def c_sacks_grow(ctx, t, dur, T, x=640, y=620, at="@exploded"):
    """S56: sacks appear bottom-up one every ~0.12 s until 15."""
    t0 = _T(T, at, 1.0); P = _sack_pos(x, y)
    for i, (sx, sy) in enumerate(P):
        popped(ctx, t, t0 + i*0.12, sx, sy, lambda c: rice_sack(c, 0, 0, 0.5), dur=0.3, puff=False, seed=i + 3)

# ================= 6. chart_crash (S30) =================
def c_chart_crash(ctx, t, dur, T, x=760, y=180, w=420, h=260, at="@total"):
    """S30: chart on the wall screen rises gently, falls off a cliff at `at`, screen flickers red twice."""
    box(ctx, x, y, w, h, hexc('#101c16'), 12, INK, 4)
    line(ctx, [(x + 12, y + h - 20), (x + w - 12, y + h - 20)], CHALKW, 3, .5)
    t0 = _T(T, at, 1.6)
    rise = [(x + 14, y + h - 26), (x + 70, y + h - 54), (x + 128, y + h - 42), (x + 192, y + h - 80),
            (x + 248, y + h - 68), (x + 306, y + h - 106), (x + 348, y + h - 120)]
    cliff = [(x + 348, y + h - 120), (x + 372, y + h - 96), (x + 392, y + h + 118)]
    kr = ease_io((t - (t0 - 1.3))/1.3); path = _walk(rise, kr)
    if len(path) > 1: line(ctx, path, INK, 10); line(ctx, path, GOLD, 5)
    kc = ease_out((t - t0)/0.45); cpath = _walk(cliff, kc)
    if len(cpath) > 1: line(ctx, cpath, INK, 10); line(ctx, cpath, RED, 5)
    for a, b in ((0.06, 0.20), (0.32, 0.46)):               # two flat red flickers
        if t0 + a <= t < t0 + b:
            rrect(ctx, x + 4, y + 4, w - 8, h - 8, 10); ctx.set_source_rgba(*RED, 0.32); ctx.fill()

# ================= 7. climb_line (S26) =================
def c_climb_line(ctx, t, dur, T, at="@executed"):
    """S26: a mountain-path line draws from bottom-left to top-right over 1.2 s, then a flag pops at the top."""
    t0 = _T(T, at, 0.8)
    pts = [(340, 560), (420, 522), (500, 534), (580, 470), (660, 482), (740, 414), (820, 424), (900, 342), (980, 268), (1080, 200)]
    path = _walk(pts, ease_io((t - t0)/1.2))
    if len(path) > 1: line(ctx, path, INK, 9); line(ctx, path, (1, 1, 1), 4)
    def flag(c):
        line(c, [(0, 0), (0, -52)], INK, 5); poly(c, [(0, -52), (40, -42), (0, -30)], RED, INK, 2.5)
    popped(ctx, t, t0 + 1.25, 1080, 200, flag, seed=8, puff=False)

# ================= 8. climb_dot (S141) =================
def c_climb_dot(ctx, t, dur, T, at="@gamble", cx=220, cy=160, cw=840, ch=380):
    """S141: a gold dot climbs the smile curve from ASSEMBLY (u=0.5) to R&D (u=0.04) with a fading trail.
    Geometry mirrors smile_curve(): left=cx+70 right=cx+cw-30 top=cy+70 bot=cy+ch-100."""
    t0 = _T(T, at, 1.0); k = clamp((t - t0)/1.5)
    if k <= 0: return
    L, R = cx + 70, cx + cw - 30; TOP, BOT = cy + 70, cy + ch - 100
    pos = lambda u: (L + u*(R - L), TOP + (BOT - TOP)*math.exp(-((u - 0.5)/0.2)**2))
    u = lerp(0.5, 0.04, ease_io(k))
    for j in range(9, 0, -1):
        tu = min(0.5, u + j*0.022); px, py = pos(tu)
        circle(ctx, px, py, 11 - j*0.8, GLD_L, a=0.32*(1 - j/10))
    px, py = pos(u)
    circle(ctx, px, py, 13, GLD_L, INK, 3); circle(ctx, px - 4, py - 5, 4, (1, 1, 1), a=0.6)

# ================= 9. supply_web (S23, S122) =================
def c_supply_web(ctx, t, dur, T, x=640, y=360, at="@node", hub="VIETNAM", pulse=False):
    """Glowing supply network: hub + 8 nodes, links light up one by one; pulse=True beats the hub."""
    t0 = _T(T, at, 0.8)
    labels = ("US", "EU", "CN", "KR", "JP", "SEA", "IN", "AU")
    nodes = [(x + math.cos(-math.pi/2 + i*math.pi/4)*rr, y + math.sin(-math.pi/2 + i*math.pi/4)*rr*0.82, labels[i])
             for i, rr in enumerate((250, 210, 250, 210, 250, 210, 250, 210))]
    for i, (nx, ny, lb) in enumerate(nodes):
        ti = t0 + 0.2 + i*0.25; k = ease_out((t - ti)/0.35)
        if k <= 0: continue
        ex, ey = lerp(x, nx, k), lerp(y, ny, k)
        line(ctx, [(x, y), (ex, ey)], GOLD, 9, .28); line(ctx, [(x, y), (ex, ey)], CHALKW, 3)
        if k >= 1:
            def node(c, lb=lb):
                circle(c, 0, 0, 12, hexc('#cfe6ea'), INK, 2.5); circle(c, 0, 0, 5, hexc('#5fa8d9'))
                text(c, lb, 0, -28, 30, (1, 1, 1), outline=INK)
            popped(ctx, t, ti + 0.3, nx, ny, node, seed=i + 2, puff=False)
    if pulse and t > t0:
        for ph in (((t - t0)*1.7) % 1, ((t - t0)*1.7 + 0.5) % 1):
            ctx.new_path(); ctx.arc(x, y, 62 + ph*95, 0, 2*math.pi)
            ctx.set_source_rgba(*GOLD, 0.30*(1 - ph)); ctx.set_line_width(7); ctx.stroke()
    rr = 62*(1 + (0.06*math.sin((t - t0)*4*math.pi) if t > t0 else 0))
    if t >= t0:
        circle(ctx, x, y, rr, GOLD, INK, 4); circle(ctx, x, y, rr*0.72, GOLD_D)
        text(ctx, hub, x, y, 34, hexc('#20180a'))

# ================= 10. strings_in (S64) =================
def c_strings_in(ctx, t, dur, T, x=640, y=340, r=170, at="@aggressive"):
    """6 coloured strings tie onto the globe one by one: each draws from off-screen to the rim, knot pops."""
    t0 = _T(T, at, 1.0)
    cols = [hexc('#c0392b'), hexc('#2f6db5'), hexc('#e9b949'), hexc('#0a7d5a'), hexc('#7b3f8c'), hexc('#e07b39')]
    for i, ang in enumerate((0.32, 1.44, 2.58, 3.58, 4.56, 5.66)):
        ca, sa = math.cos(ang), math.sin(ang)
        p0 = (x + ca*1080, y + sa*1080); p1 = (x + ca*(r - 6), y + sa*(r - 6))
        sw = 130 if i % 2 else -130
        pc = ((p0[0] + p1[0])/2 - sa*sw, (p0[1] + p1[1])/2 + ca*sw)
        ti = t0 + i*0.32; k = ease_out((t - ti)/0.55)
        if k <= 0: continue
        path = [_qp(p0, pc, p1, k*j/26) for j in range(27)]
        line(ctx, path, INK, 8, .45); line(ctx, path, cols[i], 4)
        if k >= 1 and pop(t, ti + 0.5, 0.25) > 0:
            s = min(pop(t, ti + 0.5, 0.25), 1.15)
            circle(ctx, p1[0], p1[1], 9*s, cols[i], INK, 2.5)

# ================= 11. trade_arcs (S81, S82) =================
def c_trade_arcs(ctx, t, dur, T, x=640, y=360, targets=(), at="@0.0"):
    """Dashed arcs from the globe rim to each target (drawn on the target's word); a small container rides each arc."""
    tbase = _T(T, at, 0.0)
    for i, tg in enumerate(targets):
        tx, ty, tok = tg[0], tg[1], tg[2]
        t0 = _T(T, tok, tbase + 0.4 + i*0.5) if isinstance(tok, str) else tbase + 0.4 + i*0.5
        dx, dy = tx - x, ty - y; dd = math.hypot(dx, dy) or 1
        ux, uy = dx/dd, dy/dd
        p0 = (x + ux*180, y + uy*180); p1 = (tx - ux*95, ty - uy*95)
        pc = ((p0[0] + p1[0])/2, (p0[1] + p1[1])/2 - 0.30*math.dist(p0, p1))
        k = ease_out((t - t0)/0.5)
        if k <= 0: continue
        path = [_qp(p0, pc, p1, k*j/26) for j in range(27)]
        ctx.save(); ctx.set_dash([15, 11])
        line(ctx, path, INK, 9); line(ctx, path, GOLD, 4.5)
        ctx.restore()
        if k >= 1:
            ph = ((t - t0 - 0.5)/1.5) % 1
            ax, ay = _qp(p0, pc, p1, ph)
            container(ctx, ax - 30, ay + 14, 0.25, c=hexc('#2f6db5'))

# ================= 12. signing (S80) =================
def c_signing(ctx, t, dur, T, x=640, y=420, n=3, at="@signed"):
    """3 documents on a table; a pen signs each in turn (squiggle draws in), purple round stamp thumps after each."""
    t0 = _T(T, at, 0.8)
    _table(ctx, x, y + 95, 620)
    for i in range(int(n)):
        px = x + (i - (n-1)/2)*175; py = y
        paper(ctx, px, py, 150, 190, (i - 1)*0.03, label="FTA", size=26)
        ti = t0 + i*1.0; k = clamp((t - ti)/0.55)
        sq = [(px - 46, py + 52), (px - 24, py + 38), (px - 2, py + 52), (px + 20, py + 38), (px + 44, py + 50)]
        if 0 < k <= 1:
            path = _walk(sq, k)
            if len(path) > 1: line(ctx, path, hexc('#2f4a8a'), 3.5)
            if k < 1:
                tip = path[-1]
                line(ctx, [(tip[0] + 16, tip[1] - 26), tip], hexc('#8a5a2b'), 5)
                circle(ctx, tip[0], tip[1], 3, GOLD)
        s = pop(t, ti + 0.62, 0.22)
        if s > 0:                                            # tiny purple round stamp
            ctx.save(); ctx.translate(px, py - 28); ctx.rotate(-0.2); ctx.scale(s, s)
            ctx.new_path(); ctx.arc(0, 0, 32, 0, 2*math.pi); ctx.set_source_rgba(*STAMP, .8)
            ctx.set_line_width(5); ctx.stroke()
            ctx.new_path(); ctx.arc(0, 0, 24, 0, 2*math.pi); ctx.set_line_width(2); ctx.stroke()
            text(ctx, "FTA", 0, 0, 20, STAMP); ctx.restore()

# ================= 13. dice_roll (S83) =================
def _die(ctx, x, y, rot, val):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    box(ctx, -72, -72, 144, 144, (1, 1, 1), 20, INK, 3.5)
    box(ctx, 45, -72, 27, 144, hexc('#d9d5c8'), 0)
    PIPS = {1: [(0, 0)], 3: [(-36, -36), (0, 0), (36, 36)],
            6: [(-28, -42), (-28, 0), (-28, 42), (28, -42), (28, 0), (28, 42)]}
    for ppx, ppy in PIPS[val]: circle(ctx, ppx, ppy, 11, INK)
    ctx.restore()

def c_dice_roll(ctx, t, dur, T, x=640, y=420, at="@gamble"):
    """Two big dice tumble in from left/right, roll across the felt, land showing 6 and 6 at at+0.6."""
    t0 = _T(T, at, 1.0); k = ease_io(clamp((t - t0)/0.6))
    if k <= 0: return
    for i, (x0, x1, spin) in enumerate(((-150, 550, 1), (1430, 730, -1))):
        dx = lerp(x0, x1, k)
        hop = abs(math.sin((k*3.2 + i*0.45)*math.pi))*130*(1 - k)
        rot = spin*k*10*math.pi                              # 5 full turns, ends at 0 mod 2pi
        ellipse(ctx, dx, y + 92, 72*(1 - hop/260), 14, (0, 0, 0), a=0.2)
        _die(ctx, dx, y - hop, rot, 6 if k >= 0.98 else 3)

# ================= 14. field_to_factory (S89) =================
def c_field_to_factory(ctx, t, dur, T, at="@greenfield"):
    """S89: a modern factory rises out of the ground on the right (site) half, clipped to the ground line, with dust."""
    t0 = _T(T, at, 1.0); k = ease_io((t - t0)/1.0)
    if k <= 0: return
    ctx.save(); ctx.rectangle(640, -200, 640, 760); ctx.clip()  # only right half, above y=560
    factory_modern(ctx, 900, lerp(760, 560, k), 0.7, label="SAMSUNG")
    ctx.restore()
    if k > 0.9: dust(ctx, 900, 556, t, t0 + 0.92, n=4, size=55, seed=9)

# ================= 15. campus_build (S91, S113) =================
def c_campus_build(ctx, t, dur, T, at="@turned"):
    """4 factory blocks rise behind the fence line one after another (0.5 s apart), each with a small crane while up."""
    t0 = _T(T, at, 0.8)
    for i, bx in enumerate((205, 465, 725, 985)):
        ti = t0 + i*0.5; k = ease_io((t - ti)/0.9)
        if k <= 0: continue
        if 0 < k < 1.35:                                     # little crane arm above, while rising
            cxx = bx + 122
            line(ctx, [(cxx, 560), (cxx, 430)], INK, 6); line(ctx, [(cxx - 95, 438), (cxx + 55, 438)], hexc('#d9a62e'), 5)
            line(ctx, [(cxx - 70, 438), (cxx - 70, 470)], INK, 2.5); box(ctx, cxx - 82, 470, 24, 18, hexc('#8d9299'), 2, INK, 2)
        ctx.save(); ctx.rectangle(0, -200, W, 760); ctx.clip()
        factory_modern(ctx, bx, lerp(745, 560, k), 0.45)
        ctx.restore()

# ================= 16. money_pour (S93) =================
def c_money_pour(ctx, t, dur, T, at="@pouring"):
    """banknotes pour from the top edge in deterministic columns; a stack grows at (640,600)."""
    t0 = _T(T, at, 1.0)
    if t < t0: return
    tt = t - t0
    for i in range(10):
        bill(ctx, 200 + i*90, 100 + ((tt*260 + i*47) % 500), 0.5*math.sin(t*2.2 + i*1.7), 0.7)
    n = int(clamp(tt/1.8)*16)
    for j in range(n):
        bill(ctx, 640 + ((j % 3) - 1)*14, 592 - j*15, ((j % 5) - 2)*0.04, 0.85)

# ================= 17. phone_wall (S95) =================
def c_phone_wall(ctx, t, dur, T, x=640, y=330, frac=0.5, at="@50"):
    """10x5 wall of phones; from `at` the left `frac` lights up gold column by column (0.15 s each)."""
    t0 = _T(T, at, 1.0); cols, rows = 10, 5; lit = int(round(cols*frac))
    for c_ in range(cols):
        for r in range(rows):
            px, py = x + (c_ - 4.5)*48, y + (r - 2)*78
            smartphone(ctx, px, py, 0.28, 0, "back", None)
            if c_ < lit:
                def scr(cc):
                    box(cc, -11, -28, 22, 56, GLD_L, 6, INK, 2); box(cc, -11, -28, 22, 14, GOLD, 6)
                popped(ctx, t, t0 + c_*0.15, px, py, scr, dur=0.25, puff=False, seed=c_*3 + r)

# ================= 18. carton_stream (S97) =================
def c_carton_stream(ctx, t, dur, T, at="@accounts", y=540):
    """cartons ride a belt from the right into the plane's nose."""
    t0 = _T(T, at, 1.0)
    if t < t0: return
    tt = t - t0
    ctx.save(); ctx.set_dash([22, 18])
    line(ctx, [(520, y + 26), (1280, y + 26)], hexc('#8d969c'), 5)
    ctx.restore()
    box(ctx, 520, y, 760, 12, hexc('#3a3f4b'), 0, INK, 2.5)
    for j in range(4):
        cxx = 1180 - ((tt*220 + j*207) % 620)
        if cxx > 585: carton(ctx, cxx, y, 0.5, label="VN")

# ================= 19. gdp_cake (S98) =================
def c_gdp_cake(ctx, t, dur, T, x=640, y=420, frac=0.15, at="@15", label="15% OF GDP"):
    """round cake (top view) with a `frac` slice lifted out and labelled."""
    t0 = _T(T, at, 1.0); k = ease_io((t - t0)/0.9); a = 2*math.pi*frac
    a0, a1 = -math.pi/2, -math.pi/2 + a; mid = (a0 + a1)/2
    circle(ctx, x, y, 172, hexc('#cfe0ee'), INK, 4)
    circle(ctx, x, y, 150, hexc('#f3e2ad'), INK, 3)
    for i in range(10):
        ia = a0 + i*a
        line(ctx, [(x + math.cos(ia)*132, y + math.sin(ia)*132), (x + math.cos(ia)*150, y + math.sin(ia)*150)], hexc('#c4a258'), 3)
    ctx.new_path(); ctx.arc(x, y, 150, a0, a1); ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
    if k > 0:
        ox, oy = math.cos(mid)*75*k, math.sin(mid)*75*k
        ctx.save(); ctx.translate(x + ox, y + oy + 8)       # cake side (depth hint)
        ctx.new_path(); ctx.move_to(0, 0); ctx.arc(0, 0, 150, a0, a1); ctx.close_path()
        ctx.set_source_rgb(*GOLD_D); ctx.fill(); ctx.restore()
        ctx.save(); ctx.translate(x + ox, y + oy)
        ctx.new_path(); ctx.move_to(0, 0); ctx.arc(0, 0, 150, a0, a1); ctx.close_path()
        ctx.set_source_rgb(*hexc('#f3e2ad')); ctx.fill_preserve()
        ctx.set_source_rgb(*INK); ctx.set_line_width(3); ctx.stroke()
        ctx.restore()
        ellipse(ctx, x + ox + math.cos(mid)*80, y + oy + math.sin(mid)*80, 26, 9, hexc('#d9776b'))
        hx, hy = x + ox + math.cos(mid)*172, y + oy + math.sin(mid)*172   # spatula
        line(ctx, [(hx, hy), (hx + math.cos(mid)*90, hy + math.sin(mid)*90)], hexc('#8d95a2'), 7)
    if k > 0.5: text(ctx, label, x, y + 186, 40, (1, 1, 1), outline=INK)

# ================= 20. box_stack (S19, S120) =================
def c_box_stack(ctx, t, dur, T, x=640, y=600, n=9, hl=0, at="@running"):
    """cartons stack into a growing pile (rows of 3) from `at`; the first `hl` boxes are gold."""
    t0 = _T(T, at, 0.8)
    for i in range(int(n)):
        row, col = i // 3, i % 3
        bx = x + (col - 1)*102; by = 560 - row*82 - 39
        gold = i < int(hl)
        c1, c2 = (GLD_L, GOLD_D) if gold else (hexc('#d8c08e'), hexc('#bfa472'))
        def drw(cc, c1=c1, c2=c2, gold=gold):
            box(cc, -48, -38, 96, 76, c1, 4, INK, 3)
            poly(cc, [(28, -38), (48, -38), (48, 38), (28, 38)], c2)
            line(cc, [(-48, -6), (48, -6)], INK, 2.5, .4)
            line(cc, [(0, -38), (0, -6)], c2, 8)
            if gold: text(cc, "VN", 0, 14, 26, hexc('#6a4a12'))
        popped(ctx, t, t0 + i*0.18, bx, by, drw, dur=0.28, seed=i + 2)

# ================= 21. gloves (S103) =================
def c_gloves(ctx, t, dur, T, at="@trade", x1=330, x2=950, y=600, s=1.0):
    """red boxing gloves on the 4 raised hands of the two officials (positions from the line's p elements)."""
    t0 = _T(T, at, 1.0)
    if t < t0: return
    tw, th = 150, 190
    for px, who, dt in ((x1, "us_official", 0.0), (x2, "cn_official", 0.15)):
        bob = math.sin(t*2.4 + sum(map(ord, who)) % 7)*2.5
        sy = y + bob + (-th + 34)*s
        for a in ((-40, -130), (40, -130)):                  # raise_both offsets from each shoulder
            hx = px + (-(tw/2 - 10) + a[0])*s if a[0] < 0 else px + ((tw/2 - 10) + a[0])*s
            hy = sy + a[1]*s
            k = pop(t, t0 + dt, 0.3)
            if k <= 0: continue
            ctx.save(); ctx.translate(hx, hy); ctx.scale(k, k)
            box(ctx, -13, 20, 26, 16, hexc('#8f2a1f'), 3, INK, 2.5)
            circle(ctx, 0, 0, 26, RED, INK, 3)
            circle(ctx, -22, -10, 9, RED, INK, 2.5)
            circle(ctx, -7, -9, 8, (1, 1, 1), a=0.28)
            ctx.restore()

# ================= 22. truck_queue (S74, S130) =================
def c_truck_queue(ctx, t, dur, T, at="@door", gate_x=250):
    """4 trucks roll right from `at`; the striped boom bar lifts as the lead truck reaches the post (~1 s in)."""
    t0 = _T(T, at, 0.8); tt = t - t0
    if tt < 0: return
    for i in range(4):                                       # trucks under the gate
        tx = -200 + ((tt*60 + i*260) % 1600)
        if -180 < tx < 1460: cargo_truck(ctx, tx, 560, 0.6, label="VN")
    box(ctx, gate_x - 16, 430, 32, 132, hexc('#8f2a1f'), 3, INK, 3)
    box(ctx, gate_x - 26, 418, 52, 22, hexc('#c0392b'), 4, INK, 3)
    lift = ease_io(clamp((tt - 1.0)/0.6))
    ctx.save(); ctx.translate(gate_x, 448); ctx.rotate(-lift*(math.pi/2 - 0.12))
    for k in range(8): box(ctx, 8 + k*37, -9, 37, 18, (1, 1, 1) if k % 2 else RED, 0, INK, 2)
    ctx.restore()

# ================= 23. coins_grow (S126) =================
def c_coins_grow(ctx, t, dur, T, x=950, y=600, at="@expanded"):
    """coin stack grows 1->50 quickly, then a 50x tag pops."""
    t0 = _T(T, at, 1.0)
    n = int(clamp((t - t0)/1.5)*50) if t >= t0 else 0
    if n > 1:                                                # column body so the stack reads as coins, not a ladder
        box(ctx, x - 16, y - n*6 - 16, 32, n*6, hexc('#e0ac2c'), 0, INK, 2.5)
    for j in range(n): coin(ctx, x, y - j*6 - 16, 16)
    def tag(c):
        box(c, -44, -26, 88, 52, PAPER, 8, INK, 3); text(c, "50x", 0, 2, 36, RED)
    popped(ctx, t, t0 + 1.6, x + 95, y - 300, tag, seed=7, puff=False)

# ================= 24. country_build (S127) =================
def c_country_build(ctx, t, dur, T, at="@Modern", ports=None, zones=None):
    """top-down build: highway draws left->right, then a port icon pops (right), then a zone grid appears."""
    t0 = _T(T, at, 0.5)
    tp = _T(T, ports, t0 + 1.0) if isinstance(ports, str) else t0 + 1.0
    tz = _T(T, zones, t0 + 2.0) if isinstance(zones, str) else t0 + 2.0
    road = [(80, 470), (420, 452), (720, 470), (1010, 442)]
    kr = ease_io((t - t0)/1.0); path = _walk(road, kr)
    if len(path) > 1: line(ctx, path, INK, 50); line(ctx, path, hexc('#8d969c'), 44)
    if kr > 0.15:
        ctx.save(); ctx.set_dash([26, 22]); line(ctx, _walk(road, kr), CHALKW, 5, .85); ctx.restore()
    branch = [(720, 470), (880, 512), (1010, 530)]
    kb = ease_io((t - (tp - 0.5))/0.6); bpath = _walk(branch, kb)
    if len(bpath) > 1: line(ctx, bpath, INK, 30); line(ctx, bpath, hexc('#8d969c'), 24)
    def drawport(c):
        box(c, -20, 0, 180, 26, hexc('#b3b7bd'), 2, INK, 2.5)      # pier
        port_crane(c, 0, 0, 0.3)
        for k in range(3): container(c, 95 + k*46, -4, 0.18, c=hexc('#2f6db5'))
    popped(ctx, t, tp, 1075, 556, drawport, seed=5, puff=True)
    for i in range(12):
        rx, ry = 175 + (i % 4)*112, 155 + (i // 4)*74
        def roof(c):
            box(c, -44, -24, 88, 48, hexc('#b0b6bb'), 2, INK, 2.5)
            for k in range(3): line(c, [(-44 + k*30, -24), (-14 + k*30, 24)], hexc('#676c74'), 4)
        popped(ctx, t, tz + i*0.08, rx, ry, roof, dur=0.25, seed=i + 2, puff=False)

# ================= 25. value_split (S131) =================
def c_value_split(ctx, t, dur, T, x=760, y=360, at="@majority"):
    """big VALUE coin splits: a small wedge rolls left to Lan (x=380), the big part rolls right to the exec (x=1040)."""
    t0 = _T(T, at, 1.0); k = ease_io((t - t0)/1.2); R = 90
    a0, a1 = math.pi*0.78, math.pi*1.22
    if k <= 0:
        circle(ctx, x, y, R, GLD_L, INK, 4); circle(ctx, x, y, R*0.66, hexc('#e0ac2c'))
        text(ctx, "VALUE", x, y, 40, hexc('#8a6418'))
        for aa in (a0, a1): line(ctx, [(x, y), (x + math.cos(aa)*R, y + math.sin(aa)*R)], INK, 2.5, .6)
        return
    def piece(px, py, rot, arc):
        ctx.save(); ctx.translate(px, py); ctx.rotate(rot)
        ctx.new_path(); ctx.move_to(0, 0); ctx.arc(0, 0, R, *arc); ctx.close_path()
        ctx.set_source_rgb(*GLD_L); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(4); ctx.stroke()
        ctx.restore()
    sx, sy = lerp(x, 460, k), y + 90 - 60*math.sin(k*math.pi)      # land at Lan's chest height, clear of her face
    bx, by = lerp(x, 980, k), y + 120 - 45*math.sin(k*math.pi)     # and low-left of the exec's head
    piece(sx, sy, -k*6, (a0, a1))
    piece(bx, by, k*6, (a1, a0 + 2*math.pi))
    text(ctx, "VALUE", bx, by, 40, hexc('#8a6418'))

# ================= 26. supplier_board (S137) =================
def c_supplier_board(ctx, t, dur, T, x=640, y=330, local=1, total=20, at="@tiny"):
    """board of `total` supplier badges: most grey KR/CN/TW, `local` gold VN badge; VN highlights on `at`."""
    t0 = _T(T, at, 1.0)
    box(ctx, x - 450, y - 210, 900, 420, hexc('#252a31'), 14, INK, 4)
    vn = 7; cols, lab = 5, ("KR", "CN", "TW")
    for i in range(int(total)):
        bx, by = x - 400 + (i % cols)*175 + 75, y - 165 + (i // cols)*95 + 34
        gold = i == vn
        popped(ctx, t, 0.15 + i*0.05, bx, by,
               lambda c, gold=gold, lb=("VN" if gold else lab[i % 3]):
               (box(c, -75, -34, 150, 68, GLD_L if gold else hexc('#8d95a2'), 10, INK, 2.5),
                text(c, lb, 0, 2, 34, hexc('#20180a') if gold else hexc('#33383f'))),
               dur=0.25, seed=i + 2, puff=False)
        if gold and t >= t0:
            s = 1 + 0.1*max(0, math.sin((t - t0)*6))
            ctx.save(); ctx.translate(bx, by); ctx.scale(s, s)
            ctx.new_path(); rrect(ctx, -84, -42, 168, 84, 14); ctx.set_source_rgba(*GOLD, 0.35)
            ctx.set_line_width(10); ctx.stroke(); ctx.restore()
            circle(ctx, bx + 92, by - 40, 7, RED, INK, 2)

# ================= 27. cartons_in (S138) =================
def c_cartons_in(ctx, t, dur, T, **kv):
    """cartons labelled from[i] slide in from 3 sides to a central table on their words (from/at arrive in kv)."""
    fr = kv.get("from", ("CHINA", "KOREA", "TAIWAN"))
    ats = kv.get("at", ["@China", "@South", "@Taiwan"])
    _table(ctx, 640, 500, 400)
    starts = [(40, 445), (1245, 255), (1245, 620)]
    ends = [(530, 500), (665, 500), (795, 500)]
    for i in range(3):
        ti = _T(T, ats[i], 0.6 + i*0.5)
        k = ease_io((t - ti)/0.6)
        if k <= 0: continue
        px, py = lerp(starts[i][0], ends[i][0], k), lerp(starts[i][1], ends[i][1], k)
        if k < 1: circle(ctx, px, py, 5, (1, 1, 1), a=0.4)
        carton(ctx, px, py, 0.6, label=fr[i])

# ---------------- registration ----------------
CUSTOM2 = {
    "zone2": c_zone2, "priceline_market": c_priceline_market, "ration_queue": c_ration_queue,
    "sacks_shrink": c_sacks_shrink, "sacks_grow": c_sacks_grow, "chart_crash": c_chart_crash,
    "climb_line": c_climb_line, "climb_dot": c_climb_dot, "supply_web": c_supply_web,
    "strings_in": c_strings_in, "trade_arcs": c_trade_arcs, "signing": c_signing,
    "dice_roll": c_dice_roll, "field_to_factory": c_field_to_factory, "campus_build": c_campus_build,
    "money_pour": c_money_pour, "phone_wall": c_phone_wall, "carton_stream": c_carton_stream,
    "gdp_cake": c_gdp_cake, "box_stack": c_box_stack, "gloves": c_gloves, "truck_queue": c_truck_queue,
    "coins_grow": c_coins_grow, "country_build": c_country_build, "value_split": c_value_split,
    "supplier_board": c_supplier_board, "cartons_in": c_cartons_in,
}
