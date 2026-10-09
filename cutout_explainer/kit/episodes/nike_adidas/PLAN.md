# Nike vs Adidas, "The Sneaker War": plan (director, Sonnet 5.5)
Audio: 5 TTS parts joined with 0.3 s gaps into `narration.wav`, 339.96 s. Word timings from the user's Whisper transcripts (`words.json`). Shots: 97, median 3.4 s (1.4-6.5 s), cuts hand-fixed to clause boundaries in `segs.json`.
Script fixes made in words.json (timing untouched): "Audie" -> "Adi", "Herzogenarach" -> "Herzogenaurach", "OnRunning" -> "On Running".
**Check by ear before building:** Act I audio says "Audie Dassler" for Adi Dassler (S28, about 99.5 s). If it really sounds like that, regenerate the line.
Act cards: the parts follow each other with no pause, so there are no black chapter cards. Each act starts with a typewriter marker top-left instead (S19, S40, S59, S80).

## 1. Chapters
| ch | shots | time | mood | music bed |
|---|---|---|---|---|
| Cold open | S01-S18 | 0:00-1:09 | rejection, then a gamble that pays off, then the war set-up | music_tension (S01-S08), music_upbeat (S09-S14), music_tension (S15-S18) |
| Act I: the split | S19-S39 | 1:09-2:15 | craft and two origin stories | music_reflective |
| Act II: asset-light | S40-S58 | 2:15-3:15 | confident, clever, money | music_upbeat |
| Act III: two mistakes | S59-S79 | 3:15-4:34 | things go wrong | music_somber (S59-S72), music_tension (S73-S79) |
| Act IV: the new war | S80-S97 | 4:34-5:40 | balance, tension, open ending | music_tension (S80-S90), music_hopeful (S91-S97) |

## 2. Motifs that recur
- **Left = Oregon / Nike (orange), right = Bavaria / Adidas (black + blue-white lozenge).** Every time both appear, the sides stay the same. Brand colour only, never a logo. Orange + dark forest green for Oregon; sky blue + white + black for Bavaria.
- **The duel pair** (orange court sneaker left, blue terrace sneaker right, on `split2`): planted S19, paid off S81 (two fronts) and S94-S95. Torn paper = feud/split.
- **Two engines** (`engine_block` orange vs blue): planted S16 ("two corporate engines"), paid off S94 with the $160B counter.
- **The shoe shelf** (`shoe_shelf`, `fill` 0..1): S64 shrinks, S68 empties, S69 the upstarts fill it, S91-S92 Nike reclaims it. The shelf is the Act III-IV storyline.
- **The shoebox pile** (`box_pile`): Nike glut S71, bigger Adidas glut S78 (the $1B), shrinks S93.
- **The handshake** (`handshake`): Nike cuts ties S62 (vanishes in a puff), repaired S92.
- **The collab pillar** (`ussr_pillar` relabelled "COLLABS"): Adidas leans on it S73, it crumbles S77.
- **Stamps** `stamp_mark`: DECLINED (S07), country stamps (S44-S46).
- **The $ counters** (`cnt`): $500,000 S10, $6.6B S12, $160B S14 and S94, $1.3B S75, 15% S76, $1B S78.

