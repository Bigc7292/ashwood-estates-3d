# Front view (ELEV-FRONT): 7-step gate log

View: EXT-4b-ELEV-FRONT. Locked camera: `../../cameras/front_lock.json` (never moves). Builder: lane 2 (exterior). Critic: independent critic thread, one fix per pass.
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

| Step | Inputs | Outputs | Review check | Status |
|---|---|---|---|---|
| 1 Reference | `step1_reference/generated_approved/EXT-4b-ELEV-FRONT_GENERATED-SOURCE-CONDITIONED.png`; brochure p25 | locked camera, `cameras/front_lock.json` (c327b6e) | critic: framing rows match | DONE (critic accepted lock) |
| 2 Layout | approved V4 CAD via `model/data/model.js` (4B-GF calibration, approx ±3%) | facade plane z 26.9, extents x 1.46–16.0 | rows match at locked camera | DONE (inherited footprint) |
| 3 Blockout | step 1 + 2 | pass 1 carport (a22d08a), pass 2 stone tower (80a4858), pass 3 palms (this commit) | critic, one fix per pass | DONE loop 1: carport, tower, palms, slat screen, planting, ground all PASS on placement; RF block hidden in front view (M26) |
| 4 Grime / finish | step 3 | materials and lighting matched to the reference (travertine, bronze slats, warm dusk light) | side by side | PASS loop 1 (critic, 981cafa) |
| 5 Printed matter | ELEV-FRONT | no house number, sign or plaque visible in the reference | Q1 record | DONE: "none in source" (Q1), critic noted |
| 6 Critique | locked pair per pass | `cameras/front_passN_side_by_side.png` | independent critic | ONGOING per pass |
| 7 Motion | passed still | short clip from the locked camera (palm sway, light change) | critic | NOT STARTED |

## Pass history
- Lock: camera solved and locked, critic accepted (rows match).
- Pass 1 (a22d08a): carport deep slab on two columns. Critic: closer, overall FAIL.
- Pass 2 (80a4858): right stone tower, top 10.1 m (M25 conflict with M2 11.6 m). Critic: tower PASS, overall FAIL.
- Pass 3 (3e69bff): palms (left group of 2, right 1), positions back-projected through the locked camera. Critic: palms placed right, crowns read as stiff ferns, FAIL.
- Pass 4 (d691222): palm crowns redrawn: drooping arched fronds with open leaflets. Critic: palm fix accepted, overall FAIL; ranked the slat screen above the hedge.
- Pass 5 (4769f7f): first-floor slat screen, two staggered layers x 5.4-11.04, y 4.0-7.4. Critic: PASS on placement, overall FAIL.
- Pass 6 (3ff454e): hedge row and planting. Critic: PASS on placement, overall FAIL; ground is the largest gap.
- Pass 7 (3f5121f): ground relief. Critic: PASS on placement; step 3 blockout complete apart from M12.
- Step 4 finish: warm travertine, low warm dusk sun and sky, warm glow behind glazing, LED lines in the carport and roof soffits. M26: RF block hidden in the front view only (display assumption per Colin, M12 stays open). Critic: PASS (981cafa).
- Step 5: none in source (Q1).
- Step 6 pass 8 (this commit): glazing. Dark clear glass with warm-lit rooms behind (timber back wall and ceiling glow behind the FF slat screen; lit lobby behind the GF entry glass). Interior depths and finishes are display assumptions. Awaiting critic.

Current position: step 6 (critique), loop 1. Pass 8 (glazing) awaiting critic.
