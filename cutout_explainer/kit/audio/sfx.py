#!/usr/bin/env python3
"""Synthesized SFX library + music bed. Run: python3 sfx.py"""
import os, wave
import numpy as np
from scipy import signal as sg

SR = 44100
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio", "sfx")
MUSIC_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)

def T(d): return np.arange(int(d * SR + 1e-6)) / SR
def noise(d): return rng.standard_normal(int(d * SR + 1e-6))
def bp(x, lo, hi, o=2):
    hi = min(hi, SR * 0.49)
    return sg.sosfilt(sg.butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sg.sosfilt(sg.butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sg.sosfilt(sg.butter(o, f, 'high', fs=SR, output='sos'), x)
def expenv(n, tau, atk=0.002):
    t = np.arange(n) / SR
    e = np.exp(-t / tau)
    a = int(atk * SR + 1e-6)
    if a > 1: e[:a] *= np.linspace(0, 1, a)
    return e
def place(buf, snd, t0, gain=1.0):
    i = int(t0 * SR + 1e-6)
    if i >= len(buf): return
    j = min(len(buf), i + len(snd))
    buf[i:j] += gain * snd[:j - i]
def sine_sweep(f0, f1, d, curve=None):
    t = T(d); k = t / d
    f = f0 + (f1 - f0) * (k if curve is None else curve(k))
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def square(ph, duty=0.5): return np.where((ph % 1.0) < duty, 1.0, -1.0)
def save(name, x, d=None, peak_db=-3.0, fade=0.004, out=OUT, norm=True):
    x = np.asarray(x, float)
    if d is not None:
        n = int(round(d * SR))
        x = np.pad(x, (0, max(0, n - len(x))))[:n]
    x = x - np.mean(x[:max(1, len(x))]) * 0  # keep
    f = int(fade * SR + 1e-6)
    x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    if norm: x = x / (np.max(np.abs(x)) + 1e-12) * 10 ** (peak_db / 20)
    pcm = (np.clip(x, -1, 1) * 32767).astype('<i2')
    with wave.open(os.path.join(out, name + ".wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

def bell(f, d, tau, partials=((1, 1), (2.76, .5), (5.40, .25), (8.93, .12))):
    t = T(d); y = np.zeros_like(t)
    for r, a in partials:
        y += a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / (tau / (1 + 0.5 * (r - 1))))
    return y

def swept_noise(d, centers, widths_oct=0.7, peak=0.5, wid=0.18, nb=10, lo=250, hi=7000):
    """band-passed noise whose centre frequency follows centers(t) via gaussian-weighted bands"""
    t = T(d); n = noise(d); y = np.zeros_like(t)
    fs = np.geomspace(lo, hi, nb)
    cf = centers(t)
    for f in fs:
        band = bp(n, f / 1.35, f * 1.35)
        w = np.exp(-(np.log2(f / cf) / widths_oct) ** 2)
        y += band * w
    return y

# ------------------------------------------------------------------ SFX
def pop():
    d = 0.15; t = T(d)
    f = 250 + 750 * (1 - np.exp(-t / 0.012))      # bubbly upward chirp
    f = f * (1 - 0.35 * t / d)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * expenv(len(t), 0.03, 0.001)
    y += 0.25 * bp(noise(d), 1500, 5000) * expenv(len(t), 0.004, 0.0005)
    return y
def whoosh(d=0.5, lo=300, hi=3800):
    t = T(d)
    c = lambda t: lo * (hi / lo) ** np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.0
    y = swept_noise(d, c)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2.2
    return y * env
def thud():
    d = 0.3; t = T(d)
    y = sine_sweep(110, 45, d, lambda k: 1 - np.exp(-k * 8)) * expenv(len(t), 0.09, 0.001)
    y += 0.5 * lp(noise(d), 300) * expenv(len(t), 0.03, 0.0005)
    return lp(y, 600)
def shove_hit():
    d = 0.25; t = T(d)
    slap = bp(noise(d), 800, 6000) * expenv(len(t), 0.025, 0.0005)
    body = sine_sweep(320, 90, d, lambda k: 1 - np.exp(-k * 14)) * expenv(len(t), 0.07, 0.0008)
    low = sine_sweep(90, 50, d) * expenv(len(t), 0.1, 0.001)
    return 0.9 * slap + 1.0 * body + 0.7 * low
def book_drop():
    d = 0.35; y = np.zeros(int(d * SR + 1e-6)); t = T(d)
    slap = hp(noise(0.12), 1200) * expenv(int(.12 * SR + 1e-6), 0.018, 0.0005)
    place(y, slap, 0.0, 0.8)
    place(y, bp(noise(0.08), 400, 1500) * expenv(int(.08 * SR + 1e-6), .02), 0.015, 0.4)
    thump = sine_sweep(120, 55, 0.3, lambda k: 1 - np.exp(-k * 7)) * expenv(int(.3 * SR + 1e-6), 0.08, .002)
    place(y, thump, 0.025, 1.1)
    return y
def key_click(pitch=1.0, vel=1.0):
    d = 0.06; n = int(d * SR + 1e-6)
    hi = bp(noise(d), 1800 * pitch, 5200 * pitch) * expenv(n, 0.004, 0.0003)
    thock = np.sin(2 * np.pi * 190 * pitch * T(d)) * expenv(n, 0.012, 0.0005)
    ping = np.sin(2 * np.pi * 2700 * pitch * T(d)) * expenv(n, 0.003, 0.0002) * 0.25
    return vel * (hi * 0.8 + thock * 0.9 + ping)
def typing_burst():
    d = 1.6; y = np.zeros(int(d * SR + 1e-6)); t = 0.03
    while t < d - 0.1:
        p = rng.uniform(0.75, 1.35); v = rng.uniform(0.55, 1.0)
        place(y, key_click(p, v), t)
        place(y, key_click(p * 1.1, 0.25 * v)[:int(.025 * SR + 1e-6)], t + rng.uniform(.06, .1))  # key-up
        r = rng.random()
        t += rng.uniform(0.04, 0.09) if r < 0.45 else rng.uniform(0.09, 0.2) if r < 0.9 else rng.uniform(0.25, 0.4)
    return y
def key_clack(): return key_click(1.0, 1.0)
def page_flip():
    d = 0.35; t = T(d)
    c = lambda t: 1500 + 3500 * np.clip(t / d, 0, 1)
    y = swept_noise(d, c, 0.9, lo=800, hi=8000)
    env = np.exp(-((t - 0.1) / 0.09) ** 2) + 0.35 * np.exp(-((t - 0.24) / 0.05) ** 2)
    y = y * env * (0.6 + 0.4 * lp(noise(d), 120) / 0.3)
    place(y, hp(noise(0.01), 3000) * 0.3, 0.27)  # flap tick
    return y
def paper_rustle():
    d = 0.6; n = int(d * SR + 1e-6); y = np.zeros(n)
    for _ in range(90):
        t0 = rng.uniform(0.0, d - 0.06)
        g = np.exp(-((t0 - 0.3) / 0.22) ** 2) * rng.uniform(0.3, 1)
        ln = rng.uniform(0.004, 0.02)
        s = bp(noise(ln), rng.uniform(1500, 3500), rng.uniform(5000, 9000)) * expenv(int(ln * SR + 1e-6), ln / 3, 0.0005)
        place(y, s, t0, g)
    return y + 0.15 * bp(noise(d), 1500, 6000) * np.exp(-((T(d) - 0.3) / 0.2) ** 2)
def retro_laser():
    d = 0.2; t = T(d); k = t / d
    f = 2200 * np.exp(-4.2 * k) + 150
    ph = np.cumsum(f) / SR
    return square(ph, 0.25) * (1 - k) ** 0.8
def retro_explosion():
    d = 0.4; n = int(d * SR + 1e-6); t = T(d)
    y = np.zeros(n); i = 0
    while i < n:
        hold = int(8 + 120 * (i / n) ** 1.2)   # sample-and-hold slows down => lower crunch
        y[i:i + hold] = rng.choice([-1.0, 1.0]) * rng.uniform(.4, 1)
        i += hold
    # bit-crush-ish amplitude steps
    env = np.floor(np.exp(-t / 0.12) * 8) / 8
    low = square(np.cumsum(70 - 40 * t / d) / SR) * 0.4
    return (y + low) * env
def retro_jingle():
    d = 0.9; y = np.zeros(int(d * SR + 1e-6))
    notes = [(523.25, 0.0, .17), (659.25, .19, .17), (783.99, .38, .17), (1046.5, .57, .33)]
    for f, t0, ln in notes:
        n = int(ln * SR + 1e-6); tt = np.arange(n) / SR
        s = square(f * tt, 0.5) * 0.6 + square(f * tt * 1.0005, 0.25) * 0.4
        s *= np.where(tt < ln - 0.02, 1, 0) * (1 - 0.35 * tt / ln)
        place(y, s, t0)
    bass = square(261.63 * T(.33), 0.5) * 0.25
    place(y, bass, .57)
    return y
def cash_register():
    d = 1.0; y = np.zeros(int(d * SR + 1e-6))
    # "cha": mechanical clunk + drawer ratchet
    place(y, hp(noise(.05), 800) * expenv(int(.05 * SR + 1e-6), .01, .0005), 0, .9)
    place(y, sine_sweep(180, 70, .12, lambda k: 1 - np.exp(-k * 6)) * expenv(int(.12 * SR + 1e-6), .035), 0.0, 1.0)
    for i in range(7):
        place(y, bp(noise(.01), 2500, 7000) * expenv(int(.01 * SR + 1e-6), .003, .0003), 0.07 + i * .014, 0.4)
    place(y, bp(noise(.08), 300, 2500) * expenv(int(.08 * SR + 1e-6), .02), 0.17, 0.5)
    # "ching": bright bell, struck twice
    b = bell(2637, 0.85, 0.35)
    place(y, b, 0.19, 0.8); place(y, bell(2637 * 1.0, 0.7, .3), 0.27, 0.5)
    place(y, bell(3951, .5, .2, ((1, 1), (2.76, .3))), 0.19, 0.3)
    return y
def coins():
    d = 0.8; y = np.zeros(int(d * SR + 1e-6)); t0 = 0.0
    while t0 < 0.62:
        f = rng.choice([3150, 3520, 4180, 4700, 5300]) * rng.uniform(.97, 1.03)
        ln = rng.uniform(.12, .25)
        s = bell(f, ln, ln / 2.5, ((1, 1), (1.47, .7), (2.3, .4), (3.1, .2)))
        place(y, s, t0, rng.uniform(.4, 1))
        place(y, hp(noise(.004), 3000), t0, .3)
        t0 += rng.uniform(.03, .085)
    return y
def footsteps():
    d = 1.6; y = np.zeros(int(d * SR + 1e-6))
    for i, t0 in enumerate([0.1, 0.5, 0.9, 1.3]):
        v = rng.uniform(.85, 1.0); p = 1 + (i % 2) * .08
        body = sine_sweep(95 * p, 55, .2, lambda k: 1 - np.exp(-k * 6)) * expenv(int(.2 * SR + 1e-6), .05, .004)
        scuff = bp(noise(.15), 200, 1800) * expenv(int(.15 * SR + 1e-6), .03, .006)
        heel = lp(noise(.03), 2500) * expenv(int(.03 * SR + 1e-6), .008, .001)
        place(y, body, t0, 0.9 * v); place(y, scuff, t0, 0.5 * v); place(y, heel, t0, 0.3 * v)
    return lp(y, 3500)
def suitcase_roll():
    d = 2.0; t = T(d); n = len(t)
    rumble = lp(noise(d), 350, 2) * 1.0
    wheel = bp(noise(d), 700, 2400) * (0.5 + 0.5 * np.sin(2 * np.pi * 26 * t)) ** 2
    buzz = lp(noise(d), 120) * 3
    y = rumble * 0.8 + wheel * 0.5 + buzz * 0.6
    y *= (0.85 + 0.15 * np.sin(2 * np.pi * 3.3 * t))
    y *= np.clip(t / 0.08, 0, 1) * np.clip((d - t) / 0.15, 0, 1)
    seam = 0.2
    for tc in np.arange(0.15, d - 0.1, seam):
        tj = tc + rng.uniform(-.004, .004); g = rng.uniform(.8, 1.1)
        place(y, bp(noise(.02), 600, 3500) * expenv(int(.02 * SR), .006, .0005), tj, 1.1 * g)
        place(y, np.sin(2 * np.pi * 140 * T(.03)) * expenv(int(.03 * SR), .01), tj, 0.9 * g)
    return y
def plane_flyby():
    d = 3.0; t = T(d)
    pos = (t - 1.4) / 0.55
    dop = 1.0 - 0.28 * (0.5 * (1 + np.tanh(pos)))       # pitch drops as it passes
    amp = 1.0 / (1.0 + (pos * 0.9) ** 2) ** 0.75
    f0 = 95 * dop
    ph = np.cumsum(f0) / SR
    tone = sum((1 / h ** 1.1) * np.sin(2 * np.pi * h * ph + h) for h in range(1, 12))
    tone *= (1 + 0.15 * np.sin(2 * np.pi * 7 * t))
    hiss = swept_noise(d, lambda tt: 900 * (1 - 0.45 * 0.5 * (1 + np.tanh((tt - 1.4) / 0.55))) + 0 * tt, 1.2, lo=300, hi=4500)
    rum = lp(noise(d), 220) * 3
    y = (tone * 0.5 + hiss * 0.7 + rum * 0.6) * amp
    return y * np.clip(t / 0.3, 0, 1) * np.clip((d - t) / 0.4, 0, 1)
def loopify(x, xf=0.4):
    n = int(xf * SR + 1e-6); L = len(x) - n
    y = x[:L].copy()
    fi = np.linspace(0, 1, n)
    y[:n] = x[:n] * np.sqrt(fi) + x[L:] * np.sqrt(1 - fi)
    return y
def wind_ambience():
    d = 4.0; x = noise(d + 0.6); t = T(d + 0.6)
    g = 0.5 + 0.5 * lp(noise(d + 0.6), 0.5, 1) * 12
    g = np.clip(0.55 + 0.45 * np.sin(2 * np.pi * 0.35 * t + 1) * np.sin(2 * np.pi * 0.13 * t + 2), 0.1, 1)
    y = lp(bp(x, 150, 900, 2), 700) * g + 0.3 * bp(x, 900, 2600) * g ** 2 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.5 * t))
    return loopify(y, 0.6)
def night_crickets():
    d = 4.0; xf = 0.4; N = d + xf; n = int(N * SR + 1e-6); y = np.zeros(n)
    for fc, per, ph0 in [(4300, 0.62, 0.0), (4650, 0.77, 0.3), (3950, 0.91, 0.5)]:
        t0 = ph0
        while t0 < N - 0.3:
            for k in range(3):
                ln = 0.035
                tt = T(ln)
                s = np.sin(2 * np.pi * fc * tt) * np.sin(np.pi * tt / ln) ** 1.5
                # fast pulse train within chirp
                s *= 0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 120 * tt))
                place(y, s, t0 + k * 0.058, 0.6)
            t0 += per * rng.uniform(.97, 1.03)
    y += 0.05 * lp(noise(N), 1500) 
    return loopify(y, xf)
