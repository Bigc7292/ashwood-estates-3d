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
