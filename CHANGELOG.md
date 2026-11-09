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
