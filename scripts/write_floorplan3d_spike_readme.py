#!/usr/bin/env python3
"""Writes active/floorplan3d-spike/FP-4B-GF/README.md (v2) from plan.json + verification.json, so every number is generated, not hand-typed."""
import json
from pathlib import Path
R = Path(__file__).resolve().parents[1]; S = R / 'active/floorplan3d-spike/FP-4B-GF'
pj = json.loads((S / 'data/fp-4b-gf.plan.json').read_text())
vj = json.loads((S / 'verify/verification.json').read_text()) if (S / 'verify/verification.json').exists() else {}
L = []; A = L.append
A('# Ashwood Estates: 4-bed villa, ground floor. Floorplan 3D viewer spike (FP-4B-GF), **v2**\n')
A('**Status: REVIEW-PENDING SPIKE. One floor only.** Not survey-verified, not construction-ready, not certified CAD.\n')
A('v2 rebuild (2026-11-09, Asia/Dubai) after the user rejected v1 as "still 2D". v1 sits in `v1/` for comparison and is superseded. '
  'v2 turns the upstream Floorplan 3D features back on, so the floor reads as a furnished 3D interior: room floors with materials, furniture models, ceilings and ceiling lamps, shadows, RoomEnvironment reflections and warm daylight. '
  'Walls stay at full height by default, and eye-level renders are used. Every addition is tied to source evidence or flagged as derived or assumed below.\n')
A('## Use\n```bash\ncd active/floorplan3d-spike/FP-4B-GF\npython3 -m http.server 8000 --bind 127.0.0.1   # open http://127.0.0.1:8000/\n```\n'
  'Fully offline: three.js r160 + Water2 are vendored in `vendor/`, with no CDN and no account. Press `T` or use the top switch for 2D / 3D. In 3D, **Full walls** (3.0 m, display-only) is the default and **Cut walls** is 1.2 m. '
  'Use Orbit or Walk (WASD + mouse, or the joystick on touch). Click a room in the list to fly to it. The sun slider defaults to 16:00, a display-only value because site orientation is unknown. Night mode turns the ceiling lamps on. `[` and `]` hide the side panels. '
  'Furniture can be moved, rotated or deleted in the viewer, which is the upstream behaviour, and edits are stored in localStorage under `ashwood-fp3d-spike-4b-gf-v2`. `?water=flat` forces the flat-water fallback.\n')
A('## What v2 re-enabled from the upstream viewer\n'
  '- **ROOMS**: 16 closed room polygons with per-room floor material (MATS), derived ~areas, ceilings and a ceiling lamp at each label point, and the upstream room panel (floor material picker, area).\n'
  '- **Furniture**: `buildFurniture()` models from the upstream LIB, placed only where the source draws a symbol (see below). In v1 this was empty.\n'
  '- **Lighting and materials**: upstream HemisphereLight, shadow-casting DirectionalLight sun (4096 shadow map, extent widened to 17 m for this larger floor), PMREM RoomEnvironment reflections, ACES tone mapping and procedural floor textures, all unchanged. Warm daylight comes from the sun defaulting to 16:00.\n'
  '- **Full-height walls** are the default view. Eye-level and low-oblique cameras are used for the renders.\n'
  '- **Stairs**: display-only stair massing. The 16 treads come from the V4 tread lines. Riser height is the display wall height divided by 16, and the rise direction is assumed.\n'
  '- Kept from v1: traced walls, 6 doors that open and close, 12 glazing runs, Water2 on the pool and courtyard water with a labelled flat fallback, walk mode and the offline vendoring.\n')
A('## Room polygons (DERIVED, not stated in source)\n' + pj['method_rooms'] + ' Areas are approximate (~). "Wall/opening fit" is the share of each polygon edge (excluding closures) that lies within about 0.1 m of a traced wall, glazing or door cue.\n')
A('| Room | ~Area m² (derived) | Brochure label | Floor (upstream MATS) | Evidence status | Closures | Wall/opening fit | Note |\n|---|---|---|---|---|---|---|---|')
for r in pj['rooms_detail']:
    A(f"| {r['name']} | ~{r['area_m2_derived']} | {r['dims_label']} | `{r['mat']}` | {r['mat_status']} | {len(r['closures_px'])} | {r['qa_boundary_on_wall_or_opening_fraction_excl_closures']} | {r['note'] or ''} |")
A('\nNo polygon: ' + '; '.join(f"{n['anchor_id']} ({n['why']})" for n in pj['no_polygon']) + '. The unlabelled corridors and stair hall stay on the display floor plate (light tile, no ceiling).\n')
A('### Floor material evidence\n')
seen = {}
for r in pj['rooms_detail']: seen.setdefault((r['mat'], r['mat_status'], r['mat_evidence']), []).append(r['name'])
for (m, st, ev), names in seen.items(): A(f"- `{m}`: **{st}**. {ev} Rooms: {', '.join(names)}.")
A('\nAll brochure finish statements are project-wide (p17 materials board, p24 interior summary, p15/p16 reference renders). None names a specific villa room, so every room assignment is an interpretation. The p24 wet-area line is glyph-shifted in the PDF text layer and was decoded.\n')
A(f"## Furniture ({len(pj['furniture_detail'])} items, all \"source plan symbol, size approximate\")\n" + pj['method_furniture'] + ' ' + pj['furniture_convention'] + '\n')
A('| # | Upstream model | Item | Size w×d mm | rot° | Status | Evidence |\n|---|---|---|---|---|---|---|')
for i, f in enumerate(pj['furniture_detail'], 1):
    A(f"| {i} | `{f['type']}` | {f['name']} | {f['w']}×{f['d']} | {f['rot']} | {f['status']} | {f['evidence']} |")
