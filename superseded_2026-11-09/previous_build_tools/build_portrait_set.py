#!/usr/bin/env python3
"""Bounded full-nine V4 portrait set. Eight hybrid source-underlay + exact existing wall-vector
sheets; source-specific clean symbol replacements. Source detail retained instead of destructive
all-contour tracing. Five approximate independent calibrations; four explicitly NTS.
"""
from pathlib import Path
import io,json,html,math,random,re,base64,shutil,hashlib,sys,xml.etree.ElementTree as E
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import pymupdf as fitz,cairosvg
R=Path('/workspace/plan-visuals-archive');O=R/'cad-visual-v4-nine';N='{http://www.w3.org/2000/svg}'
C=json.loads((O/'reports/independent_calibration.json').read_text())['floors'];old=json.loads((R/'cad-redraw-v3/final/reports/nine_plan_manifest.json').read_text())['records'];byid={r['id']:r for r in old}
# Source-specific symbol ROIs, all native cropped-source pixels. These are illustrative
# furniture footprints, not room geometry. No symbol from a different room is transplanted.
F={
'4B-FF':{'beds':[(164,237,73,65,'left'),(164,664,73,65,'left'),(414,679,82,61,'right'),(447,226,58,24,'right'),(447,278,58,24,'right')],'rugs':[(157,227,87,85),(157,653,87,82),(402,666,104,81),(440,218,69,90)],'L':[(304,210,78,96,'tr')],'round':[(326,296,13)],'coffee':[(321,247,34,34)]},
'5B-GF':{'beds':[(363,595,80,61,'right')],'rugs':[(355,584,93,78)],'dining':[(181,225,39,65,4)],'curved':[(258,213,69,66)],'L':[(363,211,85,98,'bl')],'coffee':[(398,242,30,30)],'round':[(267,242,8),(414,199,11),(439,201,7)],'cars':[(52,895,39,106),(120,895,43,106),(193,895,42,106)],'islands':[(178,317,87,21)]},
'5B-FF':{'beds':[(130,223,75,61,'left'),(131,754,76,65,'left'),(383,597,75,62,'right'),(414,799,53,22,'right'),(414,845,53,22,'right')],'rugs':[(121,211,102,84),(121,743,105,91),(374,585,88,79),(407,791,63,83)],'U':[(271,188,81,111)],'round':[(285,220,10),(298,262,14)]},
'6B-GF':{'beds':[(392,537,74,57,'right')],'rugs':[(383,526,86,74)],'dining':[(141,215,43,64,4)],'curved':[(228,203,65,69)],'L':[(327,206,83,89,'bl')],'coffee':[(362,234,29,29)],'round':[(243,239,8),(362,197,10),(388,200,6)],'cars':[(46,794,39,91),(108,794,39,91),(175,794,39,91)],'islands':[(150,295,87,19)]},
'6B-FF':{'beds':[(101,211,68,57,'left'),(102,660,79,63,'left'),(400,540,70,57,'right'),(324,746,52,47,'left'),(426,746,49,47,'right')],'rugs':[(95,201,86,77),(96,651,98,81),(391,530,85,75),(316,737,70,65),(416,737,65,65)],'U':[(230,190,77,103)],'round':[(239,219,9),(252,253,13)]},
'4B-RF':{'dining':[(198,146,29,83,4)],'L':[(314,149,84,94,'br')],'coffee':[(313,166,33,33)],'round':[(299,218,13),(329,134,11),(305,135,7)],'bars':[(107,132,27,110)]},
'5B-RF':{'dining':[(162,110,27,75,4)],'L':[(272,110,71,83,'br')],'coffee':[(272,128,29,29)],'round':[(259,170,11),(285,101,10),(263,102,6)],'bars':[(65,95,23,122)]},
'6B-RF':{'dining':[(154,107,26,66,3)],'L':[(248,109,72,73,'br')],'coffee':[(253,128,27,27)],'round':[(245,161,10),(270,101,9),(248,102,5)],'bars':[(61,93,18,88)]}}
WATER={'4B-FF':[(146,90,423,143),(389,428,518,535)],'5B-GF':[(133,55,360,118),(327,367,459,552)],'5B-FF':[(133,55,361,118),(330,367,458,553)],'6B-GF':[(109,54,318,115),(291,340,477,488)],'6B-FF':[(100,54,309,115),(281,339,467,488)]}
LIVE={'4B-FF':[138,141,523,844],'4B-RF':[64,30,447,761],'5B-GF':[110,157,476,892],'5B-FF':[111,141,477,906],'5B-RF':[19,20,387,841],'6B-GF':[91,154,505,805],'6B-FF':[82,135,490,831],'6B-RF':[24,25,428,743]}
SITE={'4B-FF':[54,55,607,932],'5B-GF':[33,24,576,1034],'5B-FF':[34,24,577,1034],'6B-GF':[27,29,571,896],'6B-FF':[20,29,563,896]}
TREE5=[(77,82,50),(512,76,52),(55,350,40),(53,523,43),(65,657,39),(66,786,37),(69,902,35),(550,371,38),(551,578,40),(551,749,39),(556,968,37),(403,1018,43)]
TREE6=[(45,49,34),(525,76,55),(40,260,29),(41,420,30),(66,670,30),(197,859,34),(362,859,43),(547,853,39),(548,275,31),(548,434,32),(550,595,33),(550,735,32)]
TREE4=[(136,93,49),(569,101,56),(132,278,41),(133,393,46),(148,522,44),(158,648,40),(613,309,42),(614,441,41),(615,574,44),(616,709,39),(626,828,36),(421,857,45)]
A=[]
def add(s):A.append(s)
def rect(x,y,w,h,c,stroke='none',sw=.5,rx=0):add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c}" stroke="{stroke}" stroke-width="{sw}"/>')
def line(a,b,c,d,col='#b3ad9c',sw=.4,opacity=1):add(f'<path d="M{a},{b}L{c},{d}" fill="none" stroke="{col}" stroke-width="{sw}" opacity="{opacity}"/>')
def path(d,fill='none',st='none',sw=.5):add(f'<path d="{d}" fill="{fill}" stroke="{st}" stroke-width="{sw}"/>')
def circle(x,y,r,c,st='none',sw=.4):add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{st}" stroke-width="{sw}"/>')
def text(x,y,t,n=7,c='#33483b',anchor='start',bold=False):add(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{n}" fill="{c}" text-anchor="{anchor}" font-weight="'+('bold' if bold else 'normal')+f'">{html.escape(t)}</text>')
def image(im,x=0,y=0,w=None,h=None,opacity=1):
 b=io.BytesIO();im.save(b,format='PNG');data=base64.b64encode(b.getvalue()).decode();add(f'<image x="{x}" y="{y}" width="{w or im.width}" height="{h or im.height}" opacity="{opacity}" xlink:href="data:image/png;base64,{data}"/>')
def floorpatch(x,y,w,h,c='#e8dfce'):
 rect(x,y,w,h,c)
 for xx in range(math.ceil(x/18)*18,int(x+w),18):line(xx,y,xx,y+h,'#c9bfaa',.25,.65)
 for yy in range(math.ceil(y/18)*18,int(y+h),18):line(x,yy,x+w,yy,'#c9bfaa',.25,.65)
def chair(x,y,w=12,h=12,rot=0):
 add(f'<g transform="translate({x},{y}) rotate({rot})">');rect(-w/2+1,-h/2+1,w,h,'#b8ad96',rx=3);rect(-w/2,-h/2,w,h,'url(#seat)','#78816e',.5,3);path(f'M{-w/2+1},{-h/2+4}Q0,{-h/2-1} {w/2-1},{-h/2+4}','none','#a5967c',.4);add('</g>')
def rug(x,y,w,h):
 floorpatch(x-1,y-1,w+2,h+2);rect(x,y,w,h,'#f0ebe0','#c1b7a1',.4,1);rect(x+2,y+2,w-4,h-4,'#e5ddca','#d2c5ad',.3,1)
def bed(x,y,w,h,head):
 rect(x+1,y+1,w,h,'#b8b49d','#828d78',.4,2);rect(x,y,w,h,'#e9e3d6','#949b87',.6,2)
 hp=max(10,w*.16);side=x+2 if head=='left' else x+w-hp-2
 rect(side,y+3,hp,h-6,'#d5c7ae','#ac9d83',.35,1)
 for yy in [y+h*.12,y+h*.54]:rect(side+1,yy,hp-2,h*.31,'#fffaf0','#bcb49f',.3,2)
 coverx=x+hp+4 if head=='left' else x+3;coverw=w-hp-7
 rect(coverx,y+3,coverw,h-6,'#e4ddcd','#c5baa2',.3,1)
 bandx=x+w-11 if head=='left' else x+5;rect(bandx,y+3,6,h-6,'#aab5a1')
 line(coverx+3,y+h*.35,coverx+coverw-2,y+h*.35,'#c8beaa',.35);line(coverx+3,y+h*.68,coverx+coverw-2,y+h*.68,'#c8beaa',.35)
def dining(x,y,w,h,count):
 # Vertical table; source-specific footprint, not copied horizontally across variants.
 for i in range(count):
  yy=y+9+(h-18)*i/max(1,count-1);chair(x-7,yy,11,11,-90);chair(x+w+7,yy,11,11,90)
 chair(x+w/2,y-7,11,11);chair(x+w/2,y+h+7,11,11,180)
 rect(x+1,y+1,w,h,'#afa58e',rx=2);rect(x,y,w,h,'#d8cbb4','#7a846d',.6,2)
 for xx in [x+w*.25,x+w*.6]:line(xx,y+2,xx-1,y+h-2,'#baaa8a',.25)
def Lsofa(x,y,w,h,orient):
 d=min(18,w*.25,h*.25);floorpatch(x-2,y-2,w+4,h+4);rect(x-1,y-1,w+2,h+2,'#ece6d8','#d7cdb7',.3,1)
 # Source sofa legs on selected real sides only; no extra seating added.
 right='r' in orient;top='t' in orient
 xx=x+w-d if right else x;yy=y if top else y+h-d
 rect(xx,y,d,h,'url(#seat)','#8c8d76',.5,2);rect(x,yy,w,d,'url(#seat)','#8c8d76',.5,2)
 for yy1 in np.linspace(y+4,y+h-d,3):rect(xx+3,float(yy1),d-6,max(8,(h-d)/3-3),'#e8dfcc','#b5a88e',.3,1)
 for xx1 in np.linspace(x+3,x+w-d,3):rect(float(xx1),yy+3,max(8,(w-d)/3-3),d-6,'#e8dfcc','#b5a88e',.3,1)
def curved(x,y,w,h,twopieces=False):
 floorpatch(x-2,y-2,w+4,h+4)
 if twopieces:
  # Two source crescent sofas face a round central table.
  path(f'M{x+w*.38},{y+8}Q{x+w*.84},{y-4} {x+w-3},{y+h*.36}L{x+w*.77},{y+h*.43}Q{x+w*.67},{y+h*.11} {x+w*.35},{y+24}Z','url(#seat)','#8d8e77',.55)
  path(f'M{x+w*.37},{y+h-9}Q{x+w*.82},{y+h+3} {x+w-3},{y+h*.63}L{x+w*.77},{y+h*.57}Q{x+w*.66},{y+h*.88} {x+w*.35},{y+h-24}Z','url(#seat)','#8d8e77',.55)
 else:
  circle(x+w*.45,y+h*.55,min(w,h)*.43,'#eee8dc','#d4cbb9',.3)
  path(f'M{x+w*.48},{y+3}Q{x+w*.95},{y+9} {x+w-2},{y+h*.62}L{x+w*.77},{y+h*.7}Q{x+w*.74},{y+22} {x+w*.38},{y+20}Z','url(#seat)','#8c8d75',.6)
  chair(x+w*.13,y+h*.35,17,17,-20)
 circle(x+w*.48,y+h*.55,11,'#d4c6ac','#8d967e',.55)
def car(x,y,w,h):
 floorpatch(x-3,y-2,w+6,h+4,'#dedfd5');add(f'<g transform="translate({x},{y})">')
 for xx in [-1,w-3]:rect(xx,21,4,13,'#47594c',rx=1);rect(xx,h-29,4,13,'#47594c',rx=1)
 path(f'M4,13Q7,0 {w/2},0Q{w-6},0 {w-3},13L{w-1},{h-13}Q{w-4},{h} {w/2},{h}Q3,{h} 2,{h-13}Z','url(#car)','#6c8171',.65)
 path(f'M7,22Q{w/2},18 {w-7},22L{w-5},39Q{w/2},35 5,39Z','#adbfba','#748c7f',.5)
 path(f'M7,{h-29}Q{w/2},{h-32} {w-7},{h-29}L{w-8},{h-17}Q{w/2},{h-13} 8,{h-17}Z','#adbfba','#748c7f',.45)
 rect(7,42,w-14,h-74,'#e8e9df','#acb9a7',.4,3);line(7,9,w-8,9,'#c0c7b7',.5);add('</g>')
def soften(im):
 a=np.array(im).astype(float);g=a.mean(2);sat=a.max(2)-a.min(2);out=a.copy();neutral=sat<17
 xp=[0,80,149,190,224,240,255];cols=np.array([[29,43,35],[64,78,62],[99,111,92],[163,169,148],[231,223,205],[246,241,230],[255,254,248]])
 for k in range(3):out[:,:,k][neutral]=np.interp(g[neutral],xp,cols[:,k])
 plant=(a[:,:,0]>a[:,:,2]+5)&(a[:,:,1]>=a[:,:,0]);z=np.clip((252-g)/70,0,1)
 for k,c in enumerate([102,133,65]):out[:,:,k][plant]=(252*(1-z)+c*z)[plant]
 return Image.fromarray(np.clip(out,0,255).astype('uint8'))
def guidance(bb,site,ppm,w,h):
 # Only actual source envelope endpoints: no invented intermediate station grid.
 a,b,z,t=bb;col='#697b6d'
 def val(n):return ('~ '+f'{n/ppm:.1f}'+' m') if ppm else 'UNKNOWN'
 for yy,edge in [(b-18,b),(t+18,t)]:
  line(a,yy,z,yy,col,.65)
  for xx in [a,z]:line(xx,edge,xx,yy,'#a8b2a1',.35);line(xx-2,yy+2,xx+2,yy-2,col,.7)
  text((a+z)/2,yy-5,'ENVELOPE '+val(z-a),7,col,'middle')
 for xx,edge in [(a-18,a),(z+18,z)]:
  line(xx,b,xx,t,col,.65)
  for yy in [b,t]:line(edge,yy,xx,yy,'#a8b2a1',.35);line(xx-2,yy+2,xx+2,yy-2,col,.7)
  cy=(b+t)/2;add(f'<text x="{xx-5}" y="{cy}" transform="rotate(-90 {xx-5} {cy})" font-family="sans-serif" font-size="7" text-anchor="middle" fill="{col}">ENVELOPE {val(t-b)}</text>')
 if site:
  a,b,z,t=site;col='#9a8358'
  for yy,edge in [(b-49,b),(t+49,t)]:
   line(a,yy,z,yy,col,.6)
   for xx in [a,z]:line(xx,edge,xx,yy,'#beb49a',.35);line(xx-2,yy+2,xx+2,yy-2,col,.7)
   text((a+z)/2,yy-5,'SITE DIAGRAM '+val(z-a),7.4,col,'middle')
  for xx,edge in [(a-49,a),(z+49,z)]:
   line(xx,b,xx,t,col,.6)
   for yy in [b,t]:line(edge,yy,xx,yy,'#beb49a',.35);line(xx-2,yy+2,xx+2,yy-2,col,.7)
   cy=(b+t)/2;add(f'<text x="{xx-5}" y="{cy}" transform="rotate(-90 {xx-5} {cy})" font-family="sans-serif" font-size="7.4" text-anchor="middle" fill="{col}">SITE DIAGRAM {val(t-b)}</text>')
 else:text(w/2,h+45,'PLOT BOUNDARY NOT SHOWN / NOT ESTABLISHED',6.5,'#8f7645','middle')

def build(id):
 global A;A=[];rec=byid[id];data=F[id];cal=C[id];ppm=cal['px_per_m'];raw=Image.open(R/f'cad-redraw-v3/source/FP-{id}_untouched_board_crop.png').convert('RGB');w,h=raw.size
 rt=E.fromstring((R/rec['svg_plan']).read_text());draw=rt.find(N+'g');wall=draw.find(N+'g[@id="source_wall_poche"]');floor=draw.find(N+'g[@id="source_floor_and_surface_shapes"]')
 assert wall is not None
 # Pick physical paper only after calibration; never shrink to fit and retain a scale claim.
 if ppm:
  needw=w*10/ppm+65;needh=h*10/ppm+65
  paper=(297,420) if needw<=297 and needh<=420 else (420,594)
  sc=(10/ppm)/(paper[0]/1000)
 else:paper=(297,420);sc=min(835/(w+120),1160/(h+140))
 H=paper[1]/paper[0]*1000;tx=(790-w*sc)/2+30;ty=84
 # Keep all external guides comfortably within page; scaled view position, never scale itself.
 tx=max(tx,60-(-15)*sc);ty=max(ty,77)
 add(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{paper[0]}mm" height="{paper[1]}mm" viewBox="0 0 1000 {H}">')
 add('''<defs><linearGradient id="seat" x1="0" x2="1"><stop stop-color="#d5c8b0"/><stop offset=".45" stop-color="#eee5d5"/><stop offset="1" stop-color="#c7b99f"/></linearGradient><linearGradient id="pool" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#77b9ce"/><stop offset=".5" stop-color="#a2d1dc"/><stop offset="1" stop-color="#70adc4"/></linearGradient><linearGradient id="car" x1="0" x2="1"><stop stop-color="#d5ded4"/><stop offset=".4" stop-color="#fffdf2"/><stop offset="1" stop-color="#c2cfc1"/></linearGradient><radialGradient id="tree"><stop stop-color="#8d9e50"/><stop offset=".6" stop-color="#607d36"/><stop offset="1" stop-color="#3b5829"/></radialGradient>''')
 if floor is not None:
  add('<clipPath id="tileclip">')
  for q in floor: add(E.tostring(q,encoding='unicode'))
  add('</clipPath>')
 add('</defs>');rect(0,0,1000,H,'white');text(40,32,'ASHWOOD ESTATES',19,bold=True);text(40,53,f'{id[0]}-BEDROOM VILLA / '+{'GF':'GROUND FLOOR','FF':'FIRST FLOOR','RF':'ROOF FLOOR'}[id[-2:]],11)
 text(965,32,'V4 · SOURCE-LIMITED PRESENTATION',8,'#7d785f','end');text(965,51,'UNAPPROVED / NOT SURVEY CAD',8,'#7d785f','end');line(40,65,965,65,'#6d806f',.7)
 add(f'<g id="source_diagram" transform="translate({tx},{ty}) scale({sc})">')
 # Continuous tonal mapping preserves the original raster's weak openings/stair strokes.
 image(soften(raw))
 if floor is not None:
  add('<g clip-path="url(#tileclip)" opacity=".4">')
  for yy in range(0,h,18):line(0,yy,w,yy,'#bcb198',.28)
  for xx in range(0,w,18):line(xx,0,xx,h,'#bcb198',.28)
  add('</g>')
 # Existing source pools only. FF water is explicitly below-floor contextual material.
 ff=id.endswith('FF')
 for n,(a,b,z,t) in enumerate(WATER.get(id,[])):
  rect(a,b,z-a,t-b,'#c1d9dc' if ff else 'url(#pool)','#8da9a4',.5)
  image(soften(raw.crop((a,b,z,t))),a,b,z-a,t-b,.6 if ff else .48)
  for yy in range(b+2,t,5):path(f'M{a},{yy}Q{(a+z)/2},{yy-2} {z},{yy}','none','#d1e8e9',.3)
 # Floor-specific clean furniture only where source evidence shows that type.
 for q in data.get('rugs',[]):rug(*q)
 for q in data.get('beds',[]):bed(*q)
 for q in data.get('dining',[]):
  x,y,ww,hh,k=q;floorpatch(x-17,y-16,ww+34,hh+32);dining(*q)
 for q in data.get('L',[]):Lsofa(*q)
 for q in data.get('curved',[]):curved(*q)
 for q in data.get('U',[]):curved(*q,twopieces=True)
 for x,y,ww,hh in data.get('coffee',[]):rect(x,y,ww,hh,'#cdbc9f','#809078',.55,1);rect(x+3,y+3,ww-6,hh-6,'#e4dac5','#b6aa8c',.3,1)
 for x,y,r in data.get('round',[]):circle(x,y,r,'url(#seat)','#8d977e',.5)
 for x,y,ww,hh in data.get('bars',[]):floorpatch(x-1,y-1,ww+2,hh+2);rect(x,y,ww,hh,'#ded3bb','#91977d',.6,1)
 for x,y,ww,hh in data.get('islands',[]):
  floorpatch(x-1,y-2,ww+2,hh+4);rect(x,y,ww,hh,'#e6ddca','#869078',.6,1);rect(x+10,y+4,18,hh-8,'#798a7a','#607460',.4)
  for xx in [x+14,x+23]:
   for yy in [y+7,y+hh-7]:circle(xx,yy,1.9,'none','#dce5d3',.35)
 for q in data.get('cars',[]):car(*q)
 # Source-located landscape; source FF context is rendered lighter, never new floor contents.
 if id=='4B-FF':trees=[(54+(x-107)*553/527,55+(y-54)*877/841,r*1.04) for x,y,r in TREE4]
 elif id.startswith('5') and id in SITE:trees=TREE5
 elif id.startswith('6') and id in SITE:trees=[(x-(7 if ff else 0),y,r) for x,y,r in TREE6]
 else:trees=[]
 for k,(x,y,r) in enumerate(trees):
  add(f'<g opacity="{.30 if ff else .93}">');circle(x,y,r,'url(#tree)');rng=random.Random(500+k)
  for _ in range(55):
   a=rng.random()*math.tau;rr=math.sqrt(rng.random())*(r-4);xx=x+math.cos(a)*rr;yy=y+math.sin(a)*rr;ra=rng.uniform(2.3,6)
   circle(xx+.7,yy+.7,ra,'#48632d');circle(xx,yy,ra,rng.choice(['#647f36','#778e45','#899d52','#58732e']))
  add('</g>')
 # Exact V3 source-derived structural contour paths, unchanged and ABOVE furniture/planting.
 add(E.tostring(wall,encoding='unicode'))
 # All room dimensions stay inside their corresponding source room, with explicit unknowns.
 for name,dim,x,y in rec['room_transcripts']:
  if id=='6B-GF' and name=='OFFICE / GYM':x,y=420,728
  fs=6.3 if len(name)<15 else 5.3;ds=5.3
  if name.startswith(('BALCONY','TERRACE','OUTDOOR')):fs=5.3;ds=4.7
  # Widen text plate only within the source-label region; structural wall layer is restored after.
  ww=max(len(name)*fs*.24,len(dim)*ds*.24)+1
  if name in ['LIVING / DINING','DOUBLE-HEIGHT ENTRY','MULTIPURPOSE']:ww=max(ww,44)
  rect(x-ww,y-6,2*ww,15,'#eee6d5');text(x,y,name,fs,anchor='middle',bold=True);text(x,y+7,dim+(' m' if re.search(r'\d',dim) else ''),ds,anchor='middle')
 # Restore wall boundaries over any annotation plate edge; never erase an opening or wall.
 # A second draw of identical contours changes no geometry, only guarantees visibility.
 w2=E.fromstring(E.tostring(wall));w2.set('id','structural_poche_visibility_restore');add(E.tostring(w2,encoding='unicode'))
 guidance(LIVE[id],SITE.get(id),ppm,w,h)
 add('</g>')
 # Compact legend occupies unused side margin only; provenance remains in separate report.
 lx=830;ly=H-380;rect(lx,ly,140,202,'#fffef8','#acb49d',.6);text(lx+10,ly+21,'LEGEND / AREA',9,bold=True)
 for i,(c,n) in enumerate([('#e8dfce','Illustrative stone'),('#dce4d9','Service / wet zones'),('#d8cbb4','Existing furniture'),('#7e9649','Source landscape'),('#a2d1dc','Source water')]):
  rect(lx+10,ly+36+i*22,11,11,c,'#a6b093',.3);text(lx+27,ly+45+i*22,n,6.8)
 area={'4B-FF':'260.19','4B-RF':'43.92','5B-GF':'326.01','5B-FF':'328.24','5B-RF':'57.02','6B-GF':'404.49','6B-FF':'392.33','6B-RF':'55.88'}[id]
 text(lx+10,ly+170,'FLOOR AREA',7.2,bold=True);text(lx+10,ly+190,area+' m²',11,bold=True)
 by=H-142
 if ppm:
  text(60,by-20,f'APPROX. 1:100 · {"A3" if paper[0]==297 else "A2"} PORTRAIT · PRINT 100% / ACTUAL SIZE',10.5,bold=True)
  u=10/(paper[0]/1000)
  for k in range(5):rect(60+k*u,by,u,6,'#3c523e' if k%2==0 else 'white','#3c523e',.4)
  for k in range(6):text(60+k*u,by+18,str(k)+(' m' if k==5 else ''),9,anchor='middle')
  text(60,by+42,'~ exterior values are derived schematic spans; declared ±3% working allowance, not guaranteed accuracy.',8.1,'#8c7444')
 else:
  text(60,by-15,'NOT TO SCALE · NO METRIC SCALE BAR',13,'#8c7444',bold=True)
  text(60,by+6,'Independent source spans conflict or reliable endpoints are unavailable; no calibration forced.',8.6,'#8c7444')
 text(60,by+62,'Room values are source-label transcripts; † flags disagreement/uncertainty. Plot boundary is not verified.',8.1)
 text(60,by+80,'Source raster detail is retained. Clean replacement symbols/material graphics are illustrative, not new design facts.',8.1)
 text(60,by+98,'UNAPPROVED PRESENTATION · Not native / certified CAD. No 3D or interior generation. ZIP held.',8.1)
 add('</svg>');svg='\n'.join(A);sfile=O/f'svg/FP-{id}_V4_portrait.svg';sfile.write_text(svg)
 pdfpath=O/f'pdf/FP-{id}_V4_'+Path('x') if False else O/f'pdf/FP-{id}_V4_portrait.pdf'
 cairosvg.svg2pdf(bytestring=svg.encode(),write_to=str(pdfpath));pdf=fitz.open(pdfpath);pg=pdf[0]
 for edge,suffix in [(1800,'preview'),(7680,'long7680')]:
  zz=edge/max(pg.rect.width,pg.rect.height);pg.get_pixmap(matrix=fitz.Matrix(zz,zz),alpha=False).save(O/f'png/FP-{id}_V4_{suffix}.png')
 # Source-aligned QA image at native source coordinates, without portrait framing.
 xml=E.fromstring(svg);body=xml.find(N+'g[@id="source_diagram"]');body.attrib.pop('transform');defs=xml.find(N+'defs')
 standalone=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}">'+E.tostring(defs,encoding='unicode')+E.tostring(body,encoding='unicode')+'</svg>'
 pb=cairosvg.svg2png(bytestring=standalone.encode());new=Image.open(io.BytesIO(pb)).convert('RGB')
 qa=Image.new('RGB',(w*2+24,h+45),'white');qa.paste(raw,(0,35));qa.paste(new,(w+24,35));qd=ImageDraw.Draw(qa);ffont=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12);qd.text((5,8),id+' · ORIGINAL SOURCE',font=ffont,fill='#3a533d');qd.text((w+29,8),'V4 · SAME SOURCE COORDINATES',font=ffont,fill='#3a533d');qa.save(O/f'qa/FP-{id}_source_vs_v4.png')
 # Validate source wall path identity, physical paper, text bounds and scale-bar length.
 orig=[p.attrib['d'] for p in wall.findall(N+'path')];vv=xml.find('.//'+N+'g[@id="source_wall_poche"]');assert orig==[p.attrib['d'] for p in vv.findall(N+'path')]
 clipped=[]
 for b in pg.get_text('dict')['blocks']:
  for l in b.get('lines',[]):
   for sp in l['spans']:
    if not pg.rect.contains(fitz.Rect(sp['bbox'])):clipped.append(sp['text'])
 actualmm=[pg.rect.width*25.4/72,pg.rect.height*25.4/72]
 assert max(abs(actualmm[k]-paper[k]) for k in [0,1])<.01
 assert not clipped,(id,clipped)
 r={'id':id,'version':'V4','status':'UNAPPROVED_SOURCE_LIMITED_PRESENTATION','source_pdf_page':rec['page'],'source_xref':rec['xref'],'source_board_crop_pixels':rec['source_board_crop_pixels'],'native_source_pixels':[w,h],'svg':str(sfile.relative_to(R)),'pdf':str(pdfpath.relative_to(R)),'preview':f'cad-visual-v4-nine/png/FP-{id}_V4_preview.png','long7680':f'cad-visual-v4-nine/png/FP-{id}_V4_long7680.png','source_comparison':f'cad-visual-v4-nine/qa/FP-{id}_source_vs_v4.png','geometry':'Original native raster underlay retained with continuous tonal mapping; exact prior source-wall contour paths unchanged. No generative structural geometry.','hybrid_svg':True,'source_wall_paths_preserved':len(orig),'source_specific_symbol_definitions':data,'calibration':cal,'paper_mm':paper,'pdf_physical_mm':actualmm,'scale_bar_metric_length_m':5 if ppm else None,'scale_bar_physical_length_mm':50 if ppm else None,'exterior_metric_status':'approximate_derived_schematic_envelope_and_site_spans' if ppm else 'unknown_NTS','plot_boundary_verified':False,'room_dimension_status':'brochure_overlay_transcripts_with_flags','clipped_pdf_text_spans':clipped,'native_CAD':False,'user_approved':False,'remaining_limits':['Room-label layer disagreements and unreadable dimensions remain flagged','Fixture/door/stair detail remains native-raster limited; not metrically certified','Replacement furniture/plant/material graphics are illustrative within evidenced source locations','Envelope guides are bounding spans, not a surveyed perimeter profile; no arbitrary interior station grid']}
 (O/f'reports/FP-{id}_V4_record.json').write_text(json.dumps(r,indent=2));print(id,cal['status'],'paper',paper,'wallpaths',len(orig),'clip',len(clipped),flush=True);return r

