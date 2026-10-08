"""Blind side-by-side. python3 bakeoff/compare.py <out.jpg> <dirX> <dirY> [...]   (each dir holds A_crop.png B_crop.png C_crop.png from score.py)
Rows = cards, columns = models in RANDOM order labelled 1,2,..; prints the secret key to a .key file next to the image. Judge first, read the key after."""
import sys, random, cairo, os
out, dirs = sys.argv[1], sys.argv[2:]; order = list(range(len(dirs))); random.shuffle(order)
TW, TH = 760, 560; sf = cairo.ImageSurface(cairo.FORMAT_ARGB32, TW*len(dirs), TH*3 + 40); c = cairo.Context(sf); c.set_source_rgb(1, 1, 1); c.paint()
for col, di in enumerate(order):
    for row, card in enumerate("ABC"):
        p = os.path.join(dirs[di], f"{card}_crop.png")
        if not os.path.exists(p): continue
        im = cairo.ImageSurface.create_from_png(p); k = min((TW - 30)/im.get_width(), (TH - 30)/im.get_height(), 2.0)
        c.save(); c.translate(col*TW + TW/2, 40 + row*TH + TH/2); c.scale(k, k); c.set_source_surface(im, -im.get_width()/2, -im.get_height()/2); c.paint(); c.restore()
    c.set_source_rgb(0, 0, 0); c.set_font_size(30); c.move_to(col*TW + 10, 30); c.show_text(f"MODEL {col+1}")
sf.write_to_png(out if out.endswith(".png") else out + ".png")
open(out + ".key", "w").write("\n".join(f"MODEL {i+1} = {dirs[di]}" for i, di in enumerate(order)) + "\n"); print("wrote", out, "(key in", out + ".key)")
