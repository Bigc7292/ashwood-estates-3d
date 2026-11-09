# Right view (ELEV-RIGHT): 7-step gate log

View: EXT-4b-ELEV-RIGHT. Page: `walk_exterior_wip/right_pass.html` (own page; overrides `overrides/right_*.js`). Locked camera: `right_lock.json` (never moves). Builder: lane 2 cloud builder. Critic: independent critic thread, one fix per pass.
Shared heights: the branch's M25-SET values (tower 11.6 m, model FF level) so both exterior builders agree; "delegated by Colin" for M25-SET not yet confirmed by Colin.
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

| Step | Inputs | Outputs | Review check | Status |
|---|---|---|---|---|
| 1 Reference | `step1_reference/generated_approved/EXT-4b-ELEV-RIGHT_GENERATED-CONCEPT.png` | locked camera `right_lock.json`, `shots/right_lock_side_by_side.png` | critic: framing rows and ends match | DONE (critic: lock PASS, 3ce23e6) |
| 2 Layout | approved V4 CAD via `model/data/model.js` | right facade, slab z 2.84-26.88 | ends match at the locked camera | DONE (inherited footprint), pending critic |
| 3 Blockout | steps 1 + 2 | pass 1 RF canopy, pass 2 RF block hidden, pass 3 thin canopy, pass 4 boundary wall | critic, one fix per pass | IN PROGRESS (loop 1) |
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
- Step 3 pass 4 (this commit): boundary wall rebuilt as a 1.8 m travertine wall with coping on the CAD line (x 18.72-18.97), verge paving and context lawn beyond (`overrides/right_pass4_boundary_wall.js`). Residual for the critic: on the CAD line the wall top lands at side-by-side row ~388, not the reference's ~425. The reference's wall base sits ~67 px below the CAD ground row, so matching row 425 on the CAD line would mean a 0.64 m wall (derived). CAD line and 1.8 m height kept (1.8 m = assumption, same as the left view's travertine wall). Awaiting critic.
