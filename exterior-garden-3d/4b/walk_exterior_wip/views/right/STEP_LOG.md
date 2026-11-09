# Right view (ELEV-RIGHT): 7-step gate log

View: EXT-4b-ELEV-RIGHT. Page: `walk_exterior_wip/right_pass.html` (own page; overrides `overrides/right_*.js`). Locked camera: `right_lock.json` (never moves). Builder: lane 2 cloud builder. Critic: independent critic thread, one fix per pass.
Shared heights: the branch's M25-SET values (tower 11.6 m, model FF level) so both exterior builders agree; "delegated by Colin" for M25-SET not yet confirmed by Colin.
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

| Step | Inputs | Outputs | Review check | Status |
|---|---|---|---|---|
| 1 Reference | `step1_reference/generated_approved/EXT-4b-ELEV-RIGHT_GENERATED-CONCEPT.png` | locked camera `right_lock.json`, `shots/right_lock_side_by_side.png` | critic: framing rows and ends match | DONE (critic: lock PASS, 3ce23e6) |
| 2 Layout | approved V4 CAD via `model/data/model.js` | right facade, slab z 2.84-26.88 | ends match at the locked camera | DONE (inherited footprint), pending critic |
| 3 Blockout | steps 1 + 2 | pass 1 RF canopy | critic, one fix per pass | IN PROGRESS (loop 1) |
| 4 Grime / finish | | | | NOT STARTED |
| 5 Printed matter | ELEV-RIGHT | | Q1 record | to check |
| 6 Critique | | | | NOT STARTED |
| 7 Motion | | | | NOT STARTED |

## Pass history
- Lock (103ccf4): critic FAIL, right end solved to the rear overhang (x 1120) instead of the main wall end.
- Lock re-solve (this commit): ends 143 / 1033, camera pos (42.6, 1.6, 13.45), target (15.88, 4.66, 13.45). Critic: lock PASS.
- Step 3 pass 1 (this commit): RF canopy moved to the reference columns (z 3.2-8.4, this view only, M36: ELEV-LEFT and ELEV-RIGHT disagree on where the roof element sits). Awaiting critic.
