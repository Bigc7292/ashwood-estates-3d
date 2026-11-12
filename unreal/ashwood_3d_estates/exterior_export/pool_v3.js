// Usage: node pool_v3.js in.glb out.glb
// Pool v3 (Colin's ruling): 4.8 m terrace between house and pool, pool water 9.50 x 3.60 m.
// The model has the CAD pool: water 2.38 m wide and a 0.9 m strip to the house.
// All pool and deck parts are axis-aligned boxes, so each is rebuilt with its z ends remapped.
const fs = require('fs');
const [, , inp, out] = process.argv;
const b = fs.readFileSync(inp); const jl = b.readUInt32LE(12); const j = JSON.parse(b.slice(20, 20 + jl).toString());
let bin = Buffer.from(b.slice(20 + jl + 8, 20 + jl + 8 + j.buffers[0].byteLength));
const TERRACE = 4.8, OLD_GAP = 0.90, WIDEN = 3.60 - 2.38;
const SHIFT = TERRACE - OLD_GAP; // 3.90 m toward the rear (negative z)
// z >= 4.6: house side, stays. 3.5..4.6: pool near edge, shifts. <= 1.2: pool far edge and steps, shift and widen.
const f = (z) => z >= 4.6 ? z : z >= 3.5 ? z - SHIFT : z <= 1.2 ? z - SHIFT - WIDEN : (() => { throw new Error('unexpected z ' + z); })();
const bounds = (n) => { const t = n.translation || [0, 0, 0], s = n.scale || [1, 1, 1]; const mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9]; for (const p of j.meshes[n.mesh].primitives) { const a = j.accessors[p.attributes.POSITION]; for (let k = 0; k < 3; k++) { mn[k] = Math.min(mn[k], Math.min(a.min[k] * s[k], a.max[k] * s[k]) + t[k]); mx[k] = Math.max(mx[k], Math.max(a.min[k] * s[k], a.max[k] * s[k]) + t[k]); } } return { mn, mx }; };
const add = (arr, minmax) => { const fa = new Float32Array(arr); const pad = (4 - bin.length % 4) % 4; const off = bin.length + pad; bin = Buffer.concat([bin, Buffer.alloc(pad), Buffer.from(fa.buffer)]); j.bufferViews.push({ buffer: 0, byteOffset: off, byteLength: fa.byteLength, target: 34962 }); const a = { bufferView: j.bufferViews.length - 1, componentType: 5126, count: fa.length / 3, type: 'VEC3' }; if (minmax) { a.min = [0, 1, 2].map(k => Math.min(...arr.filter((_, i) => i % 3 === k))); a.max = [0, 1, 2].map(k => Math.max(...arr.filter((_, i) => i % 3 === k))); } j.accessors.push(a); return j.accessors.length - 1; };
const box = (mn, mx) => { const P = [], N = []; const q = (a, bb, c, d, n) => { for (const v of [a, bb, c, a, c, d]) { P.push(...v); N.push(...n); } };
  const [x0, y0, z0] = mn, [x1, y1, z1] = mx;
  q([x0, y1, z0], [x0, y1, z1], [x1, y1, z1], [x1, y1, z0], [0, 1, 0]); q([x0, y0, z0], [x1, y0, z0], [x1, y0, z1], [x0, y0, z1], [0, -1, 0]);
  q([x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1], [0, 0, 1]); q([x1, y0, z0], [x0, y0, z0], [x0, y1, z0], [x1, y1, z0], [0, 0, -1]);
  q([x1, y0, z1], [x1, y0, z0], [x1, y1, z0], [x1, y1, z1], [1, 0, 0]); q([x0, y0, z0], [x0, y0, z1], [x0, y1, z1], [x0, y1, z0], [-1, 0, 0]);
  return { P, N }; };
const setBox = (node, mn, mx) => { const mat = j.meshes[node.mesh].primitives[0].material; const { P, N } = box(mn, mx); j.meshes.push({ name: node.name + '_v3', primitives: [{ attributes: { POSITION: add(P, true), NORMAL: add(N) }, material: mat, mode: 4 }] }); node.mesh = j.meshes.length - 1; delete node.translation; delete node.scale; };
const report = [];
for (const node of j.nodes) {
  if (node.mesh == null || !/^(POOL_|DECK_)/.test(node.name) || /^DECK_sofa/.test(node.name)) continue; // the sofa stays: the new terrace runs under it
  const { mn, mx } = bounds(node); const z0 = f(mn[2]), z1 = f(mx[2]);
  const nmn = [mn[0], mn[1], Math.min(z0, z1)], nmx = [mx[0], mx[1], Math.max(z0, z1)];
  // water is a flat plane: give it a hair of thickness so the box is valid
  if (nmx[1] - nmn[1] < 0.001) nmn[1] -= 0.01;
  setBox(node, nmn, nmx);
  report.push(`${node.name}: z ${mn[2].toFixed(2)}..${mx[2].toFixed(2)} -> ${nmn[2].toFixed(2)}..${nmx[2].toFixed(2)}`);
}
// keep the rear-right hedge out of the widened terrace
const hedge = j.nodes.find(n => n.name === 'HEDGE_lawn-4'); if (hedge) { const { mn, mx } = bounds(hedge); if (mn[0] < 15.95) { setBox(hedge, [15.95, mn[1], mn[2]], mx); report.push('HEDGE_lawn-4: trimmed to x >= 15.95'); } }
const water = j.nodes.find(n => /^POOL_water/.test(n.name)); if (water) { water.name = 'POOL_water (v3 9.50 x 3.60)'; }
// anything else standing in the new pool and terrace zone
const zone = { x0: 2.86, x1: 15.90, z0: f(0.21), z1: 3.85 };
const clash = j.nodes.filter(n => n.mesh != null && !/^(POOL_|DECK_|CONTEXT_ground|CONTEXT_lawn|GROUND_|LAWN|HEDGE_lawn-4)/.test(n.name)).map(n => ({ n: n.name, ...bounds(n) })).filter(o => o.mx[0] > zone.x0 && o.mn[0] < zone.x1 && o.mx[2] > zone.z0 && o.mn[2] < zone.z1 && o.mn[1] < 3).map(o => o.n);
j.buffers[0].byteLength = bin.length;
let js = Buffer.from(JSON.stringify(j)); js = Buffer.concat([js, Buffer.alloc((4 - js.length % 4) % 4, 0x20)]);
bin = Buffer.concat([bin, Buffer.alloc((4 - bin.length % 4) % 4)]);
const hd = Buffer.alloc(12); hd.writeUInt32LE(0x46546C67, 0); hd.writeUInt32LE(2, 4); hd.writeUInt32LE(28 + js.length + bin.length, 8);
const jh = Buffer.alloc(8); jh.writeUInt32LE(js.length, 0); jh.writeUInt32LE(0x4E4F534A, 4); const bh = Buffer.alloc(8); bh.writeUInt32LE(bin.length, 0); bh.writeUInt32LE(0x004E4942, 4);
fs.writeFileSync(out, Buffer.concat([hd, jh, js, bh, bin]));
console.log(report.join('\n')); console.log('clashes in new zone:', JSON.stringify(clash));
