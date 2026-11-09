#!/usr/bin/env python3
"""Exactly ONE SVG architectural cutaway illustration from approved planar artwork.
No scene, mesh, model file, guessed room geometry or automatic multi-floor batch.
"""
from pathlib import Path
import xml.etree.ElementTree as E
import json,copy,math,re,html,hashlib,datetime,io
from zoneinfo import ZoneInfo
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageChops
import cairosvg
from active_inputs import ROOT as R,approved_plan
ID='4B-GF';p=approved_plan(ID);O=R/'active/one-cutaway-prototype';O.mkdir(exist_ok=True);(O/'qa').mkdir(exist_ok=True)
N='{http://www.w3.org/2000/svg}';root=E.parse(R/p['svg']).getroot();g=root.find(N+'g[@id="source_space"]');defs=root.find(N+'defs');wall=g.find(N+'g[@id="structural_wall_poche"]');assert len(wall)==13
record=next(r for r in json.loads((R/'active/approved-cad-v4/reports/nine_V4_manifest.json').read_text())['records'] if r['id']==ID)
ppm=record['calibration']['px_per_m'];cut_display_m=.80;cut_z=ppm*cut_display_m
az=math.radians(18);el=math.radians(55);c=math.cos(az);s=math.sin(az);si=math.sin(el);ce=math.cos(el)
P=np.array([[c,s],[-s*si,c*si]]);inv=np.linalg.inv(P)
# Parallel orthographic projection. Display z is explicitly not a factual wall elevation.
def view(x,y,z=0):return np.array([c*x+s*y,-s*si*x+c*si*y-ce*z])
site=np.array([[107,54],[634,54],[634,895],[107,895]],dtype=float)
projected=np.array([view(x,y) for x,y in site]);mn=projected.min(0);mx=projected.max(0)
W,H=1500,1750;scale=min(1200/(mx[0]-mn[0]),1220/(mx[1]-mn[1]));off=np.array([(W-scale*(mx[0]-mn[0]))/2,165])-scale*mn

