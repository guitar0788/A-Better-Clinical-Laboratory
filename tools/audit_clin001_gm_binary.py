#!/usr/bin/env python3
"""Verify a genuinely built ABCL DLL contains Super-GM in test mode only.

This is a post-build, byte-level test marker audit: NOT compilation, L4,
nor proof of a secure release. Only uses the output addon DLL, never
uploads original game references or keys.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

GM_LABEL = "中文超级GM"
GM_LOG = "[ABCL GM TEST ONLY]"
LEGACY_TEST_BUTTON = "ABCL G1 [Test]"
LEGACY_SPAWN = "REQUEST ONE NATIVE LEAD PATIENT"
DEVELOPER_MARKERS = (GM_LABEL, GM_LOG, LEGACY_TEST_BUTTON, LEGACY_SPAWN)


def inspect(path: Path, mode: str):
    if mode not in {"test", "release"}:
        raise ValueError("Expected --mode test or release")
    if not path.is_file() or path.is_symlink():
        raise ValueError("Missing/untrusted compiled DLL")
    raw = path.read_bytes()
    if not raw.startswith(b"MZ") or b"BSJB" not in raw or len(raw) < 64:
        raise ValueError("Input is not a recognized managed PE/CLI assembly")
    markers = {value: value.encode("utf-16-le") in raw
               for value in DEVELOPER_MARKERS}
    if mode == "test":
        if not markers[GM_LABEL] or not markers[GM_LOG]:
            raise ValueError("G1 TEST DLL is missing Chinese Super-GM markers")
    else:
        included = [name for name, present in markers.items() if present]
        if included:
            raise ValueError("RELEASE candidate includes prohibited debug UI: "
                             + ", ".join(included))
    return {"mode": mode,
            "dll_sha256": hashlib.sha256(raw).hexdigest(),
            "dll_bytes": len(raw), "gm_markers_present": markers,
            "result": "BINARY_MARKER_GATE_PASS",
            "limitation": "Does not replace game-compatible L3 or real-game L4"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dll", type=Path, required=True)
    ap.add_argument("--mode", choices=["test", "release"], required=True)
    args = ap.parse_args()
    print(json.dumps(inspect(args.dll, args.mode),
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
