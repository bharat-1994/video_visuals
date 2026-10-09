<!-- SIZE w=264-336 h=492-627 banned=nike|adidas|swoosh -->
# Task: shop_app
File: `asset_shop_app.py`, function `draw(ctx, x, y, s=1.0)`. (x, y) = bottom-centre of the picture. Everything scales with s.
Size at s=1: about 300 x 560 px (window 264-336 x 492-627).
Real thing: a phone showing a shoe-shop product page. Draw the real kind of object, not a generic box. No brand names, logos or emblems; no text unless a feature asks for it.
Signature features (all must be recognisable; number them in a comment before coding):
1. portrait smartphone with rounded corners and notch
2. product image area with a simple sneaker blob
3. three colour swatch dots
4. row of size chips
5. wide rounded BUY button (the word BUY is allowed)
6. cart icon with a number badge
7. accepts accent colour

Scorer: `python3 bakeoff/score.py episodes/nike_adidas/TASKS/shop_app.md asset_shop_app.py out/shop_app`
Reply format and budgets: see the pack (RULES.md). Update episodes/nike_adidas/STATE.md with "done shop_app" when finished.