## 3. Backgrounds budget (97 shots, cap 7 each)
| bg | shots | n |
|---|---|---|
| bg_herzogenaurach (NEW) | S07 S18 S21 S25 S27 S57 | 6 |
| bg_oregon (NEW) | S09 S10 S17 S48 | 4 |
| bg_track_field (NEW) | S32 S33 S87 S88 S89 | 5 |
| office | S01 S02 S08 S53 S58 S62 S92 | 7 |
| signing_table | S04 S11 S50 | 3 |
| white_studio | S03 S06 S51 S72 S74 S96 | 6 |
| classroom | S05 S35 | 2 |
| split2 | S19 S26 S36 S37 S81 S94 S95 | 7 |
| flat (tinted; peach S12, cream others) | S12 S20 S38 S39 S43 S52 S54 | 7 |
| sky | S13 S15 S31 S63 S76 S82 S83 | 7 |
| city | S14 S49 S56 S75 S80 | 5 |
| room | S64 S68 S69 S84 S85 S91 | 6 |
| kitchen_wall (neutral tile wall) | S22 S23 S61 | 3 |
| small_workshop | S24 S28 S29 | 3 |
| lab | S30 S90 | 2 |
| factory_gate | S34 | 1 |
| sunrise | S40 S66 S97 | 3 |
| construction | S41 S42 | 2 |
| assembly_hall / garment_hall | S44 / S45 | 1 + 1 |
| port_day | S46 S59 | 2 |
| design_studio | S47 S65 | 2 |
| expo_hall | S55 S73 S86 | 3 |
| harvest_poor (bare ground) | S60 S67 S70 S79 | 4 |
| engine_room | S16 | 1 |
| warehouse | S71 S78 S93 | 3 |
| newsroom | S77 | 1 |
Never use `meeting_room`, `government_hall`, `embassy`, `samsung_*`, `seoul_hq`, `foxconn_campus` (baked Vietnam/Samsung text or brand). No dark spotlight backgrounds and no maps or ships (the `globe` in S13 is the only world picture and stays small and flat; Asian countries are stamps, not a map).

## 4. Key shots the director writes by hand (`key.py`, 12 shots = 12%)
S01 (hook: the tape), S03 (Jordan reveal), S12 ($6.6B register), S16 (two engines), S25 (town split by the river), S36+S37 (design here, outsource there, one split2 pair), S43 (zero factories), S67 (backfire), S77 (pillar collapse), S78 ($1B pile), S94 (engines return with $160B).
Everything else = one scene-language line each, written by Haiku builders from the shot table below.

## 5. Sound plan
Pop on pop-ins is automatic. Explicit: `stamp` on S07, S44-S46; `coins` S10 S11; `cash_register` S12; `typewriter_tick` on every `tx`; `stone_crumble` + shake S77; `thud` + shake S67; `page_flip` S22; `camera_shutter` S74 (celebrity collab); `soft_whoosh_out` on the vanishing puffs (S57, S62, S63, S86); `coins` S55. Ambience per bg is automatic.

## 6. Motion (each moving shot and the narration word that names it)
Camera: slow push on realizations, pull on summaries (default), none otherwise. Nothing else moves unless listed:
- Counters (`cnt`): S10 "$500,000", S12 "$6.6", S14 "$160", S66 "60%", S75 "$1.3", S76 "15%", S78 "$1", S94 "$160".
- Vanish with puff: S57 factory @abandon, S62 handshake @cut, S63 three shop fronts @terminating, S86 "HYPE" @destroying, S39 the first sign @later.
- Shelf `fill`: S64 1->0.25 @reducing, S68 1->0 @pulling, S69 0->1 @upstarts (runner shoes arrive), S91 0.2->0.8 @return, S92 0.5->1 @reclaim.
- Pile `n`: S93 14->3 @liquidation.
- Bars rise: S53 @skyrocketed, S66 @capture (margin bars), S70 bars fall @slowed.
- Pillar crumble 0->1: S77 @collapsed.
- Shake: S67 @backfired, S77 @collapsed (both are impacts).
Not moving, on purpose: all people, the plane in S31 (static), the ribbon signs, the cow, the stamps' country labels.

## 7. People (only where the script makes them relevant)
| shots | who | why |
|---|---|---|
| S01 S07 S08 | exec2 (German executive) | executives get the tape, decline, prefer tall centers |
| S03 S04 S06 S50 | jordan (NEW) | he is the story; wants to sign; loves the brand; signs with Nike |
| S21 S23 S25 S26 S28 | adi + rudi (NEW) | the feud, the split, Adi the engineer |
| S32 S33 S35 | knight + bowerman (NEW) | the founders; Knight writes the paper |
| S62 | exec (Nike executive) | the cut-ties decision |
| S74 | celebrity (NEW, generic, no real person) | script: celebrity collabs |
| S89 | knight rig as a runner, holding a runner shoe | "hardcore runners" |
Everyone else = objects. Two people share a shot only in S21, S23, S25, S26, S33 (all described in the script).
New cast: jordan, adi, rudi, knight, bowerman, celebrity. Director builds them (`assets.py`: bald + red jersey "23" for Jordan; side-parted dark hair + glasses + work coat for Adi; heavier face + moustache + work apron for Rudi; thin, headband, green singlet for Knight; cap + glasses + clipboard for Bowerman). No real logos on any of them.

