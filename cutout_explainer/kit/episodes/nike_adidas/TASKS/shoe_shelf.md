<!-- SIZE w=528-672 h=369-470 banned=nike|adidas|puma|footlocker -->
# Task: shoe_shelf
File: `asset_shoe_shelf.py`, function `draw(ctx, x, y, s=1.0)`. (x, y) = bottom-centre of the picture. Everything scales with s.
Size at s=1: about 600 x 420 px (window 528-672 x 369-470).
Real thing: a retail wall display with three shelves. Draw the real kind of object, not a generic box. No brand names, logos or emblems; no text unless a feature asks for it.
Signature features (all must be recognisable; number them in a comment before coding):
1. wood-framed back panel
2. three staggered ledges
3. accepts fill 0..1 (share of the 10 shoe slots occupied
4. slots fill from the top shelf down)
5. each slot has a pedestal peg and a tiny price tag
6. a plain header sign slot with text param
7. floor shadow

Scorer: `python3 bakeoff/score.py episodes/nike_adidas/TASKS/shoe_shelf.md asset_shoe_shelf.py out/shoe_shelf`
Reply format and budgets: see the pack (RULES.md). Update episodes/nike_adidas/STATE.md with "done shoe_shelf" when finished.
