from PIL import Image, ImageDraw, ImageFont
import json
Image.MAX_IMAGE_PIXELS=None
P=Image.open('/workspace/critic-wt-first-floor/active/approved-cad-v4/png/FP-4B-FF_V4_long7680.png').convert('RGBA')
d=json.load(open('/workspace/critic-wt-first-floor/active/floorplan3d-spike/FP-4B-FF/data/fp-4b-ff.plan.r6.json'))
k=0.18307; X=lambda x:1278.9+x*k; Y=lambda y:1334.5+y*k
ov=Image.new('RGBA',P.size,(0,0,0,0)); g=ImageDraw.Draw(ov)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',30)
R=lambda r,**kw: g.rectangle([X(min(r[0],r[2])),Y(min(r[1],r[3])),X(max(r[0],r[2])),Y(max(r[1],r[3]))],**kw)
for w in d['WALLS']: R(w[:4],fill=(255,0,0,70))
for v in d['VOIDS']: R(v['rect'],outline=(0,200,220,255),width=5)
for s in d['STAIRS']: R(s['rect'],outline=(0,0,255,255),width=6)
for fu in d['FURNITURE']:
    if 'rect' in fu: R(fu['rect'],outline=(140,0,200,255),width=4)
    else:
        cx,cy=X(fu['center'][0]),Y(fu['center'][1]); r=fu['radius_mm']*k; g.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(140,0,200,255),width=4)
for r in d['ROOMS']: g.polygon([(X(p[0]),Y(p[1])) for p in r['poly']],outline=(255,140,0,255),width=5)
for c in d['CLOSURES']: g.line([X(c['a'][0]),Y(c['a'][1]),X(c['b'][0]),Y(c['b'][1])],fill=(255,200,0,255),width=6)
for o,c in [(d['DOORS'],(0,170,0,255)),(d['WINS'],(0,120,255,255)),(d['OPENINGS_OTHER'],(255,0,160,255))]:
    for e in o:
        g.line([X(e['a'][0]),Y(e['a'][1]),X(e['b'][0]),Y(e['b'][1])],fill=c,width=9); g.text((X(e['a'][0])+6,Y(e['a'][1])+6),e['id'].split('-')[0],fill=c,font=f)
        h=(e.get('swing') or {}).get('hinge_mm')
        if h: x,y=X(h[0]),Y(h[1]); g.ellipse([x-12,y-12,x+12,y+12],fill=(0,90,0,255))
for a in d['ANCHORS']:
    x,y=X(a['at'][0]),Y(a['at'][1]); g.ellipse([x-12,y-12,x+12,y+12],fill=(255,0,255,255))
out=Image.alpha_composite(P,ov).convert('RGB'); out.save('r6_overlay_long.png')
out.crop((1150,1250,3800,3700)).save('r6_overlay_north.png')
out.crop((1150,3500,3800,5900)).save('r6_overlay_south.png')
out.crop((1000,1000,4000,6000)).resize((900,1500)).save('r6_overlay_full.png')
def area(p): return abs(sum(p[i][0]*p[(i+1)%len(p)][1]-p[(i+1)%len(p)][0]*p[i][1] for i in range(len(p))))/2e6
for r in d['ROOMS']: print(r['id'], round(area(r['poly']),2), r['area_m2_traced'], r['stated_area_m2'], r['dims_label'], r['poly'] if r['id'] in ('bath-1','lift') else '')
print('done')
