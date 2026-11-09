# Critic log – Legacy project viewer
## Round 0 (self-review, 2026-11-03 03:55 Asia/Dubai) – no independent critic spawned yet (parent to run critics)
Live: https://legacy-house-viewer.vercel.app (deploy dpl_8coEe7DGh95AuvWPhqmXQEjKRCKx)
Open defects:
1. Facade close-up (shots/facade_midday.png): arched ground-floor openings and upper windows read as stone/faience, no visible glass; stone texture tiles like small brick. Geometry/UV/material are in exterior bot's legacy_hero.glb, report to that bot. Not yet compared with real photos.
2. Interior: black rectangular gap in floor between living and hall (closeup_living_kitchen.png); cause not yet traced.
3. Interior: dining chairs are tufted Poly Haven dining_chair_02, style unlike listing photos (not compared yet); table+4 chairs crowd kitchen/dining (9.4 m2 approx).
4. Interior: bedroom 2 camera clips into wardrobe (closeup_bedroom2.png); camera position needs moving.
5. Interior: no windows/doors modelled (window positions NOT FOUND); walls full 3.663 m (clear height NOT FOUND).
6. Headless interior screenshot of live viewer timed out (software GL); exterior live verified.

## Critic Round 1 (independent critic, 2026-11-03 ~04:10 Asia/Dubai)
References downloaded to /workspace/legacy/refs/critic1/ (Rightmove 92163630 Apt 02, 92161311 Apt 03, 92992530 studio: all photos + floor plans; contact sheets sheet_*.jpg). Existing refs/critic/front.png (H&S rear elevation D06) also used. legacy-house.com/LoopNet/BE News not re-fetched this round; the Rightmove CGI exterior (same image on all 3 listings) was the facade reference.
Note: Rightmove interior photos are CGI/staged marketing images, and shared across listings, so they show the scheme's spec rather than proving the finishes of this exact flat.

### (A) Two Bed interior: score 2/10
1. HIGH. Black hole in floor between living and hall (closeup_living_kitchen, latest.png). Real: continuous floor. Fix: find the missing floor polygon or z-fighting hole in build_twobed_furnished.py and close it with one floor slab under the whole unit.
2. HIGH. Kitchen is wrong. Real: a full-height wall of handleless white or warm-cream units, black integrated microwave in the upper bank, black washing machine under the counter, stainless sink and gooseneck tap, flush black induction hob, LED strip under the wall units, and in Apt 02/03 a dark peninsula with a built-in black oven. Ours: grey box base, flat grey panel on the wall, no appliances, sink, tap or doors. Fix: model a base run plus wall units at 600 mm modules with 2–3 mm door gaps, and add the appliances, the under-cabinet emissive strip and the dark island.
3. HIGH. Furniture style mismatched. Real: navy velvet 3-seat sofa, oak-and-black-metal coffee table, cream boucle tub dining chairs on a small round table, cream rug, oak TV unit, framed monochrome art, potted plant, white globe pendant. Ours: tufted brown chesterfield dining chairs, a tufted grey settee, a dark mahogany pedestal table and a slatted sideboard. Fix: swap for a navy sofa, boucle chairs and oak pieces, using Poly Haven/CC0 models or simple modelled ones with recoloured materials.
4. HIGH. No windows or doors. Real: large black steel multi-pane window with a round-arched head (arched window visible in the bedroom photos) and door openings shown on the floor plan. Ours: sealed white boxes. The window position is unsourced, but its type is shown in the photos. Fix: add at least one black-framed arched window per the photos, marked "position unsourced", plus door openings and leaves per the Rightmove plan swings.
5. HIGH. Bedrooms bare. Real: navy velvet upholstered bed with a channel-tufted headboard, white bedding with a navy throw and cushions, oak bedside tables with drawers, mushroom or globe lamps, a tall oak 2-door wardrobe, framed art. Ours: a plain white block bed with a grey board headboard and an antique dark nightstand. Fix: build the bed per the photo, use the oak wardrobe the plan shows, and add the lamps and the art.
6. HIGH. Camera clips through furniture (bedroom2 shot is mostly a blurry wardrobe top, plus a black pole). Fix: put the camera at 1.5 m eye height inside the free floor area and check for collisions before taking each shot.
7. MED. Ceiling reads flat blue (sky or unlit), and the walls go up the full 3.663 m with no ceiling, downlights or skirting. Real: a warm white ceiling with recessed downlights, skirting boards and light-warm walls. Fix: add a ceiling at the clear height (mark the value unsourced, e.g. ~2.7–3.0 m), recessed spot emitters and a 100 mm skirting.
8. MED. Lighting is flat and cold, with no warm interior glow or soft shadows. Real: warm 3000 K, a soft daylight window key, gentle vignetting. Fix: use warm area lights or emissive downlights, a sun/sky through the window, ACES/filmic tone mapping, and SSAO or baked AO.
9. MED. Floor material. Real: light natural oak in the living room and bedrooms, pale grey wood-look in the kitchen area photo. Ours: an orange, over-saturated oak with very large grain scale. Fix: desaturate and lighten, set the plank width to about 180 mm at correct UV scale, and lower the roughness variation.
10. MED. Bathroom missing or not shown. Real: white wall-hung basin on a grey vanity, black-framed mirror, chrome heated towel rail, glass-walled walk-in shower, grey large-format tiles, back-to-wall WC. Fix: model it to that spec.
11. LOW. The Dollhouse view (latest.png) has grey-blue wall tops and dark ground tiles that read like a site model, and the plan outline is not the angled, splayed shape on the Rightmove plan (two bedrooms at the top, entrance at the bottom centre). Fix: trace the outline from apt02_fp.png at the 679 sq ft scale.
12. LOW. There's no styling or props (plants, art, books, cushions) like the photos have.

