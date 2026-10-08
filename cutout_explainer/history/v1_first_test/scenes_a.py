from lib import *
import math

KID=cast('elon_kid',1.0)
def lp(a,b,k): return (lerp(a[0],b[0],k),lerp(a[1],b[1],k))
def kw(ctx,s,t,start,x,y,size=70,rot=-3):
    k=pop(t,start,0.35)
    if k<=0: return
    ctx.save(); ctx.translate(x,y); ctx.scale(k,k); text(ctx,s,0,0,size,(1,1,1),rot=rot*math.pi/180,outline=INK); ctx.restore()

def book(ctx,w=150,h=190,c=hexc('#3b6ea8')):
    box(ctx,-w/2,-h/2,w,h,c,6,INK,4); box(ctx,-w/2+10,-h/2,8,h,hexc('#2a4f7d'),0)
    box(ctx,-w/2+30,-h/2+30,w-60,34,(1,1,1),3,INK,2)

# ---------------- shot 1 ----------------
def shot1(ctx,t,dur):
    bg_spotlight(ctx,floor_y=640)
    ctx.save(); camera(ctx,lerp(1.0,1.1,ease_io(t/dur)),640,420,t=t)
    k=cast('elon_kid',1.6)
    armL=lp((-25,125),(-45,70),ease_out(t/0.6)); armR=lp((25,125),(45,70),ease_out(t/0.6))
    info=k.draw(ctx,640,800,t,'neutral',talking=False,facing=0,armL=armL,armR=armR,legs=False,blink_seed=2)
    hl,hr=info['handL'],info['handR']
    ctx.save(); ctx.translate((hl[0]+hr[0])/2,(hl[1]+hr[1])/2-5); ctx.rotate(-0.04); book(ctx,170,210); ctx.restore()
    # hands over book edge
    circle(ctx,hl[0],hl[1],14,SKIN,INK,3); circle(ctx,hr[0],hr[1],14,SKIN,INK,3)
    # book stack bottom left
    for i,(w,c) in enumerate([(190,'#e8e4da'),(170,'#d9d3c2'),(180,'#f3f0e8')]):
        box(ctx,200-w/2+i*6,600-i*30,w,30,hexc(c),4,INK,3)
    ctx.restore()
    text(ctx,"1971 · Pretoria, South Africa",50,70,46,(1,1,1),anchor="l",reveal=clamp(t/1.2),outline=INK)

# ---------------- shot 2 ----------------
def shot2(ctx,t,dur):
    bg_sky_ground(ctx,horizon=540)
    # school wall
    box(ctx,0,170,W,370,hexc('#d9a679'),0,INK,3)
    for x in range(120,1280,300):
        box(ctx,x,230,160,120,hexc('#cfe9f5'),4,INK,4); line(ctx,[(x+80,230),(x+80,350)],INK,4)
    box(ctx,0,150,W,30,hexc('#a5683f'),0,INK,3)
    since=t-0.9
    shake=max(0,0.6-since)/0.6*9 if since>=0 else 0
    ctx.save(); camera(ctx,1.0,640,360,shake=shake,t=t)
    # fallen book
    ctx.save(); ctx.translate(640,628); ctx.rotate(0.12); ellipse(ctx,0,18,95,14,(0,0,0),a=.2)
    box(ctx,-85,-18,170,36,hexc('#3b6ea8'),5,INK,4); box(ctx,-78,-10,160,20,(1,1,1),3,INK,2); ctx.restore()
    # kid backs away
    kx=lerp(330,270,ease_out(t/1.0)); sw=math.sin(t*3)*0.0
    kid=cast('elon_kid',1.15)
    kid.draw(ctx,kx,470,t,'sad',facing=0.5,armL=(40,70),armR=(60,60),walk=t*1.2 if t<1 else 0,blink_seed=1)
    b=cast('bully',1.15)
    fist=lp((25,125),(-30,-120),ease_out((t-0.5)/0.4))
    bx=lerp(1000,930,ease_out(t/0.9))
    info=b.draw(ctx,bx,470,t,'angry',facing=-0.6,armL=(-150,10),armR=fist,walk=t*1.2 if t<0.9 else 0)
    if t>0.9:
        hr=info['handR']
        popped(ctx,t,0.9,hr[0]-10,hr[1]-70,lambda c:(text(c,"!",0,0,70,hexc('#e24b3b'),outline=INK)),seed=5)
    ctx.restore()

