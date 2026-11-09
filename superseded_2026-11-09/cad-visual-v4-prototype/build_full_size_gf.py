#!/usr/bin/env python3
"""One presentation-quality prototype: unchanged source structural contours, clean illustrative
symbols within source furniture footprints, proposed material graphics, explicit approximate scale.
No new room content or survey geometry is asserted. No 3D or generated interiors.
"""
from pathlib import Path
import math,random,json,html,xml.etree.ElementTree as E
import pymupdf as fitz
import cairosvg
R=Path('/workspace/plan-visuals-archive');O=R/'cad-visual-v4-prototype';N='{http://www.w3.org/2000/svg}'
old=E.fromstring((R/'cad-redraw-v3/svg/FP-4B-GF_full_plan_vector_trace.svg').read_text());gp=old.find(N+'g')
wall=gp.find(N+'g[@id="structural_wall_poche"]');fine=gp.find(N+'g[@id="doors_stairs_glazing_and_fine_detail"]');fixtures=gp.find(N+'g[@id="furniture_silhouettes"]')
cal=json.loads((R/'cad-redraw-v3/final/calibration/scale_feasibility.json').read_text());ppm=cal['fit_px_per_m'];S=10/(.297*ppm)
A=[]
def add(s):A.append(s)
def rect(x,y,w,h,f,st='none',sw=.6,rx=0):add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
def line(x1,y1,x2,y2,c='#9f9a8e',sw=.5,op=1):add(f'<path d="M{x1},{y1}L{x2},{y2}" stroke="{c}" stroke-width="{sw}" fill="none" opacity="{op}"/>')
def circle(x,y,r,f,st='none',sw=.5):add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
def txt(x,y,t,size=7,c='#263a34',anchor='start',bold=False):add(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" text-anchor="{anchor}" font-weight="'+('bold' if bold else 'normal')+f'" fill="{c}">{html.escape(t)}</text>')
def path(d,f='none',st='none',sw=.5):add(f'<path d="{d}" fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
foot='195,188 551,188 551,808 410,808 410,713 196,723'
add('<svg xmlns="http://www.w3.org/2000/svg" width="297mm" height="420mm" viewBox="0 0 1000 1414.1414">')
add('''<defs>
<linearGradient id="pool" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#78bacf"/><stop offset=".5" stop-color="#9cd0df"/><stop offset="1" stop-color="#66a9c4"/></linearGradient>
<linearGradient id="seat" x1="0" x2="1"><stop stop-color="#d9cdbb"/><stop offset=".4" stop-color="#eee6d8"/><stop offset="1" stop-color="#c9bba7"/></linearGradient>
<linearGradient id="car" x1="0" x2="1"><stop stop-color="#e0e3df"/><stop offset=".4" stop-color="#fffef7"/><stop offset=".7" stop-color="#f0f1e9"/><stop offset="1" stop-color="#c8d1cc"/></linearGradient>
<radialGradient id="tree"><stop stop-color="#8b9d49"/><stop offset=".55" stop-color="#617e35"/><stop offset="1" stop-color="#344f26"/></radialGradient>
''')
add(f'<clipPath id="floorclip"><polygon points="{foot}"/></clipPath>')
# Source-space service fixture clip, excluding the replaced sleeping symbol.
add('<clipPath id="serviceclip"><path d="M195,370H361V724H195Z M460,645H547V690H460Z" clip-rule="nonzero"/></clipPath>')
add('<clipPath id="poolclip"><rect x="196" y="87" width="267" height="67"/></clipPath>')
# Existing source tree centres and canopies. Symbols are illustrative, never new site geometry.
trees=[(136,93,49),(569,101,56),(132,278,41),(133,393,46),(148,522,44),(158,648,40),(613,309,42),(614,441,41),(615,574,44),(616,709,39),(626,828,36),(421,857,45)]
for i,(x,y,r) in enumerate(trees):add(f'<clipPath id="tree{i}"><circle cx="{x}" cy="{y}" r="{r}"/></clipPath>')
add('</defs>');rect(0,0,1000,1414.1414,'white')
txt(50,33,'ASHWOOD ESTATES',20,bold=True);txt(50,55,'4-BEDROOM VILLA  /  GROUND FLOOR',11)
txt(950,33,'PRESENTATION PROTOTYPE 04',9,'#7b725e','end');txt(950,52,'SOURCE WALLS · ILLUSTRATIVE FINISHES',8,'#7b725e','end');line(50,66,950,66,'#52645a',.8)
add(f'<g id="source_space" transform="translate(-5,76) scale({S})">')
# Full site surface with clean paver joints, same source rectangle.
rect(107,54,527,841,'#e3dfcf','#8d9582',.8)
for yy in range(54,895,12):
 line(107,yy,634,yy,'#c3c0ad',.4)
 for xx in range(107+(6 if (yy//12)%2 else 0),634,16):line(xx,yy,xx,min(yy+12,895),'#c3c0ad',.4)
# Original lawn-strip footprints; material detail is explicitly illustrative.
for x,y,w,h in [(111,59,77,65),(111,128,45,345),(111,490,79,43),(531,59,100,70),(592,135,39,393),(593,532,39,302),(151,583,39,111),(381,834,160,57)]:
 rect(x,y,w,h,'#9caf73')
 rng=random.Random(x+y)
 for _ in range(int(w*h/80)):
  a=x+rng.random()*w;b=y+rng.random()*h;line(a,b,a+2,b-1,'#6f8a4e',.35,.28)
# The source pool geometry remains exactly 196,87 — 463,154.
rect(195,86,269,69,'#e9e8d4','#829b96',.75);rect(196,87,267,67,'url(#pool)','#4a879e',1)
add('<g clip-path="url(#poolclip)">')
for k in range(27):
 yy=89+k*2.6;path(f'M196,{yy} Q240,{yy-2} 285,{yy} T375,{yy} T465,{yy}','none','#d5eef1',.45)
for xx in range(205,463,24):line(xx,87,xx,154,'#8fbfce',.3,.35)
add('</g>')
for y0,y1 in [(94,109),(132,145)]:
 rect(418,y0,41,y1-y0,'#c4e0e7','#6e9da6',.45)
 for xx in range(420,459,3):line(xx,y0,xx,y1,'#88b1bc',.5)
# Floor and source-supported service zones, with proposed light-stone tile representation.
add(f'<polygon points="{foot}" fill="#e7dfd0"/>');add('<g clip-path="url(#floorclip)">')
for yy in range(190,814,18):line(190,yy,558,yy,'#bfb5a2',.33,.72)
for xx in range(190,558,18):line(xx,188,xx,814,'#bfb5a2',.33,.72)
# Very restrained veining; decorative only, not surveyed/material specification.
for yy in range(204,814,54):path(f'M204,{yy} q35,-4 73,3 t72,0 t73,2 t75,-2','none','#d3c8b5',.35)
add('</g>')
for x,y,w,h in [(252,399,105,45),(260,666,49,52),(465,645,82,42)]:
 rect(x,y,w,h,'#dce4df')
 for xx in range(x,x+w,11):line(xx,y,xx,y+h,'#b5c2b8',.32)
 for yy in range(y,y+h,11):line(x,yy,x+w,yy,'#b5c2b8',.32)
# Courtyard source geometry and planter; no new landscape element.
rect(415,342,131,188,'#dddccc')
for yy in range(350,530,15):line(415,yy,546,yy,'#bdc3ad',.45)
rect(430,410,117,104,'url(#pool)','#88a5a2',.6)
for yy in range(414,514,5):path(f'M431,{yy} q25,-3 50,0 t65,1','none','#c9e4df',.4)
circle(484,462,39,'url(#tree)');rect(464,442,40,40,'#e0d9c3','#677b62',.7);rect(469,447,30,30,'#a6b28d','#6c7b5b',.5)
# Source fine architectural/fixture contours remain available beneath replacement symbols.
add(E.tostring(fine,encoding='unicode'))
add('<g clip-path="url(#serviceclip)">');add(E.tostring(fixtures,encoding='unicode'));add('</g>')
# Clean source stair centreline at every observed source row (not invented riser count).
rect(319,450,38,123,'#e9e5d9')
for yy in [454,463,471,479,487,496,504,513,521,529,538,546,555,563,572]:line(319,yy,358,yy,'#6d786e',.55)
line(358,447,358,574,'#69776c',.6);path('M319,549 L357,528 M333,539 l-2,-6 m2,6 l7,-1','none','#6d786e',.55)
# Clean designed furniture symbols, restricted to existing source footprints.
def chair(x,y,w=13,h=13,rot=0):
 add(f'<g transform="translate({x},{y}) rotate({rot})">');rect(-w/2+1,-h/2+1,w,h,'#b7ad99',rx=3);rect(-w/2,-h/2,w,h,'url(#seat)','#6a756c',.55,3);path(f'M{-w/2+1},{-h/2+4} Q0,{-h/2-1} {w/2-1},{-h/2+4}','none','#948a77',.55);add('</g>')
# Dining: four chairs on each long side, plus one at each end, as source.
for xx in [273,293,314,334]:chair(xx,239,13,13);chair(xx,284,13,13,180)
chair(253,261,13,13,-90);chair(355,261,13,13,90)
rect(262,247,83,31,'#bdb19b',rx=2);rect(261,246,83,31,'#d7cbb8','#7a8271',.65,2)
for xx in [275,288,303,321,336]:line(xx,248,xx-1,275,'#baa98c',.25,.5)
# Living sofa L and source chairs/tables. Rectangles/cushions are symbolic, not new furniture.
rect(411,229,22,86,'#c1b8a8',rx=3);rect(433,297,52,20,'#c1b8a8',rx=3)
rect(409,226,22,87,'url(#seat)','#7e8070',.6,3)
for yy in [234,258,282]:rect(413,yy,15,23,'#e7dfd0','#a99b85',.35,2)
rect(430,294,56,21,'url(#seat)','#7e8070',.6,3)
for xx in [435,459]:rect(xx,297,23,15,'#e7dfd0','#a99b85',.35,2)
rect(409,226,22,6,'#d0c1aa','#8f8c77',.35,2);rect(479,294,7,21,'#d0c1aa','#8f8c77',.35,2)
rect(459,246,34,34,'#cabaa1','#727f71',.6,1);rect(462,249,28,28,'#dfd6c4','#b8ab94',.3,1)
chair(474,216,22,22);circle(501,216,8,'#bcad91','#72816f',.65);chair(505,294,30,30,20)
# Existing show-kitchen island and hob, three source stools.
rect(250,319,109,23,'#b3a68d',rx=1);rect(249,317,109,23,'#e6dfd1','#8c8e7c',.6,1)
rect(264,322,21,14,'#7e8880','#59675e',.45)
for xx,yy in [(269,326),(279,326),(269,332),(279,332)]:circle(xx,yy,2.3,'none','#dbe1d6',.45)
for xx in [307,329,350]:chair(xx,311,11,10)
# Existing office desk and four chairs.
rect(487,557,25,61,'#b9ac93',rx=1);rect(485,555,25,61,'#d3c1a5','#78816f',.65,1)
for yy in [567,589,610]:chair(476,yy,11,13,-90)
chair(530,589,13,15,90)
# Existing maid's bed only, within source sleeping footprint.
rect(217,685,36,31,'#c5c0ae','#89927e',.5,1);rect(219,687,32,27,'#eee9dc','#b4b29d',.35,1);rect(222,705,25,7,'#fffaf0','#c3bba9',.35,1);line(220,700,250,700,'#b8b6a3',.45)
# Existing terrace pair and table, source footprint retained.
chair(495,98,13,13,-20);rect(484,114,17,17,'#d0c5af','#7b8a74',.55);chair(494,142,13,13,20)
# Existing two car footprints, clean marketing-plan symbols rather than noisy raster contours.
def car(x,y,w=44,h=114):
 add(f'<g transform="translate({x},{y})">')
 rect(1,2,w,h,'#b0b8ad',rx=13)
 for xx in [-2,w-2]:
  rect(xx,23,4,16,'#46534a',rx=1);rect(xx,h-34,4,16,'#46534a',rx=1)
 path(f'M4,13 Q7,0 {w/2},0 Q{w-6},0 {w-3},13 L{w-1},{h-14} Q{w-4},{h} {w/2},{h} Q3,{h} 2,{h-14}Z','url(#car)','#64776a',.75)
 path(f'M8,24 Q{w/2},19 {w-8},24 L{w-5},43 Q{w/2},38 5,43Z','#aebfbd','#61786f',.55)
 path(f'M7,{h-32} Q{w/2},{h-36} {w-7},{h-32} L{w-8},{h-18} Q{w/2},{h-14} 8,{h-18}Z','#aebfbd','#61786f',.5)
 rect(8,45,w-16,h-79,'#e5e9df','#a5b1a3',.5,4)
 for xx in [5,w-6]:line(xx,47,xx,h-39,'#a1aea3',.5)
 line(7,10,w-8,10,'#c4c8b9',.55);line(8,h-8,w-9,h-8,'#b8c3b7',.5)
 add('</g>')
car(164,754,44,114);car(245,754,47,114)
# Rich clean trees in evidenced source canopy locations; no new trees are added.
for i,(x,y,r) in enumerate(trees):
 add(f'<g clip-path="url(#tree{i})">');circle(x+2,y+3,r,'#82945d');circle(x,y,r-1,'url(#tree)')
 rng=random.Random(100+i)
 for k in range(65):
  a=rng.random()*math.tau;rr=math.sqrt(rng.random())*(r-4);xx=x+math.cos(a)*rr;yy=y+math.sin(a)*rr;rad=rng.uniform(2.7,7)
  circle(xx+1,yy+1,rad,'#425f2c');circle(xx,yy,rad,rng.choice(['#667f39','#718946','#80964d','#93a35d','#546f31']))
 add('</g>')
# Restore original source structural contours LAST: geometry is bit-for-bit same SVG path layer.
add(E.tostring(wall,encoding='unicode'))
# Source-backed glazing/door strokes, kept in exact source-native positions.
for p in [(198,189,408,189),(464,189,531,189),(191,190,191,223),(195,190,195,223),(191,475,191,510),(195,475,195,510),(464,334,531,334),(464,337,531,337),(410,394,410,530),(413,394,413,530),(458,532,530,532),(458,537,530,537),(410,578,410,631),(414,578,414,631),(548,695,548,725),(552,695,552,725),(515,805,537,805),(515,808,537,808),(191,678,191,700),(195,678,195,700),(318,711,377,711)]:line(*p,'#557365',.55)
for x,y,r,kind in [(221,531,26,'up'),(197,577,25,'up'),(219,631,25,'down'),(434,638,25,'up'),(405,711,27,'leftup'),(435,692,25,'down')]:
 line(x,y,x,y+(-r if kind!='down' else r),'#667b6c',.65)
 if kind=='up':dd=f'M{x},{y-r}A{r},{r} 0 0 1 {x+r},{y}'
 elif kind=='down':dd=f'M{x},{y+r}A{r},{r} 0 0 0 {x+r},{y}'
 else:dd=f'M{x-r},{y}A{r},{r} 0 0 1 {x},{y-r}'
 path(dd,'none','#84927d',.5)
# Larger labels, retaining source room positions; small-room text is intentionally abbreviated.
labels=[(328,118,'SWIMMING POOL','9.50 × 2.40 m'),(300,215,'LIVING / DINING','12.40 × 5.10 m'),(298,359,'SHOW KITCHEN','5.70 × 2.70 m'),(229,411,'PANTRY','1.70 × 2.45 m'),(278,411,'POWDER','3.65 × 1.70 m'),(249,490,'KITCHEN','4.00 × 3.00 m'),(285,555,'LAUNDRY','2.20 × 1.80 m'),(285,612,'K. STORE','2.20 × 1.40 m'),(280,649,'DRESS','1.90 × 1.10 m'),(223,669,'MAID ROOM','UNKNOWN*'),(284,697,'MAID BATH','1.70 × 1.90 m'),(365,658,'DOUBLE-HEIGHT ENTRY','3.29 × 3.30 m'),(446,581,'OFFICE / GYM','4.60 × 3.40 m'),(496,656,'BATH','2.90 × 1.70 m'),(480,755,'MULTIPURPOSE','4.60 × 3.90 m'),(436,358,'LIFT','1.50 × 1.70 m')]
for x,y,n,dim in labels:
 fs=7 if len(n)<16 else 5.6;ds=6.1 if n not in ['LIFT','MAID BATH','POWDER','PANTRY','DRESS'] else 5.0
 # Small neutral plates only in pre-existing source label areas; no walls masked.
 ww=max(len(n)*fs*.25,len(dim)*ds*.25)+1
 rect(x-ww,y-6,2*ww,15,'#eee7d8')
 txt(x,y,n,fs,anchor='middle',bold=True);txt(x,y+7,dim,ds,anchor='middle')
txt(494,166,'TERRACE',6.1,anchor='middle');txt(496,359,'OUTDOOR TERRACE',5.0,anchor='middle')
# Approximate derived exterior alignment chains. These are NOT source-stated metric lengths.
def hd(stations,y,refy,overall=False):
 line(stations[0],y,stations[-1],y,'#59665d',.6)
 for xx in stations:line(xx,refy,xx,y,'#a3aaa0',.35);line(xx-2,y+2,xx+2,y-2,'#59665d',.8)
 for a,b in zip(stations,stations[1:]):txt((a+b)/2,y-5,'~ '+f'{(b-a)/ppm:.1f}'+' m',7.6,'#3c4c43','middle')
def vd(stations,x,refx):
 line(x,stations[0],x,stations[-1],'#59665d',.6)
 for yy in stations:line(refx,yy,x,yy,'#a3aaa0',.35);line(x-2,yy+2,x+2,yy-2,'#59665d',.8)
 for a,b in zip(stations,stations[1:]):
  z=(a+b)/2;add(f'<text x="{x-5}" y="{z}" transform="rotate(-90 {x-5} {z})" font-family="sans-serif" font-size="7.6" text-anchor="middle" fill="#3c4c43">~ {(b-a)/ppm:.1f} m</text>')
hd([107,190,315,410,557,634],28,54);hd([107,634],8,54)
hd([107,190,315,410,557,634],920,895);hd([107,634],942,895)
vd([54,190,335,532,692,813,895],77,107);vd([54,895],54,107)
vd([54,190,335,532,692,813,895],663,634);vd([54,895],686,634)
txt(370,966,'DERIVED SITE-DIAGRAM SPANS · NOT A VERIFIED PLOT SURVEY',6.5,'#886c3a','middle')
for x,s in [(216,'VEHICLE ENTRY'),(383,'PEDESTRIAN ENTRY'),(600,'SERVICE ENTRY')]:txt(x,902,s,5.8,'#5c7161','middle')
add('</g>')
# Compact legend only; all provenance stays in separate report.
rect(828,924,144,230,'#fffef9','#aab49e',.7);txt(840,946,'LEGEND / AREA',10,bold=True)
for i,(c,n) in enumerate([('#e7dfd0','Living / circulation'),('#dce4df','Wet / utility zones'),('#d7cbb8','Illustrative furniture'),('#7e994a','Source landscape'),('#8ec6d9','Source water features')]):
 rect(840,961+i*24,12,12,c,'#91a085',.4);txt(859,971+i*24,n,7.3)
line(840,1090,960,1090,'#aab49e',.5);txt(840,1111,'GROUND FLOOR',7.8,bold=True);txt(840,1131,'263.01 m²',12,bold=True)
# Scale bar physically 50 mm long on A3, with explicit calibration qualification.
barunits=50/.297;bx=80;by=1292
for i in range(5):rect(bx+i*barunits/5,by,barunits/5,6,'#354b3d' if i%2==0 else 'white','#354b3d',.5)
for i in range(6):txt(bx+i*barunits/5,by+20,str(i)+(' m' if i==5 else ''),10,anchor='middle')
txt(80,1272,'APPROX. 1:100 · A3 PORTRAIT · PRINT 100% / ACTUAL SIZE',11,bold=True)
txt(80,1340,'Exterior ~ values are calibration-derived, not source-stated; working uncertainty ±3%.',9,'#876d3d')
txt(80,1359,'Room dimensions transcribe brochure labels. *Maid-room dimension conflicts: UNKNOWN.',9,'#5e715f')
txt(80,1378,'Finish textures and replacement symbols are illustrative; structural source contours retained.',9,'#5e715f')
txt(80,1397,'PROTOTYPE · NOT SURVEY / CONSTRUCTION CAD · No 3D work. ZIP held.',8.5,'#7a806e')
add('</svg>');svg='\n'.join(A);(O/'svg/4B_GF_full_size_presentation_v4.svg').write_text(svg)
cairosvg.svg2pdf(bytestring=svg.encode(),write_to=str(O/'4B_GF_A3_approx_1_100_presentation_v4.pdf'))
pdf=fitz.open(O/'4B_GF_A3_approx_1_100_presentation_v4.pdf')
for edge,name in [(1800,'preview'),(7680,'long7680')]:
 pg=pdf[0];sc=edge/max(pg.rect.width,pg.rect.height);pg.get_pixmap(matrix=fitz.Matrix(sc,sc),alpha=False).save(O/f'png/4B_GF_full_size_presentation_v4_{name}.png')
# Assert source structural wall path strings unchanged in the new document.
orig=[e.attrib['d'] for e in wall.findall(N+'path')];new=E.fromstring(svg).find('.//'+N+'g[@id="structural_wall_poche"]');assert orig==[e.attrib['d'] for e in new.findall(N+'path')]
report={'status':'ONE_REWORKED_PRESENTATION_PROTOTYPE_NOT_NINE_REPLACEMENTS','structural_wall_paths_unchanged':len(orig),'print_paper_mm':[297,420],'scale':'Approximate calibration-derived 1:100 at A3 actual-size print','calibration_evidence':'cad-redraw-v3/final/calibration/scale_feasibility.json','exterior_values':'Approximate derived schematic site/wall alignment spans, NOT source-stated or verified plot survey','new_illustrative_content':['Clean symbols replacing only source-evidenced dining/sofa/office/vehicle/terrace/bed footprints','Proposed warm neutral tile/paver hatch and wood-tone furniture graphics','Source-located tree symbols with layered foliage texture','Closed blue source water geometry with restrained ripple shading'],'source_geometry_limits':['Native low-resolution source; fine opening/fixture contours remain source-limited','Maid-room dimensional conflict unresolved','Source site outline is not verified legal plot boundary'],'not_done':['No replacement of other eight sheets with this new style','No interior image generation','No 3D','No ZIP delivery'],'template_comparison_required':True}
(O/'reports/v4_presentation_status.json').write_text(json.dumps(report,indent=2));print('V4 prototype created; structural wall paths unchanged:',len(orig),'A3 PDF mm:',[pdf[0].rect.width*25.4/72,pdf[0].rect.height*25.4/72])
