# Qwen handoff · Vietnam Act 1 · batch B01

You build 11 shots: S02–S11 and S13. The director has already built S01, S12, S14 and S15 (`key.py`), the cast, every asset and every sound cue.
Your job is drawing only. Don't redesign anything.

## Read (once, in this order)
1. `PROMPT_PRODUCTION.md`, the general rules. **This note overrides it where they differ.**
2. `STYLE_GUIDE.md` §1.4–1.6, §2, §3, §5 and `engine/API.md`.
3. `reference/original_frames_01.jpg` and `reference/GOOD_v2_example.jpg`. Look once.
4. `episodes/vietnam/BATCH_B01.md`, your 11 shot specs. Its **Staging** lines give exact positions, scales, facing and calls.
5. `episodes/vietnam/assets.py`. Read the function signatures and docstrings, not the bodies.

Skip `DIRECTION.md` (the full film plan), `key.py` and `shots.json`. You don't need them.

## Write: `episodes/vietnam/batch_01.py`
```python
import sys, os; sys.path.insert(0, os.getcwd())
from episodes.vietnam.assets import *
def s02(ctx, t, dur): ...
...
SHOT_FNS = {"S02": s02, "S03": s03, ..., "S11": s11, "S13": s13}
```
- Name the functions exactly `s02` … `s11` and `s13`, because the tools find shots by these names.
- **Don't write SCENES, CUES, SUBS or NARRATION.** `act1.py` takes durations and every sound effect from `shots.json` and mixes the voice.
  Your job on sound: make each pop happen at the time the spec gives, because the sounds play at exactly those times.
- Use `vcast()` for people and the asset functions for every prop. Don't redraw the map, cage, coupon, note, mill, lamp, counter or tag.
- Use `popped(ctx, t, start, x, y, lambda c: <asset>(c, 0, 0, ...))` for pop-ins, `keyword()` for white keywords and `sticky()` for yellow notes.
- People holding or pushing things: `arm_to(p, x, y, side, target)`. The hand has to land on the object.

## Review (max 2 rounds; each round = 1 sheet + at most 2 single-frame zooms)
Run from the kit root:
```
SHOTS=S02,S03,S04,S05,S06,S07,S08,S09,S10,S11,S13 python3 engine/sheet.py episodes.vietnam.act1 review.jpg
python3 engine/check.py episodes.vietnam.act1 s05 1.2 zoom.png       # one frame: shot function name + time in s
```
Tick every CHECK in `BATCH_B01.md`, shot by shot. Fix the failures, then re-check.

## Finish
```
python3 engine/sheet.py episodes.vietnam.act1 act1_sheet.jpg
python3 engine/build.py episodes.vietnam.act1 act1.mp4
```
Reply with **only** the following:
- S02 … S13: PASS, or FAIL and why, for each CHECK
- what you fixed
- known remaining issues
- any rule change you'd suggest, with the evidence

Send `act1_sheet.jpg`, `act1.mp4`, `batch_01.py` and your token counts (input, cached and output) to the director.
