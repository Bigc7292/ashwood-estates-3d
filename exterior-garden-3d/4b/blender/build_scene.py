"""Ashwood 4B exterior — Colin 7-step pipeline, steps 2-4, headless Blender 4.2 (free/local).
Usage: blender -b -P build_scene.py -- <stage> <out.blend>
stage in: layout | boxes | space | models | materials | grime   (cumulative)
Coordinates: Blender X = plan x (m), Blender Y = -plan z (m; street at Y=-29.88, rear plot edge Y=0), Z up.
Footprint numbers = approved CAD V4 + 4B-GF calibration (via ../model/data/model.json, ~ ±3 %).
Appearance (heights, finishes, render-only elements) = approved generated images + brochure p25/p26.
"""
import bpy, bmesh, json, math, random, sys
from mathutils import Vector
argv = sys.argv[sys.argv.index('--')+1:]
STAGE, OUT = argv[0], argv[1]
ORDER = ['layout','boxes','space','models','materials','grime']
LV = ORDER.index(STAGE)
random.seed(4)
M = json.load(open('/workspace/exterior-garden-3d/4b/model/data/model.json'))
SITE_W, SITE_D = M['meta']['site_m']
TREES = M['trees']
REG = []   # element register -> json

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# ---------------- heights (image-read appearance; NOT in CAD) ----------------
H = dict(gf_ffl=0.45, gf_clear=3.5, slab=0.50, ff_clear=3.3, roof=0.70, rf_core=3.0, canopy=0.35,
         side_wall=2.2, front_wall=1.3, gate=1.9, carport_top=3.45, carport_th=0.35, fin_top=11.6, balustrade=1.1, parapet=1.2)
GF0 = H['gf_ffl']; GF1 = GF0 + H['gf_clear']; FF0 = GF1 + H['slab']; FF1 = FF0 + H['ff_clear']; RF0 = FF1 + H['roof']; RF1 = RF0 + H['rf_core']

COLL = {}
def coll(name):
    if name not in COLL:
        c = bpy.data.collections.new(name); sc.collection.children.link(c); COLL[name] = c
    return COLL[name]

