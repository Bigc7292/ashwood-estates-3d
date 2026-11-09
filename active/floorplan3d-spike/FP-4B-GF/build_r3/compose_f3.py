#!/usr/bin/env python3
"""F3 sheets: courtyard olive (V4 crop | r3 before (pine+bench) | F3 after (olive) | brochure p12 + p18 olive crops) and
pool Water2 (index.html lite before | F3 Water2 | same camera +3 s | |difference| x4 = flow evidence | brochure p12 pool).
Concept visualisation, not survey-verified, not construction-ready, not certified CAD. Pillow only."""
import json, os, sys
from PIL import Image, ImageChops, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
src = open(os.path.join(HERE, 'compose_sbs.py')).read(); cut = src.index('made = []')
ns = {'__file__': os.path.join(HERE, 'compose_sbs.py')}; exec(src[:cut], ns)
GF, R = ns['GF'], ns['R']; sheet, plan_crop, room = ns['sheet'], ns['plan_crop'], ns['room']
V3 = os.path.join(GF, 'verify/r3_2026-11-10'); VF = os.path.join(GF, 'verify/f3_2026-11-10'); ns['OUT'] = os.path.join(VF, 'sbs'); os.makedirs(ns['OUT'], exist_ok=True)
meta = json.load(open(os.path.join(VF, 'after/capture_meta.json'))); SH = {s['id']: s for s in meta['shots']}
pg = lambda n: Image.open(os.path.join(R, f'extracts/pages/page110-{n}.png')).convert('RGB')
p12o, p18o, p12pool = pg(12).crop((1950, 0, 2934, 1150)), pg(18).crop((2200, 250, 2934, 1100)), pg(12).crop((1650, 900, 2934, 1650))
img = lambda d, n: Image.open(os.path.join(d, n + '.png')).convert('RGB')
def ms(s): b, m = s.get('bench_still', {}), s.get('bench_moving', {}); return f"still {b.get('msPerFrame')} ms / moving {m.get('msPerFrame')} ms"
made = []
for sid in ['q7_courtyard_from_living', 'q7_courtyard_from_south', 'q7_courtyard_from_entry_side', 'room_outdoor-terrace']:
    s = SH[sid]
    made.append(sheet('f3_courtyard_' + sid, 'F3 courtyard: r3 (pine + bench) vs F3 (brochure olive, no bench, Water2 1024) vs brochure p12 / p18 olive',
        [('Approved V4 GF plan (courtyard)', plan_crop(room['outdoor-terrace']['poly'], s)), ('BEFORE: r3 (concept pine + bench)', img(os.path.join(V3, 'after'), sid)),
         ('AFTER: F3 olive (f3_olive_tree.js)', img(os.path.join(VF, 'after'), sid)), ('Brochure p12 (olive, crop)', p12o), ('Brochure p18 (olive, crop)', p18o)],
        [f"Camera {s['p']} -> {s['t']} fov {s['fov']} [assumption]. Pond/island from the V4 trace [source]. Tree at island centre [derived: V4 tree symbol].",
         "Olive form/canopy from brochure p12 + p18 [source images, read by eye]; height ~5.0 m, crown ~4.6 m, trunk ~0.46 m, split ~1.1 m [assumption, derived by eye using the glazing as a ruler].",
         f"Bench dropped (MISMATCH_LOG GF-M2). Water2 1024 px, passes on camera move. SwiftShader ms/frame here: {ms(s)}."], ref_strip=False))
for sid in ['f3_pool_from_terrace_east', 'f3_pool_from_living']:
    s, sb = SH[sid], json.load(open(os.path.join(VF, 'before_index/capture_meta.json')))
    sb = {x['id']: x for x in sb['shots']}[sid]
    a, a3 = img(os.path.join(VF, 'after'), sid), img(os.path.join(VF, 'after'), sid + '_t1s')
    diff = ImageOps.autocontrast(ImageChops.difference(a, a3).convert('L')).convert('RGB')
    made.append(sheet('f3_pool_water2_' + sid, 'F3 pool: index.html lite (before) vs Water2 (after) vs Water2 +1 s, |difference| = flow, brochure p12 pool',
        [('BEFORE: index.html lite water', img(os.path.join(VF, 'before_index'), sid)), ('AFTER: Water2 1024 (reflections)', a), ('AFTER +1 s (same camera)', a3), ('|after - after+1s| autocontrast (flow)', diff), ('Brochure p12 pool (crop)', p12pool)],
        [f"Camera {s['p']} -> {s['t']} fov {s['fov']} [assumption]. Pool outline 1705-11192 x -2754..-373 mm [source: V4 trace]. Reflectivity 0.2, flowSpeed 0.02 [assumption].",
         f"SwiftShader ms/frame: before (lite) {sb.get('bench_still', {}).get('msPerFrame')} ms; after {ms(s)}. Not a GPU / phone number.",
         "Only water pixels change in the difference image (static scene, same camera): flow is running; reflections of the house/sky are in the after frames."], ref_strip=False))
