#!/usr/bin/env python3
"""SFX v2: entrance set, named effects, seamless ambience loops, and chapter music beds.

Run:  <venv>/python audio/sfx_v2.py     (idempotent; deterministic via fixed seed)

House pattern copied from sfx.py: T/noise/bp/lp/hp/expenv/place/sine_sweep/bell/
swept_noise/loopify/save. 44.1 kHz mono 16-bit. SFX peak -3 dBFS, music peak -12 dBFS.

Ownership rule: this script only writes files listed in OWNED (its own outputs);
any other pre-existing .wav is skipped, never overwritten.
"""
import os, wave
import numpy as np
from scipy import signal as sg

SR = 44100
SEED = 20260810
HERE = os.path.dirname(os.path.abspath(__file__))          # .../kit/audio
OUT = os.path.join(HERE, "sfx")                             # .../kit/audio/sfx
MUSIC_OUT = os.path.join(HERE, "music")                     # .../kit/audio/music
os.makedirs(OUT, exist_ok=True)
os.makedirs(MUSIC_OUT, exist_ok=True)

rng = np.random.default_rng(SEED)
def reseed():
    global rng
    rng = np.random.default_rng(SEED)

# ------------------------------------------------------------------ helpers (from sfx.py)
def T(d): return np.arange(int(d * SR + 1e-6)) / SR
def noise(d): return rng.standard_normal(int(d * SR + 1e-6))
def nlen(d): return int(d * SR + 1e-6)
def bp(x, lo, hi, o=2):
    hi = min(hi, SR * 0.49)
    return sg.sosfilt(sg.butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sg.sosfilt(sg.butter(o, min(f, SR * 0.49), 'low', fs=SR, output='sos'), x)
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
    if i < 0: snd = snd[-i:]; i = 0
    j = min(len(buf), i + len(snd))
    if j <= i: return
    buf[i:j] += gain * snd[:j - i]
def sine_sweep(f0, f1, d, curve=None):
    t = T(d); k = t / d
    f = f0 + (f1 - f0) * (k if curve is None else curve(k))
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def square(ph, duty=0.5): return np.where((ph % 1.0) < duty, 1.0, -1.0)
def bell(f, d, tau, partials=((1, 1), (2.76, .5), (5.40, .25), (8.93, .12))):
    t = T(d); y = np.zeros_like(t)
    for r, a in partials:
        y += a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / (tau / (1 + 0.5 * (r - 1))))
    return y
def swept_noise(d, centers, widths_oct=0.7, nb=10, lo=250, hi=7000):
    """band-passed noise whose centre follows centers(t) via gaussian-weighted bands"""
    t = T(d); n = noise(d); y = np.zeros_like(t)
    fs = np.geomspace(lo, hi, nb)
    cf = centers(t)
    for f in fs:
        band = bp(n, f / 1.35, f * 1.35)
        w = np.exp(-(np.log2(f / cf) / widths_oct) ** 2)
        y += band * w
    return y
def loopify(x, xf=0.4):
    n = int(xf * SR + 1e-6); L = len(x) - n
    y = x[:L].copy()
    fi = np.linspace(0, 1, n)
    y[:n] = x[:n] * np.sqrt(fi) + x[L:] * np.sqrt(1 - fi)
    return y
def pink(d):
    """approximate 1/f (Kellet-style IIR on white noise), normalised to ~unit peak"""
    x = noise(d)
    b = np.array([0.049922035, -0.095992946, 0.050612699, -0.004408706])
    a = np.array([1.0, -2.494956002, 2.017377692, -0.522389057])
    y = sg.lfilter(b, a, x)
    m = np.max(np.abs(y))
    return y / (m + 1e-12)

# ------------------------------------------------------------------ owned outputs
def _own(*names): return {n + ".wav" for n in names}

SFX_ENTRANCE = ["soft_whoosh_in", "soft_whoosh_out", "swish_draw", "card_flip", "paper_slide",
                "wood_knock", "metal_tink", "glass_tink", "thump_soft", "pop_soft", "click_soft",
                "ding_soft", "riser_short", "low_boom", "whip"]
SFX_NAMED = ["bicycle_bell", "boxing_bell", "camera_shutter", "chain_rattle", "chalk",
             "cleanroom_hum", "construction", "crowd_cheer", "crowd_murmur", "dice", "door_creak",
             "engine_sputter", "factory_line", "harbor", "heartbeat", "jet_idle", "marker_squeak",
             "news_sting", "rewind_tape", "sewing", "shutter_open", "shutter_slam", "street_traffic",
             "thunder", "vault_lock", "wood_crash", "riser"]
MUSIC = ["music_somber", "music_hopeful", "music_upbeat", "music_tension", "music_reflective"]
OWNED = _own(*(SFX_ENTRANCE + SFX_NAMED + MUSIC))

