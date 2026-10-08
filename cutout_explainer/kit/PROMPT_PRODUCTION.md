You are building a batch of shots for a flat 2D cut-out explainer video, using the engine in this kit.

Read only:
1. STYLE_GUIDE.md, sections 1.4–1.6, 2, 3 and 5 (characters, look, motion, staging, assets, self-review).
2. engine/API.md.
3. reference/original_frames_01.jpg and reference/GOOD_v2_example.jpg (look once; don't re-open them).
4. Your batch spec: episodes/<slug>/shots.json (only the shots assigned to you) and the asset modules it names.

Build:
- Write episodes/<slug>/batch_<NN>.py with one function per shot, plus SCENES, CUES and SUBS (see engine/API.md).
- Use the existing assets and cast. Create new assets only if the spec says builder = you, and list their signature features in a comment first.

Review (budget: max 2 rounds; per round, 1 contact sheet plus at most 2 single-frame zooms):
- `python3 engine/sheet.py <module> review.jpg`. Look at it, then go through every shot's CHECKS from the spec, one by one.
- Fix the failures and re-check.

Finish with `python3 engine/build.py <module> batch_<NN>.mp4`, then reply with:
- for each shot: PASS, or FAIL with the reason, against its CHECKS
- what you fixed
- known remaining issues
- any rule you think should change, with the evidence
