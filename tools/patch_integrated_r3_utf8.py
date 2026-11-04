#!/usr/bin/env python3
"""Rebuild the exact owner-tested ABCL R3 wrapper with PowerShell 5.1 UTF-8 fixes.

No original game DLLs or files are shipped in the repository. This patcher
takes the previous disposable ZIP locally and refuses unrecognized input.
It never changes game addon assets, original game files, or other mods.
Windows PowerShell 5.1 Get-Content defaults to ANSI on BOM-less UTF-8 files;
explicit -Encoding UTF8 avoids corrupting Chinese localizations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

INPUT_SHA256 = "01400d176d180c6ad71da96b398a8ffd170223441a3e2975c6571478d87381c0"
OUTPUT_SHA256 = "d0f96ecca6f7df1f05cc5b4a29ad56dea145ee2824647d49ecd669670e69b7c2"
PACKAGE_ID = "ABCL-G1-ART001-TO001-TO004-INTEGRATED-TESTONLY-20261104-R3"
SCRIPT_PATHS = ("Install-ABCL-Integrated.ps1", "Restore-ABCL-Previous.ps1")
EXPECTED_ADDON_ENTRIES = 26
EXPECTED_FILES = 46


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def patch_entries(source: dict[str, bytes]) -> dict[str, bytes]:
    entries = dict(source)
    manifest = json.loads(entries["PACKAGE_MANIFEST.json"].decode("utf-8"))
    if manifest["package"] != PACKAGE_ID:
        raise ValueError("Unknown integrated test package identity")
    if manifest["G1_compiled_build"]["genuine_net35_CLR2"] is not True:
        raise ValueError("G1 genuine L3 evidence missing")
    if manifest["G1_compiled_build"]["commit"] != manifest["G1_compiled_build"]["candidate_sha"]:
        raise ValueError("Wrong source SHA for G1 DLL")
    addon = [name for name in entries if name.startswith("ModABCLG1LeadTest/")]
    if len(addon) != EXPECTED_ADDON_ENTRIES:
        raise ValueError("Unexpected addon inventory")
    dll = entries["ModABCLG1LeadTest/ModABCLG1LeadTest.dll"]
    if digest(dll) != manifest["G1_compiled_build"]["dll_sha256"]:
        raise ValueError("G1 DLL digest mismatch")
    if entries["ModABCLG1LeadTest/0Harmony.dll"]:
        raise ValueError("Vanilla code-mod loading marker must be an empty file")
    for path in entries:
        if path.lower().endswith(".xml"):
            ET.fromstring(entries[path])

    for path, receipt in manifest["file_receipts"].items():
        if path not in entries or digest(entries[path]) != receipt["sha256"] or len(entries[path]) != receipt["bytes"]:
            raise ValueError("Original test input failed SHA verification: " + path)

    for name in SCRIPT_PATHS:
        original = entries[name].decode("utf-8")
        lines = original.splitlines(keepends=True)
        if "Get-Content" not in original:
            raise ValueError("Unexpected installer source, no file reads")
        replacements = 0
        result = []
        for line in lines:
            if "Get-Content" in line and " -Raw" in line and "-Encoding " not in line:
                line = line.replace(" -Raw", " -Encoding UTF8 -Raw")
                replacements += 1
            result.append(line)
        if replacements < 1:
            raise ValueError("No unsafe PowerShell read to correct: " + name)
        edited = "".join(result)
        if any("-Encoding UTF8 -Raw" not in line for line in edited.splitlines() if "Get-Content" in line):
            raise ValueError("Remaining unspecified file decoding: " + name)
        entries[name] = edited.encode("utf-8")
        manifest["file_receipts"][name] = {
            "bytes": len(entries[name]),
            "sha256": digest(entries[name]),
            "source": "2026-11-04 targeted PS5.1 UTF-8 decoding fix; original runtime assets byte-preserved",
        }

    manifest["installer_utf8_correction"] = {
        "case": "owner reported Windows PowerShell 5.1 ANSI-decoded UTF-8 Chinese TO004 XML, causing mismatched Text start/end tags",
        "method": "explicit -Encoding UTF8 -Raw for every Get-Content in Install-ABCL-Integrated.ps1 and Restore-ABCL-Previous.ps1",
        "scope": "installer/restore metadata text only; no runtime addon files, compiled DLLs, sprites, XML or other Workshop assets changed",
        "level": "offline archive/XML/hash audit passed; owner game install and L4 pending",
    }
    entries["PACKAGE_MANIFEST.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    changed = {name for name in entries if digest(entries[name]) != digest(source[name])}
    if changed != set(SCRIPT_PATHS) | {"PACKAGE_MANIFEST.json"}:
        raise ValueError("Patch unexpectedly touched files: " + repr(changed))
    if any(entries[name] != source[name] for name in addon):
        raise ValueError("Addon runtime content changed; abort")
    for path, receipt in manifest["file_receipts"].items():
        if digest(entries[path]) != receipt["sha256"] or len(entries[path]) != receipt["bytes"]:
            raise ValueError("Patched manifest receipt invalid: " + path)
    return entries


def rebuild(input_file: Path, output_file: Path) -> str:
    if input_file.resolve() == output_file.resolve() or output_file.exists():
        raise ValueError("Refuse overwriting input or existing output")
    if digest(input_file.read_bytes()) != INPUT_SHA256:
        raise ValueError("Unreviewed input package hash; fail closed")
    with ZipFile(input_file) as archive:
        if archive.testzip() is not None or len(archive.namelist()) != EXPECTED_FILES:
            raise ValueError("Invalid or truncated source ZIP")
        if len(set(archive.namelist())) != EXPECTED_FILES:
            raise ValueError("Duplicate path in input ZIP")
        entries = {name: archive.read(name) for name in archive.namelist()}
    fixed = patch_entries(entries)
    with ZipFile(output_file, "w", compression=ZIP_DEFLATED, compresslevel=9) as output:
        for name, data in fixed.items():
            output.writestr(name, data)
    with ZipFile(output_file) as archive:
        if archive.testzip() is not None or any(archive.read(name) != data for name, data in fixed.items()):
            output_file.unlink(missing_ok=True)
            raise ValueError("Output CRC or content check failed")
    actual = digest(output_file.read_bytes())
    if actual != OUTPUT_SHA256:
        output_file.unlink(missing_ok=True)
        raise ValueError("Output does not match the fixed published SHA256")
    return actual


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print("ABCL_R3_UTF8_FIX_SHA256=" + rebuild(args.input, args.output))
