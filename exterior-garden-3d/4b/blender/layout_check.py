import bpy, sys
a = sys.argv[sys.argv.index('--')+1:]
sc=bpy.context.scene; W,D=18.724,29.881
cam=bpy.data.cameras.new('C'); co=bpy.data.objects.new('C',cam); sc.collection.objects.link(co); sc.camera=co
cam.type='ORTHO'; cam.ortho_scale=D; cam.sensor_fit='VERTICAL'; co.location=(W/2,-D/2,50); co.rotation_euler=(0,0,0)
sc.render.resolution_x=int(W*30); sc.render.resolution_y=int(D*30); sc.render.engine='BLENDER_WORKBENCH'
sc.display.shading.light='FLAT'; sc.display.shading.color_type='MATERIAL'
sc.render.filepath=a[0]; bpy.ops.render.render(write_still=True)
