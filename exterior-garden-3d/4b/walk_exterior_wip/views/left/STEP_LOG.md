# Left view (ELEV-LEFT): 7-step gate log

View: EXT-4b-ELEV-LEFT. Page: `walk_exterior_wip/left_pass.html` (own page; overrides `overrides/left_*.js`). Locked camera: `left_lock.json` (never moves). Builder: lane 2 cloud builder. Critic: independent critic thread, one fix per pass.
Shared heights: the branch's M25-SET values (tower 11.6 m, model FF level 4.0-7.4 m, roof slab 7.4-7.85 m) so both exterior builders agree. "Delegated by Colin" for M25-SET is not yet confirmed by Colin.
Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

| Step | Inputs | Outputs | Review check | Status |
|---|---|---|---|---|
| 1 Reference | `step1_reference/generated_approved/EXT-4b-ELEV-LEFT_GENERATED-CONCEPT.png` | locked camera `left_lock.json`, `shots/left_lock_side_by_side.png` | critic: framing rows and ends match | DONE (critic: lock PASS on framing) |
| 2 Layout | approved V4 CAD via `model/data/model.js` | left facade x 1.46, z 2.84-26.88 | ends match at the locked camera | DONE (inherited footprint), pending critic |
| 3 Blockout | steps 1 + 2 | pass 1 RF plant strip, pass 2 central block, pass 3 base, pass 4 planting | critic, one fix per pass | IN PROGRESS (loop 1) |
| 4 Grime / finish | | | | NOT STARTED |
| 5 Printed matter | ELEV-LEFT | | Q1 record | to check |
| 6 Critique | | | | NOT STARTED |
| 7 Motion | | | | NOT STARTED |

## Pass history
- Lock (334032a): critic PASS on framing.
- Step 3 pass 1 (this commit): RF volume hidden in this view; low recessed strip (7.85-9.45 m) under a thin canopy slab (9.45-9.76 m), z 16.6-23.2, image-read (M33). Critic (da99dbf): strip PASS; next fix central block top.
- Step 3 pass 2 (this commit): central travertine block raised above the FF overhang slabs: stone parapet block x 2.85-4.0, z 7.6-21.7, top 8.94 m (derived, M34). Slab overhangs unchanged. Critic (435f6c3): block PASS; next fix the base band.
- Step 3 pass 3 (this commit): grey placeholder boundary replaced by a travertine wall on the CAD line (x -0.25-0), top 2.0 m on the reference row, with coping; planting band at its foot; off-plot gravel strip and lawn (context). Residual: the reference's wall base sits lower (~30 px), as if the wall were nearer the camera. Critic (6f55371): wall PASS, base drift accepted as residual; next fix layered planting.
- Step 3 pass 4 (this commit): three layered shrub rows (1.35/0.75/0.45 m) along the wall foot and four small multi-stem trees in front of the wall (z 2.5/8.1/12.5/17.7, tops ~3.4 m), image-read, off-plot context. Awaiting critic.
