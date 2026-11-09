"""Ashwood 4B exterior -> web glTF (GLB) with baked textures.

Usage (Windows, run from anywhere; ABSOLUTE paths; low priority, 2 threads):
  blender -b --factory-startup -t 2 -P C:/Users/Alfa/.venvs/aw4b/web3d/export_glb.py -- [--skip-tiles] [--skip-ao] [--ao-size 4096] [--ao-samples 24]

What it does (never touches blender/4b_*.blend: it copies 4b_materials.blend to web3d/work/ and opens the copy):
 1. TILE BAKE  - each procedural Cycles material's Base Color field is re-wired to an Emission shader and baked (EMIT) onto a
                 flat T x T m plane -> web3d/tex/raw_<key>.png, then made seamless (two-pass half-offset feather blend;
                 the offset is a whole number of brick/panel periods so joints stay aligned) -> web3d/tex/<key>.jpg.
                 The materials' own projection is reproduced: walls facing +-Y use (x,z), +-X use (y,z), up/down use (x,y).
 2. APPLY      - all modifiers applied (bevel / subsurf / displace) -> plain meshes, object names kept.
 3. UV0        - 'UVTile' = per-face planar world projection (metres / T) matching step 1.
 4. AO ATLAS   - 'UVAtlas' (TEXCOORD_1) = one shared smart-project + pack over all hard-surface objects; Cycles AO bake
                 (distance 1.5 m) -> web3d/tex/ao_atlas.png; foliage/glass/water/LED/context ground are not in the atlas.
 5. EXPORT     - simple glTF PBR materials (baseColor tile, constant roughness/metalness, occlusion = AO atlas on TEXCOORD_1),
                 glass = transmission, LED = emissive, Y-up, metres, named nodes -> web3d/ashwood_4b_exterior.glb
Geometry is exported exactly as built (no edits).
"""
import bpy, bmesh, os, sys, shutil, math, time
import numpy as np

SRC = r'C:/Users/Alfa/.venvs/aw4b/blender/4b_materials.blend'
OUTD = r'C:/Users/Alfa/.venvs/aw4b/web3d'
WORK = OUTD + '/work'; TEX = OUTD + '/tex'
GLB = OUTD + '/ashwood_4b_exterior.glb'
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
def arg(name, default):
    return type(default)(argv[argv.index(name) + 1]) if name in argv else default
SKIP_TILES = '--skip-tiles' in argv
SKIP_AO = '--skip-ao' in argv
AO_SIZE = arg('--ao-size', 4096); AO_SAMPLES = arg('--ao-samples', 24)
os.makedirs(WORK, exist_ok=True); os.makedirs(TEX, exist_ok=True)
T0 = time.time()
def log(*a): print('[%6.1fs]' % (time.time() - T0), *a, flush=True)

COPY = WORK + '/4b_materials_copy.blend'
shutil.copyfile(SRC, COPY)
bpy.ops.wm.open_mainfile(filepath=COPY)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
sc.render.threads_mode = 'FIXED'; sc.render.threads = 2

# ---------------------------------------------------------------- material table
# key = original material name without 'MAT_'. tex = which baked tile it uses; T = tile size in metres; px = resolution.
# (px / T = texel density: stone 341 px/m, paving 427, lawn 256, coping/soffit 256, pool mosaic 1024.)
TILES = dict(stone=(6.0, 2048), paving=(4.8, 2048), coping=(4.0, 1024), soffit=(4.0, 1024), bronze=(2.0, 512),
             lawn=(8.0, 2048), pooltile=(1.0, 1024), ground=(8.0, 1024), hedge=(2.0, 512), leaf=(2.0, 512),
             palmleaf=(2.0, 512), bark=(2.0, 512), cushion=(2.0, 256), furniture=(2.0, 256))
TEXOF = dict(stone='stone', stone_rf='stone', paving='paving', deck='paving', coping='coping', soffit='soffit', bronze='bronze',
             lawn='lawn', context_lawn='lawn', pooltile='pooltile', ground='ground', hedge='hedge', leaf='leaf', palmleaf='palmleaf',
             bark='bark', cushion='cushion', furniture='furniture')
