# Optimizer (Ashwood plan-visuals)

Read-only helpers; never edit `canonical/`, `active/`, or `original/`.
1. Archivist: after handoff/index updates, run `python3 optimizer/verify_incremental.py` (`--full` after big migrations).
2. Cache: `optimizer/.verify_cache.json`; report: `optimizer/verify_report.json`.
3. Before any Interior batch: `python3 optimizer/handoff_guard.py`, then read `optimizer/handoff_overlay.json` (JSON only, never CSV).
4. Overlay stamps `active_plan_version`, `dimension_transcript`, ceiling status, `match_status`, `generation_eligibility`.
5. Evidence-led concepts with labelled assumptions are allowed; blocked only if plan/CAD or brochure evidence is missing.
6. Style↔candidate overlaps are flagged and never treated as verified room matches.
7. Free `python3` stdlib only; scripts write temp files then `mv`.
