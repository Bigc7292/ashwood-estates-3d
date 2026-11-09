#!/usr/bin/env python3
"""Report raw JPG + labelled PNG pairs that double-store the same view.

Read-only. Writes optimizer/raw_labelled_waste_report.json.
Does not delete anything.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OPT = Path(__file__).resolve().parent
OUT = OPT / "raw_labelled_waste_report.json"

SEARCH_ROOTS = [
    ROOT / "exterior-garden-3d/generated-views",
    ROOT / "generated-exteriors",
]


def main() -> int:
    pairs = []
    raw_total = 0
    labelled_total = 0
    for tree in SEARCH_ROOTS:
        if not tree.is_dir():
            continue
        for raw_dir in tree.rglob("_raw_unlabelled"):
            if not raw_dir.is_dir():
                continue
            parent = raw_dir.parent
            for raw in sorted(raw_dir.iterdir()):
                if not raw.is_file() or raw.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                    continue
                stem = raw.stem  # e.g. EXT-4b-ELEV-FRONT
                matches = sorted(parent.glob(f"{stem}_GENERATED-*.png")) + sorted(
                    parent.glob(f"{stem}_GENERATED-*.jpg")
                )
                raw_sz = raw.stat().st_size
                raw_total += raw_sz
                for lab in matches:
                    lab_sz = lab.stat().st_size
                    labelled_total += lab_sz
                    pairs.append(
                        {
                            "view_stem": stem,
                            "raw": str(raw.relative_to(ROOT)),
                            "raw_bytes": raw_sz,
                            "labelled": str(lab.relative_to(ROOT)),
                            "labelled_bytes": lab_sz,
                            "pair_bytes": raw_sz + lab_sz,
                        }
                    )
    report = {
        "created_Asia_Dubai": datetime.now(ZoneInfo("Asia/Dubai")).isoformat(),
        "pair_count": len(pairs),
        "raw_bytes": raw_total,
        "labelled_bytes_matched": labelled_total,
        "combined_pair_bytes": raw_total + labelled_total,
        "recommendation": (
            "Keep labelled PNG as deliverable; omit _raw_unlabelled from git commits "
            "(retain locally if re-label needed). Report only — do not delete."
        ),
        "pairs": pairs,
    }
    tmp = OUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(report, indent=2) + "\n")
    tmp.replace(OUT)
    print(
        f"raw_labelled_waste: pairs={len(pairs)} raw_mb={raw_total/1024/1024:.2f} "
        f"labelled_mb={labelled_total/1024/1024:.2f} combined_mb={(raw_total+labelled_total)/1024/1024:.2f} "
        f"report={OUT.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
