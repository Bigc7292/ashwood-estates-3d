#!/usr/bin/env python3
"""v4_to_floorplan3d.py -- Ashwood pipeline adapter (SPIKE, review-pending).

Converts ONE approved V4 plan (default FP-4B-GF) into the input data format of the
open-source Floorplan 3D viewer (https://github.com/wy51ai/floorplan-3d, MIT,
Copyright (c) 2026 wuyi) and writes a self-contained, offline static viewer.

Inputs (read-only):
  ACTIVE_PIPELINE.json -> approved V4 SVG (hash-checked; FAIL CLOSED on mismatch)
  source-evidence/calibration/<ID>_source_span_calibration.json (px per metre)
  canonical/rooms_index.json (room records, matched to V4 label anchors)
  upstream viewer checkout (index.html + LICENSE) and a local three@0.160.0 npm package.

Geometry policy:
  * Walls  = the approved V4 `structural_wall_poche` group, rasterised exactly (cairosvg,
             2x supersampling of crop pixels) and decomposed losslessly into axis-aligned
             rectangles (the viewer only supports rectangular wall boxes).
  * Doors  = only the 6 swing-door cues (leaf line + arc) drawn in the approved V4 SVG.
  * Glazing= only the glazing guideline cues drawn in the approved V4 SVG.
  * Water  = only the surfaces the approved V4 fills with the `pool` water gradient (traced
             outline; solid islands drawn inside them become holes) -> three.js Water2 (MIT).
  * Rooms  = V4 label anchors + canonical room records. NO room polygons are asserted
             (the approved trace has open doorways, so no closed room boundaries exist).
  * Metres = crop px / calibrated px-per-metre (approximate, max residual 1.7 %, +/-3 % working).
  * Anything the viewer needs that the source does not give (heights, sills, slab) is a
    DISPLAY-ONLY default recorded in the manifest.
Not survey-verified, not construction-ready, not certified CAD.
"""
import argparse, hashlib, io, json, math, re, shutil, subprocess, sys, datetime
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image
import cairosvg

NS = '{http://www.w3.org/2000/svg}'
SS = 2  # supersampling of crop pixels for the wall raster (1 cell = 0.5 crop px)

# Display-only defaults (the brochure gives none of these). Recorded in the manifest.
DISPLAY = {
    'wall_height_m': 3.0,          # full-wall display height; actual floor-to-ceiling UNKNOWN
    'cut_wall_height_m': 1.2,      # viewer "cut walls" toggle
    'door_head_m': 2.1,            # lintel/header above door openings
    'door_leaf_height_m': 2.05,    # viewer leaf height (upstream constant)
    'glazing_sill_m': 0.0,         # glazing cues drawn as full-height glazed panels
    'glazing_head_m': 2.4,
    'single_line_glazing_half_thickness_px': 1.5,  # when a cue is one line with no wall band nearby
    'room_flyto_frame_default_m': 4.0,  # camera framing when a label has no transcribed size
    'walk_eye_height_m': 1.6,
    'floor_plate': 'bounding box of traced walls; display slab only, not a room boundary or slab outline',
    'shadow_extent_m': 17,
    'water_surface_y_m': 0.01,     # water rendered flush with ground; depth/coping NOT modelled
    'water2': {'color': '#a9d8e6', 'scale': 3, 'flowDirection': [1, 1], 'textureWidth': 512, 'textureHeight': 512},
    'water_flat_fallback_color': '#7fbcd0',
    'island_display_colour': '#e0d9c3',
    'sun_hour_default': 16,        # v2: warm late-afternoon daylight by default (display-only; orientation of the site NOT known)
    'plate_floor_offset_m': -0.006,  # plate sits just under room floors (no z-fighting)
    'stair_material_colour': '#e6e0d4',
    'v2_full_walls_default': True,
}

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def nums(d):
    return [float(v) for v in re.findall(r'-?\d+(?:\.\d+)?', d)]

def rep(src, old, new, count=1):
    n = src.count(old)
    if n != count:
        raise SystemExit(f'PATCH FAIL: expected {count} match(es), found {n}: {old[:90]!r}')
    return src.replace(old, new)

def rect_decompose(mask):
    """Lossless greedy decomposition of a boolean mask into axis-aligned rectangles."""
    m = mask.copy(); H, W = m.shape; rects = []
    for y in range(H):
        x = 0
        row = m[y]
        while x < W:
            if not row[x]:
                x += 1; continue
            x1 = x
            while x1 < W and row[x1]:
                x1 += 1
            y1 = y + 1
            while y1 < H and m[y1, x:x1].all():
                y1 += 1
            m[y:y1, x:x1] = False
            rects.append((x, y, x1, y1))
            x = x1
    return rects

