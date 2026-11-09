import numpy as np, sys
R=4;U0=(110,100)
th=np.load('thick.npy')
from PIL import Image
L=np.asarray(Image.open('work.png')).astype(int).mean(2)
dk=L<110
def runs(arr,start):
    out=[];cur=None
    for k,v in enumerate(arr):
        if v and cur is None: cur=k
        if not v and cur is not None: out.append((round(start+cur/R,1),round(start+k/R,1))); cur=None
    if cur is not None: out.append((round(start+cur/R,1),round(start+len(arr)/R,1)))
    return [r for r in out if r[1]-r[0]>=0.75]
def h(y,x0=139,x1=522,m=th):
    i=int((y-U0[1])*R); return runs(m[i,int((x0-U0[0])*R):int((x1-U0[0])*R)],x0)
def v(x,y0=142,y1=844,m=th):
    j=int((x-U0[0])*R); return runs(m[int((y0-U0[1])*R):int((y1-U0[1])*R),j],y0)
for a in sys.argv[1:]:
    t,c=a[0],float(a[1:])
    print(a,'thick',(h if t=='h' else v)(c),'\n   dark',(h if t=='h' else v)(c,m=dk))
