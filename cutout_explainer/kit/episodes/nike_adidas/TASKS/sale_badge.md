<!-- SIZE w=193-246 h=193-246 banned= -->
# Task: sale_badge
File: `asset_sale_badge.py`, function `draw(ctx, x, y, s=1.0)`. (x, y) = bottom-centre of the picture. Everything scales with s.
Size at s=1: about 220 x 220 px (window 193-246 x 193-246).
Real thing: a retail sale starburst. Draw the real kind of object, not a generic box. No brand names, logos or emblems; no text unless a feature asks for it.
Signature features (all must be recognisable; number them in a comment before coding):
1. red 16-point starburst with white outline
2. white word SALE in handwriting
3. percent text param
4. slight rotation
5. second inner ring

Scorer: `python3 bakeoff/score.py episodes/nike_adidas/TASKS/sale_badge.md asset_sale_badge.py out/sale_badge`
Reply format and budgets: see the pack (RULES.md). Update episodes/nike_adidas/STATE.md with "done sale_badge" when finished.
