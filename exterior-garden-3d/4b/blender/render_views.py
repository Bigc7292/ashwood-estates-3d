"""blender -b <file.blend> -P render_views.py -- <outdir> <samples> <w> <h> [names,comma] """
import bpy, json, math, sys, os
from mathutils import Vector
a = sys.argv[sys.argv.index('--')+1:]
OUT, SAMP, W, Hh = a[0], int(a[1]), int(a[2]), int(a[3]); ONLY = a[4].split(',') if len(a)>4 and a[4] else None
os.makedirs(OUT, exist_ok=True)
V = json.load(open(os.environ.get('VIEWS','/workspace/exterior-garden-3d/4b/blender/views_blender.json')))
sc = bpy.context.scene; sc.cycles.samples = SAMP; sc.render.resolution_x = W; sc.render.resolution_y = Hh
sc.render.image_settings.file_format='PNG'
cam = bpy.data.cameras.new('CAM'); co = bpy.data.objects.new('CAM', cam); sc.collection.objects.link(co); sc.camera = co
sun = bpy.data.objects.get('SUN'); sky = next((n for n in sc.world.node_tree.nodes if n.type=='TEX_SKY'), None)
labels = {}
from bpy_extras.object_utils import world_to_camera_view
for v in V:
    if ONLY and v['name'] not in ONLY: continue
    p, t = Vector(v['pos']), Vector(v['tgt'])
    co.location = p; d = (t-p); co.rotation_euler = d.to_track_quat('-Z','Y').to_euler()
    if v.get('ortho'): cam.type='ORTHO'; cam.ortho_scale=v['ortho']; co.rotation_euler=(0,0,0)
    else: cam.type='PERSP'; cam.lens=v.get('lens',30)
    cam.clip_end = 500
    hd = math.atan2(-d.x, d.y) if d.xy.length>1e-3 else 0.0
    if sun: sun.rotation_euler = (math.radians(64), 0, hd + math.radians(38))
    if sky: sky.sun_rotation = hd + math.radians(38) + math.pi
    sc.render.filepath = os.path.join(OUT, v['file'])
    bpy.ops.render.render(write_still=True)
    if v.get('labels'):
        bpy.context.view_layer.update()
        pts = {'Pool 9.50x2.40 (CAD)':(7.9,-2.4,0.6),'Raised deck +0.45 (image)':(14.3,-3.5,0.7),'Courtyard (CAD, open plan-right)':(13.6,-14.5,1.0),
               'Carport + pier (RENDER-SOURCED)':(3.8,-27,3.6),'Stone fin (RENDER-SOURCED)':(15.6,-23,11.6),'RF core: enclosed stair (CAD, NTS)':(7,-16,11.2),
               'RF canopy (image)':(7.6,-6.8,11.6),'Side walls 2.2 m (image) on CAD line':(-0.1,-20,2.3),'Off-plot context lawn (NOT PLOT)':(9.4,6,0.2)}
        labels[v['file']] = {k:list(world_to_camera_view(sc, co, Vector(xyz)))[:2] for k,xyz in pts.items()}
    print('RENDERED', v['file'], flush=True)
json.dump(labels, open(os.path.join(OUT,'_labels.json'),'w'))
