<!-- SIZE w=387-492 h=220-280 banned=hoka|asics|on|nike|adidas|cloud -->
# Task: sneaker_runner_pods
File: `asset_sneaker_runner_pods.py`, function `draw(ctx, x, y, s=1.0)`. (x, y) = bottom-centre of the picture. Everything scales with s.
Size at s=1: about 440 x 250 px (window 387-492 x 220-280).
Real thing: a lightweight road running shoe with a slotted sole. Draw the real kind of object, not a generic box. No brand names, logos or emblems; no text unless a feature asks for it.
Signature features (all must be recognisable; number them in a comment before coding):
1. midsole with a row of 7 rounded horizontal slots (pods)
2. sleek mesh upper
3. speed laces and a stretch cord
4. rubber outsole pattern at the bottom edge
5. heel pull tab
6. accepts colours and flip

Scorer: `python3 bakeoff/score.py episodes/nike_adidas/TASKS/sneaker_runner_pods.md asset_sneaker_runner_pods.py out/sneaker_runner_pods`
Reply format and budgets: see the pack (RULES.md). Update episodes/nike_adidas/STATE.md with "done sneaker_runner_pods" when finished.
