<!-- SIZE w=334-425 h=264-336 banned=nike|swoosh -->
# Task: ribbon_sign
File: `asset_ribbon_sign.py`, function `draw(ctx, x, y, s=1.0)`. (x, y) = bottom-centre of the picture. Everything scales with s.
Size at s=1: about 380 x 300 px (window 334-425 x 264-336).
Real thing: a wooden shop sign with an award rosette. Draw the real kind of object, not a generic box. No brand names, logos or emblems; no text unless a feature asks for it.
Signature features (all must be recognisable; number them in a comment before coding):
1. board on two posts with wood grain lines
2. blue award rosette (round ribbon with two tails and a gold centre) at the left corner
3. text param centred on the board (plain letters, any colour)
4. chain hangers
5. accepts board colour

Scorer: `python3 bakeoff/score.py episodes/nike_adidas/TASKS/ribbon_sign.md asset_ribbon_sign.py out/ribbon_sign`
Reply format and budgets: see the pack (RULES.md). Update episodes/nike_adidas/STATE.md with "done ribbon_sign" when finished.
