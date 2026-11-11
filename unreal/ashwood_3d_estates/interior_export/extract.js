// Usage: node extract.js <viewer.html> <out.glb>
// Loads a three.js viewer headless, captures its scene, writes a GLB (metres, Y-up).
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const hook = () => {
  window.__scenes = [];
  Object.defineProperty(Object.prototype, 'isScene', {
    configurable: true,
    get() { return undefined; },
    set(v) {
      Object.defineProperty(this, 'isScene', { value: v, writable: true, configurable: true, enumerable: true });
      if (v) window.__scenes.push(this);
    },
  });
};

const collect = async () => {
  const scenes = window.__scenes || [];
  let scene = null, best = -1;
  for (const s of scenes) { let n = 0; s.traverse && s.traverse(o => { if (o.isMesh) n++; }); if (n > best) { best = n; scene = s; } }
  if (!scene) return { error: 'no scene', count: scenes.length };
  scene.updateMatrixWorld(true);
  const chunks = []; let byteLen = 0;
  const g = { asset: { version: '2.0', generator: 'ashwood-viewer-extract' }, scene: 0, scenes: [{ nodes: [] }], nodes: [], meshes: [], materials: [], accessors: [], bufferViews: [], buffers: [{}], textures: [], images: [], samplers: [{ wrapS: 10497, wrapT: 10497 }] };
  const push = (ta, target) => {
    const pad = (4 - (byteLen % 4)) % 4; if (pad) { chunks.push(new Uint8Array(pad)); byteLen += pad; }
    const u8 = new Uint8Array(ta.buffer, ta.byteOffset, ta.byteLength);
    chunks.push(u8.slice()); const bv = { buffer: 0, byteOffset: byteLen, byteLength: u8.byteLength }; if (target) bv.target = target;
    byteLen += u8.byteLength; g.bufferViews.push(bv); return g.bufferViews.length - 1;
  };
  const texCache = new Map(), matCache = new Map();
  const texIndex = (t) => {
    if (!t || !t.image) return null;
    if (texCache.has(t.uuid)) return texCache.get(t.uuid);
    let idx = null;
    try {
      const img = t.image; const w = img.width || img.videoWidth, h = img.height || img.videoHeight;
      if (w && h) {
        const c = document.createElement('canvas'); const s = Math.min(1, 2048 / Math.max(w, h));
        c.width = Math.max(1, Math.round(w * s)); c.height = Math.max(1, Math.round(h * s));
        const ctx = c.getContext('2d');
        if (img.data && !(img instanceof HTMLElement) && !(img instanceof ImageBitmap)) {
          const id = new ImageData(new Uint8ClampedArray(img.data.buffer.slice(0, w * h * 4)), w, h); const c2 = document.createElement('canvas'); c2.width = w; c2.height = h; c2.getContext('2d').putImageData(id, 0, 0); ctx.drawImage(c2, 0, 0, c.width, c.height);
        } else ctx.drawImage(img, 0, 0, c.width, c.height);
        const b64 = c.toDataURL('image/png').split(',')[1]; const bin = atob(b64); const u8 = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) u8[i] = bin.charCodeAt(i);
        const bv = push(u8); g.images.push({ bufferView: bv, mimeType: 'image/png' }); g.textures.push({ source: g.images.length - 1, sampler: 0 }); idx = g.textures.length - 1;
      }
    } catch (e) { idx = null; }
    texCache.set(t.uuid, idx); return idx;
  };
  const matIndex = (m) => {
    if (matCache.has(m.uuid)) return matCache.get(m.uuid);
    const c = m.color || { r: 1, g: 1, b: 1 };
    const out = { name: m.name || m.type || 'mat', pbrMetallicRoughness: { baseColorFactor: [c.r, c.g, c.b, m.opacity == null ? 1 : m.opacity], roughnessFactor: m.roughness == null ? 0.8 : m.roughness, metallicFactor: m.metalness == null ? 0 : m.metalness }, doubleSided: m.side === 2 };
    if (m.transparent && (m.opacity < 1 || m.transmission > 0)) { out.alphaMode = 'BLEND'; if (m.transmission > 0 && m.opacity >= 1) out.pbrMetallicRoughness.baseColorFactor[3] = 0.25; }
    const ti = texIndex(m.map); if (ti != null) out.pbrMetallicRoughness.baseColorTexture = { index: ti };
    if (m.emissive && (m.emissive.r + m.emissive.g + m.emissive.b) > 0) { const k = Math.min(1, m.emissiveIntensity == null ? 1 : m.emissiveIntensity); out.emissiveFactor = [Math.min(1, m.emissive.r * k), Math.min(1, m.emissive.g * k), Math.min(1, m.emissive.b * k)]; }
    g.materials.push(out); matCache.set(m.uuid, g.materials.length - 1); return g.materials.length - 1;
  };
  const acc = (ta, type, comp, target, minmax) => {
    const n = { VEC3: 3, VEC2: 2, SCALAR: 1 }[type]; const a = { bufferView: push(ta, target), componentType: comp, count: ta.length / n, type };
    if (minmax) { const mn = [Infinity, Infinity, Infinity], mx = [-Infinity, -Infinity, -Infinity]; for (let i = 0; i < ta.length; i += 3) for (let k = 0; k < 3; k++) { mn[k] = Math.min(mn[k], ta[i + k]); mx[k] = Math.max(mx[k], ta[i + k]); } a.min = mn; a.max = mx; }
    g.accessors.push(a); return g.accessors.length - 1;
  };
  const visible = (o) => { for (let p = o; p; p = p.parent) if (!p.visible) return false; return true; };
  const xf = (e, x, y, z) => [e[0] * x + e[4] * y + e[8] * z + e[12], e[1] * x + e[5] * y + e[9] * z + e[13], e[2] * x + e[6] * y + e[10] * z + e[14]];
  const mul = (a, b) => { const o = new Array(16); for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) o[c * 4 + r] = a[r] * b[c * 4] + a[4 + r] * b[c * 4 + 1] + a[8 + r] * b[c * 4 + 2] + a[12 + r] * b[c * 4 + 3]; return o; };
  const buckets = {};
  const stats = { meshes: 0, tris: 0, skipped: 0, names: [] };
  const emit = (o, geo, mat, e, name, start, count) => {
    const pos = geo.attributes.position; if (!pos) return;
    const nor = geo.attributes.normal, uv = geo.attributes.uv; const idx = geo.index;
    const total = idx ? idx.count : pos.count; if (start == null) { start = 0; count = total; } count = Math.min(count, total - start); if (count < 3) return;
    const det = e[0] * (e[5] * e[10] - e[9] * e[6]) - e[4] * (e[1] * e[10] - e[9] * e[2]) + e[8] * (e[1] * e[6] - e[5] * e[2]);
    const P = new Float32Array(count * 3), N = new Float32Array(count * 3), U = uv ? new Float32Array(count * 2) : null;
    const t = mat.map; const rx = t ? t.repeat.x : 1, ry = t ? t.repeat.y : 1, ox = t ? t.offset.x : 0, oy = t ? t.offset.y : 0, flip = t ? t.flipY !== false : true;
    for (let i = 0; i < count; i++) {
      const vi = idx ? idx.getX(start + i) : start + i;
      const p = xf(e, pos.getX(vi), pos.getY(vi), pos.getZ(vi)); P.set(p, i * 3);
      if (U) { const u = uv.getX(vi) * rx + ox, v = uv.getY(vi) * ry + oy; U[i * 2] = u; U[i * 2 + 1] = flip ? 1 - v : v; }
    }
    for (let i = 0; i < count; i += 3) {
      if (det < 0) { for (let k = 0; k < 3; k++) { const a = P[(i + 1) * 3 + k]; P[(i + 1) * 3 + k] = P[(i + 2) * 3 + k]; P[(i + 2) * 3 + k] = a; } if (U) for (let k = 0; k < 2; k++) { const a = U[(i + 1) * 2 + k]; U[(i + 1) * 2 + k] = U[(i + 2) * 2 + k]; U[(i + 2) * 2 + k] = a; } }
      const ax = P[i * 3 + 3] - P[i * 3], ay = P[i * 3 + 4] - P[i * 3 + 1], az = P[i * 3 + 5] - P[i * 3 + 2], bx = P[i * 3 + 6] - P[i * 3], by = P[i * 3 + 7] - P[i * 3 + 1], bz = P[i * 3 + 8] - P[i * 3 + 2];
      let nx = ay * bz - az * by, ny = az * bx - ax * bz, nz = ax * by - ay * bx; const l = Math.hypot(nx, ny, nz) || 1; nx /= l; ny /= l; nz /= l;
      for (let k = 0; k < 3; k++) { N[(i + k) * 3] = nx; N[(i + k) * 3 + 1] = ny; N[(i + k) * 3 + 2] = nz; }
    }
    let ext = 0; { const mn=[1e9,1e9,1e9],mx=[-1e9,-1e9,-1e9]; for (let i=0;i<P.length;i+=3) for(let k=0;k<3;k++){mn[k]=Math.min(mn[k],P[i+k]);mx[k]=Math.max(mx[k],P[i+k]);} ext=Math.max(mx[0]-mn[0],mx[1]-mn[1],mx[2]-mn[2]); }
    if (ext > 100) { stats.skipped++; stats.names.push("big:" + name); return; }
    const mi = matIndex(mat); (buckets[mi] = buckets[mi] || []).push({ P, N, U });
    stats.meshes++; stats.tris += count / 3;
  };
  let n = 0;
  const all = []; scene.traverse(o => all.push(o));
  for (const o of all) {
    if (!o.isMesh || !visible(o) || !o.geometry || !o.material) { continue; }
    if (o.isSkinnedMesh) { stats.skipped++; continue; }
    const mats = Array.isArray(o.material) ? o.material : [o.material];
    if (mats.some(m => m && (m.isShaderMaterial && !m.color))) { stats.skipped++; stats.names.push('shader:' + (o.name || o.type)); continue; }
    const geo = o.geometry; const base = (o.name || (o.parent && o.parent.name) || 'mesh') + '_' + (n++);
    const mats4 = [];
    if (o.isInstancedMesh) { const im = o.instanceMatrix.array; for (let i = 0; i < o.count; i++) mats4.push(mul(o.matrixWorld.elements, Array.from(im.slice(i * 16, i * 16 + 16)))); }
    else mats4.push(o.matrixWorld.elements);
    mats4.forEach((e, k) => {
      if (Array.isArray(o.material) && geo.groups && geo.groups.length) geo.groups.forEach((gr, gi) => { const m = o.material[gr.materialIndex]; if (m && m.visible !== false) emit(o, geo, m, e, base + '_i' + k + '_g' + gi, gr.start, gr.count); });
      else if (mats[0].visible !== false) emit(o, geo, mats[0], e, base + (mats4.length > 1 ? '_i' + k : ''));
    });
    if (n % 200 === 0) await new Promise(r => setTimeout(r, 0));
  }
  for (const mi of Object.keys(buckets)) { const parts = buckets[mi]; let n = 0; for (const p of parts) n += p.P.length / 3; const P = new Float32Array(n*3), N = new Float32Array(n*3), U = new Float32Array(n*2); let o = 0; for (const p of parts) { P.set(p.P, o*3); N.set(p.N, o*3); if (p.U) U.set(p.U, o*2); o += p.P.length/3; }
    const name = (g.materials[mi].name || "mat") + "_" + mi; g.meshes.push({ name, primitives: [{ attributes: { POSITION: acc(P, "VEC3", 5126, 34962, true), NORMAL: acc(N, "VEC3", 5126, 34962), TEXCOORD_0: acc(U, "VEC2", 5126, 34962) }, material: +mi, mode: 4 }] }); g.nodes.push({ name, mesh: g.meshes.length - 1 }); g.scenes[0].nodes.push(g.nodes.length - 1); }
  g.buffers[0].byteLength = byteLen;
  if (!g.textures.length) { delete g.textures; delete g.images; delete g.samplers; }
  const bin = new Uint8Array(byteLen); let off = 0; for (const c of chunks) { bin.set(c, off); off += c.length; }
  let s = ''; const CH = 0x8000; for (let i = 0; i < bin.length; i += CH) s += String.fromCharCode.apply(null, bin.subarray(i, i + CH));
  return { json: JSON.stringify(g), bin: btoa(s), stats, sceneCount: scenes.length };
};

