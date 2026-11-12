// Usage: node serve.js <folder>   Serves a folder on http://127.0.0.1:8765 for the headless capture.
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.resolve(process.argv[2]);
const types = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.glb': 'model/gltf-binary', '.jpg': 'image/jpeg', '.png': 'image/png', '.hdr': 'application/octet-stream', '.json': 'application/json' };
http.createServer((q, r) => {
  const p = path.join(root, decodeURIComponent(q.url.split('?')[0]));
  if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); }
  r.writeHead(200, { 'Content-Type': types[path.extname(p)] || 'application/octet-stream' });
  fs.createReadStream(p).pipe(r);
}).listen(8765, '127.0.0.1', () => console.log('serving ' + root));