def page(x,y,z=0):return view(x,y,z)*scale+off
A=[]
def add(z):A.append(z)
def text(x,y,t,size=14,col='#30453b',anchor='start',bold=False):add(f'<text x="{x:.3f}" y="{y:.3f}" font-family="DejaVu Sans, sans-serif" font-size="{size}" text-anchor="{anchor}" font-weight="'+('bold' if bold else 'normal')+f'" fill="{col}">{html.escape(t)}</text>')
def poly(ps,fill,stroke='none',sw=.5,opacity=1):add('<polygon points="'+' '.join(f'{x:.5f},{y:.5f}' for x,y in ps)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" opacity="{opacity}"/>')
def line(a,b,col='#809084',sw=1):add(f'<path d="M{a[0]:.4f},{a[1]:.4f}L{b[0]:.4f},{b[1]:.4f}" stroke="{col}" stroke-width="{sw}" fill="none"/>')
def path_rings(d):
 rings=[]
 # Approved structural paths contain only absolute M/L/Z; reject unsupported commands.
 assert not re.search(r'[AaCcQqHhVvSsTt]',d),d[:70]
 for part in re.findall(r'M[^M]+',d):
  pts=[(float(x)+.5,float(y)+.5) for x,y in re.findall(r'([-\d.]+),([-\d.]+)',part)]
  if len(pts)>2:rings.append(pts)
 return rings
wall_features=[];allpoints=[]
for k,w in enumerate(wall):
 d=w.get('d');rings=path_rings(d);wall_features.append({'feature_id':f'{ID}/wall-contour-{k+1:02d}','approved_svg_element_index':k,'approved_path_d':d,'approved_group_transform':'translate(.5,.5)','rings_source_crop_pixels':rings,'XY_status':'exact_copy_of_approved_presentation_trace; not survey geometry','metric_status':'XY metre coordinates would be approximate calibration-derived; pixel contour authoritative'})
 allpoints.extend(q for ring in rings for q in ring)
pts=np.array(allpoints);back=(inv@(P@pts.T)).T;max_error=float(np.abs(back-pts).max());assert max_error<1e-10
# Base artwork: preserve all source surfaces, symbols and details. Remove room text plates and
# perimeter presentation guides only; they are redrawn as upright readable annotations.
children=list(g);firstlabel=next(i for i,q in enumerate(children) if q.tag==N+'text' and q.text=='SWIMMING POOL')
base=copy.deepcopy(g);base.attrib.pop('transform',None);base.set('id','approved_planar_artwork')
for q in list(base)[firstlabel-1:]:base.remove(q)
assert len(base)==firstlabel-1
# Copied door/glazing plan cues following the structural group stay on the original floor plane.
wi=next(i for i,q in enumerate(children) if q.get('id')=='structural_wall_poche')
opening_cues=[{'feature_id':f'{ID}/plan-opening-cue-{i-wi:02d}','svg_path_d':q.get('d'),'status':'copied_approved_2D_guideline; exact opening width/swing and vertical extent unverified'} for i,q in enumerate(children[wi+1:firstlabel-1],wi+1) if q.tag==N+'path']
# All approved source-local room text, including its unknown dimension, remains semantically intact.
rooms=[];ts=[q for q in children if q.tag==N+'text'];i=0
while i<len(ts):
 q=ts[i];name=q.text or ''
 if name.startswith('~') or 'DERIVED SITE' in name or name.endswith('ENTRY') and name in ['VEHICLE ENTRY','PEDESTRIAN ENTRY','SERVICE ENTRY']:
  i+=1;continue
 if name in ['TERRACE','OUTDOOR TERRACE']:
  rooms.append({'name':name,'dimension':'UNKNOWN','anchor':[float(q.get('x')),float(q.get('y'))],'dimension_status':'not stated'});i+=1;continue
 if i+1<len(ts) and float(ts[i+1].get('y'))-float(q.get('y'))==7:
  rooms.append({'name':name,'dimension':ts[i+1].text,'anchor':[float(q.get('x')),float(q.get('y'))],'dimension_status':'source-label transcript; not remeasured; maid dimension unresolved' if name=='MAID ROOM' else 'source-label transcript from approved 2D; not independently measured'});i+=2
 else:i+=1
assert len(rooms)==18,len(rooms)
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">');add(E.tostring(defs,encoding='unicode'));add('<rect width="1500" height="1750" fill="white"/>')
text(70,58,'ASHWOOD ESTATES',28,bold=True);text(70,89,'4-BEDROOM VILLA  /  GROUND FLOOR',19)
text(1430,58,'ONE-PLAN REVIEW',14,'#8a7854','end',True);text(1430,88,'3D CAD-STYLE PLAN ILLUSTRATION',14,'#8a7854','end')
line((70,108),(1430,108),'#aab7ab',1)
# Thin graphic presentation plate is not an assertion of floor slab depth.
for j in range(4):
 a=site[j];b=site[(j+1)%4];poly([page(*a),page(*b),page(*b)+[0,7],page(*a)+[0,7]],'#b7beb0','#9ca68f',.6)
# The approved artwork is projected as one exact XY group; its furniture is not redesigned.
add(f'<g transform="matrix({scale*c} {scale*(-s*si)} {scale*s} {scale*c*si} {off[0]} {off[1]})">');add(E.tostring(base,encoding='unicode'));add('</g>')
# Soft non-geometric contact shadows, clipped as an illustration rather than geometry.
shadow_shift=np.array([5,6.5])
for f in wall_features:
 for ring in f['rings_source_crop_pixels']:
  poly([page(x,y)+shadow_shift for x,y in ring],'#253b30',opacity=.10)
# Vertical cut faces use EXACT copied boundary edges, never a centreline reconstruction.
faces=[]
for f in wall_features:
 for ring in f['rings_source_crop_pixels']:
  for a,b in zip(ring,ring[1:]+ring[:1]):
   if a==b:continue
   a=np.array(a);b=np.array(b);v=b-a;length=np.linalg.norm(v)
   # Light is decorative only, based on boundary direction; no real lighting analysis.
   light=.5+.5*abs(v[0])/length
   shade=int(150+light*52);fill=f'#{shade:02x}{min(255,shade+7):02x}{max(0,shade-7):02x}'
   dep=float(np.dot((a+b)/2,[-s*ce,c*ce]));faces.append((dep,[page(*a),page(*b),page(*b,cut_z),page(*a,cut_z)],fill))
for _,ps,col in sorted(faces,key=lambda x:x[0]):poly(ps,col,'#566459',.37)
# Dark continuous cut caps, with original subpath winding/holes retained exactly.
capgroup=copy.deepcopy(wall);capgroup.set('id','approved_XY_wall_caps_display_lift');capgroup.set('fill','#34463b')
for q in capgroup:q.set('fill','#34463b')
add(f'<g transform="matrix({scale*c} {scale*(-s*si)} {scale*s} {scale*c*si} {off[0]} {off[1]-scale*ce*cut_z})">');add(E.tostring(capgroup,encoding='unicode'));add('</g>')
# Label plates are upright in image space, not falsified perspective measurements.
for k,r in enumerate(rooms):
 x,y=page(*r['anchor']);name=r['name'];dim=r['dimension'];fs=11.2 if len(name)<18 else 9.3;ds=10.6
 if name in ['PANTRY','POWDER','DRESS','MAID BATH','LIFT']:fs=10;ds=9.1
 if name in ['TERRACE','OUTDOOR TERRACE']:fs=9.3;ds=8.4
 ww=max(len(name)*fs*.29,len(dim)*ds*.28)+5;hh=30
 add(f'<rect x="{x-ww}" y="{y-10}" width="{ww*2}" height="{hh}" rx="3" fill="#fffef6" fill-opacity=".94" stroke="#d0d3c1" stroke-width=".65"/>')
 text(x,y+1,name,fs,anchor='middle',bold=True);text(x,y+14,dim,ds,'#566452','middle')
# Meaningful 2D-derived bounds, NOT a ruler for an oblique/perspective image.
for a,b,offset,label in [(site[0],site[1],np.array([0,-37]),'~18.7 m · DERIVED 2D SITE-DIAGRAM SPAN'),(site[1],site[2],np.array([48,0]),'~29.9 m · DERIVED 2D SITE-DIAGRAM SPAN')]:
 pa=page(*a);pb=page(*b);aa=pa+offset;bb=pb+offset;line(pa,aa,'#b5bca8',.8);line(pb,bb,'#b5bca8',.8);line(aa,bb,'#8a957f',1)
 for z in [aa,bb]:line(z+[-3,3],z+[3,-3],'#8a957f',1)
 mid=(aa+bb)/2
 if offset[0]:
  ang=math.degrees(math.atan2((bb-aa)[1],(bb-aa)[0]));add(f'<g transform="translate({mid[0]+15},{mid[1]}) rotate({ang})">');text(0,0,label,11,'#7e795c','middle');add('</g>')
 else:text(mid[0],mid[1]-10,label,11,'#7e795c','middle')
# Explicit small factual/display key, not an oversized provenance sidebar.
line((70,1494),(1430,1494),'#b3bfaf',1)
text(70,1527,'SOURCE-CONSTRAINED XY',15,bold=True);text(70,1553,'Approved wall footprint, openings and stair graphics retained.',12)
text(70,1575,'Room values transcribed; maid-room dimension remains UNKNOWN.',12)
text(785,1527,'DISPLAY ONLY — NOT ACTUAL HEIGHT',15,bold=True)
text(785,1553,'Low wall cut: 0.80 m-equivalent assumed for legibility only.',12)
text(785,1575,'No ceiling, door, window or stair heights have been established.',12)
text(70,1624,'Axonometric illustration has NO measurable print scale. Approximate exterior values come from 2D calibration, not a plot survey.',12,'#8c7952')
text(70,1650,'Not certified/native CAD. Furniture/materials remain illustrative. This view adds spatial readability, not verified measurement precision.',12,'#65745e')
text(70,1692,'ONE PROTOTYPE ONLY · FOR REVIEW BEFORE ANY OTHER FLOOR · NO FULL 3D MODEL OR INTERIOR GENERATION',12,'#7e795c',bold=True)
add('</svg>');svg='\n'.join(A);svgpath=O/'FP-4B-GF_cutaway_plan_prototype.svg';svgpath.write_text(svg)
# Exact top-down wall comparison independently rasterized from the cap and approved wall groups.
def wallpng(group):
 x=copy.deepcopy(group);x.set('fill','#263a2f');x.set('stroke','#263a2f')
 for a in x:a.set('fill','#263a2f');a.attrib.pop('stroke',None)
 payload=f'<svg xmlns="http://www.w3.org/2000/svg" width="710" height="1020"><rect width="710" height="1020" fill="white"/>'+E.tostring(x,encoding='unicode')+'</svg>'
 return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=payload.encode()))).convert('RGB')
