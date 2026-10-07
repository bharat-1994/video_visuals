# Studio-grade documentary from code — the replicable playbook

How the Lakshadweep film (8 acts, 8 min 50 s, 1080p24, Telugu VO, original score + sound design) was made, written so **any capable LLM with a shell** can repeat it for a new topic, in a new language, and still get a film with its own identity.

> **Start with `DIRECTORS_GUIDE.md`.** This file documents how *this* film was implemented (tools, numbers, recipes). Use it as a worked example and parts list, not as the rules for every film.

Read in this order: **1 Principles → 2 Pipeline → 3 Decision guidelines (rules vs dials) → 4 Audio recipe → 5 Picture recipe → 6 QA → 7 Pitfalls → 8 Starting a new film.**
Copy-paste prompts for each phase are in `PROMPTS.md`. Working reference code is everything under `render/` and `build/` in this folder.

---

## 1. Principles (why it looks like cinema, not a slideshow)

1. **The voice is the clock.** Every cut, title, SFX hit and music change is placed from word-level timestamps of the narration, never "by feel" on a free timeline. If the audio changes, re-derive the edit.
2. **Motion on every frame.** No static image ever sits still: stills get a slow push/pan; footage gets a slight scale; maps fly; particles drift. A shot with nothing moving is a bug.
3. **Show the idea, not the sentence.** Pick the visual for what the line *means* (a Hyderabad grid for "1/20th of a city"; a rising mountain for "the ridge formed"), then footage, then photos. Text on screen is the last resort.
4. **Mix real and generated honestly.** Real footage/imagery wherever it exists; procedural animation where reality can't be filmed (geology, history, data). Never pass stock footage off as the actual place — credit it, and tell the user which is which.
5. **Sound is half the film.** Bed (ocean/wind/room tone) + music + spot SFX + transition whooshes, all ducked under the voice, mastered to a loudness standard.
6. **Calm beats dramatic.** Restraint: long dissolves, quiet harmony, silence between chapters. Save big hits for 3–4 moments per film.
7. **Verify by looking.** Render contact sheets and *read the pixels* before the full render. Cheap to fix at the sheet stage, expensive after.

---

## 2. Pipeline (phases, inputs → outputs, gate to pass)

| # | Phase | Output | Gate before moving on |
|---|---|---|---|
| 0 | **Brief** (ask the user ≤5 questions: visual sourcing, captions, output spec, music source, licences) | `brief.md` | User answered or defaults agreed |
| 1 | **Script**: acts + narration only (no visuals in the VO file) | `script.md`, `narration_only.md` | User approves tone/length |
| 2 | **Voice**: user records/generates audio per act, transcribes/aligns | `audio/NN_name.mp3`, `.timestamps.json` (char/word times), `.txt` (Telugu + English lines) | Alignment parses; every line found |
| 3 | **Timeline**: place acts on one master clock with pre-roll, gaps, outro | `timeline.py` (START per act, TOTAL) | Printed table makes sense |
| 4 | **Asset hunt**: find footage/stills/maps; *look at contact sheets* of candidates | `assets/…`, `CREDITS.md` data | Each act has ≥1 real asset per beat or a planned procedural scene |
| 5 | **Shot list** = one function per act listing every cut at an act-local time | `render/actN.py` | Preview sheet of the act reads well with subs |
| 6 | **Audio build**: score, environment SFX, transition SFX, voice chain, mix, master | `build/out/master.wav` | LUFS −16, TP ≤ −1.5, music never fights voice |
| 7 | **Render** in parallel chunks, resumable, then concat | `video_silent.mp4` | No `FAILED`, durations match |
| 8 | **Mux + deliverables**: 1080p master, small preview, SRTs, credits | `out/*` | Contact-sheet QA + black-frame scan pass |

Reference scripts per phase: `build/parse_audio.py`, `build/timeline.py`, `build/catalog*.py`/`mixkit_*`/`fetch_all.py`/`fetch_maps.sh`, `render/act*.py` + `render/preview.py`, `build/score.py` + `synth.py` + `sfx_trans.py` + `mix.py`, `render/render_parts.py`, `build/final.py`, `build/make_credits.py`.

---

## 3. Decision guidelines — **rules** vs **dials**

The danger of a playbook is that every film comes out identical. So decisions are split:

