"""Parallel chunked render. usage: python3 render_parts.py [workers] [chunk_seconds] [crf]
Writes build/parts/part_XXX.mp4 (resumable) then concat -> build/out/video_silent.mp4"""
import sys, os, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from multiprocessing import Pool

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTS = os.path.join(ROOT, 'build/parts'); os.makedirs(PARTS, exist_ok=True)
OUT = os.path.join(ROOT, 'build/out')
FPS = 24


def work(args):
    idx, f0, f1, crf = args
    out = os.path.join(PARTS, f'part_{idx:03d}.mp4')
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        return idx, 0.0, 'skip'
    import film, engine
    t = time.time()
    tl = film.build_timeline()
    engine.write_range(tl, f0 / FPS, f1 / FPS, out + '.tmp.mp4', crf=crf, preset='fast')
    os.rename(out + '.tmp.mp4', out)
    return idx, time.time() - t, 'ok'


def main():
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    chunk_s = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
    crf = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    import film_core as FC
    total_frames = int(round(FC.TOTAL * FPS))
    step = int(chunk_s * FPS)
    jobs = []
    for i, f0 in enumerate(range(0, total_frames, step)):
        jobs.append((i, f0, min(f0 + step, total_frames), crf))
    print('chunks', len(jobs), 'frames', total_frames, flush=True)
    t0 = time.time()
    with Pool(workers) as p:
        for idx, dt, st in p.imap_unordered(work, jobs):
            print(f'chunk {idx:03d} {st} {dt:.0f}s  (elapsed {time.time()-t0:.0f}s)', flush=True)
    lst = os.path.join(PARTS, 'list.txt')
    with open(lst, 'w') as f:
        for j in jobs:
            f.write(f"file 'part_{j[0]:03d}.mp4'\n")
    os.makedirs(OUT, exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', os.path.join(OUT, 'video_silent.mp4')], check=True)
    print('concat done', flush=True)


if __name__ == '__main__':
    main()
