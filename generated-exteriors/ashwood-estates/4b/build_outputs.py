import json, csv, hashlib, datetime, os
from PIL import Image, ImageDraw, ImageFont
from zoneinfo import ZoneInfo
ROOT='/workspace/exterior-garden-3d/generated-views/4b'
ARCH='/workspace/plan-visuals-archive'
LABEL='AI-generated concept visualisation, not survey-verified'
now=datetime.datetime.now(ZoneInfo('Asia/Dubai')).isoformat(timespec='seconds')
R='source-refs/'
REF={'front':ROOT+'/'+R+'REF-4b-p25-front-render-crop_no-title-logo.png','rear':ROOT+'/'+R+'REF-4b-p26-rear-render-crop_no-title-logo.png',
 'gf':ROOT+'/'+R+'REF-4b-GF-plan-crop.png','ff':ROOT+'/'+R+'REF-4b-FF-plan-crop.png','rf':ROOT+'/'+R+'REF-4b-RF-plan-crop.png','v4':ROOT+'/'+R+'REF-4b-GF-V4-preview-site-crop.png'}
GF={'plan':'active/approved-cad-v4/svg/FP-4B-GF_V4_portrait.svg','preview':'active/approved-cad-v4/png/FP-4B-GF_V4_preview.png','source_crop':'source-evidence/plan-crops/FP-4B-GF_untouched_board_crop.png','pdf_page':27,'board_crop_bbox_px':[120,350,830,1370],'calibration':'approx_calibrated (~28.15 px/m, ±3% working allowance, not survey)'}
FF={'plan':'active/approved-cad-v4/svg/FP-4B-FF_V4_portrait.svg','source_crop':'source-evidence/plan-crops/FP-4B-FF_untouched_board_crop.png','pdf_page':28,'board_crop_bbox_px':[980,370,1630,1370],'calibration':'approx_calibrated'}
RF={'plan':'active/approved-cad-v4/svg/FP-4B-RF_V4_portrait.svg','source_crop':'source-evidence/plan-crops/FP-4B-RF_untouched_board_crop.png','pdf_page':28,'board_crop_bbox_px':[1820,455,2300,1250],'calibration':'NTS_conflicting_source_spans'}
P25={'page':25,'path':'extracts/pages/page110-25.png','crop_px_used_as_ref':[0,340,2934,1650],'note':'title text and logo cropped out'}
P26={'page':26,'path':'extracts/pages/page110-26.png','crop_px_used_as_ref':[0,340,2934,1650],'note':'title text and logo cropped out'}
NEG='No text, logos, watermarks, people, cars; no extra storeys, pools or structures; no photograph styling; no invented dimensions.'
OBS_MAT=[{'source_page':25,'observed_fact':'Warm beige travertine-like stone cladding, deep flat cantilevered roof slab with soffit light line, bronze/timber vertical slatted FF screen, flat carport canopy at front-left, slatted metal pedestrian gate, low stone boundary wall, date palms and flowering shrubs','inferred_application':'Used as the material/planting palette for all views','uncertainty':'Material species/products not verified; brochure is illustrative'},
 {'source_page':26,'observed_fact':'Rear: full-height GF glazing, full-width FF balcony with frameless glass balustrade, roof-level canopy slab, long rectangular pool along rear, stone terrace with steps, lawn, hedges, palms','inferred_application':'Rear, garden and pool views','uncertainty':'Render may not match final construction'}]
