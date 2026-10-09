<!-- SIZE w=492-627 h=352-448 banned= -->
# Task: balance_scale
File: `asset_balance_scale.py`, function `draw(ctx, x, y, s=1.0)`. (x, y) = bottom-centre of the picture. Everything scales with s.
Size at s=1: about 560 x 400 px (window 492-627 x 352-448).
Real thing: a classic two-pan balance. Draw the real kind of object, not a generic box. No brand names, logos or emblems; no text unless a feature asks for it.
Signature features (all must be recognisable; number them in a comment before coding):
1. central pillar with a stepped base
2. horizontal beam with a triangle fulcrum on top
3. two chains to two shallow pans
4. tilt param (0 = level)
5. function exposes pan centres in a comment so items can sit on them
6. small tick scale on the pillar

Scorer: `python3 bakeoff/score.py episodes/nike_adidas/TASKS/balance_scale.md asset_balance_scale.py out/balance_scale`
Reply format and budgets: see the pack (RULES.md). Update episodes/nike_adidas/STATE.md with "done balance_scale" when finished.
