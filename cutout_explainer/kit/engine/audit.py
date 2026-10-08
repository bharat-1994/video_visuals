"""Variety / boredom audit from the shot data (no rendering). python3 engine/audit.py <film_module> [--strict]
The film module must expose SHOTS = [(sid, Shot)] (scene_v2.build_shots). Optional module dict AUDIT overrides limits:
  AUDIT = dict(dark=10, flat=6, bg_max_frac=0.08, asset_max=12, people_min=0.55, gap=2.5, ship=5, factory=4, map_family=14, maps=set(...), exempt_run={"kitchen"})
Checks (HARD = exit 1):
  bg 'dark'/'flat' caps · no bg in more than bg_max_frac of shots · no asset used more than asset_max times (except ASSET_OK)
  people share >= people_min · beat gap <= gap s (something new tied to a narration word) · no 3 identical bgs in a row
  every asset/bg/cast/fn name used exists in the registries · pop_soft share of entrance sounds <= 10%"""
import sys, os, importlib, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.getcwd())
import scene_v2 as S
from beats import max_gap
m = importlib.import_module(sys.argv[1]); shots = m.SHOTS; n = len(shots)
A = dict(dark=10, flat=6, bg_max_frac=0.08, asset_max=12, people_min=0.55, gap=2.5, ship=5, factory=4, map_family=14,
         maps={"vietnam_map", "caged_map", "map"}, exempt_run=set(), asset_ok={"sticky", "paper"}, skip=set()); A.update(getattr(m, "AUDIT", {}))
bgs, assets, people, seq, missing, pops, ent = collections.Counter(), collections.Counter(), 0, [], set(), 0, 0
for sid, sh in shots:
    bg = next((e["pos"][0] for e in sh.els if e["typ"] == "bg" and e["pos"]), "card" if any(e["typ"] == "card" for e in sh.els) else "none")
    bgs[bg] += 1; seq.append(bg)
    if bg not in ("card", "none", "flat", "dark") and bg not in S.BG: missing.add(f"bg:{bg}")
    for e in sh.els:
        if e["typ"] == "a":
            assets[e["pos"][0]] += 1
            if e["pos"][0] not in S.ASSETS: missing.add(f"asset:{e['pos'][0]}")
        if e["typ"] == "fn":
            assets["fn:" + e["pos"][0]] += 1
            if e["pos"][0] not in S.CUSTOM: missing.add(f"fn:{e['pos'][0]}")
        if e["typ"] == "fx" and e["pos"] and e["pos"][0] not in S.FX: missing.add(f"fx:{e['pos'][0]}")
        if e["typ"] == "p" and e["pos"] and e["pos"][0] not in S.CAST: missing.add(f"cast:{e['pos'][0]}")
    people += any(e["typ"] == "p" for e in sh.els)
    for t, nm, g in sh.cues:
        if nm.startswith("auto:"): ent += 1; pops += nm == "auto:pop_soft"
slow = [f"{sid}:{max_gap(sh):.1f}s" for sid, sh in shots if sid not in A["skip"] and max_gap(sh) > A["gap"]]
runs = [seq[i] for i in range(2, n) if seq[i] == seq[i-1] == seq[i-2] and seq[i] not in A["exempt_run"]]
top_bg = bgs.most_common(1)[0]; maps = sum(v for k, v in assets.items() if k in A["maps"] or k.replace("fn:", "") in A["maps"])
over = {k: v for k, v in assets.items() if v > A["asset_max"] and k not in A["asset_ok"]}
checks = [(f"bg 'dark' <= {A['dark']}", bgs["dark"], bgs["dark"] <= A["dark"]), (f"bg 'flat' <= {A['flat']}", bgs["flat"], bgs["flat"] <= A["flat"]),
 (f"no bg in > {A['bg_max_frac']:.0%} of shots", top_bg, top_bg[1] <= max(4, A["bg_max_frac"]*n)),
 (f"no asset used > {A['asset_max']}x", over, not over), (f"map-family <= {A['map_family']}", maps, maps <= A["map_family"]),
 (f"people in >= {A['people_min']:.0%} of shots", f"{people}/{n}", people >= A["people_min"]*n),
 (f"beat gap <= {A['gap']} s", slow, not slow), ("no 3 identical bgs in a row", runs, not runs),
 ("every name used is registered", sorted(missing), not missing), ("pop_soft <= 10% of entrance sounds", f"{pops}/{ent}", ent == 0 or pops <= 0.1*ent)]
bad = 0
for name, val, ok in checks: print(("PASS " if ok else "FAIL ") + f"{name}: {val}"); bad += not ok
print("\nbackgrounds:", bgs.most_common(10)); print("top assets:", assets.most_common(10)); sys.exit(1 if bad else 0)
