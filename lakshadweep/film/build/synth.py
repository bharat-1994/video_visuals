"""Small numpy/scipy synthesizer: instruments, environment SFX, reverb.
Everything returns float32 arrays at SR. Stereo buses are shape (2, N)."""
import numpy as np, scipy.signal as sg

SR = 48000
rng = np.random.default_rng(11)

NOTE = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6,
        'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def hz(name):
    """'D4' -> Hz (A4=440)."""
    if isinstance(name, (int, float)):
        return float(name)
    p = name[:-1]
    o = int(name[-1])
    m = NOTE[p] + 12 * (o + 1)
    return 440.0 * 2 ** ((m - 69) / 12)


# ---------------------------------------------------------------- filters
def lp(x, fc, order=2):
    return sg.sosfilt(sg.butter(order, fc, 'low', fs=SR, output='sos'), x)


def hp(x, fc, order=2):
    return sg.sosfilt(sg.butter(order, fc, 'high', fs=SR, output='sos'), x)


def bp(x, lo, hi, order=2):
    return sg.sosfilt(sg.butter(order, [lo, hi], 'band', fs=SR, output='sos'), x)


def white(n):
    return rng.standard_normal(n).astype(np.float32)


def pink(n):
    f = np.fft.rfft(rng.standard_normal(n))
    k = np.arange(len(f)); k[0] = 1
    f = f / np.sqrt(k)
    x = np.fft.irfft(f, n)
    return (x / np.std(x)).astype(np.float32)


def tt(n):
    return np.arange(n) / SR


def smooth_env(points, n):
    """Piecewise-linear envelope through [(t_sec, value)...] sampled to n samples."""
    ts = np.array([p[0] for p in points]); vs = np.array([p[1] for p in points])
    return np.interp(tt(n), ts, vs).astype(np.float32)


def adsr(n, a, d, s, r):
    e = np.ones(n, np.float32)
    na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    na = min(na, n); e[:na] = np.linspace(0, 1, na, endpoint=False) ** 1.5 if na else 1
    nd = min(nd, n - na)
    if nd > 0:
        e[na:na + nd] = np.linspace(1, s, nd)
    e[na + nd:] = s
    if nr > 0 and nr < n:
        e[-nr:] *= np.linspace(1, 0, nr) ** 1.5
    return e


def pan(x, p):
    """mono -> stereo (2,N), p in [-1,1], equal power."""
    a = (p + 1) * np.pi / 4
    return np.stack([x * np.cos(a), x * np.sin(a)]).astype(np.float32)


def place(bus, x, t0, gain=1.0):
    """Add (2,N) or (N,) clip into bus (2,M) at t0 seconds."""
    i = int(t0 * SR)
    if x.ndim == 1:
        x = np.stack([x, x])
    if i >= bus.shape[1]:
        return
    if i < 0:
        x = x[:, -i:]; i = 0
    n = min(x.shape[1], bus.shape[1] - i)
    bus[:, i:i + n] += x[:, :n] * gain


