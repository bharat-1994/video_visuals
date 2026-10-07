# Director's guide — how to *think* through any documentary (tool-agnostic)

> **The exhaustive version is the `handbook/` folder (start at `handbook/00_INDEX.md`).** This file is the short summary.

This is the reasoning behind the Lakshadweep film, stripped of tools. It works whether you have code, a video editor, a stock library, an AI video/music generator, or a mix. `PLAYBOOK.md` and `PROMPTS.md` describe *how this film was implemented*; this file describes *how decisions get made*.

**One honest note:** if you only read `PLAYBOOK.md` you will copy this film's *solutions* (numbers, synth recipes, palette). Read this file first; use the playbook only as a worked example and a parts list.

---

## 0. The five questions behind every single decision

Ask these at every shot, sound and title. If you can't answer, you're decorating.

1. **What must the viewer understand or feel in this exact moment?** (one thing)
2. **Which channel carries it best — picture, sound, or words?** The voice already carries words; don't make the picture repeat them.
3. **What is the least I can do that achieves it?** Remove until it hurts, then put back one thing.
4. **What came just before and what comes next?** Contrast and continuity are decided in pairs/triples, not alone.
5. **Would this choice appear identically in a different film?** If yes, it's a habit — re-decide it from this topic.

---

## 1. Understand the story before touching a tool

1. **One-sentence promise.** "This film shows that a tiny place is held together by tiny creatures and careful people." Every beat serves it or is cut.
2. **Shape it.** Good documentary arcs repeat: *puzzle → origin → people → history/power → daily life → threat → lesson*. Pick a shape, give each act **one job**, and make the last act echo the first.
3. **Hook that corrects a misconception** ("lakh islands — actually 36"). It makes the viewer lean in and gives you an easy callback at the end.
4. **Calibrate certainty.** Facts, widely told stories, legends: label each. The visuals must never "prove" a legend.
5. **Emotional temperature curve.** Mark each act: calm / curious / tense / hopeful. Rough rule: don't have two tense acts in a row; end warm and reflective.

*Output:* promise sentence, act list with one-job each, temperature curve.

---

## 2. Let the voice set the clock

The narration is the spine. Everything else hangs off *when words are spoken*.

- Break each act into **beats** = one idea each (usually 1–2 sentences). Note start/end seconds.
- **Cut on the idea, slightly before the word that names it** (0–0.15 s early). The image arrives, then the word explains it.
- **Shot length follows information density**: a number or abstract claim needs a *longer* hold (viewer must read the picture); an emotional line needs a *held* shot; a list ("fish, coconut, rice") wants quick cuts.
- **Breath = space.** After a striking line, hold the picture 0.5–1 s with no new information.
- Between chapters leave **1.5–3 s of near-silence/black** so the viewer resets.

*Test:* mute the picture, listen to the voice — are there places where nothing in the picture would change but you've cut anyway? Remove those cuts.

---

## 3. Choosing a visual for each beat (the decision ladder)

Go down the ladder; stop at the first rung that works.

1. **Can the idea itself be drawn?** (a map, a diagram, a size comparison, a timeline, a cross-section, a count.) Then draw it. This is what makes a documentary feel designed rather than assembled.
2. **Is there real footage of exactly this?** Use it.
3. **Is there a real photograph of the place/person/object?** Use it with slow camera motion.
4. **Is there footage that carries the same emotion even if it isn't the place?** (light on water, a fisherman at dusk.) Fine as connective tissue, but be honest about it and keep it a minority.
5. **Nothing fits?** Rewrite the beat, don't stuff in filler.

