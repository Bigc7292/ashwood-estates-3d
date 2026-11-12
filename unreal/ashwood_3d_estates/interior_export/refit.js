// Usage: node refit.js in.glb out.glb sx sz tx tz
// Applies a plan-only affine to every POSITION: x' = sx*x + tx, z' = sz*z + tz (glTF metres, Y-up; y kept).
// Used to put the FF interior capture on the same plan frame as the GF (measured against the approved
// V4 sheets by unreal/pipeline/overlay_cad.py). Normals are unchanged: sx == sz keeps them valid.
const fs = require('fs');
const [, , inp, out, sx, sz, tx, tz] = process.argv; const SX = +sx, SZ = +sz, TX = +tx, TZ = +tz;
if (Math.abs(SX - SZ) > 1e-6) throw new Error('sx and sz must match so normals stay valid');
const b = Buffer.from(fs.readFileSync(inp)); const jl = b.readUInt32LE(12); const j = JSON.parse(b.slice(20, 20 + jl).toString());
const binStart = 20 + jl + 8; const done = new Set(); let verts = 0;
for (const m of j.meshes) for (const p of m.primitives) {
  const ai = p.attributes.POSITION; if (done.has(ai)) continue; done.add(ai);
  const a = j.accessors[ai], bv = j.bufferViews[a.bufferView];
  const off = binStart + (bv.byteOffset || 0) + (a.byteOffset || 0), stride = bv.byteStride || 12;
  const mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9];
  for (let i = 0; i < a.count; i++) {
    const o = off + i * stride;
    const x = b.readFloatLE(o) * SX + TX, y = b.readFloatLE(o + 4), z = b.readFloatLE(o + 8) * SZ + TZ;
    b.writeFloatLE(x, o); b.writeFloatLE(z, o + 8);
    [x, y, z].forEach((v, k) => { mn[k] = Math.min(mn[k], v); mx[k] = Math.max(mx[k], v); });
  }
  a.min = mn; a.max = mx; verts += a.count;
}
let js = Buffer.from(JSON.stringify(j)); const pad = (4 - js.length % 4) % 4; js = Buffer.concat([js, Buffer.alloc(pad, 0x20)]);
const bin = b.slice(20 + jl);  // original BIN chunk header + data, unchanged length
const hd = Buffer.alloc(12); hd.writeUInt32LE(0x46546C67, 0); hd.writeUInt32LE(2, 4); hd.writeUInt32LE(20 + js.length + bin.length, 8);
const jh = Buffer.alloc(8); jh.writeUInt32LE(js.length, 0); jh.writeUInt32LE(0x4E4F534A, 4);
fs.writeFileSync(out, Buffer.concat([hd, jh, js, bin]));
console.log(JSON.stringify({ out, verts, accessors: done.size }));
