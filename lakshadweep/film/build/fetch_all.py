"""Polite bulk downloader for Wikimedia Commons assets (honours Retry-After). Writes build/fetched.json."""
import json,glob,os,re,subprocess,time,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(ROOT,'assets/footage/raw'); STILL=os.path.join(ROOT,'assets/stills')
os.makedirs(RAW,exist_ok=True); os.makedirs(STILL,exist_ok=True)
UA="video-visuals-docu/1.0 (chandrabharat080@gmail.com)"
cat={}
for f in glob.glob(os.path.join(ROOT,'build/catalog*.json')):
    for k,v in json.load(open(f)).items():
        for r in v: cat[r['title']]=r
def find(sub,kind):
    sub=sub.lower()
    m=[t for t in cat if sub in t.lower()]
    if kind=='v': m=[t for t in m if (cat[t]['mime'] or '').startswith(('video','application/ogg'))]
    else: m=[t for t in m if (cat[t]['mime'] or '').startswith('image')]
    m.sort(key=lambda t:len(t))
    return m[0] if m else None
VIDEOS=json.load(open(os.path.join(ROOT,'build/want_videos.json')))
IMAGES=json.load(open(os.path.join(ROOT,'build/want_images.json')))
def safe(t): return re.sub(r'[^A-Za-z0-9._-]+','_',t.replace('File:',''))[:110]
def thumb_url(r,w):
    u=r['url'].split('?')[0]
    if (r['w'] or 0)<=w or not u.lower().endswith(('.jpg','.jpeg','.png')): return u
    # https://upload.wikimedia.org/wikipedia/commons/a/ab/Name.jpg -> .../thumb/a/ab/Name.jpg/2800px-Name.jpg
    m=re.match(r'(https://upload.wikimedia.org/wikipedia/commons)/(\w/\w\w)/(.+)$',u)
    name=m.group(3)
    ext='.png' if name.lower().endswith('.png') else ''
    return f"{m.group(1)}/thumb/{m.group(2)}/{name}/{w}px-{name}{'.jpg' if name.lower().endswith('.tif') else ''}"
def download(url,dest):
    for t in range(12):
        p=subprocess.run(['curl','-sS','-L','-m','1200','-A',UA,'-D','-','-o',dest+'.part','-w','\nCODE:%{http_code}',url],capture_output=True,text=True)
        m=re.search(r'CODE:(\d+)',p.stdout); code=m.group(1) if m else '0'
        if code=='200' and os.path.exists(dest+'.part') and os.path.getsize(dest+'.part')>1500:
            os.rename(dest+'.part',dest); return True
        ra=re.search(r'retry-after:\s*(\d+)',p.stdout,re.I)
        wait=int(ra.group(1))+15 if ra else 20*(t+1)
        print('  wait',code,wait,flush=True); time.sleep(min(wait,700))
    return False
done=json.load(open(os.path.join(ROOT,'build/fetched.json'))) if os.path.exists(os.path.join(ROOT,'build/fetched.json')) else {}
jobs=[('v',s) for s in VIDEOS]+[('i',s) for s in IMAGES]
for kind,sub in jobs:
    t=find(sub,kind)
    if not t: print('NOT FOUND',sub,flush=True); continue
    if t in done and os.path.exists(done[t]['path']): continue
    r=cat[t]
    if kind=='v':
        url=r['url'].split('?')[0]; dest=os.path.join(RAW,safe(t))
        if (r['size'] or 0)>200*1048576: print('SKIP big',t); continue
    else:
        url=thumb_url(r,2800); dest=os.path.join(STILL,safe(t))
        if not dest.lower().endswith(('.jpg','.jpeg','.png')): dest+='.jpg'
    ok=download(url,dest)
    print(('OK  ' if ok else 'FAIL'),t[:70],flush=True)
    if ok:
        done[t]=dict(path=dest,kind=kind,lic=r['lic'],url=r['url'].split('?')[0],w=r['w'],h=r['h'])
        json.dump(done,open(os.path.join(ROOT,'build/fetched.json'),'w'),indent=1)
    time.sleep(2.5)
print('ALL DONE')