(async () => {
  const [, , html, out] = process.argv;
  const browser = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: 'new', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--window-size=1280,800'], protocolTimeout: 600000 });
  const page = await browser.newPage();
  page.on('pageerror', e => console.log('pageerror', String(e).slice(0, 200)));
  await page.evaluateOnNewDocument(hook);
  await page.goto('file:///' + path.resolve(html).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 120000 });
  await new Promise(r => setTimeout(r, 4000));
  const clicked = await page.evaluate(() => {
    if ((window.__scenes || []).length) return 'already';
    const els = [...document.querySelectorAll('button,a,[role=tab],[role=button],div,span,li')].filter(e => e.children.length === 0 || e.tagName === 'BUTTON');
    const hit = els.find(e => /^\s*3D Scene\s*$/i.test(e.textContent)) || els.find(e => /^\s*3D( view)?\s*$/i.test(e.textContent));
    if (hit) { hit.click(); return hit.textContent.trim(); } return 'none';
  });
  console.log('clicked:', clicked);
  await new Promise(r => setTimeout(r, 12000));
  const res = await page.evaluate(collect);
  await browser.close();
  if (res.error) { console.log(JSON.stringify(res)); process.exit(1); }
  let json = Buffer.from(res.json, 'utf8'); const jp = (4 - (json.length % 4)) % 4; json = Buffer.concat([json, Buffer.alloc(jp, 0x20)]);
  let bin = Buffer.from(res.bin, 'base64'); const bp = (4 - (bin.length % 4)) % 4; bin = Buffer.concat([bin, Buffer.alloc(bp)]);
  const head = Buffer.alloc(12); head.writeUInt32LE(0x46546C67, 0); head.writeUInt32LE(2, 4); head.writeUInt32LE(12 + 8 + json.length + 8 + bin.length, 8);
  const jh = Buffer.alloc(8); jh.writeUInt32LE(json.length, 0); jh.writeUInt32LE(0x4E4F534A, 4);
  const bh = Buffer.alloc(8); bh.writeUInt32LE(bin.length, 0); bh.writeUInt32LE(0x004E4942, 4);
  fs.writeFileSync(out, Buffer.concat([head, jh, json, bh, bin]));
  const j = JSON.parse(res.json); let mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9];
  for (const a of j.accessors) if (a.min) for (let k = 0; k < 3; k++) { mn[k] = Math.min(mn[k], a.min[k]); mx[k] = Math.max(mx[k], a.max[k]); }
  console.log(JSON.stringify({ out, bytes: fs.statSync(out).size, stats: res.stats, scenes: res.sceneCount, materials: j.materials.length, textures: (j.textures || []).length, min: mn.map(v => +v.toFixed(2)), max: mx.map(v => +v.toFixed(2)) }));
})().catch(e => { console.error(e); process.exit(1); });