# ------------------------------------------------------------------ save (ownership-guarded)
def save(name, x, d=None, peak_db=-3.0, fade=0.004, out=OUT, norm=True, allow_exists=False):
    """Write wav; skip any pre-existing file this script does not own. fade=0.0 for loops."""
    fn = os.path.join(out, name + ".wav")
    if os.path.exists(fn) and name + ".wav" not in OWNED and not allow_exists:
        print(f"  skip (exists, not owned): {fn}")
        return None
    x = np.asarray(x, float)
    x = x - np.mean(x)                                   # kill DC (helps loop seams)
    if d is not None:
        n = int(round(d * SR))
        x = np.pad(x, (0, max(0, n - len(x))))[:n]
    f = int(fade * SR + 1e-6)
    if f > 0:
        x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    if norm: x = x / (np.max(np.abs(x)) + 1e-12) * 10 ** (peak_db / 20)
    if not np.all(np.isfinite(x)): raise ValueError(name + ": non-finite samples")
    pcm = (np.clip(x, -1, 1) * 32767).astype('<i2')
    with wave.open(fn, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(f"  wrote {os.path.relpath(fn, HERE)}  {len(x)/SR:.3f}s")
    return fn

# ------------------------------------------------------------------ seamless-loop builder
def build_loop(d, xf, fill):
    """fill(add, buf, Ttot) writes one seamless period of d seconds.
    add() places events and auto-copies events from the first `xf` seconds to t+d
    so the overlap-add tail-into-head (loopify) has matching content at the seam."""
    n = int(xf * SR + 1e-6)
    L = int(d * SR + 1e-6)
    buf = np.zeros(L + n)
    def add(snd, t0, g=1.0):
        place(buf, snd, t0, g)
        if t0 < xf:
            place(buf, snd, t0 + L / SR, g)
    fill(add, buf, (L + n) / SR)
    return loopify(buf, xf)

# ============================================================== 4.1 ENTRANCE SET
def _swell_env(t, d, atk=0.8, fall_tau=0.028):
    e = np.clip(t / (atk * d), 0, 1) ** 1.7
    return e * np.exp(-np.maximum(0.0, t - atk * d) / fall_tau)

def soft_whoosh_in(d=0.30):
    t = T(d)
    y = bp(noise(d), 600, 3000)
    return lp(y * _swell_env(t, d), 4200)

def soft_whoosh_out(d=0.30):
    t = T(d)
    y = bp(noise(d), 600, 3000)
    return lp(y * _swell_env(d - t, d), 4200)         # reverse envelope of soft_whoosh_in

def swish_draw(d=0.45):
    t = T(d)
    c = lambda tt: 800 + 1600 * np.clip(tt / d, 0, 1)  # 800 -> 2400 Hz band sweep
    y = swept_noise(d, c, widths_oct=0.55, lo=400, hi=5200)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.6
    return y * env

def card_flip(d=0.18):
    y = np.zeros(nlen(d))
    n1 = nlen(0.06)
    f1 = bp(noise(0.06), 900, 4200) * expenv(n1, 0.012, 0.001)
    f2 = bp(noise(0.06), 1300, 5400) * expenv(n1, 0.010, 0.001)
    place(y, f1, 0.0, 1.0)
    place(y, f2, 0.05, 0.8)                            # second flap 50 ms later
    place(y, lp(noise(0.02), 500) * expenv(nlen(0.02), 0.006), 0.05, 0.4)
    return y

def paper_slide(d=0.40):
    t = T(d)
    pn = pink(d)
    y = lp(hp(pn, 1000), 7000)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.4
    y = y * env
    for _ in range(16):                                # tiny crackle grains
        ln = rng.uniform(0.003, 0.009)
        s = bp(noise(ln), rng.uniform(2500, 5200), rng.uniform(6500, 9000)) \
            * expenv(nlen(ln), ln / 3, 0.0005)
        place(y, s, rng.uniform(0.02, d - 0.03), rng.uniform(0.15, 0.5))
    return y

def wood_knock(d=0.20):
    t = T(d)
    body = np.sin(2 * np.pi * 220 * t) * expenv(nlen(d), 0.055, 0.0005)
    body += 0.6 * np.sin(2 * np.pi * 520 * t) * expenv(nlen(d), 0.025, 0.0005)
    click = hp(noise(0.008), 1200) * expenv(nlen(0.008), 0.0015, 0.0002)
    y = body * 1.0
    place(y, click, 0.0, 0.7)
    return y

def metal_tink(d=0.40):
    t = T(d)
    y = np.zeros_like(t)
    for f, a, tau in [(1200, 1.0, 0.10), (2900, 0.6, 0.055), (4100, 0.4, 0.035)]:
        y += a * np.sin(2 * np.pi * f * t) * np.exp(-t / tau)
    y += 0.3 * bp(noise(d), 3000, 8000) * expenv(nlen(d), 0.0025, 0.0002)
    return y

def glass_tink(d=0.35):
    t = T(d)
    atk = np.clip(t / 0.008, 0, 1)                     # soft attack
    y = atk * (np.sin(2 * np.pi * 2600 * t) * np.exp(-t / 0.09)
               + 0.6 * np.sin(2 * np.pi * 3900 * t) * np.exp(-t / 0.05))
    return y

def thump_soft(d=0.25):
    t = T(d)
    y = sine_sweep(90, 60, d, lambda k: 1 - np.exp(-k * 9)) * expenv(nlen(d), 0.075, 0.002)
    y += 0.3 * lp(noise(d), 200) * expenv(nlen(d), 0.02, 0.001)
    return y

def pop_soft(d=0.12):
    """v1 pop() an octave down (250+750 -> 125+375), softer attack; the -6 dB is a
    mix-gain intent (all files here are peak-normalised to -3 dBFS)."""
    t = T(d); n = nlen(d)
    f = (125 + 375 * (1 - np.exp(-t / 0.012))) * (1 - 0.35 * t / d)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * expenv(n, 0.035, 0.003)
    y += 0.25 * bp(noise(d), 750, 2500) * expenv(n, 0.004, 0.0005)
    return y

def click_soft(d=0.04):
    t = T(d); n = nlen(d)
    y = np.sin(2 * np.pi * 3000 * t) * expenv(n, 0.006, 0.0004)
    y += 0.35 * bp(noise(d), 1500, 4600) * expenv(n, 0.002, 0.0002)
    return lp(y, 3800)

def ding_soft(d=0.60):
    return bell(880, d, 0.24, ((1, 1), (2.0, .3), (3.0, .15), (4.2, .06))) * \
        np.clip(T(d) / 0.004, 0, 1)

def riser_short(d=0.70):
    t = T(d); k = t / d
    sw = swept_noise(d, lambda tt: 300 + 2200 * np.clip(tt / d, 0, 1), widths_oct=0.9, lo=200, hi=6000)
    sn = sine_sweep(200, 900, d)
    y = (0.8 * sw + 0.5 * sn) * k ** 2.1
    return y

def low_boom(d=0.90):
    t = T(d); n = nlen(d)
    thump = sine_sweep(58, 45, d, lambda k: 1 - np.exp(-k * 12)) * expenv(n, 0.16, 0.003)
    tail = lp(noise(d), 90) * expenv(n, 0.28, 0.01)
    return thump * 1.0 + tail * 0.9

def whip(d=0.20):
    t = T(d)
    c = lambda tt: 5200 * (900 / 5200) ** np.clip(tt / d, 0, 1)     # high -> low
    y = swept_noise(d, c, widths_oct=0.5, lo=500, hi=7000)
    y *= np.exp(-t / 0.028) * np.clip(t / 0.0015, 0, 1)
    place(y, hp(noise(0.004), 2500), 0.0, 0.5)                       # crack
    return y

# ============================================================== 4.2 NAMED EFFECTS
def bicycle_bell(d=0.40):
    y = np.zeros(nlen(d))
    bp_ = ((1, 1), (2.4, .45), (4.15, .25), (6.8, .1))
    place(y, bell(2600, 0.18, 0.06, bp_), 0.0, 1.0)
    place(y, bell(2600, 0.17, 0.05, bp_), 0.22, 0.85)                # second strike
    for t0 in (0.0, 0.22):
        place(y, hp(noise(0.005), 3000), t0, 0.35)                   # hammer tick
    return y

def boxing_bell(d=1.00):
    y = np.zeros(nlen(d))
    parts = ((1, 1), (1.6, .6), (2.9, .45), (4.3, .3), (6.1, .18))
    for i, t0 in enumerate((0.0, 0.30, 0.62)):
        g = 1.0 - 0.18 * i
        place(y, bell(760, 0.42 - 0.06 * i, 0.33, parts), t0, g)
        place(y, bell(1180, 0.30, 0.20, ((1, 1), (2.3, .4))), t0, 0.5 * g)
        place(y, bp(noise(0.02), 1500, 5000) * expenv(nlen(0.02), 0.006, 0.0008), t0, 0.6 * g)
    return y

def camera_shutter(d=0.15):
    y = np.zeros(nlen(d))
    place(y, hp(noise(0.006), 2500) * expenv(nlen(0.006), 0.0015, 0.0002), 0.0, 0.9)
    place(y, np.sin(2 * np.pi * 380 * T(0.02)) * expenv(nlen(0.02), 0.005, 0.0005), 0.012, 0.5)
    for i, t0 in enumerate((0.020, 0.038, 0.058)):                   # mechanical clack
        fc = 1800 + 900 * i
        place(y, bp(noise(0.010), fc, fc * 2.2) * expenv(nlen(0.010), 0.003, 0.0004), t0, 0.7)
        place(y, np.sin(2 * np.pi * (240 + 60 * i) * T(0.015)) * expenv(nlen(0.015), 0.004), t0, 0.4)
    place(y, hp(noise(0.005), 3000) * expenv(nlen(0.005), 0.0012, 0.0002), 0.092, 0.55)  # mirror slap
    return y

def chain_rattle(d=0.60):
    y = np.zeros(nlen(d))
    for _ in range(30):
        t0 = rng.uniform(0, d - 0.05)
        f = rng.choice([2600, 3300, 4200, 5100]) * rng.uniform(0.97, 1.03)
        ln = rng.uniform(0.02, 0.05)
        s = bell(f, ln, ln / 2.5, ((1, 1), (1.47, .6), (2.3, .35)))
        place(y, s, t0, rng.uniform(0.25, 0.7))
        place(y, hp(noise(0.003), 3500), t0, rng.uniform(0.15, 0.4))
    y += 0.15 * bp(noise(d), 2000, 6000) * expenv(nlen(d), 0.25, 0.01)
    return y

def chalk(d=0.60):
    y = np.zeros(nlen(d))
    t = T(d)
    scratch = bp(noise(d), 1800, 7000) * (0.6 + 0.4 * np.sin(2 * np.pi * 17 * t + 1.3 * np.sin(2 * np.pi * 3 * t)))
    y += scratch * 0.35 * np.sin(np.pi * np.clip(t / d, 0, 1)) ** 0.8
    for _ in range(7):                                                # strokes
        ln = rng.uniform(0.05, 0.14)
        fc = rng.uniform(1800, 3500)
        s = bp(noise(ln), fc, fc * rng.uniform(1.5, 2.4))
        s *= np.sin(np.pi * np.arange(nlen(ln)) / nlen(ln)) ** 1.2
        s *= rng.uniform(0.5, 1.0)
        place(y, s, rng.uniform(0, d - ln), 1.0)
    return y

def _fill_cleanroom(add, buf, Ttot):
    t = np.arange(len(buf)) / SR
    hiss = lp(hp(noise(Ttot), 500), 6000)
    buf[:] += hiss * (0.22 + 0.03 * np.sin(2 * np.pi * 0.25 * t))     # airflow, 1 cycle/period
    hum = (0.09 * np.sin(2 * np.pi * 60 * t) + 0.035 * np.sin(2 * np.pi * 120 * t + 1)
           + 0.015 * np.sin(2 * np.pi * 180 * t + 2))
    buf[:] += hum * (1 + 0.06 * np.sin(2 * np.pi * 0.5 * t))

def _fill_construction(add, buf, Ttot):
    t = np.arange(len(buf)) / SR
    buf[:] += lp(noise(Ttot), 220) * (0.30 + 0.10 * np.sin(2 * np.pi * 0.25 * t))  # site rumble
    for t0 in (0.20, 1.00, 1.85, 2.70, 3.40):                         # distant hammering
        n = nlen(0.12); tt = T(0.12)
        h = sine_sweep(120, 65, 0.12, lambda k: 1 - np.exp(-k * 8)) * expenv(n, 0.05, 0.002)
        h += lp(noise(0.12), 300) * expenv(n, 0.02, 0.001) * 0.8
        add(h, t0, rng.uniform(0.4, 0.55))
    for i, t0 in enumerate((0.06, 1.06, 2.06, 3.06)):                 # reverse-alarm beeps (grid kept off the seam)
        f = 880 if i % 2 == 0 else 660
        n = nlen(0.18); tt = T(0.18)
        beep = square(f * tt + 0.02 * np.sin(2 * np.pi * 3 * tt)) * 0.18
        e = np.clip(tt / 0.004, 0, 1) * (tt < 0.14)
        add(lp(beep * e, min(f * 1.6, 5000)), t0, 0.9)

def crowd_cheer(d=2.0):
    t = T(d); y = np.zeros(nlen(d))
    base = np.clip(t / 0.18, 0, 1) * np.clip((d - t) / 0.65, 0, 1)
    mod = 0.75 + 0.35 * lp(noise(d), 1.6)
    for fc, g in [(500, 1.0), (900, 0.9), (1500, 0.8), (2400, 0.5)]:  # formant-ish bands
        y += g * bp(noise(d), fc * 0.7, fc * 1.5)
    y = y * base * mod * 0.5
    for _ in range(28):                                               # clap grains
        place(y, hp(noise(0.012), 1200) * expenv(nlen(0.012), 0.006, 0.0008),
              rng.uniform(0.05, d - 0.2), rng.uniform(0.2, 0.6))
    for t0, ff in [(0.3, 1800), (0.9, 2200), (1.35, 2600)]:           # whistles
        ln = 0.28; tt = T(ln)
        w = np.sin(2 * np.pi * np.cumsum(ff * (1 + 0.06 * np.sin(2 * np.pi * 6 * tt)) + 800 * tt / ln) / SR)
        place(y, w * np.sin(np.pi * np.clip(tt / ln, 0, 1)) ** 1.5 * 0.18, t0, 1.0)
    return y

def _fill_crowd_murmur(add, buf, Ttot):
    t = np.arange(len(buf)) / SR
    mur = np.zeros(len(buf))
    for fc, g in [(320, 1.0), (520, 0.9), (850, 0.7), (1400, 0.5), (2200, 0.3)]:
        v = bp(noise(Ttot), fc * 0.72, fc * 1.4)
        e = np.clip(0.4 + 0.9 * lp(noise(Ttot), rng.uniform(0.9, 1.8)), 0, 1)  # babble swells
        mur += g * v * e
    buf[:] += lp(mur, 3000) * 0.16
    buf[:] += lp(noise(Ttot), 200) * 0.03                             # room pressure

def dice(d=0.80):
    y = np.zeros(nlen(d))
    for _ in range(8):                                                # rattle
        t0 = rng.uniform(0.02, 0.42)
        fc = rng.uniform(700, 2500)
        place(y, bp(noise(0.012), fc, fc * 2) * expenv(nlen(0.012), 0.005, 0.0006), t0, rng.uniform(0.4, 0.9))
        place(y, np.sin(2 * np.pi * rng.uniform(150, 220) * T(0.02)) * expenv(nlen(0.02), 0.006), t0, 0.3)
    for t0 in (0.55, 0.66):                                           # two settling clacks
        g = 1.0 if t0 < 0.6 else 0.7
        place(y, sine_sweep(170, 120, 0.08, lambda k: 1 - np.exp(-k * 8)) * expenv(nlen(0.08), 0.03), t0, g)
        place(y, bp(noise(0.02), 1200, 4000) * expenv(nlen(0.02), 0.004, 0.0005), t0, 0.6 * g)
    return y

def door_creak(d=0.70):
    t = T(d)
    f = (210 + 60 * np.sin(2 * np.pi * 2.7 * t) + 40 * np.sin(2 * np.pi * 6.1 * t + 1)
         + 120 * (t / d))
    ph = np.cumsum(f) / SR
    saw = sg.sawtooth(2 * np.pi * ph)
    y = bp(saw, 240, 1600)
    stick = 0.55 + 0.45 * np.sin(2 * np.pi * 3.1 * t + 0.8 * np.sin(2 * np.pi * 1.7 * t))
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.1
    y = y * stick * env
    y += 0.15 * bp(noise(d), 1200, 4000) * env * stick
    return lp(y, 4500)

def engine_sputter(d=1.20):
    y = np.zeros(nlen(d))
    t0 = 0.02; g = 1.0; gap = 0.085
    while t0 < d - 0.05:
        n = nlen(0.09); tt = T(0.09)
        p = sine_sweep(95, 55, 0.09, lambda k: 1 - np.exp(-k * 10)) * expenv(n, 0.045, 0.001)
        p += lp(noise(0.09), 500) * expenv(n, 0.015, 0.001) * 0.7
        place(y, p, t0, g * rng.uniform(0.8, 1.0))
        t0 += gap * rng.uniform(0.85, 1.25)
        gap *= 1.32                                                   # slowing down
        g *= 0.88
    return y

def _fill_factory_line(add, buf, Ttot):
    t = np.arange(len(buf)) / SR
    motor = sum((1 / h) * np.sin(2 * np.pi * 100 * h * t + h) for h in range(1, 7))
    buf[:] += lp(motor, 900) * 0.10 * (1 + 0.10 * np.sin(2 * np.pi * 2 * t))   # 8 cycles/period
    buf[:] += hp(noise(Ttot), 2000) * 0.015                           # faint air hiss
    parts = ((1, 1), (1.9, .5), (3.4, .3))
    for k in range(8):                                                # clunk every 0.5 s (grid +0.06 off the seam)
        t0 = 0.06 + k * 0.5
        n = nlen(0.09); tt = T(0.09)
        cl = bp(noise(0.09), 800, 3500) * expenv(n, 0.008, 0.0008) * 0.8
        cl += sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-tt / (0.03 / (1 + .5 * (r - 1))))
                  for f, a, r in [(520, 0.5, 1), (1330, 0.3, 1.9), (2110, 0.18, 3.4)])
        add(cl, t0, rng.uniform(0.8, 1.0))
    for t0 in (1.2, 3.1):                                             # pneumatic hiss
        add(bp(noise(0.25), 1000, 4000) * np.sin(np.pi * np.arange(nlen(0.25)) / nlen(0.25)) ** 1.2,
            t0, 0.12)

