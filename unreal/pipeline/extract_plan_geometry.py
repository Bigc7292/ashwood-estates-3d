"""Extract plan geometry (walls, floor plates, stair treads) from the Unreal interior meshes.

Read-only. Run inside the Unreal Editor:
    ns = {}; exec(open(r"<repo>/unreal/pipeline/extract_plan_geometry.py").read(), ns); ns["RESULT"]

Writes <Project>/Saved/Pipeline/plan_<floor>.json in world centimetres:
  walls:  [x0, y0, x1, y1, zmin, zmax]   vertical faces at least 120 cm tall, as plan segments
  floors: [[x, y], [x, y], [x, y], z]    horizontal triangles within 15 cm of the floor level
  steps:  [[x, y], [x, y], [x, y], z]    horizontal triangles between floor and ceiling (stairs, landings)
"""
import json
import os

import unreal

PML = unreal.ProceduralMeshLibrary
FLOORS = globals().get("FLOORS_OVERRIDE") or {
    # label: (mesh, actor location, floor z, ceiling z)
    "gf": ("/Game/Rooms/GF/gf_house/StaticMeshes/SM_GF_House", (878, 1547, 45), 45, 345),
    "ff": ("/Game/Rooms/FF/ff_house/StaticMeshes/SM_FF_House", (878, 1547, 445), 445, 745),
}


def extract(label):
    path, (ox, oy, oz), floor_z, ceil_z = FLOORS[label]
    sm = unreal.load_asset(path)
    walls, floors, steps = [], [], []
    for s in range(sm.get_num_sections(0)):
        v, t, n, *_ = PML.get_section_from_static_mesh(sm, 0, s)
        for i in range(0, len(t), 3):
            a, b, c = (v[t[i + k]] for k in range(3))
            nrm = (b - a).cross(c - a)
            area2 = nrm.length()
            if area2 < 1.0:
                continue
            nz = abs(nrm.z) / area2
            pts = [(p.x + ox, p.y + oy, p.z + oz) for p in (a, b, c)]
            zs = [p[2] for p in pts]
            if nz < 0.05 and max(zs) - min(zs) >= 120:
                xs = sorted(pts, key=lambda p: (p[0], p[1]))
                walls.append([round(xs[0][0], 1), round(xs[0][1], 1), round(xs[-1][0], 1),
                              round(xs[-1][1], 1), round(min(zs)), round(max(zs))])
            elif nz > 0.95 and area2 > 200:
                z = sum(zs) / 3
                tri = [[round(p[0], 1), round(p[1], 1)] for p in pts] + [round(z)]
                if abs(z - floor_z) <= 15:
                    floors.append(tri)
                elif floor_z + 15 < z < ceil_z - 20:
                    steps.append(tri)
    return {"walls": walls, "floors": floors, "steps": steps}


out_dir = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_saved_dir()) + "Pipeline/"
os.makedirs(out_dir, exist_ok=True)
summary = {}
for lbl in FLOORS:
    data = extract(lbl)
    with open(out_dir + f"plan_{lbl}.json", "w", encoding="utf-8") as f:
        json.dump(data, f)
    summary[lbl] = {k: len(v) for k, v in data.items()}
RESULT = summary
