import json,re,glob,os
out={}
for tf in sorted(glob.glob('audio/0*_*.txt')):
    base=os.path.basename(tf)[:-4]
    j=json.load(open(f'audio/{base}.timestamps.json'))
    chars=j['graph_chars']; times=j['graph_times']
    full=''.join(chars)
    lines=[l.rstrip('\n') for l in open(tf,encoding='utf8')]
    segs=[];i=0
    while i<len(lines):
        m=re.match(r'(\d\d):(\d\d):(\d\d) --> (\d\d):(\d\d):(\d\d)',lines[i])
        if m:
            te=lines[i+1].strip(); en=lines[i+2].strip()
            segs.append((te,en)); i+=3
        else: i+=1
    pos=0;res=[]
    for te,en in segs:
        k=full.find(te,pos)
        if k<0:
            # try fuzzy: strip spaces/quotes
            k=full.find(te[:12],pos)
        if k<0: print('NOTFOUND',base,te[:30]); continue
        e=k+len(te)-1
        res.append(dict(te=te,en=en,start=times[k][0],end=times[min(e,len(times)-1)][1]))
        pos=k+len(te)
    out[base]=dict(duration=j['duration'],segs=res)
    print(base,j['duration'],len(segs),len(res), 'last end',res[-1]['end'] if res else None, 'chars',len(chars))
json.dump(out,open('build/segments.json','w'),ensure_ascii=False,indent=1)
