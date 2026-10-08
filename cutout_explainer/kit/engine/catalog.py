"""Asset catalog with pictures. python3 engine/catalog.py <film_module> <out_dir>
Writes <out_dir>/CATALOG.md (name, call signature, one-line doc, drawn size) and thumbnail sheets
catalog_assets_N.jpg / catalog_bgs_N.jpg / catalog_cast.jpg (24 tiles per sheet, name under each tile).
Builders and directors LOOK at these sheets and reuse before drawing anything new."""
import sys, os, importlib, inspect, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.getcwd())
import cairo, numpy as np
import scene_v2 as S
from lib import W, H, text, hexc
importlib.import_module(sys.argv[1]); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
def tile(draw, label):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); c.set_source_rgb(0.93, 0.93, 0.93); c.paint()
    err = None
    try: draw(c)
    except Exception as e: err = f"{type(e).__name__}: {str(e)[:60]}"
    a = np.frombuffer(s.get_data(), np.uint8).reshape(H, W, 4)[:, :, :3].astype(int)
    d = np.abs(a - 237).sum(2) > 24; ys, xs = np.where(d)
    size = (int(xs.max() - xs.min()), int(ys.max() - ys.min())) if len(xs) else (0, 0)
    TW, TH = 480, 320; t = cairo.ImageSurface(cairo.FORMAT_ARGB32, TW, TH); k = cairo.Context(t); k.set_source_rgb(0.93, 0.93, 0.93); k.paint()
    if len(xs):
        bw, bh = max(8, xs.max() - xs.min() + 1), max(8, ys.max() - ys.min() + 1); sc = min((TW - 40)/bw, (TH - 70)/bh, 3.0)
        k.save(); k.translate(TW/2, 36 + (TH - 36)/2); k.scale(sc, sc); k.set_source_surface(s, -(xs.min() + bw/2), -(ys.min() + bh/2)); k.paint(); k.restore()
    k.set_source_rgb(0, 0, 0); k.rectangle(0, 0, TW, 30); k.fill(); text(k, label + (" !" if err else ""), 8, 17, 22, (1, 1, 1), anchor="l")
    return t, size, err
def sheets(items, prefix):
    rows = []
    for i in range(0, len(items), 24):
        d = tempfile.mkdtemp()
        for j, (nm, s) in enumerate(items[i:i+24]): s.write_to_png(f"{d}/{j:02d}.png")
        n = len(items[i:i+24]); subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/%02d.png", "-vf", f"tile=4x{(n+3)//4}", "-frames:v", "1", f"{out}/{prefix}_{i//24+1}.jpg"])
md = ["# Asset catalog (generated; look at the sheets next to this file)\n", "| kind | name | call | what | drawn size px | note |", "|---|---|---|---|---|---|"]
for kind, reg in (("asset", S.ASSETS), ("bg", S.BG)):
    items = []
    for nm in sorted(reg):
        f = reg[nm]; sig = inspect.signature(f)
        req = [p for p in list(sig.parameters.values())[(1 if kind == "bg" else 3):] if p.default is inspect._empty and p.kind in (p.POSITIONAL_OR_KEYWORD,)]
        def draw(c, f=f, kind=kind, sig=sig):
            kw = {"t": 1.0} if "t" in sig.parameters else {}
            if kind == "bg": f(c, **kw)
            else: f(c, 640, 520, **kw)
        s, size, err = tile(draw, nm)
        if not err: items.append((nm, s))
        doc = (inspect.getdoc(f) or "").split("\n")[0][:90]
        md.append(f"| {kind} | `{nm}` | `{nm}{str(sig)[:70]}` | {doc} | {size[0]}x{size[1]} | {'needs args: ' + ','.join(p.name for p in req) if err else ''} |")
    sheets(items, f"catalog_{kind}s")
items = []
for nm in sorted(S.CAST):
    s, size, err = tile(lambda c, nm=nm: S.CAST[nm](1.0).draw(c, 640, 640, 0.5, "neutral"), nm); items.append((nm, s))
    md.append(f"| cast | `{nm}` | `p {nm} x y [scale]` | puppet | {size[0]}x{size[1]} | {'error' if err else ''} |")
sheets(items, "catalog_cast")
open(f"{out}/CATALOG.md", "w").write("\n".join(md) + "\n"); print(out, len(md) - 3, "entries")
