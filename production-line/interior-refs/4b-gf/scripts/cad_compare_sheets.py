"""CAD check: crop the approved V4 FP-4B-GF raster per room (old pass-1 bboxes) and place it beside the pass-1 raw image for visual comparison.
Also writes the per-room plan crops used as GenerateImage references."""
import json,glob,os
from PIL import Image,ImageDraw
P='/workspace/ashwood-estates-3d/active/approved-cad-v4/png/FP-4B-GF_V4_long7680.png'
plan=Image.open(P).convert('RGB')
meta=json.load(open('/workspace/ivg-repo/generated-interiors/ashwood-estates/4b/scripts/crops_meta.json'))
B='/workspace/ivg-repo/generated-interiors/ashwood-estates/4b/gf'
os.makedirs('cmp',exist_ok=True)
for rid,m in meta.items():
    if '/gf/' not in rid: continue
    r=rid.split('/')[-1]
    x0,y0,x1,y1=m['crop_bbox_long7680_px']
    os.makedirs('crops',exist_ok=True); cc=plan.crop((x0-60,y0-60,x1+60,y1+60)); cc.thumbnail((1400,1400)); cc.save(f'crops/4b-gf-{r}_V4-plan-crop.png')
    pad=250
    c=plan.crop((max(0,x0-pad),max(0,y0-pad),min(plan.width,x1+pad),min(plan.height,y1+pad)))
    raw=glob.glob(f'{B}/{r}/view-unassigned-001/_raw_unlabelled/*')[0]
    g=Image.open(raw).convert('RGB')
    H=700
    c=c.resize((int(c.width*H/c.height),H)); g=g.resize((int(g.width*H/g.height),H))
    out=Image.new('RGB',(c.width+g.width+20,H+30),'white')
    out.paste(c,(0,30)); out.paste(g,(c.width+20,30))
    d=ImageDraw.Draw(out); d.text((5,5),r+'  (red box = old crop bbox; pad 250px)',fill='black')
    # draw bbox
    sx=H/(min(plan.height,y1+pad)-max(0,y0-pad))
    d.rectangle(((x0-max(0,x0-pad))*sx,30+(y0-max(0,y0-pad))*sx,(x1-max(0,x0-pad))*sx,30+(y1-max(0,y0-pad))*sx),outline='red',width=3)
    out.save(f'cmp/{r}.png')
    print(r, raw)