# ---------------------------------------------------------------- reverb
def make_ir(t60=3.2, seed=3, bright=0.55, pre=0.02):
    r = np.random.default_rng(seed)
    n = int(t60 * 1.3 * SR)
    out = np.zeros((2, n), np.float32)
    for ch in range(2):
        x = r.standard_normal(n)
        t = np.arange(n) / SR
        lo = lp(x, 900) * np.exp(-6.9 * t / (t60 * 1.15))
        mid = bp(x, 900, 4000) * np.exp(-6.9 * t / (t60 * 0.8)) * bright
        hi = hp(x, 4000) * np.exp(-6.9 * t / (t60 * 0.4)) * bright * 0.5
        ir = lo + mid + hi
        k = int(pre * SR)
        ir = np.concatenate([np.zeros(k), ir])[:n]
        ir[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
        out[ch] = ir / np.sqrt(np.sum(ir ** 2))
    return out


def reverb(bus, ir, wet=1.0):
    l = sg.oaconvolve(bus[0], ir[0])[:bus.shape[1]]
    r = sg.oaconvolve(bus[1], ir[1])[:bus.shape[1]]
    return (np.stack([l, r]) * wet).astype(np.float32)


# ---------------------------------------------------------------- instruments (mono)
def ks(freq, dur, t60=6.0, bright=0.6, seed=None):
    """Karplus-Strong string via lfilter (fast)."""
    n = int(dur * SR)
    N = max(2, int(round(SR / freq)))
    r = np.random.default_rng(seed) if seed is not None else rng
    exc = r.standard_normal(N)
    exc = lp(exc, 600 + 8000 * bright, 1)
    exc -= exc.mean()
    exc /= np.max(np.abs(exc)) + 1e-9
    x = np.zeros(n); x[:N] = exc
    g = 10 ** (-3.0 / (freq * t60))
    a = np.zeros(N + 2); a[0] = 1; a[N] = -0.5 * g; a[N + 1] = -0.5 * g
    y = sg.lfilter([1.0], a, x)
    return y.astype(np.float32)


def tanpura_string(freq, dur=7.0, seed=None):
    y = ks(freq, dur, t60=9.0, bright=0.85, seed=seed)
    # jivari "buzz": mild soft clip adds odd harmonics that bloom over time
    env = np.linspace(0.2, 1.0, len(y)) ** 0.8
    y = np.tanh(y * (1 + 4 * env)) * 0.9
    return y.astype(np.float32)


def piano(freq, dur=4.0, vel=0.7):
    n = int(dur * SR); t = tt(n)
    y = np.zeros(n)
    B = 0.00025
    for k in range(1, 10):
        f = freq * k * np.sqrt(1 + B * k * k)
        if f > 9000:
            break
        amp = (1.0 / k ** 1.15) * (0.6 + 0.4 * vel)
        dec = 2.8 / (k ** 0.75) * (1 + freq / 600) ** -0.5 + 0.2
        y += amp * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) * np.exp(-t / dec)
    y *= 1 - np.exp(-t / 0.002)
    hammer = lp(white(n), 2500) * np.exp(-t / 0.012) * 0.15 * vel
    y = y + hammer
    y /= np.max(np.abs(y)) + 1e-9
    return (y * vel).astype(np.float32)


def bell(freq, dur=5.0, vel=0.6):
    """glassy mallet bell: inharmonic partials, long ring (used for coral growth)."""
    n = int(dur * SR); t = tt(n)
    y = np.zeros(n)
    for ratio, amp, dec in [(1, 1, 3.2), (2.76, 0.45, 1.8), (5.4, 0.2, 1.0), (8.93, 0.08, 0.5)]:
        y += amp * np.sin(2 * np.pi * freq * ratio * t) * np.exp(-t / dec)
    y *= 1 - np.exp(-t / 0.0015)
    y /= np.max(np.abs(y)) + 1e-9
    return (y * vel).astype(np.float32)


def flute(freq, dur, vel=0.7, glide_from=None, vib=1.0):
    """Breathy bansuri-like flute."""
    n = int(dur * SR); t = tt(n)
    f = np.full(n, freq, np.float64)
    if glide_from:
        g = np.exp(-t / 0.07)
        f = freq * (glide_from / freq) ** g
    depth = np.clip((t - 0.35) / 0.5, 0, 1) * 0.006 * vib
    f = f * (1 + depth * np.sin(2 * np.pi * 5.1 * t + 0.4))
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) + 0.30 * np.sin(2 * ph) + 0.10 * np.sin(3 * ph) + 0.04 * np.sin(4 * ph)
    env = adsr(n, 0.09, 0.15, 0.82, min(0.45, dur * 0.4))
    tremor = 1 + 0.06 * vib * np.sin(2 * np.pi * 4.7 * t) * np.clip((t - 0.3) / 0.6, 0, 1)
    breath = bp(white(n), max(200, freq * 1.5), min(9000, freq * 6)) * 0.22
    chiff = bp(white(n), freq * 2, freq * 5) * np.exp(-t / 0.06) * 0.25
    out = (y * 0.5 + breath) * env * tremor + chiff
    return (out * vel * 0.8).astype(np.float32)


