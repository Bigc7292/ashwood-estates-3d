#!/usr/bin/env python3
"""Build model.json for the Ashwood 4B exterior/garden concept model.
Read-only inputs (resolved via ACTIVE_PIPELINE.json); all outputs under /workspace/exterior-garden-3d/4b/.
Coordinates: metres, x = plan right, z = plan down (toward street/front), y = up.
Origin = top-left corner of the approved V4 GF site-diagram rectangle (GF crop px 107,54).
"""
import json, hashlib, numpy as np
from pathlib import Path
R = Path('/workspace/plan-visuals-archive')
OUT = Path('/workspace/exterior-garden-3d/4b')
act = json.loads((R/'ACTIVE_PIPELINE.json').read_text())
plans = {p['id']: p for p in act['plans']}
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
for pid in ['4B-GF','4B-FF','4B-RF']:
    p = plans[pid]
    assert 'superseded' not in p['svg']
    assert sha(R/p['svg']) == p['sha256']['svg'], f'FAIL CLOSED: hash mismatch {pid}'
cal = json.loads((R/'source-evidence/calibration/4B-GF_source_span_calibration.json').read_text())
PPM = cal['fit_px_per_m']            # GF crop px per metre (approx, max residual 1.7 %, +/-3 % working)
SX0, SY0 = 107.0, 54.0               # V4 GF site-diagram rect origin (crop px): <rect x=107 y=54 w=527 h=841>
gx = lambda px: round((px - SX0) / PPM, 3)
gz = lambda py: round((py - SY0) / PPM, 3)
# FF crop -> GF crop: map V4 FF site-diagram box (54..607 x 55..932) onto V4 GF site box (107..634 x 54..895)
FSX = (634-107)/(607-54); FSY = (895-54)/(932-55)
f2g = lambda fx, fy: (107 + (fx-54)*FSX, 54 + (fy-55)*FSY)
# RF crop -> FF crop: same embedded board (xref 439); crop offsets [1820,455] vs [980,370] => (+840,+85) board offset,
# then horizontal board placement aligned by LIFT label anchors (RF 321,291 / FF 398,376) => fx = rx+77, fy = ry+85
r2f = lambda rx, ry: (rx + 77, ry + 85)

# display-only heights (NOT in any source) ------------------------------------------------
H = dict(plinth=0.0, gf=3.6, slab=0.4, ff=3.4, rf=3.0, roof_slab=0.45, balustrade=1.1,
         boundary_side=1.8, boundary_front=1.2, gate=1.8, canopy_carport=3.0)
GF_TOP = H['gf']; FF0 = GF_TOP + H['slab']; FF_TOP = FF0 + H['ff']; RF0 = FF_TOP + H['roof_slab']

def rect_decompose(mask):
    m = mask.copy(); Hh, W = m.shape; rects = []
    for y in range(Hh):
        x = 0; row = m[y]
        while x < W:
            if not row[x]: x += 1; continue
            x1 = x
            while x1 < W and row[x1]: x1 += 1
            y1 = y + 1
            while y1 < Hh and m[y1, x:x1].all(): y1 += 1
            m[y:y1, x:x1] = False; rects.append((x, y, x1, y1)); x = x1
    return rects

M = {'meta': {}, 'boxes': [], 'polys': [], 'water': [], 'trees': [], 'labels': []}
def box(id_, cat, x0, z0, x1, z1, y0, y1, mat, status):
    M['boxes'].append(dict(id=id_, cat=cat, x0=min(x0,x1), z0=min(z0,z1), x1=max(x0,x1), z1=max(z0,z1), y0=y0, y1=y1, mat=mat, status=status))

# ---- site / ground ----------------------------------------------------------------------
site_w, site_d = gx(634), gz(895)
box('site-paving', 'ground', 0, 0, site_w, site_d, -0.05, 0.0, 'paving', 'plan')
lawns = [(111,59,77,65),(111,128,45,345),(111,490,79,43),(531,59,100,70),(592,135,39,393),(593,532,39,302),(151,583,39,111),(381,834,160,57)]
for i,(x,y,w,h) in enumerate(lawns):
    box(f'lawn-{i+1}', 'lawn', gx(x), gz(y), gx(x+w), gz(y+h), 0.0, 0.03, 'lawn', 'plan')
