// Usage: node edit_glb.js in.glb out.glb ops.json <fileKey>
// Geometry edits for the Unreal villa, expressed in UNREAL WORLD centimetres.
// ops.json: { "<fileKey>": { "origin": [ox, oy, oz], "ops": [ ... ] } }
//   origin = the Unreal actor location of this mesh. Unreal local = 100 * (glTF x, glTF z, glTF y).
// Ops (boxes are [x0, x1, y0, y1, z0, z1] in world cm; rects [x0, x1, y0, y1]):
//   {"op":"subtract","box":[...]}            clip every triangle to the outside of the box
//      ("vertOnly":true leaves horizontal faces alone, so a box can reach down to a floor without cutting it)
//   {"op":"cut","box":[...]}                 same, but only horizontal triangles (floors, ceilings, slabs)
//   {"op":"remove","box":[...]}              drop triangles that lie fully inside the box
//   {"op":"line","rect":[...],"z":[za,zb],"material":"NAME"}   vertical lining faces round a hole
//   {"op":"stair","x":[x0,x1],"yStart":y,"dir":-1,"zBase":z,"risers":n,"rise":r,"going":g,
//    "thickness":t,"material":"NAME","axis":"x"|"y"}  stepped-slab straight flight ("axis":"x" runs along X, uses "y":[y0,y1] and "yStart" as the X start)
//   {"op":"move","box":[...],"except":[[...],...],"rotZ":deg,"pivot":[x,y],"offset":[dx,dy,dz],"skipNodes":"regex"}
//                                            relocate whole furniture pieces lying fully inside box
//   {"op":"dropNodes"|"keepNodes","nodes":"regex"}  split a file by part name
//   {"op":"clipTo","box":[...]}            keep only what lies inside the box (exact clip), for tiling
// Node transforms are baked, indices expanded; material names are kept (Unreal maps slots by name).
const fs = require('fs');
const [, , inp, out, opsPath, key] = process.argv;
const cfg = JSON.parse(fs.readFileSync(opsPath, 'utf8'))[key];
if (!cfg) throw new Error(`no ops for ${key}`);
const [OX, OY, OZ] = cfg.origin;
const toG = (x, y, z) => [(x - OX) / 100, (z - OZ) / 100, (y - OY) / 100];  // world cm -> glTF m
const boxG = (b) => { const a = toG(b[0], b[2], b[4]), c = toG(b[1], b[3], b[5]); return [Math.min(a[0], c[0]), Math.max(a[0], c[0]), Math.min(a[1], c[1]), Math.max(a[1], c[1]), Math.min(a[2], c[2]), Math.max(a[2], c[2])]; };

