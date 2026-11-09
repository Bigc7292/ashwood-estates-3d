# Ashwood 4B ground floor: interior reference images

**concept visualisation, not survey-verified, not construction-ready, not certified CAD.** AI-generated. review_status: needs-review. Not approved.

Lane: interior reference images (branch `lane/interior-refs`). Used by the interior builder for materials and style only; the approved V4 plan decides dimensions.

- `images/`: 15 labelled images, one per 4B GF interior/service room in the optimizer overlay. Name: `4b-gf-<room>__<view>__<METHOD>.png`.
- `cad-check/`: the V4 plan crop each image was checked against (cut from `active/approved-cad-v4/png/FP-4B-GF_V4_long7680.png`, hash-checked against `ACTIVE_PIPELINE.json`; plan artwork unchanged).
- `index.csv`: per image: villa, floor, room, CAD check, match_status, evidence, observed, assumed, mismatches, review_status.
- `manifest.json`: hashes, raw sources, references, guard results.
- `style-guide/`: palette and finishes with source page, observed fact, inferred application and uncertainty (p15, p16, p17, p24); `refs/` holds the brochure crops attached to the generator.
- `contact-sheet/`: all 15 with room labels.
- `scripts/`: room records, build, style-guide, CAD-compare scripts and pass-2 prompts.

Inputs: `ACTIVE_PIPELINE.json` and `active/approved-cad-v4/` only. `superseded_2026-11-09/` not used. match_status is copied from `optimizer/handoff_overlay.json`; no room has a verified source photo (2 ambiguous, 13 unknown).