# ---- GF building: spike-traced V4 structural poche (mm from crop origin 148,164.5) ---------
spike = json.loads((R/'active/floorplan3d-spike/FP-4B-GF/data/fp-4b-gf.plan.json').read_text())['plan']
ox, oy = spike['origin_crop_px']
offx, offz = (ox-SX0)/PPM, (oy-SY0)/PPM
for i,(a,b,c,d,_) in enumerate(spike['WALLS']):
    box(f'gf-wall-{i}', 'gf_wall', round(offx+a/1000,3), round(offz+b/1000,3), round(offx+c/1000,3), round(offz+d/1000,3), 0.0, GF_TOP, 'stone', 'plan')
for i,(a,b,c,d) in enumerate(spike['WINS']):
    box(f'gf-glass-{i}', 'gf_glass', round(offx+a/1000,3), round(offz+b/1000,3), round(offx+c/1000,3), round(offz+d/1000,3), 0.0, GF_TOP, 'glass', 'plan_cue_height_assumed')
gf_floor = [(195,188),(551,188),(551,808),(410,808),(410,713),(196,723)]
M['polys'].append(dict(id='gf-floor-plate', pts=[[gx(x),gz(y)] for x,y in gf_floor], holes=[[[gx(430),gz(410)],[gx(547),gz(410)],[gx(547),gz(514)],[gx(430),gz(514)]]], y0=0.0, y1=0.06, mat='paving_inner', status='plan'))
# GF/FF slab over GF footprint (display) and FF envelope
# ---- water --------------------------------------------------------------------------------
pool = (196,87,463,154)
M['water'].append(dict(id='swimming-pool', x0=gx(pool[0]), z0=gz(pool[1]), x1=gx(pool[2]), z1=gz(pool[3]), holes=[], y=0.0, status='plan+calibrated 9.50x2.40'))
cop = 0.3
for nm,(a,b,c,d) in {'n':(pool[0],pool[1],pool[2],pool[1]),'s':(pool[0],pool[3],pool[2],pool[3]),'w':(pool[0],pool[1],pool[0],pool[3]),'e':(pool[2],pool[1],pool[2],pool[3])}.items():
    x0,z0,x1,z1 = gx(a),gz(b),gx(c),gz(d)
    if nm in 'ns': box(f'pool-coping-{nm}','pool_coping', x0-cop, z0-(cop if nm=='n' else 0), x1+cop, z1+(cop if nm=='s' else 0), 0.0, 0.05, 'coping', 'assumed_width')
    else: box(f'pool-coping-{nm}','pool_coping', x0-(cop if nm=='w' else 0), z0, x1+(cop if nm=='e' else 0), z1, 0.0, 0.05, 'coping', 'assumed_width')
wf = (430,410,547,514); isl=(464,442,504,482)
M['water'].append(dict(id='courtyard-water-feature', x0=gx(wf[0]), z0=gz(wf[1]), x1=gx(wf[2]), z1=gz(wf[3]), holes=[[gx(isl[0]),gz(isl[1]),gx(isl[2]),gz(isl[3])]], y=0.0, status='plan'))
box('courtyard-planter-island','planter', gx(isl[0]), gz(isl[1]), gx(isl[2]), gz(isl[3]), 0.0, 0.45, 'stone', 'plan_xy_height_assumed')
# ---- trees: V4 'source landscape' tree symbols (circle centre, radius crop px) ---------------
trees = [(136,93,49),(569,101,56),(132,278,41),(133,393,46),(148,522,44),(158,648,40),(613,309,42),(614,441,41),(615,574,44),(616,709,39),(626,828,36),(421,857,45),(484,462,39)]
for i,(x,y,r) in enumerate(trees):
    M['trees'].append(dict(id=f'tree-{i+1}', x=gx(x), z=gz(y), r=round(r/PPM,2), status='plan_symbol_species_height_unknown', courtyard=(i==12)))
