"""Assembles Act 1 in shot order. Run from the kit root:
   python3 engine/sheet.py episodes.vietnam.act1 review.jpg      (contact sheet)
   python3 engine/build.py episodes.vietnam.act1 act1.mp4        (video + narration + all SFX)
Durations and ALL sound cues come from shots.json, so builders never write CUES.
Shots that no module provides yet render as a grey placeholder card."""
import sys, os, json, importlib; sys.path.insert(0, os.getcwd())
from episodes.vietnam.assets import *

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = json.load(open(os.path.join(HERE, "shots.json")))["shots"]
FNS = {}
for mod in ("key", "batch_01"):
    try: FNS.update(importlib.import_module(f"episodes.vietnam.{mod}").SHOT_FNS)
    except ModuleNotFoundError as e:
        if mod not in str(e): raise

def _placeholder(sp):
    def f(ctx, t, dur):
        bg_flat(ctx, hexc('#3a3a42')); text(ctx, sp["id"] + "  (to build)", 640, 300, 64)
        text(ctx, sp["narration"], 640, 400, 36, hexc('#cfcfcf'))
    return f

ONLY = os.environ.get("SHOTS")                 # e.g. SHOTS=S02,S03 to preview a subset (sound cues still follow)
SEL = [s for s in SPEC if not ONLY or s["id"] in ONLY.split(",")]
SCENES = [(s["dur"], FNS.get(s["id"], _placeholder(s))) for s in SEL]
CUES = [(i+1, t, name, db) for i, s in enumerate(SEL) for name, t, db in s["sfx"]]
SUBS = [None]*len(SEL)                         # narration is voiced; no subtitles
NARRATION = "episodes/vietnam/narration.wav" if not ONLY else None
NARRATION_OFFSET = 0.0
