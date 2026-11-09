# Barclay House exterior: 3D model (free/open-source only)
Barclay House, 35 Whitworth St W, Manchester M1 5NG. OSM way 100646649. Hero centroid BNG E383889 N397519 (53.47415, -2.24419).

## Hero numbers used in the model (every one sourced; no estimates)
| Value | Figure | Source |
|---|---|---|
| Storey heights GF→1st / 1st→2nd / 2nd→3rd / 3rd→4th / 4th→roof | 3.663 / 3.925 / 3.290 / 3.323 / 3.480 m | Howard & Seddon dwg E05 rev C, Existing Front Elevation https://docs.planning.org.uk/20210803/27/QKTOMYBCKT600/goza3b6sv2a2q83u.pdf |
| GF lobby above street | 2.10 m (street 100.10, lobby 102.20) | Design & Access Statement (DAS) https://docs.planning.org.uk/20210803/27/QKTOMYBCKT600/s4c5tvdfq0syslhg.pdf |
| Roof level above street | 19.78 m (from the two rows above) | E05 + DAS |
| LIDAR check: roof above ground | median 18.96 m, p95 20.01 m (1,004 px) | EA LIDAR Composite 1m FZ DSM minus DTM (OGL) https://environment.data.gov.uk/dataset/9ba4d5ac-d596-445a-9056-dae3ddec0178 |
| Front width | 37.54 m (OSM); 37.4 m measured from E05 at 1:250 | OSM / E05 |
| Footprint | 995 m², from the OSM polygon | https://www.openstreetmap.org/way/100646649 |
| Site area | 1,363.04 m² | Application form, 128804/FO/2020 https://docs.planning.org.uk/20210803/27/QKTOMYBCKT600/1be17fqhql5gyqlx.pdf |
| Facade | 6 round-headed GF arches, central entrance, end pavilions, 15 upper bays, cornices at 1st and 4th floor and roof, roof stair tower | E05 drawing; CGI refs/plans_p1_cgi.png (LoopNet plans PDF) |
| Materials | "Portland stone up to first floor with Burmantoft vitreous terra cotta above. The remainder of the building cased in concrete blocks." | https://www.manchestervictorianarchitects.org.uk/buildings/barclays-warehouse-barclay-house-whitworth-street-west |
| Viaduct deck above street | 8.55 m (median of 120 DSM samples) | EA LIDAR |
| Neighbour heights | LIDAR nDSM median per OSM footprint (299 of 306 buildings) | EA LIDAR + OSM |
NOT FOUND (only set dressing uses these, never the hero): viaduct arch span and pier width, lamp positions, exact window sizes (taken from the drawing proportions, accurate to about ±0.3 m), and whether the 2-storey mansard (app 128804/FO/2020) was built. The 2026 LoopNet CGI shows no mansard, so the model leaves it off (ROOF_EXTENSION=False).

## Conflicts
- Storeys: WSP Planning Statement says "5-storey" (para 2.1.1) and also "six storeys" (para 3.1.15). LoopNet says "Number of Floors 6", and E05 shows basement + GF + 4 floors. Basement + 5 above-ground storeys reconciles all three. The model uses E05.
- Date: LoopNet says "Year Built 1952". Manchester Victorian Architects gives "1905-1921", Pevsner (quoted in the Heritage Statement) calls it "a warehouse of 1914, by Harry S. Fairhurst", and the WSP statement says "early 20th century". The model uses the primary and architectural sources. 1952 is probably a CoStar/LoopNet database value, perhaps a refurbishment date.
- Units: 90 (2018 prior approval, WSP) + 13 (2020 application) vs 94 (BE News / Precede, 2025) vs 93 (OSB refinance, Property Reporter, 2026). The model is exterior only, so these do not affect it.

## Pipeline (all done, all free)
1. `prep.py`: OSM (area.osm, api.openstreetmap.org) + EA LIDAR WCS (lidar/dsm.tif, dtm.tif) → scene_data.json (local BNG metres).
2. `build_scene.py` (Blender 4.2.3, free): terrain from DTM, LIDAR-height neighbours, detailed hero, arched viaduct, canal, OSM trees (heights from LIDAR), roads, lamp posts, Poly Haven CC0 textures (textures/), HDRI (hdri.exr), 3 cameras, Cycles + OIDN. Exports out/barclay_scene.blend/.glb/.fbx.
3. `tod_panel.py`: time-of-day rig, embedded in the .blend.
Commands:
```
blender -b -P build_scene.py -- --time golden_hour --render          # presets or HH:MM, optional --date 06-21
BCAMS=street,aerial,viaduct blender -b -P build_scene.py -- --all-presets --noexport   # every preset x camera
BRES=1920x1080 BSAMPLES=64 ...                                        # quick drafts
```

