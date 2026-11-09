"""Rebuild the 4B interior style guide for lane/interior-refs: pass-1 palette (p15-p17) plus brochure p24 'Interior (Summary)'.
Every item: source page, observed fact, inferred application, uncertainty."""
import json
old = json.load(open("/workspace/ivg-repo/generated-interiors/ashwood-estates/4b/style-guide/ashwood-4b_interior_style_guide.json"))
items = []
for p in old["palette"]:
    items.append(dict(item=p["name"], hex_sampled=p["hex"], source_page=p["source"], observed_fact=p["observed"],
                      inferred_application=p["inferred_application"], uncertainty=p["uncertainty"]))
P24 = "p24 'Interior (Summary)' (extracts/text/pages/page_24.txt, extracts/pages/page110-24.png)"
items += [
 dict(item="Floors: porcelain", hex_sampled=None, source_page=P24, observed_fact="Text: 'Floors: Porcelain'", inferred_application="All GF floors shown as light beige porcelain (p17 'Light Beige Marble or Porcelain')", uncertainty="Colour/size/finish not stated on p24"),
 dict(item="Walls: textured paint; feature wall Calacatta marble", hex_sampled=None, source_page=P24, observed_fact="Text: 'Walls: Textured Paint / Feature Wall: Calacatta marble'", inferred_application="General walls greige textured paint; one Calacatta feature panel per feature room (vanity walls, living)", uncertainty="Which walls are feature walls is not stated"),
 dict(item="Joinery: recon veneer", hex_sampled=None, source_page=P24, observed_fact="Text: 'Joinery: Recon Veneer'", inferred_application="Vanities, wardrobes, kitchen units, wall panelling", uncertainty="Veneer colour not stated; walnut tone taken from p15/p16 renders"),
 dict(item="Wet areas: terrazzo porcelain / porcelain concrete look", hex_sampled=None, source_page=P24, observed_fact="Text: 'Wet areas: Terrazzo Porcelain / Porcelain Concrete Look'", inferred_application="Bath, powder and maid bath floors/walls in terrazzo-look or concrete-look porcelain (supersedes pass-1 Calacatta-look wet walls)", uncertainty="Which of the two options per room is not stated; colour not stated"),
 dict(item="Doors: aluminium wood-look frame, black matt / brass handle", hex_sampled=None, source_page=P24, observed_fact="Text: 'Doors: Aluminium wood look frame door with Black Matt / Brass handle'", inferred_application="Wood-look doors with brass or black handles where a door is in view", uncertainty="Handle finish choice per room not stated"),
 dict(item="Floor-to-ceiling windows", hex_sampled=None, source_page="p24 'Building configuration' text", observed_fact="Text: 'floor-to-ceiling windows that seamlessly blend indoors and outdoor living'", inferred_application="Full-height glazing only where the V4 plan shows glazing (living rear wall, office to courtyard)", uncertainty="Which rooms get full-height glazing is not stated"),
 dict(item="Courtyard water feature", hex_sampled=None, source_page="p24 'Building configuration' text + V4 plan courtyard", observed_fact="Text: 'private courtyard with a serene water feature and an outdoor seating area'", inferred_application="View from office/gym glazing to a courtyard pool with a planted island", uncertainty="Courtyard planting/finish not in a 4B render"),
 dict(item="Lift with direct roof access", hex_sampled=None, source_page="p24 'Amenities' text", observed_fact="Text: 'Lift with direct roof access'", inferred_application="Lift car shown as a residential car", uncertainty="Car finish not in source (fully assumed)"),
]
g = dict(schema="ashwood_interior_style_guide_v2", project_id="ashwood-estates", villa_id="4b",
         label="concept visualisation, not survey-verified, not construction-ready, not certified CAD",
         scope_note="Brochure interiors p15/p16, material board p17 and spec text p24 are PROJECT-level. None is verified as a 4B room; applying them to 4B rooms is an inference.",
         design_intent=old["design_intent_summary"], items=items, rules=old["rules"] + ["Wet areas follow p24: terrazzo-look or concrete-look porcelain; Calacatta only as one feature panel"])
json.dump(g, open("/workspace/irw/style_guide_4b.json", "w"), indent=1)
md = ["# Ashwood 4B interior style guide (concept)", "", "concept visualisation, not survey-verified, not construction-ready, not certified CAD", "", g["scope_note"], "", f"**Intent:** {g['design_intent']}", "",
      "| Item | Hex (sampled, lighting-affected) | Source page | Observed fact | Inferred application | Uncertainty |", "|---|---|---|---|---|---|"]
for i in items:
    md.append(f"| {i['item']} | {i['hex_sampled'] or '-'} | {i['source_page']} | {i['observed_fact']} | {i['inferred_application']} | {i['uncertainty']} |")
md += ["", "## Rules", ""] + [f"- {r}" for r in g["rules"]] + ["", "Hex values are median pixel samples from brochure renders; they are not paint or product codes."]
open("/workspace/irw/style_guide_4b.md", "w").write("\n".join(md) + "\n")
print(len(items))
