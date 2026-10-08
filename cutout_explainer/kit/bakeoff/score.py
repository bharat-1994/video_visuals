"""Objective checks for asset cards A/B/C. python3 bakeoff/score.py <A|B|C> <asset_file.py> <out_dir>
Writes <out_dir>/<card>.png (the picture to look at) and prints PASS/FAIL lines + a machine-readable summary line.
Run from the kit root. Checks: runs at two scales, no crash, <1 s, size window, bottom-centre anchor, scales with s,
flat palette (4-16 main colours), INK outline share, banned text, <= 300 lines."""
import sys, os, time, re, importlib.util, json
sys.path.insert(0, "engine"); sys.path.insert(0, ".")
import cairo, numpy as np
from lib import W, H
CARD = {"A": dict(w=(300, 380), h=(190, 250), banned=r"vespa|piaggio|\btext\(", fn="draw"),
        "B": dict(w=(900, 1100), h=(360, 450), banned=r"golden|\btext\(", fn="draw"),
        "C": dict(w=(240, 320), h=(150, 220), banned=r"sony|walkman|\btext\(", fn="draw")}
card, path, out = sys.argv[1].upper(), sys.argv[2], sys.argv[3]; os.makedirs(out, exist_ok=True); C = CARD[card]
res = []
def chk(name, ok, val=""): res.append(bool(ok)); print(("PASS " if ok else "FAIL ") + name + (f": {val}" if val != "" else ""))
src = open(path).read(); chk("<= 300 lines", src.count("\n") <= 300, src.count("\n"))
chk("no banned text/brand", not re.search(C["banned"], src, re.I))
spec = importlib.util.spec_from_file_location("asset_mod", path); mod = importlib.util.module_from_spec(spec)
try: spec.loader.exec_module(mod); f = mod.draw
except Exception as e: chk("imports and has draw()", False, repr(e)); print("SUMMARY", json.dumps(dict(card=card, passed=0, total=len(res)))); sys.exit(1)
def render(x, y, s):
    sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(sf); c.set_source_rgb(0.93, 0.93, 0.93); c.paint()
    t0 = time.time(); f(c, x, y, s); dt = time.time() - t0
    a = np.frombuffer(sf.get_data(), np.uint8).reshape(H, W, 4)[:, :, :3].astype(int); m = np.abs(a - 237).sum(2) > 24; ys, xs = np.where(m)
    return sf, a, m, (xs.min(), xs.max(), ys.min(), ys.max()) if len(xs) else None, dt
try:
    sf, a, m, bb, dt = render(640, 640, 1.0)
    sf2, _, _, bb2, _ = render(300, 500, 0.5)
except Exception as e: chk("runs without error", False, repr(e)); print("SUMMARY", json.dumps(dict(card=card, passed=0, total=len(res)))); sys.exit(1)
chk("runs without error", True); chk("draws something", bb is not None)
if bb:
    w, h = bb[1] - bb[0], bb[3] - bb[2]
    chk("draws in < 1 s", dt < 1.0, f"{dt:.2f}s"); chk(f"width {C['w']}", C["w"][0] <= w <= C["w"][1], w); chk(f"height {C['h']}", C["h"][0] <= h <= C["h"][1], h)
    chk("bottom edge within 10 px of y", abs(bb[3] - 640) <= 10, bb[3] - 640); chk("centred within 45 px of x", abs((bb[0] + bb[1])/2 - 640) <= 45, round((bb[0] + bb[1])/2 - 640))
    if bb2: chk("scales with s (0.5 -> 40-60% size)", 0.4*w <= (bb2[1] - bb2[0]) <= 0.6*w, bb2[1] - bb2[0])
    px = a[m]; q = (px // 24); keys, cnt = np.unique(q[:, 0]*10000 + q[:, 1]*100 + q[:, 2], return_counts=True)
    main = int((cnt > 0.01*len(px)).sum()); chk("flat palette: 4-16 colours with > 1% share", 4 <= main <= 16, main)
    lum = px.mean(1); chk("INK outline present (1.5-30% dark pixels)", 0.015 <= (lum < 60).mean() <= 0.30, f"{(lum < 60).mean():.3f}")
    sf.write_to_png(f"{out}/{card}.png")
    # crop for judging
    s2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(w + 80), int(h + 80)); c2 = cairo.Context(s2); c2.set_source_rgb(.93, .93, .93); c2.paint()
    c2.set_source_surface(sf, 40 - bb[0], 40 - bb[2]); c2.paint(); s2.write_to_png(f"{out}/{card}_crop.png")
print("SUMMARY", json.dumps(dict(card=card, passed=sum(res), total=len(res))))
sys.exit(0 if all(res) else 1)
