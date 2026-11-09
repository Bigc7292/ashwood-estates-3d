"""Step 3 blockout, RF walls as boxes (new file).

Input: data/rf_wall_mask_1x.png (from rf_wall_extract.py), 1 px = 35.53 mm (GF value, ASSUMPTION for RF).
Output: data/rf_walls_boxes.json, boxes in mm relative to the wall bbox origin (x right, y down),
plus a lossless check that the boxes re-render to the mask.
Greedy rectangle decomposition: runs per row, then merge identical runs down the rows.
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
DATA = ROOT / 'active/floorplan3d-spike/FP-4B-RF/data'
MM = 35.53012869683798

mask = np.array(Image.open(DATA / 'rf_wall_mask_1x.png').convert('L')) < 128
ys, xs = np.where(mask)
x0, y0 = xs.min(), ys.min()
m = mask[y0:ys.max() + 1, x0:xs.max() + 1]
H, W = m.shape

boxes = []
open_rects = {}  # (xa, xb) -> start row
for y in range(H + 1):
    row = m[y] if y < H else np.zeros(W, dtype=bool)
    runs = set()
    if y < H:
        x = 0
        while x < W:
            if row[x]:
                s = x
                while x < W and row[x]:
                    x += 1
                runs.add((s, x))
            else:
                x += 1
    for r in list(open_rects):
        if r not in runs:
            boxes.append((r[0], open_rects.pop(r), r[1], y))
    for r in runs:
        if r not in open_rects:
            open_rects[r] = y

rec = np.zeros_like(m)
for xa, ya, xb, yb in boxes:
    rec[ya:yb, xa:xb] = True
assert (rec == m).all(), 'box decomposition not lossless'

out = {
    'units': 'mm',
    'origin': 'top-left of RF wall bbox; x right, y down',
    'mm_per_px': MM,
    'scale_status': 'ASSUMPTION: GF value (Colin 2026-11-09 18:40)',
    'wall_bbox_px_in_crop': [int(x0), int(y0), int(xs.max() + 1), int(ys.max() + 1)],
    'box_count': len(boxes),
    'boxes_mm': [[round(xa * MM), round(ya * MM), round(xb * MM), round(yb * MM)] for xa, ya, xb, yb in boxes],
    'lossless_check': 'boxes re-render to the wall mask exactly',
}
(DATA / 'rf_walls_boxes.json').write_text(json.dumps(out))
print('boxes', len(boxes), 'bbox px', H, W, 'lossless ok')