def office_hum():
    d = 4.0; t = T(d)
    y = sum(a * np.sin(2 * np.pi * f * t + p) for f, a, p in
            [(120, 1, 0), (240, .45, 1), (360, .3, 2), (480, .15, 3), (600, .08, 1), (60, .25, 0.5)])
    buzz = np.sin(2 * np.pi * 120 * t) ** 3
    y = y * 0.35 + 0.08 * bp(noise(d), 2000, 6000) * (1 + 0.5 * buzz)
    room = lp(noise(d + .4), 500)
    room = loopify(room, .4) * 0.3
    return y + room * 0.9
def snore():
    d = 2.2; y = np.zeros(int(d * SR + 1e-6))
    for t0 in (0.05, 1.15):
        L = 1.0; n = int(L * SR + 1e-6); t = np.arange(n) / SR
        # inhale rasp (rises) then exhale rattle (lower, vibrating soft palate)
        inh = np.sin(np.pi * np.clip(t / 0.42, 0, 1)) * (t < 0.42)
        exh = np.sin(np.pi * np.clip((t - 0.44) / 0.5, 0, 1)) * (t >= 0.44)
        f0 = np.where(t < 0.44, 55 + 25 * t / 0.44, 48 - 12 * (t - 0.44))
        ph = np.cumsum(f0) / SR
        saw = sg.sawtooth(2 * np.pi * ph)
        flutter = 0.5 + 0.5 * np.sin(2 * np.pi * (24 if True else 0) * t)
        rasp = bp(noise(L), 250, 1100, 2) * (0.5 + 0.5 * flutter)
        s = (lp(saw, 500) * 0.9 + rasp * 1.4) * (inh * 0.85 + exh * 1.0)
        s = bp(s, 80, 1400, 2)
        place(y, s, t0)
    return y
