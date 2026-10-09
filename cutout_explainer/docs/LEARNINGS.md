# Learnings log

An append-only log of rule changes. Each entry: date · change · reason / evidence · approved by.
Process: at the end of every job, the working model proposes entries. The human approves or rejects each one. Approved entries
are applied to the affected files and logged here in the same commit. Don't change rules on the strength of a single run unless the human approves.

## 2026-10-08 (founding session)
- **Assets must be recognizable reconstructions of the real thing, with signature features listed before drawing.** Evidence: v1's Stanford was a generic box house and was rejected by the user. Approved: user.
- **Screens, books and papers face their user. Typing shots are side-on or over-the-shoulder.** Evidence: v1 had a computer facing the camera while the kid typed. Approved: user.
- **Rig: hands can't cross the body midline (prints a warning). The far arm goes behind the torso in side view, both arms in back view.** Evidence: v2 showed crossed hands, and hands over a back-view character. Approved: user.
- **Pose presets (`pose()`) replace raw arm numbers.** Same evidence as above. Approved: user.
- **Faces resemble real people via hair, jaw, brows, nose and accessories.** Evidence: the user asked for faces closer to the real people. Approved: user.
- **Self-review checklist: re-read the brief and tick every stated requirement.** Evidence: Qwen run 1 seated two characters on the same side despite a brief saying "across". Approved: user.
- **Added rocket_rumble and engine_roar sound effects.** Evidence: Qwen's launch had no low end because the library had no rumble. Approved: user.
- **Reference images downscaled. Added a slim production prompt.** Evidence: Qwen run 1 used 7.2M input tokens for 3 shots, mostly re-sent context. Approved: user.
- **Learning happens through proposals the human approves, committed to this repo.** Approved: user.

## 2026-10-09 (Vietnam video and builder bake-off)
All entries approved by the user ("yes" to the plan of 2026-10-09).
- **Shots are one line each in the scene language (`lines.py`) instead of per-shot code.** Evidence: 151 shots built from lines; per-shot code per Qwen batch failed. Approved: user.
- **Seconds in a timing token need a decimal point (`@1.5`); `@50` means the word "50".** Evidence: a parse bug in Vietnam. Approved: user.
- **Clause auto-cut of shots (`tools/prep_audio.py`), then hand fixes by the director.** Approved: user.
- **Run `audit.py` and `layout_check.py` before any render; plan and checks come before drawing.** Evidence: v1 failed every variety check; layout check found text over a face (S29) and clipped text that eyes missed. Approved: user.
- **Shot ids may appear once per lines file; the checker flags duplicates.** Evidence: a duplicate key silently shadowed a fix in Vietnam v2. Approved: user.
- **Motion only if the narration names it or the real place has it; walk=/move=/fx must be tied to a narration word.** Evidence: user rejected filler motion (rain, confetti, motorbikes, sliding). Approved: user.
- **People appear only where the script makes them relevant; no interaction quotas.** Evidence: user preference after reviewing the film. Approved: user.
- **Dark/spotlight backgrounds only for genuine emotional beats or the cage/map motif; no background in more than ~8% of shots.** Evidence: Vietnam v1 overused spotlight, map and ship. Approved: user.
- **Sounds are chosen by element category, never "pop" for everything.** Evidence: user called the repeated pop irritating. Approved: user.
- **Builder = Haiku 5.5 sub-agents at high effort with batches, a fixed ~1k-token pack, a progress file (STATE.md) and hard budgets; Sonnet 5.5 directs and judges; Opus at medium is a per-item fallback. Qwen and MiMo not used.** Evidence: bake-off (MODEL_EVALS); Vietnam Qwen run read context ~300:1. Approved: user.
- **Keep every builder request under 100k tokens (Haiku prices rise about 5x above that, cache reads included).** Evidence: Anthropic pricing page. Approved: user.
- **Default render is 1080p (true vector re-render, RENDER_SCALE=1.5); 720p only for drafts.** Evidence: user asked for 1080p only. Approved: user.
- **Reserve the meeting-room screen area x 556-1116, y 118-418.** Approved: user.
