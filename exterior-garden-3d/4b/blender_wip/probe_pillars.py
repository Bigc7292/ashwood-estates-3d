import bpy
from mathutils import Vector
for o in bpy.data.objects:
    if o.type!='MESH' or o.hide_render: continue
    bb=[o.matrix_world @ Vector(c) for c in o.bound_box]
    xs=[v.x for v in bb]; ys=[v.y for v in bb]; zs=[v.z for v in bb]
    if max(zs)>2.5 and min(zs)<1.0 and max(ys)>-6 and min(ys)<0 and (min(xs)<4 or max(xs)>15) and max(xs)-min(xs)<3:
        print('HIT', o.name, [round(min(xs),2),round(max(xs),2)],[round(min(ys),2),round(max(ys),2)],[round(min(zs),2),round(max(zs),2)])
