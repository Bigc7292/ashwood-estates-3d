import { chromium } from 'playwright-core';
import http from 'node:http'; import fs from 'node:fs'; import path from 'node:path';
const ROOT='/workspace/exterior-garden-3d/4b/model', OUT='/workspace/exterior-garden-3d/4b/renders';
const types={'.html':'text/html','.js':'text/javascript','.json':'application/json','.jpg':'image/jpeg','.png':'image/png'};
const srv=http.createServer((q,r)=>{ const p=path.join(ROOT, decodeURIComponent(q.url.split('?')[0])); if(!p.startsWith(ROOT)||!fs.existsSync(p)){r.writeHead(404);return r.end();}
  r.writeHead(200,{'content-type':types[path.extname(p)]||'application/octet-stream'}); fs.createReadStream(p).pipe(r); }).listen(8765,'127.0.0.1');
const S=' Layout: approved CAD V4 + 4B-GF calibration (~, ±3%). Heights/levels assumed; grey = neutral placeholder (unknown). Generated content, not a marketing render.';
const V = JSON.parse(fs.readFileSync(process.argv[2]));
const only = process.argv[3] ? process.argv[3].split(',') : null;
const browser = await chromium.launch({ executablePath: process.env.HOME+'/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell',
  args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'] });
for (const v0 of V) { if (only && !only.includes(v0.name)) continue;
 for (let attempt=1; attempt<=3; attempt++) { const v = {...v0}; try {
  const page = await browser.newPage({ viewport:{width:v.w||1600,height:v.h||1000} });
  page.on('console', m=>{ if(m.type()==='error') console.log('console', v.name, m.text()); }); page.on('pageerror', e=>console.log('pageerror', v.name, e.message));
  v.sub = (v.sub||'') + S;
  const qs = `view=${encodeURIComponent(JSON.stringify(v))}` + (v.hide?`&hide=${v.hide}`:'') + (v.flatwater?'&flatwater=1':'');
  await page.goto(`http://127.0.0.1:8765/index.html?${qs}`);
  await page.waitForFunction(()=>document.title==='READY', null, {timeout:120000});
  await page.screenshot({ path: `${OUT}/${v.file}`, timeout: 180000 }); console.log('wrote', v.file); await page.close(); break;
 } catch(e) { console.log('retry', v0.name, attempt, e.message.split('\n')[0]); } } }
await browser.close(); srv.close();
