"""FP-4B-FF r6 step 2 (layout) builder. r6: explicit room polygons on measured wall faces + derived closures, door swings from arc scoring (arcs.json), fixtures.
Concept visualisation, not survey-verified, not construction-ready, not certified CAD.

Source: approved V4 plan active/approved-cad-v4/png/FP-4B-FF_V4_long7680.png (render of
active/approved-cad-v4/svg/FP-4B-FF_V4_portrait.svg, ACTIVE_PIPELINE.json id 4B-FF, approval pt16u).
All geometry uses ONE transform: SVG group 'source_diagram' units ("u", = source crop px)
  -> world mm: X = (u - 138) * MM_PER_U, Y = (v - 141) * MM_PER_U   (x east/right, y plan-down)
MM_PER_U = 13100 / 385: SVG envelope dimension line M138,123 L523,123 labelled "ENVELOPE ~ 13.1 m".
Usage: python build_r6_layout.py <repo_root> <out_dir>
Needs numpy, opencv-python-headless, pillow.
"""
import sys, json, math, re, os
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
ROOT, OUT = sys.argv[1], sys.argv[2]
SVG = os.path.join(ROOT, 'active/approved-cad-v4/svg/FP-4B-FF_V4_portrait.svg')
PNG = os.path.join(ROOT, 'active/approved-cad-v4/png/FP-4B-FF_V4_long7680.png')
# --- transforms (SOURCE: SVG) ---
GTX, GTY, GS = 77.20427844624848, 84.0, 1.1469518964165648   # <g id="source_diagram" transform=...>
PX_PER_PAGE = 5431 / 1000.0                                    # long7680 width / SVG viewBox width
ENV_U = (138.0, 141.0, 523.0, 844.0)                           # envelope dim-line extents (SVG paths)
MM_PER_U = 13100.0 / (ENV_U[2] - ENV_U[0])                     # 34.026 mm/u
def u2mm(x, y): return (round((x - ENV_U[0]) * MM_PER_U), round((y - ENV_U[1]) * MM_PER_U))
def u2px(x, y): return ((GTX + GS * x) * PX_PER_PAGE, (GTY + GS * y) * PX_PER_PAGE)
R = 4; U0 = (110.0, 100.0); U1 = (555.0, 870.0)                # working raster: 4 px per u
big = Image.open(PNG).convert('RGB')
x0, y0 = u2px(*U0); x1, y1 = u2px(*U1)
work = big.crop((round(x0), round(y0), round(x1), round(y1))).resize(
    (int((U1[0]-U0[0])*R), int((U1[1]-U0[1])*R)), Image.LANCZOS)
