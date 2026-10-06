import json,sys,os,subprocess,time,glob
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(ROOT,'assets/footage/raw'); os.makedirs(RAW,exist_ok=True)
UA="video-visuals-docu/1.0 (chandrabharat080@gmail.com)"
def catalog():
    d={}
    for f in glob.glob(os.path.join(ROOT,'build/catalog*.json'))+glob.glob(os.path.join(ROOT,'build/cat_extra*.json')):
        c=json.load(open(f))
        for k,v in c.items():
            for r in v: d[r['title']]=r
    return d
def safe(t): return t.replace('File:','').replace('/','_').replace(' ','_')[:120]
def get(title,cat=None,maxmb=None):
    cat=cat or catalog()
    r=cat.get(title)
    if not r: print('NOT IN CATALOG',title); return None
    if maxmb and (r['size'] or 0)>maxmb*1048576: print('too big',title,(r['size'] or 0)//1048576,'MB'); return None
    dest=os.path.join(RAW,safe(title))
    if os.path.exists(dest) and os.path.getsize(dest)>1000: return dest
    url=r['url']
    for t in range(6):
        p=subprocess.run(['curl','-sS','-L','-m','900','-A',UA,'-o',dest+'.part','-w','%{http_code} %{size_download} %{speed_download}',url],capture_output=True,text=True)
        code=p.stdout.split()[0] if p.stdout else '0'
        if code=='200' and os.path.getsize(dest+'.part')>1000:
            os.rename(dest+'.part',dest); print('OK',safe(title),p.stdout); return dest
        print('retry',t,code,title[:50]); time.sleep(8*(t+1))
    return None
if __name__=='__main__':
    cat=catalog()
    for t in sys.argv[1:]: get(t,cat)