### (B) Exterior facade: score 2/10
1. HIGH. No glass anywhere. Real (Rightmove CGI): large dark-glazed, black steel-framed multi-pane windows on every upper floor, with tall arched glazed openings at ground level. Ours: openings are solid stone with grey slit lines. Fix (exterior bot): put recessed glass panes in the hero glb with a dark reflective PBR material (roughness 0.05, metallic 0) and black mullion/transom frames at about 60 mm.
2. HIGH. Stone texture reads as small rubble brick. Real: smooth, pale cream Portland stone and faience in large ashlar blocks with fine joints. Ours: a tiled, high-contrast brick-like texture repeated at the wrong scale. Fix: use a smooth limestone or plaster PBR texture at real block scale (about 600×300 mm courses at ground level, near-plain faience above), with low normal strength.
3. HIGH. Ground-floor arches are barely legible. Real: a strong rusticated arcade of deep round-arched openings with voussoirs, dark glass, and the entrance in one bay. Ours: faint arch lines on a flat wall. Fix: model deep 300–400 mm reveals with the arched head and keystone, and set glazing back in each one.
4. HIGH. Entrance is a flat door-shaped panel with stone steps that look made-up. Real: the entrance sits within the arcade at pavement level. Fix: remove the steps unless they're sourced, and model a glazed door in an arched bay.
5. MED. Cornices and string courses are missing or very weak. Real: a prominent projecting top cornice, a first-floor string course, and pilaster or pier rhythm between window bays. Fix: extrude a cornice of about 400 mm projection with a profile, plus string courses at the floor lines.
6. MED. Proportions and bay rhythm. Real: 5 storeys with regular wide window bays separated by narrow piers, and the upper windows are much larger than the wall between them. Ours: mostly blank wall with thin vertical grooves. Fix: match window widths and heights to the H&S elevations (refs/critic/front.png and the D-series elevations).
7. MED. Lighting and colour. Real: warm, sunlit cream stone with a blue sky and soft shadows. Ours: flat grey-beige, a harsh single shadow and no sky in frame. Fix: HDRI sky background, a warmer sun, and AO in recesses.
8. LOW. The ground plane is a featureless grey slab. Real: cobbled granite setts and pavement. Fix: a setts texture on the street and a flag-paving pavement.

### Top 10 overall
1. A1 floor hole. 2. B1 no glass in facade. 3. B2 brick-like stone texture. 4. A2 kitchen spec missing. 5. A3 wrong furniture style. 6. A4 no windows/doors in flat. 7. B3 arches not legible. 8. A5 bedrooms bare. 9. A6 camera clipping. 10. A7/A8 no ceiling/downlights, flat lighting.

## Fix pass after Critic Round 1 (2026-11-03 ~04:25 Asia/Dubai) – build_twobed_v2.py, deploy dpl_7Xyu5ci1RbWKwUkS9ZU793JTvtRH
A1 fixed: one continuous floor slab under the whole outline (+ kitchen pale-grey and bathroom tile inlays).
A2: handleless white base + wall units at 600 mm modules, black integrated microwave, black washing machine, steel sink + gooseneck tap, black induction hob, emissive 3000K LED strip, dark peninsula with black built-in oven.
A3: navy velvet 3-seat sofa, oak/black-metal coffee table, cream boucle tub chairs (4), round oak/black pedestal table, cream rug, oak TV unit + TV, generic monochrome art, potted plant, white globe pendant. All simple modelled geometry (no CC0 model matched the style).
A4: 3 black arched multi-pane windows (named *_POSITION_UNSOURCED), door leaves with swings per plan, entrance door.
A5: navy channel-tufted bed, white bedding, navy throw/cushion, oak bedside tables with drawer + black legs, mushroom lamps, tall oak 2-door wardrobes, art.
A6: cameras at 1.5 m with 0.3 m ray-cast collision check (nudge if blocked); viewer presets at the same positions.
A7/A8: ceiling at 3.0 m (UNSOURCED), recessed emissive downlights + 3000K point lights on a 1.6 m grid, 100 mm skirting, warm white walls, AgX. Viewer hides the ceiling above 2.95 m camera height.
A9: oak desaturated/lightened (PIL-processed Poly Haven wood_floor), UV 1.2 m repeat.
A10: shower tray + glass wall, grey large-format tiles, back-to-wall WC, grey vanity + white basin, black-framed mirror, chrome towel rail.
A11: outline traced as the angled 8-point polygon from apt02_fp.png, scaled to 63 m².
Known remaining: WC/cistern orientation looks off; viewer interior lighting cooler/flatter than Cycles renders; plant is stylised; no AO in the web viewer.
Renders: interior/live/v2_{living,kitchen,bedroom1,bedroom2,bathroom}.png, latest.png (dollhouse). Live: web/shots/live_interior_living_v2.png, live_facade_closeup_r2.png.