def wall_band(mask, axis_horiz, along0, along1, at, search=7):
    """Across-extent (crop px) of traced wall next to an opening, measured just outside both ends."""
    vals = []
    for a in (along0 - 1.0, along1 + 1.0):
        c = int(round(a * SS))
        lo, hi = int((at - search) * SS), int((at + search) * SS)
        if axis_horiz:
            if not (0 <= c < mask.shape[1]): continue
            col = mask[max(lo, 0):hi, c]; idx = np.where(col)[0] + max(lo, 0)
        else:
            if not (0 <= c < mask.shape[0]): continue
            col = mask[c, max(lo, 0):hi]; idx = np.where(col)[0] + max(lo, 0)
        if len(idx):
            vals += [idx.min() / SS, (idx.max() + 1) / SS]
    return (min(vals), max(vals)) if vals else None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument('--plan', default='4B-GF')
    ap.add_argument('--upstream', default='/workspace/floorplan-3d')
    ap.add_argument('--three', default='/workspace/fp3d-vendor/package')
    ap.add_argument('--three-textures', default='/workspace/fp3d-vendor/textures', help='three.js r160 examples/textures/water (from the r160 git tag)')
    ap.add_argument('--out', default=None)
    ap.add_argument('--readings', default=None, help='room polygon / furniture / material readings JSON (source-evidence/floorplan3d-readings/FP-<plan>.json)')
    a = ap.parse_args()
    R = Path(a.root); UP = Path(a.upstream); TH = Path(a.three)
    if a.plan != '4B-GF':
        raise SystemExit('SPIKE SCOPE: only 4B-GF is authorised until the user approves the spike.')
    OUT = Path(a.out) if a.out else R / 'active/floorplan3d-spike' / f'FP-{a.plan}'
    OUT.mkdir(parents=True, exist_ok=True)

    # ---------- inputs, fail closed ----------
    act = json.loads((R / 'ACTIVE_PIPELINE.json').read_text())
    p = next(q for q in act['plans'] if q['id'] == a.plan)
    svg_path = R / p['svg']
    if sha(svg_path) != p['sha256']['svg']:
        raise SystemExit('FAIL CLOSED: approved SVG hash mismatch')
    if 'superseded' in str(svg_path):
        raise SystemExit('FAIL CLOSED: retired input')
    cal_path = R / f'source-evidence/calibration/{a.plan}_source_span_calibration.json'
    cal = json.loads(cal_path.read_text())
    ppm = float(cal['fit_px_per_m']); k = 1000.0 / ppm  # mm per crop px
    rooms_idx = json.loads((R / 'canonical/rooms_index.json').read_text())['rooms']
    villa, floor = a.plan.split('-')[0].lower(), a.plan.split('-')[1].lower()
    canon = [r for r in rooms_idx if r['villa_id'] == villa and r['floor_id'] == floor]
    orig_pdf = R / act['original_source']

    root = ET.parse(svg_path).getroot()
    g = root.find(NS + 'g[@id="source_space"]')
    ch = list(g)
    wall = g.find(NS + 'g[@id="structural_wall_poche"]')
    wi = ch.index(wall)
    assert wall.get('transform') == 'translate(.5,.5)' and len(wall) == 13

    # ---------- walls: exact raster of the approved poche group ----------
    cw = p['source_board_crop_pixels'][2] - p['source_board_crop_pixels'][0]
    chh = p['source_board_crop_pixels'][3] - p['source_board_crop_pixels'][1]
    paths = ''.join(f'<path d="{q.get("d")}"/>' for q in wall)
    wsvg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{cw*SS}" height="{chh*SS}" viewBox="0 0 {cw} {chh}">'
            f'<rect width="{cw}" height="{chh}" fill="white"/><g transform="translate(.5,.5)" fill="black" stroke="black" '
            f'stroke-width="{wall.get("stroke-width")}" fill-rule="{wall.get("fill-rule")}" stroke-linejoin="round">{paths}</g></svg>')
    mask = np.array(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=wsvg.encode()))).convert('L')) < 128
    ys, xs = np.where(mask)
    bb_px = [xs.min() / SS, ys.min() / SS, (xs.max() + 1) / SS, (ys.max() + 1) / SS]
    ox, oy = bb_px[0], bb_px[1]
    X = lambda u: round((u - ox) * k)
    Y = lambda v: round((v - oy) * k)
    rects = rect_decompose(mask)
    walls = [[X(x0 / SS), Y(y0 / SS), X(x1 / SS), Y(y1 / SS), 't'] for x0, y0, x1, y1 in rects]
    # lossless check in cell space
    chk = np.zeros_like(mask)
    for x0, y0, x1, y1 in rects: chk[y0:y1, x0:x1] = True
    assert (chk == mask).all(), 'rect decomposition not lossless'
    (OUT / 'data').mkdir(exist_ok=True)
    Image.fromarray(np.where(mask, 0, 255).astype('uint8')).save(OUT / 'data' / 'wall_mask_2x.png')

    # ---------- openings from approved cues ----------
    cues = []
    for q in ch[wi + 1:]:
        if q.tag != NS + 'path': break
        cues.append(q.get('d'))
    assert len(cues) == 33, len(cues)
    lines = [(i, nums(d)) for i, d in enumerate(cues, 1) if 'A' not in d]
    arcs = [(i, d) for i, d in enumerate(cues, 1) if 'A' in d]
    doors, wins, provenance_open = [], [], []
    used = set()
    for ai, d in arcs:
        an = nums(d); a0, a1, r = (an[0], an[1]), (an[-2], an[-1]), an[2]
        li, ln = next((i, n) for i, n in lines if i == ai - 1)
        used.add(li)
        e0, e1 = (ln[0], ln[1]), (ln[2], ln[3])
        shared = e0 if e0 in (a0, a1) else e1
        hinge = e1 if shared == e0 else e0
        closed = a1 if shared == a0 else a0
        unit = lambda t: (int(round((t[0] - hinge[0]) / r)), int(round((t[1] - hinge[1]) / r)))
        c, o = unit(closed), unit(shared)
        horiz = c[1] == 0
        a_lo, a_hi = sorted([hinge[0], closed[0]] if horiz else [hinge[1], closed[1]])
        at = hinge[1] if horiz else hinge[0]
        band = wall_band(mask, horiz, a_lo, a_hi, at)
        status = 'across-extent from traced wall band beside opening'
        if band is None:
            band = (at - 1.5, at + 1.5); status = 'no wall band found; +/-1.5 px display thickness'
        rect_px = [a_lo, band[0], a_hi, band[1]] if horiz else [band[0], a_lo, band[1], a_hi]
        rect = [X(rect_px[0]), Y(rect_px[1]), X(rect_px[2]), Y(rect_px[3])]
        cells = mask[int(rect_px[1]*SS):int(rect_px[3]*SS), int(rect_px[0]*SS):int(rect_px[2]*SS)]
        doors.append({'name': f'Door cue {len(doors)+1}', 'rect': rect, 'h': [X(hinge[0]), Y(hinge[1])], 'c': list(c), 'o': list(o),
                      'len': round(r * k), 'cue_ids': [f'{a.plan}/plan-opening-cue-{li:02d}', f'{a.plan}/plan-opening-cue-{ai:02d}'],
                      'hinge_px': list(hinge), 'leaf_radius_px': r, 'rect_px': rect_px, 'rect_status': status,
                      'wall_overlap_fraction': round(float(cells.mean()) if cells.size else 0, 3),
                      'status': 'swing taken from approved 2D cue; leaf width approx (calibration); door type/height unverified'})
    remaining = [(i, n) for i, n in lines if i not in used]
    j = 0
    while j < len(remaining):
        i, n = remaining[j]
        horiz = n[1] == n[3]
        pair = None
        if j + 1 < len(remaining):
            i2, n2 = remaining[j + 1]
            if (n2[1] == n2[3]) == horiz and i2 == i + 1:
                if horiz and abs(n2[1] - n[1]) <= 6 and {n2[0], n2[2]} == {n[0], n[2]}: pair = (i2, n2)
                if not horiz and abs(n2[0] - n[0]) <= 6 and {n2[1], n2[3]} == {n[1], n[3]}: pair = (i2, n2)
        if pair:
            i2, n2 = pair
            xsv = [n[0], n[2], n2[0], n2[2]]; ysv = [n[1], n[3], n2[1], n2[3]]
            rect_px = [min(xsv), min(ysv), max(xsv), max(ysv)]; ids = [i, i2]; kind = 'double-line glazing cue'
            status = 'rect = extent of the two approved cue lines'
            j += 2
        else:
            a_lo, a_hi = (min(n[0], n[2]), max(n[0], n[2])) if horiz else (min(n[1], n[3]), max(n[1], n[3]))
            at = n[1] if horiz else n[0]
            band = wall_band(mask, horiz, a_lo, a_hi, at)
            status = 'across-extent from traced wall band beside opening'
            if band is None:
                hw = DISPLAY['single_line_glazing_half_thickness_px']; band = (at - hw, at + hw)
                status = f'no wall band found; +/-{hw} px display thickness'
            rect_px = [a_lo, band[0], a_hi, band[1]] if horiz else [band[0], a_lo, band[1], a_hi]
            ids = [i]; kind = 'single-line glazing/threshold cue'; j += 1
        cells = mask[int(rect_px[1]*SS):int(math.ceil(rect_px[3]*SS)), int(rect_px[0]*SS):int(math.ceil(rect_px[2]*SS))]
        wins.append({'rect': [X(rect_px[0]), Y(rect_px[1]), X(rect_px[2]), Y(rect_px[3])], 'rect_px': rect_px, 'kind': kind,
                     'cue_ids': [f'{a.plan}/plan-opening-cue-{q:02d}' for q in ids], 'rect_status': status,
                     'wall_overlap_fraction': round(float(cells.mean()) if cells.size else 0, 3),
                     'status': 'glazing position from approved 2D cue; window vs glazed door, sill and head UNVERIFIED (display defaults)'})

    # ---------- room label anchors + canonical records ----------
    # Every bold room-name label in the approved SVG, plus the two plain TERRACE labels; dims = the following size text.
    seq = list(g.iter(NS + 'text'))
    anchors = []
    norm = lambda s_: re.sub(r'[^a-z]', '', s_.lower())
    alias = {'kstore': 'kitchenstorage'}
    canon_by = {norm(r['label']): r for r in canon}
    for n_i, t in enumerate(seq):
        name = (t.text or '').strip()
        if not name or not (t.get('font-weight') == 'bold' or name in ('TERRACE', 'OUTDOOR TERRACE')):
            continue
        dim = None
        if n_i + 1 < len(seq):
            nxt = (seq[n_i + 1].text or '').strip()
            if re.match(r'^[\d.]+ × [\d.]+ m$', nxt) or nxt.startswith('UNKNOWN'): dim = nxt
        ax, ay = float(t.get('x')), float(t.get('y'))
        key = alias.get(norm(name), norm(name))
        cr = canon_by.get(key)
        sz = None
        if dim and dim[0].isdigit():
            sz = max(float(v) for v in re.findall(r'[\d.]+', dim)[:2])
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        anchors.append({'id': slug, 'name': name.title(), 'at': [X(ax), Y(ay)], 'at_px': [ax, ay],
                        'dims_label': dim or 'not stated', 'frame_m': sz or DISPLAY['room_flyto_frame_default_m'],
                        'frame_status': 'from transcribed label size (camera framing only)' if sz else 'display-only default framing',
                        'canonical_room_id': cr['room_id'] if cr else None,
                        'space_type': cr['space_type'] if cr else 'label_in_approved_V4_only',
                        'polygon': None,
                        'status': 'label anchor from approved V4; room boundary NOT delineated; dims are brochure transcript, not remeasured'})

    # ---------- water surfaces: only what the approved V4 fills with the pool-water gradient ----------
    water = []
    for wi_, q in enumerate(ch):
        if q.tag == NS + 'rect' and q.get('fill') == 'url(#pool)':
            x0, y0 = float(q.get('x')), float(q.get('y')); x1, y1 = x0 + float(q.get('width')), y0 + float(q.get('height'))
            holes = []
            for j2, q2 in enumerate(ch[wi_ + 1:], wi_ + 1):
                if q2.tag != NS + 'rect' or not q2.get('fill', '').startswith('#'): continue
                if j2 + 1 < len(ch) and ch[j2 + 1].tag == NS + 'text': continue      # label background, not geometry
                fc = q2.get('fill').lstrip('#'); rr, bb_ = int(fc[0:2], 16), int(fc[4:6], 16)
                if bb_ > rr + 20: continue   # water-tinted graphic (e.g. submerged steps/bench): water surface kept over it
                a0, b0 = float(q2.get('x')), float(q2.get('y')); a1, b1 = a0 + float(q2.get('width')), b0 + float(q2.get('height'))
                if x0 < a0 and a1 < x1 and y0 < b0 and b1 < y1 and not any(h[0] <= a0 and a1 <= h[2] and h[1] <= b0 and b1 <= h[3] for h in holes):
                    holes.append([a0, b0, a1, b1])
            lab = min(anchors, key=lambda a_: (a_['at_px'][0] - (x0 + x1) / 2) ** 2 + (a_['at_px'][1] - (y0 + y1) / 2) ** 2)
            inside_label = x0 <= lab['at_px'][0] <= x1 and y0 <= lab['at_px'][1] <= y1
            wid = 'swimming-pool' if inside_label and lab['id'] == 'swimming-pool' else f'courtyard-water-feature-{sum(1 for w_ in water if w_["id"] != "swimming-pool")+1}'
            water.append({'id': wid, 'svg_element_index_in_source_space': wi_, 'outline_px': [x0, y0, x1, y1],
                          'outer': [[X(x0), Y(y0)], [X(x1), Y(y0)], [X(x1), Y(y1)], [X(x0), Y(y1)]],
                          'holes': [[[X(h[0]), Y(h[1])], [X(h[2]), Y(h[1])], [X(h[2]), Y(h[3])], [X(h[0]), Y(h[3])]] for h in holes],
                          'holes_px': holes, 'size_m_approx': [round((x1 - x0) / ppm, 2), round((y1 - y0) / ppm, 2)],
                          'label': lab['name'] if inside_label else None,
                          'status': ('labelled pool; outline = approved V4 water rect (calibration span 9.50 x 2.40 m)' if wid == 'swimming-pool' else
                                     'unlabelled water feature drawn in approved V4 and visible in source crop (courtyard); inner planter island kept as hole')})
    matched = sorted(a_['canonical_room_id'] for a_ in anchors if a_['canonical_room_id'])
    missing = sorted(r['room_id'] for r in canon if r['room_id'] not in matched)

    W_mm, H_mm = X(bb_px[2]), Y(bb_px[3])
    plate = {'id': 'plate', 'name': 'Display floor plate (not a room)', 'poly': [[0, 0], [W_mm, 0], [W_mm, H_mm], [0, H_mm]], 'mat': 'tile800', 'counted': False, 'plate': True}
    # ---------- v2: derived room polygons, source furniture symbols, material evidence ----------
    rd_path = Path(a.readings) if a.readings else R / f'source-evidence/floorplan3d-readings/FP-{a.plan}.json'
    rd = json.loads(rd_path.read_text())
    from shapely.geometry import Polygon as _Poly
    an_by = {a_['id']: a_ for a_ in anchors}
    rooms_v2, rooms_detail = [], []
    # QA barrier = traced walls (dilated 3 crop px) + approved glazing/door openings (so glazed edges count as bounded)
    bar = __import__('scipy.ndimage', fromlist=['binary_dilation']).binary_dilation(mask, iterations=6)
    for o_ in list(wins) + list(doors):
        x0_, y0_, x1_, y1_ = o_['rect_px']
        bar[max(0, int((min(y0_, y1_) - 3) * SS)):int((max(y0_, y1_) + 3) * SS) + 1, max(0, int((min(x0_, x1_) - 3) * SS)):int((max(x0_, x1_) + 3) * SS) + 1] = True
    for rr in rd['rooms']:
        an = an_by[rr['anchor_id']]
        poly_px = rr['poly_px']; pg = _Poly(poly_px); assert pg.is_valid and pg.area > 0, rr['anchor_id']
        assert pg.buffer(1).contains(_Poly([(an['at_px'][0]-.5, an['at_px'][1]-.5), (an['at_px'][0]+.5, an['at_px'][1]-.5), (an['at_px'][0]+.5, an['at_px'][1]+.5), (an['at_px'][0]-.5, an['at_px'][1]+.5)])), f"label anchor outside polygon {rr['anchor_id']}"
        area_m2 = round(pg.area * k * k / 1e6, 2)
        # wall-fit QA: share of non-closure boundary within 3 crop px of a traced wall cell
        bnd, on = pg.exterior, []
        from shapely.geometry import LineString as _LS
        cls = [_LS([(c_['seg'][0], c_['seg'][1]), (c_['seg'][2], c_['seg'][3])]) for c_ in rr['closures_px']]
        for t_ in np.arange(0, bnd.length, .5):
            p_ = bnd.interpolate(t_)
            if any(c_.distance(p_) < 1.0 for c_ in cls): continue
            on.append(bool(bar[min(bar.shape[0]-1, int(round(p_.y * SS))), min(bar.shape[1]-1, int(round(p_.x * SS)))]))
        room = {'id': rr['anchor_id'], 'name': an['name'], 'poly': [[X(x_), Y(y_)] for x_, y_ in poly_px], 'mat': rr['mat'], 'at': an['at'],
                'counted': not rr['outdoor'], 'outdoor': rr['outdoor'], 'area_m2_derived': area_m2, 'mat_status': rr['mat_status']}
        rooms_v2.append(room)
        rooms_detail.append({**room, 'poly_px': poly_px, 'closures_px': rr['closures_px'], 'mat_evidence': rr['mat_evidence'], 'note': rr['note'],
                             'dims_label': an['dims_label'], 'polygon_status': 'DERIVED from traced V4 wall faces with doorway/opening closures - not stated in source',
                             'area_status': 'derived, approximate (~); calibration ±3%',
                             'qa_boundary_on_wall_or_opening_fraction_excl_closures': round(float(np.mean(on)), 3) if on else None})
        an['area_m2_derived'] = area_m2
    furn, furn_detail = [], []
    for f_ in rd['furniture']:
        w_px, d_px = f_['size_px_object_frame']
        if f_['type'] == 'toilet': w_mm, d_mm = 400, 650
        else: w_mm, d_mm = round(w_px * k), round(d_px * k)
        it_ = {'type': f_['type'], 'name': f_['name'], 'cx': X(f_['center_px'][0]), 'cy': Y(f_['center_px'][1]), 'w': w_mm, 'd': d_mm, 'rot': f_['rot']}
        if f_.get('color'): it_['color'] = f_['color']
        furn.append(it_); furn_detail.append({**it_, 'center_px': f_['center_px'], 'size_px_object_frame': f_['size_px_object_frame'], 'size_source': f_['size_source'], 'evidence': f_['evidence'], 'status': f_['status']})
    stairs = []
    for st_ in rd['stairs']:
        x0_, y0_, x1_, y1_ = st_['rect_px']
        stairs.append({'id': st_['id'], 'rect': [X(x0_), Y(y0_), X(x1_), Y(y1_)], 'treads': st_['treads'], 'rise_to': 'north', 'status': st_['status'], 'rise_direction': st_['rise_direction']})
    entry = next((a_ for a_ in anchors if a_['id'] == 'double-height-entry'), None)
    walk = {'pos': entry['at'], 'look': [entry['at'][0], entry['at'][1] - 3000], 'status': 'display-only start at the DOUBLE-HEIGHT ENTRY label anchor, facing plan-north'}
    diag = math.hypot(W_mm, H_mm) / 1000
    plan = {
        'plan_id': a.plan, 'units': 'mm', 'origin': 'top-left of traced wall bounding box; x right, y down (plan)',
        'px_per_m': ppm, 'mm_per_crop_px': k, 'origin_crop_px': [ox, oy],
        'WALL_BBOX_MM': [0, 0, W_mm, H_mm], 'OX': W_mm / 2, 'OY': H_mm / 2,
        'BOUNDS': (lambda ymin: {'x': -2000, 'y': ymin - 1800, 'w': W_mm + 4000, 'h': H_mm - ymin + 3600})(min([0] + [pt[1] for w_ in water for pt in w_['outer']])),
        'DIM_CHAINS': [[True, -900, 0, [W_mm]], [False, -900, 0, [H_mm]]],
        'DISPLAY': DISPLAY,
        'VIEW': {'iso': [diag * .36, diag * 1.0, diag * .65], 'top_dist': round(max(W_mm, H_mm) / 1000 / 2 / math.tan(math.radians(22.5)) * 1.12, 2)},
        'WALK_START': walk,
        'WALLS': walls, 'WINS': [w['rect'] for w in wins], 'DOORS': [{k_: d[k_] for k_ in ('name', 'rect', 'h', 'c', 'o', 'len')} for d in doors],
        'SLIDES': [], 'ROOMS': [plate] + rooms_v2, 'FURNITURE': furn, 'STAIRS': stairs,
        'WATER': [{k_: w_[k_] for k_ in ('id', 'outer', 'holes', 'label')} for w_ in water],
        'ANCHORS': [{k_: a_.get(k_) for k_ in ('id', 'name', 'at', 'dims_label', 'frame_m', 'canonical_room_id', 'area_m2_derived')} for a_ in anchors],
        'LABEL': 'Ashwood Estates 4B GF - Floorplan 3D spike - not survey-verified, not construction-ready, not certified CAD',
    }
    (OUT / 'data').mkdir(exist_ok=True)
    js = ('/* Generated by scripts/v4_to_floorplan3d.py from the approved V4 SVG. Do not hand-edit.\n'
          '   Not survey-verified, not construction-ready, not certified CAD. Approximate metres (+/-3%). */\n'
          f'const PLAN = {json.dumps(plan, ensure_ascii=False)};\n'
          'const R = (x0,y0,x1,y1) => [[x0,y0],[x1,y0],[x1,y1],[x0,y1]];\n'
          'const WALLS = PLAN.WALLS, WINS = PLAN.WINS, DOORS = PLAN.DOORS, SLIDES = PLAN.SLIDES, ROOMS = PLAN.ROOMS, ANCHORS = PLAN.ANCHORS;\n')
    (OUT / 'data/fp-4b-gf.plan.js').write_text(js)
    (OUT / 'data/fp-4b-gf.plan.json').write_text(json.dumps({'plan': plan, 'doors_detail': doors, 'glazing_detail': wins, 'anchors_detail': anchors, 'water_detail': water,
        'rooms_detail': rooms_detail, 'furniture_detail': furn_detail, 'skipped_furniture': rd['skipped_furniture'], 'stairs_detail': rd['stairs'],
        'no_polygon': rd['no_polygon'], 'readings_source': {'path': str(rd_path.relative_to(R)), 'sha256': sha(rd_path)},
        'method_rooms': rd['method_rooms'], 'method_furniture': rd['method_furniture'], 'furniture_convention': rd['furniture_convention']}, indent=1, ensure_ascii=False) + '\n')

    # ---------- vendor three.js (no CDN) ----------
    vend = OUT / 'vendor/three'
    files = ['build/three.module.js', 'examples/jsm/controls/OrbitControls.js', 'examples/jsm/controls/PointerLockControls.js',
             'examples/jsm/geometries/RoundedBoxGeometry.js', 'examples/jsm/environments/RoomEnvironment.js',
             'examples/jsm/renderers/CSS2DRenderer.js', 'examples/jsm/objects/Water2.js', 'examples/jsm/objects/Reflector.js',
             'examples/jsm/objects/Refractor.js', 'LICENSE']
    tpkg = json.loads((TH / 'package.json').read_text())
    assert tpkg['version'] == '0.160.0'
    for f in files:
        (vend / f).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(TH / f, vend / f)
    for f in files[1:-1]:
        for imp in re.findall(r"from\s+'([^']+)'", (vend / f).read_text()):
            assert imp == 'three' or (vend / f).parent.joinpath(imp).resolve().is_file(), f'unvendored import {imp} in {f}'
    texdir = vend / 'examples/textures/water'; texdir.mkdir(parents=True, exist_ok=True)
    tex_files = ['Water_1_M_Normal.jpg', 'Water_2_M_Normal.jpg']
    for f in tex_files:
        shutil.copy2(Path(a.three_textures) / f, texdir / f)
        assert (texdir / f).read_bytes()[:3] == b'\xff\xd8\xff', f'{f} is not a JPEG'

    # ---------- patch upstream viewer ----------
    src = (UP / 'index.html').read_text()
    up_sha = sha(UP / 'index.html')
    commit = subprocess.run(['git', '-C', str(UP), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    lic = (UP / 'LICENSE').read_text()
    assert lic.startswith('MIT License') and 'Copyright (c) 2026 wuyi' in lic
    shutil.copy2(UP / 'LICENSE', OUT / 'LICENSE-floorplan-3d.txt')
    s = src
    s = rep(s, '<!doctype html>', '<!doctype html>\n<!--\n  Floorplan 3D viewer - MIT License, Copyright (c) 2026 wuyi\n'
            f'  Upstream: https://github.com/wy51ai/floorplan-3d @ {commit}\n  Full licence text: LICENSE-floorplan-3d.txt (kept with this copy).\n'
            '  Modified for the Ashwood Estates plan pipeline by scripts/v4_to_floorplan3d.py:\n'
            '  demo apartment data replaced by approved-V4 traced data; three.js r160 vendored locally (MIT, vendor/three/LICENSE).\n'
            '  SPIKE - not survey-verified, not construction-ready, not certified CAD.\n-->', 1)
    s = rep(s, '"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js"', '"three":"./vendor/three/build/three.module.js"')
    s = rep(s, '"three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"', '"three/addons/":"./vendor/three/examples/jsm/"')
    # data: remove the demo apartment block, load generated data instead
    i0 = s.index('/* ============================================================\n *  户型数据')
    i1 = s.index('const MATS = {')
    s = s[:i0] + '/* Plan data (WALLS/WINS/DOORS/SLIDES/ROOMS/ANCHORS/PLAN) is loaded from data/fp-4b-gf.plan.js. */\n' + s[i1:]
    s = rep(s, '<script>\n/* ======================= 多语言', '<script src="data/fp-4b-gf.plan.js"></script>\n<script>\n/* ======================= 多语言')
    # English default + isolated storage keys (never load the demo's saved state)
    s = rep(s, "const LANG_KEY = 'huxing-lang';", "const LANG_KEY = 'ashwood-fp3d-spike-lang';")
    s = rep(s, "return LANGS.includes(l) ? l : 'zh'; } catch(e) { return 'zh'; }", "return LANGS.includes(l) ? l : 'en'; } catch(e) { return 'en'; }")
    s = rep(s, "const STORE = 'huxing-design-v1';", "const STORE = 'ashwood-fp3d-spike-4b-gf-v2';")
    s = rep(s, "const PANES = 'huxing-panes';", "const PANES = 'ashwood-fp3d-spike-panes';")
    # v2: furniture = upstream models placed ONLY where the approved V4 / brochure crop draws a symbol (PLAN.FURNITURE, evidence in plan.json)
    s = rep(s, 'function defaultFurniture(){ return [', 'function defaultFurniture(){ return PLAN.FURNITURE.map(f => F(f.type, f.name, f.cx, f.cy, f.w, f.d, f.rot, f.color)); }\nfunction upstreamDemoFurnitureUnused(){ return [')
    s = rep(s, 'const BOUNDS = {x:-1850, y:-1750, w:15600, h:14100};', 'const BOUNDS = PLAN.BOUNDS;')
    s = rep(s, '<b data-en="3BR 2LR 2BA · Interior Design">三室两厅两卫 · 装修设计</b><span id="subtitle">原始户型 1:60 · 尺寸单位 mm</span>',
            '<b data-en="Ashwood Estates · 4-Bed Villa · Ground Floor (3D spike)">Ashwood Estates · 4-Bed Villa · Ground Floor (3D spike)</b><span id="subtitle">SPIKE</span>')
    s = rep(s, "document.title = tr('户型装修设计', 'Floor Plan Designer');", "document.title = 'Ashwood 4B GF · Floorplan 3D spike';")
    s = rep(s, '<title>户型装修设计</title>', '<title>Ashwood 4B GF · Floorplan 3D spike</title>')
    # upstream treats every uncounted room as a raised 0.45 m bay-window seat; our display plate must stay a flat floor
    s = rep(s, 'const m = floorMat(state.rooms[r.id].mat), bay = r.counted === false;', 'const m = floorMat(state.rooms[r.id].mat), bay = r.bay === true;')
    s = rep(s, '    fl.receiveShadow = true; fl.userData.room = r.id;\n', '    fl.receiveShadow = true; fl.userData.room = r.id; if (r.plate) fl.position.y = PLAN.DISPLAY.plate_floor_offset_m;\n')
    s = rep(s, 'ceil.position.y = H; ceil.visible = top >= H; archUp.add(ceil);', 'ceil.position.y = H; ceil.visible = top >= H; if (!r.plate && !r.outdoor) archUp.add(ceil);')
    s = rep(s, '    if (r.at){\n      const lamp', '    if (r.at && !r.outdoor){\n      const lamp')
    # traced walls: own type, dark poche, removal disabled
    s = rep(s, "let fill = k==='b' ?", "let fill = k==='t' ? '#34403e' : k==='b' ?")
    s = rep(s, "  if (w[4]==='b') return toast(", "  if (w[4]==='t') return toast(tr('描摹墙体：结构类型未知，原型中禁止拆改', 'Traced source wall: structural type unknown - removal disabled in this spike'));\n  if (w[4]==='b') return toast(")
    # dimension chains: approximate overall traced-wall extents only
    i0 = s.index('    chain(true,-750,0,[1580,240,2760,240,1540,240,3670])')
    i1 = s.index("  g.setAttribute('display', ui.layers.dims ? 'inline' : 'none');")
    s = s[:i0] + "    PLAN.DIM_CHAINS.map(c => chain(...c)).join('');\n" + s[i1:]
    s = rep(s, "font-size=\"${v<400?140:200}\" text-anchor=\"middle\" fill=\"${DC}\" ${rot?`transform=\"rotate(-90 ${x} ${y})\"`:''}>${v}</text>`",
            "font-size=\"${v<400?140:260}\" text-anchor=\"middle\" fill=\"${DC}\" ${rot?`transform=\"rotate(-90 ${x} ${y})\"`:''}>~${v} mm (approx)</text>`")
    s = rep(s, "tr(`套内使用面积约 ${fmt(tot)} m² · 尺寸单位 mm · 原图比例 1:60`, `Net floor area ≈ ${fmt(tot)} m² · Units: mm · Original scale 1:60`)",
            "tr('阿什伍德 4B 首层 · 原型 · 单位 mm（近似）', 'Ashwood 4B GF · SPIKE · mm approx (calibration ±3%) · not survey-verified, not construction-ready, not certified CAD')")
    s = rep(s, "${fmt(perim(r.poly)*2.8,1)} m²`, `Wall area (2.8m ceiling, openings not deducted)",
            "${fmt(perim(r.poly)*PLAN.DISPLAY.wall_height_m,1)} m²`, `Wall area (display-only height, openings not deducted)")
    # 2D labels: source label anchors with transcribed sizes (no polygon areas)
    i0 = s.index('function renderLabels(){'); i1 = s.index('function renderDims(){')
    s = s[:i0] + '''function renderLabels(){
  const g = $('#gLabels');
  g.setAttribute('display', ui.layers.labels ? 'inline' : 'none');
  g.innerHTML = ANCHORS.map(r => {
    const [x,y] = r.at, halo = 'stroke="#fbf9f4" stroke-width="45" paint-order="stroke" stroke-linejoin="round"';
    return `<text x="${x}" y="${y}" font-size="230" font-weight="600" text-anchor="middle" fill="#2b2824" ${halo}>${esc(r.name)}</text>
      <text x="${x}" y="${y+240}" font-size="165" text-anchor="middle" fill="#7d7366" ${halo}>${esc(r.dims_label)}${r.area_m2_derived ? ' · ~' + r.area_m2_derived.toFixed(1) + ' m² derived' : ''}</text>`;
  }).join('');
}

''' + s[i1:]
    # overview panel: source room list instead of polygon areas / demo cost estimate
    i0 = s.index("  <section><h3>${tr('房间面积','Room Areas')}"); i1 = s.index("  <section><h3>${tr('方案统计','Plan Stats')}")
    s = s[:i0] + '''  <section><h3>Rooms <small>click to view / change flooring</small></h3>
    <table>${ROOMS.filter(r => !r.plate).map(r => { const st = state.rooms[r.id], an = ANCHORS.find(a => a.id === r.id);
      return `<tr class="click" data-room="${r.id}"><td><span class="sw" style="background:${MATS[st.mat].sw}"></span>${esc(st.name)}${r.outdoor ? ' <span class="muted">(outdoor)</span>' : ''}<br><small class="muted">label ${esc(an ? an.dims_label : '')} · floor ${esc(r.mat_status.startsWith('observed') ? 'observed' : 'assumed')}</small></td><td class="r">~${fmt(area(r.poly))} m²</td></tr>`; }).join('')}
      ${ANCHORS.filter(a => !ROOMS.find(r => r.id === a.id)).map(a => `<tr class="click" data-anchor="${a.id}"><td>${esc(a.name)} <span class="muted">(no polygon)</span></td><td class="r">${esc(a.dims_label)}</td></tr>`).join('')}</table>
    <div class="muted" style="font-size:11px;margin-top:4px">~ areas are DERIVED from traced walls with doorway closures (not stated in source). Labels are brochure transcripts. Floor finishes: observed = brochure text/renders (project-wide), assumed = no evidence.</div></section>
  <section><h3>Spike status</h3><div class="muted" style="font-size:11px">Walls/doors/glazing from approved V4 FP-4B-GF trace, approx 1:100 calibration (max residual 1.7%, ±3% working). Heights, sills and floor plate are display-only defaults. Not survey-verified, not construction-ready, not certified CAD.</div></section>
''' + s[i1:]
    s = rep(s, "  document.querySelectorAll('#panel tr[data-room]').forEach(tr => tr.onclick = () => { select({kind:'room', id:tr.dataset.room}); if (is3D()) window.View3D.flyToRoom(tr.dataset.room); });",
            "  document.querySelectorAll('#panel tr[data-room]').forEach(tr => tr.onclick = () => { select({kind:'room', id:tr.dataset.room}); if (is3D()) window.View3D.flyToRoom(tr.dataset.room); });\n"
            "  document.querySelectorAll('#panel tr[data-anchor]').forEach(tr => tr.onclick = () => { if (is3D()) window.View3D.flyToRoom(tr.dataset.anchor); });")
    # 3D constants
    s = rep(s, 'const OX = 6000, OY = 5300, H = 2.8, FOV = 45;', 'const OX = PLAN.OX, OY = PLAN.OY, H = PLAN.DISPLAY.wall_height_m, FOV = 45;')
    s = rep(s, "const opt = {cut:2.8,", "const opt = {cut:H,")
    s = rep(s, 'data-cut="2.8" data-en="Full walls"', 'data-cut="3" data-en="Full walls"')
    s = rep(s, 'data-cut="1.2" data-en="Cut walls"', 'data-cut="1.2" data-en="Cut walls"')
    assert DISPLAY['wall_height_m'] == 3.0 and DISPLAY['cut_wall_height_m'] == 1.2
    s = rep(s, '{left:-11, right:11, top:11, bottom:-11, near:1, far:60}', '{left:-PLAN.DISPLAY.shadow_extent_m, right:PLAN.DISPLAY.shadow_extent_m, top:PLAN.DISPLAY.shadow_extent_m, bottom:-PLAN.DISPLAY.shadow_extent_m, near:1, far:90}')
    s = rep(s, ', [[10270,800,10510,2600], 2.4], [[10270,4260,10510,5740], 2.4]]', ']')
    s = rep(s, '[...DOORS.map(d => [d.rect, 2.1]),', '[...DOORS.map(d => [d.rect, PLAN.DISPLAY.door_head_m]),')
    s = rep(s, "const sill = i === 0 ? 1.4 : i >= 6 ? .45 : .9, head = 2.4;", "const sill = PLAN.DISPLAY.glazing_sill_m, head = PLAN.DISPLAY.glazing_head_m;")
    s = rep(s, 'const isoWhole = () => pose(new THREE.Vector3(0, 0, 0), new THREE.Vector3(5.5, 15.5, 10));', 'const isoWhole = () => pose(new THREE.Vector3(0, 0, 0), new THREE.Vector3(...PLAN.VIEW.iso));')
    s = rep(s, 'const topWhole = () => pose(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 19, 1e-4));', 'const topWhole = () => pose(new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, PLAN.VIEW.top_dist, 1e-4));')
    s = rep(s, 'camera.position.set(wx(4200), 1.6, wz(8755)); camera.lookAt(wx(7000), 1.5, wz(8755));',
            'camera.position.set(wx(PLAN.WALK_START.pos[0]), PLAN.DISPLAY.walk_eye_height_m, wz(PLAN.WALK_START.pos[1])); camera.lookAt(wx(PLAN.WALK_START.look[0]), 1.5, wz(PLAN.WALK_START.look[1]));')
    # 3D labels + room list from source anchors
    i0 = s.index('function buildLabels(){'); i1 = s.index('// 只重建变化的部分')
    s = s[:i0] + '''function buildLabels(){
  labelG.children.slice().forEach(o => { o.element.remove(); labelG.remove(o); });
  ANCHORS.forEach(r => {
    const el = document.createElement('div'); el.className = 'rlabel';
    el.innerHTML = `${esc(r.name)}<small>${esc(r.dims_label)}${r.area_m2_derived ? ' · ~' + r.area_m2_derived.toFixed(1) + ' m²' : ''}</small>`;
    const o = new CSS2DObject(el); o.position.set(wx(r.at[0]), opt.cut + .15, wz(r.at[1])); o.visible = labelG.visible; labelG.add(o);
  });
  $('#roomList').innerHTML = ANCHORS.map(r => `<button data-room="${r.id}"><span>${esc(r.name)}</span><small>${esc(r.dims_label)}</small></button>`).join('')
    + `<button data-room="__all"><span>Whole floor</span><small>4B GF</small></button>`;
  document.querySelectorAll('#roomList button').forEach(b => b.onclick = () => {
    document.querySelectorAll('#roomList button').forEach(x => x.classList.toggle('on', x === b));
    if (opt.mode === 'walk') setMode('orbit');
    b.dataset.room === '__all' ? flyTo(isoWhole()) : flyToRoom(b.dataset.room);
  });
}

''' + s[i1:]
    s = rep(s, '''function flyToRoom(id){
  const r = ROOMS.find(r => r.id === id), xs = r.poly.map(p => p[0]), ys = r.poly.map(p => p[1]);''',
            '''function flyToRoom(id){
  const an = ANCHORS.find(a => a.id === id), hf = an ? an.frame_m*500 : 0;   // derived polygon if any, else display-only anchor framing
  const r = ROOMS.find(r => r.id === id) || (an ? {poly:R(an.at[0]-hf, an.at[1]-hf, an.at[0]+hf, an.at[1]+hf)} : null);
  if (!r) return;
  const xs = r.poly.map(p => p[0]), ys = r.poly.map(p => p[1]);''')
    # three.js Water2 on source water surfaces only (flat labelled fallback if Water2/WebGL2 fails or ?water=flat)
    s = rep(s, "import {CSS2DRenderer, CSS2DObject} from 'three/addons/renderers/CSS2DRenderer.js';",
            "import {CSS2DRenderer, CSS2DObject} from 'three/addons/renderers/CSS2DRenderer.js';\nimport {Water} from 'three/addons/objects/Water2.js';   // three.js r160 Water2 (MIT), vendored locally")
    s = rep(s, 'function buildArch(){', '''const WATER_MODE = new URLSearchParams(location.search).get('water') === 'flat' ? 'flat' : 'water2';
let waterState = {mode:null, count:0, error:null, surfaces:[]};
const waterTex = {};
function waterPath(pts){ return pts.map(([x, y]) => new THREE.Vector2(wx(x), -wz(y))); }
function buildWater(){
  waterState = {mode:null, count:0, error:null, surfaces:[]};
  (PLAN.WATER || []).forEach(w => {
    const s = shapeOf(w.outer); (w.holes || []).forEach(h => s.holes.push(new THREE.Path(waterPath(h))));
    const geo = new THREE.ShapeGeometry(s), D = PLAN.DISPLAY.water2;
    let mesh = null, mode = WATER_MODE;
    if (mode === 'water2'){
      try {
        if (!renderer.capabilities.isWebGL2) throw new Error('WebGL2 unavailable');
        const tl = new THREE.TextureLoader();
        waterTex.n0 ??= tl.load('vendor/three/examples/textures/water/Water_1_M_Normal.jpg');
        waterTex.n1 ??= tl.load('vendor/three/examples/textures/water/Water_2_M_Normal.jpg');
        mesh = new Water(geo, {color:D.color, scale:D.scale, flowDirection:new THREE.Vector2(...D.flowDirection), textureWidth:D.textureWidth, textureHeight:D.textureHeight, normalMap0:waterTex.n0, normalMap1:waterTex.n1});
      } catch(e){ waterState.error = String(e); mesh = null; }
    }
    if (!mesh){ mode = 'flat'; mesh = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({color:PLAN.DISPLAY.water_flat_fallback_color, roughness:.15, transparent:true, opacity:.92})); }
    mesh.rotation.x = -Math.PI/2; mesh.position.y = PLAN.DISPLAY.water_surface_y_m; mesh.userData.water = w.id; mesh.userData.waterMode = mode;
    archFloor.add(mesh);
    (w.holes || []).forEach(h => { const ig = new THREE.ShapeGeometry(shapeOf(h)); ig.rotateX(-Math.PI/2);
      const isl = new THREE.Mesh(ig, mat(PLAN.DISPLAY.island_display_colour, {roughness:.9})); isl.position.y = .02; archFloor.add(isl); });
    waterState.mode = mode; waterState.count++; waterState.surfaces.push({id:w.id, mode});
  });
  const fb = document.getElementById('waterBadge');
  if (fb) fb.textContent = waterState.count ? (waterState.mode === 'flat' ? 'Water: FLAT FALLBACK material (Water2 not used' + (waterState.error ? ': ' + waterState.error : '') + ')' : 'Water: three.js Water2 (r160, vendored)') + ' · ' + waterState.count + ' source surface(s)' : 'Water: none in source';
}
function buildArch(){''')
    s = rep(s, "  [...DOORS, ...SLIDES].forEach(d => { const [x0, y0, x1, y1] = d.rect;", "  buildWater(); buildStairs(top);\n  [...DOORS, ...SLIDES].forEach(d => { const [x0, y0, x1, y1] = d.rect;")
    s = rep(s, 'function buildArch(){', '''function buildStairs(top){   // DISPLAY-ONLY stair massing: tread count from the approved V4 tread lines; riser = display wall height / treads; rise direction ASSUMED
  const sm = mat(PLAN.DISPLAY.stair_material_colour, {roughness:.55});
  (PLAN.STAIRS || []).forEach(st => {
    const [x0, y0, x1, y1] = st.rect, n = st.treads, run = (y1 - y0)/n, rise = H/n;
    for (let i = 0; i < n; i++){
      const h = Math.min((i + 1)*rise, top), ya = y1 - (i + 1)*run, yb = y1 - i*run;
      const b = box(M(x1 - x0), h, M(yb - ya), sm, wx((x0 + x1)/2), 0, wz((ya + yb)/2)); b.castShadow = b.receiveShadow = true; archUp.add(b);
    }
    colliders.push([wx(x0), wz(y0), wx(x1), wz(y1)]);
  });
}
function buildArch(){''')
    s = rep(s, "const opt = {cut:H, furn:true, labels:true, night:false, hour:10,", "const opt = {cut:H, furn:true, labels:true, night:false, hour:PLAN.DISPLAY.sun_hour_default,")
    s = rep(s, 'id="sun" min="7" max="18" step=".25" value="10" style="width:84px"><span id="sunT">10:00</span>', 'id="sun" min="7" max="18" step=".25" value="16" style="width:84px"><span id="sunT">16:00</span>')
    # QA hook (read-only helpers for headless verification)
    s = rep(s, 'window.View3D = {enter, exit,', '''window.__FP3D_QA__ = {
  info: () => ({inited, active, mode:opt.mode, cut:opt.cut, walls:WALLS.length, wins:WINS.length, doorsData:DOORS.length, doors3d:doors.length, doorsOpen:doors.map(d => d.open), colliders:colliders.length, anchors:ANCHORS.length, labels:labelG ? labelG.children.length : 0, cam:camera ? camera.position.toArray() : null}),
  waterMeshes: () => archFloor.children.filter(o => o.userData.water).map(o => { const b = new THREE.Box3().setFromObject(o); return {id:o.userData.water, mode:o.userData.waterMode, verts:o.geometry.attributes.position.count, index:o.geometry.index ? o.geometry.index.count : 0, windingZ:(() => { const P = o.geometry.attributes.position, I = o.geometry.index; const out = []; for (let t = 0; t < I.count; t += 3){ const a = I.getX(t), b = I.getX(t+1), c = I.getX(t+2); out.push(Math.sign((P.getX(b)-P.getX(a))*(P.getY(c)-P.getY(a)) - (P.getY(b)-P.getY(a))*(P.getX(c)-P.getX(a)))); } return out; })(), visible:o.visible, min:b.min.toArray(), max:b.max.toArray()}; }),
  topOrtho(fovDeg = 1){ cancelAnimationFrame(raf); raf = 0; fly = null; const B = PLAN.BOUNDS, b = [B.x, B.y, B.x+B.w, B.y+B.h], cx = (b[0]+b[2])/2, cy = (b[1]+b[3])/2;
    const visH = Math.max((b[3]-b[1]), (b[2]-b[0])*SH()/SW())/1000*1.02, D = visH/2/Math.tan(fovDeg/2*Math.PI/180);
    camera.fov = fovDeg; camera.far = D*3; camera.near = D*.5; camera.updateProjectionMatrix(); camera.up.set(0,0,-1);
    camera.position.set(wx(cx), D, wz(cy)); camera.lookAt(wx(cx), 0, wz(cy)); renderer.render(scene, camera);
    return {cx, cy, visH_m:visH, canvasW:renderer.domElement.width, canvasH:renderer.domElement.height}; },
  restore(){ camera.fov = FOV; camera.near = .05; camera.far = 300; camera.up.set(0,1,0); camera.updateProjectionMatrix(); startLoop(); },
  toggleDoor(i){ doors[i].open = !doors[i].open; return doors[i].open; },
  png: () => renderer.domElement.toDataURL('image/png'),
  furniture: () => ({state:state.furniture.length, meshes:furnG.children.length, plan:PLAN.FURNITURE.length}),
  rooms: () => ROOMS.map(r => ({id:r.id, mat:state.rooms[r.id].mat, area:+area(r.poly).toFixed(2)})),
  look(p, t, fovDeg = 55){   // p,t = [plan x mm, plan y mm, height m]; display camera for hero screenshots
    fly = null; camera.fov = fovDeg; camera.near = .05; camera.far = 300; camera.up.set(0,1,0); camera.updateProjectionMatrix();
    camera.position.set(wx(p[0]), p[2], wz(p[1])); orbit.target.set(wx(t[0]), t[2], wz(t[1])); camera.lookAt(orbit.target); orbit.update(); return camera.position.toArray(); },
  setCut(c){ opt.cut = c; document.querySelectorAll('[data-cut]').forEach(b => b.classList.toggle('on', +b.dataset.cut === c)); buildArch(); return opt.cut; },
  settle(){   // stop the render loop and finish any enter/fly animation (headless capture only)
    cancelAnimationFrame(raf); raf = 0; if (anim){ anim.fn(1); const r = anim.res; anim = null; r(); } if (fly){ camTween(fly.A, fly.B, 1); fly = null; }
    grow = 1; furnGrow = 1; applyGrow(); doors.forEach(d => { d.cur = d.open ? d.a1 : d.a0; d.pivot.rotation.y = d.cur; }); return true; },
  still(){ this.settle(); orbit.update(); lampFace(); renderer.render(scene, camera); return {png:renderer.domElement.toDataURL('image/png'), w:renderer.domElement.width, h:renderer.domElement.height}; },
  furn(v){ furnG.visible = v; return v; },
  labels(v){ labelG.visible = v; labelG.children.forEach(o => { o.visible = v; o.element.style.display = v ? '' : 'none'; }); return v; },
};
window.View3D = {enter, exit,''')
    # ceiling lamp discs are one-sided like the ceilings: hide them when the camera is above the ceiling (bird's-eye), keep them from inside
    s = rep(s, '  updateSel();\n  renderer.render(scene, camera);', '  updateSel(); lampFace();\n  renderer.render(scene, camera);')
    s = rep(s, 'function startLoop(){', 'function lampFace(){ const below = camera.position.y < H - .05; lampG.children.forEach(o => { if (!o.isPointLight) o.visible = below && opt.cut >= H; }); }\nfunction startLoop(){')
    s = rep(s, '</body>', '<div id="spikeBanner" style="position:fixed;left:50%;transform:translateX(-50%);bottom:6px;z-index:99;background:rgba(52,64,62,.9);color:#fff;font:11px/1.3 sans-serif;padding:4px 10px;border-radius:4px;pointer-events:none">Ashwood 4B GF · Floorplan 3D SPIKE (MIT viewer) · approx ±3% · NOT survey-verified · NOT construction-ready · NOT certified CAD</div>\n</body>')
    s = rep(s, "anchors:ANCHORS.length, labels:", "anchors:ANCHORS.length, water:waterState, labels:")
    s = rep(s, '<div id="spikeBanner"', '<div id="waterBadge" style="position:fixed;right:8px;bottom:6px;z-index:99;background:rgba(40,90,110,.9);color:#fff;font:11px/1.3 sans-serif;padding:4px 8px;border-radius:4px;pointer-events:none">Water: (3D view only)</div>\n<div id="spikeBanner"')
    assert 'cdn.jsdelivr' not in s and 'https://' not in s.split('<script type="importmap">')[1].split('</script>')[0]
    (OUT / 'index.html').write_text(s)

    # ---------- manifest ----------
    (OUT / 'adapter').mkdir(exist_ok=True)
    shutil.copy2(Path(__file__), OUT / 'adapter/v4_to_floorplan3d.py')
    out_files = sorted(str(q.relative_to(OUT)) for q in OUT.rglob('*') if q.is_file() and 'verify' not in q.parts and 'v1' not in q.relative_to(OUT).parts and q.name != 'manifest.json')
    man = {
        'spike_id': 'floorplan3d-spike/FP-4B-GF', 'status': 'REVIEW_PENDING_SPIKE_NOT_APPROVED',
        'created_at_Asia_Dubai': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
        'label': 'not survey-verified, not construction-ready, not certified CAD',
        'scope': 'ONE floor (4B GF) only; other eight floors not converted',
        'sources': {
            'original_pdf': {'path': act['original_source'], 'sha256': sha(orig_pdf)},
            'approved_v4_svg': {'path': p['svg'], 'sha256': sha(svg_path), 'active_pipeline_sha256_match': True},
            'calibration': {'path': str(cal_path.relative_to(R)), 'sha256': sha(cal_path), 'fit_px_per_m': ppm,
                            'max_abs_span_residual_percent': cal['max_abs_span_residual_percent'], 'working_uncertainty_percent': cal['working_uncertainty_percent']},
            'canonical_rooms_index': {'path': 'canonical/rooms_index.json', 'sha256': sha(R / 'canonical/rooms_index.json')},
            'canonical_floors_index': {'path': 'canonical/floors_index.json', 'sha256': sha(R / 'canonical/floors_index.json')},
            'source_crop': {'path': p['source_crop'], 'sha256': sha(R / p['source_crop'])},
            'upstream_viewer': {'repo': 'https://github.com/wy51ai/floorplan-3d', 'commit': commit, 'index_html_sha256': up_sha,
                                'license': 'MIT', 'copyright': 'Copyright (c) 2026 wuyi', 'license_copy': 'LICENSE-floorplan-3d.txt'},
            'three_js': {'package': 'three@0.160.0 (npm registry tarball)', 'license': 'MIT, Copyright © 2010-2023 three.js authors', 'license_copy': 'vendor/three/LICENSE',
                         'files_sha256': {f: sha(vend / f) for f in files}},
            'three_js_water2': {'module': 'examples/jsm/objects/Water2.js (+ Reflector.js, Refractor.js) from three@0.160.0', 'upstream_reference': 'https://github.com/mrdoob/three.js/blob/r160/examples/jsm/objects/Water2.js',
                                'normal_maps': {f'examples/textures/water/{f}': {'source': f'https://raw.githubusercontent.com/mrdoob/three.js/r160/examples/textures/water/{f}', 'sha256': sha(texdir / f)} for f in tex_files},
                                'license': 'MIT (three.js authors)', 'cdn_used': False},
        },
        'conversion_parameters': {
            'wall_source': 'structural_wall_poche group (13 contours, translate(.5,.5), stroke 0.5, evenodd) rasterised with cairosvg',
            'raster_supersampling': SS, 'raster_cell_mm': round(k / SS, 2), 'rect_decomposition': 'greedy, lossless at raster cell (verified)',
            'px_per_m': ppm, 'mm_per_crop_px': k, 'origin_crop_px': [ox, oy], 'traced_wall_bbox_crop_px': bb_px,
            'traced_wall_extent_mm_approx': [W_mm, H_mm],
            'counts': {'wall_rects': len(walls), 'doors': len(doors), 'glazing': len(wins), 'room_anchors': len(anchors), 'room_polygons': len(rooms_v2), 'furniture_items': len(furn), 'furniture_skipped': len(rd['skipped_furniture']), 'stairs_display_only': len(stairs), 'water_surfaces': len(water)},
            'water_surfaces': [{k_: w_[k_] for k_ in ('id', 'svg_element_index_in_source_space', 'outline_px', 'holes_px', 'size_m_approx', 'label', 'status')} for w_ in water],
            'canonical_rooms_matched': matched, 'canonical_rooms_missing': missing,
            'anchors_without_canonical_record': [a_['name'] for a_ in anchors if not a_['canonical_room_id']],
        },
        'display_only_defaults': DISPLAY,
        'version': 'v2 (2026-11-09) - rebuilt after user feedback that v1 looked 2D; v1 kept in v1/ for comparison',
        'v2_changes': ['derived room polygons (doorway closures) with ~areas, per-room floor materials with evidence status',
                       'upstream furniture models placed only at approved-V4 / brochure-crop furniture symbols (evidence per item)',
                       'full-height walls (3.0 m display-only) default; shadows + RoomEnvironment reflections + warm daylight (sun 16:00 display-only)',
                       'room ceilings + ceiling lamps re-enabled for derived rooms (not plate/outdoor)', 'display-only stair massing (16 treads from V4; rise direction assumed)'],
        'rooms': {'method': rd['method_rooms'], 'readings': {'path': str(rd_path.relative_to(R)), 'sha256': sha(rd_path)},
                  'items': [{k_: r_[k_] for k_ in ('id', 'name', 'area_m2_derived', 'dims_label', 'mat', 'mat_status', 'mat_evidence', 'closures_px', 'polygon_status', 'qa_boundary_on_wall_or_opening_fraction_excl_closures', 'note')} for r_ in rooms_detail],
                  'no_polygon': rd['no_polygon']},
        'furniture': {'method': rd['method_furniture'], 'convention': rd['furniture_convention'],
                      'items': [{k_: f_[k_] for k_ in ('type', 'name', 'w', 'd', 'rot', 'status', 'evidence')} for f_ in furn_detail], 'skipped': rd['skipped_furniture']},
        'stairs': stairs,
        'not_from_source': ['all heights (walls, doors, glazing sill/head, stair risers)', 'floor plate', 'walk start pose', 'camera framing', 'material colours / textures (upstream procedural)',
                            'door leaf thickness/handle', 'glazing mullion spacing (upstream rule)', 'room polygons (derived with closures)', 'furniture 3D models (generic upstream models, sizes approx)',
                            'sun time/direction (site orientation unknown)', 'stair rise direction'],
        'not_converted': ['pool depth/coping (water surface only)', 'landscape, trees, cars', 'lift as a shaft (floor + label only)', 'site boundary', 'corridor / stair-hall polygons (unlabelled; plate floor)',
                          'double-height void (ceiling drawn at display wall height)'],
        'viewer_modifications': 'see index.html header + README; patches applied by exact-match string replacement (fail on mismatch)',
        'outputs': {f: sha(OUT / f) for f in out_files},
    }
    (OUT / 'manifest.json').write_text(json.dumps(man, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(man['conversion_parameters']['counts']), 'walls bbox mm', W_mm, H_mm, 'missing', missing)

if __name__ == '__main__':
    main()