def _fill_harbor(add, buf, Ttot):
    t = np.arange(len(buf)) / SR
    w = bp(noise(Ttot), 120, 900)
    wash = (0.55 + 0.35 * np.sin(2 * np.pi * 0.5 * t - 1) + 0.15 * np.sin(2 * np.pi * 1.0 * t + 2))
    buf[:] += lp(w, 700) * wash * 0.4
    buf[:] += hp(bp(noise(Ttot), 900, 2600), 800) * np.clip(wash, 0, 1) * 0.05   # lapping foam
    def gull(t0, f0=3200, n_chirp=2):
        for i in range(n_chirp):
            ln = rng.uniform(0.14, 0.2) if i == 0 else rng.uniform(0.10, 0.16)
            tt = T(ln)
            f = f0 * (1 - 0.35 * tt / ln) * (1 + 0.05 * np.sin(2 * np.pi * 7 * tt))
            s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * np.clip(tt / ln, 0, 1)) ** 1.4
            add(bp(s, 1200, 5200), t0 + i * rng.uniform(0.22, 0.3), rng.uniform(0.3, 0.5))
    gull(1.15, 3200, 2); gull(2.75, 2800, 3)

def heartbeat(d=0.80):
    y = np.zeros(nlen(d)); t = T(d)
    def beat(t0, f0, f1, tau, g, ln=0.14):
        n = nlen(ln)
        b = sine_sweep(f0, f1, ln, lambda k: 1 - np.exp(-k * 10)) * expenv(n, tau, 0.004)
        b += lp(noise(ln), 120) * expenv(n, 0.03, 0.004) * 0.4
        place(y, b, t0, g)
    beat(0.05, 68, 46, 0.06, 1.0)          # lub
    beat(0.26, 58, 38, 0.05, 0.7)          # dub
    y += 0.05 * lp(noise(d), 90)
    return y

