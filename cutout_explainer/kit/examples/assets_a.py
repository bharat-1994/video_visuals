import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
from lib import *
import math, random

SAND=hexc('#e4c590'); SAND_S=hexc('#c6a26a'); SAND_H=hexc('#f3e0b4')
ROOF=hexc('#c8553a'); ROOF_S=hexc('#9c3d2a')
COPPER=hexc('#5fa89a'); COPPER_S=hexc('#3f7f74')
THIN=2.2

def col(ctx,x,y,w,h):
    box(ctx,x,y,w,h,SAND_H); box(ctx,x+w*.55,y,w*.45,h,SAND_S)
    line(ctx,[(x,y),(x,y+h)],INK,1.2,.7); line(ctx,[(x+w,y),(x+w,y+h)],INK,1.2,.7)

def tower(ctx,x,base,s=1.0):
    """tall tower with cupola, origin bottom-center."""
    ctx.save(); ctx.translate(x,base); ctx.scale(s,s)
    w=64; h=170
    box(ctx,-w/2,-h,w,h,SAND,0,INK,THIN); box(ctx,w*.1,-h,w*.4,h,SAND_S)
    line(ctx,[(-w/2,-h),(-w/2,0)],INK,THIN); line(ctx,[(w/2,-h),(w/2,0)],INK,THIN)
    # banding
    for y in (-120,-60): box(ctx,-w/2-4,y,w+8,8,SAND_H,0,INK,1.6)
    # windows
    for y in (-150,-100,-44):
        box(ctx,-10,y,20,28,hexc('#4a5a73'),9,INK,1.6); box(ctx,-10,y,20,6,hexc('#2f3b4d'),0)
    # cornice + belfry stage
    box(ctx,-w/2-8,-h-10,w+16,12,SAND_H,0,INK,THIN)
    box(ctx,-w/2+8,-h-44,w-16,34,SAND,0,INK,THIN); box(ctx,w*.12,-h-44,w*.3,34,SAND_S)
    for i in range(3): box(ctx,-w/2+14+i*17,-h-40,10,24,hexc('#3a4658'),5,INK,1.4)
    box(ctx,-w/2+4,-h-52,w-8,10,SAND_H,0,INK,THIN)
    # dome
    ctx.move_to(-w/2+8,-h-52); ctx.curve_to(-w/2+8,-h-100,w/2-8,-h-100,w/2-8,-h-52); ctx.close_path()
    ctx.set_source_rgb(*COPPER); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(THIN); ctx.stroke()
    ctx.move_to(0,-h-52); ctx.curve_to(0,-h-86,w/2-8,-h-86,w/2-8,-h-52); ctx.close_path(); ctx.set_source_rgb(*COPPER_S); ctx.fill()
    box(ctx,-5,-h-110,10,14,COPPER,2,INK,1.6); line(ctx,[(0,-h-110),(0,-h-128)],INK,2.4); circle(ctx,0,-h-130,3,hexc('#e8c14a'),INK,1.2)
    ctx.restore()