A = np.asarray(work).astype(int); LUM = A.mean(2)
def ui(x, y): return int(round((y-U0[1])*R)), int(round((x-U0[0])*R))
# --- walls: dark poche, opened 7px (removes text/stair/door/glazing hairlines), inside envelope ---
dark = (LUM < 95).astype(np.uint8)
thick = cv2.morphologyEx(dark, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
m = np.zeros_like(thick); a0 = ui(132, 135); a1 = ui(529, 850); m[a0[0]:a1[0], a0[1]:a1[1]] = 1; thick *= m
n, lab, st, _ = cv2.connectedComponentsWithStats(thick, 8)
for i in range(1, n):
    if st[i, 4] < 200: thick[lab == i] = 0
H, W = thick.shape
t2 = thick[:H//2*2, :W//2*2].reshape(H//2, 2, W//2, 2).mean((1, 3)) >= 0.5
t2 = cv2.morphologyEx(t2.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8)).astype(bool)
def decompose(mask, res):
    t = mask.copy(); h, w = t.shape; out = []
    while t.any():
        ys, xs = np.nonzero(t); k = np.lexsort((xs, ys))[0]; y, x = ys[k], xs[k]
        x2 = x
        while x2+1 < w and t[y, x2+1]: x2 += 1
        y2 = y
        while y2+1 < h and t[y2+1, x]: y2 += 1
        ya = y
        while ya+1 < h and t[ya+1, x:x2+1].all(): ya += 1
        xb = x
        while xb+1 < w and t[y:y2+1, xb+1].all(): xb += 1
        r = (x, y, x2, ya) if (x2-x+1)*(ya-y+1) >= (xb-x+1)*(y2-y+1) else (x, y, xb, y2)
        t[r[1]:r[3]+1, r[0]:r[2]+1] = False
        out.append([U0[0]+r[0]/res, U0[1]+r[1]/res, U0[0]+(r[2]+1)/res, U0[1]+(r[3]+1)/res])
    return [q for q in out if (q[2]-q[0])*(q[3]-q[1]) >= 1.0]
walls_u = decompose(t2, 2)
# --- labels from SVG text (SOURCE: SVG label text positions, same group transform) ---
svg = open(SVG, encoding='utf-8').read()
texts = re.findall(r'<text x="([\d.]+)" y="([\d.]+)"[^>]*font-size="([\d.]+)"[^>]*font-weight="bold">([^<]+)</text>\s*<text x="[\d.]+" y="[\d.]+"[^>]*>([^<]+)</text>', svg)
LABELS = []
for x, y, fs, name, dims in texts:
    if float(fs) > 7 or name.startswith('ASHWOOD') or name.startswith('LEGEND'): continue
    LABELS.append({'name': name.strip(), 'dims_label': dims.strip(), 'u': [float(x), float(y) - 2.5]})
# --- openings (MEASURED on the V4 raster at 4 px/u; gap in traced wall + visible swing/glazing) ---
# each: id, type, axis, fixed coordinate (u), span (u), room(s), evidence, confidence
OPEN = json.load(open(os.path.join(os.path.dirname(__file__), 'openings_u.json')))
# --- stair (MEASURED: tread box hairlines, 15 tread lines detected at ~8.8 u pitch) ---
STAIR_U = {'x0': 272.0, 'y0': 401.0, 'x1': 316.5, 'y1': 587.0, 'tread_lines_detected': 15,
           'tread_pitch_u': 8.76, 'break_line_u_y': 540}
# --- voids ---
VOIDS_U = [
    {'id': 'courtyard-void', 'u': [389, 428, 518, 535], 'source': 'SVG <image x=389 y=428 w=129 h=107> "Source water"/courtyard overlay; walls on N/W/S traced'},
    {'id': 'open-to-below-1', 'u': [272, 638, 368, 749], 'source': 'MEASURED: raster X-cross box "OPEN TO BELOW" (+-1 u)'},
    {'id': 'open-to-below-2', 'u': [272, 752, 368, 778], 'source': 'MEASURED: raster X-cross box "OPEN TO BELOW" (+-1.5 u)'},
]
# --- furniture footprints: SVG vector symbols only (SOURCE: SVG rect/circle) + raster-measured tub ---
FURN_U = json.load(open(os.path.join(os.path.dirname(__file__), 'furniture_u.json')))
# --- rooms: explicit polygons on measured wall faces (rooms_u.json) + DERIVED closures (closures_u.json) ---
HERE = os.path.dirname(os.path.abspath(__file__))
RU = json.load(open(os.path.join(HERE, 'rooms_u.json')))
CLOS = json.load(open(os.path.join(HERE, 'closures_u.json')))
OTHER = json.load(open(os.path.join(HERE, 'openings_other_u.json')))
def shoelace(P): return abs(sum(P[i][0]*P[(i+1)%len(P)][1]-P[(i+1)%len(P)][0]*P[i][1] for i in range(len(P))))/2
dims = {L['name'].title(): L['dims_label'] for L in LABELS}
ROOMS = []; ROOMS_ND = []
for r in RU:
    dl = dims[r['name'].title()] if r['name'].title() in dims else dims.get(r['name'].upper().title())
    nums = [float(q) for q in re.findall(r'[\d.]+', dl)[:2]]; stated = round(nums[0]*nums[1], 2)
    area = shoelace(r['poly']) * (MM_PER_U/1000)**2
    ROOMS.append({'name': r['name'], 'stated': stated, 'poly_u': r['poly'], 'area_m2_traced': round(area, 2), 'dims_label': dl,
                  'edges': r['edges'], 'closures': r['closures'], 'ratio': round(area/stated, 3)})
json.dump({'walls_u': walls_u, 'labels': LABELS, 'rooms_u': ROOMS}, open(os.path.join(OUT, '_trace_u.json'), 'w'))
# --- r5 data (all mm, one transform) ---
def rmm(q): a = u2mm(q[0], q[1]); b = u2mm(q[2], q[3]); return [a[0], a[1], b[0], b[1]]
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
plan = {
  'plan_id': '4B-FF', 'revision': 'r6', 'step': '2 Layout', 'units': 'mm',
  'labels': 'concept visualisation, not survey-verified, not construction-ready, not certified CAD',
  'source_plan': {'svg': 'active/approved-cad-v4/svg/FP-4B-FF_V4_portrait.svg', 'png': 'active/approved-cad-v4/png/FP-4B-FF_V4_long7680.png',
                  'pipeline_id': '4B-FF', 'approval': 'pt16u'},
  'transform': {'from': 'SVG group source_diagram units (u = source crop px)', 'origin_u': [ENV_U[0], ENV_U[1]],
                'mm_per_u': MM_PER_U, 'x': 'east (plan right)', 'y': 'plan down (south)',
                'scale_source': 'SOURCE: SVG envelope dimension line M138,123 L523,123 (385 u) labelled "ENVELOPE ~ 13.1 m" -> 13100/385',
                'checks': {'vertical_envelope': 'SVG dim line M120,141 L120,844 (703 u) labelled 23.9 m -> 33.997 mm/u (-0.09%)',
                           'scale_bar': 'SVG page scale bar 1 m = 33.670 page u; group scale 1.14695 -> 34.064 mm/u (+0.11%)',
                           'r4_used': '35.53 mm/u (GF calibration) -> r4 was +4.4% large'},
                'applies_to': 'WALLS, VOIDS, ANCHORS, ROOMS, STAIRS, DOORS, WINS, FURNITURE (single transform)'},
  'ENVELOPE_MM': [0, 0, 13100, round(703*MM_PER_U)],
  'WALLS': [rmm(q) + ['t'] for q in walls_u],
  'walls_source': 'MEASURED: V4 long7680 raster dark poche (lum<95), 7px opening, decomposed to rects at 0.5 u',
  'VOIDS': [{'id': v['id'], 'rect': rmm(v['u']), 'source': v['source']} for v in VOIDS_U],
  'ANCHORS': [{'id': slug(L['name']) + ('' if L['name'] != 'BALCONY' else '-%d' % k), 'name': L['name'].title(), 'at': list(u2mm(*L['u'])),
               'dims_label': L['dims_label'], 'source': 'SOURCE: SVG label text position (same transform)'} for k, L in enumerate(LABELS)],
  'ROOMS': [{'id': slug(r['name']), 'name': r['name'].title(), 'poly': [list(u2mm(*p)) for p in r['poly_u']],
             'area_m2_traced': round(r['area_m2_traced'], 2), 'stated_area_m2': r['stated'], 'dims_label': r['dims_label'],
             'delta_pct': round((r['ratio']-1)*100, 1), 'within_5pct': abs(r['ratio']-1) <= 0.05, 'edges': r['edges'], 'derived_closures': r['closures'],
             'source': 'DERIVED: polygon on wall faces measured by scan lines on the V4 raster; door/window gaps closed on the wall line; listed closures are DERIVED'} for r in ROOMS],
  'CLOSURES': [{'id': c['id'], 'a': list(u2mm(c['at'], c['span'][0]) if c['axis']=='x' else u2mm(c['span'][0], c['at'])),
                'b': list(u2mm(c['at'], c['span'][1]) if c['axis']=='x' else u2mm(c['span'][1], c['at'])), 'rooms': c['rooms'], 'source': c['line']} for c in CLOS],
  'ROOMS_NOT_DERIVED': ROOMS_ND,
  'STAIRS': [{'id': 'first-floor-stair', 'rect': rmm([STAIR_U['x0'], STAIR_U['y0'], STAIR_U['x1'], STAIR_U['y1']]),
              'length_mm': round((STAIR_U['y1']-STAIR_U['y0'])*MM_PER_U), 'width_mm': round((STAIR_U['x1']-STAIR_U['x0'])*MM_PER_U),
              'tread_depth_mm_derived': round(STAIR_U['tread_pitch_u']*MM_PER_U), 'treads_derived': round((STAIR_U['y1']-STAIR_U['y0'])/STAIR_U['tread_pitch_u']),
              'break_line_y_mm': u2mm(0, STAIR_U['break_line_u_y'])[1],
              'source': 'MEASURED: V4 raster tread-box hairlines; 15 tread lines visible, rest faint; count DERIVED from pitch',
              'rise_direction': 'NOT FOUND (no arrow on V4 FF plan)'}],
  'DOORS': [], 'WINS': [], 'OPENINGS_OTHER': [],
  'FURNITURE': [],
  'excluded': ['potted plants (critic defect 6: no plan symbol)', 'materials, lighting, 3D detailing (step 3+)'],
}
for o in OPEN:
    a, b = o['span']
    p0 = u2mm(o['at'], a) if o['axis'] == 'x' else u2mm(a, o['at'])
    p1 = u2mm(o['at'], b) if o['axis'] == 'x' else u2mm(b, o['at'])
    rec = {'id': o['id'], 'a': list(p0), 'b': list(p1), 'width_mm': round((b-a)*MM_PER_U), 'rooms': o['rooms'],
           'evidence': o['evidence'], 'confidence': o['confidence'], 'source': 'MEASURED on V4 raster (+-1 u = +-34 mm)'}
    if 'swing' in o:
        sw = dict(o['swing'])
        if 'hinge_u' in sw: sw['hinge_mm'] = list(u2mm(*sw.pop('hinge_u')))
        sw['method'] = 'arc scoring: 4 hinge/side hypotheses, quarter arc r = door width sampled 12-78 deg; READ only if score >= 0.65 and lead >= 0.25 (r6_step2/arc_score.py)'
        rec['swing'] = sw
    {'door': plan['DOORS'], 'window': plan['WINS']}.get(o['type'], plan['OPENINGS_OTHER']).append(rec)
for o in OTHER:
    a, b = o['span']
    plan['OPENINGS_OTHER'].append({'id': o['id'], 'type': o['type'], 'a': list(u2mm(o['at'], a)), 'b': list(u2mm(o['at'], b)), 'rooms': o['rooms'], 'evidence': o['evidence'], 'crop': o['crop']})
for f in FURN_U:
    rec = dict(f); 
    if 'rect_u' in f: rec['rect'] = rmm(f['rect_u']); rec['size_mm'] = [rec['rect'][2]-rec['rect'][0], rec['rect'][3]-rec['rect'][1]]
    if 'circle_u' in f:
        cx, cy, rr = f['circle_u']; rec['center'] = list(u2mm(cx, cy)); rec['radius_mm'] = round(rr*MM_PER_U)
    rec.pop('rect_u', None); rec.pop('circle_u', None)
    plan['FURNITURE'].append(rec)
xs = [w[0] for w in plan['WALLS']] + [w[2] for w in plan['WALLS']]; ys = [w[1] for w in plan['WALLS']] + [w[3] for w in plan['WALLS']]
plan['WALL_BBOX_MM'] = [min(xs), min(ys), max(xs), max(ys)]
os.makedirs(os.path.join(OUT, '..', 'data'), exist_ok=True)
json.dump(plan, open(os.path.join(OUT, '..', 'data', 'fp-4b-ff.plan.r6.json'), 'w'), indent=1)
with open(os.path.join(OUT, '..', 'data', 'fp-4b-ff.plan.r6.js'), 'w') as fjs:
    fjs.write('/* Generated (r6 step 2 layout) by r6_step2/build_r6_layout.py. Do not hand-edit. Concept visualisation, not survey-verified, not construction-ready, not certified CAD. */\nconst PLAN_R6 = ' + json.dumps(plan) + ';\n')
# --- images ---
big_c = big.crop((round(x0), round(y0), round(x1), round(y1))).resize(work.size, Image.LANCZOS)
big_c.save(os.path.join(OUT, 'FP-4B-FF_V4_cad_clean.png'))
ov = big_c.copy().convert('RGBA'); lay = Image.new('RGBA', ov.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
def P(x, y): return ((x-U0[0])*R, (y-U0[1])*R)
try: F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22); Fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
except Exception: F = Fs = ImageFont.load_default()
for r in ROOMS: d.polygon([P(*p) for p in r['poly_u']], fill=(255, 210, 0, 40), outline=(230, 150, 0, 255))
for q in walls_u: d.rectangle([P(q[0], q[1]), P(q[2], q[3])], fill=(220, 0, 0, 140))
for v in VOIDS_U: d.rectangle([P(v['u'][0], v['u'][1]), P(v['u'][2], v['u'][3])], outline=(0, 160, 200, 255), width=4)
s = STAIR_U; d.rectangle([P(s['x0'], s['y0']), P(s['x1'], s['y1'])], outline=(0, 0, 255, 255), width=5)
yy = s['y0']
while yy <= s['y1'] + 0.1: d.line([P(s['x0'], yy), P(s['x1'], yy)], fill=(0, 0, 255, 150), width=1); yy += s['tread_pitch_u']
for f in FURN_U:
    if 'rect_u' in f: q = f['rect_u']; d.rectangle([P(q[0], q[1]), P(q[2], q[3])], outline=(150, 0, 200, 255), width=3)
    if 'circle_u' in f: cx, cy, rr = f['circle_u']; d.ellipse([P(cx-rr, cy-rr), P(cx+rr, cy+rr)], outline=(150, 0, 200, 255), width=3)
for o in OPEN:
    a, b = o['span']; col = (0, 170, 0, 255) if o['type'] == 'door' else (0, 120, 255, 255)
    pa, pb = (P(o['at'], a), P(o['at'], b)) if o['axis'] == 'x' else (P(a, o['at']), P(b, o['at']))
    d.line([pa, pb], fill=col, width=9)
    d.text(((pa[0]+pb[0])/2+6, (pa[1]+pb[1])/2-10), o['id'], fill=col, font=Fs)
for c in CLOS:
    a, b = c['span']; pa, pb = (P(c['at'], a), P(c['at'], b)) if c['axis'] == 'x' else (P(a, c['at']), P(b, c['at']))
    n = 14
    for k in range(n):
        if k % 2 == 0: d.line([(pa[0]+(pb[0]-pa[0])*k/n, pa[1]+(pb[1]-pa[1])*k/n), (pa[0]+(pb[0]-pa[0])*(k+1)/n, pa[1]+(pb[1]-pa[1])*(k+1)/n)], fill=(0, 0, 0, 255), width=6)
    d.text(((pa[0]+pb[0])/2+6, (pa[1]+pb[1])/2+4), c['id'], fill=(0, 0, 0, 255), font=Fs)
for o in OPEN:
    sw = o.get('swing', {})
    if 'hinge_u' in sw:
        hx, hy = sw['hinge_u']; w = o['span'][1]-o['span'][0]; sgn = 1 if ('east' in sw['opens_toward'] or 'south' in sw['opens_toward']) else -1
        tip = (hx+sgn*w, hy) if o['axis'] == 'x' else (hx, hy+sgn*w)
        d.line([P(hx, hy), P(*tip)], fill=(0, 90, 0, 255), width=4); d.ellipse([P(hx-1.5, hy-1.5), P(hx+1.5, hy+1.5)], fill=(0, 90, 0, 255))
for o in OTHER:
    a, b = o['span']; d.line([P(o['at'], a), P(o['at'], b)], fill=(255, 120, 0, 255), width=7); d.text((P(o['at'], a)[0]+8, P(o['at'], (a+b)/2)[1]), 'E1 ?', fill=(255, 120, 0, 255), font=Fs)
for L in LABELS:
    cx, cy = P(*L['u']); d.ellipse([cx-7, cy-7, cx+7, cy+7], fill=(255, 0, 255, 255)); d.text((cx+9, cy-26), 'r6: ' + L['name'].title(), fill=(200, 0, 200, 255), font=Fs)
# envelope + annotation
d.rectangle([P(ENV_U[0], ENV_U[1]), P(ENV_U[2], ENV_U[3])], outline=(0, 0, 0, 255), width=2)
ya = P(0, ENV_U[1]-14)[1]; d.line([P(ENV_U[0], ENV_U[1]-14), P(ENV_U[2], ENV_U[1]-14)], fill=(0, 0, 0, 255), width=4)
d.text((P(250, 0)[0], ya-30), 'ENVELOPE 13.10 m (SVG "~13.1 m", 385 u) = r6 scale 34.03 mm/u', fill=(0, 0, 0, 255), font=F)
# scale bar 0-5 m
bx, by = P(150, 860)
for k in range(5):
    seg = 1000/MM_PER_U*R
    d.rectangle([bx+k*seg, by, bx+(k+1)*seg, by+14], fill=(0, 0, 0, 255) if k % 2 == 0 else (255, 255, 255, 255), outline=(0, 0, 0, 255))
    d.text((bx+k*seg-5, by+16), str(k), fill=(0, 0, 0, 255), font=Fs)
d.text((bx+5*seg-5, by+16), '5 m', fill=(0, 0, 0, 255), font=Fs)
d.text((bx, by-30), 'r6 scale bar (34.03 mm/u)', fill=(0, 0, 0, 255), font=Fs)
leg = ['red: r6 walls (raster poche)', 'orange: r6 room polygons, dashed black: DERIVED closures', 'magenta: r6 label anchors (SVG text)', 'blue box: r6 stair', 'dark-green tick: door hinge + swing side',
       'green: doors  light-blue: glazing/windows', 'purple: furniture + fixture footprints', 'cyan: voids', 'orange dashed: E1 void edge (NOT FOUND class)', 'Concept visualisation, not survey-verified,', 'not construction-ready, not certified CAD']
lx, ly = P(400, 852)
for k, t in enumerate(leg): d.text((lx-250, ly+k*21-30), t, fill=(0, 0, 0, 255), font=Fs)
Image.alpha_composite(ov, lay).convert('RGB').save(os.path.join(OUT, 'FP-4B-FF_r6_trace_on_V4.png'))
print('walls', len(walls_u), 'labels', len(LABELS), 'doors', len(plan['DOORS']), 'wins', len(plan['WINS']), 'furn', len(plan['FURNITURE']))
print('stair', plan['STAIRS'][0]['length_mm'], plan['STAIRS'][0]['width_mm'], 'bbox', plan['WALL_BBOX_MM'])

# --- rooms-fill overlay ---
rf = big_c.copy().convert('RGBA'); lay2 = Image.new('RGBA', rf.size, (0, 0, 0, 0)); d2 = ImageDraw.Draw(lay2)
pal = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 212), (0, 128, 128), (220, 190, 255), (170, 110, 40), (128, 0, 0)]
for k, r in enumerate(ROOMS):
    col = pal[k % len(pal)]
    d2.polygon([P(*p) for p in r['poly_u']], fill=col + (95,), outline=col + (255,))
    xs_ = [p[0] for p in r['poly_u']]; ys_ = [p[1] for p in r['poly_u']]
    cx, cy = P(sum(xs_)/len(xs_), sum(ys_)/len(ys_))
    flag = '' if abs(r['ratio']-1) <= 0.05 else '  MISS'
    t = '%s\n%.2f m2 (plan %.2f, %+.1f%%)%s' % (r['name'], r['area_m2_traced'], r['stated'], (r['ratio']-1)*100, flag)
    d2.multiline_text((cx-90, cy-22), t, fill=(0, 0, 0, 255), font=Fs)
