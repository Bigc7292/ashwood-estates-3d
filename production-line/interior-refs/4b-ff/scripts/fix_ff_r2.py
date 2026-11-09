R = "/workspace/irw/raw_r2_ffrf"
FIX = {
 "corridor": dict(attempts=1, chosen="r2a", how="regenerated", raw=f"{R}/4b-ff-corridor_r2_RAW.jpg",
  critic="Stair shown at the far end on the right; plan runs a straight stair along the west side of the corridor",
  observed="3.30x10.10 m; straight stair along the west side; lift then courtyard glazing on the east; open-to-below void over the entry at the south end",
  assumed="Glass balustrades, bronze handrail, door styles, finishes, stair direction (up/down)",
  residual="Stair now runs alongside the west (right-hand, camera looking south) wall for most of the corridor; it reads as rising away from the camera, direction not checked against the plan; the south void reads only as a low glass balustrade, the drop below is not visible; one extra wood-look door on the east wall between lift and glazing is assumed"),
 "bath-2": dict(attempts=1, chosen="r2a", how="regenerated", raw=f"{R}/4b-ff-bath-2_r2_RAW.jpg",
  critic="Vanity on the far (west) wall; plan has the basin on the south wall and the WC on the north",
  observed="2.30x2.50 m; WC on north wall; basin on south wall; door from dress on the east; no window found",
  assumed="Shower at the west end (plan symbol unclear), Calacatta panel behind vanity, p24 wet-area finish, bronze fittings",
  residual="Basin now on the south (left) wall and WC on the north (right) wall, camera at the east door; shower position on the west wall is assumed"),
}
