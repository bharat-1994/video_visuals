"""Registries for engine/scene.py + custom shot code for the Vietnam film."""
import sys, os, math, inspect; sys.path.insert(0, os.getcwd())
from episodes.vietnam import assets as A, assets_ind as I, assets_pol as P
from episodes.vietnam.assets import *
from episodes.vietnam.assets_ind import *
from episodes.vietnam.assets_pol import *
import lib as L
from scene import BG, ASSETS, CAST, CUSTOM, AMBIENCE

# ---------------- assets: every public drawing function ----------------
for mod in (L, A, I, P):
    for k, f in vars(mod).items():
        if callable(f) and not k.startswith("_") and inspect.isfunction(f):
            ps = list(inspect.signature(f).parameters)
            if ps and ps[0] == "ctx": ASSETS[k] = f

def assembly_phones(ctx, x, y, w=900, t=0.0, side="back", label="MADE IN VIETNAM"):
    """Assembly line carrying phones (standing on the belt)."""
    assembly_line(ctx, x, y, w, t, item=lambda c, cx, cy: smartphone(c, cx, cy - 62, 0.5, 0.0, side, label if side == "back" else None), gap=150)
ASSETS["assembly_phones"] = assembly_phones

# ---------------- cast ----------------
for w in ("farmer", "mother", "kid", "clerk", "chef", "official", "official2", "worker", "worker_m", "exec", "exec2", "customer"):
    CAST[w] = (lambda w: lambda s=1.0: vcast(w, s))(w)
for w in ("banker", "editor"): CAST[w] = (lambda w: lambda s=1.0: cast(w, s))(w)

# ---------------- backgrounds ----------------
def _sky(ctx, sky='#bfe3ef', ground='#8cc46f', horizon=560): bg_sky_ground(ctx, hexc(sky) if isinstance(sky, str) else sky, hexc(ground) if isinstance(ground, str) else ground, horizon)
def _night(ctx, t=0.0):
    bg_flat(ctx, NIGHT)
    for i in range(40): circle(ctx, (i*197) % 1280, (i*83) % 420, 2 + (i % 3), (1, 1, 1), a=0.5 + 0.4*math.sin(t*2 + i))
def _city(ctx, t=0.0, night=False):
    bg_flat(ctx, NIGHT if night else hexc('#cfe6ee')); skyline(ctx, 560, night=night, t=t); box(ctx, 0, 560, W, 160, hexc('#7d8a8f') if not night else hexc('#2a2f36'))
def _port(ctx, t=0.0):
    bg_flat(ctx, hexc('#cfe6ee')); sea(ctx, 520, t)
def _office(ctx, wall='#dfe3e6'):
    bg_room(ctx, hexc(wall), hexc('#9a7b5c'), 560); city_window(ctx, 820, 110, 360, 260)
def _flat(ctx, c='#e9e1cf'): bg_flat(ctx, hexc(c) if isinstance(c, str) else c)
def _room(ctx, wall='#e9e1cf', floor='#b98a5e'): bg_room(ctx, hexc(wall), hexc(floor), 560)
def _factory_in(ctx):
    bg_room(ctx, hexc('#d9dfe3'), hexc('#8d969c'), 560)
    for i in range(6): box(ctx, 40 + i*215, 60, 150, 90, hexc('#bfe3ef'), 4, INK, 3)
BG.update(paddy=lambda ctx, t=0.0: bg_paddy(ctx, t), dark=lambda ctx: bg_dark(ctx), flat=_flat, room=_room, congress=bg_congress,
          kitchen=bg_kitchen, sky=_sky, night=_night, city=_city, port=_port, office=_office, factory=_factory_in)
AMBIENCE.update(paddy=("wind_ambience", -22), kitchen=("office_hum", -26), congress=("office_hum", -26), port=("wind_ambience", -24),
                city=("wind_ambience", -26), office=("office_hum", -26), room=("office_hum", -26), factory=("office_hum", -24), night=("night_crickets", -24))

