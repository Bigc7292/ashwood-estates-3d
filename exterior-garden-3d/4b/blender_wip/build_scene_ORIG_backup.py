"""Ashwood 4B exterior — Colin 7-step pipeline, steps 2-4, headless Blender 4.2 (free/local).
Usage: blender -b -P build_scene.py -- <stage> <out.blend>
stage in: layout | boxes | space | models | materials | grime   (cumulative)
Coordinates: Blender X = plan x (m), Blender Y = -plan z (m; street at Y=-29.88, rear plot edge Y=0), Z up.
Footprint numbers = approved CAD V4 + 4B-GF calibration (via ../model/data/model.json, ~ ±3 %).
Appearance (heights, finishes, render-only elements) = approved generated images + brochure p25/p26.
"""
import bpy, bmesh, json, math, os, random, sys
from mathutils import Vector
argv = sys.argv[sys.argv.index('--')+1:]
STAGE, OUT = argv[0], argv[1]
ORDER = ['layout','boxes','space','models','materials','grime']
LV = ORDER.index(STAGE)
random.seed(4)
HERE = os.path.dirname(os.path.abspath(__file__))   # portable (was hard-coded /workspace/... Linux path)
M = json.load(open(os.path.join(HERE, '..', 'model', 'data', 'model.json')))
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
                    led='soffit',ground='paving',balglass='glass',furniture='placeholder',cushion='soffit',context_lawn='lawn',planter_soil='foliage',interior='glass').items(): MATCLASS[k]=v
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
    OVR, OVF = 1.0, 2.0   # front overhang 1.2 -> 2.0: ELEV-FRONT/GARDEN-FRONT show a deep canopy framing the FF slat screen
    for nm,(a,b,c,d) in dict(r=(FF_X0-0.3,FF_X1+0.12,FF_Z0-OVR,CY_Z0), m=(FF_X0-0.3,CY_X0,CY_Z0,CY_Z1), f=(FF_X0-0.3,11.0,CY_Z1,FF_ZF+OVF), fr=(11.0,FF_X1+0.12,CY_Z1,FF_ZF)).items():
        box(f'ROOF_{nm}', a,b,c,d, FF1,RF0,'soffit',C,'FF envelope + overhang read from ELEV-REAR/ELEV-FRONT (overhang not in CAD)', bevel=0.01)
    # RF core (enclosed stair per CAD RF plan) + lift
    # RF plan (NTS): enclosed stair/corridor core is ~3.5 m wide (lift 1.60 m = ~113 px -> ~70 px/m; core walls 222..465 px);
    # the 3.80 m-wide MEP zone beside it is an open roof area, not an enclosed volume. Previously both were one 7.9 m block,
    # Front end (z 22.5), height and set-back are UNCHANGED (CAD/RF-plan position): pulling it back or lowering it per the
    # images is mismatch M12, which is still OPEN for Colin's call.
    box('RF_core', 7.44,10.94, 9.95,22.5, RF0,RF1,'stone_rf',C,'RF plan (NTS) enclosed stair/corridor core ~3.5 m wide — CAD wins over open-stair image')
    box('RF_MEP_screen_front', 3.3,7.44, 22.3,22.5, RF0,RF0+1.5,'stone_rf',C,'RF plan MEP 3.80 x 15.70 (open roof zone); 1.5 m screen wall height assumed')
    box('RF_MEP_screen_left', 3.3,3.5, 9.95,22.5, RF0,RF0+1.5,'stone_rf',C,'RF plan MEP zone edge; screen height assumed')
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
    # Fronds = rachis + individual pinnate leaflets as real geometry (was a flat strip with an alpha-stripe texture,
    # which rendered as see-through 'cards'). Two tiers: upper arching fronds and lower drooping ones (date palm per p25/p26).
    nf=34
    for k in range(nf):
        tier = k % 2
        a=2*math.pi*k/nf+random.uniform(-.12,.12); L=random.uniform(2.7,3.5)*(0.9 if tier else 1.0)
        up=random.uniform(0.35,0.7) if tier==0 else random.uniform(-0.1,0.2); droop=random.uniform(0.6,1.0)+(0.5 if tier else 0)
        ca,sa=math.cos(a),math.sin(a); ns=14
        pts=[]
        for i in range(ns+1):
            t=i/ns; d=L*t; hz=top[2]+up*t*2.0-droop*(t**2)*2.2
            pts.append((top[0]+d*ca, top[1]+d*sa, hz))
        b=len(fv)   # rachis: thin ribbon
        for (cx,cy,hz) in pts: fv += [(cx+sa*0.02,cy-ca*0.02,hz),(cx-sa*0.02,cy+ca*0.02,hz)]
        for i in range(ns): o=b+i*2; ff.append((o,o+1,o+3,o+2))
        for i in range(1,ns):   # leaflets: pairs per segment, V-shaped, longest mid-frond
            t=i/ns; ll=0.75*math.sin(math.pi*min(t*1.05,1.0))+0.08; cx,cy,hz=pts[i]; nx,ny,nz=pts[i+1]
            for side in (-1,1):
                ox,oy = -sa*side*ll, ca*side*ll
                for (sx,sy,sz) in ((cx,cy,hz),((cx+nx)/2,(cy+ny)/2,(hz+nz)/2)):
                    q=len(fv); tip=(sx+ox*0.9+ca*0.12, sy+oy*0.9+sa*0.12, sz-0.28*ll)
                    fv += [(sx,sy,sz),(sx+ca*0.10,sy+sa*0.10,sz),(tip[0]+ca*0.05,tip[1]+sa*0.05,tip[2]),tip]
                    ff.append((q,q+1,q+2,q+3))
    ob2=add_mesh(name+'_fronds', fv, ff, 'palmleaf', C, src)
    for p in ob2.data.polygons: p.use_smooth=True
    REG.append(dict(name=name, collection=C, material='bark/palmleaf', source=src))

