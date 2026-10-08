# Batch B01: qwen builds S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S13

### S02 · 0:01.84–0:03.86 (2.02 s) · builder: qwen
**Narration:** "the average citizen in Vietnam earned"  
**Word times (s from shot start):** average 0.04, citizen 0.52, Vietnam 1.18, earned 1.56  
**Visual:** Wide countryside. The farmer stands in the paddy, left of centre. A yellow sticky 'AVERAGE CITIZEN' pops beside his head on 'citizen'. The gold map pops on the right on 'Vietnam', with the keyword 'VIETNAM' under it.  
**Staging:** bg_paddy(ctx,t). farmer = vcast('farmer',1.0) at waist (430,640), facing 0.25, expr 'neutral', pose('down'). Sticky: sticky(ctx,215,215,'AVERAGE\nCITIZEN',size=34) via popped() at 0.52 (sticky must not touch his hat or face). Map: vietnam_map(ctx,0,0,360) via popped() at (940,290) at 1.18; keyword(ctx,t,1.28,'VIETNAM',940,520,56).  
**Camera:** push_in 1.00-1.06 centred (640,360)  
**Text:** sticky "AVERAGE CITIZEN" @ 0.52; keyword "VIETNAM" @ 1.28  
**SFX (auto-mixed from shots.json; time your pops to match):** wind_ambience 0.00 (-20 dB), pop 0.52 (-4 dB), pop 1.18 (-2 dB), pop 1.28 (-6 dB)  
**Assets:** bg_paddy, vcast farmer, vietnam_map, sticky, keyword  
**CHECKS:**
- [ ] farmer wears the non la hat (comes with vcast); hat sits on his head
- [ ] map is the vietnam_map asset (S-shape), not a redrawn shape
- [ ] sticky pops at 0.52 and map at 1.18 (+-0.1 s), each with a smoke puff
- [ ] no text over the face; nothing important below y=630

### S03 · 0:03.86–0:06.96 (3.10 s) · builder: qwen
**Narration:** "less than $90 a year."  
**Word times (s from shot start):** less 0.00, than 0.30, $90 0.58, a 1.20, year 1.96  
**Visual:** Medium close-up of the sad farmer holding out one open hand. On '$90' three small coins land in his palm and a big '$90' keyword pops. On 'year' a tear-off calendar reading '1 YEAR' pops on the right.  
**Staging:** bg_paddy(ctx,t). farmer = vcast('farmer',1.5) at waist (360,900), legs=False, facing 0.5, expr 'sad'. armR = arm_to(p,360,900,1,(600,560)), armL = pose('down')[0]. Coins: coin() r=18 at (590,548),(612,542),(600,530), each popped at 0.58/0.66/0.74, resting on the hand. Keyword '$90' at (860,200) size 84 at 0.58. calendar(ctx,0,0,0.85,top='1986',big='1 YEAR') via popped() at (1030,440) at 1.96.  
**Camera:** push_in 1.00-1.08 centred (600,450)  
**Text:** keyword "$90" @ 0.58; prop "1 YEAR calendar" @ 1.96  
**SFX (auto-mixed from shots.json; time your pops to match):** wind_ambience 0.00 (-22 dB), coins 0.58 (-8 dB), pop 0.58 (-3 dB), pop 1.96 (-3 dB)  
**Assets:** vcast farmer, coin, calendar, keyword  
**CHECKS:**
- [ ] the coins sit ON the open right hand (hand touches the coins); no coin floats
- [ ] '$90' appears at 0.58 +-0.1 s, the calendar at 1.96 +-0.1 s
- [ ] the calendar reads '1 YEAR' with '1986' on its red header
- [ ] expression is sad; text does not overlap the face or hat

