// Headless walkthrough capture for GF step 7 (new file). Runs the viewer's own fly-to-room tour,
// saves PNG frames, then ffmpeg encodes them to mp4 in the same folder.
const { chromium } = require('playwright');
const path = require('path');
const { execFileSync } = require('child_process');
const dir = __dirname;
const html = 'http://127.0.0.1:8765/active/floorplan3d-spike/FP-4B-GF/index_r3.html';
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox', '--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
  const page = await browser.newPage({ viewport: { width: 640, height: 360 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(html, { waitUntil: 'load', timeout: 120000 });
  await page.waitForFunction(() => window.View3D && window.__FP3D_QA__, null, { timeout: 120000 });
  await page.evaluate(() => window.View3D.enter && window.View3D.enter());
  await page.waitForTimeout(3000);
  const rooms = await page.evaluate(() => [...new Set([...document.querySelectorAll('tr[data-room]')].map(t => t.dataset.room))]);
  const tour = rooms.slice(0, 4);
  let n = 0;
  const shot = async () => { const f = path.join(dir, 'frames', `f${String(n++).padStart(4, '0')}.png`); console.log('frame', n, Date.now()); await page.screenshot({ path: f, timeout: 90000, animations: 'allow' }); };
  for (const id of tour) {
    await page.evaluate(id => window.View3D.flyToRoom(id), id);
    for (let i = 0; i < 4; i++) { await page.waitForTimeout(400); await shot(); }
    await page.waitForTimeout(600);
    await shot(); await shot();
  }
  await browser.close();
  execFileSync('ffmpeg', ['-y', '-framerate', '6', '-i', path.join(dir, 'frames', 'f%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '28', path.join(dir, 'GF_step7_walkthrough.mp4')], { stdio: 'ignore' });
  console.log(JSON.stringify({ rooms: tour, frames: n, errors: errors.slice(0, 10) }));
})().catch(e => { console.error('FAILED', e); process.exit(1); });
