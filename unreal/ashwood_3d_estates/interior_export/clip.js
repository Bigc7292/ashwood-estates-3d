// Usage: node clip.js in.glb out.glb xmin xmax zmin zmax
// Keeps triangles whose centroid is inside the house footprint, and drops flat plan-sheet overlays.
const fs = require('fs');
const [, , inp, out, x0, x1, z0, z1] = process.argv; const X0 = +x0, X1 = +x1, Z0 = +z0, Z1 = +z1;
const b = fs.readFileSync(inp); const jl = b.readUInt32LE(12); const j = JSON.parse(b.slice(20, 20 + jl).toString());
const binStart = 20 + jl + 8; const bin = b.slice(binStart);
const f32 = (ai) => { const a = j.accessors[ai], bv = j.bufferViews[a.bufferView]; const n = { VEC3: 3, VEC2: 2 }[a.type] * a.count; return new Float32Array(bin.buffer.slice(bin.byteOffset + bv.byteOffset, bin.byteOffset + bv.byteOffset + n * 4)); };
const chunks = []; let len = 0; const views = [], accs = [];
const push = (buf, target) => { const pad = (4 - len % 4) % 4; if (pad) { chunks.push(Buffer.alloc(pad)); len += pad; } chunks.push(buf); const v = { buffer: 0, byteOffset: len, byteLength: buf.length }; if (target) v.target = target; len += buf.length; views.push(v); return views.length - 1; };
const acc = (ta, type, mm) => { const a = { bufferView: push(Buffer.from(ta.buffer, ta.byteOffset, ta.byteLength), 34962), componentType: 5126, count: ta.length / (type === 'VEC3' ? 3 : 2), type }; if (mm) { const mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9]; for (let i = 0; i < ta.length; i += 3) for (let k = 0; k < 3; k++) { mn[k] = Math.min(mn[k], ta[i + k]); mx[k] = Math.max(mx[k], ta[i + k]); } a.min = mn; a.max = mx; } accs.push(a); return accs.length - 1; };
const images = (j.images || []).map(im => { const bv = j.bufferViews[im.bufferView]; return { bufferView: push(Buffer.from(bin.slice(bv.byteOffset, bv.byteOffset + bv.byteLength))), mimeType: im.mimeType }; });
const meshes = [], nodes = []; let kept = 0, dropped = 0, overlays = 0;
for (const m of j.meshes) {
  const p = m.primitives[0]; const a = j.accessors[p.attributes.POSITION];
  const h = a.max[1] - a.min[1], w = a.max[0] - a.min[0], d = a.max[2] - a.min[2];
  if (h < 0.02 && w > 16) { overlays++; dropped += a.count / 3; continue; } // whole-plot ground plate only
  const P = f32(p.attributes.POSITION), N = f32(p.attributes.NORMAL), U = f32(p.attributes.TEXCOORD_0);
  const oP = [], oN = [], oU = [];
  const planes = [[0, 1, X0], [0, -1, -X1], [2, 1, Z0], [2, -1, -Z1]]; // axis, sign, limit: keep sign*v[axis] >= limit
  for (let t = 0; t < P.length / 9; t++) {
    let poly = [0, 1, 2].map(k => ({ p: [P[t * 9 + k * 3], P[t * 9 + k * 3 + 1], P[t * 9 + k * 3 + 2]], n: [N[t * 9 + k * 3], N[t * 9 + k * 3 + 1], N[t * 9 + k * 3 + 2]], u: [U[t * 6 + k * 2], U[t * 6 + k * 2 + 1]] }));
    const inside = poly.every(v => v.p[0] >= X0 && v.p[0] <= X1 && v.p[2] >= Z0 && v.p[2] <= Z1);
    if (!inside) for (const [ax, sg, lim] of planes) {
      const res = []; for (let i = 0; i < poly.length; i++) { const A = poly[i], B = poly[(i + 1) % poly.length]; const da = sg * A.p[ax] - lim, db = sg * B.p[ax] - lim;
        if (da >= 0) res.push(A);
        if ((da >= 0) !== (db >= 0)) { const k = da / (da - db); res.push({ p: A.p.map((v, q) => v + (B.p[q] - v) * k), n: A.n, u: A.u.map((v, q) => v + (B.u[q] - v) * k) }); } }
      poly = res; if (poly.length < 3) break; }
    if (poly.length < 3) { dropped++; continue; }
    for (let i = 1; i < poly.length - 1; i++) for (const v of [poly[0], poly[i], poly[i + 1]]) { oP.push(...v.p); oN.push(...v.n); oU.push(...v.u); }
  }
  if (!oP.length) continue; kept += oP.length / 9;
  const P2 = new Float32Array(oP), N2 = new Float32Array(oN), U2 = new Float32Array(oU);
  meshes.push({ name: m.name, primitives: [{ attributes: { POSITION: acc(P2, 'VEC3', true), NORMAL: acc(N2, 'VEC3'), TEXCOORD_0: acc(U2, 'VEC2') }, material: p.material, mode: 4 }] });
  nodes.push({ name: m.name, mesh: meshes.length - 1 });
}
// Unreal merges sections by material name, and three.js names every material by class: make names unique.
const tag = require('path').basename(out).split('_')[0].toUpperCase();
j.materials.forEach((m, i) => {
  const c = m.pbrMetallicRoughness.baseColorFactor; const hex = c.slice(0, 3).map(v => Math.round(Math.min(1, Math.max(0, v)) ** (1 / 2.2) * 255).toString(16).padStart(2, '0')).join('');
  m.name = `M_${tag}_${String(i).padStart(3, '0')}_${hex}`;
  if (m.emissiveFactor && Math.max(...m.emissiveFactor) < 0.5) delete m.emissiveFactor;
});
const g = { asset: j.asset, scene: 0, scenes: [{ nodes: nodes.map((_, i) => i) }], nodes, meshes, materials: j.materials, accessors: accs, bufferViews: views, buffers: [{ byteLength: len }] };
if (images.length) { g.images = images; g.textures = j.textures; g.samplers = j.samplers; }
let js = Buffer.from(JSON.stringify(g)); js = Buffer.concat([js, Buffer.alloc((4 - js.length % 4) % 4, 0x20)]);
let bn = Buffer.concat(chunks); bn = Buffer.concat([bn, Buffer.alloc((4 - bn.length % 4) % 4)]);
const hd = Buffer.alloc(12); hd.writeUInt32LE(0x46546C67, 0); hd.writeUInt32LE(2, 4); hd.writeUInt32LE(28 + js.length + bn.length, 8);
const jh = Buffer.alloc(8); jh.writeUInt32LE(js.length, 0); jh.writeUInt32LE(0x4E4F534A, 4); const bh = Buffer.alloc(8); bh.writeUInt32LE(bn.length, 0); bh.writeUInt32LE(0x004E4942, 4);
fs.writeFileSync(out, Buffer.concat([hd, jh, js, bh, bn]));
console.log(JSON.stringify({ out, bytes: fs.statSync(out).size, keptTris: kept, droppedTris: dropped, overlaysDropped: overlays, meshes: meshes.length }));
