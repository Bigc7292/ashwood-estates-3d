// Usage: node prune.js in.glb out.glb <nodeNameRegex> [x0 x1 z0 z1]
// Drops nodes whose name matches the regex (removes them from the scene list).
// With a box, also drops triangles whose centroid falls inside it below 2.5 m, so tree crowns overhead are kept (for flat merged meshes such as the planting capture).
const fs = require('fs');
const [, , inp, out, re, ...box] = process.argv; const rx = new RegExp(re); const B = box.map(Number);
const b = fs.readFileSync(inp); const jl = b.readUInt32LE(12); const j = JSON.parse(b.slice(20, 20 + jl).toString());
const bin = b.slice(20 + jl + 8);
const drop = new Set(); j.nodes.forEach((n, i) => { if (n.name && rx.test(n.name)) drop.add(i); });
j.scenes.forEach(s => { s.nodes = s.nodes.filter(i => !drop.has(i)); });
j.nodes.forEach(n => { if (n.children) n.children = n.children.filter(i => !drop.has(i)); });
let cut = 0;
if (B.length === 4) {
  for (const m of j.meshes) for (const p of m.primitives) {
    if (p.indices != null) continue; // planting capture is non-indexed
    const a = j.accessors[p.attributes.POSITION]; const bv = j.bufferViews[a.bufferView]; const off = bin.byteOffset + bv.byteOffset + (a.byteOffset || 0);
    const P = new Float32Array(bin.buffer.slice(off, off + a.count * 12));
    const keep = []; for (let t = 0; t < a.count / 3; t++) { const cx = (P[t * 9] + P[t * 9 + 3] + P[t * 9 + 6]) / 3, cz = (P[t * 9 + 2] + P[t * 9 + 5] + P[t * 9 + 8]) / 3; const cy = (P[t * 9 + 1] + P[t * 9 + 4] + P[t * 9 + 7]) / 3; if (cx > B[0] && cx < B[1] && cz > B[2] && cz < B[3] && cy < 2.5) cut++; else keep.push(t); }
    if (keep.length * 3 === a.count) continue;
    for (const [k, ai] of Object.entries(p.attributes)) {
      const acc = j.accessors[ai]; const v = j.bufferViews[acc.bufferView]; const n = { VEC3: 3, VEC2: 2, VEC4: 4 }[acc.type]; const o = bin.byteOffset + v.byteOffset + (acc.byteOffset || 0);
      const src = new Float32Array(bin.buffer.slice(o, o + acc.count * n * 4)); const dst = new Float32Array(keep.length * 3 * n);
      keep.forEach((t, i) => dst.set(src.subarray(t * 3 * n, t * 3 * n + 3 * n), i * 3 * n));
      Buffer.from(dst.buffer).copy(bin, v.byteOffset + (acc.byteOffset || 0)); acc.count = keep.length * 3;
      if (acc.min) { const mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9]; for (let i = 0; i < dst.length; i += 3) for (let q = 0; q < 3; q++) { mn[q] = Math.min(mn[q], dst[i + q]); mx[q] = Math.max(mx[q], dst[i + q]); } acc.min = mn; acc.max = mx; }
    }
  }
}
let js = Buffer.from(JSON.stringify(j)); js = Buffer.concat([js, Buffer.alloc((4 - js.length % 4) % 4, 0x20)]);
const bn = Buffer.from(bin);
const hd = Buffer.alloc(12); hd.writeUInt32LE(0x46546C67, 0); hd.writeUInt32LE(2, 4); hd.writeUInt32LE(28 + js.length + bn.length, 8);
const jh = Buffer.alloc(8); jh.writeUInt32LE(js.length, 0); jh.writeUInt32LE(0x4E4F534A, 4); const bh = Buffer.alloc(8); bh.writeUInt32LE(bn.length, 0); bh.writeUInt32LE(0x004E4942, 4);
fs.writeFileSync(out, Buffer.concat([hd, jh, js, bh, bn]));
console.log(JSON.stringify({ out, nodesDropped: drop.size, trisCut: cut }));
