#!/usr/bin/env python3
"""Step 6 critique pack: eye-level side-by-sides (V4 GF plan crop | r3 render | brochure reference) + F2 / Q7 before-after.
Inputs: verify/r3_2026-11-10/{before,after}/*.png from build_r3/capture_r3.cjs. Outputs: verify/r3_2026-11-10/sbs/*.jpg.
Plan crop transform copied from scripts/verify_floorplan3d_spike.py (V4 source_space translate(-5,76) scale(1.1963)).
Concept visualisation, not survey-verified, not construction-ready, not certified CAD. Pillow only.
"""
import json, os, re, math
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); GF = os.path.dirname(HERE); R = os.path.abspath(os.path.join(GF, '../../..'))
V = os.path.join(GF, 'verify/r3_2026-11-10'); OUT = os.path.join(V, 'sbs'); os.makedirs(OUT, exist_ok=True)
src = open(os.path.join(GF, 'data/fp-4b-gf.plan.js'), encoding='utf-8').read()
P = json.loads(src[src.index('{', src.index('const PLAN')):src.rindex('}') + 1])
k, (ox, oy) = P['mm_per_crop_px'], P['origin_crop_px']
V4 = Image.open(os.path.join(R, 'active/approved-cad-v4/png/FP-4B-GF_V4_long7680.png')).convert('RGB')
sc, f = V4.width / 1000.0, 1.1963006295231644
def v4px(x, y): cx, cy = x / k + ox, y / k + oy; return ((-5 + cx * f) * sc, (76 + cy * f) * sc)
FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
fnt = lambda s: ImageFont.truetype(FN, s) if os.path.exists(FN) else ImageFont.load_default()
F18, F14, F12 = fnt(18), fnt(14), fnt(12)
LBL = 'Concept visualisation - not survey-verified - not construction-ready - not certified CAD'
REF = {k_: os.path.join(R, v) for k_, v in {
  'p15-living': 'canonical/references/ref-p15-living.png', 'p15-dressing': 'canonical/references/ref-p15-dressing.png',
  'p16-bedroom': 'canonical/references/ref-p16-bedroom.png', 'p17': 'extracts/pages/page110-17.png', 'p24': 'extracts/pages/page110-24.png',
  'p15': 'extracts/pages/page110-15.png', 'p16': 'extracts/pages/page110-16.png',
  'court': 'exterior-garden-3d/4b/step1_reference/generated_approved/EXT-4b-OUTDOOR-COURTYARD_GENERATED-CONCEPT.png'}.items()}
