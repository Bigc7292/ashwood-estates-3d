/* q7_courtyard_wire.js - Q7 + F3: wires courtyard_feature_r2.js into the GF viewer r3 build.
 * Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
 *
 * Inputs (no invented geometry):
 *   pond   = bounding box of PLAN.WATER "courtyard-water-feature-1" outer  [source: approved V4 GF trace via data/fp-4b-gf.plan.json]
 *   island = bounding box of its hole                                       [source: approved V4 GF trace]
 *   tree   = OLIVE (f3_olive_tree.js) at the island centre                  [species: brochure p12 render; position derived: V4 draws a tree symbol on the island]
 *            F3 (integrator ruling 2026-11-10): the r2 pine (approved concept image) is removed; conflict logged in MISMATCH_LOG.md (GF-M1)
 *   pond lip, coping, basin, island planter, grass                         [style: approved concept EXT-4b-OUTDOOR-COURTYARD; heights = assumption DA1-DA5 in courtyard_feature_r2.js]
 *   water: three.js Water2 r160, vendored locally; res WATER2_RES, passes throttled (f3_water_perf.js)
 *   bench: DROPPED in F3 (image-only, not on V4; MISMATCH_LOG.md GF-M2)
 * Replaces in the r3 build only: the interim courtyard pond basin / lite water / island planter and the interim olive blobs of index.html.
 */
import { buildCourtyard } from './courtyard_feature_r2.js';
import { buildOlive } from './f3_olive_tree.js';
import { WATER2_RES, throttleWater } from './f3_water_perf.js';

const DA_SOIL_TOP = .21;   // = DA5 soilTop in courtyard_feature_r2.js (assumption)
function bbox(pts){ const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]); return [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)]; }

export function wireCourtyard(THREE, {PLAN, wx, wz, renderer, floorY = 0}){
  const w = (PLAN.WATER || []).find(o => !/pool/i.test(o.id) && (o.holes || []).length);
  if (!w) throw new Error('Q7: no courtyard water with an island in PLAN.WATER (NOT FOUND)');
  const [px0, py0, px1, py1] = bbox(w.outer), [ix0, iy0, ix1, iy1] = bbox(w.holes[0]);
  const pond = {x0:wx(px0), z0:wz(py0), x1:wx(px1), z1:wz(py1)}, island = {x0:wx(ix0), z0:wz(iy0), x1:wx(ix1), z1:wz(iy1)};
  const cy = buildCourtyard(THREE, {pond, island, floorY, renderer, waterRes:WATER2_RES});
  cy.group.name = 'q7-courtyard';
  // F3: olive replaces the r2 pine
  cy.group.remove(cy.tree); cy.tree.traverse(o => { if (o.geometry) o.geometry.dispose(); });
  const olive = buildOlive(THREE);
  olive.group.position.set((island.x0 + island.x1)/2, floorY + DA_SOIL_TOP + .02, (island.z0 + island.z1)/2); cy.group.add(olive.group);
  let water_error = null;
  if (cy.meta.waterMode === 'water2') throttleWater(cy.water, {flowSpeed:.006});
  else { cy.group.remove(cy.water); water_error = 'Water2 unavailable: courtyard water not shown (no fallback by design, F3)'; console.error(water_error); }
  cy.group.traverse(o => { o.raycast = () => {}; });   // decor: not pickable
  const meta = {...cy.meta, tree:{species:'olive (brochure p12)', ...olive.group.userData.stats}, source_water_id:w.id, pond_plan_mm:[px0, py0, px1, py1], island_plan_mm:[ix0, iy0, ix1, iy1], bench:false, water_res:WATER2_RES, water_error};
  const update = (dt, t) => olive.update(t);
  return {group:cy.group, update, dispose:cy.dispose, meta};
}
