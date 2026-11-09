import sys
src = open(sys.argv[1], encoding='utf-8').read()
anchor = 'var $t=JSON.parse('
assert src.count(anchor) == 1
block = ('{const cs=ds.stone,fas=lt({color:15656662,roughness:.6}),cp=lt({color:15261647,roughness:.7});'
 # deep fascia beam along the carport front edge (carport span x 0-7.39, front z 29.38)
 'const fb=new ke(new jt(7.39,0.6,0.38),fas);fb.position.set(3.695,2.65-0.3,29.2);fb.castShadow=!0;ti.add(fb);'
 # three stone columns under the fascia
 'for(const x of [0.6,3.7,6.6]){const c=new ke(new jt(0.36,2.35,0.36),cs);c.position.set(x,1.175,29.0);c.castShadow=!0;ti.add(c)}'
 # low stone plinth under the carport front, reads as the lower wall in the reference
 'const pl=new ke(new jt(7.39,0.5,0.3),cp);pl.position.set(3.695,0.25,28.95);pl.castShadow=!0;ti.add(pl)}')
src = src.replace(anchor, block + anchor)
open(sys.argv[2], 'w', encoding='utf-8').write(src); print('written', len(src))
