/* f3_olive_tree.js - F3: procedural olive tree for the GF courtyard island, matched to the brochure (replaces the r2 pine).
 * Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
 * Evidence (Colin 2026-11-10: "olive as shown in the brochure"):
 *   brochure p12 render (extracts/pages/page110-12.png, right third): courtyard olive, broad dense crown rising past the GF
 *     glazing head and the FF slab line, fine silver-green foliage in hanging sprays, crown overhangs the courtyard
 *   brochure p18 render (extracts/pages/page110-18.png, right image): mature olive by floor-to-ceiling glazing: thick, fluted,
 *     twisted trunk that splits low into 3-4 heavy limbs spreading wide, canopy starting about 0.8 x glazing height
 *   [source: brochure p12 + p18 images; form read by eye]
 * Position: island centre of the V4 courtyard water feature [derived from the V4 trace; caller passes it].
 * Scale (no dimension in any source; derived by eye from p18 using the glazing as a ruler, GF glazing head 2.4 m = viewer display value):
 *   O1 height ~5.0 m above the soil, crown ~4.6 m wide (overhangs the 1.42 m island and part of the pond), canopy base ~1.9 m   [assumption, derived by eye p12/p18]
 *   O2 trunk ~0.46 m across at the base, 3 twisted strands, splits at ~1.1 m into 4 limbs                                        [assumption, derived by eye p18]
 *   O3 foliage: ~22,000 instanced lanceolate leaves 90 x 16 mm, dull grey-green tops / silver undersides, in drooping sprays      [assumption; colour read from p12/p18]
 *   O4 sway: whole tree <= 0.15 deg (update(t))                                                                                  [display assumption]
 * Procedural only (no downloaded asset). Licence: project code; three.js (MIT) vendored.
 */
