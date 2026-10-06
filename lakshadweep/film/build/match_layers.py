"""Frequency-separation colour matching so finer satellite layers melt into coarser ones."""
import cv2,numpy as np,os,sys
os.chdir('/home/user/video_visuals/lakshadweep/film')
sys.path.insert(0,'render')
M='assets/maps'
def load(f): return cv2.cvtColor(cv2.imread(f'{M}/{f}'),cv2.COLOR_BGR2RGB).astype(np.float32)
def resample(coarse,cb,fb,shape):
    """crop coarse (bbox cb) to bbox fb, resized to shape (h,w)."""
    ch,cw=coarse.shape[:2]
    x0=(fb[0]-cb[0])/(cb[2]-cb[0])*cw; x1=(fb[2]-cb[0])/(cb[2]-cb[0])*cw
    y0=(cb[3]-fb[3])/(cb[3]-cb[1])*ch; y1=(cb[3]-fb[1])/(cb[3]-cb[1])*ch
    x0,x1,y0,y1=[int(round(v)) for v in (x0,x1,y0,y1)]
    pad=max(0,-x0,-y0,x1-cw,y1-ch)
    c=cv2.copyMakeBorder(coarse,pad,pad,pad,pad,cv2.BORDER_REPLICATE) if pad else coarse
    c=c[y0+pad:y1+pad,x0+pad:x1+pad]
    return cv2.resize(c,(shape[1],shape[0]),interpolation=cv2.INTER_CUBIC)
def match(fine_f,fine_bb,coarse_f,coarse_bb,out_f,k=0.85,sigma_frac=0.03):
    fine=load(fine_f); coarse=load(coarse_f)
    c=resample(coarse,coarse_bb,fine_bb,fine.shape[:2])
    s=sigma_frac*min(fine.shape[:2])
    bf=cv2.GaussianBlur(fine,(0,0),s); bc=cv2.GaussianBlur(c,(0,0),s)
    out=fine+k*(bc-bf)
    out=np.clip(out,0,255).astype(np.uint8)
    cv2.imwrite(f'{M}/{out_f}',cv2.cvtColor(out,cv2.COLOR_RGB2BGR),[cv2.IMWRITE_JPEG_QUALITY,93])
    print('matched',out_f)
MID_ALL=(70.5,7.5,75.5,12.5); RIDGE=(66,4,78,16)
match('mid_all_mo_e.jpg',MID_ALL,'ridge_bathy.jpg',RIDGE,'mid_all_mo_m.jpg',k=0.45,sigma_frac=0.04)
match('mid_north_e.jpg',(71.9,10.4,73.9,11.8),'mid_all_mo_m.jpg',MID_ALL,'mid_north_m.jpg')
match('mid_minicoy_e.jpg',(72.7,8.0,73.4,8.55),'mid_all_mo_m.jpg',MID_ALL,'mid_minicoy_m.jpg')
match('mid_kalpeni_e.jpg',(73.3,9.8,74.0,10.35),'mid_all_mo_m.jpg',MID_ALL,'mid_kalpeni_m.jpg')
match('agatti_hls_e.jpg',(72.00,10.74,72.40,10.965),'mid_north_m.jpg',(71.9,10.4,73.9,11.8),'agatti_hls_m.jpg')
match('minicoy_hls_e.jpg',(72.85,8.17,73.25,8.395),'mid_minicoy_m.jpg',(72.7,8.0,73.4,8.55),'minicoy_hls_m.jpg')
match('kalpeni_hls_e.jpg',(73.45,9.97,73.85,10.195),'mid_kalpeni_m.jpg',(73.3,9.8,74.0,10.35),'kalpeni_hls_m.jpg')
match('bangaram_hls_e.jpg',(72.10,10.80,72.50,11.025),'mid_north_m.jpg',(71.9,10.4,73.9,11.8),'bangaram_hls_m.jpg')
match('kadmat_hls_e.jpg',(72.58,11.05,72.98,11.275),'mid_north_m.jpg',(71.9,10.4,73.9,11.8),'kadmat_hls_m.jpg')
match('kavaratti_hls_e.jpg',(72.45,10.46,72.85,10.685),'mid_north_m.jpg',(71.9,10.4,73.9,11.8),'kavaratti_hls_m.jpg')