### 3a. HARD RULES (don't break; they are craft, not style)
- Narration timing drives the edit; every subtitle line = one aligned segment; no overlapping subtitle windows.
- Subtitles: ≥ 44 px at 1080p, max 2 lines, lower-third soft gradient, shaped with a real complex-script engine (HarfBuzz/Raqm). **Mixed-script lines must be drawn run-by-run with the right font per script** (see Pitfalls).
- Loudness −16 LUFS integrated, true peak ≤ −1.5 dBTP, voice always intelligible: music ducks ≥ 5 dB under speech.
- Never edit on a cut shorter than 0.8 s unless it is a deliberate rhythmic burst (≥3 in a row).
- No unattributed licensed material. Keep a machine-generated `CREDITS.md`.
- Every claim that is legend/oral tradition is *labelled* as such in the VO; visuals must not "prove" it.
- Do not claim stock footage is the real location. Say so in the delivery note.
- Gaps between acts: dip to black through ≥1.5 s of music-only breathing room.
- Always provide a preview/small export; never ship an un-QA'd render.

### 3b. DIALS (decide per film; write your choice into the brief — this is where identity comes from)
| Dial | Options / how to choose |
|---|---|
| **Palette** | Pick 1 hero + 1 accent grade family from the topic (here: teal/turquoise hero, warm dusk accent). Different film → different family (desert: amber/sand; city: steel/neon). Grades are just LUT numbers in `GRADES`. |
| **Pace** | Average shot length. Reflective piece: 4–7 s. Energetic: 1.5–3 s. Keep 60% of shots within ±40% of the film's own average, with a few outliers on purpose. |
| **Transition vocabulary** | Choose 3 "native" transitions for the film (here: dissolve default, whip for questions/shocks, iris/flare once). Using all 8 equals a template. Rule of thumb: dissolve = time/continuity, whip = shock/answer, iris = reveal, dip = chapter, flare = warmth/memory. |
| **Music world** | Key/mode, instrument family and motif are chosen from the culture/place (here: D Dorian, tanpura drone, bansuri flute, frame drum, glass bells for "growth"). A new film must change at least two of: tonic, mode, lead instrument, rhythm feel. |
| **Motif logic** | One 5–7 note motif for the film; return in Act 1 and the last act changed (bells for growth in Act 2 echo in Act 8). Leitmotifs create cohesion without sameness. |
| **Title style** | Typeface pairing, spacing, position. Title in native script + spaced Latin caption was chosen here; change it per film. |
| **Procedural scene set** | Invent scenes from the *content* (this film: dot-cloud "lakh", 20-square city comparison, atoll cross-section, trade routes, flag, cyclone, sea-level, matrilineal diagram). Don't reuse last film's scenes unless the topic needs them. |
| **Density of on-screen text** | Default "almost none": tags for places (≤5 s), year cards at 3–5 moments. Ask the user. |
| **Sound design density** | Beds always; spot SFX only where something audible happens on screen. 10–15 hits/act is plenty. |
| **Level of AI-generated imagery** | If an image/video generator is available and the user allows credits, use it for 5–10 hero shots *only*; keep the same style prompt for consistency. Otherwise code + free assets (what we did). |

**Anti-sameness check before rendering:** write the film's one-line identity ("calm, turquoise, tanpura + bansuri, whip only for questions") and confirm it differs from the last film in at least three dials.

---

## 4. Audio recipe (this is the part people get wrong)

### 4a. Stems, all synthesised in numpy at 48 kHz stereo (`build/synth.py`)
- **Instruments** (each returns a mono clip; panned/placed with `place(bus, clip, t)`):
  - *Tanpura string*: Karplus-Strong (`lfilter` with a delay-line feedback) + soft-clip that blooms over the note ("jivari" buzz). Pattern Pa–Sa–Sa–low Sa every ~1.5 s as a constant drone.
  - *Pad*: 4 detuned saws per channel (±2–9 cents), low-passed ~1–2 kHz, slow attack (≈2 s), long release. Chords from a hand-written list; overlap them by ~3 s.
  - *Piano*: inharmonic additive partials with decay shortened by partial number + a hammer noise burst. Used for arpeggios and sparse emphasis.
  - *Glass bell*: partial ratios 1, 2.76, 5.4, 8.93 with long decay. Used as "growth" (accelerating, ascending random notes) and "bleaching" (descending, dying).
  - *Flute (bansuri-like)*: sine + 2nd/3rd harmonics, breath noise (band-passed), chiff transient, vibrato that fades in after ~0.4 s, optional glide from a lower note.
  - *Frame drum / dhol / shaker / tick / clap*: pitch-dropping sine + band noise, decays 40–160 ms.
  - *Sub boom*: pitch-falling sine 90→32 Hz + low-passed noise burst. 3–4 per film.
