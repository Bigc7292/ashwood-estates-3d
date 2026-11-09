"""FP-4B-FF r5 step 2 (layout) builder.
Concept visualisation, not survey-verified, not construction-ready, not certified CAD.

Source: approved V4 plan active/approved-cad-v4/png/FP-4B-FF_V4_long7680.png (render of
active/approved-cad-v4/svg/FP-4B-FF_V4_portrait.svg, ACTIVE_PIPELINE.json id 4B-FF, approval pt16u).
All geometry uses ONE transform: SVG group 'source_diagram' units ("u", = source crop px)
  -> world mm: X = (u - 138) * MM_PER_U, Y = (v - 141) * MM_PER_U   (x east/right, y plan-down)
MM_PER_U = 13100 / 385: SVG envelope dimension line M138,123 L523,123 labelled "ENVELOPE ~ 13.1 m".
Usage: python build_r5_layout.py <repo_root> <out_dir>
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
# --- rooms: free space flood from each label, doors/windows/void edges closed ---
free = ~t2
def close_seg(axis, c, a, b):
    if axis == 'x':  # vertical segment at x=c from y=a..b
        i0, j0 = int((a-U0[1])*2), int((c-1.5-U0[0])*2); i1, j1 = int((b-U0[1])*2), int((c+1.5-U0[0])*2)
    else:
        i0, j0 = int((c-1.5-U0[1])*2), int((a-U0[0])*2); i1, j1 = int((c+1.5-U0[1])*2), int((b-U0[0])*2)
    free[max(i0,0):i1+1, max(j0,0):j1+1] = False
for o in OPEN: close_seg(o['axis'], o['at'], o['span'][0], o['span'][1])
for v in VOIDS_U:
    x_0, y_0, x_1, y_1 = v['u']
    close_seg('y', y_0, x_0, x_1); close_seg('y', y_1, x_0, x_1); close_seg('x', x_0, y_0, y_1); close_seg('x', x_1, y_0, y_1)
# envelope box
e0 = (int((ENV_U[1]-U0[1])*2), int((ENV_U[0]-U0[0])*2)); e1 = (int((ENV_U[3]-U0[1])*2), int((ENV_U[2]-U0[0])*2))
env = np.zeros_like(free); env[e0[0]:e1[0], e0[1]:e1[1]] = True; free &= env
nlab, comp = cv2.connectedComponents(free.astype(np.uint8), 4)
ROOMS = []; ROOMS_ND = []
for L in LABELS:
    if L['name'] == 'BALCONY': continue
    ii, jj = int((L['u'][1]-U0[1])*2), int((L['u'][0]-U0[0])*2)
    # nearest free pixel to the label point
    best = None
    for r in range(0, 30):
        win = comp[ii-r:ii+r+1, jj-r:jj+r+1]
        if (win > 0).any():
            vals, cnt = np.unique(win[win > 0], return_counts=True); best = vals[cnt.argmax()]; break
    msk = (comp == best).astype(np.uint8)
    cs, _ = cv2.findContours(msk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cs, key=cv2.contourArea)
    c = cv2.approxPolyDP(c, 1.5, True)
    poly_u = [[U0[0]+p[0][0]/2, U0[1]+p[0][1]/2] for p in c]
    area_m2 = msk.sum() * (MM_PER_U/2/1000)**2
    nums = [float(q) for q in re.findall(r'[\d.]+', L['dims_label'])[:2]]
    stated = nums[0]*nums[1] if len(nums) == 2 else None
    if not stated or not (0.6 <= area_m2/stated <= 1.5):
        ROOMS_ND.append({'name': L['name'].title(), 'dims_label': L['dims_label'], 'stated_area_m2': stated,
                         'reason': 'NOT DERIVED in r5: flood region leaks (open plan to corridor or unpoched joinery/thin partitions); traced region %.1f m2' % area_m2})
        continue
    ROOMS.append({'name': L['name'], 'stated': stated, 'poly_u': poly_u, 'area_m2_traced': round(float(area_m2), 2), 'dims_label': L['dims_label']})
json.dump({'walls_u': walls_u, 'labels': LABELS, 'rooms_u': ROOMS}, open(os.path.join(OUT, '_trace_u.json'), 'w'))
# --- r5 data (all mm, one transform) ---
def rmm(q): a = u2mm(q[0], q[1]); b = u2mm(q[2], q[3]); return [a[0], a[1], b[0], b[1]]
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
plan = {
  'plan_id': '4B-FF', 'revision': 'r5', 'step': '2 Layout', 'units': 'mm',
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
             'source': 'DERIVED: wall-enclosed free space flooded from the SVG label, door/window/void gaps closed'} for r in ROOMS],
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
    {'door': plan['DOORS'], 'window': plan['WINS']}.get(o['type'], plan['OPENINGS_OTHER']).append(rec)
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
json.dump(plan, open(os.path.join(OUT, '..', 'data', 'fp-4b-ff.plan.r5.json'), 'w'), indent=1)
with open(os.path.join(OUT, '..', 'data', 'fp-4b-ff.plan.r5.js'), 'w') as fjs:
    fjs.write('/* Generated (r5 step 2 layout) by r5_step2/build_r5_layout.py. Do not hand-edit. Concept visualisation, not survey-verified, not construction-ready, not certified CAD. */\nconst PLAN_R5 = ' + json.dumps(plan) + ';\n')
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
for L in LABELS:
    cx, cy = P(*L['u']); d.ellipse([cx-7, cy-7, cx+7, cy+7], fill=(255, 0, 255, 255)); d.text((cx+9, cy-26), 'r5: ' + L['name'].title(), fill=(200, 0, 200, 255), font=Fs)
# envelope + annotation
d.rectangle([P(ENV_U[0], ENV_U[1]), P(ENV_U[2], ENV_U[3])], outline=(0, 0, 0, 255), width=2)
ya = P(0, ENV_U[1]-14)[1]; d.line([P(ENV_U[0], ENV_U[1]-14), P(ENV_U[2], ENV_U[1]-14)], fill=(0, 0, 0, 255), width=4)
d.text((P(250, 0)[0], ya-30), 'ENVELOPE 13.10 m (SVG "~13.1 m", 385 u) = r5 scale 34.03 mm/u', fill=(0, 0, 0, 255), font=F)
# scale bar 0-5 m
bx, by = P(150, 860)
for k in range(5):
    seg = 1000/MM_PER_U*R
    d.rectangle([bx+k*seg, by, bx+(k+1)*seg, by+14], fill=(0, 0, 0, 255) if k % 2 == 0 else (255, 255, 255, 255), outline=(0, 0, 0, 255))
    d.text((bx+k*seg-5, by+16), str(k), fill=(0, 0, 0, 255), font=Fs)
d.text((bx+5*seg-5, by+16), '5 m', fill=(0, 0, 0, 255), font=Fs)
d.text((bx, by-30), 'r5 scale bar (34.03 mm/u)', fill=(0, 0, 0, 255), font=Fs)
leg = ['red: r5 walls (raster poche)', 'orange: r5 room polygons (derived)', 'magenta: r5 label anchors (SVG text)', 'blue box: r5 stair',
       'green: doors  light-blue: glazing/windows', 'purple: furniture footprints', 'cyan: voids', 'Concept visualisation, not survey-verified,', 'not construction-ready, not certified CAD']
lx, ly = P(400, 852)
for k, t in enumerate(leg): d.text((lx-250, ly+k*21-30), t, fill=(0, 0, 0, 255), font=Fs)
Image.alpha_composite(ov, lay).convert('RGB').save(os.path.join(OUT, 'FP-4B-FF_r5_trace_on_V4.png'))
print('walls', len(walls_u), 'labels', len(LABELS), 'rooms', [(r['name'], round(float(r['area_m2_traced']),2)) for r in ROOMS], 'nd', [r['name'] for r in ROOMS_ND])
print('stair', plan['STAIRS'][0]['length_mm'], plan['STAIRS'][0]['width_mm'], 'bbox', plan['WALL_BBOX_MM'])