def broadleaf(name, x, z, r, ht, src, matkey='leaf', pine=False):
    C='planting'
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.13 if not pine else 0.09, depth=ht, location=(x,-z,ht/2+ (GF0 if pine else 0)))
    t=bpy.context.object; t.name=name+'_trunk'; bpy.context.collection.objects.unlink(t) if t.name in bpy.context.collection.objects else None; coll(C).objects.link(t) if t.name not in coll(C).objects else None
    t.data.materials.append(mat('bark'))
    # Canopy = many small, loose leaf clumps over an open, irregular crown (was 6 large smooth blobs -> 'lollipop' trees).
    # Olive/frangipani-like broadleaf per OUTDOOR-SITE / ELEV-LEFT/RIGHT / ELEV-REAR (olive beside the rear glazing).
    blobs = 4 if pine else (16 if LV >= ORDER.index('models') else 6)
    for k in range(blobs):
        if pine:
            ox,oy,oz,s = random.uniform(-.6,.6), random.uniform(-.6,.6), ht*0.55+k*0.45, (0.9-0.12*k, 0.9-0.12*k, 0.28)
        elif blobs > 6:
            a=random.uniform(0,2*math.pi); rr=random.uniform(0.15,0.85)*r
            ox,oy,oz = rr*math.cos(a), rr*math.sin(a), ht+random.uniform(-0.25,0.65)*r
            ss=random.uniform(.28,.48)*r; s=(ss,ss,ss*random.uniform(0.6,0.8))
        else:
            ox,oy,oz = random.uniform(-.45,.45)*r, random.uniform(-.45,.45)*r, ht+random.uniform(-.1,.5)*r
            ss=random.uniform(.55,.8)*r; s=(ss,ss,ss*0.85)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1, location=(x+ox,-z+oy,oz+(GF0 if pine else 0)))
        b=bpy.context.object; b.name=f'{name}_canopy{k}'; b.scale=s
        if b.name in bpy.context.collection.objects: bpy.context.collection.objects.unlink(b)
        coll(C).objects.link(b); b.data.materials.append(mat(matkey))
        if LV >= ORDER.index('models'):
            tx=bpy.data.textures.get('leafclouds') or bpy.data.textures.new('leafclouds','CLOUDS'); tx.noise_scale=0.12
            d=b.modifiers.new('disp','DISPLACE'); d.texture=tx; d.strength=0.55*min(s); d.mid_level=0.5
    if not pine and LV >= ORDER.index('models'):   # visible branches into the crown (images show open crowns with branches)
        for k in range(4):
            a=2*math.pi*k/4+random.uniform(-.3,.3); L=0.55*r
            bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.06, depth=L*1.6, location=(x+math.cos(a)*L*0.4,-z+math.sin(a)*L*0.4,ht*0.85+0.25*r))
            br=bpy.context.object; br.name=f'{name}_branch{k}'; br.rotation_euler=(math.sin(a)*0.7,-math.cos(a)*0.7,0)
            if br.name in bpy.context.collection.objects: bpy.context.collection.objects.unlink(br)
            coll(C).objects.link(br); br.data.materials.append(mat('bark'))
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
    # ELEV-REAR / p26: GF rear reads glass | stone pier | wide opening (not one run of glass). Pier position image-read
    # (ref px 545..630 of a ~535 px / 13 m facade -> plan x ~6.7..8.7), glazing extents stay CAD (WINS 1777..9238).
    glass_z('GF_rear_glazing_L', gz-0.02, 3.6, 6.6, GF0, GF1, 'image p26/ELEV-REAR left glazed bay; CAD WINS extent')
    mullions_z('GF_rear_frame_L', gz-0.06, 3.6, 6.6, GF0, GF1, 1, 'image bronze frames')
    box('GF_rear_stone_pier', 6.6,8.4, gz-0.05,gz+0.25, GF0,GF1,'stone',C,'image p26/ELEV-REAR stone pier between glazed bays (position image-read)')
    glass_z('GF_rear_glazing', gz-0.02, 8.4, 12.7, GF0, GF1, 'image p26/ELEV-REAR wide sliding opening; CAD WINS extent')
    mullions_z('GF_rear_frame', gz-0.06, 8.4, 12.7, GF0, GF1, 2, 'image bronze frames')
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
    # ELEV-REAR / p26: FF rear reads glass | stone panel | bronze slat screen | glass (ref px 440..545 | 545..625 | 625..770 | 770..900)
    glass_z('FF_rear_glazing_L', GF_Z0-0.02, 3.4, 6.7, FF0, FF1, 'image p26/ELEV-REAR FF left glazing')
    mullions_z('FF_rear_frame_L', GF_Z0-0.06, 3.4, 6.7, FF0, FF1, 2, 'image')
    box('FF_rear_stone_panel', 6.7,8.6, GF_Z0-0.05,GF_Z0+0.25, FF0,FF1,'stone',C,'image p26/ELEV-REAR stone panel (position image-read)')
    glass_z('FF_rear_glazing_mid', GF_Z0+0.02, 8.6, 12.1, FF0, FF1, 'image p26 glazing behind slat screen')
    for i in range(24):
        x = 8.65 + i*0.145
        box(f'FF_rear_slat_{i}', x,x+0.06, GF_Z0-0.22,GF_Z0-0.14, FF0,FF1,'bronze',C,'image p26/ELEV-REAR vertical bronze/timber slat screen')
    glass_z('FF_rear_glazing_R', GF_Z0-0.02, 12.1, 15.4, FF0, FF1, 'image p26/ELEV-REAR FF right glazing')
    mullions_z('FF_rear_frame_R', GF_Z0-0.06, 12.1, 15.4, FF0, FF1, 2, 'image')
    box('FF_balcony_slab', FF_X0,FF_X1, FF_Z0,GF_Z0, GF1,FF0,'soffit',C,'FF V4 BALCONY (extent traced)', bevel=0.01)
    box('FF_balcony_balustrade_glass', FF_X0+0.1,FF_X1-0.1, FF_Z0+0.05,FF_Z0+0.07, FF0,FF0+H['balustrade'],'balglass',C,'image p26 frameless CLEAR glass; height assumed')
    for nm,(a,b) in dict(L=(FF_X0+0.5,FF_X0+1.6), R=(FF_X1-1.6,FF_X1-0.5)).items():   # p26: planting behind the balustrade at both ends
        box(f'FF_balcony_planter_{nm}', a,b, FF_Z0+0.15,FF_Z0+0.65, FF0,FF0+0.45,'stone',C,'image p26 balcony planters (illustrative)', bevel=0.01)
        hedge(f'FF_balcony_planting_{nm}', a+0.05,b-0.05, FF_Z0+0.2,FF_Z0+0.6, FF0+1.25, 'image p26 planting behind balustrade')
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
    box('FF_front_left_balustrade', FF_X0,7.3, FF_ZF+1.05,FF_ZF+1.1, FF0,FF0+H['balustrade'],'balglass',C,'image ELEV-FRONT clear glass/planter balustrade')
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
    box('RF_balustrade_rear', 3.0,15.6, 4.55,4.6, RF0,RF0+H['balustrade'],'balglass',C,'image ROOF-TERRACE clear glass balustrade; RF edge NTS')
    box('RF_balustrade_right', 15.55,15.6, 4.6,9.95, RF0,RF0+H['balustrade'],'balglass',C,'image')
    glass_z('RF_core_door', 9.95-0.02, 8.6, 10.1, RF0, RF0+2.4,'CAD RF stair inside core; door to terrace (image shows open stair — CAD wins)')
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
    # --- carport canopy bronze fascia (ELEV-FRONT / GARDEN-FRONT / p25: dark metal edge band, not a plain white slab)
    ct = H['carport_top']
    box('CARPORT_fascia_front', CARPORT[0]+0.05,CARPORT[1]+0.02, CARPORT[3]-0.34,CARPORT[3]-0.28, ct-H['carport_th']-0.04,ct+0.03,'bronze',C,'image ELEV-FRONT/p25 bronze fascia')
    box('CARPORT_fascia_side', CARPORT[1]-0.04,CARPORT[1]+0.02, GF_FRONT_LEFT_Z,CARPORT[3]-0.3, ct-H['carport_th']-0.04,ct+0.03,'bronze',C,'image ELEV-FRONT/p25 bronze fascia')
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

