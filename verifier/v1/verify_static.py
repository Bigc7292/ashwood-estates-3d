#!/usr/bin/env python3
"""Structural release checks for Ashwood v1. Appends every run to verifier/runs/."""
from __future__ import annotations
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FF = ROOT / "active/floorplan3d-spike/FP-4B-FF"
EXT = ROOT / "exterior-garden-3d/4b/walk_exterior_wip"
RUNS = ROOT / "verifier/runs"

def check(results, name, ok, detail):
    results.append({"check": name, "pass": bool(ok), "detail": detail})

def main():
    results = []
    required = [FF / "data/fp-4b-ff.plan.r8.json", FF / "data/fp-4b-ff.plan.r8.js", FF / "r8_step2/build_r8_layout.py"]
    for path in required:
        check(results, f"exists:{path.relative_to(ROOT)}", path.is_file(), str(path))
    plan_path = FF / "data/fp-4b-ff.plan.r8.json"
    if plan_path.is_file():
        plan = json.loads(plan_path.read_text())
        expected = {"WALL_RECTS": 417, "ROOM_POLYS": 14, "DOORS": 12, "WINDOWS": 10, "FURNITURE": 41, "STAIRS": 1, "VOIDS": 3}
        aliases = {"WALL_RECTS": ["WALL_RECTS", "walls"], "ROOM_POLYS": ["ROOM_POLYS", "rooms"], "DOORS": ["DOORS", "doors"], "WINDOWS": ["WINDOWS", "windows"], "FURNITURE": ["FURNITURE", "furniture"], "STAIRS": ["STAIRS", "stairs"], "VOIDS": ["VOIDS", "voids"]}
        for key, count in expected.items():
            value = next((plan.get(k) for k in aliases[key] if isinstance(plan.get(k), list)), None)
            check(results, f"ff-count:{key}", value is not None and len(value) == count, f"expected={count}, actual={None if value is None else len(value)}")
        text = json.dumps(plan)
        check(results, "ff-scale-assumption", "35.53012869683798" in text and "ASSUM" in text.upper(), "r8 plan must carry scale and assumption provenance")
    index_path = FF / "index.html"
    if index_path.is_file():
        index = index_path.read_text()
        check(results, "ff-active-r8", "fp-4b-ff.plan.r8.js" in index, "active FF index must load r8 plan JS")
        check(results, "ff-no-gf-ceiling", "[1528,640]" not in index.replace(" ", "") and "[14372,22899]" not in index.replace(" ", ""), "GF CEIL_OUTLINE coordinates must not remain")
    pages = ["front_v2.html", "left_pass.html", "right_pass.html", "site_pass.html", "rear_v3.html"]
    for name in pages:
        path = EXT / name
        if not path.is_file():
            check(results, f"exterior-exists:{name}", False, "missing")
            continue
        text = path.read_text()
        check(results, f"water-reflectivity:{name}", "MODEL_OVERRIDES" in text and re.search(r"reflectivity\s*:\s*(?:0\.(?:[2-9]\d*)|1(?:\.0+)?)", text) is not None, "active Water2 reflectivity must be >=0.2")
        check(results, f"orbit-controls:{name}", re.search(r"new\s+OrbitControls\s*\(", text) is not None, "locked views require OrbitControls")
        check(results, f"capture-hook:{name}", "__capture" in text and "__frame" in text, "deterministic one-frame capture hooks required")
        check(results, f"no-unseeded-random:{name}", re.search(r"(?<![\w.])Math\.random\s*\(", text) is None, "bare Math.random found")
    protected = ROOT / "exterior-garden-3d/4b/model/data/model.json"
    check(results, "protected-model-present", protected.is_file(), "M30/M44 source model must remain present")
    changelog = (ROOT / "CHANGELOG.md").read_text() if (ROOT / "CHANGELOG.md").is_file() else ""
    check(results, "changelog-quality-pass", "viewer-quality-2026-11-10" in changelog, "integrated change set must be logged")
    ok = all(r["pass"] for r in results)
    report = {"version": "v1", "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(), "command": " ".join(sys.argv), "exit_code": 0 if ok else 1, "passed": sum(r["pass"] for r in results), "failed": sum(not r["pass"] for r in results), "results": results}
    try:
        report["git_head"] = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        report["git_head"] = "NOT FOUND"
    RUNS.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    (RUNS / f"{stamp}-static-v1.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return report["exit_code"]

if __name__ == "__main__":
    raise SystemExit(main())
