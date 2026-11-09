/* courtyard_feature.js - Ashwood Estates 4B GF courtyard water feature (procedural, real-time, three.js r160)
 *
 * Target look: approved concept EXT-4b-OUTDOOR-COURTYARD_GENERATED-CONCEPT.png (cloud-pruned black pine on a low
 * travertine planter island in a calm, clear, shallow reflecting pond; slim oak bench by the glazing).
 *
 * Positions and sizes of the POND and the ISLAND come only from opts (CAD-derived rectangles, metres, viewer frame).
 * Nothing here moves or resizes them. Everything else is a DISPLAY ASSUMPTION (not in any source):
 *   DA1  pond depth 0.35 m below paving (stone basin floor at floorY - 0.35)
 *   DA2  water line 0.045 m below paving
 *   DA3  stone lip: 0.08 m wide light limestone band inside the CAD pond outline, top flush with paving (+4 mm)
 *   DA4  island planter: travertine body inset 15 mm under a 0.10 m wide x 0.06 m coping; coping top floorY + 0.25 m
 *        (0.295 m above the water line); the coping's outer edge = the CAD island rectangle
 *   DA5  planting soil top floorY + 0.21 m, covered with ~300 instanced ornamental-grass tufts (0.15-0.32 m) + 7 stones
 *   DA6  tree: single cloud-pruned Japanese black pine, ~3.4 m above the soil (top ~3.6 m above paving),
 *        crown ~3.3 m wide, 8 flat foliage pads, trunk base dia ~0.30 m (+ root flare); placed at the island centre
 *   DA7  tree yaw: opts.treeYaw (default 0 => the "front" of the tree faces +Z)
 *   DA8  water: three.js Water2 (vendored r160), pale blue-grey tint, very slow flow, reflectivity 0.40 (+ fresnel)
 *   DA9  bench (buildBench): natural oak, 1.60 x 0.40 x 0.45 m; 70 mm plank on two 0.30 m wide block legs
 *   DA10 textures are procedural canvases (no downloaded assets). Travertine panel 1.2 x 0.6 m; basin limestone 0.6 m.
 *   DA11 subtle sway: whole tree rotates <= 0.25 deg about its base (update(dt, t))
 *
 * API
 *   import { buildCourtyard, buildBench } from './courtyard_feature.js';
 *   const cy = buildCourtyard(THREE, { pond:{x0,z0,x1,z1}, island:{x0,z0,x1,z1}, floorY:0, renderer });
 *   scene.add(cy.group);                       // cy.group.userData.update === cy.update
 *   per frame: cy.update(dt, t);               // dt, t in seconds
 *   cy.dispose();                              // frees geometries / materials / textures / water targets
 *   const bench = buildBench(THREE); bench.position.set(x, floorY, z); bench.rotation.y = a; scene.add(bench);
 * Water2 imports the bare specifier 'three': the page needs an importmap mapping "three" to the same
 * vendor/three/build/three.module.js that THREE comes from (the viewer and the test page both do).
 * Licence: project code. three.js (MIT) is vendored under ./vendor/three. Water normal maps are three.js examples (MIT).
 */
import { Water } from './vendor/three/examples/jsm/objects/Water2.js';

// Water2 shader variant: refraction / reflection distortion 0.05 -> 0.014 (calm pond, no wobbly floor), and the refracted
// floor is attenuated towards blue-grey (0.35 m of clear water) before the fresnel mix.
function calmWaterShader(){
  const S = Water.WaterShader, fs = S.fragmentShader
    .replace('coord.z * normal.xz * 0.05', 'coord.z * normal.xz * 0.014')
    .replace('vec4 refractColor = texture2D( tRefractionMap, uv );', 'vec4 refractColor = texture2D( tRefractionMap, uv ); refractColor.rgb *= vec3( 0.66, 0.76, 0.80 );');
  if (fs === S.fragmentShader) console.warn('courtyard: Water2 shader patch did not apply');
  return {name:'CalmWaterShader', uniforms:THREE_UNIFORMS_CLONE(S.uniforms), vertexShader:S.vertexShader, fragmentShader:fs};
}
function THREE_UNIFORMS_CLONE(u){ const o = {}; for (const k in u){ const v = u[k].value; o[k] = {value:v && v.clone ? v.clone() : v}; } return o; }

const DA = {
  pondDepth: .35, waterDrop: .045, lipW: .08,
  copingTop: .25, copingW: .10, copingT: .06, bodyInset: .015, soilTop: .21,
  treeYaw: 0,
};

