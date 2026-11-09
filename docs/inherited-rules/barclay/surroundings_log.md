# Surroundings log

## Round S1, 3 Nov 2026 08:35–08:58 (UTC+4), Surroundings Bot
**Built** (on the copy tests/surr/scene_copy.blend, saved as tests/surr/scene_surr.blend; the master barclay_scene.blend was not touched):
- surroundings_data.py → surroundings_data.json. It holds 234 OSM furniture nodes and 74 POIs (Overpass, 250 m), 98 OSM buildings with tags, 239 raw LIDAR blobs (61 used after filtering), rails, and the viaduct deck at 8.55 m (LIDAR).
- surroundings_specs.md: 16 buildings in the 120 m zone, tagged confirmed / ref-observed / stand-in, plus a 10-item Street View list. refs/surroundings/: 17 CC BY-SA images, with LICENCES.md.
- build_surroundings.py, in layers (bldg, via, street, trees, canal). It contains:
  - 16 detailed neighbours: windows with frames and sills, a cornice/coping, shopfronts with fascias, and the Peveril tile band.
  - On the viaduct: PBR brick, 56 arch shopfront infills on the outer faces, sandstone coping and string course, sleepers, and stand-in OLE masts.
  - On the street: 53 upgraded lamp columns, double yellows on WSW, and furniture at OSM positions (11 signals, 11 signal crossings, 3 zebras, 12 bus stops, 8 benches, 4 bins, 18 cycle stands, 2 bollards, post box, telephones, ATMs).
  - 61 LIDAR trees, rippled canal water, and towpath railings.
- export_surroundings_detail.py → out/barclay_surroundings_detail.glb (45.3 MB, written as temp then mv). make_mobile_surr_detail.sh with surr_mobile_pre.mjs → out/mobile/barclay_surroundings_detail_mobile.glb (4.94 MB: 300 m cull, merged by material, JPEG 512, quantized).
- Validation: Khronos validator gives 0 errors on both new files. ./validate.sh PASS (the existing files are unchanged).
- Previews: out/surroundings_preview/surr_{wsw_east,wsw_west,street,viaduct,aerial}_960x540.png (Cycles CPU, 32 samples). ref_check: wsw_east vs Geograph 5809790 F1 0.329 / precision 0.320; wsw_west vs 4329092 F1 0.226 / precision 0.296. These cameras are **not matched**, so the scores are only a baseline.

**Rules followed:** free only (Poly Haven CC0, OSM, EA LIDAR, Commons CC BY-SA); no estimated facts (everything else is tagged stand-in); writes go to temp files, then mv; the master .blend was never saved; no messages sent.
**MCPs:** none used. The Blender MCP was skipped so that the open session isn't disturbed; all work was headless on copies. **Skills:** none loaded (no applicable skill; teardown is not needed without a flythrough).
**x_tricks:**
- #1 locked camera: partly. Cameras Cam_Surr_WSW_east/west are fixed, but camera_match point picks were not done yet.
- #10 canal ripples (Blender noise bump): applied.
- #2 meshopt/KTX2: skipped (the viewer decoder belongs to the Interior bot). KHR_mesh_quantization was used on the mobile file instead.
- #7 instancing: skipped (the merged-by-material output is already 40 draw calls).
- #8 displacement: skipped (CPU budget).
- #3, #4, #5, #6, #9, #11: not relevant to surroundings this round.

**Open defects (next round):**
1. Match the Cam_Surr cameras to refs 5809790 and 4329092 with camera_match.py.
2. 647385655/657 and 167682674 are a single prism at the median height. The p95 of 67–85 m shows stepped towers, so they need splitting by LIDAR height bands.
3. Gabled and pitched roofs (737719730, Peveril) are modelled flat.
4. Hotspur Press ruin uses the median 4.6 m; the walls reach the 16.7 m p95.
5. OLE should use full-span portals.
6. The steel bridge over Cambridge St is missing.
7. Puffin crossing red surfacing is missing.
8. Lamp positions are stand-in (no OSM nodes).
9. The arch span of 9 m is stand-in.
10. Window grids are generic, and party-wall detection is approximate.
11. The mid zone (120–250 m) is unchanged from build_scene.py massing: colours are generic, and roof colours have not been taken from imagery.
12. Shop blade signs are generic boxes with no lettering.
13. Facade textures repeat visibly on large walls.
