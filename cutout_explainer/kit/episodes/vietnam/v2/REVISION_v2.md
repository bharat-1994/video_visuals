# Vietnam film: revision v2 (director's brief for Qwen)

> **UPDATE 2 (supersedes anything below that conflicts): no decorative motion.**
> Motion is only allowed when the narration names it or the real place has it (motorbikes on a Hanoi street, sparks on "soldering").
> Never add birds, dust, sparkles, steam, light rays and the like just so something moves.
> Slow stretches are fixed with **beats**: something the narration names appears on its word, or a person **reacts** on a word (`e2=expr@word`, `pose2=pose@word`).
> The director has already added these beats (`V2_ADD`, `V2_SUB` in `film_v2_lines.py`). The audit now checks the beat gap instead of motion.
> If you already built fx layers: keep only the ones listed in section 9 and delete the rest.

v1 works, but a normal viewer gets bored: the same pop sound, the same dark spotlight, the same map, the same ship, the same factory, and very few people.
v2 fixes this. **The director has already written every shot change** (`film_v2_lines.py`) and the assembly (`film_v2.py`).
Your job is to build the new engine features, sounds, backgrounds, assets and cast that those lines use, render, check, and report.

---

## 0. Ground rules (read first)
1. Clone `github.com/bharat-1994/video_visuals`, branch `main`, then **create your own branch `qwen-v2`**. Never push to `main`.
   Work from `cutout_explainer/kit/`. Setup: `pip install pycairo numpy` and `mkdir -p ~/.fonts && cp fonts/* ~/.fonts && fc-cache -f`.
2. **Do not edit any v1 file.** v1 must still render exactly as before. You only create these new files:
   | new file | what |
   |---|---|
   | `engine/scene_v2.py` | copy of `engine/scene.py` + the features in section 3 |
   | `engine/build_v2.py` | copy of `engine/build.py` + chapter music (section 4.3) |
   | `audio/sfx_v2.py` + the new wavs in `audio/sfx/` + `audio/music/*.wav` | sounds (section 4) |
   | `episodes/vietnam/v2/assets_v2.py` | backgrounds, props and cast (sections 5–7) |
   | `episodes/vietnam/v2/fx_v2.py` | custom shot functions and fx layers (sections 8–9) |
   | `episodes/vietnam/v2/setup_v2.py` | registers everything into `scene_v2` registries (BG, ASSETS, CAST, CUSTOM, AMBIENCE, FX) |
   | `episodes/vietnam/v2/REPORT_v2.md` | your report (section 11) |

Already provided by the director (do not edit): `film_v2_lines.py`, `film_v2.py`, `audit.py`, `beats.py`.
3. Don't change `film_v2_lines.py`, except to nudge a position by up to 60 px when a render shows overlap. List every nudge in your report.
4. Read only: this file, `engine/API.md`, `engine/scene.py` (its docstring and the `_autocues` / `_draw` parts), `episodes/vietnam/film_setup.py` (it shows how registries and custom functions are written) and the **signatures** in `episodes/vietnam/assets*.py`.
   Look once at `reference/GOOD_v2_example.jpg`. Skip everything else.
5. House drawing rules still apply: flat colours with 2–3 tones per material, INK outlines 2–3 px, detail built with loops, no gradients, no photo textures, nothing important in the bottom 90 px, text never over a face.
6. **Logos:** never draw a real company logo, emblem, flag or seal. Companies are recognised by **brand colour + plain name lettering + their real kind of place** (section 6). This is a hard rule.

## 1. Diagnosis (measured with `python3 episodes/vietnam/v2/audit.py v1`)
| problem | v1 | v2 target |
|---|---|---|
| sound: `pop` | 263 of ~540 cues (49%), plus 154 typewriter ticks | pop ≤ 10% of cues, never 2 pops within 0.6 s, a different sound per kind of thing |
| dark spotlight background | 43 of 151 shots | ≤ 10, reserved for the cage/map motif |
| flat single-colour background | 42 shots | 0 |
| map family (VN map, Asia map, pins, cage) | 33 shots | ≤ 14 |
| container ship | 7 | ≤ 5 |
| generic "factory" box with a label (stood in for Foxconn, Intel, Samsung...) | 17 | 0; every company gets its real kind of place |
| shots with a person | 44 (29%) | ≥ 55% (v2 lines: 91 of 151) |
| shots with continuous motion | 10 | ≥ 35% |
| one 40 s music loop for 10 min | 1 bed | 5 chapter beds |
| shots with > 2.5 s of speech and nothing new on screen | 41 | 0. Fixed with narration-tied beats and person reactions, never decorative motion |

