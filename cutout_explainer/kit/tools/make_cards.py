"""Expand the asset table in PLAN.md into builder task cards.
   python3 tools/make_cards.py episodes/<slug>/PLAN.md            -> episodes/<slug>/TASKS/<name>.md (one card per asset)
Asset table: lines under the heading '## New assets' in the form
   - name | real thing it is | WxH px at scale 1 | feature; feature; feature; ...      (3-8 features; first word of 'real thing' is the kind)
Optional trailing  | banned=word|word  adds brand words that must not appear in code. Anchor is always bottom-centre at (x, y).
Each card ends with the standard budgets from bakeoff/RULES.md; the scorer reads the SIZE line (window = size -12% .. +12%)."""
import sys, os, re
plan = sys.argv[1]; ep = os.path.dirname(plan); out = os.path.join(ep, "TASKS"); os.makedirs(out, exist_ok=True)
txt = open(plan).read(); sec = txt.split("## New assets", 1)[-1].split("\n## ", 1)[0]
n = 0
for line in sec.splitlines():
    m = re.match(r"^\s*-\s*([a-z0-9_]+)\s*\|\s*([^|]+)\|\s*(\d+)\s*x\s*(\d+)\s*px\s*\|\s*([^|]+)(?:\|\s*banned=(\S+))?\s*$", line)
    if not m: continue
    name, real, w, h, feats, banned = m.group(1), m.group(2).strip(), int(m.group(3)), int(m.group(4)), [f.strip() for f in m.group(5).split(";") if f.strip()], (m.group(6) or "")
    lo = lambda v: int(v*0.88); hi = lambda v: int(v*1.12)
    body = f"""<!-- SIZE w={lo(w)}-{hi(w)} h={lo(h)}-{hi(h)} banned={banned} -->
# Task: {name}
File: `asset_{name}.py`, function `draw(ctx, x, y, s=1.0)`. (x, y) = bottom-centre of the picture. Everything scales with s.
Size at s=1: about {w} x {h} px (window {lo(w)}-{hi(w)} x {lo(h)}-{hi(h)}).
Real thing: {real}. Draw the real kind of object, not a generic box. No brand names, logos or emblems; no text unless a feature asks for it.
Signature features (all must be recognisable; number them in a comment before coding):
""" + "\n".join(f"{i+1}. {f}" for i, f in enumerate(feats)) + f"""

Scorer: `python3 bakeoff/score.py episodes/{os.path.basename(ep)}/TASKS/{name}.md asset_{name}.py out/{name}`
Reply format and budgets: see the pack (RULES.md). Update episodes/{os.path.basename(ep)}/STATE.md with "done {name}" when finished.
"""
    open(os.path.join(out, f"{name}.md"), "w").write(body); n += 1
print(f"{n} cards in {out}")
