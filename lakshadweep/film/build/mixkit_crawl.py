import re,subprocess,json,time,sys
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
cats=["sea","beach","water","nature","sunset","sky","cloud","rain","night","earth","space","fish","underwater","diving","fishing","boat","ship","sailing","island","ocean","tropical","palm","aerial","drone","storm","lightning","wave","airplane","airport","port","harbor","village","market","food","seafood","cooking","dance","culture","street","people","family","children","kids","women","woman","craft","rope","coconut","india","indian","lifestyle","travel","vacation","snorkel","coral","turtle","bird","seagull","pier","bridge","lighthouse","mosque","temple","city","night-city","traffic","hands","map","globe","technology","internet","cable","server","data","network","wind","clouds","sunrise","reflection","fog","mist","timelapse","time-lapse","slow-motion","macro","bubbles","drops","rainfall","flood","hurricane","tide","resort","hotel","swimming","jetty","dock","fisherman","net","kayak","canoe","sail","yacht","rock","cliff","sand","footprints","walking","child","old-man","elderly","portrait","smile"]
out={}
for c in cats:
    for pg in range(1,4):
        url=f"https://mixkit.co/free-stock-video/{c}/" + (f"?page={pg}" if pg>1 else "")
        r=subprocess.run(['curl','-sS','-m','30','-L','-A',UA,url],capture_output=True,text=True)
        h=r.stdout
        items=re.findall(r'href="/free-stock-video/([a-z0-9-]+-(\d+))/"',h)
        if not items: break
        n=0
        for slug,vid in items:
            if vid not in out: out[vid]=slug; n+=1
        print(c,pg,len(items),n,flush=True)
        if n==0: break
        time.sleep(0.4)
json.dump(out,open('build/mixkit_index.json','w'),indent=0)
print('TOTAL',len(out))
