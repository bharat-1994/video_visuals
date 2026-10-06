"""Asset resolution + clip conforming (1080p24 cache)."""
import os, json, hashlib, subprocess, glob, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUT = os.path.join(ROOT, 'assets/footage/cut'); os.makedirs(CUT, exist_ok=True)
_F = None


def fetched():
    global _F
    p = os.path.join(ROOT, 'build/fetched.json')
    if _F is None or (os.path.exists(p) and len(_F) != len(json.load(open(p)))):
        _F = json.load(open(p)) if os.path.exists(p) else {}
    return _F


def find(sub, kind=None):
    sub = sub.lower()
    best = None
    for t, r in fetched().items():
        if sub in t.lower() and (kind is None or r['kind'] == kind) and os.path.exists(r['path']):
            if best is None or len(t) < len(best[0]):
                best = (t, r)
    return best


def flickr(n):
    t = json.load(open(os.path.join(ROOT, 'assets/flickr/table.json')))
    return os.path.join(ROOT, t[str(n)]['file'])


def still(sub):
    if str(sub).startswith('fl:'):
        return flickr(int(str(sub)[3:]))
    f = find(sub, 'i')
    if not f:
        raise FileNotFoundError('still: ' + sub)
    return f[1]['path']


def mk(vid_id, quality='hd1080'):
    """Mixkit stock clip (free licence, no attribution needed). Downloads on first use."""
    import sys
    sys.path.insert(0, os.path.join(ROOT, 'build'))
    import mixkit_lib as M
    d = os.path.join(ROOT, 'assets/mixkit/hd'); os.makedirs(d, exist_ok=True)
    dest = os.path.join(d, f'{vid_id}.mp4')
    if os.path.exists(dest) and os.path.getsize(dest) > 20000:
        return dest
    u = M.urls(str(vid_id))
    import subprocess
    for key in ([quality, 'hd'] if quality in u else ['hd']):
        url = u.get(key)
        if not url:
            continue
        subprocess.run(['curl', '-sS', '-L', '-m', '900', '-A', M.UA, '-o', dest + '.part', url])
        if os.path.exists(dest + '.part') and os.path.getsize(dest + '.part') > 20000:
            os.rename(dest + '.part', dest)
            return dest
    raise FileNotFoundError('mixkit ' + str(vid_id))


def video(sub):
    if str(sub).startswith('mk:'):
        return mk(str(sub)[3:])
    f = find(sub, 'v')
    if not f:
        raise FileNotFoundError('video: ' + sub)
    return f[1]['path']


def has(sub):
    return find(sub) is not None


def probe_dur(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip()
    try:
        return float(r)
    except Exception:
        return 0.0


def conform(src, ss, dur, speed=1.0, vf_extra='', key=''):
    """returns path of a 1920x1080 24fps clip made from `src` starting at ss, lasting `dur` seconds of output."""
    h = hashlib.md5(f'{src}|{ss:.3f}|{dur:.3f}|{speed}|{vf_extra}|{key}'.encode()).hexdigest()[:14]
    out = os.path.join(CUT, f'{h}.mp4')
    if os.path.exists(out) and os.path.getsize(out) > 2000:
        return out
    sd = probe_dur(src)
    need = dur * speed
    loop = []
    if sd and ss + need > sd - 0.05:
        if need >= sd - 0.1:
            ss = 0.0; loop = ['-stream_loop', '-1']
        else:
            ss = max(0.0, sd - need - 0.05)
    vf = f'scale=1920:1080:force_original_aspect_ratio=increase:flags=lanczos,crop=1920:1080,setsar=1,fps=24'
    if speed != 1.0:
        vf = f'setpts=PTS/{speed},' + vf
    if vf_extra:
        vf += ',' + vf_extra
    cmd = ['ffmpeg', '-y', '-v', 'error'] + loop + ['-ss', f'{ss:.3f}', '-t', f'{need + 0.2:.3f}', '-i', src, '-an', '-vf', vf, '-t', f'{dur:.3f}',
           '-c:v', 'libx264', '-crf', '13', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-400:])
    return out
