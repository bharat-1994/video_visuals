# cutout_explainer

A pipeline for flat 2D cut-out explainer videos: round-headed puppets, pop-in props, handwritten captions, fast literal visuals.
A strong model directs and builds the key parts, and cheaper models (e.g. Qwen) build the bulk of the shots.

## Start here
1. `docs/HANDOVER.md`: everything decided and learned so far. Read it first.
2. `kit/STYLE_GUIDE.md`: the style (a fixed identity layer and a free variety layer), staging rules, the asset bar and the self-review checklist.
3. `docs/DIRECTION_TEMPLATE.md`: how a script becomes a shot-by-shot direction document plus `shots.json`.

## Layout
```
cutout_explainer/
├── PROJECT_INSTRUCTIONS.md   paste into the Claude Project's instructions
├── docs/
│   ├── HANDOVER.md           context, decisions, history, open work, token economics
│   ├── DIRECTION_TEMPLATE.md direction document format and shots.json schema
│   ├── LEARNINGS.md          approved rule changes, append-only
│   └── MODEL_EVALS.md        scored model runs (Qwen run 1, about 21/30)
├── kit/                      self-contained working kit (give this to a shot-building model)
│   ├── STYLE_GUIDE.md  PROMPT.md (bake-off)  PROMPT_PRODUCTION.md (batches)  TEST_BRIEF.md  RUBRIC.md
│   ├── engine/   lib.py (rig, poses, effects, render; 1080p default)  scene_v2.py (scene lines)  SCENE_LANGUAGE.md  API.md
│   │             build.py (render+mix)  sheet.py  check.py  audit.py  layout_check.py  catalog.py  beats.py
│   ├── tools/    prep_audio.py (audio -> words.json, segs.json)
│   ├── library/  register.py (loads all shared assets)  catalog/ (CATALOG.md + picture sheets of every asset, bg, cast)
│   ├── bakeoff/  builder test: cards, RULES.md, scorers, README (Haiku vs MiMo)
│   ├── episodes/ _template/ (copy per episode)  vietnam/ (finished)
│   ├── audio/    sfx/*.wav (31) + INDEX.md, music_bed.wav, sfx.py + sfx_extra.py (synthesis sources)
│   ├── reference/  style reference frames, cast, poses, a bad example and a good example
│   ├── examples/   accepted v2 shot code (9 shots)
│   └── fonts/      CaveatBrush.ttf
├── history/                  v1, v2 and Qwen run 1 outputs, kept for comparison
└── episodes/                 (per-episode direction, assets, batches; created when work starts)
```

## Setup
```bash
pip install pycairo numpy            # plus ffmpeg on PATH
mkdir -p ~/.fonts && cp kit/fonts/CaveatBrush.ttf ~/.fonts/ && fc-cache -f
cd kit/examples && python3 ../engine/sheet.py all_shots ../check.jpg   # should match reference/GOOD_v2_example.jpg
```

## Claude Project setup
- **Instructions:** paste the text of `PROJECT_INSTRUCTIONS.md`.
- **Knowledge (11 files, about 70 KB):** `docs/HANDOVER.md`, `kit/STYLE_GUIDE.md`, `docs/DIRECTION_TEMPLATE.md`, `docs/LEARNINGS.md`,
  `docs/MODEL_EVALS.md`, `kit/RUBRIC.md`, `kit/engine/API.md`, `kit/engine/lib.py`, `kit/PROMPT_PRODUCTION.md`,
  `kit/audio/sfx/INDEX.md`, `README.md`.
- **Optional images:** `kit/reference/original_frames_01.jpg` and `kit/reference/GOOD_v2_example.jpg`.
- **Repo only:** example code, bake-off files (`PROMPT.md`, `TEST_BRIEF.md`), audio, font, reference images, history.

Re-upload whichever knowledge files a commit changes. Each commit message lists them.
