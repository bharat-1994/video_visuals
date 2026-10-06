import re,json,os,glob,sys
sys.path.insert(0,'build'); sys.path.insert(0,'render')
from timeline import ACTS,START,SEG
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(ROOT,'out'),exist_ok=True)
def ts(t):
    h=int(t//3600); m=int(t%3600//60); s=t%60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s-int(s))*1000)):03d}"
te=[];en=[]
n=0
for a in ACTS:
    for s in SEG[a]['segs']:
        n+=1; t0=START[a]+s['start']; t1=START[a]+s['end']
        te.append(f"{n}\n{ts(t0)} --> {ts(t1)}\n{s['te']}\n"); en.append(f"{n}\n{ts(t0)} --> {ts(t1)}\n{s['en']}\n")
open(os.path.join(ROOT,'out','Lakshadweep_telugu.srt'),'w',encoding='utf8').write('\n'.join(te))
open(os.path.join(ROOT,'out','Lakshadweep_english.srt'),'w',encoding='utf8').write('\n'.join(en))
# credits: scan act modules
src=''.join(open(f,encoding='utf8').read() for f in glob.glob(os.path.join(ROOT,'render','act*.py')))
fl_used=sorted(set(int(x) for x in re.findall(r"'fl:(\d+)'",src)))
mk_used=sorted(set(re.findall(r"'mk:(\d+)'",src)),key=int)
tbl=json.load(open(os.path.join(ROOT,'assets/flickr/table.json')))
idx=json.load(open(os.path.join(ROOT,'build/mixkit_index.json')))
L=['# Credits & licences','',
 'Narration (Telugu voice-over): supplied by the author. Score, sound design, procedural animation and edit: generated in this repository (`lakshadweep/film/`).','',
 '## Satellite imagery','',
 '- NASA Global Imagery Browse Services (GIBS) / Worldview: Blue Marble shaded-relief bathymetry, MODIS (Terra/Aqua) and VIIRS (Suomi NPP) true-colour imagery, Harmonized Landsat-Sentinel-2 (HLS) true colour, VIIRS Black Marble. NASA imagery is in the public domain; "We acknowledge the use of imagery provided by services from NASA\'s Global Imagery Browse Services (GIBS), part of NASA\'s Earth Observing System Data and Information System (EOSDIS)."','',
 '## Stock footage (Mixkit Free Video licence — free for commercial use, no attribution required; credited here anyway)','']
for v in mk_used: L.append(f"- Mixkit #{v}: {idx.get(v,'?').rsplit('-',1)[0].replace('-',' ')} — https://mixkit.co/free-stock-video/{idx.get(v,'')}/")
L+=['','## Photographs (Flickr, Creative Commons — attribution)','']
for n_ in fl_used:
    t=tbl.get(str(n_))
    if t: L.append(f"- \"{t['title']}\" by {t['creator']} — CC {t['lic'].upper()} — {t.get('page') or ''}")
L+=['','Licences: CC BY = https://creativecommons.org/licenses/by/4.0/ · CC BY-SA = https://creativecommons.org/licenses/by-sa/4.0/','']
open(os.path.join(ROOT,'CREDITS.md'),'w',encoding='utf8').write('\n'.join(L))
print('srt',n,'fl',len(fl_used),'mk',len(mk_used))