// ---------- read ----------
const b = fs.readFileSync(inp); const jl = b.readUInt32LE(12); const j = JSON.parse(b.slice(20, 20 + jl).toString());
const bin = b.slice(20 + jl + 8);
const NC = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4 };
const read = (ai) => {
  const a = j.accessors[ai], bv = j.bufferViews[a.bufferView], n = NC[a.type];
  const base = (bv.byteOffset || 0) + (a.byteOffset || 0);
  const csz = { 5126: 4, 5125: 4, 5123: 2, 5121: 1 }[a.componentType];
  const stride = bv.byteStride || n * csz; const outA = new Array(a.count * n);
  for (let i = 0; i < a.count; i++) for (let k = 0; k < n; k++) {
    const o = base + i * stride + k * csz;
    outA[i * n + k] = a.componentType === 5126 ? bin.readFloatLE(o) : a.componentType === 5125 ? bin.readUInt32LE(o) : a.componentType === 5123 ? bin.readUInt16LE(o) : bin.readUInt8(o);
  }
  return outA;
};
const mul = (A, B) => { const C = new Array(16).fill(0); for (let r = 0; r < 4; r++) for (let c = 0; c < 4; c++) for (let k = 0; k < 4; k++) C[c * 4 + r] += A[k * 4 + r] * B[c * 4 + k]; return C; };
const trs = (n) => {
  if (n.matrix) return n.matrix.slice();
  const [tx, ty, tz] = n.translation || [0, 0, 0], [qx, qy, qz, qw] = n.rotation || [0, 0, 0, 1], [sx, sy, sz] = n.scale || [1, 1, 1];
  const R = [1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy + qz * qw), 2 * (qx * qz - qy * qw), 0,
    2 * (qx * qy - qz * qw), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz + qx * qw), 0,
    2 * (qx * qz + qy * qw), 2 * (qy * qz - qx * qw), 1 - 2 * (qx * qx + qy * qy), 0, 0, 0, 0, 1];
  return [R[0] * sx, R[1] * sx, R[2] * sx, 0, R[4] * sy, R[5] * sy, R[6] * sy, 0, R[8] * sz, R[9] * sz, R[10] * sz, 0, tx, ty, tz, 1];
};
const I4 = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
const groups = [];  // {name, material, tris: [{p:[[x,y,z]x3], n:[[...]x3], u:[[..]x3]|null}]}
const visit = (ni, M) => {
  const n = j.nodes[ni]; const W = mul(M, trs(n));
  if (n.mesh !== undefined) for (const p of j.meshes[n.mesh].primitives) {
    if ((p.mode ?? 4) !== 4) continue;
    const P = read(p.attributes.POSITION), N = p.attributes.NORMAL !== undefined ? read(p.attributes.NORMAL) : null;
    const U = p.attributes.TEXCOORD_0 !== undefined ? read(p.attributes.TEXCOORD_0) : null;
    const idx = p.indices !== undefined ? read(p.indices) : [...Array(P.length / 3).keys()];
    const tp = (i) => [W[0] * P[i * 3] + W[4] * P[i * 3 + 1] + W[8] * P[i * 3 + 2] + W[12], W[1] * P[i * 3] + W[5] * P[i * 3 + 1] + W[9] * P[i * 3 + 2] + W[13], W[2] * P[i * 3] + W[6] * P[i * 3 + 1] + W[10] * P[i * 3 + 2] + W[14]];
    const tn = (i) => { if (!N) return null; const v = [W[0] * N[i * 3] + W[4] * N[i * 3 + 1] + W[8] * N[i * 3 + 2], W[1] * N[i * 3] + W[5] * N[i * 3 + 1] + W[9] * N[i * 3 + 2], W[2] * N[i * 3] + W[6] * N[i * 3 + 1] + W[10] * N[i * 3 + 2]]; const l = Math.hypot(...v) || 1; return v.map(c => c / l); };
    const tris = [];
    for (let t = 0; t + 2 < idx.length; t += 3) {
      const ids = [idx[t], idx[t + 1], idx[t + 2]]; const ps = ids.map(tp);
      let ns = ids.map(tn);
      if (!ns[0]) { const e1 = ps[1].map((v, k) => v - ps[0][k]), e2 = ps[2].map((v, k) => v - ps[0][k]); const c = [e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0]]; const l = Math.hypot(...c) || 1; ns = [0, 1, 2].map(() => c.map(v => v / l)); }
      tris.push({ p: ps, n: ns, u: U ? ids.map(i => [U[i * 2], U[i * 2 + 1]]) : null });
    }
    groups.push({ name: n.name || `mesh_${n.mesh}`, material: p.material, tris });
  }
  for (const c of n.children || []) visit(c, W);
};
for (const r of j.scenes[j.scene || 0].nodes) visit(r, I4);