def typewriter_tick():
    d = 0.05; n = int(d * SR + 1e-6)
    return (bp(noise(d), 2500, 8000) * expenv(n, .005, .0002)
            + 0.5 * np.sin(2 * np.pi * 1200 * T(d)) * expenv(n, .006, .0002))
def sparkle():
    d = 0.6; y = np.zeros(int(d * SR + 1e-6))
    scale = [1046.5, 1318.5, 1568, 2093, 2637, 3136, 4186, 5274]
    for i, f in enumerate(scale):
        t0 = i * 0.045 + rng.uniform(0, .01)
        ln = 0.3; tt = T(ln)
        s = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * f * 2.01 * tt)) * expenv(len(tt), .09, .001)
        place(y, s, t0, 0.5 + 0.06 * i)
    return y
def boing():
    d = 0.5; t = T(d)
    wob = np.exp(-t / 0.2) * np.sin(2 * np.pi * 11 * t)
    f = 160 + 420 * np.exp(-t / 0.25) * (1 + 0.9 * wob) + 120 * wob
    ph = np.cumsum(f) / SR
    y = np.sin(2 * np.pi * ph + 1.5 * np.sin(2 * np.pi * 2 * ph))
    y = y * np.exp(-t / 0.22)
    return y * np.clip(t / .003, 0, 1)
