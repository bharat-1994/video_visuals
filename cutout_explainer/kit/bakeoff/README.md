> **Status: finished 2026-10-09** (Haiku 5.5 vs MiMo v2.6 Flash vs Qwen 3.8 Flash; results in `docs/MODEL_EVALS.md`). Kept so any future candidate model can be tested the same way. `RULES.md` is now the live builder rules.

# Builder bake-off: Haiku 5.5 vs MiMo v2.6 Flash

Question: which cheap model should build props and shot lines for episode 2, at what quality and cost? Same four cards, same rules, same scripts.
Decision is made from the numbers below, not from feel. Sonnet is the director in both cases (it judges; it does not build in this test).

## What each model gets (and nothing else)
`bakeoff/RULES.md` + ONE card from `bakeoff/cards/` + `bakeoff/LIB_CHEATSHEET.md` (+ for card D: `engine/SCENE_LANGUAGE.md`, `library/catalog/CATALOG.md` and one sheet image).
Same repo commit for both. Fresh session per card, per model (so 4 runs each, 8 in total). Do not give hints beyond the card.

## How to run
- **Haiku 5.5**: Sonnet runs it in this chat as sub-agents, one per card, prompt = the files above verbatim.
- **MiMo v2.6 Flash** (you run it): check out branch `prep-ep2`, `pip install pycairo numpy`, copy `kit/fonts/CaveatBrush.ttf` to `~/.fonts`. Start a fresh session per card, paste RULES.md + the card + the cheatsheet
  (card D: also SCENE_LANGUAGE.md, CATALOG.md and one sheet image). It writes the file named in the card into the kit folder and runs the scorer itself, from the kit root:
  `python3 bakeoff/score.py A asset_scooter.py out/A` (cards A-C) / `python3 bakeoff/score_lines.py lines_D.py out/D` (card D).
- **Record per run** (copy into RESULTS.md): input tokens uncached / cached, output tokens, wall-clock minutes, number of scorer runs, whether it looked at its own image.
- **Return to me**: for each card the `.py` file, the `out/<card>_crop.png` (or `out/D/sheet.jpg`), the scorer text, the token numbers, and the model's final report. A zip is fine.

## How I score (Sonnet, blind)
1. Scripts (automatic, in the scorer): runs, size window, anchor, scaling, palette, ink, banned text, line budget; for D: parse, names exist, beat gap, layout, variety.
2. Visual (0-5 each, `compare.py` hides which model drew what): recognisable as the real thing, signature features present (count of 8 verified by me, not by the model's own list),
   style match against `kit/reference/GOOD_v2_example.jpg`, polish (no stray shapes, clean overlaps). For D: do the ten pictures say what the narration says, variety, no faces covered.
3. Honesty: model's FEATURES claim vs what I count (a false YES costs 1 point).
4. Cost: $ per card from the token counts and list prices (MiMo $0.10/$0.28, Haiku $0.10/$0.50 per M in/out; cache $0.003 / $0.01) and minutes.

## Decision rule
- Quality = mean of the visual scores over A-D (max 20 per model per run-set), cost = mean $ per card.
- A model is **usable** if every card has all scripts passing (or one trivial failure) and quality >= 12/20 with a Sonnet-level fix list that is short.
- If both are usable: take the cheaper one unless the other is >= 3 quality points higher (5% quality for 20% cost rule from the user: below that gap, cheaper wins).
- If only one is usable: that one. If neither: Sonnet builds the props (about $0.4-1 per prop from earlier runs), the cheap model only writes shot lines (card D).
- If the gap is within noise (a card flips between runs), run cards B and C once more for each model before deciding.
- Also note which model needed fewer scorer runs and whether it obeyed the budgets (cheap models usually blow them).
