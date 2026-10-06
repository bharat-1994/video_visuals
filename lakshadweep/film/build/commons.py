import sys,json,time,urllib.parse,subprocess
UA="video-visuals-docu/1.0 (chandrabharat080@gmail.com)"
def get(url,tries=6):
    for t in range(tries):
        r=subprocess.run(['curl','-sS','-m','40','-A',UA,url],capture_output=True,text=True)
        if r.stdout.startswith('{'):
            return json.loads(r.stdout)
        time.sleep(4*(t+1))
    return None
def search(q,kind='video',limit=20):
    qq=f'{q} filetype:{kind}' if kind else q
    u=("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search&gsrnamespace=6"
       f"&gsrlimit={limit}&gsrsearch={urllib.parse.quote(qq)}&prop=imageinfo&iiprop=url|size|mime|extmetadata|mediatype&iiextmetadatafilter=LicenseShortName|Artist&iiurlwidth=1920")
    d=get(u)
    out=[]
    if not d or 'query' not in d: return out
    for p in sorted(d['query']['pages'].values(),key=lambda x:x.get('index',0)):
        ii=p.get('imageinfo',[{}])[0]
        md=ii.get('extmetadata',{})
        out.append(dict(title=p['title'],url=ii.get('url'),w=ii.get('width'),h=ii.get('height'),mime=ii.get('mime'),lic=md.get('LicenseShortName',{}).get('value'),size=ii.get('size')))
    return out
if __name__=='__main__':
    kind=sys.argv[2] if len(sys.argv)>2 else 'video'
    for r in search(sys.argv[1],kind): print(r['title'],'|',r['w'],'x',r['h'],'|',r['lic'],'|',(r['size'] or 0)//1024,'KB')