The v2 lines already pass the audit: `python3 episodes/vietnam/v2/audit.py` → all PASS. Your build must keep it passing.

**Story device added:** one family carries the film. **Ba** (the 1986 farmer = existing `farmer`), his daughter **Lan** (the kid in S08, later a factory worker) and her son **Minh** (an engineer in 2024).
Viewers follow people, not charts.

## 2. What "done" looks like
- `python3 engine/build_v2.py episodes.vietnam.v2.film_v2 vietnam_v2.mp4` renders the full 10:09 film with no errors.
- Audit PASS. The section 3 sound rules hold (`thin_cues` enforces them).
- Every new background or asset is recognizable by its listed signature features (sections 5–7), checked on contact sheets.
- Every shot's CHECKS in section 10 pass.

## 3. Engine v2 (`engine/scene_v2.py` = copy of scene.py, plus these)
1. **Sound by category (replaces "pop for everything" in `_autocues`).** Each element's entrance sound comes from this table. A per-element `snd=NAME` overrides it, and `snd=none` silences it.
   | element / asset | entrance sound (dB) |
   |---|---|
   | `kw` keyword | alternate `soft_whoosh_in` (−11) and `card_flip` (−12) |
   | `st` sticky, `paper`, `land_deed`, `ration_coupon`, `fta_scroll`, `whiteboard` lines, `chalk_text` | `paper_slide` (−10); `chalk_text` uses `chalk` |
   | `tx` typewriter | at most 3 `click_soft` ticks (−16), 0.09 s apart |
   | `cnt` counter | `riser_short` at start (−14), `ding_soft` at the end (−8) |
   | money_bag, coin, money items | `coins` (−12) |
   | metal: cage, padlock, container, port_crane, chip, wafer, tariff_wall | `metal_tink` (−12) |
   | wood: price_board, podium, open_doors, shop_front, empty_chairs | `wood_knock` (−10) |
   | glass/tech: smartphone, tablet, smartwatch, earbuds_case, laptop, tv_screen | `glass_tink` (−12) |
   | people popping in | `soft_whoosh_in` (−14) |
   | food: dish, rice_bowl, rice_sack, pork, rice_heap | `pop_soft` (−14), the only pop left |
   | `arrow` | `swish_draw` (−12) |
   | `bars`, `fn` pie/charts | `riser_short` (−14) |
   | anything else | `thump_soft` (−12) |
   | `shake` | `low_boom` (−6) instead of thud |
   | `out@` exit | `soft_whoosh_out` (−14) |
2. **`thin_cues(CUES)`** (global, after assembly):
   - drop any auto entrance cue that falls within 0.35 s of another auto entrance cue in the same shot (explicit `sfx` items are kept);
   - never let the same entrance sound play twice within 0.6 s;
   - cap at 3 entrance sounds per shot. Keep the earliest and the loudest.
3. **`remap_key_cue(name)`**: maps the cue names of the director's key shots (S01, S12, S14, S15): `pop`→`thump_soft`, `typewriter_tick`→`click_soft`; everything else is unchanged.
4. **Ambience per background:** `AMBIENCE[bg] = (sound, dB)` is added at t=0 of each shot (v1 already does this). Map every new background in section 6 to its ambience. If two consecutive shots share an ambience, the second one starts at −3 dB lower (no restart click).
5. **Camera:** add `cam whip` (starts 280 px off to the left and snaps in within 0.25 s with ease_out, plus a `whip` sound) and `cam track X0 X1` (constant-speed horizontal track, zoom 1.06).
6. **`fx NAME [@word]`:** a continuous motion layer, drawn after the world and before text, looking up `FX[NAME](ctx, t, dur, T, **kv)`. Starts at `@word` if given. Section 9 lists them.
7. **Background params:** `bg NAME k=v` passes its kv to the background function untouched (e.g. `bg meeting_room screen="WHY VIETNAM?"`, `bg split2 left=#hex right=#hex`, `bg assembly_hall uniform=#hex`).
8. **Reactions:** `p ... e2=EXPR@word` switches the expression at that word (the reaction beat). `pose2=POSE@word` already exists. Both are beats.
9. **Merged lines:** `film_v2.py` builds the final lines with `merged()` from `film_v2_lines.py` (V2 → V2_ADD → V2_SUB → V2_FX). Never apply these by hand.
10. **People:** `talk=@w1~@w2` already exists. Make sure `dlg` lines (S46, S48, S70, S71, S86) show **only while** the speaker's `talk` window or the line's own window runs. Default line window: from `@word` for 1.6 s.

