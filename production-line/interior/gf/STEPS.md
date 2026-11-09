# GF interior (FP-4B-GF) step log: lane/gf-interior

Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
Owner: thread "Finish ground floor interior steps 5–7". Loop tracker: STATUS.md.

| Step | Status | Inputs | Outputs | Review check |
|---|---|---|---|---|
| 1 Reference | DONE (carried from v2) | brochure p15–p17, p24; V4 GF plan (active/approved-cad-v4/) | references listed in Q3 handoff | n/a |
| 2 Layout | DONE (carried from v2) | V4 GF plan via data/fp-4b-gf.plan.json | FP-4B-GF/data/ | n/a |
| 3 Blockout | DONE (carried from v2) | data/ | index.html | n/a |
| 4 Grime / finish | DONE (v2 clean finish, Q3 KEEP verdicts) | index.html, verify/gf_polish_2026-11-09/ | index.html | Q4 critic: PASS furniture, media wall, pool basin, lighting; FIX entry streak (F2) |
| 5 Printed matter | DONE: none in source | canonical/references/ref-p15-living.png, ref-p15-dressing.png, ref-p16-bedroom.png | no room signage or readable text in the interior renders. Only mark: a small spiral brand logo on ref-p16-bedroom.png (top right, on the door). Brand watermark, not a room sign: not reproduced in the viewer | Labels only if visible in source: none. p17 and p24 are text-only in the brochure notes (materials), no sign images found in the repo |
| 6 Critique | BLOCKED on 5 and on F2/F3 fixes | side-by-side with references | none yet | Independent critic lane must sign off |
| 7 Motion | BLOCKED on 6 | walkthrough path (walk speed unsourced: Q3 open issue 2) | none yet | needs headless render to video |

## Courtyard module (Q7)
- Source: `FP-4B-GF/courtyard_feature_r2.js` (F3 fix: pine lowered and widened, long low bench). Syntax check passed (`node --check`, integrator 26d6bfe).
- Not wired into `index.html` yet. The viewer has an interim olive tree and pond (index.html ~line 2616 and 2925). Replacing that needs a headless render and a critic pass before index.html changes.
- Rule: new files only until critic passes, so index.html is untouched in this lane for now.

## Open items for this lane
1. Step 5: open brochure p15–p17, p24 and V4 GF labels; log what is visible; mark "none in source" only after checking.
2. F2: fix the travertine entry streak texture (index.html, after critic-approved build file).
3. Q7: wire courtyard_feature_r2.js in a new build file, render, critic.
4. Walk speed 3.2 / 7.0 m/s needs Colin's decision (unsourced).
