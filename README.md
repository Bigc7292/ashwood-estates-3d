# Ashwood — current active pipeline

**Agents: read `AGENTS.md` (rules) and `STATUS.md` (current state) first.**

ONLY `ACTIVE_PIPELINE.json` selects inputs. Nine user-approved V4 floor plans live in `active/approved-cad-v4/`; their artwork is unchanged. `canonical/` holds current floor/room evidence and missing-interior handoff. `source-evidence/`, `original/` and `extracts/` are provenance, not selectable prior drawings.

All obsolete processed drawings, old scripts/manifests and the old ZIP are reversibly retired under `superseded_2026-11-09/`. That folder is excluded from input resolution; no fallback is permitted. Never package or display its ZIP as current. Existing footers saying unapproved are frozen artwork; approval is recorded by pt16u in the manifest.

Start: `scripts/active_inputs.py`; validate with `scripts/verify_active_pipeline.py`. One derived cutaway illustration is permitted for review, not a complete 3D model, not a replacement XY plan. Source limitations and missing measurements remain.
