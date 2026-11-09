#!/usr/bin/env python3
"""Evidence-linked stage-1 organization. Does not generate interiors, match unknown photos,
contact a bot, change geometry, or package/deliver a ZIP."""
from pathlib import Path
import json,csv,re,hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
import pymupdf as fitz
R=Path(__file__).resolve().parents[2];P=R/'canonical';F=R/'cad-redraw-v3/final'
D=fitz.open(R/'original/ashwood-residences_brochure.pdf');M=json.loads((F/'reports/nine_plan_manifest.json').read_text());now=datetime.now(ZoneInfo('Asia/Dubai')).isoformat()
def rel(p):return str(Path(p).relative_to(R))
def write(p,data):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2))
def slug(s):return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
# Three actual source visual panels, not generated or assigned room views.
refdefs=[('ref-p15-dressing',15,[0,0,890,1080],'dressing',['Wood-toned and glass-fronted joinery','Dark metal-framed centre island','Light beige floor','Rectangular suspended linear luminaire']),('ref-p15-living',15,[1123,130,1700,950],'living',['Light stone-like TV/feature wall','Cream and muted green seating','Glass-rod chandelier','Dark TV and narrow linear fireplace']),('ref-p16-bedroom',16,[0,0,1920,1080],'bedroom',['Cream upholstered headboard and bench','Wood-toned wall panelling','Grey/cream textiles','Full-height glazing','Black linear ceiling-light slots'])]
refs=[]
for id,pg,box,kind,cues in refdefs:
 dest=P/'references'/f'{id}.png';D[pg-1].get_pixmap(matrix=fitz.Matrix(1.2,1.2),clip=fitz.Rect(box),alpha=False).save(dest)
 refs.append({'reference_id':id,'source_page':pg,'source_bbox_pdf_points':box,'bbox_kind':'manually selected visible visual panel, not plan-room bounds','path':rel(dest),'observed_category':kind,'observed_visible_cues':cues,'material_species_or_product_verified':False,'villa_id':None,'floor_id':None,'room_id':None,'match_status':'unknown','scope':'project brochure reference only; not matched to any villa/floor/room'})
finish=['Recon veneer joinery','Calacatta marble or porcelain feature material','Textured paint general walls','Clear glass','Bronze metal ironmongery','Travertine stone feature material','White paint walls and ceiling','Light beige marble or porcelain general flooring','Stainless steel ironmongery']
refs.append({'reference_id':'ref-p17-materials','source_page':17,'source_bbox_pdf_points':[0,0,1920,1080],'path':'extracts/pages/page110-17.png','description_path':'extracts/text/pages/page_17.txt','source_stated_material_alternatives':finish,'scope':'Project-wide illustrated material palette, not a verified finish schedule for each room','disclaimer':'Illustrative materials may change; final selections may differ.','match_status':'source_present_project_level'})
for villa,pages in [('4b',[25,26]),('5b',[29,30]),('6b',[33,34])]:
 for pg in pages:refs.append({'reference_id':f'ref-{villa}-p{pg}-exterior','source_page':pg,'source_bbox_pdf_points':[0,0,1920,1080],'path':f'extracts/pages/page110-{pg:02}.png','villa_id':villa,'floor_id':None,'room_id':None,'scope':'Villa-type exterior context; NOT room-interior evidence','match_status':'villa_type_context_only'})
