"""python3 preview.py <acts e.g. 1,2> [per_entry=2] -> contact sheets in scratch"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cv2, numpy as np
import film, film_core as FC
from engine import FPS
acts = tuple(int(x) for x in sys.argv[1].split(','))
per = int(sys.argv[2]) if len(sys.argv) > 2 else 2
SCR = '/tmp/claude-0/-home-user-video-visuals/e9e240b6-d78e-5c48-b043-e4e820848b97/scratchpad'
tl = film.build_timeline(acts)
lo = FC.GT(acts[0], 0.0) - 5.0 if acts[0] == 1 else FC.GT(acts[0], 0.0) - 0.5
hi = FC.GT(acts[-1], 0.0) + 80
tiles = []
for i, e in enumerate(tl.entries):
    if e.start < lo or e.start > hi:
        continue
    end = e.start + e.dur
    nx = tl.entries[i + 1].tdur if i + 1 < len(tl.entries) else 0.0
    lo_t = e.start + e.tdur + 0.15
    hi_t = max(lo_t, end - nx - 0.15)
    for k in range(per):
        T = lo_t + (hi_t - lo_t) * ((k + 0.5) / per)
        t0 = time.time()
        fr = tl.frame_at(T, int(T * FPS))
        im = cv2.resize(cv2.cvtColor(fr, cv2.COLOR_RGB2BGR), (480, 270))
        cv2.rectangle(im, (0, 0), (480, 16), (0, 0, 0), -1)
        cv2.putText(im, f'{e.name[:20]} T={T:.1f} {time.time()-t0:.1f}s', (3, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        tiles.append(im)
cols = 4
while len(tiles) % cols:
    tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[j:j + cols]) for j in range(0, len(tiles), cols)]
n = 0
for j in range(0, len(rows), 5):
    cv2.imwrite(f'{SCR}/prev_{"_".join(map(str,acts))}_{n}.jpg', np.vstack(rows[j:j + 5]), [cv2.IMWRITE_JPEG_QUALITY, 85]); n += 1
print('sheets', n, 'tiles', len(tiles))
