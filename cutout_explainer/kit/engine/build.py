"""Render + mix: python3 build.py <module> out.mp4
Module must define SCENES=[(dur,fn)...], CUES=[(shot_id,t,'sfx',gain_db)...], optional SUBS=[str|None per shot]."""
import sys, os, importlib, json, wave, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.getcwd())
from lib import *
m = importlib.import_module(sys.argv[1]); out = sys.argv[2]
AUD = os.environ.get("AUDIO_DIR", os.path.join(HERE, "..", "audio"))
S = m.SCENES; CUES = getattr(m, "CUES", []); SUBS = getattr(m, "SUBS", [None]*len(S))
def wrap(fn, sub):
    def f(ctx, t, dur):
        fn(ctx, t, dur)
        if sub:
            a = clamp(t/0.15)*clamp((dur-t)/0.1)
            ctx.save(); ctx.select_font_face(FONT); ctx.set_font_size(36); fs = min(36, 36*1180/ctx.text_extents(sub).width)
            ctx.set_font_size(fs); w = ctx.text_extents(sub).width
            ctx.set_source_rgba(0, 0, 0, .55*a); rrect(ctx, 640-w/2-18, 652, w+36, 50, 12); ctx.fill(); ctx.restore()
            if a > .5: text(ctx, sub, 640, 677, fs, (1, 1, 1))
    return f
render([(d, wrap(fn, SUBS[i] if i < len(SUBS) else None)) for i, (d, fn) in enumerate(S)], "_video.mp4")
SR = 44100; N = int((sum(d for d, _ in S)+0.5)*SR); starts = np.cumsum([0]+[d for d, _ in S])
def load(p):
    with wave.open(p) as w: return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768
mix = np.zeros(N, np.float32)
for sid, t, name, g in CUES:
    x = load(f"{AUD}/sfx/{name}.wav")*10**(g/20); o = int((starts[sid-1]+t)*SR); x = x[:max(0, N-o)]; mix[o:o+len(x)] += x
mb = load(f"{AUD}/music_bed.wav"); mix += np.tile(mb, 1+N//len(mb))[:N]*10**(-8/20)
mix[-int(1.5*SR):] *= np.linspace(1, 0, int(1.5*SR)); mix /= max(1.0, np.abs(mix).max()/0.89)
with wave.open("_mix.wav", "w") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "_video.mp4", "-i", "_mix.wav", "-c:v", "copy", "-c:a", "aac", "-shortest", out]); print(out)
