// Headless still/frame grabber for walk_exterior_wip pages (box: playwright-core + chromium headless shell, swiftshader WebGL).
// usage: node shoot.cjs <page.html> <view-json-file> <out.png|outdir> [w h] [frames fps]
//   still: waits for document.title==='READY', screenshots the canvas.
//   frames>0: drives window.__frame(t,T) deterministically and writes outdir/f_%04d.png (for ffmpeg).
const path = require('path'), fs = require('fs'), http = require('http');
const { chromium } = require(process.env.PWCORE || '/tmp/pw/node_modules/playwright-core');
const [page_, viewFile, out, w = '1280', h = '720', frames = '0', fps = '24'] = process.argv.slice(2);
const ROOT = path.resolve(__dirname, '..', '..');   // exterior-garden-3d/4b
const srv = http.createServer((q, r) => { const p = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(p, (e, d) => { if (e) { r.writeHead(404); return r.end(); }
    const ext = path.extname(p); r.writeHead(200, {'Content-Type': {'.html':'text/html','.js':'text/javascript','.json':'application/json','.png':'image/png','.jpg':'image/jpeg'}[ext] || 'application/octet-stream'}); r.end(d); }); });
srv.listen(0, async () => {
  const port = srv.address().port, view = fs.readFileSync(viewFile, 'utf8').trim();
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await b.newPage({ viewport: { width: +w, height: +h } });
  const errs = []; pg.on('pageerror', e => { errs.push(String(e)); console.log('PAGEERR', String(e)); }); pg.on('requestfailed', q => console.log('REQFAIL', q.url())); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto(`http://127.0.0.1:${port}/walk_exterior_wip/${page_}?view=${encodeURIComponent(view)}`, { waitUntil: 'commit', timeout: 0 });
  await pg.waitForFunction(() => document.title === 'READY', null, { timeout: +(process.env.TO||300000) });
  await pg.waitForTimeout(1500);
  const N = +frames;
  if (!N) { await pg.screenshot({ path: out }); }
  else { fs.mkdirSync(out, { recursive: true }); const T = N / +fps;
    for (let i = 0; i < N; i++) { await pg.evaluate(([t, T]) => window.__frame(t, T), [i / +fps, T]);
      await pg.screenshot({ path: path.join(out, `f_${String(i).padStart(4, '0')}.png`) }); if (i % 24 === 0) console.log('frame', i); } }
  if (errs.length) console.log('PAGE ERRORS:', errs.slice(0, 5).join(' | ')); else console.log('ok', out);
  await b.close(); srv.close();
});