// ---------- geometry helpers ----------
const lerp = (A, B, k) => ({ p: A.p.map((v, q) => v + (B.p[q] - v) * k), n: A.n, u: A.u ? A.u.map((v, q) => v + (B.u[q] - v) * k) : null });
const clipPoly = (poly, planes) => {
  for (const [ax, sg, lim] of planes) {
    const res = [];
    for (let i = 0; i < poly.length; i++) {
      const A = poly[i], B = poly[(i + 1) % poly.length], da = sg * A.p[ax] - lim, db = sg * B.p[ax] - lim;
      if (da >= 0) res.push(A);
      if ((da >= 0) !== (db >= 0)) res.push(lerp(A, B, da / (da - db)));
    }
    poly = res; if (poly.length < 3) return [];
  }
  return poly;
};
const area = (a, b, c) => { const e1 = b.map((v, k) => v - a[k]), e2 = c.map((v, k) => v - a[k]); return Math.hypot(e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0]) / 2; };
const verts = (t) => [0, 1, 2].map(k => ({ p: t.p[k], n: t.n[k], u: t.u ? t.u[k] : null }));
const fan = (poly) => { const outT = []; for (let i = 1; i < poly.length - 1; i++) { const vs = [poly[0], poly[i], poly[i + 1]]; if (area(vs[0].p, vs[1].p, vs[2].p) > 1e-8) outT.push({ p: vs.map(v => v.p), n: vs.map(v => v.n), u: vs[0].u ? vs.map(v => v.u) : null }); } return outT; };
const bboxOf = (t) => { const mn = [0, 1, 2].map(k => Math.min(t.p[0][k], t.p[1][k], t.p[2][k])), mx = [0, 1, 2].map(k => Math.max(t.p[0][k], t.p[1][k], t.p[2][k])); return [mn, mx]; };
const isHoriz = (t) => { const e1 = t.p[1].map((v, k) => v - t.p[0][k]), e2 = t.p[2].map((v, k) => v - t.p[0][k]); const c = [e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0]]; const l = Math.hypot(...c); return l > 0 && Math.abs(c[1]) / l > 0.9; };
const subtractBox = (t, B) => {
  const [x0, x1, y0, y1, z0, z1] = B; const [mn, mx] = bboxOf(t);
  if (mx[0] <= x0 || mn[0] >= x1 || mx[1] <= y0 || mn[1] >= y1 || mx[2] <= z0 || mn[2] >= z1) return [t];
  if (mn[0] >= x0 && mx[0] <= x1 && mn[1] >= y0 && mx[1] <= y1 && mn[2] >= z0 && mx[2] <= z1) return [];
  const inX = [[0, 1, x0], [0, -1, -x1]], inZ = [[2, 1, z0], [2, -1, -z1]];
  const regions = [[[0, -1, -x0]], [[0, 1, x1]], [...inX, [2, -1, -z0]], [...inX, [2, 1, z1]], [...inX, ...inZ, [1, -1, -y0]], [...inX, ...inZ, [1, 1, y1]]];
  const res = []; for (const R of regions) res.push(...fan(clipPoly(verts(t), R))); return res;
};
const quad = (a, b, c, d, nrm) => [{ p: [a, b, c], n: [nrm, nrm, nrm], u: null }, { p: [a, c, d], n: [nrm, nrm, nrm], u: null }];
const box = (x0, x1, y0, y1, z0, z1) => {  // glTF coords: y is up
  const P = (x, y, z) => [x, y, z]; const T = [];
  T.push(...quad(P(x0, y1, z0), P(x0, y1, z1), P(x1, y1, z1), P(x1, y1, z0), [0, 1, 0]));   // top
  T.push(...quad(P(x0, y0, z0), P(x1, y0, z0), P(x1, y0, z1), P(x0, y0, z1), [0, -1, 0]));  // bottom
  T.push(...quad(P(x0, y0, z0), P(x0, y0, z1), P(x0, y1, z1), P(x0, y1, z0), [-1, 0, 0]));
  T.push(...quad(P(x1, y0, z0), P(x1, y1, z0), P(x1, y1, z1), P(x1, y0, z1), [1, 0, 0]));
  T.push(...quad(P(x0, y0, z0), P(x0, y1, z0), P(x1, y1, z0), P(x1, y0, z0), [0, 0, -1]));
  T.push(...quad(P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1), [0, 0, 1]));
  return T;
};
const matIndex = (name) => { const i = j.materials.findIndex(m => m.name === name); if (i < 0) throw new Error(`material ${name} not found`); return i; };
const hasUV = groups.some(g => g.tris.length && g.tris[0].u);
const withUV = (tris) => tris.map(t => ({ ...t, u: hasUV ? t.p.map(p => [p[0] + p[2], p[1]]) : null }));