write(P/'references/source_style_evidence.json',{'references':refs,'legacy_inventory_corrections':['Page 15 contains a dressing view (left) and double-height/living view (right), not a single generic living view.','Page 16 is a bedroom view, NOT a kitchen view as legacy page classification stated.'],'inference_policy':{'allowed':'Logically extrapolate decor, furnishing palette and lighting from factual brochure cues, keeping every extrapolation labelled as proposed/inferred.','forbidden':'Treat generic project imagery as a verified room match; change structural geometry; invent metric dimensions or material product specifications.'}})
# GF prototype's original label anchors, matching its actual source trace.
gfanchors=[(328,117),(300,215),(296,359),(229,410),(278,411),(248,491),(285,556),(286,612),(445,581),(496,657),(365,659),(480,755),(280,648),(223,671),(284,697),(436,358)]
rooms=[];floors=[];views=[];qa=[]
for rec in M['records']:
 id=rec['id'];villa=id[:2].lower();floor=id[-2:].lower();fid=f'ashwood-estates/{villa}/{floor}'
 dr=P/'villas'/villa/'floors'/floor;dr.mkdir(parents=True,exist_ok=True)
 floorrooms=[]
 for n,(name,dim,x,y) in enumerate(rec['room_transcripts']):
  if id=='4B-GF':x,y=gfanchors[n]
  rid=f'{fid}/{slug(name)}';viewid=rid+'/view-unassigned-001'
  outside=any(k in name.upper() for k in ['BALCONY','TERRACE','SWIMMING POOL'])
  geom='source_raster_trace_review_required';unknown=any(k in dim for k in ['UNKNOWN','UNREADABLE']);conflict='†' in dim or ('MAID ROOM' in name.upper() and id=='4B-GF')
  b=rec['source_board_crop_pixels'];labelbox=[round(b[0]+x-25,2),round(b[1]+y-9,2),round(b[0]+x+25,2),round(b[1]+y+12,2)]
  category='bedroom' if any(k in name.upper() for k in ['BEDROOM','MASTER SUITE','JUNIOR SUITE']) else 'dressing' if 'DRESS' in name.upper() else 'living' if 'LIVING' in name.upper() else None
  candidates=[r['reference_id'] for r in refs if r.get('observed_category')==category] if category else []
  desc=f'Source plan identifies {name.lower()} on the {floor.upper()} of the {villa[0]}-bedroom villa. '
  desc+=('Dimensions are unknown/unreadable.' if unknown else f'Brochure-overlay dimension transcript: {dim} metres; not remeasured.')
  if conflict:desc+=' Source label layers conflict; the stated pair is not geometry-verified.'
  rr={'project_id':'ashwood-estates','villa_id':villa,'floor_id':floor,'floor_stable_id':fid,'room_id':rid,'label':name,'space_type':'outdoor_feature' if outside else 'interior_or_service_space','description':desc,'description_status':'source_label_based_only','source_page':rec['page'],'source_pdf':'original/ashwood-residences_brochure.pdf','source_embedded_xref':rec['xref'],'source_board_crop_bbox_pixels':b,'source_label_reference_bbox':labelbox,'source_label_bbox_coordinate_system':'original embedded-board pixels; approximate label region, NOT room polygon','room_polygon':None,'room_polygon_status':'not delineated','plan_source_path':f'cad-redraw-v3/source/FP-{id}_untouched_board_crop.png','cad_svg_path':rec['svg_sheet'],'cad_plan_svg_path':rec['svg_plan'],'cad_preview_path':rec['sheet_preview'],'source_room_plan_crop_available':False,'source_verified_room_interior_visual_status':'missing','source_verified_room_interior_visual_present':False,'source_candidate_match_status':'ambiguous' if candidates else 'unknown','source_candidate_visual_refs':candidates,'project_material_reference':'ref-p17-materials','same_villa_context_refs':[r['reference_id'] for r in refs if r.get('villa_id')==villa],'same_villa_interior_style_reference_verified':False,'dimension_transcript':dim,'dimension_status':'unknown' if unknown else 'conflicting_source_layers' if conflict else 'brochure_transcript_not_geometry_certified','perimeter_numeric_status':'unknown_source','geometry_status':geom,'floor_assignment_confidence':'source-supported: anchored to named floor panel','room_outline_confidence':'not established','uncertainties':['No independently delineated room polygon','Opening widths, exact door swings, wall thicknesses and stair riser/tread count not metrically verified','No verified room-to-interior-photo match','No verified ceiling height or camera pose'],'logical_inference_cues':{'allowed':'Use referenced project material alternatives and visible brochure decor as a coherent proposed style; label all unobserved decor as inferred.','structural_lock':'Do not alter openings, walls, room adjacency or invent missing dimensions. Return geometry gaps for review.','style_transfer_scope':'Project-level cues; same-villa interior match is not proven.'},'generated_available':False,'generated_paths':[],'view_id':viewid,'view_requirement_status':'camera/view brief not specified','ready_status':'ready_for_evidence_review_and_proposed_decor; blocked_for_claimed_dimensionally_faithful_render'}
  rooms.append(rr);floorrooms.append(rr)
  if not outside:
   views.append({'project_id':'ashwood-estates','villa_id':villa,'floor_id':floor,'room_id':rid,'view_id':viewid,'source_status':'missing','source_present':False,'source_status_definition':'No verified room-specific interior visual asset; does NOT assert no potentially relevant brochure image exists.','candidate_matching_status':rr['source_candidate_match_status'],'candidate_visual_refs':candidates,'generated_available':False,'generated_paths':[],'source_page':rec['page'],'source_bbox':labelbox,'source_bbox_coordinate_system':rr['source_label_bbox_coordinate_system'],'description':desc,'cad_path':rec['svg_plan'],'source_plan_path':rr['plan_source_path'],'geometry_status':geom,'room_polygon':None,'dimensions':dim,'dimension_status':rr['dimension_status'],'style_evidence_path':'canonical/references/source_style_evidence.json','style_reference_ids':candidates+['ref-p17-materials'],'logical_inference_cues':rr['logical_inference_cues'],'evidence_gaps':rr['uncertainties'],'review_required':True})
 q={'floor_id':fid,'asset_id':id,'source_vs_output_review':'performed: all nine comparison images visually opened','source_comparison_path':f'cad-redraw-v3/final/qa/FP-{id}_source_vs_vector.png','macro_wall_room_stair_location':'source-derived arrangement retained at presentation level; no survey validation','doors_and_openings':'source pixel contours retained; faint door arcs/glazing strokes may be incomplete or irregular. Exact swing/width not certified.','stairs':'stairwell location retained; some thin source tread strokes are weak/missing in exported contours. Tread/riser count and geometry require review.','labels':'room-local source transcripts added; limited native source quality leaves occasional residual source glyph fragments. Conflicting values flagged.','numeric_perimeter_source_count':0,'plot_boundary_verified':False,'disagreements':rec['conflicts'],'status':'SOURCE_LIMITED_REVIEW_REQUIRED','critical_use_restriction':'Not ready for dimensionally faithful 3D/interior reconstruction without opening/stair/room-boundary review.'}
 qa.append(q)
 desc=f'# {villa[0]}-bedroom villa / {floor.upper()}\n\nSource: PDF page {rec["page"]}, embedded board xref {rec["xref"]}; crop {b}.\n\nBrochure floor area: '+({'4B-GF':'263.01','4B-FF':'260.19','4B-RF':'43.92','5B-GF':'326.01','5B-FF':'328.24','5B-RF':'57.02','6B-GF':'404.49','6B-FF':'392.33','6B-RF':'55.88'}[id])+' m² (source schedule, not measured).\n\nRoom/space descriptions, exact file pointers and missing visuals are in index.json. No room polygon or room image crop is supplied. All numeric exterior lengths remain unknown. Source-resolution openings and stairs require review.\n'
 (dr/'DESCRIPTION.md').write_text(desc)
 fr={'project_id':'ashwood-estates','villa_id':villa,'floor_id':floor,'floor_stable_id':fid,'description_path':rel(dr/'DESCRIPTION.md'),'source_pdf_page':rec['page'],'source_embedded_xref':rec['xref'],'source_board_crop_bbox_pixels':b,'source_plan_path':f'cad-redraw-v3/source/FP-{id}_untouched_board_crop.png','source_text_path':f'extracts/text/pages/page_{rec["page"]:02}.txt','drawing_sheet_svg':rec['svg_sheet'],'drawing_plan_svg':rec['svg_plan'],'drawing_preview':rec['sheet_preview'],'drawing_sheet_long7680':f'cad-redraw-v3/final/png/FP-{id}_CAD_style_sheet_long7680.png','drawing_plan_long7680':f'cad-redraw-v3/final/png/FP-{id}_CAD_style_plan_long7680.png','scale_status':'approximate derived 1:100 A2 alternative available' if id=='4B-GF' else 'NTS','scale_alternative_pdf':'cad-redraw-v3/final/calibration/FP-4B-GF_A2_APPROX_1_100.pdf' if id=='4B-GF' else None,'scale_evidence':'cad-redraw-v3/final/calibration/scale_feasibility.json','geometry_qa':q,'room_count_including_outdoor_features':len(floorrooms),'rooms':floorrooms}
 write(dr/'index.json',fr);floors.append({k:v for k,v in fr.items() if k!='rooms'})
