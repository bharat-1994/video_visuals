"""Shot factories & wrappers used by film.py."""
import os, math
import numpy as np, cv2
from engine import *
import assets as AS
import fx as FX
import geo as G
from data import ISLANDS, OTHERS


class Layered(Shot):
    """wrap a shot and apply per-frame effect callables fn(img, t, dur)->img."""
    def __init__(self, shot, effects):
        self.shot = shot; self.effects = effects; self.dur = shot.dur

    def frame(self, t, ctx=None):
        self.shot.dur = self.dur
        f = self.shot.frame(t, ctx)
        for fn in self.effects:
            f = fn(f, t, self.dur)
        return f

    def close(self):
        self.shot.close()


def vid(sub, ss=0.0, speed=1.0, zoom=(1.0, 1.06), pan=(0, 0, 0, 0), fx=None, vf='', flip=False):
    def make(dur):
        path = AS.conform(AS.video(sub), ss, dur, speed, vf_extra=vf)
        s = VideoShot(path, dur, 0.0, zoom, pan, flip=flip)
        return Layered(s, fx) if fx else s
    return make


WM_IMAGES = {'fl:9', 'fl:10', 'fl:11', 'fl:12', 'fl:13', 'fl:14', 'fl:23'}   # photographer's corner watermark -> crop it out


def img(sub, z0=1.0, z1=1.14, p0=(0.5, 0.5), p1=(0.5, 0.5), rot=(0, 0), shake=0.0, fx=None, maps=False, max_side=4200):
    if sub in WM_IMAGES:
        z0 = max(z0, 1.19); z1 = max(z1, 1.30)
        p0 = (p0[0], min(p0[1], 0.40)); p1 = (p1[0], min(p1[1], 0.40))

    def make(dur):
        path = os.path.join(G.MAPS, sub) if maps else AS.still(sub)
        s = StillShot(path, dur, z0, z1, p0, p1, rot, shake, max_side=max_side)
        return Layered(s, fx) if fx else s
    return make


def dust(strength=0.35, seed=1, n=110, color=(255, 240, 215)):
    return lambda f, t, d: FX.particles(f, t, seed, n, color, strength)


def rays(strength=0.3, color=(200, 235, 255)):
    return lambda f, t, d: FX.god_rays(f, t, strength, color)


def caust(strength=0.3):
    return lambda f, t, d: FX.caustics(f, t, strength)


def fade_in(sec=0.5):
    return lambda f, t, d: FX.fade_black(f, 1 - smooth(t / sec)) if t < sec else f


def fade_out(sec=0.6):
    return lambda f, t, d: FX.fade_black(f, smooth((t - (d - sec)) / sec)) if t > d - sec else f


class FuncShotF(Shot):
    """shot whose frame function is f(t, dur, state)->img"""
    def __init__(self, fn, dur):
        self.fn = fn; self.dur = dur; self.state = {}

    def frame(self, t, ctx=None):
        return self.fn(t, self.dur, self.state)


def func(fn):
    return lambda dur: FuncShotF(fn, dur)


def solid(color=(0, 0, 0)):
    def make(dur):
        return FuncShotF(lambda t, d, s: np.full((H, W, 3), color, np.uint8), dur)
    return make
