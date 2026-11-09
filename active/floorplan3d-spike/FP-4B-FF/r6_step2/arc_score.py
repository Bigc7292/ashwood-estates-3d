import numpy as np, json, math
from PIL import Image
R=4;U0=(110,100)
L=np.asarray(Image.open('work.png')).astype(float).mean(2)
def val(x,y):
    i,j=(y-U0[1])*R,(x-U0[0])*R; return L[int(round(i)),int(round(j))]
D=json.load(open('doors6.json')); out={}
for d in D:
    a,b=d['span']; w=b-a; c=d['at']
    hyps=[]
    for hinge in ('a','b'):
        for side in (-1,1):
            # hinge point and closed direction
            if d['axis']=='x':
                hx,hy=c,(a if hinge=='a' else b); cdir=(0,1 if hinge=='a' else -1); odir=(side,0)
            else:
                hx,hy=(a if hinge=='a' else b),c; cdir=(1 if hinge=='a' else -1,0); odir=(0,side)
            sc=[];bg=[]
            for k in range(12,79,3):
                t=math.radians(k)
                for rr,lst in ((w*0.97,sc),(w*0.97,None)):
                    pass
                # sample min lum across radius +-0.75u
                vals=[val(hx+(cdir[0]*math.cos(t)+odir[0]*math.sin(t))*r_, hy+(cdir[1]*math.cos(t)+odir[1]*math.sin(t))*r_) for r_ in np.arange(w*0.85,w*1.06,0.25)]
                ref=[val(hx+(cdir[0]*math.cos(t)+odir[0]*math.sin(t))*r_, hy+(cdir[1]*math.cos(t)+odir[1]*math.sin(t))*r_) for r_ in (w*0.6,w*0.7)]
                mv=min(vals); sc.append(np.nan if mv<95 or min(ref)<95 else np.median(ref)-mv)
            # fraction of arc samples that show a darker line
            S=np.array(sc); ok=~np.isnan(S); hyps.append((round(float(np.sum(S[ok]>12)/len(S)),2),int(ok.sum()),round(float(np.nanmedian(S)) if ok.any() else 0,1),hinge,side))
    hyps.sort(reverse=True); out[d['id']]=hyps
    print(d['id'],hyps[:2])
json.dump(out,open('arcs.json','w'))
