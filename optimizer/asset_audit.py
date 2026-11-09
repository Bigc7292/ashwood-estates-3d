#!/usr/bin/env python3
"""Audit generated-visuals manifests and handoff against files on disk.

Checks (read-only; writes report under optimizer/ only):
  - missing files listed in manifests
  - orphan image files next to a manifest (not listed, not source-refs)
  - duplicate content hashes across audited trees
  - generated assets lacking method label GENERATED-CONCEPT / GENERATED-SOURCE-CONDITIONED
  - generated assets lacking source-ref / plan / brochure reference
  - absolute output_path that does not resolve under this repo

Exit nonzero on breaches. Free stdlib only.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OPT = Path(__file__).resolve().parent
REPORT = OPT / "asset_audit_report.json"

MANIFEST_GLOBS = [
    "**/generated_visuals_manifest.json",
]
SKIP_DIR_NAMES = {".git", ".venv", "node_modules", "__pycache__", "superseded_2026-11-09"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
OK_METHODS = {"GENERATED-CONCEPT", "GENERATED-SOURCE-CONDITIONED"}
ALLOWED_ORPHAN_DIRS = {"_raw_unlabelled", "_rejected_first_pass", "source-refs"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_write(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    tmp.replace(path)


def find_manifests() -> list[Path]:
    out: list[Path] = []
    for p in ROOT.rglob("generated_visuals_manifest.json"):
        if any(part in SKIP_DIR_NAMES for part in p.parts):
            continue
        out.append(p)
    # Floorplan3D spike manifests (different schema) — include lightly
    for p in [
        ROOT / "active/floorplan3d-spike/FP-4B-GF/manifest.json",
        ROOT / "canonical/handoff/missing_interior_visuals.json",
    ]:
        if p.is_file():
            out.append(p)
    return sorted(set(out))


def remap_abs(path_str: str) -> list[Path]:
    """Try to resolve absolute paths that were written outside this repo root."""
    candidates: list[Path] = []
    raw = Path(path_str)
    if not path_str:
        return candidates
    if not raw.is_absolute():
        candidates.append(ROOT / raw)
        candidates.append(raw)
        return candidates
    s = str(raw)
    # Common misplaced roots seen in Ashwood manifests
    markers = (
        "/exterior-garden-3d/",
        "/generated-exteriors/",
        "/plan-visuals-archive/",
        "/active/",
        "/canonical/",
    )
    for marker in markers:
        if marker in s:
            rel = s.split(marker, 1)[1]
            prefix = marker.strip("/")
            # marker like /exterior-garden-3d/ -> prefix exterior-garden-3d
            top = marker.strip("/").split("/")[0]
            candidates.append(ROOT / top / rel)
            candidates.append(ROOT / rel)
    # Strip a leading /workspace/<something>/
    if s.startswith("/workspace/"):
        rest = s[len("/workspace/") :]
        # rest may be exterior-garden-3d/... OR plan-visuals-archive/...
        if rest.startswith("plan-visuals-archive/"):
            candidates.append(ROOT / rest[len("plan-visuals-archive/") :])
        candidates.append(ROOT / rest)
        # also try just the basename tree under known dirs
    candidates.append(raw)
    # de-dupe preserving order
    seen = set()
    uniq = []
    for c in candidates:
        key = str(c)
        if key in seen:
            continue
        seen.add(key)
        uniq.append(c)
    return uniq


def resolve_existing(path_str: str) -> Path | None:
    for c in remap_abs(path_str):
        try:
            if c.is_file():
                return c.resolve()
        except OSError:
            continue
    return None


def audit_generated_visuals(manifest_path: Path, report: dict) -> None:
    data = json.loads(manifest_path.read_text())
    rel_m = str(manifest_path.relative_to(ROOT))
    entry = {
        "manifest": rel_m,
        "kind": "generated_visuals",
        "assets": 0,
        "missing": [],
        "orphans": [],
        "bad_method_label": [],
        "missing_source_ref": [],
        "unresolved_abs_paths": [],
        "sha_mismatches": [],
    }
    assets = data.get("assets") or []
    if not isinstance(assets, list):
        report["breaches"].append({"type": "schema", "manifest": rel_m, "detail": "assets not a list"})
        report["manifests"].append(entry)
        return
    entry["assets"] = len(assets)
    listed: set[Path] = set()
    base = manifest_path.parent

    for a in assets:
        if not isinstance(a, dict):
            continue
        aid = a.get("asset_id") or a.get("id") or "?"
        op = a.get("output_path") or a.get("path") or ""
        method = (a.get("method") or "").strip()
        found = resolve_existing(op) if op else None
        if op and Path(op).is_absolute() and found is None:
            entry["unresolved_abs_paths"].append({"asset_id": aid, "output_path": op})
        if op and Path(op).is_absolute() and found is not None:
            # still flag if the literal absolute path is outside repo
            try:
                if not Path(op).resolve().is_relative_to(ROOT) and str(Path(op)) != str(found):
                    entry["unresolved_abs_paths"].append(
                        {
                            "asset_id": aid,
                            "output_path": op,
                            "resolved_under_repo": str(found.relative_to(ROOT)),
                            "note": "absolute path points outside repo; remapped for check",
                        }
                    )
            except Exception:
                entry["unresolved_abs_paths"].append({"asset_id": aid, "output_path": op})
        if not found:
            entry["missing"].append({"asset_id": aid, "output_path": op})
        else:
            listed.add(found)
            expected = a.get("sha256")
            if expected:
                actual = sha256_file(found)
                if actual != expected:
                    entry["sha_mismatches"].append(
                        {"asset_id": aid, "expected": expected, "actual": actual}
                    )
        # method / label checks for generated assets
        if method.startswith("GENERATED") or "GENERATED" in method:
            if method not in OK_METHODS:
                entry["bad_method_label"].append({"asset_id": aid, "method": method})
            # filename should also carry the label when burned
            name = (found.name if found else Path(op).name)
            if name and not any(tag in name for tag in OK_METHODS):
                # soft: contact sheets etc.
                if "CONTACT-SHEET" not in name.upper():
                    entry["bad_method_label"].append(
                        {"asset_id": aid, "method": method, "filename": name, "detail": "filename missing method tag"}
                    )
            refs = []
            for key in ("reference_paths", "source_plans", "brochure_renders", "source_refs"):
                v = a.get(key)
                if v:
                    refs.append(v)
            if not refs:
                entry["missing_source_ref"].append({"asset_id": aid, "method": method})

    listed_hashes = {}
    for lp in listed:
        try:
            listed_hashes[sha256_file(lp)] = str(lp.relative_to(ROOT))
        except OSError:
            pass

    # orphans: images under manifest dir not listed and not in allowed dirs as "expected extras"
    # Raw/rejected are expected_extra (warning only). Byte-identical mirrors -> mirror_duplicate warning.
    # Truly unlisted deliverables (e.g. contact sheet with no asset row) -> breach.
    for p in base.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        if p.name.startswith("generated_visuals"):
            continue
        try:
            rp = p.resolve()
        except OSError:
            continue
        if rp in listed:
            continue
        rel = str(p.relative_to(ROOT))
        if any(part in ALLOWED_ORPHAN_DIRS for part in p.parts):
            entry["orphans"].append({"path": rel, "class": "expected_extra", "dir": next(d for d in p.parts if d in ALLOWED_ORPHAN_DIRS)})
            continue
        try:
            digest = sha256_file(rp)
        except OSError:
            digest = None
        if digest and digest in listed_hashes:
            entry["orphans"].append({"path": rel, "class": "mirror_duplicate", "matches": listed_hashes[digest]})
        elif "CONTACT-SHEET" in p.name.upper() or "CONTACT_SHEET" in p.name.upper():
            entry["orphans"].append({"path": rel, "class": "companion_contact_sheet"})
        else:
            entry["orphans"].append({"path": rel, "class": "unlisted"})

    report["manifests"].append(entry)
    # Breaches: missing files, truly unlisted orphans, bad labels, missing source refs, sha mismatch
    for m in entry["missing"]:
        report["breaches"].append({"type": "missing_file", "manifest": rel_m, **m})
    for o in entry["orphans"]:
        if o.get("class") == "unlisted":
            report["breaches"].append({"type": "orphan_unlisted", "manifest": rel_m, **o})
        elif o.get("class") == "mirror_duplicate":
            report["warnings"].append({"type": "mirror_duplicate", "manifest": rel_m, **o})
        elif o.get("class") == "companion_contact_sheet":
            report["warnings"].append({"type": "companion_contact_sheet", "manifest": rel_m, **o})
        elif o.get("class") == "expected_extra":
            report["warnings"].append({"type": "raw_or_rejected_present", "manifest": rel_m, **o})
    for b in entry["bad_method_label"]:
        report["breaches"].append({"type": "bad_method_label", "manifest": rel_m, **b})
    for b in entry["missing_source_ref"]:
        report["breaches"].append({"type": "missing_source_ref", "manifest": rel_m, **b})
    for b in entry["sha_mismatches"]:
        report["breaches"].append({"type": "sha_mismatch", "manifest": rel_m, **b})
    # absolute-path remap is a warning, not hard breach (migration may still use old abs roots)
    for u in entry["unresolved_abs_paths"]:
        if "resolved_under_repo" in u:
            report["warnings"].append({"type": "abs_path_remapped", "manifest": rel_m, **u})
        else:
            report["breaches"].append({"type": "abs_path_unresolved", "manifest": rel_m, **u})


def audit_handoff(manifest_path: Path, report: dict) -> None:
    data = json.loads(manifest_path.read_text())
    rel_m = str(manifest_path.relative_to(ROOT))
    records = data.get("rooms") or data.get("records") or data.get("items") or data
    if isinstance(data, dict) and "rooms" not in data and "records" not in data and "items" not in data:
        # try common handoff shapes
        for k, v in data.items():
            if isinstance(v, list) and v and isinstance(v[0], dict):
                records = v
                break
    if not isinstance(records, list):
        report["manifests"].append({"manifest": rel_m, "kind": "handoff", "skipped": "no record list"})
        return
    entry = {
        "manifest": rel_m,
        "kind": "handoff",
        "records": len(records),
        "missing_paths": [],
        "generated_without_source_flag": [],
    }
    path_keys = (
        "cad_path",
        "plan_path",
        "source_plan_path",
        "style_evidence_path",
        "output_path",
        "image_path",
        "generated_path",
    )
    for rec in records:
        if not isinstance(rec, dict):
            continue
        rid = rec.get("room_id") or rec.get("id") or rec.get("slot_id") or "?"
        for key in path_keys:
            v = rec.get(key)
            if isinstance(v, str) and v.strip():
                if resolve_existing(v) is None and not v.startswith("http"):
                    # only flag if it looks like a repo-relative file path
                    if "/" in v or v.endswith((".png", ".jpg", ".svg", ".pdf", ".json")):
                        entry["missing_paths"].append({"record": rid, "field": key, "path": v})
        if rec.get("generated_available") and rec.get("source_missing") is True:
            # allowed, but must not silently claim source
            pass
        if rec.get("generated_available") and not (
            rec.get("source_page")
            or rec.get("source_bbox")
            or rec.get("source_plan_path")
            or rec.get("style_evidence_path")
            or rec.get("reference_paths")
        ):
            # informational — handoff_guard owns eligibility; we only note
            entry["generated_without_source_flag"].append(rid)
    report["manifests"].append(entry)
    for m in entry["missing_paths"]:
        # handoff paths can be aspirational during migration — warnings unless clearly under active/
        p = m["path"]
        if p.startswith("active/") or p.startswith("canonical/") or p.startswith("original/"):
            report["breaches"].append({"type": "handoff_missing_path", "manifest": rel_m, **m})
        else:
            report["warnings"].append({"type": "handoff_missing_path", "manifest": rel_m, **m})


def audit_floorplan_manifest(manifest_path: Path, report: dict) -> None:
    data = json.loads(manifest_path.read_text())
    rel_m = str(manifest_path.relative_to(ROOT))
    entry = {"manifest": rel_m, "kind": "floorplan3d", "missing": []}
    # collect string paths that look like files
    def walk(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str) and any(v.endswith(s) for s in (".png", ".jpg", ".json", ".js", ".html", ".svg", ".pdf", ".glb", ".gltf")):
                    if resolve_existing(v) is None and not v.startswith("http"):
                        # try relative to manifest parent
                        alt = manifest_path.parent / v
                        if not alt.is_file():
                            entry["missing"].append({"field": f"{prefix}{k}", "path": v})
                else:
                    walk(v, prefix=f"{prefix}{k}.")
        elif isinstance(obj, list):
            for i, v in enumerate(obj[:50]):
                walk(v, prefix=f"{prefix}[{i}].")
    walk(data)
    report["manifests"].append(entry)
    for m in entry["missing"]:
        report["warnings"].append({"type": "floorplan_path_missing", "manifest": rel_m, **m})


def duplicate_hash_scan(report: dict) -> None:
    trees = [
        ROOT / "exterior-garden-3d/generated-views",
        ROOT / "generated-exteriors",
    ]
    by_hash: dict[str, list[dict]] = defaultdict(list)
    total = 0
    count = 0
    for tree in trees:
        if not tree.is_dir():
            continue
        for p in tree.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            digest = sha256_file(p)
            size = p.stat().st_size
            total += size
            count += 1
            by_hash[digest].append({"path": str(p.relative_to(ROOT)), "bytes": size})
    dup_groups = []
    excess = 0
    for digest, files in by_hash.items():
        if len(files) < 2:
            continue
        files_sorted = sorted(files, key=lambda x: x["path"])
        excess += sum(f["bytes"] for f in files_sorted[1:])
        dup_groups.append({"sha256": digest, "files": files_sorted})
    report["duplicates"] = {
        "image_files": count,
        "total_bytes": total,
        "duplicate_groups": len(dup_groups),
        "excess_bytes": excess,
        "groups": sorted(dup_groups, key=lambda g: -sum(f["bytes"] for f in g["files"]))[:50],
    }
    # Cross-tree full duplicates are warnings (recommend symlink/single tree), not hard breaches
    if excess > 0:
        report["warnings"].append(
            {
                "type": "duplicate_image_bytes",
                "excess_bytes": excess,
                "excess_mb": round(excess / 1024 / 1024, 2),
                "groups": len(dup_groups),
                "detail": "Identical image bytes stored under multiple trees (often exterior-garden-3d vs generated-exteriors).",
            }
        )


def main() -> int:
    report = {
        "created_Asia_Dubai": datetime.now(ZoneInfo("Asia/Dubai")).isoformat(),
        "root": str(ROOT),
        "manifests": [],
        "breaches": [],
        "warnings": [],
        "duplicates": {},
    }
    for mp in find_manifests():
        name = mp.name
        rel = str(mp.relative_to(ROOT))
        if name == "generated_visuals_manifest.json":
            audit_generated_visuals(mp, report)
        elif rel.endswith("missing_interior_visuals.json"):
            audit_handoff(mp, report)
        elif "floorplan3d" in rel and name == "manifest.json":
            audit_floorplan_manifest(mp, report)
        else:
            report["warnings"].append({"type": "unhandled_manifest", "manifest": rel})

    duplicate_hash_scan(report)

    # summary counts
    report["summary"] = {
        "manifests_audited": len(report["manifests"]),
        "breaches": len(report["breaches"]),
        "warnings": len(report["warnings"]),
        "duplicate_excess_mb": report["duplicates"].get("excess_mb")
        if isinstance(report["duplicates"], dict)
        else None,
    }
    if report["duplicates"]:
        report["summary"]["duplicate_excess_mb"] = round(
            report["duplicates"].get("excess_bytes", 0) / 1024 / 1024, 2
        )
        report["summary"]["duplicate_groups"] = report["duplicates"].get("duplicate_groups", 0)

    atomic_write(REPORT, json.dumps(report, indent=2) + "\n")
    print(
        f"asset_audit: manifests={report['summary']['manifests_audited']} "
        f"breaches={report['summary']['breaches']} warnings={report['summary']['warnings']} "
        f"dup_groups={report['summary'].get('duplicate_groups', 0)} "
        f"dup_excess_mb={report['summary'].get('duplicate_excess_mb', 0)} "
        f"report={REPORT.relative_to(ROOT)}"
    )
    # print top breaches
    for b in report["breaches"][:20]:
        print("  BREACH", b.get("type"), b.get("manifest", ""), b.get("asset_id") or b.get("path") or b.get("record") or "")
    for w in report["warnings"][:10]:
        print("  WARN", w.get("type"), w.get("detail") or w.get("manifest") or w.get("excess_mb") or "")

    return 1 if report["breaches"] else 0


if __name__ == "__main__":
    sys.exit(main())