def _fill_jet_idle(add, buf, Ttot):
    t = np.arange(len(buf)) / SR
    vib = 1 + 0.0025 * np.sin(2 * np.pi * 2 * t)
    ph = np.cumsum(1250 * vib) / SR
    whine = (np.sin(2 * np.pi * ph) + 0.4 * np.sin(2 * np.pi * 2 * ph + 1) + 0.15 * np.sin(2 * np.pi * 3 * ph + 2))
    buf[:] += whine * 0.05 * (1 + 0.3 * np.sin(2 * np.pi * 0.5 * t))  # 1250 Hz: 5000 cycles/period
    rum = lp(noise(Ttot), 160)
    buf[:] += rum * (0.5 + 0.18 * np.sin(2 * np.pi * 0.5 * t + 1)) * 0.35
    buf[:] += bp(noise(Ttot), 250, 900) * 0.06                         # compressor roar

def marker_squeak(d=0.40):
    t = T(d)
    f = 2900 + 500 * np.sin(2 * np.pi * 3 * t) + 250 * np.sin(2 * np.pi * 8 * t + 1)
    squeak = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.35
    rasp = bp(noise(d), 2200, 5600) * (0.55 + 0.45 * np.sin(2 * np.pi * 13 * t))
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 1.3
    return (squeak + rasp * 0.7) * env

def news_sting(d=1.20):
    y = np.zeros(nlen(d))
    stabs = [(0.0, [57, 60, 64], 0.22, 900), (0.22, [60, 64, 67], 0.22, 1300),
             (0.44, [64, 67, 72, 76], 0.60, 2600)]                    # rising A-C-E -> E-G-C-E
    for t0, notes, ln, cut in stabs:
        n = nlen(ln); tt = T(ln)
        s = np.zeros(n)
        for m in notes:
            f = 440 * 2 ** ((m - 69) / 12)
            ph1 = sg.sawtooth(f * tt)
            ph2 = sg.sawtooth(f * 1.006 * tt)
            s += 0.5 * (ph1 + ph2) * np.exp(-tt / (ln / 3))
        s *= np.clip(tt / 0.004, 0, 1)
        place(y, lp(s, cut), t0, 0.5)
    place(y, sine_sweep(110, 82, 0.4) * expenv(nlen(0.4), 0.12, 0.003), 0.44, 0.8)  # sub hit
    shim = bp(noise(0.4), 4000, 9000) * expenv(nlen(0.4), 0.12, 0.03)
    place(y, shim, 0.44, 0.35)                                       # shimmer on the last stab
    return y

def rewind_tape(d=1.00):
    t = T(d)
    f = 300 * 2 ** (2.5 * (t / d) ** 1.5) * (1 + 0.3 * np.sin(2 * np.pi * 28 * t + 2 * np.sin(2 * np.pi * 7 * t)))
    ph = np.cumsum(f) / SR
    y = square(ph, 0.3) * 0.6 + np.sin(2 * np.pi * ph) * 0.4
    y *= 0.7 + 0.3 * np.sin(2 * np.pi * 31 * t + 1)
    y *= np.clip(t / 0.005, 0, 1)
    return lp(y, 5500)

