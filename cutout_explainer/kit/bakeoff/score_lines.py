"""Objective checks for card D. python3 bakeoff/score_lines.py <lines_D.py> <out_dir>
Builds the ten shots (S60-S69 of the Vietnam narration) from the model's lines against the shared library, then reports:
parse/registry errors, beat gap, layout (text on face / clipped / overlap), bg and asset variety, people share, sounds; writes sheet.jpg."""
import sys, os, json, importlib.util, collections, subprocess, cairo, re
sys.path.insert(0, "engine"); sys.path.insert(0, ".")
path, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
IDS = [f"S{i}" for i in range(60, 70)]
src = open(path).read(); res = []
def chk(name, ok, val=""): res.append(bool(ok)); print(("PASS " if ok else "FAIL ") + name + (f": {val}" if val != "" else ""))
ids_in_file = re.findall(r'["\'](S\d+)["\']\s*:', src); chk("each shot id appears exactly once", sorted(ids_in_file) == sorted(IDS), ids_in_file)
spec = importlib.util.spec_from_file_location("lines_mod", path); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); L = mod.L
chk("all ten ids present", all(i in L for i in IDS))
import layout_check  # noqa  (patches lib first so every asset is observed)
import library.register  # noqa
import scene_v2 as S
from beats import max_gap
EP = "episodes/vietnam"; W = json.load(open(f"{EP}/words.json")); END = 608.76
segs = [{"id": s["id"], "start": s["start"]} for s in json.load(open(f"{EP}/shots.json"))["shots"]] + json.load(open(f"{EP}/segs.json"))
for j, s in enumerate(segs):
    nx = segs[j+1]["start"] if j + 1 < len(segs) else END; idx = [i for i, w in enumerate(W) if s["start"] - 0.05 <= w["t0"] < nx - 0.05]; s["i0"], s["n"] = idx[0], len(idx)
try: shots = [(sid, sh) for sid, sh in S.build_shots({s["id"]: L.get(s["id"], "bg flat") for s in segs}, segs, W, END) if sid in IDS]
except Exception as e: chk("lines parse and every @word exists", False, repr(e)[:300]); print("SUMMARY", json.dumps(dict(card="D", passed=0, total=len(res)))); sys.exit(1)
chk("lines parse and every @word exists", True)
miss = set(); bgs = collections.Counter(); assets = collections.Counter(); people = 0; seq = []
for sid, sh in shots:
    bg = next((e["pos"][0] for e in sh.els if e["typ"] == "bg" and e["pos"]), "card" if any(e["typ"] == "card" for e in sh.els) else "none"); bgs[bg] += 1; seq.append(bg)
    if bg not in ("card", "none") and bg not in S.BG: miss.add("bg:" + bg)
    for e in sh.els:
        if e["typ"] == "a": assets[e["pos"][0]] += 1; (e["pos"][0] in S.ASSETS) or miss.add("asset:" + e["pos"][0])
        if e["typ"] == "p": (e["pos"][0] in S.CAST) or miss.add("cast:" + e["pos"][0])
        if e["typ"] == "fn": (e["pos"][0] in S.CUSTOM) or miss.add("fn:" + e["pos"][0])
    people += any(e["typ"] == "p" for e in sh.els)
chk("every name exists in the library", not miss, sorted(miss))
slow = [f"{sid}:{max_gap(sh):.1f}s" for sid, sh in shots if max_gap(sh) > 2.5]; chk("beat gap <= 2.5 s", not slow, slow)
chk("no bg used more than twice", max(bgs.values()) <= 2, bgs.most_common(3)); chk("no 3 same bg in a row", not any(seq[i] == seq[i-1] == seq[i-2] for i in range(2, len(seq))))
chk("dark/spotlight bg at most once", bgs["dark"] + bgs.get("spotlight", 0) <= 1)
chk("at most one map-type asset", sum(v for k, v in assets.items() if "map" in k) <= 1)
F = layout_check.check([(sh.dur, sh.draw) for _, sh in shots], [sid for sid, _ in shots])
for f in F: print("   ", f)
chk("layout: no text on faces / clipped / overlapping", not F, len(F))
sheetd = os.path.join(out, "_f"); os.makedirs(sheetd, exist_ok=True); i = 0
for sid, sh in shots:
    for t in (0.4, sh.dur*0.85):
        sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1280, 720); c = cairo.Context(sf); c.set_source_rgb(1, 1, 1); c.paint(); sh.draw(c, min(t, sh.dur - 0.02), sh.dur); sf.write_to_png(f"{sheetd}/{i:02d}.png"); i += 1
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{sheetd}/%02d.png", "-vf", "scale=640:-1,tile=2x10", "-frames:v", "1", f"{out}/sheet.jpg"])
print("SUMMARY", json.dumps(dict(card="D", passed=sum(res), total=len(res)))); sys.exit(0 if all(res) else 1)