# STEP 4 levels (from the model's own heights, not hard-coded guesses).
# Walking/standing levels -> base dirt + hand-height smudges; slab TOP edges -> rain streaks run down from them.
FLOOR_LEVELS = (0.0, GF0, FF0, RF0)
DRIP_FROM = (H['carport_top'], FF0, FF0 + H['parapet'], RF0, RF1 + H['canopy'], H['front_wall'], H['side_wall'])
GRIME_SPEC = dict(
    base_dirt='darker band within ~0.75 m above every walking level %s, noise-broken, splash-back on walls/piers' % (FLOOR_LEVELS,),
    drips='vertical rain streaks running down up to 1.4 m below each slab/parapet/wall top %s (stone, render, metal)' % (tuple(round(v,2) for v in DRIP_FROM),),
    dust='light dust on up-facing surfaces (ledges, slab tops, copings, deck)',
    edge_chips='clustered chips on outside edges of render/soffit (grey concrete shows) and stone (fresh paler stone); sparse on metal',
    patina='broad bronze tonal variation, browner/duller toward the bottom of each element (no dot pattern)',
    stone_weathering='soft large blotches + slightly darker lower band',
    glass='hand smudges 0.8-1.7 m above each floor level (roughness + faint haze); no specks',
)
def _levels_above(nodes, links, Z, levels, span):
    """max over levels of (1 - (Z-level)/span) for Z above that level -> 1 at the level, 0 at span above it."""
    out = None
    for lv in levels:
        d = math_(nodes,links,'SUBTRACT', Z, lv)
        u = math_(nodes,links,'MULTIPLY', math_(nodes,links,'GREATER_THAN', d, -0.02), math_(nodes,links,'SUBTRACT', 1.0, math_(nodes,links,'DIVIDE', d, span), clamp=True))
        out = u if out is None else math_(nodes,links,'MAXIMUM', out, u)
    return out
