"""Data-driven shots: one line of text per shot instead of a hand-written function.
A shot is a list of elements separated by " | ". Each element: TYPE then args (shlex: quote text with spaces).
Positional numbers come first (x y [s|size]), then key=value pairs, then timing tokens:
  @word      appear (pop) when that narration word starts   (@word#2 = 2nd occurrence, @word+0.3, @1.25 = seconds)
  out@word   vanish with a smoke puff
  key=a>b:@word:0.6   animate a param from a to b starting at @word over 0.6 s (eased)
Element types (registries are filled by the episode: BG, ASSETS, CAST, CUSTOM):
  bg NAME k=v                     background (static, drawn before the camera)
  cam push|pull|still|pan [z0 z1 cx cy [cx2 cy2]]
  shake @word [amp=0.6]           impact shake (adds a thud)
  p WHO x y s e=expr f=facing pose=name pose2=name@word legs=0 view=back walk=px_per_s talk=@w1~@w2 hat=0 to=x,y(side=1|-1 hand target)
  a NAME x y k=v                  asset call NAME(ctx, x, y, **kv) (t passed if accepted). With @ it pops in around (x,y).
  kw "TEXT" x y size              white outlined keyword
  st "TEXT" x y size rot=         yellow sticky note ('\\n' for 2 lines)
  tx "TEXT" x y size c=#hex anchor=c  typewriter text (time markers, labels)
  card "TEXT" sub="..."           black chapter card, typewriter
  cnt A B x y size fmt="${:,}B" dur=1.2   number counting A->B
  dlg "TEXT" x y tox toy          dialogue line with tick
  arrow x1 y1 x2 y2 c=#hex lw=10  arrow drawing itself
  bars x y w h vals=[..] labels=[..] fmt="{}" c=#hex   bar chart growing
  fn NAME k=v                     custom code: CUSTOM[NAME](ctx, t, dur, T, **kv); T(word)->seconds
  sfx NAME @word db=-6            extra sound
Auto sounds: pop on every pop-in / keyword / sticky, ticks on typewriter + counters, thud on shake, puff whoosh on out@.
"""
import shlex, ast, re, math, inspect
from lib import *

BG, ASSETS, CAST, CUSTOM, AMBIENCE = {}, {}, {}, {}, {}
TEXTKEYS = {"top", "big", "label", "value", "text", "name", "banner", "sub", "fmt", "lock_label"}

def _norm(w): return re.sub(r"[^a-z0-9$%]", "", w.lower())

def _split(e):
    """Split on spaces outside quotes and brackets (keeps quotes; lists like pins=[["HO CHI MINH",1,2]] stay whole)."""
    out, cur, q, depth = [], "", None, 0
    for ch in e.strip():
        if q:
            cur += ch
            if ch == q: q = None
        elif ch in "\"'" and (not cur or cur[-1] in "=[,(" or depth): q = ch; cur += ch
        elif ch in "[(": depth += 1; cur += ch
        elif ch in "])": depth -= 1; cur += ch
        elif ch.isspace() and depth == 0:
            if cur: out.append(cur); cur = ""
        else: cur += ch
    if cur: out.append(cur)
    return out

