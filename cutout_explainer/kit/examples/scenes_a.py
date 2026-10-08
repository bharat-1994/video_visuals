import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from lib import *
from assets_a import *
import math

def lp(a,b,k): return (lerp(a[0],b[0],k),lerp(a[1],b[1],k))

def arm_to(p,x,y,side,target,view_scale=None):
    """arm offset so the hand of `p` (waist at x,y) reaches target. side -1 = armL, +1 = armR."""
    s=p.scale*(0.82 if p.kid else 1.0)
    tw,th=(150,190) if not p.kid else (130,150)
    sh=(x+side*(tw/2-10)*s, y+(-th+34)*s)
    return ((target[0]-sh[0])/s,(target[1]-sh[1])/s)

def glow_face(ctx,info,p,dx=0.55,a=0.22,c=(0.7,0.85,1.0)):
    hx,hy=info['head']; R=info['R']
    ctx.save(); head_path(ctx,hx-0,hy,R/ (1.0),p.jaw) if False else None
    ctx.restore()

# =============================================================== SHOT 1
def shot1(ctx,t,dur):
    # sky
    box(ctx,0,0,W,H,hexc('#7cc3ec'))
    box(ctx,0,0,W,200,hexc('#5fb3e6'),0); box(ctx,0,200,W,140,hexc('#9bd4f2'))
    for (cx,cy,sc) in [(180+t*4,90,1.0),(820+t*3,60,1.3),(1120+t*3,150,.8)]:
        for dx,r in [(-45,30),(0,44),(45,32),(15,26)]: circle(ctx,cx+dx*sc,cy+(r%7)*.0,r*sc,(1,1,1))
    z=lerp(1.0,1.38,ease_io(t/dur)); cx=lerp(640,860,ease_io(t/dur)); cy=lerp(360,470,ease_io(t/dur))
    ctx.save(); camera(ctx,z,cx,cy,t=t)
    # hill
    hill=hexc('#6fb25c'); ctx.move_to(-200,560); ctx.line_to(-200,420); ctx.curve_to(80,360,200,345,300,340); ctx.line_to(760,340)
    ctx.curve_to(900,345,1100,380,1500,430); ctx.line_to(1500,560); ctx.close_path()
    ctx.set_source_rgb(*hill); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
    # distant trees on hill
    for i,xx in enumerate([40,110,170,880,950,1010,1070,1150]):
        yy=345+abs(xx-520)*0.12
        circle(ctx,xx,yy+8,22,hexc('#3f8a45'),INK,2); circle(ctx,xx-6,yy,16,hexc('#58a352'))
    # terraces
    terraces(ctx,130,335,780,200)
    union_buildings(ctx,520,340,0.86)
    # foreground lawn
    box(ctx,-300,520,W+600,260,hexc('#7cc06a'))
    line(ctx,[(-300,520),(W+300,520)],INK,2.5,.5)
    for i in range(12):
        xx=-100+i*130+(i*47)%60; yy=560+(i*53)%130
        line(ctx,[(xx,yy),(xx+8,yy-12)],hexc('#4d9a4d'),3); line(ctx,[(xx+8,yy),(xx+18,yy-10)],hexc('#4d9a4d'),3)
    jacaranda(ctx,120,640,0.85,seed=4)
    jacaranda(ctx,1010,640,1.05,seed=7)
    # kid sitting under tree
    k=cast('elon_kid',0.95)
    kx,ky=880,650
    ellipse(ctx,kx,ky+8,130,26,hexc('#68ac56'))
    ellipse(ctx,kx,ky+16,110,16,(0,0,0),a=.12)
    # book held in front of chest (we see outer cover; faces him)
    s=0.82*0.95
    bk=(kx+58,ky-78)
    hl=arm_to(k,kx,ky,-1,(bk[0]-18,bk[1]+34)); hr=arm_to(k,kx,ky,1,(bk[0]+22,bk[1]+38))
    flip=0
    info=k.draw(ctx,kx,ky,t,'neutral',False,0.7,armL=hl,armR=hr,legs=False,blink_seed=3)
    ctx.save(); ctx.translate(*bk); ctx.rotate(-0.06); ctx.scale(0.5,0.5); open_book_back(ctx,170,210); ctx.restore()
    for hnd in (info['handL'],info['handR']): circle(ctx,hnd[0],hnd[1]+2,9,SKIN,INK,2.5)
    # grass mound over legs/lower body, crossed legs hint
    ellipse(ctx,kx-6,ky+4,92,24,hexc('#7cc06a')); 
    for xx in range(-80,90,22): line(ctx,[(kx+xx,ky+4),(kx+xx+5,ky-10)],hexc('#4d9a4d'),3)
    petals(ctx,t,780,1100,300,640,16,3)
    ctx.restore()
    # caption
    text(ctx,"1971 · Pretoria, South Africa",50,62,48,(1,1,1),anchor="l",reveal=clamp((t-0.3)/1.5),outline=INK)

