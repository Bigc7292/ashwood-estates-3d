#!/usr/bin/env python3
"""Nine source-locked vector presentation sheets, including explicit UNKNOWN exterior guides.
Original embedded raster geometry is traced; no metric geometry is inferred.
Run from archive root with .venv/bin/python. Previous prototype is preserved.
"""
from pathlib import Path
import io,json,html,hashlib,re,xml.etree.ElementTree as ET
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
import pymupdf as fitz
R=Path(__file__).resolve().parents[2]; V=R/'cad-redraw-v3'; O=V/'final'
D=fitz.open(R/'original/ashwood-residences_brochure.pdf')
NS='{http://www.w3.org/2000/svg}'
# [label, dimension transcript, x,y] anchored to actual room label area.
def room(n,v,x,y):return [n,v,x,y]
C=[
 dict(id='4B-GF',xref=313,box=[120,350,830,1370],page=27,area='263.01',site=[107,54,634,895],live=[148,164,557,813],poly=None,rooms=[],water=[[196,87,463,154],[430,410,547,514]],special=True),
 dict(id='4B-FF',xref=439,box=[980,370,1630,1370],page=28,area='260.19',site=[54,55,607,932],live=[138,141,523,844],poly=[(138,141),(497,141),(497,170),(523,170),(523,844),(367,844),(367,790),(138,790)],holes=[[369,427,520,550]],water=[[146,90,423,143],[389,428,518,535]],rooms=[
 room('MASTER SUITE','4.00 × 5.10',199,322),room('FAMILY LIVING','4.00 × 5.10',330,322),room('BEDROOM 1','4.00 × 5.10 †',460,328),room('M. DRESSING','4.00 × 3.50',207,401),room('M. BATH','4.00 × 2.70',206,478),room('CORRIDOR','3.30 × 10.10',341,539),room('LIFT','1.50 × 1.70',398,376),room('BATH 1','3.00 × 2.30 †',461,380),room('BATH 2','2.30 × 2.50',169,580),room('DRESS','1.70 × 2.00',235,583),room('BEDROOM 2','3.90 × 4.30',236,638),room('J. DRESS','2.00 × 2.80',408,596),room('J. BATH','2.50 × 2.60',486,596),room('JUNIOR SUITE','4.60 × 4.00 †',415,640),room('BALCONY','UNKNOWN',329,172),room('BALCONY','UNKNOWN',211,766),room('BALCONY','UNKNOWN',437,812)],
 conflicts=['Bedroom 1, upper bath and junior-suite overlay values differ from board labels.']),
 dict(id='4B-RF',xref=439,box=[1820,455,2300,1250],page=28,area='43.92',site=None,live=[64,30,447,761],poly=None,rooms=[room('MEP','3.80 × 15.70 †',134,421),room('LIFT','1.60 × 1.80 †',321,291),room('POWDER','1.50 × 2.40 †',223,520),room('PANTRY','2.00 × 2.40 †',268,519),room('TERRACE','UNKNOWN',273,193)],conflicts=['MEP board reads 3.00 × 12.80; overlay reads 3.80 × 15.70.','Lift and service-room labels also differ; do not resolve by scaling.']),
 dict(id='5B-GF',xref=384,box=[55,220,665,1300],page=31,area='326.01',site=[33,24,576,1034],live=[104,149,451,845],sf=1080/1024,poly=[(104,165),(451,165),(451,324),(300,324),(300,580),(329,580),(329,540),(443,540),(443,845),(326,845),(326,813),(104,813)],water=[[126,52,341,111],[310,348,435,523]],rooms=[
 room('SWIMMING POOL','9.00 × 2.50',231,81),room('LIVING / DINING','9.00 × 5.40',218,187),room('SHOW KITCHEN','5.30 × 2.70',218,330),room('PANTRY','1.70 × 2.60',155,378),room('POWDER','3.30 × 1.70',215,378),room('KITCHEN','3.50 × 3.00',165,442),room('K. STORAGE','1.70 × 1.80',183,511),room('LAUNDRY','1.70 × 1.80',184,548),room('MAID BATH','1.50 × 2.00',186,603),room('MAID ROOM','3.30 × 2.40',172,658),room('LIFT','1.60 × 1.80',230,600),room('GUEST BEDROOM','4.10 × 4.10',402,630),room('G. DRESS','2.30 × 1.60',401,663),room('G. BATH','2.15 × 2.20',403,714),room('MULTIPURPOSE','5.00 × 4.50',186,751),room('DOUBLE-HEIGHT ENTRY','3.00 × 3.40',289,727),room('OFFICE','4.00 × 4.00',390,820),room('TERRACE','UNKNOWN',214,150),room('OUTDOOR TERRACE','UNKNOWN',323,329)],conflicts=[]),
 dict(id='5B-FF',xref=384,box=[760,220,1380,1300],page=32,area='328.24',site=[34,24,577,1034],live=[105,134,452,859],sf=1080/1024,poly=[(105,134),(297,134),(297,163),(452,163),(452,859),(105,859)],holes=[[302,326,441,510]],water=[[126,52,342,111],[313,348,434,524]],rooms=[
 room('MASTER SUITE','5.30 × 5.40',173,288),room('FAMILY LIVING','4.70 × 5.40',278,288),room('LOBBY','3.20 × 1.80',199,330),room('M. DRESSING','4.10 × 5.70',160,463),room('M. BATH','4.10 × 3.20',160,516),room('CORRIDOR','1.80 × 16.00',276,463),room('LIFT','1.60 × 1.80',232,611),room('J. BATH','3.90 × 2.00',156,605),room('J. DRESSING','5.65 × 2.40',162,665),room('JUNIOR SUITE','5.65 × 4.50',172,793),room('BEDROOM 1','4.70 × 4.10',399,552),room('BATH 1','2.90 × 1.80',399,664),room('DRESS','1.80 × 1.80',359,722),room('BATH 2','2.90 × 1.80',400,723),room('BEDROOM 2','4.70 × 4.60',358,795),room('BALCONY','UNKNOWN',219,152),room('BALCONY','UNKNOWN',390,527),room('BALCONY','UNKNOWN',200,834),room('BALCONY','UNKNOWN',367,848)],conflicts=['Context pool: GF overlay says 9.00 × 2.50; FF overlay says 9.50 × 2.40.']),
 dict(id='5B-RF',xref=384,box=[1520,320,1920,1180],page=32,area='57.02',site=None,live=[19,20,387,841],poly=None,rooms=[room('MEP','3.80 × 15.70',78,473),room('LIFT','1.60 × 1.80',154,539),room('POWDER','1.50 × 2.40',154,596),room('PANTRY','2.00 × 2.40',198,595),room('TERRACE','UNKNOWN',176,216)],conflicts=[]),
 dict(id='6B-GF',xref=598,box=[0,185,595,1135],page=35,area='404.49',site=[27,29,571,896],live=[91,154,505,805],poly=[(91,168),(428,154),(428,320),(280,320),(280,528),(315,528),(315,502),(479,502),(479,708),(505,708),(505,805),(314,805),(314,744),(91,744)],water=[[109,54,318,115],[291,340,477,488]],rooms=[
 room('SWIMMING POOL','9.50 × 2.40',211,82),room('LIVING / DINING','14.80 × 5.70',191,189),room('SHOW KITCHEN','5.80 × 2.70',193,325),room('PANTRY','2.30 × 2.85',126,390),room('POWDER','3.75 × 2.00',191,371),room('KITCHEN','4.00 × 3.55',141,437),room('K. STORE','2.10 × 2.30',128,506),room('LAUNDRY','2.10 × 2.40',126,574),room('LIFT','1.90 × 1.80',209,550),room('G. STORE','1.90 × 1.70',209,594),room('SERVICE ENTRY','3.80 × 1.50',174,626),room('DRIVER BATH','1.70 × 1.40',126,673),room('DRIVER ROOM','2.20 × 2.40',130,708),room('MAID BATH','2.00 × 1.50',210,669),room('MAID ROOM','3.10 × 2.40',180,709),room('G. BATH','2.50 × 2.50',349,535),room('G. DRESSING','2.76 × 2.10',348,580),room('GUEST BEDROOM','4.20 × 4.70',411,598),room('DOUBLE-HEIGHT ENTRY','3.60 × 3.60',274,684),room('MULTIPURPOSE','4.90 × 4.00',418,659),room('OFFICE / GYM','6.90 × 4.10',420,759),room('TERRACE','UNKNOWN',369,150),room('TERRACE','UNKNOWN',373,311)],conflicts=[]),
 dict(id='6B-FF',xref=598,box=[595,185,1170,1135],page=36,area='392.33',site=[20,29,563,896],live=[82,135,490,831],poly=[(82,135),(267,135),(267,154),(418,154),(418,318),(270,318),(270,526),(305,526),(305,502),(490,502),(490,831),(302,831),(302,764),(82,764)],water=[[100,54,309,115],[281,339,467,488]],rooms=[
 room('MASTER SUITE','5.70 × 5.70',137,283),room('FAMILY LIVING','4.80 × 5.70',246,283),room('LOBBY','3.80 × 1.90',164,330),room('M. DRESSING','4.00 × 6.00',132,459),room('M. BATH','4.00 × 3.50',132,506),room('LIFT','1.90 × 1.80',200,551),room('CORRIDOR','1.80 × 16.00',248,456),room('BATH 1','2.80 × 2.40',119,600),room('DRESSING','2.80 × 2.40',179,600),room('BEDROOM 1','6.00 × 5.00',203,650),room('JUNIOR SUITE','5.30 × 4.70',420,517),room('J. BATH','2.40 × 2.40',339,537),room('J. DRESS','2.70 × 2.30',338,584),room('BATH 2','2.10 × 2.75',328,687),room('DRESS 2','1.70 × 2.90',373,687),room('BEDROOM 2','3.85 × 4.00',373,724),room('DRESS 3','1.70 × 2.90',429,687),room('BATH 3','2.05 × 2.65',471,687),room('BEDROOM 3','3.80 × 4.00',424,724),room('BALCONY','UNKNOWN',177,153),room('TERRACE','UNKNOWN',357,151),room('TERRACE','UNKNOWN',339,311),room('BALCONY','UNKNOWN',420,495),room('BALCONY','UNKNOWN',146,762),room('BALCONY','UNKNOWN',385,820)],conflicts=[]),
 dict(id='6B-RF',xref=598,box=[1270,280,1720,1050],page=36,area='55.88',site=None,live=[24,25,428,743],poly=None,rooms=[room('MEP 1','3.80 × 15.70',68,382),room('MEP 2','UNREADABLE',236,606),room('LIFT','1.60 × 1.80',144,455),room('POWDER','1.50 × 2.40 †',143,494),room('PANTRY','2.00 × 2.40 †',186,494),room('TERRACE','UNKNOWN',167,197)],conflicts=['Second MEP-zone board dimension is too blurred to verify.','Service-room board labels differ/are unclear; overlay values retained with †.'])]
