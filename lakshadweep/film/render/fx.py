"""Cinematic effects: dust/plankton particles, god rays, caustics, light leaks."""
import math, functools
import numpy as np, cv2
from engine import W, H, smooth, lerp


@functools.lru_cache(None)
def _particles(seed, n):
    r = np.random.default_rng(seed)
    return dict(x=r.uniform(0, W, n), y=r.uniform(0, H, n), vx=r.uniform(-14, 14, n), vy=r.uniform(-9, 9, n),
                s=r.uniform(1.2, 5.0, n), ph=r.uniform(0, 6.28, n), z=r.uniform(0.3, 1.0, n))


def particles(img, T, seed=1, n=140, color=(255, 240, 210), strength=0.5, drift=(1.0, 1.0), blur=1.0):
    """soft floating motes (dust / plankton / snow). additive glow."""
    P = _particles(seed, n)
    sc = 0.5
    cv = np.zeros((int(H * sc), int(W * sc), 3), np.uint8)
    x = (P['x'] + P['vx'] * drift[0] * T * P['z'] + 18 * np.sin(T * 0.4 + P['ph'])) % W
    y = (P['y'] + P['vy'] * drift[1] * T * P['z'] + 12 * np.cos(T * 0.3 + P['ph'])) % H
    tw = 0.55 + 0.45 * np.sin(T * 1.7 + P['ph'] * 3)
    for i in range(n):
        a = tw[i] * P['z'][i]
        c = tuple(int(v * a) for v in color)
        cv2.circle(cv, (int(x[i] * sc), int(y[i] * sc)), max(1, int(P['s'][i] * sc * (0.6 + P['z'][i]))), c, -1, cv2.LINE_AA)
    g = cv2.GaussianBlur(cv, (0, 0), 2.5 * blur)
    layer = cv2.resize(cv2.addWeighted(cv, 0.6, g, 1.4, 0), (W, H), interpolation=cv2.INTER_LINEAR)
    return np.clip(img.astype(np.float32) + layer.astype(np.float32) * strength, 0, 255).astype(np.uint8)


@functools.lru_cache(None)
def _ray_tex(seed):
    r = np.random.default_rng(seed)
    w, h = 480, 270
    x = np.linspace(-1, 1, w)[None, :].repeat(h, 0)
    y = np.linspace(0, 1, h)[:, None].repeat(w, 1)
    tex = np.zeros((h, w), np.float32)
    for _ in range(14):
        a = r.uniform(-0.9, 0.9); wd = r.uniform(0.02, 0.09); amp = r.uniform(0.3, 1.0)
        center = a * (0.4 + 0.9 * y)           # rays fan out from the top
        tex += amp * np.exp(-((x - center) / (wd * (0.6 + y))) ** 2)
    tex *= (1 - y) ** 1.2
    tex = cv2.GaussianBlur(tex, (0, 0), 2)
    return tex / tex.max()


def god_rays(img, T, strength=0.35, color=(190, 235, 255), seed=2, speed=0.15):
    tex = _ray_tex(seed)
    shift = int(30 * math.sin(T * speed))
    t2 = np.roll(tex, shift, axis=1)
    t2 = t2 * (0.75 + 0.25 * np.sin(T * 0.6 + np.linspace(0, 6, tex.shape[1]))[None, :])
    layer = cv2.resize(t2, (W, H), interpolation=cv2.INTER_CUBIC)[..., None] * np.array(color, np.float32)[None, None, :]
    return np.clip(img.astype(np.float32) + layer * strength, 0, 255).astype(np.uint8)


@functools.lru_cache(None)
def _caustic_base():
    r = np.random.default_rng(5)
    n = r.random((90, 160)).astype(np.float32)
    n = cv2.resize(n, (640, 360), interpolation=cv2.INTER_CUBIC)
    n = cv2.GaussianBlur(n, (0, 0), 6)
    n = (n - n.min()) / (n.max() - n.min())
    return n


def caustics(img, T, strength=0.35, scale=1.0, color=(170, 240, 255)):
    b = _caustic_base()
    h, w = b.shape
    ox = int(T * 14) % w; oy = int(T * 9) % h
    a = np.roll(np.roll(b, ox, 1), oy, 0)
    b2 = np.roll(np.roll(b, -int(T * 11) % w, 1), int(T * 7) % h, 0)
    c = 1 - np.abs(a - b2) * 2.4          # bright net-like lines where the two layers cross
    c = np.clip(c, 0, 1) ** 6
    c = cv2.resize(c, (W, H), interpolation=cv2.INTER_CUBIC)[..., None]
    return np.clip(img.astype(np.float32) + c * np.array(color, np.float32) * strength, 0, 255).astype(np.uint8)


def light_leak(img, T, t0, dur, color=(255, 170, 90), strength=0.5, side='left'):
    if not (t0 <= T <= t0 + dur):
        return img
    u = (T - t0) / dur
    a = math.sin(math.pi * u) ** 2 * strength
    xx = np.linspace(0, 1, 64)[None, :].repeat(36, 0)
    yy = np.linspace(0, 1, 36)[:, None].repeat(64, 1)
    if side == 'left':
        m = np.exp(-((xx - 0.05 - 0.3 * u) / 0.25) ** 2) * (0.6 + 0.4 * yy)
    else:
        m = np.exp(-((xx - 0.95 + 0.3 * u) / 0.25) ** 2) * (0.6 + 0.4 * yy)
    m = cv2.resize(m.astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)[..., None]
    return np.clip(img.astype(np.float32) + m * np.array(color, np.float32) * a, 0, 255).astype(np.uint8)


def fade_black(img, a):
    return (img.astype(np.float32) * (1 - a)).astype(np.uint8) if a > 0.001 else img


def depth_haze(img, strength=0.25, color=(10, 40, 80)):
    """subtle top-down gradient tint (deep water)."""
    g = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    return np.clip(img.astype(np.float32) * (1 - 0.25 * g * strength) + np.array(color, np.float32) * g * strength * 0.5, 0, 255).astype(np.uint8)
