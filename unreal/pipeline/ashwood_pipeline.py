"""Ashwood 3D production-line audit (Stage 1 geometry prep, Stage 2 material standardisation).

Read-only. Run inside the Unreal Editor (execute_python):
    exec(open(r"<repo>/unreal/pipeline/ashwood_pipeline.py").read()); RESULT

Writes a Markdown verification report to <Project>/Saved/Pipeline/audit.md and leaves the
same text in RESULT.

Project rules enforced here (from unreal/HANDOVER_UNREAL.md):
- Nanite must be OFF on imported villa / interior / planting meshes.
- Material slots are resolved through get_lod_material_slot: section index != slot index
  on SM_GF_House / SM_FF_House.
- Only assets whose names use the standard prefixes (SM_, M_, MI_, T_) are trusted.
"""
import os
import statistics

import unreal

PREFIXES = ("SM_", "M_", "MI_", "T_")
PLASTER = "MI_Soffit"
SME = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
PML = unreal.ProceduralMeshLibrary


def _section_stats(sm, s, offset):
    v, t, *_ = PML.get_section_from_static_mesh(sm, 0, s)
    if not v:
        return None
    areas = []
    for i in range(0, len(t), 3):
        a, b, c = v[t[i]], v[t[i + 1]], v[t[i + 2]]
        areas.append(0.5 * (b - a).cross(c - a).length())
    zs = [p.z + offset.z for p in v]
    return {
        "tris": len(areas),
        "median_area": statistics.median(areas) if areas else 0.0,
        "z": (min(zs), max(zs)),
        "x": (min(p.x for p in v) + offset.x, max(p.x for p in v) + offset.x),
        "y": (min(p.y for p in v) + offset.y, max(p.y for p in v) + offset.y),
    }


def stage1_geometry():
    """Every StaticMeshActor: mesh, triangle count, Nanite state, transform."""
    rows = []
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()
    for a in actors:
        if not isinstance(a, unreal.StaticMeshActor):
            continue
        sm = a.static_mesh_component.static_mesh
        if not sm:
            continue
        tris = sum(
            len(PML.get_section_from_static_mesh(sm, 0, s)[1]) // 3
            for s in range(sm.get_num_sections(0))
        )
        nanite = sm.get_editor_property("nanite_settings").enabled
        loc = a.get_actor_location()
        issues = []
        if nanite:
            issues.append("NANITE ON (rule: off)")
        if not sm.get_name().startswith(PREFIXES):
            issues.append("bad prefix")
        rows.append((a.get_actor_label(), sm.get_name(), tris, nanite,
                     f"({loc.x:.0f}, {loc.y:.0f}, {loc.z:.0f})", ", ".join(issues) or "ok"))
    return rows


def stage2_plaster_audit(mesh_path, actor_offset):
    """Slots bulk-mapped to plaster whose geometry does not look like a wall or ceiling."""
    sm = unreal.load_asset(mesh_path)
    off = unreal.Vector(*actor_offset)
    rows = []
    for s in range(sm.get_num_sections(0)):
        slot = SME.get_lod_material_slot(sm, 0, s)
        mat = sm.get_material(slot)
        if not mat or mat.get_name() != PLASTER:
            continue
        st = _section_stats(sm, s, off)
        if not st:
            continue
        # Walls/ceilings: few, large triangles. Furniture, fabric, foliage: many tiny ones.
        if st["median_area"] > 200 or (st["tris"] < 300 and st["median_area"] > 50):
            verdict = "wall/ceiling"
        elif st["median_area"] < 20:
            verdict = "SUSPECT detail (tiny tris)"
        else:
            verdict = "check"
        rows.append((s, slot, str(sm.static_materials[slot].material_slot_name), st["tris"],
                     round(st["median_area"], 1),
                     f"x{st['x'][0]:.0f}..{st['x'][1]:.0f} y{st['y'][0]:.0f}..{st['y'][1]:.0f} "
                     f"z{st['z'][0]:.0f}..{st['z'][1]:.0f}", verdict))
    return rows


def _table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def run():
    parts = ["# Ashwood 3D pipeline audit", "", "## Stage 1: geometry and Nanite", ""]
    parts.append(_table(["Actor", "Mesh", "Tris", "Nanite", "Location", "Status"], stage1_geometry()))
    for label, path, off in [
        ("GF", "/Game/Rooms/GF/gf_house/StaticMeshes/SM_GF_House", (878, 1547, 45)),
        ("FF", "/Game/Rooms/FF/ff_house/StaticMeshes/SM_FF_House", (878, 1547, 445)),
    ]:
        parts += ["", f"## Stage 2: {label} slots mapped to {PLASTER}", ""]
        parts.append(_table(["Section", "Slot", "Slot name", "Tris", "Median tri cm2",
                             "World bounds", "Verdict"], stage2_plaster_audit(path, off)))
    text = "\n".join(parts)
    d = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_saved_dir()) + "Pipeline/"
    os.makedirs(d, exist_ok=True)
    with open(d + "audit.md", "w", encoding="utf-8") as f:
        f.write(text)
    return text


RESULT = run()
