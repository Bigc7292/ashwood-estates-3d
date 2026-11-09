# Q2 fact sheet: 4B exterior steps 5-7 and the ground-floor interior

Status: REVIEW-PENDING (lane 1, Facts). Concept visualisation: not survey-verified, not construction-ready, not certified CAD.

Rules applied: every number carries a source path or is labelled `assumption`, `derived` or `NOT FOUND`. Conflicting sources are shown side by side, not resolved. No approved V4 file, plan, viewer or model file was changed.

---

## 1. Approved CAD record: 4B-GF

### 1.1 Which record

- There is no file named `FP-4B-GF_V4_record.json` in `active/approved-cad-v4/reports/` (the directory holds records for 4B-FF, 4B-RF and the other six plans only). **NOT FOUND as a separate file.**
- The 4B-GF record is the `records[0]` entry of `active/approved-cad-v4/reports/nine_V4_manifest.json`. Its values are used below, with that path as source.
- Approved-plan status and the approval code are in `ACTIVE_PIPELINE.json` (`approved_by_user_message`: `pt16u`).

### 1.2 Plan identity and integrity

| Item | Value | Source |
|---|---|---|
| Plan id | 4B-GF, V4 | `nine_V4_manifest.json` records[0] |
| Status | USER_APPROVED_SOURCE_LIMITED_PRESENTATION | `nine_V4_manifest.json` records[0].status |
| User approved | true | `nine_V4_manifest.json` records[0].user_approved |
| Native CAD | false | `nine_V4_manifest.json` records[0].native_CAD |
| Plot boundary verified | false | `nine_V4_manifest.json` records[0].plot_boundary_verified; `canonical/villas/4b/floors/gf/index.json` geometry_qa |
| SVG (approved) | `active/approved-cad-v4/svg/FP-4B-GF_V4_portrait.svg` | `ACTIVE_PIPELINE.json` |
| SVG sha256 | `7f1e9fa6984cb6946c9b8d38d7c0f1daac010eb9a25209aa44b335ec08815554` | `ACTIVE_PIPELINE.json` sha256.svg. Re-computed with `sha256sum` on 2026-11-09: matches. |
| Source PDF page | 27 | `ACTIVE_PIPELINE.json`; `nine_V4_manifest.json` |
| Source xref | 313 | `nine_V4_manifest.json` records[0].source_xref |
| Source board crop (px) | [120, 350, 830, 1370] | `ACTIVE_PIPELINE.json`; `nine_V4_manifest.json` |
| Native source pixels | [710, 1020] | `nine_V4_manifest.json` records[0].native_source_pixels |
| Source wall paths preserved | 13 | `nine_V4_manifest.json` records[0].source_wall_paths_preserved |
| Source: original brochure | `original/ashwood-residences_brochure.pdf` | `ACTIVE_PIPELINE.json` original_source |

### 1.3 Scale calibration

| Item | Value | Source |
|---|---|---|
| Calibration status | approx_calibrated (labelled approximate, prototype only) | `ACTIVE_PIPELINE.json`; `source-evidence/calibration/4B-GF_source_span_calibration.json` status: `APPROXIMATE_CALIBRATION_PROTOTYPE_ONLY` |
| Scale | 28.145 px/m (x fit 28.147, y fit 28.135) | `source-evidence/calibration/4B-GF_source_span_calibration.json` fit_px_per_m, axis_fits_px_per_m; same value in `nine_V4_manifest.json` and `active/approved-cad-v4/reports/independent_calibration.json` |
| Max span residual | 1.7 % | `source-evidence/calibration/4B-GF_source_span_calibration.json`; `nine_V4_manifest.json` |
| Working allowance | 3 % (a working allowance, not a confidence interval or survey accuracy) | `source-evidence/calibration/4B-GF_source_span_calibration.json` working_uncertainty_percent and uncertainty_note |
| Independent calibration count | 5 calibrated, 4 NTS across nine floors | `active/approved-cad-v4/reports/independent_calibration.json` |

**Conflict (paper size):** `nine_V4_manifest.json` records[0].paper_mm = [297, 420]. `source-evidence/calibration/4B-GF_source_span_calibration.json` paper_mm = [420, 594], and its `svg_physical_dimensions` = "420mm x 594mm" and `pdf_physical_mm` = [420.0, 594.0]. Both are shown; the manifest value is not used here. Colin or the integrator should decide which field is wrong.

### 1.4 Calibration spans (source-measured, from the 4B-GF span file)

These are the brochure-overlay transcripts measured against pixel spans on the source board. They are not remeasured geometry.

