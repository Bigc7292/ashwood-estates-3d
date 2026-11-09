# Ashwood 4B — source vs generated concept: discrepancies & gaps

Compared: generated renders (`../renders/`) vs brochure p25/p26 (same-villa marketing renders), p27/p28 untouched plan crops, approved V4 GF/FF/RF.
Style cross-check p29/30 (5B) and p33/34 (6B): same stone, vertical slat screen, flat carport canopy, frameless glass balustrade, raised stone pool deck, lawns + palms. Consistent with 4B; used only as a fallback style register.

## Render elements absent from the plan (not invented; placeholder or omitted)
1. **Carport canopy** (p25, also p29/p33): not drawn on GF/FF plan, which shows open parking with 2 car symbols. Modelled as a grey placeholder; extent and height assumed.
2. **Tall stone fin/pier at the street-right corner** rising above roof level (p25): not in any plan. **Not modelled.**
3. **Raised pool deck + steps down to lawn** (p26): the plan gives no levels; the pool and deck are modelled at ground level.
4. **Rear lawn beyond the pool** (p26 shows a deep lawn in front of the deck): the V4 site diagram ends ~1.2 m behind the pool water. Rear garden depth/boundary is UNKNOWN; nothing is modelled beyond the site diagram.
5. **RF floating canopy** (p26) is narrower and higher than the RF plan outline suggests. Grey placeholder; RF plan is NTS.
6. **Golf cart, street lamp, cars, furniture, loungers, hedges/shrubs, palms by species**: not modelled.

## Plan elements not visible in any render
7. **Courtyard water feature + planter island + tree** (GF/FF plan): no brochure render shows it. Plan geometry is used; finish assumed. There is no canonical room record for it.
8. **GF "TERRACE" and "OUTDOOR TERRACE"** are V4 labels with no delineated extent and no canonical record (also flagged by the floorplan3d spike). Shown as site paving only.
9. **Side boundary walls**: the site diagram is "NOT a verified plot survey". Side walls are grey placeholders (1.8 m assumed). The rear boundary is not modelled.

## Geometric / numeric gaps
10. Heights are not in any source: GF 3.6 m, slab 0.4 m, FF 3.4 m, roof slab 0.45 m, RF 3.0 m, balustrade 1.1 m, front wall 1.2 m and gates 1.8 m are display assumptions. In the renders, the storey proportions look broadly similar but are not measurable.
11. Site span: GF V4 gives ~18.7 m, FF V4 gives ~18.8 m (and FF envelope ~13.1 × ~23.9 m). The FF→GF alignment uses the two site-diagram boxes (scale x 0.953 / y 0.959). The pool-edge check shows a residual of ≤0.15 m. The FF courtyard void shows a visible offset of about 0.3–0.5 m against the GF water feature in `view_outdoor_terrace_courtyard.png`.
12. FF walls are a raster trace of the untouched FF crop (threshold), not an approved CAD contour. FF glazing is inferred from gaps in the envelope.
13. The RF is NTS (conflicting spans 3.8×15.7 vs 3.0×12.8). The RF core was positioned by the shared board (xref 439) offset and LIFT anchor alignment. It is a placeholder only.
14. Roof overhang depths: p25/p26 show deep cantilevered soffits beyond the envelope. They are not modelled because the extents are unknown.
15. Pool: 9.50 × 2.40 m (transcript), ~9.49 × ~2.38 m (calibrated). Depth, coping width (0.30 m assumed), tile finish and edge type are unknown. In p26 the pool edge reads as an infinity/overflow-like edge, which is not confirmable.
16. Tree symbols: 13 generic plan canopies. The renders show date palms and broadleaf trees, but the species cannot be matched to positions. Heights are assumed.
17. The FF front slat-screen location is inferred from p25 vs the FF "OPEN TO BELOW" zone. The FF front-right stone volume in p25 is only approximated by the balcony parapet.
18. Materials are visual readings of marketing renders only. No exterior finish schedule exists in the source. The p17 palette (travertine, etc.) is interior/project-level.
