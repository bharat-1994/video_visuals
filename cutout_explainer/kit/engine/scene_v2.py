"""Data-driven shots, engine v2 (REVISION_v2.md section 3). A copy of engine/scene.py plus:
  1. sound by category in _autocues (replaces "pop for everything"); per-element snd=NAME overrides, snd=none silences.
     Auto cues carry a kind prefix in their name until thin_cues strips it:
       "auto:" entrance sound (subject to all thinning rules)   "tick:" typewriter ticks (exempt)
       "exit:" out@ whoosh (exempt)                             "hit:" shake/whip impact (rule 2 only)
       "amb:" background ambience at t=0 (dedupe + consecutive -3 dB rule)
  2. thin_cues(CUES): global sound rules — 0.35 s auto spacing, same entrance sound never twice within 0.6 s,
     cap 3 entrance sounds per shot (keep earliest + loudest).
  3. remap_key_cue(name): the director's key-shot cues pop->thump_soft, typewriter_tick->click_soft.
  4. cam whip (snap in from 280 px left in 0.25 s + whip sound) and cam track X0 X1 (constant-speed, zoom 1.06).
  5. fx NAME [@word]: continuous motion layer FX[NAME](ctx, t_since_start, dur, T, **kv),
     drawn after the world and before text elements.
  6. p ... e2=EXPR@word: reaction beat — the expression switches at that word.
  7. dlg lines show only while the speaker's talk window or the line's own 1.6 s window runs.
  8. asset calls: "@word" strings inside list kwargs are resolved to seconds (whiteboard at=[...]),
     and t0 (the element's appear time) is passed to asset functions that declare a t0 parameter (chalk_text).
Registries (BG, ASSETS, CAST, CUSTOM, AMBIENCE, FX) are this module's own; film_v2.py seeds them from v1's scene.py.
"""
import shlex, ast, re, math, inspect
from lib import *

BG, ASSETS, CAST, CUSTOM, AMBIENCE, FX = {}, {}, {}, {}, {}, {}
TEXTKEYS = {"top", "big", "label", "value", "text", "name", "banner", "sub", "fmt", "lock_label"}

