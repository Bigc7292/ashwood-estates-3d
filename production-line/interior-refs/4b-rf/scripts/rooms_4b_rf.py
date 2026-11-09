"""Per-room record for the Ashwood 4B RF interior reference set (lane/interior-refs, 2026-11-10).
Each entry written after comparing the V4 plan crop (active/approved-cad-v4/png/FP-4B-RF_V4_long7680.png) with the image.
Overlay lists 4 RF interior/service rooms; the roof terrace is outdoor and belongs to the exterior lane."""
FLOOR, PLAN_ID = "rf", "4B-RF"
RAW = "/workspace/irw/rf/raw"
SC, CO = "GENERATED-SOURCE-CONDITIONED", "GENERATED-CONCEPT"
EXCLUDED = [dict(space="roof terrace (TERRACE, dimension UNKNOWN on plan)", reason="Outdoor; not an interior/service record in optimizer/handoff_overlay.json; exterior lane"),
            dict(space="stair core on RF", reason="Not a separate record in the overlay; not generated")]
README_EXTRA = "\nNot included: the roof terrace (outdoor, exterior lane) and the RF stair core (no overlay record). The RF plan is labelled NOT TO SCALE with every room dimension flagged uncertain (dagger).\n"
ROOMS = [
 dict(room="mep", label="MEP (plant)", method=SC, result="regenerated", refs=["plan-crop","p17-materials"],
  observed="3.80x15.70 m label (flagged uncertain, plan not to scale); large enclosed room west of the stair; three shaft/hatch symbols on the west wall",
  assumed="Room proportions, hatch sizes, finishes, lighting; all plant equipment omitted (none drawn)",
  mismatches="Pass 1 rejected: shafts drawn as three open lift-style doors. Pass 2: recess/opening at the far right not checked against the plan; drawn room shape is not a simple rectangle"),
 dict(room="lift", label="Lift (roof)", method=CO, result="regenerated", refs=["plan-crop","p17-materials"],
  observed="1.60x1.80 m label (flagged uncertain); brochure p24 'Lift with direct roof access'",
  assumed="Car interior entirely assumed (no source image)",
  mismatches="Pass 1 rejected: glass side panel in the car. Pass 2: landing indicator shows invented digits '67' (printed matter not in source; ignore)"),
 dict(room="powder", label="Powder (roof)", method=SC, result="pass", refs=["plan-crop","p17-materials","p24-spec-text"],
  observed="1.50x2.40 m label (flagged uncertain); basin symbol at the NW; WC towards the south; door on the north from the stair lobby; no window",
  assumed="Calacatta panel, terrazzo floor, bronze fittings",
  mismatches="None found"),
 dict(room="pantry", label="Pantry (roof)", method=SC, result="regenerated", refs=["plan-crop","p17-materials"],
  observed="2.00x2.40 m label (flagged uncertain); single counter run on the south wall; open to the stair lobby on the north",
  assumed="Sink, under-counter fridge, cabinet style, finishes",
  mismatches="Pass 1 rejected: U-shaped counters. Pass 2: sink and fridge are not drawn on the plan"),
]
