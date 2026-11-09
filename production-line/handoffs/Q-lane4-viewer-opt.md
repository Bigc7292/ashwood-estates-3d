# Hand-off: Lane 4 viewer optimization (Q-lane4)

**Lane:** 4-viewer (Optimizer Bot)  
**Branch:** `lane/4-viewer`  
**Status:** REVIEW-PENDING  
**Date:** 2026-11-10 (Asia/Dubai)

## What changed
New files only under `production-line/viewer/` (+ optimizer helper ports). Builders' sources untouched.

- GF / FF optimized forks: PR cap, shadow bake, demand-render, shared local vendor, offline.
- Exterior lean viewer: MODEL extracted from walkable_v6; HTML 8 KB + model.js 108 KB vs source 1.78 MB embedded file; load ~3.4 s vs ~25.7 s headless.
- `check.sh` size/CDN/offline/patch gate — PASS.
- Optimizer ports: `asset_audit.py`, `precommit_guard.sh`, `raw_labelled_waste.py`; README updated.

## Evidence
- `production-line/viewer/baseline/before.json`
- `production-line/viewer/baseline/after.json`
- `bash production-line/viewer/check.sh` → PASS

## Before → after (key numbers)
| Item | Before | After |
|---|---|---|
| GF HTML | 251501 B, PR≤2, shadows auto, continuous rAF | 250363 B, PR≤1.5/1, shadow bake, demand-render |
| FF | not on main | 250234 B opt fork (r4 data) |
| Exterior payload | walkable_v6 1,777,697 B single file | 8,045 + 107,953 B (+ shared 2.2 MB vendor once) |
| Exterior headless load | ~25.7 s | ~3.4 s |
| Draw calls / tris (exterior opt) | n/a (embedded) | 792 calls / 11,408 tris |

## Open / blocked
- RF viewer: none on main (`lane/roof-floor` has STEPS only).
- FF source still lives on `lane/first-floor`; opt fork uses copied r4 plan data.
- Exterior front_pass WIP not on main; lean MODEL viewer is the lane4 deliverable (no geometry edits).
- No GLBs → gltf-transform / Khronos validator not applicable yet.
- Headless FPS samples are not idle-power metrics (QA.fps forces frames).

## Ask of critic (lane 5)
Confirm opt forks still match GF/FF/exterior look (no geometry change intended). Flag any missing furniture/walls vs source viewers.

## Ask of integrator (lane 6)
Merge `lane/4-viewer` when critic passes; do not force-push; leave builders' files alone.