### S04 · 0:06.96–0:10.12 (3.16 s) · builder: qwen
**Narration:** "More than 70% of the entire population lived in"  
**Word times (s from shot start):** More 0.00, 70 0.30, % 0.86, entire 1.44, population 1.94, lived 2.66  
**Visual:** Number shot. A row of 10 small people on a pale wall. A counter ticks 0 to 70% at the top. A dark grey 'poverty' zone then sweeps in behind the left 7, who turn sad. The right 3 stay neutral in the light.  
**Staging:** bg_flat(ctx,hexc('#e9e1cf')), floor box from y=560 colour #d7cdb6. 10 puppets, scale 0.42, waists at y=520, x = 130 + i*113 (i=0..9), cycling vcast farmer, mother, kid; all facing 0. Zone: box(ctx,60,150,w,440,hexc('#5a5560'),r=16) drawn BEFORE the puppets, w = lerp(0,770,ease_io((t-1.0)/0.9)), so it covers people 0-6 only. People 0-6 use expr 'sad' once the zone edge has passed their x, else 'neutral'. Counter: text(ctx, f'{n}%', 640, 95, 84, outline=INK), n = int(70*clamp((t-0.30)/0.56)), shown from 0.30.  
**Camera:** pull_out 1.06-1.00  
**Text:** number "70%" @ 0.30  
**SFX (auto-mixed from shots.json; time your pops to match):** typewriter_tick 0.34 (-8 dB), typewriter_tick 0.46 (-8 dB), typewriter_tick 0.58 (-8 dB), typewriter_tick 0.70 (-8 dB), pop 0.86 (-2 dB), whoosh 1.00 (-6 dB)  
**Assets:** vcast farmer/mother/kid, keyword  
**CHECKS:**
- [ ] exactly 10 people standing on the same baseline; hats on the adults
- [ ] the counter ends exactly at '70%' by 0.86 s and stays
- [ ] the zone covers exactly 7 people (left); 3 on the right stay outside it, in the light
- [ ] the 7 inside are sad, the 3 outside neutral; the counter text does not overlap any head

### S05 · 0:10.12–0:13.18 (3.06 s) · builder: qwen
**Narration:** "extreme, grinding poverty."  
**Word times (s from shot start):** extreme 0.00, grinding 0.94, poverty 1.56  
**Visual:** Metaphor: the tired farmer pushes the pole of a huge stone mill that never stops turning, at dusk. 'GRINDING' pops on its word, then 'POVERTY' under it.  
**Staging:** bg_paddy(ctx,t) then a dusk overlay box(0,0,W,H,(0.15,0.1,0.2)) at alpha 0.30 (use ctx.set_source_rgba + rectangle fill). end = stone_mill(ctx,520,640,1.0,ang=t*1.6,pole_dir=1). farmer = vcast('farmer',0.85) at waist (end[0]+75, 610), facing -0.7, expr 'tired', walk=t*1.4, armL=arm_to(p,x,610,-1,end), armR=arm_to(p,x,610,1,(end[0]+14,end[1]+8)), cross=True. Recompute x from end EVERY frame so the hands stay on the pole. keyword 'GRINDING' at (330,140) size 72 at 0.94; keyword 'POVERTY' at (330,215) size 72 at 1.56.  
**Camera:** push_in 1.00-1.10 centred (620,430)  
**Text:** keyword "GRINDING" @ 0.94; keyword "POVERTY" @ 1.56  
**SFX (auto-mixed from shots.json; time your pops to match):** wind_ambience 0.00 (-18 dB), thud 0.00 (-14 dB), pop 0.94 (-3 dB), pop 1.56 (-3 dB)  
**Assets:** bg_paddy, stone_mill, vcast farmer, arm_to, keyword  
**CHECKS:**
- [ ] both hands touch the pole end in every frame (no gap as the pole swings)
- [ ] the pole joins the top stone; the stone grooves visibly move between frames
- [ ] the farmer is tired and faces the mill (facing -0.7)
- [ ] the words pop on time (0.94 / 1.56); neither overlaps the farmer's head or hat

