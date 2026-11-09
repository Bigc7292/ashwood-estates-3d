"""Extract RF structural walls from the approved V4 SVG, at the GF scale.

Method (same as FP-4B-GF/adapter/v4_to_floorplan3d.py): take the approved
poche group exactly, rasterise its paths, then measure the bounding box.
Validated on GF: this method gives 14541 x 22997 mm against 14550 x 23006 mm
in FP-4B-GF/data/fp-4b-gf.plan.json (difference under 0.3 px; stroke ignored).

RF group: id="source_wall_poche", 11 path elements (ElementTree parse).
Each <path> is filled even-odd inside itself, then the paths are unioned.
Scale: 35.53 mm per crop px = GF value (Colin 2026-11-09 18:40).
ASSUMPTION for RF: no RF-specific calibration exists.
New files only.
"""
import json, re
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[4]
SVG = ROOT / 'active/approved-cad-v4/svg/FP-4B-RF_V4_portrait.svg'
OUT = ROOT / 'active/floorplan3d-spike/FP-4B-RF/data'
MM = 35.53012869683798
SS = 4
CW, CH = 480, 795  # RF board crop, ACTIVE_PIPELINE.json source_board_crop_pixels [1820,455,2300,1250]


def group_paths(svg, gid):
    root = ET.parse(svg).getroot()
    for el in root.iter():
        if el.get('id') == gid:
            return [c.get('d') for c in el.iter() if c.tag.endswith('path') and c.get('d')]
    raise KeyError(gid)


def rasterise(ds, cw, ch):
    acc = np.zeros((ch * SS, cw * SS), dtype=bool)
    for d in ds:
        elem = np.zeros_like(acc)
        for sub in re.findall(r'M[^M]*', d):
            pts = [tuple(map(float, q.split(','))) for q in re.findall(r'-?\d+\.?\d*,-?\d+\.?\d*', sub)]
            if len(pts) < 3:
                continue
            pts = [((x + 0.5) * SS, (y + 0.5) * SS) for x, y in pts]
            layer = Image.new('1', (cw * SS, ch * SS), 0)
            ImageDraw.Draw(layer).polygon(pts, fill=1)
            elem ^= np.array(layer, dtype=bool)
        acc |= elem
    return acc


if __name__ == '__main__':
    ds = group_paths(SVG, 'source_wall_poche')
    acc = rasterise(ds, CW, CH)
    ys, xs = np.where(acc)
    x0, y0, x1, y1 = xs.min() / SS, ys.min() / SS, (xs.max() + 1) / SS, (ys.max() + 1) / SS
    OUT.mkdir(parents=True, exist_ok=True)
    m1 = acc.reshape(CH, SS, CW, SS).any(axis=(1, 3))
    Image.fromarray(np.where(m1, 0, 255).astype('uint8')).save(OUT / 'rf_wall_mask_1x.png')
    res = {
        'source': 'active/approved-cad-v4/svg/FP-4B-RF_V4_portrait.svg, id source_wall_poche (%d paths)' % len(ds),
        'method': 'same as FP-4B-GF/adapter/v4_to_floorplan3d.py; validated on GF (14541 x 22997 mm vs plan json 14550 x 23006)',
        'mm_per_crop_px': MM,
        'scale_status': 'ASSUMPTION: GF value (Colin 2026-11-09 18:40); no RF-specific calibration',
        'wall_bbox_crop_px': [round(x0, 2), round(y0, 2), round(x1, 2), round(y1, 2)],
        'wall_bbox_mm': [round((x1 - x0) * MM), round((y1 - y0) * MM)],
    }
    (OUT / 'rf_walls_summary.json').write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))
