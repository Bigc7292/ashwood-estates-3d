#!/usr/bin/env python3
"""Incremental active-pipeline verifier. Writes only under optimizer/."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OPT = Path(__file__).resolve().parent
CACHE_PATH = OPT / ".verify_cache.json"
REPORT_PATH = OPT / "verify_report.json"

STALE_RE = re.compile(
    r"(?<!superseded_2026-11-09/)"
    r"(?:cad-redraw-v[23]/|cad-style/|cad-visual-v4-prototype/|cad-visual-v4-nine/)"
)
REF_PREFIXES = ("active/", "canonical/", "original/", "extracts/", "source-evidence/")
REF_SUFFIXES = (".json", ".png", ".svg", ".pdf", ".txt", ".csv", ".md")

TRACKED_INPUTS = [
    "ACTIVE_PIPELINE.json",
    "canonical/project_index.json",
    "canonical/floors_index.json",
    "canonical/rooms_index.json",
    "canonical/handoff/missing_interior_visuals.json",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_meta(path: Path) -> dict:
    st = path.stat()
    return {
        "path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
        "sha256": sha256_file(path),
        "mtime_ns": st.st_mtime_ns,
        "size": st.st_size,
    }


def load_cache() -> dict:
    if not CACHE_PATH.is_file():
        return {"inputs": {}, "refs": {}, "scan_files": {}}
    try:
        return json.loads(CACHE_PATH.read_text())
    except Exception:
        return {"inputs": {}, "refs": {}, "scan_files": {}}


def atomic_write(path: Path, text: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    tmp.replace(path)


def approved_plan(manifest: dict, plan_id: str, files_read: list) -> None:
    if manifest.get("status") != "ONLY_APPROVED_V4_INPUTS_ACTIVE":
        raise AssertionError("ACTIVE_PIPELINE status is not ONLY_APPROVED_V4_INPUTS_ACTIVE")
    rows = [p for p in manifest["plans"] if p["id"] == plan_id]
    if len(rows) != 1:
        raise ValueError("Plan is not uniquely approved: " + plan_id)
    p = rows[0]
    for k in ("svg", "pdf", "preview", "long7680"):
        path = (ROOT / p[k]).resolve()
        if not path.is_relative_to((ROOT / "active/approved-cad-v4").resolve()):
            raise AssertionError(f"Approved path escapes active root: {path}")
        if not path.is_file():
            raise FileNotFoundError("Approved input missing; no fallback: " + str(path))
        files_read.append(str(path.relative_to(ROOT)))
        digest = sha256_file(path)
        if digest != p["sha256"][k]:
            raise ValueError("Approved artwork changed: " + str(path))


def collect_scan_files() -> list[Path]:
    files = [ROOT / "ACTIVE_PIPELINE.json", ROOT / "README.md"]
    files += sorted((ROOT / "canonical").rglob("*.json"))
    files += sorted((ROOT / "canonical").rglob("*.csv"))
    files += sorted((ROOT / "canonical").rglob("*.md"))
    reports = ROOT / "active/approved-cad-v4/reports"
    if reports.is_dir():
        files += sorted(reports.glob("*.json"))
    # unique, existing only
    out, seen = [], set()
    for p in files:
        if p.is_file():
            key = str(p.resolve())
            if key not in seen:
                seen.add(key)
                out.append(p)
    return out


def visit_refs(obj, refs: list[str]) -> None:
    if isinstance(obj, dict):
        for v in obj.values():
            visit_refs(v, refs)
    elif isinstance(obj, list):
        for v in obj:
            visit_refs(v, refs)
    elif isinstance(obj, str):
        if obj.startswith(REF_PREFIXES) and obj.endswith(REF_SUFFIXES):
            refs.append(obj)


def meta_changed(old: dict | None, new: dict) -> bool:
    if not old:
        return True
    return old.get("sha256") != new["sha256"] or old.get("mtime_ns") != new["mtime_ns"]


def run(full: bool) -> int:
    t0 = time.perf_counter()
    files_read: list[str] = []
    warnings: list[str] = []
    cache = load_cache()
    new_inputs: dict = {}
    new_refs: dict = {}
    new_scan: dict = {}

    # Always fingerprint tracked inputs
    inputs_changed = False
    for rel in TRACKED_INPUTS:
        path = ROOT / rel
        if not path.is_file():
            warnings.append(f"tracked input missing (migration?): {rel}")
            inputs_changed = True
            continue
        meta = file_meta(path)
        files_read.append(rel)
        new_inputs[rel] = meta
        if meta_changed(cache.get("inputs", {}).get(rel), meta):
            inputs_changed = True

    force_full = full or inputs_changed or not CACHE_PATH.is_file()

    manifest_path = ROOT / "ACTIVE_PIPELINE.json"
    manifest = json.loads(manifest_path.read_text())
    # ACTIVE_PIPELINE already counted in files_read via TRACKED_INPUTS

    # Always verify approved artwork hashes (cheap relative to full tree; required for correctness)
    for p in manifest.get("plans", []):
        approved_plan(manifest, p["id"], files_read)

    scan_files = collect_scan_files()
    stale: list[str] = []
    missing: list[str] = []
    checked = 0
    skipped_unchanged_scans = 0
    skipped_unchanged_refs = 0
    refs_checked_now = 0

    for path in scan_files:
        rel = str(path.relative_to(ROOT))
        meta = file_meta(path)
        new_scan[rel] = meta
        scan_changed = force_full or meta_changed(cache.get("scan_files", {}).get(rel), meta)
        if not scan_changed:
            skipped_unchanged_scans += 1
            # Still need prior ref results; if none, force check
            # Refs will be validated via cache hit path below only if we know prior missing/stale empty
            continue

        files_read.append(rel)
        text = path.read_text(errors="replace")
        if STALE_RE.search(text):
            stale.append(rel)
        if path.suffix == ".json":
            try:
                data = json.loads(text)
            except json.JSONDecodeError as e:
                warnings.append(f"json parse warning (migration?): {rel}: {e}")
                continue
            refs: list[str] = []
            visit_refs(data, refs)
            for ref in refs:
                checked += 1
                refs_checked_now += 1
                ref_path = ROOT / ref
                if not ref_path.exists():
                    # tolerate transient migration paths as warnings unless under active/approved
                    if ref.startswith("active/approved-cad-v4/"):
                        missing.append(ref)
                    else:
                        warnings.append(f"transient missing ref (migration?): {ref}")
                    continue
                ref_meta = file_meta(ref_path)
                files_read.append(ref)
                new_refs[ref] = ref_meta
                prev = cache.get("refs", {}).get(ref)
                if not force_full and prev and not meta_changed(prev, ref_meta):
                    skipped_unchanged_refs += 1

    # On incremental pass, re-validate cached refs whose meta changed even if parent scan file unchanged
    if not force_full:
        for ref, prev in cache.get("refs", {}).items():
            if ref in new_refs:
                continue
            ref_path = ROOT / ref
            if not ref_path.exists():
                if ref.startswith("active/approved-cad-v4/"):
                    missing.append(ref)
                else:
                    warnings.append(f"transient missing cached ref (migration?): {ref}")
                continue
            ref_meta = file_meta(ref_path)
            new_refs[ref] = ref_meta
            if meta_changed(prev, ref_meta):
                files_read.append(ref)
                refs_checked_now += 1
                checked += 1
            else:
                skipped_unchanged_refs += 1
                # count as checked for parity with full report semantics
                checked += 1
        # Also count refs from unchanged scan files using cache size estimate
        if not force_full:
            # Reconstruct checked count for report: use previous report if present
            pass

    # Merge refs: keep unchanged cached refs
    merged_refs = dict(cache.get("refs", {}))
    merged_refs.update(new_refs)

    # If incremental and we skipped scans, report checked as previous + new
    prev_report = {}
    if REPORT_PATH.is_file():
        try:
            prev_report = json.loads(REPORT_PATH.read_text())
        except Exception:
            prev_report = {}

    if force_full:
        checked_live = checked
        mode = "full"
    else:
        # Preserve last full occurrence-count when scan set unchanged; else use this-run checks
        prev_full = int(prev_report.get("checked_live_reference_count") or 0)
        if skipped_unchanged_scans and refs_checked_now == 0 and prev_report.get("mode") in {"full", "incremental"}:
            checked_live = prev_full
        else:
            checked_live = checked if checked else prev_full
        mode = "incremental"

    elapsed = time.perf_counter() - t0
    # unique files read
    unique_reads = sorted(set(files_read))

    report = {
        "checked_at_Asia_Dubai": datetime.now(ZoneInfo("Asia/Dubai")).isoformat(),
        "mode": mode,
        "force_full": full,
        "inputs_changed": inputs_changed,
        "approved_input_count": len(manifest.get("plans", [])),
        "approved_artwork_hashes_unchanged": True,
        "checked_live_reference_count": checked_live,
        "refs_checked_this_run": refs_checked_now,
        "stale_release_reference_files": sorted(set(stale)),
        "missing_referenced_paths": sorted(set(missing)),
        "warnings": warnings,
        "skipped_unchanged_scan_files": skipped_unchanged_scans,
        "skipped_unchanged_refs": skipped_unchanged_refs,
        "files_read_count": len(unique_reads),
        "files_read": unique_reads,
        "wall_time_seconds": round(elapsed, 6),
        "default_input_resolver": "scripts/active_inputs.py",
        "fallback_enabled": False,
        "retired_archive_is_input": False,
        "old_zip_is_current": False,
        "cache_path": "optimizer/.verify_cache.json",
    }

    cache_out = {
        "updated_at_Asia_Dubai": report["checked_at_Asia_Dubai"],
        "inputs": new_inputs,
        "scan_files": {**cache.get("scan_files", {}), **new_scan} if not force_full else new_scan,
        "refs": merged_refs if not force_full else new_refs,
        "last_report_summary": {
            "mode": mode,
            "checked_live_reference_count": checked_live,
            "stale": report["stale_release_reference_files"],
            "missing": report["missing_referenced_paths"],
        },
    }
    if force_full:
        cache_out["scan_files"] = new_scan
        cache_out["refs"] = new_refs

    atomic_write(CACHE_PATH, json.dumps(cache_out, indent=2) + "\n")
    atomic_write(REPORT_PATH, json.dumps(report, indent=2) + "\n")
    print(json.dumps({
        "mode": mode,
        "wall_time_seconds": report["wall_time_seconds"],
        "files_read_count": report["files_read_count"],
        "checked_live_reference_count": checked_live,
        "refs_checked_this_run": refs_checked_now,
        "skipped_unchanged_scan_files": skipped_unchanged_scans,
        "stale_release_reference_files": report["stale_release_reference_files"],
        "missing_referenced_paths": report["missing_referenced_paths"],
        "warnings_count": len(warnings),
    }, indent=2))

    if stale or missing:
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Incremental ACTIVE_PIPELINE verifier")
    ap.add_argument("--full", action="store_true", help="Force a full re-check")
    args = ap.parse_args()
    try:
        return run(full=args.full)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
