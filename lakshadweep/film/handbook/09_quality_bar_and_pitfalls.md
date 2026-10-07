# 09 — Quality bar, pitfalls & the anti-sameness system

## 9.1 The 40 details that make it look expensive

**Story & script (1–6)**
1. A one-sentence promise every act serves.
2. A hook that corrects a misconception.
3. One idea per sentence; punchy short lines among longer ones.
4. Numbers converted into comparisons.
5. Legends explicitly hedged in the words.
6. The last act echoes the first (name/creature/image).

**Timing & edit (7–14)**
7. All timing from aligned narration; cut 0–0.15 s *before* the naming word.
8. Shot-length distribution varied; bursts only for acceleration.
9. Breath after strong lines; 1–3 s chapter breaks with silence.
10. A small transition vocabulary (3 + dip) with meanings.
11. One "iris" or equivalent used once for a scale reveal.
12. Callback shots (polyps in Act 2 and 8; "lakh" lights in Acts 1 and 5).
13. Different framing/colour/motion between adjacent shots.
14. A "rest" shot every ~2 minutes.

**Picture (15–26)**
15. Real data used for place (satellite imagery) rather than generic stock.
16. Drawn ideas (counts, comparisons, cross-sections, routes) instead of text.
17. Camera dives through resolution stacks with log-zoom easing.
18. Layers colour-matched and feather-masked so seams vanish.
19. Every still pushes/pans with micro-sway; every footage clip gets gentle scale.
20. Grade changes inside a shot to show change (bleaching).
21. Common finishing: bloom + vignette + grain across all sources.
22. Overlays obey a design language (glow, hairlines, spacing, easing).
23. Text almost absent: tags at first visit, year cards at date turns.
24. Subtitles: big, gradient-backed, 2 lines, shaped correctly for the script, no overlaps.
25. Watermarks cropped, stills upscaled with sharpening.
26. Particles/rays/caustics so subtle you only notice their absence.

**Sound (27–36)**
27. Four layers planned in order: voice, bed, music, spot.
28. Bed continues across cuts; changes with environment (underwater, storm).
29. Music has a world, motif, arc and rests.
30. Growth and decay have signature musical gestures (ascending vs descending bells).
31. Booms limited to ~4 and tied to narrative turns.
32. Spot SFX only where justified by a visible/implied event; panned; with reverb sends.
33. Transition sounds generated from the real edit.
34. Voice chain (EQ, compression, light room) and ducking with release ≈0.5 s.
35. −16 LUFS, TP ≤ −1.5, per-act level table checked.
36. Silence used deliberately (after shocks, before reveals, between acts).

**Process & honesty (37–40)**
37. Contact sheets for every act reviewed *by looking*, before full render.
38. Chunked, resumable parallel rendering; per-shot fix by deleting a chunk.
39. Credits generated; disclosures for stock/generated/legend.
40. Delivery note with compromises and upgrade suggestions.

---

## 9.2 Pitfalls we hit and how we resolved them

### Timing & text
| Symptom | Cause | Fix |
|---|---|---|
| A line "not found" in alignment | Quote marks/spacing differ | Normalise; match by prefix; never guess |
| Subtitles overlapping | Alignment ends overlap next starts | Clamp each window to next start − 0.14 s |
| Tofu boxes in Telugu+English subs | One font for both scripts | Split into script runs, different fonts, advance by run width |
| Text too low contrast on bright footage | Box or none | Smooth bottom gradient (not a box) + soft shadow |

