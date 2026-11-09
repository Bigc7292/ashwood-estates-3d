# Hand-off Q10 (L2 exterior): walkable 4-bed exterior, WIP

Date: 2026-11-09 (Asia/Dubai). Lane: L2 exterior. Branch: `lane/exterior` (cut from `claude/rules-and-status`). Status: **WIP, REVIEW-PENDING.** Not critic-reviewed. Not signed off.

Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.

## What exists
- `exterior-garden-3d/4b/walk_exterior_wip/index.html`: walk-mode copy of the existing 4B exterior sketch (`exterior-garden-3d/4b/model/index.html`, geometry from `model/data/model.js`).
- Controls: drag to look, WASD or arrow keys to walk at 3 m/s, eye height 1.6 m. Start point (-6, 1.6, 40) is a neutral viewpoint, NOT sourced.
- Assets load from `../model/vendor` and `../model/data`. Nothing new is vendored. The official `4b_*.blend` and the sketch itself are untouched.
- Check run (headless Chromium, swiftshader): page loads, no console or page errors. Screenshot after W shows the walk moved toward the house. Screenshot viewed by the lane builder; a critic must still review it.

## Not done / open (do not treat as finished)
- **Critic gate Q4 not run.** Geometry is the 16:39 WIP snapshot. Blender M20–M24 realism pass is NOT in this viewer.
- **Courtyard module not integrated.** `active/floorplan3d-spike/FP-4B-GF/courtyard_feature.js` is separate (queue Q7).
- **M24 open:** rear GF stone pier / FF stone panel may be mirrored vs brochure p26. Geometry inherits this.
- **M12 open:** RF core position.
- **No collision.** You can walk through the house and the pool. No room polygons, no doors.
- **Label mismatch:** the top label still reads "GENERATED 3D CONCEPT · … · aerial" (from the sketch). Cosmetic, not fixed.
- Unused `OrbitControls` import left in place (harmless).
- Pool 9.5 × 2.4 m (brochure transcript) vs CAD-derived 9.49 × 2.38 m: see Q2 fact sheet §1.5.
- No palm sway, pool motion or video: those are step 7 (Q6), gated behind Q5.

## Process notes
- Per the relay, this lane is not committing to `main` or `claude/rules-and-status`. The root `CHANGELOG.md` entry is left for the integrator (queue Q9). Proposed entry:
  `2026-11-09 Dubai | exterior-garden-3d/4b/walk_exterior_wip/index.html (new), production-line/handoffs/Q10-exterior-walkable.md (new) | Walk-mode page over the 4B exterior sketch geometry | why: Colin wants to walk the outside | status WIP, REVIEW-PENDING (critic Q4 not run; courtyard not integrated)`
- Plan (written before build, per AGENTS.md rule 8): (1) reuse the sketch geometry, no new modelling; (2) walk controls only; (3) critic review, then courtyard (Q7) and viewer (Q8). Colin's approval of this plan is still needed.

## Evidence paths
- `exterior-garden-3d/4b/walk_exterior_wip/index.html`
- `exterior-garden-3d/4b/model/index.html` (source sketch)
- `production-line/facts/Q2_fact_sheet.md` §1.5 (pool and footprint dims)
- `exterior-garden-3d/4b/mismatches/mismatch_log.md` (M1–M24)
