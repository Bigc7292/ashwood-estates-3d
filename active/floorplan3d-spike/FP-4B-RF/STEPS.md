# FP-4B-RF: 4-bed villa roof floor, 7-step gate log

Lane: Build villa roof floor in 3D (branch `lane/roof-floor`). Status: step 1 and 2 logged; step 3 blocked. Not survey-verified, not construction-ready, not certified CAD.

## Step 1 Reference: GATE LOGGED, PASS WITH NOTES
- Inputs: `active/approved-cad-v4/svg/FP-4B-RF_V4_portrait.svg`, `active/approved-cad-v4/png/FP-4B-RF_V4_preview.png`, `source-evidence/plan-crops/FP-4B-RF_untouched_board_crop.png`. Listed in `ACTIVE_PIPELINE.json` as 4B-RF (approval `pt16u`).
- Brochure interior reference (p15 to p17, p24) is the same set the GF viewer used: `FP-4B-GF/README.md`.
- Note 1: the sheet's own legend reads "UNAPPROVED / NOT SURVEY CAD" and "NOT TO SCALE · NO METRIC SCALE BAR". The pipeline registers it as approved, so the sheet's wording is treated as a presentation label, not an approval change. Colin to confirm.
- Note 2: the sheet states the roof floor area as 43.92 m². Roof floor room labels are read from the sheet, not from the brochure.
- Status: PASS WITH NOTES (Colin to confirm note 1).

## Step 2 Layout: PASS (dimension check, method validated; overlay not possible)
- Scale: 35.53 mm per crop px. GF value, applied to RF as an ASSUMPTION (Colin 2026-11-09 18:40: "THE SCALE SHOULD BE LIKE THE GROUND FLOOR").
- RF walls extracted exactly from the approved sheet, group `source_wall_poche` (11 paths): `adapter/rf_wall_extract.py`, output `data/rf_walls_summary.json`, `data/rf_wall_mask_1x.png`.
- Method check on GF: the same extraction gives 14541 x 22997 mm against 14550 x 23006 mm in `FP-4B-GF/data/fp-4b-gf.plan.json`. Under 0.3 px.
- Wall bounding boxes at 35.53 mm/px:
  - GF: 14.54 x 23.00 m (plan json 14.55 x 23.01)
  - FF: 13.58 x 24.95 m (group `source_wall_poche`, 26 paths)
  - RF: 13.51 x 22.82 m (group `source_wall_poche`, 11 paths)
- RF fits inside the GF and FF envelope on both axes. This is consistent, not proven: each sheet is a separate crop with its own frame, so no shared origin exists and a true overlay can't be made from the sheets alone.
- Stated RF labels (sheet text, not traced): LIFT 1.60 x 1.80 m; POWDER 1.50 x 2.40 m; PANTRY 2.00 x 2.40 m; MEP 3.80 x 15.70 m (corrected: this is the MEP label, not a roof run); TERRACE UNKNOWN; FLOOR AREA 43.92 m2.
- Sheet legend "UNAPPROVED / NOT SURVEY CAD" logged as a presentation label; the sheet is approved in ACTIVE_PIPELINE.json (pt16u).

## Step 3 Blockout: BLOCKED ON ROOM OUTLINES (decision needed)
- Walls as boxes: done (165 boxes, lossless; `data/rf_walls_boxes.json`).
- Room outlines: NOT DERIVABLE from the sheet. A flood fill of the free space on the wall mask (`rf_wall_mask_1x.png`) finds one open region. Every room label (LIFT, POWDER, PANTRY, TERRACE, MEP) falls inside it. The sheet itself marks the envelope as "ENVELOPE UNKNOWN" on all four sides, so the RF walls do not close any room.
- Furniture: 12 seat rects in 4 clusters, 3 seat circles, about 10 small rects in source_diagram. Not mapped to items. The "Existing furniture" legend swatch is needed.
- Options for Colin (decision requested):
  1. Build room outlines as ASSUMED rectangles from the label sizes (LIFT 1.60 x 1.80 m, POWDER 1.50 x 2.40 m, PANTRY 2.00 x 2.40 m), placed at the label points. Labelled ASSUMED throughout. Low evidence; the critic will flag it.
  2. Colin supplies the RF room outlines or envelope.
- Status: BLOCKED pending that decision.

## Steps 4 to 7: NOT STARTED
- Step 4 Grime / finish, step 5 Printed matter, step 6 Critique (independent critic, side-by-side with brochure p15 to p17 and V4 RF plan), step 7 Motion.
- Furniture comes from the labelled place markers on the approved RF sheet (not yet extracted).
- Viewer target: match `FP-4B-GF/` v2 in rooms, furniture, materials and lighting.

## Loop tracker
Loop 1. Current step: 3 (blocked on room outlines; decision requested).