class Shot:
    def __init__(self, sid, line, words, start, dur):
        self.id, self.words, self.start, self.dur = sid, words, start, dur   # words: [(word, t_rel)]
        self.els = [self._parse(e) for e in line.split(" | ") if e.strip()]
        self.cues = []; self._autocues()

    def T(self, tok, default=0.0):
        """'@word', '@word#2+0.2', '@1.5' or number -> seconds from shot start."""
        if tok is None: return default
        if isinstance(tok, (int, float)): return float(tok)
        s = tok.lstrip("@"); off = 0.0
        m = re.match(r"^(.*?)([+-][\d.]+)$", s)
        if m and m.group(1): s, off = m.group(1), float(m.group(2))
        if re.fullmatch(r"\d+\.\d+", s): return float(s) + off      # '@1.5' = seconds; '@50' = the word "50"
        n = 1
        if "#" in s: s, n = s.split("#"); n = int(n)
        k = _norm(s)
        hits = [t for w, t in self.words if _norm(w).startswith(k)]
        if len(hits) < n: raise ValueError(f"{self.id}: word '{tok}' not in narration: {' '.join(w for w, _ in self.words)}")
        return hits[n-1] + off

    def _parse(self, e):
        toks = _split(e); typ = toks[0]; pos, kv, at, out, anims = [], {}, None, None, {}
        unq = lambda v: v[1:-1] if len(v) > 1 and v[0] == v[-1] and v[0] in "\"'" else None
        for tk in toks[1:]:
            if tk.startswith("out@"): out = tk[3:]
            elif tk.startswith("@"): at = tk
            elif "=" in tk and not tk.startswith('"'):
                k, v = tk.split("=", 1)
                m = re.match(r"^(-?[\d.]+)>(-?[\d.]+):(@?[^:]+):([\d.]+)$", v)
                if m: anims[k] = (float(m.group(1)), float(m.group(2)), m.group(3), float(m.group(4))); kv[k] = float(m.group(1)); continue
                if unq(v) is not None: kv[k] = unq(v); continue
                if k in TEXTKEYS: kv[k] = v; continue
                try: kv[k] = ast.literal_eval(v)
                except Exception: kv[k] = v
            else:
                if unq(tk) is not None: pos.append(unq(tk)); continue
                try: pos.append(ast.literal_eval(tk))
                except Exception: pos.append(tk)
        el = dict(typ=typ, pos=pos, kv=kv, at=at, out=out, anims=anims)
        el["t_at"] = self.T(at) if at else None
        el["t_out"] = self.T(out) if out else None
        el["anim_t"] = {k: (a, b, self.T(w), d) for k, (a, b, w, d) in anims.items()}
        return el

    def _autocues(self):
        C = self.cues
        for el in self.els:
            t, typ = el["t_at"], el["typ"]
            if typ == "bg" and el["pos"] and el["pos"][0] in AMBIENCE: C.append((0.0,) + AMBIENCE[el["pos"][0]])
            if typ == "sfx": C.append((el["t_at"] or 0.0, el["pos"][0], el["kv"].get("db", -6)))
            elif typ == "shake": C.append((t or 0.0, "thud", -2))
            elif typ in ("tx", "card"):
                t0 = t or 0.0; n = min(6, max(2, len(str(el["pos"][0]))//3))
                C += [(t0 + i*0.07, "typewriter_tick", -8) for i in range(n)]
            elif typ == "cnt":
                t0 = t or 0.0; d = el["kv"].get("dur", 1.2); C += [(t0 + i*d/6, "typewriter_tick", -10) for i in range(6)]; C.append((t0 + d, "pop", -4))
            elif t is not None and typ in ("a", "p", "kw", "st", "bars", "arrow", "dlg"):
                C.append((t, "whoosh_short" if typ == "arrow" else "pop", -6 if typ != "kw" else -3))
            if el["t_out"] is not None: C.append((el["t_out"], "whoosh_short", -10))

    # ---------------- drawing ----------------
    def val(self, el, k, t, default=None):
        if k in el["anim_t"]:
            a, b, t0, d = el["anim_t"][k]; return lerp(a, b, ease_io((t - t0)/max(d, 1e-3)))
        return el["kv"].get(k, default)

    def draw(self, ctx, t, dur):
        cam, shakes = ("push",), []
        for el in self.els:
            if el["typ"] == "bg": self._bg(ctx, t, el)
            elif el["typ"] == "cam": cam = el["pos"]
            elif el["typ"] == "shake": shakes.append((el["t_at"] or 0.0, el["kv"].get("amp", 0.6)))
        k = ease_io(t/dur); mode = cam[0] if cam else "push"; nums = [float(x) for x in cam[1:]]
        z0, z1 = {"push": (1.0, 1.08), "pull": (1.1, 1.0), "still": (1.0, 1.0), "pan": (1.05, 1.05)}.get(mode, (1, 1.08))
        cx, cy, cx2, cy2 = 640, 360, 640, 360
        if mode == "pan": cx, cx2 = 560, 720
        if len(nums) >= 2: z0, z1 = nums[0], nums[1]
        if len(nums) >= 4: cx, cy = nums[2], nums[3]; cx2, cy2 = cx, cy
        if len(nums) >= 6: cx2, cy2 = nums[4], nums[5]
        sh = sum(a*clamp(1 - (t - s)/0.4) for s, a in shakes if t >= s)
        ctx.save(); camera(ctx, lerp(z0, z1, k), lerp(cx, cx2, k), lerp(cy, cy2, k), shake=sh, t=t)
        for i, el in enumerate(self.els):
            if el["typ"] in ("bg", "cam", "shake", "sfx"): continue
            self._el(ctx, t, dur, el, i)
        ctx.restore()

    def _bg(self, ctx, t, el):
        name = el["pos"][0] if el["pos"] else "flat"; f = BG[name]
        kw = dict(el["kv"])
        if "t" in inspect.signature(f).parameters: kw["t"] = t
        f(ctx, **kw)

    def _el(self, ctx, t, dur, el, i):
        ta, to = el["t_at"], el["t_out"]
        if ta is not None and t < ta: return
        if to is not None and t >= to:
            if t < to + 0.6: smoke(ctx, *self._xy(el), clamp((t - to)/0.6), 70, i)
            return
        draw = lambda c: self._draw(c, t, dur, el, origin=True)
        typ = el["typ"]
        if ta is not None and typ in ("a", "kw", "st", "p", "dlg") and not el["kv"].get("nopop"):
            x, y = self._xy(el); popped(ctx, t, ta, x, y, draw, seed=i+3)
        else: self._draw(ctx, t, dur, el, origin=False)

    def _xy(self, el):
        p = el["pos"]
        if el["typ"] in ("kw", "st", "tx", "dlg"): return (p[1], p[2]) if len(p) > 2 else (640, 360)
        if el["typ"] in ("a", "p"):
            nums = [v for v in p if isinstance(v, (int, float))]
            return (nums[0], nums[1]) if len(nums) >= 2 else (640, 360)
        return (640, 360)

    def _draw(self, ctx, t, dur, el, origin):
        typ, p, kv = el["typ"], el["pos"], el["kv"]
        X = lambda x, y: (0, 0) if origin else (x, y)
        mv = kv.get("move")
        if mv and not origin:                       # move="dx,dy:@word:dur"
            d, w, du = mv.split(":"); dx, dy = map(float, d.split(","))
            k = ease_io((t - self.T(w))/float(du)); ctx.save(); ctx.translate(dx*k, dy*k)
        if typ == "a":
            name = p[0]; f = ASSETS[name]; nums = p[1:]
            args = dict((k, self.val(el, k, t)) for k in kv if k not in ("nopop", "move"))
            for k, v in list(args.items()):
                if isinstance(v, str) and v.startswith("#") and len(v) == 7: args[k] = hexc(v)
            sig = inspect.signature(f).parameters
            if "t" in sig and "t" not in args: args["t"] = t
            if len(nums) >= 2: x, y = X(nums[0], nums[1]); f(ctx, x, y, *nums[2:], **args)
            elif len(nums) == 1: f(ctx, nums[0], **args)           # e.g. sea(ctx, y), skyline(ctx, y)
            else: f(ctx, **args)
        elif typ == "p":
            who = p[0]; x, y = X(p[1], p[2]); s = p[3] if len(p) > 3 else 1.0
            pup = CAST[who](s)
            if kv.get("walk"): x += kv["walk"]*t
            pose_ = kv.get("pose", "down")
            if "pose2" in kv:
                n2, w2 = (kv["pose2"].split("@") + ["0"])[:2]
                arms = pose(pose_, n2, clamp((t - self.T("@" + w2))/0.35))
            else: arms = pose(pose_)
            for side, key in ((-1, "handL"), (1, "handR")):        # handR=x,y puts that hand exactly on a point
                if key in kv:
                    hx, hy = kv[key]; sc = pup.scale*(0.82 if pup.kid else 1.0); tw, th = (150, 190) if not pup.kid else (130, 150)
                    sx, sy = p[1] + side*(tw/2 - 10)*sc, p[2] + (-th + 34)*sc
                    off = (0, 0) if not origin else (p[1], p[2])
                    a = ((hx - sx)/sc, (hy - sy)/sc); arms = (a, arms[1]) if side < 0 else (arms[0], a)
            talking = False
            if "talk" in kv:
                a, b = kv["talk"].split("~"); talking = self.T(a) <= t <= self.T(b)
            extra = {}
            if "view" in kv: extra["view"] = kv["view"]
            if "hat" in kv and hasattr(pup, "who"): extra["hat"] = bool(kv["hat"])
            pup.draw(ctx, x, y, t, kv.get("e", "neutral"), talking, self.val(el, "f", t, 0.0), armL=arms[0], armR=arms[1],
                     legs=bool(kv.get("legs", 1)), walk=(t*1.6 if kv.get("walk") else 0.0), blink_seed=sum(map(ord, who)) % 7,
                     cross=("handL" in kv or "handR" in kv), **extra)
        elif typ == "kw":
            x, y = X(p[1], p[2]); text(ctx, str(p[0]), x, y, p[3] if len(p) > 3 else 72, (1, 1, 1), outline=INK, rot=kv.get("rot", 0))
        elif typ == "st":
            x, y = X(p[1], p[2]); ASSETS["sticky"](ctx, x, y, str(p[0]).replace("\\n", "\n"), rot=kv.get("rot", -0.05), size=p[3] if len(p) > 3 else 44,
                                                   **({"c": hexc(kv["c"])} if "c" in kv else {}))
        elif typ == "tx":
            ta = el["t_at"] or 0.0
            text(ctx, str(p[0]), p[1], p[2], p[3] if len(p) > 3 else 48, hexc(kv["c"]) if "c" in kv else (1, 1, 1),
                 anchor=kv.get("anchor", "c"), reveal=clamp((t - ta)/max(0.3, 0.05*len(str(p[0])))), outline=INK if kv.get("ol", 1) else None)
        elif typ == "card":
            ta = el["t_at"] or 0.0; bg_flat(ctx, (0.06, 0.06, 0.07))
            text(ctx, str(p[0]), 640, 330, kv.get("size", 96), (1, 1, 1), reveal=clamp((t - ta)/0.6))
            if "sub" in kv: text(ctx, kv["sub"], 640, 430, 44, hexc('#c9c9c9'), reveal=clamp((t - ta - 0.5)/0.6))
        elif typ == "cnt":
            a, b, x, y = p[0], p[1], p[2], p[3]; size = p[4] if len(p) > 4 else 84; ta = el["t_at"] or 0.0
            k = ease_out((t - ta)/kv.get("dur", 1.2)); v = lerp(a, b, k)
            fmt = kv.get("fmt", "{:,.0f}")
            s = fmt.format(v if "f}" in fmt or ".1" in fmt else int(round(v)))
            if t >= ta: text(ctx, s, x, y, size, (1, 1, 1), outline=INK)
        elif typ == "dlg":
            x, y = X(p[1], p[2]); tx_, ty_ = p[3], p[4]
            if origin: tx_, ty_ = tx_ - p[1], ty_ - p[2]
            ta = el["t_at"] or 0.0
            dialogue(ctx, str(p[0]).replace("\\n", "\n"), x, y, (tx_, ty_), size=kv.get("size", 40), reveal=clamp((t - ta)/0.5))
        elif typ == "arrow":
            x1, y1, x2, y2 = p[:4]; ta = el["t_at"] or 0.0; k = ease_out((t - ta)/kv.get("dur", 0.5))
            if t >= ta and k > 0:
                ex, ey = lerp(x1, x2, k), lerp(y1, y2, k); c = hexc(kv.get("c", "#e9b949")); lw = kv.get("lw", 12)
                line(ctx, [(x1, y1), (ex, ey)], INK, lw + 6); line(ctx, [(x1, y1), (ex, ey)], c, lw)
                a = math.atan2(ey - y1, ex - x1); h = lw*2.6
                pts = [(ex + math.cos(a)*h*0.6, ey + math.sin(a)*h*0.6), (ex + math.cos(a + 2.4)*h, ey + math.sin(a + 2.4)*h), (ex + math.cos(a - 2.4)*h, ey + math.sin(a - 2.4)*h)]
                poly(ctx, pts, c, INK, 3)
        elif typ == "bars":
            x, y, w, h = p[:4]; vals = kv["vals"]; labels = kv.get("labels", [""]*len(vals)); ta = el["t_at"] or 0.0
            mx = max(vals); bw = w/len(vals)*0.62; c = hexc(kv.get("c", "#e9b949")); fmt = kv.get("fmt", "{}")
            line(ctx, [(x, y), (x + w, y)], INK, 4)
            for j, v in enumerate(vals):
                k = ease_out((t - ta - j*0.25)/0.5)
                if k <= 0: continue
                bh = h*v/mx*k; bx = x + (j + 0.5)*w/len(vals) - bw/2
                hl = kv.get("hl"); cc = hexc('#c0392b') if hl == j else c
                box(ctx, bx, y - bh, bw, bh, cc, 4, INK, 3)
                if k > 0.9: text(ctx, fmt.format(v), bx + bw/2, y - bh - 26, 34, (1, 1, 1), outline=INK)
                text(ctx, str(labels[j]), bx + bw/2, y + 28, 30, (1, 1, 1), outline=INK)
        elif typ == "fn":
            CUSTOM[p[0]](ctx, t, dur, self.T, **{k: self.val(el, k, t) for k in kv})
        if mv and not origin: ctx.restore()

def build_shots(lines, segs, words, end_time):
    """lines: {sid: line}; segs: [{'id','start','i0','n'}]; words: full word list with t0. Returns [(sid, Shot)]."""
    out = []
    for j, s in enumerate(segs):
        nxt = segs[j+1]["start"] if j + 1 < len(segs) else end_time
        ws = [(w["w"], w["t0"] - s["start"]) for w in words[s["i0"]: s["i0"] + s["n"]]]
        out.append((s["id"], Shot(s["id"], lines[s["id"]], ws, s["start"], round(nxt - s["start"], 3))))
    return out
