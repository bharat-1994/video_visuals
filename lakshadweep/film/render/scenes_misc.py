"""Map routes, flag, year cards, cyclone, cable, sea-level, matrilineal graphic."""
import math, os, functools
import numpy as np, cv2
from engine import *
import geo as G
import fx as FX
from shots import FuncShotF
from data import ISLANDS
import assets as AS


# --------------------------------------------------------------------------------------------- routes on the satellite map
def route_map(dur, cam_keys, routes=(), markers=(), labels=(), extra=(), layers=None, t0=0.0, pulse=None, dim=0.0):
    """routes: dict(pts=[(lon,lat)...], t0, t1, color, width, dash); markers: (lon,lat,t_on,color,r,ring)
    labels: (text,lon,lat,t_on,t_off,dx,dy) ; times are shot-relative."""
    gv = G.GeoView(layers=layers, extra=extra)
    cam = G.cam_path(cam_keys)

    def fn(t, d, st):
        lon, lat, span = cam(t)
        f = gv.render(lon, lat, span)
        if dim:
            f = (f.astype(np.float32) * (1 - dim)).astype(np.uint8)
        for r in routes:
            p = smooth((t - r['t0']) / max(r['t1'] - r['t0'], 1e-3))
            if p <= 0:
                continue
            pts = [G.GeoView.project(lo, la, lon, lat, span) for (lo, la) in r['pts']]
            f = G.path_overlay(f, pts, p, r.get('color', (255, 214, 120)), r.get('width', 3), r.get('dash', True), r.get('head', True), r.get('alpha', 1.0))
        for m in markers:
            lo, la, ton = m[0], m[1], m[2]
            col = m[3] if len(m) > 3 else (255, 225, 150)
            rr = m[4] if len(m) > 4 else 8
            ring = m[5] if len(m) > 5 else True
            x, y = G.GeoView.project(lo, la, lon, lat, span)
            f = G.marker_overlay(f, [(x, y, ton)], t, color=col, r=rr, ring=ring)
        for (txt, lo, la, ton, toff, dx, dy) in labels:
            a = smooth((t - ton) / 0.6) * smooth((toff - t) / 0.6)
            x, y = G.GeoView.project(lo, la, lon, lat, span)
            f = G.label(f, txt, x + dx, y + dy, a, size=26)
        return f
    return FuncShotF(fn, dur)