def ding():
    d = 0.6
    return bell(1568, d, 0.28, ((1, 1), (2.0, .3), (3.0, .15), (4.2, .06)))
def money_rain():
    d = 2.0; n = int(d * SR + 1e-6); y = np.zeros(n)
    for _ in range(420):
        t0 = rng.uniform(0, d - 0.1)
        ln = rng.uniform(.02, .08)
        fc = rng.uniform(1800, 5000)
        s = bp(noise(ln), fc, fc * 1.8) * np.sin(np.pi * np.arange(int(ln * SR + 1e-6)) / (ln * SR))
        place(y, s, t0, rng.uniform(.2, 1))
    y += 0.35 * bp(noise(d), 1500, 6000)
    t = T(d)
    return y * np.clip(t / .25, 0, 1) * np.clip((d - t) / .5, 0, 1)
def door_close():
    d = 0.4; y = np.zeros(int(d * SR + 1e-6))
    place(y, sine_sweep(140, 60, .3, lambda k: 1 - np.exp(-k * 7)) * expenv(int(.3 * SR + 1e-6), .07, .001), 0, 1.0)
    place(y, lp(noise(.1), 900) * expenv(int(.1 * SR + 1e-6), .02, .001), 0, .7)
    # latch click
    place(y, bp(noise(.02), 1500, 5000) * expenv(int(.02 * SR + 1e-6), .004, .0003), .075, .7)
    place(y, np.sin(2 * np.pi * 900 * T(.03)) * expenv(int(.03 * SR + 1e-6), .006), .078, .25)
    place(y, sine_sweep(210, 160, .15) * expenv(int(.15 * SR + 1e-6), .04), .08, .25)
    return y

