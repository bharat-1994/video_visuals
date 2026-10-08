"""Automatic layout checker: python3 engine/layout_check.py <episode_module> [SHOTS=S1,S2]
Renders every shot at 4 times with drawing hooks and reports, per shot/time:
  TEXT_ON_FACE   a text box overlaps a character's head circle (dialogue ticks excluded)
  TEXT_CLIPPED   a text box leaves the 1280x720 frame (after camera)
  TEXT_OVERLAP   two different text boxes overlap by > 25% of the smaller one
  HEAD_CLIPPED   a head circle is more than 35% outside the frame
  DUP_KEY        (separate) a shot id defined twice in a *_lines.py / film.py file (later one silently wins)
Exit 1 if anything is found. Heads/text only; prop-over-face still needs the contact sheet."""
import sys, os, ast, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.getcwd())
import cairo, lib
REC = []; _BG = [False]   # text drawn by a background (signs on walls) is scenery, not a caption
_text, _head, _back = lib.text, lib.Puppet._head, lib.Puppet._back_head
def _tx(ctx, x, y): return ctx.get_matrix().transform_point(x, y)
def text(ctx, s, x, y, size=48, c=(1, 1, 1), anchor="c", reveal=1.0, rot=0, outline=None):
    ctx.save(); ctx.select_font_face(lib.FONT); ctx.set_font_size(size); w = ctx.text_extents(s).width; ctx.restore()
    x0 = x + {"c": -w/2, "l": 0, "r": -w}[anchor]
    p = [_tx(ctx, x0, y - size*0.6), _tx(ctx, x0 + w, y + size*0.35)]
    if reveal >= 0.99 and s.strip() and not _BG[0]: REC.append(("text", s, min(p[0][0], p[1][0]), min(p[0][1], p[1][1]), max(p[0][0], p[1][0]), max(p[0][1], p[1][1])))
    return _text(ctx, s, x, y, size, c, anchor, reveal, rot, outline)
def head(orig):
    def f(self, ctx, hx, hy, R, *a, **k):
        cx, cy = _tx(ctx, hx, hy); sc = math.hypot(*ctx.get_matrix().transform_distance(R, 0))
        REC.append(("head", "", cx, cy, sc, 0)); return orig(self, ctx, hx, hy, R, *a, **k)
    return f
lib.text = text; lib.Puppet._head = head(_head); lib.Puppet._back_head = head(_back)
import scene_v2 as _sv2
_bgf = _sv2.Shot._bg
def _bg_wrap(self, ctx, t, el):
    _BG[0] = True
    try: return _bgf(self, ctx, t, el)
    finally: _BG[0] = False
_sv2.Shot._bg = _bg_wrap
def circ_rect(cx, cy, r, b):
    nx, ny = max(b[0], min(cx, b[2])), max(b[1], min(cy, b[3])); return (cx-nx)**2 + (cy-ny)**2 < (r*0.8)**2
def check(scenes, ids, sel=None, quiet=False):
    """scenes [(dur, fn)], ids [shot id per scene] -> list of 'SID: FINDING' strings. Import this module BEFORE any asset module
    (it patches lib.text / Puppet._head so the hooks see every draw call)."""
    out = []; W, H = lib.W, lib.H; surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    for i, (dur, fn) in enumerate(scenes):
        sid = ids[i] if i < len(ids) else f"#{i+1}"
        if sel and sid not in sel: continue
        found = set()
        for t in (0.5, dur*0.4, dur*0.7, dur*0.95):
            REC.clear(); ctx = cairo.Context(surf); ctx.set_source_rgb(1, 1, 1); ctx.paint()
            try: fn(ctx, min(t, dur - 0.02), dur)
            except Exception as e: found.add(f"CRASH {type(e).__name__}: {e}"); continue
            T = [r for r in REC if r[0] == "text"]; Hd = [r for r in REC if r[0] == "head"]
            for r in T:
                b = r[2:]
                if b[0] < -4 or b[1] < -4 or b[2] > W + 4 or b[3] > H + 4: found.add(f"TEXT_CLIPPED '{r[1][:28]}'")
                for h in Hd:
                    if circ_rect(h[2], h[3], h[4], b): found.add(f"TEXT_ON_FACE '{r[1][:28]}'")
            for a in range(len(T)):
                for b2 in range(a+1, len(T)):
                    A, B = T[a], T[b2]
                    if A[1] == B[1]: continue
                    ox = min(A[4], B[4]) - max(A[2], B[2]); oy = min(A[5], B[5]) - max(A[3], B[3])
                    if ox > 0 and oy > 0 and ox*oy > 0.25*min((A[4]-A[2])*(A[5]-A[3]), (B[4]-B[2])*(B[5]-B[3])): found.add(f"TEXT_OVERLAP '{A[1][:20]}' / '{B[1][:20]}'")
            for h in Hd:
                if h[2] - h[4] < -0.35*2*h[4] or h[2] + h[4] > W + 0.35*2*h[4]: found.add("HEAD_CLIPPED")
        out += [f"{sid}: {f}" for f in sorted(found)]
    return out
if __name__ == "__main__":
    import importlib
    m = importlib.import_module(sys.argv[1]); only = os.environ.get("SHOTS")
    ids = [s for s, _ in getattr(m, "SHOTS", [])] or [f"#{i+1}" for i in range(len(m.SCENES))]
    F = check(m.SCENES, ids, set(only.split(",")) if only else None); bad = len(F)
    for f in F: print(f)
    # duplicate shot keys in any lines file next to the module / under episodes
    def dups(path):
        try: tree = ast.parse(open(path).read())
        except Exception: return
        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                ks = [k.value for k in node.keys if isinstance(k, ast.Constant) and isinstance(k.value, str) and k.value[:1] == "S" and k.value[1:].isdigit()]
                for k in set(ks):
                    if ks.count(k) > 1: print(f"DUP_KEY {k} appears {ks.count(k)}x in {path} (the last one wins)"); globals()["bad"] += 1
    for root, _, fs in os.walk(os.path.join(os.getcwd(), "episodes")):
        for f in fs:
            if f.endswith(".py") and ("lines" in f or f.startswith("film")): dups(os.path.join(root, f))
    print("layout check:", "CLEAN" if not bad else f"{bad} finding(s)"); sys.exit(1 if bad else 0)