## 8. Shot table (97 lines; builders turn each into one scene-language line; key shots are code)
Format: id | bg | what is on screen (pop-in word) | camera. Nike things left/orange, Adidas things right/blue.
### Cold open
- S01 KEY | office | exec2 holds `videotape` @videotape; tx "GERMANY - 1984" | push
- S02 | office | big `crt` with `basketball` on its screen, `videotape` beside; kw "ROOKIE GUARD" @rookie | push
- S03 KEY | white_studio | jordan, basketball under arm, e=happy; kw "MICHAEL JORDAN" @Michael | push
- S04 | signing_table | jordan seated at the table, pen over a `paper` "CONTRACT"; kw "SIGN" @sign | still
- S05 | classroom | big white `sneaker_lowtop`; tx "HIGH SCHOOL" @high; kw "THEIR SHOES" @shoes | push
- S06 | white_studio | jordan holds the same sneaker (hold_front), e=happy; kw "LOVED IT" @loved | push
- S07 | bg_herzogenaurach | exec2 e=angry shrug; `stamp_mark` "DECLINED" @down; tx "HERZOGENAURACH" @Herzogenaurach | still
- S08 | office | exec2 point_R at a `whiteboard` with two `bars` (GUARD short, CENTER tall); kw "TALLER" @taller | push
- S09 | bg_oregon | small `shop_front` s=0.7 label "SHOES"; tx "OREGON" @Oregon; kw "SMALL AND SCRAPPY" @scrappy | push
- S10 | bg_oregon | `money_bag` + `cnt` $500,000 @$500,000; `st` "DESPERATE" @desperate | still
- S11 | signing_table | `paper` "ROYALTY" left, coins pop @royalties; `sneaker_hightop` right (red/black) @Air; kw "AIR JORDAN" @Jordan | still
- S12 KEY | flat peach | big `cash_register`, `sneaker_hightop` on top, `cnt` $6.6B; sfx cash_register | push
- S13 | sky | small flat `globe`; kw "HISTORY" @history | pull
- S14 | city | two `money_bag` (orange left, black right), tx NIKE / ADIDAS, `cnt` $160B between them @$160 | pull
- S15 | sky | `billboard` (plain slogan "BE BOLD") + `tv_screen` headline "GOING VIRAL"; kw "GLITZY" @glitzy | still
- S16 KEY | engine_room | `engine_block` orange left vs blue right facing each other; kw "WAR" @war | pull
- S17 | bg_oregon | `rd_center` + tx "BEAVERTON, OREGON"; kw "ASSET-LIGHT" @asset-light | push
- S18 | bg_herzogenaurach | `factory` (blue) ; tx "BAVARIA, GERMANY"; kw "PRECISION" @precision | push
### Act I
- S19 | split2 | tx "ACT I - OREGON vs BAVARIA"; `sneaker_lowtop` orange left, `sneaker_terrace` blue right pop @Nike @Adidas | still
- S20 | flat cream | same two shoes small; kw "BORN" @born | push
- S21 | bg_herzogenaurach | adi + rudi face each other, e=angry; kw "FAMILY FEUD" @feud | push
- S22 | kitchen_wall | `calendar` top "1948"; kw "TWO BROTHERS" @brothers; sfx page_flip | still
- S23 | kitchen_wall | adi left, rudi right facing, e=happy; tx "ADI" "RUDI" @Adi @Rudi | still
- S24 | small_workshop | `cobbler_bench`; kw "COBBLING" @cobbling; `money_bag` small @successful | push
- S25 KEY | bg_herzogenaurach | river down the middle; adi on left bank, rudi on right, backs turned, e=angry; kw "SPLIT" @split | pull
- S26 | split2 | adi left with sign tx "ADIDAS"; rudi right with sign tx "PUMA" (red) @Adidas @Puma | still
- S27 | bg_herzogenaurach | `factory` (1950s); kw "CRAFTSMANSHIP" @craftsmanship | pull
- S28 | small_workshop | adi alone holds `football_boot` (hold_front), e=determined; kw "ENGINEER" @engineer | push
- S29 | small_workshop | big `football_boot` + brown `paper` swatch; kw "LEATHER" @leather | push
- S30 | lab | `football_boot` with arrows to its studs; kw "SCREW-IN CLEATS" @screw-in; tx "BIOMECHANICS" @biomechanics | still
- S31 | sky | `cargo_plane` small in the sky; tx "1964" @1964 (the Atlantic is only said, not drawn) | pan
- S32 | bg_track_field | knight on the track, e=determined; tx "UNIVERSITY OF OREGON"; kw "PHIL KNIGHT" @Phil | push
- S33 | bg_track_field | knight left, bowerman right facing each other; kw "BILL BOWERMAN" @Bill | still
- S34 | factory_gate | `factory` + falling `bill` pops; kw "TOO EXPENSIVE" @expensive | push
- S35 | classroom | knight at a desk writing on a `paper` (type_R); kw "RADICAL IDEA" @radical | push
- S36 KEY | split2 | left: shoe blueprint `paper` + tx "AMERICA" @America; kw "?" | still
- S37 KEY | split2 | same left; right: `assembly_line` + `factory_modern` + tx "ASIA" @Asian; `arrow` left to right; cnt "100%" @100% | still
- S38 | flat cream | `ribbon_sign` "BLUE RIBBON SPORTS" (blue) @Blue | push
- S39 | flat cream | the first sign vanishes with a puff @later; `ribbon_sign` "NIKE" (orange board, plain letters) @Nike | push
### Act II
- S40 | sunrise | tx "ACT II - THE ASSET-LIGHT REVOLUTION"; orange `sneaker_lowtop`; kw "OUTSOURCING" @outsourcing | push
- S41 | construction | `chained_bag` left + `factory` right; kw "BILLIONS" @billions | push
- S42 | construction | `assembly_line` (machinery) + `st` "REAL ESTATE" @real | pull
- S43 KEY | flat cream | `empty_lot`; huge kw "ZERO" @zero; cnt "0" | push
- S44 | assembly_hall | `stamp_mark` "MADE IN JAPAN" @Japan; sfx stamp | push
- S45 | garment_hall | `stamp_mark` "SOUTH KOREA" left @Korea, "TAIWAN" right @Taiwan | still
- S46 | port_day | `stamp_mark` "VIETNAM" @Vietnam, "INDONESIA" @Indonesia | still
- S47 | design_studio | `money_bag` + cnt "100%" @100%; kw "TWO THINGS" @two | push
- S48 | bg_oregon | `rd_center` + `microscope` + `circuit_board`; kw "R&D" @R&D | push
- S49 | city | `billboard` + `tv_screen` "NEW DROP"; kw "EMOTIONAL" @emotional | push
- S50 | signing_table | jordan signs a `paper`; tx "1984" | push
- S51 | white_studio | `sneaker_hightop` + `basketball`; kw "NOT JUST SHOES" @shoes | push
- S52 | flat cream | three `sneaker_hightop` colourways pop one per word; kw "STATUS" @status, "IDENTITY" @identity, "REBELLION" @rebellion | still
- S53 | office | `bars` rise (5 bars) + `arrow` up + tx "ROCE"; kw "SKYROCKETED" @skyrocketed | push
- S54 | flat cream | `factory_modern` greyed; huge kw "$0" @$0; tx "MAINTENANCE" @maintenance | still
- S55 | expo_hall | big orange `money_bag` vs small black one + `trophy`; kw "OUTBIDDING" @outbidding; sfx coins | pull
- S56 | city | `billboard` + `tv_screen` + `trophy`; pops @athletes, @advertising | pull
- S57 | bg_herzogenaurach | the blue `factory` vanishes with a puff @abandon; kw "ABANDON" | still
- S58 | office | `whiteboard` with play lines "MADE IN ASIA"; kw "SURVIVE" @survive | push
### Act III
- S59 | port_day | tx "ACT III - TWO MISCALCULATIONS"; orange + blue `container`, `cargo_truck`, `port_crane` | pull
- S60 | harvest_poor | two `pit_trap` (labels "MISTAKE 1", "MISTAKE 2"); kw "CATASTROPHIC" @catastrophic | push
- S61 | kitchen_wall | `shop_app` + `laptop`; kw "DTC" @DTC; tx "DIRECT-TO-CONSUMER" | push
- S62 | office | exec (Nike) e=determined; `handshake` (orange sleeve, grey) vanishes with a puff @cut | push
- S63 | sky | three small `shop_front` (labels KICKS, SOLE, SNEAKERS) vanish with puffs @terminating | still
- S64 | room | `shoe_shelf` fill 1->0.25 @reducing; tx "FOOT LOCKER" on a plain sign | push
- S65 | design_studio | `shop_app` + `laptop` (screen "SHOP"); kw "OWN APPS" @apps | push
- S66 | sunrise | margin `bars` rise; cnt "60%+" @60%; kw "GROSS MARGINS" @gross | push
- S67 KEY | harvest_poor | `pit_trap` "DTC" with the orange `sneaker_lowtop` tipped at its edge; kw "BACKFIRED" @backfired; shake | push
- S68 | room | `shoe_shelf` fill 1->0 @pulling; tx "WHOLESALE" | still
- S69 | room | same shelf fills with `sneaker_runner_stack` + `sneaker_runner_pods` @upstarts; tx "ON RUNNING" "HOKA" @On @Hoka | still
- S70 | harvest_poor | falling `bars` @slowed; tx "POST-2022" | push
- S71 | warehouse | `box_pile` (orange boxes); kw "INVENTORY GLUT" @gluts | pull
- S72 | white_studio | the same pile + `sale_badge` "-50%" @discounts | push
- S73 | expo_hall | `ussr_pillar` labelled "COLLABS" propping a blue `factory_modern` with tx "ADIDAS"; kw "DEPENDENCY" @dependency | push
- S74 | white_studio | celebrity (sunglasses) + a collab `sneaker_terrace` on a pedestal; kw "CELEBRITY COLLABS" @celebrity; sfx camera_shutter | push
- S75 | city | cnt "$1.3B" @$1.3; kw "ANNUAL SALES" @annual | still
- S76 | sky | one `bars` pair [15, 85] + cnt "15%" @15% | still
- S77 KEY | newsroom | the pillar crumbles @collapsed; `tv_screen` "CONTROVERSY"; shake | push
- S78 KEY | warehouse | very large blue `box_pile` + cnt "$1B" @$1; kw "UNSELLABLE" @unsellable | pull
- S79 | harvest_poor | `calendar` "30 YEARS" + red `arrow` down; kw "FIRST LOSS" @first | push
### Act IV
- S80 | city | tx "ACT IV - THE NEW WAR"; the duel pair again, small; kw "TODAY" @today | push
- S81 | split2 | left retro `sneaker_lowtop`, right `sneaker_runner_stack`; tx "RETRO" / "PERFORMANCE"; kw "DUAL-FRONT" @dual-front | still
- S82 | sky | `cash_cow`; kw "RETRO CASH COW" @cow | push
- S83 | sky | cow + a `sneaker_lowtop` and `sneaker_terrace` beside it; kw "STEADY CASH FLOW" @steady | pull
- S84 | room | `sneaker_lowtop` (Dunk-style panda), `sneaker_lowtop` (all white), `sneaker_hightop`; tx "DUNK" "AIR FORCE 1" "JORDAN 1" | still
- S85 | room (blue wall) | `sneaker_terrace` x2 (Samba-style, Gazelle-style) + `sneaker_lowtop` grey; tx names | still
- S86 | expo_hall | full `shoe_shelf` ; kw "HYPE" vanishes with a puff @destroying | push
- S87 | bg_track_field | `sneaker_runner_stack` pops; kw "THREAT" @threat | push
- S88 | bg_track_field | three runner shoes with name tags HOKA, ON, ASICS @Hoka @On @Asics | still
- S89 | bg_track_field | knight rig as a runner, holds `sneaker_runner_pods`; kw "STEALING" @stealing | push
- S90 | lab | big `sneaker_runner_stack` cutaway: black carbon plate + foam layers, arrows; tx "CARBON PLATE" "SUPER FOAM" | push
- S91 | room | `shoe_shelf` fill 0.2->0.8 @return; tx "WHOLESALE" | push
- S92 | office | `handshake` (orange sleeve) pops @repairing; `shoe_shelf` behind fill 0.5->1 @reclaim | push
- S93 | warehouse | `box_pile` n 14->3 @liquidation; `sale_badge`; kw "LEAN TURNAROUND" @lean | pull
- S94 KEY | split2 | the two `engine_block`s again, cnt "$160B" between @$160; kw "OREGON MARKETING" left, "BAVARIAN ENGINEERING" right | pull
- S95 | split2 | hightop orange + terrace blue; `stamp_mark` "NOT THE POINT" @longer | still
- S96 | white_studio | `balance_scale`; `container` on the left pan @supply; kw "AGILITY" @agility | push
- S97 | sunrise | same scale; `handshake` on the left pan @relationships, `microscope` on the right pan @innovation; hold to the end | pull

