<!-- SIZE w=228-291 h=140-179 banned=nike|adidas|puma|swoosh -->
# Task: shoe_box
File: `asset_shoe_box.py`, function `draw(ctx, x, y, s=1.0)`. (x, y) = bottom-centre of the picture. Everything scales with s.
Size at s=1: about 260 x 160 px (window 228-291 x 140-179).
Real thing: a cardboard shoebox with a lid. Draw the real kind of object, not a generic box. No brand names, logos or emblems; no text unless a feature asks for it.
Signature features (all must be recognisable; number them in a comment before coding):
1. lid overhanging the base
2. two visible faces for a 3D look
3. colour band on the lid (param)
4. blank rectangular end label
5. tissue paper edge peeking out
6. corner stitching lines

Scorer: `python3 bakeoff/score.py episodes/nike_adidas/TASKS/shoe_box.md asset_shoe_box.py out/shoe_box`
Reply format and budgets: see the pack (RULES.md). Update episodes/nike_adidas/STATE.md with "done shoe_box" when finished.
