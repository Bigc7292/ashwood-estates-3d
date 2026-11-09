# 4B mismatch log (images vs CAD V4)

Default rule: **image for appearance, CAD for footprint dimensions.**

| ID | Item | Status | Rule | Resolution / reason open |
|---|---|---|---|---|
| M1 | Carport canopy + stone pier | RESOLVED | image for appearance, CAD for footprint dimensions | Modelled as CARPORT_canopy / CARPORT_pier, labelled RENDER-SOURCED, not on plan; footprint = CAD vehicle-entry zone x 0-7.6, z 23.6-29.3; top 3.45 m image-read |
| M2 | Tall stone fin, front-right | RESOLVED | image for appearance, CAD for footprint dimensions | STONE_FIN 0.5 m blade on the CAD GF right edge, top 11.6 m image-read, labelled render-sourced |
| M3 | Raised pool deck with steps | RESOLVED | image for appearance, CAD for footprint dimensions | Deck +0.45 m (3 risers) in the CAD terrace/pool zone; steps at the plan-right end as in the images; pool coping 0.30 |
| M4 | Rear lawn depth | RESOLVED (rear boundary type still OPEN) | CAD wins for plot depth; image lawn kept only as off-plot context | CONTEXT_lawn_beyond_plot labelled NOT PLOT (Y 0..+14). Rear boundary wall/fence type has no source and is not modelled **Open:** No source shows the rear boundary treatment |
| M5 | Pool proportion | RESOLVED | CAD footprint dimensions win | Pool kept at CAD 9.49 x 2.38 m; POOL image proportion logged as an image error |
| M6 | Courtyard open side | RESOLVED | image for appearance, CAD for footprint dimensions | Open side kept per CAD with side steps (ELEV-RIGHT); wall closed z 11.5-14.05; glazing west + south per image |
| M7 | Roof stair (open vs enclosed) | RESOLVED | CAD wins for plan arrangement | Stair enclosed in RF_core with a door to the terrace; image open stair logged as a deviation |
| M8 | Side walls + planted strip | RESOLVED | image for appearance, CAD for footprint dimensions | 2.2 m stone walls on the CAD site line; hedges/trees only inside CAD planted strips; side path = CAD hardscape. Lawn in front of side elevations (images) not modelled because it is not on the plan |
| M9 | Courtyard ~0.3-0.5 m offset between floors | RESOLVED | Calibrated GF CAD is authoritative; FF void snapped to it | FF void = GF water-feature rect 11.48-15.78 x 12.65-16.34; covered terrace strip z 11.5-12.65 |
| M10 | FF front slat screen extent | RESOLVED | image for appearance, CAD for footprint dimensions | Slats across x 3.45-11.0 in front of glazing; CAD envelope unchanged |
| M11 | Roof fascia / slab depth | RESOLVED (approx.) | Heights are image-read (no CAD heights) | Roof fascia 0.70 m, FF slab 0.50 m; model ratio 1.62 vs image ~1.51 (perspective); within reading tolerance |
| M12 | RF core visible from street | OPEN | CAD position kept | RF_core kept at the RF-plan position (front end z 22.5, height to 11.45 m unchanged). 2026-11-09 revision: core narrowed to the enclosed stair/corridor (~3.5 m, x 7.44-10.94) because the RF plan labels the 3.80 x 15.70 MEP zone beside it as a separate open roof area (1.5 m screen walls, height assumed); this is a plan reading, not an image override. Visible bulk from the street is reduced but the core still shows. **Open:** RF plan is NTS; set-back/height not confirmable. Still needs Colin's call: keep CAD position or pull back/lower per images. |
| M13 | Side elevations content (windows, lawn) | OPEN | image for appearance, CAD for footprint dimensions | Narrow FF side windows placed image-read; GF side windows from CAD WINS **Open:** Generated side elevations are pure inference; no brochure side view exists |
| M14 | Exterior finish schedule | OPEN | image appearance | Materials are procedural look-alikes **Open:** No finish schedule in source; materials are appearance-only |
| M15 | Courtyard tree species / trees generally | RESOLVED | image for appearance, CAD for footprint dimensions | Species/form from images at CAD positions |
| M16 | Rear facade bays (GF stone pier; FF stone panel + slat screen) | RESOLVED | image for appearance, CAD for footprint dimensions | GF_rear_stone_pier x 6.6-8.4 and FF_rear_stone_panel x 6.7-8.6, FF slat screen x 8.6-12.1, positions image-read from ELEV-REAR proportions; glazed extents stay CAD |
| M17 | Balcony balustrade glass + planting | RESOLVED | image for appearance, CAD for footprint dimensions | All balustrades now use clear transmissive glass (MAT balglass; previously the opaque window-glass material by mistake); 2 illustrative planters on the FF rear balcony |
| M18 | Carport canopy fascia | RESOLVED | image for appearance, CAD for footprint dimensions | CARPORT_fascia_front/side bronze band added on the existing render-sourced canopy; footprint unchanged |
| M19 | Front roof overhang depth | RESOLVED (approx.) | Heights/overhangs are image-read (no CAD) | Front overhang beyond the FF envelope 1.2 -> 2.0 m (x up to 11.0); envelope unchanged |
