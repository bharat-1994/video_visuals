# 03 — Picture

## 3.1 Principles
1. **Illustrate the idea, not the sentence.** The picture adds meaning the voice doesn't say.
2. **Draw what cannot be filmed.** Geology, history, numbers, scale, routes, systems — design these. This is what makes a documentary feel authored.
3. **Everything moves a little.** Stillness only when it is the point.
4. **One film, one look.** Different sources are unified by grade + finishing.
5. **Honesty.** Real, stock, generated and diagrammatic imagery must be distinguishable *to you* (and disclosed to the client).
6. **Restraint with text and effects.** Effects are seasoning.

## 3.2 The decision ladder (expanded)

For each beat, walk down; stop at the first rung that fully works.

1. **Draw the idea** — a map, a diagram, a size comparison, a count, a timeline, a cross-section, a flow.
   *Ask:* "If I had a whiteboard and an animator, what would I draw to make this line obvious?"
2. **Real footage of exactly this** (the actual place/event/object).
3. **Real photograph of exactly this**, animated with camera motion.
4. **Emotional-equivalent footage** (light on water, a person at work at dusk) — connective tissue, ≤25% of runtime, disclosed.
5. **Rewrite the beat** if nothing honest fits. Filler is worse than a shorter film.

### Mapping line type → picture type
| Line type | Picture |
|---|---|
| Count/quantity | counted animation on a map or grid |
| Comparison of size | overlay of familiar reference (city grid, football pitch) |
| Location/route/movement | map with animated path and pulsing markers |
| Process over time | animated cross-section or timeline |
| Cause → effect | before/after or A→B animation (sea rise; colour drain) |
| Abstract claim (language, inheritance, law) | minimal diagram with 3–4 icons |
| Emotion/mood | footage of light, water, faces (distant), hands at work |
| Legend/oral history | atmosphere only; never "evidence" |
| Danger | desaturated/cool, wide, storm imagery; sound does the rest |
| Hope/continuity | warm, slow, wider than before |

## 3.3 Camera & motion

### Camera motion rules
- **Stills:** slow push or push+drift. Scale 1.00 → 1.10–1.18 over the shot; pan ≤ 6% of frame width; add tiny handheld sway (≈0.3–0.6% amplitude) for photographs to avoid a "slide" look. Use easing (smoother-step) on larger moves.
- **Footage:** apply a small push (1.00 → 1.06–1.10) when the clip is static; none if the clip already moves.
- **Speed:** slowing a clip to 0.6–0.8× can turn busy stock into calm; avoid >1.25× speed-ups (looks sped up).
- **Direction logic:** keep movement direction consistent across a sequence (left→right = forward in time/space); reverse direction to signal return/contrast.
- **Handheld vs smooth:** choose per film. We used smooth + micro-sway on stills.

### Parallax (optional, advanced)
Cut a still into foreground/background layers and move them at different speeds. Skip if you can't mask well — a clean push-in beats a bad parallax.

## 3.4 Composition and safe areas (1080p)
- Keep key content inside the central 90%; subtitles occupy the bottom ~15% (baseline ≈ y 1010, up to 2 lines of ~74 px) — don't place key action there.
- Location tags sit top-left (x≈110, y≈96).
- Titles centred, slightly above the vertical midpoint.
- Leave **headroom** and **lead room** in motion (the subject moves into space).
- Horizons: top third or bottom third, rarely the exact middle.

## 3.5 Procedural scene catalogue (patterns you can build in any tool)

For each: **when to use**, **design**, **parameters**.

### A. The satellite dive (space → place)
- *When:* introducing a location; "far away/small" ideas.
- *Design:* stack of imagery at increasing resolution (world relief → region true colour → island 30 m). The camera interpolates in **log-zoom** with smooth easing; finer layers fade in as the view shrinks; overlays (markers, labels) are drawn in screen space from lat/lon projection.
- *Parameters:* total 11–17 s; eases: slow start, faster middle, soft landing; marker reveal staggered 0.05–0.15 s apart; labels hairline + small caps; match the colour of layers (low-frequency colour transfer from coarse to fine) to hide seams; feather masks where a fine tile has edges.
- *Why it works:* it gives a true sense of scale, with real data, at almost no cost.

