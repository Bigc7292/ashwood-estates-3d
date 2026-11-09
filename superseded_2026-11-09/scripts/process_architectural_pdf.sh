#!/usr/bin/env bash
# Portable entrypoint: process an architectural/marketing PDF into archive structure.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PDF="${1:?Usage: $0 /path/to/source.pdf}"
if [[ ! -f "$PDF" ]]; then echo "PDF not found: $PDF" >&2; exit 1; fi
VENV="$ROOT/.venv"
if [[ ! -d "$VENV" ]]; then
  python3 -m venv "$VENV"
  # shellcheck disable=SC1091
  source "$VENV/bin/activate"
  pip install -r "$ROOT/scripts/requirements.txt"
else
  # shellcheck disable=SC1091
  source "$VENV/bin/activate"
fi
mkdir -p "$ROOT/original" "$ROOT/extracts/"{text/pages,pages,images,contact-sheets,plans} \
  "$ROOT/plans" "$ROOT/floors" "$ROOT/rooms" "$ROOT/cad-style" "$ROOT/manifests" \
  "$ROOT/missing" "$ROOT/reports" "$ROOT/previews" "$ROOT/state"
# Preserve byte-for-byte copy
cp -a "$PDF" "$ROOT/original/source.pdf"
sha256sum "$ROOT/original/source.pdf" | tee "$ROOT/original/SHA256.txt"
pdfinfo "$ROOT/original/source.pdf" | tee "$ROOT/extracts/text/pdfinfo.txt"
pages=$(pdfinfo "$ROOT/original/source.pdf" | awk '/^Pages:/ {print $2}')
pdftotext -layout "$ROOT/original/source.pdf" "$ROOT/extracts/text/all_layout.txt"
for i in $(seq 1 "$pages"); do
  pdftotext -f "$i" -l "$i" -layout "$ROOT/original/source.pdf" \
    "$ROOT/extracts/text/pages/page_$(printf '%02d' "$i").txt"
done
pdfimages -list "$ROOT/original/source.pdf" | tee "$ROOT/extracts/images/pdfimages_list.txt" || true
pdfimages -all "$ROOT/original/source.pdf" "$ROOT/extracts/images/embedded/img" || true
pdftoppm -png -r 72 "$ROOT/original/source.pdf" "$ROOT/extracts/pages/page72"
pdftoppm -png -r 110 "$ROOT/original/source.pdf" "$ROOT/extracts/pages/page110"
python "$ROOT/scripts/build_contact_sheets.py"
python "$ROOT/scripts/extract_floorplans_cadstyle.py" --pdf "$ROOT/original/source.pdf"
echo "Done. Review manifests/, missing/, cad-style/, reports/. Then run package_zip.sh"
