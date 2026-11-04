#!/usr/bin/env python3
"""Fail-closed ABCL integrated package audit: owner art + independent equipment.

This is an offline packaging (L2) gate only. Never opens the installed game,
rewrites PNG artwork, touches saves, or pretends to verify Windows L3/game L4.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import struct
import xml.etree.ElementTree as ET
import zipfile

G1 = "ModABCLG1LeadTest/"
ART = "ModABCLArt001Test/"
APPROVED = {
    G1+"Assets/ABCL/toxicology_room_icon.png":
        "c2c6c83cb0f8c2ca49dce7184bdd4f71df1c71a20ecf0c38e05337df6a48f62b",
    G1+"Assets/ABCL/toxicology_room_icon_inactive.png":
        "eb37ce261299f7df2ac87c61272168f71b5faca5de1578b71a172a8d75e861eb",
    G1+"Assets/ABCL/toxicology_floor_atlas_private_376.png":
        "00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd",
    G1+"Assets/ABCL/Prefabs/toxicology_small.png":
        "a0ec4ea41b5d96d4b755c5d244700548a6a2485d6a1d3e1bef73d8dcf09a0847",
    G1+"Assets/ABCL/Prefabs/toxicology_large.png":
        "3461bf9bbb8476d79e869d98f718b887a32ea88f5b0b158f185abc9f6cf85947",
    ART+"Assets/ABCL/equipment_atlas.png":
        "b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651",
    G1+"Prefabs/room_toxicology_small.xml":
        "ec3be4046d90c219d28143ffd838712fc8030b3a84a05e80a4b8e65ec0141b1d",
    G1+"Prefabs/room_toxicology_large.xml":
        "7d5c559cc60211ea37b42026c8066fbff98865be88d76ef8730350f3ac81b54d",
}
DEVICES = {
    "OBJECT_ABCL_ART001_ICP_MS": (0, 1, 2, 3),
    "OBJECT_ABCL_ART001_DIGESTION": (4, 5, 6, 7),
}
PROTECTED_VANILLA_IDS = {"hematoanalyzer", "RIA", "lab_analyzer", "ui_hematoanalyzer", "ui_ria"}
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HARMONY1_SHA="e271d22a7c32bfca105d0e471c04eee14eec6142d37a30cd73cb7d32c7d1dd0f"


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def png_shape(data):
    require(data.startswith(b"\x89PNG\r\n\x1a\n") and data[12:16] == b"IHDR",
            "Invalid owner-supplied PNG")
    return struct.unpack(">IIBB", data[16:26])


def verify_device_xml(raw):
    root = ET.fromstring(raw)
    require(root.tag == "Database", "Invalid ART GameDB root")
    objects = root.findall("GameDBObject")
    actual = {o.get("ID"): o for o in objects}
    require(len(objects) == 2 and set(actual) == set(DEVICES),
            "REJECTED_ART: old three-object workbench or unknown equipment ID")
    for name, expected_slots in DEVICES.items():
        obj = actual[name]
        require(obj.findtext("AttachedToObject") == "false" and
                obj.findtext("Placement") == "INDOORS",
                "REJECTED_ART: equipment is not independent floor-standing: " + name)
        require(obj.findtext("TextureRef") == "ASSET_TEX_ABCL_ART001_EQUIPMENT"
                and obj.findtext("TextureAtlasLayout") == "LAYOUT_16_X_8"
                and obj.findtext("SpriteShape") == "SHAPE_1_X_1",
                "REJECTED_ART: private atlas / object footprint changed: " + name)
        slots = tuple(int(obj.findtext("TextureID" + d, "-1"))
                      for d in ("NW", "NE", "SE", "SW"))
        require(slots == expected_slots,
                "REJECTED_ART: rotated device slots changed: " + name)
        tags = {t.text for t in obj.findall("./Tags/Tag")}
        require(not (tags & PROTECTED_VANILLA_IDS),
                "REJECTED_ART: equipment impersonates a vanilla clinical tag")
        require(obj.find("AttachmentSlot") is None and obj.find("AccessPositions") is not None,
                "REJECTED_ART: obsolete attachment/device-access XML")


def verify_package(path, expected_source_sha, expected_dll_sha):
    require(HEX40.fullmatch(expected_source_sha or "") is not None,
            "Missing independently verified compiled C# source SHA")
    require(HEX64.fullmatch(expected_dll_sha or "") is not None,
            "Missing independently verified net35 DLL SHA-256")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "Duplicate ZIP names")
        for name in names:
            p = PurePosixPath(name)
            require(not name.startswith("/") and "\\" not in name and
                    ".." not in p.parts and not name.endswith("/"),
                    "Unsafe ZIP entry " + name)
            require(name.startswith((G1, ART)) or name in {
                "BUILD_INFO.json", "Install-TOFA-Unified.ps1", "Install-ABCL-G1.ps1",
                "INSTALL_TOFA_UNIFIED.cmd", "RESTORE_TOFA_PREVIOUS.cmd",
                "INSTALL_ABCL_FULL_TEST.cmd", "TOFA_L4_CHECKLIST.txt",
                "README_FIRST_CN.txt"},
                "Unexpected original/third-party game path " + name)
        require(G1+"0Harmony.dll" in names,
                "REJECTED_CODE_LOADER: original game skips C# addon without 0Harmony.dll")
        harmony=archive.read(G1+"0Harmony.dll")
        require(len(harmony)==113152 and harmony[:2]==b'MZ' and
                b'BSJB' in harmony and b'HarmonyInstance' in harmony and
                sha(harmony)==HARMONY1_SHA,
                "REJECTED_CODE_LOADER: requires genuine official Harmony1 net35")
        require(G1+"THIRD_PARTY_HARMONY1_MIT_LICENSE.txt" in names,
                "REJECTED_CODE_LOADER: missing MIT license")
        require(not any("workbench" in n.lower() or n.endswith("ModColorSets.xml")
                        for n in names),
                "REJECTED_ART: old workbench assets/color set remain")
        require(G1+"ModABCLG1LeadTest.dll" in names,
                "Compiled G1 DLL missing")
        dll = archive.read(G1+"ModABCLG1LeadTest.dll")
        require(len(dll) >= 5120 and sha(dll) == expected_dll_sha,
                "REJECTED_BINARY: DLL hash not equal to independently verified L3 artifact")
        require("BUILD_INFO.json" in names, "Missing pinned BUILD_INFO.json")
        manifest = json.loads(archive.read("BUILD_INFO.json"))
        require(manifest.get("compiled_g1_source_sha") == expected_source_sha,
                "REJECTED_BINARY: no exact compiled source SHA binding")
        require(manifest.get("dll_sha256") == expected_dll_sha,
                "REJECTED_BINARY: manifest DLL SHA differs from verified L3")
        require(manifest.get("native_game_L4") == "NOT_RUN",
                "L4 cannot be marked PASS by packaging code")
        require(isinstance(manifest.get("entries"), dict),
                "Missing SHA manifest")
        for key, expected in APPROVED.items():
            require(key in names, "Missing APPROVED asset: " + key)
            require(sha(archive.read(key)) == expected,
                    "REJECTED_ART: owner-approved bytes were changed/reverted: " + key)
        dims = {
            G1+"Assets/ABCL/toxicology_room_icon.png": (64, 64, 8, 6),
            G1+"Assets/ABCL/toxicology_room_icon_inactive.png": (64, 64, 8, 6),
            G1+"Assets/ABCL/toxicology_floor_atlas_private_376.png": (2048, 2048, 8, 6),
            G1+"Assets/ABCL/Prefabs/toxicology_small.png": (104, 104, 8, 6),
            G1+"Assets/ABCL/Prefabs/toxicology_large.png": (104, 104, 8, 6),
            ART+"Assets/ABCL/equipment_atlas.png": (2048, 1024, 8, 6),
        }
        for key, size in dims.items():
            require(png_shape(archive.read(key)) == size,
                    "REJECTED_ART: wrong owner-approved PNG dimensions: " + key)
        verify_device_xml(archive.read(ART+"Database/ModObjectsABCL.xml"))
        require(ART+"Database/ModAddon.xml" in names,
                "Independent ART addon identity missing")
        room = ET.fromstring(archive.read(G1+"Database/ModRoomTypes.xml"))
        room = room.find("./GameDBRoomType[@ID='ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB']")
        require(room is not None and room.findtext("TextureID") == "376",
                "REJECTED_ROOM: mismatched native floor tile index")
        asset_db = ET.fromstring(archive.read(G1+"Database/ModAssetListsTO001.xml"))
        assets = {a.get("ID"): a.findtext("File") for a in asset_db.findall("GameDBAsset")}
        for aid, relative in {
            "ASSET_ABCL_TOXICOLOGY_ROOM_ICON": "toxicology_room_icon.png",
            "ASSET_ABCL_TOXICOLOGY_ROOM_ICON_INACTIVE": "toxicology_room_icon_inactive.png",
            "ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS": "toxicology_floor_atlas_private_376.png",
        }.items():
            require(assets.get(aid) == "MOD_ROOT/Assets/ABCL/" + relative,
                    "REJECTED_BINDING: private UI/floor GameDBAsset path is wrong")
        for xml_name in (G1+"Database/ModPrefabObjectsTO004.xml",
                         G1+"Database/ModAssetListsTO004.xml"):
            require(xml_name in names, "Missing TO-004 prefab registration " + xml_name)
            ET.fromstring(archive.read(xml_name))
        for name, digest in manifest["entries"].items():
            require(name in names and sha(archive.read(name)) == digest,
                    "REJECTED_PACKAGE: manifest mismatch " + name)
        require(set(manifest["entries"]) == set(names) - {"BUILD_INFO.json"},
                "REJECTED_PACKAGE: untracked or missing file")
        return {"result": "L2_PACKAGE_CONTRACT_PASS_L4_NOT_RUN",
                "package_sha256": sha(Path(path).read_bytes()),
                "compiled_g1_source_sha": expected_source_sha,
                "compiled_g1_dll_sha256": expected_dll_sha,
                "approved_assets_pinned": len(APPROVED),
                "devices": len(DEVICES), "entries": len(names)}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--package", type=Path, required=True)
    p.add_argument("--compiled-source-sha", required=True)
    p.add_argument("--compiled-dll-sha256", required=True)
    a = p.parse_args()
    print(json.dumps(verify_package(a.package, a.compiled_source_sha,
                                    a.compiled_dll_sha256), indent=2))
