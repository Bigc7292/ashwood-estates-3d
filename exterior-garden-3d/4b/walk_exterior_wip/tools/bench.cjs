// fps bench: node bench.cjs <page.html> <view.json> [phone] -> ms/frame over 40 frames via window.__frame (headless swiftshader: relative numbers only)
const path=require('path'),fs=require('fs'),http=require('http'); const {chromium}=require(process.env.PWCORE||'/tmp/pw/node_modules/playwright-core');
const [pg_,vf,phone]=process.argv.slice(2); const ROOT=path.resolve(__dirname,'..','..');
const srv=http.createServer((q,r)=>{const p=path.join(ROOT,decodeURIComponent(q.url.split('?')[0]));fs.readFile(p,(e,d)=>{if(e){r.writeHead(404);return r.end();}r.writeHead(200,{'Content-Type':p.endsWith('.js')?'text/javascript':p.endsWith('.html')?'text/html':'application/octet-stream'});r.end(d);});});
srv.listen(0,async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});const pg=await b.newPage({viewport:{width:1280,height:720}});
await pg.goto(`http://127.0.0.1:${srv.address().port}/walk_exterior_wip/${pg_}?view=${encodeURIComponent(fs.readFileSync(vf,'utf8').trim())}${phone?'&phone=1':''}`, { waitUntil: 'commit', timeout: 0 });
await pg.waitForFunction(()=>document.title==='READY',null,{timeout:250000});
const ms=await pg.evaluate(()=>{const gl=document.querySelector('canvas').getContext('webgl2');const t0=performance.now();for(let i=0;i<40;i++){window.__frame(i/24,2);gl.finish();}return (performance.now()-t0)/40;});
console.log(JSON.stringify({page:pg_,phone:!!phone,ms_per_frame:+ms.toFixed(1),fps:+(1000/ms).toFixed(1)}));await b.close();srv.close();});