def pad_note(freq, dur, vel=0.5, bright=1500.0, vib=0.0, stereo=True):
    """detuned-saw string pad (stereo (2,N))."""
    n = int(dur * SR); t = tt(n)
    chans = []
    for side in (0, 1):
        y = np.zeros(n)
        for d in ((-7, -2, 4, 9) if side == 0 else (-9, -4, 2, 7)):
            f = freq * 2 ** (d / 1200)
            if vib:
                f = f * (1 + 0.004 * vib * np.sin(2 * np.pi * 5.0 * t + d))
                ph = 2 * np.pi * np.cumsum(f) / SR
            else:
                ph = 2 * np.pi * f * t + d
            y += sg.sawtooth(ph) * 0.25
        y = lp(y, min(bright, SR * 0.4), 2)
        chans.append(y)
    y = np.stack(chans)
    a = min(2.2, dur * 0.4); r = min(3.0, dur * 0.5)
    env = adsr(n, a, 0.3, 0.9, r)
    return (y * env * vel * 0.6).astype(np.float32)


def sub(freq, dur, vel=0.6, a=0.6, r=1.5):
    n = int(dur * SR); t = tt(n)
    y = np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(4 * np.pi * freq * t)
    return (y * adsr(n, a, 0.2, 0.9, r) * vel * 0.7).astype(np.float32)


def boom(f0=90.0, f1=32.0, dur=3.5, vel=0.8):
    n = int(dur * SR); t = tt(n)
    f = f1 + (f0 - f1) * np.exp(-t / 0.35)
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t / 1.4)
    y += lp(white(n), 220) * np.exp(-t / 0.5) * 0.7
    y += lp(white(n), 2500) * np.exp(-t / 0.05) * 0.25
    y *= 1 - np.exp(-t / 0.003)
    return (y / (np.max(np.abs(y)) + 1e-9) * vel).astype(np.float32)


def frame_drum(vel=0.6, f=95.0, size=0.5):
    n = int(size * SR); t = tt(n)
    fr = f * (1 + 0.9 * np.exp(-t / 0.02))
    ph = 2 * np.pi * np.cumsum(fr) / SR
    y = np.sin(ph) * np.exp(-t / 0.16)
    y += bp(white(n), 180, 1400) * np.exp(-t / 0.04) * 0.5
    y *= 1 - np.exp(-t / 0.002)
    return (y / (np.max(np.abs(y)) + 1e-9) * vel).astype(np.float32)


def dhol_hi(vel=0.4):
    n = int(0.25 * SR); t = tt(n)
    y = np.sin(2 * np.pi * 210 * t * (1 + 0.5 * np.exp(-t / 0.015))) * np.exp(-t / 0.07)
    y += bp(white(n), 800, 3500) * np.exp(-t / 0.02) * 0.4
    return (y / (np.max(np.abs(y)) + 1e-9) * vel).astype(np.float32)


def shaker(vel=0.3):
    n = int(0.12 * SR); t = tt(n)
    y = hp(white(n), 5500) * np.exp(-t / 0.03) * (1 - np.exp(-t / 0.006))
    return (y / (np.max(np.abs(y)) + 1e-9) * vel).astype(np.float32)


def tick(vel=0.3):
    n = int(0.06 * SR); t = tt(n)
    y = bp(white(n), 2500, 6000) * np.exp(-t / 0.006) + np.sin(2 * np.pi * 1900 * t) * np.exp(-t / 0.01) * 0.5
    return (y / (np.max(np.abs(y)) + 1e-9) * vel).astype(np.float32)


def clap(vel=0.4):
    n = int(0.3 * SR); t = tt(n)
    y = bp(white(n), 900, 3800) * (np.exp(-t / 0.03) + 0.6 * np.exp(-np.clip(t - 0.012, 0, None) / 0.05) * (t > 0.012))
    return (y / (np.max(np.abs(y)) + 1e-9) * vel).astype(np.float32)


def sweep_noise(dur, f0, f1, q=3.0, vel=0.5, shape='in'):
    """whoosh/riser: noise through a swept resonant band-pass. shape 'in' ramps up, 'out' ramps down, 'swell' both."""
    n = int(dur * SR)
    x = white(n)
    block = 512
    y = np.zeros(n, np.float32)
    zi = None
    for i in range(0, n, block):
        frac = i / max(n - 1, 1)
        fc = f0 * (f1 / f0) ** frac
        fc = min(fc, SR * 0.45)
        bw = fc / q
        lo = max(30.0, fc - bw / 2); hi = min(SR * 0.47, fc + bw / 2)
        sos = sg.butter(2, [lo, hi], 'band', fs=SR, output='sos')
        if zi is None:
            zi = np.zeros((sos.shape[0], 2))
        seg, zi = sg.sosfilt(sos, x[i:i + block], zi=zi)
        y[i:i + block] = seg
    t = np.linspace(0, 1, n)
    if shape == 'in':
        env = t ** 2.2
    elif shape == 'out':
        env = (1 - t) ** 1.8
    else:
        env = np.sin(np.pi * t) ** 1.6
    y = y * env
    return (y / (np.max(np.abs(y)) + 1e-9) * vel).astype(np.float32)


