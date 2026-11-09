# Optimizer log

## 2026-11-03 07:27 Asia/Dubai: Run 1 (audit only, builder mid-Round 3; no fixes applied)
Sizes (out/, 06:37–07:12):
- hero.glb 4.84 MB (budget <5, OK but tight)
- mobile hero 1.74 MB (<2, OK)
- mobile surroundings 4.60 MB (<6, OK)
- full surroundings 36.2 MB, full scene.glb 95.2 MB (phones must not load these)
- 4K PNGs 13.9–17.8 MB each
Validator: not run this pass, and no validator report found on disk.
Render times: not logged anywhere (only "several minutes" per 4K at 128 samples on CPU).
Critic: R1 score 3/10. No R2/R3 scores in root critic_log.md (they live in interior/critic_log.md, which is split).
Housekeeping:
- 4 old build_scene_r*/v1 copies plus export_glb_r2.py
- hdri.exr 83 MB, dl.log 1.3 MB
- 6 tests/scene_copy*.blend + .blend1, out/*.blend1, out/hero_.png (stray)
- AGENTS/CLAUDE/GROK.md are copies, not symlinks (drift risk)
- refs/ root has only plans/CGI; real photos are in refs/critic1
Next ideas (after R3):
- validate.sh: Khronos validator + size-budget check + draw calls
- auto-backup of out/ before export
- log render seconds/samples per still
- try 64 samples + OIDN for previews
- archive old scripts into old/
- symlink CLAUDE/GROK to AGENTS
- unify the two critic_logs
- convert 4K PNG to JPEG for delivery

## 2026-11-03 08:05 Asia/Dubai: Run 2
Builder busy (build_scene.py midday --noexport running), so no model touches.
Added `validate.sh` + `.gltf/validate.mjs` (free Khronos gltf-validator + gltf-transform; runs in 1.7 s; JSONL report in tests/validate_*.jsonl).
Measured: hero 4.61 MiB, 0 err, 1464 primitives (draw calls) | mobile hero 1.66 MiB, 8 prims | mobile surr 4.39 MiB, 20 prims | full surr 34.5 MiB, 5453 prims. All budgets pass, 0 validator errors.
FAIL: both mobile GLBs are stale (07:12, built from the 06:37 export; hero/surr re-exported 07:40), so phones see pre-R3 geometry. Sent to Barclay House 3D.
AGENTS.md: export step now runs validate.sh; Lesson added. Copies synced to CLAUDE/GROK.md.
Still open from R3 critic: neighbour roofs pale, viaduct parapet salmon (material not taking effect).
Next: render-time logging, archive old scripts to old/, 1464 hero prims (join by material for desktop), unify critic logs.