## 4. Sound v2 (`audio/sfx_v2.py`, numpy synthesis like `audio/sfx.py`; 44.1 kHz mono 16-bit; peak −3 dBFS)
### 4.1 Entrance set (short, soft; these replace the pop)
| name | dur | recipe |
|---|---|---|
| soft_whoosh_in | 0.30 | band-passed noise (600–3000 Hz), swell up then fast fall, light low-pass |
| soft_whoosh_out | 0.30 | the reverse envelope of soft_whoosh_in |
| swish_draw | 0.45 | noise through a sweeping band-pass, 800→2400 Hz |
| card_flip | 0.18 | two quick filtered-noise flaps 50 ms apart |
| paper_slide | 0.40 | pink noise, high-passed at 1 kHz, envelope rising then falling, with tiny crackle grains |
| wood_knock | 0.20 | 220 Hz + 520 Hz decaying sines with a noise click |
| metal_tink | 0.40 | inharmonic partials (1.2, 2.9, 4.1 kHz), fast decay |
| glass_tink | 0.35 | sine pair (2.6 + 3.9 kHz), soft attack, short ring |
| thump_soft | 0.25 | 90 Hz sine falling to 60 Hz, decaying |
| pop_soft | 0.12 | the old pop, an octave lower and −6 dB |
| click_soft | 0.04 | 3 kHz click through a low-pass |
| ding_soft | 0.60 | bell (880 Hz + harmonics), soft |
| riser_short | 0.70 | filtered noise plus a sine sweeping up 200→900 Hz |
| low_boom | 0.90 | 45 Hz sine thump plus a sub-noise tail |
| whip | 0.20 | fast noise sweep, high to low |
### 4.2 Named effects used by the v2 lines
bicycle_bell (0.4, two bell strikes) · boxing_bell (1.0, three fast metallic rings) · camera_shutter (0.15, click plus a mechanical clack) · chain_rattle (0.6, random metallic pings) · chalk (0.6, scratchy band-passed noise strokes) · cleanroom_hum (4 s loop, airflow noise plus 60 Hz) · construction (4 s loop, distant hammering and a beeping reverse alarm) · crowd_cheer (2.0) · crowd_murmur (4 s loop, layered formant-filtered noise babble) · dice (0.8, rattle then 2 clacks) · door_creak (0.7, slow pitch-wobbling saw through a band-pass) · engine_sputter (1.2, irregular low pops slowing down) · factory_line (4 s loop, rhythmic clunks every 0.5 s plus a motor hum) · harbor (4 s loop, gull chirps plus water wash) · heartbeat (0.8, lub-dub) · jet_idle (4 s loop, a whine plus rumble) · marker_squeak (0.4) · news_sting (1.2, three rising synth stabs) · rewind_tape (1.0, a fast pitched-up warble) · sewing (4 s loop, a fast needle tick at 12 Hz plus a motor) · shutter_open / shutter_slam (0.6, a metal roller-shutter rattle going up or down) · street_traffic (4 s loop, motorbike buzzes passing plus horns) · thunder (1.5) · vault_lock (0.8, heavy clunk plus a bolt slide) · wood_crash (0.9).
Loops (4 s) must crossfade seamlessly. Add every new sound to `audio/sfx/INDEX.md` as one row: name, duration, description.
### 4.3 Chapter music (`audio/music/`, 60–90 s seamless loops, peak −12 dBFS)
| file | mood | how |
|---|---|---|
| music_somber | 1986 hardship | slow 72 BPM, minor key, soft plucked pentatonic notes plus a low pad |
| music_hopeful | Doi Moi reforms | 92 BPM, major key, kalimba arpeggio plus light shaker |
| music_upbeat | FDI and the Samsung boom | 110 BPM, bright marimba plus bass plus claps (can derive from the v1 bed) |
| music_tension | trade war | 100 BPM, staccato low strings (saw through a low-pass), ticking hi-hat |
| music_reflective | the trap and the ending | 80 BPM, piano-like sine with a soft delay, ends on a resolved chord |
`build_v2.py` reads `MUSIC = [(start_s, name), ...]` from the module, plays each bed from its start, crossfades 1.5 s at each change, and keeps the v1 ducking under narration. Music level −10 dB (v1 used −8).

