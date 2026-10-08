# Explainer-animation bake-off kit

A self-contained kit for testing whether a model (DeepSeek, Qwen, Haiku, Sonnet…) can produce shots in this style.
Every model gets exactly the same inputs and the same scoring sheet.

## What's inside
| path | what it is | who reads it |
|---|---|---|
| `PROMPT.md` | the exact prompt to paste into the model | model |
| `STYLE_GUIDE.md` | the style, split into FIXED identity and FREE variety, plus staging rules, the asset quality bar and a self-review checklist | model |
| `TEST_BRIEF.md` | the task: 3 new shots (a landmark, a staging test, a dialogue) | model |
| `engine/` | `lib.py` (puppets, expressions, pose presets, effects, camera), `API.md`, `check.py`, `sheet.py`, `build.py` | model |
| `reference/` | frames from the original video, the cast sheet, pose presets, a rejected and an accepted attempt | model (needs to see images) |
| `examples/` | the accepted v2 shot code (9 shots) as patterns | model |
| `audio/` | 29 synthesized sound effects, a music bed and `sfx/INDEX.md` | engine |
| `fonts/CaveatBrush.ttf` | the handwritten font | install once |
| `RUBRIC.md` | the scoring sheet and an optional blind-judge prompt | you |

## Setup (once per machine or sandbox)
```bash
pip install pycairo numpy          # add --break-system-packages on some Linux distros
# ffmpeg must be on PATH
mkdir -p ~/.fonts && cp fonts/CaveatBrush.ttf ~/.fonts/ && fc-cache -f   # Linux. On Mac/Windows, double-click the font to install it

cd examples && python3 ../engine/sheet.py all_shots ../check.jpg && cd ..   # should reproduce reference/GOOD_v2_example.jpg
```

## The model's environment must have
1. **Code execution** in this folder (Python and ffmpeg).
2. **File reading**, including **images**. The model must be able to look at `reference/*.jpg` and at its own `review.jpg`.
   A text-only model can still run, but it works blind; note that in the rubric, because it is usually the deciding factor.
3. Optional: web or image search, so it can look at real photos of landmarks. Either give every model this or give none.

## Running the comparison
1. Copy the kit to a fresh folder for each run (so no model sees another's output).
2. Paste `PROMPT.md` as the task. Don't add hints. Note the tokens used, the cost and the time.
3. Collect `review.jpg` and `test_out.mp4`. Rename them A, B, C… so judging is blind.
4. Score with `RUBRIC.md`, yourself and optionally with a stronger model using the blind-judge prompt.
5. Run each model **twice**. Cheap models can vary a lot from run to run.

## Reading the result
- **24–30:** viable as the main shot builder, with light review.
- **18–23:** viable for drafting, with a stronger model reviewing contact sheets and sending back fixes. This is probably the cost-effective setup.
- **Under 18:** limit it to mechanical work, such as cue lists, shot splitting and running renders.

What separates the models will mostly be whether they looked at their own render and actually caught the problems.
Check the model's reply to see whether its "defects found" match what you see.
