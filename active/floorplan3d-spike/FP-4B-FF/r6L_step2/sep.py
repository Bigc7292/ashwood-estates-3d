import json, numpy as np
from scipy import ndimage as ndi
FF = 'active/floorplan3d-spike/FP-4B-FF/data/'
src = json.load(open(FF + 'fp-4b-ff.plan.r5L.json'))
p = src['plan']
MM = p['mm_per_crop_px']; x0, y0 = p['origin_crop_px']
# closures from the step-2 lane (closures_u.json, coords in crop px frame; C2/C3 coincide with the traced void outlines)
CL = [  # (id, x1,y1,x2,y2 in crop px), ASSUMED closures, 4 crop px thick
 ('C1', 271.8, 347.5, 368.5, 351.5),   # Family Living / Corridor, closed on M. Dressing / lift north wall
 ('C2', 370.0, 420.0, 374.0, 552.0),   # Corridor / courtyard void edge (drawn double line)
 ('C3', 271.8, 636.0, 368.5, 640.0),   # Corridor / open-to-below top edge
 ('C4', 377.8, 638.5, 437.0, 642.5),   # J. Dress / Junior Suite, on J. Bath south wall line
]
walls = [list(w) for w in p['WALLS']]
closure_walls = []
for cid, a, b, c, d in CL:
    w = [round((a-x0)*MM), round((b-y0)*MM), round((c-x0)*MM), round((d-y0)*MM), 't']
    closure_walls.append(w)
allw = walls + closure_walls
W = p['WALL_BBOX_MM'][2]; H = p['WALL_BBOX_MM'][3]
R = 2  # px per crop px raster (~17.8 mm)
def mm2px(v): return int(round(v / MM * R))
gw, gh = mm2px(W) + 2, mm2px(H) + 2
def raster(ws):
    g = np.zeros((gh, gw), bool)
    for x1, y1, x2, y2, _ in ws:
        g[mm2px(y1):mm2px(y2)+1, mm2px(x1):mm2px(x2)+1] = True
    return g
wall = raster(allw)
free = ~wall
lab, n = ndi.label(free)
rooms = [r for r in p['ROOMS'] if r['id'] != 'plate']
seeds = {a['id']: (a['at'], a.get('dims_label'), a.get('area_m2_derived')) for a in p['ANCHORS']}
out = {}
for r in rooms:
    rid = r['id']
    if rid not in seeds: continue
    (sx, sy), dims, area = seeds[rid]
    px, py = mm2px(sx), mm2px(sy)
    L = lab[py, px]
    if L == 0:
        out[rid] = ('seed in wall', None); continue
    comp = lab == L
    a_m2 = comp.sum() / (R*R) * (MM/1000)**2
    ys, xs = np.nonzero(comp)
    bw = (xs.max()-xs.min()+1) * MM/R/1000; bh = (ys.max()-ys.min()+1) * MM/R/1000
    out[rid] = (round(a_m2, 2), area, dims, round(bw, 2), round(bh, 2), int(comp.sum() and (xs.max()-xs.min()+1)))
for k, v in out.items(): print(k, v)
print('components', n, 'closures', len(closure_walls))
json.dump({'closures': CL, 'closure_walls_mm': closure_walls}, open('/tmp/claude-0/-home-user/afc66905-f2fa-5a30-bd08-01c638af991e/scratchpad/r6L/closures_mm.json','w'), indent=1)

# diagnostics: component sizes and seed positions
sizes = ndi.sum(np.ones_like(lab), lab, index=range(1, n+1))
print('comp sizes (px at R=2):', sorted([int(s) for s in sizes], reverse=True))
from PIL import Image
img = np.zeros((gh, gw, 3), np.uint8)
rng = np.random.default_rng(1)
cols = rng.integers(60, 255, size=(n+1, 3)); cols[0] = 0
img[free] = cols[lab[free]]
img[wall] = (255, 255, 255)
for rid, (sx, sy), in [(a['id'], a['at']) for a in p['ANCHORS']]:
    img[max(0,mm2px(sy)-3):mm2px(sy)+3, max(0,mm2px(sx)-3):mm2px(sx)+3] = (255, 0, 0)
Image.fromarray(img).resize((gw*2, gh*2), Image.NEAREST).save('/tmp/claude-0/-home-user/afc66905-f2fa-5a30-bd08-01c638af991e/scratchpad/r6L/diag.png')