if __name__=='__main__':
 rows=[]
 # Preserve accepted-to-preview prototype unchanged, exposing it in the nine-sheet set.
 for src,dest in [('cad-visual-v4-prototype/svg/4B_GF_full_size_presentation_v4.svg','svg/FP-4B-GF_V4_portrait.svg'),('cad-visual-v4-prototype/4B_GF_A3_approx_1_100_presentation_v4.pdf','pdf/FP-4B-GF_V4_portrait.pdf'),('cad-visual-v4-prototype/png/4B_GF_full_size_presentation_v4_preview.png','png/FP-4B-GF_V4_preview.png'),('cad-visual-v4-prototype/png/4B_GF_full_size_presentation_v4_long7680.png','png/FP-4B-GF_V4_long7680.png')]:shutil.copy2(R/src,O/dest)
 rows.append({'id':'4B-GF','version':'V4','status':'UNAPPROVED_SOURCE_LIMITED_PRESENTATION','source_pdf_page':27,'source_xref':313,'source_board_crop_pixels':[120,350,830,1370],'native_source_pixels':[710,1020],'svg':'cad-visual-v4-nine/svg/FP-4B-GF_V4_portrait.svg','pdf':'cad-visual-v4-nine/pdf/FP-4B-GF_V4_portrait.pdf','preview':'cad-visual-v4-nine/png/FP-4B-GF_V4_preview.png','long7680':'cad-visual-v4-nine/png/FP-4B-GF_V4_long7680.png','calibration':C['4B-GF'],'paper_mm':[297,420],'source_wall_paths_preserved':13,'clipped_pdf_text_spans':[],'user_approved':False,'plot_boundary_verified':False,'native_CAD':False,'note':'Original V4 prototype preserved, not silently redesigned.'})
 for id in ['4B-FF','4B-RF','5B-GF','5B-FF','5B-RF','6B-GF','6B-FF','6B-RF']:
  if len(sys.argv)>1 and id not in sys.argv[1:]:rows.append(json.loads((O/f'reports/FP-{id}_V4_record.json').read_text()))
  else:rows.append(build(id))
 manifest={'status':'NINE_V4_SOURCE_LIMITED_PRESENTATIONS_EXPORTED_NOT_USER_APPROVED','count':len(rows),'approx_1_100_count':sum(r['calibration']['status']=='approx_calibrated' for r in rows),'NTS_count':sum(r['calibration']['status']!='approx_calibrated' for r in rows),'records':rows}
 (O/'reports/nine_V4_manifest.json').write_text(json.dumps(manifest,indent=2))
 im=Image.new('RGB',(2100,3180),'white');dd=ImageDraw.Draw(im);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
 dd.text((30,18),'ASHWOOD · NINE V4 PORTRAIT PRESENTATIONS',font=font,fill='#344c38');dd.text((30,55),'5 approximate calibrated 1:100 · 4 NOT TO SCALE · unapproved / source limited',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20),fill='#917747')
 for row in rows:
  id=row['id'];x=(int(id[0])-4)*700;y=110+{'GF':0,'FF':1,'RF':2}[id[-2:]]*1010
  pic=Image.open(R/row['preview']);pic.thumbnail((680,980));im.paste(pic,(x+(700-pic.width)//2,y));dd.text((x+25,y+977),id+' · '+('APPROX 1:100' if row['calibration']['status']=='approx_calibrated' else 'NTS'),font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16),fill='#526348')
 im.save(O/'png/ALL_NINE_V4_PORTRAIT_OVERVIEW.png');print('NINE V4 EXPORTED; inspect actual previews and comparisons.')
