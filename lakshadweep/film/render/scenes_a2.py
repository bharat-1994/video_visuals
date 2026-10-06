"""Act 2 procedural scenes: ridge rising, coral polyps, time-lapse atoll growth (cross-section), top-down atoll ring."""
import math, functools
import numpy as np, cv2
from engine import *
import fx as FX
import geo as G
from shots import FuncShotF

YS = 240                # sea level in world px
SEABED = 1020
PEAKS = [(520, 300, 440), (960, 330, 330), (1400, 280, 470)]    # centre x, half-width, peak y when fully risen


def _noise(h, w, scale, seed, octaves=3):
    r = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        s = max(2, int(scale / (2 ** o)))
        n = r.random((h // s + 2, w // s + 2)).astype(np.float32)
        out += cv2.resize(n, (w, h), interpolation=cv2.INTER_CUBIC) * amp; tot += amp; amp *= 0.5
    return out / tot


@functools.lru_cache(None)
def _tex():
    h, w = H, W
    yy = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    # water gradient in world space (top = bright teal, deep = navy)
    d = np.clip((np.arange(h)[:, None] - YS) / (SEABED - YS), 0, 1).astype(np.float32)
    top = np.array([40, 190, 210], np.float32); mid = np.array([14, 85, 150], np.float32); bot = np.array([3, 12, 40], np.float32)
    wat = np.where(d[..., None] < 0.45, top + (mid - top) * (d[..., None] / 0.45), mid + (bot - mid) * ((d[..., None] - 0.45) / 0.55))
    water = np.repeat(wat, w, axis=1).astype(np.uint8)
    # sky above the surface (dawn)
    sy = np.clip(np.arange(h)[:, None] / YS, 0, 1).astype(np.float32)
    sk_top = np.array([60, 90, 150], np.float32); sk_bot = np.array([255, 190, 140], np.float32)
    sky = (sk_top + (sk_bot - sk_top) * (sy[..., None] ** 1.6))
    sky = np.repeat(sky, w, axis=1).astype(np.uint8)
    n1 = _noise(h, w, 80, 1); n2 = _noise(h, w, 14, 2)
    rock = np.zeros((h, w, 3), np.float32)
    base = 0.55 * n1 + 0.45 * n2
    rock[..., 0] = 30 + 50 * base; rock[..., 1] = 26 + 44 * base; rock[..., 2] = 38 + 46 * base
    c1 = _noise(h, w, 70, 3); c2 = _noise(h, w, 9, 4); c3 = _noise(h, w, 4, 7)
    pal = np.array([[236, 104, 92], [248, 146, 98], [222, 92, 128], [244, 182, 108], [104, 200, 182], [236, 104, 92]], np.float32)
    cn = (c1 - c1.min()) / (c1.max() - c1.min()) * 4.99
    i0 = np.clip(cn.astype(np.int32), 0, 4); fr = (cn - i0)[..., None]
    coral = pal[i0] * (1 - fr) + pal[i0 + 1] * fr
    polyp = (c3 > 0.62).astype(np.float32)[..., None]
    coral = coral * (0.86 + 0.22 * c2[..., None]) * (1 - 0.18 * polyp) + polyp * 22
    return dict(water=water, sky=sky, rock=np.clip(rock, 0, 255).astype(np.uint8), coral=np.clip(coral, 0, 255).astype(np.uint8))


def _cam_matrix(cx, cy, z):
    return np.array([[z, 0, W / 2 - cx * z], [0, z, H / 2 - cy * z]], np.float64)


def _warp(tex, M, border=cv2.BORDER_REFLECT):
    return cv2.warpAffine(tex, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=border)


def _poly_mask(pts_world, M):
    p = np.asarray(pts_world, np.float64)
    sc = np.stack([p[:, 0] * M[0, 0] + M[0, 2], p[:, 1] * M[1, 1] + M[1, 2]], 1)
    m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m, [sc.astype(np.int32)], 255, cv2.LINE_AA)
    return m, sc


def ridge_rise(t_local):
    return smoother((t_local - 8.1) / (19.0 - 8.1))


def rock_y(xs, r, sink):
    y = np.full_like(xs, SEABED, dtype=np.float64)
    top = np.full_like(xs, SEABED, dtype=np.float64)
    for (cx, w, ytop) in PEAKS:
        g = np.exp(-((xs - cx) / w) ** 2)
        top = np.minimum(top, SEABED - (SEABED - ytop) * r * g)
    return top + sink * (0.35 + 0.65 * np.exp(-((xs - 960) / 520) ** 2))


def coral_top(xs, g, lag, t_local):
    """top surface of the central coral edifice (None where there is no coral)."""
    gauss = np.exp(-((xs - 960) / 520.0) ** 8)           # flat-topped extent ~ +-520 px
    base_top = rock_y(xs, 1.0, 0.0)                       # rock top before sinking
    top = base_top - g * 330 * gauss                     # grows upward
    top = np.maximum(top, YS + 12)                        # cannot pass sea level
    lagoon = np.exp(-((xs - 960) / 190.0) ** 4)
    top = top + lag * 58 * lagoon
    return top, gauss


def palm(img, x, y, h, wind=0.0, col=(14, 38, 26)):
    xe = x + 4 * math.sin(wind)
    cv2.line(img, (int(x), int(y)), (int(xe + 6), int(y - h)), col, max(2, int(h / 14)), cv2.LINE_AA)
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * 0.55 + 0.08 * math.sin(wind + k)
        L = h * 0.62
        ex, ey = xe + 6 + math.cos(a) * L, y - h + math.sin(a) * L * 0.5 + abs(k - 3) * h * 0.06
        cv2.line(img, (int(xe + 6), int(y - h)), (int(ex), int(ey)), col, max(2, int(h / 22)), cv2.LINE_AA)


def cross_section(dur, t0_local, cam_keys, grow=(23.4, 36.6), sink=(36.6, 43.2), islets=(43.3, 45.7), show_coral=True):
    T = _tex()
    cam = G.cam_path([(k[0], k[1], k[2], k[3]) for k in cam_keys])   # (t, cx, cy, zoom) – reuse log-interp of 3rd as span; fine for zoom
    xs = np.arange(-200, 2121, 8, dtype=np.float64)

    def fn(t, d, st):
        TL = t0_local + t
        cx, cy, z = cam(t)
        M = _cam_matrix(cx, cy, z)
        # background: sky + water, split by the (wavy) sea surface
        sky = _warp(T['sky'], M); water = _warp(T['water'], M)
        wave = 5 * np.sin(xs * 0.012 + TL * 1.3) + 3 * np.sin(xs * 0.031 - TL * 1.9) + 2 * np.sin(xs * 0.07 + TL * 2.7)
        surf = np.stack([xs, YS + wave], 1)
        poly = np.vstack([[xs[0], 4000], surf, [xs[-1], 4000]])
        wm, scs = _poly_mask(poly, M)
        f = np.where(wm[..., None] > 0, water, sky)
        # sun glow at the horizon
        sx, sy = (1500 * M[0, 0] + M[0, 2]), (YS * M[1, 1] + M[1, 2])
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        glow = np.exp(-(((xx - sx) / 520) ** 2 + ((yy - sy) / 260) ** 2))[..., None] * np.array([255, 190, 120], np.float32)
        f = np.clip(f.astype(np.float32) + glow * 0.45 * (1 - wm[..., None] / 255.0 * 0.6), 0, 255).astype(np.uint8)
        r = ridge_rise(TL)
        s0, s1 = sink
        D = 330 * smoother((TL - s0) / (s1 - s0))
        lagoon = smoother((TL - 38.5) / (s1 - 38.5 + 4))
        # ---- rock
        ry = rock_y(xs, r, D)
        poly = np.vstack([[xs[0], 4000], np.stack([xs, ry], 1), [xs[-1], 4000]])
        rm, rsc = _poly_mask(poly, M)
        rock = _warp(T['rock'], M)
        # vertical shading + glowing lava veins while the ridge is rising
        shade = np.clip(1.0 - (np.arange(H, dtype=np.float32)[:, None] - 0) / (H * 1.8), 0.35, 1.0)[..., None]
        rock = (rock.astype(np.float32) * shade)
        if 8.1 <= TL <= 24.0:
            veins = _warp(cv2.cvtColor(_vein_tex(), cv2.COLOR_GRAY2RGB), M)
            gl = np.array([255, 120, 40], np.float32)
            act = math.sin(math.pi * np.clip((TL - 8.1) / 14.0, 0, 1)) ** 0.8
            rock += veins.astype(np.float32) / 255.0 * gl * act * 0.9 * (0.6 + 0.4 * math.sin(TL * 3))
        f = np.where(rm[..., None] > 0, np.clip(rock, 0, 255).astype(np.uint8), f)
        # rim light on the rock surface
        rimline = np.zeros((H, W, 3), np.uint8)
        cv2.polylines(rimline, [rsc[1:-1].astype(np.int32)], False, (120, 170, 200), 3, cv2.LINE_AA)
        f = np.clip(f.astype(np.float32) + rimline.astype(np.float32) * 0.45, 0, 255).astype(np.uint8)
        # ---- coral
        if show_coral and TL >= grow[0]:
            g = smoother((TL - grow[0]) / (grow[1] - grow[0]))
            if TL > grow[1]:
                g = 1.0
            ct, gauss = coral_top(xs, g, lagoon, TL)
            mask_x = gauss > 0.02
            sel = np.where(mask_x)[0]
            if len(sel) > 3:
                a, b = sel[0], sel[-1] + 1
                top_pts = np.stack([xs[a:b], ct[a:b]], 1)
                bot_pts = np.stack([xs[a:b][::-1], np.maximum(ry[a:b][::-1], ct[a:b][::-1] + 2)], 1)
                cm, csc = _poly_mask(np.vstack([top_pts, bot_pts]), M)
                cor = _warp(T['coral'], M)
                # strata: darker deeper bands drawn as curves
                band = np.zeros((H, W), np.float32)
                for j in range(1, 9):
                    off = j * 44
                    ln = np.zeros((H, W), np.uint8)
                    pts = np.stack([xs[a:b], ct[a:b] + off], 1)
                    p = np.stack([pts[:, 0] * M[0, 0] + M[0, 2], pts[:, 1] * M[1, 1] + M[1, 2]], 1).astype(np.int32)
                    cv2.polylines(ln, [p], False, 255, 3, cv2.LINE_AA)
                    band = np.maximum(band, ln.astype(np.float32) / 255.0 * (0.55 if j % 2 else 0.35))
                dep = np.clip((np.arange(H, dtype=np.float32)[:, None] - M[1, 2] - YS * M[1, 1]) / (900 * M[1, 1]), 0, 1)[..., None]
                cor = cor.astype(np.float32) * (1 - 0.45 * dep) * (1 - band[..., None] * 0.6)
                f = np.where(cm[..., None] > 0, np.clip(cor, 0, 255).astype(np.uint8), f)
                # glowing crest
                crest = np.zeros((H, W, 3), np.uint8)
                cv2.polylines(crest, [csc[:len(top_pts)].astype(np.int32)], False, (255, 215, 170), 3, cv2.LINE_AA)
                f = np.clip(f.astype(np.float32) + crest.astype(np.float32) * 0.5 + cv2.GaussianBlur(crest, (0, 0), 7).astype(np.float32) * 0.8, 0, 255).astype(np.uint8)
        # ---- islets & palms on the rim
        isl = smooth((TL - islets[0]) / 1.8)
        if isl > 0:
            for side in (-1, 1):
                for k, (off, hh) in enumerate([(300, 46), (342, 84), (380, 40)]):
                    cxw = 960 + side * off; w2 = 28
                    sand = []
                    for q in np.linspace(-1, 1, 15):
                        sand.append((cxw + q * w2 * 2.2, YS + 4 - hh * isl * (1 - q * q) ** 0.8))
                    pts = np.array([[(p[0] * M[0, 0] + M[0, 2]), (p[1] * M[1, 1] + M[1, 2])] for p in sand] + [[(cxw + w2 * 2.2) * M[0, 0] + M[0, 2], (YS + 18) * M[1, 1] + M[1, 2]], [(cxw - w2 * 2.2) * M[0, 0] + M[0, 2], (YS + 18) * M[1, 1] + M[1, 2]]], np.float32)
                    cv2.fillPoly(f, [pts.astype(np.int32)], (222, 204, 168), cv2.LINE_AA)
                    if hh > 60:
                        px, py = cxw * M[0, 0] + M[0, 2], (YS - hh * isl * 0.9) * M[1, 1] + M[1, 2]
                        palm(f, px, py, 120 * isl * M[0, 0], TL * 1.1 + side)
        # ---- surface foam line
        foam = np.zeros((H, W, 3), np.uint8)
        cv2.polylines(foam, [scs.astype(np.int32)], False, (235, 250, 255), 3, cv2.LINE_AA)
        f = np.clip(f.astype(np.float32) + foam.astype(np.float32) * 0.55 + cv2.GaussianBlur(foam, (0, 0), 5).astype(np.float32) * 0.6, 0, 255).astype(np.uint8)
        # underwater lighting: rays + caustics + plankton
        f = FX.god_rays(f, TL, 0.28, (190, 235, 255))
        f = FX.caustics(f, TL, 0.045)
        f = FX.particles(f, TL, 3, 120, (210, 240, 255), 0.45, drift=(0.6, -0.4))
        return f
    return FuncShotF(fn, dur)


@functools.lru_cache(None)
def _vein_tex():
    n = _noise(H, W, 34, 8, 4)
    v = np.exp(-((n - 0.5) / 0.016) ** 2)
    v = cv2.GaussianBlur(v.astype(np.float32), (0, 0), 2)
    return np.clip(v * 255, 0, 255).astype(np.uint8)


def polyp_macro(dur, t0_local=23.4):
    """macro: coral polyps appearing on rock; tentacles sway, calcium cups form."""
    rng = np.random.default_rng(21)
    N = 46
    px = rng.uniform(120, 1800, N); py = rng.uniform(560, 1000, N)
    sc = rng.uniform(0.55, 1.5, N); t_in = np.sort(rng.uniform(0.2, dur * 0.78, N)); ph = rng.uniform(0, 6.28, N)
    hue = rng.integers(0, 5, N)
    pal = np.array([[255, 150, 110], [255, 190, 120], [240, 120, 170], [255, 225, 150], [140, 235, 215]], np.float32)
    bgn = _noise(H, W, 100, 5)
    rockn = _noise(H, W, 18, 6)
    base = np.zeros((H, W, 3), np.float32)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    base[..., 0] = 6 + 12 * (1 - yy) ; base[..., 1] = 40 + 70 * (1 - yy) ; base[..., 2] = 70 + 100 * (1 - yy)
    base += bgn[..., None] * 18
    ground = (yy > 0.55 + 0.04 * bgn).astype(np.float32)
    gcol = np.stack([30 + 55 * rockn, 28 + 48 * rockn, 40 + 46 * rockn], -1)
    base = np.where(ground[..., None] > 0, gcol * (1.0 - 0.3 * yy)[..., None], base)
    base = np.clip(base, 0, 255).astype(np.uint8)

    def fn(t, d, st):
        f = base.copy()
        glow = np.zeros((H, W, 3), np.uint8)
        TL = t0_local + t
        for i in range(N):
            if t < t_in[i]:
                continue
            u = smooth((t - t_in[i]) / 1.6)
            s = sc[i] * u
            x, y = px[i], py[i] + 20 * (1 - u)
            col = tuple(int(c) for c in pal[hue[i]])
            # calcium cup (white-ish) + body
            cv2.ellipse(f, (int(x), int(y + 22 * s)), (int(46 * s), int(16 * s)), 0, 0, 360, (225, 220, 205), -1, cv2.LINE_AA)
            cv2.ellipse(f, (int(x), int(y)), (int(26 * s), int(34 * s)), 0, 0, 360, tuple(int(c * 0.8) for c in col), -1, cv2.LINE_AA)
            # tentacles
            for k in range(9):
                a0 = -math.pi / 2 + (k - 4) * 0.34
                pts = []
                for q in np.linspace(0, 1, 9):
                    sway = 0.30 * math.sin(TL * 2.1 + ph[i] + k * 0.7 + q * 4) * q
                    L = 82 * s * q
                    pts.append((x + math.cos(a0 + sway) * L, y - 10 * s + math.sin(a0 + sway) * L))
                p = np.array(pts, np.int32)
                cv2.polylines(f, [p], False, col, max(2, int(5 * s)), cv2.LINE_AA)
                cv2.circle(glow, tuple(p[-1]), max(2, int(5 * s)), (255, 245, 220), -1, cv2.LINE_AA)
            cv2.circle(glow, (int(x), int(y)), int(10 * s), col, -1, cv2.LINE_AA)
        g = cv2.GaussianBlur(glow, (0, 0), 10)
        f = np.clip(f.astype(np.float32) + g.astype(np.float32) * 0.8 + glow.astype(np.float32) * 0.5, 0, 255).astype(np.uint8)
        # depth of field + slow push
        z = 1.0 + 0.12 * t / d
        f = crop_zoom(f, W / 2, H / 2 + 60 * t / d, z)
        blur = cv2.GaussianBlur(f, (0, 0), 6)
        yy2 = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
        m = np.clip((0.35 - yy2) / 0.35, 0, 1)
        f = (f * (1 - m * 0.8) + blur * m * 0.8).astype(np.uint8)
        f = FX.particles(f, TL, 5, 160, (210, 245, 255), 0.7, drift=(0.8, -0.5), blur=1.6)
        f = FX.god_rays(f, TL, 0.20)
        return f
    return FuncShotF(fn, dur)


def atoll_ring(dur, t0_local=43.3, morph=(2.2, 5.6)):
    """top-down procedural atoll that melts into the real satellite atoll (Bangaram)."""
    gv = G.GeoView(extra=('mid_north', 'bangaram'))
    cam = G.cam_path([(0, 72.30, 10.915, 0.55), (dur, 72.30, 10.915, 0.26)])
    rng = np.random.default_rng(4)
    ang = np.linspace(0, 2 * np.pi, 360, endpoint=False)
    rr = 1 + 0.10 * np.sin(3 * ang + 1.0) + 0.06 * np.sin(5 * ang + 2.0) + 0.03 * np.sin(9 * ang)

    def fn(t, d, st):
        real = gv.render(*cam(t))
        # procedural ring: water gradient, reef ring, lagoon, thin sand
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        cx, cy = W / 2, H / 2
        dx, dy = (xx - cx) / 640, (yy - cy) / 420
        r = np.sqrt(dx * dx + dy * dy)
        th = np.arctan2(dy, dx)
        wob = 1 + 0.10 * np.sin(3 * th + 1.0) + 0.06 * np.sin(5 * th + 2.0 + t * 0.2) + 0.03 * np.sin(9 * th)
        rn = r / wob
        grow = smooth(t / 1.6)
        nz = st.setdefault('nz', cv2.resize(_noise(54, 96, 6, 12), (W, H), interpolation=cv2.INTER_CUBIC))
        deep = np.array([6, 24, 70], np.float32); turq = np.array([32, 196, 204], np.float32); lagc = np.array([16, 150, 186], np.float32)
        out_d = np.clip((rn - 0.96) / 0.38, 0, 1)[..., None]           # 0 at the reef edge -> 1 deep ocean
        outside = turq + (deep - turq) * (out_d ** 0.55)
        lag_d = np.clip(rn / 0.9, 0, 1)[..., None]
        lagoon = lagc + (turq - lagc) * (lag_d ** 2.2) + (nz[..., None] - 0.5) * 36
        inside = (rn < 0.93).astype(np.float32)[..., None]
        edge = smooth((0.93 - rn) / 0.02)[..., None] if False else np.clip((0.935 - rn) / 0.018, 0, 1)[..., None]
        out = outside * (1 - edge) + lagoon * edge
        reef = np.exp(-((rn - 0.945) / (0.030 * grow + 0.004)) ** 2)[..., None]
        sand = np.exp(-((rn - 0.925) / (0.016 * grow + 0.003)) ** 2)[..., None]
        out = out + reef * np.array([150, 230, 220], np.float32) * 0.28 * grow + sand * np.array([238, 226, 190], np.float32) * 0.5 * grow
        out = out * (0.92 + 0.16 * nz[..., None])
        proc = np.clip(out, 0, 255).astype(np.uint8)
        proc = crop_zoom(proc, W / 2, H / 2, 1.0 + 0.1 * t / d)
        m = smooth((t - morph[0]) / (morph[1] - morph[0]))
        return cv2.addWeighted(proc, 1 - m, real, m, 0)
    return FuncShotF(fn, dur)
