# Interior Visuals Generator branch (`interior-visuals`)

AI-generated concept visuals for the Ashwood Estates project. **None of these are photographs or survey-verified drawings.** Every image carries a burned-in label: "AI-generated concept visualisation, not survey-verified". All assets are `needs-review`.

- `generated-exteriors/ashwood-estates/4b/`: 10 exterior concept views of villa 4B (4 elevations, front and back gardens, site aerial, roof terrace, courtyard, pool), built from the approved V4 plans and brochure pages 25/26.
  - `generated_visuals_manifest.json` / `.csv`: sources, prompts, observed vs assumed, plan checks, conflicts.
  - `source-refs/`: brochure crops used as generation references (source evidence, not generated).
  - `_raw_unlabelled/`: pre-label originals. `_rejected_first_pass/`: replaced drafts, not deliverables.
  - `build_outputs.py`: labels images, builds the manifests and the contact sheet.
- Future interiors go under `generated-interiors/<project>/<villa>/<floor>/<room-id>/`.

The Plan & Visuals Archivist merges this branch into `main`. See CHANGELOG.md.
