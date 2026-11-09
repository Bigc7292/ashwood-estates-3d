# GF interior step 7: motion (walkthrough to video)

Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
Branch: lane/gf-interior-step7 (cut from lane/gf-interior at 8368286, which is merged via PR #4).

## Status
- Step 6 pack (2ed944a, loop 1) exists on lane/gf-interior. Independent critic pass: NOT YET RUN. Step 7 does not start until the critic passes step 6.
- Step 7 gate: WIP, planned, not rendered.

## Plan
1. Walk path: entry, living/dining, kitchen, pool terrace. Keep the walk speed out of sign-off until Colin sets it (unsourced 3.2 / 7.0 m/s, Q3 open issue 2).
2. Capture frames headlessly from FP-4B-GF/index.html with a fixed camera list, then encode to video.
3. Output paths go under production-line/interior/gf/step7/ (new files only).
4. Critic reviews the video frames against the step 6 references. Defects loop back to the earliest affected step.

## Open
- Video encoding tool: check what is installed before choosing; no paid tools (AGENTS rule 1).
- Walk speed decision (Colin).
