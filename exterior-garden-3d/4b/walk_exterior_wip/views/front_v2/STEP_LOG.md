# Front view v2 (ELEV-FRONT): 7-step gate log

Why v2: Colin, 2026-11-09 23:25 (via coordinator): "Grok is no longer being used i need you to correct it nd fix it". The Grok worker's front changes (M25-SET heights swap, pass 17 terracotta/dusk, camera off the lock) are retired as unverified input. `front_pass.html` and the Grok files are left untouched (no-overwrite rule); the lane works on a new page.
Page: `walk_exterior_wip/front_v2.html` = `front_pass.html` at 50ec220 (981cafa finish + passes 8-16; title and a provenance comment changed). New fixes go in `overrides/front_v2_*.js`, one per pass.
Locked camera: `cameras/front_lock.json` (pos 8.57, 1.6, 45.4; target 8.57, 4.5, 26.9; vFOV 40) with the pass 13 shift lens (view param shift:true). Never moves.
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

| Step | Inputs | Outputs | Review check | Status |
|---|---|---|---|---|
| 1 Reference | `step1_reference/generated_approved/EXT-4b-ELEV-FRONT_GENERATED-SOURCE-CONDITIONED.png` | `cameras/front_lock.json` | lock | DONE (earlier critic PASS) |
| 2 Layout | approved V4 CAD via `model/data/model.js` | front facade | | DONE (earlier) |
| 3 Blockout | | passes 1-7 | | DONE (earlier) |
| 4 Grime / finish | | 981cafa finish | | DONE (earlier); re-check under v2 |
| 5 Printed matter | ELEV-FRONT | | Q1 | to re-check |
| 6 Critique | | passes 8-16 + v2 passes | critic, one fix per pass | IN PROGRESS (v2 loop) |
| 7 Motion | | | | to redo on v2 |

## v2 pass history
- v2 baseline (this commit): restored page, rendered at the locked camera: `shots/front_v2_base_side_by_side.png`.
- Tower height check (this commit): same camera, v2 (pass 14, tower top 9.73 m) vs a check build with the M25-SET swap (11.6 m): `shots/front_v2_tower_check.png`. Tower top row at x 1020 of 1280: v2 80, reference 78; at 11.6 m the tower runs off the top of the frame (row < 30). 9.73 m kept as a front-view display ASSUMPTION (M25 / M43), Colin can overrule; M25-SET's 11.6 m was never confirmed by Colin.
- Note: pass 16 (multi-stem tree, 50ec220) was authored by the Grok worker and never critic-reviewed; it stays in the baseline only as unverified input for the critic to pass or fail.
- Pass 15 (roof slab row, M28) critic note was never found; carried as review-pending.
- Critic (dc1edac): baseline framing and 9.73 m tower PASS (M43 accepted); single fix: the Grok entry tree.
- v2 pass 1 (this commit): entry tree checked at the locked camera (`shots/front_v2_pass1_tree_crop.png`, before / after / reference): ELEV-FRONT does show a small multi-stem tree there (thin stems, loose dome, top row ~412 -> 3.35 m at z 28.6, derived), so it is kept, not swapped for low planting; its column already matched. Fix: canopy was a flat band of blobs on bare stems; top 3.35 m, narrower spread, more and smaller clusters, plus a lower second crown (top 2.4 m, x 13.9) so the dome reaches down to the wall on its right as in the reference (`overrides/front_v2_pass1_entry_tree.js`). Critic (5903abb): placement and 3.35 m top PASS; next fix: bare stems under the crown.
- v2 pass 2 (this commit): leafy understorey behind the low wall (x 11.4-15.2, top 2.2 m, small dark-olive clumps; assumption) hides the stems below the crown line (`overrides/front_v2_pass2_tree_understorey.js`; first try with r 0.55 read as big faceted balls). A few stem bits still show mid-crown. Crop: `shots/front_v2_pass2_tree_crop.png`. Critic: PASS; next fix: palm crowns. Logged for later: carport stops short of the left edge.
- v2 pass 3 (this commit): palm crowns rebuilt as filled, denser leaflet fronds (texture spacing 3 px, line width 4.2, olive greens, slight emissive lift) in three rings (22 / 10 / 5 fronds, wider, drooping), so each crown reads as one leafy mass. Trunk positions, heights and camera unchanged. Hook: `palm_style` in `front_v2.html`; values in `overrides/front_v2_pass3_palm_crowns.js` (display assumption). Shot: `shots/front_v2_pass3_side_by_side.png`. Critic (114dca0): shape PASS; crowns too big (left ~300 vs ~170 px, right ~280+ vs ~130 px); next fix: scale.
- v2 pass 4 (this commit): crowns scaled to ELEV-FRONT widths, centred on the same trunk tops: crown x0.57 on the two left palms, x0.40 on the right; frond widths scale with crown (`palm_style.wByCrown`, new optional hook in `front_v2.html`). Measured in the side-by-side half (960 px): left crown ~100-270 (~170 px, reference ~170), right ~780-925 (~145 px, reference ~130). Colour unchanged (next pass). `overrides/front_v2_pass4_palm_scale.js` (display assumption). Shot: `shots/front_v2_pass4_side_by_side.png`. Awaiting critic.