# Legacy page-level labels are not independently room geometry; never fabricate a floor match.
legacy=json.loads((R/'manifests/rooms_manifest.json').read_text())['rooms']
write(P/'unresolved_legacy_room_labels.json',{'records':[dict(r,canonical_floor_id=None,canonical_room_id=None,status='unresolved_legacy_label_not_auto_merged',reason='Legacy text-label entry has no isolated room geometry and may be a page heading or duplicate. Use canonical visually anchored room records instead; do not guess floor/room matching.') for r in legacy]})
write(P/'rooms_index.json',{'rooms':rooms});write(P/'floors_index.json',{'floors':floors});write(P/'handoff/missing_interior_visuals.json',{'schema_version':'1.0','recipient_stage':'Interior Visuals Generator','recipient_bot_id':'f34d2a2c-d88a-4f59-9f85-7d8284ee48f2','contacted':False,'generated_available':False,'view_policy':'Unassigned view IDs are placeholders, not invented camera instructions.','records':views})
cols=['project_id','villa_id','floor_id','room_id','view_id','source_status','source_present','candidate_matching_status','generated_available','source_page','source_bbox','description','cad_path','source_plan_path','geometry_status','dimensions','dimension_status','style_reference_ids','review_required']
with (P/'handoff/missing_interior_visuals.csv').open('w',newline='') as f:
 wr=csv.DictWriter(f,fieldnames=cols);wr.writeheader()
 for r in views:wr.writerow({k:json.dumps(r[k]) if isinstance(r[k],(list,dict)) else r[k] for k in cols})
