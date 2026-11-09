"""web3d viewer screenshot | Cycles render (step3_blockout/renders_raw) | approved image -> web3d/verify/sbs_<round>_<view>.jpg
usage: python side_by_side.py <round-tag>"""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); W3 = os.path.join(HERE, '..')
RAW = r'C:/Users/Alfa/.venvs/aw4b/step3_blockout/renders_raw'
APP = r'C:/Users/Alfa/.venvs/awroot/generated-exteriors/ashwood-estates/4b'
VIEWS = [('elev_front', 'elevation_front.png', 'EXT-4b-ELEV-FRONT_GENERATED-SOURCE-CONDITIONED.png'),
         ('garden_pool', 'preview_03_garden_pool_side.png', 'EXT-4b-ELEV-REAR_GENERATED-SOURCE-CONDITIONED.png'),
         ('front_approach', 'preview_02_front_approach.png', 'EXT-4b-GARDEN-FRONT_GENERATED-SOURCE-CONDITIONED.png'),
         ('back_garden', 'view_back_garden.png', 'EXT-4b-GARDEN-BACK_GENERATED-SOURCE-CONDITIONED.png'),
         ('pool', 'view_swimming_pool.png', 'EXT-4b-POOL_GENERATED-SOURCE-CONDITIONED.png'),
         ('aerial', 'preview_01_aerial.png', 'EXT-4b-OUTDOOR-SITE_GENERATED-SOURCE-CONDITIONED.png')]
tag = sys.argv[1] if len(sys.argv) > 1 else 'r1'
try: F = ImageFont.truetype('arial.ttf', 18)
except Exception: F = ImageFont.load_default()
pw, ph = 800, 450
for v, r, a in VIEWS:
    shot = os.path.join(W3, 'verify', 'shots', f'{tag}_{v}.png')
    if not os.path.exists(shot): print('missing', shot); continue
    out = Image.new('RGB', (pw * 3, ph + 30), (20, 22, 26)); d = ImageDraw.Draw(out)
    for i, (p, lab) in enumerate([(shot, f'web3d viewer ({tag}) - {v}'), (os.path.join(RAW, r), f'Cycles render - {r}'), (os.path.join(APP, a), f'approved - {a[:24]}')]):
        im = Image.open(p).convert('RGB'); im = im.resize((pw, int(im.height * pw / im.width))).crop((0, 0, pw, ph))
        out.paste(im, (i * pw, 30)); d.text((i * pw + 8, 6), lab, fill=(235, 235, 235), font=F)
    fn = os.path.join(W3, 'verify', f'sbs_{tag}_{v}.jpg'); out.save(fn, quality=88); print(fn)