# PBR constants (from the Cycles Principled settings in build_scene.py)
PBR = dict(stone=(0.72, 0.0), stone_rf=(0.72, 0.0), paving=(0.70, 0.0), deck=(0.70, 0.0), coping=(0.60, 0.0), soffit=(0.55, 0.0),
           bronze=(0.45, 0.6), lawn=(0.95, 0.0), context_lawn=(0.95, 0.0), pooltile=(0.15, 0.0), ground=(0.85, 0.0), hedge=(0.75, 0.0),
           leaf=(0.70, 0.0), palmleaf=(0.70, 0.0), bark=(0.90, 0.0), cushion=(0.90, 0.0), furniture=(0.60, 0.0))
NO_AO = {'glass', 'balglass', 'water', 'led', 'hedge', 'leaf', 'palmleaf', 'bark', 'ground'}

def matkey(m): return m.name[4:] if m and m.name.startswith('MAT_') else (m.name if m else 'none')

# ---------------------------------------------------------------- 1. tile bakes
def seamless(a):
    """two-pass half-offset feather blend -> tileable; a: (H,W,C) float"""
    H, W = a.shape[:2]
    def tent(n):
        x = (np.arange(n) + 0.5) / n
        w = np.clip((0.5 - np.abs(x - 0.5)) / 0.25, 0, 1)   # 0 at the edges, 1 over the middle half
        return w * w * (3 - 2 * w)
    wx = tent(W)[None, :, None]; c = a * wx + np.roll(a, W // 2, axis=1) * (1 - wx)
    wy = tent(H)[:, None, None]; return c * wy + np.roll(c, H // 2, axis=0) * (1 - wy)

def bake_tile(key, T, px):
    src = bpy.data.materials.get('MAT_' + key)
    if src is None: log('no material', key); return
    m = src.copy(); m.name = 'BAKE_' + key; nodes, links = m.node_tree.nodes, m.node_tree.links
    out = next(n for n in nodes if n.type == 'OUTPUT_MATERIAL' and n.is_active_output)
    bsdf = next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')
    em = nodes.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = 1.0
    bc = bsdf.inputs['Base Color']
    if bc.is_linked: links.new(bc.links[0].from_socket, em.inputs['Color'])
    else: em.inputs['Color'].default_value = bc.default_value
    links.new(em.outputs[0], out.inputs['Surface'])
    if out.inputs.get('Displacement') and out.inputs['Displacement'].is_linked: links.remove(out.inputs['Displacement'].links[0])
    img = bpy.data.images.new('raw_' + key, px, px, alpha=False, float_buffer=False)
    tn = nodes.new('ShaderNodeTexImage'); tn.image = img; nodes.active = tn
    me = bpy.data.meshes.new('PLANE_' + key)
    me.from_pydata([(0, 0, 0), (T, 0, 0), (T, T, 0), (0, T, 0)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name='UVTile')
    for i, (u, v) in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]): uv.data[i].uv = (u, v)
    ob = bpy.data.objects.new('PLANE_' + key, me); sc.collection.objects.link(ob); me.materials.append(m)
    for o in sc.objects: o.select_set(False)
    ob.select_set(True); bpy.context.view_layer.objects.active = ob
    sc.cycles.samples = 8
    bpy.ops.object.bake(type='EMIT', margin=0, use_clear=True)
    img.filepath_raw = TEX + '/raw_%s.png' % key; img.file_format = 'PNG'; img.save()
    a = np.array(img.pixels[:], dtype=np.float32).reshape(px, px, 4)[:, :, :3]
    s = seamless(a)
    o = bpy.data.images.new(key, px, px, alpha=False); o.pixels[:] = np.concatenate([s, np.ones((px, px, 1), np.float32)], 2).ravel()
    o.filepath_raw = TEX + '/%s.jpg' % key; o.file_format = 'JPEG'; sc.render.image_settings.quality = 90; o.save()
    bpy.data.objects.remove(ob); bpy.data.meshes.remove(me); bpy.data.materials.remove(m)
    log('tile', key, T, 'm', px, 'px', '%.0f px/m' % (px / T))

if not SKIP_TILES:
    for k, (T, px) in TILES.items(): bake_tile(k, T, px)

# ---------------------------------------------------------------- 2. apply modifiers
dg = bpy.context.evaluated_depsgraph_get()
meshes = [o for o in sc.objects if o.type == 'MESH' and not o.hide_render]
for o in meshes:
    if o.modifiers:
        new = bpy.data.meshes.new_from_object(o.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
        new.name = o.data.name; o.modifiers.clear(); o.data = new
log('applied modifiers on', len(meshes), 'objects; tris', sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in meshes))

# ---------------------------------------------------------------- 3. UVTile (planar world projection matching the shaders' facemap)
for o in meshes:
    me = o.data
    for l in list(me.uv_layers): me.uv_layers.remove(l)
    bm = bmesh.new(); bm.from_mesh(me); ul = bm.loops.layers.uv.new('UVTile')
    Mw = o.matrix_world; N3 = Mw.to_3x3().inverted().transposed()
    slots = [matkey(s.material) for s in o.material_slots]
    for f in bm.faces:
        k = slots[f.material_index] if slots else 'none'
        T = TILES.get(TEXOF.get(k, ''), (1.0, 0))[0]
        n = (N3 @ f.normal); ax = max(range(3), key=lambda i: abs(n[i]))
        for lp in f.loops:
            p = Mw @ lp.vert.co
            u, v = ((p.y, p.z) if ax == 0 else (p.x, p.z) if ax == 1 else (p.x, p.y))
            lp[ul].uv = (u / T, v / T)
    bm.to_mesh(me); bm.free()
log('UVTile done')

# ---------------------------------------------------------------- 4. AO atlas
def is_ao(o): return o.material_slots and all(matkey(s.material) not in NO_AO for s in o.material_slots)
ao_objs = [o for o in meshes if is_ao(o)]
for o in ao_objs: o.data.uv_layers.new(name='UVAtlas'); o.data.uv_layers.active = o.data.uv_layers['UVAtlas']
for o in sc.objects: o.select_set(False)
for o in ao_objs: o.select_set(True)
bpy.context.view_layer.objects.active = ao_objs[0]
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(60), island_margin=0.0, area_weight=0.0, correct_aspect=True, scale_to_bounds=False)
bpy.ops.uv.average_islands_scale()
bpy.ops.object.mode_set(mode='OBJECT')
# never-visible faces (undersides at/below ground) get ~no atlas space
for o in ao_objs:
    me = o.data; uvl = me.uv_layers['UVAtlas']; Mw = o.matrix_world; N3 = Mw.to_3x3().inverted().transposed()
    for p in me.polygons:
        n = N3 @ p.normal; c = Mw @ p.center
        if n.z < -0.9 and c.z < 0.05:
            idx = list(p.loop_indices); cu = sum(uvl.data[i].uv.x for i in idx) / len(idx); cv = sum(uvl.data[i].uv.y for i in idx) / len(idx)
            for i in idx: uvl.data[i].uv = (cu + (uvl.data[i].uv.x - cu) * 0.02, cv + (uvl.data[i].uv.y - cv) * 0.02)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.uv.select_all(action='SELECT')