# ---------------------------------------------------------------- environment SFX (stereo)
def ocean(dur, level=1.0, surf=1.0, seed=1, period=(7.5, 11.5)):
    """Wave wash: pink noise with random swells; stereo-decorrelated."""
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    out = np.zeros((2, n), np.float32)
    for ch in range(2):
        base = lp(pink(n), 1800) * 0.25
        foam = hp(pink(n), 3500) * 0.12
        env = np.full(n, 0.35, np.float32)
        t = 0.0
        t += r.uniform(0, 4) + ch * 1.7
        while t < dur + 12:
            T = r.uniform(*period)
            a = r.uniform(2.0, 3.5)
            idx0 = int(t * SR)
            m = int((a + T * 0.6) * SR)
            x = np.arange(m) / SR
            wave = np.where(x < a, (x / a) ** 1.8, np.exp(-(x - a) / (T * 0.28)))
            amp = r.uniform(0.6, 1.0)
            if idx0 < n:
                seg = wave[:max(0, min(m, n - idx0))]
                env[idx0:idx0 + len(seg)] += amp * seg
            t += T * r.uniform(0.7, 1.0)
        # foam hiss follows the crest a little later
        env2 = np.roll(env, int(0.6 * SR))
        out[ch] = (base * (0.4 + env) + foam * env2 * surf) * level
    return out


def wind(dur, level=1.0, gust=0.5, seed=2):
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    out = np.zeros((2, n), np.float32)
    for ch in range(2):
        x = pink(n)
        bandA = bp(x, 250, 700) * 0.6
        bandB = bp(x, 700, 1800) * 0.3
        # slow gust envelope
        k = max(4, int(dur / 3.5))
        pts = np.interp(np.linspace(0, k, n), np.arange(k + 1), r.uniform(0.25, 1.0, k + 1))
        mix = 0.25 + gust * pts
        out[ch] = (bandA * mix + bandB * mix * mix) * level
    return out


def gull(f0=1700.0, dur=1.1, vel=0.3):
    n = int(dur * SR); t = tt(n)
    sig = np.zeros(n)
    t0 = 0.0
    for k, (cdur, f1) in enumerate([(0.28, 1.0), (0.25, 1.12), (0.35, 0.95)]):
        i0 = int(t0 * SR); m = int(cdur * SR)
        x = np.arange(m) / SR / cdur
        f = f0 * f1 * (0.9 + 0.55 * np.sin(np.pi * x) ** 0.8 - 0.25 * x)
        ph = 2 * np.pi * np.cumsum(f) / SR
        y = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)
        y *= np.sin(np.pi * x) ** 0.7 * (1 + 0.35 * np.sin(2 * np.pi * 38 * x * cdur))
        if i0 + m <= n:
            sig[i0:i0 + m] += y
        t0 += cdur + 0.08
    sig = bp(sig, 700, 6500)
    return (sig / (np.max(np.abs(sig)) + 1e-9) * vel).astype(np.float32)


def bubbles(dur, density=6.0, vel=0.2, seed=5):
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    out = np.zeros(n, np.float32)
    for _ in range(int(dur * density)):
        t0 = r.uniform(0, dur - 0.2)
        f0 = r.uniform(350, 1100); m = int(r.uniform(0.04, 0.11) * SR)
        x = np.arange(m) / SR
        f = f0 * (1 + 8 * x)
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / 0.025)
        i0 = int(t0 * SR)
        out[i0:i0 + m] += y[:max(0, min(m, n - i0))] * r.uniform(0.3, 1) * vel
    return out