write(P/'handoff/drawing_geometry_QA.json',{'checked_count':9,'check_scope':'bounded visual source-versus-output review of all nine, not survey or native CAD certification','all_status':'SOURCE_LIMITED_REVIEW_REQUIRED','records':qa})
write(P/'project_index.json',{'project_id':'ashwood-estates','source_name':'Ashwood Estates brochure','updated_at_Asia_Dubai':now,'root_paths_relative_to':'/workspace/plan-visuals-archive','source_pdf':'original/ashwood-residences_brochure.pdf','source_sha256':hashlib.sha256((R/'original/ashwood-residences_brochure.pdf').read_bytes()).hexdigest(),'villa_ids':['4b','5b','6b'],'floor_index':'canonical/floors_index.json','room_index':'canonical/rooms_index.json','style_evidence':'canonical/references/source_style_evidence.json','missing_visuals_json':'canonical/handoff/missing_interior_visuals.json','missing_visuals_csv':'canonical/handoff/missing_interior_visuals.csv','qa_index':'canonical/handoff/drawing_geometry_QA.json','unresolved_legacy_labels':'canonical/unresolved_legacy_room_labels.json','floor_count':len(floors),'room_or_space_count':len(rooms),'interior_or_service_missing_view_count':len(views),'verified_room_interior_visual_matches':0,'generated_visual_count':0,'legacy_unresolved_label_count':len(legacy),'approx_calibrated_floor_count':1,'scale_unvalidated_or_blocked_floor_count':8,'exterior_numeric_source_coverage':'0 of 9 plans','status':'ORGANIZED_SOURCE_EVIDENCE_HANDOFF_READY; GEOMETRY_REVIEW_AND_ROOM_MATCHING_REQUIRED','zip_delivered':False,'3d_started':False,'stage2_contacted':False})
(P/'README.md').write_text('''# Ashwood stage-1 canonical evidence index

Start at `project_index.json`. Paths are relative to `/workspace/plan-visuals-archive`; move the archive root as a unit for portability. Existing originals, extracts, room SOURCE.txt files and previous drawing versions remain unchanged.

## Organization
- `villas/{4b,5b,6b}/floors/{gf,ff,rf}/index.json`: source page/xref/crop, source and drawing paths, floor description, room records, geometry QA and scale status.
- `rooms_index.json`: stable project/villa/floor/room IDs, source-label descriptions, room-local reference anchors and uncertainties.
- `references/`: three extracted brochure visual panels plus factual style/material evidence. These are **not** matched room images or newly generated visuals.
- `handoff/missing_interior_visuals.json` and `.csv`: one unassigned placeholder view per interior/service space; `generated_available=false` independently of source matching status.
- `handoff/drawing_geometry_QA.json`: bounded all-nine source-versus-output checks and unresolved opening/stair detail.
- `unresolved_legacy_room_labels.json`: old page-level labels, including potentially spurious headers/duplicates, not auto-merged or assigned invented floors.

## Facts, missing assets and inference
135 canonical entries are room/space records, including exterior pools/terraces/balconies; they are NOT 135 verified room polygons. `source_label_reference_bbox` is an approximate LABEL box in the embedded board's native pixels—not a room boundary. Floor assignment comes from the visually identified floor panel. Ceiling heights, camera poses, exact openings and room polygons are not established.

Existing legacy `rooms/` folders contain text references only. There are **no individual room plan crops or verified room-to-interior-photo matches**. A missing view means no VERIFIED room-specific file, not proof that the brochure lacks a potentially relevant view. Source candidates remain ambiguous/unassigned.

Page 15 supplies dressing/living examples; page 16 is a BEDROOM (correcting a legacy kitchen classification); page 17 provides project-wide illustrated material alternatives. Same-villa exterior pages are context only. Do not claim generic project interiors belong to a particular villa/floor/room. A later generator may logically propose coherent decor using these factual cues, but must label inferred decor and never promote it to source evidence or alter unknown geometry.

## Drawing and scale status
Nine source-limited vector presentation sheets are exported, not native/survey CAD. All nine comparisons were visually checked at presentation level. Some source-faint door/glazing/tread strokes remain weak/incomplete; geometry QA is REVIEW REQUIRED. Do not silently treat them as detailed verified CAD.

All source-stated numeric exterior lengths are missing. UNKNOWN exterior chains are schematic source wall-alignment guides, not verified plot bounds. No scale is inferred from floor/plot areas.

A separate **4B GF approximate calibration-derived 1:100 A2 SVG/PDF** is available under `cad-redraw-v3/final/calibration/`. It uses eight explicit room/pool spans, 1.7% maximum fit residual, and a conservative ±3% working allowance. Print A2 420×594 mm at 100% / actual size, no fit. That does NOT make the plan survey accurate. The other eight remain NTS: one demonstrated conflicting overlay/board case and seven not independently validated. PNG zoom is never a fixed print scale.

## Ready / blocked
Ready: evidence review, file navigation and proposed evidence-led decor briefs.
Blocked: claiming source-matched room interiors, exact room polygons, certified openings/stair dimensions, fully dimensioned metric perimeters or faithful construction/3D reconstruction.

No interior images generated, no bot contacted, no 3D started, no ZIP delivered. The separate stage-2 bot is listed only as a handoff destination; the parent controls any transfer.
''')
# Check every referenced local deliverable path, without evaluating unresolved labels as facts.
paths=[]
for fl in floors:
 for k in ['description_path','source_plan_path','source_text_path','drawing_sheet_svg','drawing_plan_svg','drawing_preview','drawing_sheet_long7680','drawing_plan_long7680']:
  paths.append(fl[k])
for r in refs:paths.append(r['path'])
missing=[p for p in paths if not (R/p).is_file()]
assert not missing,missing
write(P/'handoff/package_verification.json',{'timestamp_Asia_Dubai':now,'floor_count':len(floors),'room_or_space_count':len(rooms),'interior_view_handoff_count':len(views),'source_reference_paths_checked':len(paths),'missing_referenced_paths':missing,'generated_visuals':0,'verified_room_interior_matches':0,'legacy_unresolved_labels':len(legacy),'geometry_review_required_floor_count':9})
print(json.dumps({'floors':len(floors),'room_or_space_records':len(rooms),'interior_missing_view_records':len(views),'legacy_unresolved':len(legacy),'missing_paths':missing,'ready_index':str(P/'project_index.json')},indent=2))
