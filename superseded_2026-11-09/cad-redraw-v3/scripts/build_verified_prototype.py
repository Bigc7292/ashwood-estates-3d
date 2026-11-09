#!/usr/bin/env python3
"""Source-constrained, layered SVG tracing prototype; never generates plan geometry.
Coordinates in untouched xref313 crop: board origin (120,350), size 710x1020.
Wall ROIs are manually classified, then clipped to source dark/neutral pixels.
Furniture white silhouettes and thin dark detail are independently contoured.
No bitmap is embedded in final SVG. Raster-source limitations remain.
Run: .venv/bin/python cad-redraw-v3/scripts/build_verified_prototype.py
"""
from pathlib import Path
import json,html,hashlib,io
import cv2,numpy as np
from PIL import Image,ImageDraw
import pymupdf as fitz
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'cad-redraw-v3'
# Always derive input directly from the original PDF, not a previously processed panel.
pdf=fitz.open(ROOT/'original/ashwood-residences_brochure.pdf')
embedded=pdf.extract_image(313)
board=Image.open(io.BytesIO(embedded['image'])).convert('RGB')
source_crop=board.crop((120,350,830,1370))
source_crop.save(OUT/'source/FP-4B-GF_untouched_board_crop.png')
im=np.array(source_crop)
h,w=im.shape[:2]; g=cv2.cvtColor(im,cv2.COLOR_RGB2GRAY); sat=im.max(2)-im.min(2)
parts=[]; counts={}
def put(s):parts.append(s)
def rect(x,y,w,h,fill,stroke='none',sw=.6,rx=0):
 put(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def line(x1,y1,x2,y2,col='#929b98',sw=.55,dash=''):
 put(f'<path d="M{x1},{y1}L{x2},{y2}" fill="none" stroke="{col}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def poly(points,fill,stroke='none',sw=.5):
 put(f'<polygon points="'+ ' '.join(f'{x},{y}' for x,y in points)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def text(x,y,s,size=8,col='#33413f',anchor='start',weight='normal',spacing=None):
 put(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}"'+(f' letter-spacing="{spacing}"' if spacing else '')+f'>{html.escape(s)}</text>')
def mask_rects(rs):
 a=np.zeros((h,w),np.uint8)
 for x0,y0,x1,y1 in rs:cv2.rectangle(a,(x0,y0),(x1,y1),255,-1)
 return a
def pmask(ps):
 a=np.zeros((h,w),np.uint8)
 for p in ps:cv2.fillPoly(a,[np.array(p,np.int32)],255)
 return a
def trace(mask,name,fill,stroke='none',sw=.3,minarea=.3,eps=.22):
 cs,hi=cv2.findContours(mask,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE); paths=[]
 if hi is None:return
 for i,c in enumerate(cs):
  if hi[0,i,3]!=-1 or abs(cv2.contourArea(c))<minarea:continue
  def path(c):
   q=cv2.approxPolyDP(c,eps,True).reshape(-1,2)
   return 'M'+'L'.join(f'{x},{y}' for x,y in q)+'Z'
  d=path(c);child=hi[0,i,2]
  while child!=-1:
   if abs(cv2.contourArea(cs[child]))>=minarea:d+=path(cs[child])
   child=hi[0,child,0]
  paths.append(d)
 put(f'<g id="{name}" transform="translate(.5,.5)" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" fill-rule="evenodd" stroke-linejoin="round">')
 for d in paths:put(f'<path d="{d}"/>')
 put('</g>');counts[name]=len(paths)
# Source building footprint includes the enclosed rooms, but not the front drive.
foot=[(195,188),(551,188),(551,808),(410,808),(410,713),(196,723)]
building=pmask([foot])
# Manually classified wall capture ROIs. Dark source pixels alone define edge locations.
wall_rois=[(189,222,200,475),(189,510,200,538),(196,528,224,538),
 (189,575,201,676),(190,698,201,725),(148,699,198,725),(196,716,317,726),
 (307,445,319,725),(197,627,221,635),(245,625,315,635),(256,661,266,721),
 (293,661,315,670),(245,557,254,604),(249,585,313,594),(293,590,315,603),
 (248,532,313,542),(247,375,256,449),(250,441,360,450),(299,413,306,446),
 (251,392,359,400),(351,380,362,402),(196,374,223,381),(197,331,217,341),
 (408,332,465,342),(456,335,465,393),(409,382,465,394),(408,337,417,353),
 (408,376,417,393),(531,164,556,191),(531,335,556,360),(546,189,557,807),
 (408,182,464,192),(409,530,458,541),(531,529,554,541),
 (408,537,419,641),(416,633,436,644),(459,633,552,645),
 (459,684,553,695),(458,665,466,692),(515,657,522,691),
 (408,687,435,695),(408,691,418,750),(408,759,419,808),(416,801,515,813),(537,800,552,813)]
wm=(mask_rects(wall_rois)>0)&(g<191)&(sat<18)
# Label ROIs: text alone is omitted before independent tracing and reset cleanly below.
label_rois=[(265,110,326,130),(259,209,350,229),(263,348,326,371),
 (212,400,244,423),(260,401,301,428),(229,482,273,502),(265,545,309,568),
 (265,601,308,624),(258,640,292,658),(202,658,251,686),(263,686,307,710),
 (326,650,406,676),(422,572,471,595),(475,648,519,670),(447,733,537,773),
 (425,349,455,373),(476,348,526,366),(479,161,510,173)]
labels=mask_rects(label_rois)
# White furniture silhouettes, independent of structural walls; restricted to interior.
furniture=(g>239)&(sat<10)&(building>0)&(labels==0)
# Exclude open courtyard, glazing strips, and lift shaft from furniture classification.
for x0,y0,x1,y1 in [(418,343,546,531),(409,338,460,389),(187,187,206,730),(545,180,560,810)]:
 furniture[y0:y1,x0:x1]=False
# Fine dark neutral source detail: door swings, glazing, stair treads, cupboards, fixtures.
detail=(g<211)&(sat<18)&(building>0)&(~wm)&(labels==0)
# Those local source contours must not be confused with walls; separate SVG layer.
# Explicit opening cleanup boxes refer only to source-visible door swings, not rooms.
door_boxes=[(218,505,249,537),(196,548,224,578),(218,630,245,659),
            (431,611,462,641),(376,682,409,714),(431,689,462,720)]
for x0,y0,x1,y1 in door_boxes:detail[y0:y1,x0:x1]=False
# Draw title and non-overlapping page structure.
put('<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1240" viewBox="0 0 1440 1240">')
put('<metadata>Source-constrained vector tracing prototype. Original raster xref313; not native CAD; not a measured survey. No embedded raster or external asset.</metadata>')
rect(0,0,1440,1240,'white');line(42,93,1398,93,'#304744',1.3)
text(42,43,'ASHWOOD ESTATES',23,weight='bold',spacing='1.5')
text(42,71,'4-BEDROOM VILLA  /  GROUND FLOOR',14,spacing='1')
text(1398,42,'SOURCE-CONSTRAINED VECTOR TRACE',10,anchor='end',weight='bold')
text(1398,65,'PROTOTYPE 03  ·  VISUAL REVIEW REQUIRED',9,anchor='end',col='#866c43')
# Drawing uses uniform source pixel coordinates; no world-unit calibration.
put('<g id="plan" transform="translate(-30,83) scale(1.18)">')
# Outer paving/boundary are visible in the source; no plot dimensions are inferred.
rect(107,54,527,841,'#f4f3ed','#a6ada7',.7)
# Source-supported landscaped strips and patches.
for a in [(111,59,77,65),(111,128,45,345),(111,490,79,43),(531,59,100,70),(592,135,39,393),(593,532,39,302),(151,583,39,111),(381,834,160,57)]:rect(*a,'#d4ddc4')
# Source traced planting tones retain original silhouette, never add a tree.
exterior=(building==0)
tree_roi=mask_rects([(83,39,192,150),(514,47,622,161),(103,228,180,337),(103,317,171,474),(103,477,191,568),(130,590,190,709),(585,223,648,383),(584,350,651,528),(584,518,653,690),(584,675,655,811),(589,780,660,871),(374,811,460,915)])>0
for hi,c in [(220,'#c5d1b6'),(205,'#b5c4a3'),(185,'#9eaf8c'),(165,'#849b76')]:
 m=((g<hi)&((sat>8)|tree_roi)&exterior&(np.indices((h,w))[0]<900)).astype(np.uint8)*255
 trace(m,'planting_'+str(hi),c,minarea=3,eps=.7)
# Paving joints, sampled from visible source paving boundaries.
for y in [225,253,282,310,339,367,396,424,452,481,510]:line(157,y,190,y,'#c2c7bc',.45)
for y in [133,162,191,219,247,276,305,334,362,390,418,446,474,502,530,558,586,614,642,670,698,726,754,782,810,838,866]:line(557,y,593,y,'#c2c7bc',.45)
for y in [746,774,802,830,859,887]:line(318,y,410,y,'#c2c7bc',.45)
# Source swimming pool: blue closed base means the texture has no white knockout holes.
rect(196,87,267,67,'#b7dbe0','#6f9fa7',1.1)
# Source texture traced into subtle blue vector tones; source label region excluded.
water=mask_rects([(198,89,461,152)]); water[109:132,259:332]=0
for level,c in [(172,'#b0d5dc'),(193,'#c0dfe4'),(210,'#c7e3e7')]:
 trace(((water>0)&(g>level)&(g<level+12)).astype(np.uint8)*255,'pool_texture_'+str(level),c,minarea=1.4,eps=.5)
# Pool source step/hatch area retained from neutral source detail, not an invented scale.
# Two source-visible hatched pool elements; hand digitized from the unchanged crop.
for y0,y1 in [(94,109),(132,145)]:
 rect(418,y0,41,y1-y0,'#c7e1e3','#8bafb4',.4)
 for xx in range(420,459,3):line(xx,y0,xx,y1,'#98bdc1',.4)
# Source terrace chairs/tables, contoured separately from the building furniture.
ext_furn=mask_rects([(480,90,511,153)])
trace(((ext_furn>0)&(g>238)&(sat<12)).astype(np.uint8)*255,'exterior_furniture','#fffefa','#aeb8af',.4,minarea=2,eps=.3)
trace(((ext_furn>0)&(g<241)&(sat<14)).astype(np.uint8)*255,'exterior_furniture_outlines','#a0ada2','#a0ada2',.35,minarea=0,eps=.25)
# Main interior floors: zoning fills have no structural authority.
poly(foot,'#f0eee5')
rect(251,399,106,45,'#e1ebe8');rect(260,666,49,52,'#e1ebe8');rect(465,645,82,42,'#e1ebe8')
rect(199,633,110,84,'#eee9de');rect(419,541,127,92,'#efeee4')
# Courtyard and source outdoor terrace. Water feature is not inferred room area.
rect(415,342,131,188,'#eeeee7')
rect(430,410,117,104,'#b9d9d4','#97b8af',.55)
# Source courtyard texture, bounded and never clearing pixels.
cy=mask_rects([(432,412,545,512)]);cy[436:486,458:507]=0
for level,c in [(181,'#a9c9c1'),(203,'#c8e0d8')]:
 trace(((cy>0)&(g>level)&(g<level+13)).astype(np.uint8)*255,'courtyard_texture_'+str(level),c,minarea=1,eps=.5)
# Central courtyard tree/planter exact source position and envelope.
for level,c in [(205,'#9bae92'),(182,'#879f7d')]:
 trace(((mask_rects([(443,421,526,504)])>0)&(g<level)&(sat>12)).astype(np.uint8)*255,'courtyard_plant_'+str(level),c,minarea=2,eps=.5)
rect(464,442,40,40,'#e7e5d6','#8f9c89',.7);rect(469,447,30,30,'#a8b593','#778a71',.5)
# Independently traced furnishings, then fine source linework. No raster embedded.
trace(furniture.astype(np.uint8)*255,'furniture_silhouettes','#fffefa','#b1b6ae',.35,minarea=1,eps=.28)
# Shade stairwell without covering source treads.
rect(319,451,38,122,'#eeeee8')
trace(detail.astype(np.uint8)*255,'doors_stairs_glazing_and_fine_detail','#737e78','#737e78',.38,minarea=0,eps=.3)
trace(wm.astype(np.uint8)*255,'structural_wall_poche','#34403e','#34403e',.5,minarea=2,eps=.65)
# Continuous hand-digitized glazing follows the exact source openings.
for x1,y1,x2,y2 in [(198,189,408,189),(464,189,531,189),(191,190,191,223),
 (195,190,195,223),(191,475,191,510),(195,475,195,510),
 (464,334,531,334),(464,337,531,337),(410,394,410,530),(413,394,413,530),
 (458,532,530,532),(458,537,530,537),(410,578,410,631),(414,578,414,631),
 (548,695,548,725),(552,695,552,725),(515,805,537,805),(515,808,537,808),
 (191,678,191,700),(195,678,195,700),(318,711,377,711)]:line(x1,y1,x2,y2,'#6f8179',.45)
# Door leaves/swing arcs digitized against the source; coordinate uncertainty is ~1 source pixel.
for x,y,r,kind in [(221,531,26,'up'),(197,577,25,'up'),(219,631,25,'down'),
                   (434,638,25,'up'),(405,711,27,'leftup'),(435,692,25,'down')]:
 if kind=='up':
  line(x,y,x,y-r,'#7c8980',.55)
  put(f'<path d="M{x},{y-r} A{r},{r} 0 0 1 {x+r},{y}" fill="none" stroke="#98a398" stroke-width=".4"/>')
 elif kind=='down':
  line(x,y,x,y+r,'#7c8980',.55)
  put(f'<path d="M{x},{y+r} A{r},{r} 0 0 0 {x+r},{y}" fill="none" stroke="#98a398" stroke-width=".4"/>')
 else:
  line(x,y,x,y-r,'#7c8980',.55)
  put(f'<path d="M{x-r},{y} A{r},{r} 0 0 1 {x},{y-r}" fill="none" stroke="#98a398" stroke-width=".4"/>')
# Source tread centerlines: thin zero-area contours were previously dropped by contour area filtering.
for yy in [454,463,471,479,487,496,504,513,521,529,538,546,555,563,572]:line(319,yy,358,yy,'#8b958d',.4)
line(358,447,358,574,'#8b958d',.4)
# Source parking paving (outside building); source silhouettes are never labelled as structure.
drive=mask_rects([(108,731,317,896)])
trace(((drive>0)&(g<224)&(sat<14)).astype(np.uint8)*255,'source_drive_paving_and_cars','#b4bdb2','#b4bdb2',.25,minarea=0,eps=.3)
# Vehicle geometry is traced separately and explicitly NOT classified as architecture.
car_mask=mask_rects([(157,747,212,870),(240,747,299,870)])
trace(((car_mask>0)&(g<219)&(sat<18)).astype(np.uint8)*255,'source_vehicle_linework','#99a49d','#99a49d',.42,minarea=0,eps=.25)
# Lift X is already visible in the source; crisp redraw follows its corners.
rect(416,341,40,41,'#fafaf5','#858f88',.55);line(416,341,456,382);line(456,341,416,382)
# Text anchors are tied to source labels, not the style-reference layout.
def lab(x,y,title,dim=None,size=5.5):
 text(x,y,title,size,anchor='middle',weight='bold')
 if dim:text(x,y+7,dim,size-1,anchor='middle',col='#59655e')
lab(328,117,'SWIMMING POOL','9.50 × 2.40 m',6)
lab(300,215,'FAMILY LIVING / DINING','12.40 × 5.10 m',6)
lab(296,359,'SHOW KITCHEN','5.70 × 2.70 m',5.6)
lab(229,410,'PANTRY','1.70 × 2.45 m',4.7)
lab(278,411,'POWDER','3.65 × 1.70 m',4.7)
lab(248,491,'KITCHEN','4.00 × 3.00 m',5.2)
lab(285,556,'LAUNDRY','2.20 × 1.80 m',4.8)
lab(286,612,'K. STORAGE','2.20 × 1.40 m',4.8)
lab(280,648,'DRESS','1.90 × 1.10 m',4.5)
lab(223,671,'MAID ROOM','SEE NOTE 01',4.8)
lab(284,697,'MAID BATH','1.70 × 1.90 m',4.5)
lab(365,659,'DOUBLE-HEIGHT ENTRY','3.29 × 3.30 m',4.7)
lab(445,581,'OFFICE / GYM',None,5.3)
lab(496,657,'BATH',None,4.8)
lab(480,755,'MULTIPURPOSE','4.60 × 3.90 m',5.3)
lab(436,358,'LIFT','1.50 × 1.70 m',4.3)
lab(496,358,'OUTDOOR TERRACE',None,4.4)
lab(494,166,'TERRACE',None,4.4)
# Source-supported entry labels; no north marker/scale/dimension chain is invented.
for x,s in [(216,'VEHICLE ENTRY'),(383,'PEDESTRIAN ENTRY'),(600,'SERVICE ENTRY')]:
 text(x,924,s,5.5,anchor='middle',col='#657069');line(x,904,x,913,'#657069',.7)
put('</g>')
# Panel, fully outside plan footprint.
X=815;R=1398; text(X,131,'DRAWING INFORMATION',12,weight='bold',spacing='.7');line(X,145,R,145,'#ccd3cd',.8)
for y,k,v in [(171,'SOURCE','Ashwood brochure · PDF page 27'),(194,'TYPE','4-bedroom villa · ground floor'),(217,'GEOMETRY','Traced from embedded board xref 313'),(240,'PRESENTATION','Orthographic · source pixel proportions'),(263,'STATUS','Vector-tracing prototype, not native CAD')]:
 text(X,y,k,8,weight='bold',col='#76857b');text(X+108,y,v,10)
text(X,309,'SOURCE-STATED DIMENSIONS',12,weight='bold',spacing='.7');text(X,330,'Room sizes below are transcribed, not remeasured.',9,col='#6c7770')
rows=[('Swimming pool','9.50 × 2.40 m'),('Family living / dining','12.40 × 5.10 m'),('Show kitchen','5.70 × 2.70 m'),('Pantry','1.70 × 2.45 m'),('Powder room','3.65 × 1.70 m'),('Kitchen','4.00 × 3.00 m'),('Laundry','2.20 × 1.80 m'),('Kitchen storage','2.20 × 1.40 m'),('Office / gym','4.60 × 3.40 m'),('Bath','2.90 × 1.70 m'),('Double-height entrance','3.29 × 3.30 m'),('Multipurpose room','4.60 × 3.90 m'),('Dress','1.90 × 1.10 m'),('Maid bath','1.70 × 1.90 m'),('Lift','1.50 × 1.70 m')]
for i,(a,b) in enumerate(rows):
 y=359+i*25
 if i%2==0:rect(X-2,y-16,R-X+2,24,'#f6f7f3')
 text(X+9,y,a,10);text(R-10,y,b,10,anchor='end')
text(X,765,'FLOOR AREA',8,weight='bold',col='#778679');text(R-10,765,'263.01 m²',13,anchor='end',weight='bold')
text(X,783,'Brochure schedule value; not a sum of the room rectangles.',8.5,col='#6d776f')
text(X,823,'LAYER KEY',11,weight='bold',spacing='.6')
for i,(c,s) in enumerate([('#34403e','Source-classified structural wall poché'),('#f0eee5','Interior floor · furniture independently traced'),('#e1ebe8','Wet / service-zone presentation tint'),('#b7dbe0','Source pool and courtyard water feature'),('#a8b593','Source-traced planting and landscape')]):
 y=850+23*i;rect(X,y-10,17,12,c,'#b9c3b8',.5);text(X+29,y,s,9)
text(X,995,'READ BEFORE USE',11,weight='bold',col='#886c40')
notes=['01  Maid-room dimension conflicts with brochure text layer.',
       '     A repeated “31.10 m” value is not treated as verified.',
       '02  No supported overall dimension chain or north bearing.',
       '     Drawing is NTS; no reference scale bar is copied.',
       '03  Furniture, doors and stairs are source-raster contours.',
       '     Fine detail remains limited by native source resolution.',
       '04  No geometry, watermark or labels copied from style example.']
for i,s in enumerate(notes):text(X,1018+19*i,s,9,col='#68746d')
line(42,1182,1398,1182,'#304744',1)
text(42,1208,'AW-4B-GF  /  V03-PROTOTYPE',9,weight='bold')
text(1398,1208,'NOT CONSTRUCTION DOCUMENTATION  ·  NO SURVEY / SCALE CERTIFICATION',8.5,anchor='end',col='#6b766e')
put('</svg>')
svg='\n'.join(parts); path=OUT/'svg/FP-4B-GF_vector_prototype.svg';path.write_text(svg)
# Source-aligned QA overlay; red means vector wall mask, not generated wall geometry.
qa=im.copy();qa[wm]=(qa[wm]*.35+np.array([210,45,35])*.65).astype(np.uint8)
Image.fromarray(qa).save(OUT/'qa/FP-4B-GF_wall_classification_overlay.png')
Image.fromarray(wm.astype(np.uint8)*255).save(OUT/'qa/FP-4B-GF_wall_mask.png')
# Render true vectors at both review and requested long-edge resolution.
d=fitz.open(stream=svg.encode(),filetype='svg');p=d[0]
for longedge,suffix in [(1800,'review'),(7680,'long7680')]:
 pix=p.get_pixmap(matrix=fitz.Matrix(longedge/max(p.rect.width,p.rect.height),longedge/max(p.rect.width,p.rect.height)),alpha=False)
 pix.save(OUT/f'png/FP-4B-GF_vector_prototype_{suffix}.png')
(OUT/'reports/prototype_metrics.json').write_text(json.dumps({'status':'prototype_only','assets_redrawn':1,'all_nine_completed':False,'source_xref':313,'source_crop_board_pixels':[120,350,830,1370],'crop_native_size':[w,h],'wall_pixel_count':int(wm.sum()),'wall_capture_rois':wall_rois,'layer_paths':counts,'svg_has_embedded_raster':'<image' in svg,'style_reference_sha256':hashlib.sha256((OUT/'source/style_reference.png').read_bytes()).hexdigest(),'notes':'Contours preserve source pixel geometry; not semantic editable CAD or measured survey. High-res raster is a vector render from low-resolution source trace; no architectural information is added.'},indent=2))
print(path);print(counts)
