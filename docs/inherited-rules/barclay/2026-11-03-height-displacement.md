# Barclay House: height-displacement
Date: 2026-11-03 · Source note: notes/2117128574964560278.md
Status: proposed · Owner: Barclay House 3D · Briefed: not yet

WHAT: full aligned PBR sets (16-bit height + AO, ORM) and true Cycles displacement for hero Portland stone/terracotta/brick, plus mask-driven moss/weeds — technique from https://x.com/mukadeshinigami/status/2117128574964560278 (and its quoted "one reference photo → PBR" article).
WHY: textures/{stone,terracotta,brick} contain only diff/nor/rough; hero relief = bump node (build_scene.py l.126, Strength 0.25). Street camera (render_street_*) close-ups of rusticated stone/terracotta read flat at grazing sun (tod golden_hour). Lenses: quality gain, visualization gain.
HOW:
1) For each set derive height from diff: Material Maker (MIT) or Blender bake (normal→height via a small numpy Poisson integrate of nor.jpg) → height.png (16-bit) + ao.png; verify alignment by overlay.
2) build_scene.py pbr(): if height.png exists, add Displacement node (Midlevel 0.5, scale 0.004–0.01 m) and set material displacement_method='BOTH'.
3) Enable Adaptive Subdivision (Cycles experimental) only on HERO facade objects and only for the street camera (env flag BDISP=1), dicing rate 2 px — keeps aerial renders cheap (no GPU, 15 GB RAM).
4) Moss/weeds: Geometry Nodes scatter on Rail_Viaduct ballast/brick using a mask (dark/low-height areas of diff), two lengths (short dense + sparse long), separate material.
5) Compare: tests/ render street cam before/after + ref_check.py vs refs geograph/commons photo.
CHANGES: textures/*/height.png, ao.png; build_scene.py pbr() + BDISP flag; tests/disp/. Owner: Barclay House 3D.
EFFORT S-M · RISK med (render time/RAM; try 960x540 first) · ROLLBACK BDISP=0 (bump only, as today).
LICENSE: own maps from existing textures (check their source licence stays CC0/own).
COST: £0 (Blender GPL, Material Maker MIT). Avoided: Opus credits, paid scan libraries.
SUCCESS: street-cam stone/terracotta shows shadowed relief at golden hour; render time ≤2× baseline at 960x540; no OOM.
