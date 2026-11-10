"""Step 3 rooms as ASSUMED rectangles (new file).

Source: the RF sheet does not close its envelope (marked ENVELOPE UNKNOWN), so no room
outline can be derived from the walls. Working default (coordinator, Colin's loop rule):
each labelled room is a rectangle centred on its label point, sized from the label.
Every room is ASSUMED. Open ruling for Colin: see STEPS.md.
Scale: 35.53 mm per px (GF value, ASSUMPTION for RF).
Origin: top-left of the RF wall bbox (same as rf_walls_boxes.json).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DATA = ROOT / 'active/floorplan3d-spike/FP-4B-RF/data'
MM = 35.53012869683798
walls = json.loads((DATA / 'rf_walls_boxes.json').read_text())
bx, by = walls['wall_bbox_px_in_crop'][0], walls['wall_bbox_px_in_crop'][1]

# label point (sheet text coords, same space as the wall paths), label size in m (sheet text)
ROOMS = [
    ('LIFT', (321, 291), (1.60, 1.80)),
    ('POWDER', (223, 520), (1.50, 2.40)),
    ('PANTRY', (268, 519), (2.00, 2.40)),
    ('MEP', (134, 421), (3.80, 15.70)),
]
out = []
for name, (cx, cy), (w_m, h_m) in ROOMS:
    w_px, h_px = w_m * 1000 / MM, h_m * 1000 / MM
    x0, y0 = cx - w_px / 2, cy - h_px / 2
    x1, y1 = cx + w_px / 2, cy + h_px / 2
    out.append({
        'name': name,
        'status': 'ASSUMED (rectangle at label point, label size; not a traced outline)',
        'box_mm': [round((x0 - bx) * MM), round((y0 - by) * MM), round((x1 - bx) * MM), round((y1 - by) * MM)],
        'size_m': [w_m, h_m],
    })
# TERRACE: label has no size ("UNKNOWN"), so it is not drawn.
(DATA / 'rf_rooms_assumed.json').write_text(json.dumps({
    'units': 'mm', 'origin': 'top-left of RF wall bbox; x right, y down', 'mm_per_px': MM,
    'scale_status': 'ASSUMPTION: GF value (Colin 2026-11-09 18:40)',
    'rooms': out, 'not_drawn': ['TERRACE (no size on sheet)'],
}, indent=1))
for r in out:
    print(r['name'], r['box_mm'])
