
## Round 1 (critic, 2026-11-03 ~03:30 Asia/Dubai)

**References used** (copied to refs/critic/): `cgi.png` / `plans_p1_cgi.png` (Howard & Seddon CGI "Context Impact" drg 12,982 M06 rev B, 26.11.20), `fefac.png` + `front.png` (architects' front elevation). barclay-house.com hero photo `Barclay_House-*.jpg` is bot-blocked (returns HTML); other site images are interior stock photos (discarded). Street View not scraped.
Caveat: the CGI shows a slate mansard with dormers above the cornice; the elevation drawing shows a flat attic storey + roof box. Treat CGI as proposal context; elevation is the build source for massing.

**Overall score vs online pictures: 3/10.** Massing/bay rhythm roughly right; materials, lighting, context and realism far below the CGI.

Defects (ranked by visual impact):
1. **Flat, uniform, overexposed lighting / no sky.** Ref CGI: deep blue sky with clouds, strong directional sun, shadowed returns, contrast. Render: pale grey-blue flat sky, near-shadowless frontal light, washed-out cream. Fix: Nishita/HDRI sky with clouds, sun ~35–45° elevation from the side (not frontal), Filmic/AgX "Medium High Contrast", exposure −0.5.
2. **Head-on orthographic-looking street camera.** CGI: 3/4 corner view from street level, ~1.6 m eye height, 2-point perspective, showing the front + side return. Render: dead-frontal, symmetrical, elevation-like. Fix: add a 3/4 hero camera matching the CGI (use camera_match.py on cgi.png), ~24–28 mm, vertical shift to keep verticals straight.
3. **Base and upper materials look identical (cream with faint brick pattern).** CGI: grey, heavily textured/rusticated stone base with deep horizontal channels, clearly darker than the pale glazed upper. Render: base and upper same cream; base reads as stacked planks with white stripes across the arched windows. Fix: separate Portland stone mat (cool grey, rough 0.7, weathering/dirt AO in joints), deeper rustication grooves; remove the horizontal lines crossing the arch glazing.
4. **Terracotta upper has a brick/block coursing pattern and no faience sheen.** Elevation shows large ashlar-style faience blocks; source says smooth white faience. Render: small brick-like courses with noisy bumps. Fix: larger block size per elevation, very fine joints, roughness ~0.25 with clearcoat, slight colour variation per block, soot streaks under sills/cornices.
5. **Arch keystone/voussoir surround missing.** Elevation: each ground-floor arch has a radiating voussoir fan reaching up to the first-floor band, plus pilasters between arches. Render: plain round-headed openings punched in the wall with thin trims. Fix: model radiating voussoirs (~13–15 per arch) and stepped imposts.
6. **Entrance wrong.** Elevation/CGI: projecting central porch with tall door, glazed fanlight panel above, flanking pilasters and steps. Render: a blank rectangular window block over a pale plinth, no door. Fix: model recessed doorway, steps, framed panel above, pilasters to first-floor band.
7. **Upper bay rhythm/details simplified.** Elevation: 15 bays but grouped — giant pilasters between bays, two pedimented end bays (floors 1–3) with triple windows, wider corner bays with single windows, multi-pane (glazing-bar) sashes. Render: uniform equal bays, single-pane grey glass, no pediments. Fix: add the two aedicule/pediment bays, 3-light window groupings, glazing bars per elevation.
8. **Cornice/attic proportions.** Elevation: main cornice below an attic storey of 15 full-size windows, small horizontal oculus-like windows at the corners, light parapet. Render: attic windows are short letterbox slots and the top cornice is a heavy slab overhang. Fix: attic windows to elevation height, thinner moulded parapet cornice, add corner small windows.
9. **Glass is opaque grey, no reflections/interior.** CGI: dark reflective glass with sky reflections, frames visible. Render: matte flat grey panes. Fix: glass IOR 1.5 with roughness 0.02 over an interior-mapping/emissive-dim room card; dark frames.
10. **Neighbours are untextured beige extrusions with brick-noise; viaduct pink/salmon.** CGI: real red-brick viaduct with deep arches, varied modern/red neighbours, detailed streets. Render: identical sandy boxes, roofs same colour as walls, pink plasticky viaduct and parapet, no arches visible from street. Fix: per-building material variety (red brick, render, glass), dark roofs, proper deep-red/blue brick viaduct with soot, rails on sleepers/ballast.
11. **No life/realism cues.** CGI: trees framing shot, cars, pedestrians, cyclists, road markings, setts paving, street lamps. Render: empty flat paving, no road, kerbs or props. Fix: road with markings and kerbs, setts texture, free CC0 trees/cars/people (Poly Haven / BlenderKit free), bollards and lamps.
12. **No weathering.** Everything looks new and clean. Fix: grime masks (AO + pointiness) darkening joints, sill drips, base dirt band.
13. **Aerial: roof is cream like walls and stair-tower box is a plain cube; ground and all roofs same tone.** Fix: dark roof membrane/asphalt, plant/roof details, ground/roads separated by colour.
14. **Viaduct shot: Barclay House is hidden behind a giant parapet in the foreground and a dark box neighbour dominates; sky haze is flat.** Fix: lower parapet height relative to camera or raise camera, reframe so hero is the subject.
15. **Night preset:** windows are lit as flat white rectangles with identical brightness, facade is dark and muddy, no street-lamp pools. Fix: varied warm emission + curtains, facade uplight/lamp light pools, deep blue night sky instead of black.

## Round 1 fixes applied (2026-11-03, Asia/Dubai)
1. Lighting: Nishita sky with a procedural cloud layer (CLOUD_COVER), sun from NOAA position at midday 15:30 (side light, not frontal), AgX "Medium High Contrast", day exposure −0.5. Clouds are a stand-in.
2. New default camera Cam_Hero_34 (3/4 view from the pavement, 1.6 m eye height, 16 mm lens, shift 0.2) showing the front and east return. Street, aerial and viaduct cameras kept. Placed by hand, not solved with camera_match.py: the first CGI-like pose (west of the facade) started inside a neighbour.
3. Stone base: separate cool-grey Portland stone (0.62, roughness 0.75), recessed dark rustication channels that stop at openings. The cross-arch white lines are gone because the grooves now stop at the arches. Clearer glass/frames.
4. Faience: procedural large blocks 1.2×0.55 m, fine joints, glossy coat, per-block tone variation, soot streaks/dirt (weather()). Block size is a stand-in (E05 shows ashlar coursing, not dimensioned).
5. 13 radiating voussoirs per arch (longer keystone) plus pilasters between arches.
6. Projecting entrance porch: pilasters, entablature, door, framed fanlight panel, 8 steps (step count is a stand-in).
7. Upper bays per E05: two pedimented aedicule bays with triple windows at 0.127–0.223 and 0.777–0.873 of the width, 13 single bays between, wider corner/pavilion bays, giant pilasters with capitals, glazing bars (glass(panes=…)).
8. Attic windows full height (L4+0.7 to roof−0.85), small corner windows, thinner cornice (0.55×0.32 m) and parapet (0.25 m). Mansard in the CGI not modelled: it is a planning proposal (128804/FO/2020), not built.
9. Glass: dark base (0.01), roughness 0.02, reflective, with dark frames and glazing bars.
10. Neighbours: varied stand-in materials by id hash (red brick, cream render, grey cladding, glass curtain wall for tall blocks), dark roofs. Viaduct deep red brick (0.36,0.14,0.09) with weathering (Heritage Statement: "Red brick with some small sections of blue brick").
11. Roads: kerbs and dashed centre markings (stand-ins), trees and lamps kept. No cars or people yet (open).
12. Weathering: base dirt band and soot streaks on stone, faience, viaduct and neighbours (stand-in).
13. Roofs dark (0.13), separated from walls and ground. Stair tower detail still basic (open).
14. Viaduct camera raised to deck +6.5 m, 28 mm lens, reframed on the hero.
15. Night: deep blue night sky (0.012,0.025,0.09), window emission varied per window in strength (0.25–1.2×) and warm colour, overall window glow reduced to 0.3×, 7 facade uplights (stand-ins) plus street lamps.

### Round 1 addendum: Interior-bot viewer critic (interior/critic_log.md, section B) folded in
- B1 (no glass in GLB): root cause found. The window/arch boolean modifiers were dropped in the R1 hero rewrite, and export_glb.py also deleted the cutters before applying the modifiers. Fixed both. Glass is exported as "Glass_dark": alphaMode BLEND, alpha 0.85, doubleSided, roughness 0.03, dark tint. Checked in model-viewer (three.js): web/shots/hero_glb_r1.png.
- B2 (rubble-like stone texture): the GLB stone and faience now use smooth flat PBR colours (stone 0.62 grey, roughness 0.75; faience 0.86/0.84/0.78, roughness 0.2) instead of the tiled brick-like JPEG.
- B3/B4: deep arch reveals, voussoirs and keystones are in place. The 8 entrance steps were unsourced and are removed. The DAS lobby level (+2.10 m) is assumed to be handled internally: NOT FOUND in any elevation.
- B5/B6: cornice (0.55 m projection), first-floor band and giant pilasters per E05, as in items 5–8 above.
- B7/B8: lighting as in item 1. Granite setts: NOT done (no CC0 setts texture integrated yet; open).

## Round 2 fixes applied (2026-11-03, Asia/Dubai). Source: interior/critic_log.md "Critic Round 2" items 13+, real photos refs/critic1/real_commons.jpg (https://commons.wikimedia.org/wiki/File:Barclay_House,_Manchester.jpg, 2015) and real_geograph.jpg (https://www.geograph.org.uk/photo/8144686, Jul 2025)
1. Colour: faience changed to warm buff (linear 0.62/0.54/0.39 ≈ sRGB #CFC3A6, the critic's target read from the photos), darker joints, block grid 0.9×0.45 m. The block size is read off the photos, not measured, so it's a stand-in. Portland base is slightly darker/greyer buff. GLB uses the same flat colours.
2. Windows: white-painted frames and small-pane glazing (4×5 / 3×5 / 6×6 panes), matching the 2015 Commons photo. Exact pane counts are a stand-in. Black frames were the planned-conversion CGI look (Rightmove, LoopNet) and are no longer used.
3. Arches: 9 larger fanned voussoirs per arch with a longer keystone (Commons/Geograph). The heavy band above is the existing first-floor band. Grooved piers kept (rustication channels).
4. Entrance: doorway at pavement level with dark double doors, a stone lintel and a small multi-pane window above, between pilasters with an entablature (Geograph 2025). No external steps: Commons 2015 shows the steps inside the doorway. Moulding profiles are not modelled (open).
5. Oriels: projecting bays on floors 1–2 at both triple-window bays (Commons). The projection depth (0.6 m) is NOT FOUND and is a stand-in. Small triangular pediments now sit over the corner-bay first-floor windows (both photos) instead of the earlier large pediments over the triple bays. Heraldic cartouches/carved panels seen in the photos are NOT modelled (open).

## Round 3 fixes applied (2026-11-03, Asia/Dubai). Source: interior/critic_log.md "Critic Round 3" items 9–11 + own open items; refs real_commons.jpg (2015), real_geograph.jpg (2025)
1. Ground-floor stone: one warm Portland stone material (linear 0.58/0.52/0.40 ≈ sRGB #C9BFA8) on every base object, in both the Blender scene and the GLB. The blue-grey right half in the web viewer is a neighbour's cast shadow lit by blue sky, not a second material.
2. Decoration (all sizes/depths are stand-ins; none is dimensioned in any source):
   - Large oval cartouches with scroll heads on both end bays at ground floor (Commons left, Geograph right).
   - 'RB' monogram shields: plain shield discs on the piers beside the oriel bays at floors 2–3. The monogram relief itself is not modelled.
   - The pediments over the end-bay windows were added in R2 and are kept.
   - The left-end oriel was added in R2 and is kept.
   - Heavier top cornice: 0.85 m projection × 0.55 m.
3. Arches:
   - Larger voussoirs (1.0 m, keystone 1.25 m).
   - Fanned glazing bars and a hub inside each arch head.
   - Upper windows are now paired, with broad piers (0.76 m) at every second bay. This follows the photos; E05 positions are kept. Because 13 bays can't pair evenly, the end bay is a single.
4. Faience is warmer and darker (0.55/0.47/0.33 and 0.50/0.43/0.30 per block).
5. Doorcase: stepped three-fascia moulded architrave with a stepped head (profile is a stand-in).
6. Viaduct: deep red brick (0.24/0.075/0.045) per the Heritage Statement ("Red brick… sandstone dressings"), with weathering. The salmon tiled texture is dropped.
7. Neighbour roofs: three dark stand-in roof finishes (membrane, dark slate, asphalt), assigned deterministically by crc32 of the OSM id.
8. Roads trimmed to the terrain/LIDAR extent: no lines run past the edge.
9. Street: the Geograph 2025 photo shows an asphalt carriageway on Whitworth St W, not granite setts, so I kept asphalt with kerbs and markings (stand-ins) and flag paving on the footway. Setts are NOT added because the source shows asphalt.

### Round 3 results + x-bookmarks tricks (2026-11-03 07:50 Asia/Dubai)
Outputs (07:00–07:40):
- 4K stills: out/render_{hero,street,aerial,viaduct}_4096x2304.png.
- Previews: out/tod_*_hero_960x540.png (re-rendered after the cartouche fix).
- GLBs: out/barclay_hero.glb (4.8 MB), out/barclay_surroundings.glb (36.2 MB).
- GLB screenshot: web/shots/hero_glb_r3.png.

Still NOT fixed (seen in the 4K results):
- Neighbour roofs still render pale in the aerial, and the viaduct parapet still reads salmon. The material change didn't take visible effect; the cause still needs tracing (prism top-face index or weather() lightening).
- The cartouche on the left end bay first overlapped the small window; it has been moved to z = 3.2 m.

Tricks from /home/box/x-bookmarks/:
- APPLIED: PBR finish presets (implementations/offplan/2026-11-02-pbr-finish-presets.md, "polished/glazed": clearcoat 1, clearcoatRoughness 0.05). Used for the faience because sources call it "vitreous"/"smooth white faience". Set in both the Blender faience and the GLB (KHR_materials_clearcoat).
- APPLIED: teardown-style render-vs-reference check (ref_check.py). Baselines: hero 4K vs real_commons.jpg edge_F1 0.428; street 4K vs real_geograph.jpg edge_F1 0.501 (tests/r3_*_check.png). The cameras aren't matched yet, so these are baselines only, not accuracy scores.
- SKIPPED (time and CPU): camera_match.py solve to the Commons/Geograph photos. That is the next step, so ref_check scores become meaningful.
- SKIPPED: Blender MCP locked-camera dressing (2026-11-02-blender-mcp-reference-match.md). It's an interior and furniture workflow; the exterior is scripted and deterministic.
- SKIPPED: deterministic tour MP4 and low-GPU tiers (backlog #15). These belong to the viewer, not to facade quality.
- /workspace/barclay/x_tricks.md does not exist.

## Round 4 (2026-11-03 ~08:00 Asia/Dubai). Rules: AGENTS.md read first. Tools used: Blender 4.2.3 (-y), camera_match.py, ref_check.py, export_glb.py, make_mobile.sh, gltf-transform validate (Khronos validator). Blender MCP was not used (no session open), so the blend was not saved while an MCP session had it.
### 1. Root cause: pale neighbour roofs and salmon viaduct
- Checked via bpy: the material assignments were correct. Neighbour tops use Roof / Roof_grey_membrane / Roof_dark_slate (polygon index 1), and the parapets use Viaduct_brick.
- An emission test (roof = red, viaduct = green) showed the right surfaces, but desaturated.
- Cause: in tod_panel.apply(), the Nishita sky had `sun_disc = True` on top of the sun lamp (energy 4). Direct sun was counted twice, so a 0.13-albedo roof rendered at RGB about 220.
- Fix: `sun_disc = False`; the sun lamp alone gives the direct light. Test render: the roof pixel dropped from 220 to about 132, roofs read dark, and the viaduct reads deep red.
### 2. Camera match + ref check (locked cameras Cam_Match_geograph and Cam_Match_commons; one change per pass)
- Points: tests/{geograph,commons}_points.json. These are 6 pixel picks per photo on the parapet corners, first-floor band ends and entrance, read off a grid overlay. Their 3D positions come from E05 levels and width.
- Solve results:
  - Geograph: rms 14.2 px, lens 21.7 mm.
  - Commons: rms 39.3 px, lens 24.2 mm. The point picks are poorer here because of the occluded corners.
- Scores (edge F1 / precision / recall):
  | pass | change | Geograph | Commons |
  |---|---|---|---|
  | baseline (R3, unmatched cams) | none | 0.501 | 0.428 |
  | p1 | matched cameras + sun_disc fix | 0.621 / 0.688 / 0.566 | 0.611 / 0.730 / 0.525 |
  | p2 | day exposure −0.5 → 0.0 | 0.622 / 0.683 / 0.571 | 0.616 / 0.730 / 0.533 |
  | p3 | oriel raised to floors 1–3 (Commons photo shows 3 storeys) | 0.625 / 0.685 / 0.575 | 0.614 / 0.726 / 0.532 |
- Check sheets: tests/match_*_p{1,2,3}_*_check.png.
- The photos (Geograph Jul 2025) have summer sun on the facade. The renders use the Nov 3 sun, so colour isn't directly comparable; the edge score measures geometry.
### 3. Faience clearcoat capped for web
- Coat 0.6, coat roughness 0.15 (x_tricks #3), in both Blender and the GLB (KHR_materials_clearcoat).
- GLBs re-exported 08:03 (temp+mv): barclay_hero.glb 4.84 MB, barclay_surroundings.glb 36.18 MB.
- make_mobile.sh 08:04: barclay_hero_mobile.glb 1.74 MB, barclay_surroundings_mobile.glb 4.73 MB.
- Khronos validator (gltf-transform validate): 0 errors on all 4 files. The only warnings are MESH_PRIMITIVE_GENERATED_TANGENT_SPACE on normal-mapped materials, which are harmless.
- Interior bot: please redeploy the viewer with the new out/mobile + full GLBs.
### x_tricks.md
1. One-change-per-pass critic loop with a locked camera: APPLIED (section 2 above).
2. Meshopt + KTX2: SKIPPED this round. make_mobile.sh already gets the mobile files under 5 MB. Changing the output format needs the viewer's decoder/KTX2Loader updated, which is the Interior bot's side. Proposed next.
3. Clearcoat preset: APPLIED (coat 0.6 / 0.15). Glass transmission is set in the viewer, not in my export (my glass is alpha-blend), so I SKIPPED it here.
4. Render-check-before-animate gate: SKIPPED. There's no flythrough this round.
5. Clickable floor/unit showcase: SKIPPED. It's a viewer feature, and unit-to-floor mapping data is NOT FOUND.
6. mcp-for-blender-pro + Ollama: SKIPPED. Its licence is unverified, and the existing Blender MCP plus scripts already cover this.
### Stand-ins kept from R3 (still labelled)
- Cartouche and shield sizes and depths, top cornice size, oriel depth 0.6 m, doorcase profile, window pane counts, neighbour materials and roofs, kerbs and markings, soot and weathering, clouds, uplights.

### Round 4 final (2026-11-03 08:50 Asia/Dubai)
- 4K stills, all rendered after the fixes: hero 08:18, street 08:28, aerial 08:35, viaduct 08:47 (out/render_*_4096x2304.png). Previews: out/tod_*_hero_960x540.png, about 08:10.
- sun_disc fix, visible result:
  - Aerial: worked. Neighbour roofs now read dark grey or slate, and the viaduct deck and arches read red brick.
  - Viaduct close-up: only partly. The parapet's side faces are red, but its sunlit top and inner faces still read salmon or orange under direct sun. Open: darken the albedo further, or add brick texture variation (stand-in).
- ./validate.sh: PASS (tests/validate_20261103_0841.jsonl). 0 errors, and all files are within budget: hero 4.61 MB, mobile hero 1.66 MB, mobile surroundings 4.51 MB, surroundings 34.5 MB.

## Exterior 7-step, Step 6 critique (2026-11-04, branch `exterior-7step`)
- Round: first 7-step pass. Reference: `refs/exterior_target.png` (look only), real photos for facts.
- Score: not scored (own still). Needs Colin or an independent critic.
- Defects and fixes: D1–D9 in `ext7/step6/CRITIQUE.md` (terrain through the road, sky-blue ledges, near-black neighbour, door speckle, small notice, clean faience, streaky neighbour walls traced to stretched photo textures).
- Rules used: hard rule 2 (stand-ins labelled), rule 5 (temp file then move for the .blend), rule 6 (commit per step), lesson "tiled stone reads as rubble" (Portland and neighbours to flat colour).
- Tools: Blender 5.2 bpy module (headless). No Blender MCP in this session. Cycles CPU 16 samples with denoise.
- Tricks applied: none from x_tricks.md this round (not on this branch).

## Colin's notes, 2026-11-08
1. White glazing bars, where Street View shows them dark. Fixed (see `ext7/step6/CRITIQUE.md` C1).
2. BARCLAY HOUSE not clearly visible. Fixed with a granite band, raised pale serif letters, and an Entrance view (C2).
3. 2-bed furniture blocky. Fixed: a real sofa and real dining chairs, soft bedding, and bevels on the rest (`interior/FURNITURE_V5.md`).

Checked in headless Chromium against the local viewer (entrance, living, kitchen, bedroom 1 and 2). No console errors. The video and stills on `/video/` were rendered before these fixes.