def union_buildings(ctx,x,base,s=1.0):
    """long symmetrical sandstone building, origin bottom-center, ~900*s wide."""
    ctx.save(); ctx.translate(x,base); ctx.scale(s,s)
    # wings
    for sd in (-1,1):
        wx=sd*235; 
        # wing body
        x0=min(wx,wx+sd*235) ; 
        box(ctx,x0,-78,235 if True else 0,78,SAND,0,INK,THIN)
        box(ctx,x0,-18,235,18,SAND_S)
        # roof (tiles)
        poly(ctx,[(x0-4,-78),(x0+235+4,-78),(x0+235-18,-108),(x0+18,-108)],ROOF,INK,THIN)
        for i in range(1,5): line(ctx,[(x0+i*47,-78),(x0+i*47-(6 if i<3 else -6)*0+0,-108)],ROOF_S,1.6,.8)
        line(ctx,[(x0+10,-93),(x0+225,-93)],ROOF_S,1.6,.8)
        for i in range(10):
            wxx=x0+16+i*22
            box(ctx,wxx,-62,12,30,hexc('#4a5a73'),5,INK,1.3); line(ctx,[(wxx-2,-31),(wxx+14,-31)],SAND_H,2.5)
    # ends: pavilions
    for sd in (-1,1):
        px=sd*470-34
        box(ctx,px,-96,68,96,SAND,0,INK,THIN); box(ctx,px+(36 if sd<0 else 8),-96,26,96,SAND_S)
        poly(ctx,[(px-5,-96),(px+73,-96),(px+60,-122),(px+8,-122)],ROOF,INK,THIN)
        for i in range(3): box(ctx,px+10+i*20,-78,12,34,hexc('#4a5a73'),5,INK,1.3)
    # central amphitheatre: stepped base, curved colonnade
    box(ctx,-210,-14,420,14,SAND_H,0,INK,THIN); box(ctx,-190,-26,380,12,SAND,0,INK,THIN)
    # back wall behind columns
    box(ctx,-200,-120,400,94,SAND_S,0,INK,THIN)
    for i in range(7): box(ctx,-190+i*58,-100,26,60,hexc('#8a7a64'),13,None) 
    # columns: pairs in arc (center ones larger, outer smaller via y offset)
    N=15
    for i in range(N):
        u=(i/(N-1))*2-1
        cx=u*190; hh=104-abs(u)*0   ; y0=-26-(1-u*u)**.5*0
        col(ctx,cx-6,-124,12,98+ (1-abs(u))*0)
    box(ctx,-206,-134,412,14,SAND_H,0,INK,THIN); box(ctx,-206,-124,412,6,SAND_S)
    # curved cornice hint
    ctx.move_to(-206,-134); ctx.curve_to(-120,-170,120,-170,206,-134); ctx.line_to(206,-148); ctx.curve_to(120,-186,-120,-186,-206,-148); ctx.close_path()
    ctx.set_source_rgb(*SAND); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(THIN); ctx.stroke()
    # stairs
    for i in range(4): box(ctx,-70-i*10,-i*0-4-i*0+i*0,140+i*20,0.1,SAND_S)
    # towers flanking
    tower(ctx,-232,-92,1.0); tower(ctx,232,-92,1.0)
    ctx.restore()

def terraces(ctx,x,y,w,h):
    """terraced gardens: bands of green with retaining walls and path."""
    cols=[hexc('#5fa653'),hexc('#79bb62'),hexc('#5fa653'),hexc('#79bb62')]
    n=4; bh=h/n
    for i in range(n):
        yy=y+i*bh
        box(ctx,x,yy,w,bh,cols[i]); box(ctx,x,yy+bh-14,w,14,SAND,0,INK,1.6)
        box(ctx,x,yy+bh-14,w,5,SAND_H)
        for k in range(int(w/38)):
            circle(ctx,x+20+k*38+(i%2)*19,yy+bh*.4,9,hexc('#3f8a45'),a=.55)
    # central stair/path
    poly(ctx,[(x+w/2-40,y),(x+w/2+40,y),(x+w/2+70,y+h),(x+w/2-70,y+h)],SAND_H,INK,1.6)
    for i in range(1,10):
        yy=y+i*h/10; line(ctx,[(x+w/2-40-30*i/10,yy),(x+w/2+40+30*i/10,yy)],SAND_S,2)

