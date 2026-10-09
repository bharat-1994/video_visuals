<!-- bakeoff/RULES.md -->
# Builder rules (identical for every model in the test; paste this + one card)

You build ONE file for ONE task card. Read only: this file, your card, LIB_CHEATSHEET.md. Do not read engine/lib.py or other assets.

Hard budgets (stop and report if you hit one; do not argue with them):
- ONE file. At most TWO runs of `python3 bakeoff/score.py <card-letter> <your file> <out_dir>` (or score_lines.py for card D).
- Look at each output image at most ONCE. No extra zoom images. No helper agents. No re-reading files you already read.
- Write the whole file in one go, run, fix once, run, then STOP.

Style (the channel's look): flat fills, 2-3 tones per material, INK outlines 2-3 px, details via loops, no gradients, no emblems,
no brand logos or brand names (plain generic lettering only if the card allows text). Draw the REAL kind of object, not a generic box.

Before writing code, write a comment block listing the signature features you will draw (copy them from the card, numbered).
After your last run, reply with exactly:
1. FEATURES: for each numbered signature feature, YES or NO (be honest; a script and a person will check)
2. RUNS used: n.  3. Known flaws: one line each.  4. Anything in the card that was unclear.


---

<!-- bakeoff/LIB_CHEATSHEET.md -->
# lib cheatsheet (everything you need from engine/lib.py; do not read lib.py)

Canvas 1280x720, y grows downward. `from lib import *` gives all of these plus INK (outline colour) and FONT.

```
hexc(h)
clamp(x, a=0, b=1)
lerp(a, b, t)
box(ctx, x, y, w, h, c, r=0, line=None, lw=3)
rrect(ctx, x, y, w, h, r)
circle(ctx, x, y, r, c, line=None, lw=3, a=1)
ellipse(ctx, x, y, rx, ry, c, a=1)
poly(ctx, pts, c, line=None, lw=3, a=1)
line(ctx, pts, c=(0.08, 0.08, 0.1), lw=6, a=1)
hose(ctx, p0, p1, bend=0.25, lw=9, c=(0.08, 0.08, 0.1))   # rubber-hose limb: curved stroke from p0 to p1; bend>0 bows to the right of travel.
text(ctx, s, x, y, size=48, c=(1, 1, 1), anchor='c', reveal=1.0, rot=0, outline=None)   # handwritten text; reveal 0..1 = typewriter.
smooth(ctx, pts, start=True)   # Catmull-Rom spline through pts (continues current path unless start).
```

`box(ctx, x, y, w, h, ...)` takes the TOP-LEFT corner; `circle`/`ellipse` take the CENTRE; `text(ctx, s, x, y)` is centred on x by default.
Colours are RGB tuples 0..1; `hexc('#e5b73b')` makes one (6-digit hex only).
`poly(ctx, pts, fill, line=INK, lw=3)` fills a closed polygon; `smooth(ctx, pts)` adds a smooth path you then fill/stroke yourself.
`ctx` is a pycairo Context: ctx.save()/restore(), translate, scale, rotate, arc, curve_to are all allowed.
Style: flat fills, 2 or 3 tones per material (base, shadow side, highlight), INK outlines 2-3 px, small repeated details via loops, no gradients, no blur, no emblems or logos.


---

<!-- engine/SCENE_LANGUAGE.md -->
# Scene lines (engine/scene_v2.py): one line per shot

A shot = elements separated by ` | `. Element = TYPE, positional numbers (x y [scale|size]), key=value pairs, timing tokens. Quote text that has spaces.
Canvas 1280x720, y down. A person's (x, y) is the waist base: y 600-640 puts feet near the bottom; the head centre is ~230 px above y at scale 1.

## Timing tokens
`@word` appears when that narration word is spoken (case/punctuation ignored, prefix match: `@invest` hits "investment") · `@word#2` 2nd occurrence ·
`@word+0.3` offset · `@1.5` = seconds from shot start (**seconds need a decimal point**; `@50` means the word "50") · `out@word` vanishes with a puff ·
`key=a>b:@word:0.6` animates a number from a to b starting at @word over 0.6 s. A word that is not in this shot's narration is an error.
Every shot needs something NEW tied to a narration word at least every 2.5 s. engine/beats.py measures the longest stretch between the cut, each @word beat and the end of the speech; only the first beat of a shot may sit at the cut itself.

## Elements
| element | meaning |
|---|---|
| `bg NAME k=v` | background (see CATALOG). Always first. |
| `cam push\|pull\|still\|pan\|whip\|track [z0 z1 cx cy [cx2 cy2]]` | camera; default push. whip = snap in from the left; track X0 X1 = constant-speed pan |
| `shake @word amp=0.6` | impact shake + thud (only for real impacts) |
| `p WHO x y s e=EXPR f=-1..1 pose=NAME pose2=NAME@word e2=EXPR@word legs=0 view=back walk=px/s talk=@w1~@w2 handL=x,y handR=x,y` | person from CAST. f = facing (-1 left, 1 right). handL/handR put that hand exactly on a point |
| `a NAME x y [s] k=v @word` | asset call `NAME(ctx, x, y, ...)`; with @word it pops in. `move=dx,dy:@word:dur` slides it. `snd=NAME` sets its entrance sound, `snd=none` silences |
| `kw "TEXT" x y size @word` | white outlined keyword; give it an @word so it appears on that word |
| `st "TEXT" x y size rot=` | yellow sticky note (`\n` = 2 lines) |
| `tx "TEXT" x y size c=#hex anchor=c` | typewriter text (time markers, labels) |
| `card "TEXT" sub="..."` | black chapter card |
| `cnt A B x y size fmt="${:,}B" dur=1.2` | counting number |
| `dlg "TEXT" x y tox toy` | dialogue line with a tick pointing to the speaker's mouth (tox,toy) |
| `arrow x1 y1 x2 y2 c=#hex lw=10` · `bars x y w h vals=[..] labels=[..] fmt="{}" c=#hex hl=i` | arrow / growing bar chart |
| `fn NAME k=v` | custom shot code (CUSTOM registry) |
| `fx NAME @word` | continuous motion layer (FX registry). ONLY when the narration names the motion or the real place has it |
| `sfx NAME @word db=-6` | extra sound from audio/sfx/INDEX.md |

Poses: carry_R down hips hold_front phone_R point_L point_R raise_both shrug think_R type_L type_R wave_R.
Expressions: neutral happy sad angry worried shocked smug tired determined.

## House rules (the audits enforce what they can)
- **Motion only if the narration names it or the real place has it.** No sliding or walking people, no moving vehicles, no spinning, rain, confetti or steam for their own sake. `walk=`, `move=` and `fx` must be tied to a narration word (the audit flags untied ones; a director can list a shot in the episode's AUDIT motion_ok after checking that the narration or the real place really has that motion). If there is no real motion, the shot stays still: pop-ins on words, a slow camera, nothing else.
- **People appear only when the script makes them relevant** (a character acts, speaks, reacts, or the point is about people). Otherwise show the thing: the place, the object, the chart. Two people interact only when the script describes an interaction (a deal, an argument, a handshake). No quotas.
- Backgrounds: none in more than ~8% of shots, no 3 identical in a row. Dark/spotlight only for a real emotional beat or the cage/map motif.
- Sounds are automatic by element category (see audio/sfx/INDEX.md); do not add `pop`. At most 3 entrance sounds per shot.
- Never put text over a face; keep text in y 90-130 (top) or below the chin of the nearest head; nothing important in the outer 40 px.
- No logos or seals. Companies = brand colour + plain name lettering + the real kind of place (factory, office, store).
- Reserve the meeting-room screen area x 556-1116, y 118-418.
- A shot id may appear only once in a lines file (the last duplicate silently wins; layout_check flags it).


---

<!-- library/catalog/CATALOG.md (names you may use) -->
asset `asia_map` `asia_map(ctx, x, y, h=600, highlight='VN', labels=True)`
asset `assembly_line` `assembly_line(ctx, x, y, w=900, t=0.0, item=None, gap=170, speed=90)`
asset `assembly_phones` `assembly_phones(ctx, x, y, w=900, t=0.0, side='back', label='MADE IN VIETNAM')`
asset `bg_congress` `bg_congress(ctx, t=0.0, banner='6TH NATIONAL CONGRESS  ·  1986')`
asset `bg_dark` `bg_dark(ctx)`
asset `bg_flat` `bg_flat(ctx, c)`
asset `bg_kitchen` `bg_kitchen(ctx, t=0.0)`
asset `bg_paddy` `bg_paddy(ctx, t=0.0, karst=True)`
asset `bg_room` `bg_room(ctx, wall=(0.9137254901960784, 0.8941176470588236, 0.8470588235294118`
asset `bg_sky_ground` `bg_sky_ground(ctx, sky=(0.6235294117647059, 0.8470588235294118, 0.9411764705882353)`
asset `bg_spotlight` `bg_spotlight(ctx, base=(0.13, 0.13, 0.15), cx=640.0, floor_y=620)`
asset `bg_sunset` `bg_sunset(ctx)`
asset `bill` `bill(ctx, x, y, rot=0, s=1.0)`
asset `books_cap` `books_cap(ctx, x, y, s=1.0)`
asset `box` `box(ctx, x, y, w, h, c, r=0, line=None, lw=3)`
asset `cage` `cage(ctx, x, y, w, h, lock_label='EMBARGO', bars=7, lock=1.0)`
asset `caged_map` `caged_map(ctx, x, y, h=440, tilt=0.0, lock=1.0, cracks=1.0)`
asset `calendar` `calendar(ctx, x, y, s=1.0, top='1986', big='MONTH', flip=0.0)`
asset `camera` `camera(ctx, zoom=1.0, cx=640.0, cy=360.0, shake=0.0, t=0)`
asset `cargo_plane` `cargo_plane(ctx, x, y, s=1.0, **kv)`
asset `cargo_truck` `cargo_truck(ctx, x, y, s=1.0, label=None, c=None)`
asset `carton` `carton(ctx, x, y, s=1.0, label='FRAGILE', **kv)`
asset `chalk_text` `chalk_text(ctx, x, y, s=1.0, text='chalk', t=0.0, t0=0.0, size=52, seed=4, **kv)`
asset `chip` `chip(ctx, x, y, s=1.0, label='CHIP')`
asset `circle` `circle(ctx, x, y, r, c, line=None, lw=3, a=1)`
asset `circuit_board` `circuit_board(ctx, x, y, w=400, h=260)`
asset `city_card` `city_card(ctx, x, y, s=1.0, city='newyork', label=None, **kv)`
asset `city_window` `city_window(ctx, x, y, w, h, night=False)`
asset `coin` `coin(ctx, x, y, r=22)`
asset `compass` `compass(ctx, x, y, s=1.0, **kv)`
asset `container` `container(ctx, x, y, s=1.0, c=None, label=None)`
asset `container_ship` `container_ship(ctx, x, y, s=1.0, t=0.0, label=None)`
asset `coop_farm` `coop_farm(ctx, x, y, s=1.0, t=0.0)`
asset `crt` `crt(ctx, x, y, s=1.0, screen=(0.11372549019607843, 0.16862745098039217, 0`
asset `desk` `desk(ctx, x, y, w=420, c=(0.6588235294117647, 0.4392156862745098, 0.247058`
asset `dialogue` `dialogue(ctx, s, x, y, to, size=40, reveal=1.0, c=(1, 1, 1), ink=(0.08, 0.08, `
asset `dish` `dish(ctx, x, y, s=1.0, state='fresh', t=0.0)`
asset `dong_note` `dong_note(ctx, x, y, s=1.0, rot=0.0, value='100', wither=0.0)`
asset `draw_hair` `draw_hair(ctx, hx, hy, R, style, hc, f=0.0)`
asset `dust` `dust(ctx, x, y, t, start, n=5, size=70, seed=1)`
asset `earbuds_case` `earbuds_case(ctx, x, y, s=1.0)`
asset `ellipse` `ellipse(ctx, x, y, rx, ry, c, a=1)`
asset `empty_chairs` `empty_chairs(ctx, x, y, s=1.0, **kv)`
asset `factory` `factory(ctx, x, y, s=1.0, t=0.0, label='FACTORY')`
asset `factory_modern` `factory_modern(ctx, x, y, s=1.0, label='', **kv)`
asset `fill` `fill(ctx, c, a=1)`
asset `food_stall` `food_stall(ctx, x, y, s=1.0, label='COM TAM', **kv)`
asset `fta_scroll` `fta_scroll(ctx, x, y, s=1.0, label='FTA')`
asset `globe` `globe(ctx, x, y, r=150, t=0.0)`
asset `golden_key` `golden_key(ctx, x, y, s=1.0, rot=0.0)`
asset `handshake` `handshake(ctx, x, y, s=1.0, sleeveL=None, sleeveR=None)`
asset `head_path` `head_path(ctx, hx, hy, R, jaw=0.0)`
asset `highway` `highway(ctx, y, t=0.0)`
asset `hose` `hose(ctx, p0, p1, bend=0.25, lw=9, c=(0.08, 0.08, 0.1))`
asset `kerosene_lamp` `kerosene_lamp(ctx, x, y, s=1.0, lit=True, t=0.0)`
asset `keyword` `keyword(ctx, t, start, s, x, y, size=72, seed=5)`
asset `ladder` `ladder(ctx, x, y, h=500, missing_from=0.65, s=1.0)`
asset `land_deed` `land_deed(ctx, x, y, s=1.0, rot=0.0, name='NGUYEN FAMILY')`
asset `laptop` `laptop(ctx, x, y, s=1.0, screen='', **kv)`
asset `line` `line(ctx, pts, c=(0.08, 0.08, 0.1), lw=6, a=1)`
asset `loudspeaker_pole` `loudspeaker_pole(ctx, x, y, s=1.0, **kv)`
asset `microscope` `microscope(ctx, x, y, s=1.0, **kv)`
asset `money_bag` `money_bag(ctx, x, y, s=1.0, label='$')`
asset `non_la` `non_la(ctx, x, y, R)`
asset `open_doors` `open_doors(ctx, x, y, w=420, h=520, open_=0.0, label='FDI')`
asset `padlock` `padlock(ctx, x, y, s=1.0, label='EMBARGO')`
asset `palm` `palm(ctx, x, y, s=1.0)`
asset `paper` `paper(ctx, x, y, w, h, rot=0, c=(1, 1, 1), lines_=4, label=None, size=30, i`
asset `pit_trap` `pit_trap(ctx, x, y, w=420, label='MIDDLE-INCOME TRAP')`
asset `podium` `podium(ctx, x, y, s=1.0)`
asset `poly` `poly(ctx, pts, c, line=None, lw=3, a=1)`
asset `popped` `popped(ctx, t, start, x, y, draw, dur=0.35, puff=True, seed=3)`
asset `pork` `pork(ctx, x, y, s=1.0)`
asset `port_crane` `port_crane(ctx, x, y, s=1.0)`
asset `price_board` `price_board(ctx, x, y, s=1.0, locked=False)`
asset `price_tag` `price_tag(ctx, x, y, s=1.0, value='100', walk=None, t=0.0)`
asset `rank_podium` `rank_podium(ctx, x, y, s=1.0, labels=('', 'VIETNAM', ''), ranks=(1, 2, 3), hl=Non`
asset `ration_coupon` `ration_coupon(ctx, x, y, s=1.0, rot=0.0, rows=(('RICE', '13 kg'), ('PORK', '0.5 kg'`
asset `rd_center` `rd_center(ctx, x, y, s=1.0, label='R&D CENTER')`
asset `rice_bowl` `rice_bowl(ctx, x, y, s=1.0, fill_=1.0)`
asset `rice_heap` `rice_heap(ctx, x, y, s=1.0)`
asset `rice_sack` `rice_sack(ctx, x, y, s=1.0, label='RICE')`
asset `road_sign` `road_sign(ctx, x, y, s=1.0, text='BAC NINH 30 km', **kv)`
asset `rrect` `rrect(ctx, x, y, w, h, r)`
asset `rubber_stamp` `rubber_stamp(ctx, x, y, s=1.0)`
asset `sea` `sea(ctx, y, t=0.0)`
asset `sewing_machine` `sewing_machine(ctx, x, y, s=1.0, **kv)`
asset `shop_front` `shop_front(ctx, x, y, s=1.0, closed=0.0, label='PHO', **kv)`
asset `skyline` `skyline(ctx, y, night=False, t=0.0)`
asset `smartphone` `smartphone(ctx, x, y, s=1.0, rot=0.0, side='front', label=None)`
asset `smartwatch` `smartwatch(ctx, x, y, s=1.0)`
asset `smile_curve` `smile_curve(ctx, x, y, w=820, h=420, progress=1.0, labels=('R&D', 'DESIGN', 'ASSE`
asset `smoke` `smoke(ctx, x, y, t, size=60, seed=1)`
asset `smooth` `smooth(ctx, pts, start=True)`
asset `sneaker` `sneaker(ctx, x, y, s=1.0, **kv)`
asset `solar_panel` `solar_panel(ctx, x, y, s=1.0, **kv)`
asset `stamp_mark` `stamp_mark(ctx, x, y, text='MADE IN VIETNAM', s=1.0, rot=-0.12)`
asset `state_cap` `state_cap(ctx, x, y, R, f=0.0)`
asset `state_counter` `state_counter(ctx, x, y, w=520)`
asset `sticky` `sticky(ctx, x, y, s, rot=-0.05, c=(1.0, 0.8901960784313725, 0.43137254901960`
asset `stone_mill` `stone_mill(ctx, x, y, s=1.0, ang=0.0, pole_dir=1)`
asset `tablet` `tablet(ctx, x, y, s=1.0, rot=0.0)`
asset `tariff_wall` `tariff_wall(ctx, x, y, w=600, h=360, label='25% TARIFF', build=1.0)`
asset `text` `text(ctx, s, x, y, size=48, c=(1, 1, 1), anchor='c', reveal=1.0, rot=0, ou`
asset `toque` `toque(ctx, x, y, R)`
asset `trophy` `trophy(ctx, x, y, s=1.0, **kv)`
asset `tv_screen` `tv_screen(ctx, x, y, s=1.0, headline='VIETNAM EXPORTS SOAR', **kv)`
asset `ussr_pillar` `ussr_pillar(ctx, x, y, h=460, crumble=0.0, t=0.0, label='USSR')`
asset `vault_door` `vault_door(ctx, x, y, s=1.0, open_=0.0, **kv)`
asset `vietnam_map` `vietnam_map(ctx, x, y, h, c=(0.9137254901960784, 0.7254901960784313, 0.2862745098`
asset `wafer` `wafer(ctx, x, y, s=1.0, **kv)`
asset `whiteboard` `whiteboard(ctx, x, y, s=1.0, lines=(), at=(), t=0.0, **kv)`
bg `air_cargo` `air_cargo(ctx, t=0.0, **kv)`
bg `assembly_hall` `assembly_hall(ctx, t=0.0, **kv)`
bg `beijing_1978` `beijing_1978(ctx, t=0.0, **kv)`
bg `border` `border(ctx, t=0.0, **kv)`
bg `boxing_ring` `boxing_ring(ctx, t=0.0, **kv)`
bg `casino_table` `casino_table(ctx, t=0.0, **kv)`
bg `city` `city(ctx, t=0.0, night=False)`
bg `classroom` `classroom(ctx, t=0.0, **kv)`
bg `cleanroom` `cleanroom(ctx, t=0.0, **kv)`
bg `congress` `congress(ctx, t=0.0, banner='6TH NATIONAL CONGRESS  ·  1986')`
bg `construction` `construction(ctx, t=0.0, **kv)`
bg `coop_yard` `coop_yard(ctx, t=0.0, **kv)`
bg `dark` `dark(ctx)`
bg `design_studio` `design_studio(ctx, t=0.0, **kv)`
bg `drone_view` `drone_view(ctx, t=0.0, **kv)`
bg `embassy` `embassy(ctx, t=0.0, **kv)`
bg `engine_room` `engine_room(ctx, t=0.0, **kv)`
bg `expo_hall` `expo_hall(ctx, t=0.0, **kv)`
bg `factory` `factory(ctx)`
bg `factory_gate` `factory_gate(ctx, t=0.0, **kv)`
bg `flat` `flat(ctx, c='#e9e1cf')`
bg `foxconn_campus` `foxconn_campus(ctx, t=0.0, **kv)`
bg `garment_hall` `garment_hall(ctx, t=0.0, **kv)`
bg `globe_space` `globe_space(ctx, t=0.0, **kv)`
bg `government_hall` `government_hall(ctx, t=0.0, **kv)`
bg `hanoi_1986` `hanoi_1986(ctx, t=0.0, **kv)`
bg `hanoi_street_1990` `hanoi_street_1990(ctx, t=0.0, **kv)`
bg `hanoi_today` `hanoi_today(ctx, t=0.0, **kv)`
bg `harvest_gold` `harvest_gold(ctx, t=0.0, **kv)`
bg `harvest_poor` `harvest_poor(ctx, t=0.0, **kv)`
bg `kitchen` `kitchen(ctx, t=0.0)`
bg `kitchen_wall` `kitchen_wall(ctx, t=0.0, **kv)`
bg `lab` `lab(ctx, t=0.0, **kv)`
bg `market` `market(ctx, t=0.0, **kv)`
bg `meeting_room` `meeting_room(ctx, t=0.0, **kv)`
bg `newsroom` `newsroom(ctx, t=0.0, **kv)`
bg `night` `night(ctx, t=0.0)`
bg `night_city` `night_city(ctx, t=0.0, **kv)`
bg `north_vn_hills` `north_vn_hills(ctx, t=0.0, **kv)`
bg `office` `office(ctx, wall='#dfe3e6')`
bg `office_1980s` `office_1980s(ctx, t=0.0, **kv)`
bg `paddy` `paddy(ctx, t=0.0)`
bg `port` `port(ctx, t=0.0)`
bg `port_day` `port_day(ctx, t=0.0, **kv)`
bg `port_night` `port_night(ctx, t=0.0, **kv)`
bg `race_track` `race_track(ctx, t=0.0, **kv)`
bg `renovation` `renovation(ctx, t=0.0, **kv)`
bg `rice_to_factory` `rice_to_factory(ctx, t=0.0, **kv)`
bg `room` `room(ctx, wall='#e9e1cf', floor='#b98a5e')`
bg `ruins` `ruins(ctx, t=0.0, **kv)`
bg `samsung_campus` `samsung_campus(ctx, t=0.0, **kv)`
bg `samsung_hall` `samsung_hall(ctx, t=0.0, **kv)`
bg `sea_lanes` `sea_lanes(ctx, t=0.0, **kv)`
bg `seoul_hq` `seoul_hq(ctx, t=0.0, **kv)`
bg `signing_table` `signing_table(ctx, t=0.0, **kv)`
bg `sky` `sky(ctx, sky='#bfe3ef', ground='#8cc46f', horizon=560)`
bg `small_workshop` `small_workshop(ctx, t=0.0, **kv)`
bg `split2` `split2(ctx, t=0.0, **kv)`
bg `state_store` `state_store(ctx, t=0.0, **kv)`
bg `sunrise` `sunrise(ctx, t=0.0, **kv)`
bg `trophy_stage` `trophy_stage(ctx, t=0.0, **kv)`
bg `vault` `vault(ctx, t=0.0, **kv)`
bg `vhs_rewind` `vhs_rewind(ctx, t=0.0, **kv)`
bg `warehouse` `warehouse(ctx, t=0.0, **kv)`
bg `white_studio` `white_studio(ctx, t=0.0, **kv)`
cast `banker` `p banker x y [scale]`
cast `bunny` `p bunny x y [scale]`
cast `chef` `p chef x y [scale]`
cast `clerk` `p clerk x y [scale]`
cast `cn_official` `p cn_official x y [scale]`
cast `customer` `p customer x y [scale]`
cast `editor` `p editor x y [scale]`
cast `exec` `p exec x y [scale]`
cast `exec2` `p exec2 x y [scale]`
cast `farmer` `p farmer x y [scale]`
cast `kid` `p kid x y [scale]`
cast `lan` `p lan x y [scale]`
cast `minh` `p minh x y [scale]`
cast `mother` `p mother x y [scale]`
cast `official` `p official x y [scale]`
cast `official2` `p official2 x y [scale]`
cast `us_official` `p us_official x y [scale]`
cast `worker` `p worker x y [scale]`
cast `worker_m` `p worker_m x y [scale]`