# pixel-diff stats over 1 s (critic method: count px with RGB-sum diff > 12 of 765)
import numpy as np
stats = {}
for sid in ['f3_pool_from_terrace_east', 'f3_pool_from_living', 'q7_courtyard_from_living']:
    a, b = [np.asarray(img(os.path.join(VF, 'after'), n), dtype=int) for n in (sid, sid + '_t1s')]
    dsum = np.abs(a - b).sum(-1); stats[sid] = {'px_changed_gt12': int((dsum > 12).sum()), 'max': int(dsum.max()), 'mean': round(float(dsum.mean()), 3)}
json.dump(stats, open(os.path.join(VF, 'water2_flow_diff_1s.json'), 'w'), indent=1); print(stats)
# G2 Calacatta wall + G4/G5 fixture sheets
p15l = Image.open(os.path.join(R, 'canonical/references/ref-p15-living.png')).convert('RGB'); p15d = Image.open(os.path.join(R, 'canonical/references/ref-p15-dressing.png')).convert('RGB')
p24c = Image.open(os.path.join(R, 'extracts/pages/page110-24.png')).convert('RGB').crop((1780, 1255, 2750, 1480))
for sid in ['g2_living_calacatta_wall', 'g2_living_calacatta_wall_oblique']:
    s = SH[sid]
    made.append(sheet('f3_' + sid, 'F3 G2: living feature wall in Calacatta (ambientCG Marble012, CC0) vs brochure p15 living + p24',
        [('Approved V4 GF plan (living)', plan_crop(room['living-dining']['poly'], s)), ('BEFORE: r3 (procedural marble + oak flanks)', img(os.path.join(V3, 'after'), 'room_living-dining')), ('AFTER: F3 Calacatta wall', img(os.path.join(VF, 'after'), sid)), ('Brochure p15 living', p15l), ('Brochure p24 summary', p24c)],
        [f"Camera {s['p']} -> {s['t']} fov {s['fov']} [assumption]. Wall x 14137-14159, y 1013-5987 [source: V4 trace]. Texture ambientCG Marble012 CC0, levels-brightened (assets/credits.csv); slab 1.6 m [assumption].",
         "Entry and dining walls stay travertine (p12, p17 swatch). Conflict with p24 logged: MISMATCH_LOG.md GF-M3."], ref_strip=False))
for rid in ['powder', 'k-store', 'dress', 'maid-bath', 'bath']:
    a, c = SH['g5_' + rid + '_fixtures'], SH['g5_' + rid + '_cutaway45']
    refs = [('Brochure p15 dressing', p15d)] if rid == 'dress' else [('Brochure p24 summary (wet areas)', p24c)]
    made.append(sheet('f3_g5_' + rid, f"F3 G5: {room[rid].get('label', rid)} fixture check (eye level wide + 1.2 m cutaway) vs V4 plan",
        [('Approved V4 GF plan (crop)', plan_crop(room[rid]['poly'], a)), ('Eye level, wide', img(os.path.join(VF, 'after'), 'g5_' + rid + '_fixtures')), ('Cutaway, walls cut at 1.2 m', img(os.path.join(VF, 'after'), 'g5_' + rid + '_cutaway45'))] + refs,
        [f"Eye camera {a['p']} -> {a['t']} fov {a['fov']}; cutaway {c['p']} -> {c['t']} fov {c['fov']} [assumption: QA cameras].",
         'Fixtures modelled only where PLAN.FURNITURE has a V4 symbol (source plan symbol, size approximate). Unmodelled V4 glyphs: see MISMATCH_LOG.md GF-M5.'], ref_strip=False))
print('\n'.join(made))
