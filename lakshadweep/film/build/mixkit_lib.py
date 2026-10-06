import re,json,subprocess,os
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX=json.load(open(os.path.join(ROOT,'build/mixkit_index.json')))
CACHE=os.path.join(ROOT,'build/mixkit_urls.json')
URLS=json.load(open(CACHE)) if os.path.exists(CACHE) else {}
def urls(vid):
    """returns dict(hd=..., preview=...) for a mixkit id"""
    if vid in URLS: return URLS[vid]
    if int(vid)<100000:
        d=dict(hd1080=f'https://assets.mixkit.co/videos/{vid}/{vid}-1080.mp4',hd=f'https://assets.mixkit.co/videos/{vid}/{vid}-720.mp4',preview=f'https://assets.mixkit.co/videos/{vid}/{vid}-360.mp4')
    else:
        slug=IDX[vid]
        h=subprocess.run(['curl','-sS','-m','30','-L','-A',UA,f'https://mixkit.co/free-stock-video/{slug}/'],capture_output=True,text=True).stdout
        c=re.search(r'"contentUrl":"([^"]+)"',h); e=re.search(r'"embedUrl":"([^"]+)"',h)
        d=dict(hd=c.group(1) if c else None,preview=e.group(1) if e else None)
    URLS[vid]=d; json.dump(URLS,open(CACHE,'w'),indent=0)
    return d
def fetch(vid,which='hd',dest=None):
    u=urls(vid)[which]
    dest=dest or os.path.join(ROOT,'assets/mixkit',('prev' if which=='preview' else 'hd'),f'{vid}.mp4')
    os.makedirs(os.path.dirname(dest),exist_ok=True)
    if os.path.exists(dest) and os.path.getsize(dest)>5000: return dest
    subprocess.run(['curl','-sS','-L','-m','600','-A',UA,'-o',dest,u])
    return dest