### Visuals
| Symptom | Cause | Fix |
|---|---|---|
| Satellite zoom shows rectangles | Fine tile meets coarse | Feathered mask + low-frequency colour matching + enhancement |
| Dull, dark ocean in raw satellite | Raw levels | Gamma 0.72–0.9, saturation ×1.2, lift deep blues, unsharp |
| Cyclone washes to white | Clipped cloud tops | Gamma ≈1.35 and cap at ~235 before swirl |
| Dot-cloud covers land | No ocean mask | Mask with "bluish" pixels + weight by distance from archipelago |
| Hyderabad lights blown out | Linear tone | Exposure curve `1−exp(−k·x)` with blurred base |
| Sea-level diagram unreadable | Scale too small | Larger island, fewer palms, dashed reference line, arrow |
| Coral diagram muddy | Random palette | Smooth palette interpolation across noise field; polyp speckle |
| Two unrelated frames blended too long | Long dissolves | ≤1.2 s dissolves; use dip or cut instead |
| Photographer watermark in corner | Source | Crop (zoom ≥1.19, bias upward) |
| Stock beach looks like the wrong place | It *is* | Prefer real stills; slow; disclose |

### Audio
| Symptom | Cause | Fix |
|---|---|---|
| Music masks voice | Fixed level | Ducking envelope; trim low-mid; reduce level in dense speech |
| Harsh limiter pumping | Mastering too hot | Two-pass loudnorm at −16 LUFS with TP −1.5 |
| Silence feels dead | Bed dropped to zero | Keep a low bed except deliberate silence |
| Hits too frequent | Over-enthusiasm | Max 3–4 booms |

### Process
| Symptom | Cause | Fix |
|---|---|---|
| Download 429s | Bulk Commons requests | Honour Retry-After; slow; alternatives; front-load |
| Render crashed at hour 1 | Unhandled exception in one chunk | Per-chunk try/except; resumable parts |
| Memory grows | All shots alive | Lazy build and release |
| `read-only` array errors | Frame buffers from a pipe | Copy arrays before mutation |
| User cannot get a 737 MB file | Chat/Git limits | Plan delivery: smaller share version, LFS/hosting/split parts; confirm with the user |
| Shell timeouts | Long commands | Background + poll logs; avoid `sleep` chains |

---

## 9.3 The anti-sameness system

### What stays constant (craft)
- Voice-driven timing; motion on every shot; look-before-choose; honest sourcing; restrained text; layered sound; loudness standard; QA passes.

### What must change each film (identity)
| Layer | Change from the topic |
|---|---|
| Palette | From materials/light of the subject |
| Pace | From the subject's tempo (calm sea vs busy city) |
| Transitions | Different signature trio |
| Music | Tonic, mode, lead instrument, rhythm feel, motif |
| Titles | Typeface pairing, placement, language treatment |
| Diagrams | Invent visuals the *new* content needs |
| Opening/closing images | New, but echo each other |
| Sound beds | Different world (forest, city, desert) |

### Mechanics
1. Write the identity line (T2) before anything else.
2. Compare with the last film's identity line: change ≥3 dials if similar.
3. Prohibit copy-paste of act files; only reuse *engine* code and *patterns*.
4. Add **one signature idea** per film (like the "lakh lights" or a unique diagram) that appears twice (setup and callback).
5. In review (Pass C/D) ask: "Could this scene appear in the last film unchanged?" If yes → redesign.

---

## 9.4 If your tools are different

| Tool reality | Adjustment |
|---|---|
| No GPU, only CPU | Keep per-frame cost low; chunk and parallelise; use pre-computed noise/LUTs |
| Video editor (not code) | Implement diagrams as motion graphics (Figma/AE/Canva animation); same grading ideas; same audio buses |
| AI video generator available | Use for rung-4 mood shots only; consistent style prompt; label as generated |
| AI music generator | Use T9 as the prompt; edit to hit points; same ducking |
| Narrator is human | Provide a pronunciation sheet; record per act with room tone; get timestamps |
| Short-form/vertical output | Re-plan beats for 9:16 (centre-weighted compositions, bigger subtitles, faster pace); don't just crop |

---

## 9.5 The final five questions (ask before shipping)
1. Could I tell the film's promise from the first minute alone?
2. Does every picture explain or deepen its line?
3. If I mute the picture, does it still feel finished? If I mute the sound, does it still tell the story?
4. Is anything here dishonest, uncredited or unverifiable?
5. Would this film look and sound like *this* topic — and only this topic?
