# CHANGELOG (Ashwood Estates 3D)

Every code edit gets an entry here, in the same turn it is committed and pushed (see AGENTS.md, "Change log and push rule").

## 2026-11-10 (Asia/Dubai), lane 4 viewer (Optimizer Bot)

- **Viewer optimization forks** (branch `lane/4-viewer`). New files under `production-line/viewer/` only; builders' HTML/GLB untouched. GF + FF (r4 data) get pixelRatio cap (1.5/1), `shadowMap.autoUpdate=false` with one bake, render-on-demand, shared local three.js r160 (offline, no CDN). Exterior lean viewer extracts MODEL from `walkable_v6.html`: HTML 8 KB + model.js 108 KB vs source 1.78 MB; headless load ~3.4 s vs ~25.7 s. RF blocked (no viewer yet). `check.sh` PASS. Baseline in `production-line/viewer/baseline/`. Optimizer ports: `asset_audit.py`, `precommit_guard.sh`. Status: REVIEW-PENDING.

## 2026-11-09 (Asia/Dubai)

- **Rules and handoff** (branch `claude/rules-and-status`, PR #1). Added `AGENTS.md` (with `CLAUDE.md` and `GROK.md` copies) and `STATUS.md`. Copied the Legacy and Axis3D rule files into `docs/inherited-rules/`. Status: DONE, draft PR.
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
- **Project name cleanup** (Colin, 18:07): the old project name is removed from this repo's text. The copied rule files moved from the old rules folder to `docs/inherited-rules/legacy/`, and every reference in the docs, rules and lane briefs now uses "legacy" instead. One retired report in `superseded_2026-11-09/` still has the old name and is left unchanged. Git history of earlier commits is not rewritten. Status: DONE.
- **Critic pass Q4 logged** (reported 18:08 by the critic lane). Verdicts recorded in `production-line/QUEUE.md`. Exterior WIP fails on appearance; GF viewer passes on furniture, media wall, pool basin and lighting; entry streak, entry ceiling and walk speed need fixes; courtyard not ready; M24 pier side to be re-checked. The hand-off file `production-line/handoffs/Q4.md` is not in the repo yet, so these verdicts are not yet verified. Status: REVIEW-PENDING.
- **Q4 hand-off merged and verified** (`production-line/handoffs/Q4.md`, commit `212c79f`, merged fast-forward). Integrator opened the referenced images: the brochure p26 render and rear elevation confirm the GF stone panel sits left of centre (about 0.29–0.44 of the width). That corrects the M24 note, which said right of centre; the correction is queued as F4 because it belongs to the mismatch log owner. Walk speed line confirmed at `index.html` line 3191. Status: REVIEW-PENDING.
