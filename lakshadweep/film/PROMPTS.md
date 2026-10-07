# Copy-paste prompts (any LLM with a shell + file tools)

Give the model this repo (or the `render/` + `build/` folders) and `PLAYBOOK.md`, then use the prompts below in order. Replace `{…}`. They are written to be model-agnostic: plain instructions, explicit outputs, explicit checks.

---

## 0. Master kickoff (paste once at the start of the project)

```
You are the director, editor, composer and sound designer of a documentary I want rendered entirely with code
on a CPU-only Linux box (python3, numpy, scipy, opencv, PIL with Raqm/HarfBuzz, ffmpeg).
Read PLAYBOOK.md fully before doing anything. Follow its HARD RULES. Treat its DIALS as decisions you must
make and write down per film — do not copy the previous film's dial settings.
Work in phases (PLAYBOOK §2). After each phase: show me evidence (printed tables, contact-sheet images you
have actually looked at, numbers), then continue unless I interrupt. Never skip the visual QA.
Be honest in delivery: say what is real footage, what is stock, what is generated, what is legend.
Topic: {topic}. Language of narration: {language}. Target length: {minutes} min. Audience: {audience}.
Output spec: 1080p, 24 fps, H.264+AAC, -16 LUFS. Subtitles burned in {language} + separate .srt.
```

---

## 1. Brief <a id="brief"></a>

```
Ask me at most five questions, each with a recommended default, covering:
1) where visuals may come from (free/public-domain downloads, my own library, paid AI credits),
2) caption style (burned subs only / minimal titles / none),
3) output spec (1080p24 default; 4K; vertical),
4) music & SFX source (synthesise original / I supply / placeholder),
5) anything I must not show (people, brands, politics, specific places).
Then write brief.md with: topic, audience, tone, length, languages, output spec, licences allowed, and the DIAL
DECISIONS (palette, pace, three signature transitions, music world [tonic, mode, lead instrument, rhythm],
motif idea, title style, list of procedural scenes you plan). End with the one-line identity of the film.
```

## 2. Script

```
Write a {minutes}-minute narration for {topic} in {language} as {N} acts (6–8). For each act:
- 14–19 short spoken lines; one idea per line; conversational, like explaining to a smart friend;
  light code-mixing with English where people really do mix; calm, not dramatic.
- Open with a hook that corrects a common misconception; close with a reflective payoff that echoes the opening.
- Hedge anything that is legend/oral tradition ("according to the belief…", "it is said…"). No invented facts.
  List every number/date you used in a "verify before publishing" block.
- Structure the story as: puzzle -> origin -> people -> power/history -> daily life -> threats -> what it teaches.
Output two files: script.md (with act titles) and narration_only.md (no headings, no stage directions,
no visual notes) for text-to-speech. No visuals in either file.
```

## 3. Voice alignment (what to ask the human)

```
Give me, per act: an .mp3 and a *character-level* timestamps json {graph_chars, graph_times:[[start,end]], duration}
plus a .txt of lines in the form "HH:MM:SS --> HH:MM:SS / native line / English line".
(Any forced aligner or TTS-with-timestamps works.)
```

```
Parse the files with build/parse_audio.py: locate each native line inside the concatenated characters,
store start/end seconds per line into build/segments.json. Print: act, lines expected, lines found, last end vs duration.
If any line is not found, fix the matching (strip quotes/spaces) — do not guess times.
Then edit build/timeline.py (pre-roll 5 s, gap 1.6 s, outro 10 s) and print the master timeline table.
```

## 4. Asset hunt

```
For each act, list the beats (one per narration line or group). For each beat decide the visual using
PLAYBOOK §5c (map/diagram -> real footage -> real still -> mood footage). Then:
- fetch NASA GIBS imagery (build/fetch_maps.sh pattern) for every geographic beat; create a multi-resolution stack
  and run the colour-match script so zooms are seamless;
- crawl/search free stock (Mixkit pattern in build/mixkit_*.py; Commons/Openverse for local stills);
- download 360p previews, build contact sheets with the clip id burned in, and LOOK at every sheet;
- write assets tables (id -> what it shows -> which beat) before writing any shot list.
Reject: wrong location that is presented as the real place, watermarks you cannot crop, clips with
people who could be identified in a negative context, anything without a clear licence.
```

## 5. Shot list

```
Write render/act{N}.py using the cut() helper: cut(act, local_seconds, factory, transition, tdur, grade, name).
Anchor each cut to a line start in segments.json. Rules:
- every shot moves (zoom/pan/particles); stills use Ken-Burns with slight shake;
- choose from the film's three signature transitions plus dip for chapter ends; do not use all transitions;
- the cut should land 0–0.15 s before the word that the new image illustrates;
- vary framing wide->close->abstract; no two similar frames adjacent;
- add a location tag only the first time a place appears; year cards only for date turns;
- write procedural scenes as FuncShotF(fn(t, dur, state)) functions, vectorised with numpy/opencv, <1.5 s/frame.
Then run render/preview.py {N} 2 and open the sheets. Fix: wrong clips, dark/blank frames, clipped whites,
subtitle collisions, watermarks, long dissolves that show two unrelated frames.
```

## 6. Score + sound design

```
Using build/synth.py primitives, compose build/score.py for this film. First write, per act, a table:
mood word | chords (8 s each) | motif | hit points tied to narration timestamps | groove? (where/why) | bed levels.
Constraints: the music world dials from brief.md; drone under every act at low level; booms only on narrative turns
(max 4); growth/decay gestures (ascending/descending bells) where the story has growth/decay; reverb sends for pads,
bells, lead; drums mostly dry; leave ≥1 s near-silence after each act's last word.
Environment beds: write level automation curves per act; add spot SFX by reading the shot list (list them first).
Generate transition whooshes from the actual edit (build/sfx_trans.py).
Mix with build/mix.py: voice chain, ducking (music -0.62 / sfx -0.40 at full voice), loudnorm -16 LUFS, TP -1.5.
Report: per-act dB table (voice/music/sfx) and ebur128 summary. If the voice is not ~4 dB above the music, fix the mix, not the voice.
```

## 7. Render & deliver

```
Run render/render_parts.py (4 workers, 20 s chunks, crf 20). It must be resumable and report per-chunk FAILED.
When complete: build/final.py (mux + 720p preview), build/make_credits.py (SRTs + CREDITS.md).
Run the QA checklist in PLAYBOOK §6, including the black-frame scan and a 1-per-7-seconds contact sheet of the final.
Deliver: master mp4, small preview, srt files, CREDITS.md, and a plain note: what is real / stock / generated /
legend; which shots you would replace if better footage were available; how to re-render a single act.
```

## 8. Revisions

```
I want to change {shot / act / music mood}. Edit only the relevant render/actN.py (or score.py section), preview that
act, and re-render only the affected 20-second chunks by deleting those part_XXX.mp4 files (resumable renderer).
Re-run the mix only if timing or SFX changed. Report what changed and what you verified.
```

---

## Prompts to keep videos from looking the same

```
Before starting, compare brief.md with the previous film's brief.md. List the dials that are identical.
If more than two are identical, change them and explain the reason from the *topic* (place, culture, emotion),
not from taste. Re-read PLAYBOOK §3b.
```

```
Invent three procedural scenes that only this topic needs (a diagram, a map behaviour, a data reveal).
Do not reuse scenes from earlier films unless the content is identical. Sketch each in one sentence, then implement.
```
