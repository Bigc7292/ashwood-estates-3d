import bpy, collections, json
dg = bpy.context.evaluated_depsgraph_get()
out=[]
for o in bpy.data.objects:
    if o.type!='MESH': out.append((o.name,o.type)); continue
    e=o.evaluated_get(dg); me=e.to_mesh()
    out.append((o.name, [c.name for c in o.users_collection][0], [m.type for m in o.modifiers], [s.material.name if s.material else None for s in o.material_slots], len(me.polygons), o.hide_render))
    e.to_mesh_clear()
tot=collections.Counter(); 
for r in out:
    if len(r)>2: tot[r[1]]+=r[4]
print('TOTALS',dict(tot))
for r in out:
    if len(r)<3 or r[4]>500 or r[2]: print('OBJ',r)
print('NOBJ',len(out))
print('MATS',[m.name for m in bpy.data.materials])
print('COLLS',[(c.name,c.hide_render) for c in bpy.data.collections])
