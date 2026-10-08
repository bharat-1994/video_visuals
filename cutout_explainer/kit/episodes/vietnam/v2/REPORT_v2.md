# Vietnam v2 — Qwen build report

## 1. What I built (✓)

**Engine**
- ✓ `engine/scene_v2.py` — copy of `engine/scene.py` plus every section-3 feature:
  sound-by-category `_autocues` (entrance table + `snd=`/`snd=none` overrides), `thin_cues`
  (0.35 s auto-spacing incl. explicit-sfx protection, 0.6 s same-sound rule, 3-per-shot cap keeping
  earliest+loudest, ambience dedupe vs explicit sfx, consecutive-shot ambience −3 dB), `remap_key_cue`,
  `cam whip` (280 px snap-in + whip sound), `cam track X0 X1` (constant-speed, zoom 1.06),
  `fx NAME [@word]` layers drawn after the world and before text, `bg NAME k=v` param passthrough,
  **`e2=EXPR@word` reactions** (UPDATE 2 §3.8), dlg lines shown only during their own 1.6 s window
  or a nested talk window, and two small plumbing additions the section-5–7 assets need:
  `"@word"` strings inside asset list kwargs are resolved to seconds (whiteboard `at=[...]`), and
  asset functions that declare `t0` receive the element's appear time (chalk_text reveal).
- ✓ `engine/build_v2.py` — copy of build.py + chapter music: reads `MUSIC`, plays each bed from its
  start, 1.5 s crossfades at each change, music at −10 dB, v1 ducking kept.

**Sound** (`audio/sfx_v2.py` → 42 new wavs + 5 beds; existing v1 wavs untouched; `INDEX.md` +47 rows)
- ✓ all 15 entrance sounds (§4.1), all 27 named effects + `riser` (§4.2), 8 seamless 4 s loops,
  all −3 dBFS peak, 44.1 kHz mono 16-bit, generator deterministic (md5-identical reruns).
- ✓ `audio/music/`: music_somber 80 s @72, music_hopeful 62.6 s @92, music_upbeat 69.8 s @110,
  music_tension 72 s @100, music_reflective 72 s @80 — all 60–90 s seamless loops, −12 dBFS.

**Cast** (§5, in `assets_v2.py`, `VPuppet`-style wrappers over `Puppet`)
- ✓ lan (low bun at the nape + optional work cap, light-blue uniform — same hair colour/face as the S08 kid),
  ✓ minh (short hair, glasses, white polo, blue lanyard + badge), ✓ bunny (white hood ring framing the
  visible eyes, mask, white gloves; no logo), ✓ us_official (navy suit, red tie, light-brown part, strong
  jaw — generic), ✓ cn_official (grey suit, black part, glasses — generic).
  Family check frame (kid | lan | minh side by side) passed.

**Backgrounds** (§6) — **all 21 P1 built; all 30 P2 also built — zero aliases used**
- ✓ P1: hanoi_1986, hanoi_today (motorbikes with t), market, meeting_room (`screen=`), assembly_hall
  (`uniform=`), samsung_hall (blue band + plain SAMSUNG lettering, no logo), white_studio, port_day,
  port_night, warehouse, construction (jibs swing with t), classroom, lab, cleanroom (yellow light),
  foxconn_campus, split2 (`left=`/`right=`), sunrise (sun rises with t), coop_yard, globe_space
  (twinkle with t), boxing_ring, newsroom, state_store (near-empty shelves).
- ✓ P2: office_1980s, ruins, engine_room, renovation, hanoi_street_1990, harvest_gold, harvest_poor,
  beijing_1978, embassy, government_hall, expo_hall, signing_table, trophy_stage, night_city, seoul_hq,
  drone_view, north_vn_hills, rice_to_factory, samsung_campus, factory_gate, garment_hall,
  small_workshop, design_studio, air_cargo, border, sea_lanes, race_track, casino_table, vault,
  vhs_rewind, kitchen_wall.

**Props** (§7) — ✓ all 22: city_card (7 landmarks, name-only lettering), rank_podium, shop_front
(`closed`), factory_modern, sewing_machine, wafer, microscope, laptop (`screen=code`), whiteboard
(`lines`/`at`), chalk_text (own mini-board, jitter, typewriter from `t0`), tv_screen, carton,
cargo_plane, road_sign, trophy, vault_door (`open_`), food_stall, empty_chairs, loudspeaker_pole,
compass, sneaker, solar_panel.

**Custom shots** (§8) — ✓ all 27: zone2, priceline_market, ration_queue, sacks_shrink, sacks_grow,
chart_crash, climb_line, climb_dot, supply_web (pulse), strings_in, trade_arcs, signing, dice_roll,
field_to_factory, campus_build, money_pour, phone_wall, carton_stream, gdp_cake, box_stack, gloves,
truck_queue, coins_grow, country_build, value_split, supplier_board, cartons_in.

**FX layers** (§9, UPDATE 2) — ✓ exactly the 11 allowed: motorbikes, rice_burst, storm, solder_sparks,
smoke_puffs, fireworks, confetti, camera_flashes, ticker, shift_crowd, sepia. No other motion layer
exists in the build (the decorative ones from the first brief were never shipped; `V2_FX` is now
ticker-only, as the director set it).

