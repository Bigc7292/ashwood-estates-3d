const path=require('path'),fs=require('fs'),http=require('http');
const {chromium}=require('/tmp/pw/node_modules/playwright-core');
const ROOT='/workspace/pool-critic-ext/exterior-garden-3d/4b', OUT='/tmp/poolcrit';
const view=fs.readFileSync(ROOT+'/walk_exterior_wip/views/garden/cams/pool.json','utf8').trim();
const srv=http.createServer((q,r)=>{const p=path.join(ROOT,decodeURIComponent(q.url.split('?')[0]));fs.readFile(p,(e,d)=>{if(e){r.writeHead(404);return r.end();}r.writeHead(200,{'Content-Type':{'.html':'text/html','.js':'text/javascript','.json':'application/json','.png':'image/png','.jpg':'image/jpeg'}[path.extname(p)]||'application/octet-stream'});r.end(d);});});
srv.listen(0,async()=>{const port=srv.address().port;
 const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
 for (const [tag,extra] of [['flat','&flatwater=1'],['w2','']]) {
 const pg=await b.newPage({viewport:{width:1280,height:720}});
 pg.on('pageerror',e=>console.log('PAGEERR',String(e)));pg.on('console',m=>{if(m.type()!=='log')console.log('CON',m.text())});
 await pg.goto(`http://127.0.0.1:${port}/walk_exterior_wip/rear_pass.html?view=${encodeURIComponent(view)}${extra}`);
 await pg.waitForFunction(()=>document.title==='READY',null,{timeout:600000});
 await pg.waitForTimeout(1500);
 await pg.evaluate(()=>window.__frame(5,0)); await pg.screenshot({path:`${OUT}/${tag}_t5.png`});
 if(tag==='w2'){
  console.log(await pg.evaluate(()=>{const w=window.__WATERS[0]; let n=0; const ob=w.onBeforeRender; w.onBeforeRender=function(...a){n++; return ob.apply(this,a)}; window.__frame(5,0); w.geometry.computeBoundingBox(); const bb=w.geometry.boundingBox; return JSON.stringify({calls:n,pos:w.position.toArray(),min:bb.min.toArray(),max:bb.max.toArray(),parentVisible:w.parent.visible,layers:w.layers.mask,mat:w.material.type,transparent:w.material.transparent,depthWrite:w.material.depthWrite,side:w.material.side})}));
  console.log(await pg.evaluate(()=>JSON.stringify((window.__WATERS||[]).map(w=>({vis:w.visible,u:Object.keys(w.material.uniforms),n0:!!(w.material.uniforms.tNormalMap0.value.image),n0w:w.material.uniforms.tNormalMap0.value.image&&w.material.uniforms.tNormalMap0.value.image.width,col:w.material.uniforms.color.value.getHexString()})))));
  await pg.evaluate(()=>{window.__WATERS.forEach(w=>w.visible=false); window.__frame(5,0)}); await pg.screenshot({path:`${OUT}/nowater_t5.png`});
 }
 await pg.close();}
 await b.close();srv.close();});
