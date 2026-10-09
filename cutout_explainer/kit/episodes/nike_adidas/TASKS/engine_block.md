<!-- SIZE w=369-470 h=281-358 banned= -->
# Task: engine_block
File: `asset_engine_block.py`, function `draw(ctx, x, y, s=1.0)`. (x, y) = bottom-centre of the picture. Everything scales with s.
Size at s=1: about 420 x 320 px (window 369-470 x 281-358).
Real thing: a four-cylinder car engine. Draw the real kind of object, not a generic box. No brand names, logos or emblems; no text unless a feature asks for it.
Signature features (all must be recognisable; number them in a comment before coding):
1. cast block body in a colour param
2. valve cover with ridges on top
3. four spark plugs with wires
4. front pulley with a belt
5. two exhaust manifold pipes
6. bolts drawn with a loop

Scorer: `python3 bakeoff/score.py episodes/nike_adidas/TASKS/engine_block.md asset_engine_block.py out/engine_block`
Reply format and budgets: see the pack (RULES.md). Update episodes/nike_adidas/STATE.md with "done engine_block" when finished.