# ---- FF: wall mask traced from untouched FF crop (lum<175, 5px open) --------------------------
ffm = np.load(OUT/'work/ff_wallmask.npy')
for i,(x0,y0,x1,y1) in enumerate(rect_decompose(ffm)):
    if (x1-x0)*(y1-y0) < 6: continue
    a,b = f2g(x0,y0); c,d = f2g(x1,y1)
    box(f'ff-wall-{i}', 'ff_wall', gx(a),gz(b),gx(c),gz(d), FF0, FF_TOP, 'stone', 'plan_trace_approx')
def frect(id_, cat, fx0,fy0,fx1,fy1, y0,y1, mat, status):
    a,b = f2g(fx0,fy0); c,d = f2g(fx1,fy1); box(id_, cat, gx(a),gz(b),gx(c),gz(d), y0,y1, mat, status)
# FF floor slab (GF roof) over FF envelope incl. balconies (FF V4 envelope dims 138..523 x 141..844)
def fpoly(id_, fpts, holes, y0, y1, mat, status):
    P=lambda pts: [[gx(f2g(x,y)[0]), gz(f2g(x,y)[1])] for x,y in pts]
    M['polys'].append(dict(id=id_, pts=P(fpts), holes=[P(h) for h in holes], y0=y0, y1=y1, mat=mat, status=status))
ENV=[(138,141),(523,141),(523,844),(138,844)]; VOID=[(389,428),(518,428),(518,535),(389,535)]  # FF V4 courtyard void (water seen below)
fpoly('ff-slab', ENV, [VOID], GF_TOP, FF0, 'soffit', 'plan_envelope_thickness_assumed')
# GF-only front volume beyond FF envelope? GF footprint stays inside; GF roof over GF-only parts = same slab
# FF glazing loop on enclosed footprint edges (x141..520, y192..757): rendered where no traced wall
for nm,(a,b,c,d) in {'rear':(141,194,520,196),'front-l':(141,755,270,757),'front-c':(270,773,380,775),'front-r':(380,758,520,760),'left':(144,192,146,757),'right':(515,192,517,760)}.items():
    frect(f'ff-glass-{nm}','ff_glass', a,b,c,d, FF0, FF_TOP, 'glass', 'inferred_from_plan_gaps')
# balconies
frect('ff-balcony-rear','balcony', 141,142,520,190, FF0-0.02, FF0+0.02, 'paving', 'plan_label_extent_traced')
frect('ff-balustrade-rear','balustrade', 141,142,520,145, FF0, FF0+H['balustrade'], 'glass_balustrade', 'render_p26_observed_height_assumed')
frect('ff-balcony-front-l','balcony', 141,757,270,790, FF0-0.02, FF0+0.02, 'paving', 'plan_label_extent_traced')
frect('ff-parapet-front-l','parapet', 141,787,270,790, FF0, FF0+H['balustrade'], 'stone', 'assumed')
frect('ff-balcony-front-r','balcony', 380,760,520,843, FF0-0.02, FF0+0.02, 'paving', 'plan_label_extent_traced')
frect('ff-parapet-front-r','parapet', 380,840,520,843, FF0, FF0+H['balustrade'], 'stone', 'render_p25_observed_stone_parapet_height_assumed')
# FF front vertical slat screen (p25) over 'open to below' front zone
frect('ff-slat-screen','slats', 262,777,380,781, FF0-0.0, FF_TOP, 'bronze_slats', 'render_p25_observed_location_inferred')
# FF roof slab (deep overhang observed p25/p26; extent = FF envelope only)
fpoly('ff-roof-slab', ENV, [VOID], FF_TOP, RF0, 'soffit', 'plan_envelope_overhang_unknown')
# ---- RF (NTS): core walls traced from RF crop, translated to FF crop via board offset ------------
rfm = np.load(OUT/'work/rf_wallmask.npy')
for i,(x0,y0,x1,y1) in enumerate(rect_decompose(rfm)):
    if (x1-x0)*(y1-y0) < 6: continue
    fa,fb = r2f(x0,y0); fc,fd = r2f(x1,y1)
    frect(f'rf-wall-{i}','rf_wall', fa,fb,fc,fd, RF0, RF0+H['rf'], 'placeholder', 'NTS_placeholder')
