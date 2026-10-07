# 04 — Sound (music, ambience, SFX, voice, mix)

Sound is half of what makes a film feel "studio grade". The viewer rarely notices good sound; they feel it. This chapter gives a complete method, independent of tools, plus the recipes we used.

## 4.1 Principles
1. **Voice is king** — intelligible at low volume on a phone.
2. **Four layers:** voice → bed (ambience) → music → spot sounds (+ transition sounds). Plan them in that order.
3. **The world is never silent.** Even "silence" has a bed; true silence is a rare dramatic tool.
4. **Music has a world** (culture, place, instrument), a **motif**, and an **arc**. It supports; it doesn't narrate.
5. **Less, but placed:** a few sounds exactly on action beat many random sounds.
6. **Measure, don't guess:** loudness meter, per-act level table, headphone + laptop check.

## 4.2 Layer 1 — The voice

### Processing chain (any DAW/code)
1. High-pass ~70–80 Hz (remove rumble/pops).
2. Gentle warmth: +1 to +2 dB around 150–250 Hz (if thin).
3. Presence: +2 dB around 3 kHz (intelligibility).
4. De-harsh: −1 to −2 dB around 8–10 kHz if sibilant/synthetic.
5. Compression: soft knee, ratio ≈ 2:1, to even out sentences (don't squash).
6. Level: target speech around **−18 to −20 dBFS RMS** before the final master.
7. Room: a *tiny* room reverb (RT ≈ 0.3–0.5 s, 8–12% wet) to sit it in the mix; slight L/R decorrelation for width.

### Voice issues
- Synthetic voices can sound pasted-on — the room + shared bed with the world glues them.
- Breaths/pauses: keep them; they are rhythm. Trim only dead air > 0.8 s.

## 4.3 Layer 2 — The bed (ambience)

### Method
For each scene type write the *room tone*: shore (waves + wind), underwater (low rumble + bubbles), storm (wind + rain + thunder rumbles), village (distant voices, birds), city hum, forest, interior.

- **Continuous across cuts** — if the picture changes within the same world, the bed continues; this hides edit seams.
- **Level automation per act** (curve points), e.g. ocean 0.25–0.65; wind 0.06–0.14 normal, up to 0.9 in a storm; underwater bed replaces ocean when the picture goes underwater.
- **Stereo:** decorrelate L/R slightly (different random seeds/offsets) so it feels wide.
- Beds sit ~10–15 dB below the voice before ducking.

### Synthesis recipes (if no library)
- *Waves:* pink noise, low-passed ≈1.8 kHz, multiplied by random swell envelopes (attack 2–3.5 s, decay ≈ 28% of the period; periods 7.5–11.5 s) + a high-passed foam hiss delayed ≈0.6 s.
- *Wind:* band-passed pink noise (250–700 Hz plus a weaker 700–1800 Hz band) with a slow random gust envelope.
- *Underwater:* very low-passed noise (<180 Hz) + faint mid + rising-pitch bubble "bloops".
- *Rain:* high-passed noise + a little mid noise.
- *Thunder:* low-passed noise bursts with 3–5 decaying rumbles over 4–6 s.

## 4.4 Layer 3 — Music

### 4.4.1 The music brief (write before composing or prompting an AI)
```
World:        place/culture/era; instruments; scale/mode; rhythm feel
Palette:      3–6 timbres max (e.g. drone, pad, flute, frame drum, glass bells, piano)
Motif:        5–7 notes (rhythm + contour), how it transforms
Arc:          mood word per act + the turn
Hit points:   narration moments where music changes (with timestamps)
Rests:        where music stops
Dynamics:     typical level vs voice; peak events
Avoid:        genres/clichés (epic trailer hits, stock "corporate" piano), copyrighted references
```

### 4.4.2 Choosing the world (decision guide)
| Topic character | Modal/harmonic colour | Timbres | Rhythm |
|---|---|---|---|
| Indian coastal/cultural (this film) | Dorian/Mixolydian over a tonic drone (tanpura) | bansuri-like flute, frame drum, shaker, soft bells, warm pad | slow pulse 60–100 bpm, sparse |
| Desert/ancient | Phrygian dominant, drone | oud-like pluck, frame drum, low pad | free, slow |
| Industrial/tech | minor, ostinati | pulsed synths, clicks, low sub | steady 80–110, mechanical |
| Nordic/wilderness | Aeolian/Dorian, open fifths | strings, felt piano, field recordings | sparse, no pulse |
| Urban/street | minor pentatonic, syncopation | muted guitar, soft kit | 90–110, groove |
| Space/science | modal drones, suspended chords | pads, bells, sub | rubato |
Choose from the *topic's place and emotion*; never default to "cinematic".

### 4.4.3 Emotion → harmony cheat-sheet
- **Wonder/awe:** open chords (add9, sus2), slow harmonic rhythm (8 s per chord), high bells/piano, wide reverb.
- **Reverence/stillness:** drone + very sparse notes + long reverb; no percussion.
- **Curiosity/travel:** gentle rhythm (frame drum + shaker), arpeggiated piano, light flute motif.
- **Tension:** flat-2/flat-5/diminished colours over the drone, pad with vibrato, sub pulse (heartbeat 40–60 bpm), noise riser (4–8 s).
- **Danger/event:** low impact (sub boom 90→32 Hz, ~3–5 s), drum hits, filtered noise swells.
- **Loss/decay:** descending bell notes dying out, minor 6th/major 7th clusters thinning to a bare drone.
- **Hope/resolution:** return to major triad, flute motif at a higher register, piano arpeggio, harmonic rhythm 4–6 s.
- **Joy/community:** faster pulse (96–116 bpm), shakers/sticks, major pentatonic arpeggio.

### 4.4.4 Motif and development techniques
- Present the motif simply in Act 1 (flute/piano).
- **Transform** it later: harmonise differently (minor ↔ major), invert, stretch (augmentation), compress, move register, change timbre (flute → bells).
- **Callback:** bells that accelerate and ascend for *growth* (Act 2) return, calmer, in the final act.
- Give each mood a **signature gesture** (growth = ascending random bells; decay = descending bells with decreasing velocity; threat = low drone + sub pulse; hope = piano arpeggio + flute).

### 4.4.5 Per-act composition table (fill this per act)
```
Act | Mood | Chord loop (8 s each) | Motif use | Rhythm (where, bpm) | Hit points (time → event) | Rests | Reverb sends
```
Example (Act 2 of this film): wonder → Dm9 | Dm9 | Bbmaj7 | Dm9 (pads) + tanpura; tectonic rumble at 8.2 s; bells accelerate 23→46 s; sinking descent at 36.6 s; major chords from 41 s as the ring forms; flute at 46 s.

### 4.4.6 Structure of a cue
1. **Entry** 1–3 s *under* the previous silence or bed (never a hard start).
2. **Develop** using changing density (add/remove layers), not volume alone.
3. **Hit** (if any) 0.0–0.1 s after the key word starts, so the voice isn't masked.
4. **Resolve** or **drop** — cues rarely end abruptly; fade pads over 2–4 s.
5. Leave **≥1 s** of near-silence between an act's last word and the next sound.

### 4.4.7 Levels and ducking
- Music typically sits 10–14 dB below voice RMS under speech; it can rise 3–6 dB in pauses.
- Use **sidechain-style ducking** from the voice: reduction ≈ 5–8 dB (we used gain ×0.38 at full speech), attack ≈ 40 ms, release ≈ 0.5 s.
- Use a spectral gap: if music has strong 200–400 Hz, trim it so the voice's body can speak.

### 4.4.8 Instrument palette: how to realise it
| Palette | Realised with code | With samples/AI/DAW |
|---|---|---|
| Drone (tanpura) | Karplus–Strong strings + soft saturation; pattern Pa–Sa–Sa–low Sa every ~1.5 s | Tanpura loop sample; or sustained organ-ish drone at tonic+fifth |
| Pad | 4 detuned saws/channel, ±2–9 cents, low-passed ~1–2 kHz, 2 s attack, long release | Warm string/pad patch |
| Piano | additive partials with inharmonicity & hammer noise | Felt piano |
| Bells | partial ratios 1, 2.76, 5.4, 8.93, long decay | Glass/mallet patch |
| Flute | sine + harmonics + breath noise + chiff + fading vibrato | Bansuri/air flute sample |
| Frame drum | pitch-dropping sine + band noise (≈160 ms) | Frame/tabla/tom |
| Sub boom | pitch-fall sine 90→32 Hz + LP noise | Cinematic hit sample (low-passed) |
| Riser | swept band-pass noise, Q 1.5–3, exponential ramp 4–8 s | Reverse cymbal/noise riser |

### 4.4.9 AI music generator prompt template (if used)
```
[Genre/world]: warm ambient world-fusion, Indian coastal, tanpura drone in D, soft bansuri flute lead, frame drum, glass bells
[Mood/arc]: curious and calm, slowly opening, a gentle rise at 0:30, resolves warm at 0:50
[Tempo]: 70 bpm, mostly pulse-free
[Dynamics]: low, supportive, leaves room for a spoken voice, no sudden loud hits
[Duration]: 65 s, fade in 2 s, fade out 3 s
[Avoid]: epic trailer drums, cheesy piano, vocals, lyrics
```
Generate several takes per act; keep the same palette wording in every prompt; then edit to hit points and apply ducking.

## 4.5 Layer 4 — Spot SFX and transition sounds

### 4.5.1 The cue-sheet method
1. Watch (or read) the shot list. For each beat ask: *what would be audible here?* or *does this transition need weight?*
2. Write a cue sheet:
```
time | on-screen event | sound | pan | level | reverb? | notes
```
3. Group by function:
   - **Diegetic**: things in the scene (boat creak, splash, flag flap, gulls, rain, thunder, horn).
   - **Interface**: map pings when markers appear; soft ticks for chronometers.
   - **Transitions**: whooshes for whips/zooms/flares; low impacts for chapter openings.
   - **Narrative punctuation**: 3–4 booms per film.
4. Place 8–15 spot sounds per act at most. If you can't justify a sound by a frame, delete it.

### 4.5.2 Sound catalogue (what we used and how to realise)
| Sound | Trigger | Recipe |
|---|---|---|
| Gull | sea/sky scenes | 3 FM-swept chirps 0.25–0.35 s each, band-passed 700–6500 Hz; place sparsely, panned, with reverb send |
| Boat creak | boats/ships | band-passed noise with slowly wandering centre (170–260 Hz), 0.8–1.2 s |
| Splash | fishing | band-passed noise burst 0.3–0.5 s + LF thump |
| Ping | map marker | sine ~1.2 kHz with fast attack, 0.5 s decay, soft reverb |
| Flag flap | flag raised | band noise 120–1400 Hz amplitude-modulated at ~7 Hz with random wobble |
| Paper flutter | archive/newsreel moments | high-passed noise with sparse random gating |
| Thunder | storm | LP noise with multiple rumbles |
| Rain | storm | high-passed noise bed |
| Horn | ship/plane | two low sines (~98 + 147 Hz), slow attack/release |
| Drip/bubbles | water scenes | short rising-pitch sine blips |
| Whoosh | whips, flares, zooms | swept band-pass noise: whip 400→4200 Hz swell; zoom 250→2500 Hz rising; flare 600→7000 Hz swell |
| Boom | narrative turns | pitch-falling sine + LP noise burst, 3–5 s, mostly dry |

### 4.5.3 Placement rules
- Spot SFX are **~8–12 dB below voice**; they're felt, not heard.
- Place the sound **at** the action (or 0.05 s early for anticipation), never late.
- Pan to match screen position if possible; otherwise slight random pan ±0.5.
- Send 30–70% of SFX to a small reverb (RT ≈ 2–3 s) to place them in space.
- Vary: no two identical SFX within 10 s; vary pitch ±5% or choose another variant.

### 4.5.4 Using silence
- After a shocking line: duck everything for 0.5–1.0 s.
- Before a reveal: let the bed thin out 1 s before the hit.
- Act ends: music tail → bed only → black.

## 4.6 Reverb (space)
- Music reverb: long (RT60 ≈ 3.5–4.5 s), pre-delay 20 ms, darker tail (low-pass the tail); send pads/flute/bells; keep drums mostly dry.
- SFX reverb: shorter (2–2.5 s).
- Voice: nearly dry.
- If generating impulse responses: filtered noise × exponential decay, three bands (low, mid, high) with different decay times, normalised energy.

## 4.7 Mixing and mastering

### Level plan (per act table — produce this!)
| Act | Voice | Music | Bed+SFX | Notes |
|---|---|---|---|---|
Pre-duck levels in our film (dB, RMS): voice ≈ −21; music ≈ −24; sfx ≈ −24 to −37 depending on scene; after ducking music sits ~5–7 dB lower during speech.

### Steps
1. Normalise each stem's long-term level to target RMS (voice ≈ 0.115 ≈ −19 dBFS; music ≈ 0.06 ≈ −24.4 dBFS; bed/SFX ≈ 0.03 ≈ −30 dBFS) *before* ducking.
2. Create a voice envelope follower (attack 40 ms, release 550 ms).
3. Ducking gains: music ×(1 − 0.62·env); SFX ×(1 − 0.40·env); smooth the gain curves to ~3 Hz.
4. Add transition whooshes at ~0.55× and let them duck less.
5. Sum; apply a gentle soft limiter (e.g., tanh at 0.9 drive) to catch peaks.
6. **Loudness normalise** two-pass to **−16 LUFS integrated, true peak −1.5 dBTP** (platforms normalise around −14; −16 leaves headroom and avoids a harsh limiter). Keep LRA 8–12 LU for a calm documentary.
7. Fade-in 0.5 s at the start; fade-out ≥ 5 s at the end.

### Checks
- `ebur128`: integrated, true peak, LRA.
- 5-second RMS profile over the whole film: should hover within ±2 dB (no cliffs).
- Spectrogram: no broad 2–4 kHz mud under the voice; nothing above −3 dBFS.
- Listen: laptop speaker, earbuds, headphones. If a word is lost anywhere, fix the mix there.

## 4.8 Doing it without code
- **DAW** (Reaper/Logic/Ableton/Audition): four buses (Voice, Bed, Music, SFX); sidechain compress Music and SFX from Voice; reverb sends; loudness meter on master.
- **Video editor:** same layers on audio tracks; use "auto-ducking" cautiously — check by ear and by loudness meter.
- **AI tools:** generate per-act music and SFX; assemble in an editor; same mix rules.

## 4.9 Mistakes to avoid
| Mistake | Fix |
|---|---|
| Music constant at one level | Use arcs, rests, ducking |
| Booms too many | Max 3–4; each on a narrative turn |
| SFX everywhere | Only where justified; quiet |
| Hard music start/stop | Enter/exit under a bed; fade 2–4 s |
| Clashing keys between acts | Keep a tonic world; modulate deliberately |
| Voice buried in storm scene | Duck more; reduce wind 2–3 dB; add a high-pass on the bed under the voice |
| Reverb on voice too wet | Keep ≤12% |
| Different loudness per act | Level table; adjust automation |

## 4.10 Checklist (sound)
- [ ] Music brief and per-act table written.
- [ ] Bed levels automated per act; underwater/storm variants exist.
- [ ] Cue sheet derived from the shot list; each sound justified.
- [ ] Transition sounds generated from the real edit.
- [ ] Voice chain applied; ducking verified.
- [ ] −16 LUFS, TP ≤ −1.5; level table within ±2 dB; headphone + laptop check.
