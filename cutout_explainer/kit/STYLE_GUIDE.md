# Style Guide — flat cut-out explainer animation

This guide describes a house style for animated explainer videos (YouTube "story of / why X" format).
You will not see the original reference video. Everything you need is here, in `reference/` (frames from it),
and in `engine/` (the style already encoded as code). **Look at every image in `reference/` before you start.**

The guide has two layers:

* **FIXED** — the identity of the style. Never change these; they are why every video is recognizable.
* **FREE** — what makes each video different. Vary these deliberately; do not copy the examples.

---

## 1. FIXED — the style's identity

### 1.1 Why it looks the way it does (understand this, then the rules follow)
The style is *cut-out puppet animation*: a small kit of reusable characters and props, swapped very fast in sync
with the narration. It feels "animated" mostly through **cuts, pop-ins and camera moves**, not through
frame-by-frame drawing. Consistency comes from reuse — never redraw a character from scratch.

### 1.2 Pacing (measured from the reference: 170 shots in 10.7 min)
| rule | value |
|---|---|
| shot length | median 3.4 s; range 1.5–6.5 s |
| narration per shot | ~8–12 words = one clause / one list item |
| a new visual idea | every shot; a new location every 20–25 s |
| dialogue mini-scene | about once per minute, 8–25 s each, ending on an ironic line |
| chapter title card | black screen, white handwritten typewriter text — only at chapter breaks |

### 1.3 Every line becomes a *literal* picture
Read the line and draw exactly what it says. "New York, London, Singapore" → those three landmarks.
"Golden handcuffs" → actual gold handcuffs on his wrists. "Sold it for $500" → an envelope with "$500" pops in.
Abstract claim → physical metaphor (trap, chain, cage, rope bridge, door, ladder, hourglass).

### 1.4 Characters (use `cast()`; never redefine looks)
* Big round head, dot eyes, short brow strokes, simple swap mouths; body = flat shirt shape; limbs = single
  black rubber-hose lines with dot hands. See `reference/cast.jpg`.
* **Expression = brows + eyes + mouth only.** Choose from: neutral happy sad angry worried shocked smug tired determined.
* Lip-flap (`talking=True`) **only** while that character's line is on screen.
* Real people: resemble them through hair shape/colour, jaw, brows, accessories — not detail.
* Poses: use `pose("name")` presets (see `reference/pose_presets.jpg`). Raw arm numbers are allowed only for
  touching a specific object, and hands must land ON that object.

### 1.5 Look
* Flat colours, 2–3 tones per material (base, shadow, highlight). Black outlines 2–4 px. No photo textures.
* Emotional beats: dark background + single spotlight. Story beats: simple real-world settings.
* Text: font "Caveat Brush" only. Keywords = white with dark outline, size 56–84, popped in, in empty space.
  Dialogue = white handwritten line + a short tick toward the speaker's head (`dialogue()`), never a bubble.
  Time markers ("1989 · Age 17") typewritered top-left. **Text never covers a face.**

### 1.6 Motion grammar
* Props/keywords enter with `popped()` (overshoot + smoke puff), timed to the word that names them.
* Camera: slow push-in on realizations, pull-out on summaries/reveals, gentle pan for travel. Shake only on impacts (<0.6 s).
* Hard cuts between shots. Things that vanish go out with a smoke puff.

### 1.7 Sound
Every on-screen event has a sound: pop on pop-ins, whoosh on fast moves/exits, typewriter ticks while text types,
diegetic sounds (typing, plane, cash register), a quiet ambience bed per location. Music bed is global (build.py adds it).

---

## 2. STAGING — physical common sense (most failures happen here)
1. **Screens, books, papers face the person using them.** If someone types, show them side-on (`facing` ≥ 0.6 toward
   the device) with the device seen from its side/back, OR over-the-shoulder (`view="back"`, screen facing camera beyond them).
2. Hands touch what they hold/type on/point at. Objects rest on surfaces; nothing floats unless it is flying.
3. Back view = we see the back of the head; arms are behind the body (the engine handles it — don't draw hands over a back).
4. Characters in dialogue face each other (|facing| ≈ 0.6).
5. Scale is believable: people fit through doors, a desk is waist-high, a plane in the sky is small but readable.
6. Keep the bottom 90 px free (subtitles) and keep faces clear of rain/props/text.

## 3. ASSETS — the quality bar
* A real place/object must be **recognizable to someone who knows it**: correct silhouette, proportions and its
  2–3 signature features (e.g. Memorial Church: central gable + mosaic band + round-arch arcades + red tiles + palms).
  Before drawing, write down those signature features, then check the render against them.
* If you can view photos, look at 1–2 real photos first and match proportions. If not, rely on the written brief.
* Build detail with loops (windows, arches, tiles, keys) and layered tones, not with one big box.
  Compare `reference/BAD_v1_generic_assets.jpg` (generic boxes — rejected) with `reference/GOOD_v2_example.jpg`.
* No official logos, seals or brand marks. Names as plain lettering.
* Put reusable drawing functions in an assets module so they can be reused in later videos.

---

## 4. FREE — vary these every video (do not copy the examples)
* Colour palette of backgrounds per location (keep it flat and harmonious).
* Choice of metaphors (never reuse the same metaphor twice in one video).
* Camera choices per shot, compositions (left/right placement, close-up vs wide), which shots are dialogue.
* Settings, props, supporting cast (build new ones with `Puppet(...)` params; keep the construction rules).
* Mix of shot types — aim for a spread: character close-up, two-shot dialogue, wide establishing, object-only,
  metaphor, number/keyword, over-the-shoulder.

---

## 5. Self-review loop (mandatory)
After writing shots: `python3 engine/sheet.py <module> review.jpg`, open the image, and check every frame against:

- [ ] Each landmark/prop recognizable? (name its signature features — are they visible?)
- [ ] Any screen/book facing the wrong way? Any hand not touching what it holds? Anything floating?
- [ ] Any crossed or broken limbs, hands drawn over a back?
- [ ] Any text over a face, cut off at an edge, or in the bottom 90 px?
- [ ] Does each shot show exactly what its line says?
- [ ] **Re-read the brief/spec for each shot and tick every stated requirement** (who faces whom, who sits where, who holds what, which hand). Polishing a frame is not the same as meeting the brief — this was the most common miss in testing.
- [ ] Does it look like `reference/original_frames_*.jpg` in spirit (flat, clean, bold, readable at a glance)?

Fix and re-check, up to 3 rounds. Then `python3 engine/build.py <module> out.mp4`.
