# Ashwood Plan Visuals Archive — Changelog

## 2026-11-09 — Initial GitHub backup (Optimizer Bot)

**Branch:** `ashwood-plan-visuals` (orphan) on `Bigc7292/barclay-house-3d` (private).

### Included
- `original/` — source brochure PDF (`ashwood-residences_brochure.pdf`) and SHA notes (private repo; retained for provenance)
- `canonical/` — project index, handoff manifests, room organization
- `active/` — current approved cad-visual-v4-nine pipeline inputs
- `extracts/`, `source-evidence/` — page extracts and evidence
- `scripts/`, `ACTIVE_PIPELINE.json`, `README.md`
- `optimizer/` — Optimizer Bot scripts:
  - `verify_incremental.py` — mtime/size cached path verify (cuts ~7s → <1s on re-run)
  - `handoff_guard.py` — evidence-vs-inference guard (blocks silent promotion of unknown/ambiguous room matches; keeps `generated_available` separate from `source_missing`)
  - `handoff_overlay.json`, `verify_report.json`, `README.md`
- `superseded_2026-11-09/` — prior pipeline versions (except the ZIP below)

### Excluded (and why)
- `.venv/` — regenerable Python env (~608 MB)
- `node_modules/`, `__pycache__/` — regenerable
- `superseded_2026-11-09/Ashwood_Estates_plan_visuals_archive.zip` (~99 MB, over 95 MB threshold)
- `optimizer/.verify_cache.json` — regenerable incremental verify cache
- Any file over 95 MB (none besides the ZIP at backup time)

### Why orphan branch
Ashwood is a separate project from Barclay House 3D. Orphan history keeps trees independent while sharing the same private GitHub repo for backup.

## 2026-11-09 — FP-4B-GF Floorplan 3D spike rebuilt as v2 (Plan & Visuals Archivist)

**Why:** the user rejected v1 because it still looked 2D. v1 had walls, doors and glazing only, with no rooms or furniture, and was shown in top or high views.
**What changed (FP-4B-GF only; the other eight floors are untouched; still REVIEW-PENDING):**
- Upstream Floorplan 3D features turned back on:
  - 16 derived room polygons (traced V4 walls plus recorded doorway closures, with ~areas), each with a floor material and evidence status (observed from brochure p17/p24/p15, or assumed). Rooms now have ceilings and ceiling lamps.
  - 43 upstream furniture models, placed only where the approved V4 or the brochure crop draws a symbol. Evidence is recorded per item; 6 drawn items were skipped and listed.
  - Full-height walls (3.0 m, display-only) by default, with shadows, RoomEnvironment reflections and the sun at 16:00. Display-only stair massing.
- New input: `source-evidence/floorplan3d-readings/FP-4B-GF.json`. Adapter, verify and README scripts updated (`scripts/v4_to_floorplan3d.py`, `scripts/verify_floorplan3d_spike.py`, `scripts/write_floorplan3d_spike_readme.py`).
- New renders in `active/floorplan3d-spike/FP-4B-GF/verify/`: 1920×1080 eye-level and bird's-eye shots (`v2_0*.png`), plus a side-by-side with the untouched upstream demo rendered locally (`v2_20_*`).
- v1 kept in `active/floorplan3d-spike/FP-4B-GF/v1/` (superseded).
- Still offline (vendored three r160 + Water2), MIT notices kept, zero cost. Labelled not survey-verified, not construction-ready, not certified CAD.

- 2026-11-09: FP-4B-GF viewer - walk speed raised (3.2 m/s walk, 7.0 m/s run, real frame time with 50 ms collision substeps). UNREVIEWED work-in-progress from an interrupted sub-agent polishing the GF interior (furniture styling, feature walls, entry ceiling, pool basin, lighting); before-screenshots in active/floorplan3d-spike/FP-4B-GF/verify/gf_polish_2026-11-09/. Needs critic review before sign-off.
