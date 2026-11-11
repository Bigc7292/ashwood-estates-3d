const puppeteer=require('puppeteer-core');const path=require('path');
(async()=>{const b=await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:'new',args:['--ignore-gpu-blocklist','--enable-unsafe-swiftshader','--window-size=1280,800']});
const p=await b.newPage();p.on('console',m=>console.log('console',m.type(),m.text().slice(0,300)));p.on('pageerror',e=>console.log('pageerror',String(e).slice(0,300)));
await p.evaluateOnNewDocument(()=>{window.__s=[];Object.defineProperty(Object.prototype,'isScene',{configurable:true,get(){return undefined},set(v){Object.defineProperty(this,'isScene',{value:v,writable:true,configurable:true,enumerable:true});window.__s.push(this)}})});
await p.goto('file:///'+path.resolve(process.argv[2]).split(path.sep).join('/'),{waitUntil:'load',timeout:120000});
await new Promise(r=>setTimeout(r,8000));
console.log(await p.evaluate(()=>JSON.stringify({scenes:window.__s.length,three:window.__THREE__,canv:document.querySelectorAll('canvas').length,gl:!!document.createElement('canvas').getContext('webgl2'),body:document.body.innerText.slice(0,300)})));
await p.screenshot({path:process.argv[3]});await b.close()})();