**Wiring** — ✓ `episodes/vietnam/v2/setup_v2.py` registers BG/ASSETS/CAST/CUSTOM/AMBIENCE/FX;
AMB mapped for every new bg per the §6 table.

**Full render** — ✓ `python3 engine/build_v2.py episodes.vietnam.v2.film_v2 vietnam_v2.mp4` produced
`vietnam_v2.mp4`: 1280×720@30, 608.8 s (10:09), h264+aac, max −1.1 dBFS, no render errors.

## 2. P2 items that became aliases
None — every P2 background was built. (`setup_v2.ALIAS` remains as a safety net; `ALIASED == []`.)

## 3. Per-shot FAIL list (PASS shots not listed)
- **S149** — after the 60 px nudges, the golden key's bow still grazes the right edge of Minh's cheek.
  The face (eyes, mouth, glasses) stays fully visible and the key now sits at hand height; the 60 px
  nudge budget cannot separate a 180 px-wide key from a head without moving the director's layout
  further. Left as-is and flagged for the director.
- **S70 / S78 / S105 / S140 / S141** — a person's head overlaps the meeting-room wall-screen text.
  Judged acceptable: the person stands *in front of* the screen (correct depth), and no caption text
  is over a face. No action.
- Everything else in §10 passes on the contact sheets, incl. the specific checks: S04 (10 people,
  cloud over the sad left 7), S07 (empty shelves, clerk legs behind counter), S17/S57 (podium ranks),
  S20/S94/S131/S147/S150 (Samsung = blue + band + plain word only), S21/S81/S82/S135 (landmark-only
  city cards), S103 (gloves on raised hands, generic officials), S111 (per-company colours, huge
  campus, no logos), S117 (yellow cleanroom + bunny + wafer), S125 (70% on Ba's side, 3% on Minh's),
  Lan identical in all 16 of her shots, and the sound check below.

## 4. Position nudges in film_v2_lines.py (all ≤ 60 px; nothing else changed)
1. **S20** `tx SAMSUNG` y 520 → 566 (collided with the pie's "50%" label).
2. **S28** `tx "HANOI · DEC 1986"` x 60 → 120 (pan camera clipped it off-frame at the end of the pan).
3. **S124** `p kid` x 1050 → 990 and `a globe` (1080,330) → (1140,270) (globe popped directly on the kid's head).
4. **S141** `kw "NOT JUST CHEAP LABOR"` y 640 → 580 (was inside the bottom-90 px subtitle band).
5. **S149** `p minh` x 1000 → 940 and `a golden_key` (1000,420) → (1060,480) (key covered Minh's face).

## 5. Audit + sound counts

`python3 episodes/vietnam/v2/audit.py` → **exit 0, all PASS**:

```
PASS bg 'dark' shots <= 10 (reserved for the cage/map motif): 7
PASS bg 'flat' shots <= 6: 0
PASS no single bg in > 12 shots: ('meeting_room', 10)
PASS map-family shots <= 14 (incl. cage motif): 13
PASS container_ship <= 5: 5
PASS generic factory <= 4: 0
PASS shots with a person >= 55%: 91/151
PASS no shot has > 2.5 s of speech without a new narration-tied beat: []
PASS no 3 same-bg shots in a row (kitchen run exempt): []
```

Sound counter (`Counter(c[2] for c in F.CUES)`), total **504** cues:

```
click_soft 69 (13.7%)   soft_whoosh_in 56 (11.1%)   thump_soft 47 (9.3%)
office_hum 40   paper_slide 36   card_flip 31   wind_ambience 22
crowd_murmur 14   low_boom 14   factory_line 14   riser_short 13   metal_tink 11
pop_soft 10 (2.0%)
```

`pop_soft` 2.0% ≤ 10% ✓; no entrance sound above 18% ✓ (max is click_soft at 13.7%).

Interpretation notes (chose the reading most literal to the brief, per §12):
- Typewriter ticks are capped at **2** per `tx` element (spec allows "at most 3"): with ~45 tx/card
  elements, 3 ticks each pushed click_soft to 20% and broke the "no entrance sound above 18%" rule;
  2 keeps every sound under the cap. Ticks are also exempt from `thin_cues` spacing (they are typing
  texture, counted separately in the §1 diagnosis, like v1's typewriter ticks).
- `kw` whoosh/card_flip alternation runs **globally** across the film (per-shot alternation degenerated
  to ~95% whoosh since most shots have one keyword).
- `caged_map` counts as metal (it is the cage motif) → metal_tink.
- Ambience is dropped when the director's line also plays the same sound explicitly at t≈0
  (e.g. S16 street_traffic), so beds never double up.
- v1 is untouched: `git diff` shows zero changes to any v1 file; `episodes.vietnam.film` still renders.

## 6. Token usage
The harness does not expose an exact counter for this session; from the session log (215 assistant
steps, content sizes ÷ 4): **input ≈ 990 M cumulative tokens (≈ 98.5% cached), output ≈ 93 K**.
Wall time ≈ 2 h 15 m; 5 subagents (audio, backgrounds, props, fx, custom) built in parallel.
