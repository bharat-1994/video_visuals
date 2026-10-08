# Scene lines (engine/scene_v2.py): one line per shot

A shot = elements separated by ` | `. Element = TYPE, positional numbers (x y [scale|size]), key=value pairs, timing tokens. Quote text that has spaces.
Canvas 1280x720, y down. A person's (x, y) is the waist base: y 600-640 puts feet near the bottom; the head centre is ~230 px above y at scale 1.

## Timing tokens
`@word` appears when that narration word is spoken (case/punctuation ignored, prefix match: `@invest` hits "investment") · `@word#2` 2nd occurrence ·
`@word+0.3` offset · `@1.5` = seconds from shot start (**seconds need a decimal point**; `@50` means the word "50") · `out@word` vanishes with a puff ·
`key=a>b:@word:0.6` animates a number from a to b starting at @word over 0.6 s. A word that is not in this shot's narration is an error.
Every shot needs something NEW tied to a narration word at least every 2.5 s (engine/beats.py measures it).

## Elements
| element | meaning |
|---|---|
| `bg NAME k=v` | background (see CATALOG). Always first. |
| `cam push\|pull\|still\|pan\|whip\|track [z0 z1 cx cy [cx2 cy2]]` | camera; default push. whip = snap in from the left; track X0 X1 = constant-speed pan |
| `shake @word amp=0.6` | impact shake + thud (only for real impacts) |
| `p WHO x y s e=EXPR f=-1..1 pose=NAME pose2=NAME@word e2=EXPR@word legs=0 view=back walk=px/s talk=@w1~@w2 handL=x,y handR=x,y` | person from CAST. f = facing (-1 left, 1 right). handL/handR put that hand exactly on a point |
| `a NAME x y [s] k=v @word` | asset call `NAME(ctx, x, y, ...)`; with @word it pops in. `move=dx,dy:@word:dur` slides it. `snd=NAME` sets its entrance sound, `snd=none` silences |
| `kw "TEXT" x y size` | white outlined keyword (use sparingly, keep clear of faces) |
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

## House rules (the audits enforce them)
- No decorative motion (rain, confetti, steam, motorbikes, spinning things) unless the narration says it or the real place has it.
- Backgrounds: none in more than ~8% of shots, no 3 identical in a row, dark/spotlight only for the cage/map motif. People in >= 55% of shots.
- Sounds are automatic by element category (see audio/sfx/INDEX.md); do not add `pop`. At most 3 entrance sounds per shot.
- Never put text over a face; keep text in y 90-130 (top) or below the chin of the nearest head; nothing important in the outer 40 px.
- No logos or seals. Companies = brand colour + plain name lettering + the real kind of place (factory, office, store).
- Reserve the meeting-room screen area x 556-1116, y 118-418.
- A shot id may appear only once in a lines file (the last duplicate silently wins; layout_check flags it).