def roller(d=0.60, opening=True):
    y = np.zeros(nlen(d)); t = T(d)
    tg = 0.01
    while tg < d - 0.06:
        fc = rng.uniform(1400, 4200)
        g = (0.5 + 0.9 * tg / d) if opening else (1.2 - 0.7 * tg / d)
        n = nlen(0.008)
        place(y, bp(noise(0.008), fc, fc * 1.7) * expenv(n, 0.003, 0.0005),
              tg + rng.uniform(-0.003, 0.003), g * rng.uniform(0.5, 1.0))
        tg += rng.uniform(0.010, 0.022)
    tc = (d - 0.05) if opening else 0.02                              # end clank
    n = nlen(0.12)
    place(y, sine_sweep(220, 120, 0.12, lambda k: 1 - np.exp(-k * 8)) * expenv(n, 0.05, 0.001), tc, 1.2)
    place(y, bp(noise(0.05), 700, 3200) * expenv(nlen(0.05), 0.015, 0.001), tc, 0.9)
    return y
def shutter_open(d=0.60): return roller(d, True)
def shutter_slam(d=0.60): return roller(d, False)

def _fill_street_traffic(add, buf, Ttot):
    t = np.arange(len(buf)) / SR
    road = bp(noise(Ttot), 120, 1200)
    buf[:] += lp(road, 1500) * (0.75 + 0.15 * np.sin(2 * np.pi * 0.5 * t)) * 0.30
    def passby(tc, gain=1.0):
        ln = 1.4; tt = T(ln)
        x = (tt - ln * 0.5) / (ln * 0.28)
        dop = 1.12 - 0.38 * (0.5 * (1 + np.tanh(x)))
        ph = np.cumsum(90 * dop) / SR
        buzz = sum((1 / h ** 1.1) * np.sin(2 * np.pi * h * ph + h) for h in range(1, 9))
        buzz += 0.6 * lp(noise(ln), 400)
        amp = gain / (1.0 + (x * 0.9) ** 2) ** 0.8
        place(buf, bp(buzz, 60, 2200) * amp * 0.35, tc - ln / 2)
    passby(1.15, 1.0); passby(3.10, 0.8)                              # 2nd pass ends >=0.15 s before the seam
    def horn(t0, f0, f1):
        ln = 0.3; tt = T(ln)
        h = (np.sin(2 * np.pi * f0 * tt) + 0.5 * np.sin(2 * np.pi * f1 * tt)) * 0.6
        h *= np.clip(tt / 0.02, 0, 1) * np.clip((ln - tt) / 0.05, 0, 1)
        add(h, t0, 0.25)
    horn(0.35, 440, 554); horn(2.3, 392, 494)

def thunder(d=1.50):
    t = T(d); n = nlen(d)
    nc = nlen(0.09)
    crack = bp(noise(0.09), 300, 5000) * expenv(nc, 0.03, 0.0008)
    crack += 0.8 * hp(noise(0.09), 800) * expenv(nc, 0.010, 0.0008)
    y = np.zeros(n)
    place(y, crack, 0.02, 1.2)
    rum = lp(noise(d), 110) * 1.6
    roll = 0.5 + 0.8 * np.abs(lp(noise(d), 1.4)) * 4
    roll = np.clip(roll, 0.2, 1.4) * (1 - 0.55 * t / d)
    y += rum * roll
    y += np.sin(2 * np.pi * 38 * t) * np.exp(-np.maximum(0, t - 0.15) / 0.5) * np.clip(t / 0.02, 0, 1) * 0.6
    return y * np.clip(t / 0.004, 0, 1)

def vault_lock(d=0.80):
    y = np.zeros(nlen(d))
    n = nlen(0.2)
    clunk = sine_sweep(140, 70, 0.2, lambda k: 1 - np.exp(-k * 9)) * expenv(n, 0.08, 0.0015)
    clunk += lp(noise(0.2), 400) * expenv(n, 0.02, 0.001) * 0.9
    place(y, clunk, 0.0, 1.1)
    tt = T(0.16)
    parts = sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-tt / tau)
                for f, a, tau in [(480, 0.4, 0.05), (1130, 0.3, 0.04), (1780, 0.2, 0.03)])
    place(y, parts, 0.0, 0.8)
    c = lambda x: 700 + 1700 * np.clip(x / 0.18, 0, 1)               # bolt slide
    slide = swept_noise(0.18, c, widths_oct=0.5, lo=400, hi=5000)
    slide *= np.sin(np.pi * np.arange(nlen(0.18)) / nlen(0.18)) ** 1.2
    place(y, slide, 0.24, 0.8)
    for i in range(4):                                                # detent ticks
        place(y, bp(noise(0.006), 2500, 6500) * expenv(nlen(0.006), 0.002, 0.0003), 0.42 + i * 0.035, 0.5)
    n2 = nlen(0.05)
    place(y, sine_sweep(200, 160, 0.05) * expenv(n2, 0.02, 0.001), 0.62, 0.9)   # lock home
    place(y, hp(noise(0.008), 1500) * expenv(nlen(0.008), 0.002, 0.0003), 0.62, 0.7)
    return y

def wood_crash(d=0.90):
    y = np.zeros(nlen(d))
    place(y, bp(noise(0.05), 600, 4500) * expenv(nlen(0.05), 0.012, 0.0006) * 1.4, 0.0, 1.0)   # crack
    place(y, sine_sweep(190, 90, 0.1, lambda k: 1 - np.exp(-k * 10)) * expenv(nlen(0.1), 0.03, 0.001), 0.0, 0.9)
    for t0 in (0.06, 0.12, 0.19):                                     # splinter pops
        fc = rng.uniform(900, 2400)
        place(y, bp(noise(0.02), fc, fc * 2) * expenv(nlen(0.02), 0.004, 0.0006), t0, rng.uniform(0.5, 0.8))
    n = nlen(0.25)
    place(y, sine_sweep(110, 60, 0.25, lambda k: 1 - np.exp(-k * 8)) * expenv(n, 0.08, 0.002), 0.03, 1.0)  # body
    for _ in range(20):                                               # splatter
        t0 = rng.uniform(0.10, 0.7)
        fc = rng.uniform(400, 2000)
        ln = rng.uniform(0.006, 0.02)
        place(y, bp(noise(ln), fc, fc * 1.8) * expenv(nlen(ln), ln / 3, 0.0005), t0, rng.uniform(0.15, 0.5))
    return y

def riser(d=1.00):
    """longer, slightly stronger riser_short (film impact lead-in)"""
    t = T(d); k = t / d
    sw = swept_noise(d, lambda tt: 400 + 2600 * np.clip(tt / d, 0, 1), widths_oct=0.9, lo=200, hi=7000)
    sn = sine_sweep(220, 1100, d)
    y = (0.9 * sw + 0.55 * sn) * k ** 2.3
    y += 0.2 * lp(noise(d), 120) * k ** 3                             # rising sub
    return y

