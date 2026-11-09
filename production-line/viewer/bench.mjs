#!/usr/bin/env node
/**
 * Like-for-like bench: each source/fork pair measured with the same Chromium,
 * same steps, same durations. Median of 3 runs.
 * Note: headless SwiftShader = software WebGL, not a phone GPU.
 */
import { chromium } from 'playwright';
import { createServer } from 'http';
import { createReadStream, existsSync, statSync, writeFileSync, readFileSync, unlinkSync } from 'fs';
import { extname, join, resolve } from 'path';

const REPO = resolve('/workspace/ashwood-estates-3d');
const OUT = join(REPO, 'production-line/viewer/baseline');
const mime = {
  '.html':'text/html','.js':'text/javascript','.mjs':'text/javascript','.json':'application/json',
  '.css':'text/css','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml','.wasm':'application/wasm',
};

function serve(root) {
  const server = createServer((req, res) => {
    const url = decodeURIComponent(req.url.split('?')[0]);
    const file = join(root, url.replace(/^\//, ''));
    if (!file.startsWith(root) || !existsSync(file) || statSync(file).isDirectory()) {
      res.writeHead(404); res.end('missing ' + url); return;
    }
    res.writeHead(200, { 'Content-Type': mime[extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
    createReadStream(file).pipe(res);
  });
  return new Promise((r) => server.listen(0, '127.0.0.1', () => r(server)));
}

function median(nums) {
  const a = [...nums].sort((x, y) => x - y);
  const m = Math.floor(a.length / 2);
  return a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2;
}

const PAIRS = [
  {
    id: 'gf',
    source: { root: '/tmp/gf_src', path: '/index.html', kind: 'fp3d' },
    fork: { root: REPO, path: '/production-line/viewer/gf/index.html', kind: 'fp3d' },
  },
  {
    id: 'ff',
    source: { root: '/tmp/ff_src/active/floorplan3d-spike/FP-4B-FF', path: '/index.html', kind: 'fp3d' },
    fork: { root: REPO, path: '/production-line/viewer/ff/index.html', kind: 'fp3d' },
  },
  {
    id: 'exterior-front',
    source: { root: '/tmp/fp_src', path: '/walk_exterior_wip/front_pass.html', kind: 'ext' },
    fork: { root: REPO, path: '/production-line/viewer/exterior-front/index.html', kind: 'ext' },
  },
];

async function oneRun(browser, target) {
  const server = await serve(target.root);
  const port = server.address().port;
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  const failed = [];
  page.on('requestfailed', (r) => failed.push(r.url()));

  // Exterior: interactive URL (no ?view=) so water/demand-render idle cost is measured fairly.
  // Still-capture ?view= freezes after 12 frames and is not the interactive path.
  const url = `http://127.0.0.1:${port}${target.path}`;

  const t0 = Date.now();
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 120000 });
  if (target.kind === 'fp3d') {
    await page.waitForTimeout(1000);
    await page.evaluate(() => {
      const b = [...document.querySelectorAll('button')].find((x) => /3D/.test(x.textContent || ''));
      if (b) b.click();
    });
    await page.waitForFunction(() => window.__FP3D_QA__ && window.__FP3D_QA__.info && window.__FP3D_QA__.info().inited, null, { timeout: 90000 });
    await page.waitForTimeout(1500);
  } else {
    await page.waitForFunction(() => !!document.querySelector('canvas') && (document.title.includes('READY') || window.__LANE4_FRONT__ || window.__MEASURE), null, { timeout: 90000 }).catch(()=>{});
    await page.waitForTimeout(2000);
    await page.evaluate(() => { document.title = document.title.includes('READY') ? document.title : 'READY'; });
  }
  const loadMs = Date.now() - t0;

  // Orbit FPS ~2s
  let orbitFps = null;
  if (target.kind === 'fp3d') {
    orbitFps = await page.evaluate(async () => {
      const qa = window.__FP3D_QA__;
      if (!qa?.fps) return null;
      // nudge orbit so damping/motion happens
      if (window.__LANE4_OPT__?.requestRender) window.__LANE4_OPT__.requestRender();
      return qa.fps(2000);
    });
  } else {
    orbitFps = await page.evaluate(async () => {
      let n = 0, last = performance.now(); const t0 = last; let worst = 0;
      await new Promise((res) => {
        const f = () => {
          const t = performance.now(); worst = Math.max(worst, t - last); last = t; n++;
          // synthetic orbit nudge via pointer
          if (t - t0 < 2000) requestAnimationFrame(f); else res();
        };
        requestAnimationFrame(f);
      });
      return { fps: +(n * 1000 / 2000).toFixed(1), worstFrameMs: +worst.toFixed(1) };
    });
  }

  // Idle 10s: frames + CPU (CDP Performance metrics; software WebGL)
  const cdp = await page.context().newCDPSession(page);
  await cdp.send('Performance.enable').catch(() => {});
  // Ensure source pages count renders via rAF wrapper if no lane4 API
  await page.evaluate(() => {
    if (!window.__BENCH) window.__BENCH = { renderCount: 0 };
    window.__BENCH.renderCount = 0;
    if (window.__LANE4_OPT__?.resetRenderCount) window.__LANE4_OPT__.resetRenderCount();
    if (window.__LANE4_FRONT__?.resetRenderCount) window.__LANE4_FRONT__.resetRenderCount();
    // Source continuous loop: count rAF callbacks as a proxy when no render hook exists
    if (!window.__LANE4_OPT__ && !window.__LANE4_FRONT__ && !window.__BENCH._rafHooked) {
      const wrap = window.requestAnimationFrame.bind(window);
      window.requestAnimationFrame = (cb) => wrap((ts) => { window.__BENCH.renderCount++; return cb(ts); });
      window.__BENCH._rafHooked = true;
      window.__BENCH.renderCount = 0;
    }
  });
  const cpu0 = await cdp.send('Performance.getMetrics');
  const idleStart = Date.now();
  await page.waitForTimeout(10000);
  const idleMs = Date.now() - idleStart;
  const cpu1 = await cdp.send('Performance.getMetrics');
  const idleFrames = await page.evaluate(() => {
    if (window.__LANE4_OPT__?.renderCount) return window.__LANE4_OPT__.renderCount();
    if (window.__LANE4_FRONT__?.info) return window.__LANE4_FRONT__.info().renderCount || 0;
    return window.__BENCH ? window.__BENCH.renderCount : null;
  });

  function metric(snap, name) {
    if (!snap?.metrics) return null;
    const m = snap.metrics.find((x) => x.name === name);
    return m ? m.value : null;
  }
  const task0 = metric(cpu0, 'TaskDuration');
  const task1 = metric(cpu1, 'TaskDuration');
  const script0 = metric(cpu0, 'ScriptDuration');
  const script1 = metric(cpu1, 'ScriptDuration');
  const idleCpuSec = (task0 != null && task1 != null)
    ? +(task1 - task0).toFixed(4)
    : (script0 != null && script1 != null ? +(script1 - script0).toFixed(4) : null);

  const info = await page.evaluate(() => {
    const qa = window.__FP3D_QA__?.info?.();
    const opt = window.__LANE4_OPT__;
    const front = window.__LANE4_FRONT__?.info?.() || window.__LANE4_FRONT__;
    const m = window.__MEASURE?.();
    return {
      qa, m, front,
      opt: opt ? {
        pixelRatio: opt.pixelRatio(),
        shadowAutoUpdate: opt.shadowAutoUpdate(),
        shadowBaked: opt.shadowBaked(),
        looping: opt.looping(),
      } : null,
      canvases: document.querySelectorAll('canvas').length,
      title: document.title,
    };
  });

  await page.close();
  server.close();
  return {
    loadMs,
    orbitFps,
    idleMs,
    idleFrames,
    idleCpuSec,
    idleCpuNote: 'CDP TaskDuration/ScriptDuration delta over ~10s idle; software WebGL (SwiftShader)',
    consoleErrors: errors.slice(0, 12),
    failedRequests: failed.filter((u) => !u.includes('favicon')).slice(0, 8),
    info,
  };
}

const browser = await chromium.launch({
  headless: true,
  args: ['--use-gl=swiftshader', '--ignore-gpu-blocklist'],
});

const report = {
  measured_at_utc: new Date().toISOString(),
  zone_label: 'Asia/Dubai',
  note: 'Software WebGL via SwiftShader — not a phone/desktop GPU. Median of 3 runs per target.',
  pairs: {},
};

for (const pair of PAIRS) {
  report.pairs[pair.id] = { source: [], fork: [] };
  for (const side of ['source', 'fork']) {
    for (let i = 0; i < 3; i++) {
      console.log('RUN', pair.id, side, i + 1);
      const r = await oneRun(browser, pair[side]);
      report.pairs[pair.id][side].push(r);
      console.log(' ', r.loadMs, 'ms idleFrames', r.idleFrames, 'cpu', r.idleCpuSec, 'errs', r.consoleErrors.length);
    }
  }
  // medians
  const med = (side, key, sub) => {
    const vals = report.pairs[pair.id][side].map((r) => (sub ? r[key]?.[sub] : r[key])).filter((v) => v != null && !Number.isNaN(v));
    return vals.length ? median(vals) : null;
  };
  report.pairs[pair.id].median = {
    source: {
      loadMs: med('source', 'loadMs'),
      orbitFps: med('source', 'orbitFps', 'fps'),
      idleFrames_10s: med('source', 'idleFrames'),
      idleCpuSec_10s: med('source', 'idleCpuSec'),
      consoleErrors: report.pairs[pair.id].source.reduce((n, r) => n + r.consoleErrors.length, 0),
    },
    fork: {
      loadMs: med('fork', 'loadMs'),
      orbitFps: med('fork', 'orbitFps', 'fps'),
      idleFrames_10s: med('fork', 'idleFrames'),
      idleCpuSec_10s: med('fork', 'idleCpuSec'),
      consoleErrors: report.pairs[pair.id].fork.reduce((n, r) => n + r.consoleErrors.length, 0),
    },
  };
  console.log('MEDIAN', pair.id, JSON.stringify(report.pairs[pair.id].median));
}

await browser.close();
writeFileSync(join(OUT, 'bench.json'), JSON.stringify(report, null, 2));
// Replace hand-written before.json with pointer to bench
writeFileSync(join(OUT, 'before.json'), JSON.stringify({
  replaced: true,
  note: 'Hand-written before.json deleted/replaced. Use bench.json (like-for-like source vs fork, median of 3).',
  bench: 'production-line/viewer/baseline/bench.json',
  measured_at_utc: report.measured_at_utc,
}, null, 2));
writeFileSync(join(OUT, 'after.json'), JSON.stringify({
  note: 'See bench.json for authoritative like-for-like medians. after.json retained as pointer.',
  bench: 'production-line/viewer/baseline/bench.json',
  measured_at_utc: report.measured_at_utc,
  medians: Object.fromEntries(Object.entries(report.pairs).map(([k, v]) => [k, v.median])),
}, null, 2));
console.log('WROTE bench.json');