# --------------------------------------------------------------------------------------------- year typography
def year_card(dur, text, sub='', bg=None, t_in=0.3, color=(255, 255, 255), size=250):
    """big numeral over a dark sea (optionally over a given background shot factory frame function)."""
    def fn(t, d, st):
        base = bg(t, d, st) if bg else np.zeros((H, W, 3), np.uint8)
        a = smooth((t - t_in) / 0.8) * smooth((d - t - 0.2) / 0.7)
        drift = int(-30 * t / d)
        f = draw_title(base.copy(), text, H // 2 - 20, a, size=size, spacing=18, fname='Marcellus-Regular.ttf', color=color, dx=drift)
        if sub:
            f = draw_title(f, sub, H // 2 + 150, a * 0.85, size=34, spacing=10, fname='Marcellus-Regular.ttf', color=(230, 235, 240), glow=False, dx=drift)
        return f
    return FuncShotF(fn, dur)


# --------------------------------------------------------------------------------------------- the tricolour
@functools.lru_cache(None)
def _flag_tex():
    w, h = 1200, 800
    f = np.zeros((h, w, 3), np.uint8)
    f[:h // 3] = (255, 153, 51); f[h // 3:2 * h // 3] = (250, 250, 250); f[2 * h // 3:] = (19, 136, 8)
    c = (w // 2, h // 2); r = int(h / 3 * 0.46)
    cv2.circle(f, c, r, (20, 20, 140), 6, cv2.LINE_AA)
    for k in range(24):
        a = k * math.pi / 12
        cv2.line(f, (int(c[0] + math.cos(a) * r * 0.12), int(c[1] + math.sin(a) * r * 0.12)), (int(c[0] + math.cos(a) * r * 0.96), int(c[1] + math.sin(a) * r * 0.96)), (20, 20, 140), 3, cv2.LINE_AA)
        a2 = a + math.pi / 24
        cv2.circle(f, (int(c[0] + math.cos(a2) * r * 0.88), int(c[1] + math.sin(a2) * r * 0.88)), 4, (20, 20, 140), -1, cv2.LINE_AA)
    cv2.circle(f, c, int(r * 0.10), (20, 20, 140), -1, cv2.LINE_AA)
    return f


def flag_overlay(img, T, cx, cy, width=1100, hoist=1.0, wind=1.0):
    """composite a waving tricolour onto img (pole on the left of the flag). hoist in [0,1] raises it."""
    tex = _flag_tex()
    th, tw = tex.shape[:2]
    fw = width; fh = int(width * 2 / 3)
    ys, xs = np.mgrid[0:fh, 0:fw].astype(np.float32)
    u = xs / fw
    ph = T * 5.2
    amp = (0.05 * fh) * u * wind
    dy = amp * (np.sin(u * 9.0 - ph) + 0.35 * np.sin(u * 17.0 - ph * 1.7 + 1.0))
    dx = -amp * 0.35 * np.cos(u * 9.0 - ph)
    mx = (xs + dx) / fw * tw; my = (ys - dy) / fh * th
    cloth = cv2.remap(tex, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    slope = np.cos(u * 9.0 - ph) + 0.4 * np.cos(u * 17.0 - ph * 1.7 + 1.0)
    shade = (1.0 + 0.22 * slope * u)[..., None]
    cloth = np.clip(cloth.astype(np.float32) * shade, 0, 255).astype(np.uint8)
    alpha = np.ones((fh, fw), np.float32)
    # frayed edge
    edge = np.clip((fw - xs) / 8, 0, 1)
    alpha *= edge
    # place with pole at x=cx-? ; raise by hoist
    x0 = int(cx); y0 = int(cy - fh * 0.5 + (1 - hoist) * 600)
    x1 = min(W, x0 + fw); y1 = min(H, y0 + fh)
    if x0 >= W or y1 <= 0:
        return img
    ya = max(0, -y0); yb = fh - max(0, y0 + fh - H)
    reg = img[max(y0, 0):y1, x0:x1].astype(np.float32)
    c = cloth[ya:ya + reg.shape[0], :reg.shape[1]].astype(np.float32)
    a = alpha[ya:ya + reg.shape[0], :reg.shape[1]][..., None]
    img[max(y0, 0):y1, x0:x1] = (reg * (1 - a) + c * a).astype(np.uint8)
    # pole
    px = x0 - 7
    top = max(0, y0 - 60)
    cv2.line(img, (px, top), (px, H), (210, 205, 195), 12, cv2.LINE_AA)
    cv2.circle(img, (px, top), 10, (240, 200, 90), -1, cv2.LINE_AA)
    return img


# --------------------------------------------------------------------------------------------- cyclone (real VIIRS) with swirl
def cyclone(dur, src='ockhi_viirs3.jpg', eye=(0.356, 0.43), zoom=(1.0, 1.6), swirl=0.9, rot=(0, 0)):
    im = load_img(os.path.join(G.MAPS, src), 3000)
    im = np.clip(((im.astype(np.float32) / 255.0) ** 1.35) * 235.0, 0, 255).astype(np.uint8)   # tame the clipped white cloud tops
    ih, iw = im.shape[:2]
    ex, ey = eye[0] * iw, eye[1] * ih
    R0 = 0.28 * min(ih, iw)
    ys, xs = np.mgrid[0:ih, 0:iw].astype(np.float32)
    dxm, dym = xs - ex, ys - ey
    rr = np.sqrt(dxm * dxm + dym * dym); th = np.arctan2(dym, dxm)
    fall = np.exp(-(rr / R0) ** 1.2)

    def fn(t, d, st):
        ang = swirl * (t * 0.45) * fall
        mx = ex + rr * np.cos(th - ang); my = ey + rr * np.sin(th - ang)
        sw = cv2.remap(im, mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        z = lerp(zoom[0], zoom[1], smooth(t / d)) * max(W / iw, H / ih)
        cxp = lerp(0.5 * iw, ex, smooth(t / d) * 0.8); cyp = lerp(0.5 * ih, ey, smooth(t / d) * 0.8)
        return crop_zoom(sw, cxp, cyp, z, rot=lerp(rot[0], rot[1], t / d))
    return FuncShotF(fn, dur)


# --------------------------------------------------------------------------------------------- submarine cable
def cable_map(dur, t0=0.0):
    kochi = (76.27, 9.97)
    gv = G.GeoView(extra=())
    cam = G.cam_path([(0, 74.6, 10.3, 7.8), (dur, 74.3, 10.3, 6.4)])
    ends = [(m[0], m[1]) for m in [(72.64, 10.57), (72.18, 10.86), (72.73, 11.12), (73.68, 10.82), (73.65, 10.08), (72.78, 11.23), (73.00, 11.49), (72.71, 11.68), (72.18, 11.60), (73.04, 8.28)]]

    def fn(t, d, st):
        lon, lat, span = cam(t)
        f = gv.render(lon, lat, span)
        f = (f.astype(np.float32) * 0.78).astype(np.uint8)
        kx, ky = G.GeoView.project(kochi[0], kochi[1], lon, lat, span)
        for i, (elon, elat) in enumerate(ends):
            p = smooth((t - 0.6 - 0.28 * i) / 2.2)
            if p <= 0:
                continue
            ex_, ey_ = G.GeoView.project(elon, elat, lon, lat, span)
            mx, my = (kx + ex_) / 2, (ky + ey_) / 2 - 40
            pts = [(kx, ky), (kx + (mx - kx) * 0.7, ky + (my - ky) * 0.7 - 20), (mx, my), (ex_, ey_)]
            # smooth the polyline via quadratic samples
            cp = np.array(pts, np.float32)
            ss = np.linspace(0, 1, 40)
            curve = [tuple(((1 - s) ** 2 * cp[0] + 2 * (1 - s) * s * cp[2] + s * s * cp[3])) for s in ss]
            f = G.path_overlay(f, curve, p, (110, 235, 255), 3, False, False, 0.9)
            # light pulses travelling along the finished cable
            if p > 0.99:
                q = ((t * 0.55 + i * 0.13) % 1.0)
                j = int(q * (len(curve) - 1))
                f = G.marker_overlay(f, [(curve[j][0], curve[j][1], 0)], t + 10, color=(255, 255, 255), r=5, ring=False)
        f = G.marker_overlay(f, [(kx, ky, 0.2)], t, color=(255, 220, 140), r=10, ring=True)
        pts = [(G.GeoView.project(e[0], e[1], lon, lat, span) + (1.0 + 0.2 * i,)) for i, e in enumerate(ends)]
        f = G.marker_overlay(f, pts, t, color=(255, 225, 150), r=7, ring=False)
        return f
    return FuncShotF(fn, dur)


# --------------------------------------------------------------------------------------------- sea level / erosion cross-section
def sea_level(dur, t0=0.0):
    """low coral-sand island on its reef platform: sea rises, waves bite into the shore."""
    import scenes_a2 as A2
    T = A2._tex()
    xs = np.arange(-100, 2021, 6, dtype=np.float64)
    YSL = 600          # starting sea level
    BASE = 860         # reef platform top

    def mound(x, erode):
        half = 520 - 130 * erode
        prof = np.clip(1 - ((x - 960) / half) ** 2, 0, 1) ** 0.5
        return BASE - 318 * prof * (1 - 0.12 * erode), prof > 0.001

    def fn(t, d, st):
        u = smooth(t / d)
        rise = 46 * u
        sky = A2._warp(T['sky'], np.array([[1, 0, 0], [0, 2.4, 20]], np.float64))
        f = sky.copy()
        wave = 7 * np.sin(xs * 0.011 + t * 1.2) + 4 * np.sin(xs * 0.028 - t * 1.7) + 2 * np.sin(xs * 0.06 + t * 2.4)
        lvl = YSL - rise
        surf = np.stack([xs, lvl + wave + 6 * u * np.sin(xs * 0.02 + t * 2.2)], 1)
        poly = np.vstack([[xs[0], 3000], surf, [xs[-1], 3000]]).astype(np.int32)
        wm = np.zeros((H, W), np.uint8); cv2.fillPoly(wm, [poly], 255, cv2.LINE_AA)
        wat = A2._warp(T['water'], np.array([[1, 0, 0], [0, 1.0, 560 - 240]], np.float64))
        f = np.where(wm[..., None] > 0, wat, f)
        # reef platform (coral) with sloping flanks
        plat = np.where(np.abs(xs - 960) < 820, BASE, BASE + (np.abs(xs - 960) - 820) * 1.3)
        rp = np.vstack([[xs[0], 3000], np.stack([xs, plat], 1), [xs[-1], 3000]]).astype(np.int32)
        rm = np.zeros((H, W), np.uint8); cv2.fillPoly(rm, [rp], 255, cv2.LINE_AA)
        cor = A2._warp(T['coral'], np.array([[1, 0, 0], [0, 1, 0]], np.float64)).astype(np.float32)
        dep = np.clip((np.arange(H, dtype=np.float32)[:, None] - BASE) / 380, 0, 1)[..., None]
        # healthy -> bleached as the story moves on
        bl = smooth((t - d * 0.35) / (d * 0.5))
        gray = cor.mean(axis=2, keepdims=True)
        cor = cor * (1 - bl) + (gray * 0.5 + np.array([150, 165, 160], np.float32)) * bl
        cor = cor * (1 - 0.65 * dep)
        f = np.where(rm[..., None] > 0, np.clip(cor, 0, 255).astype(np.uint8), f)
        # sand mound
        y_m, inside = mound(xs, u)
        sm_pts = np.vstack([[xs[0], BASE + 6], [xs[0], BASE + 6]] + [[x, y] for x, y, ins in zip(xs, y_m, inside) if ins] + [[xs[-1], BASE + 6]]).astype(np.int32)
        sm = np.zeros((H, W), np.uint8); cv2.fillPoly(sm, [sm_pts], 255, cv2.LINE_AA)
        g2 = np.clip((np.arange(H, dtype=np.float32)[:, None] - 480) / 260, 0, 1)[..., None]
        sandc = np.array([240, 226, 192], np.float32) * (1 - 0.35 * g2) + np.array([150, 130, 100], np.float32) * g2 * 0.35
        sandc = np.repeat(sandc, W, axis=1)
        f = np.where(sm[..., None] > 0, sandc.astype(np.uint8), f)
        ln = np.zeros((H, W, 3), np.uint8)
        cv2.polylines(ln, [surf.astype(np.int32)], False, (240, 250, 255), 3, cv2.LINE_AA)
        f = np.clip(f.astype(np.float32) + ln.astype(np.float32) * 0.6 + cv2.GaussianBlur(ln, (0, 0), 5).astype(np.float32) * 0.5, 0, 255).astype(np.uint8)
        for k, off in enumerate([-300, -110, 140, 330]):
            px = 960 + off * (1 - 0.15 * u)
            py = float(mound(np.array([px]), u)[0][0]) + 6
            if abs(off) * (1 - 0.15 * u) > 520 - 130 * u - 70:
                continue
            A2.palm(f, px, py, 170 + 20 * (k % 2), t * 1.1 + k)
        if rise > 4:
            for xx in range(0, W, 38):
                cv2.line(f, (xx, YSL), (xx + 18, YSL), (255, 255, 255), 2, cv2.LINE_AA)
            ax = 1760; cv2.arrowedLine(f, (ax, YSL + 80), (ax, int(lvl) + 8), (255, 235, 180), 4, cv2.LINE_AA, tipLength=0.35) if rise > 14 else None
        f = FX.god_rays(f, t, 0.16)
        f = FX.particles(f, t, 12, 70, (255, 245, 230), 0.25)
        return f
    return FuncShotF(fn, dur)


# --------------------------------------------------------------------------------------------- matrilineal inheritance (quiet line-art)
def matri(dur, t0=0.0):
    def draw_house(cv, cx, cy, s, col, a):
        pts = np.array([[cx - 60 * s, cy], [cx - 60 * s, cy - 55 * s], [cx, cy - 105 * s], [cx + 60 * s, cy - 55 * s], [cx + 60 * s, cy]], np.int32)
        cv2.polylines(cv, [pts], True, tuple(int(c * a) for c in col), max(2, int(5 * s)), cv2.LINE_AA)
        cv2.rectangle(cv, (int(cx - 16 * s), int(cy - 40 * s)), (int(cx + 16 * s), int(cy)), tuple(int(c * a) for c in col), max(2, int(4 * s)), cv2.LINE_AA)

    def draw_woman(cv, cx, cy, s, col, a):
        c = tuple(int(v * a) for v in col)
        cv2.circle(cv, (int(cx), int(cy - 78 * s)), int(15 * s), c, -1, cv2.LINE_AA)
        tri = np.array([[cx, cy - 62 * s], [cx - 30 * s, cy], [cx + 30 * s, cy]], np.int32)
        cv2.fillPoly(cv, [tri], c, cv2.LINE_AA)

    grad = np.zeros((H, W, 3), np.float32)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    grad[...] = (np.array([12, 52, 84], np.float32) * (1 - yy[..., None]) + np.array([6, 22, 50], np.float32) * yy[..., None])
    grad = grad.astype(np.uint8)

    def fn(t, d, st):
        f = grad.copy()
        glow = np.zeros((H, W, 3), np.uint8)
        gold = (255, 205, 130); rose = (255, 150, 165); mint = (140, 235, 215)
        # three generations, house passing from mother to daughter to granddaughter
        xs = [500, 960, 1420]; ys = 640
        for i, (x, s, col) in enumerate(zip(xs, [1.5, 1.25, 1.0], [rose, gold, mint])):
            a = smooth((t - 0.2 - 0.7 * i) / 0.7)
            draw_house(glow, x, ys, s, col, a)
            draw_woman(glow, x, ys - 150 * s, s * 0.95, col, a)
        for i in range(2):
            p = smooth((t - 1.6 - 1.1 * i) / 1.0)
            if p <= 0:
                continue
            x0, x1 = xs[i] + 150, xs[i + 1] - 150
            xe = x0 + (x1 - x0) * p
            cv2.line(glow, (int(x0), ys - 330), (int(xe), ys - 330), gold, 4, cv2.LINE_AA)
            if p > 0.95:
                cv2.arrowedLine(glow, (int(x1 - 60), ys - 330), (int(x1), ys - 330), gold, 4, cv2.LINE_AA, tipLength=0.6)
        # the son marries and walks to his wife's house
        u = smooth((t - 6.6) / 3.0)
        if t > 6.4:
            x0, x1 = xs[0] + 20, xs[1] - 20
            px_ = x0 + (x1 - x0) * u; py_ = ys - 40 - 70 * math.sin(math.pi * u)
            blue = (140, 190, 255)
            cv2.circle(glow, (int(px_), int(py_ - 60)), 14, blue, -1, cv2.LINE_AA)
            cv2.fillPoly(glow, [np.array([[px_, py_ - 46], [px_ - 24, py_], [px_ + 24, py_]], np.int32)], blue, cv2.LINE_AA)
        g = cv2.GaussianBlur(glow, (0, 0), 12)
        f = np.clip(f.astype(np.float32) + glow.astype(np.float32) + g.astype(np.float32) * 1.2, 0, 255).astype(np.uint8)
        return f
    return FuncShotF(fn, dur)


# --------------------------------------------------------------------------------------------- Chagos-Laccadive ridge fly-along
def ridge_fly(dur, t0_local=16.14):
    lay = [G.Layer('world_bm.jpg', (-180, -90, 180, 90)), G.Layer('ridge_long.jpg', (64, -10, 80, 16))]
    gv = G.GeoView(layers=lay)
    cam = G.cam_path([(0, 72.9, 6.5, 17.0), (dur, 72.5, 0.5, 21.0)])
    ridge = [(72.55, 11.6), (72.8, 10.2), (73.0, 8.3), (73.3, 6.0), (73.4, 4.0), (73.2, 1.5), (73.1, -0.5), (72.9, -3.0), (72.2, -5.5), (71.6, -6.8)]

    def fn(t, d, st):
        lon, lat, span = cam(t)
        f = gv.render(lon, lat, span)
        f = (f.astype(np.float32) * 0.9).astype(np.uint8)
        pts = [G.GeoView.project(lo, la, lon, lat, span) for (lo, la) in ridge]
        p = smooth((t - 0.5) / (d - 1.5))
        f = G.path_overlay(f, pts, p, (255, 200, 120), 5, False, True, 0.9)
        f = G.label(f, 'CHAGOS - LACCADIVE RIDGE', pts[4][0] + 40, pts[4][1], smooth((t - 1.2) / 0.8), size=28)
        return f
    return FuncShotF(fn, dur)


# --------------------------------------------------------------------------------------------- tall-ship silhouettes (Portuguese carrack with the red cross)
def _carrack(cv, x, y, s, bob, col=(8, 6, 10), sail=(54, 34, 28), cross=(118, 18, 22), pennant=True):
    """draws a stylised carrack at (x,y) = waterline centre. s = scale. returns nothing."""
    hull = np.array([[-150, 0], [-165, -30], [-120, -62], [-40, -70], [60, -70], [140, -52], [175, -78], [160, -20], [110, 8], [-60, 16]], np.float32) * s
    hull[:, 0] += x; hull[:, 1] += y + bob
    cv2.fillPoly(cv, [hull.astype(np.int32)], col, cv2.LINE_AA)
    # castles
    cv2.fillPoly(cv, [(np.array([[-165, -30], [-175, -92], [-120, -92], [-120, -62]], np.float32) * s + [x, y + bob]).astype(np.int32)], col, cv2.LINE_AA)
    for mx, mh, sw in [(-70, 230, 120), (10, 300, 150), (95, 210, 100)]:
        top = (x + mx * s, y + bob - 70 * s - mh * s)
        cv2.line(cv, (int(x + mx * s), int(y + bob - 60 * s)), (int(top[0]), int(top[1])), col, max(2, int(5 * s)), cv2.LINE_AA)
        # square sail with billow
        w = sw * s; h = mh * 0.62 * s
        bill = 10 * s * math.sin(bob * 0.5 + mx)
        pts = np.array([[top[0] - w / 2, top[1] + 18 * s], [top[0] + w / 2, top[1] + 18 * s], [top[0] + w / 2 + bill, top[1] + 18 * s + h * 0.55], [top[0] + w / 2, top[1] + 18 * s + h], [top[0] - w / 2, top[1] + 18 * s + h], [top[0] - w / 2 - bill, top[1] + 18 * s + h * 0.55]], np.int32)
        cv2.fillPoly(cv, [pts], sail, cv2.LINE_AA)
        cx_, cy_ = top[0], top[1] + 18 * s + h * 0.5
        arm = min(w, h) * 0.30
        cv2.rectangle(cv, (int(cx_ - arm * 0.17), int(cy_ - arm)), (int(cx_ + arm * 0.17), int(cy_ + arm)), cross, -1, cv2.LINE_AA)
        cv2.rectangle(cv, (int(cx_ - arm), int(cy_ - arm * 0.17)), (int(cx_ + arm), int(cy_ + arm * 0.17)), cross, -1, cv2.LINE_AA)
    cv2.line(cv, (int(x - 150 * s), int(y + bob - 20 * s)), (int(x - 310 * s), int(y + bob - 70 * s)), col, max(2, int(4 * s)), cv2.LINE_AA)


def carracks(dur, base, ships=((0.34, 0.505, 0.62), (0.66, 0.50, 0.40)), t0=0.0, haze=(255, 170, 100)):
    """real sea footage frame fn `base(t,d,st)->img` with carrack silhouettes sailing along the horizon."""
    def fn(t, d, st):
        f = base(t, d, st).copy()
        lay = np.zeros_like(f)
        for k, (xf, yf, sc) in enumerate(ships):
            x = (xf + 0.04 * (t / d) * (1 if k % 2 == 0 else -1)) * W
            y = yf * H
            _carrack(lay, x, y, sc, 4 * math.sin(t * 0.9 + k * 2.0))
        m = (lay.sum(axis=2) > 0).astype(np.float32)
        m = cv2.GaussianBlur(m, (0, 0), 1.2)[..., None]
        lay = cv2.GaussianBlur(lay, (0, 0), 0.9)
        # warm atmospheric haze lifts the silhouettes slightly toward the sky colour
        lay = np.clip(lay.astype(np.float32) * 0.9 + np.array(haze, np.float32) * 0.07, 0, 255)
        f = (f * (1 - m) + lay * m).astype(np.uint8)
        # soft reflection below the waterline
        return f
    return FuncShotF(fn, dur)


# --------------------------------------------------------------------------------------------- colour-bleach effect (coral dying)
def bleach_fx(start=0.0, end=1.0, hold=True):
    """effect for Layered: fraction of shot duration over which colour drains and highlights rise."""
    def fx(f, t, d):
        u = smooth((t / d - start) / max(end - start, 1e-3))
        if u <= 0.001:
            return f
        g = f.astype(np.float32)
        gray = g.mean(axis=2, keepdims=True)
        out = g * (1 - 0.92 * u) + gray * 0.92 * u
        out = out + (255 - out) * 0.16 * u + np.array([6, 10, 8], np.float32) * u
        return np.clip(out, 0, 255).astype(np.uint8)
    return fx


# --------------------------------------------------------------------------------------------- warm-ocean anomaly map (El Nino 2016)
def heat_map(dur, t0=0.0):
    gv = G.GeoView(extra=())
    cam = G.cam_path([(0, 75.0, 8.0, 52.0), (dur, 73.0, 9.0, 34.0)])
    rng = np.random.default_rng(31)
    base = cv2.resize(rng.random((18, 32)).astype(np.float32), (W // 4, H // 4), interpolation=cv2.INTER_CUBIC)
    base = cv2.GaussianBlur(base, (0, 0), 6)
    base = (base - base.min()) / (base.max() - base.min())

    def fn(t, d, st):
        lon, lat, span = cam(t)
        f = gv.render(lon, lat, span)
        f = (f.astype(np.float32) * 0.75).astype(np.uint8)
        u = smooth((t - 0.4) / (d * 0.75))
        # anomaly field: warm pool centred over the Indian Ocean, wobbling
        yy, xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)
        cxp, cyp = (W / 8) * 1.05, (H / 8) * 1.05
        r = np.sqrt(((xx - cxp) / (W / 4 * 0.62)) ** 2 + ((yy - cyp) / (H / 4 * 0.78)) ** 2)
        field = np.clip((1.2 * u - r) * 1.6 + (base - 0.5) * 0.9 * u, 0, 1)
        field = cv2.GaussianBlur(field, (0, 0), 5)
        # colour ramp: transparent -> amber -> red -> white-hot
        ramp = np.zeros((H // 4, W // 4, 3), np.float32)
        ramp[..., 0] = np.clip(field * 2.4, 0, 1) * 255
        ramp[..., 1] = np.clip(field * 1.9 - 0.55, 0, 1) * 200
        ramp[..., 2] = np.clip(field * 1.6 - 1.0, 0, 1) * 160
        ramp = cv2.resize(ramp, (W, H), interpolation=cv2.INTER_CUBIC)
        a = cv2.resize(np.clip(field * 1.1, 0, 0.55), (W, H), interpolation=cv2.INTER_CUBIC)[..., None]
        f = (f * (1 - a) + ramp * a * 0.9).clip(0, 255).astype(np.uint8)
        f = G.label(f, 'EL NINO  2016', 120, H - 120, smooth((t - 0.8) / 0.7) * smooth((d - t) / 0.6), size=34)
        return f
    return FuncShotF(fn, dur)


# --------------------------------------------------------------------------------------------- split-screen slider wipe
def split_wipe(dur, fa, fb, slider=((0, 0.5), (1, 0.5)), angle=0.0, bar=True):
    """fa/fb: frame functions f(t,d,st)->img. slider: [(t_frac, x_frac)] left side shows A, right side B."""
    xs = np.array([k[0] for k in slider]); vs = np.array([k[1] for k in slider])

    def fn(t, d, st):
        a = fa(t, d, st); b = fb(t, d, st)
        x = float(np.interp(t / d, xs, vs)) * W
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        edge = x + (yy - H / 2) * math.tan(math.radians(angle))
        m = np.clip((xx - edge) / 3.0, 0, 1)[..., None]
        out = (a * (1 - m) + b * m).astype(np.uint8)
        if bar:
            bl = np.clip(1 - np.abs(xx - edge) / 3.0, 0, 1)[..., None]
            out = np.clip(out.astype(np.float32) + bl * 255 * 0.9 + cv2.GaussianBlur(bl[..., 0], (0, 0), 10)[..., None] * 90, 0, 255).astype(np.uint8)
        return out
    return FuncShotF(fn, dur)


# --------------------------------------------------------------------------------------------- zoom-out from the island to the planet
def island_to_earth(dur, island='bangaram', t0=0.0):
    gv = G.GeoView(extra=('mid_north', island))
    lon0, lat0 = (72.30, 10.915) if island == 'bangaram' else (72.2, 10.86)
    cam = G.cam_path([(0, lon0, lat0, 0.07), (dur * 0.38, 72.4, 10.9, 0.9), (dur * 0.62, 72.8, 10.8, 7.0), (dur * 0.86, 76.0, 14.0, 60.0), (dur, 70.0, 12.0, 130.0)])

    def fn(t, d, st):
        lon, lat, span = cam(t)
        return gv.render(lon, lat, span)
    return FuncShotF(fn, dur)