def apply_grime(nodes, links, bsdf, P, col, rough, kind):
    """STEP 4 procedural grime. kind: stone | render | metal | glass | paving"""
    sep = N(nodes,'ShaderNodeSeparateXYZ'); links.new(P, sep.inputs[0]); Z = sep.outputs['Z']
    geo = N(nodes,'ShaderNodeNewGeometry')
    nz = N(nodes,'ShaderNodeSeparateXYZ'); links.new(geo.outputs['Normal'], nz.inputs[0])
    vert = math_(nodes,links,'LESS_THAN', math_(nodes,links,'ABSOLUTE', nz.outputs['Z']), 0.5)   # vertical faces only
    if kind != 'glass':
        # base dirt / splash-back above every walking level (ground, GF deck, FF balconies, roof terrace)
        n1 = N(nodes,'ShaderNodeTexNoise', **{'Scale':4.0,'Detail':8.0,'Roughness':0.65}); links.new(P, n1.inputs['Vector'])
        bd = _levels_above(nodes, links, Z, FLOOR_LEVELS, 0.75)
        bd = math_(nodes,links,'POWER', bd, 1.6)
        bd = math_(nodes,links,'MULTIPLY', math_(nodes,links,'MULTIPLY', bd, vert), math_(nodes,links,'ADD', math_(nodes,links,'MULTIPLY', n1.outputs['Fac'], 0.9), 0.35), clamp=True)
        col = mixrgb(nodes,links, math_(nodes,links,'MULTIPLY', bd, 0.55), col, (0.46,0.39,0.31,1), 'MULTIPLY')
    if kind in ('stone','render','metal'):
        # rain streaks running DOWN from slab / parapet / wall tops: noise stretched vertically, thresholded into streaks
        mp = N(nodes,'ShaderNodeMapping'); mp.inputs['Scale'].default_value=(9,9,0.35); links.new(P, mp.inputs['Vector'])
        sn = N(nodes,'ShaderNodeTexNoise', **{'Scale':3.0,'Detail':5.0,'Roughness':0.55}); links.new(mp.outputs[0], sn.inputs['Vector'])
        streak = N(nodes,'ShaderNodeMapRange'); streak.inputs['From Min'].default_value=0.57; streak.inputs['From Max'].default_value=0.72
        links.new(sn.outputs['Fac'], streak.inputs['Value'])
        under = None
        for lvl in DRIP_FROM:
            d = math_(nodes,links,'SUBTRACT', lvl, Z)      # distance below the top edge
            u = math_(nodes,links,'MULTIPLY', math_(nodes,links,'GREATER_THAN', d, 0.0), math_(nodes,links,'SUBTRACT', 1.0, math_(nodes,links,'DIVIDE', d, 1.4), clamp=True))
            under = u if under is None else math_(nodes,links,'MAXIMUM', under, u)
        dr = math_(nodes,links,'MULTIPLY', math_(nodes,links,'MULTIPLY', streak.outputs['Result'], under), vert, clamp=True)
        col = mixrgb(nodes,links, math_(nodes,links,'MULTIPLY', dr, 0.45), col, (0.40,0.34,0.27,1), 'MULTIPLY')
    if kind != 'glass':
        # dust on up-facing surfaces
        up = math_(nodes,links,'GREATER_THAN', nz.outputs['Z'], 0.7)
        dn = N(nodes,'ShaderNodeTexNoise', **{'Scale':7.0,'Detail':10.0}); links.new(P, dn.inputs['Vector'])
        dust = math_(nodes,links,'MULTIPLY', up, math_(nodes,links,'MULTIPLY', dn.outputs['Fac'], 0.6), clamp=True)
        col = mixrgb(nodes,links, dust, col, (0.78,0.72,0.62,1))
        rough = math_(nodes,links,'ADD', rough, math_(nodes,links,'MULTIPLY', dust, 0.3), clamp=True)
    if kind in ('render','metal','stone'):
        # edge chips: bevel-normal vs true normal -> outside-edge mask, broken into CLUSTERS by low-frequency noise
        bev = N(nodes,'ShaderNodeBevel'); bev.inputs['Radius'].default_value=0.025; bev.samples=8
        dot = N(nodes,'ShaderNodeVectorMath'); dot.operation='DOT_PRODUCT'; links.new(bev.outputs['Normal'], dot.inputs[0]); links.new(geo.outputs['Normal'], dot.inputs[1])
        edge = math_(nodes,links,'MULTIPLY', math_(nodes,links,'SUBTRACT', 1.0, dot.outputs['Value']), 30.0, clamp=True)
        cl = N(nodes,'ShaderNodeTexNoise', **{'Scale':1.6,'Detail':2.0}); links.new(P, cl.inputs['Vector'])          # where chips cluster
        cn = N(nodes,'ShaderNodeTexNoise', **{'Scale':40.0,'Detail':10.0,'Roughness':0.7}); links.new(P, cn.inputs['Vector'])  # chip shapes
        thr = {'render':0.42,'stone':0.42,'metal':0.88}[kind]   # metal: thin bars/fascias are 'all edge' -> keep chips rare
        chip = math_(nodes,links,'GREATER_THAN',
                     math_(nodes,links,'MULTIPLY', edge, math_(nodes,links,'MULTIPLY', cn.outputs['Fac'], math_(nodes,links,'ADD', cl.outputs['Fac'], 0.45))), thr)
        sub = {'render':(0.50,0.49,0.47,1),'metal':(0.55,0.44,0.30,1),'stone':(0.93,0.89,0.82,1)}[kind]
        col = mixrgb(nodes,links, chip, col, sub)
    if kind=='metal':
        # bronze patina: broad tonal variation across neighbouring bars (low-frequency), duller/browner toward the bottom
        pn = N(nodes,'ShaderNodeTexNoise', **{'Scale':0.9,'Detail':4.0}); links.new(P, pn.inputs['Vector'])
        low = math_(nodes,links,'SUBTRACT', 1.0, math_(nodes,links,'DIVIDE', Z, 3.5), clamp=True)
        pat = math_(nodes,links,'MULTIPLY', math_(nodes,links,'ADD', math_(nodes,links,'MULTIPLY', pn.outputs['Fac'], 0.7), math_(nodes,links,'MULTIPLY', low, 0.5)), 0.75, clamp=True)
        col = mixrgb(nodes,links, math_(nodes,links,'MULTIPLY', pat, 0.55), col, (0.27,0.24,0.17,1))
        rough = math_(nodes,links,'ADD', rough, math_(nodes,links,'MULTIPLY', pat, 0.35), clamp=True)
    if kind=='stone':
        # weathering: soft large blotches + slightly darker lower band
        wn = N(nodes,'ShaderNodeTexNoise', **{'Scale':0.45,'Detail':5.0}); links.new(P, wn.inputs['Vector'])
        col = mixrgb(nodes,links, math_(nodes,links,'MULTIPLY', wn.outputs['Fac'], 0.30), col, (0.70,0.62,0.52,1), 'MULTIPLY')
    if kind=='glass':
        # hand smudges 0.8-1.7 m above each floor level: noise-distorted soft blobs -> extra roughness + faint haze
        band = None
        for lv in (GF0, FF0, RF0):
            hz = math_(nodes,links,'SUBTRACT', Z, lv)
            bnd = math_(nodes,links,'MULTIPLY', math_(nodes,links,'GREATER_THAN', hz, 0.8), math_(nodes,links,'LESS_THAN', hz, 1.7))
            band = bnd if band is None else math_(nodes,links,'MAXIMUM', band, bnd)
        dn = N(nodes,'ShaderNodeTexNoise', **{'Scale':3.0,'Detail':2.0}); links.new(P, dn.inputs['Vector'])
        vo = N(nodes,'ShaderNodeTexVoronoi', **{'Scale':6.0,'Randomness':1.0}); links.new(P, vo.inputs['Vector'])
        blob = N(nodes,'ShaderNodeMapRange'); blob.inputs['From Min'].default_value=0.16; blob.inputs['From Max'].default_value=0.05
        links.new(vo.outputs['Distance'], blob.inputs['Value'])
        fp = math_(nodes,links,'MULTIPLY', math_(nodes,links,'MULTIPLY', blob.outputs['Result'], band), math_(nodes,links,'GREATER_THAN', dn.outputs['Fac'], 0.5))
        rough = math_(nodes,links,'ADD', rough, math_(nodes,links,'MULTIPLY', fp, 0.22), clamp=True)
        col = mixrgb(nodes,links, math_(nodes,links,'MULTIPLY', fp, 0.10), col, (0.6,0.58,0.55,1))
    return col, rough

