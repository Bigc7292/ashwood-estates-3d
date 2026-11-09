// Still grabber for roof_courtyard_pass.html (same as shoot.cjs, playwright from the repo cwd, system chromium).
const path = require('path'), fs = require('fs'), http = require('http');
const { chromium } = require('playwright');
const [page_, viewJson, out, w = '1280', h = '720'] = process.argv.slice(2);
const ROOT = path.resolve(__dirname, '..', '..');
function lockOf(f){ const j = JSON.parse(fs.readFileSync(f, 'utf8')); return j.view_param || j; }
const srv = http.createServer((q, r) => { const p = path.join(ROOT, decodeURIComponent(q.url.split('?')[0]));
  fs.readFile(p, (e, d) => { if (e) { r.writeHead(404); return r.end(); }
    const ext = path.extname(p); r.writeHead(200, {'Content-Type': {'.html':'text/html','.js':'text/javascript','.json':'application/json','.png':'image/png'}[ext] || 'application/octet-stream'}); r.end(d); }); });
srv.listen(0, async () => {
  const port = srv.address().port, view = JSON.stringify((lockOf(viewJson)));
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--no-sandbox'] });
  const pg = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 1 });
  const errs = []; pg.on('pageerror', e => errs.push(String(e))); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto(`http://127.0.0.1:${port}/walk_exterior_wip/${page_}?view=${encodeURIComponent(view)}`, { waitUntil: 'commit', timeout: 0 });
  await pg.waitForFunction(() => document.title === 'READY', null, { timeout: 120000 });
  await pg.waitForTimeout(1500);
  await pg.evaluate(() => { window.__capture = true; }); await pg.waitForTimeout(1500);
  await pg.screenshot({ path: out, timeout: 0 });
  console.log(errs.length ? 'PAGE ERRORS: ' + errs.slice(0, 5).join(' | ') : 'ok ' + out);
  await b.close(); srv.close();
});
