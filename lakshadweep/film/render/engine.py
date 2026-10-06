"""Frame-level compositor for the Lakshadweep film.

A *shot* is any object with .dur (seconds) and .frame(t, ctx) -> uint8 RGB (H,W,3), t in [0,dur].
A *timeline entry* places a shot at a global start time with a transition-in overlap.
All heavy lifting is numpy + OpenCV (no GPU)."""
import os, sys, subprocess, json, math, functools
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, features

cv2.setNumThreads(1)
W, H, FPS = 1920, 1080, 24
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, 'assets')
FONTS = os.path.join(ASSETS, 'fonts')


# ----------------------------------------------------------------------------- small helpers
def smooth(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def smoother(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * x * (x * (x * 6 - 15) + 10)


def ease_io(x, p=2.2):
    x = np.clip(x, 0.0, 1.0)
    return np.where(x < .5, .5 * (2 * x) ** p, 1 - .5 * (2 - 2 * x) ** p)


def lerp(a, b, x):
    return a + (b - a) * x


@functools.lru_cache(None)
def font(name, size, var=None):
    f = ImageFont.truetype(os.path.join(FONTS, name), size, layout_engine=ImageFont.Layout.RAQM)
    if var:
        try:
            f.set_variation_by_axes(list(var))
        except Exception:
            pass
    return f


@functools.lru_cache(None)
def load_img(path, max_side=None):
    im = cv2.imread(path, cv2.IMREAD_COLOR)
    if im is None:
        raise FileNotFoundError(path)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    if max_side and max(im.shape[:2]) > max_side:
        s = max_side / max(im.shape[:2])
        im = cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    return im


def cover_resize(im, w=W, h=H):
    """resize+center-crop to fill w x h."""
    ih, iw = im.shape[:2]
    s = max(w / iw, h / ih)
    r = cv2.resize(im, (int(math.ceil(iw * s)), int(math.ceil(ih * s))), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
    y0 = (r.shape[0] - h) // 2; x0 = (r.shape[1] - w) // 2
    return r[y0:y0 + h, x0:x0 + w]


def crop_zoom(im, cx, cy, zoom, w=W, h=H, rot=0.0, interp=cv2.INTER_LINEAR, border=cv2.BORDER_REFLECT):
    """Virtual camera on a big image. (cx,cy) in source pixels = view centre, zoom = output px per source px."""
    M = cv2.getRotationMatrix2D((cx, cy), rot, 1.0)
    # we want: source (cx,cy) -> output centre, scaled by zoom
    A = np.array([[zoom, 0, w / 2 - cx * zoom], [0, zoom, h / 2 - cy * zoom]], np.float64)
    if rot:
        R = cv2.getRotationMatrix2D((w / 2, h / 2), rot, 1.0)
        A = (np.vstack([R, [0, 0, 1]]) @ np.vstack([A, [0, 0, 1]]))[:2]
    return cv2.warpAffine(im, A, (w, h), flags=interp, borderMode=border)


# ----------------------------------------------------------------------------- ffmpeg clip reader
class ClipReader:
    """Sequential reader of a pre-conformed clip (1920x1080, 24 fps). Loops/holds last frame."""

    def __init__(self, path, w=W, h=H):
        self.path = path; self.w, self.h = w, h
        self.proc = None; self.idx = -1; self.last = None
        info = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_packets', '-show_entries',
                               'stream=nb_read_packets', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip()
        try:
            self.n = int(info.split(',')[0])
        except Exception:
            self.n = 10 ** 9

    def _open(self):
        self.proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', self.path, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                                     stdout=subprocess.PIPE, stdin=subprocess.DEVNULL, bufsize=self.w * self.h * 3 * 4)
        self.idx = -1

    def get(self, i):
        i = int(max(0, min(i, self.n - 1)))
        if self.proc is None or i < self.idx:
            if self.proc:
                self.proc.kill()
            self._open()
        while self.idx < i:
            buf = self.proc.stdout.read(self.w * self.h * 3)
            if len(buf) < self.w * self.h * 3:
                break
            self.last = np.frombuffer(buf, np.uint8).reshape(self.h, self.w, 3)
            self.idx += 1
        return self.last

    def close(self):
        if self.proc:
            self.proc.kill(); self.proc = None


# ----------------------------------------------------------------------------- shot classes
class Shot:
    dur = 3.0

    def frame(self, t, ctx=None):  # pragma: no cover
        raise NotImplementedError

    def close(self):
        pass


class VideoShot(Shot):
    """Pre-conformed 1080p24 clip. Optional virtual-camera move on top (zoom/pan), clip starts at `ss` seconds."""

    def __init__(self, path, dur, ss=0.0, zoom=(1.0, 1.08), pan=(0.0, 0.0, 0.0, 0.0), hold_speed=1.0, flip=False):
        self.path = path; self.dur = dur; self.ss = ss; self.zoom = zoom; self.pan = pan
        self.speed = hold_speed; self.flip = flip
        self.r = None

    def frame(self, t, ctx=None):
        if self.r is None:
            self.r = ClipReader(self.path)
        fr = self.r.get(int((self.ss + t * self.speed) * FPS))
        z = lerp(self.zoom[0], self.zoom[1], smooth(t / self.dur))
        px = lerp(self.pan[0], self.pan[2], t / self.dur); py = lerp(self.pan[1], self.pan[3], t / self.dur)
        if self.flip:
            fr = fr[:, ::-1]
        if abs(z - 1.0) < 1e-4 and px == 0 and py == 0:
            return np.ascontiguousarray(fr)
        return crop_zoom(fr, W / 2 + px * W, H / 2 + py * H, z)

    def close(self):
        if self.r:
            self.r.close()


@functools.lru_cache(maxsize=48)
def _prep_still(path, max_side):
    im = load_img(path, max_side)
    if im.shape[1] < 2200:
        s = 2400 / im.shape[1]
        im = cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_LANCZOS4)
        bl = cv2.GaussianBlur(im, (0, 0), 2.2)
        im = cv2.addWeighted(im, 1.55, bl, -0.55, 0)
    return im


class StillShot(Shot):
    """Ken-Burns over a still with parallax-ish extras. path -> big image (any aspect)."""

    def __init__(self, path, dur, z0=1.0, z1=1.15, p0=(0.5, 0.5), p1=(0.5, 0.5), rot=(0, 0), shake=0.0, max_side=4200, fill=True):
        self.im = _prep_still(path, max_side)
        self.dur = dur; self.z0, self.z1 = z0, z1; self.p0, self.p1 = p0, p1; self.rot = rot; self.shake = shake
        ih, iw = self.im.shape[:2]
        self.base = max(W / iw, H / ih)   # scale to just cover
        self.seed = (hash(path) % 997) / 997.0 * 6.28

    def frame(self, t, ctx=None):
        x = t / self.dur
        e = smooth(x) * 0.6 + x * 0.4
        z = lerp(self.z0, self.z1, e) * self.base
        ih, iw = self.im.shape[:2]
        px = lerp(self.p0[0], self.p1[0], e); py = lerp(self.p0[1], self.p1[1], e)
        # clamp so the view stays inside the image
        vw, vh = W / z, H / z
        cx = np.clip(px * iw, vw / 2, iw - vw / 2); cy = np.clip(py * ih, vh / 2, ih - vh / 2)
        if self.shake:
            cx += self.shake * (math.sin(t * 1.7 + self.seed) + 0.5 * math.sin(t * 4.3)) * vw * 0.004
            cy += self.shake * (math.cos(t * 1.3 + self.seed) + 0.5 * math.sin(t * 3.7)) * vh * 0.004
        return crop_zoom(self.im, cx, cy, z, rot=lerp(self.rot[0], self.rot[1], e), interp=cv2.INTER_CUBIC if z > 1 else cv2.INTER_AREA)


class FuncShot(Shot):
    def __init__(self, fn, dur, init=None):
        self.fn = fn; self.dur = dur; self.state = {}
        self.init = init

    def frame(self, t, ctx=None):
        return self.fn(t, self.dur, self.state)


# ----------------------------------------------------------------------------- transitions
def _blur_dir(img, k, horizontal=True):
    if k < 2:
        return img
    k = int(k) | 1
    return cv2.blur(img, (k, 1) if horizontal else (1, k))


def tr_dissolve(a, b, p):
    p = smooth(p)
    return cv2.addWeighted(a, 1 - p, b, p, 0)


def tr_dip(a, b, p, color=0):
    p2 = p * 2
    if p < .5:
        f = smooth(p2)
        return (a.astype(np.float32) * (1 - f) + color * f).astype(np.uint8)
    f = smooth(p2 - 1)
    return (color * (1 - f) + b.astype(np.float32) * f).astype(np.uint8)


def tr_whip(a, b, p, direction=1):
    """fast horizontal slide with motion blur."""
    p = smoother(p)
    off = int(direction * W * p)
    sh_a = np.roll(a, -off, axis=1); sh_b = np.roll(b, int(direction * (W - W * p)) * 1, axis=1)
    # compose: A slides out left, B slides in from right
    canvas = np.empty_like(a)
    x = int(W * p) * direction
    if direction > 0:
        canvas[:, :W - x] = a[:, x:]; canvas[:, W - x:] = b[:, :x]
    else:
        x = -x
        canvas[:, x:] = a[:, :W - x]; canvas[:, :x] = b[:, W - x:]
    k = int(10 + 160 * math.sin(math.pi * min(max(p, 0), 1)) ** 1.5)
    return _blur_dir(canvas, k, True)


def tr_zoom(a, b, p):
    """push-through: A zooms+blurs out, B zooms in from slightly large."""
    p = smooth(p)
    za = 1 + 0.55 * p ** 1.6
    zb = 1.35 - 0.35 * p
    fa = crop_zoom(a, W / 2, H / 2, za)
    fb = crop_zoom(b, W / 2, H / 2, zb)
    k = int(3 + 70 * math.sin(math.pi * p) ** 1.2)
    fa = cv2.GaussianBlur(fa, (0, 0), k * 0.25 + 0.1) if k > 2 else fa
    fb = cv2.GaussianBlur(fb, (0, 0), k * 0.25 + 0.1) if k > 2 else fb
    m = smooth((p - 0.35) / 0.3)
    return cv2.addWeighted(fa, 1 - m, fb, m, 0)


def tr_flare(a, b, p):
    """cross-dissolve through a warm light flash."""
    f = math.sin(math.pi * p) ** 2.2
    base = tr_dissolve(a, b, p).astype(np.float32)
    glow = cv2.GaussianBlur(base, (0, 0), 40) * 0.5
    out = base + (glow + 70) * f * np.array([1.0, 0.88, 0.7], np.float32)
    return np.clip(out, 0, 255).astype(np.uint8)


@functools.lru_cache(None)
def _radial_dist():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt((xx - W / 2) ** 2 + (yy - H / 2) ** 2) / math.hypot(W / 2, H / 2)
    return d


def tr_iris(a, b, p):
    """circular reveal of B from the centre with soft edge."""
    d = _radial_dist(); r = smooth(p) * 1.15
    m = np.clip((r - d) / 0.12, 0, 1)[..., None]
    return (a * (1 - m) + b * m).astype(np.uint8)


@functools.lru_cache(None)
def _noise_field():
    rng = np.random.default_rng(3)
    n = rng.random((H // 40 + 2, W // 40 + 2)).astype(np.float32)
    n = cv2.resize(n, (W, H), interpolation=cv2.INTER_CUBIC)
    n = cv2.GaussianBlur(n, (0, 0), 30)
    n = (n - n.min()) / (n.max() - n.min())
    return n


def tr_luma(a, b, p):
    """organic cloud-like dissolve."""
    n = _noise_field(); t = smooth(p) * 1.3 - 0.15
    m = np.clip((t - n) / 0.15, 0, 1)[..., None]
    return (a * (1 - m) + b * m).astype(np.uint8)


def tr_cut(a, b, p):
    return b if p >= 0.5 else a


TRANS = dict(dissolve=tr_dissolve, dip=tr_dip, whip=tr_whip, zoom=tr_zoom, flare=tr_flare, iris=tr_iris, luma=tr_luma, cut=tr_cut,
             dipwhite=lambda a, b, p: tr_dip(a, b, p, 255))


# ----------------------------------------------------------------------------- grading
@functools.lru_cache(None)
def _vignette(strength):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    v = 1 - strength * np.clip(d - 0.35, 0, None) ** 1.7
    return np.clip(v, 0.3, 1)[..., None].astype(np.float32)


@functools.lru_cache(None)
def _grain_bank():
    rng = np.random.default_rng(99)
    bank = []
    for _ in range(12):
        g = rng.standard_normal((H // 2, W // 2)).astype(np.float32)
        g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)
        bank.append((g * 3.2).astype(np.int16))
    return bank


@functools.lru_cache(None)
def _lut(contrast, lift, gain, tint_sh, tint_hi, sat):
    """returns three 256-entry LUTs (R,G,B) implementing filmic S-curve + split tone."""
    x = np.arange(256) / 255.0
    # filmic-ish S curve (toe & shoulder)
    y = x + contrast * (x - 0.5) * (1 - np.abs(2 * x - 1)) * 1.0
    y = np.clip(y * gain + lift, 0, 1)
    luts = []
    for c in range(3):
        sh = (1 - y) ** 2 * tint_sh[c]
        hi = y ** 2 * tint_hi[c]
        luts.append(np.clip((y + sh + hi) * 255, 0, 255).astype(np.uint8))
    return luts


GRADES = {
    'neutral': dict(contrast=0.5, lift=0.0, gain=1.0, tint_sh=(-.010, .012, .028), tint_hi=(.030, .012, -.020), sat=1.08),
    'teal': dict(contrast=0.6, lift=0.0, gain=1.0, tint_sh=(-.020, .018, .040), tint_hi=(.035, .010, -.030), sat=1.12),
    'warm': dict(contrast=0.5, lift=0.0, gain=1.02, tint_sh=(.012, .004, .010), tint_hi=(.050, .020, -.040), sat=1.10),
    'cold': dict(contrast=0.6, lift=0.0, gain=0.97, tint_sh=(-.020, .005, .045), tint_hi=(-.010, .012, .030), sat=0.92),
    'storm': dict(contrast=0.75, lift=-0.01, gain=0.92, tint_sh=(-.025, .000, .040), tint_hi=(-.020, .005, .018), sat=0.70),
    'bleach': dict(contrast=0.5, lift=0.01, gain=1.0, tint_sh=(.00, .00, .020), tint_hi=(.010, .010, .010), sat=0.45),
    'sepia': dict(contrast=0.55, lift=0.0, gain=0.98, tint_sh=(.030, .012, -.010), tint_hi=(.050, .030, -.020), sat=0.50),
    'dusk': dict(contrast=0.6, lift=0.0, gain=0.98, tint_sh=(-.005, -.005, .040), tint_hi=(.060, .015, -.040), sat=1.10),
}


def grade(img, g, vig=0.55, bloom=0.18, grain=True, fi=0):
    p = GRADES[g] if isinstance(g, str) else g
    luts = _lut(p['contrast'], p['lift'], p['gain'], p['tint_sh'], p['tint_hi'], p['sat'])
    out = cv2.merge([cv2.LUT(img[..., c], luts[c]) for c in range(3)])
    if abs(p['sat'] - 1) > 0.01:
        hsv = cv2.cvtColor(out, cv2.COLOR_RGB2HSV)
        hsv[..., 1] = np.clip(hsv[..., 1].astype(np.float32) * p['sat'], 0, 255).astype(np.uint8)
        out = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    if bloom:
        small = cv2.resize(out, (W // 6, H // 6), interpolation=cv2.INTER_AREA)
        lum = cv2.cvtColor(small, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
        m = np.clip((lum - 0.62) / 0.38, 0, 1)[..., None]
        hi = cv2.GaussianBlur((small.astype(np.float32) * m), (0, 0), 9)
        hi = cv2.resize(hi, (W, H), interpolation=cv2.INTER_LINEAR)
        out = np.clip(out.astype(np.float32) + hi * bloom * 1.6, 0, 255).astype(np.uint8)
    if vig:
        out = (out.astype(np.float32) * _vignette(vig)).astype(np.uint8)
    if grain:
        gb = _grain_bank()[fi % 12]
        out = np.clip(out.astype(np.int16) + gb[..., None], 0, 255).astype(np.uint8)
    return out


# ----------------------------------------------------------------------------- overlay: subtitles / titles
def _is_latin(c):
    return c.isascii() and c.isalpha()


def _runs(text):
    runs = []
    for c in text:
        lat = _is_latin(c)
        if runs and runs[-1][0] == lat:
            runs[-1][1] += c
        else:
            runs.append([lat, c])
    return runs


def _mixed_len(runs_fonts, text):
    return sum((ft_la if lat else ft_te).getlength(r) for lat, r, ft_te, ft_la in [(l, r, runs_fonts[0], runs_fonts[1]) for l, r in _runs(text)])


@functools.lru_cache(None)
def _sub_layer(text):
    """pre-render a Telugu subtitle (mixed Telugu/Latin script) with soft shadow; wraps to <=2 lines."""
    f_te = font('NotoSansTelugu-Regular.ttf', 46)
    f_la = font('Jost[wght].ttf', 47, (440,))
    fonts = (f_te, f_la)
    maxw = 1500
    words = text.split(' ')
    lines = []; cur = ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if _mixed_len(fonts, t) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w_
    lines.append(cur)
    if len(lines) > 2:   # rebalance into 2 lines at the best word split
        words = text.split(' '); best = None
        for i in range(1, len(words)):
            a_ = ' '.join(words[:i]); b_ = ' '.join(words[i:])
            m = max(_mixed_len(fonts, a_), _mixed_len(fonts, b_))
            if best is None or m < best[0]:
                best = (m, a_, b_)
        lines = [best[1], best[2]]
    lh = 74
    h = lh * len(lines) + 40
    lay = Image.new('L', (W, h), 0)
    d = ImageDraw.Draw(lay)
    for i, ln in enumerate(lines):
        total = _mixed_len(fonts, ln)
        x = (W - total) / 2
        base_y = 20 + i * lh + lh * 0.68
        for lat, r in _runs(ln):
            ft = f_la if lat else f_te
            d.text((x, base_y), r, font=ft, fill=255, anchor='ls')
            x += ft.getlength(r)
    a = np.array(lay).astype(np.float32) / 255.0
    sh = cv2.GaussianBlur(a, (0, 0), 6) * 0.9
    sh2 = cv2.GaussianBlur(a, (0, 0), 2) * 0.8
    return a, np.clip(sh + sh2, 0, 1), h


def draw_subtitle(img, text, alpha, y_bottom=1010):
    if alpha <= 0.01 or not text:
        return img
    a, sh, h = _sub_layer(text)
    # soft legibility gradient over the whole lower third (no visible edge)
    gh = 380
    g = np.linspace(0, 1, gh, dtype=np.float32)
    g = (g * g * (3 - 2 * g))[:, None, None] * 0.42 * alpha
    reg = img[H - gh:H].astype(np.float32)
    img[H - gh:H] = (reg * (1 - g)).astype(np.uint8)
    y0 = y_bottom - h
    reg = img[y0:y0 + h].astype(np.float32)
    reg *= (1 - sh[..., None] * 0.55 * alpha)
    reg = reg + (255 - reg) * (a[..., None] * 0.97 * alpha)
    img[y0:y0 + h] = np.clip(reg, 0, 255).astype(np.uint8)
    return img


@functools.lru_cache(None)
def _title_layer(kind, text, size, spacing, fname, tint):
    """text rendered once as float alpha mask."""
    f = font(fname, size)
    # manual letter spacing
    lay = Image.new('L', (W, 260), 0)
    d = ImageDraw.Draw(lay)
    if spacing:
        total = sum(f.getlength(c) for c in text) + spacing * (len(text) - 1)
        x = (W - total) / 2
        for c in text:
            d.text((x, 130), c, font=f, fill=255, anchor='lm'); x += f.getlength(c) + spacing
    else:
        d.text((W / 2, 130), text, font=f, fill=255, anchor='mm')
    return np.array(lay).astype(np.float32) / 255.0


def draw_title(img, text, cy, alpha, size=64, spacing=0, fname='Marcellus-Regular.ttf', color=(255, 255, 255), glow=True, dx=0):
    if alpha <= 0.01:
        return img
    a = _title_layer('t', text, size, spacing, fname, 0)
    y0 = int(cy - 130)
    y0 = max(0, min(H - 260, y0))
    if dx:
        a = np.roll(a, int(dx), axis=1)
    reg = img[y0:y0 + 260].astype(np.float32)
    if glow:
        gl = cv2.GaussianBlur(a, (0, 0), 14) * 0.55
        reg *= (1 - gl[..., None] * 0.55 * alpha)
    col = np.array(color, np.float32)
    reg = reg * (1 - a[..., None] * alpha) + col * a[..., None] * alpha
    img[y0:y0 + 260] = np.clip(reg, 0, 255).astype(np.uint8)
    return img


def draw_hline(img, x0, x1, y, alpha=1.0, thick=2, color=(255, 255, 255)):
    if alpha <= 0.01 or x1 <= x0:
        return img
    ov = img[y:y + thick, int(x0):int(x1)].astype(np.float32)
    ov = ov * (1 - alpha) + np.array(color, np.float32) * alpha
    img[y:y + thick, int(x0):int(x1)] = ov.astype(np.uint8)
    return img


def draw_tag(img, title, sub, alpha, prog=1.0, x=110, y=96):
    """location lower-third: thin line + small caps title + coordinates."""
    if alpha <= 0.01:
        return img
    L = int(260 * smooth(prog))
    draw_hline(img, x, x + L, y, alpha * 0.85)
    ft = font('Marcellus-Regular.ttf', 34); fs = font('Jost[wght].ttf', 22, (400,))
    lay = Image.new('L', (900, 120), 0); d = ImageDraw.Draw(lay)
    tx = 0
    for c in title.upper():
        d.text((tx, 8), c, font=ft, fill=255); tx += ft.getlength(c) + 5
    sx = 0
    for c in sub.upper():
        d.text((sx, 66), c, font=fs, fill=235); sx += fs.getlength(c) + 3.5
    a = np.array(lay).astype(np.float32) / 255.0
    a = a[:, :int(900 * 1)]
    yy = y + 10
    reg = img[yy:yy + 120, x:x + 900].astype(np.float32)
    sh = cv2.GaussianBlur(a, (0, 0), 5) * 0.6
    reg *= (1 - sh[..., None] * alpha)
    reg = reg * (1 - a[..., None] * alpha) + 255 * a[..., None] * alpha
    img[yy:yy + 120, x:x + 900] = np.clip(reg, 0, 255).astype(np.uint8)
    return img


# ----------------------------------------------------------------------------- compositor
class Entry:
    """A cut on the timeline. `factory(dur)` builds the shot once the timeline knows how long it must live
    (until the next cut starts plus that cut's transition overlap)."""

    def __init__(self, start, factory, trans='dissolve', tdur=0.8, grade_name=None, name=''):
        self.start = start; self.factory = factory; self.trans = trans if tdur > 0 else 'cut'
        self.tdur = tdur if trans != 'cut' else 0.0; self.grade = grade_name; self.name = name
        self.shot = None; self.dur = None


def render_entry_frame(e, T, ctx=None):
    if e.shot is None:
        e.shot = e.factory(e.dur)
        e.shot.dur = e.dur
    t = T - e.start
    t = min(max(t, 0), e.shot.dur - 1.0 / FPS)
    f = e.shot.frame(t, ctx)
    if f.shape[0] != H or f.shape[1] != W:
        f = cv2.resize(f, (W, H))
    return f


class Timeline:
    def __init__(self, entries, total, subs=None, tags=None, overlays=None, default_grade='neutral'):
        self.entries = sorted(entries, key=lambda e: e.start)
        es = self.entries
        for i, e in enumerate(es):
            nxt = es[i + 1] if i + 1 < len(es) else None
            end = (nxt.start + nxt.tdur) if nxt else total
            e.dur = max(end - e.start, 0.5)
            e.shot = None            # built lazily (keeps memory flat when rendering a long timeline)
        self.total = total
        subs = sorted(subs or [])
        self.subs = []                # (t0,t1,text) with non-overlapping display windows
        for i, (a0, a1, tx) in enumerate(subs):
            nxt = subs[i + 1][0] if i + 1 < len(subs) else 1e9
            self.subs.append((a0, min(a1 + 0.12, nxt - 0.14), tx))
        self.tags = tags or []        # (t0,t1,title,sub)
        self.overlays = overlays or []  # callables (img, T) -> img
        self.default_grade = default_grade

    def _idx(self, T):
        lo = 0
        for i, e in enumerate(self.entries):
            if e.start <= T + 1e-9:
                lo = i
        return lo

    def release_old(self, T):
        for e in self.entries:
            if e.shot is not None and T > e.start + e.dur + 0.5:
                try:
                    e.shot.close()
                except Exception:
                    pass
                e.shot = None; e.factory = (lambda dur: (_ for _ in ()).throw(RuntimeError('rebuilt after release')))

    def frame_at(self, T, fi):
        es = self.entries
        i = self._idx(T)
        e = es[i]
        cur = render_entry_frame(e, T)
        g_c = e.grade or self.default_grade
        gc = grade(cur, g_c, fi=fi, bloom=0.0, vig=0.0, grain=False)
        if i > 0 and e.trans != 'cut' and T < e.start + e.tdur:
            prev = es[i - 1]
            p = (T - e.start) / max(e.tdur, 1e-3)
            a = render_entry_frame(prev, T)
            ga = grade(a, prev.grade or self.default_grade, fi=fi, bloom=0.0, vig=0.0, grain=False)
            out = TRANS[e.trans](ga, gc, p)
        else:
            out = gc
        return self._finish(out, T, fi)

    def _finish(self, img, T, fi):
        # global film finish: bloom + vignette + grain run once on the composited frame
        img = _finish_look(img, fi)
        for fn in self.overlays:
            img = fn(img, T)
        for (t0, t1, title, sub) in self.tags:
            if t0 - 0.01 <= T <= t1 + 0.01:
                a = smooth((T - t0) / 0.6) * smooth((t1 - T) / 0.6)
                img = draw_tag(img, title, sub, a, prog=smooth((T - t0) / 1.0))
        for (t0, t1, text) in self.subs:
            if t0 - 0.2 <= T <= t1 + 0.1:
                a = smooth((T - (t0 - 0.08)) / 0.16) * smooth((t1 + 0.1 - T) / 0.16)
                img = draw_subtitle(img, text, a)
        return img


def _finish_look(img, fi, vig=0.55, bloom=0.16):
    small = cv2.resize(img, (W // 6, H // 6), interpolation=cv2.INTER_AREA)
    lum = cv2.cvtColor(small, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
    m = np.clip((lum - 0.62) / 0.38, 0, 1)[..., None]
    hi = cv2.GaussianBlur((small.astype(np.float32) * m), (0, 0), 9)
    hi = cv2.resize(hi, (W, H), interpolation=cv2.INTER_LINEAR)
    out = img.astype(np.float32) + hi * bloom * 1.6
    out *= _vignette(vig)
    out += _grain_bank()[fi % 12][..., None]
    return np.clip(out, 0, 255).astype(np.uint8)


def write_range(tl, t0, t1, out_path, crf=16, preset='veryfast'):
    """render frames [t0,t1) of the timeline to an mp4 (video only)."""
    n0 = int(round(t0 * FPS)); n1 = int(round(t1 * FPS))
    cmd = ['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-preset', preset, '-crf', str(crf), '-pix_fmt', 'yuv420p', '-an', out_path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(n0, n1):
        T = n / FPS
        fr = tl.frame_at(T, n)
        if n % 48 == 0:
            tl.release_old(T)
        p.stdin.write(np.ascontiguousarray(fr).tobytes())
    p.stdin.close(); p.wait()
