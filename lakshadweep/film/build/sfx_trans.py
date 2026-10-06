"""Transition whooshes / impacts derived from the actual edit. -> build/out/trans_sfx.npy (2,N)"""
import sys, os, numpy as np
sys.path.insert(0, 'build'); sys.path.insert(0, 'render')
import synth as S
from synth import SR, place
import film, film_core as FC
tl = film.build_timeline()
N = int((FC.TOTAL + 6) * SR)
bus = np.zeros((2, N), np.float32)
rng = np.random.default_rng(77)
n = 0
for e in tl.entries:
    if e.trans in ('whip', 'zoom', 'flare', 'iris') and e.tdur > 0.2:
        d = max(e.tdur * 1.2, 0.5)
        if e.trans == 'whip':
            w = S.sweep_noise(d, 400, 4200, 1.6, 0.30, 'swell')
        elif e.trans == 'zoom':
            w = S.sweep_noise(d * 1.4, 250, 2500, 1.3, 0.34, 'in')
        elif e.trans == 'flare':
            w = S.sweep_noise(d * 1.6, 600, 7000, 1.4, 0.30, 'swell')
        else:
            w = S.sweep_noise(d * 1.2, 500, 5000, 1.5, 0.26, 'swell')
        place(bus, S.pan(w, rng.uniform(-0.4, 0.4)), max(e.start - 0.1, 0), 1.0)
        n += 1
np.save('build/out/trans_sfx.npy', bus)
print('transition sfx', n)
