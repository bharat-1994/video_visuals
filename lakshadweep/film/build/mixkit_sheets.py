import json,re,subprocess,os,sys
import cv2,numpy as np
idx=json.load(open('build/mixkit_index_sel.json'))
kw=["sea","ocean","wave","beach","island","tropical","palm","coconut","boat","ship","fish","net","underwater","coral","diving","snorkel","turtle","aerial","drone","sunset","sunrise","cloud","storm","rain","lightning","sail","canoe","kayak","pier","jetty","dock","port","harbor","village","market","food","cooking","rope","craft","weaving","hands","woman","women","elderly","old","man","child","kid","children","family","dance","drum","airplane","plane","aircraft","airport","runway","cargo","container","bridge","map","globe","earth","space","satellite","timelapse","time-lapse","rock","sand","footprint","drop","bubble","reflection","sunlight","lagoon","reef","shell","crab","seagull","bird","lighthouse","mosque","temple","island","water","flying","over","hill","cliff","coast","shore","horizon","tide","fog","mist","wind","tree","trees","leaves","sun","sky","night","stars","milky","moon"]
sel=list(idx.items())
print(len(idx),len(sel))
os.makedirs('assets/mixkit/prev',exist_ok=True)
UA="Mozilla/5.0"
def prev(v):
    p=f'assets/mixkit/prev/{v}-360.mp4'
    if not os.path.exists(p) or os.path.getsize(p)<1000:
        subprocess.run(['curl','-sS','-m','60','-A',UA,'-o',p,f'https://assets.mixkit.co/videos/{v}/{v}-360.mp4'])
    return p
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(8) as ex: list(ex.map(lambda t: prev(t[0]),sel))
frames={}
for v,s in sel:
    p=prev(v)
    cap=cv2.VideoCapture(p)
    n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0); fps=cap.get(cv2.CAP_PROP_FPS) or 25
    fr=[]
    for q in (0.2,0.7):
        cap.set(cv2.CAP_PROP_POS_FRAMES,int(n*q)); ok,im=cap.read()
        if ok: fr.append(cv2.resize(im,(320,180)))
    if fr:
        frames[v]=(s,n/fps,np.hstack(fr)) if len(fr)==2 else (s,n/fps,np.hstack([fr[0],fr[0]]))
json.dump({v:[s,d] for v,(s,d,_) in frames.items()},open('build/mixkit_sel.json','w'))
keys=list(frames)
per=18
for i in range(0,len(keys),per):
    rows=[]
    for v in keys[i:i+per]:
        s,d,im=frames[v]
        im=im.copy()
        cv2.rectangle(im,(0,0),(640,24),(0,0,0),-1)
        cv2.putText(im,f'{v} {s[:48]} {d:.0f}s',(4,17),cv2.FONT_HERSHEY_SIMPLEX,0.46,(255,255,255),1,cv2.LINE_AA)
        rows.append(im)
    while len(rows)%2: rows.append(np.zeros_like(rows[0]))
    sheet=np.vstack([np.hstack(rows[j:j+2]) for j in range(0,len(rows),2)])
    cv2.imwrite(f'assets/mixkit/sheet_{i//per:03d}.jpg',sheet,[cv2.IMWRITE_JPEG_QUALITY,80])
print('sheets',len(keys)//per+1)
