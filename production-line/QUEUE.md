# Production queue (Ashwood)

Owner key: L1 facts, L2 exterior, L3 interior, L4 viewer, L5 critic, L6 integrator. One item per lane at a time.

| ID | Lane | Item | Depends on | Status |
|---|---|---|---|---|
| Q1 | L2 | Exterior step 5: printed matter (check the 10 approved images and brochure p25/p26 for signage; record "none in source" if none) | none | REVIEW-PENDING (no signage found) |
| Q2 | L1 | Fact sheet for exterior steps 5–7 and the interior: CAD dimensions, brochure pages, open mismatches (M12, M24) | none | REVIEW-PENDING (facts/Q2_fact_sheet.md) |
| Q3 | L3 | Review the 17:15 GF polish WIP (`verify/gf_polish_2026-11-09/`) and list what should be kept | none | REVIEW-PENDING (handoffs/Q3.md) |
| Q4 | L5 | Critic pass on the 16:39 WIP snapshot (exterior blender_wip renders and GF viewer) | Q3 | QUEUED |
| Q5 | L2 | Exterior step 6: critique close-ups against the reference images, list defects, fix | Q1, Q4 | QUEUED |
| Q6 | L2 | Exterior step 7: motion (pool water, palm sway, sun change, slow push-in) rendered to video | Q5 | QUEUED |
| Q7 | L3 | Courtyard module: integrate as a separate build file, then critic | Q4 | QUEUED |
| Q8 | L4 | Walkable exterior viewer from the lane-2 model, once it has a critic pass | Q6 | QUEUED |
| Q9 | L6 | Log every lane's hand-off in CHANGELOG.md; push to claude/rules-and-status | every item | ONGOING |

## Q4 critic verdicts (hand-off in production-line/handoffs/Q4.md, commit 212c79f; verified by integrator 18:10)

| Item | Verdict (as reported) | Queued fix |
|---|---|---|
| Exterior WIP, back garden and pool views (`blender_wip/`) | CRITIC-FAIL on appearance: palms, balcony screen, glazing, pool coping | F1 (L2): fix palms, balcony screen, glazing and pool coping, then re-critique |
| GF viewer: furniture, media wall, pool basin, lighting | PASS | none |
| GF viewer: entry travertine streak, entry ceiling lining, walk speed 3.2/7.0 m/s | FIX | F2 (L3): fix the streak and label the ceiling as an assumption. Walk speed is Colin's choice (his clone) |
| Courtyard round 1 (tree, bench) | not ready to integrate | F3 (L3): tree and bench fix before Q7 |
| M24 back pier side | the critic says brochure p26 and the rear elevation both put the pier left of centre, which contradicts the mismatch note (right of centre). WIP rear render not yet checked | F4 (L1): re-check M24 against p26 and the elevation, then correct the mismatch log |

Verification: the integrator opened the referenced images. The brochure p26 render and the rear elevation both put the GF stone panel at roughly 0.29–0.44 of the building width, left of centre, so the M24 note (right of centre) is wrong for the references. Walk speed line confirmed at index.html line 3191. Status: Q4 REVIEW-PENDING (verdicts verified against references; the WIP rear render check for M24 is still open under F4).

