"""Episode assembly. Copy this folder to episodes/<slug>/ and edit. Run from the kit root:
   SHOTS=S03,S04 RENDER_SCALE=1 python3 engine/sheet.py episodes.<slug>.film out.jpg     preview shots (720p, fast)
   python3 engine/audit.py episodes.<slug>.film          variety + beat gap + registered-names check (exit 1 = fix first)
   python3 engine/layout_check.py episodes.<slug>.film   text over faces / clipped text / duplicate shot keys
   python3 engine/build.py episodes.<slug>.film out.mp4  full render, 1080p
Inputs in this folder: narration.wav, words.json, segs.json, END.txt (tools/prep_audio.py), lines.py (one line per shot)."""
import sys, os, json
K = os.getcwd(); sys.path.insert(0, K); sys.path.insert(0, os.path.join(K, "engine"))
import library.register                                         # shared library into the registries
import scene_v2
EP = os.path.dirname(os.path.abspath(__file__)); SLUG = os.path.basename(EP)
try:
    import importlib; importlib.import_module(f"episodes.{SLUG}.setup_ep").setup(scene_v2)   # this episode's own new assets (optional)
except ModuleNotFoundError: pass
from importlib import import_module
L = import_module(f"episodes.{SLUG}.lines").L
WORDS = json.load(open(f"{EP}/words.json")); END = float(open(f"{EP}/END.txt").read())
SEGS = json.load(open(f"{EP}/segs.json"))
for j, s in enumerate(SEGS):
    nxt = SEGS[j+1]["start"] if j + 1 < len(SEGS) else END
    idx = [i for i, w in enumerate(WORDS) if s["start"] - 0.05 <= w["t0"] < nxt - 0.05]; s["i0"], s["n"] = (idx[0], len(idx)) if idx else (0, 0)
ONLY = os.environ.get("SHOTS")
SHOTS = scene_v2.build_shots({s["id"]: L.get(s["id"], "bg dark") for s in SEGS}, SEGS, WORDS, END)
SEL = [(sid, sh) for sid, sh in SHOTS if not ONLY or sid in ONLY.split(",")]
SCENES = [(sh.dur, sh.draw) for _, sh in SEL]
CUES = scene_v2.thin_cues([(i + 1, max(0.0, t), n, g) for i, (_, sh) in enumerate(SEL) for t, n, g in sh.cues if t < sh.dur])
NARRATION = f"{EP}/narration.wav" if not ONLY else None; NARRATION_OFFSET = 0.0
MUSIC = []            # [(start_s, "music_somber"|"music_hopeful"|"music_upbeat"|"music_tension"|"music_reflective"), ...] one bed per chapter
AUDIT = dict()        # per-episode overrides, see engine/audit.py