# ---------------- custom shot code ----------------
def c_zone(ctx, t, dur, T):
    """S04: 10 people, a dark zone sweeps behind the left 7, who turn sad; counter 0->70%."""
    w = lerp(0, 770, ease_io((t - T("@entire") + 0.3)/0.9))
    box(ctx, 0, 0, W, H, hexc('#e9e1cf')); box(ctx, 0, 560, W, 160, hexc('#d7cdb6'))
    if w > 1: box(ctx, 60, 150, w, 440, hexc('#5a5560'), 16)
    who = ("farmer", "mother", "kid")
    for i in range(10):
        x = 130 + i*113; inside = i < 7 and 60 + w > x + 30
        vcast(who[i % 3], 0.42).draw(ctx, x, 520, t, "sad" if inside else "neutral", blink_seed=i)
    t0 = T("@70")
    if t >= t0: text(ctx, f"{int(70*clamp((t - t0)/0.56))}%", 640, 95, 84, (1, 1, 1), outline=INK)

def c_mill(ctx, t, dur, T):
    """S05: tired farmer pushes a stone mill at dusk; hands stay on the pole."""
    ctx.save(); ctx.rectangle(-200, -200, W + 400, H + 400); ctx.set_source_rgba(0.15, 0.1, 0.2, 0.3); ctx.fill(); ctx.restore()
    end = stone_mill(ctx, 520, 640, 1.0, ang=t*1.6, pole_dir=1)
    p = vcast("farmer", 0.85); x = end[0] + 75
    p.draw(ctx, x, 610, t, "tired", facing=-0.7, walk=t*1.4, armL=arm_to(p, x, 610, -1, end),
           armR=arm_to(p, x, 610, 1, (end[0] + 14, end[1] + 8)), cross=True)

def c_stamp(ctx, t, dur, T):
    """S06: ration book on a table, a rubber stamp slams down and lifts."""
    box(ctx, -200, 520, W + 400, 300, hexc('#a8703f')); line(ctx, [(-200, 520), (W + 200, 520)], INK, 3)
    ts = T("@dictated") + 0.14
    S = 0 if t < ts else clamp((t - ts)/0.25)
    t0 = T("@coupons")
    if t >= t0: popped(ctx, t, t0, 600, 330, lambda c: ration_coupon(c, 0, 0, 1.1, rot=-0.04, stamped=S), seed=4)
    if ts - 0.18 <= t <= ts + 0.5:
        if t < ts: y = lerp(-60, 402, clamp((t - ts + 0.18)/0.18)**2)
        elif t < ts + 0.15: y = 402
        else: y = lerp(402, -60, ease_io((t - ts - 0.15)/0.35))
        rubber_stamp(ctx, 736, y, 1.0)

def c_priceline(ctx, t, dur, T):
    """S09: a running price tag climbs a jagged line that draws itself."""
    pts = [(120, 600), (230, 560), (300, 575), (420, 480), (500, 500), (640, 390), (720, 410), (880, 300), (960, 320), (1080, 210)]
    tr, tp = T("@running"), T("@587")
    k = clamp((t - 0.4)/(tp - 0.4))
    segs = [(pts[i], pts[i+1]) for i in range(len(pts) - 1)]
    L_ = [math.dist(a, b) for a, b in segs]; tot = sum(L_); d = k*tot; path = [pts[0]]; tip = pts[0]
    for (a, b), l in zip(segs, L_):
        if d >= l: path.append(b); d -= l; tip = b
        else: tip = (lerp(a[0], b[0], d/l), lerp(a[1], b[1], d/l)); path.append(tip); break
    if len(path) > 1: line(ctx, path, INK, 15); line(ctx, path, RED, 9)
    price_tag(ctx, tip[0] - 40, tip[1] - 90, 0.8, value=str(int(lerp(100, 687, k))), walk=(t*3.2 if tr <= t < tp else None))