# All metric figures are literal source transcripts, never geometry calibration.
parts=[];metrics={}
def put(s):parts.append(s)
def rect(x,y,w,h,c,stroke='none',sw=.5):put(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" stroke="{stroke}" stroke-width="{sw}"/>')
def text(x,y,s,size=8,col='#33463e',anchor='start',weight='normal'):
 put(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" fill="{col}" text-anchor="{anchor}" font-weight="{weight}">{html.escape(s)}</text>')
def line(x1,y1,x2,y2,c='#8c9b90',sw=.5,dash=''):
 put(f'<path d="M{x1},{y1}L{x2},{y2}" fill="none" stroke="{c}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def trace(a,name,c,stroke='none',sw=.3,area=.4,eps=.3,opacity=1):
 cs,hi=cv2.findContours(a.astype(np.uint8)*255,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
 if hi is None:return
 put(f'<g id="{name}" transform="translate(.5,.5)" fill="{c}" fill-rule="evenodd" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" opacity="{opacity}">');cnt=0
 def path(c):
  q=cv2.approxPolyDP(c,eps,True).reshape(-1,2)
  return 'M'+'L'.join(f'{x},{y}' for x,y in q)+'Z'
 for i,c0 in enumerate(cs):
  if hi[0,i,3]!=-1 or abs(cv2.contourArea(c0))<area:continue
  if len(c0)==1:continue
  d=path(c0);child=hi[0,i,2]
  while child!=-1:
   if abs(cv2.contourArea(cs[child]))>=area:d+=path(cs[child])
   child=hi[0,child,0]
  put(f'<path d="{d}"/>');cnt+=1
 put('</g>');metrics[name]=cnt

def guides(c,w,h):
 """Source-pixel guide positions only. Every metric length explicitly UNKNOWN."""
 x0,y0,x1,y1=c['live'];col='#7f8f87'
 # Four exterior alignment chains. Stations are source-visible wall/return alignments,
 # not inferred metric lengths. Overall and every station span are explicitly unknown.
 title='ROOF ENVELOPE' if c['id'].endswith('RF') else 'BUILDING EXTENT'
 stations={
 '4B-GF':([148,190,315,410,557],[164,190,335,532,692,813]),
 '4B-FF':([138,269,369,523],[141,195,347,550,790,844]),
 '4B-RF':([64,194,297,447],[30,110,264,475,630,761]),
 '5B-GF':([104,249,327,451],[149,322,544,696,845]),
 '5B-FF':([105,248,330,452],[134,305,542,694,859]),
 '5B-RF':([19,135,225,387],[20,78,274,510,634,841]),
 '6B-GF':([91,234,315,428,505],[154,300,504,648,744,805]),
 '6B-FF':([82,221,305,418,490],[135,302,503,616,764,831]),
 '6B-RF':([24,118,209,391,428],[25,76,259,435,518,646,743])}
 xs,ys=stations[c['id']];sf=c.get('sf',1);xs=[q*sf for q in xs];ys=[q*sf for q in ys]
 # These source alignments extend internal and exterior wall returns as guide stations;
 # they must not be interpreted as a surveyed polygonal plot-perimeter chain.
 for top in [True,False]:
  yy=y0-16 if top else y1+16;yy2=yy-17 if top else yy+17
  line(x0,yy,x1,yy,col,.7)
  for xx in xs:
   line(xx,(y0 if top else y1),xx,yy2,col,.35);line(xx-2,yy+2,xx+2,yy-2,col,.8)
  for a,z in zip(xs,xs[1:]):text((a+z)/2,yy-4,'UNKNOWN',5.2,col,'middle')
  line(x0,yy2,x1,yy2,col,.7)
  for xx in [x0,x1]:line(xx-2,yy2+2,xx+2,yy2-2,col,.8)
  text((x0+x1)/2,yy2-4,title+' · OVERALL UNKNOWN m',5.7,col,'middle')
 for left in [True,False]:
  xx=x0-16 if left else x1+16;xx2=xx-17 if left else xx+17
  line(xx,y0,xx,y1,col,.7)
  for yy in ys:
   line((x0 if left else x1),yy,xx2,yy,col,.35);line(xx-2,yy+2,xx+2,yy-2,col,.8)
  for a,z in zip(ys,ys[1:]):
   put(f'<text x="{xx-4}" y="{(a+z)/2}" transform="rotate(-90 {xx-4} {(a+z)/2})" font-family="sans-serif" font-size="5.2" fill="{col}" text-anchor="middle">UNKNOWN</text>')
  line(xx2,y0,xx2,y1,col,.7)
  for yy in [y0,y1]:line(xx2-2,yy+2,xx2+2,yy-2,col,.8)
  put(f'<text x="{xx2-4}" y="{(y0+y1)/2}" transform="rotate(-90 {xx2-4} {(y0+y1)/2})" font-family="sans-serif" font-size="5.7" fill="{col}" text-anchor="middle">{title} · OVERALL UNKNOWN m</text>')
 # Site outline is taken only from source GF/FF. Roof source does not establish plot bounds.
 if c['site']:
  a,b,z,t=c['site'];cc='#b09263'
  for yy,edge in [(b-42,b),(t+42,t)]:
   line(a,yy,z,yy,cc,.5)
   for xx in [a,z]:line(xx,edge,xx,yy,cc,.35);line(xx-2,yy+2,xx+2,yy-2,cc,.6)
   text((a+z)/2,yy-4,'SITE OUTLINE · UNKNOWN m',5.1,cc,'middle')
  for xx,edge in [(a-42,a),(z+42,z)]:
   line(xx,b,xx,t,cc,.5)
   for yy in [b,t]:line(edge,yy,xx,yy,cc,.35);line(xx-2,yy+2,xx+2,yy-2,cc,.6)
   put(f'<text x="{xx-4}" y="{(b+t)/2}" transform="rotate(-90 {xx-4} {(b+t)/2})" font-family="sans-serif" font-size="5.1" fill="{cc}" text-anchor="middle">SITE OUTLINE · UNKNOWN m</text>')
 else:text(w/2,h+40,'PLOT BOUNDARY NOT SHOWN / NOT ESTABLISHED',6,'#aa895b','middle')

def render(c):
 global parts,metrics
 parts=[];metrics={};id=c['id'];special=c.get('special',False)
 raw=Image.open(io.BytesIO(D.extract_image(c['xref'])['image'])).convert('RGB').crop(c['box']);im=np.array(raw);h,w=im.shape[:2]
 raw.save(V/f'source/FP-{id}_untouched_board_crop.png')
 g=cv2.cvtColor(im,cv2.COLOR_RGB2GRAY);sat=im.max(2)-im.min(2);sf=c.get('sf',1)
 # Convert manually reviewed display anchors to native pixels uniformly.
 c=dict(c);c['rooms']=[[a,b,x*sf,y*sf] for a,b,x,y in c['rooms']]
 if sf!=1:
  c['live']=[v*sf for v in c['live']]
  c['poly']=[(x*sf,y*sf) for x,y in c['poly']] if c.get('poly') else None
  c['water']=[[v*sf for v in q] for q in c.get('water',[])]
  c['holes']=[[v*sf for v in q] for q in c.get('holes',[])]
 # Adequate drawing margin reserves all four exterior dimension lanes.
 margin=78;S=min(860/(w+2*margin),1190/(h+2*margin));tx=52+margin*S+(860-(w+2*margin)*S)/2;ty=128+margin*S+(1190-(h+2*margin)*S)/2
 put('<svg xmlns="http://www.w3.org/2000/svg" width="1680" height="1440" viewBox="0 0 1680 1440">')
 put('<metadata>Source-raster vector tracing; no inferred metric scale; all perimeter lengths unknown. Not native or survey CAD.</metadata>')
 rect(0,0,1680,1440,'white');text(46,43,'ASHWOOD ESTATES',24,weight='bold')
 floor={'GF':'GROUND FLOOR','FF':'FIRST FLOOR','RF':'ROOF FLOOR'}[id[-2:]]
 text(46,73,f'{id[0]}-BEDROOM VILLA  /  {floor}',14)
 text(1634,44,'CAD-STYLE VECTOR PRESENTATION',11,anchor='end',weight='bold')
 text(1634,69,'SOURCE-LIMITED  ·  NOT NATIVE / SURVEY CAD',9,'#91764f','end');line(46,96,1634,96,'#3d5448',1.2)
 put(f'<g id="drawing" transform="translate({tx},{ty}) scale({S})">')
 if special:
  rt=ET.fromstring((V/'svg/FP-4B-GF_full_plan_vector_trace.svg').read_text());gp=rt.find(f'{NS}g[@id="plan"]')
  for el in gp:put(ET.tostring(el,encoding='unicode').replace('SEE NOTE 01','UNKNOWN*'))
  text(445,588,'4.60 × 3.40 m',4.3,anchor='middle');text(496,664,'2.90 × 1.70 m',4.2,anchor='middle')
 else:
  labelmask=np.zeros((h,w),np.uint8)
  for name,dim,x,y in c['rooms']:
   ww=max(25,min(44,max(len(name)*1.3,len(dim)*1.25)))
   cv2.rectangle(labelmask,(round(x-ww),round(y-7)),(round(x+ww),round(y+11)),255,-1)
  allowed=labelmask==0
  # Layer 1: all source-supported neutral surface silhouettes. Source white is not erased.
  neutral=(sat<16)&allowed
  trace(neutral&(g>=211)&(g<240),'source_floor_and_surface_shapes','#efeee6',area=1,eps=.35)
  trace(neutral&(g>=185)&(g<211),'source_secondary_shading','#cbd2c4',area=.5,eps=.35)
  # Full source linework before structural classification; zero-area lines retained with stroke.
  trace(neutral&(g<185),'source_fine_linework','#718176','#718176',.36,area=0,eps=.3)
  # Original source furniture silhouettes remain white, outlined from their actual source boundary.
  # A >239 mask is bounded by nearby midtone source surfaces; isolated paper regions are ignored.
  white=((sat<15)&(g>239)&allowed).astype(np.uint8)*255
  cs,_=cv2.findContours(white,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
  fmask=np.zeros((h,w),np.uint8)
  for co in cs:
   ar=cv2.contourArea(co)
   if 2<ar<2500:
    x,y,ww,hh=cv2.boundingRect(co)
    if x>3 and y>3 and x+ww<w-3 and y+hh<h-3:cv2.drawContours(fmask,[co],-1,255,-1)
  
  stair_boxes={'4B-FF':(269,401,318,588),'4B-RF':(197,317,243,486),'5B-GF':(224,432,268,608),'5B-FF':(230,413,269,571),'5B-RF':(139,321,178,509),'6B-GF':(190,398,238,530),'6B-FF':(178,359,217,530),'6B-RF':(122,278,165,436)}
  if id in stair_boxes:
   a,b,z,t=stair_boxes[id];fmask[b:t,a:z]=0
  aa,bb,zz,tt=[round(q) for q in c['live']]
  foreground=np.zeros((h,w),bool);foreground[bb:tt,aa:zz]=True
  trace((fmask>0)&allowed&foreground,'source_furnishings','#fffefa','#a4afa2',.32,area=1,eps=.35)
  # Source vegetation colour is independent of architectural classification.
  plant=(im[:,:,0].astype(int)>im[:,:,2].astype(int)+5)&(im[:,:,1]>=im[:,:,0])&allowed
  for lev,col in [(245,'#dce5cf'),(220,'#c3d0ad'),(202,'#abbf96'),(183,'#8fa77f'),(165,'#778f6c')]:
   trace(plant&(g<lev),f'landscape_{lev}',col,area=1.5,eps=.45)
  # Source pools/courtyard water: closed coloured base; no knockout whites.
  for k,q in enumerate(c.get('water',[])):
   x0,y0,x1,y1=[round(t) for t in q];water=np.zeros((h,w),np.uint8);water[y0:y1,x0:x1]=255
   # Source pools are rectangles; courtyard source may contain a planter. Source green reinstated below.
   rect(x0,y0,x1-x0,y1-y0,'#bfdddf','#8dafaf',.6)
   for lo,hi,col in [(0,170,'#a8cdd1'),(170,188,'#b3d5d7'),(202,220,'#c9e3e3')]:
    trace((water>0)&(g>=lo)&(g<hi)&allowed,f'water_{k}_{lo}',col,area=1.5,eps=.4)
   trace((water>0)&plant,f'water_{k}_source_planting','#a9ba94',area=1.5,eps=.4)
   # Retain source neutral planter rims and objects, not geometry from a style sample.
   trace((water>0)&(sat<14)&(g<190)&allowed,f'water_{k}_source_detail','#879b8a','#879b8a',.3,area=0,eps=.3)
  # Recover every source-supported stair tread, using a strong full-width horizontal
  # contrast peak rather than discarding one-pixel source lines as zero-area contours.
  if id in stair_boxes:
   aa,bb,zz,tt=stair_boxes[id]
   scores=[]
   for yy in range(max(1,bb),min(h-1,tt)):
    row=g[yy,aa+2:zz-2].astype(float)
    neighbors=(g[yy-1,aa+2:zz-2].astype(float)+g[yy+1,aa+2:zz-2].astype(float))/2
    if len(row) and np.mean(neighbors-row>7)>.44 and row.mean()<245:scores.append(yy)
   # Adjacent antialias rows are a single observed source tread, not additional steps.
   kept=[]
   for yy in scores:
    if kept and yy-kept[-1]<3:
     if g[yy,aa+2:zz-2].mean()<g[kept[-1],aa+2:zz-2].mean():kept[-1]=yy
    else:kept.append(yy)
   for yy in kept:line(aa+1,yy,zz-1,yy,'#8b9b8c',.5)
   metrics['source_stair_tread_rows']=kept
  # A separate source-only vehicle trace is not classified as architecture.
  carboxes={'5B-GF':(48,890,266,1019),'6B-GF':(39,793,224,887)}
  if id in carboxes:
   aa,bb,zz,tt=carboxes[id];car=np.zeros((h,w),bool);car[bb:tt,aa:zz]=True
   trace(car&(g<235)&(sat<16),'source_vehicle_detail','#9eafa0','#9eafa0',.32,area=0,eps=.3)
  # Main-floor wall poché: source-only grey pixels, spatially separated from lower-floor context.
  live=np.zeros((h,w),np.uint8)
  if c.get('poly'):cv2.fillPoly(live,[np.array(c['poly'],np.int32)],255)
  else:
   a,b,z,t=[round(t) for t in c['live']];live[b:t,a:z]=255
  for a,b,z,t in c.get('holes',[]):live[round(b):round(t),round(a):round(z)]=0
  candidate=(g>=115)&(g<186)&(sat<17)&(live>0)&allowed
  n,lab,stats,cent=cv2.connectedComponentsWithStats(candidate.astype(np.uint8),8)
  walls=np.zeros_like(candidate)
  for i in range(1,n):
   a,b,ww,hh,area=stats[i]
   if area>=15 and ww>=2 and hh>=2:walls[lab==i]=True
  trace(walls,'source_wall_poche','#35463c','#35463c',.5,area=1,eps=.4)
  qa=im.copy();qa[walls]=(qa[walls]*.3+np.array([220,50,35])*.7).astype(np.uint8)
  Image.fromarray(qa).save(O/f'qa/FP-{id}_wall_selection.png')
  # Crisp room transcripts are placed in their own source-label areas.
  for name,dim,x,y in c['rooms']:
   ww=max(25,min(44,max(len(name)*1.3,len(dim)*1.25)))
   rect(x-ww,y-7,2*ww,18,'#f1efe7')
   fs=min(5.4,72/max(12,len(name))*1.0)
   text(x,y,name,fs,anchor='middle',weight='bold')
   text(x,y+7,dim+(' m' if re.search(r'\d',dim) else ''),4.8,'#52685a','middle')
 guides(c,w,h)
 put('</g>')
 # Side panel and source transcription table.
 X=980;E=1634
 text(X,135,'DRAWING / SOURCE RECORD',13,weight='bold');line(X,150,E,150,'#c4cfc2',.7)
 for y,a,b in [(176,'SOURCE',f'Brochure page {c["page"]} · embedded board xref {c["xref"]}'),(200,'FLOOR',f'{id[0]}-bedroom villa · {floor.lower()}'),(224,'NATIVE INPUT',f'{w} × {h} pixels · raster-origin geometry'),(248,'RENDER', '7680px long edge · vector render, not new measured detail')]:
  text(X,y,a,8,'#788a79',weight='bold');text(X+117,y,b,10)
 text(X,290,'PERIMETER / EXTERIOR DIMENSIONS',13,weight='bold')
 rect(X,306,E-X,82,'#faf5e9','#dac9a7',.6)
 text(X+13,327,'ALL METRIC PERIMETER LENGTHS: UNKNOWN',11,'#907441',weight='bold')
 text(X+13,348,'Building/roof extents and four-side exterior guides are shown.',9)
 text(X+13,366,'Site outline ≠ verified plot boundary; plot lengths are not supplied.',9)
 text(X,417,'ROOM DIMENSIONS · BROCHURE TRANSCRIPT',12,weight='bold')
 text(X,437,'Clean labels are anchored to their corresponding source rooms.',9,'#6d7e6d')
 rows=c['rooms']
 if special:
  rows=[room('Swimming pool','9.50 × 2.40',0,0),room('Living / dining','12.40 × 5.10',0,0),room('Show kitchen','5.70 × 2.70',0,0),room('Pantry','1.70 × 2.45',0,0),room('Powder','3.65 × 1.70',0,0),room('Kitchen','4.00 × 3.00',0,0),room('Laundry','2.20 × 1.80',0,0),room('Kitchen storage','2.20 × 1.40',0,0),room('Office / gym','4.60 × 3.40',0,0),room('Bath','2.90 × 1.70',0,0),room('Double-height entry','3.29 × 3.30',0,0),room('Multipurpose','4.60 × 3.90',0,0),room('Dress','1.90 × 1.10',0,0),room('Maid room','UNKNOWN *',0,0),room('Maid bath','1.70 × 1.90',0,0),room('Lift','1.50 × 1.70',0,0)]
 # Avoid cluttering the room table with unmeasured balcony repetitions.
 table=[r for r in rows if not r[0].startswith(('BALCONY','TERRACE','OUTDOOR'))]
 rowheight=min(27,540/max(1,len(table)))
 for i,(a,b,_,_) in enumerate(table):
  yy=470+i*rowheight
  if i%2==0:rect(X,yy-17,E-X,rowheight,'#f4f6ef')
  text(X+9,yy,a,10);text(E-10,yy,b+(' m' if re.search(r'\d',b) else ''),10,anchor='end')
 y=470+len(table)*rowheight+15
 text(X,y,'FLOOR AREA (brochure schedule)',9,'#71826f');text(E-10,y,c['area']+' m²',12,anchor='end',weight='bold')
 # Consistent limitations panel; table ends before y1100 even largest schedule.
 Y=max(1090,y+45);text(X,Y,'SOURCE LIMITATIONS / MISSING MEASUREMENTS',11,'#927744',weight='bold')
 notes=['No plot-side lengths, setbacks or overall building lengths supplied.',
 'No metric perimeter chain is inferred from room sizes or floor areas.',
 'UNKNOWN chains use source wall alignments; schematic, NTS.',
 'Room values transcribe brochure labels, not a dimensional survey.',
 '† Source layers disagree or are unclear; do not resolve by scaling.',
 'Furniture, stairs and doors remain source-resolution vector traces.']
 if special:notes.insert(0,'* Maid-room label conflict (2.10 × 31.10 in text layer): UNKNOWN.')
 if c.get('conflicts'):notes+=c['conflicts'][:2]
 for i,s in enumerate(notes):text(X,Y+21+i*19,s,8.6,'#677964')
 line(46,1385,1634,1385,'#3d5448',1)
 text(46,1410,f'AW-{id}  /  V03 · SOURCE-TRACED PRESENTATION',9,weight='bold')
 text(1634,1410,'NOT CONSTRUCTION DOCUMENTATION · ZIP HELD · NO 3D',8.5,anchor='end')
 put('</svg>');svg='\n'.join(parts);sp=O/f'svg/FP-{id}_CAD_style_sheet.svg';sp.write_text(svg)
 doc=fitz.open(stream=svg.encode(),filetype='svg');p=doc[0]
 for edge,suf in [(2000,'preview'),(7680,'long7680')]:
  p.get_pixmap(matrix=fitz.Matrix(edge/1680,edge/1680),alpha=False).save(O/f'png/FP-{id}_CAD_style_sheet_{suf}.png')
 # Standalone plan with all dimension guides, identical coordinates to source crop plus margin.
 rt=ET.fromstring(svg);draw=rt.find(f'{NS}g[@id="drawing"]');draw.attrib.pop('transform');draw.set('transform',f'translate({margin},{margin})')
 standalone=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w+2*margin}" height="{h+2*margin}"><rect width="100%" height="100%" fill="white"/>'+ET.tostring(draw,encoding='unicode')+'</svg>'
 (O/f'svg/FP-{id}_CAD_style_plan.svg').write_text(standalone)
 pp=fitz.open(stream=standalone.encode(),filetype='svg')[0];sc=7680/max(pp.rect.width,pp.rect.height)
 pp.get_pixmap(matrix=fitz.Matrix(sc,sc),alpha=False).save(O/f'png/FP-{id}_CAD_style_plan_long7680.png')
 # Actual PDF text span bounds detect clipped titles/notes/footers.
 pd=fitz.open('pdf',doc.convert_to_pdf());out=[]
 for b in pd[0].get_text('dict')['blocks']:
  for l in b.get('lines',[]):
   for t in l['spans']:
    a,b,z,t1=t['bbox']
    if a<0 or b<0 or z>1680 or t1>1440:out.append(t['text'])
 # Source-aligned comparison, same source-native coordinates; exterior guides excluded here.
 testdraw=rt.find(f'{NS}g[@id="drawing"]');testdraw.set('transform','translate(0,0)')
 testsvg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="white"/>'+ET.tostring(testdraw,encoding='unicode')+'</svg>'
 pix=fitz.open(stream=testsvg.encode(),filetype='svg')[0].get_pixmap(alpha=False)
 new=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
 side=Image.new('RGB',(w*2+30,h+60),'white');side.paste(raw,(0,40));side.paste(new,(w+30,40));dd=ImageDraw.Draw(side)
 ff=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
 dd.text((5,8),id+' · UNTOUCHED SOURCE',font=ff,fill='#405640');dd.text((w+35,8),'SOURCE-LOCKED VECTOR PRESENTATION',font=ff,fill='#405640');side.save(O/f'qa/FP-{id}_source_vs_vector.png')
 # Check exact native source input and literal source dimension pairs (where not unreadable).
 src=D[c['page']-1].get_text();pairs=[]
 for name,dim,x,y in rows:
  nums=re.findall(r'\d+\.\d+',dim)
  if len(nums)==2:pairs.append({'room':name,'value':dim,'numbers_in_page_text':all(n in src for n in nums)})
 rec={'id':id,'page':c['page'],'xref':c['xref'],'source_board_crop_pixels':c['box'],'native_crop_size':[w,h],
 'svg_sheet':str(sp.relative_to(R)),'svg_plan':str((O/f'svg/FP-{id}_CAD_style_plan.svg').relative_to(R)),
 'sheet_preview':str((O/f'png/FP-{id}_CAD_style_sheet_preview.png').relative_to(R)),
 'method':'Geometry-locked raster-origin vector contour layers; source-aligned text transcriptions. No embedded image in SVG.',
 'exterior':{'building_metric_lengths_sourced':0,'building_guide_sides_unknown':4,'site_metric_lengths_sourced':0,'site_guide_sides_unknown':4 if c['site'] else 0,'plot_boundary_established':False,'roof_plot_not_shown':c['site'] is None},
 'source_limited':True,'native_CAD':False,'metric_scale_established':False,'room_transcripts':rows,'dimension_text_checks':pairs,
 'text_outside_sheet':out,'embedded_rasters':len(rt.findall('.//'+NS+'image')),'layer_counts':metrics,'conflicts':c.get('conflicts',[])}
 (O/f'reports/FP-{id}_record.json').write_text(json.dumps(rec,indent=2));print(id,'rendered','clipped',out,'rooms',len(rows),flush=True)
 return rec

if __name__=='__main__':
 records=[render(c) for c in C]
 (O/'reports/nine_plan_manifest.json').write_text(json.dumps({'source_sha256':hashlib.sha256((R/'original/ashwood-residences_brochure.pdf').read_bytes()).hexdigest(),'status':'9 SOURCE-LIMITED PRESENTATION SHEETS; NOT NATIVE CAD','records':records},indent=2))
 # Nine-sheet overview, villas in columns and floors in rows.
 thumbw=680;thumbh=620;sheet=Image.new('RGB',(thumbw*3,thumbh*3+85),'white');dd=ImageDraw.Draw(sheet)
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',23)
 dd.text((25,15),'ASHWOOD · NINE SOURCE-TRACED CAD-STYLE PRESENTATIONS',font=font,fill='#334c3a')
 dd.text((25,48),'4 / 5 / 6-bedroom columns · ground / first / roof rows · all exterior metric lengths UNKNOWN',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17),fill='#8d774f')
 for rec in records:
  id=rec['id'];col=int(id[0])-4;row={'GF':0,'FF':1,'RF':2}[id[-2:]]
  im=Image.open(R/rec['sheet_preview']);im.thumbnail((thumbw-15,thumbh-20));sheet.paste(im,(col*thumbw+(thumbw-im.width)//2,85+row*thumbh));
 sheet.save(O/'previews/ALL_NINE_CAD_STYLE_OVERVIEW.png')
 print('All nine rendered. Inspect every preview and comparison before declaring visual checks complete.')