def jacaranda(ctx,x,y,s=1.0,seed=1,t=0):
    """y = ground at trunk base."""
    rnd=random.Random(seed)
    ctx.save(); ctx.translate(x,y); ctx.scale(s,s)
    TR=hexc('#4a3329')
    ctx.move_to(-16,0); ctx.curve_to(-12,-80,-18,-140,-8,-210); ctx.line_to(10,-210); ctx.curve_to(16,-140,12,-80,18,0); ctx.close_path()
    ctx.set_source_rgb(*TR); ctx.fill_preserve(); ctx.set_source_rgb(*INK); ctx.set_line_width(2.5); ctx.stroke()
    line(ctx,[(0,-170),(-70,-250)],TR,12); line(ctx,[(2,-180),(80,-260)],TR,12); line(ctx,[(0,-190),(2,-290)],TR,10)
    blobs=[(0,-340,120),(-110,-290,90),(110,-296,92),(-60,-390,80),(70,-392,82),(-170,-250,60),(170,-255,62),(0,-440,60)]
    P1=hexc('#7b52a8'); P2=hexc('#9a72c8'); P3=hexc('#b895e0')
    for (bx,by,r) in blobs: circle(ctx,bx,by+10,r,P1,INK,2.2)
    for (bx,by,r) in blobs: circle(ctx,bx,by,r*.92,P2)
    for (bx,by,r) in blobs:
        for k in range(7):
            a=rnd.uniform(0,6.28); d=rnd.uniform(0,r*.7); circle(ctx,bx+math.cos(a)*d-r*.15,by+math.sin(a)*d-r*.2,rnd.uniform(9,18),P3,a=.85)
    for k in range(14):
        a=rnd.uniform(0,6.28); d=rnd.uniform(40,170); circle(ctx,math.cos(a)*d,-330+math.sin(a)*d*.8,4,hexc('#d8c1f0'))
    ctx.restore()

def petals(ctx,t,x0,x1,y0,y1,n=14,seed=2):
    rnd=random.Random(seed)
    for i in range(n):
        px=lerp(x0,x1,rnd.random()); ph=rnd.random(); sp=rnd.uniform(30,50)
        py=y0+((t*sp+ph*(y1-y0))%(y1-y0))
        circle(ctx,px+math.sin(t*2+i)*14,py,4,hexc('#b895e0'))

# ----------------------------------------------------------------- books
def open_book_back(ctx,w=170,h=210,c=hexc('#3b6ea8')):
    """book held open facing the reader (to the right/behind); we see its outer back cover as a flat slab with spine ridge."""
    box(ctx,-w/2,-h/2,w,h,c,6,INK,4)
    box(ctx,-w/2,-h/2,14,h,tuple(v*.7 for v in c),3,INK,2)
    box(ctx,-w/2+34,-h/2+36,w-68,38,(1,1,1),3,INK,2)
    text(ctx,"READ",-w/2+34+(w-68)/2,-h/2+55,26,INK)
    for i in range(3): line(ctx,[(-w/2+34,-h/2+96+i*16),(w/2-34,-h/2+96+i*16)],hexc('#ffffff'),3,.6)

def spiral_manual(ctx,w=200,h=120,open_=True):
    """open spiral-bound thick manual, seen from above-front, centered origin."""
    # page stack thickness
    poly(ctx,[(-w,-h/2+6),(0,-h/2+10),(0,h/2+10),(-w,h/2+6)],hexc('#d8d2c0'),INK,2)
    poly(ctx,[(w,-h/2+6),(0,-h/2+10),(0,h/2+10),(w,h/2+6)],hexc('#d8d2c0'),INK,2)
    for sd in (-1,1):
        poly(ctx,[(0,-h/2),(sd*w,-h/2-6),(sd*w,h/2-6),(0,h/2)],hexc('#fbf8ee'),INK,2.5)
        for i in range(7):
            yy=-h/2+16+i*(h-32)/7
            line(ctx,[(sd*14,yy+2),(sd*(w-22),yy-3 )],(0.62,0.62,0.66),2.2)
    # code snippet boxes
    box(ctx,-w+20,-h/2+12,60,30,hexc('#cfe3f2'),2,INK,1.2)
    # spiral rings
    for i in range(9):
        yy=-h/2+8+i*(h-6)/8.5
        ellipse(ctx,0,yy+2,7,4.4,hexc('#9aa3ad')); ctx.new_path()
        line(ctx,[(-9,yy+2),(9,yy+2)],INK,2)

def sticky(ctx,w=170,h=150,c=hexc('#ffe36b')):
    poly(ctx,[(-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2+14,h/2),(-w/2,h/2-14)],c,INK,2.5)
    box(ctx,-w/2,-h/2,w,16,tuple(v*.92 for v in c))

# ----------------------------------------------------------------- VIC-20 & TV
BEIGE=hexc('#e6dcc3'); BEIGE_S=hexc('#c9bd9d'); BEIGE_H=hexc('#f6f0dc'); KEYB=hexc('#6a4a3a'); KEYB_H=hexc('#8a6652')

