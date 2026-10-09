# Handover: cut-out explainer animation pipeline

This file holds everything decided and learned in the founding session (2026-10-08). It lets any later session, by any model,
continue without that conversation. Read this first, then `kit/STYLE_GUIDE.md`.

## 0. Current workflow (episode 2 onward; supersedes the per-shot Qwen handoff in section 5.1)
Updated 2026-10-09 after the Vietnam video (151 shots) and the builder bake-off. Numbers are in sections 7b and docs/MODEL_EVALS.md.
1. **Audio in:** `python3 tools/prep_audio.py episodes/<slug> part*.wav` gives narration.wav, words.json, segs.json (clause-cut shots), END.txt. The director then hand-fixes segs.json against the script.
2. **Plan before drawing:** copy `kit/episodes/_template/` to `kit/episodes/<slug>/`. The director writes PLAN.md: chapters, motifs, background budget, key shots, which shots move and why, which need people and why, and a one-line-per-asset table. Search `kit/library/catalog/` first; reuse before drawing.
3. **Cards:** `python3 tools/make_cards.py episodes/<slug>/PLAN.md` turns the asset lines into task cards (`episodes/<slug>/TASKS/`). `python3 tools/make_pack.py [--lines]` builds the fixed builder pack (about 1k tokens; 5k with scene grammar and catalog names).
4. **Builders = Haiku 5.5 sub-agents at high effort,** one fresh session per batch (about 5 props or 25 shot lines), each getting the pack + its cards + STATE.md. Rules in `kit/bakeoff/RULES.md`: 2 scorer runs and 1 look per item, short tool output, about 60 tool calls, then write STATE.md and stop. A successor session continues from STATE.md. This keeps every request far below Haiku's 100k-token price step (above it, prompts cost about 5x, cache reads included).
5. **Checks before any render** (scripts, not eyes): `engine/audit.py` (variety, beat gap, names registered, untied motion), `engine/layout_check.py` (text on faces, clipped text, duplicate shot ids), `bakeoff/score.py` (size, anchor, palette, ink for each prop).
6. **Render, look, fix:** `SHOTS=... RENDER_SCALE=1 engine/sheet.py` for drafts (720p), `engine/build.py` for the final (1080p, true vector re-render).
7. **Director = Sonnet 5.5:** plan, key shots, fixes, and judging contact sheets and catalog pictures (never reading builder code). If Haiku fails the same item twice, that one item goes to Opus at medium effort. Qwen and MiMo were tested and are not used (see MODEL_EVALS).
8. **Fresh chat per episode,** state in `episodes/<slug>/STATE.md`.
9. **Defaults:** engine = `scene_v2.py` + `build.py`; `library/register.py` loads the shared library; 1080p; chapter music from `audio/music/`; sounds automatic by category.
10. **Beauty and motion rules:** motion only when the narration names it or the real place has it; people only where the script makes them relevant; no quotas (see STYLE_GUIDE 1.6 and engine/SCENE_LANGUAGE.md).

## 1. Goal
Make YouTube explainer videos (biography and "why X" topics, around 10 min) in a specific flat 2D cut-out style, cheaply and
consistently. A strong model sets the creative direction and builds the key parts. Cheaper models build the bulk of the shots.

## 2. What the reference style is (from analysing a 10.7-min reference video)
**Mechanics.**
- It is cut-out puppet animation, not drawn animation.
- One reusable puppet per character: round head, dot eyes, short brow strokes, swap mouths, flat shirt body and rubber-hose stroke limbs.
- Expressions change only the brows, eyes and mouth. Lip-flap runs only while that character's line is on screen.
- Motion comes from fast cuts, props popping in with a smoke puff, and slow camera push or pull. The characters themselves barely move.

**Pacing (measured).**

| What | Measured value |
|---|---|
| Shots | 170 in 642 s |
| Shot length | median 3.4 s, range 1.6–6.4 s |
| Words per shot | about 10 (narration runs about 166 wpm) |
| Dialogue mini-scenes | about one per minute |
| Twist or pivot line | every 30–45 s |

**Visual rule.** Every narration clause becomes a literal picture. Abstract ideas become physical metaphors: traps, cages, golden
handcuffs, doors, rope bridges.

**On screen.**
- Black chapter cards with typewriter text.
- Sticky-note time skips such as "Month 3" and "Year 5".
- Handwritten font (we use Caveat Brush). Dialogue is white text with a small tick toward the speaker, never a speech bubble.

**Voice.** One male narrator voices every character, women included (pitch measured at about 87–111 Hz throughout).

**Script formula.**
- Hook of about 60 words: "you" grind, a quiet sad payoff, a branded term, "not just X, everywhere", then two promises (why, and how to escape).
- 3 chapters at about 17% / 47% / 31% of runtime: promise, slow decline, realization plus 5 steps.
- The middle chapter is a ladder: time skips, odd specific dollar figures and a dialogue gag on each rung.
- Ending: a fairness caveat, then a callback line that flips the opening metaphor.

We keep only this abstracted formula. The reference video, its transcript and its script are not stored here (third-party work).
A few contact sheets of its frames are in `kit/reference/` as a private style reference. Remove them if the repo goes public.