### Worked examples (line → thought → choice)
| Narration | Thinking | Choice |
|---|---|---|
| "There are 36 islands, only 10 inhabited." | A count. Show countable things. | Satellite map; 36 dots appear one by one; 10 glow warmer. |
| "…not even one-twentieth of Hyderabad." | A comparison viewers can feel. | City-lights map; one square = all of Lakshadweep; 19 more squares tile the city. |
| "A mountain range formed at the bottom of the sea." | Can't be filmed. | Simple cross-section animation of the ridge rising, lit warm. |
| "Tiny creatures began to grow." | Needs intimacy. | Macro footage of coral polyps; later reprised in the last act. |
| "Sailors came from the Kerala coast." | Movement and direction. | Animated routes on a satellite map. |
| "Pakistan's navy was coming… a few hours later." | Tension/time. | Two routes racing across the map; then the flag footage. |
| "Coral bleaching." | Loss, visible. | Same reef footage, colour drains over the shot. |
| "Taking only as much as needed." | Quiet, ethical. | Calm fishing shots, no music pushing. |

### Variety within a sequence
Alternate **wide → close → abstract**. Don't put two shots with the same framing, same colour and same motion direction next to each other. Every shot **moves a little** (push, pan, drift) unless stillness is the point.

### Honesty rule
Never present a stock clip as the real place. Credit everything. Tell the client which shots are real, stock, generated and legend-illustrating.

---

## 4. Transitions mean something — choose a small vocabulary

| Transition | Use for |
|---|---|
| Dissolve | time passing, continuity, gentle thought-links |
| Hard cut | answer to a question, a beat on the drum, an interruption |
| Whip / fast slide | shock, a list, a rapid change of topic |
| Dip to black | chapter ends, endings |
| Iris/reveal | a size or scale reveal, once per film |
| Flash/flare | memory, warmth, a "light" moment |

**Pick 3 signature transitions for the film** and use others at most once. Using every transition is the fastest way to look like a template.

---

## 5. Look and colour

1. **Derive the palette from the topic**, not from taste: place light, materials, emotion. (Island film → turquoise hero, warm dusk accent.) Write it as: *hero colour, accent colour, "danger" colour, "history" colour.*
2. **Grade as emotion.** Cooler/desaturated for threat; warm for people; sepia/low-saturation for history; bleached for loss. Make the *change* of grade the signal, not an effect.
3. **Consistency across heterogeneous sources**: footage from many sources will clash. Use a common finishing pass (slight contrast curve, same bloom/vignette/grain) so they feel like one film.
4. **Text colour/style** is part of the palette; keep it restrained (thin, spaced capitals for tags; large light numerals for years).

---

## 6. Text on screen — default to almost none

Use text only when a place name, a date, or a number *must* be read and the voice can't carry it. Subtitles are a separate accessibility layer: legible, 2 lines max, no collisions. Never caption what the picture already shows.

---

## 7. Sound — a director's way to think about it

Sound is half the film. Plan it in **four layers**, in this order:

1. **Voice** — clean, present, consistent. Everything else serves it.
2. **Bed (ambience)** — the world's room tone: sea, wind, city hum. It is continuous and changes with the scene (underwater vs shore vs storm). It makes cuts feel smooth.
3. **Music** — emotion and structure.
4. **Spot sound** — specific things you can see or imply (a boat creak, a flag flap, a splash) and **transition sounds** (soft whooshes, low impacts).

### 7a. Writing a music brief (works for a composer, a library search, or an AI music generator)
Answer these *before* making any music:
- **World:** What culture/place does this belong to? Choose scale/mode, lead instrument and rhythm feel from it (e.g. drone + bamboo flute + frame drum). Avoid generic "cinematic epic".
- **One motif:** 5–7 notes that can return changed (rising for hope, descending for loss).
- **Arc per act:** one word for the mood (wonder / reverence / tension / joy / unease / resolve) and what changes at the act's key line.
- **Hit points:** 2–4 per act, tied to specific narration moments; everything else is *under* the voice.
- **Where music stops:** at least one place per act where nothing plays and the bed/voice carry it.
- **Dynamics:** most of the film sits 10–14 dB under the voice; big gestures (a low hit, a riser) only on turns of the story, 3–4 per film.
- **Reference:** describe 2 reference moods, never a specific copyrighted tune.