function rng(seed){ let a = seed >>> 0; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
export const OLIVE_DA = {height:5.0, crown:4.6, canopyBase:1.9, trunkR:.23, split:1.1, limbs:4, leaves:22000, leafL:.09, leafW:.016};

function barkTex(THREE){
  const c = document.createElement('canvas'); c.width = 128; c.height = 256; const g = c.getContext('2d'), R = rng(5);
  g.fillStyle = '#5b5247'; g.fillRect(0, 0, 128, 256);
  for (let i = 0; i < 140; i++){ g.strokeStyle = R() < .5 ? `rgba(40,34,28,${.3 + R()*.4})` : `rgba(140,130,115,${.15 + R()*.25})`; g.lineWidth = 1 + R()*3;
    const x = R()*128; g.beginPath(); g.moveTo(x, R()*256); g.lineTo(x + (R() - .5)*14, R()*256); g.stroke(); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; return t;
}
// tapered tube along a curve: radius r0 -> r1
function limb(THREE, pts, r0, r1, mat){
  const curve = new THREE.CatmullRomCurve3(pts.map(p => new THREE.Vector3(...p))), segs = 18, rad = 8;
  const geo = new THREE.TubeGeometry(curve, segs, 1, rad, false), p = geo.attributes.position, n = geo.attributes.normal;
  const cp = curve.getSpacedPoints(segs);
  for (let i = 0; i <= segs; i++){ const r = r0 + (r1 - r0)*(i/segs)**.8, c = cp[i];
    for (let j = 0; j <= rad; j++){ const k = i*(rad + 1) + j; p.setXYZ(k, c.x + n.getX(k)*r, c.y + n.getY(k)*r, c.z + n.getZ(k)*r); } }
  geo.computeVertexNormals(); const m = new THREE.Mesh(geo, mat); m.castShadow = m.receiveShadow = true; return {mesh:m, curve};
}
export function buildOlive(THREE, {seed = 1207} = {}){
  const R = rng(seed), D = OLIVE_DA, g = new THREE.Group(); g.name = 'f3-olive-tree';
  const bark = new THREE.MeshStandardMaterial({map:barkTex(THREE), roughness:.95, color:'#d8d2c8'});
  const tips = [];
  // trunk: 3 twisted strands (p18 fluted trunk), base ~0.46 m across, to the split at ~1.1 m
  for (let k = 0; k < 3; k++){ const a0 = k/3*Math.PI*2, pts = [];
    for (let i = 0; i <= 6; i++){ const t = i/6, a = a0 + t*1.4, r = (.12 - .05*t); pts.push([Math.cos(a)*r + .06*t, -.05 + t*(D.split + .05), Math.sin(a)*r]); }
    g.add(limb(THREE, pts, D.trunkR*.62, D.trunkR*.42, bark).mesh); }
  // limbs: heavy, leaning out wide (p18), each with 4-5 branches and 2-3 twigs
  for (let i = 0; i < D.limbs; i++){
    const a = i/D.limbs*Math.PI*2 + (R() - .5)*.7, out = 1.0 + R()*.7, top = 2.3 + R()*.9;
    const p0 = [.06, D.split - .1, 0], p1 = [Math.cos(a)*out*.45, D.split + .55 + R()*.25, Math.sin(a)*out*.45], p2 = [Math.cos(a)*out, top, Math.sin(a)*out];
    const L = limb(THREE, [p0, p1, p2], .13, .06, bark); g.add(L.mesh);
    const nB = 4 + (R() < .5 ? 1 : 0);
    for (let j = 0; j < nB; j++){
      const b = a + (R() - .5)*1.9, t0 = .45 + R()*.55, s = L.curve.getPoint(t0), reach = .5 + R()*.9, up = .6 + R()*1.3;
      let e = [s.x + Math.cos(b)*reach, Math.min(D.height - .25, s.y + up), s.z + Math.sin(b)*reach];
      const rr = Math.hypot(e[0], e[2]); if (rr > D.crown/2 - .3){ e[0] *= (D.crown/2 - .3)/rr; e[2] *= (D.crown/2 - .3)/rr; }
      const m = [(s.x + e[0])/2 + (R() - .5)*.2, (s.y + e[1])/2 + .1, (s.z + e[2])/2 + (R() - .5)*.2];
      const B = limb(THREE, [[s.x, s.y, s.z], m, e], .05, .018, bark); g.add(B.mesh); tips.push(B.curve);
      for (let k = 0; k < 2 + (R() < .5 ? 1 : 0); k++){
        const t1 = .5 + R()*.5, q0 = B.curve.getPoint(t1), c = R()*Math.PI*2, rl = .35 + R()*.5;
        const q1 = [q0.x + Math.cos(c)*rl, Math.min(D.height - .1, q0.y + (R() - .2)*.6), q0.z + Math.sin(c)*rl];
        const T = limb(THREE, [[q0.x, q0.y, q0.z], [(q0.x + q1[0])/2, (q0.y + q1[1])/2 + .06, (q0.z + q1[2])/2], q1], .016, .005, bark); g.add(T.mesh); tips.push(T.curve);
      }
    }
  }
  // leaves: lanceolate blade (diamond), instanced, in hanging sprays along the outer part of each twig
  const lg = new THREE.BufferGeometry(), l = D.leafL, w = D.leafW/2;
  lg.setAttribute('position', new THREE.Float32BufferAttribute([0, 0, 0, w, 0, l*.45, 0, 0, l, -w, 0, l*.45], 3)); lg.setIndex([0, 1, 2, 0, 2, 3]); lg.computeVertexNormals();
  const lm = new THREE.MeshStandardMaterial({side:THREE.DoubleSide, roughness:.7, vertexColors:false});
  const im = new THREE.InstancedMesh(lg, lm, D.leaves); im.castShadow = true; im.receiveShadow = true; im.name = 'f3-olive-leaves';
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), sc = new THREE.Vector3(), pos = new THREE.Vector3(), col = new THREE.Color();
  const cTop = new THREE.Color('#6e7a58'), cSil = new THREE.Color('#aab39b'), cDk = new THREE.Color('#4f5a3e');
  for (let i = 0; i < D.leaves; i++){
    let p = tips[i % tips.length].getPoint(.25 + R()*.75); for (let tr = 0; tr < 12 && p.y < D.canopyBase; tr++) p = tips[Math.floor(R()*tips.length)].getPoint(.4 + R()*.6);
    // spray: offset around the twig, drooping (olive sprays hang), within the crown radius
    const r = .05 + R()*.42, ang = R()*Math.PI*2, droop = R()*.45;
    pos.set(p.x + Math.cos(ang)*r, p.y - droop + (R() - .3)*.15, p.z + Math.sin(ang)*r);
    const rr = Math.hypot(pos.x, pos.z); if (rr > D.crown/2){ pos.x *= D.crown/2/rr; pos.z *= D.crown/2/rr; }
    e.set(-Math.PI/2 + .9 + (R() - .5)*1.2, R()*Math.PI*2, (R() - .5)*.8); q.setFromEuler(e); const s = .8 + R()*.5; sc.set(s, s, s);
    m4.compose(pos, q, sc); im.setMatrixAt(i, m4);
    const k = R(); col.copy(k < .45 ? cTop : k < .8 ? cSil : cDk).offsetHSL(0, 0, (R() - .5)*.05); im.setColorAt(i, col);
  }
  g.add(im);
  const update = t => { g.rotation.z = .0022*Math.sin(t*.6) + .0006*Math.sin(t*1.9); g.rotation.x = .0014*Math.sin(t*.47 + 1); };
  g.userData.stats = {leaves:D.leaves, twigs:tips.length, height_m:D.height, crown_m:D.crown, source:'brochure p12 + p18 (form by eye)', assumptions:'O1-O4'};
  return {group:g, update};
}
