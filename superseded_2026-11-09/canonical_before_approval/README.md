# Ashwood stage-1 canonical evidence index

Start at `project_index.json`. Paths are relative to `/workspace/plan-visuals-archive`; move the archive root as a unit for portability. Existing originals, extracts, room SOURCE.txt files and previous drawing versions remain unchanged.

## Organization
- `villas/{4b,5b,6b}/floors/{gf,ff,rf}/index.json`: source page/xref/crop, source and drawing paths, floor description, room records, geometry QA and scale status.
- `rooms_index.json`: stable project/villa/floor/room IDs, source-label descriptions, room-local reference anchors and uncertainties.
- `references/`: three extracted brochure visual panels plus factual style/material evidence. These are **not** matched room images or newly generated visuals.
- `handoff/missing_interior_visuals.json` and `.csv`: one unassigned placeholder view per interior/service space; `generated_available=false` independently of source matching status.
- `handoff/drawing_geometry_QA.json`: bounded all-nine source-versus-output checks and unresolved opening/stair detail.
- `unresolved_legacy_room_labels.json`: old page-level labels, including potentially spurious headers/duplicates, not auto-merged or assigned invented floors.

## Facts, missing assets and inference
135 canonical entries are room/space records, including exterior pools/terraces/balconies; they are NOT 135 verified room polygons. `source_label_reference_bbox` is an approximate LABEL box in the embedded board's native pixels—not a room boundary. Floor assignment comes from the visually identified floor panel. Ceiling heights, camera poses, exact openings and room polygons are not established.

Existing legacy `rooms/` folders contain text references only. There are **no individual room plan crops or verified room-to-interior-photo matches**. A missing view means no VERIFIED room-specific file, not proof that the brochure lacks a potentially relevant view. Source candidates remain ambiguous/unassigned.

Page 15 supplies dressing/living examples; page 16 is a BEDROOM (correcting a legacy kitchen classification); page 17 provides project-wide illustrated material alternatives. Same-villa exterior pages are context only. Do not claim generic project interiors belong to a particular villa/floor/room. A later generator may logically propose coherent decor using these factual cues, but must label inferred decor and never promote it to source evidence or alter unknown geometry.

## Drawing and scale status
Nine source-limited vector presentation sheets are exported, not native/survey CAD. All nine comparisons were visually checked at presentation level. Some source-faint door/glazing/tread strokes remain weak/incomplete; geometry QA is REVIEW REQUIRED. Do not silently treat them as detailed verified CAD.

All source-stated numeric exterior lengths are missing. UNKNOWN exterior chains are schematic source wall-alignment guides, not verified plot bounds. No scale is inferred from floor/plot areas.

A separate **4B GF approximate calibration-derived 1:100 A2 SVG/PDF** is available under `cad-redraw-v3/final/calibration/`. It uses eight explicit room/pool spans, 1.7% maximum fit residual, and a conservative ±3% working allowance. Print A2 420×594 mm at 100% / actual size, no fit. That does NOT make the plan survey accurate. The other eight remain NTS: one demonstrated conflicting overlay/board case and seven not independently validated. PNG zoom is never a fixed print scale.

## Ready / blocked
Ready: evidence review, file navigation and proposed evidence-led decor briefs.
Blocked: claiming source-matched room interiors, exact room polygons, certified openings/stair dimensions, fully dimensioned metric perimeters or faithful construction/3D reconstruction.

No interior images generated, no bot contacted, no 3D started, no ZIP delivered. The separate stage-2 bot is listed only as a handoff destination; the parent controls any transfer.
