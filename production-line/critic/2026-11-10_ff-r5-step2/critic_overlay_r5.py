from PIL import Image, ImageDraw, ImageFont
import json
P=Image.open('/workspace/critic-wt-first-floor/active/approved-cad-v4/png/FP-4B-FF_V4_long7680.png').convert('RGBA')
d=json.load(open('/workspace/critic-wt-first-floor/active/floorplan3d-spike/FP-4B-FF/data/fp-4b-ff.plan.r5.json'))
k=0.18307; X=lambda x:1278.9+x*k; Y=lambda y:1334.5+y*k
ov=Image.new('RGBA',P.size,(0,0,0,0)); g=ImageDraw.Draw(ov)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',46)
R=lambda r,**kw: g.rectangle([X(r[0]),Y(r[1]),X(r[2]),Y(r[3])],**kw)
for w in d['WALLS']: R([min(w[0],w[2]),min(w[1],w[3]),max(w[0],w[2]),max(w[1],w[3])],fill=(255,0,0,90))
for v in d['VOIDS']: R(v['rect'],outline=(0,200,220,255),width=8)
for s in d['STAIRS']: R(s['rect'],outline=(0,0,255,255),width=10)
for fu in d['FURNITURE']:
    r=fu.get('rect'); 
    if r: R(r,outline=(140,0,200,255),width=8)
for o,c in [(d['DOORS'],(0,170,0,255)),(d['WINS'],(0,120,255,255))]:
    for e in o: g.line([X(e['a'][0]),Y(e['a'][1]),X(e['b'][0]),Y(e['b'][1])],fill=c,width=16); g.text((X(e['a'][0])+10,Y(e['a'][1])+10),e['id'].split('-')[0],fill=c,font=f)
for a in d['ANCHORS']:
    x,y=X(a['at'][0]),Y(a['at'][1]); g.ellipse([x-22,y-22,x+22,y+22],fill=(255,0,255,255))
for r in d['ROOMS']: g.polygon([(X(p[0]),Y(p[1])) for p in r['poly']],outline=(255,140,0,255),width=8)
out=Image.alpha_composite(P,ov).convert('RGB')
out.crop((1000,1000,4000,6000)).resize((600,1000)).save('r5_overlay_full.png')
out.crop((1150,1250,3800,3700)).resize((1060,980)).save('r5_overlay_north.png')
out.crop((1150,3500,3800,5900)).resize((1060,960)).save('r5_overlay_south.png')
out.save('/tmp/r5_overlay_long.jpg',quality=85)
