"""Fail-closed source selection: approved V4 only, never archived fallback."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def approved_plan(plan_id):
 m=json.loads((ROOT/'ACTIVE_PIPELINE.json').read_text());assert m['status']=='ONLY_APPROVED_V4_INPUTS_ACTIVE'
 rows=[p for p in m['plans'] if p['id']==plan_id]
 if len(rows)!=1:raise ValueError('Plan is not uniquely approved: '+plan_id)
 p=rows[0]
 for k in ['svg','pdf','preview','long7680']:
  path=(ROOT/p[k]).resolve();assert path.is_relative_to(ROOT/'active/approved-cad-v4'),path
  if not path.is_file():raise FileNotFoundError('Approved input missing; no fallback: '+str(path))
  if hashlib.sha256(path.read_bytes()).hexdigest()!=p['sha256'][k]:raise ValueError('Approved artwork changed: '+str(path))
 return p
if __name__=='__main__':
 import sys
 if len(sys.argv)!=2:raise SystemExit('Usage: active_inputs.py 4B-GF')
 print(json.dumps(approved_plan(sys.argv[1]),indent=2))
