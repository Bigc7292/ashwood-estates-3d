# Right view (ELEV-RIGHT): 7-step gate log

View: EXT-4b-ELEV-RIGHT. Page: `walk_exterior_wip/right_pass.html` (own page; overrides `overrides/right_*.js`). Locked camera: `right_lock.json` (never moves). Builder: lane 2 cloud builder. Critic: independent critic thread, one fix per pass.
Shared heights: the branch's M25-SET values (tower 11.6 m, model FF level) so both exterior builders agree; "delegated by Colin" for M25-SET not yet confirmed by Colin.
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

| Step | Inputs | Outputs | Review check | Status |
|---|---|---|---|---|
| 1 Reference | `step1_reference/generated_approved/EXT-4b-ELEV-RIGHT_GENERATED-CONCEPT.png` | locked camera `right_lock.json`, `shots/right_lock_side_by_side.png` | critic: framing rows and ends match | REVIEW-PENDING |
| 2 Layout | approved V4 CAD via `model/data/model.js` | right facade, slab z 2.84-26.88 | ends match at the locked camera | DONE (inherited footprint), pending critic |
| 3 Blockout | | | critic, one fix per pass | NOT STARTED |
| 4 Grime / finish | | | | NOT STARTED |
| 5 Printed matter | ELEV-RIGHT | | Q1 record | to check |
| 6 Critique | | | | NOT STARTED |
| 7 Motion | | | | NOT STARTED |

## Pass history
- Lock (this commit): camera solved and locked, awaiting critic.
