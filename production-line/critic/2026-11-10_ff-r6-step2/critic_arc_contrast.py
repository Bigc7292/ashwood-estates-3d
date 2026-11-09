from PIL import Image, ImageDraw, ImageOps
import json, math
Image.MAX_IMAGE_PIXELS=None
P=Image.open('/workspace/critic-wt-first-floor/active/approved-cad-v4/png/FP-4B-FF_V4_long7680.png').convert('RGB')
d=json.load(open('/workspace/critic-wt-first-floor/active/floorplan3d-spike/FP-4B-FF/data/fp-4b-ff.plan.r6.json'))
k=0.18307; X=lambda x:1278.9+x*k; Y=lambda y:1334.5+y*k
L=P.convert('L'); px=L.load()
# background ~ beige; arc pixels are darker greenish lines. score = fraction of samples with a pixel darker than bg-25 within 2px
def dark(x,y):
    x,y=int(round(x)),int(round(y)); m=255
    for dx in (-2,-1,0,1,2):
        for dy in (-2,-1,0,1,2): m=min(m,px[x+dx,y+dy])
    return m
bg=200
res={}
for D in d['DOORS']:
    a=(X(D['a'][0]),Y(D['a'][1])); b=(X(D['b'][0]),Y(D['b'][1])); w=math.dist(a,b)
    vert=abs(a[0]-b[0])<abs(a[1]-b[1]); out=[]
    for hn,h,o in (('a',a,b),('b',b,a)):
        ang0=math.atan2(o[1]-h[1],o[0]-h[0])
        for side in (1,-1):
            hits=0;n=0
            for t in range(12,79,3):
                ang=ang0+side*math.radians(t); x=h[0]+w*math.cos(ang); y=h[1]+w*math.sin(ang); n+=1
                if dark(x,y)<185: hits+=1
            out.append((round(hits/n,2),hn,side))
    out.sort(reverse=True); res[D['id']]=out[:2]
    print(D['id'],'w_px',round(w),out[:3])
# contrast crops of faint arcs
for n,(x0,y0,x1,y1) in {'D8_D12':(2400,13400,4900,17300),'D10_D11':(7700,13900,10700,17300)}.items():
    c=P.crop((int(X(x0)),int(Y(y0)),int(X(x1)),int(Y(y1)))).convert('L')
    c=c.point(lambda v: 0 if v<150 else (60 if v<205 else 255))
    c=c.resize((c.width*3,c.height*3)); c.save(f'arcs_{n}_contrast.png'); print(n,c.size)