- **Risers**: white noise through a *swept* band-pass (`sweep_noise`), Q≈1.5–3, envelope `t^2.2` (in) or `sin(πt)^1.6` (swell). 4–6 s before a reveal.
- **Environment SFX**: ocean = pink noise low-passed 1.8 kHz modulated by random wave envelopes (attack 2–3.5 s, decay ~28% of period) + foam hiss delayed 0.6 s, decorrelated per channel; wind = band-passed pink noise with slow gust envelope; gull = three FM chirps; thunder = low-passed noise with 3–5 decaying rumbles; rain = high-passed noise; underwater = LF rumble + bubble sines with rising pitch; creaks = swept resonant noise.
- **Reverb**: generated impulse response (filtered noise × exponential decay, RT60 ≈ 4.2 s for music, 2.4 s for SFX), applied by FFT convolution. Send music pads/flute/bells to the reverb bus; keep drums and booms mostly dry.

### 4b. Composing to picture (`build/score.py`)
1. For each act write: **mood in one word → chord progression (8 s per chord) → a motif → 2–4 "hit points"** tied to narration times (e.g. "a calm lagoon in the middle" → major chord arrives 41.0 s).
2. Always: drone under the whole act at low level (tanpura vel 0.18–0.30), pad chords, optional pulse/groove only where the narration lists things or speeds up.
3. Tension = flat-6/b5 colour + vibrato pad + sub pulse + riser; Resolve = major triad + flute motif + piano arpeggio.
4. Groove sections are short (10–20 s), 60–116 bpm, and *fade in/out* over 2–3 s; they correspond to action (travel, work, dance), never wallpaper.
5. Place booms only on narrative turns (title drop, "the locals did not stay quiet", cyclone, "flag already flying", final line).
6. Leave ≥ 1 s of near-silence after each act's last word before the next act's first sound.

### 4c. Environment bed per act (levels are automation curves, `level_curve`)
- Ocean continuous, level 0.25–0.65 depending on scene (0 underwater scenes; peak for storm).
- Wind 0.06–0.14 normally, ramping to 0.55–0.95 for the cyclone, then dropping to 0.2.
- Underwater room tone replaces ocean when the picture goes under.
- Spot SFX list is derived by reading the shot list: gulls, map pings (when markers appear), boat creaks, paper flutter (archive sections), splashes (fishing), cloth flap (flag), thunder + rain (storm), plane whoosh/horn, drips (water).

### 4d. Voice chain (`build/mix.py`)
`high-pass 75 Hz → +1.5 dB @190 Hz → +2.2 dB @3.2 kHz → −1.5 dB @9 kHz → soft-knee compression (thr 0.12, ratio 2.2, 30 Hz smoothing) → normalise speech RMS to 0.115 (≈ −19 dBFS) → tiny room (450 ms IR, 10% wet, 37-sample L/R offset)`.

### 4e. Ducking + master
- Envelope follower on the voice (attack 40 ms, release 550 ms).
- Music gain = `1 − 0.62·clip(env/0.06)`, SFX gain = `1 − 0.40·…`, both smoothed to 3 Hz. Music RMS target 0.060, SFX 0.030 (before ducking). Transition whooshes: ×0.55.
- Fade-in 0.5 s, fade-out 5.5 s, soft limiter `tanh(0.9x)`.
- Two-pass `loudnorm I=-16 TP=-1.5 LRA=11` with measured values, `linear=true`. Verify with `ebur128`.
- **Check**: per-act dB table of voice/music/SFX before ducking; voice should sit ~4 dB over music, SFX ~10 dB under voice.

### 4f. Making it different next time
Change the *world*, not the engine: new scale/mode and tonic, new lead instrument (swap `flute()` for a plucked/bowed synth or sampled instrument), new rhythmic feel, new bed (city room tone, forest, wind-in-grass). Keep 4b rules.

