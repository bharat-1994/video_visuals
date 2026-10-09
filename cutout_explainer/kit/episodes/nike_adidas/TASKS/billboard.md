<!-- SIZE w=492-627 h=369-470 banned=nike|adidas|swoosh|justdoit -->
# Task: billboard
File: `asset_billboard.py`, function `draw(ctx, x, y, s=1.0)`. (x, y) = bottom-centre of the picture. Everything scales with s.
Size at s=1: about 560 x 420 px (window 492-627 x 369-470).
Real thing: a roadside advertising billboard. Draw the real kind of object, not a generic box. No brand names, logos or emblems; no text unless a feature asks for it.
Signature features (all must be recognisable; number them in a comment before coding):
1. large framed board with a plain slogan text param
2. row of six lamps on a top bar
3. two steel posts with a catwalk and railing
4. ladder on the side
5. ground shadow
6. accepts board colour

Scorer: `python3 bakeoff/score.py episodes/nike_adidas/TASKS/billboard.md asset_billboard.py out/billboard`
Reply format and budgets: see the pack (RULES.md). Update episodes/nike_adidas/STATE.md with "done billboard" when finished.