# =============================================================== SHOT 2
def brick_wall(ctx,x,y,w,h):
    box(ctx,x,y,w,h,hexc('#c9714f'))
    rnd=random.Random(5)
    r=0
    for yy in range(int(y),int(y+h),22):
        off=(r%2)*30
        for xx in range(int(x)-60+off,int(x+w),60):
            c=rnd.choice([hexc('#c9714f'),hexc('#bf6644'),hexc('#d27c57')])
            box(ctx,xx+2,yy+2,56,18,c,2)
        r+=1
def shot2(ctx,t,dur):
    box(ctx,0,0,W,H,hexc('#9fd8f0'))
    bg_flat(ctx,hexc('#9fd8f0'))
    sh=0.0
    if 0.8<t<1.1: sh=9*(1-(t-0.8)/0.3)
    z=lerp(1.0,1.07,ease_io(t/dur))
    ctx.save(); camera(ctx,z,640,380,shake=sh,t=t)
    brick_wall(ctx,-100,110,W+200,430)
    box(ctx,-100,100,W+200,20,hexc('#8a8f99'),0,INK,3)
    for x in (140,520,900,1240):
        box(ctx,x-5,160,150,130,hexc('#cfe9f5'),4,INK,4); line(ctx,[(x+70,160),(x+70,290)],INK,3); line(ctx,[(x-5,225),(x+145,225)],INK,3)
        box(ctx,x-12,290,164,12,hexc('#e6dcc9'),0,INK,3)
    # door
    box(ctx,1120,300,110,240,hexc('#3f5f86'),4,INK,4)
    # ground
    box(ctx,-100,540,W+200,300,hexc('#a9a39a')); line(ctx,[(-100,540),(W+100,540)],INK,3)
    for i in range(8): line(ctx,[(-100+i*190,620),(40+i*190,620)],(1,1,1),5,.5)
    # actors
    bul=cast('bully',1.25); kid=cast('elon_kid',1.15)
    e=ease_out((t-0.8)/0.5) if t>0.8 else 0
    lunge=ease_out((t-0.7)/0.15)*0 
    bx=lerp(380,470,ease_out((t-0.6)/0.25)) if t>0.6 else 380
    bx=lerp(bx,420,ease_io((t-1.2)/0.8))
    kx=lerp(720,880,ease_out((t-0.8)/0.6)) if t>0.8 else 720
    ky=480
    # book trajectory
    if t<0.8:
        bkpos=(kx-62,ky-95); brot=-0.1
    else:
        u=(t-0.8)/0.85
        bkpos=(lerp(kx-62,1010,min(u,1)),lerp(ky-95,590,min(u,1))-math.sin(clamp(u)*math.pi)*190); brot=-0.1+clamp(u)*7.0
        if u>=1: brot=-0.1+7.0-0.0; 
    # bully arm
    if t<0.7: aR=(25,125)
    elif t<0.85: aR=lp((25,125),(170,5),(t-0.7)/0.15)
    else: aR=lp((170,5),(60,70),ease_io((t-1.0)/0.6)) if t>1.0 else (170,5)
    binfo=bul.draw(ctx,bx,ky+8,t,'angry',False,0.55,armL=(-30,110),armR=aR,legs=True,blink_seed=1)
    if t<0.8:
        hl=arm_to(kid,kx,ky,-1,(bkpos[0]-22,bkpos[1]+45)); hr=arm_to(kid,kx,ky,1,(bkpos[0]+25,bkpos[1]+50))
    else:
        w=ease_out((t-0.8)/0.3); hl=lp(arm_to(kid,kx,ky,-1,(bkpos[0]-22,bkpos[1]+45)) if False else (-60,85),(-60,-110),w); hr=lp((60,85),(55,-120),w)
    kinfo=kid.draw(ctx,kx,ky,t,'worried' if t<0.8 else 'sad',False,-0.5,armL=hl,armR=hr,legs=True,blink_seed=5)
    # book
    def bk(c):
        box(c,-34,-45,68,90,hexc('#3b6ea8'),4,INK,3); box(c,-34,-45,9,90,hexc('#2a4f7d'),2); box(c,-18,-26,40,22,(1,1,1),2,INK,1.5)
    ctx.save(); ctx.translate(*bkpos); ctx.rotate(brot); bk(ctx); ctx.restore()
    if t<0.8:
        for hnd in (kinfo['handL'],kinfo['handR']): circle(ctx,hnd[0],hnd[1],8,SKIN,INK,2.5)
    if 0.8<t<1.2:
        smoke(ctx,kx-30,ky-120,(t-0.8)/0.4,50,3)
    # impact star on shove
    if 0.78<t<1.0:
        k_=(t-0.78)/0.22; x0=(binfo['handR'][0])+10; y0=binfo['handR'][1]
        for i in range(8):
            a=i*math.pi/4; line(ctx,[(x0+math.cos(a)*18*k_+18,y0+math.sin(a)*18*k_),(x0+math.cos(a)*40*k_+18,y0+math.sin(a)*40*k_)],hexc('#ffd23f'),6)
    if t>1.65 and t<2.0: smoke(ctx,1010,598,(t-1.65)/0.35,40,9)
    ctx.restore()

