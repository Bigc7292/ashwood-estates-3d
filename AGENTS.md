# Ashwood Estates 3D: project rules (AGENTS.md)

Read this FIRST on every task. `CLAUDE.md` and `GROK.md` are copies of this file, so any agent tool finds it. Then read `STATUS.md` (where the work is now).

Ashwood Estates is Axis3D scenario test 1. These rules are carried over from Barclay House 3D (`docs/inherited-rules/barclay/AGENTS.md`) and Axis3D (`docs/inherited-rules/axis3d/AGENTS.md`, `PLAN.md`), copied from `Bigc7292/barclay-house-archive` branch `axis3d-plan` at `6417f9b` on 2026-11-09, plus the Ashwood-specific rules already written in this repo's README, `ACTIVE_PIPELINE.json` and `exterior-garden-3d/4b/PIPELINE_7STEP.md`. If this file and a source file disagree, the source file's Ashwood-specific rule wins; tell Colin.

## Hard rules
1. **Free only.** No paid tools, subscriptions, credits or paid APIs without Colin's explicit OK. A cost is a blocker: propose a zero-cost path.
2. **No estimates for project facts.** Every number carries its source (brochure page, URL, approved V4 plan) or is labelled "assumption" / "derived" / "NOT FOUND". Conflicting sources are shown, not silently resolved.
3. **No demo fallbacks.** If a model or fact can't be produced, say so. Never show a sample house in place of Ashwood.
4. **Don't ask Colin for data.** Research and build it yourself. Message Colin only with finished results or a hard blocker.
5. **Don't burn tokens.** Short replies, no duplicate research, no ack ping-pong.
6. **Never overwrite a good output:** write to temp, then mv.
7. **GitHub on every change.** Commit and push after every change set, on a branch; `main` changes only when Colin says. Never commit API keys. Never add a file over 99 MB. Do not deploy anything unless Colin says deploy.
8. **Plan before build** for any new stage. Colin approves the plan.
9. **Labels on everything:** concept visualisation, not survey-verified, not construction-ready, not certified CAD.

## Ashwood input rules
- **Only `ACTIVE_PIPELINE.json` selects inputs.** The nine user-approved V4 floor plans in `active/approved-cad-v4/` are the plans; their artwork is never changed (approval recorded as `pt16u`).
- `canonical/` = current floor/room evidence. `source-evidence/`, `original/`, `extracts/` = provenance only, never selectable drawings.
- `superseded_2026-11-09/` is retired: never an input, never a fallback, never packaged or shown as current.
- Validate with `scripts/verify_active_pipeline.py`; start from `scripts/active_inputs.py`.

## Exterior: Colin's 7-step pipeline (4-bed, `exterior-garden-3d/4b/PIPELINE_7STEP.md`)
Reference → Layout → Blockout → Grime → Printed matter → Critique → Motion. One step at a time, a gate/review after each.
- **Guide rule:** exterior appearance comes from the 10 approved generated 4B images + brochure renders p25/p26 (backups p29/30, p33/34). The V4 CAD is for sizes and plan positions only. Where they disagree, log it in `exterior-garden-3d/4b/mismatches/mismatch_log.md`: image for appearance, CAD for footprint.
- Never use `_raw_unlabelled` or `_rejected_first_pass` images.
- **Current HOLD:** stop after step 4 and wait for Colin's go-ahead before step 5.
- WIP work goes in `blender_wip/`; official `4b_*.blend`, renders and view files change only after critic review.

## Interior web viewer (`active/floorplan3d-spike/FP-4B-GF/`, v2)
- Must read as a furnished 3D interior (v1 was rejected as "still 2D"). Eye-level renders, full-height walls by default.
- Furniture only where the V4 plan or brochure crop draws a symbol; every room polygon, material and item carries its evidence status.
- Fully offline (vendored three.js r160 + Water2), no CDN, no account.

## Pipeline for every change set
0. READ: this file, `STATUS.md`, the relevant README/pipeline doc, the latest critic findings.
1. FACTS: source every number or mark it NOT FOUND / assumption.
2. BUILD: one change set, from the latest defect list.
3. CHECK: run the verify scripts; headless screenshots (before/after, same cameras).
4. CRITIC: an independent critic (not the builder) compares against the references and lists defects. A bot's own "it looks right" is not a score; the orchestrator looks at the image before it counts.
5. EXPORT (when relevant): GLB plus phone GLB; Khronos glTF validator 0 errors; size budgets.
6. DELIVER: commit + push, update `STATUS.md` and the CHANGELOG, one short message to Colin with screenshots.

## Lessons (Barclay + Kimi + Ashwood)
- Tiled photo textures read as rubble or rain at building scale: use flat colours or procedural materials.
- Phones get their own files (smaller textures, merged meshes); big files blank Samsung phones.
- glTF import in Blender sets quaternion rotation: set rotation_mode before rotating.
- Draco files need decoding before Blender 5.2 headless: use glTF-Transform.
- Material names drive viewer overrides; name new materials on purpose.
- Test readiness: wait for explicit "scene ready" / "images decoded" signals, never "network idle".
- Renderer cost: cached static shadows, capped pixel ratio, redraw only on change.
- Don't message a running executor mid-task; it interrupts. Executors can't spawn subagents; the orchestrator runs the critic loop.
- Interrupted sub-agents leave UNREVIEWED work: log exactly what is WIP in the CHANGELOG and `STATUS.md` before stopping.
- Keep `STATUS.md` current at the end of every session, so a lost chat costs no context.

## Reference copies
`docs/inherited-rules/` holds verbatim copies of the Barclay and Axis3D rules, tools, tricks registers, Axis3D plan and QA register. They are reference; this file is the rule set for Ashwood.
