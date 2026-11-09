"""python3 water_diff.py <prefix> x0 y0 x1 y1  -> pool-box mean/max |t5-t6| and |t6-hidden|, pool std (1280x720 frames)"""
import sys; from PIL import Image, ImageChops, ImageStat
pre=sys.argv[1]; box=tuple(int(v) for v in sys.argv[2:6]); L=lambda s: Image.open(f'{pre}_{s}.png').convert('RGB').crop(box)
a,b,h=L('t5'),L('t6'),L('t6_hidden')
for nm,(p,q) in {'t5_vs_t6':(a,b),'water_vs_hidden':(b,h)}.items():
    d=ImageChops.difference(p,q).convert('L'); st=ImageStat.Stat(d); print(nm,'mean',round(st.mean[0],2),'max',d.getextrema()[1])
print('pool box RGB mean',[round(v,1) for v in ImageStat.Stat(b).mean],'std',[round(v,1) for v in ImageStat.Stat(b).stddev])
