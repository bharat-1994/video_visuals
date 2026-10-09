"""words.txt transcripts + part wavs -> narration.wav, words.json, segs.json, END.txt (same cut logic as prep_audio.py)"""
import sys, os, re, json, subprocess, wave, numpy as np
ep, words_txt = sys.argv[1], sys.argv[2]; parts = sys.argv[3:]
os.makedirs(ep, exist_ok=True)
def pcm(p):
    raw = subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar","44100","-f","s16le","-"],capture_output=True).stdout
    return np.frombuffer(raw, np.int16)
gap = np.zeros(int(0.3*44100), np.int16); chunks=[]; offs=[]; t=0.0
for i,p in enumerate(parts):
    a=pcm(p)
    if i: chunks.append(gap); t+=0.3
    offs.append(t); chunks.append(a); t+=len(a)/44100
a=np.concatenate(chunks); total=len(a)/44100
with wave.open(os.path.join(ep,"narration.wav"),"w") as w: w.setnchannels(1);w.setsampwidth(2);w.setframerate(44100);w.writeframes(a.tobytes())
open(os.path.join(ep,"END.txt"),"w").write(f"{total:.2f}\n")
sec=-1; words=[]; bounds=[]
FIX={"Audie":"Adi","Herzogenarach":"Herzogenaurach"}
for line in open(words_txt):
    if line.startswith("==="): sec+=1; continue
    m=re.match(r"\[([\d.]+) - ([\d.]+)\] (.+)",line.strip())
    if not m: continue
    t0,t1,w=float(m[1])+offs[sec],float(m[2])+offs[sec],m[3]
    if w in FIX: w=FIX[w]
    if w=="OnRunning," or w=="OnRunning":
        tail=w[9:]; mid=(t0+t1)/2
        words+= [dict(w="On",t0=round(t0,3),t1=round(mid,3),sec=sec),dict(w="Running"+tail,t0=round(mid,3),t1=round(t1,3),sec=sec)]; continue
    words.append(dict(w=w,t0=round(t0,3),t1=round(t1,3),sec=sec))
json.dump([{k:v for k,v in x.items()} for x in words],open(os.path.join(ep,"words.json"),"w"))
cuts=[0];n=0
for i,w in enumerate(words):
    n+=1; nxt=words[i+1]["t0"] if i+1<len(words) else total; pause=nxt-w["t1"]; start=words[cuts[-1]]["t0"]
    length=nxt-start; punct=w["w"][-1:] in ",.;:?!"
    newsec = i+1<len(words) and words[i+1]["sec"]!=w["sec"]
    if i+1<len(words) and (newsec or length>=6.0 or (length>=1.6 and n>=4 and (pause>=0.28 or punct)) or (n>=12 and length>=1.6)):
        cuts.append(i+1);n=0
S=[]
for j,c in enumerate(cuts):
    e=cuts[j+1] if j+1<len(cuts) else len(words)
    S.append(dict(id=f"S{j+1:02d}",start=round(words[c]["t0"] if j else 0.0,3),text=" ".join(x["w"] for x in words[c:e]),i0=c,n=e-c,sec=words[c]["sec"]))
json.dump(S,open(os.path.join(ep,"segs.json"),"w"),indent=0)
print(f"{total:.2f}s offsets={[round(o,2) for o in offs]} {len(words)} words {len(S)} shots")
