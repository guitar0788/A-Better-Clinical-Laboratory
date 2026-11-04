#!/usr/bin/env python3
"""Reject the retired C1/Super-GM path from current G1 test and release DLLs.

This post-build marker check is not compilation, clinical validation or L4.
The native R3 test panel remains permitted in a test-only DLL, never release.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

GM_LABEL = "中文超级GM"
GM_LOG = "[ABCL GM TEST ONLY]"
C1_ID = "DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE"
RETIRED_MARKERS = (GM_LABEL, GM_LOG, C1_ID, "ForceMobilePatient")
R3_TEST_MARKERS = ("ABCL G1 [Test]", "REQUEST ONE NATIVE LEAD PATIENT")


def inspect(path: Path, mode: str):
    if mode not in {"test", "release"}:
        raise ValueError("Expected --mode test or release")
    if not path.is_file() or path.is_symlink():
        raise ValueError("Missing/untrusted compiled DLL")
    raw = path.read_bytes()
    if not raw.startswith(b"MZ") or b"BSJB" not in raw or len(raw) < 64:
        raise ValueError("Input is not a recognized managed PE/CLI assembly")
    retired = {value: value.encode("utf-16-le") in raw for value in RETIRED_MARKERS}
    if any(retired.values()):
        included = [name for name, present in retired.items() if present]
        raise ValueError("Retired C1/Super-GM markers present: " + ", ".join(included))
    r3 = {value: value.encode("utf-16-le") in raw for value in R3_TEST_MARKERS}
    if mode == "release" and any(r3.values()):
        included = [name for name, present in r3.items() if present]
        raise ValueError("Release candidate includes native R3 test controls: " + ", ".join(included))
    return {
        "mode": mode,
        "dll_sha256": hashlib.sha256(raw).hexdigest(),
        "dll_bytes": len(raw),
        "retired_gm_markers_present": retired,
        "native_r3_test_markers_present": r3,
        "result": "RETIRED_GM_MARKER_GATE_PASS",
        "limitation": "Does not replace genuine net35/CLR2 L3 or real-game L4",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dll", type=Path, required=True)
    ap.add_argument("--mode", choices=["test", "release"], required=True)
    args = ap.parse_args()
    print(json.dumps(inspect(args.dll, args.mode), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