def vic20_side(ctx,x,y,s=1.0):
    """wedge keyboard computer seen from its left side (front/low end at left), slightly from above.
    origin = bottom-left corner of the case on the desk."""
    ctx.save(); ctx.translate(x,y); ctx.scale(s,s)
    L=230; Hf=30; Hb=78; dz=34   # length, front height, back height, depth offset (top face recedes up-right)
    # right-hand (far) top face: sloped keyboard surface as parallelogram
    top=[(0,-Hf),(L,-Hb),(L+dz,-Hb-dz*.55),(dz,-Hf-dz*.55)]
    # near side face (profile)
    side=[(0,0),(L,0),(L,-Hb),(0,-Hf)]
    poly(ctx,side,BEIGE,INK,2.5)
    poly(ctx,[(0,-6),(L,-6),(L,0),(0,0)],BEIGE_S)
    for i in range(4): line(ctx,[(40+i*38,-12),(40+i*38,-4)],BEIGE_S,3)
    poly(ctx,top,BEIGE_H,INK,2.5)
    # keys: 5 rows along slope direction (rows go back = up-right), 
    ux=(L-24)/L; 
    for r in range(5):
        for k in range(8):
            u=0.06+k*0.115   # along length
            v=0.12+r*0.17     # along depth
            px=u*L+v*dz; py=-Hf+u*(Hf-Hb)*-1*-1  # slope
            py=-Hf-(Hb-Hf)*u - v*dz*.55
            poly(ctx,[(px,py),(px+16,py-(Hb-Hf)*0.07*1),(px+16+4,py-6-2),(px+4,py-5)],KEYB,None)
            poly(ctx,[(px,py-1),(px+14,py-1-(Hb-Hf)*.07),(px+17,py-5),(px+4,py-5)],KEYB_H,None)
    # label strip (plain, no logo)
    poly(ctx,[(L*.62,-Hf-(Hb-Hf)*.62-1),(L*.62+36,-Hf-(Hb-Hf)*.62-2.5),(L*.62+40,-Hf-(Hb-Hf)*.62-8),(L*.62+6,-Hf-(Hb-Hf)*.62-6)],hexc('#8b8f98'))
    # back panel/port & cable exit
    ctx.restore()
    return (x+(L+dz*.5)*s, y-(Hb+dz*.25)*s)  # cable exit

def tv_angled(ctx,x,y,t,s=1.0,draw_screen=None,glow=1.0):
    """small CRT TV on wood-grain casing, facing LEFT (screen toward the user), seen from the side:
    origin = bottom-left of its front face on the surface. front face is a narrow skewed quad, body recedes right."""
    ctx.save(); ctx.translate(x,y); ctx.scale(s,s)
    WD=hexc('#a8703f'); WD_S=hexc('#80502a'); WD_H=hexc('#c28a52')
    fw=112; fh=200; sk=-20  # front face: width, height, skew
    Dp=150  # body depth
    # feet
    box(ctx,fw+10,-6,30,8,INK,2); box(ctx,fw+Dp-60,-6,30,8,INK,2)
    # top face (back narrower)
    poly(ctx,[(0,-fh),(fw,-fh+sk),(fw+Dp,-fh+sk+22),(Dp*0.18,-fh+22)],WD_H,INK,2.5)
    # side body (far/right side visible, tapering)
    poly(ctx,[(fw,-fh+sk),(fw+Dp,-fh+sk+22),(fw+Dp,-34),(fw,0+sk*0-2)],WD,INK,2.5)
    for i in range(1,8):
        yy=-fh+sk+i*(fh-30)/8
        line(ctx,[(fw+4,yy+ (2)),(fw+Dp-6,yy+22*(1-i/8)+i*0.6)],WD_S,1.6,.7)
    # knobs on side near front? put on front face lower strip
    # front face
    poly(ctx,[(0,-fh),(fw,-fh+sk),(fw,0+sk*0-2),(0,0)],WD,INK,2.5)
    # screen bezel + glass (skewed)
    m=cairo.Matrix(1,0,0,1,0,0)
    sx0,sy0=8,-fh+12; sw,sh=fw-20,fh-66
    poly(ctx,[(sx0,sy0),(sx0+sw,sy0+sk*(sw/fw)),(sx0+sw,sy0+sh+sk*(sw/fw)),(sx0,sy0+sh)],hexc('#1d1d22'),INK,2)
    ix0,iy0=sx0+4,sy0+5; iw,ih=sw-8,sh-10
    ctx.save()
    ctx.move_to(ix0,iy0); ctx.line_to(ix0+iw,iy0+sk*(iw/fw)); ctx.line_to(ix0+iw,iy0+ih+sk*(iw/fw)); ctx.line_to(ix0,iy0+ih); ctx.close_path(); ctx.clip()
    ctx.set_source_rgb(*hexc('#3d5fd0')); ctx.paint()
    ctx.transform(cairo.Matrix(iw/184,sk*(iw/fw)/184,0,ih/132,ix0,iy0))
    if draw_screen: draw_screen(ctx,t)
    ctx.restore()
    # control strip
    for i in range(2): circle(ctx,14+i*20,-30,6,hexc('#2b2b2b'),INK,1.5)
    for i in range(5): line(ctx,[(48,-40+i*6),(fw-10,-40+i*6+sk*0.5)],WD_S,2)
    ctx.restore()