# =============================================================== SHOT 3
def shot3(ctx,t,dur):
    NAVY=hexc('#1d2850')
    bg_room(ctx,wall=NAVY,floor=hexc('#3a2b3d'),floor_y=612)
    # wallpaper stripes
    for x in range(0,W,80): box(ctx,x,0,36,612,hexc('#222f5c'))
    z=lerp(1.0,1.1,ease_io(t/dur)); cx=lerp(640,700,ease_io(t/dur)); cy=lerp(360,350,ease_io(t/dur))
    ctx.save(); camera(ctx,z,cx,cy,t=t)
    # window w/ moon
    box(ctx,76,96,200,200,hexc('#6d7480'),8,INK,3); box(ctx,88,108,176,176,hexc('#0f1838'))
    circle(ctx,200,170,28,hexc('#f6efc4')); circle(ctx,212,164,24,hexc('#0f1838'))
    for (sx,sy) in [(120,150),(160,240),(235,250),(110,210),(230,130)]:
        circle(ctx,sx,sy,2.5,(1,1,1))
    line(ctx,[(176,108),(176,284)],hexc('#6d7480'),8); line(ctx,[(88,196),(264,196)],hexc('#6d7480'),8)
    # shelf with books
    box(ctx,980,170,250,12,hexc('#7a5232'),2,INK,3)
    for i,(bw,c) in enumerate([(22,'#d9534f'),(18,'#e9c46a'),(26,'#2a9d8f'),(16,'#e76f51'),(24,'#6a8fd8')]):
        box(ctx,1000+sum([22,18,26,16,24][:i])+i*2,170-70-(i%2)*8,bw,70+(i%2)*8,hexc(c),2,INK,2)
    # wall: rocket poster
    box(ctx,430,70,120,170,hexc('#f3ead0'),3,INK,3)
    poly(ctx,[(490,100),(510,150),(510,190),(470,190),(470,150)],hexc('#d9d9de'),INK,2.2)
    poly(ctx,[(470,170),(452,198),(470,190)],hexc('#d9534f'),INK,2); poly(ctx,[(510,170),(528,198),(510,190)],hexc('#d9534f'),INK,2)
    circle(ctx,490,148,8,hexc('#7ec8f2'),INK,2)
    poly(ctx,[(478,190),(502,190),(490,218)],hexc('#ffb02e'),INK,2)
    # floor rug
    ellipse(ctx,560,640,420,34,hexc('#5b3b63'),a=.9)
    # kid's legs (side view), behind desk edge
    kid=cast('elon_kid',1.35)
    s=0.82*1.35
    kx,ky=380,462
    PANT=hexc('#3c4a7a')
    # chair
    box(ctx,kx-125,ky-190,28,220,hexc('#6b4a8a'),8,INK,3)   # chair back
    box(ctx,kx-120,ky+2,200,22,hexc('#7e5aa2'),8,INK,3)    # seat
    line(ctx,[(kx-20,ky+24),(kx-20,603)],INK,10); line(ctx,[(kx-80,603),(kx+40,603)],INK,8)
    # thigh + shin
    hip=(kx-10,ky-4); knee=(kx+112,ky+2); foot=(kx+122,ky+142)
    line(ctx,[hip,knee],INK,52,1); line(ctx,[hip,knee],PANT,46); line(ctx,[knee,foot],INK,40); line(ctx,[knee,foot],PANT,34)
    box(ctx,foot[0]-14,foot[1]-8,56,22,hexc('#f3f3f3'),10,INK,3)
    # DESK (side-on slab) : top surface y=470..540
    DK=hexc('#a8703f')
    box(ctx,470,470,780,12,hexc('#c28a52'),0,INK,3)       # back edge highlight
    box(ctx,470,482,780,50,hexc('#b87d48'),0,INK,3)        # top surface
    box(ctx,470,532,780,26,DK,0,INK,3)                     # front edge
    box(ctx,1150,558,30,54,hexc('#80502a'),0,INK,3)        # leg
    box(ctx,500,558,30,54,hexc('#80502a'),0,INK,3)
    # typing: hands bob
    kb_x,kb_y=520,508
    typ=1 if 0.15<t<4.3 else 0
    bobL=math.sin(t*18)*5*typ; bobR=math.sin(t*18+2)*5*typ
    key_front=(kb_x+46,kb_y-44)
    hl=arm_to(kid,kx,ky,-1,(kb_x+88,kb_y-60+bobL)); hr=arm_to(kid,kx,ky,1,(kb_x+58,kb_y-48+bobR))
    # TV on desk: draw first (further right), then keyboard
    # glow cone on desk
    tv_x,tv_y=860,488
    tv_angled(ctx,tv_x,tv_y,t,1.0,vic_screen)
    # cable
    cab=(kb_x+250,kb_y-52)
    hose(ctx,(kb_x+232,kb_y-30),(tv_x+120,tv_y-10),0.18,6,hexc('#2a2a30'))
    vic20_side(ctx,kb_x,kb_y,1.0)
    # manual (open, spiral) lying on the desk in front
    ctx.save(); ctx.translate(722,528); ctx.scale(0.9,0.52); ctx.rotate(-0.04)
    spiral_manual(ctx,130,120); ctx.restore()
    # head glow + body
    info=kid.draw(ctx,kx,ky,t,'neutral',False,0.85,armL=hl,armR=hr,legs=False,blink_seed=4)
    for h_ in (info['handL'],info['handR']): circle(ctx,h_[0],h_[1],8,SKIN,INK,2.5)
    hx,hy=info['head']; R=info['R']
    ctx.save(); head_path(ctx,hx,hy,R/ (s) if False else R,0) if False else None; ctx.restore()
    # screen glow on face (right side)
    ctx.save()
    ctx.translate(hx,hy); ctx.scale(s,s); head_path(ctx,0,0,92,kid.jaw); ctx.clip(); ctx.scale(1/s,1/s)
    g=cairo.RadialGradient(R*1.05,R*0.15,2,R*1.05,R*0.15,R*1.0); g.add_color_stop_rgba(0,0.6,0.95,1,0.6); g.add_color_stop_rgba(1,0.7,0.85,1,0)
    ctx.set_source(g); ctx.paint(); ctx.restore()
    # soft light on shoulder/arm
    # sticky note sequence
    sx,sy=720,215
    popped(ctx,t,0.3,sx,sy,lambda c:(sticky(c,190,150),text(c,"6 months",0,8,44,hexc('#2b2b33'),rot=-0.05)),puff=True,seed=2)
    if t>1.3:
        k=ease_out((t-1.3)/0.35)
        line(ctx,[(sx-84,sy-14),(lerp(sx-84,sx+84,k),lerp(sy-14,sy+30,k))],hexc('#d12f2f'),8)
        k2=ease_out((t-1.55)/0.3); 
        if k2>0: line(ctx,[(sx-84,sy+28),(lerp(sx-84,sx+84,k2),lerp(sy+28,sy-18,k2))],hexc('#d12f2f'),8)
    def n3(c):
        sticky(c,170,130,hexc('#9be58a')); text(c,"3 days",0,8,52,hexc('#1b4d2a'),rot=-0.04)
    ctx.save(); ctx.translate(0,0)
    popped(ctx,t,2.2,sx+215,sy+30,n3,seed=6)
    ctx.restore()
    ctx.restore()