for c in CLOS:
    a, b = c['span']; pa, pb = (P(c['at'], a), P(c['at'], b)) if c['axis'] == 'x' else (P(a, c['at']), P(b, c['at']))
    d2.line([pa, pb], fill=(0, 0, 0, 255), width=5); d2.text(((pa[0]+pb[0])/2+4, (pa[1]+pb[1])/2+4), c['id'] + ' derived', fill=(0, 0, 0, 255), font=Fs)
bx, by = P(150, 860)
for k in range(5):
    seg = 1000/MM_PER_U*R
    d2.rectangle([bx+k*seg, by, bx+(k+1)*seg, by+14], fill=(0, 0, 0, 255) if k % 2 == 0 else (255, 255, 255, 255), outline=(0, 0, 0, 255))
d2.text((bx, by+18), '0-5 m scale bar (34.03 mm/u). Rooms r6 on V4 FF. Concept visualisation, not survey-verified, not construction-ready, not certified CAD.', fill=(0, 0, 0, 255), font=Fs)
Image.alpha_composite(rf, lay2).convert('RGB').save(os.path.join(OUT, 'FP-4B-FF_r6_rooms_fill_on_V4.png'))
for r in ROOMS: print('%-14s %6.2f %6.2f %+5.1f%% %s' % (r['name'], r['area_m2_traced'], r['stated'], (r['ratio']-1)*100, 'ok' if abs(r['ratio']-1) <= 0.05 else 'MISS'))
