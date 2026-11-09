#!/usr/bin/env python3
"""Explicit user-requested approximate calibration; never treats brochure raster as survey CAD."""
from pathlib import Path
import json,xml.etree.ElementTree as E
import numpy as np,pymupdf as f
R=Path(__file__).resolve().parents[2];P=R/'cad-redraw-v3/final';O=P/'calibration'
# Inner-face endpoints manually read from the untouched source xref313 crop.
# Pool endpoints reference water rectangle; other spans reference clear inside wall faces.
spans=[
 {'feature':'Living/dining clear width','axis':'x','a':[198,215],'b':[547,215],'source_m':12.4},
 {'feature':'Living/dining clear depth','axis':'y','a':[390,190],'b':[390,335],'source_m':5.1},
 {'feature':'Pool water width','axis':'x','a':[196,120],'b':[463,120],'source_m':9.5},
 {'feature':'Pool water depth','axis':'y','a':[350,87],'b':[350,154],'source_m':2.4},
 {'feature':'Office clear width','axis':'x','a':[417,555],'b':[547,555],'source_m':4.6},
 {'feature':'Office clear depth','axis':'y','a':[535,539],'b':[535,634],'source_m':3.4},
 {'feature':'Kitchen clear width','axis':'x','a':[199,490],'b':[312,490],'source_m':4.0},
 {'feature':'Kitchen clear depth','axis':'y','a':[280,449],'b':[280,532],'source_m':3.0}]
for s in spans:s['pixels']=float(np.linalg.norm(np.array(s['b'])-s['a']));s['pixels_per_m']=s['pixels']/s['source_m']
pxm=sum(s['pixels']*s['source_m'] for s in spans)/sum(s['source_m']**2 for s in spans)
for s in spans:s['fit_relative_residual_percent']=round(100*(s['pixels']-pxm*s['source_m'])/(pxm*s['source_m']),3)
axes={a:sum(s['pixels']*s['source_m'] for s in spans if s['axis']==a)/sum(s['source_m']**2 for s in spans if s['axis']==a) for a in ['x','y']}
mm_per_px=10/pxm
cross={'feature':'4B FF contextual pool width','xref':439,'endpoints_crop_pixels':[[146,120],[423,120]],'brochure_overlay_m':9.5,'observed_px_per_m':277/9.5,'normalized_to_xref313_resolution':277/9.5*2360/2455,'note':'Cross-floor context/resolution check only, NOT an independent FF geometry calibration.'}
# Demonstrable conflicting roof labels mean current roof cannot share a verified metric calibration.
roof={'id':'4B-RF','status':'NOT_CALIBRATABLE_FROM_CURRENT_OVERLAY_PAIR','feature':'MEP inner rectangle','endpoints_crop_pixels':{'x':[[75,420],[188,420]],'y':[[130,271],[130,622]]},'brochure_overlay_m':[3.8,15.7],'board_label_m':[3.0,12.8],'overlay_px_per_m':[113/3.8,351/15.7],'reason':'Isotropic x/y fit inconsistent; embedded-board and overlay dimensions disagree. Do not choose a convenient scale silently.'}
# Reproducible physically sized A2 sheet; source-native coordinate system is untouched.
ns='{http://www.w3.org/2000/svg}';rt=E.fromstring((P/'svg/FP-4B-GF_CAD_style_plan.svg').read_text())
draw=rt.find(ns+'g');assert draw is not None
# Plan SVG already carries 78px exterior-guide margins.
body=E.tostring(draw,encoding='unicode')
label=f'APPROX. 1:100 AT A2 · DERIVED FROM ROOM LABELS · NOT SURVEY CAD'
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="594mm" viewBox="0 0 420 594">
<rect width="420" height="594" fill="white"/>
<text x="30" y="22" font-family="sans-serif" font-size="7" fill="#334a3c">ASHWOOD · 4-BEDROOM · GROUND FLOOR</text>
<text x="30" y="34" font-family="sans-serif" font-size="4" fill="#8d713c">{label}</text>
<text x="30" y="43" font-family="sans-serif" font-size="3.7" fill="#566d58">Print paper A2 (420 × 594 mm), 100% / actual size. Do not fit or shrink.</text>
<g transform="translate(40,62) scale({mm_per_px:.10f})">{body}</g>
<text x="30" y="517" font-family="sans-serif" font-size="4.3" fill="#8d713c">Calibration-derived approximate scale; conservative working uncertainty ±3%.</text>
<text x="30" y="526" font-family="sans-serif" font-size="3.7" fill="#566d58">Source-stated exterior dimensions remain UNKNOWN. PNG display zoom has no fixed scale.</text>
<text x="30" y="540" font-family="sans-serif" font-size="4" fill="#334a3c">Approximate scale bar (target 1:100 at stated print settings)</text>
'''
for i in range(5):svg+=f'<rect x="{30+i*10}" y="546" width="10" height="3" fill="'+('#344a3b' if i%2==0 else 'white')+'" stroke="#344a3b" stroke-width=".2"/>'
for i in range(6):svg+=f'<text x="{30+i*10}" y="555" text-anchor="middle" font-family="sans-serif" font-size="3.5" fill="#344a3b">{i}'+(' m' if i==5 else '')+'</text>'
svg+=f'<text x="30" y="574" font-family="sans-serif" font-size="3.5" fill="#566d58">8 spans · isotropic fit {pxm:.3f} source pixels / metre · no metric geometry fabricated.</text></svg>'
(O/'FP-4B-GF_A2_APPROX_1_100.svg').write_text(svg)
doc=f.open(stream=svg.encode(),filetype='svg');pdf=f.open('pdf',doc.convert_to_pdf());pdf.save(O/'FP-4B-GF_A2_APPROX_1_100.pdf')
pdf[0].get_pixmap(matrix=f.Matrix(1400/pdf[0].rect.width,1400/pdf[0].rect.width),alpha=False).save(O/'FP-4B-GF_A2_APPROX_1_100_preview.png')
report={'status':'APPROXIMATE_CALIBRATION_PROTOTYPE_ONLY','source':'PDF page27 / xref313 / board crop [120,350,830,1370]','span_endpoint_units':'native cropped-source pixels; x right, y down','source_dimensions_units':'metres; brochure overlay transcripts','spans':spans,'fit_px_per_m':pxm,'axis_fits_px_per_m':axes,'max_abs_span_residual_percent':max(abs(s['fit_relative_residual_percent']) for s in spans),'working_uncertainty_percent':3,'uncertainty_note':'Conservative engineering-working allowance, not a statistical confidence interval; native endpoint uncertainty about 1–2 pixels plus marketing-label accuracy unknown.','cross_floor_context_check':cross,'paper_mm':[420,594],'svg_physical_dimensions':'420mm × 594mm','pdf_points':list(pdf[0].rect),'pdf_physical_mm':[pdf[0].rect.width*25.4/72,pdf[0].rect.height*25.4/72],'approx_calibrated_count':1,'demonstrably_not_calibratable_count':1,'not_yet_independently_validated_count':7,'blocked_example':roof,'other_floor_status':'Retain NTS; no calibration propagated from one villa/floor to others.'}
(O/'scale_feasibility.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['fit_px_per_m','axis_fits_px_per_m','max_abs_span_residual_percent','pdf_physical_mm','approx_calibrated_count','demonstrably_not_calibratable_count','not_yet_independently_validated_count']},indent=2))