## New assets
Brand rule for every card: no marks, no stripes, no swoosh, no wings. Colours come in as keyword arguments. Sneakers: side view, toe to the right, `flip=True` mirrors them.
- videotape | VHS cassette seen from the front | 220x140 px | black rectangular shell with rounded corners; two white reel hubs behind a clear window; paper label strip on the front, blank ruled lines; ridged lower edge with a door flap; notch for the write-protect tab
- basketball | a basketball | 130x130 px | orange sphere; one vertical and one horizontal black seam; two curved side seams; subtle dimple dots made with a loop; highlight crescent top-left | banned=nike|adidas|puma
- sneaker_lowtop | a low-cut court sneaker (the classic leather cupsole kind) | 420x230 px | thick cupsole with side wall and stitch ridge; perforated toe box made with a dot loop; padded collar and tongue visible; five eyelets and crossed laces; panel overlays (toe cap, side panel, heel counter) in a second colour; heel tab; accepts body, accent, sole colours and flip | banned=nike|adidas|puma|swoosh|trefoil|jordan|converse
- sneaker_hightop | a high-top basketball sneaker (1985 style) | 380x300 px | collar rising above the ankle with padded rim; ankle strap with hook; seven eyelets; layered panels (toe, mid, heel) in two colours; perforated toe; chunky cupsole; accepts body, accent, sole colours and flip | banned=nike|adidas|puma|swoosh|jordan|jumpman|wings|converse
- sneaker_terrace | a slim low terrace-style suede sneaker | 420x220 px | slim gum-rubber sole in caramel with a thin white sidewall line; T-shaped toe overlay; suede mudguard at the toe; flat laces and thin tongue; contrast heel tab; low profile; accepts body, accent colours and flip | banned=nike|adidas|puma|samba|gazelle|trefoil|stripes
- sneaker_runner_stack | a maximal-cushion road running shoe | 440x260 px | tall stacked midsole, at least 45% of shoe height; rocker curve at toe and a bevelled heel; breathable mesh upper drawn with a dot grid; plain heel pull tab; neat laces; accepts body, accent, sole colours, flip, and cutaway=True which shows a black carbon plate line inside layered foam | banned=hoka|asics|on|nike|adidas|swoosh
- sneaker_runner_pods | a lightweight road running shoe with a slotted sole | 440x250 px | midsole with a row of 7 rounded horizontal slots (pods); sleek mesh upper; speed laces and a stretch cord; rubber outsole pattern at the bottom edge; heel pull tab; accepts colours and flip | banned=hoka|asics|on|nike|adidas|cloud
- football_boot | a 1950s leather screw-in-stud football boot | 400x260 px | leather upper, ankle-low cut; six screw-in studs under the sole (three front, three rear) with visible thread rings; lace cover flap with fringed tongue; stitch lines along the sole; sturdy toe cap; no logo | banned=adidas|puma|nike|stripes
- shoe_box | a cardboard shoebox with a lid | 260x160 px | lid overhanging the base; two visible faces for a 3D look; colour band on the lid (param); blank rectangular end label; tissue paper edge peeking out; corner stitching lines | banned=nike|adidas|puma|swoosh
- box_pile | a heap of shoeboxes | 460x360 px | accepts n=15 boxes stacked in a loose pyramid with uneven offsets; two or three band colours (params); a few boxes tilted; lids slightly open on two; one toppled box at the foot; shadow under the pile | banned=nike|adidas|puma
- shoe_shelf | a retail wall display with three shelves | 600x420 px | wood-framed back panel; three staggered ledges; accepts fill 0..1 (share of the 10 shoe slots occupied; slots fill from the top shelf down); each slot has a pedestal peg and a tiny price tag; a plain header sign slot with text param; floor shadow | banned=nike|adidas|puma|footlocker
- shop_app | a phone showing a shoe-shop product page | 300x560 px | portrait smartphone with rounded corners and notch; product image area with a simple sneaker blob; three colour swatch dots; row of size chips; wide rounded BUY button (the word BUY is allowed); cart icon with a number badge; accepts accent colour | banned=nike|adidas|swoosh
- cobbler_bench | a shoemaker's workbench | 520x300 px | wooden bench with thick legs; an iron shoe last on a stand with a half-finished boot; hammer; awl; leather roll and scraps; wall rack with a row of wooden lasts above; apron hook
- ribbon_sign | a wooden shop sign with an award rosette | 380x300 px | board on two posts with wood grain lines; blue award rosette (round ribbon with two tails and a gold centre) at the left corner; text param centred on the board (plain letters, any colour); chain hangers; accepts board colour | banned=nike|swoosh
- empty_lot | an empty industrial lot | 560x300 px | cracked concrete pad; chain-link fence drawn with a diamond loop and posts; open gate; weed tufts; light pole; blank rectangular sign board on a post; no building, nothing standing
- chained_bag | a money bag bound with chain | 340x320 px | tied-neck money bag with a $ sign; heavy chain wrapped twice diagonally (links as alternating ovals); padlock at the front centre; rope at the neck; soft shading on the bulge
- billboard | a roadside advertising billboard | 560x420 px | large framed board with a plain slogan text param; row of six lamps on a top bar; two steel posts with a catwalk and railing; ladder on the side; ground shadow; accepts board colour | banned=nike|adidas|swoosh|justdoit
- sale_badge | a retail sale starburst | 220x220 px | red 16-point starburst with white outline; white word SALE in handwriting; percent text param; slight rotation; second inner ring
- cash_cow | a cartoon dairy cow standing in profile | 460x340 px | black-and-white patches with two patches shaped like dollar signs; pink udder with four teats; gold coin hung as a bell on the neck; tail tuft; small horns; a milk pail beside her overflowing with gold coins
- cash_register | a vintage mechanical cash register | 380x320 px | brass body with a grid of round keys (4 rows); display window with a $ sign; open drawer with bills and coins; curly scroll at the top; receipt strip hanging out of the top
- balance_scale | a classic two-pan balance | 560x400 px | central pillar with a stepped base; horizontal beam with a triangle fulcrum on top; two chains to two shallow pans; tilt param (0 = level); function exposes pan centres in a comment so items can sit on them; small tick scale on the pillar
- engine_block | a four-cylinder car engine | 420x320 px | cast block body in a colour param; valve cover with ridges on top; four spark plugs with wires; front pulley with a belt; two exhaust manifold pipes; bolts drawn with a loop

## Proposed learnings (go to the user at the end of the job)
See STATE.md once cards and checks have run.
