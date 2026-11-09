/* f3_basin_box.js - F3 (integrator ruling, critic batch 4): GF NE basin box, modelled CLOSED, no door.
 * Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
 * V4 GF plan: a small box, about 0.58 x 0.39 m (critic q11-gf-refs-r3) holding a basin symbol, in the NE corner of the
 *   K. store footprint. Its west and south sides have drawn walls (facing the K. store); its north edge sits on the laundry's south wall.
 *   Which room it opens into = **access NOT FOUND in V4** (critic withdrew "basin in the K. store"; not moved into the K. store).
 * Extent: plan x 5205-5791, y 15065-15455 mm [derived: read by eye from the V4 long7680 crop, about ±50 mm]; east and north faces = existing traced walls.
 * Partitions: 60 mm, full display wall height [assumption]. Basin: 450 x 300 mm at 0.85 m [assumption, plan basin symbol inside the box].
 */
export const BASIN_BOX = {x0:5205, x1:5791, y0:15065, y1:15455, t:60, label:'Basin box: access NOT FOUND in V4 (closed, no door)'};
export function buildBasinBox(THREE, parent, {wx, wz, top, wallMat, basinMat}){
  const B = BASIN_BOX, g = new THREE.Group(); g.name = 'f3-basin-box (access NOT FOUND in V4)'; g.userData.label = B.label;
  const M = v => v/1000, h = top;
  const add = (x0, y0, x1, y1, y, hh, m) => { const o = new THREE.Mesh(new THREE.BoxGeometry(M(x1 - x0), hh, M(y1 - y0)), m); o.position.set(wx((x0 + x1)/2), y + hh/2, wz((y0 + y1)/2)); o.castShadow = o.receiveShadow = true; o.name = 'basin-box'; g.add(o); return o; };
  add(B.x0, B.y0, B.x0 + B.t, B.y1, 0, h, wallMat);              // west partition (drawn on V4)
  add(B.x0, B.y1 - B.t, B.x1, B.y1, 0, h, wallMat);              // south partition (drawn on V4)
  const cx = (B.x0 + B.t + B.x1)/2, cy = (B.y0 + B.y1 - B.t)/2;   // basin symbol: box centre [derived]
  add(cx - 225, cy - 150, cx + 225, cy + 150, .7, .15, basinMat);
  parent.add(g); return g;
}
