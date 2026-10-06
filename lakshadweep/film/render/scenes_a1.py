"""Act 1 scenes: map dive with the 'lakh' dot cloud, 36 markers, Hyderabad comparison, EEZ."""
import math
import numpy as np, cv2
from engine import *
import geo as G
import fx as FX
from data import ISLANDS, OTHERS
from shots import FuncShotF

# 36 marker positions: the 10 inhabited islands + 26 other reefs/islets (approximate)
PTS36 = list(ISLANDS.items())
_other = [(n, lon, lat) for (n, lon, lat) in OTHERS if not n.startswith(('Misc', 'Chetlat2', 'Bangaram2', 'Pitti2', 'Androth2', 'Kalpeni2', 'Thinakara2', 'Tinnakara', 'Aminidivi'))]
LAK36 = [(lon, lat, n, True) for n, (lon, lat) in ISLANDS.items()] + [(lon, lat, n, False) for (n, lon, lat) in _other][:26]


def _dot_cloud(img, T, cam, appear, vanish, n=100000, seed=3):
    """a 'lakh' of tiny lights over the sea that burst away on vanish."""
    lon, lat, span = cam
    r = np.random.default_rng(seed)
    if not hasattr(_dot_cloud, 'P'):
        _dot_cloud.P = (r.uniform(66.5, 79.5, n), r.uniform(4.0, 16.5, n), r.uniform(0, 6.28, n), r.uniform(0.6, 1.0, n))
    X, Y, ph, br = _dot_cloud.P
    if T < appear:
        return img
    px = (X - lon) / span * W + W / 2
    py = (lat - Y) / (span * H / W) * H + H / 2
    k = np.clip((T - appear) / 2.2, 0, 1)
    wgt = np.exp(-(((X - 72.6) / 4.2) ** 2 + ((Y - 10.5) / 3.6) ** 2))
    vis = ((np.arange(n) / n) < k ** 1.3) & (wgt > np.random.default_rng(9).random(n) * 0.9)
    if T > vanish:
        u = np.clip((T - vanish) / 0.55, 0, 1)
        # scatter outward + fade
        cx, cy = W / 2, H / 2
        dx, dy = px - cx, py - cy
        px = px + dx * u * 1.6; py = py + dy * u * 1.6
        fade = 1 - u
    else:
        fade = 1.0
    ok = vis & (px >= 0) & (px < W) & (py >= 0) & (py < H)
    ix = px[ok].astype(np.int32); iy = py[ok].astype(np.int32)
    tw = (0.55 + 0.45 * np.sin(T * 3.0 + ph[ok])) * br[ok]
    buf = np.bincount(iy * W + ix, weights=tw, minlength=W * H).reshape(H, W).astype(np.float32)
    core = cv2.GaussianBlur(buf, (0, 0), 0.9) * 5.0
    halo = cv2.GaussianBlur(buf, (0, 0), 3.5) * 14.0
    layer = (np.clip(core, 0, 1) * 255 * 0.9 + np.clip(halo, 0, 1) * 255 * 0.35)[..., None] * np.array([0.60, 0.92, 1.0], np.float32)
    ocean = (img[..., 2].astype(np.int16) > img[..., 0].astype(np.int16) + 6).astype(np.float32)
    ocean = cv2.GaussianBlur(ocean, (0, 0), 8)[..., None]
    return np.clip(img.astype(np.float32) + layer * fade * ocean, 0, 255).astype(np.uint8)