### S06 · 0:13.18–0:15.50 (2.32 s) · builder: qwen
**Narration:** "Ration coupons dictated how many grams of"  
**Word times (s from shot start):** Ration 0.00, coupons 0.22, dictated 0.66, how 1.16, grams 1.74  
**Visual:** Close-up on a ration book lying on a table. A rubber stamp slams down on it ('dictated'), leaves the purple STATE STORE mark and lifts away. On 'grams' a yellow sticky 'grams?' pops.  
**Staging:** bg_flat #e9e1cf; table top box(0,520,W,200,#a8703f) with an ink line at y=520. ration_coupon(ctx,0,0,1.1,rot=-0.04,stamped=S) via popped() at (600,330) at 0.22, where S = 0 before 0.80, then clamp((t-0.80)/0.25). Stamp: rubber_stamp(ctx,736,y,1.0), y = lerp(-60,402,ease_in) over 0.62-0.80 (bottom edge of the stamp lands on the coupon at the stamp mark), holds 0.80-0.95, rises back to -60 over 0.95-1.30. sticky(ctx,1030,190,'grams?',rot=0.06) via popped() at 1.74.  
**Camera:** push_in 1.00-1.08 centred (620,340)  
**Text:** sticky "grams?" @ 1.74  
**SFX (auto-mixed from shots.json; time your pops to match):** office_hum 0.00 (-22 dB), paper_rustle 0.22 (-8 dB), pop 0.22 (-4 dB), whoosh_short 0.62 (-8 dB), stamp 0.80 (0 dB), pop 1.74 (-4 dB)  
**Assets:** ration_coupon, rubber_stamp, sticky  
**CHECKS:**
- [ ] the stamp mark is absent before 0.80 and appears exactly when the stamp face touches the paper
- [ ] the stamp is gone (off the top) by 1.30; the coupon rows 'RICE 13 kg' etc. are readable
- [ ] the coupon rests on the table (no floating)
- [ ] the sticky pops at 1.74 +-0.1 s

### S07 · 0:15.50–0:17.54 (2.04 s) · builder: qwen
**Narration:** "rice, pork, or kerosene"  
**Word times (s from shot start):** rice 0.00, pork 0.86, kerosene 1.40  
**Visual:** State store counter. Each ration pops onto the counter on its word: rice sack, pork, kerosene lantern. Each has a paper tag on the counter front with its monthly amount.  
**Staging:** bg_flat #e9e1cf; state_counter(ctx,640,470,w=1040) (top surface y=456, sign at top). Items sitting ON the counter top: rice_sack(ctx,0,0,0.8) popped at (330,456) at 0.05; pork(ctx,0,0,0.8) popped at (640,418) at 0.86; kerosene_lamp(ctx,0,0,0.8,t=t) popped at (950,456) at 1.40. Tags: paper(ctx,x-75,517,150,46,lines_=0,label=...) with label 'RICE 13 kg' / 'PORK 0.5 kg' / 'KEROSENE 1 L', size 26, centred at x=330/640/950, y=540, popped together with their item.  
**Camera:** static (zoom 1.0)  
**Text:** tag "RICE 13 kg" @ 0.05; tag "PORK 0.5 kg" @ 0.86; tag "KEROSENE 1 L" @ 1.40  
**SFX (auto-mixed from shots.json; time your pops to match):** office_hum 0.00 (-22 dB), pop 0.05 (-3 dB), pop 0.86 (-3 dB), pop 1.40 (-3 dB)  
**Assets:** state_counter, rice_sack, pork, kerosene_lamp, paper  
**CHECKS:**
- [ ] all three items rest on the counter top (bottom edges at y about 456), none floating
- [ ] each item pops on its word (0.05 / 0.86 / 1.40, +-0.1 s)
- [ ] the tags read RICE 13 kg, PORK 0.5 kg, KEROSENE 1 L, all fully on screen
- [ ] the 'STATE STORE' sign is visible and not cut off

### S08 · 0:17.54–0:20.04 (2.50 s) · builder: qwen
**Narration:** "a family could receive each month."  
**Word times (s from shot start):** a 0.00, family 0.20, receive 0.62, each 1.02, month 1.32  
**Visual:** A family of three faces the store counter. The mother holds out the ration book. The clerk slides one tiny bowl of rice onto the counter. A wall calendar 'MONTH' pops and its page tears away.  
**Staging:** bg_room(ctx,wall=hexc('#e9e1cf')). Draw order: calendar, clerk, counter, family. clerk = vcast('clerk',0.9) at waist (930,470), legs=False, facing -0.6, expr 'smug'; then state_counter(ctx,930,470,w=520), drawn AFTER the clerk so it hides his lower body. Family on the left, all facing +0.6, expr 'tired': farmer (0.95) waist (150,600); mother (0.95) waist (300,600); kid (0.95) waist (440,615). Mother's right hand: armR = arm_to(p,300,600,1,(560,430)); ration_coupon(ctx,575,430,0.28) drawn at that hand. rice_bowl(ctx,0,0,0.6,fill_=0.35) popped at (760,456) at 0.62 (it sits on the counter top). calendar(ctx,0,0,0.65,top='1986',big='MONTH',flip=F) popped at (640,165) at 1.02; F = clamp((t-1.32)/0.4).  
**Camera:** static (zoom 1.0)  
**Text:** prop "MONTH calendar" @ 1.02  
**SFX (auto-mixed from shots.json; time your pops to match):** office_hum 0.00 (-22 dB), pop 0.62 (-4 dB), pop 1.02 (-4 dB), page_flip 1.32 (-4 dB)  
**Assets:** state_counter, vcast family+clerk, ration_coupon, rice_bowl, calendar, arm_to  
**CHECKS:**
- [ ] the family faces right toward the counter, the clerk faces left toward them
- [ ] the clerk's legs are NOT visible through or below the counter
- [ ] the mother's hand touches the ration book; the bowl rests on the counter
- [ ] the calendar pops at 1.02 and its page tears at 1.32; it covers no face or hat

