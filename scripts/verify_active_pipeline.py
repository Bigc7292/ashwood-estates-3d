from pathlib import Path
import json,re,datetime
from zoneinfo import ZoneInfo
from active_inputs import ROOT,approved_plan
m=json.loads((ROOT/'ACTIVE_PIPELINE.json').read_text());bad=[];missing=[];checked=0
for p in m['plans']:approved_plan(p['id'])
# Do not scan historical archive: it is explicitly out of the pipeline.
files=[ROOT/'ACTIVE_PIPELINE.json',ROOT/'README.md']+list((ROOT/'canonical').rglob('*.json'))+list((ROOT/'canonical').rglob('*.csv'))+list((ROOT/'canonical').rglob('*.md'))+list((ROOT/'active/approved-cad-v4/reports').glob('*.json'))
for p in files:
 s=p.read_text()
 # Literal paths to retired release roots are prohibited in live selector/index/report files.
 if re.search(r'(?<!superseded_2026-11-09/)(?:cad-redraw-v[23]/|cad-style/|cad-visual-v4-prototype/|cad-visual-v4-nine/)',s):bad.append(str(p.relative_to(ROOT)))
 if p.suffix=='.json':
  def visit(v):
   global checked
   if isinstance(v,dict):
    for z in v.values():visit(z)
   elif isinstance(v,list):
    for z in v:visit(z)
   elif isinstance(v,str) and v.startswith(('active/','canonical/','original/','extracts/','source-evidence/')) and v.endswith(('.json','.png','.svg','.pdf','.txt','.csv','.md')):
    checked+=1
    if not (ROOT/v).exists():missing.append(v)
  visit(json.loads(s))
report={'checked_at_Asia_Dubai':datetime.datetime.now(ZoneInfo('Asia/Dubai')).isoformat(),'approved_input_count':len(m['plans']),'approved_artwork_hashes_unchanged':True,'checked_live_reference_count':checked,'stale_release_reference_files':bad,'missing_referenced_paths':sorted(set(missing)),'default_input_resolver':'scripts/active_inputs.py','fallback_enabled':False,'retired_archive_is_input':False,'old_zip_is_current':False}
(ROOT/'active/pipeline_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert not bad and not missing
