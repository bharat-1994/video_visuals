# Production prompt (superseded)
The per-shot batch handoff was retired after Vietnam (Qwen rebuilt assets from scratch and re-read context ~300x). Builders now work from small task cards:
see `kit/bakeoff/RULES.md` (budgets and report format) and `kit/bakeoff/cards/` (card format: file, signature, size, anchor, signature features).
Shot lines are written against `kit/engine/SCENE_LANGUAGE.md` and `kit/library/catalog/CATALOG.md`, then checked by `engine/audit.py` and `engine/layout_check.py`.