### S09 · 0:20.04–0:24.38 (4.34 s) · builder: qwen
**Narration:** "Inflation was running at a staggering 587%,"  
**Word times (s from shot start):** Inflation 0.00, running 0.68, staggering 1.36, 587% 1.98  
**Visual:** Metaphor: a rice price tag with legs runs up a steep jagged price line that draws itself. Its price climbs fast. On '587%' a huge '587%' slams in with a camera shake.  
**Staging:** bg_dark(ctx). Price line: a jagged polyline from (120,600) to (1120,140) with 9 points (alternating small dips), drawn progressively from 0.40 to 1.98 (k = clamp((t-0.4)/1.58)): line(ctx,pts_up_to_k,RED,9) over line(ctx,...,INK,15). Tag: price_tag(ctx,tip_x-40,tip_y-90,0.8,value=str(int(lerp(100,687,k))),walk=t*3.2) running on the line's tip from 0.68. Before 0.68 the tag stands still at the start (walk=None). After 1.98 the tag holds at the top. Keyword '587%' at (430,210) size 84 popped at 1.98. Shake: camera(...,shake=0.6*(1-(t-1.98)/0.4)) for 1.98-2.38 only.  
**Camera:** push_in 1.00-1.10 centred (700,320), plus a shake at 1.98-2.38  
**Text:** number "587%" @ 1.98  
**SFX (auto-mixed from shots.json; time your pops to match):** footsteps 0.68 (-8 dB), whoosh 0.70 (-8 dB), typewriter_tick 1.40 (-10 dB), typewriter_tick 1.55 (-10 dB), typewriter_tick 1.70 (-10 dB), typewriter_tick 1.85 (-10 dB), thud 1.98 (0 dB), pop 1.98 (-3 dB)  
**Assets:** price_tag, keyword, bg_dark  
**CHECKS:**
- [ ] the line draws progressively and the tag stays on its tip (feet on the line)
- [ ] the legs animate only while running (0.68-1.98)
- [ ] '587%' appears at 1.98 +-0.1 s; the shake lasts 0.4 s or less
- [ ] '587%' does not overlap the tag; nothing important below y=630

### S10 · 0:24.38–0:27.41 (3.03 s) · builder: qwen
**Narration:** "destroying the value of money overnight."  
**Word times (s from shot start):** destroying 0.00, value 1.12, money 1.54, overnight 1.82  
**Visual:** A big banknote in daylight shrinks, greys and curls. On 'overnight' the sky turns to night, a moon pops up and the note is left tiny and grey.  
**Staging:** Sky: bg_flat with colour lerp(hexc('#9fd8f0'), NIGHT, ease_io((t-1.82)/0.6)) per channel. dong_note(ctx,600,330,1.5,rot=-0.05,value='100',wither=clamp((t-0.1)/2.5)). Keyword 'VALUE' at (600,120) size 64 popped at 1.12. Moon: circle(ctx,1080,130,52,hexc('#f4eec8'),INK,3) popped at 1.82, plus 3 small stars (circle r 4, white) popped at 1.95/2.05/2.15. Keyword 'OVERNIGHT' at (600,560) size 64 popped at 1.90.  
**Camera:** push_in 1.00-1.06 centred (600,330)  
**Text:** keyword "VALUE" @ 1.12; keyword "OVERNIGHT" @ 1.90  
**SFX (auto-mixed from shots.json; time your pops to match):** whoosh_short 0.10 (-10 dB), paper_rustle 0.60 (-8 dB), pop 1.12 (-4 dB), sparkle 1.82 (-6 dB), pop 1.90 (-6 dB), night_crickets 2.00 (-18 dB)  
**Assets:** dong_note, keyword  
**CHECKS:**
- [ ] the note visibly smaller and greyer at 2.4 s than at 0.4 s (continuous)
- [ ] the note has no portrait, seal or emblem (use the asset as is)
- [ ] the sky stays day until 1.82, then goes dark; the moon pops at 1.82
- [ ] 'OVERNIGHT' sits above y=600 and does not overlap the note