def intro_map(dur, t0_local=2.3):
    """map dive: wide Arabian Sea -> archipelago (dots, 36 markers, 10 highlighted) -> Agatti atoll."""
    gv = G.GeoView(extra=('mid_north', 'agatti'))
    cam = G.cam_path([(0, 62, 15, 28), (2.5, 71.6, 11.2, 11.5), (3.8, 72.6, 10.4, 6.2), (8.9, 72.9, 10.3, 5.6),
                      (11.5, 72.4, 10.95, 1.4), (14.6, 72.22, 10.88, 0.42), (dur, 72.2, 10.86, 0.22)])
    pings = []

    def fn(t, d, st):
        TL = t0_local + t                       # act-local time
        lon, lat, span = cam(t)
        f = gv.render(lon, lat, span)
        f = _dot_cloud(f, TL, (lon, lat, span), 2.5, 4.86)
        # 36 markers 6.3 -> 8.84, 10 inhabited glow brighter from 8.9
        mk = []
        for i, (mlon, mlat, name, inh) in enumerate(LAK36):
            x, y = G.GeoView.project(mlon, mlat, lon, lat, span)
            ta = 6.3 + 2.5 * i / 36.0
            mk.append((x, y, ta - t0_local))
        if span > 0.8:
            f = G.marker_overlay(f, [(x, y, ta) for (x, y, ta) in mk], t, color=(130, 230, 255), r=6, ring=False, alpha=0.9 * smooth((span - 0.8) / 1.5))
            inh = [(G.GeoView.project(m[0], m[1], lon, lat, span) + (8.9 - t0_local,)) for m in LAK36 if m[3]]
            f = G.marker_overlay(f, inh, t, color=(255, 220, 140), r=9, ring=True, alpha=smooth((span - 0.8) / 1.5))
        return f
    return FuncShotF(fn, dur)


_HYD = {}