SFX = dict(
 pop=(pop, .15, "Bubbly cartoon pop: quick upward-chirping sine with a tiny noise click."),
 whoosh=(lambda: whoosh(.5), .5, "Airy band-passed noise sweep rising then falling, smooth swell."),
 whoosh_short=(lambda: whoosh(.25, 400, 4500), .25, "Quick, snappy version of the whoosh for fast moves."),
 thud=(thud, .3, "Low body hit: pitch-dropping sine with soft noise click."),
 shove_hit=(shove_hit, .25, "Cartoon punch/slap: noisy smack plus pitch-dropping body and low thump."),
 book_drop=(book_drop, .35, "Papery slap followed by a deep thump."),
 typing_burst=(typing_burst, 1.6, "Keyboard clatter, irregular timing, varied key pitch/velocity, key-up ticks."),
 key_clack=(key_clack, .08, "Single mechanical key press."),
 page_flip=(page_flip, .35, "Paper page turn: swept noise swish plus flap tick."),
 paper_rustle=(paper_rustle, .6, "Crinkly paper handling: clustered random crackle grains."),
 retro_laser=(retro_laser, .2, "8-bit pew: square wave diving from high to low."),
 retro_explosion=(retro_explosion, .4, "8-bit explosion: sample-and-hold noise crunch with stepped decay."),
 retro_jingle=(retro_jingle, .9, "4-note ascending chiptune title jingle (C-E-G-C) on pulse waves."),
 cash_register=(cash_register, 1.0, "Cha-ching: mechanical clunk and drawer ratchet, then bright double bell ring."),
 coins=(coins, .8, "Jingling coins: rapid random metallic pings."),
 footsteps=(footsteps, 1.6, "Four soft footsteps (thump + scuff) at 0.1/0.5/0.9/1.3 s."),
 suitcase_roll=(suitcase_roll, 2.0, "Wheel rumble with rhythmic clicks at pavement seams (every 0.2 s)."),
 plane_flyby=(plane_flyby, 3.0, "Jet rumble with doppler pitch drop; mono, peak ~1.4 s (pan in the mixer)."),
 wind_ambience=(wind_ambience, 4.0, "Soft gusting wind bed, crossfaded to loop."),
 night_crickets=(night_crickets, 4.0, "Three overlapping crickets chirping in triplets; loopable."),
 office_hum=(office_hum, 4.0, "120 Hz fluorescent hum with harmonics and soft room tone; loopable."),
 snore=(snore, 2.2, "Two cartoon snores: rasping inhale and rattly exhale."),
 typewriter_tick=(typewriter_tick, .05, "Tiny crisp tick for text reveals."),
 sparkle=(sparkle, .6, "Ascending glittery chimes."),
 boing=(boing, .5, "Springy boing: wobbling pitch-swept FM sine."),
 ding=(ding, .6, "Clean bell ding."),
 money_rain=(money_rain, 2.0, "Dense paper-flutter bed for raining bills, fades in/out."),
 door_close=(door_close, .4, "Door thud with latch click."),
)

