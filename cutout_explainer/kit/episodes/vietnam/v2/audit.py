"""Objective boredom/variety audit of a film's shot lines. Run from the kit root:
   python3 episodes/vietnam/v2/audit.py            -> audits v1 lines merged with v2 replacements
   python3 episodes/vietnam/v2/audit.py v1         -> audits v1 only
Text analysis of the shot lines + word timings (needs no assets). Exit code 1 if any HARD limit fails."""
import sys, os, re, collections, json
sys.path.insert(0, os.path.join(os.getcwd(), "engine")); sys.path.insert(0, os.getcwd())
from scene import _split
import importlib.util
def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
src = open("episodes/vietnam/film.py").read()
L = eval(src[src.index("L = {") + 4: src.index("\n}\n", src.index("L = {")) + 2])
if not (len(sys.argv) > 1 and sys.argv[1] == "v1"):
    L = load("episodes/vietnam/v2/film_v2_lines.py", "v2l").merged(L)
KEY = {"S01": "bg dark | a vietnam_map", "S12": "bg dark | a caged_map", "S14": "bg dark | a caged_map | a ussr_pillar", "S15": "bg dark | a caged_map | a ussr_pillar"}
segs = json.load(open("episodes/vietnam/shots.json"))["shots"]
ids = [s["id"] for s in segs] + [s["id"] for s in json.load(open("episodes/vietnam/segs.json"))]
MAPS = {"vietnam_map", "caged_map", "fn:asia", "fn:vnpins", "fn:cage_lift", "fn:cracks"}
bgs, assets, people, dyn, seq = collections.Counter(), collections.Counter(), 0, 0, []
for sid in ids:
    line = KEY.get(sid) or L.get(sid, "bg dark")
    els = [_split(e) for e in line.split(" | ")]
    bg = next((e[1] for e in els if e[0] == "bg" and len(e) > 1), "card" if any(e[0] == "card" for e in els) else "none")
    if bg == "flat": bg = "flat"
    bgs[bg] += 1; seq.append(bg)
    for e in els:
        if e[0] == "a": assets[e[1]] += 1
        if e[0] == "fn": assets["fn:" + e[1]] += 1
    people += any(e[0] == "p" for e in els)
    dyn += any(e[0] in ("fx",) or any(t.startswith(("walk=", "move=")) for t in e) or (e[0] == "cam" and len(e) > 1 and e[1] in ("track", "whip")) for e in els)
import scene
from episodes.vietnam.v2.beats import max_gap
W = json.load(open("episodes/vietnam/words.json")); S = [{"id": s["id"], "start": s["start"]} for s in segs] + json.load(open("episodes/vietnam/segs.json"))
for j, s in enumerate(S):
    nx = S[j+1]["start"] if j + 1 < len(S) else 608.76; idx = [i for i, w in enumerate(W) if s["start"] - 0.05 <= w["t0"] < nx - 0.05]; s["i0"], s["n"] = idx[0], len(idx)
slow = []
for j, s in enumerate(S):
    if s["id"] in KEY: continue
    sh = scene.build_shots({s["id"]: L.get(s["id"], "bg dark")}, [s], W, S[j+1]["start"] if j + 1 < len(S) else 608.76)[0][1]
    g = max_gap(sh)
    if g > 2.5: slow.append(f"{s['id']}:{g:.1f}s")
n = len(ids); maps = sum(v for k, v in assets.items() if k in MAPS)
runs = [seq[i] for i in range(2, n) if seq[i] == seq[i-1] == seq[i-2] and seq[i] not in ("kitchen",)]
checks = [
    ("bg 'dark' shots <= 10 (reserved for the cage/map motif)", bgs["dark"], bgs["dark"] <= 10),
    ("bg 'flat' shots <= 6", bgs["flat"], bgs["flat"] <= 6),
    ("no single bg in > 12 shots", bgs.most_common(1)[0], bgs.most_common(1)[0][1] <= 12),
    ("map-family shots <= 14 (incl. cage motif)", maps, maps <= 14),
    ("container_ship <= 5", assets["container_ship"], assets["container_ship"] <= 5),
    ("generic factory <= 4", assets["factory"], assets["factory"] <= 4),
    ("shots with a person >= 55%", f"{people}/{n}", people >= 0.55*n),
    ("no shot has > 2.5 s of speech without a new narration-tied beat", slow, not slow),
    ("no 3 same-bg shots in a row (kitchen run exempt)", runs, not runs),
]
bad = 0
for name, val, ok in checks:
    print(("PASS " if ok else "FAIL ") + f"{name}: {val}"); bad += not ok
print("\nbackgrounds:", bgs.most_common(12)); print("top assets:", assets.most_common(12))
sys.exit(1 if bad else 0)