def _fill_sewing(add, buf, Ttot):
    t = np.arange(len(buf)) / SR
    motor = sum((1 / h) * np.sin(2 * np.pi * 120 * h * t + 0.5 * h) for h in range(1, 5))
    buf[:] += lp(motor, 1200) * 0.08 * (1 + 0.12 * np.sin(2 * np.pi * 3 * t))
    n = nlen(0.02); tt = T(0.02)
    tick = bp(noise(0.02), 3200, 7000) * expenv(n, 0.0025, 0.0004)
    tick += 0.3 * np.sin(2 * np.pi * 1800 * tt) * expenv(n, 0.002, 0.0004)
    for k in range(48):                                               # 12 Hz, 48 ticks per 4 s (grid +0.05 off the seam)
        add(tick, 0.05 + k / 12.0, 0.5 + 0.5 * (k % 2) * 0.4 + rng.uniform(-0.1, 0.1))
    for k in range(8):                                                # shuttle clack each bar-ish
        add(sine_sweep(300, 220, 0.03) * expenv(nlen(0.03), 0.01, 0.001), 0.06 + k * 0.5, 0.15)

def _loop_gen(name, fill):
    """bound generator for 4 s seamless ambience loops"""
    def f():
        return build_loop(4.0, 0.6, fill)
    f.__name__ = name
    return f

SFX_BUILDERS = dict(
    soft_whoosh_in=(soft_whoosh_in, 0.30, "Entry whoosh: 600-3000 Hz noise swell, fast cutoff at the end."),
    soft_whoosh_out=(soft_whoosh_out, 0.30, "Exit whoosh: reversed envelope (quick suck, slow trailing decay)."),
    swish_draw=(swish_draw, 0.45, "Draw-on swish: noise through 800->2400 Hz swept band-pass."),
    card_flip=(card_flip, 0.18, "Two quick filtered-noise card flaps 50 ms apart."),
    paper_slide=(paper_slide, 0.40, "Pink-noise paper slide (HP 1 kHz) with tiny crackle grains."),
    wood_knock=(wood_knock, 0.20, "Knock: 220+520 Hz decaying sines with a noise click."),
    metal_tink=(metal_tink, 0.40, "Inharmonic metal ping 1.2/2.9/4.1 kHz, fast decay."),
    glass_tink=(glass_tink, 0.35, "Glass ping: 2.6+3.9 kHz sine pair, soft attack, short ring."),
    thump_soft=(thump_soft, 0.25, "Soft low thump: 90->60 Hz falling sine."),
    pop_soft=(pop_soft, 0.12, "v1 pop an octave down, softer attack; use at -6 dB mix gain."),
    click_soft=(click_soft, 0.04, "Tiny 3 kHz click through a low-pass."),
    ding_soft=(ding_soft, 0.60, "Soft 880 Hz bell ding with harmonics."),
    riser_short=(riser_short, 0.70, "Quick riser: swept noise + 200->900 Hz sine, rising envelope."),
    low_boom=(low_boom, 0.90, "45 Hz sine thump with a sub-noise tail."),
    whip=(whip, 0.20, "Fast whip crack: noise sweep 5200->900 Hz, sharp attack."),
    bicycle_bell=(bicycle_bell, 0.40, "Two bright 2.6 kHz bell strikes with hammer ticks."),
    boxing_bell=(boxing_bell, 1.00, "Three fast metallic rings (inharmonic 760 Hz bell)."),
    camera_shutter=(camera_shutter, 0.15, "Shutter click + mechanical clack + mirror slap."),
    chain_rattle=(chain_rattle, 0.60, "Random metallic pings over a bright rattle bed."),
    chalk=(chalk, 0.60, "Scratchy chalk strokes: band-passed noise with stick-slip AM."),
    cleanroom_hum=(_loop_gen("cleanroom_hum", _fill_cleanroom), 4.0, "Steady airflow hiss + 60/120/180 Hz hum; seamless 4 s loop."),
    construction=(_loop_gen("construction", _fill_construction), 4.0, "Distant hammering + alternating reverse-alarm beeps over site rumble; loop."),
    crowd_cheer=(crowd_cheer, 2.0, "Formant-band roar with clap grains and whistle chirps."),
    crowd_murmur=(_loop_gen("crowd_murmur", _fill_crowd_murmur), 4.0, "Layered formant-filtered noise babble with slow swells; loop."),
    dice=(dice, 0.80, "Dice rattle then two settling clacks."),
    door_creak=(door_creak, 0.70, "Slow pitch-wobbling saw through a band-pass, stick-slip AM."),
    engine_sputter=(engine_sputter, 1.20, "Irregular low pops, gaps widening, fading out."),
    factory_line=(_loop_gen("factory_line", _fill_factory_line), 4.0, "Clunk every 0.5 s + 100 Hz motor hum + pneumatic hisses; loop."),
    harbor=(_loop_gen("harbor", _fill_harbor), 4.0, "Gull chirps over slow water wash; loop."),
    heartbeat=(heartbeat, 0.80, "Lub-dub: two low swept thumps."),
    jet_idle=(_loop_gen("jet_idle", _fill_jet_idle), 4.0, "1250 Hz whine with vibrato over low rumble; loop."),
    marker_squeak=(marker_squeak, 0.40, "Dry-erase squeak: wobbling 2.9 kHz tone + rasp."),
    news_sting=(news_sting, 1.20, "Three rising synth stabs (A minor -> open) with sub hit and shimmer."),
    rewind_tape=(rewind_tape, 1.00, "Pitched-up warble: exponential rise + fast vibrato."),
    sewing=(_loop_gen("sewing", _fill_sewing), 4.0, "12 Hz needle tick over a 120 Hz sewing-machine motor; loop."),
    shutter_open=(shutter_open, 0.60, "Roller-shutter rattle accelerating up, ending in a clank."),
    shutter_slam=(shutter_slam, 0.60, "Roller-shutter rattle starting with a clank, dying down."),
    street_traffic=(_loop_gen("street_traffic", _fill_street_traffic), 4.0, "Traffic bed, two doppler motorbike passes, horns; loop."),
    thunder=(thunder, 1.50, "Crack then rolling low rumble with sub tail."),
    vault_lock=(vault_lock, 0.80, "Heavy clunk, bolt slide with detent ticks, lock-home click."),
    wood_crash=(wood_crash, 0.90, "Board break: crack, splinter pops, body thud, splatter."),
    riser=(riser, 1.00, "Long strong riser (film impact lead-in): noise sweep + 220->1100 Hz + rising sub."),
)

# ============================================================== 4.3 CHAPTER MUSIC
def mid(m): return 440 * 2 ** ((m - 69) / 12)
def kal(f, ln=.5, tau=.16):                # kalimba-like pluck (v1 music_bed)
    tt = T(ln); idx = 3.0 * np.exp(-tt / .02)
    s = np.sin(2 * np.pi * f * tt + idx * np.sin(2 * np.pi * f * 3.0 * tt)) * np.exp(-tt / tau)
    s += 0.2 * np.sin(2 * np.pi * f * 4.0 * tt) * np.exp(-tt / .03)
    return s * np.clip(tt / .002, 0, 1)