## 5. Cast v2 (add to `CAST`; build with `Puppet(...)` + `VPuppet`-style hats, as in `assets.py`)
| id | look | notes |
|---|---|---|
| lan | adult woman, black hair in a low bun (wavy + a bun circle), light-blue factory uniform with a collar, small cap optional | the kid of S08 grown up; must read as the same family (same hair colour, similar face) |
| minh | young man, short neat hair, glasses, white polo, blue lanyard with a badge | Lan's son, engineer |
| bunny | cleanroom worker: white hooded suit covering the hair, white mask over the mouth (eyes visible), white gloves (hands as white dots) | used for Intel/semiconductors; no logo on the suit |
| us_official | generic American politician: navy suit, red tie, light-brown side-part hair, strong jaw. **Not** a caricature of any real person | trade war |
| cn_official | generic Chinese official: dark grey suit, black side-part hair, glasses. **Not** a caricature of any real person | trade war, 1978 |
Check: put lan, minh and the S08 kid side by side on one frame. They must look related.

## 6. Backgrounds (`assets_v2.py`; full-frame, `def bg_x(ctx, t=0.0, **kv)`; ground line y≈560–640 unless stated)
**P1 = must build. P2 = build if your budget allows, otherwise register the alias** (set `BG[name] = BG[alias]` and note it in the report).
| name | P | signature features | ambience | alias if skipped |
|---|---|---|---|---|
| hanoi_1986 | P1 | low tube houses (narrow, 3 storeys, faded yellow/ochre), roll-down shutters, tangled overhead wires, bicycles parked, a few plain cloth banners **without** emblems, leafy trees, muted palette | crowd_murmur −24 | — |
| hanoi_today | P1 | same street grammar, but bright: shophouses with colourful generic signs ("PHO", "CAFE", "MOBILE"), glass towers behind, a stream of motorbikes (animated with t) | street_traffic −22 | — |
| market | P1 | open-air market: striped umbrellas, baskets of produce, rice sacks, hanging bananas, stall tables | crowd_murmur −22 | — |
| meeting_room | P1 | boardroom: long table front edge at y=600, a wall screen showing the `screen=` text in big plain letters, window with a city view, potted plant | office_hum −26 | — |
| assembly_hall | P1 | long factory hall in one-point perspective: rows of workstations, ceiling lights, floor lane lines, small workers far back in `uniform=` colour | factory_line −20 | — |
| samsung_hall | P1 | assembly_hall with uniform `#2f6db5`, white/blue palette and a plain blue wall band with the word "SAMSUNG" in plain letters (`#1428a0`). No logo shape. | factory_line −20 | assembly_hall |
| white_studio | P1 | seamless white cyclorama, soft grey floor shadow, one soft light glow (an Apple-style product shot, without any Apple mark) | none | — |
| port_day / port_night | P1 | quay edge, stacked containers in 4 colours, 2 gantry cranes, water; night = navy sky, crane lights, reflections | harbor −22 | — |
| warehouse | P1 | tall shelving with cartons (loops), a yellow forklift, floor markings | factory_line −26 | — |
| construction | P1 | site fence, steel frame rising, 2 tower cranes (jib swinging slightly with t), dust | construction −20 | — |
| classroom | P1 | green chalkboard, rows of wooden desks, window, a globe on the shelf | none | — |
| lab | P1 | R&D lab: white benches, monitors with waveforms (screens face their benches, side view), a microscope, cable trays | office_hum −26 | — |
| cleanroom | P1 | semiconductor fab: **yellow-tinted lighting**, white walls, wafer racks, overhead rails, a tool with an orange status light. Instantly reads "chip factory" | cleanroom_hum −20 | — |
| foxconn_campus | P1 | huge campus seen from above at 3/4: identical long blue-grey blocks, dormitory towers, shuttle buses, gate with a plain sign; a crowd of tiny workers in shift colours (animated) | crowd_murmur −24 | — |
| split2 | P1 | vertical split: left half `left=` colour, right half `right=` colour, a white jagged divider, subtle paper texture lines (flat) | none | — |
| sunrise | P1 | layered hills, a rising sun (rises with t), warm sky bands, birds | wind_ambience −24 | — |
| coop_yard | P1 | dusty collective yard: a work-points board, a loudspeaker on a pole, stacked tools, a hay pile | wind_ambience −22 | — |
| globe_space | P1 | deep blue starfield with soft constellation dots (twinkle with t); used behind globe and Asia-map shots | none | — |
| boxing_ring | P1 | ropes (3), corner posts, spotlights, crowd silhouettes with tiny flash dots | crowd_murmur −20 | — |
| newsroom | P1 | TV studio: desk, blue backdrop with a generic world-map pattern, ticker band at the bottom (above y=630) | office_hum −26 | — |
| state_store | P1 | 1986 state store interior: **mostly empty shelves** (scarcity), a few tins, a counter, a ration poster written in plain text | office_hum −26 | — |
| office_1980s | P2 | grey filing cabinets, a rotary phone, a desk lamp, a beige wall calendar | office_hum −26 | office |
| ruins | P2 | silhouetted broken walls, smoke columns, dim orange sky (no gore) | wind_ambience −20 | dark |
| engine_room | P2 | pipes, valves, a big boiler, dim light | factory_line −22 | factory |
| renovation | P2 | scaffolding on an old house, fresh paint buckets, ladders | construction −24 | construction |
| hanoi_street_1990 | P2 | hanoi_1986 brighter, with a few shops reopening | street_traffic −26 | hanoi_1986 |
| harvest_gold / harvest_poor | P2 | golden ripe field with sheaves / sparse brown field | wind_ambience −22 | paddy |
| beijing_1978 | P2 | wide avenue, bicycles, grey Soviet-style blocks (no Tiananmen gate, no emblems) | street_traffic −26 | hanoi_1986 |
| embassy / government_hall / expo_hall / signing_table / trophy_stage | P2 | formal hall variants: columns + curtains / booths with flags-free banners / a long table with pens / a stage with confetti cannons | office_hum −26 | meeting_room |
| night_city / seoul_hq / drone_view / north_vn_hills / rice_to_factory / samsung_campus / factory_gate / garment_hall / small_workshop / design_studio / air_cargo / border / sea_lanes / race_track / casino_table / vault / vhs_rewind / kitchen_wall | P2 | as named (night skyline / a glass HQ tower with the plain word SAMSUNG / top-down roads and fields / green hills with mist / half rice field, half factory site / a campus with blue roofs / a factory gate with a crowd / sewing rows / a garage workshop / a desk with drawing tablets / a cargo jet nose open / a border gate with a truck queue / open sea with dotted lanes / a speedway / a green felt table / a steel vault room / VHS static stripes) | as fits | city, sky, hills→paddy, city, foxconn_campus, foxconn_campus, assembly_hall, room, office, port_day, sky, port_day, sky, room, dark, dark, kitchen |

