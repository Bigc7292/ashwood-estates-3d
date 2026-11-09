# Axis3D: project rules (AGENTS.md)
Read this FIRST on every task. CLAUDE.md and GROK.md are copies of this file, so any agent tool finds it.
Carried over from Barclay House 3D (`barclay/AGENTS.md`, 2026-11-08) and adapted. The plan is in `PLAN.md`.

## Hard rules
1. **Free only.** No paid tools, subscriptions, credits or paid APIs without Colin's explicit OK. A cost is a blocker: propose a zero-cost path.
2. **No estimates for project facts.** Every number in a report, fact sheet or model carries its source: brochure page, URL, or "assumption" (labelled in the UI). Conflicting sources are shown, not silently resolved.
3. **No demo fallbacks.** If a project's model or fact can't be produced, say so. Never show a sample house in place of a client's project.
4. **Don't ask Colin for data.** Research and build it yourself. Message Colin only with finished results or a hard blocker.
5. **Don't burn tokens.** Short replies, no duplicate research, no ack ping-pong.
6. **Never overwrite a good output:** write to temp, then mv.
7. **GitHub on every change.** Commit and push after every change set, on a branch; `main` changes only when Colin says. Do not deploy or alias Vercel unless Colin says deploy. **Never commit API keys** (they go in Vercel env vars).
8. **Plan before build** for any new stage. Colin approves the plan.

## Pipeline (same order every time)
0. READ: this file, PLAN.md, docs/QA_REGISTER.md (the last scenario test), the Lessons below.
1. FACTS: source every number (page or URL) or mark it NOT FOUND / assumption.
2. BUILD: one change set, from the latest defect list.
3. CHECK: run the module test, then the end-to-end run on the current scenario project. Headless browser screenshots of the report, the model and the phone layout.
4. CRITIC: an independent critic (a separate agent, not the builder) scores the model against the developer's renders and the plan, and lists defects. Log them in docs/QA_REGISTER.md.
5. EXPORT: GLB plus phone GLB; Khronos glTF validator must pass with 0 errors; check size budgets.
6. DELIVER: one short message to Colin, with screenshots.

## Model look: the 7-step process (from Barclay, adapted for new builds)
1. Reference: the developer's renders.
2. Layout: from the traced plans.
3. Blockout.
4. Finish: materials from the spec, colours from the renders, clean-build details.
5. Printed matter: name and signage.
6. Critique: compare side by side with the renders.
7. Motion: a flythrough.

Run the steps straight through.

## Lessons (Barclay + Kimi)
- **Tiled photo textures read as rubble or rain at building scale.** Use flat colours or procedural materials.
- **Phones get their own files** (smaller textures, merged meshes); big files blank Samsung phones.
- **glTF import in Blender sets quaternion rotation:** set rotation_mode before rotating.
- **Draco files need decoding before Blender 5.2 headless** (no Draco library there): use glTF-Transform.
- **Material names drive viewer overrides;** name new materials on purpose.
- **Test readiness:** wait for explicit "scene ready" and "images decoded" signals, never "network idle".
- **Renderer cost:** cached static shadows, capped pixel ratio, redraw only on change.
- **Phone first frame:** a wider camera on narrow screens; no opening tween overriding it.
- **Accepted intake must unlock the model.** One status vocabulary across all stages.
- **Additive database migrations only** (v2).
- **Decorative PDF pages** (paper textures, dividers) look like full-size images. The classifier must reject them.
- **A bot's own "it looks right" is not a score.** The orchestrator looks at the image before it counts.
