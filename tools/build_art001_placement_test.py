#!/usr/bin/env python3
"""Build one isolated, never-release ART-001 placement-test ZIP.

Consumes only generated original artwork and explicitly allowlisted ABCL XML.
No proprietary game assets, DLLs, save files or unrelated addons are read.
"""
import argparse
import hashlib
import json
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_DATABASE = (
    "ModAddon.xml",
    "ModAssetListsABCL.xml",
    "ModObjectsABCL.xml",
    "ModStringTableEnABCLArt001.xml",
    "ModStringTableZhHansABCLArt001.xml",
    "ModColorSets.xml",
)
ALLOWED_PNGS = (
    "equipment_atlas.png",
    "icp_ms_icon.png",
    "digestion_station_icon.png",
    "workbench_icon.png",
)
ALLOWED_TOOLS = (
    "Install-ABCL-ART001.ps1",
    "INSTALL_ART001.cmd",
    "ART001_TEST_README.txt",
)


def build(proof, output, source_sha):
    proof = Path(proof).resolve()
    output = Path(output).resolve()
    if not proof.is_dir():
        raise ValueError("Offline proof directory does not exist")
    if output.exists():
        raise FileExistsError("Refusing to overwrite test package")
    if "Addons" in output.parts or "StreamingAssets" in output.parts:
        raise ValueError("Refusing to build into live game directory")
    if len(source_sha) != 40 or any(x not in "0123456789abcdef" for x in source_sha):
        raise ValueError("Expected a full lowercase 40-character Git SHA")

    manifest = json.loads((proof / "art_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("atlas_layout") != "LAYOUT_16_X_8":
        raise ValueError("Unexpected atlas format")
    records = []
    for name in ALLOWED_DATABASE:
        records.append(("ModABCLArt001Test/Database/" + name,
                        (proof / "Database" / name).read_bytes()))
    for name in ALLOWED_PNGS:
        data = (proof / "Assets" / "ABCL" / name).read_bytes()
        if data[:8] != bytes((137, 80, 78, 71, 13, 10, 26, 10)):
            raise ValueError("Invalid PNG: " + name)
        if hashlib.sha256(data).hexdigest() != manifest["sha256"][name]:
            raise ValueError("Atlas/icon hash mismatch: " + name)
        records.append(("ModABCLArt001Test/Assets/ABCL/" + name, data))
    for name in ALLOWED_TOOLS:
        records.append((name, (ROOT / "tools" / name).read_bytes()))

    info = (
        "ABCL ART-001 TEST-ONLY PLACEMENT ARTIFACT\n"
        "SOURCE_SHA=" + source_sha + "\n"
        "NOT_AN_ALPHA=TRUE\n"
        "G1_R3_WORKFLOW_UNMODIFIED=TRUE\n"
        "L4_PLACEMENT_NOT_YET_VERIFIED=TRUE\n"
        "ATLAS_SHA256=" + manifest["sha256"]["equipment_atlas.png"] + "\n"
    ).encode("utf-8")
    records.append(("BUILD_INFO.txt", info))
    # Fixed ZIP timestamps ensure reproducibility for the exact source.
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "x", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path, payload in records:
            item = zipfile.ZipInfo(path, (2020, 1, 1, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            item.external_attr = 0o644 << 16
            z.writestr(item, payload, compress_type=zipfile.ZIP_DEFLATED)
    return { "path": str(output), "source_sha": source_sha,
             "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
             "file_count": len(records) }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--proof", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--source-sha", required=True)
    args = p.parse_args()
    print(json.dumps(build(args.proof, args.output, args.source_sha)))


if __name__ == "__main__":
    main()
