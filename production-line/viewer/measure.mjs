#!/usr/bin/env node
/**
 * Headless baseline / after metrics for lane-4 viewers.
 * Free: Playwright from repo .venv or npx. Serves repo root over localhost.
 */
import { createServer } from 'http';
import { readFileSync, writeFileSync, statSync, existsSync } from 'fs';
import { extname, join, resolve } from 'path';
import { pathToFileURL } from 'url';
import { spawnSync } from 'child_process';

const ROOT = resolve(new URL('.', import.meta.url).pathname, '../..');
const OUT = join(ROOT, 'production-line/viewer/baseline');
const port = 8765 + Math.floor(Math.random() * 1000);

const mime = {
  '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.json': 'application/json', '.css': 'text/css', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.wasm': 'application/wasm',
  '.module.js': 'text/javascript',
};

const server = createServer((req, res) => {
  let url = decodeURIComponent(req.url.split('?')[0]);
  if (url === '/') url = '/production-line/viewer/exterior/index.html';
  const file = join(ROOT, url.replace(/^\//, ''));
  if (!file.startsWith(ROOT) || !existsSync(file) || statSync(file).isDirectory()) {
    res.writeHead(404); res.end('missing'); return;
  }
  const ext = extname(file);
  res.writeHead(200, { 'Content-Type': mime[ext] || 'application/octet-stream', 'Cache-Control': 'no-store' });
  res.end(readFileSync(file));
});

function fileSize(rel) {
  const p = join(ROOT, rel);
  return existsSync(p) ? statSync(p).size : null;
}

const targets = [
  {
    id: 'gf-source',
    url: '/active/floorplan3d-spike/FP-4B-GF/index.html',
    html: 'active/floorplan3d-spike/FP-4B-GF/index.html',
    kind: 'fp3d',
  },
  {
    id: 'gf-opt',
    url: '/production-line/viewer/gf/index.html',
    html: 'production-line/viewer/gf/index.html',
    kind: 'fp3d',
  },
  {
    id: 'ff-opt',
    url: '/production-line/viewer/ff/index.html',
    html: 'production-line/viewer/ff/index.html',
    kind: 'fp3d',
  },
  {
    id: 'exterior-source-v6',
    url: '/exterior-garden-3d/4b/walkable/walkable_v6.html',
    html: 'exterior-garden-3d/4b/walkable/walkable_v6.html',
    kind: 'ext-embed',
  },
  {
    id: 'exterior-opt',
    url: '/production-line/viewer/exterior/index.html',
    html: 'production-line/viewer/exterior/index.html',
    kind: 'ext-opt',
  },
];

async function withPlaywright(fn) {
  let pw;
  try {
    pw = await import('playwright');
  } catch {
    // try venv path
    const r = spawnSync(join(ROOT, '.venv/bin/python'), ['-c', 'import playwright,os;print(os.path.dirname(playwright.__file__))'], { encoding: 'utf8' });
    if (r.status !== 0) throw new Error('playwright not importable from node; install or use python measure');
    throw new Error('Use measure.py with venv playwright');
  }
  return fn(pw);
}

await new Promise(r => server.listen(port, '127.0.0.1', r));
console.log('serving', ROOT, 'on', port);

const results = [];
try {
  const { chromium } = await import('playwright').catch(() => ({ chromium: null }));
  if (!chromium) throw new Error('no playwright');
  const browser = await chromium.launch({ headless: true, args: ['--use-gl=swiftshader', '--ignore-gpu-blocklist'] });
  for (const t of targets) {
    const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
    const consoleErrors = [];
    page.on('pageerror', e => consoleErrors.push(String(e)));
    page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
    const failed = [];
    page.on('requestfailed', r => failed.push(r.url()));
    const t0 = Date.now();
    let status = 'ok';
    let metrics = {};
    try {
      await page.goto(`http://127.0.0.1:${port}${t.url}`, { waitUntil: 'domcontentloaded', timeout: 60000 });
      // wait for READY title or canvas
      await page.waitForFunction(() => document.title.includes('READY') || !!document.querySelector('canvas'), null, { timeout: 45000 }).catch(() => {});
      // give scene a moment
      await page.waitForTimeout(1500);
      if (t.kind === 'fp3d') {
        // switch to 3D if needed
        await page.evaluate(() => {
          const b = [...document.querySelectorAll('button')].find(x => /3D/.test(x.textContent || ''));
          if (b) b.click();
        }).catch(() => {});
        await page.waitForTimeout(2000);
        metrics = await page.evaluate(async () => {
          const qa = window.__FP3D_QA__;
          const opt = window.__LANE4_OPT__;
          let fps = null;
          if (qa && qa.fps) fps = await qa.fps(1200);
          return {
            qa: qa ? qa.info() : null,
            opt: opt ? { pixelRatio: opt.pixelRatio(), shadowAutoUpdate: opt.shadowAutoUpdate(), shadowBaked: opt.shadowBaked(), looping: opt.looping() } : null,
            fps,
            canvases: document.querySelectorAll('canvas').length,
          };
        });
      } else if (t.kind === 'ext-opt') {
        metrics = await page.evaluate(() => ({
          ext: window.__LANE4_EXT__ ? window.__LANE4_EXT__.info() : null,
          canvases: document.querySelectorAll('canvas').length,
          title: document.title,
        }));
      } else {
        metrics = await page.evaluate(() => ({
          canvases: document.querySelectorAll('canvas').length,
          title: document.title,
          scripts: document.scripts.length,
        }));
      }
    } catch (e) {
      status = 'error';
      metrics = { error: String(e) };
    }
    const loadMs = Date.now() - t0;
    results.push({
      id: t.id,
      htmlBytes: fileSize(t.html),
      loadMs,
      status,
      consoleErrors: consoleErrors.slice(0, 8),
      failedRequests: failed.filter(u => !u.includes('favicon')).slice(0, 8),
      metrics,
      offlineVendor: t.id.includes('opt') ? 'production-line/viewer/vendor/three' : (t.id.startsWith('gf') ? 'active/.../vendor' : 'embedded'),
    });
    await page.close();
    console.log('measured', t.id, loadMs + 'ms', status);
  }
  await browser.close();
} catch (e) {
  console.error('playwright failed', e);
  writeFileSync(join(OUT, 'measure_error.json'), JSON.stringify({ error: String(e) }, null, 2));
  server.close();
  process.exit(1);
}

const summary = {
  measured_at: new Date().toISOString(),
  zone: 'Asia/Dubai',
  results,
  sizes: {
    gf_source_html: fileSize('active/floorplan3d-spike/FP-4B-GF/index.html'),
    gf_opt_html: fileSize('production-line/viewer/gf/index.html'),
    ff_opt_html: fileSize('production-line/viewer/ff/index.html'),
    exterior_v6_html: fileSize('exterior-garden-3d/4b/walkable/walkable_v6.html'),
    exterior_opt_html: fileSize('production-line/viewer/exterior/index.html'),
    exterior_opt_model_js: fileSize('production-line/viewer/exterior/model.js'),
    shared_vendor_three_module: fileSize('production-line/viewer/vendor/three/build/three.module.js'),
  },
};
writeFileSync(join(OUT, 'after.json'), JSON.stringify(summary, null, 2));
// also write before snapshot from sizes of sources
writeFileSync(join(OUT, 'before.json'), JSON.stringify({
  note: 'Source baselines (builders untouched)',
  gf_html_bytes: summary.sizes.gf_source_html,
  gf_pixelRatio_cap: 2,
  gf_shadow_autoUpdate: true,
  gf_loop: 'continuous requestAnimationFrame',
  exterior_v6_html_bytes: summary.sizes.exterior_v6_html,
  exterior_v6: 'single-file embedded three + textures (~1.78MB)',
  ff_on_main: false,
  rf_viewer: false,
}, null, 2));
console.log(JSON.stringify(summary.sizes, null, 2));
server.close();
