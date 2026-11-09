#!/usr/bin/env node
/** Pixel regressions: sun slider, door toggle, water animation (GF). */
import { chromium } from 'playwright';
import { createServer } from 'http';
import { createReadStream, existsSync, statSync } from 'fs';
import { extname, join, resolve } from 'path';

const REPO = resolve('/workspace/ashwood-estates-3d');
const mime = { '.html':'text/html','.js':'text/javascript','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml','.json':'application/json' };

function serve(root) {
  const server = createServer((req, res) => {
    const url = decodeURIComponent(req.url.split('?')[0]);
    const file = join(root, url.replace(/^\//, ''));
    if (!file.startsWith(root) || !existsSync(file) || statSync(file).isDirectory()) {
      res.writeHead(404); res.end('missing'); return;
    }
    res.writeHead(200, { 'Content-Type': mime[extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
    createReadStream(file).pipe(res);
  });
  return new Promise((r) => server.listen(0, '127.0.0.1', () => r(server)));
}

function diffPixels(a, b) {
  // a,b: Uint8ClampedArray RGBA
  let n = 0;
  const step = 8; // subsample RGBA
  for (let i = 0; i < a.length; i += 4 * step) {
    const d = Math.abs(a[i] - b[i]) + Math.abs(a[i + 1] - b[i + 1]) + Math.abs(a[i + 2] - b[i + 2]);
    if (d > 30) n++;
  }
  return n;
}

async function shot(page) {
  return page.evaluate(() => {
    const c = document.querySelector('canvas');
    const ctx = document.createElement('canvas');
    ctx.width = c.width; ctx.height = c.height;
    ctx.getContext('2d').drawImage(c, 0, 0);
    return {
      w: c.width, h: c.height,
      data: Array.from(ctx.getContext('2d').getImageData(0, 0, c.width, c.height).data),
    };
  });
}

async function enter3d(page) {
  await page.waitForTimeout(800);
  await page.evaluate(() => {
    const b = [...document.querySelectorAll('button')].find((x) => /3D/.test(x.textContent || ''));
    if (b) b.click();
  });
  await page.waitForFunction(() => window.__FP3D_QA__?.info?.().inited, null, { timeout: 90000 });
  await page.waitForTimeout(2000);
}

let failed = 0;
function pass(msg) { console.log('PASS:', msg); }
function fail(msg) { console.error('FAIL:', msg); failed++; }

const browser = await chromium.launch({ headless: true, args: ['--use-gl=swiftshader', '--ignore-gpu-blocklist'] });

async function withPage(path, fn) {
  const server = await serve(REPO);
  const port = server.address().port;
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  await page.goto(`http://127.0.0.1:${port}${path}`, { waitUntil: 'domcontentloaded', timeout: 120000 });
  try {
    await fn(page, errors);
  } finally {
    await page.close();
    server.close();
  }
}

// --- GF sun + door + water ---
await withPage('/production-line/viewer/gf/index.html', async (page, errors) => {
  await enter3d(page);
  const before = await shot(page);
  // sun to 9
  await page.evaluate(() => {
    const sun = document.querySelector('#sun');
    sun.value = '9';
    sun.dispatchEvent(new Event('input', { bubbles: true }));
  });
  await page.waitForTimeout(800);
  const afterSun = await shot(page);
  const sunDiff = diffPixels(Uint8ClampedArray.from(before.data), Uint8ClampedArray.from(afterSun.data));
  if (sunDiff > 50) pass(`GF sun slider changed canvas (~${sunDiff} sampled px)`);
  else fail(`GF sun slider did not change canvas (diff=${sunDiff})`);

  // door toggle if any
  const doorN = await page.evaluate(() => window.__FP3D_QA__?.info?.().doors3d || 0);
  if (doorN > 0) {
    // Move toward first door so the leaf fills more pixels, then toggle and wait for swing.
    await page.evaluate(() => {
      const qa = window.__FP3D_QA__;
      const info = qa.info();
      // eye-level near living looking in; then toggle
      if (qa.cam) qa.cam([7710, 1600, 17534], [7710, 1600, 14534], 60);
    });
    await page.waitForTimeout(400);
    const d0 = await shot(page);
    await page.evaluate(() => { window.__FP3D_QA__.toggleDoor(0); if (window.__LANE4_OPT__) window.__LANE4_OPT__.invalidateShadows(); });
    await page.waitForTimeout(1600);
    const d1 = await shot(page);
    const dd = diffPixels(Uint8ClampedArray.from(d0.data), Uint8ClampedArray.from(d1.data));
    if (dd > 5) pass(`GF door toggle changed canvas (~${dd})`);
    else fail(`GF door toggle no canvas change (diff=${dd})`);
  } else {
    pass('GF no doors to toggle (skipped)');
  }

  // water over 3s
  const w0 = await shot(page);
  await page.waitForTimeout(3000);
  const w1 = await shot(page);
  const wd = diffPixels(Uint8ClampedArray.from(w0.data), Uint8ClampedArray.from(w1.data));
  if (wd > 3) pass(`GF water animated over 3s (~${wd} sampled px)`);
  else fail(`GF water did not animate over 3s (diff=${wd})`);

  if (errors.length) fail('GF console errors: ' + errors.slice(0, 3).join(' | '));
  else pass('GF no console errors');
});

// --- FF sun (+ door if any) ---
await withPage('/production-line/viewer/ff/index.html', async (page, errors) => {
  await enter3d(page);
  const before = await shot(page);
  await page.evaluate(() => {
    const sun = document.querySelector('#sun');
    if (sun) { sun.value = '9'; sun.dispatchEvent(new Event('input', { bubbles: true })); }
  });
  await page.waitForTimeout(800);
  const afterSun = await shot(page);
  const sunDiff = diffPixels(Uint8ClampedArray.from(before.data), Uint8ClampedArray.from(afterSun.data));
  if (sunDiff > 50) pass(`FF sun slider changed canvas (~${sunDiff})`);
  else fail(`FF sun slider did not change canvas (diff=${sunDiff})`);
  const doorN = await page.evaluate(() => window.__FP3D_QA__?.info?.().doors3d || 0);
  if (doorN > 0) {
    const d0 = await shot(page);
    await page.evaluate(() => window.__FP3D_QA__.toggleDoor(0));
    await page.waitForTimeout(900);
    const d1 = await shot(page);
    const dd = diffPixels(Uint8ClampedArray.from(d0.data), Uint8ClampedArray.from(d1.data));
    if (dd > 5) pass(`FF door toggle changed canvas (~${dd})`);
    else fail(`FF door toggle no canvas change (diff=${dd})`);
  } else pass('FF no doors to toggle (skipped)');
  if (errors.length) fail('FF console errors: ' + errors.slice(0, 3).join(' | '));
  else pass('FF no console errors');
});

await browser.close();
if (failed) { console.error('RESULT: FAIL', failed); process.exit(1); }
console.log('RESULT: PASS');
