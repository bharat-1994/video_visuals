"""Key shots built by the director: S01 hook, S12 cage (motif plant), S14-S15 the USSR prop and its collapse."""
import sys, os; sys.path.insert(0, os.getcwd())
from episodes.vietnam.assets import *

def ease_in(k): k = clamp(k); return k*k

def s01(ctx, t, dur):
    bg_flat(ctx, NIGHT)
    ctx.save(); camera(ctx, lerp(1.0, 1.06, ease_io(t/dur)), 640, 360, t=t)
    text(ctx, "1986", 640, 290, 150, (1, 1, 1), reveal=clamp((t-0.38)/0.32))
    popped(ctx, t, 0.95, 640, 500, lambda c: vietnam_map(c, 0, 0, 170), seed=11)
    ctx.restore()

def s12(ctx, t, dur):
    bg_dark(ctx)
    sh = 0.7*clamp(1-(t-0.25)/0.3) if t > 0.25 else 0
    ctx.save(); camera(ctx, 1.0, 640, 360, shake=sh, t=t)
    vietnam_map(ctx, 640, 393, 317, cracks=1.0)
    yc = lerp(-60, 600, ease_in(t/0.25))
    cage(ctx, 640, yc, 360, 440, lock=pop(t, 0.68) if t > 0.68 else 0)
    dust(ctx, 640, 600, t, 0.25, n=6, size=60, seed=3)
    keyword(ctx, t, 0.30, "TRAPPED", 1010, 300, 72, seed=7)
    ctx.restore()

PIL = (830, 630, 480)            # pillar bottom-centre x, y and height (shared by S14/S15)
CM = (560, 600, 380)             # caged map bottom-centre x, y and cage height

def _scene_1415(ctx, t, rise, lean, crumble, fall, sh, kw=None):
    bg_dark(ctx)
    ctx.save(); camera(ctx, *kw.get('cam', (1.0, 640, 360)), shake=sh, t=t)
    px, py, ph = PIL
    ctx.save(); ctx.rectangle(0, 0, W, py+1); ctx.clip()            # pillar rises out of the floor
    ussr_pillar(ctx, px, py + (1-ease_out(rise))*ph, ph, crumble=crumble, t=t)
    ctx.restore()
    caged_map(ctx, CM[0], CM[1], CM[2], tilt=lean + fall)
    for f in kw.get('fx', []): f()
    ctx.restore()

def s14(ctx, t, dur):
    rise = clamp((t-0.10)/0.30); lean = 0.085*ease_out(clamp((t-0.45)/0.3))
    sh = 0.35*clamp(1-(t-0.40)/0.25) if t > 0.40 else 0
    z = lerp(1.0, 1.05, ease_io(t/dur))
    _scene_1415(ctx, t, rise, lean, 0, 0, sh, dict(cam=(z, 690, 380), fx=[
        lambda: dust(ctx, PIL[0], PIL[1], t, 0.40, n=5, size=55, seed=5),
        lambda: keyword(ctx, t, 1.18, "BACKER", 1080, 150, 72, seed=9)]))

def s15(ctx, t, dur):
    crumble = clamp((t-1.24)/1.6)
    fall = (1.42 - 0.085)*ease_in(clamp((t-2.05)/0.40))
    if t > 2.45: fall -= 0.06*math.sin((t-2.45)*18)*math.exp(-(t-2.45)*7)      # small bounce on landing
    sh = 0.0
    if 1.24 < t < 1.84: sh = 0.5*(1-(t-1.24)/0.6)
    if 2.45 < t < 2.85: sh = 0.6*(1-(t-2.45)/0.4)
    z = lerp(1.05, 0.98, ease_io((t-2.4)/1.1))
    _scene_1415(ctx, t, 1, 0.085, crumble, fall, sh, dict(cam=(z, 690, 380), fx=[
        lambda: dust(ctx, PIL[0], PIL[1]-200, t, 1.30, n=6, size=70, seed=2),
        lambda: dust(ctx, PIL[0], PIL[1]-20, t, 1.90, n=7, size=80, seed=8),
        lambda: dust(ctx, CM[0]+400, CM[1]-20, t, 2.45, n=6, size=70, seed=4)]))

SHOT_FNS = {"S01": s01, "S12": s12, "S14": s14, "S15": s15}
