import json,re,sys
B=sys.argv[1]
views=[
 ("front","Front","front_v2",{"name":"ELEV-FRONT","pos":[8.57,1.6,45.4],"tgt":[8.57,4.5,26.9],"fov":40,"labels":False,"shift":True},"Front elevation on the quality-pass locked camera. Technical labels are hidden by default; the required concept disclaimer remains visible."),
 ("left","Left side","left_pass",{"name":"ELEV-LEFT","pos":[-14.5,1.8,15.0],"tgt":[8.0,4.0,15.0],"fov":40,"labels":False,"shift":True},"Left elevation on the revised quality-pass camera. Compare with the approved reference in the Side-by-side tab."),
 ("right","Right side","right_pass",{"name":"ELEV-RIGHT","pos":[32.0,1.8,15.0],"tgt":[10.0,4.0,15.0],"fov":40,"labels":False,"shift":True},"Right elevation preserving the evidence-backed M38 slab at z0=0.53; independent critic review confirmed that retracting it would contradict the approved elevation."),
 ("site","Site + pool","site_pass",{"name":"SITE-AERIAL","pos":[30.0,26.0,-14.0],"tgt":[9.36,0.0,12.0],"fov":40,"labels":False},"Rear-east aerial framing the M44 pool, terrace and M30 enlarged garden without moving CAD trees."),
 ("rear","Rear + garden","rear_v3",{"name":"ELEV-REAR","pos":[8.0,4.5,-14.0],"tgt":[8.0,2.5,6.0],"fov":42,"labels":False},"Corrected rear source with shared_pool_v3 / M44 and visible Water2 reflection and refraction; retired rear_pass pool v2 is not used."),
]
shim=None; data={}
for key,_,f,v,_n in views:
    h=open(f"{B}/out/ext_{f}.html").read()
    m=re.search(r'<script>\(function\(\)\{var A=.*?</script>',h,re.S)
    if shim is None: shim=m.group(0)
    h=h.replace(m.group(0),'<!--SHIM-->',1)
    lit="""'{"name":"aerial","pos":[-14,30,48],"tgt":[9.4,3,15],"fov":40}'"""
    assert h.count(lit)==1, (key,h.count(lit))
    h=h.replace(lit,"(window.__V||"+lit+")")
    assert 'window.__V' in h, key
    data[key]=h
sbsL=open(f"{B}/sbs_left.b64").read(); sbsR=open(f"{B}/sbs_right.b64").read()
def js(o): return json.dumps(o).replace('</','<\\/')
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ashwood 4-Bed Exterior</title>
<style>
:root{{--bg:#f6f4ef;--fg:#1d1f1c;--muted:#5d625b;--line:#d9d6cc;--accent:#6b4f2a;--accent-fg:#fff;--surface:#fff}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151614;--fg:#ece9e1;--muted:#a6aaa1;--line:#34372f;--accent:#d1a86b;--accent-fg:#151614;--surface:#1e201d}}}}
:root[data-theme="dark"]{{--bg:#151614;--fg:#ece9e1;--muted:#a6aaa1;--line:#34372f;--accent:#d1a86b;--accent-fg:#151614;--surface:#1e201d}}
html,body{{margin:0;height:100%;background:var(--bg);color:var(--fg);font:14px/1.45 Georgia,serif}}
.wrap{{display:flex;flex-direction:column;height:100%}}
header{{padding:10px 16px 6px}} h1{{font-size:19px;margin:0 0 2px}} .sub{{color:var(--muted);font-size:12.5px;margin:0}}
.tabs{{display:flex;gap:6px;flex-wrap:wrap;padding:6px 16px}}
.tab{{font:inherit;font-size:13px;padding:6px 12px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--fg);cursor:pointer}}
.tab[aria-selected="true"]{{background:var(--accent);color:var(--accent-fg);border-color:var(--accent)}}
.note{{padding:2px 16px 8px;font-size:13px;color:var(--muted)}}
.stage{{flex:1;min-height:320px;position:relative;margin:0 16px 16px;border:1px solid var(--line);border-radius:6px;overflow:hidden;background:#cfd8de}}
iframe{{border:0;width:100%;height:100%;display:block}}
.sbs{{overflow:auto;height:100%;background:var(--surface);padding:12px;box-sizing:border-box}} .sbs img{{width:100%;height:auto;display:block;margin-bottom:6px}} .sbs h2{{font-size:15px;margin:10px 0 4px}}
.help{{font-size:12px;color:var(--muted);padding:0 16px 4px}}
</style></head><body><div class="wrap">
<header><h1>Ashwood 4-bed villa: exterior model</h1>
<p class="sub">Concept visualisation, not survey-verified, not construction-ready, not certified CAD. Built from the merged repo state, 2026-11-10. This page replaces the earlier walkable WIP (v3, grey placeholders), which the exterior lane's views below supersede.</p></header>
<div class="tabs" role="tablist" id="tabs"></div>
<p class="note" id="note"></p>
<p class="help">Drag to orbit round the house, scroll or pinch to zoom, right-drag or two fingers to pan. Each tab opens on its matched camera. One view loads at a time.</p>
<div class="stage" id="stage"></div></div>
{shim}
<script>
const VIEWS={js([[k,l,v,n] for k,l,f,v,n in views])};
const DATA={js(data)};
const SBS={{left:"data:image/jpeg;base64,{sbsL}",right:"data:image/jpeg;base64,{sbsR}"}};
const SHIM=document.scripts[0].outerHTML;
const tabs=document.getElementById('tabs'),stage=document.getElementById('stage'),note=document.getElementById('note');
function show(k){{
  [...tabs.children].forEach(b=>b.setAttribute('aria-selected',b.dataset.k===k?'true':'false'));
  stage.innerHTML='';
  if(k==='sbs'){{note.textContent='Historical model-versus-approved-reference comparisons from earlier locked-view passes; use the live tabs for the current quality-pass geometry.';
    stage.innerHTML='<div class="sbs"><h2>Left side</h2><img alt="Left side: model vs reference" src="'+SBS.left+'"><h2>Right side</h2><img alt="Right side: model vs reference" src="'+SBS.right+'"></div>';return;}}
  const v=VIEWS.find(x=>x[0]===k); note.textContent=v[3];
  const f=document.createElement('iframe'); f.title=v[1];
  f.srcdoc=DATA[k].replace('<!--SHIM-->',SHIM+'<script>window.__V='+JSON.stringify(JSON.stringify(v[2]))+';<\\/script>');
  stage.appendChild(f);
}}
VIEWS.forEach(v=>{{const b=document.createElement('button');b.className='tab';b.setAttribute('role','tab');b.dataset.k=v[0];b.textContent=v[1];b.onclick=()=>show(v[0]);tabs.appendChild(b);}});
{{const b=document.createElement('button');b.className='tab';b.setAttribute('role','tab');b.dataset.k='sbs';b.textContent='Side-by-side (left, right)';b.onclick=()=>show('sbs');tabs.appendChild(b);}}
show('front');
</script></body></html>'''
open(f"{B}/exterior.html","w").write(page); print(len(page)/1e6,"MB")
