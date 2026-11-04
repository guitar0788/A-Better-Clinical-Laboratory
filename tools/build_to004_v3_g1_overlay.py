#!/usr/bin/env python3
"""TS's strict frozen-TO004 V3 -> installed G1 test-addon resource handoff.

This is a runtime *asset overlay*, not a new C# assembly or independent mod.
The script checks the owner-approved TO snapshot and runs that snapshot's
existing packager without modifying a single PNG or owner-authored room XML.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

TO_SHA = "9130c7a3241315d1b73e8bcfdf4cc2f560cd9804"
SMALL_PNG_SHA = "a0ec4ea41b5d96d4b755c5d244700548a6a2485d6a1d3e1bef73d8dcf09a0847"
LARGE_PNG_SHA = "3461bf9bbb8476d79e869d98f718b887a32ea88f5b0b158f185abc9f6cf85947"
SMALL_XML_SHA = "1477eb5580e1002c33384f84aaa708dfbe2fb19b09ea01dcd330309295d61457"
LARGE_XML_SHA = "4454abe727234fd8f8e6a70bcfff2f58860f05dbf3f8351b99951d7725bbad8d"
FILES = {
    "Database/ModAssetListsTO004.xml": None,
    "Database/ModPrefabObjectsTO004.xml": None,
    "Database/ModStringTableEnTO004.xml": None,
    "Database/ModStringTableZhHansTO004.xml": None,
    "Prefabs/room_toxicology_small.xml": SMALL_XML_SHA,
    "Prefabs/room_toxicology_large.xml": LARGE_XML_SHA,
    "Assets/ABCL/Prefabs/toxicology_small.png": SMALL_PNG_SHA,
    "Assets/ABCL/Prefabs/toxicology_large.png": LARGE_PNG_SHA,
}
EXPECTED_IDS = {
    "PREFAB_ABCL_TO004_TOXICOLOGY_SMALL": ("8", "6", "ASSET_ABCL_TO004_PREFAB_ICON_SMALL"),
    "PREFAB_ABCL_TO004_TOXICOLOGY_LARGE": ("12", "6", "ASSET_ABCL_TO004_PREFAB_ICON_LARGE"),
}

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def check(root: Path) -> dict:
    root = root.resolve()
    if not root.is_dir() or any(p.casefold() in ("streamingassets", "addons") for p in root.parts):
        raise ValueError("Require an immutable checkout, not installed Project Hospital")
    checkout = root.parents[1]
    actual_sha = subprocess.check_output(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual_sha != TO_SHA:
        raise ValueError("Refusing nonapproved TO004 source: " + actual_sha)
    archive = {}
    for name, expected in FILES.items():
        file = root / name
        if not file.is_file() or file.is_symlink():
            raise ValueError("Missing/unsafe frozen file: " + name)
        raw = file.read_bytes()
        h = digest(raw)
        if expected and h != expected:
            raise ValueError("Approved file bytes changed: " + name)
        archive[name] = raw

    for suffix in ("small", "large"):
        raw = archive[f"Assets/ABCL/Prefabs/toxicology_{suffix}.png"]
        if raw[:8] != b"\x89PNG\r\n\x1a\n" or raw[12:16] != b"IHDR" or struct.unpack(">IIBB", raw[16:26]) != (104,104,8,6):
            raise ValueError("Invalid 104x104 RGBA approved preview: " + suffix)

    assets = ET.fromstring(archive["Database/ModAssetListsTO004.xml"]).findall("GameDBAsset")
    if len(assets) != 4:
        raise ValueError("Expected exactly four private TO004 GameDBAsset entries")
    asset_map = {}
    for entry in assets:
        key = entry.get("ID")
        target = entry.findtext("File")
        if not key or not key.startswith("ASSET_ABCL_TO004_") or not target or not target.startswith("MOD_ROOT/"):
            raise ValueError("TO004 asset ID/path not additive")
        if target[9:] not in FILES:
            raise ValueError("Missing private asset target: " + str(target))
        if key in asset_map:
            raise ValueError("Duplicate asset key")
        asset_map[key] = entry.findtext("Type")
    if sorted(asset_map.values()) != sorted(["PREFAB","PREFAB","TEXTURE_CUSTOM_PREFAB_SPRITE","TEXTURE_CUSTOM_PREFAB_SPRITE"]):
        raise ValueError("Unexpected native prefab asset types")

    objects = ET.fromstring(archive["Database/ModPrefabObjectsTO004.xml"]).findall("GameDBPrefabObject")
    if len(objects) != 2 or {o.get("ID") for o in objects} != set(EXPECTED_IDS):
        raise ValueError("Expected only two namespaced toxicology lab prefabs")
    for obj in objects:
        size_x,size_y,icon = EXPECTED_IDS[obj.get("ID")]
        if obj.findtext("DisplayedSizeX") != size_x or obj.findtext("DisplayedSizeY") != size_y:
            raise ValueError("Approved displayed dimensions changed")
        if obj.findtext("CustomIconAssetRef") != icon or obj.findtext("IconIndex") != "-1":
            raise ValueError("Wrong private icon/native menu binding")
        if [t.text for t in obj.findall("Tags/Tag")] != ["ui_prefab_lab"]:
            raise ValueError("Prefab must be additive to native lab menu")
        if obj.findtext("PrefabAssetRef") not in asset_map:
            raise ValueError("No resolved room data resource")
        for flag in ("LayerFloors", "LayerWalls", "LayerDoors", "LayerObjects"):
            if obj.findtext(flag) != "true":
                raise ValueError("Original room layers must be present: " + flag)
    # Never stage original game, Workshop or unrelated ART/clinical assets.
    return {"approved_source_sha":TO_SHA, "files":{name:digest(raw) for name,raw in sorted(archive.items())},
            "g1_required_room_id":"ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB",
            "asset_mode":"eight additive MOD_ROOT resources in existing G1 test addon, no new DLL",
            "owner_visual_approval":True, "native_game_L4":"NOT_RUN"}

def build(to_root: Path, output: Path) -> dict:
    checked = check(to_root)
    output = output.resolve()
    if output.exists():
        raise ValueError("Refusing to replace an existing test artifact")
    output.parent.mkdir(parents=True,exist_ok=True)
    pkg = to_root / "tools/package_to004.py"
    if not pkg.is_file():
        raise ValueError("Approved original TO packager missing")
    subprocess.run([sys.executable,str(pkg),"--source-sha",TO_SHA,"--output",str(output)],check=True)
    with zipfile.ZipFile(output) as z:
        if len(z.namelist()) != len(set(z.namelist())):
            raise ValueError("Duplicate files in TO004 overlay ZIP")
        for name, expected in checked["files"].items():
            if digest(z.read(name)) != expected:
                raise ValueError("Unapproved runtime entry in ZIP: " + name)
        if any(n.startswith(("ModABCLG1LeadTest/","Assembly-CSharp")) or n.endswith(".dll") for n in z.namelist()):
            raise ValueError("Overlay ZIP illegally ships or overwrites game/G1 assemblies")
    checked["overlay_zip_sha256"] = digest(output.read_bytes())
    checked["overlay_bytes"] = output.stat().st_size
    checked["entry_count"] = len(zipfile.ZipFile(output).namelist())
    return checked

if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--to-root",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--manifest",type=Path,required=True)
    opts=ap.parse_args()
    result=build(opts.to_root,opts.output)
    opts.manifest.parent.mkdir(parents=True,exist_ok=True)
    opts.manifest.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))
