# Ashwood 4B roof floor: interior reference images

**concept visualisation, not survey-verified, not construction-ready, not certified CAD.** AI-generated. review_status: needs-review. Not approved.

Lane: interior reference images (branch `lane/interior-refs`). Same process, labels and layout as `../4b-gf/`. Materials and style only; the approved V4 plan decides dimensions.

- `images/`: 4 labelled images, one per 4B RF interior/service room in the optimizer overlay. Name: `4b-rf-<room>__<view>__<METHOD>.png`.
- `cad-check/`: the V4 plan crop each image was checked against (from `active/approved-cad-v4/png/FP-4B-RF_V4_long7680.png`, hash-checked against `ACTIVE_PIPELINE.json`; plan artwork unchanged).
- `index.csv`: villa, floor, room, CAD check, match_status, evidence, observed, assumed, mismatches, review_status.
- `manifest.json`: hashes, raw sources, references, guard results.
- `contact-sheet/`: all images with room labels.
- `scripts/`: room records, build script and prompts (pass 1 plus pass-2 changes).
- Style guide: the shared 4B guide at `../4b-gf/style-guide/` (no new items for this floor).

All 4 images are new for this floor (1 accepted at pass 1, 3 regenerated once after the CAD check). Inputs: `ACTIVE_PIPELINE.json` and `active/approved-cad-v4/` only; `superseded_2026-11-09/` not used. match_status is copied from `optimizer/handoff_overlay.json`; no room has a verified source photo.

Not included: the roof terrace (outdoor, exterior lane) and the RF stair core (no overlay record). The RF plan is labelled NOT TO SCALE with every room dimension flagged uncertain (dagger).