### S11 · 0:27.41–0:31.98 (4.57 s) · builder: qwen
**Narration:** "The nation was devastated by 30 years of back-to-back conflicts,"  
**Word times (s from shot start):** nation 0.33, devastated 0.99, 30 2.05, years 2.43, back-to-back 2.99, conflicts 3.71  
**Visual:** The gold map of Vietnam under a spotlight. It cracks three times, on 'devastated', 'back-to-back' and 'conflicts', each with a jolt and a dust puff. A sticky '30 YEARS' pops on the right.  
**Staging:** bg_dark(ctx). vietnam_map(ctx,560,340,500,cracks=C). C = 1/3*clamp((t-0.99)/0.3) + 1/3*clamp((t-2.99)/0.3) + 1/3*clamp((t-3.71)/0.3). dust(ctx,x,y,t,start) at each crack start: (530,190)@0.99, (650,330)@2.99, (560,500)@3.71, n=4, size=50. Map pops in at 0.33 ('nation') with popped(). sticky(ctx,1010,230,'30 YEARS',rot=0.05,size=46) popped at 2.05.  
**Camera:** push_in 1.00-1.08 centred (600,340); shake 0.4 for 0.3 s at 0.99, 2.99 and 3.71  
**Text:** sticky "30 YEARS" @ 2.05  
**SFX (auto-mixed from shots.json; time your pops to match):** wind_ambience 0.00 (-18 dB), pop 0.33 (-4 dB), thud 0.99 (0 dB), retro_explosion 0.99 (-12 dB), pop 2.05 (-4 dB), thud 2.99 (0 dB), thud 3.71 (0 dB), retro_explosion 3.71 (-12 dB)  
**Assets:** vietnam_map, dust, sticky, bg_dark  
**CHECKS:**
- [ ] exactly 3 cracks, each appearing at its word (+-0.1 s), each with a dust puff
- [ ] the map is the asset S-shape (not redrawn) and fully on screen
- [ ] the sticky does not overlap the map
- [ ] each shake lasts 0.3 s or less

### S13 · 0:33.88–0:37.26 (3.38 s) · builder: qwen
**Narration:** "and isolated from the global financial system."  
**Word times (s from shot start):** isolated 0.42, global 1.40, financial 1.70, system 2.14  
**Visual:** Wide pull-out. The caged map sits alone on the left, with 'ISOLATED' above it. A globe pops on the right on 'global', and coins start circling it on 'financial'. The coins never reach the cage.  
**Staging:** bg_dark(ctx). caged_map(ctx,300,600,h=380) (same object as S12, smaller). keyword 'ISOLATED' at (300,130) size 64 at 0.42. globe(ctx,0,0,140,t) popped at (920,330) at 1.40. 6 coins from 1.70: coin(ctx,920+cos(a)*215, 330+sin(a)*120, 20), a = t*1.8 + i*1.047. Coin alpha/scale pops in at 1.70. Coins orbit only around the globe, never left of x=680.  
**Camera:** pull_out 1.15-1.00 centred from (300,380) to (640,360)  
**Text:** keyword "ISOLATED" @ 0.42  
**SFX (auto-mixed from shots.json; time your pops to match):** wind_ambience 0.00 (-18 dB), pop 0.42 (-4 dB), pop 1.40 (-3 dB), coins 1.70 (-8 dB), whoosh 1.75 (-10 dB)  
**Assets:** caged_map, globe, coin, keyword, bg_dark  
**CHECKS:**
- [ ] the cage and map look the same as in S12 (use caged_map; do not redraw)
- [ ] the globe pops at 1.40, the coins appear at 1.70 and orbit only around the globe
- [ ] 'ISOLATED' sits above the cage without touching it
- [ ] the camera ends at zoom 1.0 with both objects fully on screen