// ---------- apply ops ----------
const report = [];
for (const o of cfg.ops) {
  let before = 0, after = 0;
  if (o.op === 'dropInternal') {
    // Massing boxes (groups whose name matches o.nodes) share faces where they touch. A vertical face is
    // internal when the point just beyond it lies inside another massing box and the point just behind it
    // lies inside its own box. Those faces become phantom walls inside the house, so they are dropped.
    const re = new RegExp(o.nodes), D = (o.offsetCm || 5) / 100, eps = 0.002;
    const boxes = groups.filter(g => re.test(g.name)).map(g => {
      const mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9];
      for (const t of g.tris) for (const p of t.p) for (let k = 0; k < 3; k++) { mn[k] = Math.min(mn[k], p[k]); mx[k] = Math.max(mx[k], p[k]); }
      return { g, mn, mx };
    });
    // Exact version: every other massing box, inflated by 2 mm, is subtracted from this box's vertical
    // faces. Face parts that lie on a neighbour's surface (or inside it) are clipped away; the rest stays.
    // (Judging whole triangles by their centroid left diagonal half-walls where one big face is only
    // partly shared.)
    void D; void eps;
    const infl = 0.002;
    for (const own of boxes) {
      before += own.g.tris.length; const nt = [];
      for (const t of own.g.tris) {
        if (isHoriz(t)) { nt.push(t); continue; }
        let pieces = [t];
        for (const b of boxes) {
          if (b === own) continue;
          const B = [b.mn[0] - infl, b.mx[0] + infl, b.mn[1] - infl, b.mx[1] + infl, b.mn[2] - infl, b.mx[2] + infl];
          pieces = pieces.flatMap(p => subtractBox(p, B));
          if (!pieces.length) break;
        }
        nt.push(...pieces);
      }
      own.g.tris = nt; after += nt.length;
    }
  } else if (o.op === 'subtract' || o.op === 'cut' || o.op === 'remove') {
    const B = boxG(o.box);
    for (const g of groups) {
      before += g.tris.length; const nt = [];
      for (const t of g.tris) {
        if (o.op === 'remove') { const [mn, mx] = bboxOf(t); if (mn[0] >= B[0] && mx[0] <= B[1] && mn[1] >= B[2] && mx[1] <= B[3] && mn[2] >= B[4] && mx[2] <= B[5]) continue; nt.push(t); }
        else if (o.op === 'cut' && !isHoriz(t)) nt.push(t);
        else if (o.op === 'subtract' && o.vertOnly && isHoriz(t)) nt.push(t);
        else nt.push(...subtractBox(t, B));
      }
      g.tris = nt; after += nt.length;
    }
  } else if (o.op === 'move') {
    // Furniture relocation: triangles lying fully inside o.box (and not fully inside o.except) are
    // rotated by o.rotZ degrees about world Z round o.pivot [x, y] (world cm), then shifted by o.offset
    // [dx, dy, dz] (world cm). Whole pieces move intact; walls and floors that cross the box stay put.
    const B = boxG(o.box), E = (o.except ? (Array.isArray(o.except[0]) ? o.except : [o.except]) : []).map(boxG);
    const inside = (t, X) => { const [mn, mx] = bboxOf(t); return mn[0] >= X[0] && mx[0] <= X[1] && mn[1] >= X[2] && mx[1] <= X[3] && mn[2] >= X[4] && mx[2] <= X[5]; };
    const th = (o.rotZ || 0) * Math.PI / 180, c = Math.cos(th), s = Math.sin(th);
    const [px, py] = o.pivot || [OX, OY], pg = toG(px, py, OZ);  // pivot in glTF (x, z)
    const [dx, dy, dz] = o.offset || [0, 0, 0];
    // world (x, y) -> glTF (x, z): world rotation by th is the same rotation in the glTF x-z plane
    const rotP = (p) => { const x = p[0] - pg[0], z = p[2] - pg[2]; return [pg[0] + x * c - z * s + dx / 100, p[1] + dz / 100, pg[2] + x * s + z * c + dy / 100]; };
    const rotN = (n) => [n[0] * c - n[2] * s, n[1], n[0] * s + n[2] * c];
    const skip = o.skipNodes ? new RegExp(o.skipNodes) : null;  // e.g. wall materials whose floor-level caps must stay
    for (const g of groups) {
      if (skip && skip.test(g.name)) { before += g.tris.length; continue; }
      for (const t of g.tris) {
        if (!inside(t, B) || E.some(X => inside(t, X))) continue;
        t.p = t.p.map(rotP); t.n = t.n.map(rotN); after++;
      }
      before += g.tris.length;
    }
  } else if (o.op === 'clipTo') {
    // Keep only the part of every triangle inside the box (exact clip), e.g. to cut a floor into tiles for Lumen.
    // Bounds use half-open intervals in X/Y via the clip planes, so neighbouring tiles meet without gaps or overlaps.
    const B = boxG(o.box); const planes = [[0, 1, B[0]], [0, -1, -B[1]], [1, 1, B[2]], [1, -1, -B[3]], [2, 1, B[4]], [2, -1, -B[5]]];
    for (const g of groups) {
      before += g.tris.length; const nt = [];
      for (const t of g.tris) { const [mn, mx] = bboxOf(t); if (mx[0] < B[0] || mn[0] > B[1] || mx[1] < B[2] || mn[1] > B[3] || mx[2] < B[4] || mn[2] > B[5]) continue; nt.push(...fan(clipPoly(verts(t), planes))); }
      g.tris = nt; after += nt.length;
    }
  } else if (o.op === 'dropNodes' || o.op === 'keepNodes') {
    // Split a file by part name: dropNodes removes parts whose name matches o.nodes, keepNodes keeps only those.
    const re = new RegExp(o.nodes);
    for (const g of groups) { before += g.tris.length; if (re.test(g.name) === (o.op === 'dropNodes')) g.tris = []; after += g.tris.length; }
  } else if (o.op === 'line') {
    const [x0, x1, y0, y1] = o.rect, [za, zb] = o.z; const a = toG(x0, y0, za), c = toG(x1, y1, zb);
    const [gx0, gx1, gz0, gz1, gya, gyb] = [Math.min(a[0], c[0]), Math.max(a[0], c[0]), Math.min(a[2], c[2]), Math.max(a[2], c[2]), a[1], c[1]];
    const T = [];
    const wall = (p0, p1, nrm) => { const q = quad([p0[0], gya, p0[1]], [p1[0], gya, p1[1]], [p1[0], gyb, p1[1]], [p0[0], gyb, p0[1]], nrm); T.push(...q, ...q.map(t => ({ p: [t.p[0], t.p[2], t.p[1]], n: t.n.map(v => v.map(c2 => -c2)), u: null }))); };
    wall([gx0, gz0], [gx1, gz0], [0, 0, 1]); wall([gx1, gz0], [gx1, gz1], [-1, 0, 0]); wall([gx1, gz1], [gx0, gz1], [0, 0, -1]); wall([gx0, gz1], [gx0, gz0], [1, 0, 0]);
    groups.push({ name: `lining_${report.length}`, material: matIndex(o.material), tris: withUV(T) }); after = T.length;
  } else if (o.op === 'stair') {
    const T = [];
    for (let i = 1; i < o.risers; i++) {
      const ya = o.yStart + o.dir * i * o.going, yb = o.yStart + o.dir * (i - 1) * o.going, zt = o.zBase + i * o.rise;
      const zb = Math.max(o.zBase, zt - o.rise - o.thickness);
      // axis "y" (default): treads advance along Y between o.x[0..1]; axis "x": along X between o.y[0..1]
      const a = o.axis === 'x' ? toG(Math.min(ya, yb), o.y[0], zb) : toG(o.x[0], Math.min(ya, yb), zb);
      const c = o.axis === 'x' ? toG(Math.max(ya, yb), o.y[1], zt) : toG(o.x[1], Math.max(ya, yb), zt);
      T.push(...box(Math.min(a[0], c[0]), Math.max(a[0], c[0]), a[1], c[1], Math.min(a[2], c[2]), Math.max(a[2], c[2])));
    }
    groups.push({ name: o.name || `stair_${report.length}`, material: matIndex(o.material), tris: withUV(T) }); after = T.length;
  }
  report.push({ op: o.op, note: o.note || '', before, after });
}

