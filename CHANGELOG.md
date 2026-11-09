# CHANGELOG (Ashwood Estates 3D)

Every code edit gets an entry here, in the same turn it is committed and pushed (see AGENTS.md, "Change log and push rule").

## 2026-11-09 (Asia/Dubai)

- **Rules and handoff** (branch `claude/rules-and-status`, PR #1). Added `AGENTS.md` (with `CLAUDE.md` and `GROK.md` copies) and `STATUS.md`. Copied the Barclay and Axis3D rule files into `docs/inherited-rules/`. Status: DONE, draft PR.
- **7-step rule set** in `AGENTS.md`, covering exterior and interior. Status: DONE.
- **Ashwood runs straight through to step 7** (Colin, 17:40). The step-4 hold is removed from `AGENTS.md` and `STATUS.md`. Status: DONE. Steps 5–7 are WIP.
- **Change log and push rule** added to `AGENTS.md` (Colin, 17:41). This file created. Status: DONE.
- **Model viewer and progress artifacts** published from the scratchpad, not from the repo (no repo files changed). Viewer: https://claude.ai/artifact/77CUbtNzDqqUYUW75GFiuq. Progress: https://claude.ai/artifact/XZnAbwEKiLHGLLaWnqBq1C. Status: DONE.

## 2026-11-09 (Asia/Dubai), production line

- **Production line set up** (Colin, 17:44 via coordinator). Added `production-line/` with `README.md` (six lanes, ownership, flow, status vocabulary), six lane briefs in `production-line/lanes/`, `QUEUE.md` seeded with Q1–Q9, and empty folders for handoffs, facts, critic reports and viewer build files. Status: DONE (structure). Work items Q1–Q9 WIP or QUEUED.
- **Exterior step 5 inventory (Q1, lane 2)**: checked the 10 approved 4B images and brochure p25/p26 for signage. No in-scene signage found; the only text is the brochure overlay title "4 BEDROOM VILLA" and a logo, not on the building. Files: `production-line/exterior/step5/step5_inventory.md`, `production-line/handoffs/Q1.md`. Status: REVIEW-PENDING. Brochure p29/p30/p33/p34 not yet checked. Also flagged: the generated images carry a burned-in "concept visualisation" caption, which Colin should decide on for presentation copies.
- **Step-hold text removed** from `exterior-garden-3d/4b/PIPELINE_7STEP.md` so it matches the straight-through rule in AGENTS.md (Colin, 17:40). Status: DONE.
- **GF polish WIP review (Q3, lane 3)**: per-area verdicts in `production-line/handoffs/Q3.md`. Keep furniture, feature walls (fix the entry travertine streak texture first), lighting and pool basin. Walk speed (3.2 / 7.0 m/s) is unsourced and needs a decision. Courtyard module reviewed but not integrated (Q7). Status: REVIEW-PENDING.
- **Ashwood fact sheet (Q2, lane 1)**: `production-line/facts/Q2_fact_sheet.md`. CAD values for 4B-GF, brochure page map, M12 and M24 evidence. Open conflicts recorded, not resolved: paper size (297x420 vs 420x594 mm), pool size (9.50x2.40 brochure vs 9.49x2.38 CAD), M24 pier side (building x-extent NOT FOUND), brochure page attribution for p29/30 and p33/34 (5B/6B in README, 4B in PIPELINE_7STEP), and a missing `generated-views/4b` path in the pipeline doc. Status: REVIEW-PENDING.

## 2026-11-10 (Asia/Dubai), lane 2 exterior (branch `lane/exterior`)

- **Front step 6 pass 16** (00:30). Files: `exterior-garden-3d/4b/walk_exterior_wip/front_pass.html` (flag-guarded multi-stem tree builder + step 7 sway), `overrides/front_pass16_multistem_tree.js` (new), `cameras/front_pass16_model.png`, `cameras/front_pass16_side_by_side.png`, `views/front/STEP_LOG.md`, `views/front/cams/front.json`, `tools/shoot.cjs` + `tools/sbs.py` (new box capture tools). What: the three faceted shrub balls behind the front-right wall replaced by one open multi-stem tree, as ELEV-FRONT shows. Why: step 6 "looks unnatural" defect. Status: REVIEW-PENDING (independent critic). M25/M26 not touched.
- **Rear + garden step 6 pass 1** (00:45). Files: `walk_exterior_wip/rear_pass.html` (new, renderer copy with the rear override list), `overrides/rear_pass1_base.js` (new), `views/rear/` and `views/garden/` (STEP_LOG, cams, shots), `production-line/handoffs/L2-exterior_2026-11-10.md` (new). What: baseline ELEV-REAR, GARDEN-BACK and POOL views; palms on plan tree symbols, off-plot context lawn (look only), side hedges; pool on three.js Water2. Why: Q5 step 6 for rear/garden. Status: REVIEW-PENDING.
- **Rear + garden step 6 pass 2** (00:55). Files: `walk_exterior_wip/overrides/rear_pass2_glazing.js` (new), `rear_pass.html`, `views/{rear,garden}/` (STEP_LOG, cams, pass-2 shots), `tools/_shootall.sh`. What: rear glazing reads as clear glass with lit rooms and slim frames (CAD glass lines; interiors are display assumptions). Why: step 6 defect "glazing reads as tan opaque slabs". Status: REVIEW-PENDING.
- **Rear + garden step 6 pass 3** (01:00). Files: `walk_exterior_wip/rear_pass.html` (Water2 tuning hook, rear page only), `overrides/rear_pass3_water2.js` (new), `views/{rear,garden}/` (STEP_LOG, cams, pass-3 shots). What: pool Water2 now visibly reflective with ripples. Why: step 6 defect "pool reads as flat blue paint"; Water2 must be visible. Status: REVIEW-PENDING.
