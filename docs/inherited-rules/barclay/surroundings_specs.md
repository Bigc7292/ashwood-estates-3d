# Barclay House surroundings: per-building spec sheet (120 m high-detail zone), R1 3 Nov 2026
Origin = hero centroid (BNG E383889.38 N397518.84). Heights: EA LIDAR 1 m nDSM median / p95 from `scene_data.json` (prep.py; EA National LIDAR Programme, OGL v3, https://environment.data.gov.uk/survey). Levels, names, use, addresses: OSM (ODbL) via Overpass https://overpass-api.de/api/interpreter, fetched 2026-11-03 (`data/overpass_250m.json`); each building is linked as https://www.openstreetmap.org/way/<id>.
Tags: **confirmed** = taken from the source given. **ref-observed** = visible in the CC photo named, but no dimension measured (material type only). **stand-in** = by-eye or generic; it needs a Street View check.
Refs are in `refs/surroundings/` (all CC BY-SA 2.0/3.0, Wikimedia Commons/Geograph; see `LICENCES.md` for author, URL and date).

| OSM way | Name / use | Dist m | Height (LIDAR median / p95) | Storeys | Facade material + colour | Windows | Ground floor / shopfront + signage | Roof | Refs |
|---|---|---|---|---|---|---|---|---|---|
| 204921679 | apartments (E of hero, N side WSW) | 32 | 30.92 / 35.23 confirmed | 10 (OSM confirmed) | grey cladding: **stand-in** | 3.0 m bay grid: **stand-in** | shop units. Names from OSM nodes (**confirmed**): Band Box, Close Male Grooming, iSmart Communications, Frurt, Olivitta, Vampire Vape, The Nail, Jamie's Salon. Fascia colours and lettering: **stand-in** | flat (OSM roof:levels 0) | Whitworth_Street_West_-_5809790 |
| 100646631 | apartments (W) | 58 | 15.72 / 17.49 | ~5 (h/3.2: stand-in) | red brick: stand-in | stand-in grid | none modelled | flat dark: stand-in | — |
| 737719731 | apartments (canal side) | 60 | 17.73 / 20.16 | 6 (OSM) | red brick: ref-observed (Rochdale_Canal_and_Barclay_House_-_8389611) | stand-in grid | residential | flat (OSM) | 8389611 |
| 737719730 | apartments | 65 | 12.21 / 13.48 | 3 (OSM) | brick: ref-observed | stand-in | residential | **gabled (OSM), modelled flat: defect** | 8389611 |
| 737719729 | apartments | 68 | 12.22 / 13.44 | ~4 (stand-in) | brick: stand-in | stand-in | residential | flat: stand-in | — |
| 737719728 | apartments | 79 | 20.34 / 22.5 | 6 (OSM) | brick: stand-in | stand-in | residential | OSM roof:levels 1 (setback storey not modelled: defect) | — |
| 647385657 | apartments (S, Cambridge St) | 83 | 48.8 / 66.96 | ~15 (stand-in) | cream/white cladding, irregular windows: ref-observed (Cambridge_Street_Block_A) | 2.6 m grid: stand-in (real pattern is irregular) | residential lobby | stepped: p95 shows a taller part (single prism = defect) | Cambridge_Street_Block_A |
| 705574571 | **O2 Ritz** music venue | 83 | 10.12 / 13.35 | 1 (OSM) + tall hall | white render: ref-observed (The_Ritz_-_4329097) | sparse: stand-in | black canopy over the entrance: ref-observed. Signage "RITZ" / "O2 RITZ": ref-observed text, size stand-in | flat (OSM) | 4329097, Manchester_UK_panoramio_10 |
| 136999879 | retail, 2 storeys | 84 | 7.59 / 12.16 | 2 (OSM) | brick: stand-in | stand-in | shopfront band: stand-in | flat (OSM) | — |
| 100646641 | **Rain Bar**, 80 Great Bridgewater St (pub) | 86 | 9.18 / 14.64 | ~3 (stand-in) | red brick former warehouse: stand-in | stand-in | pub frontage: stand-in. Name confirmed (OSM) | stand-in | — |
| 114615385 | **The Hotspur Press** (ruins, fire 23/06/2025 per OSM description + manchesterfire.gov.uk) | 88 | 4.57 / 16.69 (ruin, partial walls) | ruin | red brick shell, graffiti: ref-observed (Hotspur_Press_remains_-_8088127, Hotspur_House_-_8082744, Jul 2025) | blown-out openings | hoarding / Heras fencing: ref-observed | none (burnt) | 8088127, 8082744 |
| 1281855670 | substation | 90 | 2.59 / 5.87 | 1 | brick: stand-in | none | — | flat | — |
| 100646638 | **Peveril of the Peak**, 127 Great Bridgewater St (pub) | 92 | 5.87 / 7.02 | 2 (ref-observed) | green and yellow glazed tiles. Colour confirmed: OSM building:colour #eada0b, plus ref-observed (Peveril_of_the_Peak_-_3606000) | sash windows: stand-in | green doors, name sign boards: ref-observed | pitched slate + chimneys: ref-observed, modelled flat (defect) | 3606000 |
| 737719727 | apartments | 95 | 14.7 / 16.1 | 5 (OSM) | brick: stand-in | stand-in | residential | flat (OSM) | — |
| 647385655 | apartments tower (Cambridge St) | 101 | 51.21 / 85.38 | stand-in | cream/white: ref-observed (Cambridge_Street_Block_A) | stand-in | — | **stepped tower to ~85 m (p95); single prism at median = defect** | Cambridge_Street_Block_A |
| 167682674 | apartments | 109 | 11.56 / 38.55 (mixed) | stand-in | stand-in | stand-in | — | mixed heights (defect) | — |

## Viaduct (MSJ&AR, Oxford Road to Deansgate), S side of WSW
- Deck: 8.55 m above street (LIDAR DSM median, 116 samples along OSM `railway=rail bridge=viaduct`). **confirmed**
- Material: red brick, with some small sections of blue brick and sandstone dressings. **confirmed** (Heritage Statement list description, already in dossier)
- Arches with shop/club infills facing WSW (glazed fronts, dark doors, fascia signs): ref-observed (Whitworth_Street_West_-_4329092, 5809790, Entrance_to_Vision_Nightclub_-_7423592). Examples: "HALL CYCLES" fascia (5809790) and Gorilla (OSM node). Arch span 9 m and pier width 1.6 m: **stand-in** (NOT FOUND).
- Parapet with sandstone coping, plus a string course: copings ref-observed, sizes stand-in.
- Overhead line equipment portals and masts over the tracks: ref-observed (Railway_west_from_Oxford_Road_-_5779559, Oxford_Road_viaduct_to_Deansgate_-_5724012). Spacing 55 m: **stand-in**. The real portals span all tracks; the model uses single cantilever masts (defect).
- Sleepers 0.65 m spacing: stand-in. Ballast: Poly Haven CC0 texture.
- Steel bridge over Cambridge St (Cyclist_at_traffic_lights_-_1607775): **not modelled** (defect).

## Streets
- Whitworth St W: carriageway width is a 9 m stand-in (ROAD_W secondary). Double yellow lines on both kerbs: ref-observed (4329092, 5809790). Red-surfaced puffin crossing in front of the hero: **confirmed** (OSM node: crossing_ref=puffin, surface:colour=red, tactile_paving red). It is modelled as studs and lines; the red surfacing is not yet modelled (defect).
- Traffic signals (11), crossings (40), bus stops (12), benches (8), waste baskets (4), cycle stands (19), bollards (2), post box (1), telephones (2) and ATMs (2): positions **confirmed** from OSM nodes. Geometry: stand-in generic.
- Lamp columns: OSM has **0** `highway=street_lamp` nodes within 250 m, so positions (25 m spacing, 6 m columns) are **stand-in**. Refs show tall steel columns with side lanterns (4329092).
- Trees: 102 blobs from EA LIDAR DSM-DTM (height + canopy diameter **measured**). Vehicles on the carriageway and facade overhangs are filtered out. Species and leaf colour: stand-in.
- Canal (Rochdale): water from OSM. Black railings on the towpath side: ref-observed (Rochdale_Canal_-_5477629). Railing offset 3.4 m: stand-in.

## Needs Street View eyeballing (browser agent)
1. WSW north side, 204921679 ground-floor units: fascia colours/lettering per unit, bay widths, cladding colour.
2. Every viaduct arch facing WSW from Oxford Rd to Albion St: which arches are open, glazed, bricked up or roller-shuttered; tenant signage (Gorilla, Hall Cycles, Dog Bowl, Viva and others); arch count between the junctions (to replace the 9 m stand-in span).
3. Lamp column positions and type (WSW, Gloucester St, Cambridge St), plus any banners.
4. O2 Ritz: canopy extent, sign lettering and size, colour of the upper facade.
5. Peveril of the Peak: roof form, chimney positions, tile pattern bands.
6. 647385655/647385657: real window pattern and the stepped tower outline.
7. Rain Bar and 100646631 facades (brick colour, window rhythm, signage).
8. Street trees in front of / beside the hero: confirm the LIDAR blobs at (-21.7, 32.1) and (-35.0, 3.8) are trees.
9. Traffic sign posts (no OSM traffic_sign nodes), bins, planters and A-boards along WSW.
10. Puffin crossing red surface extent and the guard railings at the Gloucester St junction.