# =============================================================== SHOT 4
def tv_frame(ctx,x,y,w,h):
    WD=hexc('#a8703f'); WD_S=hexc('#80502a')
    box(ctx,x-34,y-34,w+68,h+68,WD,26,INK,4)
    rnd=random.Random(2)
    for i in range(10):
        yy=y-26+i*(h+52)/10
        line(ctx,[(x-28,yy),(x-8,yy+rnd.uniform(-2,2))],WD_S,2,.7); line(ctx,[(x+w+8,yy),(x+w+28,yy)],WD_S,2,.7)
    box(ctx,x-8,y-8,w+16,h+16,hexc('#2b2b30'),24,INK,3)

FIRES=[(0.35,3,3),(0.75,2,3),(1.15,4,3),(1.6,3,2),(2.0,5,3),(2.4,1,3),(2.8,3,1)]
def alien_pos(c,r,t):
    x=105+c*88+math.sin(t*0.9)*70; y=60+r*58+t*14
    return x,y
def shot4(ctx,t,dur):
    bg_flat(ctx,hexc('#14172c'))
    for i in range(30): circle(ctx,(i*97)%W,(i*61)%260,1.6,hexc('#5a6090'))
    z=lerp(1.0,1.07,ease_io(t/dur))
    ctx.save(); camera(ctx,z,700,300,t=t)
    sx0,sy0,sw,sh=360,52,840,490
    # desk
    box(ctx,-100,590,W+300,200,hexc('#5d3d2a'),0,INK,3)
    # light spill onto desk
    ellipse(ctx,780,600,420,20,hexc('#4a7bd8'),a=.25)
    tv_frame(ctx,sx0,sy0,sw,sh)
    ctx.save(); rrect(ctx,sx0,sy0,sw,sh,18); ctx.clip(); ctx.translate(sx0,sy0)
    box(ctx,0,0,sw,sh,hexc('#050510'))
    for i in range(40):
        circle(ctx,(i*131+t*6)%sw,(i*71+t*14)%sh,1.8,hexc('#7f86c9'))
    PX=5
    dead={}
    for (f,c,r) in FIRES:
        if t>=f+0.26: dead[(c,r)]=f+0.26
    cols=[hexc('#ff4fa0'),hexc('#ffd23f'),hexc('#48e0a0'),hexc('#5cc8ff')]
    for r in range(4):
        for c in range(7):
            if (c,r) in dead: continue
            ax,ay=alien_pos(c,r,t); sp=ALIEN if (int(t*2.5)+r)%2==0 else ALIEN2
            sprite(ctx,sp if r%2==0 else ALIEN2 if (int(t*2.5)%2==0) else ALIEN,ax,ay,PX,cols[r])
    # ship + lasers
    keys=[(0.0,alien_pos(3,3,0.0)[0])]
    for (f,c,r) in FIRES:
        xs=alien_pos(c,r,f+0.26)[0]+25
        keys+= [(f-0.18,keys[-1][1]),(f,xs),(f+0.1,xs)]
    shx=keys[-1][1]
    for i in range(len(keys)-1):
        if keys[i][0]<=t<keys[i+1][0]:
            shx=lerp(keys[i][1],keys[i+1][1],ease_io((t-keys[i][0])/max(.001,keys[i+1][0]-keys[i][0]))); break
    shy=sh-60
    # ship: triangle
    poly(ctx,[(shx,shy-34),(shx-28,shy+10),(shx+28,shy+10)],hexc('#e9f4ff'),None)
    poly(ctx,[(shx,shy-22),(shx-12,shy+4),(shx+12,shy+4)],hexc('#5cc8ff'))
    box(ctx,shx-40,shy+10,80,10,hexc('#8aa0c8')); box(ctx,shx-5,shy+20,10,8,hexc('#ffb02e'))
    for (f,c,r) in FIRES:
        if f<=t<f+0.26:
            xs=alien_pos(c,r,f+0.26)[0]+25; u=(t-f)/0.26; ty=alien_pos(c,r,f+0.26)[1]+30
            ly=lerp(shy-40,ty,u)
            box(ctx,xs-3,ly,6,26,hexc('#fff3a0')); box(ctx,xs-1.5,ly,3,26,(1,1,1))
        if f+0.26<=t<f+0.7:
            ex,ey=alien_pos(c,r,f+0.26); explosion_px(ctx,ex+25,ey+20,(t-f-0.26)/0.44,5,seed=f*10)
    # title
    k=pop(t,1.2,0.35)
    if k>0:
        tw=pixel_width("BLASTAR",12); ctx.save(); ctx.translate(sw/2,215); ctx.scale(k,k)
        box(ctx,-tw/2-30,-60,tw+60,140,hexc('#050510'),6,None); ctx.restore()
        ctx.save(); ctx.translate(sw/2,215); ctx.scale(k,k)
        pixel_text(ctx,"BLASTAR",-tw/2,-42,12,hexc('#ffd23f'),hexc('#d1352b'))
        ctx.restore()
    # scanlines
    for yy in range(0,sh,6): box(ctx,0,yy,sw,2,(0,0,0),0)
    ctx.restore()
    ctx.save(); rrect(ctx,sx0,sy0,sw,sh,18); ctx.set_source_rgba(0.4,0.6,1,0.06); ctx.fill(); ctx.restore()
    # glass highlight
    poly(ctx,[(sx0+30,sy0+16),(sx0+190,sy0+16),(sx0+130,sy0+60),(sx0+30,sy0+60)],(1,1,1),None,a=.05)
    # keyboard (back / top) in foreground
    box(ctx,430,628,500,60,BEIGE,6,INK,3)
    for r_ in range(2):
        for k_ in range(14): box(ctx,446+k_*34,636+r_*24,26,18,KEYB,3,INK,1.5)
    # kid from behind
    kid=cast('elon_kid',1.75)
    kx,ky=250,760
    kbob=math.sin(t*14)*3
    hl=arm_to(kid,kx,ky,-1,(520,668+kbob)); hr=arm_to(kid,kx,ky,1,(610,664-kbob))
    info=kid.draw(ctx,kx,ky,t,'neutral',False,0,armL=hl,armR=hr,legs=False,view="back",blink_seed=1)
    for h_ in (info['handL'],info['handR']): circle(ctx,h_[0],h_[1],10,SKIN,INK,2.5)
    # screen rim light on hair
    hx,hy=info['head']; R=info['R']
    ctx.save(); ctx.translate(hx,hy); ctx.scale(R/92,R/92); head_path(ctx,0,0,92,kid.jaw); ctx.clip()
    g=cairo.RadialGradient(120,-10,10,120,-10,150); g.add_color_stop_rgba(0,0.6,0.8,1,0.28); g.add_color_stop_rgba(1,0.6,0.8,1,0)
    ctx.set_source(g); ctx.paint(); ctx.restore()
    ctx.restore()

