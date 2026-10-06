"""Master timeline: where each act's voice sits on the final timeline."""
import json
SEG=json.load(open('/home/user/video_visuals/lakshadweep/film/build/segments.json'))
ACTS=['01_introduction','02_formation','03_first_people','04_rulers_traders','05_1947_flag','06_island_life','07_challenges','08_lessons']
PRE=5.0      # cold-open before first word
GAP=1.6      # breathing room between acts
OUTRO=10.0
START={};t=PRE
for a in ACTS:
    START[a]=t; t+=SEG[a]['duration']+GAP
TOTAL=t-GAP+OUTRO
FPS=24
def gt(act,local): return START[act]+local   # global time of act-local time
if __name__=='__main__':
    for a in ACTS: print(a,round(START[a],2),round(START[a]+SEG[a]['duration'],2))
    print('TOTAL',round(TOTAL,2))
