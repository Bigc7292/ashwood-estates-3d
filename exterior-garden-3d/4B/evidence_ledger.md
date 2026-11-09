# 4B villa — exterior evidence ledger (STEP 1–2 only)
Concept evidence only. Not survey-verified, not construction-ready, not certified. Full data: `evidence_ledger.json`. No 3D build or render was made (Colin's scope change: the exterior modelling moves to a Blender process).

## Villa choice: 4B
- 4B-GF (28.145 px/m) and 4B-FF (29.356 px/m) are approx_calibrated, with ≤1.8% residual and ~3% working uncertainty. The 4B-GF spike exists, and the pool is itself one of the calibration spans.
- The GF plan shows: a pool labelled 9.50×2.40, a rear terrace, an outdoor terrace, a courtyard water feature, a 2-bay driveway, vehicular, pedestrian and service entrances, planting strips and 12 tree symbols.
- Same-villa brochure exterior renders: p25 (front, street and driveway) and p26 (rear, pool and garden).
- 5B has more labelled outdoor spaces (8 against 4B's 5) and is also calibrated. It remains the alternative. 6B-GF is NTS.

## Saved crops (evidence/)
- `crop_p25_4B_front_street_driveway.png`: front façade, car-porch canopy, gates, front wall
- `crop_p26_4B_rear_garden_pool.png` and `crop_p26_4B_pool_detail.png`: rear façade, glass balcony, raised pool, terrace steps, lawn
- `crop_p24_heights_courtyard_materials_text.png`: "G+1+R (14m)", "private courtyard with a serene water feature", stone cladding and paint, laminated glass balustrade, aluminium frames, WPC ceiling
- `plan_outline_extraction_4B_GF.png`: generated outlines drawn over the source GF crop
- Full pages: `brochure_p24..p28-*.png`

## Elements (px = GF crop pixels; ~ = approximate)
| Element | Status | Key dims |
|---|---|---|
| Plot boundary (107,54)-(634,895) | observed | ~18.72 × ~29.88 m ≈ 559.5 m² (brochure minimum plot is 561.49) |
| Swimming pool (196,87)-(463,154) | observed | 9.50 × 2.40 m (label); measured ~9.49 × ~2.38 m; depth unknown; p26 shows a raised coping, height unknown |
| Courtyard water + planter (430,412)-(550,515) | observed (plan hatch, p24 text) | ~4.26 × ~3.66 m, planter ~1.24 m sq.; not in rooms_index; open to sky |
| Rear terrace (192,154)-(530,185) + east deck (463,80)-(530,154) | observed | ~12.0 × ~1.1 m strip; deck ~2.4 × ~2.6 m |
| Outdoor terrace (460,335)-(553,410) | observed | ~3.3 × ~2.7 m; covered by the FF bath; missing from rooms_index |
| Driveway, 2 bays (150,725)-(315,890) | observed | ~5.9 × ~5.9 m |
| Car-porch canopy | render only (p25) | extent and height unknown. Conflict: not drawn on FF or RF |
| Pedestrian path (318,712)-(410,890) | observed | ~3.3 × ~6.3 m |
| East service paver path | observed | ~1.5 m wide × ~27 m |
| Planting strips W/E | observed | W ~2.6 m wide, E ~1.3 m wide; species unknown |
| 12 trees (SVG tree0–11) | observed (symbols) | canopy diameter ~2.6–4.0 m; species and height unknown |
| Lawn | unknown | Conflict: p26 shows a lawn, but the plan has no lawn and only ~1.2 m between the pool and the rear boundary |
| Boundary walls, side/rear | line observed, build assumed | height unknown (p26 ~2 m, unverified) |
| Front wall + gates | observed (plan markers, p25) | ~18.7 m frontage; height unknown |
| GF footprint (polygon in JSON) | observed (traced) | ~12.9 × ~22.2 m bbox; traced ~229 m² against 263–266 m² brochure GF area |
| FF footprint (registered polygon) | observed (traced) | ~229 m² traced against 252.6–260.19 m² brochure; includes the open-to-below volume |
| FF balconies ×3 | observed | rear ~13.0 × ~1.9 m; front-W ~4.3 × ~1.4 m; front-E ~5.0 × ~3.1 m |
| RF core + roof terrace + overhead canopy | observed, NTS | MEP label 3.60 × 12.80; lift 1.50 × 1.70; terrace dims unknown |
| Overall height | observed (p24) | 14 m G+1+R; per-floor, parapet, plinth and canopy heights not sourced, so assumed |
| Garage, pergola, extra water features | absent | do not add |

## Key gaps
1. Per-floor heights, plinth, parapet and canopy heights: only the 14 m total is sourced.
2. Car-porch canopy extent: shown in the render but not on any plan.
3. Lawn vs plan conflict at the rear. The surface between the pool and the rear boundary is unknown.
4. Pool depth and coping height; courtyard water depth.
5. Boundary and front wall heights; paving and planting species and finishes (render style cues only).
6. RF is NTS, so the roof canopy extent is approximate. Brochure RF area conflicts: 39.5 vs 43.92 m².
7. FF→GF registration offset is ~0.3 m in x at the east wall, within the ~3% working uncertainty.
8. rooms_index omits the GF outdoor terrace and the courtyard water feature for 4B.
9. Which plot variant this board represents is unknown.
