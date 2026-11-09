// Water2 proof: node water_probe.cjs <page> <view.json> <outprefix>  -> <prefix>_t5.png, _t6.png (window.__frame at t=5 s, 6 s), _t6_hidden.png (Water2 + glint hidden)
const path=require('path'),fs=require('fs'),http=require('http'); const {chromium}=require(process.env.PWCORE||'/tmp/pw/node_modules/playwright-core');
const [pg_,vf,pre]=process.argv.slice(2); const ROOT=path.resolve(__dirname,'..','..');
const srv=http.createServer((q,r)=>{const p=path.join(ROOT,decodeURIComponent(q.url.split('?')[0]));fs.readFile(p,(e,d)=>{if(e){r.writeHead(404);return r.end();}r.writeHead(200,{'Content-Type':p.endsWith('.js')?'text/javascript':p.endsWith('.html')?'text/html':'application/octet-stream'});r.end(d);});});
srv.listen(0,async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});const pg=await b.newPage({viewport:{width:1280,height:720}});
await pg.goto(`http://127.0.0.1:${srv.address().port}/walk_exterior_wip/${pg_}?view=${encodeURIComponent(fs.readFileSync(vf,'utf8').trim())}`, { waitUntil: 'commit', timeout: 0 });
await pg.waitForFunction(()=>document.title==='READY',null,{timeout:250000}); await pg.waitForTimeout(1000);
await pg.evaluate(()=>window.__frame(5,10)); await pg.screenshot({timeout:0,path:pre+'_t5.png'});
await pg.evaluate(()=>window.__frame(6,10)); await pg.screenshot({timeout:0,path:pre+'_t6.png'});
await pg.evaluate(()=>{ for(const m of window.__WATERMESH||[]) m.visible=false; window.__frame(6,10); }); await pg.screenshot({timeout:0,path:pre+'_t6_hidden.png'});
console.log('ok'); await b.close(); srv.close();});
