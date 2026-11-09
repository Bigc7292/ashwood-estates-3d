# Ashwood Estates 3D: project rules (AGENTS.md)

Read this FIRST on every task. `CLAUDE.md` and `GROK.md` are copies of this file, so any agent tool finds it. Then read `STATUS.md` (where the work is now).

Ashwood Estates is Axis3D scenario test 1. These rules are carried over from Legacy project (`docs/inherited-rules/legacy/AGENTS.md`) and Axis3D (`docs/inherited-rules/axis3d/AGENTS.md`, `PLAN.md`), copied from `Bigc7292/legacy-archive` branch `axis3d-plan` at `6417f9b` on 2026-11-09, plus the Ashwood-specific rules already written in this repo's README, `ACTIVE_PIPELINE.json` and `exterior-garden-3d/4b/PIPELINE_7STEP.md`. If this file and a source file disagree, the source file's Ashwood-specific rule wins; tell Colin.

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

## The 7-step rule set (set in stone, exterior AND interior)
Colin, 2026-11-09: this rule set applies to both exterior and interior work in this project. Full source: `docs/inherited-rules/legacy/ext7/` (step docs), `docs/inherited-rules/legacy/AGENTS.md` (the Legacy "Exterior 7-step process"), and `exterior-garden-3d/4b/PIPELINE_7STEP.md` (the Ashwood 4-bed version).

| Step | Exterior (4-bed) | Interior (floors, rooms, furniture) |
|---|---|---|
| 1 Reference | the 10 approved generated 4B images + brochure p25/p26 (backups p29/30, p33/34) | internal brochure images and reference renders (p15–p17, p24), no raw/rejected files |
| 2 Layout | footprint and plot positions from the approved V4 CAD (sizes only) | room layout from the approved V4 CAD plans (GF/FF/RF) |
| 3 Blockout | boxes first, then space, models, materials, in that order; proportions fixed while still boxes | walls, rooms and floors as boxes, then furniture and materials |
| 4 Grime / finish | procedural wear: chips, dust, drips, base dirt, weathering | clean-build finish from the spec: materials, reveals, lighting; no grime on new interiors |
| 5 Printed matter | signs/plaques/house numbers only if visible in the source images; else "none in source" | labels and signage only if visible in source images |
| 6 Critique | side-by-side with the reference images; list "looks unnatural" defects and fix them | side-by-side with the reference images and the V4 plan |
| 7 Motion | flythrough or pool/palm/sun motion, rendered to video | walkthrough or light change, rendered to video |

Rules for all seven steps:
- One step at a time. Log each step's gate in its step doc (`ext7/`-style: Inputs, Outputs, Review check, Status).
- Images decide appearance, CAD decides dimensions. Where they disagree, log it in `exterior-garden-3d/4b/mismatches/mismatch_log.md` and use image for look, CAD for footprint.
- **Run straight through to step 7** (Colin, 2026-11-09 17:40): no hold. Each step still gets its gate log and critic check before the next step starts, but no wait for Colin between steps 1 and 7. Colin reviews the finished set.
- Pure review gates use the independent critic (not the builder).

## Exterior: 4-bed status
- Steps 1–4 done, revised. Steps 5–7 now go ahead (Colin, 2026-11-09 17:40). Official `4b_*.blend` untouched by WIP.
- WIP in `blender_wip/` (M20–M24) is not critic-reviewed and not used for official renders.

## Interior web viewer (`active/floorplan3d-spike/FP-4B-GF/`, v2)
- Must read as a furnished 3D interior (v1 was rejected as "still 2D"). Eye-level renders, full-height walls by default.
- Furniture only where the V4 plan or brochure crop draws a symbol; every room polygon, material and item carries its evidence status.
- Fully offline (vendored three.js r160 + Water2), no CDN, no account.

## Change log and push rule (Colin, 2026-11-09 17:41, set in stone)
- **Every edit to the code base is documented and pushed.** Any change to a file in this repo (code, data, docs, rules, renders, viewer) gets, in the same turn:
  1. One entry in `CHANGELOG.md` at the repo root: date (Asia/Dubai), files changed, what changed, why, and status (DONE / WIP / REVIEW-PENDING).
  2. A commit on the working branch with that entry included.
  3. A push to GitHub (`git push -u origin <branch>`). No edit is left only on disk or only in a chat.
- If an edit is not finished, the entry says WIP and names what is left.
- Changes to `main` happen only when Colin says so.

## Pipeline for every change set
0. READ: this file, `STATUS.md`, the relevant README/pipeline doc, the latest critic findings.
1. FACTS: source every number or mark it NOT FOUND / assumption.
2. BUILD: one change set, from the latest defect list.
3. CHECK: run the verify scripts; headless screenshots (before/after, same cameras).
4. CRITIC: an independent critic (not the builder) compares against the references and lists defects. A bot's own "it looks right" is not a score; the orchestrator looks at the image before it counts.
5. EXPORT (when relevant): GLB plus phone GLB; Khronos glTF validator 0 errors; size budgets.
6. DELIVER: CHANGELOG entry, commit + push (see the change log rule above), update `STATUS.md`, one short message to Colin with screenshots.

## Lessons (Legacy + Kimi + Ashwood)
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

## Production line of agents (requested by Colin, 2026-11-09)
Goal: several agents on separate tasks in parallel to finish faster, with the same seven steps and rules above.
- Lanes: (1) Facts & evidence (CAD, brochure, mismatch log); (2) Exterior builder; (3) Interior builder; (4) Viewer/web; (5) Critic (independent, reads outputs and logs defects); (6) Integrator (merges one change set at a time, runs verify scripts, updates STATUS.md).
- Each lane writes only in its own folder and logs its work in its step doc; the integrator is the only one that commits to `main` (and only on Colin's word).
- Nobody marks a step done on their own: the critic and then Colin pass the gate.
- This section is the plan, not yet built. Colin approves the plan before any lane starts.

## Reference copies
`docs/inherited-rules/` holds verbatim copies of the Legacy and Axis3D rules, tools, tricks registers, Axis3D plan and QA register. They are reference; this file is the rule set for Ashwood.
