import re, sys
src = open(sys.argv[1], encoding='utf-8').read()
def once(old, new):
    global src
    n = src.count(old); assert n == 1, (n, old[:70]); src = src.replace(old, new)
# A. context ground: flat grey plane -> warm gravel texture (same map as the paving material)
once('i=lt({color:13223613,roughness:1});', 'i=fs(lt({map:Ug,roughness:1,color:15132390}),200,200);')
# B. boundary walls: grey placeholder block -> stone texture, shadows on
once('c=ds[n.mat]||Fg;', 'c=ds[n.mat]||Fg;n.cat==="boundary"&&(c=fs(ds.stone,Math.max(r,o),a));')
# C. trees: lollipop (cylinder + sphere) -> date palms at the same CAD tree positions
loop = re.search(r'for\(let n of xn\.trees\)\{.*?tn\.add\(i\)\}', src, re.S)
assert loop and src.count(loop.group(0)) == 1
palm = '''if(!Ul.has("trees"))xn.trees.forEach((n,idx)=>{const PH=[7.2,6.6,7.8,6.9,7.4,6.5,7.6,7.0,7.9,6.8,7.3,7.7,6.9],H=PH[idx%PH.length],x=n.x,z=n.z;const trM=lt({color:9078664,roughness:.95}),fA=lt({color:4420402,roughness:.8,side:Jt}),fB=lt({color:6328638,roughness:.8,side:Jt});const tr=new ke(new fr(.13,.2,H,10),trM);tr.position.set(x,H/2,z);tr.castShadow=!0;tn.add(tr);const top=new U(x,H,z);for(let k=0;k<18;k++){const a=k/14*Math.PI*2+idx*.37,len=2.2+.6*((k%3)/2),up=k%2?.5:.9,dr=k%2?1.2:.9;const pts=[];for(let s=0;s<=6;s++){const t=s/6;pts.push(new U(top.x+Math.cos(a)*len*t,top.y+up*Math.sin(Math.PI*t*.5)*.9-dr*t*t*.9,top.z+Math.sin(a)*len*t))}for(let s=0;s<6;s++){const p=pts[s],q=pts[s+1],m=new ke(new jt(.2,.05,p.distanceTo(q)*1.02),k%2?fA:fB);m.position.set((p.x+q.x)/2,(p.y+q.y)/2,(p.z+q.z)/2);m.lookAt(q);m.castShadow=!0;tn.add(m)}}});'''
src = src.replace(loop.group(0), palm)
open(sys.argv[2], 'w', encoding='utf-8').write(src)
print('written', len(src))