def c_gauge(ctx, t, dur, T, x=640, y=380, r=200, at="@out", label="ECONOMY", up=False):
    """Fuel gauge: needle sinks to E and the warning light blinks."""
    ctx.arc(x, y, r, math.pi, 0); ctx.close_path(); ctx.set_source_rgb(*hexc('#f4efe2')); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(6); ctx.stroke()
    for i in range(9):
        a = math.pi + i*math.pi/8; line(ctx, [(x + math.cos(a)*r*0.82, y + math.sin(a)*r*0.82), (x + math.cos(a)*r*0.95, y + math.sin(a)*r*0.95)], INK, 5)
    text(ctx, "E", x - r*0.7, y - 30, 56, RED); text(ctx, "F", x + r*0.7, y - 30, 56, INK); text(ctx, label, x, y - r*0.45, 34, INK)
    k = ease_io((t - T(at) + 0.6)/1.0)
    if up: a = math.pi*(1.25 + 0.75*k) + (0.03*math.sin(t*25) if k >= 1 else 0)
    else: a = math.pi*(1.75 - 0.75*k) if k < 1 else math.pi*(1.0 + 0.02*math.sin(t*20))
    line(ctx, [(x, y), (x + math.cos(a)*r*0.78, y + math.sin(a)*r*0.78)], RED, 9); circle(ctx, x, y, 18, INK)
    if k >= 1 and int(t*4) % 2: circle(ctx, x + r*0.55, y + 60, 22, hexc('#5fd35a') if up else hexc('#ff5a3c'), INK, 3)

def c_vnpins(ctx, t, dur, T, x=640, y=360, h=560, pins=(), glow=False):
    """Vietnam map with pins popping on words: pins=[["Bac Ninh",106.07,21.18,"@Baknin"], ...]."""
    if glow: circle(ctx, x, y, h*0.45, (1, 0.9, 0.5), a=0.15)
    vietnam_map(ctx, x, y, h)
    k = h/(23.35-8.6); kx = k*0.96
    for i, (name, lo, la, w) in enumerate(pins):
        px, py = x + (lo-105.8)*kx, y - (la-15.97)*k
        def pin(c, name=name):
            circle(c, 0, -28, 16, RED, INK, 3); poly(c, [(-10, -20), (10, -20), (0, 0)], RED, INK, 3); circle(c, 0, -28, 6, (1, 1, 1))
            text(c, name, 26 if i % 2 == 0 else -26, -28, 34, (1, 1, 1), anchor="l" if i % 2 == 0 else "r", outline=INK)
        if t >= T(w): popped(ctx, t, T(w), px, py, pin, seed=i + 2)

def c_asia(ctx, t, dur, T, x=640, y=370, h=640, pins=(), arrows=(), labels=True, hl="VN"):
    """asia_map + pins [[label,lon,lat,@w]] + arrows [[lon1,lat1,lon2,lat2,@w,'#hex']]."""
    r = asia_map(ctx, x, y, h, highlight=hl, labels=labels); Pj = r["proj"]
    for lo1, la1, lo2, la2, w, c in arrows:
        t0 = T(w); k = ease_out((t - t0)/0.6)
        if k > 0:
            (x1, y1), (x2, y2) = Pj(lo1, la1), Pj(lo2, la2); ex, ey = lerp(x1, x2, k), lerp(y1, y2, k)
            line(ctx, [(x1, y1), (ex, ey)], INK, 14); line(ctx, [(x1, y1), (ex, ey)], hexc(c), 8)
            a = math.atan2(ey - y1, ex - x1)
            poly(ctx, [(ex + math.cos(a)*16, ey + math.sin(a)*16), (ex + math.cos(a + 2.4)*24, ey + math.sin(a + 2.4)*24), (ex + math.cos(a - 2.4)*24, ey + math.sin(a - 2.4)*24)], hexc(c), INK, 3)
    for i, (name, lo, la, w) in enumerate(pins):
        if t >= T(w):
            px, py = Pj(lo, la)
            popped(ctx, t, T(w), px, py, lambda c, name=name: (circle(c, 0, 0, 12, RED, INK, 3), text(c, name, 20, -4, 34, (1, 1, 1), anchor="l", outline=INK)), seed=i + 5)

