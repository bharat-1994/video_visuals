import sys,os,subprocess,urllib.parse,json,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(ROOT,'assets/footage/raw'); STILL=os.path.join(ROOT,'assets/stills')
UA="video-visuals-docu/1.0 (chandrabharat080@gmail.com)"
def safe(t): return t.replace('File:','').replace(' ','_').replace('/','_')
def fetch(title,dest=None,thumb_w=None):
    """download a Commons file (video or image). thumb_w for images -> scaled thumbnail."""
    name=title.replace('File:','')
    dest=dest or os.path.join(RAW,safe(title))
    if os.path.exists(dest) and os.path.getsize(dest)>1000: return dest
    url='https://commons.wikimedia.org/wiki/Special:FilePath/'+urllib.parse.quote(name)
    if thumb_w: url+=f'?width={thumb_w}'
    for t in range(5):
        r=subprocess.run(['curl','-sS','-L','-m','600','-A',UA,'-o',dest+'.part','-w','%{http_code}',url],capture_output=True,text=True)
        if r.stdout.strip()=='200' and os.path.getsize(dest+'.part')>1000:
            os.rename(dest+'.part',dest); return dest
        time.sleep(5*(t+1))
    print('FAILED',title,r.stdout,r.stderr[:100]); return None
if __name__=='__main__':
    for t in sys.argv[1:]:
        d=fetch(t); print(d, os.path.getsize(d)//1024 if d else None,'KB')
