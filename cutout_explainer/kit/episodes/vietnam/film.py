"""The whole film. One line per shot (see engine/scene.py for the mini-language); key shots are code in key.py.
   python3 engine/sheet.py episodes.vietnam.film sheet.jpg     |  SHOTS=S16,S17 ... to preview a subset
   python3 engine/build.py episodes.vietnam.film film.mp4"""
import sys, os, json; sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
from episodes.vietnam import film_setup            # fills the registries
from episodes.vietnam.key import SHOT_FNS as KEY
from scene import build_shots

L = {
# ---------------- Act 1a: 1986 (key shots S01 S12 S14 S15 are code) ----------------
"S02": 'bg paddy | cam push 1 1.06 | p farmer 430 640 1 f=0.25 | st "AVERAGE\\nCITIZEN" 215 215 34 @citizen | a vietnam_map 940 290 360 @Vietnam | kw VIETNAM 940 520 56 @Vietnam+0.1',
"S03": 'bg paddy | cam push 1 1.08 600 450 | p farmer 360 900 1.5 e=sad f=0.5 legs=0 handR=600,560 | a coin 596 548 18 @$90 | a coin 618 540 18 @$90+0.08 | a coin 604 528 18 @$90+0.16 | sfx coins @$90 db=-8 | kw "$90" 860 200 84 @$90 | a calendar 1030 440 0.85 top=1986 big="1 YEAR" @year',
"S04": 'cam pull 1.06 1.0 | fn zone | sfx whoosh @entire-0.3 db=-6 | sfx pop @70+0.56 db=-2',
"S05": 'bg paddy | cam push 1 1.1 620 430 | fn mill | kw GRINDING 330 140 72 @grinding | kw POVERTY 330 215 72 @poverty',
"S06": 'bg flat c=#e9e1cf | cam push 1 1.08 620 340 | fn stamp | st "grams?" 1030 190 rot=0.06 @grams | sfx paper_rustle @coupons db=-8 | sfx pop @coupons db=-4 | sfx whoosh_short @dictated db=-8 | sfx stamp @dictated+0.14 db=0',
"S07": 'bg flat c=#e9e1cf | cam still | a state_counter 640 470 w=1040 | a rice_sack 330 456 0.8 @rice | a pork 640 418 0.8 @pork | a kerosene_lamp 950 456 0.8 @kerosene | a paper 330 540 150 46 lines_=0 label="RICE 13 kg" size=26 @rice | a paper 640 540 150 46 lines_=0 label="PORK 0.5 kg" size=26 @pork | a paper 950 540 150 46 lines_=0 label="KEROSENE 1 L" size=26 @kerosene',
"S08": 'bg room wall=#e9e1cf | cam still | a calendar 640 165 0.65 top=1986 big=MONTH flip=0>1:@month:0.4 @each | p clerk 930 470 0.9 f=-0.6 e=smug legs=0 | a state_counter 930 470 w=520 | p farmer 150 600 0.95 f=0.6 e=tired | p mother 300 600 0.95 f=0.6 e=tired handR=560,430 | p kid 440 615 0.95 f=0.6 e=tired | a ration_coupon 575 430 0.28 | a rice_bowl 760 456 0.6 fill_=0.35 @receive | sfx page_flip @month db=-4',
"S09": 'bg dark | cam push 1 1.1 700 320 | fn priceline | kw "587%" 430 210 84 @587 | shake @587 amp=0.6 | sfx footsteps @running db=-8',
"S10": 'bg flat c=#9fd8f0 | cam push 1 1.06 600 330 | fn dusk at=@overnight | a dong_note 600 330 1.5 rot=-0.05 wither=0>1:@0.1:2.5 | kw VALUE 600 120 64 @value | a circle 1080 130 52 c=#f4eec8 @overnight | kw OVERNIGHT 600 560 64 @overnight+0.08 | sfx sparkle @overnight | sfx night_crickets @overnight+0.2 db=-18 | sfx paper_rustle @0.6 db=-8',
"S11": 'bg dark | cam push 1 1.08 600 340 | fn cracks | st "30 YEARS" 1010 230 46 rot=0.05 @30 | shake @devastated amp=0.4 | shake @back amp=0.4 | shake @conflicts amp=0.4 | sfx retro_explosion @devastated db=-12 | sfx retro_explosion @conflicts db=-12 | sfx pop @nation db=-4',
"S13": 'bg dark | cam pull 1.15 1.0 300 380 640 360 | a caged_map 300 600 380 | kw ISOLATED 300 130 64 @isolated | a globe 920 330 140 @global | fn orbit | sfx coins @financial db=-8',
# ---------------- Act 1b: today, the questions, the rewind ----------------
"S16": 'bg city | sfx whoosh @Fast db=-4 | kw TODAY 640 110 84 @today | a vietnam_map 640 390 380 @nation',
"S17": 'bg dark | a smartphone 170 330 1.0 @smartphone | bars 330 560 700 380 vals=[10,6] labels=["CHINA","VIETNAM"] fmt="" hl=1 @second | kw "No. 2 ON EARTH" 900 100 60 @Earth',
"S18": 'bg port | cam pan | a container_ship 640 520 0.9 label="VIETNAM" | a sea 520 | cnt 0 683 640 140 96 fmt="${:,}B" @$683 dur=1.2',
"S19": 'bg dark | bars 200 560 880 340 vals=[3,5,4,6,7,9,8,10,12] labels=[1,2,3,4,5,6,7,8,9] fmt="" c=#5fae5a @surplus | kw "SURPLUS" 640 110 72 @massive | st "9 YEARS\\nIN A ROW" 1110 200 36 @nine',
"S20": 'bg dark | fn pie x=420 y=320 r=170 frac=0.5 at=@50 label="50%" | a smartphone 900 320 1.4 side=back @Samsung | tx SAMSUNG 900 560 48 @Samsung',
"S21": 'bg flat c=#e9e1cf | a smartphone 640 330 1.8 side=back | st "NEW YORK" 220 200 @New | st TOKYO 1060 200 @Tokyo | a stamp_mark 640 400 text="MADE IN VIETNAM" s=1.2 @made | sfx stamp @made db=0 | shake @made amp=0.3',
"S22": 'bg dark | a caged_map 400 600 380 | kw WAR-TORN 400 110 60 @war | kw ISOLATED 400 180 60 @isolated | kw "?" 960 330 150 @transform',
"S23": 'bg flat c=#20303a | fn asia labels=False pins=[["VIETNAM",105.8,16,"@favorite"]] arrows=[[106,21,121.5,31.2,"@node","#e9b949"],[106.7,10.8,139.7,35.7,"@global","#e9b949"],[106,21,127,37.5,"@supply","#e9b949"],[106.7,10.8,103.8,1.3,"@chains","#e9b949"]] | kw FAVORITE 1140 250 56 @favorite | kw NODE 1140 320 56 @node',
"S24": 'bg flat c=#e9e1cf | a ration_coupon 300 330 0.85 @ration | arrow 520 330 700 330 @to | a assembly_phones 740 470 470 side=front @assembling',
"S25": 'bg dark | a chip 400 330 1.3 label=ELECTRONICS @sophisticated | a calendar 900 340 0.9 top="1986 - 2024" big="< 40 YRS" @four',
"S26": 'bg dark | a vietnam_map 220 500 200 | arrow 300 520 1080 160 c=#5fae5a lw=16 dur=1.2 @executed | kw COMEBACK 640 110 72 @comebacks',
"S27": 'bg dark | cam pull | sfx whoosh @rewind db=-4 | tx "<< REWIND" 60 70 48 anchor=l @rewind | a calendar 640 340 1.4 top=DECEMBER big=1986 @1986',
"S28": 'bg congress | tx "HANOI  ·  DEC 1986" 60 160 44 anchor=l @Hanoi',
"S29": 'bg congress | p official 640 560 1 e=determined | a podium 640 660 1 | kw "CHANGE EVERYTHING" 640 250 64 @change',
"S30": 'bg dark | a vietnam_map 640 360 520 cracks=0>1:@total:0.9 | kw COLLAPSE 1000 200 72 @collapse | shake @collapse',
# ---------------- Chapter 1: the broken engine ----------------
"S31": 'card 1975 sub="Chapter 1  ·  The Broken Engine"',
"S32": 'bg dark | a vietnam_map 360 360 480 | a ussr_pillar 900 640 400 @Soviet | kw SOVIET-STYLE 900 120 60 @Soviet',
"S33": 'bg office | p official 300 600 1 f=0.5 e=smug pose=point_R | a paper 560 300 240 300 label="CENTRAL PLAN" size=30 @planning | a padlock 900 360 1.2 label=CLOSED @outlawed | kw "PRIVATE BUSINESS" 900 120 52 @private',
"S34": 'bg sky | a coop_farm 820 560 0.9 @collective | p mother 80 600 0.7 walk=45 f=0.7 e=sad | p farmer 200 600 0.7 walk=45 f=0.7 e=sad | p farmer 320 600 0.7 walk=45 f=0.7 e=sad | kw MILLIONS 300 110 64 @millions',
"S35": 'bg dark | a rice_bowl 640 470 1.6 fill_=0 @result | kw DISASTER 640 160 84 @disaster | shake @catastrophic amp=0.4',
"S36": 'bg paddy | p farmer 420 640 1.1 e=tired f=0.3 pose=shrug | kw "$0" 820 200 84 @zero | st "EXTRA\\nCROPS?" 920 420 40 @extra',
"S37": 'bg paddy | p clerk 980 600 1 f=-0.6 e=smug pose=hips | a rice_sack 380 600 0.9 move=420,0:@confiscated:0.8 | a price_tag 640 230 1.0 value="1" @rock | kw ROCK-BOTTOM 640 100 60 @rock',
"S38": 'bg dark | bars 300 560 680 360 vals=[10,7,4,2] labels=["","","",""] fmt="" c=#e9e1cf @collapsed | kw "RICE PRODUCTION" 640 100 60 @Rice | kw COLLAPSED 1060 260 56 @collapsed',
"S39": 'bg port | a container_ship 1100 520 0.6 label=GRAIN move=-520,0:@import:2.0 | a sea 520 | kw IMPORT 640 110 72 @import | st "TO PREVENT\\nSTARVATION" 280 230 34 @starvation',
"S40": 'bg office | tx "LATE 1986" 60 70 48 anchor=l @1986 | p official 400 600 1 e=worried f=0.6 pose=think_R | p official2 760 600 1 f=-0.6 e=worried @realized',
"S41": 'bg dark | fn gauge x=640 y=430 r=230 at=@fuel label=ECONOMY | kw EMPTY 640 110 72 @completely',
"S42": 'bg congress | cam pull 1.12 1.0',
"S43": 'bg congress | p official 640 560 1 e=determined pose=down pose2=raise_both@Doi | a podium 640 660 1 | kw "DOI MOI" 1010 260 84 @Doi | sfx sparkle @Doi db=-6',
"S44": 'bg dark | kw "DOI MOI" 640 200 84 | arrow 640 260 640 370 @translates | kw "= RENOVATION" 640 450 72 @renovation',
"S45": 'bg flat c=#ffe9a8 | tx "II  PAUSE" 60 70 48 anchor=l @pause | p kid 380 620 1.2 e=happy f=0.4 | st "EXPLAIN LIKE\\nI\'M 5" 860 260 40 @ELI',
"S46": 'bg kitchen | p chef 380 600 1 f=0.6 e=worried | p clerk 860 600 1 f=-0.6 e=smug pose=point_L @manager | st "BUY ONLY:\\nRICE" 1060 160 36 @ingredients',
"S47": 'bg kitchen | a price_board 560 280 1.3 locked=1 @price | p clerk 1050 600 0.9 f=-0.6 e=smug',
"S48": 'bg kitchen | p chef 260 600 1 e=angry f=0.6 | p clerk 820 600 1 f=-0.6 e=smug | a money_bag 480 470 0.8 label=100% move=300,0:@takes+0.3:0.7 | kw "100%" 520 120 72 @100 | st "NO-SHOWS\\nGET PAID" 1110 220 34 @show',
"S49": 'bg kitchen | p chef 160 600 0.9 e=tired f=0.5 | a dish 420 520 1.2 state=rotten @rots | p customer 860 600 1 f=0.7 e=angry walk=140 @customers',
"S50": 'bg kitchen | p chef 360 600 1 e=happy f=0.5 | a money_bag 600 470 0.8 label=YOURS @profits | a dish 900 520 1 @extra | kw "KEEP THE PROFITS" 640 110 64 @keep',
"S51": 'bg kitchen | a price_board 360 280 1.1 @prices | p chef 680 600 0.9 e=happy f=0.3 pose=point_L | a rice_sack 960 520 0.8 label=MARKET @ingredients',
"S52": 'bg room wall=#efe3cc | a open_doors 900 600 w=360 h=460 open_=0>1:@open:0.8 label=FOREIGN | p exec 520 600 0.9 f=0.6 e=happy @foreign | kw "FOREIGN SUPPLIERS" 420 110 56 @foreign | sfx door_close @open db=-8',
"S53": 'bg room wall=#efe3cc | a open_doors 900 600 w=360 h=460 open_=1 label=FOREIGN | p exec 520 600 0.9 f=0.6 e=happy walk=70 | kw DUTY-FREE 360 160 72 @duty',
"S54": 'bg sky | a coop_farm 640 560 1 out@dismantled | shake @dismantled amp=0.3 | p farmer 400 600 0.9 e=happy @dismantled+0.4 | p mother 880 600 0.9 e=happy f=-0.3 @dismantled+0.55 | kw DISMANTLED 640 110 72 @dismantled',
"S55": 'bg paddy | p farmer 330 640 1 f=0.6 e=happy handR=560,430 | a land_deed 600 400 0.8 @land | p mother 820 640 1 f=-0.5 e=happy | p kid 960 650 0.9 f=-0.5 e=happy @families',
"S56": 'bg paddy | a rice_heap 640 640 1.4 @exploded | kw EXPLODED 640 120 72 @exploded | shake @exploded amp=0.3 | sfx sparkle @exploded db=-6',
"S57": 'bg port | cam pan | a container_ship 640 520 0.8 label=RICE | a sea 520 | kw "No. 3 RICE EXPORTER" 640 110 60 @third | st "IN 3\\nYEARS" 1100 250 40 @years',
"S58": 'bg room wall=#f2d9a6 | a price_board 640 240 1.0 @legalized | p mother 360 600 1 e=happy f=0.4 | p customer 900 600 1 e=happy f=-0.5 @businesses | st OPEN! 1080 140 @small',
"S59": 'bg dark | a price_board 330 330 0.9 locked=1 out@abolished+0.3 | a price_board 330 330 0.9 @abolished+0.4 | a price_tag 900 330 1.0 value="100" @stabilized | kw STABLE 900 480 56 @stabilized | kw "MOST IMPORTANTLY..." 640 600 48 @importantly',
"S60": 'bg sky | a open_doors 640 600 w=460 h=540 open_=0>1:@open:0.8 label=FDI | kw "FOREIGN DIRECT INVESTMENT" 640 60 52 @Foreign | sfx door_close @open db=-8',
"S61": 'bg flat c=#20303a | fn asia labels=False pins=[["CHINA",112,32,"@China"],["VIETNAM",105.8,16,"@0.2"]] | tx "DENG XIAOPING" 1110 300 34 @Deng',
"S62": 'bg dark | a calendar 380 330 1.1 top=CHINA big=1978 @1978 | a open_doors 900 600 w=320 h=420 open_=0>1:@opening:0.8 label=CHINA',
"S63": 'bg dark | a calendar 380 330 1.1 top=VIETNAM big=1986 @1986 | a open_doors 900 600 w=320 h=420 open_=0>1:@followed:0.8 label=VIETNAM',
"S64": 'bg flat c=#20303a | a globe 640 330 170 @global | arrow 260 330 430 330 @aggressive | arrow 1020 330 850 330 @aggressive | kw "GLOBAL INTEGRATION" 640 590 56 @integration',
"S65": 'bg dark | fn cage_lift at=@lifted | tx 1994 60 70 56 anchor=l @1994 | sfx metal_clang @lifted db=-6 | sfx sparkle @lifted+1.0 db=-8 | kw "EMBARGO LIFTED" 1040 200 52 @lifted+0.6',
"S66": 'bg flat c=#e9e1cf | a handshake 640 330 1.3 sleeveL=#232b45 sleeveR=#5b5f66 @normalized | tx 1995 60 70 56 anchor=l @1995 | kw "RELATIONS NORMALIZED" 640 560 52 @diplomatic',
"S67": 'bg dark | cam push 1 1.1 | fn vnpins x=640 y=360 h=560 glow=True | kw READY 960 300 84 @ready',
# ---------------- Chapter 2: the pitch ----------------
"S68": 'card 1990s sub="Chapter 2  ·  The Pitch"',
"S69": 'bg flat c=#e9e1cf | p official 200 600 0.9 f=0.6 pose=wave_R e=happy | p clerk 380 610 0.8 f=0.6 pose=point_R e=happy | p exec 640 600 1 e=neutral | a money_bag 640 470 0.7 label=FDI | p official2 1080 600 0.9 f=-0.6 pose=wave_R e=happy | kw COMPETING 640 100 64 @competing',
"S70": 'bg office | p exec 820 600 1 f=-0.6 e=neutral pose=think_R | st "WHY\\nVIETNAM?" 380 250 40 @value',
"S71": 'bg office | p official 300 600 1 f=0.6 e=happy pose=point_R talk=@offered~@pitch | p exec 900 600 1 f=-0.6 e=happy @executives | a paper 590 230 220 160 label=PITCH size=40 @pitch',
"S72": 'bg flat c=#20303a | fn asia labels=True | st "1. GEOGRAPHY" 1140 120 36 @strategic | cnt 0 3200 1140 330 60 fmt="{:,} km" @3 dur=1.0',
"S73": 'bg flat c=#20303a | fn asia labels=False arrows=[[100,2,112,18,"@shipping","#ffffff"],[112,18,124,33,"@lanes","#ffffff"]] | kw "SHIPPING" 1140 280 52 @shipping | kw "LANES" 1140 340 52 @lanes',
"S74": 'bg flat c=#20303a | fn asia labels=False pins=[["FACTORIES",113.3,23.1,"@industrial"]] | a factory 1110 470 0.4 @heartland | kw "NEXT DOOR" 1140 180 52 @door',
"S75": 'bg flat c=#e9e1cf | st "2. PEOPLE" 1080 120 36 @demographic | p worker 240 600 0.85 e=happy @young | p worker_m 450 600 0.85 e=happy @young+0.15 | p worker 660 600 0.85 e=happy @young+0.3 | a books_cap 960 600 0.9 @literate',
"S76": 'bg factory | p worker 340 500 0.8 legs=0 e=determined | p worker_m 640 500 0.8 legs=0 e=determined | p worker 940 500 0.8 legs=0 e=determined | a assembly_phones 140 470 1000 | kw "COMPETITIVE WAGES" 640 100 56 @wage',
"S77": 'bg dark | a ussr_pillar 640 640 440 label=POLICY @stability | st "3. STABILITY" 1060 200 36 @Institutional | a open_doors 280 600 w=260 h=360 open_=0>1:@openness:0.6 label=OPEN',
"S78": 'bg flat c=#e9e1cf | p official 300 600 1 e=smug f=0.5 | arrow 200 110 1150 110 c=#5fae5a dur=1.5 @long | tx 2000 220 170 40 c=#333333 @long | tx 2030 1120 170 40 c=#333333 @continuity | kw "SAME RULES" 820 380 64 @policy',
"S79": 'bg office | p official 250 600 0.9 f=0.6 e=determined | a fta_scroll 620 330 1.1 @free | kw FTAs 640 80 72 @FTAs',
"S80": 'bg flat c=#20303a | cnt 0 16 640 130 96 fmt="{} FTAs" @16 dur=0.8 | a fta_scroll 300 420 0.6 @signed | a fta_scroll 640 420 0.6 @signed+0.15 | a fta_scroll 980 420 0.6 @signed+0.3',
"S81": 'bg flat c=#20303a | a globe 640 360 170 | arrow 560 290 330 200 @Europe | st EUROPE 230 160 @Europe | arrow 720 290 950 200 @North | st "NORTH\\nAMERICA" 1060 160 36 @North | arrow 780 420 960 480 @Japan | st JAPAN 1060 500 @Japan | kw TARIFF-FREE 640 600 52 @tariff',
"S82": 'bg flat c=#20303a | a globe 640 360 170 | st EUROPE 230 160 | st "NORTH\\nAMERICA" 1060 160 36 | st JAPAN 1060 500 | arrow 500 420 330 480 @Southeast | st "SOUTHEAST\\nASIA" 230 500 36 @Southeast | tx 2008 640 80 56 @2008',
"S83": 'bg dark | cam push 1 1.1 | a vietnam_map 640 380 460 | kw GAMBLE 640 100 72 @gamble',
"S84": 'bg flat c=#e9e1cf | a factory 320 560 0.6 label=TEXTILES @textile | arrow 560 400 720 400 @into | a chip 960 380 1.3 label=HIGH-TECH @high | kw POWERHOUSE 960 120 60 @powerhouse',
# ---------------- Samsung ----------------
"S85": 'bg city | tx 2008 60 70 56 anchor=l @2008 | kw SAMSUNG 640 140 84 @Samsung | st "SOUTH KOREA" 640 290 @South',
"S86": 'bg office | p exec 400 600 1 f=0.5 e=neutral pose=think_R | a globe 900 300 140 @global | st "NEW BASE?" 900 520 @manufacturing',
"S87": 'bg office | p exec 260 600 1 f=0.6 pose=point_R e=neutral | a paper 650 330 380 420 lines_=0 label="NEEDS" size=44 | tx "- low labor costs" 490 260 40 c=#222222 ol=0 anchor=l @low',
"S88": 'bg office | p exec 260 600 1 f=0.6 pose=point_R e=neutral | a paper 650 330 380 420 lines_=0 label="NEEDS" size=44 | tx "- low labor costs" 490 260 40 c=#222222 ol=0 anchor=l | tx "- stable support" 490 330 40 c=#222222 ol=0 anchor=l @government | tx "- fast logistics" 490 400 40 c=#222222 ol=0 anchor=l @fast | tx "- suppliers nearby" 490 470 40 c=#222222 ol=0 anchor=l @component',
"S89": 'bg flat c=#20303a | fn vnpins x=420 y=360 h=600 pins=[["BAC NINH",106.07,21.18,"@Baknin"]] | cnt 0 670 960 220 84 fmt="${}M" @$670 dur=1.0 | a money_bag 960 450 1.0 label=$ @greenfield',
"S90": 'bg flat c=#20303a | fn vnpins x=420 y=360 h=600 pins=[["BAC NINH",106.07,21.18,"@0.0"],["HANOI",105.85,21.03,"@Hanoi"]] | a smartphone 960 360 1.4 @phone',
"S91": 'bg sky | a factory 640 560 0.7 @factory | a factory 290 560 0.5 @mega | a factory 990 560 0.5 @mega+0.4 | kw MEGA-EXPANSION 640 100 64 @mega',
"S92": 'bg flat c=#20303a | fn vnpins x=640 y=360 h=600 pins=[["BAC NINH",106.07,21.18,"@Baknin"],["THAI NGUYEN",105.84,21.59,"@Taiguan"],["HO CHI MINH CITY",106.7,10.78,"@Ho"]]',
"S93": 'bg dark | a vietnam_map 400 360 520 | a money_bag 400 140 0.7 label=$ move=0,200:@pouring:0.5 @pouring | sfx money_rain @pouring db=-10 | cnt 0 22 950 300 96 fmt="${}B" @$22 dur=1.0',
"S94": 'bg factory | tx TODAY 60 70 48 anchor=l @Today | a assembly_phones 0 520 1280 side=front | kw "NOT JUST A FEW" 640 140 64 @few',
"S95": 'bg dark | fn pie x=420 y=320 r=180 frac=0.5 at=@50 label="50%+" | a smartphone 950 320 1.3 @mobile',
"S96": 'bg flat c=#e9e1cf | a smartphone 300 330 0.9 side=back label="MADE IN VIETNAM" @built | a factory 820 560 0.9 label=VIETNAM @Vietnamese',
"S97": 'bg port | cam pan | a container_ship 640 520 0.9 label=EXPORTS | a sea 520 | cnt 0 55 640 140 96 fmt="${}B" @$55 dur=1.0',
"S98": 'bg dark | fn pie x=640 y=320 r=200 frac=0.15 at=@15 label="15% OF GDP" c=#c0392b c2=#e9b949',
# ---------------- Chapter 3: the trade war windfall ----------------
"S99": 'bg sky | tx 2018 60 70 56 anchor=l @2018 | a factory 640 560 0.8 label=CLOTHING @clothing | kw "ASSEMBLY HUB" 640 100 64 @assembly',
"S100": 'bg flat c=#e9e1cf | st FOOTWEAR 330 300 @footwear | a smartphone 840 330 1.0 @electronics | a tablet 1080 360 0.6 @electronics+0.15',
"S101": 'card "THE EARTHQUAKE" sub="Chapter 3  ·  2018" | shake @earthquake amp=0.8',
"S102": 'bg dark | fn gauge x=640 y=440 r=230 at=@overdrive label=GROWTH up=True | kw OVERDRIVE 640 100 72 @overdrive',
"S103": 'bg dark | p exec 330 600 1 f=0.6 e=angry @trade | p official2 950 600 1 f=-0.6 e=angry @trade+0.15 | st USA 330 150 @U.S | st CHINA 950 150 @U.S+0.2 | kw "TRADE WAR" 640 300 72 @war | shake @erupted',
"S104": 'bg sky | a tariff_wall 640 600 w=640 h=360 build=0>1:@slapped:1.2 label="25% TARIFF" | a container 40 600 0.8 label=CHINA move=60,0:@worth:0.5 | shake @Chinese amp=0.3',
"S105": 'bg office | p exec 640 600 1 e=worried pose=think_R | st "MADE IN\\nCHINA" 300 240 40 @relying | kw "100%" 960 200 84 @100',
"S106": 'bg dark | a container 400 480 1.1 label="MADE IN CHINA" | kw "NOT SAFE" 640 160 84 @safe | shake @safe amp=0.3',
"S107": 'bg office | a paper 640 360 340 420 label=PLAYBOOK size=40 lines_=0 @playbook | tx "CHINA + 1" 640 380 72 c=#c0392b ol=0 @China | p exec 1050 600 0.9 f=-0.6 e=smug',
"S108": 'bg flat c=#e9e1cf | kw "RULE:" 1000 150 60 @rule | a factory 400 560 0.7 label=CHINA @primary | st "FOR CHINA\'S\\nMARKET" 400 150 36 @domestic',
"S109": 'bg flat c=#e9e1cf | a factory 330 560 0.6 label=CHINA | a factory 930 560 0.6 label=VIETNAM @secondary | kw "+1" 930 140 84 @secondary | st TARIFF-FREE 930 280 36 @tariff',
"S110": 'bg dark | fn vnpins x=640 y=360 h=560 glow=True | kw WINNER 980 200 84 @winner | sfx retro_jingle @winner db=-8',
"S111": 'bg sky | a factory 250 560 0.45 label=FOXCONN @Foxconn | a factory 640 560 0.45 label=PEGATRON @Pegatron | a factory 1030 560 0.45 label=LUXSHARE @Luxshare',
"S112": 'bg flat c=#e9e1cf | a assembly_phones 140 520 1000 side=front | st "FOR APPLE" 640 180 @Apple',
"S113": 'bg sky | a money_bag 200 470 0.8 label=$ @billions | a factory 700 560 0.8 @building | kw "NEW FACTORIES" 640 100 60 @facilities',
"S114": 'bg flat c=#20303a | cam push 1 1.06 | fn vnpins x=640 y=470 h=700 pins=[["QUANG NINH",107.3,21.0,"@Quangning"],["BAC GIANG",106.2,21.27,"@Baxiang"]]',
"S115": 'bg flat c=#e9e1cf | a earbuds_case 380 360 1.4 @AirPods | a tablet 880 360 1.3 @iPads | kw "MOVED TO VIETNAM" 640 100 56 @shifted',
"S116": 'bg flat c=#e9e1cf | a smartwatch 560 330 1.8 @watches | a vietnam_map 1020 360 320 @Vietnam',
"S117": 'bg city | a factory 400 560 0.75 label=INTEL @Intel | a chip 960 320 1.1 label=CHIPS @semiconductor | tx "HO CHI MINH CITY" 960 520 40 @Ho',
"S118": 'bg port | a port_crane 200 520 0.9 | a container_ship 780 520 0.8 label=VIETNAM | a sea 520 | tx 2024 60 70 56 anchor=l @2024 | cnt 0 405 760 140 96 fmt="${}B" @$405 dur=1.2',
"S119": 'bg flat c=#e9e1cf | a circuit_board 120 200 400 260 @computer | a chip 720 330 0.9 @components | a smartphone 1050 330 1.1 @smartphones',
"S120": 'bg dark | fn pie x=640 y=320 r=190 frac=0.18 at=@$72 label="$72B ELECTRONICS"',
"S121": 'bg dark | a caged_map 640 600 440 | kw ISOLATED 1030 250 60 @isolated',
"S122": 'bg flat c=#20303a | fn asia labels=False arrows=[[106,21,121.5,31.2,"@global","#e9b949"],[106.7,10.8,139.7,35.7,"@consumer","#e9b949"],[106,21,127,37.5,"@tech","#e9b949"],[106.7,10.8,103.8,1.3,"@assembly","#e9b949"]] | kw "BEATING" 1140 270 52 @heart | kw "HEART" 1140 330 52 @heart | sfx thud @heart db=-6 | sfx thud @heart+0.3 db=-8',
# ---------------- Chapter 4: the trap ----------------
"S123": 'bg city | tx TODAY 60 70 48 anchor=l @Today | a vietnam_map 640 330 360 @transformation | kw TEXTBOOK 1000 200 60 @textbook | sfx sparkle @celebrated db=-6',
"S124": 'bg flat c=#e9e1cf | a books_cap 360 600 1.2 @triumph | st "MARKET\\nREFORM" 840 240 40 @market | st "GLOBAL\\nINTEGRATION" 1050 430 36 @global',
"S125": 'bg dark | bars 340 560 600 380 vals=[70,3] labels=["1986","TODAY"] fmt="{}%" hl=1 @70 | kw POVERTY 640 100 64 @Poverty',
"S126": 'bg dark | bars 340 560 600 380 vals=[1,50] labels=["1986","TODAY"] fmt="{}x" c=#5fae5a @income | kw "50-FOLD" 640 100 72 @50',
"S127": 'bg city | a highway 580 | a container 80 560 0.6 @container | a factory 640 560 0.4 label="TECH ZONE" @industrial | a port_crane 1120 560 0.6 @ports | kw MODERN 640 100 64 @Modern',
"S128": 'card "THE CATCH" sub="Chapter 4  ·  The Middle-Income Trap"',
"S129": 'bg sky | p worker_m 260 560 0.9 f=0.6 e=worried walk=40 | a pit_trap 700 560 w=520 @trap',
"S130": 'bg port | a container_ship 640 520 0.9 label=VIETNAM | a sea 520 | cnt 0 400 640 140 96 fmt="${}B" @$400 dur=1.0',
"S131": 'bg flat c=#e9e1cf | fn pie x=400 y=320 r=190 frac=0.85 at=@majority label=FOREIGN c=#c0392b c2=#e9b949 | p exec 950 600 1 f=-0.5 e=smug | a money_bag 950 470 0.7 label=$ @captured',
"S132": 'bg factory | p worker 330 500 0.85 legs=0 e=determined f=0.3 | p worker_m 940 500 0.85 legs=0 e=determined f=-0.3 | a assembly_phones 140 470 1000 side=front | st ASSEMBLY 300 140 34 @assembly | st SOLDERING 640 140 34 @soldering | st TESTING 980 140 34 @testing',
"S133": 'bg dark | kw "INTELLECTUAL PROPERTY" 640 100 56 @intellectual | a golden_key 640 230 0.8 @property | a chip 640 450 1.1 label=CPU @microprocessors',
"S134": 'bg flat c=#e9e1cf | a tablet 360 330 1.2 @display | a paper 850 330 300 260 label="</> CODE" size=36 @software',
"S135": 'bg flat c=#20303a | fn asia x=560 labels=False pins=[["SEOUL",127,37.5,"@Seoul"],["TAIPEI",121.5,25,"@Taipei"],["TOKYO",139.7,35.7,"@Tokyo"]] | st CUPERTINO 1150 250 34 @Cupertino | st BRAND 1150 480 40 @brand',
"S136": 'bg flat c=#e9e1cf | p worker_m 400 600 1 e=sad f=0.4 | st "TIER 1" 850 150 @Tier | a chip 850 380 0.8 label=LOCAL @local',
"S137": 'bg dark | fn pie x=640 y=320 r=200 frac=0.05 at=@tiny label="TINY FRACTION" c=#c0392b c2=#9aa0a8',
"S138": 'bg flat c=#20303a | fn asia labels=True arrows=[[113,30,106,20.5,"@China","#c0392b"],[127,36,107,19,"@South","#c0392b"],[121,24,107.5,17.5,"@Taiwan","#c0392b"]] | kw IMPORTED 1140 300 52 @imported',
"S139": 'bg port | a container_ship 640 520 0.8 label=EXPORT move=800,0:@shipped:1.4 | a sea 520 | kw "SHIPPED OUT" 640 120 64 @shipped',
"S140": 'bg room wall=#e9e1cf | p official 300 600 1 e=determined f=0.6 pose=think_R | a smile_curve 560 140 600 340 progress=0>1:@understands:1.2',
"S141": 'bg flat c=#e9e1cf | a smile_curve 220 140 840 400 | arrow 640 470 330 200 c=#5fae5a @gamble | kw "NEXT GAMBLE" 640 70 56 @gamble',
"S142": 'bg city | a rd_center 640 560 0.9 @R | cnt 0 200 1080 160 72 fmt="${}M+" @$200 dur=1.0 | tx HANOI 640 610 48 @Hanoi',
"S143": 'bg flat c=#e9e1cf | a books_cap 400 600 1.3 @STEM | p kid 820 620 1.1 e=happy f=-0.4 @education',
"S144": 'bg sky | a chip 380 320 1.3 label=PACKAGING @semiconductor | a factory 880 560 0.6 label=GREEN @green | a palm 1160 560 0.6',
"S145": 'bg paddy | tx "20TH CENTURY" 60 70 48 anchor=l @20th | p farmer 560 640 1 e=tired | a rice_bowl 880 560 0.8 fill_=0.2 @impoverished',
"S146": 'bg dark | fn cage_lift at=@opening | kw REBUILD 1040 200 60 @rebuild',
"S147": 'bg factory | p worker 640 580 1 legs=0 pose=raise_both e=happy | a assembly_phones 0 520 1280 side=back | kw "THE WORLD\'S FACTORY" 640 70 56 @world',
"S148": 'bg dark | tx "21ST CENTURY" 60 70 48 anchor=l @21st | a ladder 700 640 h=520 missing_from=0.6 @test | p worker_m 520 640 0.8 f=0.6 e=determined',
"S149": 'bg flat c=#e9e1cf | a assembly_phones 60 560 560 side=front | arrow 660 400 800 400 @into | a golden_key 1000 380 1.1 @owner | kw OWNER 1000 160 72 @owner',
"S150": 'bg factory | a assembly_phones 140 520 1000 side=back | kw "ASSEMBLING = GOOD" 640 120 64 @good',
"S151": 'bg dark | cam pull 1.1 1.0 | a golden_key 640 300 1.6 rot=-0.3 @owning | kw "OWNING = FORTUNE" 640 520 72 @fortune | sfx sparkle @fortune db=-4 | sfx retro_jingle @fortune+0.4 db=-10',
}

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = json.load(open(os.path.join(HERE, "words.json")))
END = 608.76
act1 = json.load(open(os.path.join(HERE, "shots.json")))["shots"]
SEGS = [{"id": s["id"], "start": s["start"]} for s in act1] + json.load(open(os.path.join(HERE, "segs.json")))
for j, s in enumerate(SEGS):                       # word ranges by time window
    nxt = SEGS[j+1]["start"] if j + 1 < len(SEGS) else END
    idx = [i for i, w in enumerate(WORDS) if s["start"] - 0.05 <= w["t0"] < nxt - 0.05]
    s["i0"], s["n"] = (idx[0], len(idx)) if idx else (0, 0)
ACT1_CUES = {s["id"]: s["sfx"] for s in act1 if s["id"] in KEY}

ONLY = os.environ.get("SHOTS")
SHOTS = build_shots({k: L.get(k, "bg dark") for k in [s["id"] for s in SEGS]}, SEGS, WORDS, END)
SEL = [(sid, sh) for sid, sh in SHOTS if not ONLY or sid in ONLY.split(",")]

def _fn(sid, sh):
    f = KEY.get(sid) or sh.draw
    def g(ctx, t, dur): f(ctx, t, dur)
    g.__name__ = sid.lower(); return g
SCENES = [(sh.dur, _fn(sid, sh)) for sid, sh in SEL]
CUES = []
for i, (sid, sh) in enumerate(SEL):
    cues = [(t, n, g) for n, t, g in ACT1_CUES[sid]] if sid in KEY else sh.cues
    CUES += [(i + 1, max(0.0, t), n, g) for t, n, g in cues if t < sh.dur]
SUBS = [None]*len(SEL)
NARRATION = "episodes/vietnam/narration.wav" if not ONLY else None
NARRATION_OFFSET = 0.0