| Feature | Axis | Source length (m) | Pixels | Fit residual |
|---|---|---|---|---|
| Living/dining clear width | x | 12.4 | 349 | 0.0 % |
| Living/dining clear depth | y | 5.1 | 145 | 1.017 % |
| Pool water width | x | 9.5 | 267 | -0.142 % |
| Pool water depth | y | 2.4 | 67 | -0.812 % |
| Office clear width | x | 4.6 | 130 | 0.411 % |
| Office clear depth | y | 3.4 | 95 | -0.725 % |
| Kitchen clear width | x | 4.0 | 113 | 0.373 % |
| Kitchen clear depth | y | 3.0 | 83 | -1.7 % |

Source: `nine_V4_manifest.json` records[0].calibration.spans (same eight spans in `source-evidence/calibration/4B-GF_source_span_calibration.json`).

### 1.5 Dimensions used for steps 5-7 (footprint and plan)

| Item | Value | Status | Source |
|---|---|---|---|
| Pool (brochure transcript) | 9.50 x 2.40 m | brochure transcript, not geometry-certified | `canonical/villas/4b/floors/gf/index.json` (swimming-pool room) |
| Pool (CAD footprint used in model) | 9.49 x 2.38 m (measured ~) | derived from calibration | `exterior-garden-3d/4b/mismatches/mismatch_log.md` M5; `exterior-garden-3d/4b/evidence_ledger.md` line 21 |
| Pool coping width | 0.30 m | assumption (not in source) | `exterior-garden-3d/4b/mismatches/mismatch_log.md` M22 ("0.30 assumed") |
| Pool deck | +0.45 m, 3 risers | image-read, CAD zone | `mismatch_log.md` M3 |
| Carport footprint | x 0-7.6, z 23.6-29.3 m | CAD vehicle-entry zone (footprint); top 3.45 m image-read | `mismatch_log.md` M1 |
| Stone fin (front right) | 0.5 m blade, top 11.6 m | CAD edge; height image-read | `mismatch_log.md` M2 |
| Rear lawn/plot depth | plot Y 0..+14 m; context lawn extended to 30 m (NOT PLOT) | CAD for plot; context is off-plot | `mismatch_log.md` M4, M21 |
| GF rear stone pier | x 6.6-8.4 m | image-read proportions (see M24) | `mismatch_log.md` M16 |
| FF rear stone panel | x 6.7-8.6 m; FF slat screen x 8.6-12.1 m | image-read | `mismatch_log.md` M16 |
| Front roof overhang | 2.0 m (was 1.2) | image-read; envelope unchanged | `mismatch_log.md` M19 |
| Roof fascia / FF slab | 0.70 m / 0.50 m | image-read (no CAD heights) | `mismatch_log.md` M11 |
| Courtyard water feature (FF void) | 11.48-15.78 x 12.65-16.34 m | GF CAD water-feature rect | `mismatch_log.md` M9 |
| Covered terrace strip | z 11.5-12.65 m | CAD | `mismatch_log.md` M9 |
| Side stone walls | 2.2 m, on CAD site line | image-read height | `mismatch_log.md` M8 |
| Rear boundary wall/fence | NOT FOUND | no source | `mismatch_log.md` M4 |
| Carport and canopy heights | top 3.45 m | image-read | `mismatch_log.md` M1 |
| Plot boundary coordinates | NOT FOUND (plot_boundary_verified = false) | | `nine_V4_manifest.json` records[0] |
| Brochure floor area (GF) | 263.01 m2 | brochure schedule, not measured | `canonical/villas/4b/floors/gf/DESCRIPTION.md` |
| Ceiling heights (GF) | NOT FOUND | | `canonical/villas/4b/floors/gf/index.json` uncertainties |
| Opening widths, door swings, wall thicknesses, stair tread/riser count | NOT FOUND (not metrically verified) | | `canonical/villas/4b/floors/gf/index.json` geometry_qa |

---

## 2. Ground-floor interior: room dimensions (brochure transcripts)

Source for every row: `canonical/villas/4b/floors/gf/index.json` (rooms list), brochure PDF page 27 (`original/ashwood-residences_brochure.pdf`). Status for every row: `brochure_transcript_not_geometry_certified`. No room polygon has been delineated (`room_polygon_status`: not delineated). Perimeter numeric status: unknown_source.