bpy.ops.uv.pack_islands(rotate=True, scale=True, margin_method='FRACTION', margin=0.0012, shape_method='CONCAVE')
bpy.ops.object.mode_set(mode='OBJECT')
for o in ao_objs: o.data.uv_layers.active = o.data.uv_layers['UVTile']; o.data.uv_layers['UVTile'].active_render = True
area = sum(sum(p.area for p in o.data.polygons) for o in ao_objs)
log('atlas objects', len(ao_objs), 'area %.0f m2 -> ~%.0f px/m at %d' % (area, AO_SIZE * 0.75 / math.sqrt(area), AO_SIZE))

# ---------------------------------------------------------------- 5. export materials
def gltf_out_group():
    g = bpy.data.node_groups.get('glTF Material Output')
    if g: return g
    g = bpy.data.node_groups.new('glTF Material Output', 'ShaderNodeTree')
    g.interface.new_socket('Occlusion', in_out='INPUT', socket_type='NodeSocketFloat')
    g.interface.new_socket('Thickness', in_out='INPUT', socket_type='NodeSocketFloat')
    return g
AOIMG = None
if SKIP_AO and os.path.exists(TEX + '/ao_atlas.png'):
    AOIMG = bpy.data.images.load(TEX + '/ao_atlas.png'); AOIMG.colorspace_settings.name = 'Non-Color'
else:
    AOIMG = bpy.data.images.new('ao_atlas', AO_SIZE, AO_SIZE, alpha=False); AOIMG.colorspace_settings.name = 'Non-Color'
TEXIMG = {}
def teximg(t):
    if t not in TEXIMG:
        TEXIMG[t] = bpy.data.images.load(TEX + '/%s.jpg' % t)
    return TEXIMG[t]