def mpluck(f, ln, tau):                    # soft pentatonic pluck
    tt = T(ln)
    s = np.sin(2 * np.pi * f * tt) * np.exp(-tt / tau)
    s += 0.35 * np.sin(2 * np.pi * f * 2 * tt) * np.exp(-tt / (tau * 0.5))
    s += 0.12 * np.sin(2 * np.pi * f * 3.1 * tt) * np.exp(-tt / (tau * 0.3))
    return s * np.clip(tt / 0.004, 0, 1)
def mpad(fs, ln, f_snap):                  # sustained pad; f_snap = cycles-per-loop snap
    tt = T(ln); y = np.zeros_like(tt)
    for f in fs:
        fk = round(f * f_snap) / f_snap if f_snap else f
        y += np.sin(2 * np.pi * fk * tt) + 0.6 * np.sin(2 * np.pi * fk * 1.004 * tt)
    e = np.clip(tt / 0.35, 0, 1) * np.clip((ln - tt) / 0.5, 0, 1)
    return lp(y * e * 0.5, 1200)
def msaw(f, ln, cutoff, tau):              # staccato string stab
    tt = T(ln)
    s = sg.sawtooth(f * tt) + 0.95 * sg.sawtooth(f * 1.008 * tt)
    return lp(s * np.exp(-tt / tau) * np.clip(tt / 0.006, 0, 1), cutoff)
def mmarimba(f, ln, tau):                  # bright marimba bar
    tt = T(ln)
    y = (np.sin(2 * np.pi * f * tt) * np.exp(-tt / tau)
         + 0.4 * np.sin(2 * np.pi * f * 2 * tt) * np.exp(-tt / (tau * 0.5))
         + 0.12 * np.sin(2 * np.pi * f * 3 * tt) * np.exp(-tt / (tau * 0.25)))
    tr = hp(noise(0.012), 3000) * expenv(nlen(0.012), 0.004, 0.0005) * 0.12
    y[:min(len(tr), len(y))] += tr[:min(len(tr), len(y))]
    return y
def mpiano(f, ln, tau):                    # piano-ish sine stack
    tt = T(ln); y = np.zeros_like(tt)
    for r, a, dsc in [(1, 1, 1), (2, 0.42, 0.55), (3, 0.2, 0.4), (4.01, 0.09, 0.3), (5.3, 0.05, 0.25)]:
        y += a * np.sin(2 * np.pi * f * r * tt + r) * np.exp(-tt / (tau * dsc))
    tr = hp(noise(0.012), 1500) * expenv(nlen(0.012), 0.004, 0.0008)
    y[:min(len(tr), len(y))] += 0.06 * tr[:min(len(tr), len(y))]
    return y * np.clip(tt / 0.003, 0, 1)
def mshaker(ln=0.05, fc=6000):
    return hp(noise(ln), fc) * expenv(nlen(ln), 0.012, 0.002)
def mclap(ln=0.16):
    tt = T(ln)
    y = bp(noise(ln), 700, 2800) * expenv(nlen(ln), 0.05, 0.002)
    y += 0.5 * bp(noise(ln), 2500, 6000) * expenv(nlen(ln), 0.02, 0.001)
    return y
def mbass(m, ln, sub=0.25):
    tt = T(ln)
    s = np.sin(2 * np.pi * mid(m) * tt) * np.exp(-tt / (ln / 2.2))
    s += sub * np.sin(2 * np.pi * mid(m - 12) * tt) * np.exp(-tt / (ln / 1.8))
    return lp(s, 700) * np.clip(tt / 0.006, 0, 1)

def music_track(name, bpm, bars, fill, xf=1.0, peak_db=-12.0):
    """one seamless looped piece; fill(add, buf, beat) places events on the beat grid.
    add() wraps events from the first xf seconds into the tail for loopify."""
    spb = int(round(60.0 / bpm * SR))
    L = spb * 4 * bars
    d = L / SR
    n = int(xf * SR + 1e-6)
    buf = np.zeros(L + n)
    beat = spb / SR
    def add(snd, t0, g=1.0):
        place(buf, snd, t0, g)
        if t0 < xf:
            place(buf, snd, t0 + d, g)
    fill(add, buf, beat)
    y = loopify(buf, xf)
    return save(name, y, d, peak_db=peak_db, fade=0.0, out=MUSIC_OUT)

def fill_somber(add, buf, beat):
    bars = 24
    prog = [(45, [57, 60, 64]), (41, [53, 57, 60]), (43, [55, 59, 62]), (45, [57, 60, 64])]  # Am F G Am
    pent = [57, 60, 62, 64, 67, 69, 72]
    d = bars * 4 * beat                                             # loop period (s), for cycle snapping
    mel = [0, 2, 1, 4, 3, 1, 2, 5, 4, 0, 3, 2, 5, 4, 2, 1, 3, 0, 4, 2, 1, 5, 3, 2]
    for bar in range(bars):
        root, tones = prog[bar % 4]
        t0 = bar * 4 * beat
        add(mpad([mid(root), mid(root + 7)], 4 * beat + 0.5, d), t0, 0.5)
        if bar % 2 == 0:
            add(mbass(root - 12, 2 * beat, sub=0.5), t0, 0.5)
        m = mel[bar % len(mel)]
        f = mid(pent[m % len(pent)] + (12 if bar % 8 < 4 else 0))
        add(mpluck(f, 1.8 * beat, 0.5), t0, 0.5)
        if bar % 4 == 1:
            add(mpluck(mid(pent[(m + 2) % len(pent)] + 12), 1.2 * beat, 0.4), t0 + 2.5 * beat, 0.3)
        if bar % 4 == 3:
            add(mpluck(f * 2, 2.0 * beat, 0.5), t0 + 2 * beat, 0.25)
    buf[:] += 0.004 * lp(noise(len(buf) / SR), 400)               # faint tape warmth

def fill_hopeful(add, buf, beat):
    bars = 24
    prog = [(48, [48, 52, 55, 59]), (43, [43, 47, 50, 54]), (45, [45, 48, 52, 57]), (41, [41, 45, 48, 53])]
    arp_idx = [0, 1, 2, 3, 2, 1, 2, 3]
    for bar in range(bars):
        root, tones = prog[bar % 4]
        t0 = bar * 4 * beat + 0.05                                    # grid offset keeps transients off the seam
        add(mbass(root - 12, 1.8 * beat, sub=0.3), t0, 0.5)
        add(mbass(root - 5, 1.2 * beat, sub=0.2), t0 + 2 * beat, 0.35)
        for i in range(8):                                         # kalimba 8th arpeggio
            m = tones[arp_idx[i % 8]] + (12 if bar % 2 == 0 else 24)
            add(kal(mid(m), 4 * beat, 0.35), t0 + i * beat / 2, 0.5 if i % 2 == 0 else 0.32)
        for i in range(16):                                        # light shaker 16ths
            g = 0.16 if i % 4 == 2 else (0.08 if i % 2 == 0 else 0.05)
            add(mshaker(), t0 + i * beat / 4, g)
        if bar % 8 == 7:
            for m in tones: add(kal(mid(m + 24), 3 * beat, 0.6), t0 + 2 * beat, 0.18)

