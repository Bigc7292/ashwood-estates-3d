# Exterior quality_r1 — functional increment evidence (text; binaries outside repo)

Change-set: viewer-quality-2026-11-10, lane/exterior-quality. Captures: /mnt/agents/work/integration-evidence/exterior-quality/quality_r1/{before,after}/*.png
Pages: front_v2.html, left_pass.html, right_pass.html, site_pass.html, rear_v3.html. Viewport 1280x720, locked cameras cameras/lock_*.json (identical before/after).

## What changed (functional increment)
1. Water2 (all five sources): confirmed rear_pass3_water2.js settings are now ACTIVE defaults in source (reflectivity 0.32, scale 1.1,
   flowSpeed 0.035; MODEL_OVERRIDES.water2 can still tune). Plus the confirmed rear_pass.html orientation fix: flat XY ShapeGeometry +
   mesh.rotation.x=-PI/2 so the Reflector/Refractor actually render; window.__WATERMESH exposed; deterministic flow via window.__T in __frame.
2. OrbitControls instantiated for locked ?view= hub cameras (drag orbits, wheel/pinch zooms; damping off; shift-lens views re-apply the shift
   on 'change'). Walk mode (no ?view=) untouched. Caption gains "Locked hub view: drag to orbit, wheel / pinch to zoom." (instructions match behaviour).
3. Deterministic capture: front_v2.html ported to the shared __capture/__frame pattern; __frame sets __capture=true and __T=t in all five pages,
   so capture mode renders exactly one requested frame and continuous rendering stops.
4. Seeded PRNG: every bare Math.random() in the five sources replaced by a fixed-seed LCG RND() (18 sites per page). Reproducible captures.
5. Probe hooks: window.__info() (renderer counts/view/viewport) and window.__project(x,y,z) (screen projection) added to all five pages.
6. tools/quality_capture.py: free python-playwright capture/probe/orbit/walk tool (still | probe | orbit | walk), zero external assets.
7. M38 (right_pass5_rear_overhang.js): rear-lane proposal z0 0.53->2.56 was FALSIFIED by the independent critic (approved ELEV-RIGHT
   re-measure matches the original 64 px projection at z0=0.53 within +/-2 px; 2.56 contradicts the source by ~76 px; report
   /mnt/agents/output/rear-critic-report.md). z0=0.53 stands; finding recorded in the override header.

## Probe values (SwiftShader headless chromium; 0 page errors, 0 failed requests on every run)
| page | renderer calls | triangles | water meshes | pool crop px | t5-vs-t6 mean/max | water-vs-hidden mean/max |
|---|---|---|---|---|---|---|
| rear_v3 (ELEV-REAR lock) | 885 | 18678 | 2 | [326,562,1076,676] | 1.45 / 61 | 16.46 / 63 |
| front_v2 (ELEV-FRONT lock) | 1255 | 116106 | 2 | [511,547,744,561] | 0.51 / 6 | 0.0 / 0 (pool behind house from street; proof carried by rear/site) |

Still captures renderer counts: front 1016 calls / 101816 tris; rear 860 calls / 15576 tris.

## Before/after visual inspection
- rear: BEFORE pool was an opaque flat pale slab (Water2 orientation bug: reflection/refraction contributed nothing). AFTER: rippled,
  reflective, refractive surface over the mosaic basin; hiding __WATERMESH exposes the basin floor. Defect attributed (Water2 plane
  transform) and fixed; verified by hide/show + two-frame diffs above.
- front: framing and labels intact; pool correctly not visible from the street.

## Open (next change sets)
- left/right/site after captures pending sandbox CPU contention (before pairs taken, locks unchanged).
- Presentation: technical labels default off (opt-in via view JSON) keeping the concept disclaimer; pale seating bases (display treatment).
- Proposed hub cameras: cameras/lock_site_full.json (full villa + pool, no roof clip), cameras/lock_rear_eye.json (near-eye-level off-axis;
  garden-tree-rear-c NOT moved) from rear-lane evidence.
- Orbit/walk numeric probes to be appended per page (tool ready: orbit | walk modes).

Labels: concept visualisation, not survey-verified, not construction-ready, not certified CAD.
