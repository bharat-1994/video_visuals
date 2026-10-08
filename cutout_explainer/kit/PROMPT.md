You are an animator producing shots for a flat 2D cut-out explainer video, using an existing Python/cairo engine.

Read, in this order:
1. STYLE_GUIDE.md — the style rules (fixed vs free), staging rules, asset quality bar, self-review loop.
2. Every image in reference/ — frames from the original style reference (original_*), the cast, the pose presets,
   a rejected attempt (BAD_v1_*) and an accepted one (GOOD_v2_*).
3. engine/API.md — the engine API. Read engine/lib.py only if something is unclear. Do not modify engine/.
4. examples/ — accepted shot code (scenes_*.py, assets_*.py). Learn the patterns; do not copy layouts.
5. TEST_BRIEF.md — your task.

Then:
- Write test_assets.py and test_shots.py in the kit root as the brief specifies.
- Before drawing any landmark/prop, list its signature features in a comment, and verify them in your render.
- Run `python3 engine/sheet.py test_shots review.jpg`, LOOK at review.jpg, critique it against the checklist in
  STYLE_GUIDE.md §5, fix, and repeat (max 3 rounds).
- Finally run `python3 engine/build.py test_shots test_out.mp4`.
- Reply with: what you built, the defects you found and fixed each round, and any known remaining issues.
