"""Deterministic walkability check (no navmesh): can a person get from the front door to every room?

Run inside the editor (execute_python), then await the coroutine:
    ns = {}; exec(open(r"<repo>/unreal/pipeline/walk_check.py").read(), ns); await ns["run"]()

Method, on a 20 cm grid over the house (needs complex-as-simple collision on the villa meshes):
  1. Every column is scanned top-down with line traces; each upward-facing hit is a candidate floor.
  2. A floor cell is walkable when a person capsule (radius 25 cm, clear from 30 cm to 195 cm above the
     floor) overlaps nothing. Walls, glass, closed door leaves and furniture block; steps up to 30 cm don't.
  3. Neighbouring walkable cells connect when their floors differ by max_step (default 25 cm; risers are 19 cm).
  4. Flood fill from outside the front door. A room passes when a reached cell lies within 60 cm (plan)
     and 40 cm (height) of its probe point, taken from the room labels on the approved V4 sheets.
Writes <Saved>/Pipeline/walk_grid.json (cells and reach flags) for walk_map.py.
"""
import asyncio
import json
import os
from collections import deque

import unreal

STEP, R, HALF, LIFT = 20.0, 25.0, 82.5, 30.0  # BP_FirstPersonCharacter: radius 25, 1.92 m tall (top at floor + 30 + 2*82.5 = 1.95 m)
X0, X1, Y0, Y1, ZTOP = 250, 1650, 250, 2900, 1250
gf = lambda px, py: ((px - 148) / 0.435, (py - 165) / 0.435, 45)
ff = lambda px, py: ((px - 170) / 0.435, (py - 174) / 0.435, 445)
START = (985, 2840, 17)
ROOMS = {
    "GF Double-height entry": gf(548, 1100), "GF Living/dining": gf(560, 560), "GF Show kitchen": gf(447, 650),
    "GF Pantry": gf(340, 740), "GF Powder": gf(415, 735), "GF Kitchen": gf(372, 845), "GF Laundry": gf(425, 955),
    "GF K.store": gf(425, 1035), "GF Dress": gf(420, 1085), "GF Maid room": gf(330, 1130), "GF Maid bath": gf(425, 1165),
    "GF Office/gym": gf(670, 1000), "GF Bath": gf(750, 1100), "GF Multipurpose": gf(725, 1250), "GF Lift": gf(657, 650),
    "GF Pool terrace": gf(745, 345),
    "FF Corridor": ff(600, 890), "FF Master suite": ff(390, 500), "FF Family living": ff(580, 500),
    "FF Bedroom 1": ff(770, 500), "FF M.dressing": ff(400, 690), "FF M.bath": ff(400, 810), "FF Lift": ff(680, 650),
    "FF Bath 1": ff(775, 670), "FF Bath 2": ff(345, 960), "FF Dress": ff(440, 965), "FF Bedroom 2": ff(410, 1100),
    "FF J.dress": ff(690, 975), "FF J.bath": ff(805, 985), "FF Junior suite": ff(710, 1100),
    "FF Balcony N": ff(580, 355), "FF Balcony SW": ff(405, 1225), "FF Balcony SE": ff(735, 1290),
    "RF Stair arrival (core)": (825, 1350, 845), "RF Terrace": (900, 700, 845),
}


async def run(save=True, max_step=25.0):
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    SL = unreal.SystemLibrary
    chan = unreal.TraceTypeQuery.TRACE_TYPE_QUERY1
    otypes = [unreal.ObjectTypeQuery.OBJECT_TYPE_QUERY1, unreal.ObjectTypeQuery.OBJECT_TYPE_QUERY2]
    nx, ny = int((X1 - X0) / STEP) + 1, int((Y1 - Y0) / STEP) + 1
    cells = {}  # (i, j) -> list of (h, walkable)
    for i in range(nx):
        x = X0 + i * STEP
        for j in range(ny):
            y = Y0 + j * STEP
            z, found = ZTOP, []
            for _ in range(12):
                hit = SL.line_trace_single(world, unreal.Vector(x, y, z), unreal.Vector(x, y, -40), chan, True, [],
                                           unreal.DrawDebugTrace.NONE, True)
                if not hit:
                    break
                t = hit.to_tuple()
                loc, nrm = t[4], t[7]
                if nrm.z > 0.7:
                    h = loc.z
                    c = unreal.Vector(x, y, h + LIFT + HALF)
                    blocked = SL.capsule_overlap_actors(world, c, R, HALF, otypes, None, [])
                    found.append((round(h, 1), not blocked))
                z = loc.z - 2.0
                if z < -30:
                    break
            if found:
                cells[(i, j)] = found
        await asyncio.sleep(0)
    # flood fill
    def nodes_at(i, j):
        return [(i, j, k) for k, (h, ok) in enumerate(cells.get((i, j), [])) if ok]
    si, sj = round((START[0] - X0) / STEP), round((START[1] - Y0) / STEP)
    start = min(nodes_at(si, sj), key=lambda n: abs(cells[(n[0], n[1])][n[2]][0] - START[2]), default=None)
    seen = set()
    if start:
        dq = deque([start]); seen.add(start)
        while dq:
            i, j, k = dq.popleft(); h = cells[(i, j)][k][0]
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if di == dj == 0:
                        continue
                    for n in nodes_at(i + di, j + dj):
                        if n not in seen and abs(cells[(n[0], n[1])][n[2]][0] - h) <= max_step:
                            seen.add(n); dq.append(n)
    rows = []
    for name, (px, py, pz) in ROOMS.items():
        near = [n for n in seen if abs(X0 + n[0] * STEP - px) <= 60 and abs(Y0 + n[1] * STEP - py) <= 60
                and abs(cells[(n[0], n[1])][n[2]][0] - pz) <= 40]
        walk = [(i, j, k) for (i, j), lst in cells.items() for k, (h, ok) in enumerate(lst) if ok
                and abs(X0 + i * STEP - px) <= 60 and abs(Y0 + j * STEP - py) <= 60 and abs(h - pz) <= 40]
        rows.append((name, "REACHED" if near else ("BLOCKED (room floor walkable, not connected)" if walk
                                                    else "NO WALKABLE FLOOR at probe")))
    if save:
        d = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_saved_dir()) + "Pipeline/"
        os.makedirs(d, exist_ok=True)
        json.dump({"grid": [X0, Y0, STEP], "cells": [[i, j, k, h, ok, (i, j, k) in seen]
                                                    for (i, j), lst in cells.items() for k, (h, ok) in enumerate(lst)],
                   "rooms": {n: list(p) for n, p in ROOMS.items()}, "result": rows},
                  open(d + "walk_grid.json", "w"))
    return [("START", str(start))] + rows
