"""Caption the step-4 grime close-ups (the pipeline lists step4_grime/closeups/ as a captioned output).
usage: python caption_closeups.py <raw_closeups_dir> <out_dir>"""
import sys, os, json
from PIL import Image, ImageDraw, ImageFont
def LP(p):
    """Absolute path; on Windows add the \\\\?\\ long-path prefix (deep repo paths exceed the 260-char limit)."""
    p = os.path.abspath(p)
    if os.name == 'nt' and not p.startswith('\\\\?\\'): p = '\\\\?\\' + p
    return p
raw, out = LP(sys.argv[1]), LP(sys.argv[2])
os.makedirs(out, exist_ok=True)
HERE = LP(os.path.dirname(os.path.abspath(__file__)))
views = json.load(open(os.path.join(HERE, 'views_closeups.json')))
def _font(*c):
    for p in c:
        if os.path.exists(p): return p
    return c[-1]
FB = _font('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 'C:/Windows/Fonts/arialbd.ttf')
FR = _font('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'C:/Windows/Fonts/arial.ttf')
CAP = 'Concept visualisation: not survey-verified, not construction-ready, not certified'
SHOWS = {
    'cu_plinth_base_dirt': 'base dirt / splash-back above deck level; hand smudges on glass at 0.8-1.7 m',
    'cu_slab_drips': 'rain streaks running down from the FF slab edge onto the stone pier; edge chips on slab fascia',
    'cu_gate_patina': 'bronze patina (duller/browner low down, varies bar to bar); base dirt on wall',
    'cu_carport_pier': 'edge chips on stone pier and canopy fascia; dust on up-facing surfaces',
}
n = 0
for v in views:
    p = os.path.join(raw, v['file'])
    if not os.path.exists(p): print('MISSING', p); continue
    im = Image.open(p).convert('RGB'); W, Hh = im.size; bar = 54
    o = Image.new('RGB', (W, Hh + bar), (24, 22, 20)); o.paste(im, (0, 0)); d = ImageDraw.Draw(o)
    d.text((12, Hh + 6), CAP, fill=(255, 214, 140), font=ImageFont.truetype(FB, 17))
    d.text((12, Hh + 30), f'Ashwood 4B, step 4 grime close-up | {v["name"]} | shows: {SHOWS.get(v["name"], "grime detail")}',
           fill=(210, 210, 205), font=ImageFont.truetype(FR, 14))
    o.save(os.path.join(out, v['file'])); n += 1
print('captioned', n)
