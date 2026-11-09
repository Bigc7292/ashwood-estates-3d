# 4B first floor — enhanced presentation plan FF-E1

**Concept visualisation, not survey-verified, not construction-ready, not certified CAD.**

## What
An enhanced presentation plan of the Ashwood 4-bed villa first floor (4B-FF), brought up to the style of the 4B ground-floor V4 plan ("Presentation prototype 04"): colour zone fills, illustrative finishes, template-style trees, cars, pool and courtyard, dimension chains on all four sides, room plates with area, a legend and a room schedule.

| File | What |
|---|---|
| `FP-4B-FF_ENHANCED_FF-E1_portrait.svg` | Master vector (A3 portrait, same 1000×1414 page and same `source_diagram` transform as V4) |
| `FP-4B-FF_ENHANCED_FF-E1_portrait.pdf` | PDF of the SVG |
| `FP-4B-FF_ENHANCED_FF-E1_preview.png` | 1600 px preview |
| `FP-4B-FF_ENHANCED_FF-E1_hires3400.png` | 3400 px render |
| `FP-4B-GF_V4_vs_FF-E1_side_by_side.png` | GF template next to the new FF, for style consistency |
| `qa/FF-E1_vs_V4_wall_overlay.png` | V4 wall poche (red) vs enhanced (black where they coincide) |
| `qa/FF-E1_vs_V4_blend.png` | 50/50 blend of the V4 FF and FF-E1 renders |
| `qa/FF_V4_base_vs_FF-E1.png` | Before/after |
| `qa/qa_report.json`, `qa/build_log.json` | Wall IoU, zone-edge check, every chain span with its pixel endpoints |
| `scripts/build_enhanced_ff.py`, `scripts/qa_enhanced_ff.py` | Rebuild + QA (python3, numpy, opencv-python-headless, cairosvg; all free) |

## Why
Colin (pt20u, 2026-11-10): the V4 FF plan is only the base; enhance it like the ground floor, with better colour and more measurements.

## Sources (ACTIVE_PIPELINE.json inputs only; sha256 checked in the script)
- Base: `active/approved-cad-v4/svg/FP-4B-FF_V4_portrait.svg` — wall poche (both groups, geometry unchanged), furniture symbols, room labels (positions + values), site/envelope guides, page transform.
- Calibration: `active/approved-cad-v4/reports/FP-4B-FF_V4_record.json` — 29.356 px/m, approx_calibrated, ±3% working allowance.
- Brochure p28 board crop: `source-evidence/plan-crops/FP-4B-FF_untouched_board_crop.png` — doors, swings, stairs, fixtures, glazing traced to vector (replaces the V4 raster underlay); landscape strip positions.
- Style template only: `active/approved-cad-v4/svg/FP-4B-GF_V4_portrait.svg` — palette, tree, car and pool style, chain style, legend layout. The car symbol is scaled by FF/GF calibration (29.356 / 28.145).
- Nothing from `superseded_2026-11-09/`. No AI image generation.

## Measurements
- Room plates: brochure label transcripts parsed from the V4 label layer (no new values). † = V4 disagreement flag (Bedroom 1, Bath 1, Junior Suite).
- `A x.xx m²` = label width × depth (arithmetic only, not a measured area).
- `≈` chain spans: derived from calibrated scale, between V4 envelope/site guides and wall-poche centrelines measured from the V4 poche (`build_log.json`). Not source-stated.
- `~` values (site 18.8 × 29.9 m, envelope 13.1 × 23.9 m) and floor area 260.19 m² are carried over from V4.
- Balconies: UNKNOWN (no source dimensions).

## Known limits
- Zone fills are rectangles laid under walls; a few edges sit on open plan or door openings (listed in `qa/qa_report.json`).
- Traced line-art is source-raster limited (0.25 px trace at 4×), not CAD linework.
- Some `≈` chain spans disagree with labels where V4 already flags † (Bedroom 1 depth, Bath 1 depth).
