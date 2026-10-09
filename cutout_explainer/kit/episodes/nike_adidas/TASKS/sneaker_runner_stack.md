<!-- SIZE w=387-492 h=228-291 banned=hoka|asics|on|nike|adidas|swoosh -->
# Task: sneaker_runner_stack
File: `asset_sneaker_runner_stack.py`, function `draw(ctx, x, y, s=1.0)`. (x, y) = bottom-centre of the picture. Everything scales with s.
Size at s=1: about 440 x 260 px (window 387-492 x 228-291).
Real thing: a maximal-cushion road running shoe. Draw the real kind of object, not a generic box. No brand names, logos or emblems; no text unless a feature asks for it.
Signature features (all must be recognisable; number them in a comment before coding):
1. tall stacked midsole, at least 45% of shoe height
2. rocker curve at toe and a bevelled heel
3. breathable mesh upper drawn with a dot grid
4. plain heel pull tab
5. neat laces
6. accepts body, accent, sole colours, flip, and cutaway=True which shows a black carbon plate line inside layered foam

Scorer: `python3 bakeoff/score.py episodes/nike_adidas/TASKS/sneaker_runner_stack.md asset_sneaker_runner_stack.py out/sneaker_runner_stack`
Reply format and budgets: see the pack (RULES.md). Update episodes/nike_adidas/STATE.md with "done sneaker_runner_stack" when finished.