def vic_screen(ctx,t):
    """classic VIC-20 boot screen (light blue border, blue field)."""
    ctx.set_source_rgb(*hexc('#b9c4f5')); ctx.paint()
    box(ctx,12,10,160,112,hexc('#3d3fcf'))
    text(ctx,"**** CBM BASIC V2 ****",92,28,12,hexc('#b9c4f5'))
    text(ctx,"3583 BYTES FREE",92,46,12,hexc('#b9c4f5'))
    text(ctx,"READY.",32,68,13,hexc('#b9c4f5'),anchor="l")
    if int(t*2)%2==0: box(ctx,32,76,10,13,hexc('#b9c4f5'))

# ----------------------------------------------------------------- pixel stuff
FONT5={
 'B':["1111.","1...1","1111.","1...1","1...1","1...1","1111."],
 'L':["1....","1....","1....","1....","1....","1....","11111"],
 'A':[".111.","1...1","1...1","11111","1...1","1...1","1...1"],
 'S':[".1111","1....","1....",".111.","....1","....1","1111."],
 'T':["11111","..1..","..1..","..1..","..1..","..1..","..1.."],
 'R':["1111.","1...1","1...1","1111.","1.1..","1..1.","1...1"],
}
def pixel_text(ctx,s,x,y,px,c=(1,1,1),sh=None,gap=1):
    """draw string with squares; x,y top-left."""
    cx=x
    for ch in s:
        g=FONT5[ch]
        for r,row in enumerate(g):
            for k,v in enumerate(row):
                if v=='1':
                    if sh: box(ctx,cx+k*px+px*.35,y+r*px+px*.35,px,px,sh)
        for r,row in enumerate(g):
            for k,v in enumerate(row):
                if v=='1': box(ctx,cx+k*px,y+r*px,px+0.6,px+0.6,c)
        cx+=(5+gap)*px
    return cx-x
def pixel_width(s,px,gap=1): return len(s)*(5+gap)*px-gap*px

ALIEN=[
 "..1....1..",
 "...1..1...",
 "..111111..",
 ".11.11.11.",
 "1111111111",
 "1.111111.1",
 "1.1....1.1",
 "...11.11..",
]
ALIEN2=[
 "...1111...",
 ".11111111.",
 "1111111111",
 "11..11..11",
 "1111111111",
 "..11..11..",
 ".11.11.11.",
 "11......11",
]
def sprite(ctx,rows,x,y,px,c):
    for r,row in enumerate(rows):
        for k,v in enumerate(row):
            if v=='1': box(ctx,x+k*px,y+r*px,px+0.5,px+0.5,c)

