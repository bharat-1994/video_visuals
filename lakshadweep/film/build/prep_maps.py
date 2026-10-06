import cv2,numpy as np,os,glob
M='assets/maps'
def enhance(im, gamma=0.72, sat=1.25, blue=True):
    # fill isolated black (masked) pixels by median of neighbours
    mask=(im.sum(axis=2)==0).astype(np.uint8)
    k=cv2.dilate(mask,np.ones((3,3),np.uint8))
    med=cv2.medianBlur(im,5)
    # only fill small isolated holes: where mask local density is low
    dens=cv2.blur(mask.astype(np.float32),(15,15))
    fill=(mask>0)&(dens<0.25)
    im=np.where(fill[...,None],med,im)
    f=im.astype(np.float32)/255.0
    f=f**gamma
    hsv=cv2.cvtColor((f*255).astype(np.uint8),cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[...,1]=np.clip(hsv[...,1]*sat,0,255)
    out=cv2.cvtColor(hsv.astype(np.uint8),cv2.COLOR_HSV2RGB).astype(np.float32)
    if blue:
        lum=out.mean(axis=2,keepdims=True)/255.0
        out=out+(1-lum)**3*np.array([-4,10,26],np.float32)   # lift deep-ocean into a richer navy/teal
    return np.clip(out,0,255).astype(np.uint8)
for f in ['agatti_hls','minicoy_hls','kavaratti_hls','kalpeni_hls','kadmat_hls','bangaram_hls']:
    p=f'{M}/{f}.jpg'
    if not os.path.exists(p): continue
    im=cv2.cvtColor(cv2.imread(p),cv2.COLOR_BGR2RGB)
    # cubic upsample 2x with mild unsharp for less blocky zooms
    im=cv2.resize(im,None,fx=1.5,fy=1.5,interpolation=cv2.INTER_CUBIC)
    e=enhance(im)
    bl=cv2.GaussianBlur(e,(0,0),1.2)
    e=cv2.addWeighted(e,1.5,bl,-0.5,0)
    cv2.imwrite(f'{M}/{f}_e.jpg',cv2.cvtColor(e,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,93])
    print(f,e.shape)
# Hyderabad night glow, tone-mapped
n=cv2.imread(f'{M}/hyd_night.jpg').astype(np.float32)[...,::-1]/255.0
n=cv2.resize(n,None,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)
g=cv2.GaussianBlur(n,(0,0),7)*0.85+cv2.GaussianBlur(n,(0,0),22)*0.9+n*0.25
g=1-np.exp(-g*1.9)
g=g**0.9
g=g*np.array([1.0,0.82,0.55])+0.02*np.array([0.1,0.3,0.6])
cv2.imwrite(f'{M}/hyd_glow.jpg',cv2.cvtColor((np.clip(g,0,1)*255).astype(np.uint8),cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,93])
print('hyd glow done')
