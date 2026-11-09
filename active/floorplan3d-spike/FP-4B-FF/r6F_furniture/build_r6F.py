# FF furniture from the approved V4 FP-4B-FF raster symbols (display coords on the 2x view of the 650x1000 embedded raster).
# crop px = display / 2 ; mm = (crop - wall origin) * 35.53 (same origin as r5L walls). Sizes derived from symbol extents.
import json, re, numpy as np, sys
sys.path.insert(0, '.')
MM = 35.53012869683798
keep = np.load('/tmp/claude-0/-home-user/afc66905-f2fa-5a30-bd08-01c638af991e/scratchpad/ff_wall_raster.npy')
ys, xs = np.nonzero(keep); X0, Y0 = int(xs.min()), int(ys.min())
# (room, type, name, status, display rect x1,y1,x2,y2)
ITEMS = [
 ('master-suite','bed','Bed','PLAN symbol, type ASSUMED',(305,455,480,630)),
 ('master-suite','nightstand','Nightstand N','ASSUMED: circle symbol at bed corner',(302,458,326,482)),
 ('master-suite','nightstand','Nightstand S','ASSUMED: circle symbol at bed corner',(302,600,326,624)),
 ('master-suite','armchair','Armchair','PLAN symbol, type ASSUMED',(468,412,520,460)),
 ('master-suite','sidetable','Side table','PLAN symbol (round), type ASSUMED',(428,414,458,444)),
 ('master-suite','vanity','Vanity','PLAN symbol (basin), type ASSUMED',(342,650,378,670)),
 ('family-living','cornersofa','L-sofa','PLAN symbol (L-shaped sofa)',(605,412,768,578)),
 ('family-living','coffeetable','Coffee table','PLAN symbol (round table)',(632,578,690,632)),
 ('family-living','cabinet','Sideboard','PLAN symbol (tall unit), type ASSUMED',(510,470,568,600)),
 ('family-living','cabinet','Wall unit','PLAN symbol (tall strip), type ASSUMED',(790,400,818,612)),
 ('bedroom-1','dresser','Dresser A','PLAN symbol (panel), type ASSUMED',(890,440,1015,495)),
 ('bedroom-1','dresser','Dresser B','PLAN symbol (panel), type ASSUMED',(890,550,1015,605)),
 ('bedroom-1','nightstand','Nightstand NE','ASSUMED: circle symbol in corner',(1000,418,1016,436)),
 ('bedroom-1','nightstand','Nightstand SE','ASSUMED: circle symbol in corner',(1000,603,1016,621)),
 ('bath-1','toilet','WC','PLAN symbol (WC)',(925,785,947,815)),
 ('bath-1','vanity','Basin','PLAN symbol (basin)',(852,797,898,828)),
 ('master-dressing','wardrobe','Wardrobe N','PLAN symbol (shelving), type ASSUMED',(300,695,428,738)),
 ('master-dressing','wardrobe','Wardrobe E','PLAN symbol (shelving), type ASSUMED',(414,740,430,870)),
 ('master-dressing','wardrobe','Wardrobe S','PLAN symbol (shelving), type ASSUMED',(300,870,430,905)),
 ('master-bath','toilet','WC','PLAN symbol (WC)',(318,940,336,966)),
 ('master-bath','bathtub','Bathtub','PLAN symbol (oval tub)',(378,1020,490,1064)),
 ('master-bath','vanity','Double vanity','PLAN symbol (twin basins), type ASSUMED',(512,930,534,1010)),
 ('bath-2','toilet','WC','PLAN symbol (WC), type ASSUMED',(395,1095,421,1132)),
 ('bath-2','vanity','Basin','PLAN symbol (basin)',(370,1200,410,1232)),
 ('dressing','wardrobe','Wardrobe','PLAN symbol (shelving), type ASSUMED',(425,1120,440,1220)),
 ('bedroom-2','bed','Bed','PLAN symbol (bed), type ASSUMED',(315,1310,480,1460)),
 ('bedroom-2','nightstand','Nightstand N','ASSUMED: circle symbol at bed corner',(312,1312,330,1330)),
 ('bedroom-2','nightstand','Nightstand S','ASSUMED: circle symbol at bed corner',(312,1446,330,1464)),
 ('bedroom-2','wardrobe','Wardrobe strip','PLAN symbol (strip), type ASSUMED',(510,1330,530,1420)),
 ('junior-suite','bed','Bed','PLAN symbol (bed), type ASSUMED',(850,1320,1010,1480)),
 ('junior-suite','nightstand','Nightstand NE','ASSUMED: circle symbol at bed corner',(998,1326,1014,1344)),
 ('junior-suite','nightstand','Nightstand SE','ASSUMED: circle symbol at bed corner',(998,1462,1014,1480)),
 ('junior-suite','wardrobe','Wardrobe strip','PLAN symbol (strip), type ASSUMED',(755,1320,790,1500)),
 ('junior-dressing','wardrobe','Wardrobe','PLAN symbol (shelving), type ASSUMED',(755,1120,870,1150)),
 ('junior-bath','vanity','Vanity','PLAN symbol (basin), type ASSUMED',(900,1120,1000,1146)),
 ('junior-bath','toilet','WC','PLAN symbol (WC)',(908,1235,928,1262)),
]
out = []; n = 0
for room, typ, name, status, (x1, y1, x2, y2) in ITEMS:
    cx = ((x1+x2)/4 - X0) * MM; cy = ((y1+y2)/4 - Y0) * MM
    w = (x2-x1)/2 * MM; d = (y2-y1)/2 * MM
    n += 1
    out.append({'id': f'ff-f{n:02d}', 'room': room, 'type': typ, 'name': name, 'status': status,
                'cx': round(cx), 'cy': round(cy), 'w': round(w), 'd': round(d), 'rot': 0})
plan = json.load(open('data/fp-4b-ff.plan.r5L.json'))['plan']
plan['FURNITURE'] = out
plan['LABEL'] = plan['LABEL'] + ' r6F: furniture from approved FF raster symbols (see r6F_furniture/furniture_r6F.json for PLAN vs ASSUMED per item).'
json.dump({'plan': plan, 'furniture_count': len(out)}, open('data/fp-4b-ff.plan.r6F.json', 'w'), indent=1)
hdr = open('data/fp-4b-ff.plan.r5L.js', encoding='utf-8').read().split('\n')
body = 'const PLAN = ' + json.dumps(plan, ensure_ascii=False) + ';\n'
rest = '\n'.join(hdr[2:])
rest = rest[rest.index('const R ='):] if 'const R =' in rest else rest
open('data/fp-4b-ff.plan.r6F.js', 'w', encoding='utf-8').write(
 '/* Generated (r6F) for the 4B FF viewer: r5L walls + furniture from approved V4 raster symbols. Not survey-verified, not construction-ready, not certified CAD. */\n' + body + rest)
json.dump(out, open('r6F_furniture/furniture_r6F.json', 'w'), indent=1)
print('furniture', len(out), 'origin', X0, Y0, 'bbox mm', plan['WALL_BBOX_MM'])
