import json
from PIL import Image, ImageDraw
import numpy as np
S=4.0; OXU,OYU=148.0,164.5; MM=35.53012869683798
d=json.load(open('/home/user/ashwood-estates-3d/active/floorplan3d-spike/FP-4B-GF/data/fp-4b-gf.plan.json'))
W=d['plan']['WALLS']
def tp(x,y): return (S*(OXU+x/MM), S*(OYU+y/MM))
src=Image.open('sheet4x.png').convert('RGB')
g=np.asarray(src.convert('L')).astype(float)
ov=src.copy(); dr=ImageDraw.Draw(ov)
for w in W:
    x0,y0,x1,y1=w[:4]
    dr.rectangle([tp(x0,y0),tp(x1,y1)],outline=(255,0,0),width=2)
# crop to building extent
xs=[tp(0,0)[0],tp(14550,23006)[0]]; ys=[tp(0,0)[1],tp(14550,23006)[1]]
box=(int(min(xs))-150,int(min(ys))-150,int(max(xs))+150,int(max(ys))+150)
ov.crop(box).save('overlay_gf_walls_crop.png')
print('box',box, 'walls',len(W))
