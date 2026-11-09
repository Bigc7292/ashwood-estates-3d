#!/usr/bin/env python3
"""Re-runnable prototype checks. This does not certify semantic completeness or dimensions."""
from pathlib import Path
import xml.etree.ElementTree as ET
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import pymupdf as fitz
ROOT=Path(__file__).resolve().parents[2]; O=ROOT/'cad-redraw-v3';NS='{http://www.w3.org/2000/svg}'
p=O/'svg/FP-4B-GF_vector_prototype.svg';s=p.read_text();root=ET.fromstring(s)
plan=root.find(f'{NS}g[@id="plan"]');assert plan is not None
plan.attrib.pop('transform')
standalone=f'<svg xmlns="http://www.w3.org/2000/svg" width="710" height="960" viewBox="0 0 710 960"><rect width="710" height="960" fill="white"/>'+ET.tostring(plan,encoding='unicode')+'</svg>'
(O/'svg/FP-4B-GF_full_plan_vector_trace.svg').write_text(standalone)
d=fitz.open(stream=standalone.encode(),filetype='svg')
d[0].get_pixmap(matrix=fitz.Matrix(8,8),alpha=False).save(O/'png/FP-4B-GF_full_plan_vector_trace_7680.png')
pix=d[0].get_pixmap(alpha=False);a=np.frombuffer(pix.samples,np.uint8).reshape(pix.height,pix.width,3).copy()
Image.fromarray(a).resize((1065,1440)).save(O/'previews/FP-4B-GF_full_plan_review.png')
# Compare identical source crop pixel coordinates, not different page framings.
source=Image.open(O/'source/FP-4B-GF_untouched_board_crop.png').convert('RGB').crop((0,0,710,960))
canvas=Image.new('RGB',(1460,1040),'white');draw=ImageDraw.Draw(canvas)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
draw.text((20,12),'UNTOUCHED EMBEDDED SOURCE',font=f,fill='#33403d')
draw.text((750,12),'SOURCE-CONSTRAINED VECTOR PROTOTYPE',font=f,fill='#33403d')
canvas.paste(source,(10,45));canvas.paste(Image.fromarray(a),(740,45))
draw.text((20,1016),'Same source-pixel coordinates; not a survey comparison. Low-resolution source limits remain.',font=small,fill='#667268')
canvas.save(O/'previews/FP-4B-GF_source_vs_vector.png')
# Pool interior must not contain opaque white knockout holes.
pool=a[90:152,199:461];white=((pool.min(2)>245)).sum()
# The wall layer is separately recoverable; compare rendered outline to recorded source mask.
wall=plan.find(f'{NS}g[@id="structural_wall_poche"]');assert wall is not None
wallsvg='<svg xmlns="http://www.w3.org/2000/svg" width="710" height="1020"><rect width="710" height="1020" fill="white"/>'+ET.tostring(wall,encoding='unicode')+'</svg>'
wp=fitz.open(stream=wallsvg.encode(),filetype='svg')[0].get_pixmap(alpha=False)
wa=np.frombuffer(wp.samples,np.uint8).reshape(wp.height,wp.width,3).min(2)<180
wm=np.array(Image.open(O/'qa/FP-4B-GF_wall_mask.png'))>0
intersection=(wa&wm).sum();union=(wa|wm).sum()
# SVG text bounding boxes from the actual render document, not guessed character counts.
full=fitz.open(stream=s.encode(),filetype='svg');pd=fitz.open('pdf',full.convert_to_pdf())
outside=[]
for b in pd[0].get_text('dict')['blocks']:
 for l in b.get('lines',[]):
  for sp in l['spans']:
   x0,y0,x1,y1=sp['bbox']
   if x0<0 or y0<0 or x1>1440 or y1>1240:outside.append(sp['text'])
checks={'status':'PARTIAL_PROTOTYPE_NOT_NINE_COMPLETED','svg_parse':True,'embedded_raster_images':len(root.findall('.//'+NS+'image')),
        'pool_white_knockout_pixels':int(white),'text_spans_outside_sheet':outside,
        'wall_source_mask_pixels':int(wm.sum()),'rendered_vector_wall_mask_iou':round(float(intersection/union),4),
        'iou_scope':'Source-selected wall pixels versus simplified vector rendering only; NOT a semantic accuracy or survey metric.',
        'source_rooms_accounted':['Swimming pool','Family living/dining','Show kitchen','Pantry','Powder','Kitchen','Laundry','K.storage','Office/gym','Bath','Double-height entrance','Multipurpose','Dress','Maid room (dimension held)','Maid bath','Lift'],
        'source_stair_tread_rows':[454,463,471,479,487,496,504,513,521,529,538,546,555,563,572],
        'uncompleted_floors':['4B-FF','4B-RF','5B-GF','5B-FF','5B-RF','6B-GF','6B-FF','6B-RF'],
        'remaining_review':['Low-resolution vehicle/furniture contours remain irregular.','Fine cupboards/fixtures and some opening strokes are approximate source traces.','No calibrated world-coordinate model or verified plot/perimeter dimensions.','No final professional or construction-grade acceptance.']}
assert white==0, 'Pool has white knockouts'
assert not outside,'Text clipped outside sheet'
assert checks['embedded_raster_images']==0
(O/'reports/verification.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2))