| Room (index id) | Space type | Transcript (m) | Bbox on p27 (px) |
|---|---|---|---|
| Swimming pool | outdoor feature | 9.50 x 2.40 | 423,458-473,479 |
| Living / dining | interior | 12.40 x 5.10 | 395,556-445,577 |
| Show kitchen | interior | 5.70 x 2.70 | 391,700-441,721 |
| Pantry | service | 1.70 x 2.45 | (index.json) |
| Powder | service | 3.65 x 1.70 | (index.json) |
| Kitchen | service | 4.00 x 3.00 | (index.json) |
| Laundry | service | 2.20 x 1.80 | (index.json) |
| Kitchen storage | service | 2.20 x 1.40 | (index.json) |
| Office / gym | interior | 4.60 x 3.40 | (index.json) |
| Bath | interior | 2.90 x 1.70 | (index.json) |
| Double-height entry | interior | 3.29 x 3.30 | (index.json) |
| Multipurpose | interior | 4.60 x 3.90 | (index.json) |
| Dress | interior | 1.90 x 1.10 | (index.json) |
| Maid room | interior | **UNKNOWN** (source label layers conflict) | 318,1012-368,1033 |
| Maid bath | interior | 1.70 x 1.90 | (index.json) |
| Lift | service | 1.50 x 1.70 | (index.json) |

Notes:
- The bbox column is given where `index.json` states it. For the other rows, the bbox is in `dimension_provenance` in the same file; it was not copied here.
- Consistency check: the living/dining, office and kitchen transcripts (12.4, 5.1, 4.6, 3.4, 4.0, 3.0) match the calibration spans in section 1.4. These are the same brochure-overlay values, so they are not independent confirmation.
- Brochure floor area 263.01 m2 (`canonical/villas/4b/floors/gf/DESCRIPTION.md`). **Derived sum of room areas: not computed here** (no room polygons; spaces overlap or are unlabelled in source).
- Furniture symbols: source plan contains symbol contours (beds, rugs, L-sofa, round table, coffee table) in `active/approved-cad-v4/reports/FP-4B-FF_V4_record.json` for FF; **no GF symbol-to-room mapping was found in the GF record.** NOT FOUND for GF furniture placement.

---

## 3. Open mismatches

### M12: RF core visible from street (OPEN)

| Field | Content | Source |
|---|---|---|
| Images | ELEV-FRONT shows no RF volume above the front roof | `exterior-garden-3d/4b/mismatches/mismatch_log.json` M12 |
| CAD | RF plan (NTS) core reaches z ~22.5 m | same |
| Current model | RF core front end z 22.5 m; height to 11.45 m; core narrowed to ~3.5 m (x 7.44-10.94) on 2026-11-09 | `mismatch_log.md` M12 |
| Reason for narrowing | RF plan labels a 3.80 x 15.70 MEP zone beside the core as an open roof area with 1.5 m screen walls (height assumed) | `mismatch_log.md` M12 |
| RF calibration status | NTS_conflicting_source_spans; px_per_m: none accepted; MEP width overlay 3.8 m has a 30.6 % residual; MEP depth 15.7 m is -1.8 % | `active/approved-cad-v4/reports/FP-4B-RF_V4_record.json` calibration; `ACTIVE_PIPELINE.json` (4B-RF) |
| Screen wall height | assumption (1.5 m is source-labelled per log; height assumed) | `mismatch_log.md` M12 |
| Decision needed | Colin: keep CAD position, or pull back or lower the core per the images | `mismatch_log.md` M12 "open_reason" |

Status: OPEN. The RF plan is NTS, so set-back and height cannot be confirmed from the source. The 3.80 x 15.70 MEP reading does not calibrate on both axes (see the RF record).

### M24: GF rear stone pier / FF stone panel side, possible mirror of M16 (OPEN)

| Field | Content | Source |
|---|---|---|
| Images | p26 and ELEV-REAR are seen from the garden, so image-left = plan-right (high x) | `mismatch_log.json` M24 |
| Pier position as logged in the images | "LEFT of centre (~plan x 10.2-12.1 by proportion)" | `mismatch_log.json` M24 "images" field |
| Pier position as logged in open reason | "Rear renders show the pier RIGHT of centre, mirrored vs p26" | `mismatch_log.json` M24 "open_reason" field |
| Current model (M16) | GF_rear_stone_pier x 6.6-8.4 m; FF_rear_stone_panel x 6.7-8.6 m; FF slat screen x 8.6-12.1 m | `mismatch_log.md` M16 |
| Resolution | Not changed in this pass | `mismatch_log.md` M24 |

**Internal conflict inside the log:** M24's "images" field says the pier is LEFT of centre in p26, and its "open_reason" field says the pier is RIGHT of centre and mirrored. Both readings are from the same log entry and cannot both be right. The fact sheet does not pick one.

Facts needed to resolve M24, and their status:
- Plan x-extent of the building (GF): **NOT FOUND** in the sources read for this sheet. Without it, "left of centre" and "right of centre" cannot be checked against the 6.6-8.4 m placement.
- Rear view direction: M24 states image-left = plan-right when seen from the garden (a viewpoint fact from the log, not independently checked here).
- Rear elevation image: `exterior-garden-3d/4b/step1_reference/generated_approved/EXT-4b-ELEV-REAR_GENERATED-SOURCE-CONDITIONED.png` (present). Brochure p26: `exterior-garden-3d/4b/step1_reference/brochure_renders/MARKETING_RENDER_p26.png` (present). Not re-read for this fact sheet; a visual check is the next step.

