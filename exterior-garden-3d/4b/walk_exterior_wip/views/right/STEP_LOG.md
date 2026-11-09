# Right view (ELEV-RIGHT): 7-step gate log

View: EXT-4b-ELEV-RIGHT. Page: `walk_exterior_wip/right_pass.html` (own page; overrides `overrides/right_*.js`). Locked camera: `right_lock.json` (never moves). Builder: lane 2 cloud builder. Critic: independent critic thread, one fix per pass.
Shared heights: the branch's M25-SET values (tower 11.6 m, model FF level) so both exterior builders agree; "delegated by Colin" for M25-SET not yet confirmed by Colin.
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

| Step | Inputs | Outputs | Review check | Status |
|---|---|---|---|---|
| 1 Reference | `step1_reference/generated_approved/EXT-4b-ELEV-RIGHT_GENERATED-CONCEPT.png` | locked camera `right_lock.json`, `shots/right_lock_side_by_side.png` | critic: framing rows and ends match | DONE (critic: lock PASS, 3ce23e6) |
| 2 Layout | approved V4 CAD via `model/data/model.js` | right facade, slab z 2.84-26.88 | ends match at the locked camera | DONE (inherited footprint), pending critic |
| 3 Blockout | steps 1 + 2 | pass 1 RF canopy, pass 2 RF block hidden, pass 3 thin canopy, pass 4 boundary wall, pass 5 rear overhang, pass 6 entrance recess, pass 7 recess head, pass 8 GF entry, pass 9 wall entry + steps, pass 10 trunk out of entry | critic, one fix per pass | IN PROGRESS (loop 1) |
| 4 Grime / finish | | | | NOT STARTED |
| 5 Printed matter | ELEV-RIGHT | | Q1 record | to check |
| 6 Critique | | | | NOT STARTED |
| 7 Motion | | | | NOT STARTED |

## Pass history
- Lock (103ccf4): critic FAIL, right end solved to the rear overhang (x 1120) instead of the main wall end.
- Lock re-solve (this commit): ends 143 / 1033, camera pos (42.6, 1.6, 13.45), target (15.88, 4.66, 13.45). Critic: lock PASS.
- Step 3 pass 1 (this commit): RF canopy moved to the reference columns (z 3.2-8.4, this view only, M36: ELEV-LEFT and ELEV-RIGHT disagree on where the roof element sits). Critic (86c4d87): canopy PASS; next fix the RF block.
- Step 3 pass 2 (this commit): RF walls/roofs hidden in this view (as M26/M33). Residual: the canopy now reads as a big floating slab seen from below (top ~137, underside to ~215 in the panel) vs the reference's thin slab (~154-180). Critic (7ad022f): RF block PASS; next fix flatten the canopy.
- Step 3 pass 3 (this commit): canopy as a thin 0.30 m slab, top 9.13 m, x 11.94-14.93 (derived from the reference's edge-top and soffit rows), columns kept. Critic: PASS; next fix the boundary wall (top at row ~425).
- Step 3 pass 4 (this commit): boundary wall rebuilt as a 1.8 m travertine wall with coping on the CAD line (x 18.72-18.97), verge paving and context lawn beyond (`overrides/right_pass4_boundary_wall.js`). Residual for the critic: on the CAD line the wall top lands at side-by-side row ~388, not the reference's ~425. The reference's wall base sits ~67 px below the CAD ground row, so matching row 425 on the CAD line would mean a 0.64 m wall (derived). CAD line and 1.8 m height kept (1.8 m = assumption, same as the left view's travertine wall). Critic: PASS with the residual accepted; logged as M37.
- RESIDUAL FOR COLIN (M37): the right boundary wall top sits at side-by-side row ~388 vs the reference's ~425 (reference wall base ~67 px below the CAD ground row). CAD line and 1.8 m height kept. Same kind of drift as the left view (~30 px base drift).
- Step 3 pass 5 (this commit): lower rear overhang beyond the main wall end (`overrides/right_pass5_rear_overhang.js`): slab x 7.1-15.85, z 0.53-2.84, y 6.91-7.38, all derived from the reference rows/columns at the locked camera. The CAD draws no slab here, so it is an image-read assumption for this view (M38). Side-by-side: fascia at rows ~235-250 and right end at x ~838, on the reference's ~235-252 and ~840. Critic: PASS.
- Step 3 pass 6 (this commit): FF entrance recess moved 2.35 m toward the street (65 px at 0.0361 m/px, derived) to the reference columns, same 4.22 m size: opening z 15.03-19.25 (`overrides/right_pass6_entry_recess.js`). CAD wall lines kept; stone skin over z 12.68-15.03, ff-wall-72 trimmed to start at 19.25, cross-wall stub ff-wall-70 hidden in this view (M39). Side-by-side: opening x ~320-435 vs the reference ~320-415 (the extra ~20 px is the kept CAD width). Critic: PASS, M39 accepted.
- Step 3 pass 7 (this commit): stone head over the FF entrance recess, z 15.03-19.25, y 6.29-7.4 (top of glazing at side-by-side row ~265, derived), `overrides/right_pass7_recess_head.js`. Open residual noted by the critic: the lower lit GF entry glazing (rows ~370-430) is still missing; later pass. Critic: PASS.
- Step 3 pass 8 (this commit): GF entry glazing as a flat warm lit panel (MAT timber_lit) at z 15.78-19.19, y 0.34-2.49 (derived from the reference rows/columns), `overrides/right_pass8_gf_entry.js`. Columns ~320-415 match. Only the part above the CAD-line boundary wall (rows ~370-388) shows: the reference sees the entry through an opening in the boundary wall (steps at rows ~460-515), which the model lacks. Critic: PASS.
- Step 3 pass 9 (this commit): opening in the boundary wall at z 15.68-18.55 (reference columns ~320-410 on the wall's outer face, derived) with 3 steps + a 0.60 m landing (0.15 m risers, assumption) on the verge in front (`overrides/right_pass9_wall_entry.js`, M40). The opening follows the reference COLUMNS, not its wall height: the wall keeps the CAD line and 1.8 m (M37), so the step rows (~425-445) sit above the reference's ~460-515 by the same ground drift. A plan tree trunk shows through the opening. Critic: FAIL on that trunk only; rest PASS.
- Step 3 pass 10 (this commit): plan tree tree-9's trunk moved +0.55 m in z (18.476 -> 19.03, display shift, this view only, logged with M40) so it sits behind the wall beyond the opening edge; canopy kept (`overrides/right_pass10_tree_out_of_entry.js`). Opening now clear. Awaiting critic.
