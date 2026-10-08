# Asset catalog (generated; look at the sheets next to this file)

| kind | name | call | what | drawn size px | note |
|---|---|---|---|---|---|
| asset | `asia_map` | `asia_map(ctx, x, y, h=600, highlight='VN', labels=True)` | Stylized East + Southeast Asia, (x,y) = centre of a rounded sea-blue frame covering lon 92 | 683x502 |  |
| asset | `assembly_line` | `assembly_line(ctx, x, y, w=900, t=0.0, item=None, gap=170, speed=90)` | Anchor: x = left end, y = belt TOP. Steel frame + legs, rollers, moving belt stripes (t*sp | 641x170 |  |
| asset | `assembly_phones` | `assembly_phones(ctx, x, y, w=900, t=0.0, side='back', label='MADE IN VIETNAM')` | Assembly line carrying phones (standing on the belt). | 641x291 |  |
| asset | `bg_congress` | `bg_congress(ctx, t=0.0, banner='6TH NATIONAL CONGRESS  ·  1986')` | Full-frame party congress hall. Anchor: whole canvas. Deep red curtain with 3-tone vertica | 0x0 | needs args:  |
| asset | `bg_dark` | `bg_dark(ctx)` | Emotional/abstract beats: near-black with a soft spotlight. | 0x0 | needs args:  |
| asset | `bg_flat` | `bg_flat(ctx, c)` |  | 0x0 | needs args:  |
| asset | `bg_kitchen` | `bg_kitchen(ctx, t=0.0)` | Full-frame restaurant kitchen. Anchor: whole canvas. White tile wall (60px grid, y 0-520), | 0x0 | needs args:  |
| asset | `bg_paddy` | `bg_paddy(ctx, t=0.0, karst=True)` | Northern countryside: pale sky, limestone karst peaks, flooded paddy rows reflecting sky,  | 0x0 | needs args:  |
| asset | `bg_room` | `bg_room(ctx, wall=(0.9137254901960784, 0.8941176470588236, 0.8470588235294118` |  | 0x0 | needs args:  |
| asset | `bg_sky_ground` | `bg_sky_ground(ctx, sky=(0.6235294117647059, 0.8470588235294118, 0.9411764705882353)` |  | 0x0 | needs args:  |
| asset | `bg_spotlight` | `bg_spotlight(ctx, base=(0.13, 0.13, 0.15), cx=640.0, floor_y=620)` |  | 0x0 | needs args:  |
| asset | `bg_sunset` | `bg_sunset(ctx)` |  | 0x0 | needs args:  |
| asset | `bill` | `bill(ctx, x, y, rot=0, s=1.0)` |  | 83x43 |  |
| asset | `books_cap` | `books_cap(ctx, x, y, s=1.0)` | Stack of three textbooks (MATH, SCIENCE, CODE spines facing us, slightly offset) with a gr | 339x261 |  |
| asset | `box` | `box(ctx, x, y, w, h, c, r=0, line=None, lw=3)` |  | 0x0 | needs args: w,h,c |
| asset | `cage` | `cage(ctx, x, y, w, h, lock_label='EMBARGO', bars=7, lock=1.0)` | Bird-cage style trap, (x,y) = bottom centre. Dome top, ring, vertical bars, base rail, pad | 0x0 | needs args: w,h |
| asset | `caged_map` | `caged_map(ctx, x, y, h=440, tilt=0.0, lock=1.0, cracks=1.0)` | RECURRING: the map of Vietnam inside the EMBARGO cage. (x,y) = cage bottom centre, h = cag | 389x461 |  |
| asset | `calendar` | `calendar(ctx, x, y, s=1.0, top='1986', big='MONTH', flip=0.0)` | Tear-off wall calendar, centre x,y. flip 0..1 animates the top page tearing away upward. | 183x229 |  |
| asset | `camera` | `camera(ctx, zoom=1.0, cx=640.0, cy=360.0, shake=0.0, t=0)` | apply camera: zoom about (cx,cy). | 0x0 |  |
| asset | `cargo_plane` | `cargo_plane(ctx, x, y, s=1.0, **kv)` | Anchor: centre (fuselage middle). Wide-body cargo jet ~700 wide at s=1 facing LEFT: white  | 864x362 |  |
| asset | `cargo_truck` | `cargo_truck(ctx, x, y, s=1.0, label=None, c=None)` | Anchor: bottom-centre. Side-view box truck ~340x170 facing right: big box body (colour c,  | 351x173 |  |
| asset | `carton` | `carton(ctx, x, y, s=1.0, label='FRAGILE', **kv)` | Anchor: bottom-centre. 180x140 cardboard box at s=1: front face in 2 tones, top face in pe | 187x141 |  |
| asset | `chalk_text` | `chalk_text(ctx, x, y, s=1.0, text='chalk', t=0.0, t0=0.0, size=52, seed=4, **kv)` | Anchor: centre of the text block. White chalk handwriting, per-letter jitter (seeded), rev | 203x141 |  |
| asset | `chip` | `chip(ctx, x, y, s=1.0, label='CHIP')` | Anchor: centre. ~160x160. Dark IC package with bevelled edge, 8 gold pins on each of the 4 | 157x157 |  |
| asset | `circle` | `circle(ctx, x, y, r, c, line=None, lw=3, a=1)` |  | 0x0 | needs args: r,c |
| asset | `circuit_board` | `circuit_board(ctx, x, y, w=400, h=260)` | Anchor: top-left. Green PCB with darker border, right-angled light-green traces ending in  | 403x201 |  |
| asset | `city_card` | `city_card(ctx, x, y, s=1.0, city='newyork', label=None, **kv)` | Anchor: centre. 300x200 framed postcard at s=1. A city LANDMARK SILHOUETTE inside a border | 299x203 |  |
| asset | `city_window` | `city_window(ctx, x, y, w, h, night=False)` |  | 0x0 | needs args: w,h |
| asset | `coin` | `coin(ctx, x, y, r=22)` |  | 47x47 |  |
| asset | `compass` | `compass(ctx, x, y, s=1.0, **kv)` | Anchor: centre. Nautical compass rose r=150 at s=1: parchment ring with tick marks, 8-poin | 303x303 |  |
| asset | `container` | `container(ctx, x, y, s=1.0, c=None, label=None)` | Anchor: bottom-left. Side view 240x100 at s=1: corrugated vertical ribs (loop), door end a | 243x103 |  |
| asset | `container_ship` | `container_ship(ctx, x, y, s=1.0, t=0.0, label=None)` | Anchor: waterline centre (x,y). ~800 wide at s=1. Dark navy hull with red bottom stripe an | 806x269 |  |
| asset | `coop_farm` | `coop_farm(ctx, x, y, s=1.0, t=0.0)` | Collective barn, (x,y) = bottom centre. ~560x300: red plank walls, gable roof with shingle | 659x322 |  |
| asset | `crt` | `crt(ctx, x, y, s=1.0, screen=(0.11372549019607843, 0.16862745098039217, 0` | CRT monitor sitting with base at (x,y). | 223x193 |  |
| asset | `desk` | `desk(ctx, x, y, w=420, c=(0.6588235294117647, 0.4392156862745098, 0.247058` |  | 423x169 |  |
| asset | `dialogue` | `dialogue(ctx, s, x, y, to, size=40, reveal=1.0, c=(1, 1, 1), ink=(0.08, 0.08, ` | reference style: white handwritten line, dark outline, tiny tick pointing at speaker mouth | 0x0 | needs args: y,to |
| asset | `dish` | `dish(ctx, x, y, s=1.0, state='fresh', t=0.0)` | Bowl of pho on a plate, (x,y) = bottom centre. ~300 wide x ~170 tall. Fresh: broth, white  | 326x220 |  |
| asset | `dong_note` | `dong_note(ctx, x, y, s=1.0, rot=0.0, value='100', wither=0.0)` | Generic banknote, NO portrait/seal/emblem: green paper, guilloche ovals, value in corners, | 303x143 |  |
| asset | `draw_hair` | `draw_hair(ctx, hx, hy, R, style, hc, f=0.0)` |  | 0x0 | needs args: R,style,hc |
| asset | `dust` | `dust(ctx, x, y, t, start, n=5, size=70, seed=1)` | A burst of smoke puffs (impacts, collapse). | 0x0 | needs args: t,start |
| asset | `earbuds_case` | `earbuds_case(ctx, x, y, s=1.0)` | Anchor: centre. ~120x150 at s=1. Generic white rounded charging case with open lid (tilted | 127x155 |  |
| asset | `ellipse` | `ellipse(ctx, x, y, rx, ry, c, a=1)` |  | 0x0 | needs args: rx,ry,c |
| asset | `empty_chairs` | `empty_chairs(ctx, x, y, s=1.0, **kv)` | Anchor: bottom-centre. Three empty chairs (~90 wide each, 190 tall at s=1) with jackets dr | 363x283 |  |
| asset | `factory` | `factory(ctx, x, y, s=1.0, t=0.0, label='FACTORY')` | Anchor: bottom-centre. ~520x300 at s=1. Brick wall in 2 tones, sawtooth roof (4 teeth, gla | 523x438 |  |
| asset | `factory_modern` | `factory_modern(ctx, x, y, s=1.0, label='', **kv)` | Anchor: bottom-centre. 520x260 modern flat-roof plant at s=1: light wall with a high glass | 539x279 |  |
| asset | `fill` | `fill(ctx, c, a=1)` |  | 0x0 | needs args:  |
| asset | `food_stall` | `food_stall(ctx, x, y, s=1.0, label='COM TAM', **kv)` | Anchor: bottom-centre. Vietnamese street cart ~300x290 at s=1: wooden cart with plank line | 334x268 |  |
| asset | `fta_scroll` | `fta_scroll(ctx, x, y, s=1.0, label='FTA')` | Half-unrolled treaty document, (x,y) = centre, ~340x330. Cream sheet between two wooden ro | 437x344 |  |
| asset | `globe` | `globe(ctx, x, y, r=150, t=0.0)` | Generic globe: ocean disc, simple drifting continent blobs, latitude lines. No real-countr | 303x303 |  |
| asset | `golden_key` | `golden_key(ctx, x, y, s=1.0, rot=0.0)` | Ornate gold key, (x,y) = centre, ~240 long, horizontal at rot=0 (bow on the left, bit on t | 299x147 |  |
| asset | `handshake` | `handshake(ctx, x, y, s=1.0, sleeveL=None, sleeveR=None)` | Two forearms meeting in a firm handshake, (x,y) = centre of the clasp. ~520 wide. Left arm | 723x223 |  |
| asset | `head_path` | `head_path(ctx, hx, hy, R, jaw=0.0)` |  | 0x0 | needs args: R |
| asset | `highway` | `highway(ctx, y, t=0.0)` | Anchor: full width, band from y downward ~140 px. Light kerb strip on top, asphalt, white  | 0x0 | needs args:  |
| asset | `hose` | `hose(ctx, p0, p1, bend=0.25, lw=9, c=(0.08, 0.08, 0.1))` | rubber-hose limb: curved stroke from p0 to p1; bend>0 bows to the right of travel. | 0x0 | needs args:  |
| asset | `kerosene_lamp` | `kerosene_lamp(ctx, x, y, s=1.0, lit=True, t=0.0)` | Hurricane lantern, (x,y) = bottom centre. Tin tank, glass globe with wire guards, top cap  | 139x209 |  |
| asset | `keyword` | `keyword(ctx, t, start, s, x, y, size=72, seed=5)` | House keyword: white text with ink outline, popped on its word. | 0x0 | needs args: s,x,y |
| asset | `ladder` | `ladder(ctx, x, y, h=500, missing_from=0.65, s=1.0)` | Tall wooden ladder, (x,y) = bottom centre. Rails converge slightly toward the top. Rungs e | 199x512 |  |
| asset | `land_deed` | `land_deed(ctx, x, y, s=1.0, rot=0.0, name='NGUYEN FAMILY')` | Land-use-rights certificate, (x,y) = centre, ~260x340, rotatable. Cream paper, title 'LAND | 268x350 |  |
| asset | `laptop` | `laptop(ctx, x, y, s=1.0, screen='', **kv)` | Anchor: bottom-centre. Open laptop ~330x230 at s=1, 3/4 view: silver skewed deck with loop | 378x229 |  |
| asset | `line` | `line(ctx, pts, c=(0.08, 0.08, 0.1), lw=6, a=1)` |  | 0x0 | needs args:  |
| asset | `loudspeaker_pole` | `loudspeaker_pole(ctx, x, y, s=1.0, **kv)` | Anchor: bottom-centre. Village PA pole ~330 tall at s=1: 2-tone wooden pole with a crossba | 336x396 |  |
| asset | `microscope` | `microscope(ctx, x, y, s=1.0, **kv)` | Anchor: bottom-centre. Compound microscope ~230x300 at s=1: dark base with built-in illumi | 183x299 |  |
| asset | `money_bag` | `money_bag(ctx, x, y, s=1.0, label='$')` |  | 111x141 |  |
| asset | `non_la` | `non_la(ctx, x, y, R)` | Conical palm-leaf hat. (x,y) = brim centre. Signature: wide shallow cone, radial weave lin | 0x0 | needs args: R |
| asset | `open_doors` | `open_doors(ctx, x, y, w=420, h=520, open_=0.0, label='FDI')` | Big double doors in a brick/stone frame, (x,y) = bottom centre. Wall block w x h; opening  | 423x546 |  |
| asset | `padlock` | `padlock(ctx, x, y, s=1.0, label='EMBARGO')` |  | 161x152 |  |
| asset | `palm` | `palm(ctx, x, y, s=1.0)` | Coconut palm. (x,y) = base. | 158x223 |  |
| asset | `paper` | `paper(ctx, x, y, w, h, rot=0, c=(1, 1, 1), lines_=4, label=None, size=30, i` |  | 0x0 | needs args: w,h |
| asset | `pit_trap` | `pit_trap(ctx, x, y, w=420, label='MIDDLE-INCOME TRAP')` | Hole in the ground, (x,y) = centre of the opening at ground level. Grass+earth patch, dark | 621x414 |  |
| asset | `podium` | `podium(ctx, x, y, s=1.0)` | Wooden lectern, (x,y) = bottom centre. ~150 wide x 220 tall (body 190 + slanted top), fron | 183x320 |  |
| asset | `poly` | `poly(ctx, pts, c, line=None, lw=3, a=1)` |  | 0x0 | needs args:  |
| asset | `popped` | `popped(ctx, t, start, x, y, draw, dur=0.35, puff=True, seed=3)` | draw(ctx) around origin, scaled in with overshoot at time start, with smoke puff. | 0x0 | needs args: x,y,draw |
| asset | `pork` | `pork(ctx, x, y, s=1.0)` | Cut of pork belly (layered fat/meat stripes), centre x,y. | 211x103 |  |
| asset | `port_crane` | `port_crane(ctx, x, y, s=1.0)` | Anchor: bottom-centre. Ship-to-shore gantry crane ~380 tall x ~460 wide: A-frame legs with | 465x390 |  |
| asset | `price_board` | `price_board(ctx, x, y, s=1.0, locked=False)` | Chalk menu board, (x,y) = centre. ~300x220: wood frame, dark green board, 'MENU' title, 4  | 307x229 |  |
| asset | `price_tag` | `price_tag(ctx, x, y, s=1.0, value='100', walk=None, t=0.0)` | Shop price tag with optional running legs. (x,y) = tag centre. walk = phase (e.g. t*3) ->  | 183x113 |  |
| asset | `rank_podium` | `rank_podium(ctx, x, y, s=1.0, labels=('', 'VIETNAM', ''), ranks=(1, 2, 3), hl=Non` | Anchor: bottom-centre (block feet on y). 3 blocks ~420 wide at s=1. Block i sits left-to-r | 427x175 |  |
| asset | `ration_coupon` | `ration_coupon(ctx, x, y, s=1.0, rot=0.0, rows=(('RICE', '13 kg'), ('PORK', '0.5 kg'` | Coupon sheet (centre x,y). Signature: cream paper, perforated grid of stubs, item + ration | 307x349 |  |
| asset | `rd_center` | `rd_center(ctx, x, y, s=1.0, label='R&D CENTER')` | Anchor: bottom-centre. Modern glass building ~380x320: tall main block + lower wing, curta | 403x357 |  |
| asset | `rice_bowl` | `rice_bowl(ctx, x, y, s=1.0, fill_=1.0)` | Small bowl with a heap of rice (fill_ 0..1), (x,y) = bottom centre. Use for 'grams of rice | 155x101 |  |
| asset | `rice_heap` | `rice_heap(ctx, x, y, s=1.0)` | Heap of white rice, (x,y) = bottom centre. ~300 wide x ~165 tall mound drawn as hundreds o | 349x149 |  |
| asset | `rice_sack` | `rice_sack(ctx, x, y, s=1.0, label='RICE')` | Burlap sack, (x,y) = bottom centre. Tied neck, stitched seam, grains spilling. | 204x188 |  |
| asset | `road_sign` | `road_sign(ctx, x, y, s=1.0, text='BAC NINH 30 km', **kv)` | Anchor: bottom-centre (post feet at y). Green highway sign ~328x122 panel on two steel pos | 331x313 |  |
| asset | `rrect` | `rrect(ctx, x, y, w, h, r)` |  | 0x0 | needs args: w,h,r |
| asset | `rubber_stamp` | `rubber_stamp(ctx, x, y, s=1.0)` | Office rubber stamp, (x,y) = bottom centre of the rubber face. Wooden knob handle + block  | 135x158 |  |
| asset | `sea` | `sea(ctx, y, t=0.0)` | Anchor: full width, from y to the bottom of the frame. Two blue tones (lighter top, deeper | 0x0 | needs args:  |
| asset | `sewing_machine` | `sewing_machine(ctx, x, y, s=1.0, **kv)` | Anchor: bottom-centre. 200x140 classic industrial sewing machine at s=1: heavy bed, tall c | 236x157 |  |
| asset | `shop_front` | `shop_front(ctx, x, y, s=1.0, closed=0.0, label='PHO', **kv)` | Anchor: bottom-centre. 300x300 tube-house shopfront at s=1: living quarters above (grilled | 319x347 |  |
| asset | `skyline` | `skyline(ctx, y, night=False, t=0.0)` | Anchor: full width, bottom at y. 12 towers of varied heights in 3 tones (base / mid / shad | 1176x487 |  |
| asset | `smartphone` | `smartphone(ctx, x, y, s=1.0, rot=0.0, side='front', label=None)` | Anchor: centre. 120x240 at s=1. Front: rounded black body, thin bezel, punch-hole camera,  | 125x243 |  |
| asset | `smartwatch` | `smartwatch(ctx, x, y, s=1.0)` | Anchor: centre. Square rounded face (~92x92) showing time digits, orange silicone strap ab | 105x227 |  |
| asset | `smile_curve` | `smile_curve(ctx, x, y, w=820, h=420, progress=1.0, labels=('R&D', 'DESIGN', 'ASSE` | Smile-curve chart, (x,y) = top-left of the chart area. Axes with arrowheads and 'VALUE' on | 627x207 |  |
| asset | `smoke` | `smoke(ctx, x, y, t, size=60, seed=1)` | puff cloud: t in 0..1 lifetime. | 0x0 |  |
| asset | `smooth` | `smooth(ctx, pts, start=True)` | Catmull-Rom spline through pts (continues current path unless start). | 0x0 | needs args:  |
| asset | `sneaker` | `sneaker(ctx, x, y, s=1.0, **kv)` | Anchor: centre. Side-view trainer ~270x150 at s=1 facing right: thick white sole with toe  | 265x116 |  |
| asset | `solar_panel` | `solar_panel(ctx, x, y, s=1.0, **kv)` | Anchor: bottom-centre. Ground-mounted PV array ~340 wide at s=1: tilted panel with alumini | 337x252 |  |
| asset | `stamp_mark` | `stamp_mark(ctx, x, y, text='MADE IN VIETNAM', s=1.0, rot=-0.12)` | Anchor: centre. Rectangular rubber-stamp impression in red ink: double border, bold letter | 465x161 |  |
| asset | `state_cap` | `state_cap(ctx, x, y, R, f=0.0)` | Olive peaked cap (state employee). No badge/insignia. | 0x0 | needs args: R |
| asset | `state_counter` | `state_counter(ctx, x, y, w=520)` | State store counter: wooden counter top at y, iron grille window above, sign plain text. C | 523x513 |  |
| asset | `sticky` | `sticky(ctx, x, y, s, rot=-0.05, c=(1.0, 0.8901960784313725, 0.43137254901960` |  | 0x0 | needs args: s |
| asset | `stone_mill` | `stone_mill(ctx, x, y, s=1.0, ang=0.0, pole_dir=1)` | Hand rice-grinding mill (side view). (x,y) = bottom centre. Two stone cylinders (wide base | 509x233 |  |
| asset | `tablet` | `tablet(ctx, x, y, s=1.0, rot=0.0)` | Anchor: centre. ~260x190 landscape, dark body, bezel, front camera dot, colourful home scr | 263x193 |  |
| asset | `tariff_wall` | `tariff_wall(ctx, x, y, w=600, h=360, label='25% TARIFF', build=1.0)` | Brick wall in running bond, (x,y) = bottom centre. Rows (30px) are laid bottom->top as bui | 605x363 |  |
| asset | `text` | `text(ctx, s, x, y, size=48, c=(1, 1, 1), anchor='c', reveal=1.0, rot=0, ou` | handwritten text; reveal 0..1 = typewriter. | 0x0 | needs args: y |
| asset | `toque` | `toque(ctx, x, y, R)` | Chef's hat: band + puffy top. | 0x0 | needs args: R |
| asset | `trophy` | `trophy(ctx, x, y, s=1.0, **kv)` | Anchor: centre. Gold cup ~190x230 at s=1: wide rim ellipse, U bowl with highlight arc and  | 197x162 |  |
| asset | `tv_screen` | `tv_screen(ctx, x, y, s=1.0, headline='VIETNAM EXPORTS SOAR', **kv)` | Anchor: centre. TV set ~532x330 at s=1: dark bezel with sheen strip + neck/pedestal stand; | 535x337 |  |
| asset | `ussr_pillar` | `ussr_pillar(ctx, x, y, h=460, crumble=0.0, t=0.0, label='USSR')` | Tall grey stone column of stacked blocks, (x,y) = bottom centre. Plain 'USSR' lettering, n | 193x463 |  |
| asset | `vault_door` | `vault_door(ctx, x, y, s=1.0, open_=0.0, **kv)` | Anchor: centre. Round steel vault r=200 at s=1: concrete wall ring with rivets + side keyp | 411x405 |  |
| asset | `vietnam_map` | `vietnam_map(ctx, x, y, h, c=(0.9137254901960784, 0.7254901960784313, 0.2862745098` | S-shaped silhouette with shadow edge. cracks 0..1 grows 3 jagged cracks. Bounding box ~0.4 | 0x0 | needs args: h |
| asset | `wafer` | `wafer(ctx, x, y, s=1.0, **kv)` | Anchor: centre. Silicon wafer r=110 at s=1: disc with a chisel flat edge (bottom), metalli | 223x205 |  |
| asset | `whiteboard` | `whiteboard(ctx, x, y, s=1.0, lines=(), at=(), t=0.0, **kv)` | Anchor: centre (board middle). 420x320 board at s=1: aluminium frame, white tray with eras | 443x371 |  |
| bg | `air_cargo` | `air_cargo(ctx, t=0.0, **kv)` | cargo apron: pale sky, hangar, control tower, tarmac with painted guide lines. | 1279x719 |  |
| bg | `assembly_hall` | `assembly_hall(ctx, t=0.0, **kv)` | Factory hall in one-point perspective: converging workstation rows, ceiling lights, lane l | 1279x719 |  |
| bg | `beijing_1978` | `beijing_1978(ctx, t=0.0, **kv)` | wide avenue, bicycles, grey Soviet-style blocks; no gate, no emblems. | 1279x719 |  |
| bg | `border` | `border(ctx, t=0.0, **kv)` | border checkpoint: road through a gate arch, hills behind, flag-free signs. | 1279x719 |  |
| bg | `boxing_ring` | `boxing_ring(ctx, t=0.0, **kv)` | Boxing ring: crowd silhouettes with camera flashes, flat translucent spotlight cones, corn | 1279x719 |  |
| bg | `casino_table` | `casino_table(ctx, t=0.0, **kv)` | green felt table seen from above-front, wood rail, chips stacked at the edges. | 1279x719 |  |
| bg | `city` | `city(ctx, t=0.0, night=False)` |  | 1279x719 |  |
| bg | `classroom` | `classroom(ctx, t=0.0, **kv)` | Classroom: green chalkboard with plain chalk text, rows of wooden desks, sunny window, glo | 1279x683 |  |
| bg | `cleanroom` | `cleanroom(ctx, t=0.0, **kv)` | Semiconductor fab: yellow-tinted light, white panels, overhead rails with carriage, wafer  | 1279x719 |  |
| bg | `congress` | `congress(ctx, t=0.0, banner='6TH NATIONAL CONGRESS  ·  1986')` | Full-frame party congress hall. Anchor: whole canvas. Deep red curtain with 3-tone vertica | 1279x719 |  |
| bg | `construction` | `construction(ctx, t=0.0, **kv)` | Construction site: corrugated fence with plain sign, rising steel frame, 2 tower cranes (j | 1279x719 |  |
| bg | `coop_yard` | `coop_yard(ctx, t=0.0, **kv)` | Dusty collective yard: work-points chalk board on posts, horn loudspeaker on a pole, stack | 1279x719 |  |
| bg | `dark` | `dark(ctx)` |  | 1279x719 |  |
| bg | `design_studio` | `design_studio(ctx, t=0.0, **kv)` | bright studio desk with drawing tablets on stands, pinned sketches on the wall. | 1279x631 |  |
| bg | `drone_view` | `drone_view(ctx, t=0.0, **kv)` | top-down: patchwork fields, a river, a highway ribbon. | 1279x719 |  |
| bg | `embassy` | `embassy(ctx, t=0.0, **kv)` | formal reception hall: columns, dark red curtains, plain gold-trim banner. | 1279x719 |  |
| bg | `engine_room` | `engine_room(ctx, t=0.0, **kv)` | pipes, valves, big boiler, dim light; ground y=640. | 1279x719 |  |
| bg | `expo_hall` | `expo_hall(ctx, t=0.0, **kv)` | trade expo: booths with flag-free banners along the back. | 1279x719 |  |
| bg | `factory` | `factory(ctx)` |  | 1279x719 |  |
| bg | `factory_gate` | `factory_gate(ctx, t=0.0, **kv)` | factory entrance: gatehouse, boom barrier posts (trucks/queue drawn by fn), fence, crowd d | 1279x719 |  |
| bg | `flat` | `flat(ctx, c='#e9e1cf')` |  | 1279x719 |  |
| bg | `foxconn_campus` | `foxconn_campus(ctx, t=0.0, **kv)` | Aerial 3/4 campus: identical long blue-grey factory blocks receding, dorm towers, gate wit | 1279x719 |  |
| bg | `garment_hall` | `garment_hall(ctx, t=0.0, **kv)` | sewing hall: long tables with machine silhouettes, thread spools, fabric rolls. | 1279x719 |  |
| bg | `globe_space` | `globe_space(ctx, t=0.0, **kv)` | Deep-blue starfield: deterministic twinkling dots, two soft constellations, a few larger s | 1279x719 |  |
| bg | `government_hall` | `government_hall(ctx, t=0.0, **kv)` | columns + plain deep-blue wall band, flag-free. | 1279x719 |  |
| bg | `hanoi_1986` | `hanoi_1986(ctx, t=0.0, **kv)` | 1986 Hanoi street: faded ochre tube houses, closed shutters, tangled wires, bicycles, plai | 1279x719 |  |
| bg | `hanoi_street_1990` | `hanoi_street_1990(ctx, t=0.0, **kv)` | 1990 Hanoi street: same grammar as 1986 but brighter, more shutters rolled up, a couple of | 1279x719 |  |
| bg | `hanoi_today` | `hanoi_today(ctx, t=0.0, **kv)` | Today's Hanoi: bright shophouses with generic signs, glass towers behind, motorbike stream | 1279x719 |  |
| bg | `harvest_gold` | `harvest_gold(ctx, t=0.0, **kv)` | golden ripe field with sheaves. | 1279x719 |  |
| bg | `harvest_poor` | `harvest_poor(ctx, t=0.0, **kv)` | sparse brown field, dry cracks. | 1279x719 |  |
| bg | `kitchen` | `kitchen(ctx, t=0.0)` | Full-frame restaurant kitchen. Anchor: whole canvas. White tile wall (60px grid, y 0-520), | 1279x719 |  |
| bg | `kitchen_wall` | `kitchen_wall(ctx, t=0.0, **kv)` | kitchen wall closeup: tiles, shelf with jars, hanging pans; ground y=620. | 1279x719 |  |
| bg | `lab` | `lab(ctx, t=0.0, **kv)` | R&D lab: white benches, monitors facing their benches (backs to camera; one angled showing | 1279x719 |  |
| bg | `market` | `market(ctx, t=0.0, **kv)` | Open-air market: striped parasols, stall tables with produce baskets, rice sacks, hanging  | 1279x719 |  |
| bg | `meeting_room` | `meeting_room(ctx, t=0.0, **kv)` | Boardroom: long table front edge y=600, dark wall screen showing screen= text, city window | 1279x708 |  |
| bg | `newsroom` | `newsroom(ctx, t=0.0, **kv)` | TV studio: anchor desk front edge y=600, blue backdrop with generic dotted world map, tick | 1279x719 |  |
| bg | `night` | `night(ctx, t=0.0)` |  | 1279x719 |  |
| bg | `night_city` | `night_city(ctx, t=0.0, **kv)` | night skyline with lit windows; deep blue, reads as a city at night. | 1279x719 |  |
| bg | `north_vn_hills` | `north_vn_hills(ctx, t=0.0, **kv)` | layered karst hills with mist bands; ground y=620. | 1279x719 |  |
| bg | `office` | `office(ctx, wall='#dfe3e6')` |  | 1279x719 |  |
| bg | `office_1980s` | `office_1980s(ctx, t=0.0, **kv)` | grey filing cabinets, rotary phone, desk lamp, beige wall calendar; ground y=620. | 1279x719 |  |
| bg | `paddy` | `paddy(ctx, t=0.0)` |  | 1279x719 |  |
| bg | `port` | `port(ctx, t=0.0)` |  | 1279x719 |  |
| bg | `port_day` | `port_day(ctx, t=0.0, **kv)` | Day port: quay edge, 4-colour container stacks, 2 gantry cranes, water with wave lines. | 1279x719 |  |
| bg | `port_night` | `port_night(ctx, t=0.0, **kv)` | Night port: navy sky, moon, crane lights, water reflections. | 1279x719 |  |
| bg | `race_track` | `race_track(ctx, t=0.0, **kv)` | speedway: banked curve, start line, grandstand, warm sunset sky. | 1279x719 |  |
| bg | `renovation` | `renovation(ctx, t=0.0, **kv)` | scaffolding on an old house, fresh paint buckets, ladders; ground y=640. | 1279x719 |  |
| bg | `rice_to_factory` | `rice_to_factory(ctx, t=0.0, **kv)` | left half: ripe rice field; right half: graded factory site with stakes. | 1279x719 |  |
| bg | `room` | `room(ctx, wall='#e9e1cf', floor='#b98a5e')` |  | 1279x719 |  |
| bg | `ruins` | `ruins(ctx, t=0.0, **kv)` | silhouetted broken walls, smoke columns, dim orange sky. No gore. | 1279x719 |  |
| bg | `samsung_campus` | `samsung_campus(ctx, t=0.0, **kv)` | campus of long blocks with blue roofs, plain SAMSUNG band on the main hall. | 1279x719 |  |
| bg | `samsung_hall` | `samsung_hall(ctx, t=0.0, **kv)` | Samsung-flavoured assembly hall: white/blue palette, blue wall band reading SAMSUNG (plain | 1279x718 |  |
| bg | `sea_lanes` | `sea_lanes(ctx, t=0.0, **kv)` | open sea top-down-ish: deep blue water, dotted shipping lanes, small islands. | 1279x719 |  |
| bg | `seoul_hq` | `seoul_hq(ctx, t=0.0, **kv)` | glass HQ tower with the plain word SAMSUNG; day skyline behind. | 1279x719 |  |
| bg | `signing_table` | `signing_table(ctx, t=0.0, **kv)` | long polished table with pens and folders; two chairs behind. | 1279x719 |  |
| bg | `sky` | `sky(ctx, sky='#bfe3ef', ground='#8cc46f', horizon=560)` |  | 1279x719 |  |
| bg | `small_workshop` | `small_workshop(ctx, t=0.0, **kv)` | garage workshop: roller door, workbench with tools, shelves with parts bins. | 1279x719 |  |
| bg | `split2` | `split2(ctx, t=0.0, **kv)` | Vertical split: left half left= colour, right half right= colour, white jagged divider, fl | 1219x719 |  |
| bg | `state_store` | `state_store(ctx, t=0.0, **kv)` | 1986 state store: mostly EMPTY shelves with a few lone tins, ration poster in plain text,  | 1279x719 |  |
| bg | `sunrise` | `sunrise(ctx, t=0.0, **kv)` | Layered hills at dawn: flat warm sky bands, a sun that rises with t, still bird silhouette | 1279x719 |  |
| bg | `trophy_stage` | `trophy_stage(ctx, t=0.0, **kv)` | awards stage: steps, curtains, spotlight cones (flat), plain banner. | 1279x719 |  |
| bg | `vault` | `vault(ctx, t=0.0, **kv)` | steel vault room: riveted plate walls, floor grate, cold light panel. | 1279x719 |  |
| bg | `vhs_rewind` | `vhs_rewind(ctx, t=0.0, **kv)` | VHS rewind look: dark frame, horizontal static stripes drifting, corner PLAY marker. | 1279x719 |  |
| bg | `warehouse` | `warehouse(ctx, t=0.0, **kv)` | Warehouse: tall racking full of cartons (loops), yellow forklift, floor lane markings. | 1279x719 |  |
| bg | `white_studio` | `white_studio(ctx, t=0.0, **kv)` | Seamless white cyclorama: flat wall, soft grey floor-shadow bands, one flat light band at  | 1279x663 |  |
| cast | `banker` | `p banker x y [scale]` | puppet | 205x435 |  |
| cast | `bunny` | `p bunny x y [scale]` | puppet | 231x451 |  |
| cast | `chef` | `p chef x y [scale]` | puppet | 205x486 |  |
| cast | `clerk` | `p clerk x y [scale]` | puppet | 205x435 |  |
| cast | `cn_official` | `p cn_official x y [scale]` | puppet | 205x458 |  |
| cast | `customer` | `p customer x y [scale]` | puppet | 205x444 |  |
| cast | `editor` | `p editor x y [scale]` | puppet | 205x420 |  |
| cast | `exec` | `p exec x y [scale]` | puppet | 205x435 |  |
| cast | `exec2` | `p exec2 x y [scale]` | puppet | 205x458 |  |
| cast | `farmer` | `p farmer x y [scale]` | puppet | 265x469 |  |
| cast | `kid` | `p kid x y [scale]` | puppet | 162x352 |  |
| cast | `lan` | `p lan x y [scale]` | puppet | 234x453 |  |
| cast | `minh` | `p minh x y [scale]` | puppet | 205x446 |  |
| cast | `mother` | `p mother x y [scale]` | puppet | 265x469 |  |
| cast | `official` | `p official x y [scale]` | puppet | 205x458 |  |
| cast | `official2` | `p official2 x y [scale]` | puppet | 205x420 |  |
| cast | `us_official` | `p us_official x y [scale]` | puppet | 205x458 |  |
| cast | `worker` | `p worker x y [scale]` | puppet | 205x453 |  |
| cast | `worker_m` | `p worker_m x y [scale]` | puppet | 205x446 |  |