views=[
 dict(view_id='ELEV-FRONT',title='Front (street) elevation',method='GENERATED-SOURCE-CONDITIONED',sources_plan=[GF],brochure=[P25],refs=[REF['front'],REF['gf']],prompt_summary='Straight-on street elevation of the p25 villa; carport left (2 bays), central pedestrian gate/double-height entry, multipurpose block and low stone wall right; no cars/people/text.',
  observed=[OBS_MAT[0],{'source_page':27,'observed_fact':'GF plan front edge: P01/P02 parking (vehicular entrance) left, pedestrian entrance centre, multipurpose room and service entrance right','inferred_application':'Left-to-right order of frontage','uncertainty':'Openings/heights unverified'}],
  assumptions=['Near-orthographic eye-level framing inferred; massing follows render p25','Cars, people and golf cart from render deliberately removed'],
  layout_check='PASS (visual): carport left with two bays, central gate, right-hand stone block and low wall match GF plan order and p25 render.',conflicts=['Near-replica of brochure render p25 composition; must not be presented as a marketing render']),
 dict(view_id='ELEV-REAR',title='Rear (garden) elevation',method='GENERATED-SOURCE-CONDITIONED',sources_plan=[GF,FF],brochure=[P26],refs=[REF['rear'],REF['gf']],prompt_summary='Straight-on rear elevation of the p26 villa with pool, terrace, FF glass balcony, roof canopy slab.',
  observed=[OBS_MAT[1],{'source_page':27,'observed_fact':'Pool 9.50 x 2.40 (brochure transcript) across rear, terrace label beside it; FF rear full-width BALCONY (p28)','inferred_application':'Pool on viewer right, terrace viewer left (mirror of plan from garden side)','uncertainty':'Pool rendered shorter/wider than 9.5x2.4 proportion would suggest'}],
  assumptions=['Lawn depth and boundary hedging inferred from render'],layout_check='PASS with caveat: pool/terrace sides consistent with mirrored plan; pool proportion approximate.',conflicts=['Near-replica of brochure render p26 composition']),
 dict(view_id='ELEV-LEFT',title='Left side elevation (vehicular/carport side; plan-left)',method='GENERATED-CONCEPT',sources_plan=[GF,FF],brochure=[P25,P26],refs=['generated ELEV-FRONT','generated ELEV-REAR',REF['gf'],REF['p25'] if 'p25' in REF else REF['front']],prompt_summary='Side elevation inferred: long stone wall, few narrow windows, carport canopy at street end, balcony slab at rear end, planted side strip. Regenerated once to remove invented street and enclosed garage.',
  observed=[{'source_page':27,'observed_fact':'Plan-left side: planted strip with row of trees along boundary; kitchen/pantry/maid rooms on this side; carport at front-left','inferred_application':'Mostly solid side wall with planting strip and carport at the street end','uncertainty':'No source side elevation exists; window positions, sizes and heights unknown'}],
  assumptions=['ENTIRE ELEVATION IS A LOGICAL INFERENCE - no source side view','Window count/positions invented for plausibility','FF balconies at both ends inferred from FF plan balconies (front-left bedroom balcony, rear balcony)'],
  layout_check='PARTIAL: carport at street end and pool at rear end correct; foreground lawn shown along the full side whereas plan shows a narrow planted/paved strip; carport back wall reads semi-enclosed.',conflicts=['First pass (rejected) invented a public road along the side']),
 dict(view_id='ELEV-RIGHT',title='Right side elevation (service-entrance side; plan-right)',method='GENERATED-CONCEPT',sources_plan=[GF,FF],brochure=[P25,P26],refs=['generated ELEV-FRONT','generated ELEV-REAR',REF['gf']],prompt_summary='Side elevation inferred: multipurpose block and service gate at street end, mid-side courtyard opening with water feature/tree, roof canopy towards rear. Regenerated once to remove invented street.',
  observed=[{'source_page':27,'observed_fact':'Plan-right: multipurpose room front-right, office/gym, open courtyard water feature with central planter beside lift ("OUTDOOR TERRACE"), side path and planted strip, service entrance','inferred_application':'Courtyard shown as glazed recess mid-side; service gate at street end','uncertainty':'No source side view; whether courtyard is visible from the side path is unverified'}],
  assumptions=['ENTIRE ELEVATION IS A LOGICAL INFERENCE','Window positions/heights invented','Lawn in foreground inferred (plan shows path + planting)'],
  layout_check='PARTIAL: element order (service gate front, courtyard mid, rear end) matches plan; courtyard depicted as a glazed interior-like recess; foreground lawn not on plan.',conflicts=['First pass (rejected) invented a public road along the side']),
 dict(view_id='GARDEN-FRONT',title='Front garden / forecourt',method='GENERATED-SOURCE-CONDITIONED',sources_plan=[GF],brochure=[P25],refs=['generated ELEV-FRONT',REF['gf']],prompt_summary='Three-quarter street view: driveway under carport, central gate path, low stone wall with planted strip and shade tree, service gate right.',
  observed=[OBS_MAT[0],{'source_page':27,'observed_fact':'Front strip: 2 parking bays, pedestrian path, planting/large tree at right front, service entrance','inferred_application':'Forecourt layout','uncertainty':'Paving pattern and plant species not specified'}],
  assumptions=['Plant species generic (grasses, pink groundcover, shrubs) from render','Street kerb in foreground inferred (front of plot does face the street per plan entrances)'],
  layout_check='PASS (visual): carport left, gate centre, planted wall and service gate right.',conflicts=[]),
 dict(view_id='GARDEN-BACK',title='Back garden',method='GENERATED-SOURCE-CONDITIONED',sources_plan=[GF],brochure=[P26],refs=['generated ELEV-REAR',REF['rear']],prompt_summary='Three-quarter view from rear lawn corner: lawn, pool, terrace, palms, hedges.',
  observed=[OBS_MAT[1]],assumptions=['Bougainvillea-like pink accents inferred from render colours; species unverified','Lawn depth beyond pool unknown; plan shows only a narrow strip behind the pool'],
  layout_check='PARTIAL: lawn shown deeper than the plan suggests (plan: pool near rear boundary); otherwise consistent with p26.',conflicts=['Garden depth behind pool: plan vs render p26 disagree (render shows wide lawn); render followed for mood']),
 dict(view_id='OUTDOOR-SITE',title='Outdoor spaces overview: driveway, paving, side paths, boundary walls, courtyard, pool',method='GENERATED-SOURCE-CONDITIONED',sources_plan=[GF,RF],brochure=[P25,P26],refs=[REF['gf'],REF['v4'],'generated ELEV-FRONT'],prompt_summary='High oblique aerial of the whole plot following the GF plan. Regenerated once (first pass had a second pool and wrong plot proportions).',
  observed=[{'source_page':27,'observed_fact':'Plot ~18.7 m x ~29.9 m (V4 derived spans, not survey); building near full width; narrow planted side strips; front parking, central path, rear pool + terrace; enclosed courtyard water feature','inferred_application':'Aerial layout','uncertainty':'Plot spans are calibration-derived only'}],
  assumptions=['Boundary wall heights/material inferred from p25 low stone wall','Roof terrace canopy not clearly shown'],
  layout_check='PASS with caveats: single rear pool, courtyard inside footprint, multipurpose block front-right, two-bay carport front-left, side strips both sides. Plot proportion slightly wider than ~1.6:1.',conflicts=['First pass rejected: invented second pool, oversized plot']),
 dict(view_id='OUTDOOR-ROOF-TERRACE',title='Roof terrace',method='GENERATED-CONCEPT',sources_plan=[RF],brochure=[P26],refs=[REF['rf'],'generated ELEV-REAR'],prompt_summary='Roof terrace with dining for ~8, L-sofa, round tables, long counter, canopy slab, glass balustrade.',
  observed=[{'source_page':28,'observed_fact':'RF plan: TERRACE at rear with dining table (~8-10 seats), L-shaped lounge, round tables, long counter; lift, stair, powder, pantry, MEP; p26 shows roof canopy slab','inferred_application':'Furniture arrangement and canopy','uncertainty':'RF plan is NTS (conflicting spans); balustrade type inferred from FF balcony'}],
  assumptions=['No source roof-terrace render exists; finishes inferred','Glass balustrade inferred'],
  layout_check='PARTIAL: furniture types match RF plan; stair shown as an open external stair, whereas the plan places the stair inside the enclosed core.',conflicts=['Stair depiction does not match RF plan']),
 dict(view_id='OUTDOOR-COURTYARD',title='GF side courtyard / outdoor terrace with water feature',method='GENERATED-CONCEPT',sources_plan=[GF],brochure=[P25],refs=[REF['gf'],'generated ELEV-FRONT'],prompt_summary='Square open-to-sky courtyard with shallow reflecting water feature and central planter tree, paved strip by lift core.',
  observed=[{'source_page':27,'observed_fact':'GF plan: "OUTDOOR TERRACE" label by lift; square water feature with square central planter between lift and office/gym','inferred_application':'Courtyard composition','uncertainty':'Not in canonical rooms_index for 4b (only labelled on plan); wall heights/glazing unverified'}],
  assumptions=['Tree species (shown bonsai/pine-like) invented','Bench and glazing extent inferred'],
  layout_check='PARTIAL: square pool + central planter matches plan; enclosure on all sides and amount of glazing are assumptions (plan suggests one side open to the side strip).',conflicts=['4B GF TERRACE and OUTDOOR TERRACE labels are on the plan but missing from canonical/rooms_index.json for villa 4b']),
 dict(view_id='POOL',title='Swimming pool',method='GENERATED-SOURCE-CONDITIONED',sources_plan=[GF,FF],brochure=[P26],refs=['generated ELEV-REAR'],prompt_summary='End-of-pool view along a long narrow lap pool beside the rear glazing. Regenerated once (first pass duplicated the rear elevation).',
  observed=[{'source_page':27,'observed_fact':'SWIMMING POOL 9.50 x 2.40 (brochure transcript, ~4:1) at rear; calibrated span residual <1%','inferred_application':'Pool included (shown in both plan and same-villa render p26)','uncertainty':'Depth, coping and step position unknown'},OBS_MAT[1]],
  assumptions=['Step location inferred','Pool edge raised above lawn as in p26'],
  layout_check='MISMATCH FLAGGED: pool still reads ~3:1 rather than ~4:1 after one regeneration; pool sits slightly away from facade (plan shows ~1 m gap, so acceptable).',conflicts=['Proportion not fully corrected; needs review']),
]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
fontb=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',15)
rows=[];thumbs=[]
for v in views:
  aid=f"EXT-4b-{v['view_id']}"
  fn=f"{aid}_{v['method']}.png"
  im=Image.open(f'{ROOT}/_raw_unlabelled/{aid}.jpg').convert('RGB')
  d=ImageDraw.Draw(im,'RGBA')
  t2=f'{aid} | Ashwood 4B | needs review'
  w=max(d.textlength(LABEL,font=fontb),d.textlength(t2,font=font))+16
  x0=im.width-w-10; y0=im.height-52
  d.rectangle([x0,y0,im.width-10,im.height-10],fill=(0,0,0,150))
  d.text((x0+8,y0+5),LABEL,font=fontb,fill=(255,255,255,255))
  d.text((x0+8,y0+23),t2,font=font,fill=(230,230,230,255))
  im.save(f'{ROOT}/{fn}')
  thumbs.append((fn,im.copy()))
  sha=hashlib.sha256(open(f'{ROOT}/{fn}','rb').read()).hexdigest()
  rec=dict(asset_id=aid,project_id='ashwood-estates',villa_id='4b',view_id=v['view_id'],view_title=v['title'],output_path=f'{ROOT}/{fn}',sha256=sha,
    method=v['method'],generator='Grok Bot GenerateImage (included, no paid credits requested)',prompt_summary=v['prompt_summary'],negative_constraints=NEG,
    source_plans=[dict(plan_path=p['plan'],source_crop=p['source_crop'],source_pdf='original/ashwood-residences_brochure.pdf',pdf_page=p['pdf_page'],board_crop_bbox_px=p['board_crop_bbox_px'],calibration=p['calibration']) for p in v['sources_plan']],
    brochure_renders=v['brochure'],reference_paths=v['refs'],output_dimensions=list(im.size),timestamp_Asia_Dubai=now,
    observed_facts=v['observed'],assumptions=v['assumptions'],layout_check_against_plan=v['layout_check'],conflicts=v['conflicts'],
    label_burned=LABEL,review_status='needs-review',source_missing=True,source_missing_note='No source-verified image exists for this exact view' if v['method']=='GENERATED-CONCEPT' else 'Only brochure marketing render/plan context exists; no survey/photo of this view',generated_available=True,
    excluded_sources=['superseded_2026-11-09/','cad-redraw-v3'])
  rows.append(rec)