---

## 5. Picture recipe

### 5a. Engine (`render/engine.py`)
- Shots are objects with `.frame(t) → RGB uint8`; a `Timeline` composites `Entry(start, factory, transition, tdur, grade)`. Shots are built lazily and released when passed (memory flat).
- Per-shot grade (`GRADES`, LUT-based S-curve + split-tone + saturation), then a *global* finish once per composited frame: highlight bloom (down-scaled, blurred), vignette (0.55), film grain (12 pre-computed 1080p noise frames cycled).
- Transitions: dissolve, dip (to black/white), whip (slide + directional blur), zoom-through, flare (warm flash), iris, luma (organic noise matte), cut.
- Overlays: location tag (hairline + spaced caps), titles (letter-spaced), year cards, subtitles (mixed-script runs, soft gradient).
- Output via raw RGB pipe to `ffmpeg libx264 -crf 20 -preset fast`, **chunked every 20 s and rendered in parallel (4 processes)**; resumable; concatenated with `-c copy`.

### 5b. Asset sourcing (in order of preference)
1. **NASA GIBS WMS** (public domain): Blue Marble bathymetry/relief, MODIS/VIIRS true colour, HLS 30 m true colour, Black Marble night lights. Build a **multi-resolution stack** (world → regional → island) with feathered masks and frequency-separation colour matching (`render/geo.py`, `build/match_layers.py`) so a camera dive from space to a 30 m island is seamless.
2. **Mixkit** (free commercial licence): crawl category pages → `mixkit_index.json`; get direct file URLs from the page's JSON-LD (`contentUrl` = HD, `embedUrl` = preview); ids < 100000 follow `/videos/{id}/{id}-1080.mp4`. Always fetch 360p previews first and **look at contact sheets** to choose.
3. **Wikimedia Commons / archive.org / Openverse→Flickr (CC)** for local stills and history. Commons video downloads rate-limit hard (HTTP 429, `Retry-After: 600`) — fetch earlier in the session, slowly, with a descriptive User-Agent, honour Retry-After, and have a fallback.
4. **Procedural generation** when nothing exists: cross-sections, diagrams, maps, silhouettes, flags, cyclone swirl on real satellite imagery.
5. Image generators/AI video **only** if the user supplied credits; otherwise skip.

### 5c. Choosing a visual per narration line (decision order)
1. Can the line be shown as a **map/data/diagram** that *is* the idea? → procedural scene.
2. Is there **real footage** of the thing? → use it, 4–6 s, slight push.
3. **Real still of the place** → Ken-Burns 5–8 s with `shake=0.3–0.6`.
4. **Texture/mood footage** (waves, light, sky) that matches the emotion → fine as connective tissue, ≤ 25% of the film.
5. Never: logo-ish clip art, a still held without motion, text-only slides.
Alternate **wide → close → abstract** every 2–3 shots; don't put two same-framing shots adjacent.

### 5d. Procedural scenes that generalise (reusable patterns)
Route/path drawing with glowing head • pulsing location markers • camera path through log-space zoom • dot-cloud → count reveal • area-comparison grid • cross-section with sea level • swirl warp for storms • split-screen slider wipe • timeline year cards • light-pulse network map.

### 5e. Titles/captions policy
Subtitles on (user-chosen), burned in; everything else sparse: place tags at first visit of a location, big year numerals at date turns, title at 1–4.7 s, credits at the end. Never caption what the picture already says.

---

## 6. QA checklist (do all; each caught a real bug in this project)

- [ ] Alignment: each narration segment found in the char-timestamp stream (print count found vs expected).
- [ ] Per-act preview contact sheets with subtitles (`render/preview.py ACT 2`): look for dark frames, wrong clip, clipped whites, missing assets, watermarks (crop them out in `WM_IMAGES`).
- [ ] Mixed-script subtitle test string rendered once (Telugu + Latin) — tofu boxes mean the wrong font for a script run.
- [ ] Black-frame scan of the final: only chapter gaps/ends (and deliberate beats) may be near-black.
- [ ] Audio: LUFS/TP numbers, per-act level table, spectrogram glance.
- [ ] Transitions: no stuck double-exposure of two unrelated shots for >1.2 s.
- [ ] Contact sheet of the *final* file every 7 s: story reads, no repeats of the same clip within 90 s (unless it is a deliberate callback).
- [ ] Delivery note says what is real vs stock vs generated and lists legend-based claims.

