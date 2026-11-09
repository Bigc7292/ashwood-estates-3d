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
- Step 6 pass 8 (this commit): glazing. Dark clear glass with warm-lit rooms behind (timber back wall and ceiling glow behind the FF slat screen; lit lobby behind the GF entry glass). Interior depths and finishes are display assumptions. Critic (bbe1b36): closer, FAIL; next fix the GF glazing.
- Step 6 loop 2 pass 9 (this commit): GF glazing band widened to the entry recess walls (x 7.50-10.70, M27) with two bronze mullions and a transom; brown panel replaced by a lit lobby. Also added: step 7 motion hook (window.__frame) in front_pass.html, inactive in stills and walk mode. Critic (f1cd5ad): look PASS, but width breaks CAD (M16 rule); restore CAD width.
- Step 6 loop 2 pass 10 (this commit): GF glass back to the CAD cue x 7.50-9.59; x 9.59-10.70 is a dark timber entry door (image-read, display assumption); lit lobby kept. M27 resolved (CAD width kept). Critic (8aba267): GF glass PASS; next fix the FF slat screen.
- Step 6 loop 2 pass 11 (this commit): FF slat screen recoloured to warm lit timber and the staggered back layer dropped, so the lit rooms show between the slats. Extent unchanged. Critic (e62ad64): screen PASS (saturation residual accepted); next fix the right tower top.
- Step 6 loop 2 pass 12 (this commit): right tower. The sloping side-face top is perspective of the 4 m deep blade and is in ELEV-FRONT too (cameras/front_pass12_tower_crop.png); added the flat dark coping cap the reference shows. Footprint and 10.1 m height unchanged. Critic (0eea0b2): cap PASS, wedge reading withdrawn; next fix converging verticals.
- Step 6 loop 2 pass 13 (this commit): vertical shift (shift lens) in the render: same camera position, target still at frame centre, camera held level with the frustum shifted up (view param shift:true, front_pass.html). Verticals now parallel. front_lock.json is NOT changed; all later front stills and the step 7 clip use shift:true. Side effect: rows away from the centre move slightly (tower top ~18 px higher, roof slab top ~8 px higher at 960x540). Critic (8fda529): shift PASS; next fix tower top ~18 px down = height change, held, then applied per Colin's "don't wait" (relayed by the coordinator).
- Step 6 loop 2 pass 14 (this commit): tower top to the reference row, 9.73 m derived (M25 front-view assumption, views/front/M25_assumption_2026-11-09.md; Colin can overrule). Also fixed: remove[] did not filter boxes added by earlier override files; pass 9 and pass 14 now drop those from add[] directly (pass 8's GF entry panel no longer z-fights the pass 9 lobby wall). Awaiting critic.

Current position: step 6 (critique), loop 1. Step 6 loop 2, pass 14 (tower top on the reference row) awaiting critic.