## 7. Props / assets (`assets_v2.py`; `def name(ctx, x, y, s=1.0, **kv)`, docstring = anchor + size + features)
| name | anchor, size at s=1 | signature features |
|---|---|---|
| city_card | centre, 300×200 card | a framed postcard of a city by its **landmark silhouette**, `city=` newyork (skyline + Empire State spire), tokyo (Tokyo Tower, red/white lattice), seoul (N Seoul Tower on a hill), taipei (Taipei 101 stacked pagoda segments), cupertino (ring-shaped building among trees), paris (Eiffel tower), singapore (Marina Bay Sands: 3 towers + a boat on top). Plain city name under it. **No logos.** |
| rank_podium | bottom-centre, 3 blocks ~420 wide | gold/silver/bronze blocks with heights 1st > 2nd > 3rd; `labels`, `ranks`, `hl` index highlighted with a glow |
| shop_front | bottom-centre, 300×300 | a tube-house shopfront with a roll-down shutter; `closed` 0..1 shutter position; `label` shop sign |
| factory_modern | bottom-centre, 520×260 | a modern flat-roof plant: glass band, solar panels on the roof, loading bays; plain `label`. Replaces the generic factory |
| sewing_machine | bottom-centre, 200×140 | a classic industrial sewing machine with fabric under the needle |
| wafer | centre, r=110 | silicon wafer: a disc with a flat edge, a grid of dies, a rainbow sheen done as 3 flat bands |
| microscope | bottom-centre | stand, two eyepieces, a stage, a light |
| laptop | bottom-centre | open laptop, side 3/4 view; `screen=code` shows coloured code lines |
| whiteboard | centre, 420×320 | an aluminium frame on a stand; `lines` list revealed one per `at` word, in marker-handwriting style |
| chalk_text | centre | white chalk handwriting with slight jitter, revealed like a typewriter |
| tv_screen | centre, 520×320 | a TV set with a red "BREAKING" band and the `headline` in plain text; generic channel name "WORLD NEWS" |
| carton | bottom-centre, 180×140 | a cardboard box with tape and a stamped `label` |
| cargo_plane | centre, 700 wide | a wide-body cargo jet with the nose door open and cartons on the loader; plain livery |
| road_sign | bottom-centre | green highway sign on posts, white `text` |
| trophy | centre | a gold cup with handles on a black base |
| vault_door | centre, r=200 | a round steel vault door with spokes and a wheel handle; `open_` 0..1 |
| food_stall | bottom-centre | a small cart with an umbrella, pots, a menu flag |
| empty_chairs | bottom-centre | 3 empty chairs with jackets draped (no-shows), and "Zzz" |
| loudspeaker_pole | bottom-centre | wooden pole with 2 horn speakers and wires |
| compass | centre | a nautical compass rose |
| sneaker | centre | a side-view trainer, 2 tones, laces |
| solar_panel | bottom-centre | a tilted panel grid on a stand, with a sun glint |

