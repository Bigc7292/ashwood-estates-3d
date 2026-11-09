from pathlib import Path
import json,numpy as np
from PIL import Image,ImageDraw
R=Path('/workspace/plan-visuals-archive');O=R/'cad-visual-v4-nine'
def sp(n,a,b,m):return dict(feature=n,a=a,b=b,source_m=m)
T={
'4B-FF':[sp('Master width',[148,250],[267,250],4),sp('Master depth',[170,196],[170,346],5.1),sp('Family width',[274,230],[392,230],4),sp('Family depth',[350,196],[350,346],5.1),sp('Lower bedroom width',[148,640],[262,640],3.9),sp('Lower bedroom depth',[175,621],[175,745],4.3)],
'5B-GF':[sp('Pool width',[133,80],[360,80],9),sp('Pool depth',[300,55],[300,118],2.5),sp('Kitchen clear width',[132,490],[221,490],3.5),sp('Kitchen clear depth',[200,433],[200,509],3),sp('Guest bedroom width',[351,600],[453,600],4.1),sp('Guest bedroom depth',[400,575],[400,678],4.1)],
'5B-FF':[sp('Master width',[118,250],[252,250],5.3),sp('Master depth',[130,182],[130,317],5.4),sp('Bedroom 1 width',[351,620],[468,620],4.7),sp('Bedroom 1 depth',[450,575],[450,678],4.1)],
'6B-GF':[sp('Kitchen width',[99,435],[185,435],4),sp('Kitchen depth',[175,403],[175,478],3.55),sp('Guest bedroom width',[380,570],[469,570],4.2),sp('Guest bedroom depth',[450,502],[450,608],4.7),sp('Pool width disputed label',[109,80],[318,80],9.5),sp('Pool depth disputed label',[290,54],[290,115],2.4)],
'6B-FF':[sp('Master width',[91,250],[212,250],5.7),sp('Master depth',[115,174],[115,297],5.7),sp('Bedroom 1 width',[90,690],[220,690],6),sp('Bedroom 1 depth',[200,631],[200,740],5),sp('Junior width',[369,535],[483,535],5.3),sp('Junior depth',[450,508],[450,609],4.7)],
'4B-RF':[sp('MEP width ambiguous overlay',[75,420],[188,420],3.8),sp('MEP depth ambiguous overlay',[130,271],[130,622],15.7)],
'5B-RF':[sp('MEP width',[28,470],[131,470],3.8),sp('MEP depth',[78,278],[78,674],15.7)],
'6B-RF':[]}
C={}
old=json.loads((R/'cad-redraw-v3/final/calibration/scale_feasibility.json').read_text());C['4B-GF']={'status':'approx_calibrated','px_per_m':old['fit_px_per_m'],'spans':old['spans'],'max_abs_residual_percent':old['max_abs_span_residual_percent'],'source_report':'cad-redraw-v3/final/calibration/scale_feasibility.json','working_allowance_percent':3}
for id,ss in T.items():
 for s in ss:s['pixels']=float(np.linalg.norm(np.array(s['b'])-s['a']));s['axis']='x' if s['a'][1]==s['b'][1] else 'y';s['px_per_m']=s['pixels']/s['source_m']
 if ss:
  fit=sum(s['pixels']*s['source_m'] for s in ss)/sum(s['source_m']**2 for s in ss)
  for s in ss:s['relative_residual_percent']=round(100*(s['pixels']/(fit*s['source_m'])-1),3)
  residual=max(abs(s['relative_residual_percent']) for s in ss)
  axes={a:sum(s['pixels']*s['source_m'] for s in ss if s['axis']==a)/sum(s['source_m']**2 for s in ss if s['axis']==a) for a in ['x','y']}
  good=len(ss)>=4 and residual<=3 and abs(axes['x']/axes['y']-1)<.03
  C[id]={'status':'approx_calibrated' if good else 'NTS_conflicting_source_spans','px_per_m':fit if good else None,'test_fit_px_per_m_not_accepted':None if good else fit,'max_abs_residual_percent':residual,'axis_fits_px_per_m':axes,'spans':ss,'working_allowance_percent':3 if good else None}
 else:C[id]={'status':'NTS_insufficient_unambiguous_independent_spans','px_per_m':None,'spans':[],'reason':'MEP region is irregular/open and source labels ambiguous; reliable independent orthogonal room endpoints not established.'}
 im=Image.open(R/f'cad-redraw-v3/source/FP-{id}_untouched_board_crop.png').convert('RGB');d=ImageDraw.Draw(im)
 for n,s in enumerate(ss,1):
  a,b=tuple(s['a']),tuple(s['b']);col='#bd422f' if s['axis']=='x' else '#236eae';d.line([a,b],fill=col,width=2)
  for x,y in [a,b]:d.ellipse((x-2,y-2,x+2,y+2),fill=col)
  d.text(((a[0]+b[0])/2+2,(a[1]+b[1])/2+2),str(n),fill=col)
 im.save(O/f'qa/{id}_calibration_endpoints.png')
# Document visible shared native-board/context alignment without imposing a scale.
for a,b in [('4B-GF','4B-FF'),('5B-GF','5B-FF')]:
 expected=C[a]['px_per_m']*(2455/2360 if a.startswith('4') else 1)
 C[b]['cross_floor_alignment_check']={'against':a,'expected_px_per_m_after_native_board_resolution':expected,'observed_px_per_m':C[b]['px_per_m'],'relative_difference_percent':100*(C[b]['px_per_m']/expected-1),'scope':'Visible contextual site/pool alignment corroboration only; independent room spans govern acceptance.'}
report={'status':'independent_approximate_source_calibration_not_survey','endpoint_units':'native source-crop pixels, inner structural faces where identifiable; manually read precision approximately 1–2 pixels','metric_units':'metres, brochure overlay room/pool transcripts','acceptance_rule':'At least four independent orthogonal spans from two rooms/features, max fit residual <=3%, x/y fit mismatch <3%; rejects contradictory cases. This is a feasibility rule, not proof of real-world accuracy.','working_allowance_note':'Declared conservative ±3% working allowance is NOT a guarantee, survey accuracy or statistical confidence interval. Source room labels may be inaccurate.','calibrated_count':sum(c['status']=='approx_calibrated' for c in C.values()),'NTS_count':sum(c['status']!='approx_calibrated' for c in C.values()),'floors':C}
(O/'reports/independent_calibration.json').write_text(json.dumps(report,indent=2));print({i:(j['status'],j.get('px_per_m'),j.get('max_abs_residual_percent')) for i,j in C.items()});print('counts',report['calibrated_count'],report['NTS_count'])
