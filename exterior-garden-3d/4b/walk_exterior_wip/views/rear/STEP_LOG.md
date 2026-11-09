# ELEV-REAR view(s): 7-step gate log (web, `rear_pass.html`)

Builder: lane 2 (exterior). Critic: independent critic, one fix per pass. Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.
Page: `../../rear_pass.html` (same renderer as front_pass.html; rear override list only, so front-only M25/M26/M28 assumptions are not loaded).

| Step | Inputs | Outputs | Review check | Status |
|---|---|---|---|---|
| 1 Reference | EXT-4b-ELEV-REAR_GENERATED-SOURCE-CONDITIONED.png; brochure p26 | cameras cams/rear.json (from blender_wip/views_wip.json elev_rear, lens 36 -> vfov 31.4, shift) | framing vs reference | carried from exterior steps 1-4 (critic-passed for Blender set); web framing REVIEW-PENDING |
| 2 Layout | approved V4 CAD via model/data/model.js; pool 9.50 x 2.40 m (brochure) / 9.49 x 2.38 (CAD) | same footprint as front | — | inherited |
| 3 Blockout | model.js boxes | inherited | — | inherited |
| 4 Finish | warm finish flag (finish=true) | as front step 4 | side by side | inherited, REVIEW-PENDING for these views |
| 5 Printed matter | Q1 inventory | none in source | Q1 | DONE: none in source (Q1) |
| 6 Critique | side-by-side per pass | `shots/*_passN_side_by_side.png` | independent critic | ONGOING |
| 7 Motion | passed still | step 7 clip | critic | NOT STARTED |

## Pass history
- Pass 1 (2026-11-10): baseline rear set on the box. Palms on the four approved-plan tree symbols nearest the rear garden (replacing generic ball trees; palm look image-read), off-plot context lawn behind the rear boundary (image look; plan ends ~1.2 m behind the pool, M-log), low side-boundary hedges. Pool uses three.js Water2 (r160, vendored). Self-critique for pass 2: glazing reads as tan opaque slabs, the references show clear glass with lit rooms and slim frames.
- Pass 2 (2026-11-10): glazing. Dark clear glass (glass_mode interior, as front pass 8) with warm-lit floor, ceiling and back wall behind the CAD rear glass lines (gf-glass-0/1, ff-glass-rear), plus slim dark frames ~2.4 m (GF) and 5 bays (FF). Interior depths/finishes/mullion spacing are display assumptions. Self-critique for pass 3: Water2 pool reads as flat blue paint, reflections too weak to see.
