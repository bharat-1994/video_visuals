"""Geo camera: multi-resolution satellite dive using real NASA GIBS imagery, plus map overlays."""
import os, math, functools
import numpy as np, cv2
from engine import W, H, FPS, ASSETS, load_img, crop_zoom, smooth, smoother, lerp, font
from PIL import Image, ImageDraw

MAPS = os.path.join(ASSETS, 'maps')


class Layer:
    def __init__(self, fname, bbox, max_side=None):
        self.im = load_img(os.path.join(MAPS, fname), max_side)
        self.lon0, self.lat0, self.lon1, self.lat1 = bbox
        self.ppd = self.im.shape[1] / (self.lon1 - self.lon0)          # pixels per degree (x)
        self.ppd_y = self.im.shape[0] / (self.lat1 - self.lat0)

    def contains(self, lon, lat, span):
        hw = span / 2; hh = span * H / W / 2
        return (lon - hw >= self.lon0 and lon + hw <= self.lon1 and lat - hh >= self.lat0 and lat + hh <= self.lat1)

    def mask_view(self, cx, cy, zoom):
        """feathered coverage mask (H,W float): ramp toward the layer's own edges so patches melt into the layer below."""
        if not hasattr(self, '_ms'):
            h, w = max(4, self.im.shape[0] // 32), max(4, self.im.shape[1] // 32)
            pad = np.zeros((h + 2, w + 2), np.uint8); pad[1:-1, 1:-1] = 1
            d = cv2.distanceTransform(pad, cv2.DIST_L2, 3)[1:-1, 1:-1]
            ramp = 0.14 * min(h, w)
            self._ms = np.clip(d / ramp, 0, 1).astype(np.float32) ** 1.2
        m = crop_zoom(self._ms, cx / 32, cy / 32, zoom * 4, w=W // 8, h=H // 8, interp=cv2.INTER_LINEAR, border=cv2.BORDER_CONSTANT)
        m = cv2.resize(m, (W, H), interpolation=cv2.INTER_CUBIC)
        return np.clip(m, 0, 1)

    def to_px(self, lon, lat):
        return (lon - self.lon0) * self.ppd, (self.lat1 - lat) * self.ppd_y


@functools.lru_cache(None)
def default_layers():
    return [
        Layer('world_bm.jpg', (-180, -90, 180, 90)),
        Layer('trade_bm.jpg', (40, 0, 85, 30)),
        Layer('bm_region.jpg', (60, 0, 90, 28)),
        Layer('ridge_bathy.jpg', (66, 4, 78, 16)),
        Layer('mid_all_mo_m.jpg', (70.5, 7.5, 75.5, 12.5)),
    ]


# fine layers (30 m satellite) that can be appended to the default stack for a specific island dive
FINE = {
    'agatti': ('agatti_hls_m.jpg', (72.00, 10.74, 72.40, 10.965)),
    'minicoy': ('minicoy_hls_m.jpg', (72.85, 8.17, 73.25, 8.395)),
    'kavaratti': ('kavaratti_hls_m.jpg', (72.45, 10.46, 72.85, 10.685)),
    'kalpeni': ('kalpeni_hls_m.jpg', (73.45, 9.97, 73.85, 10.195)),
    'bangaram': ('bangaram_hls_m.jpg', (72.10, 10.80, 72.50, 11.025)),
    'kadmat': ('amini_kadmat_hls_e.jpg', (72.66, 11.08, 72.86, 11.25)),
    'bitra': ('bitra_hls_e.jpg', (72.08, 11.55, 72.24, 11.65)),
    'kiltan': ('kiltan_hls_e.jpg', (72.93, 11.42, 73.07, 11.5)),
    'mid_north': ('mid_north_m.jpg', (71.9, 10.4, 73.9, 11.8)),
    'mid_minicoy': ('mid_minicoy_m.jpg', (72.7, 8.0, 73.4, 8.55)),
    'mid_kalpeni': ('mid_kalpeni_m.jpg', (73.3, 9.8, 74.0, 10.35)),
}


@functools.lru_cache(None)
def fine_layer(name):
    f, bb = FINE[name]
    return Layer(f, bb)


class GeoView:
    def __init__(self, layers=None, extra=()):
        self.layers = list(layers or default_layers()) + [fine_layer(n) for n in extra]

    def render(self, lon, lat, span):
        base = None
        hh = span * H / W / 2; hw = span / 2
        for i, L in enumerate(self.layers):
            if i > 0 and (lon + hw < L.lon0 or lon - hw > L.lon1 or lat + hh < L.lat0 or lat - hh > L.lat1):
                continue
            vpx = span * L.ppd
            a = 1.0 if i == 0 else smooth((vpx - 0.5 * W) / (0.55 * W))
            if a <= 0.001:
                continue
            cx, cy = L.to_px(lon, lat)
            zoom = W / max(vpx, 1e-6)
            fr = crop_zoom(L.im, cx, cy, zoom, interp=cv2.INTER_AREA if zoom < 1 else cv2.INTER_CUBIC,
                           border=cv2.BORDER_CONSTANT)
            if i == 0:
                base = fr
                continue
            if L.contains(lon, lat, span):
                base = cv2.addWeighted(base, 1 - a, fr, a, 0)
            else:
                m = L.mask_view(cx, cy, zoom) * a
                base = (base * (1 - m[..., None]) + fr * m[..., None]).astype(np.uint8)
        return base

    @staticmethod
    def project(lon, lat, clon, clat, span):
        x = (lon - clon) / span * W + W / 2
        y = (clat - lat) / (span * H / W) * H + H / 2
        return x, y


def cam_path(keys):
    """keys: [(t, lon, lat, span)] -> f(t) -> (lon,lat,span) with smooth eased interpolation (span in log space)."""
    ks = sorted(keys)

    def f(t):
        if t <= ks[0][0]:
            return ks[0][1:]
        if t >= ks[-1][0]:
            return ks[-1][1:]
        for a, b in zip(ks[:-1], ks[1:]):
            if a[0] <= t <= b[0]:
                u = smoother((t - a[0]) / (b[0] - a[0]))
                lon = lerp(a[1], b[1], u); lat = lerp(a[2], b[2], u)
                span = math.exp(lerp(math.log(a[3]), math.log(b[3]), u))
                return lon, lat, span
    return f


# ------------------------------------------------------------------ overlay helpers (draw on an RGB uint8 frame)
def blend_add(img, layer, gain=1.0):
    return np.clip(img.astype(np.float32) + layer.astype(np.float32) * gain, 0, 255).astype(np.uint8)


def glow_layer(draw_fn, blur=9, scale=0.5):
    """draw_fn(canvas_uint8 RGB at reduced scale) draws bright shapes on black; returns upscaled glow + crisp layer."""
    sw, sh = int(W * scale), int(H * scale)
    cv = np.zeros((sh, sw, 3), np.uint8)
    draw_fn(cv, scale)
    crisp = cv2.resize(cv, (W, H), interpolation=cv2.INTER_LINEAR)
    g = cv2.GaussianBlur(cv, (0, 0), blur * scale)
    g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)
    return crisp, g


def marker_overlay(img, pts, t, color=(120, 235, 255), r=7, ring=True, alpha=1.0, pulse_phase=0.0, big=None):
    """pts: list of (x,y,appear_t) in px; draws pulsing glow dots."""
    def draw(cv, s):
        for (x, y, t0) in pts:
            if t < t0:
                continue
            u = min(1.0, (t - t0) / 0.35)
            rr = r * (0.4 + 0.6 * smooth(u))
            c = tuple(int(v * smooth(u) * alpha) for v in color)
            cv2.circle(cv, (int(x * s), int(y * s)), max(1, int(rr * s)), c, -1, cv2.LINE_AA)
            if ring:
                ph = ((t - t0) * 0.9 + pulse_phase) % 1.0
                c2 = tuple(int(v * (1 - ph) * 0.8 * alpha) for v in color)
                cv2.circle(cv, (int(x * s), int(y * s)), int((rr + 36 * ph) * s), c2, 2, cv2.LINE_AA)
    crisp, g = glow_layer(draw, blur=10)
    return blend_add(blend_add(img, g, 1.3), crisp, 1.0)


def path_overlay(img, pts_px, prog, color=(255, 214, 120), width=3, dash=True, head=True, alpha=1.0):
    """polyline through pts_px (list of (x,y)), drawn up to fraction prog with a glowing head."""
    pts = np.array(pts_px, np.float32)
    if len(pts) < 2:
        return img
    seg = np.sqrt(((pts[1:] - pts[:-1]) ** 2).sum(axis=1))
    tot = seg.sum()
    target = tot * np.clip(prog, 0, 1)

    def draw(cv, s):
        acc = 0.0
        last = pts[0]
        for i in range(len(pts) - 1):
            L = seg[i]
            if acc >= target:
                break
            take = min(L, target - acc)
            p1 = pts[i] + (pts[i + 1] - pts[i]) * (take / max(L, 1e-6))
            if dash:
                n = max(1, int(take / 22))
                for k in range(n):
                    a0 = pts[i] + (p1 - pts[i]) * (k / n); a1 = pts[i] + (p1 - pts[i]) * ((k + 0.58) / n)
                    cv2.line(cv, tuple((a0 * s).astype(int)), tuple((a1 * s).astype(int)), tuple(int(c * alpha) for c in color), max(1, int(width * s)), cv2.LINE_AA)
            else:
                cv2.line(cv, tuple((pts[i] * s).astype(int)), tuple((p1 * s).astype(int)), tuple(int(c * alpha) for c in color), max(1, int(width * s)), cv2.LINE_AA)
            acc += L; last = p1
        if head and 0 < prog < 1.0:
            cv2.circle(cv, tuple((last * s).astype(int)), int(9 * s), tuple(int(c * alpha) for c in (255, 255, 255)), -1, cv2.LINE_AA)
    crisp, g = glow_layer(draw, blur=8)
    return blend_add(blend_add(img, g, 1.1), crisp, 0.95)


def label(img, text, x, y, alpha=1.0, size=26, color=(255, 255, 255), fname='Marcellus-Regular.ttf', spacing=4, anchor='lm'):
    if alpha <= 0.01:
        return img
    f = font(fname, size)
    pad = 8
    wdt = int(sum(f.getlength(c) + spacing for c in text)) + pad * 2
    lay = Image.new('L', (wdt, size + 24), 0); d = ImageDraw.Draw(lay)
    xx = pad
    for c in text:
        d.text((xx, (size + 24) // 2), c, font=f, fill=255, anchor='lm'); xx += f.getlength(c) + spacing
    a = np.array(lay).astype(np.float32) / 255.0
    h, w = a.shape
    x0 = int(x if anchor[0] == 'l' else x - w / 2); y0 = int(y - h / 2)
    x0 = max(0, min(W - w, x0)); y0 = max(0, min(H - h, y0))
    reg = img[y0:y0 + h, x0:x0 + w].astype(np.float32)
    sh = cv2.GaussianBlur(a, (0, 0), 4) * 0.85
    reg *= (1 - sh[..., None] * alpha)
    reg = reg * (1 - a[..., None] * alpha) + np.array(color, np.float32) * a[..., None] * alpha
    img[y0:y0 + h, x0:x0 + w] = np.clip(reg, 0, 255).astype(np.uint8)
    return img
