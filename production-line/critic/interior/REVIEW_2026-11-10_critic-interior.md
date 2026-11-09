# Interior critic review, loop 1 (lane/critic-interior)

Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
Critic lane: independent of all builders. Writes only in this folder. Nothing in the lanes was edited.
Date: 2026-11-10 (Asia/Dubai). Checked against the approved V4 plans in `active/approved-cad-v4/` and the brochure reference set.

## Verdicts

| Lane | Branch | Step reviewed | Verdict | Earliest step to loop back to | One fix (priority order) |
|---|---|---|---|---|---|
| Ground floor | lane/gf-interior-step7 (r3 build, `verify/r3_2026-11-10/`) | 6 Critique | **PASS with one labelling fix**. Visual items pass; the walk speed is an unsourced number | 7 Motion (proceed) | Label the walk speed 3.2 / 7.0 m/s as ASSUMPTION (Colin can overrule) in `index_r3.html` and the step 7 plan, then proceed to step 7. Not a blocker (coordinator ruling, 2026-11-09 23:37 UTC). |
| First floor | lane/first-floor (r5L, step 2) | 2 Layout | **FAIL** | 2 Layout | Separate the 14 room polygons from the wall outlines. The flood fill is still leaking through doorways. Close the doorway gaps first, then re-run the per-room check at 35.53 mm/px. |
| Roof floor | lane/roof-floor (step 3 started) | 2 Layout (passed), 3 Blockout (in progress) | **REVIEW-PENDING**. Nothing to pass yet at step 3 | 3 Blockout | Finish the wall-box decomposition and place the rooms. Send the built blockout for review. |

## Ground floor: detail

Sheets checked (4 of 17): `sbs_living-dining_rev`, `f2_before_after_f2_entry_void_up`, `q7_courtyard_from_living`, plus the reference board `ref_board_p15_p16_p17_p24`. The other sheets were not reviewed in this pass.

- **Living-dining, layout:** the room sits in the approved V4 GF polygon (12.40 x 5.10 m, label on plan). Dining, sofa, island and pool view are placed in the right zones. PASS.
- **Living-dining, look:** warm stone wall, porcelain floor and a sliding-glass pool wall match the p15 reference style. PASS.
- **F2 entry travertine:** the radial streak artefact from the before render is gone in the after render. The 6.0 m void lining is labelled as an assumption in the sheet. PASS.
- **Q7 courtyard:** the bonsai-form pine now matches the approved concept image. The pond sits in the plan's pond outline. PASS. Note: the long low timber bench from the concept is not visible in the after render. This is not a blocking fix. Add it only if Colin wants the concept bench.
- **Walk speed (step 7 gate):** the 3.2 / 7.0 m/s values have no source. Under AGENTS.md rule 2 they must be labelled as assumption. Coordinator ruling: label as an assumption Colin can overrule, and proceed to step 7. This is the one labelling fix.

## First floor: detail

- The step log (`active/floorplan3d-spike/FP-4B-FF/STEPS.md`, lane/first-floor) says step 2 is still blocked on doorway closures. The r5L file fixes label anchors only.
- The scale of 35.53 mm/px is an ASSUMPTION, labelled as such. The envelope check gives +2.8% width and -4.0% height. Logged, not fixed.
- The per-room check puts the polygons 1 to 5% above the stated sizes, with Bedroom 1 and Bedroom 2 depth about 12% over. Logged as an assumption. Not yet resolved.
- `standalone_r4.html` (the earlier FAIL) still has missing partitions and overhanging floor plates. The r5L file has not been viewed in this pass. Step 2 must pass before any viewer review.
- Outside r6/r7 files at 34.03 mm/px are not applied. Correct.

## Roof floor: detail

- Step 2 PASS (dimension method, not an overlay). Method check on GF reproduces the plan json to under 0.3 px. The RF wall bounding box is 13.51 x 22.82 m, inside the GF and FF envelope. This is consistent, not proven.
- Legend wording, recorded: the approved RF sheet's own legend says "UNAPPROVED / NOT SURVEY CAD" and "NOT TO SCALE". Coordinator ruling (2026-11-09 23:37 UTC): treat the RF sheet as approved. These are generated pre-start CAD plans (per Colin in the project chat), not surveyor drawings. Scale comes from the GF calibration at 35.53 mm/px.
- Scale 35.53 mm/px for RF is an ASSUMPTION, set by Colin's instruction (2026-11-09 18:40). Labelled.

## Open items for the integrator
1. GF: add the walk-speed ASSUMPTION label, then proceed to step 7. Lane: lane/gf-interior-step7.
2. FF: step 2 must pass again after the doorway-closure fix. Lane: lane/first-floor.
3. RF: no step 6 until step 3 and 4 are built. Lane: lane/roof-floor.
4. RF legend wording recorded; sheet treated as approved per coordinator ruling.

## Evidence
- Sheets: `active/floorplan3d-spike/FP-4B-GF/verify/r3_2026-11-10/sbs/` on lane/gf-interior-step7 (sbs_living-dining_rev.jpg, f2_before_after_f2_entry_void_up.jpg, q7_courtyard_q7_courtyard_from_living.jpg, ref_board_p15_p16_p17_p24.jpg).
- Plans: `active/approved-cad-v4/png/FP-4B-GF_V4_preview.png`, `FP-4B-FF_V4_preview.png`, `FP-4B-RF_V4_preview.png`.
