R = "/workspace/irw/raw_r2_ffrf"
FIX = {
 "lift": dict(attempts=1, chosen="local-edit", how="clean local edit of the pass-2 raw: the indicator window (px 718-737 x 519-545) filled with its own dark background colour; no other pixels changed, no digits added", raw=f"{R}/4b-rf-lift_r2_RAW.png",
  critic="Landing indicator shows invented digits '67'",
  observed="1.60x1.80 m label (flagged uncertain, NTS); brochure p24 'Lift with direct roof access'",
  assumed="Car interior entirely assumed (no source image); landing panel assumed",
  residual="Indicator now blank/dark; door side still not verified against the plan's door mark"),
 "pantry": dict(attempts=1, chosen="r2a", how="regenerated", raw=f"{R}/4b-rf-pantry_r2_RAW.jpg",
  critic="Sink and under-counter fridge not drawn on the RF plan or sourced in the brochure",
  observed="2.00x2.40 m label (flagged uncertain, NTS); single counter run on the south wall; open to the stair lobby on the north",
  assumed="Cabinet style, finishes",
  residual="Plain counter run only, no sink, tap or fridge; room proportion not judged (NTS)"),
}
