# Ashwood 4B first floor: interior reference images

**concept visualisation, not survey-verified, not construction-ready, not certified CAD.** AI-generated. review_status: needs-review. Not approved.

Lane: interior reference images (branch `lane/interior-refs`). Same process, labels and layout as `../4b-gf/`. Materials and style only; the approved V4 plan decides dimensions.

- `images/`: 14 labelled images, one per 4B FF interior/service room in the optimizer overlay. Name: `4b-ff-<room>__<view>__<METHOD>.png`.
- `cad-check/`: the V4 plan crop each image was checked against (from `active/approved-cad-v4/png/FP-4B-FF_V4_long7680.png`, hash-checked against `ACTIVE_PIPELINE.json`; plan artwork unchanged).
- `index.csv`: villa, floor, room, CAD check, match_status, evidence, observed, assumed, mismatches, review_status.
- `manifest.json`: hashes, raw sources, references, guard results.
- `contact-sheet/`: all images with room labels.
- `scripts/`: room records, build script and prompts (pass 1 plus pass-2 changes).
- Style guide: the shared 4B guide at `../4b-gf/style-guide/` (no new items for this floor).

All 14 images are new for this floor (8 accepted at pass 1, 6 regenerated once after the CAD check). Inputs: `ACTIVE_PIPELINE.json` and `active/approved-cad-v4/` only; `superseded_2026-11-09/` not used. match_status is copied from `optimizer/handoff_overlay.json`; no room has a verified source photo.

## r2 critic fix (2026-11-10, Asia/Dubai)

Critic report: `claude/rules-and-status` @ `1e4df63`, `production-line/critic/2026-11-10_q11-ff-rf-refs.md` (FF/RF CRITIC-FAIL, 14 pass / 4 fail). On this floor, corridor and bath-2 were regenerated as `_r2`, conditioned on their `cad-check/` V4 crops, with the style unchanged. The replaced images are in `images/_superseded-r1/`; don't use them. The other 12 rooms are unchanged. `index.csv` has two new columns, `critic_1e4df63` and `r2_critic_fix`. The residual mismatches are in `mismatches` and on `contact-sheet/critic-fix_plan-vs-image.png` (plan crop | old | new). The scripts are `scripts/apply_fix.py` and `scripts/fix_ff_r2.py`. Status: needs-review, not self-approved.
