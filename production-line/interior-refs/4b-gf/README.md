# Ashwood 4B ground floor: interior reference images

**concept visualisation, not survey-verified, not construction-ready, not certified CAD.** AI-generated. review_status: needs-review. Not approved.

Lane: interior reference images (branch `lane/interior-refs`). Used by the interior builder for materials and style only; the approved V4 plan decides dimensions.

- `images/`: 15 current labelled images, one per 4B GF interior/service room in the optimizer overlay. Name: `4b-gf-<room>__<view>__<METHOD>.png`; a `_r2` suffix marks the critic-fix version (same stable room/view ID). `images/_superseded-r1/` keeps the 9 replaced r1 images for comparison; do not use them.
- `cad-check/`: the V4 plan crop each image was checked against (cut from `active/approved-cad-v4/png/FP-4B-GF_V4_long7680.png`, hash-checked against `ACTIVE_PIPELINE.json`; plan artwork unchanged).
- `index.csv`: per image: villa, floor, room, CAD check, match_status, evidence, observed, assumed, mismatches, review_status.
- `manifest.json`: hashes, raw sources, references, guard results.
- `style-guide/`: palette and finishes with source page, observed fact, inferred application and uncertainty (p15, p16, p17, p24); `refs/` holds the brochure crops attached to the generator.
- `contact-sheet/`: all 15 current images with room labels, plus `critic-fix_plan-vs-image.png` (V4 plan crop | old r1 | new r2 for the 9 critic-fix rooms, with residual mismatches).
- `scripts/`: room records, build, style-guide, CAD-compare scripts, pass-2 prompts, and r2 files (`r2_rooms.py`, `apply_r2.py`, `build_review_sheet.py`, `prompts_r2.json`).

Inputs: `ACTIVE_PIPELINE.json` and `active/approved-cad-v4/` only. `superseded_2026-11-09/` not used. match_status is copied from `optimizer/handoff_overlay.json`; no room has a verified source photo (2 ambiguous, 13 unknown).

## r2 critic fix (2026-11-10, Asia/Dubai)

Critic report: `claude/rules-and-status` @ `1f58518`, `production-line/critic/2026-11-10_q11-gf-refs.md` (CRITIC-FAIL 5/10).

- Kept (critic PASS): kitchen, maid room, maid bath, double-height entry, dress, lift (concept).
- Regenerated as `_r2` for layout against the V4 plan crop, style unchanged (p15-p17, p24): pantry, powder, office/gym, bath, living/dining, show kitchen, laundry, K. store, multipurpose. Each prompt stated room shape, door/window positions and fixtures read from the crop; each output was compared to the crop, with at most 2 attempts used. The residual mismatches are in `index.csv` (`mismatches`) and on the review sheet.
- Count correction: the earlier pass-2 record said 7 rooms were "regenerated". 6 were regenerated for layout (pantry, powder, kitchen, office/gym, maid room, maid bath), and bath was regenerated for style only (p24 wet-area finish). `index.csv` `result` now reads `regenerated` (6) and `regenerated-style-only` (bath). The new columns `critic_1f58518` and `r2_critic_fix` record the critic verdict and the r2 action.
- Status: needs-review. Not self-approved; this is waiting for the critic's re-review.

## r3 critic fix (2026-11-10, Asia/Dubai)

Critic report: `claude/rules-and-status` @ `d3e35b0`, `production-line/critic/2026-11-10_q11-gf-refs-r2.md` (CRITIC-FAIL, 9 PASS / 6 FAIL, 6/10). These 6 rooms were redone as `_r3`, conditioned on their V4 crops, with the style unchanged:
- pantry: counter capped at the 2.45 m length
- powder: narrower room, with the door moved into the north wall at the plan's gap
- living/dining: the ~2 m solid rear-wall section is restored, and the right-hand return is now solid
- laundry: the tall cupboards are removed
- K. store: the basin is moved into the NE recess, and the shelving is removed
- multipurpose: the door is at the NW corner on the north wall

The replaced r2 images are in `images/_superseded-r2/`. Office/gym, bath and show kitchen keep their `_r2` images; the other 6 rooms keep their originals. `index.csv` has two new columns, `critic_d3e35b0` and `r3_critic_fix`. `contact-sheet/critic-fix_plan-vs-image.png` now shows plan crop | r2 | r3 for the 6 rooms; the r2 sheet is in git at `b965bbd`. Scripts: `scripts/apply_fix.py` and `scripts/fix_gf_r3.py`. Status: needs-review, not self-approved.
