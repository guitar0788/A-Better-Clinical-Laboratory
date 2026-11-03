#!/usr/bin/env python3
"""One TEST-ONLY artifact: TO004 prefabs + FA ART001 + TO001 icons/floor + TO002 probe.
No original game DLLs, textures, patient saves or AES material in public artifacts.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import zipfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
FA_SHA="cafcc32d9eb21b1f7e5df39a7f7f443d3ebf1da7"
TO_SHA="eac88c04f6d585e987b921938b76e3a3a4d4d1b0"
TO_FILES=(
 "Database/ModAssetListsTO004.xml",
 "Database/ModPrefabObjectsTO004.xml",
 "Database/ModStringTableEnTO004.xml",
 "Database/ModStringTableZhHansTO004.xml",
 "Prefabs/room_toxicology_small.xml",
 "Prefabs/room_toxicology_large.xml",
 "Assets/ABCL/Prefabs/toxicology_small.png",
 "Assets/ABCL/Prefabs/toxicology_large.png",
)
G1_XML=("ModAddon.xml","ModExaminations.xml","ModRoomTypes.xml",
 "ModStringTableEnABCL.xml","ModStringTableZhHansABCL.xml")
ART_XML=("ModAddon.xml","ModAssetListsABCL.xml","ModObjectsABCL.xml",
 "ModStringTableEnABCLArt001.xml","ModStringTableZhHansABCLArt001.xml",
 "ModColorSets.xml")
ART_PNG=("equipment_atlas.png","icp_ms_icon.png",
 "digestion_station_icon.png","workbench_icon.png")
ROOM_PNG=("toxicology_room_icon.png","toxicology_room_icon_inactive.png")
FLOOR="toxicology_floor_atlas_private_376.png"
ART_ROOT="ModABCLArt001Test/"
G1_ROOT="ModABCLG1LeadTest/"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def load_file(p):
    if not p.is_file() or p.is_symlink(): raise ValueError("Missing/unsafe source: "+str(p))
    return p.read_bytes()

def png_size(data):
    if data[:8]!=b'\x89PNG\r\n\x1a\n' or data[12:16]!=b'IHDR':
        raise ValueError("Expected original RGBA PNG")
    return struct.unpack(">IIBB",data[16:26])

def add(data,rel,source):
    if rel in data: raise ValueError("Duplicate package path: "+rel)
    if rel.startswith("/") or "\\" in rel or ".." in Path(rel).parts:
        raise ValueError("Unsafe package path: "+rel)
    data[rel]=load_file(source)

def assemble(args):
    out=Path(args.output).resolve()
    if out.exists():raise ValueError("Refusing to overwrite an existing test candidate")
    if any(p.casefold() in ("addons","streamingassets") for p in out.parts):
        raise ValueError("Never write directly into installed game directory")
    if len(args.source_sha)!=40 or any(c not in "0123456789abcdef" for c in args.source_sha):
        raise ValueError("Missing exact integration SHA")
    fa,to,art,floor=map(Path,(args.fa_root,args.to_root,args.art_proof,args.floor_proof))
    files={}
    for name in G1_XML:
        add(files,G1_ROOT+"Database/"+name,ROOT/"assets/g1/Database"/name)
    add(files,G1_ROOT+"ModABCLG1LeadTest.dll",Path(args.g1_dll))
    if len(files[G1_ROOT+"ModABCLG1LeadTest.dll"])<5120:
        raise ValueError("Compiled ABCL DLL absent/incomplete")
    files[G1_ROOT+"0Harmony.dll"]=b"" # native loader compatibility placeholder only
    menu=ET.fromstring(load_file(ROOT/"assets/g1/Database/ModAssetListsTO001.xml"))
    ids={x.get("ID") for x in menu.findall("GameDBAsset")}
    if ids!={"ASSET_ABCL_TOXICOLOGY_ROOM_ICON","ASSET_ABCL_TOXICOLOGY_ROOM_ICON_INACTIVE"}:
        raise ValueError("Unexpected existing TO001 asset IDs")
    new=ET.SubElement(menu,"GameDBAsset",ID="ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS")
    ET.SubElement(new,"Type").text="TEXTURE"
    ET.SubElement(new,"File").text="MOD_ROOT/Assets/ABCL/"+FLOOR
    files[G1_ROOT+"Database/ModAssetListsTO001.xml"]=ET.tostring(menu,encoding="utf-8",xml_declaration=True)
    for name in ROOM_PNG:
        add(files,G1_ROOT+"Assets/ABCL/"+name,fa/"assets/art/to001"/name)
        if png_size(files[G1_ROOT+"Assets/ABCL/"+name])!=(64,64,8,6):
            raise ValueError("Room UI sprite must be 64x64 RGBA")
    add(files,G1_ROOT+"Assets/ABCL/"+FLOOR,floor/FLOOR)
    if png_size(files[G1_ROOT+"Assets/ABCL/"+FLOOR])!=(2048,2048,8,6):
        raise ValueError("Private floor atlas must be 2048x2048 RGBA")
    for name in TO_FILES:
        add(files,G1_ROOT+name,to/"assets/to004"/name)
    expected_originals={
       "Prefabs/room_toxicology_small.xml":"1477eb5580e1002c33384f84aaa708dfbe2fb19b09ea01dcd330309295d61457",
       "Prefabs/room_toxicology_large.xml":"4454abe727234fd8f8e6a70bcfff2f58860f05dbf3f8351b99951d7725bbad8d",
    }
    for name,sha in expected_originals.items():
        if digest(files[G1_ROOT+name])!=sha:
            raise ValueError("Owner original TO004 prefab source changed: "+name)
    for name in ART_XML:
        add(files,ART_ROOT+"Database/"+name,art/"Database"/name)
    for name in ART_PNG:
        add(files,ART_ROOT+"Assets/ABCL/"+name,art/"Assets/ABCL"/name)
        if png_size(files[ART_ROOT+"Assets/ABCL/"+name])[2:]!=(8,6):
            raise ValueError("ART001 device PNG not RGBA: "+name)
    # These two addon IDs must remain disjoint; no vanilla ID/asset override.
    for rel in files:
        if rel.lower().endswith((".aes",".pdb",".mdb",".key")) or "Assembly-CSharp" in rel:
            raise ValueError("Prohibited original/private binary: "+rel)
    add(files,"Install-ABCL-G1.ps1",ROOT/"tools/Install-ABCL-G1.ps1")
    add(files,"Install-TOFA-Unified.ps1",ROOT/"tools/Install-TOFA-Unified.ps1")
    add(files,"INSTALL_TOFA_UNIFIED.cmd",ROOT/"tools/INSTALL_TOFA_UNIFIED.cmd")
    add(files,"TOFA_L4_CHECKLIST.txt",ROOT/"tools/TOFA_L4_CHECKLIST.txt")
    manifest={
        "stage":"TO+FA SINGLE SESSION TEST-ONLY / NOT A RELEASE",
        "integration_sha":args.source_sha,"fa_sha":FA_SHA,"to_sha":TO_SHA,
        "native_game_L4":"NOT_RUN","l3_compiled":True,
        "touches_original_game_files":False,
        "dll_sha256":digest(files[G1_ROOT+"ModABCLG1LeadTest.dll"]),
        "entries":{p:digest(d) for p,d in sorted(files.items())}
    }
    files["BUILD_INFO.json"]=(json.dumps(manifest,indent=2)+"\n").encode()
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,"x",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,raw in sorted(files.items()):
            item=zipfile.ZipInfo(name,(2026,11,3,0,0,0))
            item.compress_type=zipfile.ZIP_DEFLATED
            item.external_attr=0o100644<<16
            z.writestr(item,raw)
    with zipfile.ZipFile(out) as z:
        if set(z.namelist())!=set(files) or len(z.namelist())!=len(files):
            raise ValueError("Archive entry inventory mismatch")
        for name,data in files.items():
            if z.read(name)!=data:raise ValueError("ZIP byte mismatch: "+name)
    return {"archive_sha256":digest(out.read_bytes()),"entries":len(files),
            "dll_sha256":manifest["dll_sha256"],
            "integration_sha":args.source_sha,"fa_sha":FA_SHA,"to_sha":TO_SHA}

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for flag in ("g1-dll","fa-root","to-root","art-proof","floor-proof","output","source-sha"):
        p.add_argument("--"+flag,required=True)
    print(json.dumps(assemble(p.parse_args()),indent=2))
