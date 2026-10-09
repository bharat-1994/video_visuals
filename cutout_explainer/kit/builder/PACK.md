<!-- bakeoff/RULES.md -->
# Builder rules (every builder session gets this + the cheatsheet [+ scene grammar and catalog names for shot lines] + its task cards)

You build a BATCH of items (props, or shot lines) for one episode. Read only: this pack, your task cards, and `episodes/<slug>/STATE.md`.
Do not read engine/lib.py, other assets or other episodes. Never edit an existing file; write only the files named in your cards.

Budgets (hard; stop and report if you hit one):
- Per item: at most TWO scorer runs and ONE look at your own output image. No extra zooms, no helper agents.
- Keep tool output short: pipe scorer output through `| tail -20`. Do not paste whole files back to yourself.
- At most about 60 tool calls per session. When you finish or run out, write STATE.md (below) and stop; a fresh session continues from it.

Style: flat fills, 2-3 tones per material, INK outlines 2-3 px, details via loops, no gradients, no emblems, no brand logos or names.
Draw the real kind of object. Beautiful, clean, readable shapes beat clutter. No decorative motion: a still picture is fine.

Before coding an item, write a comment listing the numbered signature features from its card.
After each item, append one line to `episodes/<slug>/STATE.md`:  `done <name>: scorer <passed>/<total>, flaws: <one line>`  (or `blocked <name>: <why>`).
Final reply, per item: FEATURES (each numbered feature YES/NO, honest, a person will check) · runs used · known flaws · anything unclear in the card.
Read the scorer's own words for what failed (values are fractions: 0.339 means 33.9%).


---

<!-- bakeoff/LIB_CHEATSHEET.md -->
# lib cheatsheet (everything you need from engine/lib.py; do not read lib.py)

Canvas 1280x720, y grows downward. `from lib import *` gives all of these plus INK (outline colour) and FONT.

```
hexc(h)
clamp(x, a=0, b=1)
lerp(a, b, t)
box(ctx, x, y, w, h, c, r=0, line=None, lw=3)
rrect(ctx, x, y, w, h, r)
circle(ctx, x, y, r, c, line=None, lw=3, a=1)
ellipse(ctx, x, y, rx, ry, c, a=1)
poly(ctx, pts, c, line=None, lw=3, a=1)
line(ctx, pts, c=(0.08, 0.08, 0.1), lw=6, a=1)
hose(ctx, p0, p1, bend=0.25, lw=9, c=(0.08, 0.08, 0.1))   # rubber-hose limb: curved stroke from p0 to p1; bend>0 bows to the right of travel.
text(ctx, s, x, y, size=48, c=(1, 1, 1), anchor='c', reveal=1.0, rot=0, outline=None)   # handwritten text; reveal 0..1 = typewriter.
smooth(ctx, pts, start=True)   # Catmull-Rom spline through pts (continues current path unless start).
```

`box(ctx, x, y, w, h, ...)` takes the TOP-LEFT corner; `circle`/`ellipse` take the CENTRE; `text(ctx, s, x, y)` is centred on x by default.
Colours are RGB tuples 0..1; `hexc('#e5b73b')` makes one (6-digit hex only).
`poly(ctx, pts, fill, line=INK, lw=3)` fills a closed polygon; `smooth(ctx, pts)` adds a smooth path you then fill/stroke yourself.
`ctx` is a pycairo Context: ctx.save()/restore(), translate, scale, rotate, arc, curve_to are all allowed.
Style: flat fills, 2 or 3 tones per material (base, shadow side, highlight), INK outlines 2-3 px, small repeated details via loops, no gradients, no blur, no emblems or logos.
