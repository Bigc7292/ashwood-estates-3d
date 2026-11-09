import sys
src = open(sys.argv[1], encoding='utf-8').read()
def once(old, new):
    global src
    n = src.count(old); assert n == 1, (n, old[:70]); src = src.replace(old, new)
# 1. date palms: fuller, wider leaflet fronds (replaces the thin v4 frond boxes)
once('for(let k=0;k<18;k++)', 'for(let k=0;k<22;k++)')
once('new jt(.2,.05,p.distanceTo(q)*1.02)', 'new jt(.3,.06,p.distanceTo(q)*1.02)')
# 2. sky: less saturated top colour
once('t.addColorStop(0,"#3f87bd")', 't.addColorStop(0,"#8fb1c9")')
# 3. RF massing (rf_wall, rf_roof): hidden in the front view (RF is NTS in the sources; grey volume has no image counterpart)
once('for(let n of xn.boxes){if(Ul.has(n.cat))continue;', 'for(let n of xn.boxes){if(Ul.has(n.cat)||n.cat==="rf_wall"||n.cat==="rf_roof")continue;')
# 4. carport canopy: warm lit soffit instead of a plain grey slab
once('c=ds[n.mat]||Fg;', 'c=ds[n.mat]||Fg;n.cat==="canopy"&&(c=lt({color:15656662,roughness:.6,emissive:16766112,emissiveIntensity:.35}));')
# 5. planting: hedge row along the inside of the front boundary
once('var $t=JSON.parse(', '{const hm=lt({color:5216309,roughness:1});for(let x=0.6;x<18.2;x+=0.9){const b=new ke(new jt(0.8,1.0,0.8),hm);b.position.set(x,0.5,28.9);b.castShadow=!0;ti.add(b)}}var $t=JSON.parse(')
open(sys.argv[2], 'w', encoding='utf-8').write(src); print('written', len(src))
