# Hand-off: 4B first floor interior viewer (lane 3-interior, first floor)

Status: REVIEW-PENDING. Walls only. Not survey-verified, not construction-ready, not certified CAD.

## What was built
- New viewer folder: `active/floorplan3d-spike/FP-4B-FF/` (index.html, data/, vendor/three/). GF viewer v2 is untouched.
- Walls: rasterised from the approved V4 `FP-4B-FF_V4_portrait.svg` `source_wall_poche` group (2 px per crop px), decomposed into 1014 axis-aligned rectangles.
- Scale: mm = crop px x 35.53 (approx, taken from the 4B-GF calibration, assumed the same board scale). Bounding box about 11849 x 21762 mm (GF: 14550 x 23006 mm).
- Viewer renders in 2D and 3D (checked headless, no page errors).

## Not done (NOT FOUND in source, nothing invented)
- Rooms: no FF room polygons or names. Room list shows "Whole floor" only.
- Furniture: none. No FF furniture readings exist.
- Doors and glazing: none. The V4 FF door and glazing cues were not extracted.
- Stair: the GF stair massing is carried over as display-only. Its FF position is NOT verified against the FF source.
- Courtyard, GF polish WIP: out of scope for this hand-off.

## Evidence
- Plan data: `active/floorplan3d-spike/FP-4B-FF/data/fp-4b-ff.plan.json`
- Source SVG hash: see `ACTIVE_PIPELINE.json` (4B-FF sha256.svg `927be9ea0c48d6410e960189c6fdc17d8f3a35d2ed20ef1942882aceb3246ba4`)

## Next
- Critic review of wall fidelity vs the FF source (`active/approved-cad-v4/qa/FP-4B-FF_source_vs_v4.png`).
- Room and stair readings for FF, then doors and glazing.
