# Ashwood Estates — 4-bedroom villa (4B) exterior/garden 3D concept model

**Concept visualisation: not survey-verified, not construction-ready, not certified.** This makes no structural, safety or compliance claims.

## Why 4B
4B is the only villa with a source-span **calibration** file (4B-GF, 8 spans, max residual 1.7 %). It has approx-calibrated GF and FF V4 plans, a pool with a calibrated span (9.50 × 2.40 m), plan tree/lawn/water symbols, an existing V4-derived wall trace (floorplan3d spike), and two same-villa exterior renders (p25 street, p26 garden/pool). 5B and 6B also have p29/30 and p33/34 renders, but they have no calibration file, and 6B-GF is NTS.

## Layout
- `model/index.html`: three.js r160 viewer (vendored, MIT, `model/vendor/three/LICENSE`). It uses Water2 for plan-drawn water only. No CDN and no network. Open it via a local HTTP server, e.g. `python3 -m http.server` in `model/`.
- `model/data/model.json`: every generated element with its status tag.
- `renders/`: 4 previews, 4 orthographic elevations and 11 garden/outdoor-space views. Every image carries the concept caption.
- `comparison/comparison_source_vs_concept.png` and `comparison/discrepancies.md`
- `ledger/element_ledger.json` and `.md`
- `evidence/`: labelled copies. MARKETING_RENDER_* are brochure marketing renders. SOURCE_PLAN_* are untouched crops. APPROVED_V4_* are approved plans. DERIVED_* are my FF/RF wall traces.
- `work/`: build_model.py, build_ledger.py, render.mjs, views.json. playwright-core (Apache-2.0) in node_modules is used for headless rendering only and is not part of the model.

## Inputs (read-only; resolved from ACTIVE_PIPELINE.json; SHA-256 checked; superseded_2026-11-09/ never read)
- approved V4 SVG/PNG 4B-GF/FF/RF; source-evidence/plan-crops FP-4B-*; source-evidence/calibration/4B-GF_source_span_calibration.json
- canonical/rooms_index.json, floors_index.json, references/source_style_evidence.json
- active/floorplan3d-spike/FP-4B-GF/data/fp-4b-gf.plan.json (sha256 29b6d498a614746a575edba0b82dbf3b67604a553a7b011f438286df5bed3363, regenerated upstream 07:30 UTC+4; same input SVG hash)
- original/ashwood-residences_brochure.pdf (sha256 a716d74a…ca1b) pages 25–28, 29/30, 33/34 (rasterised read-only)

## Colour key in renders
Stone/glass/paving/lawn/water = plan geometry with brochure-observed finish. **Neutral grey = placeholder / unknown** (RF core, RF canopy, carport canopy, side boundary walls). Trees = generic plan-symbol canopies (species unknown).