---

## 7. Pitfalls we hit (and the fix)

| Symptom | Cause | Fix |
|---|---|---|
| Telugu subtitles show boxes / Latin words as boxes | A single font used for mixed script | Split text into script runs; draw Telugu with Noto Sans Telugu, Latin with Jost, advance x by each run's length; wrap using mixed length |
| `ValueError: assignment destination is read-only` mid-render | `np.frombuffer` frames from ffmpeg are read-only | `.copy()` the array in the reader |
| `Broken pipe` spam from ffmpeg when probing | Reader killed early | Harmless; close reader or ignore |
| Wikimedia 429 on every request | Shared egress IP + bulk requests | Slow, UA with contact, honour `Retry-After`; use the API only for search; prefer other sources |
| `sleep` blocked in the shell | Harness rule | Use a monitor/until-loop or background process + completion notification |
| Memory growth in long renders | Every shot kept alive | Lazy-build entries, `release_old()` every 2 s, process in 20 s chunks |
| Crash in one chunk loses everything | Pool exception | Catch per chunk, return `FAILED`, resumable parts on disk |
| Overlapping subtitles at line boundaries | Alignment end of line N > start of N+1 | Clamp each window to next start − 0.14 s |
| Satellite zoom shows hard rectangles | Fine layer meets coarse layer | Feathered distance-transform mask + colour match low frequencies |
| Dull deep-ocean imagery | Raw GIBS levels | Gamma 0.72–0.9, saturation 1.2, lift deep blues, unsharp mask |
| Cyclone white-out | Clipped cloud tops | Gamma 1.35 and cap at 235 before the swirl warp |
| Stock "beach resort" looks like the wrong place | Mixkit footage isn't the location | Prefer real stills of the place; pan slowly; disclose |
| Photographer watermark in corner | Source photos | Zoom ≥1.19 and bias crop up |

---

## 8. Starting a new film — the 10-step recipe

1. **Brief** (use the 5 questions in `PROMPTS.md#brief`). Record the dial choices (palette, pace, 3 transitions, music world, title style, scene set).
2. **Script** per `PROMPTS.md#script` — acts of 40–80 s, 14–19 lines each, conversational, one idea per sentence, hedge unverifiable claims. Strip to narration-only for TTS.
3. User produces voice + alignment. Parse → `segments.json` (`build/parse_audio.py`).
4. Edit `timeline.py` (pre-roll 5 s, gap 1.6 s, outro 10 s).
5. Fetch maps/imagery/assets; **look at contact sheets**; write the asset tables.
6. Write `render/actN.py` — one `cut(act, local_time, factory, transition, tdur, grade, name)` per beat, anchored to segment start times from the table in `segments.json`.
7. Preview every act (`render/preview.py N 2`), fix, repeat.
8. Compose/score + SFX (`score.py`, `sfx_trans.py`), mix (`mix.py`), check numbers.
9. Render in parallel (`render_parts.py 4 20 20`), mux (`final.py`), SRT + credits (`make_credits.py`).
10. Final QA checklist; deliver master + preview + SRTs + credits + a plain-language "what's real/stock/generated" note.

### What is reusable vs. content-specific in this repo
- **Reusable as-is**: `render/engine.py`, `geo.py`, `fx.py`, `assets.py`, `shots.py`, `film_core.py`, `render_parts.py`, `preview.py`; `build/synth.py`, `mix.py`, `sfx_trans.py`, `final.py`, `make_credits.py`, `parse_audio.py`, `timeline.py`, `mixkit_lib.py`, `fetch_all.py`, `fetch_maps.sh`, `commons.py`, `ov.py`.
- **Content-specific (rewrite per film)**: `render/act1..8.py`, `scenes_a1.py`, `scenes_a2.py`, `scenes_misc.py` (borrow patterns), `build/score.py` compose() body, `data.py`, `want_*.json`.

### Time/cost reference (this film, 4 vCPU, no GPU)
Score+SFX synth ≈ 4 min • mix+master ≈ 1.5 min • full 1080p render ≈ 30–40 min wall (27 chunks × 4 workers) • all assets free.