BUILD = {}
def facemap(nodes, links, P):
    """Per-face planar projection -> (u, v, 0) so wall textures run ALONG the wall face.
    Walls facing +-Y use (x, z); walls facing +-X use (y, z); up/down faces use (x, y).
    (The old stone used object XY directly, which on vertical faces collapsed panels into thin stripes -> 'siding' look.)"""
    sp = N(nodes,'ShaderNodeSeparateXYZ'); links.new(P, sp.inputs[0])
    geo = N(nodes,'ShaderNodeNewGeometry'); sn = N(nodes,'ShaderNodeSeparateXYZ'); links.new(geo.outputs['Normal'], sn.inputs[0])
    fx = math_(nodes,links,'GREATER_THAN', math_(nodes,links,'ABSOLUTE', sn.outputs['X']), 0.5)
    fz = math_(nodes,links,'GREATER_THAN', math_(nodes,links,'ABSOLUTE', sn.outputs['Z']), 0.5)
    lerp = lambda t,a,b: math_(nodes,links,'ADD', a, math_(nodes,links,'MULTIPLY', t, math_(nodes,links,'SUBTRACT', b, a)))
    u = lerp(fx, sp.outputs['X'], sp.outputs['Y'])
    v = lerp(fz, sp.outputs['Z'], sp.outputs['Y'])
    cb = N(nodes,'ShaderNodeCombineXYZ'); links.new(u, cb.inputs['X']); links.new(v, cb.inputs['Y'])
    return cb.outputs[0]