## 8. Custom shot functions (`fx_v2.py` → `CUSTOM[name](ctx, t, dur, T, **kv)`; `T('@word')` → seconds)
| name | shot(s) | behaviour |
|---|---|---|
| zone2 | S04 | v1 `zone`, but the 10 people stand in the hanoi_1986 street (no beige box). The dark zone becomes a grey **rain cloud** drifting over the left 7, with rain lines; the counter goes 0→70% on "70" |
| priceline_market | S09 | v1 price line, drawn over the market background on a chalk price board (dark green panel) so the line reads as a price chart in the market |
| ration_queue | S35 | a long queue of 8 people (mixed cast, sad) in front of a closed state-store window; the queue shuffles forward 20 px every second |
| sacks_shrink / sacks_grow | S38 / S56 | a pyramid of rice sacks: shrink removes sacks top-down with a puff (after `at`); grow adds sacks bottom-up from `at` until 15 |
| chart_crash | S30 | a line chart on the meeting-room screen falls off a cliff at `at`, the screen flickers red twice |
| climb_line | S26 | a mountain-path line drawn from bottom-left to top-right with a flag planted at the top on `at` |
| climb_dot | S141 | a gold dot travels up the smile curve from ASSEMBLY to R&D, leaving a trail |
| supply_web | S23, S122 | a glowing network: 8 city nodes around a hub labelled `hub`; links light up one by one from `at`; `pulse=True` makes the hub beat like a heart |
| strings_in | S64 | 6 coloured strings from off-screen tie onto the globe one by one (global integration) |
| trade_arcs | S81, S82 | dashed curved arcs from (x,y) to each target, drawn on each target's word, with a small container moving along the arc |
| signing | S80 | 3 documents on a table; a pen signs each one in turn (squiggle draws in), with a stamp after each |
| dice_roll | S83 | two big dice tumble across the felt and land on 6-6 at `at` + 0.6 |
| field_to_factory | S89 | the left half is a rice field; from `at` a factory_modern rises out of the ground on the right half, with a dust puff |
| campus_build | S91, S113 | from `at`, 4 factory_modern blocks rise one after another (0.5 s apart) behind the fence, with cranes |
| money_pour | S93 | banknotes pour from the top into the construction site; a stack grows |
| phone_wall | S95 | a wall of 10×5 phones; from `at`, the left half lights up gold column by column (50%) |
| carton_stream | S97 | cartons slide along a conveyor into the plane's nose from `at` |
| gdp_cake | S98 | a round cake with a 15% slice lifted out and labelled (keeps the "slice of GDP" idea fresh vs the v1 pies) |
| box_stack | S19, S120 | cartons stack into a growing pile, n boxes; `hl` boxes in gold |
| gloves | S103 | draw red boxing gloves on both puppets' hand positions (use the info dicts; the hands stay attached) |
| truck_queue | S74, S130 | a line of trucks rolling right through a border gate / along a road; the gate barrier lifts |
| coins_grow | S126 | a coin stack grows 1→50 coins quickly from `at`, with a "50x" tag |
| country_build | S127 | top-down: a highway draws across, then a port icon, then an industrial-zone grid appears, each on its word (highways / ports / zones) |
| value_split | S131 | a big gold coin labelled VALUE splits: a small slice rolls to Lan, the large part rolls to the exec |
| supplier_board | S137 | a board of 20 supplier badges: 19 grey badges marked KR / CN / TW and 1 gold badge marked VN (plain text, no flags); the VN badge is highlighted on `at` |
| cartons_in | S138 | cartons labelled CHINA / KOREA / TAIWAN slide in from 3 sides on their words to a central table |