man=dict(schema='exterior_generated_visuals_v1',project_id='ashwood-estates',villa_id='4b',created_Asia_Dubai=now,
  villa_selection_rationale='4B has the strongest exterior evidence: same-villa front (p25) and rear (p26) renders; 2 of 3 floors approx_calibrated, GF calibration has 8 spans incl. pool with residuals <=1.02%; plan 2-bay parking matches 2-car carport in render. 5B also has 2/3 calibrated and 3-car consistency but no dedicated GF calibration evidence; 6B has only 1/3 calibrated and render shows 3 cars vs 2-bay plan.',
  pool_decision='INCLUDED: pool labelled on 4B GF plan (9.50 x 2.40 transcript) and visible in same-villa render p26.',
  orientation_note='No verified north point used; left/right defined as seen from the street facing the front elevation (left = vehicular entrance side).',
  disclaimer=LABEL,separation_note='Kept separate from brochure marketing renders; brochure crops in source-refs/ are references only.',
  counts=dict(generated_available=len(rows),source_missing=len(rows),source_verified_views=0),
  rejected_first_pass='_rejected_first_pass/ (4 images; not deliverables)',assets=rows)
json.dump(man,open(f'{ROOT}/generated_visuals_manifest.json','w'),indent=1,ensure_ascii=False)
with open(f'{ROOT}/generated_visuals_manifest.csv','w',newline='') as f:
  cols=['asset_id','villa_id','view_id','view_title','output_path','method','output_dimensions','timestamp_Asia_Dubai','source_plans','brochure_renders','reference_paths','prompt_summary','negative_constraints','observed_facts','assumptions','layout_check_against_plan','conflicts','review_status','source_missing','generated_available','sha256']
  w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
  for r in rows: w.writerow({c:(json.dumps(r[c],ensure_ascii=False) if isinstance(r[c],(list,dict)) else r[c]) for c in cols})
# contact sheet
TW,TH=640,360; cols_n=2; pad=12; cap=26
n=len(thumbs); rows_n=(n+1)//2
sheet=Image.new('RGB',(cols_n*TW+(cols_n+1)*pad, rows_n*(TH+cap)+(rows_n+1)*pad+50),(245,243,238))
d=ImageDraw.Draw(sheet)
d.text((pad,14),'Ashwood Estates 4B - exterior concept set - '+LABEL+' - needs review',font=fontb,fill=(20,20,20))
for i,(fn,im) in enumerate(thumbs):
  im=im.resize((TW,TH)); x=pad+(i%2)*(TW+pad); y=50+pad+(i//2)*(TH+cap+pad)
  sheet.paste(im,(x,y)); d.text((x,y+TH+5),fn,font=font,fill=(30,30,30))
sheet.save(f'{ROOT}/EXT-4b_CONTACT-SHEET.png')
print('ok',len(rows))