### 7b. Spot-sound logic
Add a sound only when (a) something audible is visible/implied, or (b) a transition needs to feel physical. If you can't point to the frame that justifies it, delete it. Lots of small, quiet, well-placed sounds beat a few loud ones.

### 7c. Mix principles (tool-independent)
- Voice is the loudest *consistent* element; music ducks **~5–8 dB** while someone speaks and recovers slowly (≈0.5 s) so it breathes.
- Low frequencies of music and voice fight; roll off music under the voice's body range or lower its level there.
- Reverb adds depth to music and soft sounds; keep voice nearly dry with a hint of room.
- Master to the platform standard (YouTube-style **−14 to −16 LUFS integrated**, true peak ≤ −1.5 dB). Check with a loudness meter, don't trust ears at one volume.
- Listen on laptop speakers *and* headphones.

### 7d. How to get the sound with different tools
- **Code only:** synthesise (see `PLAYBOOK.md` §4).
- **AI music/SFX generators:** use the music brief above as the prompt, generate per act, keep the same instrument/mode wording in each prompt for coherence, then mix by the same rules.
- **Royalty-free library:** search by *mood + instrument*; edit to the hit points; layer your own ambience.
- **DAW:** same layers, same ducking via sidechain.

---

## 8. Review like a director (do this before calling anything "done")

1. **Sound-off pass:** does the picture alone tell a coherent, varied story?
2. **Picture-off pass:** does voice + sound alone feel finished?
3. **Beat check:** at each beat, does the first frame after the cut show the new idea within 0.5 s?
4. **Contrast check:** list consecutive shots; flag any pair with the same framing/colour/motion.
5. **Repeat check:** any clip reused within 90 s without intent?
6. **Honesty check:** which shots are not the real place? Are they credited and disclosed?
7. **Dead-air check:** places where nothing moves or changes for >4 s (visual) or >8 s (sound).
8. **Mix check:** can you understand every word at low volume? Does anything jump out?
9. **Text check:** can any title/tag be deleted without loss? Delete it.
10. **Identity check (§9).**

---

## 9. Keeping every film different (without breaking craft)

**Keep constant (craft):** voice-driven timing, motion on every shot, honest sourcing, restrained text, clean mix, loudness standard, QA passes.

**Vary on purpose (identity):** palette, pace, signature transitions, music world (scale, instrument, rhythm), motif, title style, the *kinds of diagrams* you invent, opening and closing images.

Before starting a new film write its **identity line**, e.g. *"calm, turquoise, drone + flute + frame drum, whip only for questions."* If the identity line could describe the last film too, change at least three things — decide them from the *topic's* place, culture and emotion.

---

## 10. Adapting the process to your tools

| If you have… | Do this |
|---|---|
| Only a coding environment + free assets | Follow `PLAYBOOK.md` (this repo) end-to-end. |
| A video editor (Premiere/Resolve/CapCut) | Use §1–§9 as the edit brief; sourcing from stock/NASA; keyframe slow pushes; build diagrams in Figma/After Effects; use the timing table from §2. |
| An AI video/image generator | Use it for the *rung 4* shots and only a few hero shots; keep one style prompt; never to fake a real place; label as generated. |
| An AI music generator | Use the §7a brief per act; generate several takes; edit to hit points. |
| A human voice artist | Give them the script with breath marks; get per-act files and a word-level transcript for timing. |

---

## 11. What a new LLM should do (process summary)

1. Read this guide, then `PLAYBOOK.md` for examples.
2. Write: promise, act jobs, temperature curve, identity line, dial choices.
3. Write the script (one idea per line, hedged claims).
4. After the voice exists: beat table with timestamps (§2).
5. For each beat apply the decision ladder (§3) and write *why* in a one-line comment next to each shot.
6. Pick palette/transitions (§4–5), music brief (§7a), sound layers (§7).
7. Produce → review per §8 → fix → deliver with an honest sourcing note.

*Keep a decision log:* one line per major choice ("Chose X because the line means Y"). It lets a different model, or you, continue consistently — and it's the real "thought process" artifact.
