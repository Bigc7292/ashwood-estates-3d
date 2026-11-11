
function applyGlass(scene, root){
  const panes = [];
  const glass = new THREE.MeshPhysicalMaterial({
    name: 'MAT_glass',
    color: 0x8ea3ab,
    metalness: 0.92,
    roughness: 0.06,
    envMapIntensity: 1.15
  });
  const bal = new THREE.MeshPhysicalMaterial({
    name: 'MAT_balglass',
    color: 0xd5e4e8,
    metalness: 0.05,
    roughness: 0.04,
    transmission: 0.86,
    thickness: 0.04,
    ior: 1.5,
    transparent: true,
    opacity: 0.45,
    depthWrite: false,
    side: THREE.DoubleSide
  });
  root.traverse((o) => {
    if (!o.isMesh || !o.material) return;
    const n = o.material.name;
    if (n === 'MAT_glass'){
      o.material = glass;
      o.castShadow = false;
      panes.push(o);
    } else if (n === 'MAT_balglass'){
      o.material = bal;
      o.castShadow = false;
    } else if (n === 'MAT_bronze'){
      o.material = new THREE.MeshStandardMaterial({
        name: 'MAT_bronze',
        color: 0x4a3424,
        metalness: 0.86,
        roughness: 0.28,
        envMapIntensity: 0.55
      });
      o.castShadow = true;
    }
  });
  const house = new THREE.Vector3(9.2, 4, 14);
  const groups = new Map();
  panes.forEach((o) => {
    o.updateWorldMatrix(true, false);
    if (!o.geometry.boundingBox) o.geometry.computeBoundingBox();
    const b = o.geometry.boundingBox.clone().applyMatrix4(o.matrixWorld);
    const size = new THREE.Vector3(), center = new THREE.Vector3();
    b.getSize(size);
    b.getCenter(center);
    let axis = 0;
    if (size.y <= size.x && size.y <= size.z) axis = 1;
    if (size.z <= size.x && size.z <= size.y) axis = 2;
    if (axis === 1) return;
    const sign = center.getComponent(axis) >= house.getComponent(axis) ? 1 : -1;
    const plane = sign > 0 ? b.max.getComponent(axis) : b.min.getComponent(axis);
    const key = axis + ':' + sign + ':' + Math.round(plane * 5);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push({ o, axis, sign, plane, center, size, name: o.name });
  });
  const mirrors = [];
  let reflecting = false;
  const clipBias = 0.003;
  groups.forEach((items) => {
    const rt = new THREE.WebGLRenderTarget(512, 512);
    const virtualCamera = new THREE.PerspectiveCamera();
    const tint = new THREE.Color(0xc5d5dc);
    const meshes = items.map((info) => {
      const w = info.axis === 0 ? info.size.z : info.size.x;
      const h = info.size.y;
      const mat = new THREE.ShaderMaterial({
        name: 'MAT_window_mirror',
        uniforms: THREE.UniformsUtils.clone(Reflector.ReflectorShader.uniforms),
        vertexShader: Reflector.ReflectorShader.vertexShader,
        fragmentShader: Reflector.ReflectorShader.fragmentShader
      });
      mat.uniforms.color.value = tint;
      mat.uniforms.tDiffuse.value = rt.texture;
      mat.uniforms.textureMatrix.value = new THREE.Matrix4();
      const mesh = new THREE.Mesh(new THREE.PlaneGeometry(Math.max(0.05, w - 0.02), Math.max(0.05, h - 0.02)), mat);
      mesh.position.copy(info.center);
      mesh.position.setComponent(info.axis, info.plane + info.sign * 0.02);
      mesh.rotation.y = info.axis === 2 ? (info.sign > 0 ? 0 : Math.PI) : (info.sign > 0 ? Math.PI / 2 : -Math.PI / 2);
      mesh.name = 'PROC_window_' + info.name;
      mesh.userData.planeAxis = info.axis;
      mesh.userData.planeSign = info.sign;
      info.o.visible = false;
      scene.add(mesh);
      mirrors.push(mesh);
      return mesh;
    });
    const leader = meshes[0];
    const normal = new THREE.Vector3();
    const reflectorWorldPosition = new THREE.Vector3();
    const cameraWorldPosition = new THREE.Vector3();
    const rotationMatrix = new THREE.Matrix4();
    const lookAtPosition = new THREE.Vector3();
    const view = new THREE.Vector3();
    const target = new THREE.Vector3();
    const q = new THREE.Vector4();
    const reflectorPlane = new THREE.Plane();
    const clipPlane = new THREE.Vector4();
    leader.onBeforeRender = function (renderer, scene, camera) {
      if (reflecting) return;
      reflectorWorldPosition.setFromMatrixPosition(leader.matrixWorld);
      cameraWorldPosition.setFromMatrixPosition(camera.matrixWorld);
      rotationMatrix.extractRotation(leader.matrixWorld);
      normal.set(0, 0, 1).applyMatrix4(rotationMatrix);
      view.subVectors(reflectorWorldPosition, cameraWorldPosition);
      if (view.dot(normal) > 0) return;
      view.reflect(normal).negate().add(reflectorWorldPosition);
      rotationMatrix.extractRotation(camera.matrixWorld);
      lookAtPosition.set(0, 0, -1).applyMatrix4(rotationMatrix).add(cameraWorldPosition);
      target.subVectors(reflectorWorldPosition, lookAtPosition);
      target.reflect(normal).negate().add(reflectorWorldPosition);
      virtualCamera.position.copy(view);
      virtualCamera.up.set(0, 1, 0).applyMatrix4(rotationMatrix);
      virtualCamera.up.reflect(normal);
      virtualCamera.lookAt(target);
      virtualCamera.far = camera.far;
      virtualCamera.updateMatrixWorld();
      virtualCamera.projectionMatrix.copy(camera.projectionMatrix);
      meshes.forEach((m) => {
        const tm = m.material.uniforms.textureMatrix.value;
        tm.set(0.5, 0, 0, 0.5, 0, 0.5, 0, 0.5, 0, 0, 0.5, 0.5, 0, 0, 0, 1);
        tm.multiply(virtualCamera.projectionMatrix);
        tm.multiply(virtualCamera.matrixWorldInverse);
        tm.multiply(m.matrixWorld);
      });
      reflectorPlane.setFromNormalAndCoplanarPoint(normal, reflectorWorldPosition);
      reflectorPlane.applyMatrix4(virtualCamera.matrixWorldInverse);
      clipPlane.set(reflectorPlane.normal.x, reflectorPlane.normal.y, reflectorPlane.normal.z, reflectorPlane.constant);
      const pe = virtualCamera.projectionMatrix.elements;
      q.x = (Math.sign(clipPlane.x) + pe[8]) / pe[0];
      q.y = (Math.sign(clipPlane.y) + pe[9]) / pe[5];
      q.z = -1;
      q.w = (1 + pe[10]) / pe[14];
      clipPlane.multiplyScalar(2 / clipPlane.dot(q));
      pe[2] = clipPlane.x;
      pe[6] = clipPlane.y;
      pe[10] = clipPlane.z + 1 - clipBias;
      pe[14] = clipPlane.w;
      reflecting = true;
      mirrors.forEach((m) => { m.visible = false; });
      const prevTarget = renderer.getRenderTarget();
      const prevXr = renderer.xr.enabled;
      const prevShadow = renderer.shadowMap.autoUpdate;
      renderer.xr.enabled = false;
      renderer.shadowMap.autoUpdate = false;
      renderer.setRenderTarget(rt);
      renderer.state.buffers.depth.setMask(true);
      if (renderer.autoClear === false) renderer.clear();
      renderer.render(scene, virtualCamera);
      renderer.xr.enabled = prevXr;
      renderer.shadowMap.autoUpdate = prevShadow;
      renderer.setRenderTarget(prevTarget);
      mirrors.forEach((m) => { m.visible = true; });
      reflecting = false;
    };
  });
}

