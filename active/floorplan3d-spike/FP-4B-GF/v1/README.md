# Ashwood Estates: 4-bed villa, ground floor. Floorplan 3D viewer spike (FP-4B-GF)

**Status: REVIEW-PENDING SPIKE. One floor only.** Not survey-verified, not construction-ready, not certified CAD.

This is an offline, walkable 3D view of the approved V4 FP-4B-GF plan. It runs in the open-source Floorplan 3D viewer, with three.js Water2 used on the two water surfaces drawn in the source plan. No other floor has been converted.

## Use
```bash
cd active/floorplan3d-spike/FP-4B-GF
python3 -m http.server 8000 --bind 127.0.0.1   # then open http://127.0.0.1:8000/
```
Everything loads from this folder: no CDN, no network, no account. ES modules need an http server, so `file://` won't work.

- **2D Plan / 3D Scene** switch is at the top. You can also press `T`.
- **Room list** (left) and **Source rooms** table (right): click a name to fly the camera there. The camera frames the label anchor; no room boundaries are drawn.
- **Walk**: on a computer, click the overlay, then use WASD and the mouse. On touch devices, use the joystick at the bottom left and drag to look. Walking starts at the Double-Height Entry label, facing plan-north.
- **Doors**: click or tap a door, or press `E` while walking, to open or close it. The 6 doors are the swing-door symbols drawn in V4.
- **Full / Cut walls**: wall height 3.0 m or 1.2 m. Both are display-only values.
- **Water**: three.js Water2 by default. `index.html?water=flat` forces the labelled flat-material fallback. The badge at the bottom right shows which mode is active.

## What comes from the source, and what doesn't
| Element | Origin |
|---|---|
| Walls (587 rectangles) | Approved V4 `structural_wall_poche` (13 traced contours), rasterised exactly at 0.5 crop-px (~17.8 mm) and split into rectangles with no loss. Coordinates are crop px ÷ 28.145 px/m (approx 1:100 calibration, max residual 1.7 %, ±3 % working allowance). |
| Doors (6) | V4 swing-door symbols (leaf line + arc): hinge, swing side and leaf width. Door type and height are unverified. |
| Glazing (12) | V4 glazing guide lines. Whether each is a window or a glazed door, and its sill and head heights, are unverified (display defaults). |
| Water (2) | The two V4 rects filled with the pool-water gradient: the **Swimming Pool** (9.49 × 2.38 m approx; brochure label 9.50 × 2.40) and an **unlabelled courtyard water feature** (4.16 × 3.70 m approx) that is also visible in the source crop. The central planter (1.42 m square approx) is a hole in that water. Depth, coping and steps are not modelled. |
| Rooms (18 labels) | V4 label anchors plus the size text from brochure labels. All 16 canonical 4B-GF rooms matched. TERRACE and OUTDOOR TERRACE have no canonical record. **No room polygons or areas**, because the approved trace has open doorways and doesn't close any room boundary. |
| Floor plate | Display-only: the bounding box of the traced walls. It is not a slab or room outline. |
| Heights, sills, colours, sun, walk start, camera framing | Display-only defaults, listed in `manifest.json → display_only_defaults`. |

Not converted: stairs (no tread or riser data), lift shaft (label only), landscape, cars, furniture symbols and site boundary. The furniture library is the upstream generic set, and no furniture is placed. The upstream ¥ material prices are demo values and are not used in the overview.

## Files
- `index.html`: the patched upstream viewer, with the attribution header kept.
- `data/fp-4b-gf.plan.js` / `.plan.json`: generated plan data plus per-element provenance. `data/wall_mask_2x.png` is the wall raster.
- `vendor/three/`: three.js r160 (`three.module.js`, OrbitControls, PointerLockControls, RoundedBoxGeometry, RoomEnvironment, CSS2DRenderer, **Water2 + Reflector + Refractor**, and the water normal maps `examples/textures/water/Water_1_M_Normal.jpg` and `Water_2_M_Normal.jpg`) plus its LICENSE.
- `adapter/v4_to_floorplan3d.py`: a copy of the reusable adapter (canonical copy: `scripts/v4_to_floorplan3d.py`). It is locked to `--plan 4B-GF` until the spike is approved.
- `manifest.json`: source paths and hashes, conversion parameters, display defaults and output hashes.
- `verify/`: headless verification output (`verification.json`) and screenshots. Produced by `scripts/verify_floorplan3d_spike.py`.

Regenerate and verify (from the archive root):
```bash
.venv/bin/python scripts/v4_to_floorplan3d.py
.venv/bin/python scripts/verify_floorplan3d_spike.py
```

## Attribution (MIT)
- **Floorplan 3D**, https://github.com/wy51ai/floorplan-3d (commit recorded in the manifest). MIT License, Copyright (c) 2026 wuyi. Full text: `LICENSE-floorplan-3d.txt`. The demo apartment data was removed and replaced with Ashwood V4 data. Patches are listed in the adapter.
- **three.js r160**, including `examples/jsm/objects/Water2.js`, `Reflector.js`, `Refractor.js` and the `examples/textures/water` normal maps. MIT License, Copyright © 2010-2023 three.js authors. Full text: `vendor/three/LICENSE`. The JS comes from the npm `three@0.160.0` tarball. The normal maps come from the three.js `r160` git tag, because the npm package doesn't ship textures.

**Not survey-verified, not construction-ready, not certified CAD.** All metric values are approximate (±3 %).
