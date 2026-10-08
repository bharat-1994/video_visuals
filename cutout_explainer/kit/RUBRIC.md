# Scoring rubric (fill one row per model run)

Judge from the contact sheet (`review.jpg`) and the final video. Ideally judge **blind**: rename outputs A/B/C first.

| criterion | 0 | 3 | 5 |
|---|---|---|---|
| **Asset recognizability** (Shot 1 rocket/island; any prop) | generic boxes | recognizable with effort | instantly recognizable, signature features present |
| **Staging correctness** (Shot 2) | screens/hands wrong, floating objects | 1–2 errors | physically correct throughout |
| **Character & dialogue** (Shot 3) | lip-flap wrong / text over faces / crossed limbs | minor issues | clean, expressive, text well placed |
| **Style match** vs `reference/original_frames_*` | different style | similar but off (clutter, gradients, wrong text) | could pass as the same channel |
| **Motion & timing** | static or chaotic | some pops/camera | pops on beats, camera moves, sound cues synced |
| **Originality** (not copying examples) | copied layouts | partly | fresh compositions within the style |

Also record:
- Hard failures: crashes, missing shots, wrong durations (Y/N)
- Fix rounds the model needed, and whether it actually looked at its own render
- Tokens in/out and cost; wall-clock time
- Run-to-run variance: run each model **twice**; note if quality swings a lot

Total = sum of 6 criteria (max 30). Rough reading: ≥24 production-ready with light review · 18–23 usable with a strong reviewer · <18 not viable for this role.

## Blind judge prompt (optional, for a stronger model)
"You are an art director. Attached are contact sheets from anonymous runs A, B, C of the same 3-shot brief
(TEST_BRIEF.md) and the style reference images. Score each run 0–5 on the six criteria in RUBRIC.md, listing
concrete defects you see (frame + issue) for each score below 5. Do not guess which model made which."