# ------------------------------------------------------------------ MUSIC
def music_bed():
    d = 40.0; bpm = 105; beat = 60 / bpm; n = int(d * SR + 1e-6)
    L = np.zeros(n); B = np.zeros(n); S = np.zeros(n); P = np.zeros(n)
    mr = np.random.default_rng(11)
    mid = lambda m: 440 * 2 ** ((m - 69) / 12)
    def kal(f, ln=.5, tau=.16):
        tt = T(ln); idx = 3.0 * np.exp(-tt / .02)
        s = np.sin(2 * np.pi * f * tt + idx * np.sin(2 * np.pi * f * 3.0 * tt)) * np.exp(-tt / tau)
        s += 0.2 * np.sin(2 * np.pi * f * 4.0 * tt) * np.exp(-tt / .03)
        return s * np.clip(tt / .002, 0, 1)
    chords = [(60, [60, 64, 67]), (55, [55, 59, 62]), (57, [57, 60, 64]), (53, [53, 57, 60])]  # C G Am F
    scale = [0, 2, 4, 5, 7, 9, 11]
    nbars = int(d / (4 * beat)) + 1
    motif = [0, 2, 1, 3, 2, 1, 0, 2]
    last = 72
    for bar in range(nbars):
        root, tones = chords[bar % 4]
        t0 = bar * 4 * beat
        # bass: root on 1, fifth-ish on 2&, root on 3
        bn = lambda m: np.sin(2 * np.pi * mid(m - 12) * T(.45)) * np.exp(-T(.45) / .22) + 0.25 * np.sin(2 * np.pi * mid(m) * T(.45)) * np.exp(-T(.45) / .1)
        place(B, bn(root), t0, 1.0)
        place(B, bn(root + 7), t0 + 1.5 * beat, 0.6)
        place(B, bn(root), t0 + 2 * beat, 0.85)
        place(B, bn(root + (7 if bar % 2 else 12)), t0 + 3.5 * beat, 0.5)
        # soft chord pluck on beats 1 and 3
        for m in tones:
            place(P, kal(mid(m + 12), .6, .22), t0, .22)
            place(P, kal(mid(m + 12), .6, .22), t0 + 2.5 * beat, .14)
        # lead: eighth notes, rhythm pattern with rests
        pat = [1, 0, 1, 1, 0, 1, 1, 0] if bar % 2 == 0 else [1, 1, 0, 1, 1, 0, 1, 1]
        pool = [m + o for m in tones for o in (12, 24)] + [tones[0] + 24 + 2, tones[1] + 12 + 5]
        pool = sorted(set(pool))
        for i, on in enumerate(pat):
            if not on: continue
            if i == 0 and bar % 4 == 0: m = tones[2] + 12
            else:
                j = min(range(len(pool)), key=lambda k: abs(pool[k] - last))
                j = int(np.clip(j + mr.choice([-2, -1, -1, 1, 1, 2]), 0, len(pool) - 1))
                m = pool[j]
            last = m
            place(L, kal(mid(m + 12 if m < 64 else m)), t0 + i * beat / 2, 0.6 if i % 2 == 0 else 0.4)
        # shaker: 16ths, accents on offbeats
        for i in range(16):
            ts = t0 + i * beat / 4
            amp = 0.5 if i % 4 == 2 else (0.25 if i % 2 == 0 else 0.15)
            s = hp(noise(.05), 6000) * expenv(int(.05 * SR + 1e-6), .012, .002)
            place(S, s, ts, amp)
    # gentle high/low shaping and delay on lead
    L = L + 0.3 * np.roll(L, int(beat * .75 * SR + 1e-6)); L[:int(beat * .75 * SR + 1e-6)] = L[:int(beat * .75 * SR + 1e-6)]
    mix = 0.55 * L + 0.4 * P + 0.75 * B + 0.12 * S
    mix = lp(mix, 9000, 2)
    t = T(d)
    mix *= np.clip(t / 0.05, 0, 1) * np.clip((d - t) / 1.2, 0, 1)
    save("music_bed", mix, d, peak_db=-12.0, fade=0.01, out=MUSIC_OUT)

if __name__ == "__main__":
    rows = []
    for name, (fn, dur, desc) in SFX.items():
        save(name, fn(), dur)
        rows.append((name, dur, desc))
    music_bed()
    with open(os.path.join(OUT, "INDEX.md"), "w") as f:
        f.write("# SFX index\n\n44.1 kHz mono 16-bit WAV, peak -3 dBFS. Music bed is at `../music_bed.wav` (40 s, 105 BPM, peak -12 dBFS).\n\n")
        f.write("| name | duration (s) | description |\n|---|---|---|\n")
        for n, d, desc in rows: f.write(f"| {n} | {d} | {desc} |\n")
        f.write("| music_bed (../music_bed.wav) | 40.0 | Upbeat kalimba/marimba explainer loop, I-V-vi-IV in C, soft bass + shaker. |\n")
    print("done")