# room -> (chosen camera(s), reference key, why). Reference = style only (images decide look; CAD decides layout).
ROOMS = {
 'living-dining': (['', '_rev'], 'p15-living', 'p15 living render (style: Calacatta media wall, light floor)'),
 'show-kitchen': ([''], 'p15-living', 'no kitchen render in p15-17; p15 living style + p17 board'),
 'kitchen': (['_rev'], 'p15-living', 'no kitchen render; p17 board (Recon Veneer joinery, Calacatta)'),
 'pantry': (['_rev'], 'p17', 'no render; p17 board only'),
 'k-store': (['_rev'], 'p17', 'no render; p17 board only'),
 'powder': (['_rev'], 'p24', 'no render; p24 wet areas: Terrazzo Porcelain / Porcelain Concrete Look'),
 'laundry': ([''], 'p24', 'no render; p24 wet areas'),
 'dress': (['_rev'], 'p15-dressing', 'p15 dressing render (glass-front wardrobes, island)'),
 'maid-room': ([''], 'p16-bedroom', 'p16 bedroom render (only bedroom image; maid room style = interpretation)'),
 'maid-bath': (['_rev'], 'p24', 'no render; p24 wet areas'),
 'double-height-entry': ([''], 'p17', 'p17 board: Travertine Stone Feature Material (F2 wall)'),
 'office-gym': ([''], 'p15-living', 'no office render; p15 living style'),
 'bath': ([''], 'p24', 'no render; p24 wet areas'),
 'multipurpose': (['_rev'], 'p15-living', 'no render; p15 living style'),
 'lift': (['_rev'], 'p17', 'no lift finish evidence (NOT FOUND); p17 board'),
 'outdoor-terrace': ([''], 'court', 'approved generated concept EXT-4b-OUTDOOR-COURTYARD (Q7 style)'),
}
meta = json.load(open(os.path.join(V, 'after/capture_meta.json'))); SH = {s['id']: s for s in meta['shots']}
room = {r['id']: r for r in P['ROOMS']}
def fit(im, h): return im.resize((max(1, round(im.width * h / im.height)), h), Image.LANCZOS)
def plan_crop(poly, cam, h=520):
    xs, ys = [p[0] for p in poly] + [cam['p'][0]], [p[1] for p in poly] + [cam['p'][1]]; m = 1500
    a, b = v4px(min(xs) - m, min(ys) - m), v4px(max(xs) + m, max(ys) + m)
    a = (max(0, a[0]), max(0, a[1])); b = (min(V4.width, b[0]), min(V4.height, b[1]))
    im = V4.crop((int(a[0]), int(a[1]), int(b[0]), int(b[1]))).copy(); d = ImageDraw.Draw(im); s = im.height / h
    pt = lambda x, y: (v4px(x, y)[0] - a[0], v4px(x, y)[1] - a[1])
    d.line([pt(*p) for p in poly] + [pt(*poly[0])], fill=(220, 30, 30), width=max(2, int(4 * s)))
    cx, cy = pt(cam['p'][0], cam['p'][1]); tx, ty = pt(cam['t'][0], cam['t'][1]); r = 10 * s
    ang = math.atan2(ty - cy, tx - cx); hf = math.radians(cam['fov'] * 1280 / 800 / 2) * .8; L = 60 * s
    d.polygon([(cx, cy), (cx + L * math.cos(ang - hf), cy + L * math.sin(ang - hf)), (cx + L * math.cos(ang + hf), cy + L * math.sin(ang + hf))], outline=(20, 90, 200), width=max(2, int(3 * s)))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(20, 90, 200))
    return fit(im, h)
def p24_crop(): return Image.open(REF['p24']).convert('RGB').crop((1780, 1255, 2750, 1480))
def sheet(name, title, panels, notes, ref_strip=True):
    H = 520; ims = [(cap, fit(im, H)) for cap, im in panels]; W = sum(i.width for _, i in ims) + 20 * (len(ims) + 1)
    strip = []
    if ref_strip: strip = [('brochure p17 materials board', fit(Image.open(REF['p17']).convert('RGB'), 150)), ('brochure p24 Interior (Summary)', fit(p24_crop(), 150))]
    SHh = 190 if strip else 0; NH = 22 * len(notes) + 20
    W = max(W, sum(i.width for _, i in strip) + 60)
    c = Image.new('RGB', (W, 70 + H + 30 + SHh + NH), 'white'); d = ImageDraw.Draw(c)
    d.text((20, 10), title, fill='black', font=F18); d.text((20, 38), LBL, fill=(150, 60, 30), font=F14)
    x = 20
    for cap, im in ims: c.paste(im, (x, 70)); d.text((x, 70 + H + 6), cap, fill='black', font=F12); x += im.width + 20
    y = 70 + H + 30; x = 20
    for cap, im in strip: c.paste(im, (x, y)); d.text((x, y + 154), cap, fill='black', font=F12); x += im.width + 20
    y += SHh
    for n in notes: d.text((20, y), n, fill=(40, 40, 40), font=F14); y += 22
    p = os.path.join(OUT, name + '.jpg'); c.save(p, quality=86); return os.path.relpath(p, R)
