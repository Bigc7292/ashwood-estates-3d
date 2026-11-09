# V3 correction — partial vector prototype, not nine completed drawings

Checked 2026-11-09 05:50 Asia/Dubai (UTC+4).

## Outcome
One materially improved, source-constrained vector prototype: **4-bedroom villa / ground floor**, brochure page 27. Eight floors have NOT been redrawn in V3. Do not report the nine-plan brief complete.

## What changed
- Read the actual supplied watermarked example; used its muted green/blue palette, dark wall emphasis, white sheet and side information-panel concept only. No reference geometry, measurements, north, scale or watermark copied.
- Started directly from original PDF embedded image xref313, not the damaged/rejected panels. Canonical decoded crop is verified against the PDF.
- New SVGs contain **no embedded raster**. Separate source-classified structural wall contours, white furniture silhouettes, fine doors/stairs/glazing details, parking/vehicles, landscape and water-feature contours. They are vector traces of a raster source, NOT clean semantic native CAD.
- Digitized continuous source opening strokes and 15 observed stair tread rows. Replaced source labels with legible text and source-stated room-size table. Maid-room dimensional typo/conflict is flagged rather than guessed.
- Retained neutral/low-saturation tree canopy silhouettes and exterior overhangs; no broad colour-to-white knockout treatment. Pool uses a closed blue base with subtle traced texture, not destructive colour removal.
- White margins, title, complete footer, legend and provenance panel are outside the plan. No invented perimeter dimension chains or scale bar.
- Both a full-plan image and presentation sheet are rendered at 7680px long edge from SVG. Source architecture still originates in a 710×1020 crop of a 2360×1667 embedded board; 7680 rendering adds no measured architectural evidence.

## Checks performed on the actual output
- Visually opened full presentation sheet, source-versus-vector comparison and standalone full plan.
- Source input pixels match direct original-PDF JPEG decode.
- SVG parses, contains zero raster image elements.
- Actual rendered pool interior: zero white knockout pixels.
- Actual rendered text bounds: zero spans outside sheet.
- Rendered vector-wall mask vs the source-selected wall mask: IoU 0.9857. This measures tracing of the selected pixels only, NOT semantic correctness, world-coordinate accuracy or survey validation.
- Rooms/labels accounted for: swimming pool, living/dining, show kitchen, pantry, powder, kitchen, laundry, storage, office/gym, bath, entrance, multipurpose, dress, maid room, maid bath, lift. Source terraces, stairs, two parking cars and three entrances are retained.

## Remaining work / limitation
- All eight other floors remain unredrawn in V3: 4B-FF/RF, 5B-GF/FF/RF, 6B-GF/FF/RF.
- First prototype still has irregular fine furniture/vehicle contours and weak/approximate minor fixtures inherited from the low-resolution raster. It is not yet the polished fully semantic architectural redraw the user originally expected; not native DXF/DWG or construction-ready.
- To reach that standard without inventing detail, manually regularize source-confirmed linework and verify every opening/furnishing; higher-resolution source or original CAD would remove ambiguity. Do not fabricate missing detail from the style sample.
- The source has no usable native wall-vector layer. Brochure plan pages are marketing raster boards plus overlaid labels/sidebar graphics; source-stated room dimensions do not establish a calibrated overall drawing.

## Reproduction
From archive root:
```
.venv/bin/python cad-redraw-v3/scripts/build_verified_prototype.py
.venv/bin/python cad-redraw-v3/scripts/verify_prototype.py
```

## Preview paths
- `cad-redraw-v3/png/FP-4B-GF_vector_prototype_review.png` — sheet, dimensions table and limitations.
- `cad-redraw-v3/previews/FP-4B-GF_full_plan_review.png` — standalone full plan.
- `cad-redraw-v3/previews/FP-4B-GF_source_vs_vector.png` — same-coordinate source comparison.

Originals and V1/V2 are preserved. No ZIP was rebuilt/delivered. No 3D work was performed.