MATS = {}
def clay(name, rgb):
    m = bpy.data.materials.new('CLAY_'+name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = .8; m.diffuse_color = (*rgb, 1)
    return m
CLAY = {}
def mat(key):
    """stage < materials -> clay; else real procedural material (built lazily)."""
    if LV < ORDER.index('materials'):
        tint = {'stone':(.72,.72,.72),'glass':(.35,.42,.48),'water':(.35,.6,.7),'lawn':(.45,.6,.4),'foliage':(.4,.55,.38),'paving':(.82,.82,.8),
                'bronze':(.3,.28,.26),'soffit':(.9,.9,.88),'placeholder':(.6,.6,.6)}.get(MATCLASS.get(key,'stone'),(.75,.75,.75))
        if key not in CLAY: CLAY[key] = clay(key, tint)
        return CLAY[key]
    if key not in MATS: MATS[key] = bpy.data.materials.new('PENDING_'+key)
    return MATS[key]
MATCLASS = {}

def add_mesh(name, verts, faces, matkey, cname, src, mods=None):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    ob = bpy.data.objects.new(name, me); coll(cname).objects.link(ob)
    ob.data.materials.append(mat(matkey))
    for p in me.polygons: p.use_smooth = False
    REG.append(dict(name=name, collection=cname, material=matkey, source=src))
    return ob

def box(name, x0, x1, z0, z1, h0, h1, matkey, cname, src, bevel=0.0):
    """plan box: x0..x1 (plan x), z0..z1 (plan z, toward street), h0..h1 height."""
    X0,X1 = min(x0,x1),max(x0,x1); Y0,Y1 = -max(z0,z1), -min(z0,z1); Z0,Z1 = min(h0,h1),max(h0,h1)
    e = 0.0008*(len(REG)%7)  # anti-coplanar jitter (<6 mm) so overlapping faces don't self-shadow black
    X0,X1,Y0,Y1,Z0,Z1 = X0-e,X1+e,Y0-e,Y1+e,Z0-e*(Z0>0.01),Z1+e
    v = [(X0,Y0,Z0),(X1,Y0,Z0),(X1,Y1,Z0),(X0,Y1,Z0),(X0,Y0,Z1),(X1,Y0,Z1),(X1,Y1,Z1),(X0,Y1,Z1)]
    f = [(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    ob = add_mesh(name, v, f, matkey, cname, src)
    if bevel and LV >= ORDER.index('models'):
        md = ob.modifiers.new('bev','BEVEL'); md.width = bevel; md.segments = 2; md.limit_method = 'ANGLE'
    return ob

# ============================ STEP 2: LAYOUT (zones read from images, CAD-checked) ============================
LAYOUT = []
def zone(name, x0,x1,z0,z1, kind, img, cad):
    LAYOUT.append(dict(zone=name, x=[round(x0,2),round(x1,2)], z=[round(z0,2),round(z1,2)], kind=kind, image_ref=img, cad_check=cad))
# CAD-derived footprints (m)
GF_X0, GF_X1 = 3.13, 15.78; GF_Z0, GF_Z1 = 4.76, 26.79          # V4 GF floor polygon 195..551 x 188..808 crop px
GF_FRONT_LEFT_Z = 23.6; MP_X0 = 10.77                              # polygon notch (196,723)/(410,713) & multipurpose block (410..551, ..808)
FF_X0, FF_X1, FF_Z0, FF_ZF = 2.92, 15.88, 2.93, 24.0              # FF V4 envelope ~13.1 x ~23.9 (mapped to GF frame)
CY_X0, CY_X1, CY_Z0, CY_Z1 = 11.48, 15.78, 12.65, 16.34          # courtyard = GF water feature rect (V4 430..547 x 410..514); FF void snapped to it
CY_TERR_Z0 = 11.50                                                 # covered OUTDOOR TERRACE strip (V4 label 496,359; GF wall at z 11.51)
CY_OPEN_Z0, CY_OPEN_Z1 = 14.05, 16.34                              # CAD gap in GF right wall (traced poche)
POOL = [w for w in M['water'] if w['id']=='swimming-pool'][0]      # 9.50 x 2.40 (CAD transcript, calibrated)
PX0,PX1,PZ0,PZ1 = POOL['x0'],POOL['x1'],POOL['z0'],POOL['z1']
CARPORT = (0.0, 7.6, 23.6, 29.6)                                   # V4 vehicle entry zone 107..315 crop px (+ gate tick 315)
GATE = (7.6, 10.77); SERVICE_GATE = (16.8, 18.4)                   # V4 PEDESTRIAN / SERVICE ENTRY labels
zone('plot (CAD site diagram, not survey)',0,SITE_W,0,SITE_D,'plot','OUTDOOR-SITE','V4 ~18.7 x ~29.9 m')
zone('GF footprint',GF_X0,GF_X1,GF_Z0,GF_Z1,'building','OUTDOOR-SITE / ELEV-*','V4 GF floor polygon')
zone('FF envelope',FF_X0,FF_X1,FF_Z0,FF_ZF,'building','ELEV-REAR / ELEV-FRONT','FF V4 envelope ~13.1 x ~23.9 m')
zone('courtyard (open to sky, open on plan-right 14.05-16.34)',CY_X0,CY_X1,CY_Z0,CY_Z1,'outdoor','OUTDOOR-COURTYARD / ELEV-RIGHT','V4 water feature rect + GF wall gap')
zone('covered outdoor terrace',CY_X0,CY_X1,CY_TERR_Z0,CY_Z0,'outdoor','OUTDOOR-COURTYARD','V4 OUTDOOR TERRACE label')
zone('pool 9.50 x 2.40',PX0,PX1,PZ0,PZ1,'water','POOL / ELEV-REAR','CAD transcript + calibration span')
zone('raised rear deck +0.45 (pool terrace)',2.9,15.9,0.87,GF_Z0,'outdoor','ELEV-REAR / POOL / GARDEN-BACK','V4 TERRACE label; deck height image-read')
zone('carport / driveway',*CARPORT,'outdoor','ELEV-FRONT / GARDEN-FRONT','V4 2 car symbols + VEHICLE ENTRY')
zone('pedestrian entry path',GATE[0],GATE[1],23.6,SITE_D,'outdoor','ELEV-FRONT / GARDEN-FRONT','V4 PEDESTRIAN ENTRY')
zone('front planted bed',9.73,15.42,27.71,29.74,'planting','GARDEN-FRONT','V4 lawn rect 381,834,160,57')
for i,l in enumerate([b for b in M['boxes'] if b['cat']=='lawn']):
    zone(f'side/rear planted strip {i+1}',l['x0'],l['x1'],l['z0'],l['z1'],'planting','OUTDOOR-SITE / ELEV-LEFT / ELEV-RIGHT','V4 Source landscape rect')
zone('off-plot context lawn (render p26 / ELEV-REAR) — NOT PLOT',-6,SITE_W+6,-14,0,'context','ELEV-REAR / GARDEN-BACK','outside CAD plot; appearance only')
zone('RF core (enclosed stair/MEP; RF NTS)',3.01,10.94,9.95,22.5,'building','OUTDOOR-ROOF-TERRACE','RF plan NTS, board-offset placement')
zone('RF terrace',3.01,15.6,4.6,9.95,'outdoor','OUTDOOR-ROOF-TERRACE','RF TERRACE label (extent unknown)')

if LV == 0:
    zc = {'plot':(.9,.88,.82),'building':(.6,.6,.62),'outdoor':(.85,.78,.6),'water':(.4,.7,.85),'planting':(.45,.65,.4),'context':(.7,.8,.65)}
    for i,zd in enumerate(LAYOUT):
        MATCLASS[f'zone_{zd["kind"]}']='paving'
        m = CLAY.get(zd['kind']) or clay(zd['kind'], zc[zd['kind']]); CLAY[zd['kind']] = m
        x0,x1 = zd['x']; z0,z1 = zd['z']; e = 0.002*i + (0.05 if zd['kind'] in ('water','planting') else 0)
        ob = add_mesh('ZONE_'+zd['zone'][:40], [(x0,-z1,e),(x1,-z1,e),(x1,-z0,e),(x0,-z0,e)], [(0,1,2,3)], 'x', 'layout', 'layout')
        ob.data.materials.clear(); ob.data.materials.append(m)

# ============================ STEP 3a: BOXES (massing, proportions fixed here) ============================
if LV >= ORDER.index('boxes'):
    for k,v in dict(stone='stone',stone_rf='stone',glass='glass',water='water',lawn='lawn',hedge='foliage',paving='paving',deck='paving',
                    bronze='bronze',soffit='soffit',coping='paving',pooltile='water',leaf='foliage',palmleaf='foliage',bark='bronze',render='soffit',
                    led='soffit',ground='paving',furniture='placeholder',cushion='soffit',context_lawn='lawn',planter_soil='foliage',interior='glass').items(): MATCLASS[k]=v
    C='massing'
    box('CONTEXT_ground (neutral, outside plot)', -80,100, -60,90, -0.30,-0.16,'ground','context','neutral context ground so views have a horizon; not a site claim')
    # GF (solid volumes; courtyard left open)
    box('GF_rear', GF_X0,GF_X1, GF_Z0,CY_TERR_Z0, GF0,GF1,'stone',C,'CAD GF footprint; height image-read')
    box('GF_mid', GF_X0,CY_X0, CY_TERR_Z0,CY_Z1, GF0,GF1,'stone',C,'CAD GF footprint')
    box('GF_front', GF_X0,GF_X1, CY_Z1,GF_FRONT_LEFT_Z, GF0,GF1,'stone',C,'CAD GF footprint')
    box('GF_multipurpose', MP_X0,GF_X1, GF_FRONT_LEFT_Z,GF_Z1, GF0,GF1,'stone',C,'CAD V4 multipurpose block 410..551 x ..808')
    box('GF_plinth', GF_X0-0.05,GF_X1+0.05, GF_Z0,GF_Z1, 0,GF0,'stone',C,'image: raised plinth/steps (p25/p26); CAD footprint')
    # slab GF->FF and FF volume (courtyard void snapped to GF courtyard)
    for nm,(a,b,c,d) in dict(r=(FF_X0,FF_X1,FF_Z0,CY_TERR_Z0), m=(FF_X0,CY_X0,CY_TERR_Z0,CY_Z1), t=(CY_X0,FF_X1,CY_TERR_Z0,CY_Z0), f=(FF_X0,FF_X1,CY_Z1,FF_ZF+0.0)).items():
        box(f'SLAB_FF_{nm}', a,b,c,d, GF1,FF0,'soffit',C,'FF V4 envelope; slab thickness image-read', bevel=0.01)
    box('SLAB_FF_front_ext', FF_X0, GF_X1, FF_ZF, GF_Z1, GF1,FF0,'soffit',C,'GF front roof under FF balconies (CAD)')
    box('FF_rear', FF_X0+0.0,FF_X1, GF_Z0,CY_Z0, FF0,FF1,'stone',C,'FF V4 envelope (rear balcony 2.93..4.76 open)')
    box('FF_mid', FF_X0,CY_X0, CY_Z0,CY_Z1, FF0,FF1,'stone',C,'FF V4 envelope beside courtyard void')
    box('FF_front', FF_X0,FF_X1, CY_Z1,FF_ZF-0.6, FF0,FF1,'stone',C,'FF V4 envelope; front recess for slat screen (image ELEV-FRONT)')
    box('FF_front_left_bedroom', FF_X0,7.3, FF_ZF-0.6,FF_ZF, FF0,FF1,'stone',C,'FF V4 bedroom 2 front')
    box('FF_front_right_suite', 11.0,FF_X1, FF_ZF-0.6,FF_ZF, FF0,FF1,'stone',C,'FF V4 junior suite front')
    # roof slab with deep overhang (image p25/p26) minus courtyard void
    OVR, OVF = 1.0, 1.2
    for nm,(a,b,c,d) in dict(r=(FF_X0-0.3,FF_X1+0.12,FF_Z0-OVR,CY_Z0), m=(FF_X0-0.3,CY_X0,CY_Z0,CY_Z1), f=(FF_X0-0.3,11.0,CY_Z1,FF_ZF+OVF), fr=(11.0,FF_X1+0.12,CY_Z1,FF_ZF)).items():
        box(f'ROOF_{nm}', a,b,c,d, FF1,RF0,'soffit',C,'FF envelope + overhang read from ELEV-REAR/ELEV-FRONT (overhang not in CAD)', bevel=0.01)
    # RF core (enclosed stair per CAD RF plan) + lift
    box('RF_core', 3.01,10.94, 9.95,22.5, RF0,RF1,'stone_rf',C,'RF plan (NTS) core incl. enclosed stair — CAD wins over open-stair image')
    box('RF_lift', 10.6,12.3, 9.95,11.9, RF0,RF1,'stone_rf',C,'RF plan lift (NTS)')
    box('RF_canopy', 3.3,12.0, 3.4,10.3, RF1,RF1+H['canopy'],'soffit',C,'image ELEV-REAR/ROOF-TERRACE + p26: floating canopy; extent read from image', bevel=0.01)
    # render-sourced: carport + stone pier + tall stone fin
    cx0,cx1,cz0,cz1 = CARPORT
    box('CARPORT_canopy (render-sourced, not on plan)', cx0+0.05,cx1, GF_FRONT_LEFT_Z,cz1-0.3, H['carport_top']-H['carport_th'],H['carport_top'],'soffit',C,'RENDER-SOURCED p25 + EXT-4b-ELEV-FRONT/GARDEN-FRONT; footprint = CAD parking zone', bevel=0.01)
    box('CARPORT_pier (render-sourced)', cx1-0.6,cx1, cz1-0.9,cz1-0.3, 0,H['carport_top']-H['carport_th'],'stone',C,'RENDER-SOURCED p25/ELEV-FRONT: stone pier at gate side')
    box('STONE_FIN (render-sourced, not on plan)', 15.38,15.88, 19.0,GF_Z1+0.06, GF0,H['fin_top'],'stone',C,'RENDER-SOURCED p25/ELEV-FRONT: tall stone blade at front-right')
    # boundary walls: sides tall stone (image), front low stone + gates (image p25)
    box('WALL_side_left', -0.25,0, 0,SITE_D, 0,H['side_wall'],'stone',C,'image OUTDOOR-SITE/ELEV-LEFT; line = CAD site diagram (not survey)')
    box('WALL_side_right', SITE_W,SITE_W+0.25, 0,SITE_D, 0,H['side_wall'],'stone',C,'image OUTDOOR-SITE/ELEV-RIGHT; CAD site line')
    box('WALL_front_right', MP_X0,SERVICE_GATE[0], SITE_D-0.3,SITE_D, 0,H['front_wall'],'stone',C,'image p25/ELEV-FRONT low stone wall')
    box('WALL_front_end', SERVICE_GATE[1],SITE_W, SITE_D-0.3,SITE_D, 0,H['front_wall'],'stone',C,'image')
    box('WALL_carport_back_left', 0.0,0.35, GF_FRONT_LEFT_Z,SITE_D, 0,H['carport_top']-H['carport_th'],'stone',C,'image ELEV-FRONT: carport left stone wall')

# ============================ STEP 3b: SPACE (ground, plot, deck, pool basin, paths, context) ============================
if LV >= ORDER.index('space'):
    C='space'
    box('GROUND_paving_plot', 0,SITE_W, 0,SITE_D, -0.10,0.0,'paving',C,'CAD site hardscape')
    box('GROUND_street_verge', -6,SITE_W+6, SITE_D,SITE_D+6, -0.15,-0.02,'paving',C,'image ELEV-FRONT street edge (context, outside plot)')
    box('CONTEXT_lawn_beyond_plot (NOT PLOT)', -6,SITE_W+6, -14,0, -0.12,-0.01,'context_lawn',C,'image ELEV-REAR/GARDEN-BACK + p26 lawn; outside CAD plot (CAD wins on plot depth)')
    for l in [b for b in M['boxes'] if b['cat']=='lawn']:
        box(l['id'].upper()+'_bed', l['x0'],l['x1'],l['z0'],l['z1'], 0,0.05,'lawn',C,'CAD V4 Source landscape rect')
    # raised rear deck at GF FFL with pool cut (pool 9.50 x 2.40 CAD); coping 0.30
    cp = 0.30; DZ0 = PZ0-cp
    box('DECK_rear_strip', 2.9,15.9, PZ1+cp,GF_Z0, 0,GF0,'deck',C,'image: raised deck; CAD z between pool & facade')
    box('DECK_left_of_pool', 2.9,PX0-cp, DZ0,PZ1+cp, 0,GF0,'deck',C,'image deck; CAD pool x')
    box('DECK_terrace_right', PX1+cp,15.9, PZ0+0.0,PZ1+cp, 0,GF0,'deck',C,'CAD TERRACE label zone; image lounge deck')
    for nm,(a,b,c,d) in dict(n=(PX0-cp,PX1+cp,DZ0,PZ0), s=(PX0-cp,PX1+cp,PZ1,PZ1+cp), w=(PX0-cp,PX0,PZ0,PZ1), e=(PX1,PX1+cp,PZ0,PZ1)).items():
        box(f'POOL_coping_{nm}', a,b,c,d, 0,GF0+0.03,'coping',C,'coping width assumed 0.30; raised pool edge per p26/ELEV-REAR', bevel=0.01)
    box('POOL_floor', PX0,PX1, PZ0,PZ1, -1.25,-1.2,'pooltile',C,'depth NOT in source (display 1.6 m)')
    for nm,(a,b,c,d) in dict(n=(PX0,PX1,PZ0,PZ0+0.02), s=(PX0,PX1,PZ1-0.02,PZ1), w=(PX0,PX0+0.02,PZ0,PZ1), e=(PX1-0.02,PX1,PZ0,PZ1)).items():
        box(f'POOL_wall_{nm}', a,b,c,d, -1.2,GF0,'pooltile',C,'pool shell display')
    wo = add_mesh('POOL_water (CAD 9.50 x 2.40)', [(PX0,-PZ1,GF0-0.06),(PX1,-PZ1,GF0-0.06),(PX1,-PZ0,GF0-0.06),(PX0,-PZ0,GF0-0.06)], [(0,1,2,3)], 'water', C, 'CAD 9.50 x 2.40')
    # steps from deck down to lawn (image ELEV-REAR: wide steps at plan-right end)
    for i in range(3):
        box(f'DECK_step_{i}', PX1+cp,15.9, PZ0-0.0-(i+1)*0.32, PZ0-i*0.32, 0, GF0-(i+1)*0.15+0.15 - 0.15, 'deck', C, 'image ELEV-REAR/p26 steps (3 risers 0.15 read from image)')
    # courtyard: water feature + planter island at GF FFL
    isl = M['boxes'][[b['id'] for b in M['boxes']].index('courtyard-planter-island')]
    box('COURTYARD_floor', CY_X0,CY_X1, CY_TERR_Z0,CY_Z1, 0,GF0-0.25,'deck',C,'CAD courtyard')
    box('COURTYARD_terrace_paving', CY_X0,CY_X1, CY_TERR_Z0,CY_Z0, GF0-0.25,GF0,'deck',C,'CAD OUTDOOR TERRACE strip')
    add_mesh('COURTYARD_water (CAD)', [(CY_X0,-CY_Z1,GF0-0.12),(CY_X1,-CY_Z1,GF0-0.12),(CY_X1,-CY_Z0,GF0-0.12),(CY_X0,-CY_Z0,GF0-0.12)], [(0,1,2,3)], 'water', C, 'CAD water feature')
    box('COURTYARD_planter_island', isl['x0'],isl['x1'],isl['z0'],isl['z1'], 0,GF0+0.15,'coping',C,'CAD island; height image-read', bevel=0.01)
    box('COURTYARD_wall_right_closed', GF_X1-0.3,GF_X1, CY_TERR_Z0,CY_OPEN_Z0, GF0,GF1,'stone',C,'CAD GF right wall line z 11.5..14.05')
    for i in range(3):   # open side steps down to side path (image ELEV-RIGHT)
        box(f'COURTYARD_side_step_{i}', GF_X1+i*0.3,GF_X1+(i+1)*0.3, CY_OPEN_Z0,CY_OPEN_Z1, 0,GF0-(i+1)*0.15,'deck',C,'image ELEV-RIGHT: steps at courtyard opening; CAD open gap')
    # entry path + steps
    box('ENTRY_path', GATE[0]+0.2,GATE[1]-0.2, GF_FRONT_LEFT_Z,SITE_D-0.3, 0,0.02,'deck',C,'CAD PEDESTRIAN ENTRY; image paving')
    for i in range(3):
        box(f'ENTRY_step_{i}', GATE[0]+0.2,GATE[1]-0.2, GF_FRONT_LEFT_Z+i*0.35,GF_FRONT_LEFT_Z+(i+1)*0.35, 0,GF0-i*0.15,'deck',C,'image ELEV-FRONT steps')
    box('DRIVEWAY', CARPORT[0]+0.35,CARPORT[1], GF_FRONT_LEFT_Z,SITE_D, 0,0.015,'paving',C,'CAD parking zone')

# ============================ STEP 3c: MODELS (openings, glazing, screens, balustrades, gates, planting, furniture) ============================
def glass_x(name, x, z0, z1, h0, h1, src, out=1):   # pane on a face normal to x
    box(name, x-0.03*out, x+0.03*out, z0, z1, h0, h1, 'glass','models',src)
def glass_z(name, z, x0, x1, h0, h1, src, out=1):
    box(name, x0, x1, z-0.03*out, z+0.03*out, h0, h1, 'glass','models',src)
def mullions_z(prefix, z, x0, x1, h0, h1, n, src):
    for i in range(n+1):
        x = x0 + (x1-x0)*i/n
        box(f'{prefix}_m{i}', x-0.035,x+0.035, z-0.05,z+0.05, h0,h1,'bronze','models',src)
    box(f'{prefix}_head', x0,x1, z-0.05,z+0.05, h1-0.06,h1,'bronze','models',src); box(f'{prefix}_sill', x0,x1, z-0.05,z+0.05, h0,h0+0.05,'bronze','models',src)
def mullions_x(prefix, x, z0, z1, h0, h1, n, src):
    for i in range(n+1):
        z = z0 + (z1-z0)*i/n
        box(f'{prefix}_m{i}', x-0.05,x+0.05, z-0.035,z+0.035, h0,h1,'bronze','models',src)
    box(f'{prefix}_head', x-0.05,x+0.05, z0,z1, h1-0.06,h1,'bronze','models',src)

def palm(name, x, z, ht, src):
    C='planting'
    bm = bmesh.new(); seg=10; rings=8
    for r in range(rings+1):
        t=r/rings; rad=0.22*(1-t)+0.14*t; zz=ht*t; lean=0.35*t*t
        for s in range(seg):
            a=2*math.pi*s/seg; bm.verts.new((x+lean+rad*math.cos(a), -z+rad*math.sin(a), zz))
    bm.verts.ensure_lookup_table()
    for r in range(rings):
        for s in range(seg):
            a=r*seg+s; b=r*seg+(s+1)%seg; bm.faces.new((bm.verts[a],bm.verts[b],bm.verts[b+seg],bm.verts[a+seg]))
    me=bpy.data.meshes.new(name+'_trunk'); bm.to_mesh(me); bm.free()
    ob=bpy.data.objects.new(name+'_trunk',me); coll(C).objects.link(ob); ob.data.materials.append(mat('bark'))
    for p in me.polygons: p.use_smooth=True
    top=(x+0.35, -z, ht); fv=[]; ff=[]
    nf=18
    for k in range(nf):
        a=2*math.pi*k/nf+random.uniform(-.15,.15); L=random.uniform(2.6,3.4); droop=random.uniform(0.55,1.0); up=random.uniform(0.2,0.6)
        base=len(fv); ns=8
        for i in range(ns+1):
            t=i/ns; w=0.55*math.sin(math.pi*min(t*1.1,1))+0.05
            d=L*t; hz=top[2]+up*t*2.2-droop*(t**2)*2.4
            cx=top[0]+d*math.cos(a); cy=top[1]+d*math.sin(a)
            px,py=-math.sin(a)*w/2, math.cos(a)*w/2
            fv += [(cx-px,cy-py,hz-0.08*w),(cx+px,cy+py,hz-0.08*w),(cx,cy,hz+0.05)]
        for i in range(ns):
            o=base+i*3; ff += [(o,o+2,o+5,o+3),(o+2,o+1,o+4,o+5)]
    ob2=add_mesh(name+'_fronds', fv, ff, 'palmleaf', C, src)
    for p in ob2.data.polygons: p.use_smooth=True
    REG.append(dict(name=name, collection=C, material='bark/palmleaf', source=src))

def broadleaf(name, x, z, r, ht, src, matkey='leaf', pine=False):
    C='planting'
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.13 if not pine else 0.09, depth=ht, location=(x,-z,ht/2+ (GF0 if pine else 0)))
    t=bpy.context.object; t.name=name+'_trunk'; bpy.context.collection.objects.unlink(t) if t.name in bpy.context.collection.objects else None; coll(C).objects.link(t) if t.name not in coll(C).objects else None
    t.data.materials.append(mat('bark'))
    blobs = 4 if pine else 6
    for k in range(blobs):
        if pine:
            ox,oy,oz,s = random.uniform(-.6,.6), random.uniform(-.6,.6), ht*0.55+k*0.45, (0.9-0.12*k, 0.9-0.12*k, 0.28)
        else:
            ox,oy,oz = random.uniform(-.45,.45)*r, random.uniform(-.45,.45)*r, ht+random.uniform(-.1,.5)*r
            ss=random.uniform(.55,.8)*r; s=(ss,ss,ss*0.85)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1, location=(x+ox,-z+oy,oz+(GF0 if pine else 0)))
        b=bpy.context.object; b.name=f'{name}_canopy{k}'; b.scale=s
        if b.name in bpy.context.collection.objects: bpy.context.collection.objects.unlink(b)
        coll(C).objects.link(b); b.data.materials.append(mat(matkey))
        if LV >= ORDER.index('models'):
            tx=bpy.data.textures.get('leafclouds') or bpy.data.textures.new('leafclouds','CLOUDS'); tx.noise_scale=0.35
            d=b.modifiers.new('disp','DISPLACE'); d.texture=tx; d.strength=0.35*min(s); d.mid_level=0.5
        for p in b.data.polygons: p.use_smooth=True
    REG.append(dict(name=name, collection=C, material=matkey, source=src))

def hedge(name, x0,x1,z0,z1,h,src):
    ob=box(name, x0,x1,z0,z1, 0.05,h,'hedge','planting',src)
    if LV >= ORDER.index('models'):
        s=ob.modifiers.new('sub','SUBSURF'); s.subdivision_type='SIMPLE'; s.levels=3; s.render_levels=4
        tx=bpy.data.textures.get('hedgeclouds') or bpy.data.textures.new('hedgeclouds','CLOUDS'); tx.noise_scale=0.25
        d=ob.modifiers.new('disp','DISPLACE'); d.texture=tx; d.strength=0.18

if LV >= ORDER.index('models'):
    C='models'
    # --- GF rear: full-height glazing (p26/ELEV-REAR), stone end piers
    gz = GF_Z0
    glass_z('GF_rear_glazing', gz-0.02, 3.6, 12.7, GF0, GF1, 'image p26/ELEV-REAR full-height glazing; CAD WINS 1777..9238')
    mullions_z('GF_rear_frame', gz-0.06, 3.6, 12.7, GF0, GF1, 4, 'image bronze frames')
    glass_z('GF_rear_glazing_terrace', gz-0.02, 13.4, 15.2, GF0, GF1, 'CAD WINS 11228..13608 cue')
    mullions_z('GF_rear_frame_t', gz-0.06, 13.4, 15.2, GF0, GF1, 1, 'image')
    # --- GF side windows from CAD glazing cues (WINS) — positions CAD, height image
    for b in [b for b in M['boxes'] if b['cat']=='gf_glass']:
        w=b['x1']-b['x0']; d=b['z1']-b['z0']
        if b['x0']<3.6 and d>0.5: glass_x(f'GF_win_L_{b["id"]}', GF_X0-0.02, b['z0'], b['z1'], GF0+0.0, GF1-0.4, 'CAD GF glazing cue (left side)', out=1)
        elif b['x1']>15.3 and d>0.5: glass_x(f'GF_win_R_{b["id"]}', GF_X1+0.02, b['z0'], b['z1'], GF0, GF1-0.4, 'CAD GF glazing cue (right side)')
    # courtyard glazing (image OUTDOOR-COURTYARD: glass walls to interior on 2 sides)
    glass_x('CY_glazing_west', CY_X0-0.02, CY_Z0+0.1, CY_Z1-0.1, GF0, GF1-0.1, 'image OUTDOOR-COURTYARD; CAD courtyard edge', out=-1)
    mullions_x('CY_frame_west', CY_X0-0.06, CY_Z0+0.1, CY_Z1-0.1, GF0, GF1-0.1, 3, 'image')
    glass_z('CY_glazing_south', CY_Z1+0.02, CY_X0+0.1, GF_X1-0.4, GF0, GF1-0.1, 'image OUTDOOR-COURTYARD (office/gym side)', out=-1)
    # GF front: entry glazing + timber door (ELEV-FRONT), multipurpose glazing
    glass_z('GF_entry_glazing', GF_FRONT_LEFT_Z+0.02, 7.7, 10.6, GF0, GF1, 'image ELEV-FRONT double-height entry')
    box('GF_entry_door_timber', 9.3,10.4, GF_FRONT_LEFT_Z+0.0,GF_FRONT_LEFT_Z+0.08, GF0,GF0+2.9,'bronze',C,'image ELEV-FRONT timber pivot door')
    glass_z('GF_carport_back_glazing', GF_FRONT_LEFT_Z+0.02, 3.6, 7.0, GF0+0.3, GF1-0.6, 'image ELEV-FRONT')
    glass_z('GF_multipurpose_win', GF_Z1+0.02, 12.0, 14.6, GF0+0.6, GF1-0.6, 'CAD WINS cue 13040..13821 / image')
    # --- FF rear: full-width glazing behind balcony + glass balustrade (p26)
    glass_z('FF_rear_glazing', GF_Z0-0.02, 3.4, 15.4, FF0, FF1, 'image p26/ELEV-REAR')
    mullions_z('FF_rear_frame', GF_Z0-0.06, 3.4, 15.4, FF0, FF1, 5, 'image')
    box('FF_balcony_slab', FF_X0,FF_X1, FF_Z0,GF_Z0, GF1,FF0,'soffit',C,'FF V4 BALCONY (extent traced)', bevel=0.01)
    box('FF_balcony_balustrade_glass', FF_X0+0.1,FF_X1-0.1, FF_Z0+0.05,FF_Z0+0.07, FF0,FF0+H['balustrade'],'glass',C,'image p26 frameless glass; height assumed')
    box('FF_rear_pier_left', FF_X0,FF_X0+0.45, FF_Z0,GF_Z0, FF0,FF1,'stone',C,'image p26 stone end pier')
    box('FF_rear_pier_right', FF_X1-0.45,FF_X1, FF_Z0,GF_Z0, FF0,FF1,'stone',C,'image p26 stone end pier')
    # --- FF front: slat screen box (ELEV-FRONT), bedroom/suite windows, front balconies
    z=FF_ZF-0.6
    for i in range(26):
        x=7.35+i*0.143
        box(f'FF_slat_{i}', x,x+0.06, z+0.55,z+0.65, GF1+0.2,FF1,'bronze',C,'image p25/ELEV-FRONT vertical bronze/timber slats; location CAD OPEN TO BELOW')
    for i in range(27):
        x=3.45+i*0.143
        box(f'FF_slat_L{i}', x,x+0.06, FF_ZF+0.10,FF_ZF+0.18, FF0,FF1,'bronze',C,'image ELEV-FRONT/GARDEN-FRONT: slat screen spans FF front-left in front of bedroom glazing (appearance from image)')
    box('FF_slat_frame_top', 7.3,11.0, z+0.5,z+0.7, FF1-0.15,FF1,'bronze',C,'image')
    glass_z('FF_front_left_glazing', FF_ZF+0.02, 3.4, 7.1, FF0, FF1, 'image ELEV-FRONT')
    box('FF_front_left_balcony', FF_X0,7.3, FF_ZF,FF_ZF+1.1, GF1,FF0,'soffit',C,'FF V4 front-left BALCONY (traced)')
    box('FF_front_left_balustrade', FF_X0,7.3, FF_ZF+1.05,FF_ZF+1.1, FF0,FF0+H['balustrade'],'glass',C,'image ELEV-FRONT glass/planter balustrade')
    box('FF_front_right_box_parapet', 11.0,FF_X1, GF_Z1-0.3,GF_Z1, FF0,FF0+H['parapet'],'stone',C,'image p25 stone box w/ planter; CAD front-right BALCONY')
    box('FF_front_right_side', 11.0,11.3, FF_ZF,GF_Z1, FF0,FF0+H['parapet'],'stone',C,'image')
    hedge('FF_front_right_planter', 11.3,15.3, GF_Z1-0.8,GF_Z1-0.3, FF0+1.6, 'image p25 planter on stone box')
    glass_z('FF_front_right_glazing', FF_ZF+0.02, 11.4, 15.3, FF0, FF1, 'image ELEV-FRONT')
    # --- FF side windows (image ELEV-LEFT/RIGHT: narrow vertical windows; positions image-read)
    for i,zc in enumerate([9.2, 13.5, 17.8]):
        glass_x(f'FF_win_left_{i}', FF_X0-0.02, zc-0.45, zc+0.45, FF0+0.4, FF1-0.2, 'image ELEV-LEFT narrow windows (positions image-read, not CAD)')
    glass_x('FF_win_right_0', FF_X1+0.02, 18.6, 19.4, FF0+0.4, FF1-0.2, 'image ELEV-RIGHT narrow window')
    glass_x('FF_win_right_court', CY_X0+0.0, CY_Z0+0.2, CY_Z1-0.2, FF0, FF1-0.1, 'image ELEV-RIGHT courtyard-facing glazing', out=-1)
    # --- RF: balustrade, door in core (enclosed stair), furniture (RF plan symbols + ROOF-TERRACE image)
    box('RF_balustrade_rear', 3.0,15.6, 4.55,4.6, RF0,RF0+H['balustrade'],'glass',C,'image ROOF-TERRACE glass balustrade; RF edge NTS')
    box('RF_balustrade_right', 15.55,15.6, 4.6,9.95, RF0,RF0+H['balustrade'],'glass',C,'image')
    glass_z('RF_core_door', 9.95-0.02, 8.4, 9.9, RF0, RF0+2.4, 'CAD RF stair inside core; door to terrace (image shows open stair — CAD wins)')
    box('RF_counter', 3.3,4.0, 5.0,9.6, RF0,RF0+0.95,'stone',C,'RF plan long counter + ROOF-TERRACE image', bevel=0.01)
    box('RF_table', 5.8,6.8, 5.6,8.6, RF0+0.72,RF0+0.77,'furniture',C,'RF plan dining (~8-10 seats)')
    box('RF_table_base', 6.1,6.5, 6.6,7.6, RF0,RF0+0.72,'furniture',C,'RF plan')
    for i in range(4):
        for sx in (5.35, 7.05):
            box(f'RF_chair_{i}_{sx}', sx,sx+0.45, 5.8+i*0.75,6.25+i*0.75, RF0,RF0+0.45,'furniture',C,'RF plan chairs (illustrative)')
            box(f'RF_chairback_{i}_{sx}', sx+(0 if sx<6 else 0.38),sx+(0.07 if sx<6 else 0.45), 5.8+i*0.75,6.25+i*0.75, RF0+0.45,RF0+0.85,'furniture',C,'RF plan')
    box('RF_sofa_long', 13.6,14.5, 5.2,9.4, RF0,RF0+0.42,'cushion',C,'RF plan L-sofa (illustrative)', bevel=0.05)
    box('RF_sofa_short', 11.0,13.6, 8.6,9.4, RF0,RF0+0.42,'cushion',C,'RF plan L-sofa', bevel=0.05)
    box('RF_sofa_back', 14.3,14.5, 5.2,9.4, RF0+0.42,RF0+0.8,'cushion',C,'RF plan', bevel=0.04)
    # --- pool-deck lounge (ELEV-REAR: sofa on terrace, plan-right)
    box('DECK_sofa', 13.2,15.4, 1.6,2.4, GF0,GF0+0.42,'cushion',C,'image ELEV-REAR / p26 outdoor sofa (illustrative)', bevel=0.05)
    box('DECK_sofa_back', 13.2,15.4, 2.25,2.4, GF0+0.42,GF0+0.8,'cushion',C,'image', bevel=0.04)
    # --- gates (bronze slatted, p25/ELEV-FRONT)
    for nm,(a,b) in dict(PED=GATE, SERVICE=SERVICE_GATE).items():
        n=int((b-a)/0.12)
        for i in range(n):
            x=a+i*(b-a)/n
            box(f'GATE_{nm}_bar{i}', x,x+0.05, SITE_D-0.2,SITE_D-0.1, 0.05,H['gate'],'bronze',C,'image p25/ELEV-FRONT slatted metal gate; position CAD entry label')
        box(f'GATE_{nm}_rail', a,b, SITE_D-0.22,SITE_D-0.08, H['gate']-0.06,H['gate'],'bronze',C,'image')
    # --- soffit LED lines (image: linear light at slab edges)
    box('LED_roof_rear', FF_X0-0.2,FF_X1, FF_Z0-0.9,FF_Z0-0.85, FF1-0.01,FF1,'led',C,'image ELEV-REAR soffit light line')
    box('LED_roof_front', FF_X0-0.2,11.0, FF_ZF+1.05,FF_ZF+1.1, FF1-0.01,FF1,'led',C,'image ELEV-FRONT soffit line')
    box('LED_carport', 0.4,7.4, 29.0,29.05, H['carport_top']-H['carport_th']-0.01,H['carport_top']-H['carport_th'],'led',C,'image ELEV-FRONT carport light line')
    # --- planting: CAD tree positions; species from images
    PALMS = {1,2,4,9}
    for i,t in enumerate(TREES):
        n=i+1
        if t.get('courtyard'): broadleaf(f'TREE_{n}_courtyard_pine', t['x'], t['z'], 1.0, 2.6, 'CAD tree symbol; species/form from image OUTDOOR-COURTYARD (pine/bonsai-like)', pine=True)
        elif n in PALMS: palm(f'TREE_{n}_palm', t['x'], t['z'], random.uniform(6.5,8.0), 'CAD tree symbol position; date palm per images p25/p26/OUTDOOR-SITE')
        else: broadleaf(f'TREE_{n}_broadleaf', t['x'], t['z'], max(t['r'],1.4), random.uniform(3.2,4.2), 'CAD tree symbol position; broadleaf per images OUTDOOR-SITE/ELEV-LEFT/RIGHT')
    for l in [b for b in M['boxes'] if b['cat']=='lawn']:   # hedges/shrubs along the outer edge of each planted strip (image OUTDOOR-SITE)
        w=l['x1']-l['x0']; d=l['z1']-l['z0']
        if d>w: 
            edge = (l['x0'], l['x0']+min(0.7,w*0.5)) if l['x0']<5 else (l['x1']-min(0.7,w*0.5), l['x1'])
            hedge(f'HEDGE_{l["id"]}', edge[0],edge[1], l['z0']+0.1,l['z1']-0.1, 1.5, 'image OUTDOOR-SITE hedges inside CAD planted strip')
        else:
            hedge(f'HEDGE_{l["id"]}', l['x0']+0.1,l['x1']-0.1, l['z0']+0.1,l['z0']+0.6 if l['z0']<10 else l['z1']-0.1, 0.9, 'image planting inside CAD strip')
    hedge('HEDGE_front_bed', 9.9,15.3, SITE_D-0.9,SITE_D-0.35, 0.8, 'image GARDEN-FRONT planted bed (CAD front lawn rect)')
    hedge('HEDGE_context_rear_left', -6,-0.3, -12,-0.3, 1.6, 'image ELEV-REAR hedges (off-plot context)')
    hedge('HEDGE_context_rear_right', SITE_W+0.3,SITE_W+6, -12,-0.3, 1.6, 'image ELEV-REAR hedges (off-plot context)')
    for k,(x,z) in enumerate([(-3,-6),(22,-5),(-4,-11),(23,-11)]):
        palm(f'CONTEXT_palm_{k}', x, z, random.uniform(7,8.5), 'image ELEV-REAR context palms (off-plot)')

# ============================ STEP 3d: MATERIALS + STEP 4: GRIME (procedural, Cycles) ============================
GRIME = LV >= ORDER.index('grime')
def nt(m): return m.node_tree.nodes, m.node_tree.links
def N(nodes, t, **kw):
    n = nodes.new(t)
    for k,v in kw.items():
        if k in n.inputs: n.inputs[k].default_value = v
        else: setattr(n, k.lower().replace(' ','_'), v)
    return n
def mixrgb(nodes, links, fac, a, b, blend='MIX'):
    m = nodes.new('ShaderNodeMix'); m.data_type='RGBA'; m.blend_type=blend
    for src,idx in ((fac,0),(a,6),(b,7)):
        if isinstance(src,(float,int)): m.inputs[idx].default_value = src
        elif isinstance(src,tuple): m.inputs[idx].default_value = src
        else: links.new(src, m.inputs[idx])
    return m.outputs[2]
def math_(nodes, links, op, a, b=None, clamp=False):
    m = nodes.new('ShaderNodeMath'); m.operation=op; m.use_clamp=clamp
    for src,idx in ((a,0),(b,1)):
        if src is None: continue
        if isinstance(src,(float,int)): m.inputs[idx].default_value=src
        else: links.new(src, m.inputs[idx])
    return m.outputs[0]
def ramp(nodes, links, fac, stops):
    r = nodes.new('ShaderNodeValToRGB'); e=r.color_ramp.elements
    e[0].position, e[0].color = stops[0][0], (*stops[0][1],1); e[1].position, e[1].color = stops[-1][0], (*stops[-1][1],1)
    for p,c in stops[1:-1]:
        el=e.new(p); el.color=(*c,1)
    links.new(fac, r.inputs['Fac']); return r.outputs['Color']
def base(name):
    m = bpy.data.materials.new(name); m.use_nodes=True; nodes,links = nt(m)
    bsdf = nodes['Principled BSDF']; co = N(nodes,'ShaderNodeTexCoord'); return m,nodes,links,bsdf,co.outputs['Object']

def apply_grime(nodes, links, bsdf, P, col, rough, kind):
    """STEP 4 procedural grime. kind: stone | render | metal | glass | paving"""
    sep = N(nodes,'ShaderNodeSeparateXYZ'); links.new(P, sep.inputs[0]); Z = sep.outputs['Z']
    geo = N(nodes,'ShaderNodeNewGeometry')
    nz = N(nodes,'ShaderNodeSeparateXYZ'); links.new(geo.outputs['Normal'], nz.inputs[0])
    # base dirt / splash-back: darker within ~0.6 m of ground and of each slab/deck level
    n1 = N(nodes,'ShaderNodeTexNoise', **{'Scale':3.0,'Detail':8.0,'Roughness':0.6}); links.new(P, n1.inputs['Vector'])
    zl = math_(nodes,links,'SUBTRACT', Z, 0.0)
    bd = math_(nodes,links,'SUBTRACT', 1.0, math_(nodes,links,'DIVIDE', zl, 0.75), clamp=True)
    bd = math_(nodes,links,'MULTIPLY', bd, math_(nodes,links,'ADD', n1.outputs['Fac'], 0.2), clamp=True)
    col = mixrgb(nodes,links, math_(nodes,links,'MULTIPLY', bd, 0.55), col, (0.28,0.22,0.16,1), 'MULTIPLY')
    if kind in ('stone','render','metal'):
        # drip / rain streaks below slab edges: vertically stretched noise, strongest just under each slab line (3.95, 7.65, 11.1)
        mp = N(nodes,'ShaderNodeMapping'); mp.inputs['Scale'].default_value=(14,14,0.6); links.new(P, mp.inputs['Vector'])
        sn = N(nodes,'ShaderNodeTexNoise', **{'Scale':4.0,'Detail':4.0}); links.new(mp.outputs[0], sn.inputs['Vector'])
        streak = math_(nodes,links,'POWER', sn.outputs['Fac'], 4.0)
        under = None
        for lvl in (3.95, 7.65, 11.1, 3.1):
            d = math_(nodes,links,'SUBTRACT', lvl, Z)
            u = math_(nodes,links,'MULTIPLY', math_(nodes,links,'GREATER_THAN', d, 0.0), math_(nodes,links,'SUBTRACT',1.0, math_(nodes,links,'DIVIDE', d, 1.6), clamp=True))
            under = u if under is None else math_(nodes,links,'MAXIMUM', under, u)
        dr = math_(nodes,links,'MULTIPLY', math_(nodes,links,'MULTIPLY', streak, under), 2.2, clamp=True)
        col = mixrgb(nodes,links, math_(nodes,links,'MULTIPLY', dr, 0.6), col, (0.42,0.36,0.28,1), 'MULTIPLY')
    # dust on up-facing surfaces
    up = math_(nodes,links,'GREATER_THAN', nz.outputs['Z'], 0.7)
    dn = N(nodes,'ShaderNodeTexNoise', **{'Scale':9.0,'Detail':10.0}); links.new(P, dn.inputs['Vector'])
    dust = math_(nodes,links,'MULTIPLY', up, math_(nodes,links,'MULTIPLY', dn.outputs['Fac'], 0.55), clamp=True)
    col = mixrgb(nodes,links, dust, col, (0.80,0.74,0.64,1))
    rough = math_(nodes,links,'ADD', rough, math_(nodes,links,'MULTIPLY', dust, 0.3), clamp=True)
    if kind in ('render','metal','stone'):
        # chipped paint / edge wear: bevel-normal vs true normal -> edge mask, broken up by noise
        bev = N(nodes,'ShaderNodeBevel'); bev.inputs['Radius'].default_value=0.03; bev.samples=8
        dot = N(nodes,'ShaderNodeVectorMath'); dot.operation='DOT_PRODUCT'; links.new(bev.outputs['Normal'], dot.inputs[0]); links.new(geo.outputs['Normal'], dot.inputs[1])
        edge = math_(nodes,links,'SUBTRACT', 1.0, dot.outputs['Value'])
        edge = math_(nodes,links,'MULTIPLY', edge, 25.0, clamp=True)
        cn = N(nodes,'ShaderNodeTexNoise', **{'Scale':18.0,'Detail':12.0,'Roughness':0.7}); links.new(P, cn.inputs['Vector'])
        chip = math_(nodes,links,'GREATER_THAN', math_(nodes,links,'MULTIPLY', edge, cn.outputs['Fac']), 0.42)
        sub = {'render':(0.55,0.53,0.5,1),'metal':(0.62,0.55,0.42,1),'stone':(0.82,0.76,0.66,1)}[kind]
        col = mixrgb(nodes,links, chip, col, sub)
    if kind=='metal':
        # oxidation / patina on bronze, more toward the bottom
        pn = N(nodes,'ShaderNodeTexNoise', **{'Scale':6.0,'Detail':6.0}); links.new(P, pn.inputs['Vector'])
        pat = math_(nodes,links,'MULTIPLY', math_(nodes,links,'POWER', pn.outputs['Fac'], 2.0), math_(nodes,links,'SUBTRACT',1.2, math_(nodes,links,'DIVIDE',Z,4.0), clamp=True))
        col = mixrgb(nodes,links, math_(nodes,links,'MULTIPLY', pat, 0.6), col, (0.30,0.36,0.30,1))
        rough = math_(nodes,links,'ADD', rough, math_(nodes,links,'MULTIPLY', pat, 0.4), clamp=True)
    if kind=='stone':
        # weathering: subtle tonal blotches + darker lower band
        wn = N(nodes,'ShaderNodeTexNoise', **{'Scale':0.6,'Detail':5.0}); links.new(P, wn.inputs['Vector'])
        col = mixrgb(nodes,links, math_(nodes,links,'MULTIPLY', wn.outputs['Fac'], 0.35), col, (0.62,0.55,0.45,1), 'MULTIPLY')
    if kind=='glass':
        # fingerprints / hand smudges at 0.8-1.7 m: voronoi blobs with noise -> roughness bumps
        vo = N(nodes,'ShaderNodeTexVoronoi', **{'Scale':9.0}); links.new(P, vo.inputs['Vector'])
        fn = N(nodes,'ShaderNodeTexNoise', **{'Scale':60.0,'Detail':6.0}); links.new(P, fn.inputs['Vector'])
        band = math_(nodes,links,'MULTIPLY', math_(nodes,links,'GREATER_THAN', Z, 1.25), math_(nodes,links,'LESS_THAN', Z, 2.15))
        fp = math_(nodes,links,'MULTIPLY', math_(nodes,links,'LESS_THAN', vo.outputs['Distance'], 0.12), math_(nodes,links,'MULTIPLY', band, fn.outputs['Fac']))
        rough = math_(nodes,links,'ADD', rough, math_(nodes,links,'MULTIPLY', fp, 0.35), clamp=True)
        col = mixrgb(nodes,links, math_(nodes,links,'MULTIPLY', fp, 0.25), col, (0.7,0.68,0.64,1))
    return col, rough

BUILD = {}
def M_stone(name):
    m,nodes,links,b,P = base(name)
    mp = N(nodes,'ShaderNodeMapping'); mp.inputs['Scale'].default_value=(0.6,0.6,6.0); links.new(P, mp.inputs['Vector'])
    w = N(nodes,'ShaderNodeTexWave', **{'Scale':1.2,'Distortion':6.0,'Detail':6.0}); w.bands_direction='Z'; links.new(mp.outputs[0], w.inputs['Vector'])
    n = N(nodes,'ShaderNodeTexNoise', **{'Scale':2.0,'Detail':10.0}); links.new(P, n.inputs['Vector'])
    br = N(nodes,'ShaderNodeTexBrick', **{'Scale':1.0,'Mortar Size':0.006,'Brick Width':1.2,'Row Height':0.6,'Offset':0.5}); links.new(P, br.inputs['Vector'])
    br.inputs['Color1'].default_value=(1,1,1,1); br.inputs['Color2'].default_value=(.93,.93,.93,1); br.inputs['Mortar'].default_value=(.55,.5,.44,1)
    col = ramp(nodes,links, math_(nodes,links,'ADD', math_(nodes,links,'MULTIPLY', w.outputs['Fac'],0.5), math_(nodes,links,'MULTIPLY', n.outputs['Fac'],0.5)),
               [(0.25,(0.62,0.52,0.40)),(0.5,(0.80,0.70,0.56)),(0.8,(0.88,0.80,0.68))])
    col = mixrgb(nodes,links, 1.0, col, br.outputs['Color'], 'MULTIPLY')
    rough = 0.75
    if GRIME: col, rough = apply_grime(nodes,links,b,P,col,rough,'stone')
    links.new(col, b.inputs['Base Color'])
    if isinstance(rough,float): b.inputs['Roughness'].default_value=rough
    else: links.new(rough, b.inputs['Roughness'])
    bump = N(nodes,'ShaderNodeBump', **{'Strength':0.25,'Distance':0.01}); links.new(n.outputs['Fac'], bump.inputs['Height']); links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return m
def M_flat(rgb, rough, kind=None, metal=0.0, bump_scale=0.0):
    def f(name):
        m,nodes,links,b,P = base(name)
        n = N(nodes,'ShaderNodeTexNoise', **{'Scale':5.0,'Detail':6.0}); links.new(P, n.inputs['Vector'])
        col = mixrgb(nodes,links, math_(nodes,links,'MULTIPLY', n.outputs['Fac'], 0.12), (*rgb,1), (rgb[0]*0.8,rgb[1]*0.8,rgb[2]*0.8,1))
        r = rough
        if GRIME and kind: col, r = apply_grime(nodes,links,b,P,col,r,kind)
        links.new(col, b.inputs['Base Color']); b.inputs['Metallic'].default_value=metal
        if isinstance(r,float): b.inputs['Roughness'].default_value=r
        else: links.new(r, b.inputs['Roughness'])
        if bump_scale:
            bump = N(nodes,'ShaderNodeBump', **{'Strength':0.3,'Distance':0.02}); nb=N(nodes,'ShaderNodeTexNoise', **{'Scale':bump_scale,'Detail':8.0}); links.new(P, nb.inputs['Vector'])
            links.new(nb.outputs['Fac'], bump.inputs['Height']); links.new(bump.outputs['Normal'], b.inputs['Normal'])
        return m
    return f
def M_paving(name):
    m,nodes,links,b,P = base(name)
    br = N(nodes,'ShaderNodeTexBrick', **{'Scale':1.0,'Mortar Size':0.008,'Brick Width':1.2,'Row Height':0.6,'Offset':0.0,'Mortar Smooth':0.1})
    br.inputs['Color1'].default_value=(.86,.80,.70,1); br.inputs['Color2'].default_value=(.82,.76,.66,1); br.inputs['Mortar'].default_value=(.6,.55,.48,1)
    mp = N(nodes,'ShaderNodeMapping'); links.new(P, mp.inputs['Vector']); links.new(mp.outputs[0], br.inputs['Vector'])
    mp.inputs['Rotation'].default_value=(math.pi/2,0,0)  # tiles on XY plane
    sep = N(nodes,'ShaderNodeSeparateXYZ'); links.new(P, sep.inputs[0]); comb=N(nodes,'ShaderNodeCombineXYZ'); links.new(sep.outputs['X'],comb.inputs['X']); links.new(sep.outputs['Y'],comb.inputs['Y'])
    links.new(comb.outputs[0], br.inputs['Vector'])
    n = N(nodes,'ShaderNodeTexNoise', **{'Scale':3.0,'Detail':8.0}); links.new(P, n.inputs['Vector'])
    col = mixrgb(nodes,links, math_(nodes,links,'MULTIPLY', n.outputs['Fac'],0.25), br.outputs['Color'], (.7,.64,.54,1))
    r = 0.7
    if GRIME: col, r = apply_grime(nodes,links,b,P,col,r,'paving')
    links.new(col, b.inputs['Base Color'])
    if isinstance(r,float): b.inputs['Roughness'].default_value=r
    else: links.new(r, b.inputs['Roughness'])
    return m
def M_glass(name):
    m,nodes,links,b,P = base(name)
    # fake lit interior (images show warm interiors): dark reflective with low warm emission
    n = N(nodes,'ShaderNodeTexNoise', **{'Scale':0.8,'Detail':3.0}); links.new(P, n.inputs['Vector'])
    col = mixrgb(nodes,links, n.outputs['Fac'], (0.025,0.03,0.035,1), (0.07,0.06,0.05,1))
    r = 0.03
    if GRIME: col, r = apply_grime(nodes,links,b,P,col,r,'glass')
    links.new(col, b.inputs['Base Color'])
    if isinstance(r,float): b.inputs['Roughness'].default_value=r
    else: links.new(r, b.inputs['Roughness'])
    b.inputs['Specular IOR Level'].default_value=0.9; b.inputs['Coat Weight'].default_value=1.0; b.inputs['Coat Roughness'].default_value=0.02
    em = ramp(nodes,links, n.outputs['Fac'], [(0.45,(0.0,0.0,0.0)),(0.75,(1.0,0.72,0.42))]); links.new(em, b.inputs['Emission Color']); b.inputs['Emission Strength'].default_value=0.12
    return m
def M_balglass(name):
    m,nodes,links,b,P = base(name); b.inputs['Base Color'].default_value=(.85,.95,.95,1); b.inputs['Transmission Weight'].default_value=1.0
    b.inputs['Roughness'].default_value=0.02; b.inputs['IOR'].default_value=1.5
    if GRIME:
        col, r = apply_grime(nodes,links,b,P,(.85,.95,.95,1),0.02,'glass'); links.new(r, b.inputs['Roughness'])
    return m
def M_water(name):
    m,nodes,links,b,P = base(name); b.inputs['Base Color'].default_value=(.55,.88,.92,1); b.inputs['Transmission Weight'].default_value=1.0
    b.inputs['Roughness'].default_value=0.02; b.inputs['IOR'].default_value=1.33
    n = N(nodes,'ShaderNodeTexNoise', **{'Scale':3.5,'Detail':6.0}); links.new(P, n.inputs['Vector'])
    bump = N(nodes,'ShaderNodeBump', **{'Strength':0.25,'Distance':0.02}); links.new(n.outputs['Fac'], bump.inputs['Height']); links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return m
def M_lawn(name):
    m,nodes,links,b,P = base(name)
    n = N(nodes,'ShaderNodeTexNoise', **{'Scale':40.0,'Detail':12.0}); links.new(P, n.inputs['Vector'])
    n2 = N(nodes,'ShaderNodeTexNoise', **{'Scale':0.5,'Detail':4.0}); links.new(P, n2.inputs['Vector'])
    col = ramp(nodes,links, math_(nodes,links,'ADD', math_(nodes,links,'MULTIPLY', n.outputs['Fac'],0.6), math_(nodes,links,'MULTIPLY', n2.outputs['Fac'],0.4)),
               [(0.3,(0.12,0.20,0.05)),(0.55,(0.22,0.33,0.09)),(0.75,(0.34,0.40,0.14))])
    links.new(col, b.inputs['Base Color']); b.inputs['Roughness'].default_value=0.95
    bump = N(nodes,'ShaderNodeBump', **{'Strength':0.6,'Distance':0.02}); links.new(n.outputs['Fac'], bump.inputs['Height']); links.new(bump.outputs['Normal'], b.inputs['Normal'])
    return m
def M_foliage(rgb_dark, rgb_light, alpha_wave=False):
    def f(name):
        m,nodes,links,b,P = base(name)
        n = N(nodes,'ShaderNodeTexNoise', **{'Scale':6.0,'Detail':8.0}); links.new(P, n.inputs['Vector'])
        col = ramp(nodes,links, n.outputs['Fac'], [(0.3,rgb_dark),(0.7,rgb_light)])
        links.new(col, b.inputs['Base Color']); b.inputs['Roughness'].default_value=0.7
        b.inputs['Subsurface Weight'].default_value=0.15
        bump = N(nodes,'ShaderNodeBump', **{'Strength':0.8}); links.new(n.outputs['Fac'], bump.inputs['Height']); links.new(bump.outputs['Normal'], b.inputs['Normal'])
        if alpha_wave:   # pinnate palm leaflets
            uv = N(nodes,'ShaderNodeTexCoord'); w = N(nodes,'ShaderNodeTexWave', **{'Scale':6.0,'Distortion':0.5}); links.new(uv.outputs['Object'], w.inputs['Vector'])
            a = math_(nodes,links,'GREATER_THAN', w.outputs['Fac'], 0.35); links.new(a, b.inputs['Alpha'])
            m.blend_method='HASHED' if hasattr(m,'blend_method') else None
        return m
    return f
BUILD.update(stone=M_stone, stone_rf=M_stone, paving=M_paving, deck=M_paving, coping=M_flat((.88,.83,.74),.6,'stone'),
    soffit=M_flat((.90,.86,.80),.55,'render'), render=M_flat((.9,.86,.8),.55,'render'), bronze=M_flat((.20,.14,.09),.45,'metal',metal=0.6),
    glass=M_glass, water=M_water, pooltile=M_flat((.55,.85,.88),.2), lawn=M_lawn, context_lawn=M_lawn,
    hedge=M_foliage((0.05,0.12,0.03),(0.16,0.26,0.08)), leaf=M_foliage((0.06,0.14,0.04),(0.22,0.32,0.10)), palmleaf=M_foliage((0.10,0.18,0.05),(0.30,0.36,0.12),True),
    bark=M_flat((.32,.26,.20),.9,'stone',bump_scale=20.0), furniture=M_flat((.55,.42,.30),.6,'metal'), cushion=M_flat((.86,.84,.80),.9),
    led=None, placeholder=M_flat((.6,.6,.6),.8), interior=M_glass)
def M_led(name):
    m,nodes,links,b,P = base(name); b.inputs['Base Color'].default_value=(1,.85,.6,1); b.inputs['Emission Color'].default_value=(1,.8,.55,1); b.inputs['Emission Strength'].default_value=12.0
    return m
BUILD['led']=M_led
BUILD['ground']=M_flat((.62,.56,.46),.9,None,0.0,0.0)
BUILD['hedge'] = M_foliage((0.05,0.12,0.03),(0.16,0.26,0.08))
# resolve pending materials now that builders exist
for key, ph in list(MATS.items()):
    real = BUILD[key]('MAT_'+key); ph.user_remap(real); bpy.data.materials.remove(ph); MATS[key] = real

# ---------------- world / sun (Nishita sky, local) ----------------
w = bpy.data.worlds.new('W'); sc.world = w; w.use_nodes=True; wn=w.node_tree.nodes; wl=w.node_tree.links
sky = wn.new('ShaderNodeTexSky'); sky.sky_type='NISHITA'; sky.sun_elevation=math.radians(24); sky.sun_rotation=math.radians(200); sky.sun_intensity=0.6; sky.sun_disc=False
sky.air_density=1.0; sky.dust_density=0.6
wl.new(sky.outputs[0], wn['Background'].inputs[0]); wn['Background'].inputs[1].default_value=0.30
sun = bpy.data.lights.new('SUN','SUN'); sun.energy=3.2; sun.color=(1.0,0.86,0.68); sun.angle=math.radians(1.0)
so = bpy.data.objects.new('SUN', sun); sc.collection.objects.link(so); so.rotation_euler=(math.radians(62), 0, math.radians(200))
sc.render.engine='CYCLES'; sc.cycles.samples=32; sc.cycles.use_denoising=True; sc.cycles.device='CPU'
sc.render.resolution_x=1280; sc.render.resolution_y=720; sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
sc.view_settings.exposure=-0.5; sc.cycles.max_bounces=6; sc.cycles.transparent_max_bounces=12; sc.render.use_persistent_data=True
bpy.ops.wm.save_as_mainfile(filepath=OUT)
json.dump(dict(stage=STAGE, heights_image_read=H, levels=dict(GF0=GF0,GF1=GF1,FF0=FF0,FF1=FF1,RF0=RF0,RF1=RF1), layout=LAYOUT, elements=REG),
          open(OUT.replace('.blend','_register.json'),'w'), indent=1)
print('BUILT', STAGE, len(REG))