Status: OPEN. Per the log, the M16 placement must be checked before the pier is moved.

---

## 4. Brochure page references for the 4B exterior

| Page | Use | Source |
|---|---|---|
| p25 | Street / front view (ELEV-FRONT, GARDEN-FRONT, OUTDOOR-SITE); flat 2-bay canopy; dark bronze canopy edge band | `exterior-garden-3d/4b/README.md` line 6; `mismatch_log.json` M1, M18 |
| p26 | Garden / pool view (ELEV-REAR, POOL, GARDEN-BACK); raised stone deck with steps; glass rear facade; warm lit interiors; deep lawn; raised pool box; FF balcony planters | `mismatch_log.json` (M3, M8, M16, M22, M23, M24); `README.md` line 6 |
| p27 | GF floor plan board (source of the GF CAD and room transcripts) | `ACTIVE_PIPELINE.json`; `canonical/villas/4b/floors/gf/index.json` |
| p28 | FF and RF plan board | `ACTIVE_PIPELINE.json` (4B-FF, 4B-RF) |
| p29, p30 | Backup renders (on disk: `exterior-garden-3d/4b/step1_reference/brochure_renders/MARKETING_RENDER_p29.png`, `..._p30.png`) | `PIPELINE_7STEP.md`; `README.md` (5B/6B only mention) |
| p33, p34 | Backup renders (on disk: `..._p33.png`, `..._p34.png`) | same |
| p17 (implied) | Project materials reference id `ref-p17-materials`; the page number comes only from the reference name, not verified | `canonical/villas/4b/floors/gf/index.json` project_material_reference |

Note: `README.md` says p29/30 and p33/34 belong to 5B and 6B. `PIPELINE_7STEP.md` lists them as 4B backups. **Conflict, not resolved here.**

---

## 5. Exterior steps 5-7: source inputs

### Step 5, printed matter (signage)
- Rule (from `exterior-garden-3d/4b/PIPELINE_7STEP.md`): only items visible in the source images; if none, record "none in source" and skip.
- Signage found in source: **NOT FOUND in the evidence ledger, the mismatch log, or the canonical references read for this sheet.** Q1 (lane 2) owns the visual check of the 10 approved images and p25/p26. This sheet does not record a signage finding.
- Approved images (10) on disk: `exterior-garden-3d/4b/step1_reference/generated_approved/` (file names listed in `reference_index.json`).
- The path `generated-views/4b/` named in `PIPELINE_7STEP.md` **does not exist** in this repo (`ls` returned an error). The files are in `step1_reference/generated_approved/`.

### Step 6, critique
- Inputs: step 4 renders (`exterior-garden-3d/4b/step4_grime/renders/`, 19 captioned) and close-ups (`step4_grime/closeups/`, 4 files on disk); reference images in `step1_reference/generated_approved/`.
- Status of step 6 per the pipeline doc: NOT STARTED.

### Step 7, motion
- Planned effects (from the pipeline doc): pool water ripple, palm/tree sway, sun or light change, slow push-in.
- Pool water and palm dimensions: pool water 9.5 x 2.4 m (section 1.4 and 1.5). Palm heights, sun angles and camera path: **NOT FOUND** in the sources read.
- Status of step 7 per the pipeline doc: NOT STARTED. HOLD: go-ahead for step 5 was given by Colin on 2026-11-09 17:40 (`STATUS.md`); the pipeline doc still shows the step-4 hold.

---

## 6. Open issues found while writing this sheet

1. No `FP-4B-GF_V4_record.json` exists. The 4B-GF record used is `nine_V4_manifest.json` records[0].
2. Paper size conflict for 4B-GF: manifest [297, 420] vs calibration file [420, 594] (section 1.3).
3. Pool size: brochure transcript 9.50 x 2.40 m vs CAD-used 9.49 x 2.38 m (both in the repo; the log calls the second "measured").
4. M24 log contradicts itself on whether the pier is left or right of centre.
5. p29/30 and p33/34 are assigned to 5B/6B in `README.md` but to 4B in `PIPELINE_7STEP.md`.
6. `generated-views/4b/` path in `PIPELINE_7STEP.md` does not exist; files are in `step1_reference/generated_approved/`.
7. Building plot coordinates and GF building x-extent: NOT FOUND.
8. GF maid room dimensions: UNKNOWN (source label conflict).
9. Ceiling heights, opening widths, stair counts: NOT FOUND.
