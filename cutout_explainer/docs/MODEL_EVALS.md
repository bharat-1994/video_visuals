# Model evaluations

Scoring uses `kit/RUBRIC.md`: 6 criteria, 0–5 each, maximum 30. Add a row for every run. Run each model twice, because cheap models vary between runs.

| Date | Model | Run | Kit version | Score | Tokens (uncached / cached / out) | Notes |
|---|---|---|---|---|---|---|
| 2026-10-08 | Qwen 3.8 Flash | 1 | founding kit (before the brief-check rule, rumble SFX and image downscale) | ~21 | 0.83M / 6.4M / 68k | details below |
| 2026-10-08 | DeepSeek V4.1 Flash | 1 | founding kit | n/a | n/a | did not finish |
| 2026-10 | Qwen 3.8 Flash | Vietnam v2 | v2 brief | accepted after director fixes | 25M / 45M / 225k | built 53 bgs, 22 props, 27 custom shots; needed layout fixes; re-read context ~300:1 |
| 2026-10-09 | Haiku 5.5 (high) | bake-off A-D | f3bf1ce | 3.6/5 avg (14.3/20) | ~435k total | scripts A,B,C 12/12, D 10/11; 2 min per card |
| 2026-10-09 | MiMo v2.6 Flash (high) | bake-off A-D | f3bf1ce | 3.8/5 avg (15.3/20) | est ~1.8M in / 223k out | best scooter; 5-36 min per card |
| 2026-10-09 | Qwen 3.8 Flash (high) | bake-off A-D | f3bf1ce | 3.5/5 avg (14.2/20) | 516k uncached / 552k cached / 113k out (exact) | best bridge, D 11/11 first run; weak scooter and cassette; 7-9 min per card |

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

## Builder bake-off, 2026-10-09 (cards A scooter, B bridge, C cassette player, D ten shot lines; `kit/bakeoff/`)
Scored blind by the director (Sonnet 5.5) on recognisability, signature features, style, polish; D on story, variety, layout. Scripts as a second check.

| | Haiku 5.5 | MiMo v2.6 Flash | Qwen 3.8 Flash |
|---|---|---|---|
| A scooter /5 | 3.7 | 4.3 | 3.3 |
| B bridge /5 | 2.7 | 3.3 | 3.8 |
| C cassette /5 | 4.3 | 3.8 | 3.2 |
| D shots /5 | 3.7 | 3.8 | 3.8 |
| average | 3.6 | 3.8 | 3.5 |
| time per card | ~2 min | 5-36 min | 7-9 min |

- Differences are within noise (under 3 points of 20), so cost and speed decide. All three cost cents per episode of building; the director's reading is the real cost.
- Chosen: Haiku 5.5 at high effort as the builder (user decision: fastest, cheapest on the Claude side, no extra harness), kept under 100k per request by batch size and budgets; Opus at medium as per-item fallback.
- Honesty: Qwen's scooter report claimed all checks passed when 11/12 did; Haiku's bridge report said YES to features that were barely visible. Models over-claim, so the director verifies from pictures.
- Pack defects found and fixed after the test: card B (water vs bottom-edge check), ink check too strict (dark colours failed it), banned-text check hit comments, cheatsheet lacked box() corner convention, `kw` @word undocumented, calendar prop ignores its year.
- Not tested: any model's ability to find defects in a contact sheet (vision review).
