# Model evaluations

Scoring uses `kit/RUBRIC.md`: 6 criteria, 0–5 each, maximum 30. Add a row for every run. Run each model twice, because cheap models vary between runs.

| Date | Model | Run | Kit version | Score | Tokens (uncached / cached / out) | Notes |
|---|---|---|---|---|---|---|
| 2026-10-08 | Qwen 3.8 Flash | 1 | founding kit (before the brief-check rule, rumble SFX and image downscale) | ~21 | 0.83M / 6.4M / 68k | details below |
| 2026-10-08 | DeepSeek V4.1 Flash | 1 | founding kit | n/a | n/a | did not finish |
| 2026-10 | Qwen 3.8 Flash | Vietnam v2 | v2 brief | accepted after director fixes | 25M / 45M / 225k | built 53 bgs, 22 props, 27 custom shots; needed layout fixes; re-read context ~300:1 |
| (pending) | Haiku 5.5 vs MiMo v2.6 Flash | bake-off | prep-ep2 | see `kit/bakeoff/RESULTS.md` | | cards A-D, blind scoring |

## Qwen 3.8 Flash, run 1 (TEST_BRIEF: Falcon 1, 2008 office, investor dialogue)

**Scores:**

| Criterion | Score |
|---|---|
| Asset recognizability | 3.5 |
| Staging | 3 |
| Character and dialogue | 3 |
| Style match | 3.5 |
| Motion and timing | 4 |
| Originality | 3 |

**Strengths:**
- Real self-review: 3 rounds, with extra full-resolution frame checks.
- Caught subtle defects: a dialogue tick that crossed a face and looked like a cracked lens, a hand landing on a mug, envelopes sinking into the desk.
- Good invented details: a flight-log chart with three red X's, a flip-chart sketch, "OVERDUE" envelopes popping in on beats.
- Sound cues tightly synced to on-screen events.

**Misses:**
- Both characters were seated on the same side of the table. The brief said across.
- One speaker's dialogue tick pointed at a window instead of at him. Qwen reported this only as "a little off".
- The phone appeared to float. Its stated reason (far hand, arm hidden in side view) was defensible, but the character faced the camera, so it still read as floating.

**Pattern:** strong at polishing frames, weak at checking the frame against the brief. Mitigations: per-shot CHECKS in the direction
document, the brief-check line in the self-review checklist, and a brief-check review by the strong model per batch.

**Audio:** about 4 dB quieter than v2. The launch used whooshes without low-end rumble, because the kit had no rumble sound at the time.

**Cost note:** nearly all input was context re-sent across loop turns. Output was small.

**Verdict:** viable as the bulk shot builder, with one strong-model review per batch.