made = []
for rid, (cams, ref, why) in ROOMS.items():
    r = room[rid]
    for sfx in cams:
        sid = 'room_' + rid + sfx; s = SH[sid]
        rend = Image.open(os.path.join(V, 'after', sid + '.png')).convert('RGB')
        refim = Image.open(REF[ref]).convert('RGB')
        if ref == 'p24': refim = p24_crop()
        notes = [f"Room: {r.get('label', rid)} (plan id {rid}). Layout/dimensions: approved V4 FP-4B-GF via ACTIVE_PIPELINE.json [source]; room polygon [derived, README].",
                 f"Camera (plan mm, height m): {s['p']} -> {s['t']}, fov {s['fov']} deg [assumption: QA camera]. Eye height 1.6 m [source: PLAN.DISPLAY.walk_eye_height_m, display value].",
                 f"Reference: {why}. Wall height 3.0 m [display assumption]. Finishes: README 'Floor material evidence' (project-wide, interpretation).",
                 "Red = room polygon on the approved V4 plan; blue = camera position and view cone."]
        made.append(sad := sheet('sbs_' + rid + sfx, f'FP-4B-GF step 6 side-by-side: {r.get("label", rid)} (eye level, r3 build)',
              [('Approved V4 GF plan (crop, unaltered artwork + overlay)', plan_crop(r['poly'], s)), ('r3 viewer render, eye level', rend), (f'Brochure / approved reference: {ref}', refim)], notes))
# F2 before / after (same cameras)
for sid in ['f2_entry_wall_oblique', 'f2_entry_void_up', 'room_double-height-entry']:
    s = SH[sid]; b, a = [Image.open(os.path.join(V, w, sid + '.png')).convert('RGB') for w in ('before', 'after')]
    made.append(sheet('f2_before_after_' + sid, 'F2 entry travertine wall: before (index.html) vs after (index_r3.html), same camera',
        [('Approved V4 GF plan (entry)', plan_crop(room['double-height-entry']['poly'], s)), ('BEFORE: index.html texTravertine (streak)', b), ('AFTER: f2_entry_travertine.js', a)],
        [f"Camera {s['p']} -> {s['t']} fov {s['fov']} [assumption]. Wall plan x 6040, y 16113-19169 [source: V4 trace]; clad 20 mm, 0.09 m to wall top / 6.0 m void lining [assumption, Q4 note].",
         "Texture: slab 1.2 x 0.6 m [assumption, as before], stretcher bond [assumption], tone from p17 travertine swatch [source image, read by eye]. Dining wall travertine unchanged (Q4 PASS)."]))
# Q7 courtyard: before / after / concept
for sid in ['q7_courtyard_from_living', 'q7_courtyard_from_south', 'q7_courtyard_from_entry_side', 'room_outdoor-terrace']:
    s = SH[sid]; b, a = [Image.open(os.path.join(V, w, sid + '.png')).convert('RGB') for w in ('before', 'after')]
    made.append(sheet('q7_courtyard_' + sid, 'Q7 courtyard: before (interim olive + lite pond) vs after (courtyard_feature_r2.js, Water2) vs approved concept',
        [('Approved V4 GF plan (courtyard)', plan_crop(room['outdoor-terrace']['poly'], s)), ('BEFORE: index.html', b), ('AFTER: index_r3.html', a), ('Approved concept (style only)', Image.open(REF['court']).convert('RGB'))],
        [f"Camera {s['p']} -> {s['t']} fov {s['fov']} [assumption]. Pond 10019-14177 x 8723-12418 mm, island 11228-12649 x 9860-11281 mm [source: V4 trace, PLAN.WATER].",
         "Pond depth 0.35 m, water line -0.045 m, coping top +0.25 m, tree ~2.5 m, crown ~3.3 m [assumption DA1-DA6]. Water: vendored three.js r160 Water2 [source: vendor/].",
         "Bench 2.00 x 0.38 x 0.40 m at plan (9775, 9153) [ASSUMPTION: concept image only, not on V4 plan]. Brochure p12 text/README says olive tree; concept shows pine: open conflict."], ref_strip=False))
# brochure reference board (p15, p16, p17, p24 full pages)
pages = [(f'brochure p{n}', Image.open(REF[f'p{n}']).convert('RGB')) for n in (15, 16, 17)] + [('brochure p24', Image.open(REF['p24']).convert('RGB'))]
made.append(sheet('ref_board_p15_p16_p17_p24', 'Reference board: brochure p15, p16, p17, p24 (style/material sources for step 6)', [(c_, fit(i, 300)) for c_, i in pages], ['Brochure pages from extracts/pages/page110-NN.png (provenance copies of the brochure; style only).'], ref_strip=False))
print('\n'.join(made)); print(len(made), 'sheets')
