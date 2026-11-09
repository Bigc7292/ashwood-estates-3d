# Optimizer (Ashwood Estates 3D)

Read-only helpers for evidence/handoff integrity, plus lane-4 viewer checks.
Never edit `active/approved-cad-v4/`, builders' `index.html`, or `ACTIVE_PIPELINE.json` from these scripts.

1. After handoff/index updates: `python3 optimizer/verify_incremental.py` (`--full` after big migrations).
2. Cache: `optimizer/.verify_cache.json`; report: `optimizer/verify_report.json`.
3. Before interior generation batches: `python3 optimizer/handoff_guard.py`, then read `optimizer/handoff_overlay.json`.
4. Asset inventory: `python3 optimizer/asset_audit.py` (if present).
5. Pre-commit size/CDN guard: `bash optimizer/precommit_guard.sh`.
6. Lane-4 viewer gate: `bash production-line/viewer/check.sh`.

Free `python3` stdlib / bash only. Scripts write temp files then `mv`.