def explosion_px(ctx,x,y,k,px=5,seed=1):
    """pixel burst; k 0..1."""
    if k<=0 or k>=1: return
    rnd=random.Random(seed); r=ease_out(k)*px*7
    cols=[hexc('#fff3a0'),hexc('#ffb02e'),hexc('#ff5a36'),(1,1,1)]
    for i in range(22):
        a=rnd.uniform(0,6.28); d=r*rnd.uniform(.3,1)
        sz=px*(1.6 if rnd.random()<.4 else 1.0)*(1-k*.6)
        c=cols[int(clamp(k*2+rnd.random()*1.5,0,3))]
        px_=round((x+math.cos(a)*d)/px)*px; py_=round((y+math.sin(a)*d)/px)*px
        box(ctx,px_,py_,sz,sz,c)

# ----------------------------------------------------------------- office props
def mag_cover(ctx,w=190,h=250):
    box(ctx,-w/2-10,-h/2-10,w+20,h+20,hexc('#6b4a2e'),4,INK,3)   # frame
    box(ctx,-w/2,-h/2,w,h,(1,1,1),0,INK,2)
    box(ctx,-w/2,-h/2,w,66,hexc('#1f4f9a'))
    text(ctx,"PC and Office",0,-h/2+22,30,(1,1,1))
    text(ctx,"Technology",0,-h/2+50,30,(1,1,1))
    # cover art: little computer
    box(ctx,-46,-30,92,70,hexc('#d9d3bd'),6,INK,2.5); box(ctx,-36,-22,72,48,hexc('#2f5fb0'),3)
    line(ctx,[(-28,-12),(10,-12)],(1,1,1),3); line(ctx,[(-28,0),(22,0)],(1,1,1),3); line(ctx,[(-28,12),(0,12)],(1,1,1),3)
    box(ctx,-52,50,104,16,hexc('#bdb6a0'),4,INK,2)
    box(ctx,-w/2+12,h/2-34,w-24,10,hexc('#e0603a')); box(ctx,-w/2+12,h/2-18,60,6,hexc('#999999'))

def code_listing(ctx,w=130,h=170,seed=3):
    """printed code listing: tractor-feed paper with tiny code lines."""
    rnd=random.Random(seed)
    box(ctx,-w/2,-h/2,w,h,(0.98,0.98,0.95),2,INK,3)
    box(ctx,-w/2,-h/2,12,h,(0.88,0.9,0.86),0,INK,1.5); box(ctx,w/2-12,-h/2,12,h,(0.88,0.9,0.86),0,INK,1.5)
    for i in range(8):
        circle(ctx,-w/2+6,-h/2+10+i*21,2.4,(0.55,0.55,0.55)); circle(ctx,w/2-6,-h/2+10+i*21,2.4,(0.55,0.55,0.55))
    for i in range(13):
        yy=-h/2+12+i*(h-20)/13
        ind=rnd.choice([0,0,10,20]); ln=rnd.randint(30,w-44-ind)
        line(ctx,[(-w/2+20+ind,yy),(-w/2+20+ind+ln,yy)],hexc('#3a3a46'),2.4,.85)
        if rnd.random()<.4: line(ctx,[(-w/2+22+ind,yy),(-w/2+22+ind+10,yy)],hexc('#c0392b'),2.4)
    # line numbers column
    for i in range(13):
        yy=-h/2+12+i*(h-20)/13; line(ctx,[(-w/2+15,yy),(-w/2+18,yy)],(0.5,0.5,0.5),2)

def envelope(ctx,w=120,h=76):
    box(ctx,-w/2,-h/2,w,h,hexc('#f2ebd3'),4,INK,3)
    line(ctx,[(-w/2+2,-h/2+2),(0,6),(w/2-2,-h/2+2)],INK,2.5)
    line(ctx,[(-w/2+2,h/2-2),(-14,0)],INK,1.5,.5); line(ctx,[(w/2-2,h/2-2),(14,0)],INK,1.5,.5)
    circle(ctx,0,12,15,hexc('#e1f2d8'),hexc('#3f8a45'),2.5)
    text(ctx,"$500",0,14,18,hexc('#2c6e33'))