def fill_upbeat(add, buf, beat):
    bars = 32
    prog = [(48, [48, 52, 55, 60]), (43, [43, 47, 50, 54]), (45, [45, 48, 52, 57]), (41, [41, 45, 48, 53])]
    penta = [60, 62, 64, 67, 69, 72, 74, 76]
    walk = 3; mr = np.random.default_rng(5)
    for bar in range(bars):
        root, tones = prog[bar % 4]
        t0 = bar * 4 * beat
        pat = [1, 0, 1, 1, 0, 1, 1, 0] if bar % 2 == 0 else [1, 1, 0, 1, 0, 1, 1, 1]
        for i, on in enumerate(pat):
            if not on: continue
            if i == 0 and bar % 4 == 0: m = tones[2] + 12
            else:
                walk = int(np.clip(walk + mr.choice([-3, -2, -1, 1, 1, 2, 3]), 0, len(penta) - 1))
                m = penta[walk]
            add(mmarimba(mid(m), 3 * beat, 0.28), t0 + i * beat / 2, 0.5 if i % 2 == 0 else 0.35)
        for bpos in (0, 1.5, 2, 3.5):
            add(mbass(root - 12 + (7 if bpos == 1.5 else 0), 0.9 * beat, sub=0.4), t0 + bpos * beat, 0.55)
        for i in range(8):                                          # offbeat marimba chord stab
            if i % 4 == 2:
                add(mmarimba(mid(tones[0] + 24), 2 * beat, 0.16), t0 + i * beat / 2, 0.22)
        add(mclap(), t0 + 1 * beat, 0.5)                            # claps on 2 & 4
        add(mclap(), t0 + 3 * beat, 0.55)
        add(mclap()[:nlen(0.05)], t0 + 3.75 * beat, 0.2)
        for i in range(16):
            add(mshaker(), t0 + i * beat / 4, 0.10 if i % 2 == 0 else 0.05)

def fill_tension(add, buf, beat):
    bars = 30
    ost = [38, 38, 38, 38, 34, 34, 36, 36]                          # Dm x4, Bb x2, C x2
    for bar in range(bars):
        root = ost[bar % 8]
        t0 = bar * 4 * beat + 0.06                                    # grid off the seam (see music_hopeful)
        for i in range(8):                                          # staccato 8th ostinato
            f = mid(root - (12 if i % 4 == 0 else 0))
            add(msaw(f, 0.16, 380, 0.06), t0 + i * beat / 2, 0.42 if i % 2 == 0 else 0.3)
        for i in range(16):                                         # ticking hi-hat
            tick = hp(noise(0.03), 7500) * expenv(nlen(0.03), 0.008, 0.001)
            add(tick, t0 + i * beat / 4, 0.14 if i % 4 == 2 else 0.07)
        if bar % 8 == 3:                                            # accent stab
            for m in (root + 12, root + 15, root + 19):
                add(msaw(mid(m), 0.3, 1400, 0.1), t0 + 3.5 * beat, 0.3)
        if bar % 8 == 7:
            add(mbass(root - 24, 2 * beat, sub=0.6), t0 + 2 * beat, 0.5)
    t = np.arange(len(buf)) / SR
    buf[:] += 0.02 * lp(noise(len(buf) / SR), 250) * (0.6 + 0.4 * np.sin(2 * np.pi * 2 * t))

def fill_reflective(add, buf, beat):
    bars = 24
    p4 = [(41, [53, 57, 60]), (48, [52, 55, 60]), (55, [55, 59, 62]), (57, [57, 60, 64])]
    end = [(41, [53, 57, 60]), (55, [55, 59, 62]), (48, [52, 55, 60]), (48, [48, 52, 55, 60, 64])]
    prog = (p4 * 5) + end                                            # resolves to C at the loop end
    melody = [72, None, 74, 72, 76, None, 72, 69, 71, None, 72, 74, 76, 79, None, 76, 74, 72, None, 74, 72, 69, None, None]
    for bar in range(bars):
        root, tones = prog[bar]
        t0 = bar * 4 * beat + 0.06                                    # grid off the seam (see music_hopeful)
        ln = 5.0
        for j, m in enumerate(tones):                               # rolled chord
            add(mpiano(mid(m + 12), ln, 1.1), t0 + j * 0.03, 0.30)
        add(mbass(root - 12, 3.2 * beat, sub=0.35), t0, 0.4)
        mi = melody[bar % len(melody)]
        if mi:
            add(mpiano(mid(mi), 2.6 * beat, 0.8), t0 + 2 * beat, 0.4)
            add(mpiano(mid(mi), 1.2 * beat, 0.4), t0 + 2 * beat + 0.75 * beat, 0.14)  # soft delay
        if bar % 4 == 2:
            add(mpiano(mid(tones[1] + 24), 1.8 * beat, 0.5), t0 + 3 * beat, 0.12)
    t = np.arange(len(buf)) / SR
    buf[:] += 0.003 * lp(noise(len(buf) / SR), 1000)

MUSIC_BUILDERS = [
    ("music_somber", 72, 24, fill_somber, "Slow 72 BPM A-minor loop: sparse pentatonic plucks over a low pad + bass (1986 hardship)."),
    ("music_hopeful", 92, 24, fill_hopeful, "92 BPM major loop: kalimba 8th arpeggios, soft bass, light shaker (Doi Moi reforms)."),
    ("music_upbeat", 110, 32, fill_upbeat, "110 BPM bright marimba ostinato + bass + claps + shaker (FDI/Samsung boom)."),
    ("music_tension", 100, 30, fill_tension, "100 BPM staccato low-string ostinato (saw through low-pass) + ticking hi-hat (trade war)."),
    ("music_reflective", 80, 24, fill_reflective, "80 BPM piano-like sines with soft delay; 24-bar cycle ending resolved on C (trap/ending)."),
]

# ============================================================== main
def append_index():
    idx = os.path.join(OUT, "INDEX.md")
    old = open(idx).read() if os.path.exists(idx) else "# SFX index\n\n| name | duration (s) | description |\n|---|---|---|\n"
    rows = []
    for n, (fn, d, desc) in SFX_BUILDERS.items():
        if f"\n| {n} |" not in old:
            rows.append(f"| {n} | {d} | {desc} |")
    for n, bpm, bars, fill, desc in MUSIC_BUILDERS:
        spb = int(round(60.0 / bpm * SR)); d = spb * 4 * bars / SR
        if f"\n| {n} (" not in old:
            rows.append(f"| {n} (../music/{n}.wav) | {d:.1f} | {desc} |")
    if rows:
        with open(idx, "a") as f:
            f.write("\n".join(rows) + "\n")
        print(f"  INDEX.md: appended {len(rows)} rows")
    else:
        print("  INDEX.md: already complete, nothing appended")

def main():
    reseed()
    print("SFX v2:")
    for name, (fn, d, desc) in SFX_BUILDERS.items():
        is_loop = name in ("cleanroom_hum", "construction", "crowd_murmur", "factory_line",
                           "harbor", "jet_idle", "sewing", "street_traffic")
        x = fn()
        save(name, x, d, fade=0.0 if is_loop else 0.004)
    print("Music v2:")
    for name, bpm, bars, fill, desc in MUSIC_BUILDERS:
        music_track(name, bpm, bars, fill, xf=1.0)
    append_index()
    print("done")

if __name__ == "__main__":
    main()
