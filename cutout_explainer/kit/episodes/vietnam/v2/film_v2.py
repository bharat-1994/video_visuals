"""V2 film assembly (director-written; Qwen does not need to edit this file unless an import name differs).
   SHOTS=S16,S17 python3 engine/sheet.py episodes.vietnam.v2.film_v2 out.jpg     (preview)
   python3 engine/build.py episodes.vietnam.v2.film_v2 vietnam_v2.mp4              (full film)
Needs (written by Qwen): engine/scene_v2.py, episodes/vietnam/v2/setup_v2.py (+ assets_v2.py, audio/sfx_v2.py)."""
import sys, os, json, importlib.util
K = os.getcwd(); sys.path.insert(0, K); sys.path.insert(0, os.path.join(K, "engine"))
from episodes.vietnam import film_setup                      # v1 registries (into engine/scene.py)
import scene, scene_v2
for d in ("BG", "ASSETS", "CAST", "CUSTOM", "AMBIENCE"): getattr(scene_v2, d).update(getattr(scene, d))
from episodes.vietnam.v2 import setup_v2                      # v2 registries + overrides (into scene_v2)
from episodes.vietnam.key import SHOT_FNS as KEY
from episodes.vietnam.v2.film_v2_lines import merged

EP = os.path.join(K, "episodes", "vietnam")
src = open(os.path.join(EP, "film.py")).read()
L = eval(src[src.index("L = {") + 4: src.index("\n}\n", src.index("L = {")) + 2])   # v1 lines (not executed)
L = merged(L)

WORDS = json.load(open(os.path.join(EP, "words.json"))); END = 608.76
act1 = json.load(open(os.path.join(EP, "shots.json")))["shots"]
SEGS = [{"id": s["id"], "start": s["start"]} for s in act1] + json.load(open(os.path.join(EP, "segs.json")))
for j, s in enumerate(SEGS):
    nxt = SEGS[j+1]["start"] if j + 1 < len(SEGS) else END
    idx = [i for i, w in enumerate(WORDS) if s["start"] - 0.05 <= w["t0"] < nxt - 0.05]
    s["i0"], s["n"] = (idx[0], len(idx)) if idx else (0, 0)
ACT1_CUES = {s["id"]: s["sfx"] for s in act1 if s["id"] in KEY}

ONLY = os.environ.get("SHOTS")
SHOTS = scene_v2.build_shots({s["id"]: L.get(s["id"], "bg dark") for s in SEGS}, SEGS, WORDS, END)
SEL = [(sid, sh) for sid, sh in SHOTS if not ONLY or sid in ONLY.split(",")]
def _fn(sid, sh):
    f = KEY.get(sid) or sh.draw
    def g(ctx, t, dur): f(ctx, t, dur)
    g.__name__ = sid.lower(); return g
SCENES = [(sh.dur, _fn(sid, sh)) for sid, sh in SEL]
CUES = []
for i, (sid, sh) in enumerate(SEL):
    cues = [(t, scene_v2.remap_key_cue(n), g) for n, t, g in ACT1_CUES[sid]] if sid in KEY else sh.cues
    CUES += [(i + 1, max(0.0, t), n, g) for t, n, g in cues if t < sh.dur]
CUES = scene_v2.thin_cues(CUES)                               # global sound rules (see REVISION_v2.md section 3)
SUBS = [None]*len(SEL)
NARRATION = "episodes/vietnam/narration.wav" if not ONLY else None
NARRATION_OFFSET = 0.0
# chapter music (build_v2.py crossfades 1.5 s between beds; each bed loops seamlessly)
MUSIC = [(0.0, "music_somber"), (160.9, "music_hopeful"), (252.9, "music_upbeat"), (396.8, "music_tension"), (507.2, "music_reflective")]
AUDIT = dict(asset_ok={"sticky", "paper", "city_card"}, exempt_run={"kitchen"}, skip={"S01", "S12", "S14", "S15"}, motion_ok={"S16", "S28", "S34", "S53", "S90", "S104", "S111", "S129", "S142", "S145"})