### B. Count reveal ("36 islands", "a lakh")
- Dots appear one by one (stagger 0.03–0.1 s), with a soft glow; then **highlight a subset** (10 of 36) with a warmer colour and a pulse ring.
- For "a lakh" show a dust cloud of tiny points that then collapses/vanishes to the real number — visual surprise matches the verbal surprise.

### C. Size comparison grid
- Show a known area (a city's night lights) and overlay a square equal to the subject's area; clone squares until they fill the city (e.g., 20 squares).
- Keep the first square brighter (it *is* the subject); others dimmer.
- Timing: first square appears with the sentence start; clones accelerate (0.08–0.2 s apart).

### D. Area-of-influence bloom
- A circle (or polygon) grows from the subject over 2–3 s with soft fill + bright rim to show "the sea around it is vast" (EEZ-like).

### E. Cross-section animation (geology/biology/architecture)
- Flat 2D side view: sky above, water (gradient) below, solid ground shapes.
- Animate one variable at a time (rise → growth → sinking → ring). Each phase ~6–12 s.
- Add light rays, caustics, floating particles for life; a thin bright line along the key surface (waterline, crest).
- Use diagram colours with a hero (warm for living growth) vs cold for inert (rock).

### F. Routes/paths
- Dashed path draws progressively with a bright head; origin and destination pulse; labels appear after arrival.
- Two competing routes (race) use contrasting colours (warm vs cool) and the same duration so the viewer feels simultaneity.
- Camera slowly pushes toward the destination while the route draws.

### G. Time/before-after
- Same footage with a **grade change over the shot** (colour drains for bleaching; warm → cold for threat) rather than a cut.

### H. Storm/weather
- Use real satellite imagery; add a swirl warp around the eye (angular rotation falloff with radius) and a slow push; follow with real wave/lightning footage, with occasional brightness flashes.

### I. Network/connectivity map
- Lines grow from hub to nodes sequentially; light pulses travel along finished lines; nodes pulse.

### J. Minimal "concept diagram"
- 3 icons + 2 arrows on a dark gradient; each element appears in sequence (0.7 s stagger) with a glow. Colour-code (e.g., three generations = three hues).
- Use for abstract ideas (inheritance, supply chain, cause-effect).

### K. Split-screen slider
- Two shots divided by a bright vertical line that slides; use for "A vs B" ideas (development vs conservation), slight angle (5–7°) for energy.

### L. Year/number cards
- Large thin numerals (180–250 px), letter-spaced, dark background (subtle map texture), small caption below; fade 0.7 s, slow drift ≈ −30 px over the card. Only at **date turns** (3–4 per film).

### M. Flag/emblem
- A flag waving needs real cloth motion (sine displacement increasing from the pole, shading from slope). Raise it along a pole for "hoisting". A crisp pole + frayed edge sells it.

### N. Silhouette ships/characters
- For historical/legendary visuals where no honest archive exists: dark silhouettes at the horizon over real sea footage, scaled small, bobbing slowly; palette: near-black hull, muted sails with one accent (red cross). Never show them as "evidence".

### Design language for all overlays
- **Line weights:** 2–5 px at 1080p; **glow:** blurred copy added at 1.0–1.4× opacity.
- **Colour roles:** hero (cyan/teal) for the subject; warm gold for focus; red-ish for danger/rival; white for the head of a path.
- **Type:** letter-spaced capitals, small (22–36 px) for tags; avoid bold.
- **Timing:** ease in/out 0.35–0.8 s; stagger multiples; never everything at once.
- **Restraint:** one concept per overlay.

## 3.6 Using stills well
- Choose stills with a clear subject, space for motion, and no heavy watermark; crop/zoom to remove watermarks or text.
- **Upscale** small stills to ~2400 px wide with a good resampler plus mild unsharp mask before applying a push, otherwise they look soft.
- Keep ~15–20% safe margin so the push doesn't crop key content.
- For panoramas, a long slow pan reads as a shot.
- Vary orientation: portrait images → crop to a 16:9 window and pan vertically.

## 3.7 Using footage well
- **Conform** every clip to the project's frame rate (e.g., 24 fps) and size (scale to cover, centre crop) before editing; keep a cache of conformed clips.
- Trim to the *good* seconds (stock clips often have a weak start/end).
- Choose 1080p+ sources; downscale 4K for sharpness.
- Check for **logos, text, faces** that would harm context.
- If the footage is of a different place than the story: only use for *mood*, slow it slightly, and disclose.

## 3.8 Colour

### Palette derivation (from the topic, not taste)
1. List the *materials of the place* (water, sand, foliage, rock, sky).
2. Choose **hero** (dominant, 60%), **accent** (25%), **signal** (15%: danger/hope).
3. Check emotional fit (turquoise = calm clarity; amber = history; steel = threat).

Lakshadweep: hero turquoise/teal, accent warm sunset gold, signal storm grey-blue, history sepia.

### Grade as storytelling
| Look | Use |
|---|---|
| Teal/clean | present-day beauty, science |
| Warm | people, community, hope |
| Sepia/low saturation | history/legend |
| Cold/desaturated | threat, loss, bureaucracy |
| Bleach (very low sat, lifted blacks) | dead coral / loss |
| Dusk (blue shadows, warm highlights) | reverence, endings |

Implementation idea (tool-agnostic): *S-curve for contrast + shadow tint + highlight tint + saturation multiplier*. Example presets we used: teal (contrast 0.6, shadows toward blue-green, highlights warm, sat 1.12); warm (contrast 0.5, sat 1.10); cold (sat 0.92); storm (contrast 0.75, sat 0.70, gain 0.92); bleach (sat 0.45); sepia (sat 0.50, warm tints); dusk (blue shadows, warm highlights).

### Unifying heterogeneous sources
Apply a **common finishing pass** after per-shot grading:
- Highlight **bloom**: extract >62% luminance at 1/6 scale, blur (σ≈9), add at ≈0.16–0.25 strength.
- **Vignette**: 0.5–0.6 strength, starting ~35% from the centre.
- **Film grain**: monochrome noise σ≈3 on 8-bit, cycle 12 frames of pre-computed noise; subtle, not visible as noise.
This is what makes stock, stills, satellite and animation feel like one film.

## 3.9 Titles, tags, subtitles

### Title
- Appears over the cold-open (1–5 s), native script large + spaced Latin caption beneath. Soft glow; slight drift (−14 px/s).

### Location tags
- Hairline above + name in spaced capitals + coordinates/subtitle underneath. Appear at first visit of a place only; visible 4–6 s; fade 0.6 s.

### Subtitles (burned-in)
- Size ≥ 44–48 px at 1080p; white; soft shadow; **a smooth gradient** along the bottom third (not a box) to ensure legibility on bright footage.
- Max 2 lines; balanced wrapping (split at the word boundary minimising the longer line); max ≈ 1500 px line width.
- Fade in/out 0.16 s; windows never overlap.
- **Indic/complex scripts:** use a shaping engine (HarfBuzz via Raqm/libass) and a font with full coverage (e.g., Noto Sans Telugu). **For mixed-script lines, split into runs** (Latin vs native) and draw each with an appropriate font, advancing x by run width — otherwise Latin words become boxes or shaping breaks.
- Always supply `.srt` files (native + translation) for platforms.

### Credits
- End card: film name, minimal source line, "full credits in CREDITS.md". The full list goes in a file or description.

## 3.10 Subtle effects (dust, rays, caustics)
- **Floating particles** (dust/plankton): 60–160 soft dots, additive blend at 0.2–0.5, drift 5–15 px/s with slow sin wobble. Use warm dust for sun scenes, cool plankton underwater.
- **Light rays:** soft fan shapes from the top, 0.15–0.3 strength; very slow lateral shift.
- **Caustics:** crossing noise layers → bright net lines at 0.05–0.15 strength, only underwater.
- **Light leaks:** warm gradient sweeping from an edge over 1–2 s, once or twice per film.
- Rule: if you notice the effect, it's too much.

## 3.11 Checklist (picture)
- [ ] Each beat has a rung from the ladder; rungs 1–3 dominate.
- [ ] No unmoving shots; no clip reused without intent.
- [ ] Palette defined; grades mapped to emotions; common finishing pass applied.
- [ ] Overlays obey the design language.
- [ ] Subtitle test with the hardest line (mixed script, long) passes.
- [ ] Safe areas respected; no watermarks/logos visible.
- [ ] Disclosure list of real/stock/generated shots prepared.