def make_export_mat(key, with_ao):
    name = key + ('' if with_ao else '_noao')
    m = bpy.data.materials.new(name); m.use_nodes = True
    nodes, links = m.node_tree.nodes, m.node_tree.links; b = nodes['Principled BSDF']
    t = TEXOF.get(key)
    if t:
        uvn = nodes.new('ShaderNodeUVMap'); uvn.uv_map = 'UVTile'
        tn = nodes.new('ShaderNodeTexImage'); tn.image = teximg(t); links.new(uvn.outputs[0], tn.inputs[0]); links.new(tn.outputs['Color'], b.inputs['Base Color'])
        r, mt = PBR[key]; b.inputs['Roughness'].default_value = r; b.inputs['Metallic'].default_value = mt
    elif key == 'glass':        # dark reflective glazing with a faint warm interior
        b.inputs['Base Color'].default_value = (0.03, 0.035, 0.04, 1); b.inputs['Roughness'].default_value = 0.04; b.inputs['Metallic'].default_value = 0.0
    elif key == 'balglass':     # frameless clear balustrade
        b.inputs['Base Color'].default_value = (0.85, 0.95, 0.95, 1); b.inputs['Roughness'].default_value = 0.03
        b.inputs['Transmission Weight'].default_value = 1.0; b.inputs['IOR'].default_value = 1.5
    elif key == 'water':
        b.inputs['Base Color'].default_value = (0.5, 0.88, 0.9, 1); b.inputs['Roughness'].default_value = 0.02; b.inputs['Transmission Weight'].default_value = 1.0
    elif key == 'led':
        b.inputs['Base Color'].default_value = (1, .85, .6, 1); b.inputs['Emission Color'].default_value = (1, .8, .55, 1); b.inputs['Emission Strength'].default_value = 4.0
    else:
        b.inputs['Base Color'].default_value = (0.6, 0.6, 0.6, 1)
    if with_ao:
        an = nodes.new('ShaderNodeTexImage'); an.image = AOIMG; an.name = 'AO_BAKE'
        uv2 = nodes.new('ShaderNodeUVMap'); uv2.uv_map = 'UVAtlas'; links.new(uv2.outputs[0], an.inputs[0])
        g = nodes.new('ShaderNodeGroup'); g.node_tree = gltf_out_group(); links.new(an.outputs['Color'], g.inputs['Occlusion'])
        nodes.active = an
    return m
EXP = {}
for o in meshes:
    ao = o in ao_objs
    for s in o.material_slots:
        k = matkey(s.material); kk = (k, ao)
        if kk not in EXP: EXP[kk] = make_export_mat(k, ao)
        s.material = EXP[kk]
log('export materials', sorted(m.name for m in EXP.values()))

# ---------------------------------------------------------------- AO bake
if not SKIP_AO:
    sc.world.light_settings.distance = 1.5
    sc.cycles.samples = AO_SAMPLES
    for o in sc.objects: o.select_set(False)
    for o in ao_objs: o.select_set(True)
    bpy.context.view_layer.objects.active = ao_objs[0]
    t = time.time()
    bpy.ops.object.bake(type='AO', margin=6, margin_type='EXTEND', use_clear=True)
    log('AO bake %.0fs' % (time.time() - t))
    # light denoise: 3x3 box blur weighted by coverage (bake margin already extends islands)
    a = np.array(AOIMG.pixels[:], dtype=np.float32).reshape(AO_SIZE, AO_SIZE, 4)
    g = a[:, :, 0]; k = np.zeros_like(g)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1): k += np.roll(np.roll(g, dy, 0), dx, 1)
    g = 0.5 * g + 0.5 * k / 9.0
    a[:, :, 0] = a[:, :, 1] = a[:, :, 2] = g; AOIMG.pixels[:] = a.ravel()
    AOIMG.filepath_raw = TEX + '/ao_atlas.png'; AOIMG.file_format = 'PNG'; AOIMG.save()

# ---------------------------------------------------------------- export
for o in [o for o in sc.objects if o.type != 'MESH' or o.hide_render]:
    bpy.data.objects.remove(o)
kw = dict(filepath=GLB, export_format='GLB', export_yup=True, export_apply=False, export_materials='EXPORT', export_lights=False,
          export_cameras=False, export_image_format='JPEG', export_jpeg_quality=88, export_image_quality=88, export_texcoords=True,
          export_normals=True, export_extras=False)
props = bpy.ops.export_scene.gltf.get_rna_type().properties.keys()
bpy.ops.export_scene.gltf(**{k: v for k, v in kw.items() if k in props})
bpy.ops.wm.save_as_mainfile(filepath=WORK + '/4b_web_export.blend')
log('EXPORTED', GLB, '%.1f MB' % (os.path.getsize(GLB) / 1e6))