for nm,(x0,y0,x1,y1) in {'main':(66,262,300,630),'lift':(295,262,349,322)}.items():
    fa,fb = r2f(x0,y0); fc,fd = r2f(x1,y1)
    frect(f'rf-core-roof-{nm}','rf_roof', fa,fb,fc,fd, RF0+H['rf'], RF0+H['rf']+0.3, 'placeholder', 'NTS_placeholder_roofing_unknown')
fa,fb = r2f(70,105); fc,fd = r2f(440,108)
frect('rf-balustrade-rear','balustrade', fa,fb,fc,fd, RF0, RF0+H['balustrade'], 'glass_balustrade', 'render_p26_observed_NTS_position')
fa,fb = r2f(93,105); fc,fd = r2f(418,262)
frect('rf-canopy','canopy', fa,fb,fc,fd, RF0+H['rf'], RF0+H['rf']+0.35, 'placeholder', 'render_p26_observed_extent_assumed')
# ---- render-only elements, neutral placeholders -------------------------------------------
box('carport-canopy','canopy', gx(107), gz(723), gx(315), gz(895)-0.5, H['canopy_carport']-0.35, H['canopy_carport'], 'placeholder', 'render_p25_only_not_in_plan_extent_assumed')
box('carport-canopy-post','canopy', gx(107), gz(895)-0.9, gx(107)+0.4, gz(895)-0.5, 0, H['canopy_carport']-0.35, 'placeholder', 'render_p25_only_assumed')
# boundary
t=0.25
box('boundary-left','boundary', -t, 0, 0, site_d, 0, H['boundary_side'], 'placeholder', 'site_diagram_not_verified_height_assumed')
box('boundary-right','boundary', site_w, 0, site_w+t, site_d, 0, H['boundary_side'], 'placeholder', 'site_diagram_not_verified_height_assumed')
box('boundary-front-gate','gate', gx(315), site_d, gx(381), site_d+0.08, 0, H['gate'], 'bronze_bars', 'render_p25_observed_position_from_V4_entry_label')
box('boundary-front-wall-c','boundary', gx(381), site_d, gx(541), site_d+t, 0, H['boundary_front'], 'stone', 'render_p25_observed_height_assumed')
box('boundary-front-wall-r','boundary', gx(541), site_d, gx(575), site_d+t, 0, H['boundary_front'], 'stone', 'render_p25_observed_height_assumed')
box('boundary-front-service-gate','gate', gx(575), site_d, gx(634), site_d+0.08, 0, H['gate'], 'bronze_bars', 'assumed_from_V4_service_entry_label')
M['meta'] = dict(villa='ashwood-estates/4b', px_per_m=PPM, site_m=[site_w, site_d], heights_display_only=H,
                 GF_TOP=GF_TOP, FF0=FF0, FF_TOP=FF_TOP, RF0=RF0, ff_to_gf_scale=[FSX,FSY])
# labels for annotated aerial
M['labels'] = [dict(t='Swimming pool 9.50×2.40 m (plan)', x=gx(330), z=gz(120), y=0.5),
               dict(t='Terrace (V4 label, extent unknown)', x=gx(494), z=gz(166), y=0.5),
               dict(t='Outdoor terrace (V4 label, extent unknown)', x=gx(496), z=gz(359), y=0.5),
               dict(t='Courtyard water feature (plan)', x=gx(488), z=gz(430), y=0.6),
               dict(t='Driveway / parking (plan)', x=gx(220), z=gz(820), y=0.5),
               dict(t='Carport canopy: PLACEHOLDER (render p25 only)', x=gx(210), z=gz(780), y=3.4),
               dict(t='RF core: NTS PLACEHOLDER', x=gx(230), z=gz(450), y=RF0+3.6),
               dict(t='RF canopy: PLACEHOLDER (render p26)', x=gx(330), z=gz(220), y=RF0+3.8),
               dict(t='Boundary: site diagram, NOT verified', x=gx(110), z=gz(470), y=2.2),
               dict(t='Trees: plan symbols, species/height unknown', x=gx(613), z=gz(309), y=6.0)]
(OUT/'model/data/model.json').write_text(json.dumps(M, indent=1))
(OUT/'model/data/model.js').write_text('window.MODEL = ' + json.dumps(M) + ';\n')
print('boxes', len(M['boxes']), 'site', site_w, site_d, 'FF0', FF0, 'RF0', RF0)
