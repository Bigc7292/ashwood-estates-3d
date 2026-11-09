// usage: node bundle.mjs <repoRoot> <relHtml> <assets.json> <out.html> [dropSubstring...]
import * as esbuild from 'esbuild';
import fs from 'fs'; import path from 'path';
const [root, rel, assetsFile, out, ...drop] = process.argv.slice(2);
const htmlPath = path.join(root, rel), dir = path.dirname(htmlPath);
let html = fs.readFileSync(htmlPath, 'utf8');
for (const d of drop) html = html.split('\n').filter(l => !(l.includes('<script') && l.includes(d))).join('\n');
// importmap
let imap = {};
html = html.replace(/<script type="importmap">([\s\S]*?)<\/script>/, (m, j) => { imap = JSON.parse(j).imports || {}; return ''; });
const esc = s => s.replace(/<\/script/gi, '<\\/script');
// classic scripts
html = html.replace(/<script src="([^"]+)"><\/script>/g, (m, src) => {
  const f = path.resolve(dir, src); return '<script>' + esc(fs.readFileSync(f, 'utf8')) + '\n</script>';
});
const pageUrl = 'https://ashwood.local/' + path.dirname(rel) + '/';
const plugin = { name: 'importmap', setup(b) {
  b.onResolve({ filter: /.*/ }, a => {
    const s = a.path;
    if (imap[s]) return { path: path.resolve(dir, imap[s]) };
    for (const k of Object.keys(imap)) if (k.endsWith('/') && s.startsWith(k)) return { path: path.resolve(dir, imap[k], s.slice(k.length)) };
    if (s.startsWith('.') || s.startsWith('/')) return { path: path.resolve(a.resolveDir, s) };
    return undefined;
  });
}};
const mods = [];
html = html.replace(/<script type="module">([\s\S]*?)<\/script>/g, (m, code) => { mods.push(code); return `@@MOD${mods.length - 1}@@`; });
const PATCH = process.env.PATCH ? JSON.parse(fs.readFileSync(process.env.PATCH,'utf8')) : null;
for (let i = 0; i < mods.length; i++) {
  if (PATCH) { for (const [a, b2] of PATCH.replace) { if (!mods[i].includes(a)) throw new Error('patch miss: ' + a); mods[i] = mods[i].split(a).join(b2); } mods[i] += '\n' + PATCH.append; }
  const r = await esbuild.build({ stdin: { contents: mods[i], resolveDir: dir, loader: 'js', sourcefile: 'page-module.js' }, bundle: true, format: 'esm',
    minify: true, write: false, plugins: [plugin], define: { 'import.meta.url': JSON.stringify(pageUrl + 'page-module.js') }, logLevel: 'error', target: 'es2020' });
  html = html.replace(`@@MOD${i}@@`, () => '<script type="module">' + esc(r.outputFiles[0].text) + '</script>');
}
// assets shim: static scan for image basenames, resolved to files under the page dir or the importmap dirs
const mime = { jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', webp: 'image/webp' };
const A = {};
const names = new Set([...html.matchAll(/([A-Za-z0-9_][A-Za-z0-9_.-]*\.(?:jpg|jpeg|png|webp))/g)].map(m => m[1]));
const roots = [dir, ...Object.values(imap).flatMap(v => { const d0 = path.resolve(dir, v.endsWith('/') ? v : path.dirname(v)); return [d0, path.resolve(d0, '..'), path.resolve(d0, '..', '..')]; })];
const index = {};
function walk(d, depth) { if (depth > 7 || !fs.existsSync(d)) return; for (const e of fs.readdirSync(d, { withFileTypes: true })) {
  if (e.name.startsWith('.') || ['node_modules','verify','r5_step2','r6_step2','r7_step2','shots','cameras'].includes(e.name)) continue;
  const f = path.join(d, e.name); if (e.isDirectory()) walk(f, depth + 1); else if (names.has(e.name) && !index[e.name]) index[e.name] = f; } }
for (const r of roots) walk(r, 0);
for (const [n, f] of Object.entries(index)) { const ext = n.split('.').pop().toLowerCase(); A[n] = `data:${mime[ext]};base64,` + fs.readFileSync(f).toString('base64'); }
const shim = `<script>(function(){var A=${JSON.stringify(A)};function m(u){if(typeof u!=='string'||u.startsWith('data:'))return null;var s=u.split('?')[0].split('#')[0];var n=s.split('/').pop();try{n=decodeURIComponent(n)}catch(e){}return A[n]||null;}
var d=Object.getOwnPropertyDescriptor(HTMLImageElement.prototype,'src');Object.defineProperty(HTMLImageElement.prototype,'src',{get:d.get,set:function(v){var r=m(String(v));d.set.call(this,r||v);},configurable:true});
var sa=Element.prototype.setAttribute;Element.prototype.setAttribute=function(n,v){if(n==='src'&&this instanceof HTMLImageElement){var r=m(String(v));if(r)v=r;}return sa.call(this,n,v);};
var f=window.fetch;window.fetch=function(i,o){var u=typeof i==='string'?i:(i&&i.url);var r=m(u);return f.call(this,r||i,o);};
var xo=XMLHttpRequest.prototype.open;XMLHttpRequest.prototype.open=function(me,u){var r=m(String(u));arguments[1]=r||u;return xo.apply(this,arguments);};})();</script>`;
html = html.replace(/<head>/i, m => m + '\n' + shim);
fs.writeFileSync(out, html);
console.log(out, (html.length / 1e6).toFixed(2) + ' MB', 'assets:', Object.keys(A).join(','), 'modules:', mods.length);