// ---------------------------------------------------------------- small helpers
function rng(seed){ let a = seed >>> 0; return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
const lerp = (a, b, t) => a + (b - a)*t, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
function canvas(w, h){ const c = document.createElement('canvas'); c.width = w; c.height = h; return [c, c.getContext('2d')]; }

function mergeGeos(THREE, geos){   // indexed or not; keeps position/normal/uv(/color when all have it)
  const list = geos.map(g => g.index ? g : (() => { const n = g.attributes.position.count, idx = []; for (let i = 0; i < n; i++) idx.push(i); g.setIndex(idx); return g; })());
  const hasC = list.every(g => g.attributes.color);
  let nv = 0, ni = 0; list.forEach(g => { nv += g.attributes.position.count; ni += g.index.count; });
  const P = new Float32Array(nv*3), N = new Float32Array(nv*3), U = new Float32Array(nv*2), C = hasC ? new Float32Array(nv*3) : null, I = new Uint32Array(ni);
  let ov = 0, oi = 0;
  list.forEach(g => {
    const n = g.attributes.position.count;
    P.set(g.attributes.position.array, ov*3);
    if (g.attributes.normal) N.set(g.attributes.normal.array, ov*3);
    if (g.attributes.uv) U.set(g.attributes.uv.array, ov*2);
    if (C) C.set(g.attributes.color.array, ov*3);
    const ix = g.index.array; for (let i = 0; i < ix.length; i++) I[oi + i] = ix[i] + ov;
    ov += n; oi += ix.length; g.dispose();
  });
  const out = new THREE.BufferGeometry();
  out.setAttribute('position', new THREE.BufferAttribute(P, 3)); out.setAttribute('normal', new THREE.BufferAttribute(N, 3)); out.setAttribute('uv', new THREE.BufferAttribute(U, 2));
  if (C) out.setAttribute('color', new THREE.BufferAttribute(C, 3));
  out.setIndex(new THREE.BufferAttribute(I, 1)); out.computeBoundingSphere(); out.computeBoundingBox();
  return out;
}

// BoxGeometry with UVs in metres / tile (so textures are at real scale on every face)
export function worldBox(THREE, w, h, d, tileU = 1, tileV = 1){
  const g = new THREE.BoxGeometry(w, h, d), uv = g.attributes.uv, nr = g.attributes.normal, p = g.attributes.position;
  for (let i = 0; i < uv.count; i++){
    const nx = Math.abs(nr.getX(i)), ny = Math.abs(nr.getY(i));
    const x = p.getX(i), y = p.getY(i), z = p.getZ(i);
    let u, v; if (nx > .5){ u = z; v = y; } else if (ny > .5){ u = x; v = z; } else { u = x; v = y; }
    uv.setXY(i, u/tileU, v/tileV);
  }
  return g;
}

// ---------------------------------------------------------------- procedural textures (cached per THREE instance)
const TEX = new WeakMap();
function texCache(THREE){ if (!TEX.has(THREE)) TEX.set(THREE, {}); return TEX.get(THREE); }

/** Travertine: one texture tile = one 1.2 x 0.6 m panel (joint on the tile border). opts.joint=false for no joints. */
export function travertineTexture(THREE, {joint = true, seed = 7, tone = 0} = {}){
  const key = 'trav' + joint + seed + tone, C = texCache(THREE); if (C[key]) return C[key];
  const W = 1024, H = 512, [c, x] = canvas(W, H), R = rng(seed);
  const base = [[214, 190, 152], [226, 206, 172], [208, 184, 146]][tone % 3];
  x.fillStyle = `rgb(${base})`; x.fillRect(0, 0, W, H);
  // broad horizontal banding
  for (let i = 0; i < 26; i++){ const y = R()*H, h = 6 + R()*40, d = (R() - .5)*16;
    x.fillStyle = `rgba(${base[0] + d|0},${base[1] + d|0},${base[2] + d*1.2|0},.35)`; x.fillRect(0, y, W, h); }
  // fine veins (long thin horizontal strokes)
  for (let i = 0; i < 260; i++){ const y = R()*H, x0 = R()*W, L = 60 + R()*420, dk = R() < .7;
    x.strokeStyle = dk ? `rgba(150,122,86,${.10 + R()*.22})` : `rgba(250,242,226,${.25 + R()*.3})`; x.lineWidth = .6 + R()*1.4;
    x.beginPath(); x.moveTo(x0, y); for (let s = 1; s <= 6; s++) x.lineTo(x0 + L*s/6, y + (R() - .5)*2.2); x.stroke(); }
  // travertine pits: short elongated darker voids
  for (let i = 0; i < 420; i++){ const px = R()*W, py = R()*H, l = 2 + R()*9;
    x.fillStyle = `rgba(${120 + R()*30|0},${98 + R()*25|0},${70 + R()*20|0},${.25 + R()*.35})`; x.fillRect(px, py, l, .8 + R()*1.4); }
  // speckle
  const id = x.getImageData(0, 0, W, H), a = id.data; for (let i = 0; i < a.length; i += 4){ const n = (R() - .5)*9; a[i] += n; a[i + 1] += n; a[i + 2] += n; } x.putImageData(id, 0, 0);
  if (joint){ x.fillStyle = 'rgba(140,118,90,.75)'; x.fillRect(0, 0, W, 2); x.fillRect(0, 0, 2, H); x.fillStyle = 'rgba(255,248,235,.5)'; x.fillRect(0, 2, W, 1); x.fillRect(2, 0, 1, H); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return C[key] = t;
}
function limestoneTexture(THREE){   // pale honed limestone for the basin floor / lip, 0.6 m tiles
  const C = texCache(THREE); if (C.lime) return C.lime;
  const W = 512, H = 512, [c, x] = canvas(W, H), R = rng(31);
  x.fillStyle = 'rgb(214,208,193)'; x.fillRect(0, 0, W, H);
  for (let i = 0; i < 900; i++){ const r = 1 + R()*4; x.fillStyle = `rgba(${R() < .5 ? '170,160,140' : '240,236,226'},${.12 + R()*.18})`; x.beginPath(); x.arc(R()*W, R()*H, r, 0, 7); x.fill(); }
  const id = x.getImageData(0, 0, W, H), a = id.data; for (let i = 0; i < a.length; i += 4){ const n = (R() - .5)*10; a[i] += n; a[i + 1] += n; a[i + 2] += n; } x.putImageData(id, 0, 0);
  x.fillStyle = 'rgba(150,140,122,.6)'; x.fillRect(0, 0, W, 2); x.fillRect(0, 0, 2, H);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return C.lime = t;
}
function barkTexture(THREE){   // vertical fissured pine bark; u = around the stem, v = along it (1 tile = 0.5 m)
  const C = texCache(THREE); if (C.bark) return C.bark;
  const W = 256, H = 512, [c, x] = canvas(W, H), R = rng(5);
  x.fillStyle = 'rgb(112,96,82)'; x.fillRect(0, 0, W, H);
  for (let i = 0; i < 60; i++){ const px = R()*W, py = R()*H, w = 14 + R()*26, h = 30 + R()*90, g = 120 + R()*40;   // plates
    x.fillStyle = `rgba(${g + 8|0},${g - 4|0},${g - 18|0},.55)`; x.fillRect(px - w/2, py, w, h); x.fillRect(px - w/2 - W, py, w, h); x.fillRect(px - w/2, py - H, w, h); }
  for (let i = 0; i < 34; i++){   // dark wavy fissures
    let px = R()*W; const lw = 1.5 + R()*3.5; x.strokeStyle = `rgba(38,30,24,${.6 + R()*.35})`; x.lineWidth = lw;
    x.beginPath(); x.moveTo(px, 0); for (let y = 0; y <= H; y += 16){ px += (R() - .5)*7; x.lineTo(px, y); } x.stroke();
    x.save(); x.translate(W, 0); x.stroke(); x.restore(); x.save(); x.translate(-W, 0); x.stroke(); x.restore();
  }
  for (let i = 0; i < 80; i++){ x.strokeStyle = `rgba(40,32,26,.45)`; x.lineWidth = 1; const px = R()*W, py = R()*H; x.beginPath(); x.moveTo(px, py); x.lineTo(px + 6 + R()*14, py + (R() - .5)*3); x.stroke(); }
  const id = x.getImageData(0, 0, W, H), a = id.data; for (let i = 0; i < a.length; i += 4){ const n = (R() - .5)*18; a[i] += n; a[i + 1] += n; a[i + 2] += n; } x.putImageData(id, 0, 0);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  return C.bark = t;
}
function needleTexture(THREE){   // atlas: left half = side view of a needle tuft (fan), right half = top view (starburst)
  const C = texCache(THREE); if (C.needle) return C.needle;
  const W = 512, H = 256, [c, x] = canvas(W, H), R = rng(11);
  x.lineCap = 'round';
  const needle = (x0, y0, x1, y1, w) => { const g = 150 + R()*105; x.strokeStyle = `rgb(${g*.86|0},${g|0},${g*.62|0})`; x.lineWidth = w; x.beginPath(); x.moveTo(x0, y0); x.quadraticCurveTo((x0 + x1)/2 + (R() - .5)*10, (y0 + y1)/2, x1, y1); x.stroke(); };
  for (let k = 0; k < 5; k++){   // side: several fascicle fans from a short twig
    const bx = 128 + (R() - .5)*70, by = 236 - R()*60;
    for (let i = 0; i < 46; i++){ const a = -Math.PI/2 + (R() - .5)*2.5, L = 50 + R()*85; needle(bx, by, bx + Math.cos(a)*L, by + Math.sin(a)*L*.95, 2 + R()*1.6); }
  }
  for (let k = 0; k < 7; k++){   // top: starbursts
    const bx = 384 + (R() - .5)*120, by = 128 + (R() - .5)*120;
    for (let i = 0; i < 40; i++){ const a = R()*Math.PI*2, L = 22 + R()*60; needle(bx, by, bx + Math.cos(a)*L, by + Math.sin(a)*L, 2 + R()*1.6); }
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  return C.needle = t;
}
function oakTexture(THREE){   // natural oak, grain along u (1 tile = 1.6 m x 0.4 m)
  const C = texCache(THREE); if (C.oak) return C.oak;
  const W = 1024, H = 256, [c, x] = canvas(W, H), R = rng(19);
  x.fillStyle = 'rgb(176,128,82)'; x.fillRect(0, 0, W, H);
  for (let i = 0; i < 140; i++){ let y = R()*H; const dk = R() < .65; x.strokeStyle = dk ? `rgba(110,72,40,${.12 + R()*.25})` : `rgba(214,170,118,${.15 + R()*.25})`; x.lineWidth = .7 + R()*2.2;
    x.beginPath(); x.moveTo(0, y); for (let s = 0; s <= W; s += 32){ y += (R() - .5)*1.6; x.lineTo(s, y); } x.stroke(); }
  for (let i = 0; i < 60; i++){ x.fillStyle = `rgba(120,80,45,${.2 + R()*.2})`; x.fillRect(R()*W, R()*H, 4 + R()*14, 1); }   // ray flecks
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  return C.oak = t;
}

// ---------------------------------------------------------------- tapered, gnarled tube along a curve
function taperTube(THREE, curve, segs, radial, rFn, vScale = .5){
  const frames = curve.computeFrenetFrames(segs, false), L = curve.getLength();
  const P = [], N = [], U = [], I = [], pt = new THREE.Vector3(), v = new THREE.Vector3();
  for (let i = 0; i <= segs; i++){
    const t = i/segs; curve.getPointAt(t, pt);
    const n = frames.normals[i], b = frames.binormals[i];
    for (let j = 0; j <= radial; j++){
      const th = j/radial*Math.PI*2, r = rFn(t, th);
      v.copy(n).multiplyScalar(Math.cos(th)).addScaledVector(b, Math.sin(th)).normalize();
      P.push(pt.x + v.x*r, pt.y + v.y*r, pt.z + v.z*r); N.push(v.x, v.y, v.z); U.push(j/radial*2, t*L/vScale);
    }
  }
  for (let i = 0; i < segs; i++) for (let j = 0; j < radial; j++){ const a = i*(radial + 1) + j, b = a + radial + 1; I.push(a, b, a + 1, b, b + 1, a + 1); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(N, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(U, 2)); g.setIndex(I);
  g.computeVertexNormals();   // includes the gnarl displacement
  return g;
}

// ---------------------------------------------------------------- the pine
// Tree-local frame: origin = soil surface at the trunk, +Y up, +X = viewer's right in the reference, +Z towards the viewer.
const PADS = [   // [cx, cy, cz, rx, rz, thickness, yaw]   (flat tiered clouds, from the reference silhouette)
  [-1.10, 1.30,  .18, .58, .46, .24,  .3],   // 0 low left (long low arm)
  [ 1.20, 1.52, -.05, .62, .48, .25, -.2],   // 1 low right
  [  .05, 1.80, -.62, .50, .40, .22,  .9],   // 2 rear (depth)
  [ -.72, 2.12, -.12, .58, .46, .24,  .1],   // 3 mid left
  [  .62, 2.28,  .20, .58, .46, .24, -.4],   // 4 mid right
  [ -.02, 2.70,  .02, .70, .52, .24, .25],   // 5 upper (wide)
  [ -.62, 2.55, -.38, .42, .36, .22,  .4],   // 6 upper rear left
  [  .04, 3.12,  .00, .44, .38, .26,  .2],   // 7 apex
];
const TRUNK = [[0, -.10, 0], [.04, .28, .02], [.15, .62, .04], [.16, .90, 0], [.05, 1.18, -.03], [-.06, 1.45, -.02], [-.03, 1.75, .02], [.06, 2.15, 0], [.05, 2.55, -.02], [.02, 3.00, 0]];
const BRANCH_FROM = [.95, 1.12, 1.35, 1.55, 1.75, 2.25, 2.10];   // trunk heights the pad arms leave from (pads 0..6)

function buildPine(THREE, seed = 4242){
  const R = rng(seed), V = (a) => new THREE.Vector3(...a), tree = new THREE.Group(); tree.name = 'courtyard-pine';
  // --- wood
  const woodGeos = [];
  const trunkC = new THREE.CatmullRomCurve3(TRUNK.map(V), false, 'centripetal');
  woodGeos.push(taperTube(THREE, trunkC, 64, 14, (t, th) => {
    const base = lerp(.155, .032, Math.pow(t, .75));
    const flare = t < .1 ? Math.pow(1 - t/.1, 2.2)*(.09 + .07*Math.max(0, Math.cos(5*th + .7))) : 0;   // root flare, 5 lobes
    return base*(1 + .09*Math.sin(3*th + t*19) + .05*Math.sin(5*th - t*31 + 1)) + flare;
  }));
  const trunkAt = y => { let best = 0, bd = 1e9; for (let i = 0; i <= 200; i++){ const p = trunkC.getPointAt(i/200); if (Math.abs(p.y - y) < bd){ bd = Math.abs(p.y - y); best = i/200; } } return trunkC.getPointAt(best); };
  const radAt = y => lerp(.155, .032, Math.pow(clamp((y + .1)/3.1, 0, 1), .75));
  PADS.forEach((pd, k) => {
    const [cx, cy, cz, rx, rz, th] = pd;
    if (k < 7){   // arm from the trunk: drops slightly, then rises into the pad (classic niwaki shape)
      const s = trunkAt(BRANCH_FROM[k]), e = new THREE.Vector3(cx*.92, cy - th*.35, cz*.92), d = e.clone().sub(s);
      const pts = [s, s.clone().add(new THREE.Vector3(d.x*.18, d.y*.05 + .06, d.z*.18)), s.clone().add(new THREE.Vector3(d.x*.45 + (R() - .5)*.08, d.y*.15 - .05, d.z*.45 + (R() - .5)*.08)),
                   s.clone().add(new THREE.Vector3(d.x*.75, d.y*.55 - .02, d.z*.75)), e];
      const c = new THREE.CatmullRomCurve3(pts, false, 'centripetal'), r0 = Math.min(radAt(BRANCH_FROM[k])*.62, .085);
      woodGeos.push(taperTube(THREE, c, 26, 8, (t, a) => lerp(r0, .028, Math.pow(t, .8))*(1 + .08*Math.sin(3*a + t*13))));
    }
    // twigs fanning out under the pad
    const nT = 4 + (R()*2|0), o = new THREE.Vector3(cx*(k < 7 ? .92 : 1), cy - th*.35, cz*(k < 7 ? .92 : 1));
    if (k === 7) o.copy(trunkC.getPointAt(.97));
    for (let i = 0; i < nT; i++){
      const a = i/nT*Math.PI*2 + R()*.8, L = (rx + rz)*.5*(.55 + R()*.3);
      const e = o.clone().add(new THREE.Vector3(Math.cos(a)*L*rx/((rx + rz)/2), th*.15, Math.sin(a)*L*rz/((rx + rz)/2)));
      const m = o.clone().lerp(e, .5).add(new THREE.Vector3(0, -.04, 0));
      woodGeos.push(taperTube(THREE, new THREE.CatmullRomCurve3([o.clone(), m, e]), 8, 5, t => lerp(.03, .008, t)));
    }
  });
  const barkT = barkTexture(THREE);
  const barkM = new THREE.MeshStandardMaterial({color:'#c4b3a2', map:barkT, bumpMap:barkT, bumpScale:2.2, roughness:.92, metalness:0});
  const wood = new THREE.Mesh(mergeGeos(THREE, woodGeos), barkM); wood.castShadow = wood.receiveShadow = true; wood.name = 'pine-wood'; tree.add(wood);

  // --- foliage: needle-tuft cards (3 quads each) clustered into lumpy clumps per pad
  const S = 1, card = [];
  const quad = (pts, uvs) => card.push({pts, uvs});
  quad([[-.5, 0, 0], [.5, 0, 0], [.5, 1, 0], [-.5, 1, 0]], [[0, 0], [.5, 0], [.5, 1], [0, 1]]);
  quad([[0, 0, -.5], [0, 0, .5], [0, 1, .5], [0, 1, -.5]], [[0, 0], [.5, 0], [.5, 1], [0, 1]]);
  quad([[-.55, .55, -.55], [.55, .55, -.55], [.55, .55, .55], [-.55, .55, .55]], [[.5, 0], [1, 0], [1, 1], [.5, 1]]);
  const cp = [], cn = [], cu = [], ci = [];
  card.forEach((q, qi) => { q.pts.forEach((p, i) => { cp.push(p[0]*S, p[1]*S - .25, p[2]*S); const n = new THREE.Vector3(p[0]*.55, .9 + (qi === 2 ? .4 : p[1]*.3), p[2]*.55).normalize(); cn.push(n.x, n.y, n.z); cu.push(...q.uvs[i]); });
    const b = qi*4; ci.push(b, b + 1, b + 2, b, b + 2, b + 3); });
  const cardG = new THREE.BufferGeometry(); cardG.setAttribute('position', new THREE.Float32BufferAttribute(cp, 3)); cardG.setAttribute('normal', new THREE.Float32BufferAttribute(cn, 3)); cardG.setAttribute('uv', new THREE.Float32BufferAttribute(cu, 2)); cardG.setIndex(ci);

  const items = [], core = [];
  const cTop = new THREE.Color('#a39a52'), cMid = new THREE.Color('#5d6234'), cLow = new THREE.Color('#2c321d');
  PADS.forEach(([cx, cy, cz, rx, rz, th, yaw], k) => {
    const ph = [R()*6.28, R()*6.28, R()*6.28], edge = a => 1 + .13*Math.sin(3*a + ph[0]) + .08*Math.sin(5*a + ph[1]) + .05*Math.sin(8*a + ph[2]);
    const cs = Math.cos(yaw), sn = Math.sin(yaw), toW = (x, z) => [cx + x*cs - z*sn, cz + x*sn + z*cs];
    // clumps: one ring at the rim + an inner field
    const clumps = [];
    const nRim = 11 + (R()*3|0);
    for (let i = 0; i < nRim; i++){ const a = i/nRim*Math.PI*2 + R()*.4, e = edge(a)*.78; clumps.push([Math.cos(a)*rx*e, Math.sin(a)*rz*e, .62]); }
    const nIn = 6 + (R()*3|0);
    for (let i = 0; i < nIn; i++){ const a = R()*Math.PI*2, r = Math.sqrt(R())*.45; clumps.push([Math.cos(a)*rx*r, Math.sin(a)*rz*r, 1]); }
    clumps.forEach(([lx, lz, hk]) => {
      const rr = Math.min(1, Math.hypot(lx/rx, lz/rz)), dome = Math.sqrt(Math.max(0, 1 - rr*rr*.8));
      const cr = (.13 + R()*.06)*(rx > .5 ? 1 : .9), cyy = cy + th*(.02 + .2*dome) - .02;
      const [wx, wz] = toW(lx, lz);
      const ccen = new THREE.Vector3(wx, cyy, wz), cry = th*.42*hk + .035;
      core.push([ccen.clone().add(new THREE.Vector3(0, -cry*.25, 0)), cr*.78, cry*.65]);
      const n = 20 + (R()*8|0);
      for (let i = 0; i < n; i++){
        // direction biased up / outward (the underside is mostly flat and gets fewer tufts)
        let u = R()*2 - 1; const a = R()*Math.PI*2; if (u < -.35 && R() < .65) u = -u*.5;
        const s = Math.sqrt(1 - u*u), dir = new THREE.Vector3(Math.cos(a)*s, u, Math.sin(a)*s);
        const rad = .78 + R()*.3, pos = ccen.clone().add(new THREE.Vector3(dir.x*cr*rad, dir.y*cry*rad, dir.z*cr*rad));
        const outward = new THREE.Vector3(pos.x - cx, (pos.y - cy)*2.2 + .12, pos.z - cz).normalize();
        const nrm = dir.clone().multiplyScalar(.6).add(outward.multiplyScalar(.4)).add(new THREE.Vector3(0, .35, 0)).normalize();
        const hFac = clamp((pos.y - (cy - th*.4))/(th*1.05), 0, 1);
        items.push({pos, nrm, s:.12 + R()*.07, h:hFac, j:R()});
      }
    });
  });
  const needleT = needleTexture(THREE);
  const leafM = new THREE.MeshStandardMaterial({map:needleT, alphaTest:.42, side:THREE.DoubleSide, roughness:.88, metalness:0});
  const leaves = new THREE.InstancedMesh(cardG, leafM, items.length); leaves.name = 'pine-needles';
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), q2 = new THREE.Quaternion(), up = new THREE.Vector3(0, 1, 0), sc = new THREE.Vector3(), col = new THREE.Color();
  items.forEach((it, i) => {
    q.setFromUnitVectors(up, it.nrm); q2.setFromAxisAngle(up, it.j*6.283); q.multiply(q2);
    sc.set(it.s, it.s*(.85 + it.j*.3), it.s); m4.compose(it.pos, q, sc); leaves.setMatrixAt(i, m4);
    const h = it.h; if (h > .55) col.copy(cMid).lerp(cTop, (h - .55)/.45); else col.copy(cLow).lerp(cMid, h/.55);
    col.offsetHSL((it.j - .5)*.025, (R() - .5)*.08, (R() - .5)*.06); leaves.setColorAt(i, col);
  });
  leaves.instanceMatrix.needsUpdate = true; leaves.instanceColor.needsUpdate = true;
  leaves.castShadow = true; leaves.receiveShadow = true;
  leaves.customDepthMaterial = new THREE.MeshDepthMaterial({depthPacking:THREE.RGBADepthPacking, map:needleT, alphaTest:.42});
  leaves.computeBoundingSphere?.(); tree.add(leaves);
  // dense dark cores so the clouds read solid (merged, 1 draw call)
  const coreGeos = core.map(([c, r, ry]) => { const g = new THREE.IcosahedronGeometry(1, 1); const p = g.attributes.position;
    for (let i = 0; i < p.count; i++){ const f = 1 + (R() - .5)*.25; p.setXYZ(i, c.x + p.getX(i)*r*f, c.y + p.getY(i)*ry*f, c.z + p.getZ(i)*r*f); } g.computeVertexNormals(); return g; });
  const coreM = new THREE.MeshStandardMaterial({color:'#30361e', roughness:.95});
  const cores = new THREE.Mesh(mergeGeos(THREE, coreGeos), coreM); cores.name = 'pine-pad-cores'; cores.castShadow = true; cores.receiveShadow = true; tree.add(cores);
  tree.userData.stats = {tufts:items.length, clumps:core.length};
  return tree;
}

// ---------------------------------------------------------------- grass tufts + stones
function grassTuftGeometry(THREE, R){
  const geos = [];
  const nB = 16;
  for (let b = 0; b < nB; b++){
    const a = R()*Math.PI*2, lean = .25 + R()*.55, h = .55 + R()*.45, w = .028 + R()*.016, segs = 4, P = [], C = [], I = [], U = [];
    const dx = Math.cos(a), dz = Math.sin(a), px = -dz, pz = dx;
    for (let s = 0; s <= segs; s++){
      const t = s/segs, ww = w*(1 - t*.92), off = lean*t*t*h, y = h*t*(1 - .18*t*lean);
      P.push(dx*off - px*ww, y, dz*off - pz*ww, dx*off + px*ww, y, dz*off + pz*ww);
      const c0 = [lerp(.16, .52, Math.pow(t, 1.4)), lerp(.20, .52, Math.pow(t, 1.4)), lerp(.10, .26, Math.pow(t, 1.4))];
      C.push(...c0, ...c0); U.push(0, t, 1, t);
    }
    for (let s = 0; s < segs; s++){ const k = s*2; I.push(k, k + 1, k + 3, k, k + 3, k + 2); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(P, 3)); g.setAttribute('color', new THREE.Float32BufferAttribute(C, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(U, 2)); g.setIndex(I);
    const N = []; for (let i = 0; i < P.length/3; i++) N.push(dx*.35, .93, dz*.35); g.setAttribute('normal', new THREE.Float32BufferAttribute(N, 3));
    geos.push(g);
  }
  return mergeGeos(THREE, geos);
}

// ---------------------------------------------------------------- courtyard
export function buildCourtyard(THREE, opts = {}){
  const {pond, island} = opts, Y = opts.floorY ?? 0, R = rng(opts.seed ?? 2026);
  if (!pond || !island) throw new Error('buildCourtyard: opts.pond and opts.island rectangles are required');
  const P = {x0:Math.min(pond.x0, pond.x1), x1:Math.max(pond.x0, pond.x1), z0:Math.min(pond.z0, pond.z1), z1:Math.max(pond.z0, pond.z1)};
  const I = {x0:Math.min(island.x0, island.x1), x1:Math.max(island.x0, island.x1), z0:Math.min(island.z0, island.z1), z1:Math.max(island.z0, island.z1)};
  const group = new THREE.Group(); group.name = 'courtyard-feature';
  const disposables = [];
  const mesh = (g, m, name, cast = true, recv = true) => { const o = new THREE.Mesh(g, m); o.name = name; o.castShadow = cast; o.receiveShadow = recv; group.add(o); return o; };

  // materials
  const travT = travertineTexture(THREE, {seed:7}), limeT = limestoneTexture(THREE);
  const travM = new THREE.MeshStandardMaterial({map:travT, roughness:.62, color:'#ffffff'});
  const copingT = travertineTexture(THREE, {seed:9, tone:1, joint:false});
  const copingM = new THREE.MeshStandardMaterial({map:copingT, roughness:.55, color:'#fffaf2'});
  const limeM = new THREE.MeshStandardMaterial({map:limeT, roughness:.8, color:'#efe2cc'});
  const basinM = new THREE.MeshStandardMaterial({map:limeT, roughness:.85, color:'#cfc8ba'});
  disposables.push(travM, copingM, limeM, basinM);

  const W = P.x1 - P.x0, D = P.z1 - P.z0, L = DA.lipW, depth = DA.pondDepth;
  // stone lip (flush with the paving, crisp 6 cm edge into the water)
  const lipH = .065, lipY = Y + .004 - lipH/2;
  [[P.x0 + W/2, P.z0 + L/2, W, L], [P.x0 + W/2, P.z1 - L/2, W, L], [P.x0 + L/2, P.z0 + D/2, L, D - 2*L], [P.x1 - L/2, P.z0 + D/2, L, D - 2*L]]
    .forEach(([x, z, w, d], i) => { const m = mesh(worldBox(THREE, w, lipH, d, .6, .6), limeM, 'pond-lip-' + i, false, true); m.position.set(x, lipY, z); });
  // basin walls + floor
  const iw = W - 2*L, id = D - 2*L, wallH = depth - lipH + .004;
  [[P.x0 + W/2, P.z0 + L + .01, iw, .02], [P.x0 + W/2, P.z1 - L - .01, iw, .02], [P.x0 + L + .01, P.z0 + D/2, .02, id], [P.x1 - L - .01, P.z0 + D/2, .02, id]]
    .forEach(([x, z, w, d], i) => { const m = mesh(worldBox(THREE, w, wallH, d, .6, .6), basinM, 'pond-wall-' + i, false, true); m.position.set(x, Y - depth + wallH/2, z); });
  const fl = mesh(worldBox(THREE, iw, .02, id, .6, .6), basinM, 'pond-floor', false, true); fl.position.set(P.x0 + W/2, Y - depth - .01, P.z0 + D/2);

  // water (Water2) inside the lip, with the island as a hole
  const ws = new THREE.Shape(); const wx0 = P.x0 + L, wx1 = P.x1 - L, wz0 = P.z0 + L, wz1 = P.z1 - L;
  ws.moveTo(wx0, -wz1); ws.lineTo(wx1, -wz1); ws.lineTo(wx1, -wz0); ws.lineTo(wx0, -wz0); ws.lineTo(wx0, -wz1);
  const hole = new THREE.Path(); hole.moveTo(I.x0, -I.z1); hole.lineTo(I.x0, -I.z0); hole.lineTo(I.x1, -I.z0); hole.lineTo(I.x1, -I.z1); hole.lineTo(I.x0, -I.z1); ws.holes.push(hole);
  const wg = new THREE.ShapeGeometry(ws);
  { const uv = wg.attributes.uv, p = wg.attributes.position; for (let i = 0; i < p.count; i++) uv.setXY(i, (p.getX(i) - wx0)/(wx1 - wx0), (p.getY(i) + wz1)/(wz1 - wz0)); }
  let water = null, waterMode = 'water2';
  const tl = new THREE.TextureLoader();
  try {
    if (opts.renderer && opts.renderer.capabilities && !opts.renderer.capabilities.isWebGL2) throw new Error('WebGL2 unavailable');
    const n0 = tl.load(new URL('./vendor/three/examples/textures/water/Water_1_M_Normal.jpg', import.meta.url).href);
    const n1 = tl.load(new URL('./vendor/three/examples/textures/water/Water_2_M_Normal.jpg', import.meta.url).href);
    disposables.push(n0, n1);
    water = new Water(wg, {color:opts.waterColor ?? 0xc4d4d8, scale:opts.waterScale ?? 4.5, flowDirection:new THREE.Vector2(.6, .35), flowSpeed:.006,
      reflectivity:opts.reflectivity ?? .4, shader:calmWaterShader(), textureWidth:opts.waterRes ?? 1024, textureHeight:opts.waterRes ?? 1024, normalMap0:n0, normalMap1:n1});
  } catch(e){ waterMode = 'flat'; console.warn('courtyard: Water2 unavailable, flat water fallback:', e.message); }
  if (!water) water = new THREE.Mesh(wg, new THREE.MeshPhysicalMaterial({color:'#9fb4b8', roughness:.06, metalness:0, transparent:true, opacity:.55, envMapIntensity:1.4}));
  water.rotation.x = -Math.PI/2; water.position.y = Y - DA.waterDrop; water.name = 'pond-water'; water.userData.waterMode = waterMode; group.add(water);

  // island planter: body (inset reveal), coping frame (outer edge = CAD island rect), soil
  const iW = I.x1 - I.x0, iD = I.z1 - I.z0, cx = (I.x0 + I.x1)/2, cz = (I.z0 + I.z1)/2, bi = DA.bodyInset;
  const bodyTop = Y + DA.copingTop - DA.copingT, bodyH = bodyTop - (Y - depth);
  const body = mesh(worldBox(THREE, iW - 2*bi, bodyH, iD - 2*bi, 1.2, .6), travM, 'island-body'); body.position.set(cx, Y - depth + bodyH/2, cz);
  const cw = DA.copingW, ct = DA.copingT, cy = Y + DA.copingTop - ct/2;
  [[cx, I.z0 + cw/2, iW, cw], [cx, I.z1 - cw/2, iW, cw], [I.x0 + cw/2, cz, cw, iD - 2*cw], [I.x1 - cw/2, cz, cw, iD - 2*cw]]
    .forEach(([x, z, w, d], i) => { const m = mesh(worldBox(THREE, w, ct, d, 1.2, .6), copingM, 'island-coping-' + i); m.position.set(x, cy, z); });
  const sW = iW - 2*cw, sD = iD - 2*cw;
  const sg = new THREE.PlaneGeometry(sW, sD, 18, 18); sg.rotateX(-Math.PI/2);
  { const p = sg.attributes.position; for (let i = 0; i < p.count; i++){ const u = p.getX(i)/(sW/2), v = p.getZ(i)/(sD/2), e = Math.max(Math.abs(u), Math.abs(v)); p.setY(i, (1 - e*e)*.035 + (R() - .5)*.008); } sg.computeVertexNormals(); }
  const soilM = new THREE.MeshStandardMaterial({color:'#3b2f24', roughness:1}); disposables.push(soilM);
  const soil = mesh(sg, soilM, 'island-soil', false, true); soil.position.set(cx, Y + DA.soilTop, cz);

  // ornamental grass tufts (instanced, colour varied)
  const tuftG = grassTuftGeometry(THREE, R);
  const grassM = new THREE.MeshStandardMaterial({vertexColors:true, side:THREE.DoubleSide, roughness:.85}); disposables.push(grassM);
  const tufts = [];
  for (let k = 0; k < 2000 && tufts.length < 300; k++){
    const x = (R() - .5)*(sW - .05), z = (R() - .5)*(sD - .05), r = Math.hypot(x, z);
    if (r < .2) continue;
    if (tufts.some(t => Math.hypot(t[0] - x, t[1] - z) < .048)) continue;
    tufts.push([x, z]);
  }
  const grass = new THREE.InstancedMesh(tuftG, grassM, tufts.length); grass.name = 'island-grass';
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), s3 = new THREE.Vector3(), p3 = new THREE.Vector3(), col = new THREE.Color();
  const gA = new THREE.Color('#3f5424'), gB = new THREE.Color('#66703a'), gC = new THREE.Color('#8f8450');
  tufts.forEach(([x, z], i) => {
    const edge = Math.max(Math.abs(x)/(sW/2), Math.abs(z)/(sD/2)), mound = (1 - edge*edge)*.035, hs = .14 + R()*.09 - edge*.03;
    e.set((R() - .5)*.2, R()*6.28, (R() - .5)*.2); q.setFromEuler(e); s3.set(.3 + R()*.12, hs, .3 + R()*.12);
    p3.set(cx + x, Y + DA.soilTop + mound - .01, cz + z); m4.compose(p3, q, s3); grass.setMatrixAt(i, m4);
    col.copy(gA).lerp(gB, R()*.8); if (R() < .18) col.lerp(gC, .5); grass.setColorAt(i, col);
  });
  grass.castShadow = true; grass.receiveShadow = true; group.add(grass);
  // a few stones
  const stoneGeos = [];
  for (let i = 0; i < 7; i++){
    const g = new THREE.DodecahedronGeometry(1, 0), a = R()*6.28, r = .22 + R()*.32, s = .035 + R()*.04, p = g.attributes.position;
    const sx = cx + Math.cos(a)*r*sW/1.25, sz = cz + Math.sin(a)*r*sD/1.25;
    for (let j = 0; j < p.count; j++) p.setXYZ(j, sx + p.getX(j)*s*1.3, Y + DA.soilTop + .02 + p.getY(j)*s*.55, sz + p.getZ(j)*s);
    stoneGeos.push(g);
  }
  stoneGeos.forEach(g => g.computeVertexNormals());
  const stoneM = new THREE.MeshStandardMaterial({color:'#b9b2a6', roughness:.75, flatShading:true}); disposables.push(stoneM);
  mesh(mergeGeos(THREE, stoneGeos), stoneM, 'island-stones');

  // the pine
  const tree = buildPine(THREE, opts.treeSeed ?? 4242);
  tree.position.set(cx, Y + DA.soilTop + .02, cz); tree.rotation.y = opts.treeYaw ?? DA.treeYaw; group.add(tree);

  const update = (dt, t) => {
    const s = .0036*Math.sin(t*.55) + .0012*Math.sin(t*1.7 + .4);
    tree.rotation.z = s; tree.rotation.x = .0025*Math.sin(t*.43 + 1.2);
  };
  const dispose = () => {
    group.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material){ (Array.isArray(o.material) ? o.material : [o.material]).forEach(m => m.dispose()); } });
    disposables.forEach(d => d.dispose && d.dispose());
    if (water && water.material && water.material.uniforms){ ['tReflectionMap', 'tRefractionMap'].forEach(k => water.material.uniforms[k].value?.dispose?.()); }
  };
  group.userData.update = update;
  const meta = {pond:P, island:I, floorY:Y, waterY:Y - DA.waterDrop, waterMode, assumptions:DA, tree:tree.userData.stats, tufts:tufts.length};
  group.userData.meta = meta;
  return {group, update, dispose, meta, tree, water};
}

// ---------------------------------------------------------------- bench (separate; the viewer places it)
export function buildBench(THREE, {length = 1.6, depth = .4, height = .45, plank = .07} = {}){
  const g = new THREE.Group(); g.name = 'courtyard-bench';
  const oakT = oakTexture(THREE);
  const oakM = new THREE.MeshStandardMaterial({map:oakT, color:'#d6c0a2', roughness:.62});
  const top = new THREE.Mesh(worldBox(THREE, length, plank, depth, 1.6, .4), oakM); top.position.y = height - plank/2;
  const legH = height - plank, legW = .30, legD = depth - .06;
  const legs = [-1, 1].map(s => { const m = new THREE.Mesh(worldBox(THREE, legW, legH, legD, 1.6, .4), oakM); m.position.set(s*(length/2 - .22), legH/2, 0); return m; });
  [top, ...legs].forEach(m => { m.castShadow = m.receiveShadow = true; g.add(m); });
  return g;
}