// ---------- write ----------
const chunks = []; let len = 0; const views = [], accs = [];
const push = (buf, target) => { const pad = (4 - len % 4) % 4; if (pad) { chunks.push(Buffer.alloc(pad)); len += pad; } chunks.push(buf); const v = { buffer: 0, byteOffset: len, byteLength: buf.length }; if (target) v.target = target; len += buf.length; views.push(v); return views.length - 1; };
const acc = (ta, type, mm) => { const a = { bufferView: push(Buffer.from(ta.buffer, ta.byteOffset, ta.byteLength), 34962), componentType: 5126, count: ta.length / NC[type], type }; if (mm) { const mn = [1e9, 1e9, 1e9], mx = [-1e9, -1e9, -1e9]; for (let i = 0; i < ta.length; i += 3) for (let k = 0; k < 3; k++) { mn[k] = Math.min(mn[k], ta[i + k]); mx[k] = Math.max(mx[k], ta[i + k]); } a.min = mn; a.max = mx; } accs.push(a); return accs.length - 1; };
const images = (j.images || []).map(im => { const bv = j.bufferViews[im.bufferView]; return { bufferView: push(Buffer.from(bin.slice(bv.byteOffset || 0, (bv.byteOffset || 0) + bv.byteLength))), mimeType: im.mimeType }; });
const meshes = [], nodes = []; let tri = 0;
for (const g of groups) {
  if (!g.tris.length) continue; tri += g.tris.length;
  const P = new Float32Array(g.tris.flatMap(t => t.p.flat())), N = new Float32Array(g.tris.flatMap(t => t.n.flat()));
  const attributes = { POSITION: acc(P, 'VEC3', true), NORMAL: acc(N, 'VEC3') };
  if (hasUV) attributes.TEXCOORD_0 = acc(new Float32Array(g.tris.flatMap(t => (t.u || [[0, 0], [0, 0], [0, 0]]).flat())), 'VEC2');
  const prim = { attributes, mode: 4 }; if (g.material !== undefined) prim.material = g.material;
  meshes.push({ name: g.name, primitives: [prim] }); nodes.push({ name: g.name, mesh: meshes.length - 1 });
}
const gl = { asset: j.asset, scene: 0, scenes: [{ nodes: nodes.map((_, i) => i) }], nodes, meshes, materials: j.materials, accessors: accs, bufferViews: views, buffers: [{ byteLength: len }] };
if (images.length) { gl.images = images; gl.textures = j.textures; gl.samplers = j.samplers; }
let js = Buffer.from(JSON.stringify(gl)); js = Buffer.concat([js, Buffer.alloc((4 - js.length % 4) % 4, 0x20)]);
let bn = Buffer.concat(chunks); bn = Buffer.concat([bn, Buffer.alloc((4 - bn.length % 4) % 4)]);
const hd = Buffer.alloc(12); hd.writeUInt32LE(0x46546C67, 0); hd.writeUInt32LE(2, 4); hd.writeUInt32LE(28 + js.length + bn.length, 8);
const jh = Buffer.alloc(8); jh.writeUInt32LE(js.length, 0); jh.writeUInt32LE(0x4E4F534A, 4); const bh = Buffer.alloc(8); bh.writeUInt32LE(bn.length, 0); bh.writeUInt32LE(0x004E4942, 4);
fs.writeFileSync(out, Buffer.concat([hd, jh, js, bh, bn]));
console.log(JSON.stringify({ out, meshes: meshes.length, tris: tri, ops: report }));