## Critic Round 2 (independent critic, 2026-11-03 ~04:55 Asia/Dubai)
**Our images:**
- Blender renders: v2_living, v2_kitchen, v2_bedroom1, v2_bedroom2, v2_bathroom, latest.png.
- Live viewer: I loaded it myself in headless Chromium (software GL, 1024×640) and saved the shots to web/shots/critic2/: ext_street, ext_facade, int_interior (dollhouse), int_i_living, int_i_kitchen, int_i_bed1, int_i_bed2, int_i_bath, plus sheet.jpg.

**References:**
- refs/critic1/ (Rightmove CGI images and floor plans).
- **New real, non-CGI photos:**
  - refs/critic1/real_commons.jpg ([Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Legacy_House,_Manchester.jpg), 2015, CC BY-SA)
  - refs/critic1/real_geograph.jpg ([Geograph 8144686](https://www.geograph.org.uk/photo/8144686), Jul 2025, CC BY-SA)
- **legacy-house.com:** all pages (/, /gallery/, /two-bedroom-apartment/, /studios/) return a bot-challenge page ("One moment, please…") to curl, so no gallery images. Not retried in a browser.

**Scores:**
- Interior, Blender renders: **5/10** (up from 2)
- Interior, web viewer: **4/10**
- Exterior facade: **4/10** (up from 2)

### Interior-builder fixes
1. **HIGH. WC orientation is wrong.**
   - Real (Rightmove bathroom CGI): a back-to-wall pan with a concealed cistern behind a grey vanity/boxing, and the pan faces into the room.
   - Ours (v2_bathroom, int_i_bath): the pan sits at the front edge of a tall free-standing panel, which reads as a slab, and the pan is cut off at the frame edge. The panel is about 1 m high and as deep as a fridge.
   - Fix: put the back of the pan flush against a 1.0–1.1 m boxed half-wall that runs the width of the wall, with a flush plate on top. Face the pan into the room, with ≥ 600 mm clear in front.
2. **HIGH. Bathroom is missing most of its spec, and the shot is badly framed.**
   - Real: wall-hung white basin on a grey stone-look vanity, black-framed mirror, chrome ladder towel radiator (vertical rails plus horizontal bars), framed glass shower with a grey large-format tiled wall, small plant.
   - Ours: three floating chrome bars (no vertical rails), no basin, no mirror and no vanity in view, all-white walls, and the camera looks into a corner.
   - Fix:
     - add a ladder towel rail with 2 verticals
     - add a basin on a vanity, and a black-framed mirror above it
     - put a 600×1200 grey tile texture on the shower walls
     - re-frame the shot from the doorway so the basin, WC and shower are all in view
3. **HIGH. Web viewer lighting is flat, cool and overexposed, much worse than Blender.**
   - Real: warm ~3000 K, creamy walls, soft contact shadows.
   - Ours (int_i_living, int_i_bed1): walls blown out to white, a blue-grey cast, no shadows or AO, and the ceiling is near-black in bed2/living, so the ceiling is unlit.
   - Fix:
     - bake Blender lighting/AO into lightmaps (or vertex AO), exported in the glb
     - or, in three.js: ACESFilmic plus sRGB output, exposure about 0.8, a warm HemisphereLight, renderer.shadowMap with a shadow-casting window SpotLight, SSAO/N8AO, and RectAreaLights at the downlights
     - set the ceiling material to emissive 0 but lit, and check normals
4. **HIGH. Furniture is still primitive blocks.**
   - Real: a deep-cushioned navy velvet sofa with bolster arms, curved boucle tub chairs with texture, a slim oak-and-black-metal coffee table, a cream rug, a wood TV bench on legs.
   - Ours: box primitives with flat colours. The "TV unit" is a solid brown block, the TV stands in the middle of the room facing away from the sofa, and there is no coffee table.
   - Fix:
     - swap in CC0 models (Poly Haven sofa_03/modern sofa, ArmChair_01, coffee_table_round_01; or BlenderKit free ones) and add fabric normal maps
     - move the TV onto a slim oak unit on legs against a wall, facing the sofa
     - add a coffee table on the rug
5. **HIGH. Window glass reads as a white emissive card, with no outside view and no daylight.**
   - Real: the arched black steel windows show bright daylight with some depth, and the light falls into the room.
   - Ours: a flat white fill, and in bedroom 1 a dark picture frame overlaps the window glazing.
   - Fix:
     - use transmissive glass with a blurred exterior backplate or HDRI behind it
     - add a sun/area light coming through the window
     - move the bed1 artwork off the window (the art in the photos sits on a plain wall, beside the window, not over it)
6. **MED. Beds are too crude.**
   - Real: navy velvet bed with a channel-tufted headboard (rounded flutes, ~1.2 m high) and a deep upholstered base, white duvet, 4–6 pillows plus scatter cushions, a navy throw folded across the foot.
   - Ours: flat slatted planks with gaps, which reads as a fence. Two bolsters, a single cushion, and a throw that's a flat slab covering half the bed.
   - Fix: rounded, touching flutes on the headboard; add pillows; a draped throw about 50 cm wide; a soft-bevel duvet.
7. **MED. Kitchen still lacks the key spec items.**
   - Real: a full run of tall wall units, a black integrated microwave, a black washing machine with a door bezel, a gooseneck tap, an LED strip lit under the wall units, and handleless gaps.
   - Ours: the microwave is a brown/grey panel, there's no tap visible, the LED strip doesn't glow, and the washing machine is a flat grey square with a circle on it.
   - Fix: add the tap mesh, make the LED strip emissive (~3000 K), give the microwave a black glass face with a frame, and model the washing machine drum door with a chrome ring.
8. **MED. Peninsula colour and finish.**
   - Real: dark charcoal/graphite slab with a white or grey top.
   - Ours: Blender shows mid-grey; the web viewer shows near-black with blue specular.
   - Fix: one consistent graphite PBR (albedo about #3a3a3c, roughness 0.5), with a white quartz top.
9. **MED. Ceiling height and proportions look tall and narrow.**
   - Ours: bedrooms read narrow and tall, at a 3.0 m ceiling (unsourced).
   - Fix: keep the 3.0 m ceiling but widen the camera FOV to about 70–75°, and drop the camera to 1.4–1.5 m. Check bedroom widths against the plan scale.
10. **LOW. Floors.**
    - Real: light oak boards with a matte finish.
    - Ours: the web viewer shows a grey-washed floor with shiny spec. Blender is fine.
    - Fix: match the web material roughness (~0.6) and colour to Blender.
11. **LOW. Styling is sparse.**
    - Real: books, vases, cushions, a framed abstract art print, plants.
    - Ours: one low-poly plant made of discs, and blank art frames.
    - Fix: a CC0 potted plant (Poly Haven potted_plant_01/02) and an abstract texture in each frame.
12. **LOW. Dollhouse view.**
    - The outline is now angled and good.
    - The dark site tiles and grey wall caps still look like a site model.
    - Fix: a light neutral ground and white wall caps.

### Exterior-bot fixes (legacy_hero.glb)
13. **HIGH. Colour is wrong.**
    - Real (Commons and Geograph photos): warm buff/cream/greyish-honey faience with visible block coursing and weathering. Darker grey stone at the Portland ground floor.
    - Ours: cold, near-pure white and blue-grey, like plaster, with no block joints on the upper floors.
    - Fix: albedo about #CFC3A6 to #D8CCB0, a faience block grid of ~450×300 mm with fine darker joints, subtle variation and dirt maps. Make the ground floor slightly greyer.
14. **HIGH. Windows are wrong type and colour.**
    - Real: white-painted multi-pane timber/steel sashes (small panes, white glazing bars), with windows paired in bays between piers.
    - Ours: black frames and dark glass everywhere. That is the CGI marketing look, and it is not what the real building has today.
    - Fix: use white or off-white glazing bars at the real pane pattern, on mid-reflective glass. If the CGI's black frames are what the conversion is meant to have, label them as the proposed CGI spec.
15. **HIGH. Ground-floor arcade is too weak.**
    - Real: massive radiating voussoirs (rusticated stone blocks fanning around each arch), rusticated banded piers and a keystone on each arch. Arched windows have white fanlight glazing above a dark lower panel. A big cornice/entablature sits above the arcade.
    - Ours: small evenly spaced voussoirs, shallow reveals, and a thin band above.
    - Fix: deepen the voussoirs to ~0.6–0.8 m radial depth and add banded rustication grooves on the piers. Add a projecting entablature of about 0.5 m over the ground floor, then fanlight glazing.
16. **HIGH. Entrance is wrong.**
    - Real: a tall rectangular doorcase with a moulded architrave, flanking pilasters/brackets, a small window above and a dark double door, set between the arches.
    - Ours: a plain square window in a flat panel.
    - Fix: model the doorcase per the Geograph photo (centre-left bay), with steps only as shown, which is one low step.
17. **MED. Missing decoration.**
    - Real:
      - carved cartouches/heraldic roundels on the ground floor (both ends)
      - the "RB" monogram shields between the upper windows
      - a projecting oriel/canted bay at the left end of the main front, with pediments over its windows
      - a strong top cornice with a parapet
    - Ours: none of these.
    - Fix: add a cornice profile, the oriel bay, the pediments over the end-bay windows, and simple relief shields.
18. **MED. Piers and bay rhythm.**
    - Real: flat pilaster strips between paired windows, with spandrel panels between floors.
    - Ours: uniform white strips and equal windows that read like a curtain-wall grid.
    - Fix: set pier widths and spandrel panels from the photos and the H&S elevations.
19. **MED. Lighting.**
    - Real: strong warm sun and a blue sky.
    - Ours: overcast-flat, no sky in close views, and a cast shadow is the only depth cue.
    - Fix: a warmer sun, AO in recesses, and an HDRI sky background.
20. **LOW. Street.**
    - Real: a tarmac road and a flag pavement with a kerb.
    - Ours: a grey slab with setts.
    - Fix: use a flag-pavement texture, a kerb and a tarmac road.

### Verdict
**Not yet "at least as good as the online pictures."**
- **Interior:** the Blender renders are now a believable schematic. They have the right palette (navy, cream, oak, white kitchen) and the arched windows. But they read as a clay/blockout model, well short of the Rightmove CGI, mainly because of the furniture fidelity, glass and the bathroom.
- **Web viewer:** a further step down, because the lighting is flat and blown out.
- **Exterior:** now has glass and arches, but the colour and window style don't match the real building, and the entrance, oriel and decoration are missing.

## Progress (05:45 Asia/Dubai): v3 script written (WC boxing, bathroom fittings, sofa/TV/beds/kitchen detail, window openings + sky backdrop + daylight, lightmap bake). Blender renders v3_living/kitchen/bedroom1/bedroom2 done; bathroom shot + bake pending.
Progress (05:58): v3_bathroom rendered.
Progress (06:06): lightmap bake 3072px done, twobed_raw.glb exported.
Progress (06:10): baked twobed.glb (1.47 MB) verified locally in viewer (warm, shadows).
Progress (06:12): deployed dpl_7ZYQWaw21jxnjectk1TsZ5bCe34F.
Progress (06:16): live shots of the facade and all 6 interior presets saved to web/shots/r3/. Remaining: bake seam lines visible on walls (bathroom especially); the arched-window frame overlaps the ceiling line; graphite peninsula reads near-black.

## Critic Round 3 (independent critic, 2026-11-03 ~06:30 Asia/Dubai)
**Reviewed:** all 7 images in web/shots/r3/, each viewed individually: facade_midday, interior_midday_i (dollhouse), and i_living, i_kitchen, i_bed1, i_bed2, i_bath (all _midday_i).

**Compared against:**
- refs/critic1/: the Rightmove CGI images for 92163630, 92161311 and 92992530
- real_commons.jpg and real_geograph.jpg (real photos of the facade)

All r3 images are web-viewer captures, with lighting baked from Cycles. There were no separate Blender renders this round, so "interior" and "web viewer interior" now mostly converge.

**Scores:**
- Interior (design and furnishing): **6/10** (up from 5)
- Web viewer interior: **5.5/10** (up from 4)
- Exterior facade: **5/10** (up from 4)

**What improved:**
- The baked warm lighting fixed the cold, flat web look.
- The navy sofa, boucle tub chairs, the oak and black-metal coffee table, the gooseneck tap, the black microwave and the fluted navy headboards all now match the CGI palette and style.
- The WC is now back-to-wall with a flush plate.
- The ladder towel rail and grey shower walls are in.
- On the exterior, the windows are now white multi-pane and the colour is warmer cream, both closer to the real photos.
- The entrance is now a glazed double door with a transom.

### Interior-builder fixes
1. **HIGH: the Dollhouse preset is broken.** interior_midday_i shows a closed dark-grey roof or lid over the whole flat, with only stray white wall fragments sticking out, so nothing inside is visible. Fix: hide or exclude the ceiling mesh in the dollhouse view (put it on its own layer and toggle it per preset), or cut it away. Then re-check that the wall caps aren't floating.
2. **HIGH: the bathroom is still poor.**
   - What we have:
     - murky brown-grey baked lighting with light-leak streaks on the walls
     - still no basin, vanity or mirror in view
     - the WC pan reads as a white box
     - a black disc floating near the ceiling, which is presumably the shower head
     - the shower tray is lit but sits in an empty enclosure, with no visible glass edge
   - What the real CGI shows: a bright white space with grey large-format tile, a white wall-hung basin on a grey vanity, a black-framed mirror and a glass enclosure.
   - Fix:
     - re-bake at higher samples, or add a bright ceiling area light and a white ceiling
     - lighten the tile albedo
     - add the basin, vanity and mirror, and frame the shot so they're in it
     - model the pan with a rounded bowl and seat
     - fix the lightmap UV overlap that's causing the streaks
3. **MED: bake artefacts across the flat.**
   - Blotchy dark stains on the framed art (living and kitchen): the art texture reads like a cow-hide or ink smear, with black blobs.
   - Visible dark seams and shadow bleed at the wall and ceiling junctions.
   - Noisy, grainy wall shading.
   - Fix: more bake samples plus a denoise pass, padding/margin of 8 px or more on the bake, a lightmap UV unwrap with no overlaps, and an abstract art image like the CGI's monochrome brush print.
4. **MED: the windows show a flat blue backdrop.** The blue is uniform and the arch top is a white blown area with a seam. Fix: a soft-blurred exterior photo or HDRI crop, consistent exposure across the arch, and a thin sill and reveal depth of about 0.3 m.
5. **MED: bedrooms feel cramped and the camera is poorly framed.**
   - The camera is too close and high, so the foot of the bed fills the frame and the headboard sits right against the window.
   - The real CGI looks at the bed square-on from about 3 m away, with the oak wardrobe and the art in view. The art sits on the wall with no window behind it.
   - Fix: pull the camera back toward the door and set it to about 1.3 m high with a 65–70° FOV, add the tall oak wardrobe beside the bed per the photo, and add a framed print.
6. **MED: the TV is wrong.** In the living view the TV sits on its unit in the middle of the room, side-on to the sofa and facing the camera. Fix: move it against a wall, facing the sofa. The CGI shows the TV on an oak unit by the wall.
7. **LOW: the kitchen lacks the under-cabinet LED glow** and the warm cream fronts that the CGI wall shows. There's also no oven visible in the peninsula, and no backsplash shading. Fix: an emissive strip with a bake contribution, and a black oven face on the peninsula.
8. **LOW: scale and fabric cues.** The pillows and cushions are boxy and the duvet has no folds. The boucle chairs read smooth. Fix: bevel and subdivide them, and add a fabric normal map.

### Exterior-bot fixes (legacy_hero.glb)
9. **HIGH: the ground-floor stone is now blue-grey on the right half, versus pale cream on the left.**
   - Real: one continuous warm Portland stone colour along the arcade.
   - Ours: shows a strong colour discontinuity. Part of it is shadow, but the lit section is also bluish.
   - Fix: one material, a warmer albedo of roughly #C9BFA8, and check the vertex colours/material assignment on the right bays.
10. **HIGH: decoration is still missing.** None of these from the real photos are there yet:
    - the oriel/canted bay at the left end
    - the pediments over the end-bay windows
    - the RB monogram shields
    - the large ground-floor cartouches
    - a heavy top cornice

    These are the building's signature features. Fix: model them from the Commons and Geograph photos.
11. **MED: the arcade.**
    - The voussoirs are better but still small and uniform.
    - The real arched windows have a fan of white glazing bars in the arch, with a dark lower panel.
    - Ours has dark glass throughout with sparse bars.
    - Fix: bigger voussoirs with keystones, and fanlight glazing-bar geometry.
12. **MED: upper-floor bay rhythm.**
    - Real: windows grouped in pairs between broad pilaster piers, with spandrel panels.
    - Ours: still evenly spaced, so it reads like a grid.
    - Fix: piers and window grouping per the photos and the H&S elevations.
13. **MED: the entrance is still too plain.**
    - Real: a moulded architrave with columns and brackets, and a window above.
    - Ours: a flat rectangular reveal.
    - Fix: add an architrave and pilaster detail.
14. **LOW: weathering.** The real stone has dirt streaks under the sills and a darker plinth. Fix: a grime or AO texture.

### Verdict
**Not yet as good as the online pictures.**
- **Interior:** the CGI is photoreal, with styled props, clean lighting and precise framing. Ours reads as a good-quality schematic or game-level visualisation with bake artefacts.
- **Exterior:** it captures the overall massing and the window type, but not the ornament that makes the real building recognisable.

**Worth another round?**
- **Yes, one more targeted round**, because it's cheap and high-impact:
  - fix the dollhouse lid (#1)
  - fix the bathroom (#2) and the art and bake artefacts (#3)
  - reframe the bedroom cameras (#5)
  - fix the ground-floor stone colour (#9)
- **Beyond that, more rounds give diminishing returns.** Reaching CGI parity would need proper asset modelling and offline path-traced renders, which is days of work, not iterations.

**Recommendation:** after that one round, it's good enough to show Colin with the caveats:
- the layout is approximate (no dimensions published)
- the window positions are unsourced
- the finishes come from the marketing CGI
- the facade ornament is simplified
Progress R4 (06:23): started Critic Round 3 pass, build_twobed_v4.py copied from v3.
Progress R4 (06:27): v4 script: lighter tile + bath ceiling panel light, rounded WC bowl/seat, shower riser+arm, glass edge, re-framed bath camera (basin/vanity/mirror/WC in frame, test render OK); window reveals 0.30 m + softer generated sky backdrop; new generated monochrome art; bake margin 16, island margin 0.004, normalized gaussian denoise; ceiling split into Ceiling_BAKED for dollhouse hiding; viewer ceiling lookup updated. Starting full bake.
Progress R4 (06:32): viewer presets i_bed1/i_bed2 (~3 m back, 1.3 m, 68° FOV) and i_bath reframed; app.js rebuilt (v=6). Exterior re-copied+compressed: hero/context unchanged (same sha1 as r3).
Progress R4 (06:42): full bake done (bs=160, 3072 atlas, denoised), ceiling split OK (10 faces), twobed.glb compressed.
Progress R4 (06:42): deployed dpl_AbPGYbJD34Rm4jiUccw57jU2gBde; taking r4 live shots.
Progress R4 (06:48): r4 live check: dollhouse lid persisted because gltf-transform optimize joined Ceiling_BAKED into BAKED_interior; re-compressed with --join false --flatten false. Bedroom presets landed inside geometry; re-checking camera positions in Blender.
Progress R4 (07:10): re-bake 2 done; exterior re-copied (exterior bot updated at 06:37) and compressed (hero 1.93 MB, context 2.50 MB); deployed dpl_8s44MCT832Ws35ETKg21xeZ3fJ3Y; retaking r4 shots.
Progress R4 (07:12): MOBILE: side panel was a fixed 360px column (on a phone the 3D area collapses to ~0 width) -> responsive column layout (62dvh viewer + panel below) via media query; viewport-fit; device detection (UA/deviceMemory/coarse pointer, ?lq=1/0 override) -> hero_m.glb (exterior bot's mobile hero, 1K tex, 686 KB), context_m.glb (my 256px/20% simplify of surroundings, 1.46 MB; exterior bot's surroundings_mobile was still being written, 19.9 MB raw -> 5 MB), twobed_m.glb (2K atlas, 1.34 MB); DPR cap 1.5, no AA/log-depth/shadows on mobile; WebGL check + error text; webglcontextlost -> reload ?lq=1; progress bar; touch-action none.
Progress R4 (07:13): deployed dpl_EXvT4oHnzR3hsLujeXFhAWHSUzLr (mobile + r4 interior).
Progress R4 (07:22): switched mobile to exterior bot's final mobile GLBs (hero_m 1.74 MB, context_m 4.6 MB), env_m.hdr 512x256, DPR cap 2; deployed dpl_D6Uc3q7Nb1hctYWvwSydYNtKM32E; live mobile test.
Progress R4 (07:24): live mobile (Galaxy S9+ emulation, 4x CPU + ~1.6 Mbps throttle) verified: exterior loads in ~35 s, interior dollhouse/living render; shots in web/shots/r4/mobile/. Desktop r4 shots reviewed. Remaining: see report.
Progress R5 (07:37): room menu + fly-in + first-person look (drag/touch, wheel/pinch FOV), Back to exterior, room-to-room glide; hall/storage viewpoints added; deployed dpl_C7BdL19w1QFJmahntnyeFJqhkbzk.
Progress R5 (07:44): mobile menus made single-row scroll strips (bars covered ~60% of view); deployed dpl_59fz9bgfNGzw7kbNak7YQ2JAj3Ga; live mobile re-test in shots/r5/mobile_v2.
Progress R6 (08:42): tricks check. /workspace/legacy/tricks_for_bots.md does not exist; used tricks_register.md + x_tricks.md (all 11 status NEW, none certified). Viewer-relevant: USED #3 (clearcoat via glTF KHR_materials_clearcoat from exterior bot, kept 0.6/0.15 on desktop; disabled on mobile for perf; no transmission added: glass stays existing dark blend). Already in place: #2 meshopt (desktop) - KTX2 SKIPPED (mobile files must stay unchanged; WebP already). SKIPPED #7 instancing (would alter exterior bot's files/mobile), #5 clickable floors (not asked), #10 water (low priority, canal not in view), #1/#4/#6/#8/#9/#11 not viewer work.
Progress R6 (08:43): exterior R4 re-copied (hero 08:03 -> 1.93 MB; surroundings unchanged after compression, same sha), mobile 08:04 files used unchanged (hero_m 1740244 B, context_m 4728536 B); deployed dpl_G3FDbcj4AXv5PadFWRUfyUryvDE7.
Progress R6 (08:46): exterior info panel hidden in exterior mode (desktop+mobile; 3D fills screen), interior keeps its sourcing panel; deployed dpl_B9D1cBUM1fHhfQrUUdPtyL8mqzXZ.

## Critic Round 4 (exterior renders), independent critic, 2026-11-03 ~08:55 Asia/Dubai
**Reviewed:**
- out/render_{hero,street,aerial,viaduct}_4096x2304.png, viewed downscaled to 1280 px
- the 6 time-of-day hero frames in out/tod_*_hero_960x540.png

**Compared against:**
- refs/critic1/real_commons.jpg and real_geograph.jpg (real photos)
- the Rightmove CGI exterior

**Scores:**

| Image | Score |
|---|---|
| hero | 6/10 |
| street | 6.5/10 |
| aerial | 4/10 |
| viaduct | 5.5/10 |
| time-of-day set | 5.5/10 |
| **Exterior overall** | **6/10** (up from 5) |

**Better than Round 3:**
- The attic storey above the cornice is now there, with its small windows.
- The white multi-pane windows are right.
- The main and lower cornices read clearly.
- The ground-floor arches now have fanlight glazing bars.
- The colour is warm cream.

### hero
1. **HIGH. The ground-floor stone is wrong.**
   - Real: smooth, banded Portland ashlar. The rustication is horizontal channelled joints, and the voussoirs are large, clean and radiating.
   - Ours: a rough, random sandstone/rubble texture with brown staining. It reads as a rustic cottage wall.
   - Fix: smooth, pale grey-cream ashlar with 20 mm channelled horizontal joints about every 380 mm, and clean dressed voussoirs and keystones.
2. **HIGH. There are full-height glazed curtain-wall strips at both front ends and on the side.** Neither real photo shows them. The real front has punched paired windows, and the left end has a projecting canted oriel with pediments. Fix: remove the glazed strips and model the oriel bay plus the pedimented end-bay windows.
3. **MED. The dark, monolithic neighbour block behind the building is untextured.** It dominates the frame. Fix: give it a facade texture or make it lower contrast.
4. **MED. The voussoirs are irregular, jagged extrusions** that sit proud of a messy band. Fix: clean wedge blocks with a keystone, flush with a smooth arch ring.

### street
5. **HIGH. Same as items 1 and 2:** the rubble ground floor and the glazed end strips.
6. **MED. Two odd white discs on the left pier at 2nd/3rd-floor level.** They're probably meant as the RB shields, but read as satellite dishes. Fix: shield-shaped relief panels in the faience colour, placed as in the Commons photo, between the windows above the arcade.
7. **MED. The ground-floor cartouches are small discs.** The real ones are large carved oval wreathed roundels about 1.2 m tall, at the outer bays. Fix: model a larger relief roundel.
8. **MED. Bay rhythm and spacing.** Ours is a near-symmetric centre entrance with 3 arches either side. Real (Geograph): the entrance is off-centre, with 3 smaller arches on its left and 3 large arches on its right, plus a plain end bay with the roundel. Fix: re-space the arcade from the Geograph photo and the H&S elevations.
9. **LOW. The entrance is still a flat dark slab with a transom.** Real: a moulded doorcase with columns and brackets.

### aerial
10. **HIGH. The surroundings are flat grey untextured boxes,** and the ground is a muddy tan mesh with torn polygons at the top left. The hero is a small part of the frame. Fix: neutral asphalt and paving materials and basic facade textures on context blocks, then clean up the terrain tears.
11. **MED. The roof is a plain grey slab with a single cube.** Real roof detail and plant is NOT FOUND, so label it simplified.
12. **LOW. The viaduct tracks read as pink slabs.** Fix: brick texture plus ballast.

### viaduct
13. **MED. The parapet's salmon-pink plaster colour looks unreal.** Real: Manchester engineering brick, dark red-brown. Fix: a brick PBR texture.
14. **MED. Item 2 again,** made very obvious on the side elevation.
15. **LOW. The glass building at the left has an exaggerated red reflection.**

### time-of-day
16. **MED. The golden hour and dusk frames have a blown-out white sky,** with almost no warm cast on the stone. Fix: HDRIs that match each time of day, sun elevation and colour temperature (about 3000 K at golden hour), and an exposure check.
17. **LOW. The night glow is uniform:** almost every window is lit at the same brightness. Fix: randomise about 40–60 % lit, warm/cool variance.

### Biggest remaining gaps
The building's identity rests on three things:
- the smooth ashlar arcade
- the oriel and pediment end treatment
- the carved ornament (shields, roundels, doorcase)

Our ground floor texture and the glazed strips are actively wrong, not just simplified. Fixing items 1 and 2 would lift it to about 7.5/10. Everything else is polish.
Progress R6 (08:50): live verified desktop + Galaxy S9+ (facade/aerial/street + Living & Bedroom 2 first-person), live hero.glb/hero_m.glb sha match uploads; shots in web/shots/r6/.

## Dollhouse pass
Critic Round 3 item 1 (HIGH): Dollhouse preset was a closed lid, so the inside was not visible. The blue box is that lid: `Ceiling_BAKED` in web/twobed.glb and web/twobed_m.glb (node kept separate from `BAKED_interior`; not rebuilt). Drawn, its lightmap is a flat blue-grey slab (~#44526b) over the whole flat. Hidden, the oak floor and furniture show through.

Headless Chromium (software GL) on the local viewer, `?m=i&cam=interior`:
- Dollhouse preset, camera y=12: `Ceiling_BAKED.visible === false`. Blue-lid pixels ~0.8% of the frame (sky edge, not a slab).
- Same preset with the camera dropped to y=1.2 (the old height test would have put the lid back): mesh still `visible === false`. Inside is in frame (TV, kitchen, floor), not the blue box.
- Living preset `i_living`: same mesh `visible === true` (room views unchanged).

Change is viewer-only. `web/src/app.js` (rebuilt to `web/app.js`, `index.html` cache `v=16`): the interior/Dollhouse preset never draws `Ceiling_*`. Other presets still show it while the camera is under 2.95 m. No new GLB. Bathroom and furniture not rebuilt. Flat is not finished.