# =============================================================== SHOT 5
def shot5(ctx,t,dur):
    bg_room(ctx,wall=hexc('#cfe0d6'),floor=hexc('#9c7a58'),floor_y=600)
    z=lerp(1.0,1.08,ease_io(t/dur)); 
    ctx.save(); camera(ctx,z,lerp(640,700,ease_io(t/dur)),340,t=t)
    # wall details
    box(ctx,0,572,W,28,hexc('#b9ccc0'),0,INK,2)   # skirting
    ctx.save(); ctx.translate(620,236); mag_cover(ctx,170,225); ctx.restore()
    # shelf right
    box(ctx,1090,330,170,10,hexc('#7a5232'),0,INK,3)
    for i,c in enumerate(['#d9534f','#e9c46a','#2a9d8f','#6a8fd8','#e76f51','#8d6bb8']):
        box(ctx,1098+i*24,330-62-(i%3)*6,20,62+(i%3)*6,hexc(c),2,INK,2)
    # plant
    box(ctx,1120,500,50,70,hexc('#c0643e'),6,INK,3)
    for a in (-0.7,-0.25,0.25,0.7): 
        ctx.save(); ctx.translate(1145,505); ctx.rotate(a); ellipse(ctx,0,-36,13,38,hexc('#4aa35a')); ctx.restore()
    # chair back (editor)
    ex,ey=940,468
    box(ctx,ex-78,ey-250,156,230,hexc('#5b4a7a'),20,INK,3)
    # kid
    kid=cast('elon_kid',1.2)
    kx,ky=300,448
    # envelope path
    pop_t=2.6; slide0=3.0; slide1=3.65
    pos0=(742,468); pos1=(444,404)
    if t<slide0: epos=pos0
    else:
        u=ease_io((t-slide0)/(slide1-slide0)); epos=(lerp(pos0[0],pos1[0],u),lerp(pos0[1],pos1[1],u)-math.sin(u*math.pi)*60)
    # kid arm
    reach=ease_io((t-2.85)/0.5)
    hr=lp((25,125),arm_to(kid,kx,ky,1,(pos1[0]-30,pos1[1]+20)),reach)
    kinfo=kid.draw(ctx,kx,ky,t,'smug' if t>2.0 else 'neutral',(2.0<t),0.6,armL=(-25,125),armR=hr,legs=True,blink_seed=2)
    # editor
    ed=cast('editor',1.05)
    holding=t<2.3
    if holding:
        lc=(808,392+lerp(0,0,0))
        hl=arm_to(ed,ex,ey,-1,(lc[0]+14,lc[1]+64)); hr2=arm_to(ed,ex,ey,1,(lc[0]+38,lc[1]+70))
    else:
        w=ease_io((t-2.3)/0.4)
        lc=(808,392)
        hl=lp(arm_to(ed,ex,ey,-1,(lc[0]+14,lc[1]+64)),arm_to(ed,ex,ey,-1,(742-25,468+20)),w)
        hr2=lp(arm_to(ed,ex,ey,1,(lc[0]+38,lc[1]+70)),(30,125),w)
    expr='shocked' if t<2.2 else 'happy'
    einfo=ed.draw(ctx,ex,ey,t,expr,(0.3<t<1.9),-0.6,armL=hl,armR=hr2,legs=False,blink_seed=7)
    # listing (held) in front of editor chest
    if holding:
        ctx.save(); ctx.translate(*lc); ctx.rotate(-0.06); code_listing(ctx,128,168); ctx.restore()
        for h_ in (einfo['handL'],einfo['handR']): circle(ctx,h_[0],h_[1],9,SKIN,INK,2.5)
    # desk
    box(ctx,690,500,540,18,hexc('#b87d48'),0,INK,3)
    box(ctx,690,518,540,82,hexc('#a8703f'),0,INK,3)
    for dx in (0,1):
        box(ctx,940+dx*130-60,534,120,50,hexc('#946033'),4,INK,2.5); box(ctx,940+dx*130-14,552,28,8,hexc('#d6c07a'),3,INK,1.5)
    # items on desk: monitor-less; lamp + coffee + listing laid flat after
    box(ctx,1090,478,24,22,hexc('#f2f2f2'),4,INK,2.5); line(ctx,[(1114,486),(1122,486),(1122,494),(1114,494)],INK,3)
    if not holding:
        ctx.save(); ctx.translate(850,494); ctx.scale(1,0.2); ctx.rotate(0.05); code_listing(ctx,128,168); ctx.restore()
        for h_ in (einfo['handL'],einfo['handR']): circle(ctx,h_[0],h_[1],9,SKIN,INK,2.5)
    else:
        pass
    # envelope
    ctx.save()
    if t>pop_t:
        sc=pop(t,pop_t,0.3)
        smoke(ctx,epos[0],epos[1],(t-pop_t)/0.7,60,8)
        ctx.translate(*epos); ctx.scale(sc,sc); ctx.rotate(-0.1+0.1*clamp((t-slide0)/0.65)); envelope(ctx,110,70)
    ctx.restore()
    if t>=3.65:
        pass
    # dialogue
    if 0.3<=t<2.0:
        dialogue(ctx,"A twelve-year-old\nwrote this?",1125,130,(1010,225),42,reveal=clamp((t-0.3)/1.1))
    if t>=2.0:
        dialogue(ctx,"Yep. Five hundred\ndollars, please.",330,66,(330,150),42,reveal=clamp((t-2.0)/1.6))
    ctx.restore()

