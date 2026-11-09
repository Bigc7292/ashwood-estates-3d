"""Caption Blender renders + build per-view side-by-side vs the matching APPROVED generated image.
usage: python3 caption_compare.py <raw_dir> <out_renders_dir> <out_compare_dir> <stage_label>"""
import sys, json, os, glob
from PIL import Image, ImageDraw, ImageFont
raw, outr, outc, label = sys.argv[1:5]
os.makedirs(outr, exist_ok=True); os.makedirs(outc, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
views = json.load(open(os.path.join(HERE, 'views_blender.json')))
GEN = os.path.join(HERE, '..', 'step1_reference', 'generated_approved')
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
CAP = 'Concept visualisation: not survey-verified, not construction-ready, not certified'
labels = {}
lj = os.path.join(raw, '_labels.json')
if os.path.exists(lj): labels = json.load(open(lj))
def capbar(im, line2):
    W, Hh = im.size; bar = 54
    out = Image.new('RGB', (W, Hh + bar), (24, 22, 20)); out.paste(im, (0, 0)); d = ImageDraw.Draw(out)
    d.text((12, Hh + 6), CAP, fill=(255, 214, 140), font=ImageFont.truetype(FB, 17))
    d.text((12, Hh + 30), line2, fill=(210, 210, 205), font=ImageFont.truetype(FR, 14))
    return out
for v in views:
    p = os.path.join(raw, v['file'])
    if not os.path.exists(p): print('MISSING', p); continue
    im = Image.open(p).convert('RGB')
    if v.get('labels') and labels.get(v['file']):
        d = ImageDraw.Draw(im); f = ImageFont.truetype(FB, 15)
        for t, (u, w) in labels[v['file']].items():
            x, y = int(u * im.width), int((1 - w) * im.height); tw = d.textlength(t, font=f)
            d.line((x, y, x + 6, y - 14), fill=(255, 255, 255), width=2); y -= 30
            d.rectangle((x - 3, y - 3, x + tw + 3, y + 18), fill=(255, 255, 255)); d.text((x, y), t, fill=(30, 30, 30), font=f)
    ref = glob.glob(os.path.join(GEN, v['ref'] + '_*.png'))[0]
    line2 = f'Generated Blender model (Ashwood 4B, {label}) | view: {v["name"]} | matching ref: {os.path.basename(ref)}'
    cim = capbar(im, line2); cim.save(os.path.join(outr, v['file']))
    r = Image.open(ref).convert('RGB').resize(im.size)
    rc = capbar(r, f'APPROVED GENERATED reference (image generator, approved by Colin): {os.path.basename(ref)}')
    W, Hh = cim.size; S = Image.new('RGB', (W * 2 + 16, Hh + 44), (245, 243, 238)); S.paste(rc, (0, 44)); S.paste(cim, (W + 16, 44))
    d = ImageDraw.Draw(S); f = ImageFont.truetype(FB, 20)
    d.text((12, 10), 'LEFT: approved generated image (appearance guide)', fill=(20, 90, 40), font=f)
    d.text((W + 28, 10), f'RIGHT: Blender model, {label} (CAD footprint, image appearance)', fill=(110, 60, 20), font=f)
    S.save(os.path.join(outc, 'compare_' + v['file']))
print('done', len(views))
