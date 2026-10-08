# Paste this to Qwen (one message)

You are improving an animated explainer video that is built entirely from code.

Repo: https://github.com/bharat-1994/video_visuals
1. Clone it.
2. Check out a NEW branch called `qwen-v2`.
3. Work inside `cutout_explainer/kit/` and run every command from there.

Your complete brief is `episodes/vietnam/v2/REVISION_v2.md`. Follow it exactly. It tells you:
- what to read (and what to skip)
- which new files to create
- the sound, background, asset, cast and fx specs
- the checks
- the review budget
- what to report

The director has already written every shot change (`episodes/vietnam/v2/film_v2_lines.py`) and the assembly (`episodes/vietnam/v2/film_v2.py`). You build what those lines need.

Hard rules:
- Never edit v1 files. Never push to `main`. Commit only to `qwen-v2`.
- No real company logos, emblems, flags or seals. Use brand colour, plain name lettering and the real kind of place.
- `python3 episodes/vietnam/v2/audit.py` must PASS.
- Max 2 review rounds per contact-sheet chunk.

When done, push branch `qwen-v2`. Reply with the content of `episodes/vietnam/v2/REPORT_v2.md` and your token usage.
