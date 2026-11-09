"""WIP side-by-sides (same format as blender/caption_compare.py): approved reference LEFT, WIP render RIGHT.
usage: python compare_wip.py <raw_dir> <out_dir> <label> [name=refpath ...]
Default ref per view from views_wip.json 'ref' (approved images in the repo's generated-exteriors/ashwood-estates/4b);
override with name=path (e.g. garden_pool=C:/.../page110-26.png for the brochure render)."""
import sys, json, os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
raw, outc, label = sys.argv[1:4]
over = dict(a.split('=', 1) for a in sys.argv[4:])
os.makedirs(outc, exist_ok=True)
views = json.load(open(os.path.join(HERE, 'views_wip.json')))
GEN = os.path.join(HERE, '..', '..', '..', 'generated-exteriors', 'ashwood-estates', '4b')
if not os.path.isdir(GEN): GEN = r'C:\Users\Alfa\.venvs\awroot\generated-exteriors\ashwood-estates\4b'
def find_ref(prefix):
    hits = sorted(f for f in os.listdir(GEN) if f.startswith(prefix + '_') and f.endswith('.png'))
    return os.path.join(GEN, hits[0]) if hits else None
FB = next(f for f in ('C:/Windows/Fonts/DejaVuSans-Bold.ttf', 'C:/Windows/Fonts/arialbd.ttf') if os.path.exists(f))
FR = next(f for f in ('C:/Windows/Fonts/DejaVuSans.ttf', 'C:/Windows/Fonts/arial.ttf') if os.path.exists(f))
CAP = 'Concept visualisation: not survey-verified, not construction-ready, not certified'
def capbar(im, line2):
    W, Hh = im.size; bar = 46
    out = Image.new('RGB', (W, Hh + bar), (24, 22, 20)); out.paste(im, (0, 0)); d = ImageDraw.Draw(out)
    d.text((10, Hh + 5), CAP, fill=(255, 214, 140), font=ImageFont.truetype(FB, 13))
    d.text((10, Hh + 25), line2, fill=(210, 210, 205), font=ImageFont.truetype(FR, 11))
    return out
n = 0
for v in views:
    p = os.path.join(raw, v['file'])
    if not os.path.exists(p): continue
    im = Image.open(p).convert('RGB')
    ref = over.get(v['name']) or find_ref(v['ref'])
    cim = capbar(im, f'Blender model (Ashwood 4B, {label}) | view: {v["name"]}')
    r = Image.open(ref).convert('RGB')
    r = r.resize((im.width, int(im.width * r.height / r.width)))
    if r.height != im.height:   # letterbox / crop to the render height
        c = Image.new('RGB', im.size, (245, 243, 238)); c.paste(r, (0, (im.height - r.height) // 2)); r = c
    rc = capbar(r, f'APPROVED reference (appearance guide): {os.path.basename(ref)}')
    W, Hh = cim.size; S = Image.new('RGB', (W * 2 + 12, Hh + 34), (245, 243, 238)); S.paste(rc, (0, 34)); S.paste(cim, (W + 12, 34))
    d = ImageDraw.Draw(S); f = ImageFont.truetype(FB, 15)
    d.text((10, 8), 'LEFT: approved reference (appearance guide)', fill=(20, 90, 40), font=f)
    d.text((W + 22, 8), f'RIGHT: Blender model, {label} (CAD footprint, image appearance)', fill=(110, 60, 20), font=f)
    S.save(os.path.join(outc, 'compare_' + v['file'])); n += 1
print('compared', n)
