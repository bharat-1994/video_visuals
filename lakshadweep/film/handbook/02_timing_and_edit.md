# 02 — Timing & edit

## 2.1 Principles
1. **The voice is the clock.** Not the music, not the picture. All timing derives from *when words are spoken*.
2. **Cut on ideas.** The first frame after a cut should show the thing the next words talk about, within ~0.5 s.
3. **Information density sets shot length.** Dense/abstract → longer holds; emotional → held; lists → quick.
4. **Rhythm is built from contrast** of shot lengths — not from a metronome.
5. **Space is a tool.** Pauses and chapter gaps make the next idea land.
6. **Transitions carry meaning**; keep a small vocabulary.

## 2.2 Getting reliable timing from the narration

### What you need
Per act: audio file + **word- or character-level timestamps** (forced alignment or TTS-with-timestamps) + the text lines.

### Procedure
1. Concatenate the aligned characters/words into one string per act.
2. For every text line, **find it** in that string (strip quotes/spaces if needed); take the first character's start and the last character's end. Count found vs expected — they must match.
3. Store as `segments[act] = [{text, translation, start, end}]`.
4. **Never guess times** for lines that weren't found. Fix the matching.
5. Place acts on a **master timeline**: pre-roll before the first word (4–6 s for title/cold open), a gap between acts (1.2–2.0 s of silence/black *plus* fades), outro (8–12 s for end card). Print the table: act start, end.

Why the pre-roll? The title and the first atmospheric image need time to land before the voice starts; it also lets the music establish.

### Subtitle windows
- One subtitle per aligned line.
- Show window = `[start − 0.08, end + 0.10]`, clamped to next line's start − 0.14 s so two never overlap.
- Fade in/out 0.16 s.

## 2.3 The beat table (the core planning artifact)

Break each act into **beats**: one idea per beat, usually 1–2 sentences, 2.5–9 s.

| beat | act-local start | end | narration (gloss) | idea | visual type | asset/scene | transition in | grade | sound note |
|---|---|---|---|---|---|---|---|---|---|

How to split:
- New noun the viewer must picture → new beat.
- A turn ("But…", "However…", "Because…") → new beat.
- A list → one beat per item if each is a distinct image, or a rapid sequence.
- Don't split mid-thought just because a line ends.

## 2.4 Shot length: defaults and logic

| Situation | Typical length | Notes |
|---|---|---|
| Establishing / mood | 4–7 s | Slow push; breathe |
| Informational (map, diagram) | 5–12 s | Hold so the viewer can read the picture; animate reveals inside |
| Emotional line | 4–6 s held, no cut until line ends | The pause after is part of the shot |
| List of items | 1.5–3 s each | Cut on each item |
| Callback/echo shot | same as original ± | Recognition needs time |
| Montage burst | 0.8–1.5 s each, ≥3 in a row | Only for acceleration (a chase, a dance) |

**Rules**
- No shot < 0.8 s except in an intentional burst.
- No static shot > 8 s without internal movement (camera, animation, particles).
- Aim for a *distribution*: ~60% within ±40% of the film's average length; 10–15% clearly longer; 10–15% clearly shorter. A film where every shot is 4.0 s feels mechanical.
- Longer than ~12 s is OK only for a designed sequence (a dive, a growth animation) that visibly *develops*.

## 2.5 Where exactly to cut

- Cut **0–0.15 s before** the word that names the new thing.
- Never cut during the *emphasised* word of a sentence; cut before or after.
- If two consecutive beats show different locations, use a transition that explains the move (dissolve = time; map move = space).
- If a line contains a *surprise* ("But the truth is different."), hold the previous picture until the surprise word, then cut or whip.
- **Echo cuts:** returning to an earlier image on the matching idea (coral polyps in Act 2 and Act 8) creates meaning.

## 2.6 Transition vocabulary with meaning

| Transition | Meaning | Duration | Notes |
|---|---|---|---|
| **Dissolve** (cross-fade) | time passes / ideas linked | 0.8–1.2 s (0.4–0.6 s when quick) | The default connective tissue |
| **Hard cut** | answer, interruption, beat | 0 | Use after a question, on a drum hit |
| **Whip / slide with motion blur** | shock, topic jump, answer | 0.35–0.5 s | The blur is what sells it |
| **Dip to black** | end of chapter, a death, an ending | 1.0–2.0 s | Also covers act gaps |
| **Iris / circular reveal** | scale reveal ("this is how small") | 0.6–0.9 s | Once per film |
| **Flash / flare** | warmth, memory, a spark | 0.6–0.8 s | Opening beat or one emotional turn |
| **Zoom-through** | travelling *into* something | 0.8–1.2 s | Pair with a push-in |
| **Organic (noise-matte) dissolve** | natural transformation | 1.0–1.5 s | Clouds, water — sparing |

**Select 3 signature transitions per film** from this table (plus dip-to-black for chapters). Using more than 4 makes the film look like a preset pack.

## 2.7 Chapter breaks and breathing
- End each act with the last word → hold 0.6–1.0 s → dip to black (1.0 s) → ≥0.6 s black/silence → next act fades up with the bed/drone first, **then** the first image.
- Never cut straight from the last word of an act to a loud/new musical event.
- The first line of an act can start on a fresh image *already moving*.

## 2.8 Pacing the whole film (macro)
- First 30 s: highest visual novelty per second (hook).
- Then settle to the film's native pace.
- Insert a **"rest"** every ~2 minutes: one long calm shot with no new info.
- Build to the tense act with slightly shorter shots and tighter music; resolve with the longest shots of the film in the final act.

## 2.9 Building the timeline in code or an editor

### In an editor
Put the audio on track A1. Lay down markers at every beat start. Place clips so their *first meaningful frame* is on the marker − 0.1 s. Add transitions. Export.

### In code (this repo)
- `segments.json` → beats → `cut(act, local_time, factory, transition, duration, grade)` calls.
- Each cut lives until the next cut + that cut's transition overlap.
- Timeline composites frames; transitions blend previous and current shots.

## 2.10 Checklist (edit)
- [ ] All segments found; counts match.
- [ ] Master timeline printed and sane.
- [ ] Every beat has an idea and a visual rung (chapter 03).
- [ ] Shot-length distribution varied; no <0.8 s except bursts.
- [ ] Only 3 signature transitions + dip.
- [ ] Chapter gaps present.
- [ ] Callbacks planned (at least one echo).
- [ ] Subtitle windows non-overlapping.
