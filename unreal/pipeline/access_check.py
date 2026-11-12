"""Room access check: can a person walk from outside the front door to every room in the V4 plans?

Needs a NavMeshBoundsVolume round the house and complex-as-simple collision on the villa meshes.
Run inside the editor (execute_python), then await the coroutine:
    ns = {}; exec(open(r"<repo>/unreal/pipeline/access_check.py").read(), ns); await ns["run"](call_tool)

Room probe points are the room-label positions on the approved V4 preview sheets, converted to world
cm with the sheet registrations measured by overlay_cad.py (GF: px = 148 + 0.435 x; FF: px = 170 + 0.435 x).
A room passes when the navmesh path from the front door ends at the room point (not a partial path).
"""
W = {"refPath": "/Game/Main.Main"}
gf = lambda px, py: ((px - 148) / 0.435, (py - 165) / 0.435, 135)
ff = lambda px, py: ((px - 170) / 0.435, (py - 174) / 0.435, 535)
START = gf(545, 1400)  # outside the pedestrian entry
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
    "RF Stair arrival (core)": (825, 1350, 935), "RF Terrace": (900, 700, 935),
}
V = lambda p: {"x": p[0], "y": p[1], "z": p[2]}


async def run(call_tool, start=START, rooms=ROOMS):
    async def proj(p, h=150):
        r = (await call_tool("NavMeshToolset.NavMeshToolset.ProjectPointToNavMesh", point=V(p), horizontalExtent=h,
                             verticalExtent=120, bAllAgents=False, navData=None, agentName="", world=W))[0]
        return (r["projectedPoint"]["x"], r["projectedPoint"]["y"], r["projectedPoint"]["z"]) if r["bProjected"] else None

    s = await proj(start, 250)
    rows = [("START", f"{tuple(round(c) for c in s)}" if s else "not on navmesh")]
    if not s:
        return rows
    for name, p in rooms.items():
        q = await proj(p)
        if not q:
            rows.append((name, "NO NAVMESH near room point"))
            continue
        r = await call_tool("NavMeshToolset.NavMeshToolset.FindPath", start=V(s), end=V(q), areaCostOverrides=[],
                            excludedAreaClasses=[], bAllowPartialPath=True, costLimit=0, maxPathPoints=64,
                            navData=None, agentName="", world=W)
        ok = r["result"] == "Success" and not r["bIsPartial"]
        e = r["effectiveEnd"]
        rows.append((name, ("REACHED" if ok else "BLOCKED") + f" {r['pathLength'] / 100:.1f} m"
                     + ("" if ok else f", stops at ({e['x']:.0f}, {e['y']:.0f}, {e['z']:.0f})")))
    return rows
