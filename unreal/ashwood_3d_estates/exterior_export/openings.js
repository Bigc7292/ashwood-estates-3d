// Usage: node openings.js villa-materials.glb out.glb
// The villa shell is solid stone boxes with glass panes laid on their faces.
// Rebuilds the vertical faces of each house box with rectangular holes where a glass pane sits.
const fs = require('fs');
const [, , inp, out] = process.argv;
const b = fs.readFileSync(inp); const jl = b.readUInt32LE(12); const j = JSON.parse(b.slice(20, 20 + jl).toString());
let bin = Buffer.from(b.slice(20 + jl + 8, 20 + jl + 8 + j.buffers[0].byteLength));
const BOXES = ['GF_rear', 'GF_mid', 'GF_front', 'GF_multipurpose', 'FF_rear', 'FF_mid', 'FF_front', 'FF_front_left_bedroom', 'FF_front_right_suite'];
const bounds = (n) => { const t = n.translation || [0, 0, 0], s = n.scale || [1, 1, 1]; const mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9]; for (const p of j.meshes[n.mesh].primitives) { const a = j.accessors[p.attributes.POSITION]; for (let k = 0; k < 3; k++) { mn[k] = Math.min(mn[k], Math.min(a.min[k] * s[k], a.max[k] * s[k]) + t[k]); mx[k] = Math.max(mx[k], Math.max(a.min[k] * s[k], a.max[k] * s[k]) + t[k]); } } return { mn, mx }; };
const glassIdx = j.materials.findIndex(m => m.name === 'MAT_glass');
const panes = j.nodes.filter(n => n.mesh != null && !n.rotation && j.meshes[n.mesh].primitives.every(p => p.material === glassIdx)).map(n => ({ name: n.name, ...bounds(n) }));
const report = [];
for (const name of BOXES) {
  const node = j.nodes.find(n => n.name === name); if (!node) { report.push(name + ': MISSING'); continue; }
  const { mn, mx } = bounds(node); const mat = j.meshes[node.mesh].primitives[0].material;
  const P = [], N = [];
  const quad = (a, bb, c, d, n) => { for (const v of [a, bb, c, a, c, d]) { P.push(...v); N.push(...n); } };
  let holes = 0;
  // faces: axis (0 = x, 2 = z), side (0 = min, 1 = max)
  for (const ax of [0, 2]) for (const side of [0, 1]) {
    const c = side ? mx[ax] : mn[ax]; const u = ax === 0 ? 2 : 0; // in-plane horizontal axis
    const hs = panes.filter(p => (p.mx[ax] - p.mn[ax]) < 0.2 && p.mn[ax] < c + 0.12 && p.mx[ax] > c - 0.12)
      .map(p => ({ u0: Math.max(p.mn[u], mn[u]), u1: Math.min(p.mx[u], mx[u]), y0: Math.max(p.mn[1], mn[1]), y1: Math.min(p.mx[1], mx[1]) }))
      .filter(h => h.u1 - h.u0 > 0.05 && h.y1 - h.y0 > 0.05);
    holes += hs.length;
    const us = [...new Set([mn[u], mx[u], ...hs.flatMap(h => [h.u0, h.u1])])].sort((x, y) => x - y);
    const ys = [...new Set([mn[1], mx[1], ...hs.flatMap(h => [h.y0, h.y1])])].sort((x, y) => x - y);
    const nrm = [0, 0, 0]; nrm[ax] = side ? 1 : -1;
    for (let i = 0; i < us.length - 1; i++) for (let k = 0; k < ys.length - 1; k++) {
      const cu = (us[i] + us[i + 1]) / 2, cy = (ys[k] + ys[k + 1]) / 2;
      if (hs.some(h => cu > h.u0 && cu < h.u1 && cy > h.y0 && cy < h.y1)) continue;
      const pt = (uu, yy) => { const v = [0, yy, 0]; v[ax] = c; v[u] = uu; return v; };
      const A = pt(us[i], ys[k]), B = pt(us[i + 1], ys[k]), C = pt(us[i + 1], ys[k + 1]), D = pt(us[i], ys[k + 1]);
      // wind counter-clockwise seen from outside
      const ccw = (ax === 2) === (side === 1); if (ccw) quad(A, B, C, D, nrm); else quad(A, D, C, B, nrm);
    }
  }
  // top and bottom faces unchanged
  quad([mn[0], mx[1], mn[2]], [mn[0], mx[1], mx[2]], [mx[0], mx[1], mx[2]], [mx[0], mx[1], mn[2]], [0, 1, 0]);
  quad([mn[0], mn[1], mn[2]], [mx[0], mn[1], mn[2]], [mx[0], mn[1], mx[2]], [mn[0], mn[1], mx[2]], [0, -1, 0]);
  const add = (arr, minmax) => { const f = new Float32Array(arr); const pad = (4 - bin.length % 4) % 4; const off = bin.length + pad; bin = Buffer.concat([bin, Buffer.alloc(pad), Buffer.from(f.buffer)]); j.bufferViews.push({ buffer: 0, byteOffset: off, byteLength: f.byteLength, target: 34962 }); const a = { bufferView: j.bufferViews.length - 1, componentType: 5126, count: f.length / 3, type: 'VEC3' }; if (minmax) { a.min = [0, 1, 2].map(k => Math.min(...arr.filter((_, i) => i % 3 === k))); a.max = [0, 1, 2].map(k => Math.max(...arr.filter((_, i) => i % 3 === k))); } j.accessors.push(a); return j.accessors.length - 1; };
  j.meshes.push({ name: name + '_open', primitives: [{ attributes: { POSITION: add(P, true), NORMAL: add(N) }, material: mat, mode: 4 }] });
  node.mesh = j.meshes.length - 1; delete node.translation; delete node.scale;
  report.push(`${name}: ${holes} openings, ${P.length / 9} tris`);
}
j.buffers[0].byteLength = bin.length;
let js = Buffer.from(JSON.stringify(j)); js = Buffer.concat([js, Buffer.alloc((4 - js.length % 4) % 4, 0x20)]);
bin = Buffer.concat([bin, Buffer.alloc((4 - bin.length % 4) % 4)]);
const hd = Buffer.alloc(12); hd.writeUInt32LE(0x46546C67, 0); hd.writeUInt32LE(2, 4); hd.writeUInt32LE(28 + js.length + bin.length, 8);
const jh = Buffer.alloc(8); jh.writeUInt32LE(js.length, 0); jh.writeUInt32LE(0x4E4F534A, 4); const bh = Buffer.alloc(8); bh.writeUInt32LE(bin.length, 0); bh.writeUInt32LE(0x004E4942, 4);
fs.writeFileSync(out, Buffer.concat([hd, jh, js, bh, bin]));
console.log(report.join('\n')); console.log('glass panes considered:', panes.length, 'bytes', fs.statSync(out).size);