# ---------------- sound-by-category table (section 3.1) ----------------
ENTR = {}                                   # asset name -> (sound, dB)
for _n in ("paper", "land_deed", "ration_coupon", "fta_scroll", "whiteboard"): ENTR[_n] = ("paper_slide", -10)
ENTR["chalk_text"] = ("chalk", -10)
for _n in ("money_bag", "coin", "bill", "dong_note"): ENTR[_n] = ("coins", -12)
for _n in ("cage", "padlock", "container", "port_crane", "chip", "wafer", "tariff_wall", "caged_map"): ENTR[_n] = ("metal_tink", -12)
for _n in ("price_board", "podium", "open_doors", "shop_front", "empty_chairs", "rank_podium", "loudspeaker_pole"): ENTR[_n] = ("wood_knock", -10)
for _n in ("smartphone", "tablet", "smartwatch", "earbuds_case", "laptop", "tv_screen"): ENTR[_n] = ("glass_tink", -12)
for _n in ("dish", "rice_bowl", "rice_sack", "pork", "rice_heap"): ENTR[_n] = ("pop_soft", -14)
DEFAULT_ENT = ("thump_soft", -12)
_KW = [0]                                        # global keyword-sound alternation (soft_whoosh_in / card_flip)
CHART_FNS = {"pie", "priceline", "priceline_market", "chart_crash", "climb_line", "gdp_cake"}
TEXT_TYPES = ("kw", "st", "tx", "cnt", "dlg", "card")     # drawn after fx layers

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

    # ---------------- automatic cues (section 3.1) ----------------
    def _snd_for_asset(self, name):
        return ENTR.get(name, DEFAULT_ENT)

    def _autocues(self):
        C = self.cues
        for el in self.els:
            t, typ, kv = el["t_at"], el["typ"], el["kv"]
            snd = kv.get("snd")                                  # per-element override
            if typ == "bg" and el["pos"] and el["pos"][0] in AMBIENCE:
                C.append((0.0, "amb:%s" % AMBIENCE[el["pos"][0]][0], AMBIENCE[el["pos"][0]][1]))
            if typ == "sfx": C.append((el["t_at"] or 0.0, el["pos"][0], el["kv"].get("db", -6)))
            elif typ == "cam" and el["pos"] and el["pos"][0] == "whip": C.append((0.0, "hit:whip", -10))
            elif typ == "shake": C.append((t or 0.0, "hit:low_boom", -6))
            elif typ in ("tx", "card"):
                t0 = t or 0.0
                C += [(t0 + i*0.09, "tick:click_soft", -16) for i in range(min(2, max(1, len(str(el["pos"][0]))//4)))]
            elif typ == "cnt":
                t0 = t or 0.0; d = kv.get("dur", 1.2)
                C.append((t0, "auto:riser_short", -14)); C.append((t0 + d, "auto:ding_soft", -8))
            elif typ == "fn":
                if el["pos"] and el["pos"][0] in CHART_FNS:
                    try: ta = self.T(kv.get("at", "@0.0")) if isinstance(kv.get("at"), str) else (kv.get("at", 0.0) or 0.0)
                    except Exception: ta = 0.0
                    C.append((ta, "auto:riser_short", -14))
            elif t is not None and typ in ("a", "p", "kw", "st", "bars", "arrow", "dlg"):
                if snd == "none": pass
                elif snd: C.append((t, "auto:%s" % snd, -12))
                elif typ == "kw":
                    C.append((t, "auto:%s" % ("soft_whoosh_in" if _KW[0] % 2 == 0 else "card_flip"), -11 if _KW[0] % 2 == 0 else -12)); _KW[0] += 1
                elif typ == "st": C.append((t, "auto:paper_slide", -10))
                elif typ == "p": C.append((t, "auto:soft_whoosh_in", -14))
                elif typ == "arrow": C.append((t, "auto:swish_draw", -12))
                elif typ == "bars": C.append((t, "auto:riser_short", -14))
                elif typ == "a": C.append((t, "auto:%s" % self._snd_for_asset(el["pos"][0])[0], self._snd_for_asset(el["pos"][0])[1]))
                else: C.append((t, "auto:%s" % DEFAULT_ENT[0], DEFAULT_ENT[1]))
            if el["t_out"] is not None and snd != "none": C.append((el["t_out"], "exit:soft_whoosh_out", -14))

    # ---------------- drawing ----------------
    def val(self, el, k, t, default=None):
        if k in el["anim_t"]:
            a, b, t0, d = el["anim_t"][k]; return lerp(a, b, ease_io((t - t0)/max(d, 1e-3)))
        return el["kv"].get(k, default)

    def _cam(self, el, t, dur, k):
        """camera params (z, cx, cy, shake-extra) for the shot's cam element; v1 modes keep their behaviour."""
        cam = el["pos"] if el else ("push",)
        mode = cam[0] if cam else "push"; nums = [float(x) for x in cam[1:]]
        if mode == "whip":
            return 1.0, 640 - 280*(1 - ease_out(t/0.25)), 360.0
        if mode == "track":
            x0, x1 = (nums[0], nums[1]) if len(nums) >= 2 else (560, 720)
            return 1.06, lerp(x0, x1, t/dur), 360.0
        z0, z1 = {"push": (1.0, 1.08), "pull": (1.1, 1.0), "still": (1.0, 1.0), "pan": (1.05, 1.05)}.get(mode, (1, 1.08))
        cx, cy, cx2, cy2 = 640, 360, 640, 360
        if mode == "pan": cx, cx2 = 560, 720
        if len(nums) >= 2: z0, z1 = nums[0], nums[1]
        if len(nums) >= 4: cx, cy = nums[2], nums[3]; cx2, cy2 = cx, cy
        if len(nums) >= 6: cx2, cy2 = nums[4], nums[5]
        return lerp(z0, z1, k), lerp(cx, cx2, k), lerp(cy, cy2, k)

    def draw(self, ctx, t, dur):
        cam, shakes = None, []
        for el in self.els:
            if el["typ"] == "bg": self._bg(ctx, t, el)
            elif el["typ"] == "cam": cam = el
            elif el["typ"] == "shake": shakes.append((el["t_at"] or 0.0, el["kv"].get("amp", 0.6)))
        k = ease_io(t/dur); z, cx, cy = self._cam(cam, t, dur, k)
        sh = sum(a*clamp(1 - (t - s)/0.4) for s, a in shakes if t >= s)
        ctx.save(); camera(ctx, z, cx, cy, shake=sh, t=t)
        for i, el in enumerate(self.els):
            if el["typ"] in ("bg", "cam", "shake", "sfx") or el["typ"] == "fx" or el["typ"] in TEXT_TYPES: continue
            self._el(ctx, t, dur, el, i)
        for i, el in enumerate(self.els):                    # fx layers: after the world, before text
            if el["typ"] != "fx": continue
            ta = el["t_at"] or 0.0
            if t < ta: continue
            f = FX.get(el["pos"][0] if el["pos"] else "")
            if f: f(ctx, t - ta, dur, self.T, **{kk: self.val(el, kk, t) for kk in el["kv"]})
        for i, el in enumerate(self.els):
            if el["typ"] in TEXT_TYPES: self._el(ctx, t, dur, el, i)
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
        if el["typ"] == "dlg" and not self._dlg_live(t, el): return
        draw = lambda c: self._draw(c, t, dur, el, origin=True)
        typ = el["typ"]
        if ta is not None and typ in ("a", "kw", "st", "p", "dlg") and not el["kv"].get("nopop"):
            x, y = self._xy(el); popped(ctx, t, ta, x, y, draw, seed=i+3)
        else: self._draw(ctx, t, dur, el, origin=False)

    def _talk_windows(self):
        ws = []
        for el in self.els:
            if el["typ"] == "p" and "talk" in el["kv"]:
                a, b = el["kv"]["talk"].split("~")
                try: ws.append((self.T(a), self.T(b)))
                except Exception: pass
        return ws

    def _dlg_live(self, t, el):
        """a dlg line shows only while its own 1.6 s window (from its @word) or the speaker's talk window runs."""
        ta = el["t_at"] or 0.0
        if ta <= t <= ta + 1.6: return True
        for a, b in self._talk_windows():
            if a <= ta <= b and t <= max(b, ta + 1.6): return True
        return False

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
            args = dict((k, self.val(el, k, t)) for k in kv if k not in ("nopop", "move", "snd"))
            for k, v in list(args.items()):         # resolve "@word" inside (lists of) values for assets
                if isinstance(v, str) and v.startswith("#") and len(v) == 7: args[k] = hexc(v)
                elif isinstance(v, str) and v.startswith("@"):
                    try: args[k] = self.T(v)
                    except Exception: pass
                elif isinstance(v, list):
                    args[k] = [self.T(x) if isinstance(x, str) and x.startswith("@") else x for x in v]
            sig = inspect.signature(f).parameters
            if "t" in sig and "t" not in args: args["t"] = t
            if "t0" in sig and "t0" not in args: args["t0"] = el["t_at"] or 0.0
            if len(nums) >= 2: x, y = X(nums[0], nums[1]); f(ctx, x, y, *nums[2:], **args)
            elif len(nums) == 1: f(ctx, nums[0], **args)           # e.g. sea(ctx, y), skyline(ctx, y)
            else: f(ctx, **args)
        elif typ == "p":
            who = p[0]; x, y = X(p[1], p[2]); s = p[3] if len(p) > 3 else 1.0
            pup = CAST[who](s)
            if kv.get("walk"): x += kv["walk"]*t
            expr = kv.get("e", "neutral")
            if "e2" in kv:                                            # reaction beat: e2=EXPR@word
                e2, _, w2 = kv["e2"].partition("@")
                try:
                    if t >= self.T("@" + w2): expr = e2
                except Exception: pass
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
            pup.draw(ctx, x, y, t, expr, talking, self.val(el, "f", t, 0.0), armL=arms[0], armR=arms[1],
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
    _KW[0] = 0
    out = []
    for j, s in enumerate(segs):
        nxt = segs[j+1]["start"] if j + 1 < len(segs) else end_time
        ws = [(w["w"], w["t0"] - s["start"]) for w in words[s["i0"]: s["i0"] + s["n"]]]
        out.append((s["id"], Shot(s["id"], lines[s["id"]], ws, s["start"], round(nxt - s["start"], 3))))
    _LAST["shots"] = out
    return out

_LAST = {"shots": None}

# ---------------- global sound rules (section 3.2) ----------------
def remap_key_cue(name):
    """the director's key shots (S01, S12, S14, S15) keep their cue list; map the old names to the v2 set."""
    return {"pop": "thump_soft", "typewriter_tick": "click_soft"}.get(name, name)

def _kind(n):
    for k in ("auto:", "tick:", "exit:", "hit:", "amb:"):
        if n.startswith(k): return k[:-1], n[len(k):]
    return "exp", n

def thin_cues(CUES):
    """CUES: [(shot_id, t_local, name, gain_db)] with kind prefixes from _autocues. Applies the rules of
       section 3.2 + the ambience rules of 3.4 and returns plain (shot_id, t, name, gain) sorted by time."""
    items = []
    for sid, t, n, g in CUES:
        k, bare = _kind(n)
        items.append([sid, t, k, bare, g])
    # absolute time when the full shot list is known (indices line up); else within-shot only
    starts = None
    shots = _LAST["shots"]
    if shots:
        maxid = max((it[0] for it in items), default=0)
        if maxid == len(shots): starts = [s.start for _, s in shots]
    def absof(it):
        return (starts[it[0]-1] + it[1]) if starts else it[1]
    # rule: ambience dropped when an explicit cue of the same sound exists in the same shot near t=0
    exp_by_shot = {}
    for it in items:
        if it[2] == "exp": exp_by_shot.setdefault(it[0], []).append((it[1], it[3]))
    items = [it for it in items if not (it[2] == "amb" and any(n == it[3] and abs(t - it[1]) < 0.35 for t, n in exp_by_shot.get(it[0], ())))]
    # ambience: consecutive shots sharing a sound -> each next one -3 dB (cap -9)
    ambs = sorted([it for it in items if it[2] == "amb"], key=lambda it: it[0])
    prev = None; run = 0
    for it in ambs:
        if prev and it[0] == prev[0] + 1 and it[3] == prev[3]: run += 1
        else: run = 0
        it[4] -= min(3*run, 9); prev = it
    # rule 1: auto entrance cues within 0.35 s of another auto or of an explicit cue in the same shot -> drop (keep earliest)
    by_shot = {}
    for it in items: by_shot.setdefault(it[0], []).append(it)
    kept = []
    for sid, lst in by_shot.items():
        autos = sorted([it for it in lst if it[2] == "auto"], key=lambda it: it[1])
        expl = [it for it in lst if it[2] == "exp"]
        acc = []
        for it in autos:
            if any(abs(it[1] - a[1]) < 0.35 for a in acc): continue
            if any(abs(it[1] - e[1]) < 0.35 for e in expl): continue
            acc.append(it)
        # rule 3: cap 3 entrance sounds per shot — keep the earliest and the loudest
        if len(acc) > 3:
            rest = sorted(acc[1:], key=lambda it: -it[4])[:2]
            acc = [acc[0]] + rest
        kept += acc + [it for it in lst if it[2] != "auto"]
    # rule 2: never the same entrance sound twice within 0.6 s (auto + hit impacts; ticks/exits/ambience exempt)
    ent = sorted([it for it in kept if it[2] in ("auto", "hit")], key=absof)
    last_at = {}
    drop = set()
    for it in ent:
        a = absof(it)
        if it[3] in last_at and a - last_at[it[3]] < 0.6: drop.add(id(it))
        else: last_at[it[3]] = a
    out = [(it[0], max(0.0, it[1]), it[3], it[4]) for it in kept if id(it) not in drop]
    out.sort(key=lambda c: (c[0], c[1]))
    return out
