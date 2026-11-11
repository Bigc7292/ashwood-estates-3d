# Verifier index

This index is append-only. Each version is immutable; changed criteria belong in a new version folder. Every verifier execution appends a timestamped JSON record under `verifier/runs/`, including failing and unpublished runs.

- **v1 — 2026-11-10 (Asia/Dubai):** Initial integrated gate for the FF rebuild, five-angle exterior/water pass, working orbit controls, deterministic capture, source-geometry protection, runtime checks and independent visual critique. `v1/verify_static.py` checks source structure and records its result; browser and visual evidence are recorded separately under the same run directory.
