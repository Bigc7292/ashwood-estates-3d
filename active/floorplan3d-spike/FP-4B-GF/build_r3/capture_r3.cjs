// Headless eye-level captures of the GF viewer (index.html = before, index_r3.html = after). Read-only QA harness.
// Usage: node build_r3/capture_r3.cjs <page> <outDir> [shotFilter]   (server must serve FP-4B-GF/ on PORT, default 18733)
// Concept visualisation, not survey-verified, not construction-ready, not certified CAD.
const fs = require('fs'), path = require('path');
const PW = process.env.PW || path.resolve(__dirname, '../../../../exterior-garden-3d/4b/work/node_modules/playwright-core');
const {chromium} = require(PW);
const PORT = process.env.PORT || 18733, [page_, outDir, filt] = process.argv.slice(2);
const P = new Function(fs.readFileSync(path.join(__dirname, '../data/fp-4b-gf.plan.js'), 'utf8') + ';return PLAN')();
const pip = (p, poly) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++){ const [xi, yi] = poly[i], [xj, yj] = poly[j]; if ((yi > p[1]) !== (yj > p[1]) && p[0] < (xj - xi)*(p[1] - yi)/(yj - yi) + xi) c = !c; } return c; };
// Auto eye-level camera per room (display/QA assumption): along the room's longer bbox axis, camera 0.38 x length behind the
// centroid (pulled toward the centroid until inside the polygon and >= 450 mm from its bbox edge), eye 1.6 m
// (PLAN.DISPLAY.walk_eye_height_m), looking past the centroid to the far end at 1.1 m.
function roomCam(r, flip = false){
  const xs = r.poly.map(p => p[0]), ys = r.poly.map(p => p[1]), x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
  let cx = xs.reduce((a, b) => a + b)/xs.length, cy = ys.reduce((a, b) => a + b)/ys.length;
  if (!pip([cx, cy], r.poly)){ cx = (x0 + x1)/2; cy = (y0 + y1)/2; }
  const alongX = (x1 - x0) >= (y1 - y0), L = alongX ? x1 - x0 : y1 - y0, sgn = flip ? -1 : 1, clampE = (v, lo, hi) => Math.max(lo + 450, Math.min(hi - 450, v));
  let p = null;
  for (let k = .38; k > 0; k -= .04){ const q = alongX ? [clampE(cx - sgn*k*L, x0, x1), cy] : [cx, clampE(cy - sgn*k*L, y0, y1)]; if (pip(q, r.poly)){ p = q; break; } }
  p = p || [cx, cy];
  const t = alongX ? [cx + sgn*.5*L, cy] : [cx, cy + sgn*.5*L], small = Math.min(x1 - x0, y1 - y0) < 2600;
  return {p:[Math.round(p[0]), Math.round(p[1]), 1.6], t:[Math.round(t[0]), Math.round(t[1]), 1.1], fov:small ? 80 : 66};
}
const SHOTS = [];
P.ROOMS.filter(r => r.id !== 'plate').forEach(r => { SHOTS.push({id:'room_' + r.id, room:r.id, label:r.label || r.id, ...roomCam(r)}); SHOTS.push({id:'room_' + r.id + '_rev', room:r.id, label:(r.label || r.id) + ' (reverse)', ...roomCam(r, true)}); });
// F2 (entry west travertine wall, plan x 6040) and Q7 (courtyard) fixed cameras, plan mm + height m
SHOTS.push({id:'f2_entry_wall_oblique', room:'double-height-entry', label:'Entry west travertine wall (F2), oblique', p:[8900, 19150, 1.6], t:[6040, 16600, 2.4], fov:62});
SHOTS.push({id:'f2_entry_void_up', room:'double-height-entry', label:'Entry double-height void, looking up the travertine wall (F2)', p:[8700, 18900, 1.6], t:[6040, 17200, 4.2], fov:68});
SHOTS.push({id:'q7_courtyard_from_living', room:'outdoor-terrace', label:'Courtyard from the terrace edge, eye level (Q7)', p:[9650, 7900, 1.6], t:[11938, 10570, .9], fov:62});
SHOTS.push({id:'q7_courtyard_from_south', room:'outdoor-terrace', label:'Courtyard from the south, eye level (Q7)', p:[13900, 12900, 1.6], t:[11600, 9800, 1.0], fov:62});
SHOTS.push({id:'q7_courtyard_from_entry_side', room:'outdoor-terrace', label:'Courtyard looking east from the west glazing line (Q7)', p:[9600, 12700, 1.6], t:[12649, 9860, 1.2], fov:62});
(async () => {
  fs.mkdirSync(outDir, {recursive:true});
  const br = await chromium.launch({executablePath:process.env.CHROME || (process.env.HOME + '/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell'),
    args:['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl']});
  const ctx = await br.newContext({viewport:{width:1280, height:800}, deviceScaleFactor:1}), pg = await ctx.newPage();
  const errs = [], ext = [];
  pg.on('pageerror', e => errs.push(String(e))); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await ctx.route('**/*', r => { const u = r.request().url(); if (!u.startsWith(`http://127.0.0.1:${PORT}/`) && !u.startsWith('data:') && !u.startsWith('blob:')){ ext.push(u); return r.abort(); } return r.continue(); });
  await pg.goto(`http://127.0.0.1:${PORT}/${page_}`); await pg.waitForFunction(() => window.__FP3D_QA__ && typeof setView === 'function', null, {timeout:60000});
  await pg.evaluate("setView('3d')"); await pg.waitForFunction(() => window.__FP3D_QA__.info().inited, null, {timeout:120000}); await pg.waitForTimeout(6000);
  await pg.evaluate('__FP3D_QA__.settle(); __FP3D_QA__.labels(false); __FP3D_QA__.size(1280, 800); 0');
  const meta = {page:page_, r3:await pg.evaluate('__FP3D_QA__.r3 ? __FP3D_QA__.r3() : null'), info:await pg.evaluate('__FP3D_QA__.info()'), shots:[]};
  for (const s of SHOTS){
    if (filt && !new RegExp(filt).test(s.id)) continue;
    await pg.evaluate(([p, t, f]) => { __FP3D_QA__.look(p, t, f); return 0; }, [s.p, s.t, s.fov]);
    // two stills: first warms Water2 reflection/refraction targets for this camera
    await pg.evaluate('__FP3D_QA__.still(); 0');
    const r = await pg.evaluate('__FP3D_QA__.still()');
    fs.writeFileSync(path.join(outDir, s.id + '.png'), Buffer.from(r.png.split(',')[1], 'base64'));
    meta.shots.push(s); process.stdout.write(s.id + ' ');
  }
  meta.bench = await pg.evaluate('__FP3D_QA__.bench(4)');
  meta.console_errors = errs; meta.external_requests_blocked = ext;
  fs.writeFileSync(path.join(outDir, 'capture_meta.json'), JSON.stringify(meta, null, 1) + '\n');
  console.log('\nerrors:', errs.length, 'external:', ext.length, JSON.stringify(meta.bench));
  await br.close();
})().catch(e => { console.error(e); process.exit(1); });
