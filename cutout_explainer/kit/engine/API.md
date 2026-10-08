# Engine API (engine/lib.py) — put `import sys; sys.path.insert(0,'engine'); from lib import *` at the top of your module   Canvas W=1280,H=720, FPS=30. cairo context `ctx`.
A scene is `def shotN(ctx, t, dur):` (t = seconds since shot start). Draw background -> camera -> world -> overlay text.
- Camera: `ctx.save(); camera(ctx, zoom, cx, cy, shake=0, t=t)` ... draw world ... `ctx.restore()`. push_in: zoom=lerp(1.0,1.12,ease_io(t/dur)); pull_out reverse; pan: cx=lerp(...).
- Backgrounds: bg_flat(ctx,c) | bg_spotlight(ctx, base=(r,g,b), cx=640, floor_y=620) | bg_sky_ground(ctx, sky, ground, horizon=520) | bg_sunset(ctx) | bg_room(ctx, wall, floor, floor_y=560) | city_window(ctx,x,y,w,h,night=False)
- Colors: tuples 0..1, hexc('#rrggbb'), INK (outline black), SKIN.
- Shapes: box(ctx,x,y,w,h,c,r=0,line=None,lw=3) ; circle(ctx,x,y,r,c,line=None,lw=3,a=1) ; ellipse(ctx,x,y,rx,ry,c,a=1) ; poly(ctx,pts,c,line=None,lw=3,a=1) ; line(ctx,pts,c=INK,lw=6,a=1) ; hose(ctx,p0,p1,bend,lw) ; rrect(ctx,...) path only.
- Props: money_bag(ctx,x,y,s=1,label="$") (origin ~bag center, height ~140*s) ; bill(ctx,x,y,rot,s) ; crt(ctx,x,y,s=1,screen=c,draw_screen=fn(ctx,t),t=t) base at (x,y), screen area 184x132 local coords (0,0 top-left) ; desk(ctx,x,y,w=420) top surface at y ; paper(ctx,x,y,w,h,rot=0,c=white,lines_=4,label=None,size=30)
- Text (handwritten font "Caveat Brush"): text(ctx,s,x,y,size=48,c=(1,1,1),anchor="c"|"l"|"r",reveal=0..1 typewriter,rot=0,outline=INK or None). Keywords on screen: white with outline=INK, size 56-80.
  dialogue(ctx, "line1\nline2", x, y, to=(mouth_x,mouth_y), size=40, reveal=0..1): reference-style white handwritten line + tick toward speaker. Place text in empty space near speaker's head, NOT over faces.
- Effects: pop(t,start,dur) -> scale with overshoot ; popped(ctx,t,start,x,y,draw_fn(ctx), puff=True, seed=n) draws draw_fn around origin scaled in with smoke puff ; smoke(ctx,x,y,life0..1,size,seed) ; ease_io, ease_out, back, lerp, clamp.
- Characters: p = cast(who, scale) with who in elon_kid|elon_teen|elon_adult|kimbal|bully|editor|banker (faces are designed to resemble the real people; NEVER redefine looks).
  NEW: view="back" draws the character from behind (back of head + hair, no face) — use for over-the-shoulder shots.
  info = p.draw(ctx, x, y, t, expr, talking=False, facing=0.0, armL=(dx,dy), armR=(dx,dy), legs=True, walk=0.0, blink_seed=0, look=0.0)
  * (x,y) = WAIST (bottom of torso). Full figure: torso ~190px tall + head above (~ to y-400 at scale 1), legs to y+150. Kids are 0.82x.
  * expr: neutral happy sad angry worried shocked smug tired determined. talking=True animates lip-flap.
  * facing: -1 (looks left) .. 0 front .. 1 (looks right). Two-shot dialogue: characters face each other with |facing| ~0.6.
  * armL/armR = hand offset from that shoulder in px (y down). Down: (-25,125)/(25,125). Raised: (±40,-130). Pointing: (±150,10). Holding object in front: (±50,60). Animate by lerping these over t. Hands return in info['handL'/'handR'] (scene coords) to attach props; info['head'], info['R'].
  * walk=phase (e.g. t*1.6) animates legs; also move x over time.
  * medium/closeup framing = bigger scale (1.3-1.8) with waist below frame (y ~ 760-900) so legs are off-screen; use legs=False.
Style rules (from reference video): flat colors, no gradients except bg helpers; black INK outlines 3-4px on props; props pop in with smoke puffs timed to the narration beat; one idea per shot; a slow camera push or pull on most shots; keep plenty of empty background; text never covers faces.
Render one frame: `python3 engine/check.py <module> <shotfn> <t> out.png`. Contact sheet: `python3 engine/sheet.py <module> out.jpg`. Final: `python3 engine/build.py <module> out.mp4`.

## v2 additions
- SFX: names available (see audio/sfx/INDEX.md): pop whoosh whoosh_short thud shove_hit book_drop typing_burst key_clack page_flip paper_rustle retro_laser retro_explosion retro_jingle cash_register coins footsteps suitcase_roll plane_flyby wind_ambience night_crickets office_hum snore typewriter_tick sparkle boing ding money_rain door_close rocket_rumble engine_roar.
  Each shots module must define CUES = [(shot_id, t_local_seconds, "name", gain_db), ...] matching on-screen events exactly (pop when a prop pops, whoosh on fast moves/exits, typewriter_tick every ~0.06s while caption types (or a few), ambience at t=0 of the shot at -14..-18 dB). Mixer handles placement; music bed is added globally.
- Subtitles: define SUBS = [text or None per shot]; build.py draws them at the bottom ~ y>630 — keep the bottom 90px free of important content and text.
- STAGING RULES (critical, director feedback): screens/monitors/TVs/books must face the person using them. If a character types, show them in 3/4 or side view (facing toward the device, |facing|>=0.6) with the device seen from its side/back, OR an over-the-shoulder shot (view="back", device screen facing camera beyond them). Hands must touch what they hold/type on. Objects rest on surfaces.
- ASSET QUALITY (critical): landmarks and props must be recognizable reconstructions of the REAL thing, not generic boxes: correct silhouette and proportions, 2-3 flat tones per material (base, shadow side, highlight), windows/arches/details repeated with loops, thin INK outlines (2-3px), small details (railings, roof tiles hint, trees). Put asset drawing functions in your own assets module. No official logos or seals; names are plain lettering (a serif look is fine via text() — or draw blocky letters).

## Poses & rig constraints
- `armL, armR = pose("phone_R")` — presets: down hips hold_front raise_both wave_R point_R point_L phone_R think_R shrug type_R type_L carry_R. Blend: `pose("down","wave_R",ease_out(t/0.4))`. See reference/pose_presets.jpg.
- Hands can't cross the body midline unless `cross=True`. In side view (|facing|>=0.6) the far arm is drawn behind the torso automatically; in `view="back"` both arms are behind the torso.
- New characters: `Puppet(hair="short|fringe|part|wavy|slick|bald", hair_c, shirt, jacket, tie, jaw=0..1, nose, glasses, mustache, kid, brow_w, scale)`.
- Paths in your module are relative to the kit root (audio/ is found automatically).
- Narration audio: set `NARRATION = "episodes/<slug>/narration.wav"` and `NARRATION_OFFSET = <batch start s>` in your module; build.py mixes it and ducks the music. Shot timings come from `episodes/<slug>/words.json` (see docs/DIRECTION_TEMPLATE.md).
