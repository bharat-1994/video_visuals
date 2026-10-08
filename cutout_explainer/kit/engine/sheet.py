"""Contact sheet for self-review: python3 sheet.py <module> out.jpg  -> 2 frames per shot (t=0.4, t=0.8*dur), half size."""
import sys, importlib, cairo, subprocess, os, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.getcwd())
from lib import W, H
m = importlib.import_module(sys.argv[1]); out = sys.argv[2]; d = tempfile.mkdtemp(); i = 0
for dur, fn in m.SCENES:
    for t in (0.4, dur*0.8):
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s); c.set_source_rgb(1, 1, 1); c.paint(); fn(c, t, dur)
        s.write_to_png(f"{d}/{i:03d}.png"); i += 1
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/%03d.png", "-vf", "scale=640:-1,tile=2x%d" % ((i+1)//2), "-frames:v", "1", out])
print(out)