def M_stone(name):
    """Large-format honed travertine panels (ELEV-* / p25 / p26): ~1.5 x 0.75 m panels, hairline joints,
    per-panel tone shift, soft horizontal vein banding. Low contrast so it reads as stone, not siding."""
    m,nodes,links,b,P = base(name)
    UV = facemap(nodes, links, P)
    br = N(nodes,'ShaderNodeTexBrick', **{'Scale':1.0,'Mortar Size':0.004,'Mortar Smooth':0.2,'Bias':0.0,'Brick Width':1.5,'Row Height':0.75,'Offset':0.5})
    links.new(UV, br.inputs['Vector'])
    br.inputs['Color1'].default_value=(1,1,1,1); br.inputs['Color2'].default_value=(.90,.90,.90,1); br.inputs['Mortar'].default_value=(.62,.57,.50,1)
    mp = N(nodes,'ShaderNodeMapping'); mp.inputs['Scale'].default_value=(0.35,3.5,1.0); links.new(UV, mp.inputs['Vector'])   # veins run horizontally along the face
    vn = N(nodes,'ShaderNodeTexNoise', **{'Scale':2.2,'Detail':9.0,'Roughness':0.62,'Distortion':0.4}); links.new(mp.outputs[0], vn.inputs['Vector'])
    pores = N(nodes,'ShaderNodeTexNoise', **{'Scale':60.0,'Detail':4.0}); links.new(UV, pores.inputs['Vector'])
    col = ramp(nodes,links, vn.outputs['Fac'], [(0.30,(0.56,0.47,0.36)),(0.50,(0.65,0.56,0.44)),(0.72,(0.72,0.63,0.51))])   # warm beige travertine (refs), not near-white
    col = mixrgb(nodes,links, math_(nodes,links,'MULTIPLY', math_(nodes,links,'GREATER_THAN', pores.outputs['Fac'], 0.70), 0.12), col, (0.55,0.48,0.38,1))
    col = mixrgb(nodes,links, 1.0, col, br.outputs['Color'], 'MULTIPLY')
    n = vn
    rough = 0.72
    if GRIME: col, rough = apply_grime(nodes,links,b,P,col,rough,'stone')
    links.new(col, b.inputs['Base Color'])
    if isinstance(rough,float): b.inputs['Roughness'].default_value=rough
    else: links.new(rough, b.inputs['Roughness'])
    bump = N(nodes,'ShaderNodeBump', **{'Strength':0.12,'Distance':0.005}); links.new(br.outputs['Fac'], bump.inputs['Height']); links.new(bump.outputs['Normal'], b.inputs['Normal'])
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
    """Mown lawn (ELEV-REAR / GARDEN-BACK / p26): fine grain + very soft mottling, olive-green, near-flat bump.
    (Old version: strong bump on a scale-40 noise + big low-frequency blotches read as waves/stripes at grazing angles.)"""
    m,nodes,links,b,P = base(name)
    n = N(nodes,'ShaderNodeTexNoise', **{'Scale':320.0,'Detail':4.0}); links.new(P, n.inputs['Vector'])
    n2 = N(nodes,'ShaderNodeTexNoise', **{'Scale':0.18,'Detail':3.0}); links.new(P, n2.inputs['Vector'])
    col = ramp(nodes,links, math_(nodes,links,'ADD', math_(nodes,links,'MULTIPLY', n.outputs['Fac'],0.8), math_(nodes,links,'MULTIPLY', n2.outputs['Fac'],0.2)),
               [(0.35,(0.10,0.17,0.04)),(0.52,(0.15,0.23,0.06)),(0.68,(0.20,0.27,0.08))])
    links.new(col, b.inputs['Base Color']); b.inputs['Roughness'].default_value=0.95
    b.inputs['Sheen Weight'].default_value=0.3; b.inputs['Sheen Tint'].default_value=(0.6,0.7,0.4,1)
    return m   # no bump: any bump read as waves at the low garden camera angles
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
    soffit=M_flat((.80,.75,.68),.55,'render'), render=M_flat((.80,.75,.68),.55,'render'),   # warm pale render (refs), was near-white
 bronze=M_flat((.20,.14,.09),.45,'metal',metal=0.6),
    glass=M_glass, water=M_water, pooltile=M_flat((.55,.85,.88),.2), lawn=M_lawn, context_lawn=M_lawn,
    hedge=M_foliage((0.05,0.12,0.03),(0.16,0.26,0.08)), leaf=M_foliage((0.06,0.14,0.04),(0.22,0.32,0.10)), palmleaf=M_foliage((0.10,0.18,0.05),(0.30,0.36,0.12)),   # leaflets are now real geometry -> no alpha stripes
    balglass=M_balglass,
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
sky = wn.new('ShaderNodeTexSky')
# Blender 4.x 'NISHITA' == Blender 5.x 'SINGLE_SCATTERING' (renamed)
sky.sky_type = 'NISHITA' if 'NISHITA' in [i.identifier for i in sky.bl_rna.properties['sky_type'].enum_items] else 'SINGLE_SCATTERING'
# Late-afternoon light (all approved images + p25/p26 are warm, low sun, deep blue sky; old setup was flat midday-looking)
sky.sun_elevation=math.radians(20); sky.sun_rotation=math.radians(200); sky.sun_intensity=0.5; sky.sun_disc=False
sky.air_density=1.0
if hasattr(sky,'dust_density'): sky.dust_density=0.35
if hasattr(sky,'aerosol_density'): sky.aerosol_density=0.35
wl.new(sky.outputs[0], wn['Background'].inputs[0]); wn['Background'].inputs[1].default_value=0.28
sun = bpy.data.lights.new('SUN','SUN'); sun.energy=6.5; sun.color=(1.0,0.78,0.55); sun.angle=math.radians(0.8)
so = bpy.data.objects.new('SUN', sun); sc.collection.objects.link(so); so.rotation_euler=(math.radians(68), 0, math.radians(200))
sc.render.engine='CYCLES'; sc.cycles.samples=32; sc.cycles.use_denoising=True; sc.cycles.device='CPU'
sc.render.resolution_x=1280; sc.render.resolution_y=720; sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - High Contrast'
sc.view_settings.exposure=-0.35; sc.cycles.max_bounces=6; sc.cycles.transparent_max_bounces=12; sc.render.use_persistent_data=True
# White specks on glass (old close-up 01) were caustic fireflies through glass/water, not grime -> no caustics, clamp indirect
sc.cycles.caustics_reflective=False; sc.cycles.caustics_refractive=False; sc.cycles.sample_clamp_indirect=4.0; sc.cycles.sample_clamp_direct=12.0; sc.cycles.blur_glossy=1.0
bpy.ops.wm.save_as_mainfile(filepath=OUT)
reg = dict(stage=STAGE, heights_image_read=H, levels=dict(GF0=GF0,GF1=GF1,FF0=FF0,FF1=FF1,RF0=RF0,RF1=RF1), layout=LAYOUT, elements=REG)
if GRIME:
    used = sorted({e['material'] for e in REG})
    reg['grime'] = dict(spec=GRIME_SPEC, floor_levels_m=FLOOR_LEVELS, drip_from_m=DRIP_FROM,
                        by_material={k: v for k, v in dict(stone='stone', stone_rf='stone', coping='stone', bark='stone', soffit='render', render='render',
                                                            bronze='metal', furniture='metal', glass='glass', balglass='glass', paving='paving', deck='paving').items() if k in used},
                        method='procedural Cycles shader nodes only (no image textures)')
json.dump(reg, open(OUT.replace('.blend','_register.json'),'w'), indent=1)
print('BUILT', STAGE, len(REG))
