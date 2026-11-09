#!/usr/bin/env python3
"""Build optimizer/handoff_overlay.json guardrails without mutating canonical sources."""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OPT = Path(__file__).resolve().parent
HANDOFF = ROOT / "canonical/handoff/missing_interior_visuals.json"
PIPELINE = ROOT / "ACTIVE_PIPELINE.json"
OUT = OPT / "handoff_overlay.json"

VERIFIED_TOKENS = {"verified", "matched", "exact", "confirmed"}


def atomic_write(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    tmp.replace(path)


def normalize_match(raw: str | None) -> str:
    s = (raw or "unknown").strip().lower()
    if s in VERIFIED_TOKENS or s.startswith("verified"):
        return "verified"
    if s == "ambiguous" or "ambig" in s:
        return "ambiguous"
    if s in {"unknown", "unmatched", "none", "unassigned", ""}:
        return "unknown"
    # Never promote unknown statuses to verified
    return "unknown"


def has_plan_or_cad(rec: dict) -> bool:
    for key in ("cad_path", "plan_path", "source_plan_path"):
        v = rec.get(key)
        if isinstance(v, str) and v.strip():
            return True
    return False


def has_brochure_evidence(rec: dict) -> bool:
    if rec.get("source_page") is not None:
        return True
    if rec.get("source_bbox"):
        return True
    if isinstance(rec.get("source_plan_path"), str) and rec["source_plan_path"].strip():
        return True
    if isinstance(rec.get("style_evidence_path"), str) and rec["style_evidence_path"].strip():
        return True
    if rec.get("style_reference_ids"):
        return True
    return False


def stated_ceiling(rec: dict):
    for key in ("ceiling_height", "source_ceiling_height", "stated_ceiling_height"):
        if rec.get(key) not in (None, "", []):
            return rec.get(key), "source_stated"
    return None, "not_stated"


def main() -> int:
    if not HANDOFF.is_file():
        print("ERROR: missing handoff JSON", file=sys.stderr)
        return 2
    if not PIPELINE.is_file():
        print("ERROR: missing ACTIVE_PIPELINE.json", file=sys.stderr)
        return 2

    handoff = json.loads(HANDOFF.read_text())
    pipeline = json.loads(PIPELINE.read_text())
    active_version = "V4"
    proj_path = ROOT / "canonical/project_index.json"
    if proj_path.is_file():
        try:
            proj = json.loads(proj_path.read_text())
            if proj.get("latest_version"):
                active_version = str(proj["latest_version"])
        except Exception:
            pass
    if pipeline.get("latest_version"):
        active_version = str(pipeline["latest_version"])
    # Normalize common V4 stamps from plan_version fields
    if str(active_version).upper() in {"V4", "4", "APPROVED-V4"}:
        active_version = "V4"

    records_out = []
    breaches: list[str] = []
    warnings: list[str] = []
    counts = Counter()

    for rec in handoff.get("records", []):
        room_id = rec.get("room_id", "<unknown>")
        raw_match = rec.get("candidate_matching_status") or rec.get("match_status")
        match_status = normalize_match(raw_match if isinstance(raw_match, str) else None)

        # Hard breach: source claims verified while underlying status is not
        raw_l = (raw_match or "").strip().lower() if isinstance(raw_match, str) else ""
        if raw_l in VERIFIED_TOKENS or raw_l.startswith("verified"):
            # only allow if we independently agree — currently never, unless explicitly verified token AND style provenance says same_room
            prov = rec.get("style_match_provenance") or {}
            if not (isinstance(prov, dict) and prov.get("same_room_verified_match") is True):
                breaches.append(f"{room_id}: verified claim without same_room_verified_match")
                match_status = "unknown" if match_status == "verified" else match_status
                # demote
                if match_status == "verified":
                    match_status = "unknown"

        # Never promote ambiguous/unknown
        if match_status not in {"verified", "ambiguous", "unknown"}:
            match_status = "unknown"
        if match_status == "verified" and raw_l not in VERIFIED_TOKENS and not raw_l.startswith("verified"):
            breaches.append(f"{room_id}: attempted promotion to verified from {raw_match!r}")
            match_status = normalize_match(raw_l)

        # After rules: ambiguous/unknown stay as-is; verified only if truly verified above
        if raw_l in {"ambiguous", "unknown"} and match_status == "verified":
            breaches.append(f"{room_id}: promotion blocked ({raw_l} -> verified)")
            match_status = raw_l

        cand = list(rec.get("candidate_visual_refs") or [])
        style = list(rec.get("style_reference_ids") or [])
        overlap = sorted(set(cand) & set(style))
        style_match_overlap = bool(overlap)
        if style_match_overlap and match_status != "verified":
            warnings.append(
                f"{room_id}: style_reference_ids overlap candidate_visual_refs {overlap} (not a verified match)"
            )
            counts["style_candidate_overlap"] += 1

        dim_transcript = rec.get("dimension_transcript")
        if dim_transcript is None:
            dim_transcript = rec.get("dimensions")

        ceiling_height, ceiling_height_status = stated_ceiling(rec)

        plan_ok = has_plan_or_cad(rec)
        brochure_ok = has_brochure_evidence(rec)

        if plan_ok and brochure_ok:
            generation_eligibility = "eligible_evidence_led_concept"
            counts["eligible"] += 1
        else:
            generation_eligibility = "blocked_missing_plan_or_brochure_evidence"
            counts["blocked"] += 1
            reasons = []
            if not plan_ok:
                reasons.append("no plan/CAD path")
            if not brochure_ok:
                reasons.append("no brochure evidence")
            breaches.append(f"{room_id}: generation blocked ({', '.join(reasons)})")

        # If source claimed eligibility without evidence, that is also a breach (already blocked)
        counts[f"match_{match_status}"] += 1

        overlay_rec = {
            "room_id": room_id,
            "view_id": rec.get("view_id"),
            "villa_id": rec.get("villa_id"),
            "floor_id": rec.get("floor_id"),
            "active_plan_version": active_version,
            "plan_version_source": rec.get("plan_version"),
            "dimensions": rec.get("dimensions"),
            "dimension_transcript": dim_transcript,
            "dimension_status": rec.get("dimension_status"),
            "ceiling_height": ceiling_height,
            "ceiling_height_status": ceiling_height_status,
            "match_status": match_status,
            "candidate_matching_status": rec.get("candidate_matching_status"),
            "candidate_visual_refs": cand,
            "style_reference_ids": style,
            "style_candidate_overlap": style_match_overlap,
            "style_candidate_overlap_ids": overlap,
            "style_is_not_verified_match": True if match_status != "verified" else False,
            "generation_eligibility": generation_eligibility,
            "generated_available": bool(rec.get("generated_available")),
            "source_status": rec.get("source_status"),
            "source_present": rec.get("source_present"),
            "cad_path": rec.get("cad_path") or rec.get("plan_path"),
            "source_plan_path": rec.get("source_plan_path"),
            "source_page": rec.get("source_page"),
            "review_required": rec.get("review_required", True),
            "assumptions_must_be_labelled": True,
            "same_room_image_match_required": False,
        }
        records_out.append(overlay_rec)

    summary = {
        "records": len(records_out),
        "match_verified": counts["match_verified"],
        "match_ambiguous": counts["match_ambiguous"],
        "match_unknown": counts["match_unknown"],
        "eligible": counts["eligible"],
        "blocked": counts["blocked"],
        "style_candidate_overlap": counts["style_candidate_overlap"],
        "breaches": len(breaches),
        "warnings": len(warnings),
    }

    out = {
        "schema_version": "optimizer-handoff-overlay-1",
        "created_at_Asia_Dubai": datetime.now(ZoneInfo("Asia/Dubai")).isoformat(),
        "source_handoff": "canonical/handoff/missing_interior_visuals.json",
        "source_pipeline": "ACTIVE_PIPELINE.json",
        "active_plan_version": active_version,
        "pipeline_status": pipeline.get("status"),
        "note": "Overlay only; canonical handoff unchanged. Generator should read this file.",
        "summary": summary,
        "breaches": breaches,
        "warnings": warnings[:50],  # cap for readability
        "warnings_truncated": len(warnings) > 50,
        "records": records_out,
    }
    atomic_write(OUT, json.dumps(out, indent=2) + "\n")

    print(
        "handoff_guard: "
        f"records={summary['records']} "
        f"match(verified={summary['match_verified']}, ambiguous={summary['match_ambiguous']}, unknown={summary['match_unknown']}) "
        f"eligible={summary['eligible']} blocked={summary['blocked']} "
        f"style_overlap={summary['style_candidate_overlap']} "
        f"breaches={summary['breaches']} warnings={summary['warnings']}"
    )
    print(f"wrote {OUT.relative_to(ROOT)}")

    # Exit nonzero on any guardrail breach
    return 1 if breaches else 0


if __name__ == "__main__":
    raise SystemExit(main())