def hyderabad(dur, t0_local=18.5):
    """city night-lights + a 32 km^2 square; 20 squares tile the city (=> < 1/20 of Hyderabad)."""
    if 'bg' not in _HYD:
        n = cv2.cvtColor(cv2.imread(os.path.join(G.MAPS, 'hyd_night.jpg')), cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        n = cv2.resize(n, (W, H), interpolation=cv2.INTER_CUBIC)
        lum = n.mean(axis=2, keepdims=True)
        g = cv2.GaussianBlur(n, (0, 0), 16) * 0.9 + cv2.GaussianBlur(n, (0, 0), 9) * 0.55
        g = (1 - np.exp(-g * 0.75)) ** 1.7 * 1.25
        warm = np.array([1.0, 0.72, 0.38], np.float32)
        out = g * warm * 0.9 + np.array([0.02, 0.04, 0.09], np.float32)
        _HYD['bg'] = np.clip(out * 255, 0, 255).astype(np.uint8)
    bg = _HYD['bg']
    # geometry: view is 0.96 deg wide (~102 km) -> 1 km = 18.8 px ; 32 km^2 -> 5.66 km square -> 106 px
    side = 106
    cx, cy = int(W * 0.46), int(H * 0.46)
    # 20 squares in a rough blob (5 cols x 4 rows) around the city centre; first one is 'Lakshadweep'
    cols, rows = 5, 4
    cells = [(cx + (c - (cols - 1) / 2) * (side + 8), cy + (r - (rows - 1) / 2) * (side + 8)) for r in range(rows) for c in range(cols)]
    order = list(np.argsort([(x - cx) ** 2 + (y - cy) ** 2 for x, y in cells]))
    def fn(t, d, st):
        TL = t0_local + t
        z = 1.0 + 0.03 * t / d
        f = crop_zoom(bg, W / 2, H / 2, z)
        # first square (the whole of Lakshadweep) appears at 18.7
        x0, y0 = cx - side / 2, cy - side / 2
        ov = np.zeros((H, W, 3), np.uint8)
        a1 = smooth((TL - 18.65) / 0.35)
        if a1 > 0:
            cv2.rectangle(ov, (int(x0), int(y0)), (int(x0 + side), int(y0 + side)), (255, 255, 255), 3, cv2.LINE_AA)
            fill = np.zeros_like(ov); cv2.rectangle(fill, (int(x0), int(y0)), (int(x0 + side), int(y0 + side)), (120, 200, 255), -1)
            ov = cv2.addWeighted(ov, 1.0, fill, 0.30, 0)
            ov = (ov * a1).astype(np.uint8)
        n_show = int(np.clip((TL - 19.7) / 0.07, 0, 19))
        for k in range(1, 20):
            if k - 1 >= n_show:
                break
            xk, yk = cells[order[k]]
            ak = smooth((TL - (19.7 + 0.07 * (k - 1))) / 0.25)
            cv2.rectangle(ov, (int(xk - side / 2), int(yk - side / 2)), (int(xk + side / 2), int(yk + side / 2)), (int(235 * ak), int(215 * ak), int(170 * ak)), 2, cv2.LINE_AA)
        f = np.clip(f.astype(np.float32) + ov.astype(np.float32) * 0.9 + cv2.GaussianBlur(ov, (0, 0), 6).astype(np.float32) * 1.2, 0, 255).astype(np.uint8)
        f = G.label(f, 'LAKSHADWEEP', cx + side / 2 + 30, cy - side / 2 - 18, alpha=smooth((TL - 18.9) / 0.4) * smooth((22.3 - TL) / 0.4), size=26) if False else f
        return f
    return FuncShotF(fn, dur)


def eez(dur, t0_local=22.1):
    """sea around: a ~360 km-radius circle (~4 lakh km^2) blooming around the islands."""
    gv = G.GeoView(extra=())
    cam = G.cam_path([(0, 72.6, 10.2, 5.2), (dur, 72.6, 10.0, 11.5)])
    def fn(t, d, st):
        TL = t0_local + t
        lon, lat, span = cam(t)
        f = gv.render(lon, lat, span)
        u = smooth((TL - 22.4) / 2.6)
        rdeg = 3.2 * u                   # ~355 km radius
        cx, cy = G.GeoView.project(72.6, 10.0, lon, lat, span)
        rpx = rdeg / span * W
        ov = np.zeros((H, W, 3), np.uint8)
        if rpx > 2:
            fill = np.zeros_like(ov); cv2.circle(fill, (int(cx), int(cy)), int(rpx), (90, 190, 255), -1, cv2.LINE_AA)
            ring = np.zeros_like(ov); cv2.circle(ring, (int(cx), int(cy)), int(rpx), (200, 245, 255), 3, cv2.LINE_AA)
            g = cv2.GaussianBlur(ring, (0, 0), 10)
            f = np.clip(f.astype(np.float32) * (1 - 0.25 * u) + fill.astype(np.float32) * 0.20 * u + ring.astype(np.float32) * 0.9 + g.astype(np.float32) * 1.4, 0, 255).astype(np.uint8)
        # the islands: tiny bright dots in the centre of the blue
        pts = [(G.GeoView.project(m[0], m[1], lon, lat, span) + (0,)) for m in LAK36]
        f = G.marker_overlay(f, pts, t, color=(255, 230, 160), r=5, ring=False, alpha=0.9)
        return f
    return FuncShotF(fn, dur)


def intro_map_lakh(dur, t0_local):
    """callback to the opening: the lakh of lights appears over the sea ... and condenses into the real 36."""
    gv = G.GeoView(extra=('mid_north',))
    cam = G.cam_path([(0, 72.8, 10.4, 6.8), (dur, 72.8, 10.4, 5.8)])

    def fn(t, d, st):
        lon, lat, span = cam(t)
        f = gv.render(lon, lat, span)
        f = (f.astype(np.float32) * 0.82).astype(np.uint8)
        TL = t0_local + t
        # lights appear 54.4 -> 56.8, vanish at 57.5
        f = _dot_cloud(f, t + 100.0 if False else t, (lon, lat, span), 0.3, 3.3)
        mk = [(G.GeoView.project(m[0], m[1], lon, lat, span) + (3.5 + 0.02 * i,)) for i, m in enumerate(LAK36)]
        f = G.marker_overlay(f, mk, t, color=(255, 225, 150), r=6, ring=False, alpha=0.95)
        return f
    return FuncShotF(fn, dur)
