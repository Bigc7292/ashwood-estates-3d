# Left view (ELEV-LEFT): 7-step gate log

View: EXT-4b-ELEV-LEFT. Page: `walk_exterior_wip/left_pass.html` (own page; overrides `overrides/left_*.js`). Locked camera: `left_lock.json` (never moves). Builder: lane 2 cloud builder. Critic: independent critic thread, one fix per pass.
Shared heights: the branch's M25-SET values (tower 11.6 m, model FF level 4.0-7.4 m, roof slab 7.4-7.85 m) so both exterior builders agree. "Delegated by Colin" for M25-SET is not yet confirmed by Colin.
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

| Step | Inputs | Outputs | Review check | Status |
|---|---|---|---|---|
| 1 Reference | `step1_reference/generated_approved/EXT-4b-ELEV-LEFT_GENERATED-CONCEPT.png` | locked camera `left_lock.json`, `shots/left_lock_side_by_side.png` | critic: framing rows and ends match | DONE (critic: lock PASS on framing) |
| 2 Layout | approved V4 CAD via `model/data/model.js` | left facade x 1.46, z 2.84-26.88 | ends match at the locked camera | DONE (inherited footprint), pending critic |
| 3 Blockout | steps 1 + 2 | pass 1 RF plant strip, pass 2 central block, pass 3 base, pass 4 planting, pass 5 canopies, pass 6 canopy volume, pass 7 canopy row, pass 8 verge trees, pass 9 plan trees low, pass 10 grass layer, pass 11 FF openings, pass 12 carport opening, pass 13 carport back wall | critic, one fix per pass | PASS loop 1 (critic, 6998a8a) |
| 4 Grime / finish | step 3 | pass 14 carport wall tone | side by side | IN PROGRESS (loop 1) |
| 5 Printed matter | ELEV-LEFT | | Q1 record | to check |
| 6 Critique | | | | NOT STARTED |
| 7 Motion | | | | NOT STARTED |

## Pass history
- Lock (334032a): critic PASS on framing.
- Step 3 pass 1 (this commit): RF volume hidden in this view; low recessed strip (7.85-9.45 m) under a thin canopy slab (9.45-9.76 m), z 16.6-23.2, image-read (M33). Critic (da99dbf): strip PASS; next fix central block top.
- Step 3 pass 2 (this commit): central travertine block raised above the FF overhang slabs: stone parapet block x 2.85-4.0, z 7.6-21.7, top 8.94 m (derived, M34). Slab overhangs unchanged. Critic (435f6c3): block PASS; next fix the base band.
- Step 3 pass 3 (this commit): grey placeholder boundary replaced by a travertine wall on the CAD line (x -0.25-0), top 2.0 m on the reference row, with coping; planting band at its foot; off-plot gravel strip and lawn (context). Residual: the reference's wall base sits lower (~30 px), as if the wall were nearer the camera. Critic (6f55371): wall PASS, base drift accepted as residual; next fix layered planting.
- Step 3 pass 4 (this commit): three layered shrub rows (1.35/0.75/0.45 m) along the wall foot and four small multi-stem trees in front of the wall (z 2.5/8.1/12.5/17.7, tops ~3.4 m), image-read, off-plot context. Critic (6f55371->13fff91): planting PASS; next fix canopy shapes.
- Step 3 pass 5 (this commit): plan-tree lollipop spheres replaced by irregular multi-stem canopies at the CAD plan-symbol positions (sizes varied, assumption); pass 4's four image-read front trees dropped as doubles of plan trees 1/3/4/5 (CAD decides positions). Critic (3b5b382): shapes PASS; next fix crown volume.
- Step 3 pass 6 (this commit): same CAD trunks and tops; spread x1.5, 3x leaf clusters, larger clusters, deeper crowns (builder options leaf/depth added in left_pass.html). Residual: crowns now read slightly blobby and sit a little high. Critic (353274e): FAIL, tops too high and too dark.
- Step 3 pass 7 (this commit): canopy tops lowered to the reference row (~365 in the panel; tops 2.6 m x variation), width and mass kept, softer olive greens. Critic (55ebb19): tops PASS; canopies read as a shrub band, need trunks.
- Step 3 pass 8 (this commit): geometry check: CAD plan trees stand behind the 2.0 m wall, so their trunks cannot show. The reference's four trunked trees are read as verge trees in front of the wall (off-plot context) and restored at the image-read columns (z 2.5/8.1/12.5/17.7, x -1.0), open crowns ~2.3-3.4 m with bare trunks. CAD plan trees stay behind the wall. Residual: verge and plan crowns overlap at the same height. Critic (58538c2): verge trees PASS; lower/thin plan crowns.
- Step 3 pass 9 (this commit): CAD plan-tree crowns lowered to just above the wall (2.15 m x variation), half the clusters, narrower; verge trees unchanged. Critic (1266a19): separation PASS; fill the gaps.
- Step 3 pass 10 (this commit): tall ornamental-grass layer (1.2-2.0 m, two rows, new instanced grass builder in left_pass.html) between the verge trees. Reference crop (shots/left_pass10_planting_crop.png) shows the wall visible between its trees behind grasses, so no solid hedge to the slab. Critic (2122647): planting PASS; next fix FF openings.
- Step 3 pass 11 (this commit): three tall FF windows (z 12.0-13.1 / 16.9-17.6 / 19.6-20.4, Y 4.0-6.82) in a thin stone skin on the central block; balcony bays open to the CAD FF glass at z 3.1-7.6 and 21.7-24.4 with glass rails (4.0-4.95 m) and bronze caps (M35). Windows read dark; the reference shows pale curtains (finish step). Critic (f3f9341): openings PASS; next fix carport opening.
- Step 3 pass 12 (this commit): boundary wall ends at z 21.0; carport opening to z 26.45; travertine pillar z 26.45-27.66 with coping; paved apron; planting stops at the opening (image-read, projected at the wall line). Residual: the opening shows through to sky/gate where the reference shows a lit timber back wall. Critic (dc6464b): opening PASS; next fix back wall.
- Step 3 pass 13 (this commit): flat-colour lit timber back wall inside the carport (x 7.2-7.39, z 21.0-30.5, 0-3.0 m); no sky through the opening. Critic (6998a8a): step 3 gate PASSED.
- Step 4 pass 14 (this commit): carport back wall recoloured (MAT.timber_lit in left_pass.html) to the tone sampled from ELEV-LEFT: reference median RGB ~118,76,44 in the carport opening; model now renders ~119,83,50 (was 130,80,38). Awaiting critic.