## 3. What we built
**Engine (`kit/engine/lib.py`, pycairo, renders 1280×720 at 30 fps).**
- Puppet rig: head shape with a `jaw` control, hair styles (short, fringe, part, wavy, slick, bald), nose, glasses, mustache, kid proportions.
- 9 expressions, auto-blink, lip-flap and idle bob.
- Facing from −1 to 1, with features shifting toward the facing side. A back view (`view="back"`).
- Rubber-hose arms. Walk cycle.
- Pose presets via `pose()`.
- Rig constraints: hands can't cross the body midline (with a printed warning). The far arm goes behind the torso in side view, and both arms go behind it in back view.
- Effects: `popped()` overshoot with smoke puff, typewriter text, `dialogue()` with tick, camera zoom, pan and shake.
- Backgrounds and props: spotlight, sky, sunset, room, city window, money bag, bill, CRT monitor, desk, paper.
- `cast()` registry: elon_kid, elon_teen, elon_adult, kimbal, bully, editor, banker.
- `render()` streams frames straight to ffmpeg. 30 s renders in about 26 s.

**Tools.**
- `check.py`: render a single frame.
- `sheet.py`: contact sheet for self-review.
- `build.py`: renders the video, adds subtitles from `SUBS`, mixes the sound cues from `CUES` with the music bed, and outputs the mp4.

**Audio (`kit/audio/`).**
- 31 sound effects, synthesized in numpy: `sfx.py` (made by Sonnet) and `sfx_extra.py` (rocket_rumble, engine_roar).
- A 40 s music bed at 105 BPM.
- No model can listen, so the human approves sounds by ear.

## 4. History of attempts (outputs in `history/`)

| Version | What it was | Result |
|---|---|---|
| v1 | 30 s, Musk ages 0–27. Sonnet wrote the storyboard and the shots on my engine. | Style right. Assets generic (Stanford was a box house). A computer faced the camera while the kid typed. Faces generic. |
| v2 | Same story with real landmarks (Union Buildings, Memorial Church, VIC-20, Canada arrivals), likeness faces, staging rules, and 90 sound cues plus music. | User: "visuals look good but could be better". Remaining problems: hands and crossing arms, hands drawn over a back view (both since fixed in the rig), Stanford not close enough to the real thing, and objects needing more complexity. |
| Qwen run 1 | Qwen 3.8 Flash, the 3-shot bake-off brief (Falcon 1 launch, 2008 night office, investor dialogue). | About 21/30. See `docs/MODEL_EVALS.md`. |

The voice-over was dropped for v2 (narration shown as subtitles). The final pipeline needs a voice track to time shots against.

## 5. Decisions
1. **Roles.**
   - Strong model (Opus-class): direction document, character rigs, key shots (hook, chapter openers, reveals, recurring metaphors, about 10–15% of shots), recurring assets, and judging against the brief.
   - Sonnet: new sound effects, asset drafts, second-tier review.
   - Haiku: mechanical work only (spec→JSON, timing math, cue lists, renders, code-based checks). It is not fit for visual judgment or asset drawing.
   - Qwen (run by the user): bulk shots in batches of 10–15.
2. The **direction document** is written by the strong model. It is the leverage point: precise per-shot acceptance checks cover the main weakness of cheaper models.
3. **Asset library over redrawing.** Landmarks and recurring props are built once, ideally from photo references, reviewed, and reused.
4. **Learning happens with human approval.** At the end of each job, propose changes to the rules, the human approves, then the changes are committed to `docs/LEARNINGS.md` and the affected files. Never rewrite rules from a single run on our own.
5. The **source of truth is this repo.** Qwen's environment pulls from it. A Claude Project mirrors the text docs.
6. No official logos or seals. Names are plain lettering. Real people are drawn as recognizable caricatures through hair, jaw, brows and accessories.

## 6. Open work (priority order)
1. Hands: real hand shapes (mitten with thumb, grip, point) and more pose presets.
2. Landmark accuracy: a photo-reference step before drawing any real place, with proportions checked against the photo.
3. More complex objects: layered tones, more detail; consider an SVG import path for designer-made assets.
4. Voice track: produce the narration first and derive shot durations from it. Drive lip-flap from audio amplitude (designed, not built).
5. Slimmer production context for Qwen: the first steps are done (`PROMPT_PRODUCTION.md`, downscaled reference images). Measure the effect on the next run.
6. Transitions and camera variety beyond hard cuts.

## 7. Token economics (for planning)
- **Founding session:** Haiku about 290k (shot catalogue) plus about 100k per QA pass. Sonnet: about 80k per writing task and 95–150k per batch of 4–5 shots.
- **Qwen run 1, 3 shots:** 0.83M uncached input, 6.4M cached input, 68k output. Almost all of it was re-reading context and images in its render/review loop, not writing code.
- **Levers:** smaller images, a slim production prompt, batches of 10–15 shots, a cap on full-resolution checks, and brief-checking done by the strong model so Qwen needs fewer rounds.

## 7b. Vietnam video token and cost facts (2026-10)
- Opus did the whole first build (~150k) plus Act 1 setup (~225k) plus the v2 brief (~60k); Sonnet sub-agents drew ~40 props (~354k tokens, all kept).
- The Qwen v2 run: 25M uncached input, 45M cached, 225k output (about 300:1 read:write, caused by parallel helpers re-reading the same files). Priced by model that is about $2.7 MiMo, $3.1 Haiku, $4.6 Qwen, $57 Sonnet, $113 Opus.
- List prices per M tokens in/out: MiMo v2.6 Flash 0.10/0.28 (cache 0.003), Qwen 3.8 Flash 0.15/0.47, Haiku 5.5 0.10/0.50 (cache 0.01; prompts over 100K cost 5x), Sonnet 5.5 2/10 (cache 0.10), Opus 5.5 4/20 (cache 0.20).
- Lesson: cost follows which model READS tokens. Keep the strong model on direction, rules and judgment; cheap models build; scripts check; build the plan and run the checks before drawing so nothing is built twice.