def c_pie(ctx, t, dur, T, x=640, y=360, r=180, frac=0.5, at="@50", label="", c='#e9b949', c2='#9aa0a8'):
    """Pie chart: the highlighted slice sweeps in at `at`."""
    circle(ctx, x, y, r, hexc(c2), INK, 4)
    k = ease_out((t - T(at))/0.8)*frac
    if k > 0:
        ctx.move_to(x, y); ctx.arc(x, y, r, -math.pi/2, -math.pi/2 + k*2*math.pi); ctx.close_path()
        ctx.set_source_rgb(*hexc(c)); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(4); ctx.stroke()
    if label and t >= T(at) + 0.4: text(ctx, label, x, y + r + 50, 48, (1, 1, 1), outline=INK)

def c_cage_lift(ctx, t, dur, T, at="@lifted"):
    """Embargo lifted: the padlock pops off, the cage flies up off the map (flips the S12 motif)."""
    vietnam_map(ctx, 640, 393, 317, cracks=1.0)
    t0 = T(at); k = ease_io((t - t0 - 0.35)/0.8)
    cage(ctx, 640, 600 - 760*k, 360, 440, lock=0 if t > t0 else 1)
    if t0 <= t < t0 + 1.0:
        u = (t - t0)/1.0; padlock(ctx, 640 + 220*u, 440 - 300*u + 500*u*u, 1.0 - 0.3*u, "EMBARGO")
    if t > t0 + 1.0: circle(ctx, 640, 393, 230, (1, 0.9, 0.5), a=0.12*clamp((t - t0 - 1.0)/0.5))

def c_cracks(ctx, t, dur, T):
    """S11: the map pops on 'nation' and cracks on devastated / back-to-back / conflicts, each with dust."""
    ws = [T("@devastated"), T("@back"), T("@conflicts")]
    C = sum(clamp((t - w)/0.3)/3 for w in ws); t0 = T("@nation")
    if t >= t0: popped(ctx, t, t0, 560, 340, lambda c: vietnam_map(c, 0, 0, 500, cracks=C), seed=6)
    for (x, y), w in zip([(530, 190), (650, 330), (560, 500)], ws): dust(ctx, x, y, t, w, n=4, size=50, seed=int(x))

def c_orbit(ctx, t, dur, T, x=920, y=330, at="@financial"):
    """S13: six coins orbit the globe from `at`, never crossing into the cage side."""
    t0 = T(at)
    if t < t0: return
    k = ease_out((t - t0)/0.4)
    for i in range(6):
        a = t*1.8 + i*1.047; ctx.save(); cx, cy = x + math.cos(a)*215, y + math.sin(a)*120
        ctx.translate(cx, cy); ctx.scale(k, k); coin(ctx, 0, 0, 20); ctx.restore()

def c_dusk(ctx, t, dur, T, at="@overnight"):
    """Day turns to night from `at` (overlay)."""
    k = ease_io((t - T(at))/0.6)
    if k > 0: ctx.rectangle(-300, -300, W + 600, H + 600); ctx.set_source_rgba(*NIGHT, k); ctx.fill()

CUSTOM.update(cracks=c_cracks, orbit=c_orbit, dusk=c_dusk, zone=c_zone, mill=c_mill, stamp=c_stamp, priceline=c_priceline, gauge=c_gauge, vnpins=c_vnpins, asia=c_asia, pie=c_pie, cage_lift=c_cage_lift)