SCENES=[(3.6,shot1),(2.6,shot2),(4.6,shot3),(3.4,shot4),(4.2,shot5)]

CUES=[
 (1,0.0,"wind_ambience",-17),(1,0.3,"typewriter_tick",-14),(1,0.55,"typewriter_tick",-14),(1,0.8,"typewriter_tick",-14),(1,1.05,"typewriter_tick",-14),(1,1.3,"typewriter_tick",-14),(1,1.55,"typewriter_tick",-14),(1,1.8,"typewriter_tick",-14),
 (1,2.4,"page_flip",-12),
 (2,0.0,"wind_ambience",-18),(2,0.7,"whoosh_short",-8),(2,0.82,"shove_hit",-4),(2,1.0,"boing",-12),(2,1.65,"book_drop",-5),
 (3,0.0,"night_crickets",-16),(3,0.2,"typing_burst",-8),(3,0.3,"pop",-6),(3,1.3,"paper_rustle",-10),(3,1.55,"paper_rustle",-10),(3,2.0,"typing_burst",-8),(3,2.2,"pop",-5),(3,2.3,"sparkle",-12),(3,3.4,"key_clack",-12),
 (4,0.0,"office_hum",-22),(4,0.35,"retro_laser",-12),(4,0.61,"retro_explosion",-12),(4,0.75,"retro_laser",-12),(4,1.01,"retro_explosion",-12),
 (4,1.15,"retro_laser",-12),(4,1.2,"retro_jingle",-8),(4,1.41,"retro_explosion",-12),(4,1.6,"retro_laser",-12),(4,1.86,"retro_explosion",-12),
 (4,2.0,"retro_laser",-12),(4,2.26,"retro_explosion",-12),(4,2.4,"retro_laser",-12),(4,2.66,"retro_explosion",-12),(4,2.8,"retro_laser",-12),(4,3.06,"retro_explosion",-12),
 (5,0.0,"office_hum",-18),(5,0.3,"typewriter_tick",-14),(5,0.5,"typewriter_tick",-14),(5,0.7,"typewriter_tick",-14),(5,0.9,"typewriter_tick",-14),(5,1.1,"typewriter_tick",-14),
 (5,2.0,"typewriter_tick",-14),(5,2.2,"typewriter_tick",-14),(5,2.4,"typewriter_tick",-14),(5,2.6,"pop",-6),(5,2.6,"cash_register",-6),(5,3.0,"whoosh_short",-8),(5,3.65,"ding",-12),
]
