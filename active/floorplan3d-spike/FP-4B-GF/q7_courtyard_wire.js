/* q7_courtyard_wire.js - Q7: wires courtyard_feature_r2.js (F3-fixed pine + long low bench) into the GF viewer r3 build.
 * Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
 *
 * Inputs (no invented geometry):
 *   pond   = bounding box of PLAN.WATER "courtyard-water-feature-1" outer  [source: approved V4 GF trace via data/fp-4b-gf.plan.json]
 *   island = bounding box of its hole                                       [source: approved V4 GF trace]
 *   tree position = island centre                                          [derived; the V4 plan draws a tree symbol on the island]
 *   tree form (cloud-pruned pine), water look, stone lip, coping           [style: approved concept EXT-4b-OUTDOOR-COURTYARD_GENERATED-CONCEPT.png; all heights = assumption, see DA1-DA11 in courtyard_feature_r2.js]
 *   bench: 2.00 x 0.38 x 0.40 m at plan (9775, 9153), long axis N-S, by the west glazing
 *          [ASSUMPTION: not drawn on the V4 GF plan; the bench appears only in the approved concept image. Position copied from courtyard_test.html. Critic to keep or drop: ?bench=0 hides it]
 *   water: three.js Water2 r160, vendored locally (./vendor/three/examples/jsm/objects/Water2.js); res 512 = display/perf assumption
 * Replaces in the r3 build only: the interim courtyard pond basin / lite water / island planter (index.html buildBasin/buildWater
 * for the non-pool water) and the interim olive tree (index.html buildDecor item 6). index.html itself is unchanged.
 */
import { buildCourtyard, buildBench } from './courtyard_feature_r2.js';

export const COURT_DEFAULTS = {waterRes:512, bench:{plan:[9775, 9153], rotY:Math.PI/2}};

function bbox(pts){ const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]); return [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)]; }

export function wireCourtyard(THREE, {PLAN, wx, wz, renderer, floorY = 0, bench = true}){
  const w = (PLAN.WATER || []).find(o => !/pool/i.test(o.id) && (o.holes || []).length);
  if (!w) throw new Error('Q7: no courtyard water with an island in PLAN.WATER (NOT FOUND)');
  const [px0, py0, px1, py1] = bbox(w.outer), [ix0, iy0, ix1, iy1] = bbox(w.holes[0]);
  const pond = {x0:wx(px0), z0:wz(py0), x1:wx(px1), z1:wz(py1)}, island = {x0:wx(ix0), z0:wz(iy0), x1:wx(ix1), z1:wz(iy1)};
  const cy = buildCourtyard(THREE, {pond, island, floorY, renderer, waterRes:COURT_DEFAULTS.waterRes});
  cy.group.name = 'q7-courtyard';
  let b = null;
  if (bench){ b = buildBench(THREE); const [bx, by] = COURT_DEFAULTS.bench.plan; b.position.set(wx(bx), floorY, wz(by)); b.rotation.y = COURT_DEFAULTS.bench.rotY; b.name = 'q7-bench-ASSUMPTION'; cy.group.add(b); }
  cy.group.traverse(o => { o.raycast = () => {}; });   // decor: not pickable
  const meta = {...cy.meta, source_water_id:w.id, pond_plan_mm:[px0, py0, px1, py1], island_plan_mm:[ix0, iy0, ix1, iy1], bench:!!b, bench_status:'assumption (concept image only, not on V4 plan)'};
  return {group:cy.group, update:cy.update, dispose:cy.dispose, meta};
}