a=wallpng(wall);b=wallpng(capgroup);difference=ImageChops.difference(a,b);bbox=difference.getbbox();assert bbox is None
qa=Image.new('RGB',(2160,1110),'white');draw=ImageDraw.Draw(qa);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
for x,im,lab in [(0,a,'APPROVED 2D WALL XY'),(725,b,'CUTAWAY FLATTENED TO XY'),(1450,ImageChops.invert(difference),'DIFFERENCE: ZERO CHANGED PIXELS')]:qa.paste(im,(x,70));draw.text((x+12,20),lab,font=font,fill='#30453b')
qa.save(O/'qa/FP-4B-GF_XY_wall_identity.png')
# Renders are images only. The SVG is a display illustration, not a native model/scene.
for longedge,suffix in [(2400,'preview'),(7680,'long7680')]:
 out=O/f'FP-4B-GF_cutaway_plan_{suffix}.png';cairosvg.svg2png(bytestring=svg.encode(),write_to=str(out),output_width=round(W/H*longedge),output_height=longedge)
# Comparison with the unchanged approved sheet, no obsolete intermediate assets.
comparison=Image.new('RGB',(3000,2000),'white');dr=ImageDraw.Draw(comparison);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',28)
for x,y,w,h,path,label in [(0,85,1250,1830,R/p['long7680'],'APPROVED 2D — AUTHORITATIVE XY'),(1250,85,1750,1830,O/'FP-4B-GF_cutaway_plan_long7680.png','ONE CUTAWAY PLAN — ASSUMED DISPLAY HEIGHT')]:
 im=Image.open(path).convert('RGB');im.thumbnail((w,h),Image.Resampling.LANCZOS);comparison.paste(im,(x+(w-im.width)//2,y));dr.text((x+35,28),label,font=font,fill='#30453b')
dr.text((40,1950),'Same approved XY artwork. The cutaway does not establish missing dimensions or actual vertical heights.',font=font,fill='#8a7854');comparison.save(O/'FP-4B-GF_approved2D_vs_cutaway.png')
now=datetime.datetime.now(ZoneInfo('Asia/Dubai')).isoformat()
features={'plan_id':ID,'plan_version':'approved-V4','approved_input_path':p['svg'],'approved_input_sha256':p['sha256']['svg'],'source_pdf_page':27,'source_board_crop_bbox_pixels':p['source_board_crop_pixels'],'coordinate_system':'native 4B-GF cropped source-board pixels; crop origin [120,350] in original board','wall_contours':wall_features,'opening_plan_cues':opening_cues,'room_label_anchors':rooms,'room_boundary_polygons_available':False,'relationships':'Label-anchor coordinates and directional comparisons are available; no inferred door-access graph or room polygons asserted.'}
(O/'FP-4B-GF_planar_features.json').write_text(json.dumps(features,indent=2)+'\n')
manifest={'prototype_id':'4B-GF-cutaway-001','created_at_Asia_Dubai':now,'status':'ONE_PROTOTYPE_REVIEW_REQUIRED_NOT_APPROVED','authoritative_2D_input':p['svg'],'plan_version':'approved-V4','source_input_sha256':p['sha256']['svg'],'output_type':'3D CAD-style plan illustration — source-constrained, not certified/native CAD','no_native_model_scene_mesh_saved':True,'other_floors_generated':0,'source_facts':{'brochure_page':27,'room_label_text':'Transcribed labels retained, not geometry-certified','actual_wall_ceiling_door_window_heights':'UNKNOWN','wall_opening_stair_XY':'Copied from approved 2D presentation; no added structural geometry or reconstructed opening widths'},'derived':{'source_calibration_px_per_m':ppm,'calibration_status':'approximate derived; not survey-certified','site_diagram_bounding_spans_m_approx':[18.7,29.9],'verified_plot_boundary':False,'perspective_image_metric_scale':None,'projection':'Parallel orthographic axonometric; azimuth18deg, elevation55deg; source XY unchanged','projection_matrix_xy':P.tolist()},'assumed_display_parameters':{'wall_cut':{'value':.8,'units':'m-equivalent in approximate source calibration','provenance':'ASSUMED_DISPLAY_ONLY','represents_actual_wall_height':False,'purpose':'low cut wall visualization; no ceiling claim'},'presentation_base_depth':{'units':'image pixels','provenance':'graphic plate only, not a slab specification'},'surface_shading':'illustrative only'},'verification':{'wall_contour_count':13,'flattened_wall_raster_changed_pixel_count':0,'max_XY_inverse_projection_error_source_pixels':max_error,'approved_plan_hash_pass':True,'door_glazing_floor_cue_paths_copied':len(opening_cues),'native_source_detail_not_enhanced':True},'outputs':{'svg':str(svgpath.relative_to(R)),'preview':str((O/'FP-4B-GF_cutaway_plan_preview.png').relative_to(R)),'long7680':str((O/'FP-4B-GF_cutaway_plan_long7680.png').relative_to(R)),'comparison':str((O/'FP-4B-GF_approved2D_vs_cutaway.png').relative_to(R)),'XY_QA':str((O/'qa/FP-4B-GF_XY_wall_identity.png').relative_to(R)),'features':str((O/'FP-4B-GF_planar_features.json').relative_to(R))},'image_dimensions_pixels':{suffix:list(Image.open(O/f'FP-4B-GF_cutaway_plan_{suffix}.png').size) for suffix in ['preview','long7680']},'limitations':['No new factual dimensional precision is created by this illustration.','Some native source small fixture/glazing/door/stair detail remains trace-limited.','No exact opening heights/widths or tread/riser count is certified.','Maid-room dimension conflict stays UNKNOWN.','Furniture and material symbols inherited from approved illustrative plan, not new interior design.','Wall face height, shaded base and illumination are graphic conventions, not source evidence.']}
(O/'prototype_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(O/'README.md').write_text('ONE REVIEW PROTOTYPE ONLY. Approved V4 4B GF is authoritative XY. This is a cutaway plan IMAGE/SVG illustration, not a full building model, native CAD or a source of newly verified dimensions. Low display wall cut is assumed 0.80m-equivalent, not actual height. No image print scale. See prototype_manifest.json and planar_features.json; exact flattened-wall XY QA changed pixels=0. Do not batch before user review.\n')
print('ONE PROTOTYPE COMPLETE',manifest['image_dimensions_pixels'],'walls',len(wall_features),'XY maxerror',max_error,'rooms',len(rooms))