## How to open and use (no coding)
1. Install Blender (free) from https://www.blender.org/download/ (4.2 LTS or newer).
2. Open `out/barclay_scene.blend`. If Blender warns about auto-run scripts, click "Allow Execution" (or tick Preferences → Save & Load → Auto Run Python Scripts). Otherwise go to the Scripting tab, pick `barclay_tod.py` and press ▶ Run Script once.
3. In the 3D viewport press N. Open the "Barclay" tab in the sidebar.
4. Things you can drag or change there:
   - Time of day (0–24 h), Month/Day: sets sun angle (real solar position for Manchester, UK summer time handled), sky colour, sun colour temperature and auto exposure.
   - Preset buttons: sunrise, morning, midday, golden hour, dusk, night (each also sets 4096×2304 and its sample count).
   - Camera: Cam_Street / Cam_Aerial / Cam_Viaduct.
   - Clouds (overcast HDRI mix) and Haze.
   - Manual window glow: override the automatic night lighting (windows, neighbour windows, street lights).
   - Manual exposure.
   - "Render all presets": saves stills to `renders/` next to the .blend.
5. Press Z → Rendered (or F12) to preview. Materials are in the Shading tab, and hero parameters are at the top of build_scene.py.

## Risks
CPU-only rendering: one 4K still at 128 samples takes several minutes (see dossier). Window and arch sizes come from scaled drawings. Facade ornament (pilaster capitals, roundels, carved panels) is simplified.

## Published areas and units (see dossier for exact quotes)
- LoopNet https://www.loopnet.co.uk/listing/35-whitworth-st-w-manchester/40185932/: Property Size 44,413 sq ft; Typical Floor 6,839 sq ft; 6 floors; "Year Built 1952" (conflict); basement Unit 1 1,800 + Unit 2 7,050 = 8,850 sq ft.
- LoopNet plans PDF (Howard & Seddon 3001 rev G / SK06): basement zones 437/325/422 m²; gym 655 m², coffee/co-working 168 m², private dining 27.8 m².
- Units: 90 (WSP, 2018 approval) + 13 (2020 application form: 5×2-bed, 8×3-bed); 94 (BE News https://benews.co.uk/broad-street-real-estate-secures-funding-for-manchester-office-to-resi-conversion/ , "£30m", developer Broad Street Real Estate, funders Firma Partners & Precede Capital); 93 (Property Reporter 2026).
- Unit sizes: barclay-house.com averages (studios 23–52 m², 1-bed 38, 2-bed 63); Rightmove 314/453/679 sq ft; DAS duplex GIAs 69.0–116.8 m².
- Site area 1,363.04 m² (application form). NOT FOUND: residential GIA/NIA total and per-floor areas above the basement.

## Final materials (sourced)
- Front to 1st floor: Portland stone ("Portland stone up to first floor", MVA).
- Front above: Burmantofts vitreous terracotta / faience, smooth white ("Burmantoft vitreous terra cotta above", MVA; "smooth white faiance finish", "light coloured faience, imitating light stone", Heritage Statement https://docs.planning.org.uk/20210803/27/QKTOMYBCKT600/kr3moadl8zok1e27.pdf). Exact shade: NOT FOUND.
- Sides and rear: concrete blocks ("The remainder of the building cased in concrete blocks.", MVA). Brick removed because no source was found for it.
- Viaduct: red brick ("Red brick with some small sections of blue brick, sandstone dressings", Heritage Statement list description).
- Windows: aluminium frames (WSP 121381/FO/2018); colour NOT FOUND, so dark grey is a placeholder.

## Camera match to a reference photo (camera_match.py)
1. Copy the scene: `cp out/barclay_scene.blend tests/scene_copy.blend` (never match on the master).
2. Read ≥5 pixel positions of known corners in the photo (parapet corners 20.13 m, street corners 0 m; hero-local metres: x along the
   Whitworth St W facade from its west corner, y into the building). Put them in a JSON like `tests/cgi_points.json`.
3. `blender -b -y tests/scene_copy.blend -P camera_match.py -- --ref refs/<photo>.png --points <pts>.json --render tests/match.png --scale 0.5 --save tests/matched.blend`
   (add `--hide-near 8` if it reports blockers; `--fov-h/--loc/--look` for a manual match). It prints lens, position, RMS px per point
   and writes `*_overlay.png`; then `python3 ref_check.py tests/match.png refs/<photo>.png`.
4. In the GUI the camera `Cam_Match` carries the photo as a background image; pick it in the Barclay panel camera list.
Full tool list and caveats: `TOOLS.md`.
