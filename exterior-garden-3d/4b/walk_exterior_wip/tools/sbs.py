"""side-by-side: python3 sbs.py <model.png> <reference.png> <out.png> <left-caption> [rows px at 960x540, comma]"""
import sys
from PIL import Image, ImageDraw
a, r, o, cap = sys.argv[1:5]; rows = [int(v) for v in sys.argv[5].split(',')] if len(sys.argv) > 5 and sys.argv[5] else []
W, H = 960, 540; A = Image.open(a).convert('RGB').resize((W, H)); R = Image.open(r).convert('RGB').resize((W, H))
out = Image.new('RGB', (W * 2 + 20, H + 28), (255, 255, 255)); d = ImageDraw.Draw(out)
out.paste(A, (0, 28)); out.paste(R, (W + 20, 28))
d.text((6, 8), 'LEFT: ' + cap, fill=(0, 0, 0)); d.text((W + 26, 8), 'RIGHT: approved generated reference (' + r.split('/')[-1] + ')', fill=(0, 0, 0))
for y in rows:
    for x0 in (0, W + 20): d.line([(x0, 28 + y), (x0 + W, 28 + y)], fill=(220, 0, 0), width=1)
out.save(o); print(o)
