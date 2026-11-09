# FP-4B-RF: 4-bed villa roof floor, 7-step gate log

Lane: Build villa roof floor in 3D (branch `lane/roof-floor`). Status: step 1 and 2 logged; step 3 blocked. Not survey-verified, not construction-ready, not certified CAD.

## Step 1 Reference: GATE LOGGED, PASS WITH NOTES
- Inputs: `active/approved-cad-v4/svg/FP-4B-RF_V4_portrait.svg`, `active/approved-cad-v4/png/FP-4B-RF_V4_preview.png`, `source-evidence/plan-crops/FP-4B-RF_untouched_board_crop.png`. Listed in `ACTIVE_PIPELINE.json` as 4B-RF (approval `pt16u`).
- Brochure interior reference (p15 to p17, p24) is the same set the GF viewer used: `FP-4B-GF/README.md`.
- Note 1: the sheet's own legend reads "UNAPPROVED / NOT SURVEY CAD" and "NOT TO SCALE · NO METRIC SCALE BAR". The pipeline registers it as approved, so the sheet's wording is treated as a presentation label, not an approval change. Colin to confirm.
- Note 2: the sheet states the roof floor area as 43.92 m². Roof floor room labels are read from the sheet, not from the brochure.
- Status: PASS WITH NOTES (Colin to confirm note 1).

## Step 2 Layout: GATE PARTLY PASSED (scale set; footprint alignment pending)
- Scale DECIDED (Colin, 2026-11-09 18:40): "THE SCALE SHOULD BE LIKE THE GROUND FLOOR". Use the GF value, 35.53 mm per crop px (px_per_m 28.145), applied to the RF sheet as an ASSUMPTION. It is not a calibration from the RF sheet.
- Still to do: check that the RF outline aligns with the FF and GF footprints at this scale. Not yet done.
- Room list (from sheet labels): POWDER, PANTRY, LIFT, TERRACE, and the roof-floor room set on the sheet. Dimensions carry the sheet's own dagger flags (†) and are not verified.
- Scale: GF viewer uses px_per_m = 28.145 (35.53 mm per crop px), derived from the GF sheet calibration in `FP-4B-GF/data/fp-4b-gf.plan.json`. The RF sheet has no metric scale bar and states "Independent source spans conflict or reliable endpoints are unavailable; no calibration forced." So the RF scale is NOT established. Using 35.53 mm/px for RF is an ASSUMPTION until a calibration from the RF sheet itself is found.
- Status: scale set. Footprint alignment check is the next item.

## Step 3 Blockout: NOT STARTED
Waits on the footprint alignment check in step 2.

## Steps 4 to 7: NOT STARTED
- Step 4 Grime / finish, step 5 Printed matter, step 6 Critique (independent critic, side-by-side with brochure p15 to p17 and V4 RF plan), step 7 Motion.
- Furniture comes from the labelled place markers on the approved RF sheet (not yet extracted).
- Viewer target: match `FP-4B-GF/` v2 in rooms, furniture, materials and lighting.

## Loop tracker
Loop 1. Current step: 2 (scale set; footprint alignment pending).