// garden_three.js: procedural exterior dressing for villa.html, built in three.js only.
// No downloaded models or textures. Concept visualisation, not survey-verified.
// Sizes: tree and hedge positions come from villa-materials.glb node bounds (TREE_*_broadleaf_trunk, HEDGE_*);
// pool bounds from POOL_* nodes; furniture positions follow the terrace layout already in villa.html.
// Tree heights, crown sizes and furniture dimensions are ASSUMPTIONS (typical sizes), not from the plan.
import * as THREE from 'three';
import { mergeGeometries } from './model/vendor/three/examples/jsm/utils/BufferGeometryUtils.js';
import { RoundedBoxGeometry } from './model/vendor/three/examples/jsm/geometries/RoundedBoxGeometry.js';
import { Reflector } from './model/vendor/three/examples/jsm/objects/Reflector.js';

function prng(seed){
  let a = seed >>> 0;
  return () => {
    a |= 0; a = a + 0x6D2B79F5 | 0;
    let t = Math.imul(a ^ a >>> 15, 1 | a);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

// ---------- textures drawn on canvas ----------
function leafTexture(o){
  const S = 128, c = document.createElement('canvas');
  c.width = c.height = S;
  const g = c.getContext('2d'), r = prng(o.seed);
  for (let i = 0; i < o.count; i++){
    const x = 14 + r() * (S - 28), y = 14 + r() * (S - 28);
    const len = o.len * (0.75 + r() * 0.5), wid = len * o.aspect;
    const l = o.l + (r() - 0.5) * o.lv;
    g.save();
    g.translate(x, y);
    g.rotate(r() * Math.PI * 2);
    g.fillStyle = `hsl(${o.h + (r() - 0.5) * o.hv},${o.s}%,${l}%)`;
    g.beginPath();
    g.ellipse(0, 0, len, wid, 0, 0, Math.PI * 2);
    g.fill();
    g.strokeStyle = `hsla(${o.h},${o.s}%,${l + 12}%,0.55)`;
    g.lineWidth = 1;
    g.beginPath(); g.moveTo(-len, 0); g.lineTo(len, 0); g.stroke();
    g.restore();
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 4;
  return t;
}
function barkTexture(){
  const c = document.createElement('canvas');
  c.width = 64; c.height = 128;
  const g = c.getContext('2d'), r = prng(7);
  g.fillStyle = '#6b5a48'; g.fillRect(0, 0, 64, 128);
  for (let i = 0; i < 90; i++){
    g.strokeStyle = `rgba(${40 + r() * 40},${32 + r() * 30},${24 + r() * 24},${0.25 + r() * 0.4})`;
    g.lineWidth = 1 + r() * 2;
    const x = r() * 64;
    g.beginPath(); g.moveTo(x, r() * 128);
    g.bezierCurveTo(x + (r() - 0.5) * 8, r() * 128, x + (r() - 0.5) * 8, r() * 128, x + (r() - 0.5) * 6, r() * 128);
    g.stroke();
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(2, 3);
  return t;
}
function tileTexture(){
  const S = 256, n = 8, c = document.createElement('canvas');
  c.width = c.height = S;
  const g = c.getContext('2d'), r = prng(11), w = S / n;
  g.fillStyle = '#d9ecec'; g.fillRect(0, 0, S, S);
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++){
    g.fillStyle = `hsl(${186 + r() * 10},${38 + r() * 14}%,${64 + r() * 12}%)`;
    g.fillRect(i * w + 1.5, j * w + 1.5, w - 3, w - 3);
  }
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.anisotropy = 4;
  return t;
}
function rippleNormal(){
  const S = 256, c = document.createElement('canvas');
  c.width = c.height = S;
  const g = c.getContext('2d'), img = g.createImageData(S, S), d = img.data;
  const h = (x, y) => {
    const u = x / S * Math.PI * 2, v = y / S * Math.PI * 2;
    return Math.sin(u * 3 + Math.sin(v * 2) * 1.3) * 0.5 + Math.sin(v * 5 + Math.sin(u * 3) * 1.1) * 0.3 + Math.sin((u + v) * 7) * 0.2;
  };
  for (let y = 0; y < S; y++) for (let x = 0; x < S; x++){
    const dx = h(x + 1, y) - h(x - 1, y), dy = h(x, y + 1) - h(x, y - 1);
    const i = (y * S + x) * 4;
    d[i] = 128 + dx * 420; d[i + 1] = 128 + dy * 420; d[i + 2] = 255; d[i + 3] = 255;
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
}

// ---------- leaf card cloud ----------
function CardCloud(){
  this.pos = []; this.nor = []; this.uv = []; this.col = []; this.idx = []; this.n = 0;
}
CardCloud.prototype.add = function(p, size, facing, normal, shade, r){
  // quad centred on p, plane roughly perpendicular to `facing`, randomly spun and tilted
  const f = facing.clone().add(new THREE.Vector3(r() - 0.5, r() - 0.5, r() - 0.5).multiplyScalar(0.9)).normalize();
  const up = Math.abs(f.y) > 0.9 ? new THREE.Vector3(1, 0, 0) : new THREE.Vector3(0, 1, 0);
  const a = new THREE.Vector3().crossVectors(up, f).normalize();
  const b = new THREE.Vector3().crossVectors(f, a);
  const th = r() * Math.PI * 2, cs = Math.cos(th) * size, sn = Math.sin(th) * size;
  const ax = a.clone().multiplyScalar(cs).addScaledVector(b, sn);
  const bx = a.clone().multiplyScalar(-sn).addScaledVector(b, cs);
  const q = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
  const u0 = r() < 0.5 ? 0 : 1;
  for (const [i, j] of q){
    this.pos.push(p.x + ax.x * i + bx.x * j, p.y + ax.y * i + bx.y * j, p.z + ax.z * i + bx.z * j);
    this.nor.push(normal.x, normal.y, normal.z);
    this.uv.push(u0 ? (i + 1) / 2 : (1 - i) / 2, (j + 1) / 2);
    this.col.push(shade, shade, shade);
  }
  const k = this.n * 4;
  this.idx.push(k, k + 1, k + 2, k, k + 2, k + 3);
  this.n++;
};
CardCloud.prototype.geometry = function(){
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(this.pos, 3));
  g.setAttribute('normal', new THREE.Float32BufferAttribute(this.nor, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(this.uv, 2));
  g.setAttribute('color', new THREE.Float32BufferAttribute(this.col, 3));
  g.setIndex(this.idx);
  g.computeBoundingSphere();
  return g;
};

// ---------- trees ----------
function buildTreeGeometry(o){
  const r = prng(o.seed), parts = [], tips = [];
  const Y = new THREE.Vector3(0, 1, 0);
  function limb(start, dir, len, rad, depth){
    const end = start.clone().addScaledVector(dir, len);
    const g = new THREE.CylinderGeometry(rad * o.taper, rad, len, depth === 0 ? 9 : 6, 1, true);
    g.translate(0, len / 2, 0);
    g.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(Y, dir));
    g.translate(start.x, start.y, start.z);
    parts.push(g);
    if (depth >= o.depth){ tips.push(end); return; }
    const kids = depth === 0 ? o.fork : 2 + (r() < 0.35 ? 1 : 0);
    const base = r() * Math.PI * 2;
    for (let i = 0; i < kids; i++){
      const az = base + i / kids * Math.PI * 2 + (r() - 0.5) * 0.7;
      const spread = o.spread * (0.7 + r() * 0.6);
      const d = dir.clone().multiplyScalar(Math.cos(spread))
        .add(new THREE.Vector3(Math.cos(az), 0.15, Math.sin(az)).multiplyScalar(Math.sin(spread)))
        .add(new THREE.Vector3(0, o.lift, 0)).normalize();
      limb(end, d, len * (0.62 + r() * 0.2), rad * o.taper * 0.82, depth + 1);
    }
    if (depth >= 1) tips.push(end);
  }
  const lean = new THREE.Vector3((r() - 0.5) * o.lean, 1, (r() - 0.5) * o.lean).normalize();
  limb(new THREE.Vector3(0, 0, 0), lean, o.trunk, o.radius, 0);
  const wood = mergeGeometries(parts);
  // crown centre for outward-facing normals
  const cc = new THREE.Vector3();
  tips.forEach((t) => cc.add(t));
  cc.multiplyScalar(1 / tips.length);
  const cloud = new CardCloud();
  let top = 0, low = 1e9;
  tips.forEach((t) => { top = Math.max(top, t.y); low = Math.min(low, t.y); });
  tips.forEach((t) => {
    for (let i = 0; i < o.cards; i++){
      const v = new THREE.Vector3(r() - 0.5, r() - 0.5, r() - 0.5);
      if (v.lengthSq() < 1e-4) continue;
      v.normalize().multiplyScalar(o.clump * Math.cbrt(0.25 + r() * 0.75));
      v.y *= o.squash;
      const p = t.clone().add(v);
      const out = p.clone().sub(cc).normalize();
      const n = out.clone().multiplyScalar(0.65).add(new THREE.Vector3(0, 0.55, 0)).normalize();
      const hgt = (p.y - low) / Math.max(0.5, top - low + o.clump);
      const shade = Math.min(1, 0.5 + 0.38 * Math.max(0, hgt) + (r() - 0.5) * 0.22);
      cloud.add(p, o.card * (0.75 + r() * 0.5), out, n, shade, r);
    }
  });
  return { wood, leaves: cloud.geometry() };
}

function buildTrees(scene, spots, sway){
  const bark = new THREE.MeshStandardMaterial({ name:'MAT_bark_proc', map: barkTexture(), roughness: 1 });
  const olive = new THREE.MeshStandardMaterial({
    name:'MAT_leaf_olive', roughness: 0.82, alphaTest: 0.5, side: THREE.DoubleSide, vertexColors: true,
    map: leafTexture({ seed: 21, count: 26, len: 13, aspect: 0.26, h: 92, hv: 16, s: 30, l: 34, lv: 14 })
  });
  const broad = new THREE.MeshStandardMaterial({
    name:'MAT_leaf_broad', roughness: 0.7, alphaTest: 0.5, side: THREE.DoubleSide, vertexColors: true,
    map: leafTexture({ seed: 22, count: 20, len: 15, aspect: 0.5, h: 112, hv: 14, s: 46, l: 30, lv: 14 })
  });
  // Two shapes, a few seeds each, so a row never reads as one cloned model.
  const kinds = [];
  [31, 32, 33].forEach((seed) => kinds.push({ mat: olive, g: buildTreeGeometry({
    seed, trunk: 2.1, radius: 0.19, taper: 0.72, depth: 3, fork: 3, spread: 0.72, lift: 0.18, lean: 0.35,
    cards: 46, clump: 0.95, squash: 0.7, card: 0.3 }) }));
  [41, 42].forEach((seed) => kinds.push({ mat: broad, g: buildTreeGeometry({
    seed, trunk: 2.5, radius: 0.15, taper: 0.76, depth: 3, fork: 3, spread: 0.42, lift: 0.42, lean: 0.12,
    cards: 52, clump: 0.85, squash: 0.95, card: 0.27 }) }));
  const order = [0, 3, 1, 4, 2, 3, 0, 4];
  spots.forEach((p, i) => {
    const k = kinds[order[i % order.length]];
    const tree = new THREE.Group();
    tree.name = 'PROC_tree_' + i;
    const leaves = new THREE.Mesh(k.g.leaves, k.mat);
    leaves.name = 'PROC_tree_leaves_' + i;
    tree.add(new THREE.Mesh(k.g.wood, bark), leaves);
    tree.position.set(p[0], 0, p[1]);
    tree.rotation.y = i * 1.7;
    tree.scale.setScalar(0.92 + (i * 37 % 10) / 55);
    scene.add(tree);
    sway.push({ o: leaves, p: i * 1.3, a: 0.01, s: 0.5 + (i % 3) * 0.12 });
  });
}

// ---------- hedges ----------
function buildHedges(scene, rows){
  const r = prng(77);
  const leaf = new THREE.MeshStandardMaterial({
    name:'MAT_hedge_leaf', roughness: 0.85, alphaTest: 0.5, side: THREE.DoubleSide, vertexColors: true,
    map: leafTexture({ seed: 23, count: 34, len: 9, aspect: 0.55, h: 108, hv: 14, s: 42, l: 27, lv: 12 })
  });
  const core = new THREE.MeshStandardMaterial({ name:'MAT_hedge_core', color: 0x1c2a14, roughness: 1 });
  const cloud = new CardCloud(), cores = [];
  rows.forEach((b) => {
    const x0 = b.min[0], x1 = b.max[0], z0 = b.min[2], z1 = b.max[2];
    const y0 = 0, y1 = Math.max(b.max[1], 0.7);
    const dx = x1 - x0, dz = z1 - z0, dy = y1 - y0;
    if (dx < 0.2 || dz < 0.2) return;
    const g = new THREE.BoxGeometry(Math.max(0.1, dx - 0.16), dy - 0.08, Math.max(0.1, dz - 0.16));
    g.translate((x0 + x1) / 2, y0 + (dy - 0.08) / 2, (z0 + z1) / 2);
    cores.push(g);
    const faces = [
      { n: [0, 1, 0], a: dx * dz, at: (u, v) => [x0 + u * dx, y1, z0 + v * dz] },
      { n: [1, 0, 0], a: dy * dz, at: (u, v) => [x1, y0 + u * dy, z0 + v * dz] },
      { n: [-1, 0, 0], a: dy * dz, at: (u, v) => [x0, y0 + u * dy, z0 + v * dz] },
      { n: [0, 0, 1], a: dy * dx, at: (u, v) => [x0 + v * dx, y0 + u * dy, z1] },
      { n: [0, 0, -1], a: dy * dx, at: (u, v) => [x0 + v * dx, y0 + u * dy, z0] }
    ];
    faces.forEach((f) => {
      const n = new THREE.Vector3(f.n[0], f.n[1], f.n[2]);
      const count = Math.round(f.a * 70);
      for (let i = 0; i < count; i++){
        const u = r(), v = r(), q = f.at(u, v);
        // soften the top edges so the block reads as clipped foliage, not a box
        const edge = f.n[1] === 1 ? Math.min(u, 1 - u, v, 1 - v) : 1;
        const p = new THREE.Vector3(q[0], q[1] - (f.n[1] === 1 && edge < 0.12 ? (0.12 - edge) * 0.5 : 0), q[2])
          .addScaledVector(n, (r() - 0.45) * 0.09);
        const hgt = (p.y - y0) / dy;
        const shade = Math.min(1, (f.n[1] === 1 ? 0.8 : 0.48 + 0.3 * hgt) + (r() - 0.5) * 0.25);
        const nn = n.clone().multiplyScalar(0.7).add(new THREE.Vector3(0, 0.5, 0)).normalize();
        cloud.add(p, 0.11 + r() * 0.07, n, nn, shade, r);
      }
    });
  });
  if (!cores.length) return;
  const cm = new THREE.Mesh(mergeGeometries(cores), core); cm.name = 'PROC_hedge_core';
  const lm = new THREE.Mesh(cloud.geometry(), leaf); lm.name = 'PROC_hedge_leaves';
  scene.add(cm, lm);
}

// The two balcony plantings were solid dark-green boxes. Replace each with a stone trough and a leaf column.
function buildColumns(scene, cols, sway){
  if (!cols || !cols.length) return;
  const r = prng(64);
  const leaf = new THREE.MeshStandardMaterial({
    name: 'MAT_column_leaf', roughness: 0.78, alphaTest: 0.42, side: THREE.DoubleSide, vertexColors: true,
    map: leafTexture({ seed: 64, count: 28, len: 16, aspect: 0.32, h: 118, hv: 12, s: 48, l: 32, lv: 12 })
  });
  const potMat = new THREE.MeshStandardMaterial({ name: 'MAT_planter', color: 0xc4b49a, roughness: 0.72 });
  const soil = new THREE.MeshStandardMaterial({ name: 'MAT_planter_soil', color: 0x3a3228, roughness: 1 });
  const cloud = new CardCloud();
  const pots = [];
  cols.forEach((b, i) => {
    const x0 = b.min[0], x1 = b.max[0], z0 = b.min[2], z1 = b.max[2];
    const y0 = b.min[1], y1 = b.max[1];
    const cx = (x0 + x1) / 2, cz = (z0 + z1) / 2;
    const dx = x1 - x0, dz = z1 - z0;
    const potH = 0.52;
    const pot = new THREE.BoxGeometry(dx + 0.08, potH, dz + 0.08);
    pot.translate(cx, y0 + potH / 2, cz);
    pots.push(pot);
    const dirt = new THREE.BoxGeometry(dx - 0.06, 0.04, dz - 0.04);
    dirt.translate(cx, y0 + potH - 0.02, cz);
    pots.push(dirt);
    const leafY0 = y0 + potH - 0.05;
    const leafY1 = y1 + 0.08;
    const dy = leafY1 - leafY0;
    const faces = [
      { n: [1, 0, 0], a: dy * dz, at: (u, v) => [x1, leafY0 + u * dy, z0 + v * dz] },
      { n: [-1, 0, 0], a: dy * dz, at: (u, v) => [x0, leafY0 + u * dy, z0 + v * dz] },
      { n: [0, 0, 1], a: dy * dx, at: (u, v) => [x0 + v * dx, leafY0 + u * dy, z1] },
      { n: [0, 0, -1], a: dy * dx, at: (u, v) => [x0 + v * dx, leafY0 + u * dy, z0] },
      { n: [0, 1, 0], a: dx * dz, at: (u, v) => [x0 + u * dx, leafY1, z0 + v * dz] }
    ];
    faces.forEach((f) => {
      const n = new THREE.Vector3(f.n[0], f.n[1], f.n[2]);
      const count = Math.round(f.a * 90);
      for (let k = 0; k < count; k++){
        const u = r(), v = r();
        const q = f.at(u, v);
        const p = new THREE.Vector3(q[0], q[1], q[2]).addScaledVector(n, (r() - 0.35) * 0.12);
        const hgt = (p.y - leafY0) / dy;
        // round the top so it is a shrub column, not a cut box
        if (f.n[1] === 1){
          const edge = Math.min(u, 1 - u, v, 1 - v);
          if (edge < 0.22) p.y -= (0.22 - edge) * 1.1;
        }
        const shade = Math.min(1, 0.42 + hgt * 0.45 + (r() - 0.5) * 0.22);
        const nn = n.clone().multiplyScalar(0.65).add(new THREE.Vector3(0, 0.55, 0)).normalize();
        cloud.add(p, 0.16 + r() * 0.08, n, nn, shade, r);
      }
    });
    void i;
  });
  const leaves = new THREE.Mesh(cloud.geometry(), leaf);
  leaves.name = 'PROC_column_leaves';
  const potMesh = new THREE.Mesh(mergeGeometries(pots.filter((_, idx) => idx % 2 === 0)), potMat);
  potMesh.name = 'PROC_column_planter';
  const soilMesh = new THREE.Mesh(mergeGeometries(pots.filter((_, idx) => idx % 2 === 1)), soil);
  soilMesh.name = 'PROC_column_soil';
  scene.add(potMesh, soilMesh, leaves);
  sway.push({ o: leaves, p: 0.4, a: 0.012, s: 0.45 });
}

// ---------- pool ----------
function buildPool(scene, root, renderer){
  const parts = {};
  root.traverse((o) => { if (o.isMesh && o.name.indexOf('POOL_') === 0) parts[o.name] = o; });
  const key = (s) => Object.keys(parts).find((k) => k.indexOf(s) === 0);
  const waterOld = parts[key('POOL_water')], floorOld = parts[key('POOL_floor')];
  if (!waterOld || !floorOld) return null;
  root.updateMatrixWorld(true);
  const wb = new THREE.Box3().setFromObject(waterOld), fb = new THREE.Box3().setFromObject(floorOld);
  const x0 = wb.min.x, x1 = wb.max.x, z0 = wb.min.z, z1 = wb.max.z, yw = wb.max.y, yf = fb.max.y;
  const dx = x1 - x0, dz = z1 - z0, depth = yw - yf;
  waterOld.visible = false;
  // The pool was moved to where the lawn plane lies, so anything that crosses the basin is cut out there.
  if (renderer){
    renderer.localClippingEnabled = true;
    const cut = [
      new THREE.Plane(new THREE.Vector3(-1, 0, 0), x0), new THREE.Plane(new THREE.Vector3(1, 0, 0), -x1),
      new THREE.Plane(new THREE.Vector3(0, 0, -1), z0), new THREE.Plane(new THREE.Vector3(0, 0, 1), -z1)
    ];
    const hole = new THREE.Box3(new THREE.Vector3(x0 + 0.05, yf + 0.05, z0 + 0.05), new THREE.Vector3(x1 - 0.05, yw - 0.02, z1 - 0.05));
    root.traverse((o) => {
      if (!o.isMesh || !o.visible || o.name.indexOf('POOL_') === 0) return;
      if (!new THREE.Box3().setFromObject(o).intersectsBox(hole)) return;
      o.material = o.material.clone();
      o.material.clippingPlanes = cut;
      o.material.clipIntersection = true;
    });
  }
  const tile = tileTexture();
  const caustic = { value: 0 };
  const liner = (w, h) => {
    const t = tile.clone(); t.needsUpdate = true; t.repeat.set(w / 0.8, h / 0.8);
    const m = new THREE.MeshStandardMaterial({ name:'MAT_pool_tile', map: t, roughness: 0.28, color: 0xf7fffb });
    m.onBeforeCompile = (shader) => {
      shader.uniforms.uTime = caustic;
      shader.fragmentShader = shader.fragmentShader
        .replace('#include <common>', '#include <common>\nuniform float uTime;')
        .replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
        float c1 = sin(vMapUv.x * 16.0 + uTime * 1.3) * sin(vMapUv.y * 13.0 - uTime);
        float c2 = sin((vMapUv.x + vMapUv.y) * 21.0 - uTime * 0.7);
        float cau = smoothstep(0.45, 1.0, c1 * 0.5 + c2 * 0.5 + 0.55);
        totalEmissiveRadiance += vec3(0.25, 0.75, 0.82) * cau * 0.28;`);
    };
    return m;
  };
  const add = (geo, mat, x, y, z, rx, ry, name) => {
    const m = new THREE.Mesh(geo, mat);
    m.position.set(x, y, z); m.rotation.set(rx, ry, 0); m.name = name;
    scene.add(m); return m;
  };
  const e = 0.04, top = 0.06; // liner sits just inside the model's basin walls; tiles run to the coping
  add(new THREE.PlaneGeometry(dx, dz), liner(dx, dz), (x0 + x1) / 2, yf + 0.01, (z0 + z1) / 2, -Math.PI / 2, 0, 'PROC_pool_floor');
  const hh = depth + top;
  add(new THREE.PlaneGeometry(dx, hh), liner(dx, hh), (x0 + x1) / 2, yf + hh / 2, z0 + e, 0, 0, 'PROC_pool_wall_n');
  add(new THREE.PlaneGeometry(dx, hh), liner(dx, hh), (x0 + x1) / 2, yf + hh / 2, z1 - e, 0, Math.PI, 'PROC_pool_wall_s');
  add(new THREE.PlaneGeometry(dz, hh), liner(dz, hh), x0 + e, yf + hh / 2, (z0 + z1) / 2, 0, Math.PI / 2, 'PROC_pool_wall_w');
  add(new THREE.PlaneGeometry(dz, hh), liner(dz, hh), x1 - e, yf + hh / 2, (z0 + z1) / 2, 0, -Math.PI / 2, 'PROC_pool_wall_e');
  // entry steps at the terrace end (assumption: three treads, not on the CAD sheet)
  const stepMat = liner(1.6, 0.6);
  for (let i = 0; i < 3; i++){
    const h = depth * (0.72 - i * 0.24), w = 1.6, d = 0.34;
    add(new THREE.BoxGeometry(w, h, d), stepMat, x1 - e - w / 2, yf + h / 2, z1 - e - d / 2 - i * d, 0, 0, 'PROC_pool_step_' + i);
  }
  Object.keys(parts).forEach((k) => {
    if (k.indexOf('POOL_coping') === 0){
      parts[k].material = new THREE.MeshStandardMaterial({ name:'MAT_pool_coping', color: 0xe8e0d0, roughness: 0.55 });
    }
  });
  const nm = rippleNormal(); nm.repeat.set(dx / 2.4, dz / 2.4);
  const nm2 = nm.clone(); nm2.needsUpdate = true; nm2.repeat.set(dx / 1.3, dz / 1.3);
  const water = new THREE.MeshPhysicalMaterial({
    name:'MAT_pool_water', color: 0x0c7490, roughness: 0.03, metalness: 0,
    transmission: 0.9, thickness: 1.2, ior: 1.333,
    attenuationColor: new THREE.Color(0x085e6c), attenuationDistance: 1.6,
    transparent: true, opacity: 0.82,
    normalMap: nm, normalScale: new THREE.Vector2(0.55, 0.55),
    clearcoat: 1, clearcoatRoughness: 0.015,
    clearcoatNormalMap: nm2, clearcoatNormalScale: new THREE.Vector2(0.32, 0.32),
    envMapIntensity: 1.8, depthWrite: false
  });
  const wm = add(new THREE.PlaneGeometry(dx - 0.02, dz - 0.02), water, (x0 + x1) / 2, yw, (z0 + z1) / 2, -Math.PI / 2, 0, 'PROC_pool_water');
  wm.renderOrder = 2;
  return (t) => { nm.offset.set(t * 0.018, t * 0.011); nm2.offset.set(-t * 0.013, t * 0.02); caustic.value = t; };
}

// ---------- terrace furniture ----------
function buildFurniture(scene){
  const teak = new THREE.MeshStandardMaterial({ name:'MAT_teak', color: 0x9b6d43, roughness: 0.62 });
  const fabric = new THREE.MeshStandardMaterial({ name:'MAT_outdoor_fabric', color: 0xece5d8, roughness: 0.95 });
  const accent = new THREE.MeshStandardMaterial({ name:'MAT_outdoor_accent', color: 0x8a9a8c, roughness: 0.95 });
  const metal = new THREE.MeshStandardMaterial({ name:'MAT_dark_metal', color: 0x2b2927, roughness: 0.45, metalness: 0.6 });
  const stone = new THREE.MeshStandardMaterial({ name:'MAT_table_stone', color: 0xd9d2c4, roughness: 0.4 });
  const Y0 = 0.07; // terrace slab top in villa.html
  const box = (g, w, h, d, x, y, z, mat, rad, rx) => {
    const geo = rad ? new RoundedBoxGeometry(w, h, d, 3, Math.min(rad, w / 2.01, h / 2.01, d / 2.01)) : new THREE.BoxGeometry(w, h, d);
    const m = new THREE.Mesh(geo, mat);
    m.position.set(x, y, z);
    if (rx) m.rotation.x = rx;
    g.add(m); return m;
  };
  // seat faces local -Z; back is on +Z
  function seat(W, D, n){
    const g = new THREE.Group();
    const leg = 0.16, fr = 0.1, sy = leg + fr;
    [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(([i, j]) => box(g, 0.07, leg, 0.07, i * (W / 2 - 0.06), leg / 2, j * (D / 2 - 0.06), teak));
    box(g, W, fr, D, 0, leg + fr / 2, 0, teak, 0.02);
    box(g, 0.1, 0.34, D, -(W / 2 - 0.05), sy + 0.17, 0, teak, 0.02);
    box(g, 0.1, 0.34, D, (W / 2 - 0.05), sy + 0.17, 0, teak, 0.02);
    box(g, W, 0.44, 0.08, 0, sy + 0.22, D / 2 - 0.04, teak, 0.02);
    for (let i = 0; i < 5; i++) box(g, W - 0.24, 0.02, 0.03, 0, sy + 0.06 + i * 0.08, D / 2 + 0.005, teak);
    const cw = (W - 0.22) / n;
    for (let i = 0; i < n; i++){
      const x = -(W - 0.22) / 2 + cw * (i + 0.5);
      box(g, cw - 0.02, 0.17, D - 0.2, x, sy + 0.085, -0.05, fabric, 0.05);
      box(g, cw - 0.03, 0.4, 0.17, x, sy + 0.17 + 0.19, D / 2 - 0.19, fabric, 0.07, -0.2);
    }
    box(g, 0.4, 0.38, 0.13, -(W - 0.22) / 2 + 0.26, sy + 0.17 + 0.18, D / 2 - 0.36, accent, 0.06, -0.38);
    return g;
  }
  function lounger(){
    const g = new THREE.Group(), L = 1.95, W = 0.72, fy = 0.27, hinge = 0.28;
    [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(([i, j]) => box(g, 0.05, fy, 0.05, i * (W / 2 - 0.03), fy / 2, j * (L / 2 - 0.12), teak));
    box(g, 0.05, 0.06, L, -(W / 2 - 0.03), fy, 0, teak, 0.01);
    box(g, 0.05, 0.06, L, (W / 2 - 0.03), fy, 0, teak, 0.01);
    for (let z = -L / 2 + 0.06; z < hinge; z += 0.1) box(g, W - 0.1, 0.02, 0.065, 0, fy + 0.03, z, teak);
    const flat = hinge + L / 2 - 0.03;
    box(g, W - 0.08, 0.09, flat, 0, fy + 0.085, -L / 2 + 0.03 + flat / 2, fabric, 0.04);
    const back = new THREE.Group();
    back.position.set(0, fy + 0.03, hinge);
    back.rotation.x = -0.6;
    const bl = L / 2 - hinge;
    for (let z = 0.05; z < bl; z += 0.1) box(back, W - 0.1, 0.02, 0.065, 0, 0, z, teak);
    box(back, 0.05, 0.05, bl, -(W / 2 - 0.03), -0.03, bl / 2, teak);
    box(back, 0.05, 0.05, bl, (W / 2 - 0.03), -0.03, bl / 2, teak);
    box(back, W - 0.08, 0.09, bl - 0.02, 0, 0.055, bl / 2, fabric, 0.04);
    box(back, W - 0.2, 0.1, 0.22, 0, 0.14, bl - 0.16, accent, 0.045);
    g.add(back);
    box(g, 0.05, 0.3, 0.05, 0, fy + 0.15, L / 2 - 0.16, teak);
    return g;
  }
  const put = (g, x, z, ry, name) => { g.position.set(x, Y0, z); g.rotation.y = ry; g.name = name; scene.add(g); };
  put(seat(2.6, 0.92, 3), 5.8, 3.5, 0, 'PROC_sofa');
  put(seat(0.9, 0.86, 1), 3.9, 2.27, -Math.PI / 2, 'PROC_armchair_w');
  put(seat(0.9, 0.86, 1), 7.7, 2.27, Math.PI / 2, 'PROC_armchair_e');
  const table = new THREE.Group();
  box(table, 1.3, 0.05, 0.65, 0, 0.36, 0, stone, 0.02);
  box(table, 1.2, 0.03, 0.55, 0, 0.14, 0, teak, 0.01);
  [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(([i, j]) => box(table, 0.04, 0.34, 0.04, i * 0.58, 0.17, j * 0.27, metal));
  const bowl = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.1, 0.07, 20), accent);
  bowl.position.set(0.25, 0.42, 0.05); table.add(bowl);
  put(table, 5.82, 2.22, 0, 'PROC_coffee_table');
  put(lounger(), 10.67, 1.2, 0, 'PROC_lounger_1');
  put(lounger(), 11.63, 1.2, 0, 'PROC_lounger_2');
  const side = new THREE.Group();
  const topM = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.03, 24), stone); topM.position.y = 0.42;
  const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.42, 10), metal); stem.position.y = 0.21;
  const foot = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.02, 24), metal); foot.position.y = 0.01;
  side.add(topM, stem, foot);
  put(side, 11.15, 2.45, 0, 'PROC_side_table');
  // parasol (assumption: not on the plan; shades the loungers)
  const par = new THREE.Group();
  const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 2.5, 10), metal); pole.position.y = 1.25;
  const base = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.3, 0.07, 24), metal); base.position.y = 0.035;
  const shade = new THREE.Mesh(new THREE.ConeGeometry(1.45, 0.42, 8, 1, true),
    new THREE.MeshStandardMaterial({ name:'MAT_parasol', color: 0xf1ebdf, roughness: 0.9, side: THREE.DoubleSide }));
  shade.position.y = 2.38; shade.rotation.y = Math.PI / 8;
  par.add(pole, base, shade);
  put(par, 12.45, 2.6, 0, 'PROC_parasol');
}

// spots: [[x, z]...] trunk positions; rows: [{min:[x,y,z], max:[x,y,z]}...] hedge boxes; root: loaded villa scene

function stoneMaterial(photo){
  const mat = new THREE.MeshStandardMaterial({
    name: 'MAT_stone',
    map: photo,
    color: 0xffffff,
    roughness: 0.78,
    metalness: 0
  });
  mat.customProgramCacheKey = () => 'ashwood-stone-triplanar-1';
  mat.onBeforeCompile = (shader) => {
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', '#include <common>\nvarying vec3 vWallWorld;\nvarying vec3 vWallN;')
      .replace('#include <project_vertex>', '#include <project_vertex>\n\tvWallWorld = (modelMatrix * vec4(transformed, 1.0)).xyz;\n\tvWallN = normalize(mat3(modelMatrix) * normal);');
    shader.fragmentShader = shader.fragmentShader
      .replace('#include <common>', '#include <common>\nvarying vec3 vWallWorld;\nvarying vec3 vWallN;')
      .replace('#include <map_fragment>', `#ifdef USE_MAP
        vec3 bn = abs(normalize(vWallN));
        bn /= max(bn.x + bn.y + bn.z, 0.001);
        float sc = 0.72;
        vec3 cx = texture2D(map, vWallWorld.zy * sc).rgb;
        vec3 cy = texture2D(map, vWallWorld.xz * sc).rgb;
        vec3 cz = texture2D(map, vWallWorld.xy * sc).rgb;
        vec3 stone = cx * bn.x + cy * bn.y + cz * bn.z;
        float foot = smoothstep(0.02, 1.45, vWallWorld.y);
        stone = mix(stone * vec3(0.58, 0.54, 0.46), stone, foot);
        float course = smoothstep(0.35, 0.85, fract(vWallWorld.y * 1.35));
        stone *= 0.92 + course * 0.08;
        diffuseColor *= vec4(stone, 1.0);
      #endif`);
  };
  return mat;
}

function applyWalls(root, photo){
  if (!photo) return;
  photo.wrapS = photo.wrapT = THREE.RepeatWrapping;
  photo.colorSpace = THREE.SRGBColorSpace;
  photo.anisotropy = 8;
  photo.needsUpdate = true;
  root.traverse((o) => {
    if (!o.isMesh || !o.material) return;
    const n = o.material.name;
    if (n !== 'MAT_stone' && n !== 'MAT_stone_rf' && n !== 'MAT_soffit') return;
    const mat = stoneMaterial(photo);
    mat.name = n;
    o.material = mat;
    o.castShadow = true;
    o.receiveShadow = true;
  });
}

function grassNormal(){
  const S = 256, h = new Float32Array(S * S);
  const r = prng(9);
  h.fill(0.45);
  for (let i = 0; i < 2200; i++){
    const x = r() * S, y = r() * S, len = 5 + r() * 16, ang = r() * Math.PI * 2;
    const dx = Math.cos(ang), dy = Math.sin(ang);
    for (let t = 0; t < len; t++){
      const px = (Math.floor(x + dx * t) + S) % S;
      const py = (Math.floor(y + dy * t) + S) % S;
      h[py * S + px] = Math.min(1, h[py * S + px] + 0.42 * (1 - t / len));
    }
  }
  const c = document.createElement('canvas');
  c.width = c.height = S;
  const g = c.getContext('2d'), img = g.createImageData(S, S), d = img.data;
  for (let y = 0; y < S; y++) for (let x = 0; x < S; x++){
    const xm = h[y * S + (x + S - 1) % S], xp = h[y * S + (x + 1) % S];
    const ym = h[((y + S - 1) % S) * S + x], yp = h[((y + 1) % S) * S + x];
    let nx = xm - xp, ny = ym - yp, nz = 0.42;
    const L = Math.hypot(nx, ny, nz) || 1;
    const i = (y * S + x) * 4;
    d[i] = (nx / L * 0.5 + 0.5) * 255;
    d[i + 1] = (ny / L * 0.5 + 0.5) * 255;
    d[i + 2] = (nz / L * 0.5 + 0.5) * 255;
    d[i + 3] = 255;
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
}

function lawnMaterial(photo, normalMap){
  const mat = new THREE.MeshStandardMaterial({
    name: 'MAT_lawn',
    map: photo,
    normalMap,
    normalScale: new THREE.Vector2(1.8, 1.8),
    color: 0xffffff,
    roughness: 0.92,
    metalness: 0
  });
  mat.customProgramCacheKey = () => 'ashwood-rear-grass-2';
  mat.onBeforeCompile = (shader) => {
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', '#include <common>\nvarying vec3 vGrassWorld;')
      .replace('#include <project_vertex>', '#include <project_vertex>\n\tvGrassWorld = (modelMatrix * vec4(transformed, 1.0)).xyz;');
    shader.fragmentShader = shader.fragmentShader
      .replace('#include <common>', '#include <common>\nvarying vec3 vGrassWorld;')
      .replace('#include <color_fragment>', `#include <color_fragment>
        #ifdef USE_MAP
          vec3 fine = texture2D(map, vMapUv * 2.6 + vec2(0.17, 0.41)).rgb;
          diffuseColor.rgb = mix(diffuseColor.rgb, diffuseColor.rgb * fine * 1.45, 0.55);
        #endif
        diffuseColor.rgb = pow(max(diffuseColor.rgb, 0.0), vec3(1.28));
        float byHouse = smoothstep(-4.2, 0.45, vGrassWorld.z);
        vec3 sunlit = vec3(0.78, 0.90, 0.58);
        vec3 shaded = vec3(0.34, 0.44, 0.30);
        diffuseColor.rgb *= mix(sunlit, shaded, byHouse);
        float patch = fract(sin(dot(floor(vGrassWorld.xz * 0.42), vec2(12.98, 78.23))) * 43758.5);
        diffuseColor.rgb *= 0.88 + patch * 0.20;`);
  };
  return mat;
}

function applyLawn(root, photo){
  if (photo){
    photo.wrapS = photo.wrapT = THREE.RepeatWrapping;
    photo.colorSpace = THREE.SRGBColorSpace;
    photo.anisotropy = 8;
    photo.repeat.set(1, 1);
    photo.needsUpdate = true;
  }
  const normalMap = grassNormal();
  const base = lawnMaterial(photo, normalMap);
  root.traverse((o) => {
    if (!o.isMesh || !o.material) return;
    const n = o.material.name;
    if (n !== 'MAT_lawn' && n !== 'MAT_context_lawn') return;
    o.updateWorldMatrix(true, false);
    const geo = o.geometry.clone();
    const pos = geo.attributes.position;
    const uv = new Float32Array(pos.count * 2);
    const v = new THREE.Vector3();
    for (let i = 0; i < pos.count; i++){
      v.fromBufferAttribute(pos, i).applyMatrix4(o.matrixWorld);
      uv[i * 2] = v.x * 1.25;
      uv[i * 2 + 1] = v.z * 1.25;
    }
    geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
    o.geometry = geo;
    const mat = base.clone();
    mat.name = n;
    o.material = mat;
    o.castShadow = false;
    o.receiveShadow = true;
  });
}

function buildPalms(scene, spots, sway){
  const bark = new THREE.MeshStandardMaterial({ name: 'MAT_palm_bark', color: 0x6d5642, roughness: 1 });
  const frond = new THREE.MeshStandardMaterial({
    name: 'MAT_palm_frond', roughness: 0.72, alphaTest: 0.45, side: THREE.DoubleSide, vertexColors: true,
    map: leafTexture({ seed: 51, count: 6, len: 34, aspect: 0.16, h: 112, hv: 8, s: 42, l: 26, lv: 8 })
  });
  spots.forEach((p, i) => {
    const r = prng(80 + i);
    const h = Math.max(3.2, p[3] || 5.5);
    const g = new THREE.Group();
    g.name = 'PROC_palm_' + i;
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.16, h, 8, 5), bark);
    trunk.position.y = h / 2;
    trunk.rotation.z = (r() - 0.5) * 0.06;
    trunk.rotation.x = (r() - 0.5) * 0.04;
    g.add(trunk);
    const crown = new CardCloud();
    const nFronds = 16;
    for (let f = 0; f < nFronds; f++){
      const az = (f / nFronds) * Math.PI * 2 + r() * 0.15;
      const dir = new THREE.Vector3(Math.cos(az), 0.15, Math.sin(az)).normalize();
      const len = 2.1 + r() * 0.7;
      for (let s = 0; s < 6; s++){
        const t = 0.22 + (s / 6) * 0.78;
        const pos = dir.clone().multiplyScalar(len * t);
        pos.y += h - t * t * 1.15;
        const out = dir.clone();
        crown.add(pos, 0.42 * (1.15 - t * 0.35), out, new THREE.Vector3(0, 1, 0), 0.5 + (1 - t) * 0.4, r);
      }
    }
    const leaves = new THREE.Mesh(crown.geometry(), frond);
    leaves.name = 'PROC_palm_fronds_' + i;
    g.add(leaves);
    g.position.set(p[0], p[1], p[2]);
    scene.add(g);
    sway.push({ o: leaves, p: i * 0.8, a: 0.015, s: 0.4 });
  });
}

function buildPine(scene, spot, sway){
  if (!spot) return;
  const r = prng(91);
  const bark = new THREE.MeshStandardMaterial({ name: 'MAT_pine_bark', color: 0x3e3228, roughness: 1 });
  const needle = new THREE.MeshStandardMaterial({
    name: 'MAT_pine_needle', roughness: 0.8, alphaTest: 0.5, side: THREE.DoubleSide, vertexColors: true,
    map: leafTexture({ seed: 71, count: 48, len: 11, aspect: 0.1, h: 128, hv: 10, s: 32, l: 22, lv: 10 })
  });
  const g = new THREE.Group();
  g.name = 'PROC_courtyard_pine';
  const trunkH = Math.max(1.6, spot[3] || 2.2);
  const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.14, trunkH, 7), bark);
  trunk.position.y = trunkH / 2;
  g.add(trunk);
  const cloud = new CardCloud();
  for (let L = 0; L < 6; L++){
    const y = trunkH * 0.45 + L * 0.48;
    const rad = 1.05 - L * 0.14;
    const count = 70 - L * 6;
    for (let i = 0; i < count; i++){
      const a = r() * Math.PI * 2;
      const rr = rad * Math.sqrt(r());
      const p = new THREE.Vector3(Math.cos(a) * rr, y + (r() - 0.45) * 0.16, Math.sin(a) * rr);
      const out = new THREE.Vector3(Math.cos(a), 0.35, Math.sin(a)).normalize();
      cloud.add(p, 0.14 + r() * 0.07, out, out, 0.42 + L * 0.07 + (r() - 0.5) * 0.12, r);
    }
  }
  const leaves = new THREE.Mesh(cloud.geometry(), needle);
  leaves.name = 'PROC_pine_needles';
  g.add(leaves);
  g.position.set(spot[0], spot[1], spot[2]);
  scene.add(g);
  sway.push({ o: leaves, p: 1.4, a: 0.008, s: 0.35 });
}

// spots: [[x, z]...] ; palms and pine: [x, baseY, z, height]
export function buildGarden({ scene, root, spots, rows, palms, pine, cols, sway, renderer, grassMap, stoneMap }){
  applyLawn(root, grassMap);
  applyWalls(root, stoneMap);
  buildTrees(scene, spots, sway);
  buildHedges(scene, rows);
  buildColumns(scene, cols, sway);
  buildPalms(scene, palms || [], sway);
  buildPine(scene, pine, sway);
  buildFurniture(scene);
  const tick = buildPool(scene, root, renderer);
  if (stoneMap){
    root.traverse((o) => {
      if (!o.isMesh || o.name.indexOf('POOL_coping') !== 0) return;
      const mat = stoneMaterial(stoneMap);
      mat.name = 'MAT_pool_coping';
      mat.roughness = 0.62;
      o.material = mat;
    });
  }
  scene.traverse((o) => {
    if (o.isMesh && o.name.indexOf('PROC_') === 0){
      o.castShadow = true;
      o.receiveShadow = true;
    }
  });
  applyGlass(scene, root, renderer);
  return { update: (t) => { if (tick) tick(t); } };
}
