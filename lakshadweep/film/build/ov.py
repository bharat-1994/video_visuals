import json,subprocess,urllib.parse,sys
def search(q,n=20,exclude=('wikimedia','wikimedia_audio'),min_w=1000,license_type='all-cc',extra=''):
    u=f"https://api.openverse.org/v1/images/?q={urllib.parse.quote(q)}&page_size=20&mature=false&license_type={license_type}{extra}"
    r=subprocess.run(['curl','-sS','-m','30',u],capture_output=True,text=True).stdout
    try: d=json.loads(r)
    except: return []
    out=[]
    for x in d.get('results',[]):
        if x['provider'] in exclude: continue
        if (x.get('width') or 0)<min_w: continue
        out.append(dict(provider=x['provider'],lic=x['license'],ver=x.get('license_version'),w=x['width'],h=x['height'],title=x['title'][:60],creator=(x.get('creator') or '')[:30],url=x['url'],page=x.get('foreign_landing_url')))
    return out[:n]
if __name__=='__main__':
    for q in sys.argv[1:]:
        print('##',q)
        for r in search(q): print(f"  {r['provider']:12s} {r['lic']:8s} {r['w']}x{r['h']} | {r['title']} | {r['creator']} | {r['url'][-60:]}")