# ---------------- night room ----------------
def night_room(ctx,t,lamp=(250,520),window=(110,70)):
    bg_flat(ctx,hexc('#2b3555'))
    box(ctx,0,640,W,80,hexc('#1d2340'))
    wx,wy=window
    box(ctx,wx-8,wy-8,196,226,hexc('#6d7480'),6); box(ctx,wx,wy,180,210,hexc('#0f1530'))
    ctx.save(); ctx.set_source_rgb(*hexc('#f3e7a6')); ctx.arc(wx+90,wy+80,30,0,6.283); ctx.fill()
    ctx.set_source_rgb(*hexc('#0f1530')); ctx.arc(wx+104,wy+72,27,0,6.283); ctx.fill(); ctx.restore()
    for (sx,sy) in [(30,40),(150,30),(140,160),(40,150)]: circle(ctx,wx+sx,wy+sy,3,(1,1,1))
    line(ctx,[(wx+90,wy),(wx+90,wy+210)],hexc('#6d7480'),8); line(ctx,[(wx,wy+105),(wx+180,wy+105)],hexc('#6d7480'),8)
    circle(ctx,lamp[0],lamp[1],230,hexc('#ffd978'),a=.14); circle(ctx,lamp[0],lamp[1],130,hexc('#ffd978'),a=.14)

def lamp(ctx,x,y):
    box(ctx,x-30,y-8,60,10,hexc('#555b6e'),3,INK,3)
    line(ctx,[(x,y-8),(x+10,y-90),(x-10,y-150)],INK,7)
    poly(ctx,[(x-45,y-130),(x+25,y-170),(x+45,y-120)],hexc('#f2c14e'),INK,3)

def blastar(ctx,t):
    box(ctx,0,0,184,132,hexc('#0a1020'))
    for i in range(14):
        circle(ctx,(i*53)%184,((i*37+t*40)%132),1.5,(1,1,1),a=.6)
    sx=92+math.sin(t*2.2)*55
    poly(ctx,[(sx,92),(sx-11,114),(sx+11,114)],hexc('#7fe08a'),None)
    for j in range(4):
        by=(92-((t*90+j*30)%120)); 
        if by>0: circle(ctx,sx,by,3,hexc('#ff6a5a'))
    for i in range(3):
        ex=30+i*60+math.sin(t*2+i)*15; poly(ctx,[(ex,20),(ex-9,8),(ex+9,8)],hexc('#e0b94a'))

# ---------------- shot 3 ----------------
def shot3(ctx,t,dur):
    night_room(ctx,t,lamp=(250,500))
    z=lerp(1.0,1.1,ease_io(t/dur))
    ctx.save(); camera(ctx,z,640,380,t=t)
    k=cast('elon_kid',1.3)
    typ=math.sin(t*14)*10
    info=k.draw(ctx,470,690,t,'determined',facing=0.5,armL=(110,45),armR=(150,50+typ*0.5),legs=False,blink_seed=3)
    desk(ctx,640,540,820)
    lamp(ctx,250,538)
    popped(ctx,t,0.3,950,540,lambda c:crt(c,0,0,1.1,draw_screen=blastar_lines,t=t),seed=2)
    popped(ctx,t,0.8,690,512,lambda c:open_manual(c),seed=4)
    ctx.restore()
    kw(ctx,"SELF-TAUGHT",t,1.4,980,170)

def blastar_lines(ctx,t):
    box(ctx,0,0,184,132,hexc('#10261a'))
    n=int(t*6)
    for i in range(7):
        if i<n: line(ctx,[(10,14+i*17),(10+((i*53)%120)+30,14+i*17)],hexc('#6fe58a'),4)
    if int(t*3)%2==0: box(ctx,10+((n*53)%120),14+min(n,6)*17-6,10,12,hexc('#6fe58a'))

def open_manual(ctx):
    box(ctx,-150,-14,300,16,hexc('#3b6ea8'),3,INK,3)
    poly(ctx,[(-145,-14),(0,-30),(0,-10),(-145,4)],(1,1,1),INK,3)
    poly(ctx,[(145,-14),(0,-30),(0,-10),(145,4)],(0.96,0.96,0.92),INK,3)
    for i in range(3):
        line(ctx,[(-120,-12-i*3+0),(-20,-18-i*3)],(0.6,0.6,0.6),2); line(ctx,[(20,-18-i*3),(120,-12-i*3)],(0.6,0.6,0.6),2)

