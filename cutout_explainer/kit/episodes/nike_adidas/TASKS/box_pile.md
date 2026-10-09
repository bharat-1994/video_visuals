<!-- SIZE w=404-515 h=316-403 banned=nike|adidas|puma -->
# Task: box_pile
File: `asset_box_pile.py`, function `draw(ctx, x, y, s=1.0)`. (x, y) = bottom-centre of the picture. Everything scales with s.
Size at s=1: about 460 x 360 px (window 404-515 x 316-403).
Real thing: a heap of shoeboxes. Draw the real kind of object, not a generic box. No brand names, logos or emblems; no text unless a feature asks for it.
Signature features (all must be recognisable; number them in a comment before coding):
1. accepts n=15 boxes stacked in a loose pyramid with uneven offsets
2. two or three band colours (params)
3. a few boxes tilted
4. lids slightly open on two
5. one toppled box at the foot
6. shadow under the pile

Scorer: `python3 bakeoff/score.py episodes/nike_adidas/TASKS/box_pile.md asset_box_pile.py out/box_pile`
Reply format and budgets: see the pack (RULES.md). Update episodes/nike_adidas/STATE.md with "done box_pile" when finished.
