# Usage guide — Plan & Visuals Archive

## Prerequisites
- Linux/macOS with `poppler-utils` (`pdftotext`, `pdftoppm`, `pdfinfo`, `pdfimages`)
- Python 3.10+
- Free disk for page rasters

```bash
sudo apt-get install -y poppler-utils   # Debian/Ubuntu
cd plan-visuals-archive
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
```

## Process a PDF
```bash
./scripts/process_architectural_pdf.sh /path/to/brochure.pdf
./scripts/package_zip.sh
```

For the Ashwood Estates brochure layout, floorplan clips are pre-tuned in `scripts/extract_floorplans_cadstyle.py`. For other PDFs, supply a JSON config:

```bash
python scripts/extract_floorplans_cadstyle.py --pdf original/source.pdf --config my_clips.json
```

## What you get
- `original/` — unchanged PDF + SHA256
- `extracts/` — per-page text, page rasters, contact sheets, plan crops
- `plans/`, `floors/`, `rooms/` — evidence-based groupings
- `cad-style/` — source-based CAD-style rasters (**not** DXF/DWG)
- `manifests/` — CSV/JSON with page + bbox + confidence
- `missing/` — explicit gap inventory
- `docs/SYSTEM_PROMPT.md` — portable prompt for another LLM

## Limitations
- Marketing brochures often embed plans as illustrations with furniture — outputs remain rasters.
- Text layers may be garbled; always cross-check visuals.
- Do not treat outputs as construction documents.