# ---------------- shot 4 ----------------
def shot4(ctx,t,dur):
    night_room(ctx,t,lamp=(330,430),window=(1000,60))
    z=lerp(1.12,1.0,ease_io(t/dur))
    ctx.save(); camera(ctx,z,640,380,t=t)
    # sign
    ctx.save(); ctx.translate(560,110); ctx.rotate(-0.03)
    box(ctx,-170,-50,340,100,hexc('#f4efe0'),6,INK,4); text(ctx,"BLASTAR",0,10,72,hexc('#c0392b'),outline=INK); ctx.restore()
    k=cast('elon_kid',1.4)
    wave=math.sin(t*8)*18
    a=ease_out(t/0.5)
    info=k.draw(ctx,330,660,t,'happy',facing=0.4,armL=lp((-25,125),(-40,-130+wave),a),armR=lp((25,125),(40,-130-wave),a),legs=False,blink_seed=4)
    desk(ctx,880,560,620)
    popped(ctx,t,0.4,900,560,lambda c:crt(c,0,0,1.3,draw_screen=blastar,t=t),seed=7)
    popped(ctx,t,1.2,690,556,lambda c:floppy(c),seed=9)
    ctx.restore()
    kw(ctx,"AGE 12",t,1.0,150,110,80,rot=4)

def floppy(ctx):
    ctx.save(); ctx.translate(0,-20); ctx.rotate(-0.1)
    box(ctx,-34,-34,68,68,hexc('#1b1b22'),5,INK,3); box(ctx,-22,-34,44,24,hexc('#c9c9d0'),2); box(ctx,-24,2,48,32,(1,1,1),3)
    line(ctx,[(-16,14),(16,14)],(0.5,0.5,0.5),3); line(ctx,[(-16,24),(8,24)],(0.5,0.5,0.5),3)
    ctx.restore()

# ---------------- shot 5 ----------------
def shot5(ctx,t,dur):
    bg_flat(ctx,hexc('#f2c14e'))
    box(ctx,0,640,W,80,hexc('#d9a73a'))
    ed_talk=0.2<=t<1.6; kid_talk=t>=1.6
    ctx.save(); camera(ctx,1.0,640,360,t=t)
    k=cast('elon_kid',1.3)
    a=ease_out((t-0.4)/0.5)
    ki=k.draw(ctx,300,640,t,'smug',talking=kid_talk,facing=0.6,armL=(-25,125),armR=lp((25,125),(150,40),a),legs=False,blink_seed=5)
    e=cast('editor',1.2)
    b=ease_out((t-0.1)/0.4)
    ei=e.draw(ctx,950,620,t,'shocked',talking=ed_talk,facing=-0.6,armL=lp((-25,125),(-40,-110),b),armR=lp((25,125),(-140,0),b),legs=False,blink_seed=6)
    desk(ctx,1050,560,420)
    ctx.save(); ctx.translate(1130,552); ctx.rotate(0.05);
    box(ctx,-95,-90,190,92,(1,1,1),4,INK,3); box(ctx,-95,-90,190,30,hexc('#2f6fb5'),0)
    text(ctx,"PC & Office Technology",0,-68,22,(1,1,1)); ctx.restore()
    hr=ei['handR']
    ctx.save(); ctx.translate(hr[0],hr[1]); popped(ctx,t,1.0,0,-30,lambda c:envelope(c),seed=8); ctx.restore()
    ctx.restore()
    if t>=0.2:
        dialogue(ctx,"Who wrote this?!",880,150,to=(ei['head'][0]-ei['R']*0.3,ei['head'][1]-ei['R']*1.3),size=46,reveal=clamp((t-0.2)/0.5)) if t<1.6 else None
    if t>=1.6:
        dialogue(ctx,"A twelve-year-old.\nCash, please.",300,140,to=(ki['head'][0]+ki['R']*0.45,ki['head'][1]-ki['R']*1.3),size=46,reveal=clamp((t-1.6)/0.7))

def envelope(ctx):
    ctx.rotate(-0.08)
    box(ctx,-70,-45,140,90,(1,1,1),5,INK,4)
    line(ctx,[(-70,-45),(0,10),(70,-45)],INK,3)
    text(ctx,"$500",0,32,44,hexc('#1f9d45'),outline=INK)

SCENES=[(3.4,shot1),(3.2,shot2),(3.5,shot3),(3.3,shot4),(3.4,shot5)]