## 9. fx layers (`fx_v2.py` → `FX[name]`): ONLY these, each justified by the narration or the place
| fx | shot | why it is allowed |
|---|---|---|
| motorbikes | S16, S90, S142 | Hanoi streets really are full of motorbikes |
| rice_burst | S56 | the narration says "exploded" |
| storm | S106 | "no longer safe" (metaphor shown literally) |
| solder_sparks | S132 | the narration says "soldering" |
| smoke_puffs | S41 | engine "out of fuel" sputters |
| fireworks | S123 | "celebrated worldwide" |
| confetti | S110 | "the biggest winner" |
| camera_flashes | S66 | the 1995 normalization photo-op |
| ticker | S104 | a news studio really has a ticker |
| shift_crowd | S111 | a Foxconn campus at shift change |
| sepia | S145 | the narration flashes back to the 20th century |
**Rule 13: never add any other motion layer.** If a shot feels static, add a beat tied to a word (rule in UPDATE 2), not decoration.
Each fx must be cheap (≤ 40 shapes per frame) and must never cover faces or text.

## 10. Shot CHECKS (in addition to the house checks)
- **All shots:** the background is the one named (or its listed alias); every pop-in happens on its word (±0.1 s); no text in the bottom 90 px; no text over a face; hands touch what they hold.
- **S04:** exactly 10 people, the cloud covers the left 7, and those 7 are sad.
- **S07:** the shelves behind the counter are visibly almost empty; the clerk's legs are hidden by the counter.
- **S17 / S57:** podium ranks are correct (S17: China 1st, Vietnam 2nd; S57: Vietnam 3rd).
- **S20, S94, S131, S147, S150:** Samsung is shown only by blue uniforms, the blue band and the plain word SAMSUNG. No logo shape.
- **S21, S81, S82, S135:** each city card is recognizable by its landmark alone (cover the name: could a viewer guess it?).
- **S103:** the gloves stay on the hands while the arms are raised; the two officials are generic (not real people).
- **S111:** each company name is in its own colour; the campus reads "huge"; no logos.
- **S117:** the cleanroom has yellow light and a bunny-suit worker holding a wafer; reads as a chip fab.
- **S125:** 70% is shown on Ba's side (1986), 3% on Minh's side (today).
- **Family continuity:** Lan is the same person in all 16 of her shots.
- **Sound:** run `python3 -c "import sys;sys.path[:0]=['engine','.'];from episodes.vietnam.v2 import film_v2 as F;import collections;print(collections.Counter(c[2] for c in F.CUES).most_common(12))"`. `pop_soft` must be ≤ 10% of cues, and no entrance sound may be above 18%.

## 11. Review loop, budget, report
1. Build in this order: sounds → cast → P1 backgrounds → assets → fx/custom → P2 (or aliases).
   After each group, render **one** test frame per item (`engine/check.py`) and look at it once.
2. Then contact sheets of the film in 4 chunks:
   `SHOTS=<ids> python3 engine/sheet.py episodes.vietnam.v2.film_v2 sheet_N.jpg`, using ids 1–40, 41–80, 81–120, 121–151 from `segs`.
   **Max 2 rounds per chunk.** Fix, re-check.
3. Run the audit (must PASS) and the sound count. Build the full film with `build_v2.py`.
4. Write `episodes/vietnam/v2/REPORT_v2.md`:
   - what you built (✓ list);
   - which P2 items became aliases;
   - per-shot FAIL list with reasons (PASS shots are not listed);
   - position nudges;
   - audit output and sound counts;
   - your token usage (input, cached, output).
5. Commit everything on **your branch `qwen-v2`**. The director reviews by pulling that branch; `main` stays untouched.

## 12. If something is unclear
Choose the option that is more literal to the narration line, write it in the report, and continue. Don't stop to ask.
