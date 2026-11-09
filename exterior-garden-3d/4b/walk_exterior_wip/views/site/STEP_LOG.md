# Site/aerial view (OUTDOOR-SITE): 7-step gate log

View: EXT-4b-OUTDOOR-SITE. Page: `walk_exterior_wip/site_pass.html` (own page, copied from right_pass.html without the right overrides; overrides `overrides/site_*.js`). Locked camera: `site_lock.json` (never moves). Builder: lane 2 cloud builder. Critic: independent critic thread, one fix per pass.
Shared heights: the branch's M25-SET values (tower 11.6 m, model FF level); "delegated by Colin" for M25-SET not yet confirmed by Colin.
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

| Step | Inputs | Outputs | Review check | Status |
|---|---|---|---|---|
| 1 Reference | `step1_reference/generated_approved/EXT-4b-OUTDOOR-SITE_GENERATED-SOURCE-CONDITIONED.png` | locked camera `site_lock.json`, `shots/site_lock_side_by_side.png` | critic: plot corners match | DONE (critic: lock PASS, plot accepted as anchor, 72ce002) |
| 2 Layout | approved V4 CAD via `model/data/model.js` | whole plot, house, carport, pool | plot corners match at the locked camera | pending |
| 3 Blockout | steps 1 + 2 | pass 1 RF block hidden | critic, one fix per pass | IN PROGRESS (loop 1) |
| 4 Grime / finish | | | | NOT STARTED |
| 5 Printed matter | OUTDOOR-SITE | | Q1 record | to check |
| 6 Critique | | | | NOT STARTED |
| 7 Motion | | | | NOT STARTED |

## Pass history
- Lock (this commit): camera solved on the 4 CAD plot corners (residuals 9-12 px). Known conflict (M42): the generated image is not metrically consistent with the CAD; the house roof and the carport cannot be matched together with the plot. Plot kept as the anchor (CAD decides dimensions). The model also shows the RF block (grey) that the reference does not show (same kind as M26/M33). Critic: PASS, plot accepted as the anchor; scale gap to be logged with numbers (done in M42).
- Step 3 pass 1 (this commit): RF walls/roof hidden and rf-canopy removed in this view (`overrides/site_pass1_hide_rf_block.js`), as M26/M33. Note: the page's view-comment line was missing from the lock commit (stripped with the right overrides); restored with this pass. Awaiting critic.