def underwater(dur, level=1.0, seed=6):
    n = int(dur * SR)
    rum = lp(pink(n), 180) * 0.8
    mu = lp(pink(n), 700) * 0.3
    sw = smooth_env([(0, 0.6), (dur * 0.5, 1.0), (dur, 0.7)], n)
    base = (rum + mu) * sw * level
    b = bubbles(dur, 5.0, 0.16, seed)
    return np.stack([base + b, np.roll(base, 400) + np.roll(b, 220)]).astype(np.float32)


def ping(freq=1175.0, vel=0.25, dur=3.0):
    n = int(dur * SR); t = tt(n)
    y = np.sin(2 * np.pi * freq * t) * np.exp(-t / 0.55) + 0.4 * np.sin(2 * np.pi * freq * 1.5 * t) * np.exp(-t / 0.3)
    y *= 1 - np.exp(-t / 0.002)
    return (y * vel).astype(np.float32)


def thunder(dur=5.0, vel=0.7, seed=9):
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = tt(n)
    x = lp(white(n), 160, 2) * 1.0
    x2 = lp(white(n), 700, 1) * 0.35
    env = np.zeros(n, np.float32)
    ev = r.uniform(0, dur * 0.6, 5)
    ev.sort()
    for e in ev:
        i0 = int(e * SR); m = min(n - i0, int(r.uniform(1.0, 2.6) * SR))
        env[i0:i0 + m] += (np.exp(-np.arange(m) / SR / r.uniform(0.35, 0.9)) * r.uniform(0.4, 1))[:m]
    env = np.clip(env, 0, 1.3)
    env *= 1 - np.exp(-t / 0.05)
    y = (x + x2) * env
    return (y / (np.max(np.abs(y)) + 1e-9) * vel).astype(np.float32)


def rain(dur, level=0.5, seed=12):
    n = int(dur * SR)
    x = hp(white(n), 2500) * 0.12 + bp(white(n), 800, 2500) * 0.05
    return np.stack([x * level, np.roll(x, 800) * level]).astype(np.float32)


def splash(vel=0.35):
    n = int(0.55 * SR); t = tt(n)
    y = bp(white(n), 500, 6000) * np.exp(-t / 0.12) * (1 - np.exp(-t / 0.004))
    y += lp(white(n), 400) * np.exp(-t / 0.2) * 0.4
    return (y / (np.max(np.abs(y)) + 1e-9) * vel).astype(np.float32)


def creak(dur=0.9, vel=0.18, f=240.0):
    n = int(dur * SR); t = tt(n)
    x = white(n)
    block = 256
    y = np.zeros(n, np.float32)
    for i in range(0, n, block):
        fc = f * (1 + 0.5 * np.sin(2 * np.pi * 2.2 * i / SR) + 0.3 * np.sin(2 * np.pi * 7 * i / SR))
        sos = sg.butter(2, [fc * 0.9, fc * 1.1], 'band', fs=SR, output='sos')
        y[i:i + block] = sg.sosfilt(sos, x[i:i + block])
    env = np.sin(np.pi * t / dur) ** 0.8
    y *= env
    return (y / (np.max(np.abs(y)) + 1e-9) * vel).astype(np.float32)


def paper_flutter(dur=0.6, vel=0.15):
    n = int(dur * SR); t = tt(n)
    x = bp(white(n), 1500, 7000) * (np.random.rand(n) > 0.9) * np.exp(-t / 0.25)
    x = lp(x, 6000)
    return (x / (np.max(np.abs(x)) + 1e-9) * vel).astype(np.float32)


def cloth_flap(dur=3.0, vel=0.25, seed=13):
    """flag in wind: modulated bursts of band noise."""
    r = np.random.default_rng(seed)
    n = int(dur * SR); t = tt(n)
    x = bp(white(n), 120, 1400)
    m = np.clip(np.sin(2 * np.pi * 7.0 * t + 3 * np.sin(2 * np.pi * 0.9 * t)), 0, 1) ** 1.5
    y = x * (0.3 + m) * np.sin(np.pi * t / dur) ** 0.6
    return (y / (np.max(np.abs(y)) + 1e-9) * vel).astype(np.float32)


def static_noise(dur=1.0, vel=0.1):
    n = int(dur * SR)
    x = bp(white(n), 1000, 6000) * (np.random.rand(n) > 0.6)
    return (x * vel).astype(np.float32)
