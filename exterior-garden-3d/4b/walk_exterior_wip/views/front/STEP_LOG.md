# Front view (ELEV-FRONT): 7-step gate log

View: EXT-4b-ELEV-FRONT. Locked camera: `../../cameras/front_lock.json` (never moves). Builder: lane 2 (exterior). Critic: independent critic thread, one fix per pass.
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

| Step | Inputs | Outputs | Review check | Status |
|---|---|---|---|---|
| 1 Reference | `step1_reference/generated_approved/EXT-4b-ELEV-FRONT_GENERATED-SOURCE-CONDITIONED.png`; brochure p25 | locked camera, `cameras/front_lock.json` (c327b6e) | critic: framing rows match | DONE (critic accepted lock) |
| 2 Layout | approved V4 CAD via `model/data/model.js` (4B-GF calibration, approx ±3%) | facade plane z 26.9, extents x 1.46–16.0 | rows match at locked camera | DONE (inherited footprint) |
| 3 Blockout | step 1 + 2 | pass 1 carport (a22d08a), pass 2 stone tower (80a4858), pass 3 palms (this commit) | critic, one fix per pass | IN PROGRESS: carport improved, tower PASS, palms PASS (d691222), slat screen pass 5 pending; next: hedge row, then ground relief |
| 4 Grime / finish | step 3 | materials and lighting matched to the reference (travertine, bronze slats, warm dusk light) | side by side | NOT STARTED |
| 5 Printed matter | ELEV-FRONT | no house number, sign or plaque visible in the reference | Q1 record | "none in source" (Q1 REVIEW-PENDING) |
| 6 Critique | locked pair per pass | `cameras/front_passN_side_by_side.png` | independent critic | ONGOING per pass |
| 7 Motion | passed still | short clip from the locked camera (palm sway, light change) | critic | NOT STARTED |

## Pass history
- Lock: camera solved and locked, critic accepted (rows match).
- Pass 1 (a22d08a): carport deep slab on two columns. Critic: closer, overall FAIL.
- Pass 2 (80a4858): right stone tower, top 10.1 m (M25 conflict with M2 11.6 m). Critic: tower PASS, overall FAIL.
- Pass 3 (3e69bff): palms (left group of 2, right 1), positions back-projected through the locked camera. Critic: palms placed right, crowns read as stiff ferns, FAIL.
- Pass 4 (d691222): palm crowns redrawn: drooping arched fronds with open leaflets. Critic: palm fix accepted, overall FAIL; ranked the slat screen above the hedge.
- Pass 5: first-floor slat screen, two staggered layers of vertical bronze slats x 5.4-11.04, y 4.0-7.4 (replaces the dark block). Awaiting critic.
- Pass 6 (prepared, not loaded yet): hedge row and planting, overrides/front_pass6_hedges.js.

Current position: step 3 (blockout), loop 1, pass 5.
