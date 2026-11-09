/* f3_dress_wardrobe.js - F3 (critic G4): dress-room glass-front wardrobe on the V4 joinery block. No island.
 * Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
 * Footprint: PLAN.FURNITURE "Dress wardrobe" cx 5507, cy 17126, 1101 x 568 mm, rot 90 -> plan x 5223-5791, y 16576-17677
 *            [source plan symbol, size approximate: approved V4 GF joinery block on the dress room's east side]
 * Look: brochure p15 dressing render (canonical/references/ref-p15-dressing.png): bronze-framed glass doors, lit interior,
 *       hanging clothes and shelves, taupe/oak carcass [source image, read by eye]
 * Height 2.40 m, 2 doors, bronze frame 20 mm, glass bronze-tinted 35% opaque, interior LED + warm point light [assumption]
 * The p15 island is NOT modelled: the V4 plan draws none and the room is 1.10 m wide.
 */
function rng(seed){ let a = seed >>> 0; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
export const DRESS_ROBE = {x0:5223, x1:5791, y0:16576, y1:17677, h:2.4};
export function buildDressWardrobe(THREE, wx, wz){
  const D = DRESS_ROBE, R = rng(15), g = new THREE.Group(); g.name = 'f3-dress-wardrobe'; g.userData.noMerge = true;
  const X0 = wx(D.x0), X1 = wx(D.x1), Z0 = wz(D.y0), Z1 = wz(D.y1), W = Z1 - Z0, Dp = X1 - X0, cz = (Z0 + Z1)/2;
  const M = (c, o = {}) => new THREE.MeshStandardMaterial({color:c, roughness:.5, ...o});
  const carcass = M('#a48b72', {roughness:.45}), inner = M('#e9dfcf', {roughness:.8, emissive:'#ffdcae', emissiveIntensity:.18});
  const bronze = M('#5a4433', {metalness:.85, roughness:.32}), glass = new THREE.MeshPhysicalMaterial({color:'#6b5a48', roughness:.05, metalness:0, transparent:true, opacity:.35, depthWrite:false});
  const add = (w, h, d, m, x, y, z) => { const o = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); o.position.set(x, y, z); o.castShadow = o.receiveShadow = true; g.add(o); return o; };
  // carcass: back, sides, top, base (open front toward -x, i.e. into the room)
  add(.02, D.h, W, carcass, X1 - .01, D.h/2, cz); add(Dp, D.h, .02, carcass, X0 + Dp/2, D.h/2, Z0 + .01); add(Dp, D.h, .02, carcass, X0 + Dp/2, D.h/2, Z1 - .01);
  add(Dp, .03, W, carcass, X0 + Dp/2, D.h - .015, cz); add(Dp, .08, W, M('#4a4641'), X0 + Dp/2, .04, cz);
  add(.01, D.h - .2, W - .06, inner, X1 - .025, D.h/2, cz);   // lit back panel
  // interior: hanging rail with garments (upper zone) and 3 shelves with folded items (lower zone), half-and-half along y
  const zm = cz;
  add(.015, .015, (zm - Z0) - .06, bronze, X0 + Dp/2, 1.95, (Z0 + zm)/2);
  const tones = ['#e7dfd2', '#8f8173', '#c9bba8', '#3f3a35', '#b59f86', '#d8d0c4'];
  for (let k = 0, z = Z0 + .06; z < zm - .06; k++, z += .05 + R()*.03) add(.42, .8 + R()*.35, .02 + R()*.02, M(tones[k % tones.length], {roughness:.95}), X0 + Dp/2, 1.9 - (.8 + R()*.35)/2, z);
  for (let s = 0; s < 4; s++){ const y = .35 + s*.5; add(Dp - .06, .02, (Z1 - zm) - .04, M('#d9cebd'), X0 + Dp/2, y, (zm + Z1)/2);
    for (let k = 0; k < 3; k++) add(.3, .08 + R()*.06, .22, M(tones[(s + k) % tones.length], {roughness:.95}), X0 + Dp/2, y + .06, zm + .08 + k*.17); }
  // fronts: 2 bronze-framed glass doors on the room face (x = X0)
  const nd = 2, dw = W/nd;
  for (let i = 0; i < nd; i++){ const z = Z0 + dw*(i + .5);
    const gl = add(.006, D.h - .12, dw - .03, glass, X0 + .01, D.h/2 + .02, z); gl.castShadow = false;
    add(.025, D.h - .1, .02, bronze, X0 + .01, D.h/2 + .02, z - dw/2 + .012); add(.025, D.h - .1, .02, bronze, X0 + .01, D.h/2 + .02, z + dw/2 - .012);
    add(.025, .02, dw - .02, bronze, X0 + .01, .1, z); add(.025, .02, dw - .02, bronze, X0 + .01, D.h - .04, z);
    add(.03, .5, .012, bronze, X0 - .01, 1.1, z + (i ? -1 : 1)*(dw/2 - .06)); }   // pull
  const L = new THREE.PointLight(0xffdcb0, 1.6, 3.2, 2); L.position.set(X0 + Dp*.4, 2.1, cz); g.add(L);   // DA: interior LED glow
  g.traverse(o => { o.raycast = () => {}; });
  return g;
}