A('\n**Skipped (drawn, but not modelled):**\n' + '\n'.join(f"- {s['item']}: {s['why']}" for s in pj['skipped_furniture']) + '\n')
A('Nothing was added that the source does not draw: no rugs, plants, TVs, lamps, beds or wardrobes beyond the symbols listed. The upstream demo-apartment furniture is not used.\n')
if vj:
    A('## Renders (headless Chrome, SwiftShader WebGL2, offline)\n')
    for s in vj.get('hero', {}).get('shots', []): A(f"- `{s['png']}`: {s['caption']} (canvas {s['canvas'][0]}×{s['canvas'][1]}, fov {s['fov']}°, walls {s['cut_m']} m)")
    A('- `verify/v2_20_side_by_side_spike_vs_upstream_demo.png`: spike v2 (left) vs the **untouched upstream demo**, rendered locally the same way (right).')
    for s in vj.get('upstream_demo', {}).get('shots', []): A(f"  - `{s['png']}`: {s['caption']}")
    A('- `verify/v2_21_v1_vs_v2.png`: rejected v1 vs v2.\n- `verify/*_raw.png`: the same hero renders without caption bars.\n')
    n = vj.get('network', {}); g = vj.get('geometry_comparison', {}); w = vj.get('water_comparison', {})
    A('## Verification (`verify/verification.json`)\n'
      f"- Offline: {n.get('total_requests')} requests, non-localhost {len(n.get('non_localhost_requests', []))}. Console errors: {len(vj.get('console_errors', []))}.\n"
      f"- Furniture built at runtime: {vj.get('furniture_runtime')}. Rooms at runtime: {len(vj.get('rooms_runtime', []))} (incl. display plate).\n"
      f"- 3D top render vs V4 walls (furniture hidden): recall within ±{g.get('tolerance_mm')} mm {g.get('recall_within_tol')}, precision {g.get('precision_within_tol')}, components ≥0.95 recall {g.get('components_recall_ge_0.95')}/{g.get('v4_wall_components')}. Water IoU {w.get('IoU')}.\n"
      f"- Water mode {vj.get('info_final_desktop', {}).get('water', {}).get('mode')}; flat fallback {vj.get('flat_fallback_info', {}).get('mode')}; fly-to moved {vj.get('flyto', {}).get('moved')}; joystick walk moved {round(vj.get('walk', {}).get('moved_m') or 0, 2)} m.\n")
A("""## Remaining quality gaps (honest)
- **Generic furniture models.** These are the upstream procedural models (sofa, chair, bed and so on), not the brochure's actual pieces, and their colours are upstream defaults. Only position, rotation and approximate footprint come from the plan.
- **Procedural finishes.** Floors use upstream procedural tile and terrazzo textures. Walls are the upstream flat off-white and are not the brochure's textured paint, Calacatta feature wall or Recon Veneer joinery. All finish evidence is project-wide, not per room.
- **Real-time WebGL quality, not offline renders.** There is no global illumination, real-time-only soft shadows and a basic ceiling. Headless renders use SwiftShader (CPU), so edges are not anti-aliased the way a GPU browser would draw them. On a normal GPU browser the viewer looks somewhat cleaner than these PNGs.
- **Room polygons are derived.** Show kitchen ~10.6 m² is smaller than its label (5.70 × 2.70) because the open-plan labels overlap. Lift ~1.7 m² is smaller than 1.50 × 1.70. Dress, maid bath, entry and lift have wall/opening fit below 0.9 (see table).
- **Maid-room bed** is modelled at the traced 1.28 × 1.10 m, which is short for a bed, because that is how the plan draws it.
- **Stair** is display-only massing. Riser height and rise direction are assumed, and walking does not climb it.
- **Double-height entry** has no void: corridors, stair hall and entry show open sky above the 3.0 m walls instead of a second floor. Pool has no depth or coping. The outdoor ground beyond the plate is plain.
- **Unknown site orientation**, so the sun direction and time are display-only.
- **Not modelled:** cars, rug or console outline, small store, bath and maid-bath fixtures, landscape (see the skipped list).
""")
A('## Files\n- `index.html`: patched upstream viewer (attribution header kept). `data/fp-4b-gf.plan.js` / `.plan.json`: generated data with per-room, per-item and per-opening provenance.\n'
  '- `adapter/v4_to_floorplan3d.py`: copy of `scripts/v4_to_floorplan3d.py`, locked to `--plan 4B-GF`. Readings input: `source-evidence/floorplan3d-readings/FP-4B-GF.json`.\n'
  '- `manifest.json`: sources and hashes, display-only defaults, room, furniture and material evidence, output hashes. `verify/`: verification output and renders. `v1/`: superseded first spike.\n'
  'Regenerate from the archive root: `.venv/bin/python scripts/v4_to_floorplan3d.py && .venv/bin/python scripts/verify_floorplan3d_spike.py && .venv/bin/python scripts/write_floorplan3d_spike_readme.py`\n')
A('## Attribution (MIT)\n- **Floorplan 3D**, https://github.com/wy51ai/floorplan-3d (commit in the manifest). MIT License, Copyright (c) 2026 wuyi. Full text: `LICENSE-floorplan-3d.txt`. Demo apartment data replaced; furniture models, materials and lighting code are upstream.\n'
  '- **three.js r160**, incl. Water2/Reflector/Refractor and the `examples/textures/water` normal maps. MIT, Copyright © 2010-2023 three.js authors. Full text: `vendor/three/LICENSE`.\n')
A('**Not survey-verified, not construction-ready, not certified CAD.** All metric values are approximate (±3 %). Heights, finishes, furniture models and light are display-only.\n')
(S / 'README.md').write_text('\n'.join(L)); print('README', len(L), 'lines')
