#!/usr/bin/env python3
"""Compose a disposable TO-001 UI L4 package from a verified G1 Windows L3 artifact.

No game binaries are read. Never edits installed Project Hospital files.
The protected-main G1 compiler workflow is intentionally not changed.
"""
import argparse
import hashlib
import io
from pathlib import Path
import re
import struct
import zipfile
import xml.etree.ElementTree as ET
import zlib

ROOT = Path(__file__).resolve().parents[1]
ADDON = "ModABCLG1LeadTest"
XML = ROOT / "assets/g1/Database/ModAssetListsTO001.xml"
ART = ROOT / "assets/g1/Assets/ABCL"
ART_HASHES = {
    "toxicology_room_icon.png": "acb0042bb006f1f6a85c5b099f1c311ac5268b19944206cb1003b96a7930cb8a",
    "toxicology_room_icon_inactive.png": "acb0042bb006f1f6a85c5b099f1c311ac5268b19944206cb1003b96a7930cb8a",
}
FLOOR_TILE = ROOT / "assets/g1/Source/TO001/toxicology_floor_from_approved_128x64.png"
FLOOR_TILE_SHA256 = "7c0d03ddbd370aca4ddd1a089ff91d814e1c2622659a3d300d844bd9713a8cb4"
FLOOR_ATLAS_NAME = "toxicology_floor_atlas_private_376.png"
PRECISE_BASE_FILES = {
    ADDON + "/0Harmony.dll", ADDON + "/ModABCLG1LeadTest.dll",
    *{ADDON + "/Database/" + x for x in (
        "ModAddon.xml", "ModExaminations.xml", "ModRoomTypes.xml",
        "ModStringTableEnABCL.xml", "ModStringTableZhHansABCL.xml")},
    "G1_TEST_README.txt", "INSTALL_G1_R3.cmd", "Install-ABCL-G1.ps1",
}


def sha256(data):
    return hashlib.sha256(data).hexdigest()

def decode_png_rgba(data):
    """Decode a non-interlaced 8-bit RGBA PNG using only the standard library."""
    signature = b"\x89PNG\r\n\x1a\n"
    if not data.startswith(signature):
        raise ValueError("Not a PNG")
    offset = len(signature)
    width = height = bit_depth = color_type = None
    idat = []
    saw_end = False
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError("Truncated PNG chunk")
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        start = offset + 8
        end = start + length
        if end + 4 > len(data):
            raise ValueError("Truncated PNG payload")
        payload = data[start:end]
        expected_crc = struct.unpack(">I", data[end:end + 4])[0]
        if (zlib.crc32(kind + payload) & 0xffffffff) != expected_crc:
            raise ValueError("PNG CRC mismatch")
        if kind == b"IHDR":
            width, height, bit_depth, color_type, compression, filt, interlace = struct.unpack(
                ">IIBBBBB", payload)
            if bit_depth != 8 or color_type != 6 or compression != 0 or filt != 0 or interlace != 0:
                raise ValueError("Expected non-interlaced 8-bit RGBA PNG")
        elif kind == b"IDAT":
            idat.append(payload)
        elif kind == b"IEND":
            saw_end = True
            break
        offset = end + 4
    if not saw_end or not width or not height:
        raise ValueError("PNG is missing IHDR/IEND")
    stride = width * 4
    raw = zlib.decompress(b"".join(idat))
    if len(raw) != height * (stride + 1):
        raise ValueError("Unexpected PNG decompressed length")
    pixels = bytearray(height * stride)
    previous = bytearray(stride)
    pos = 0
    for y in range(height):
        filter_type = raw[pos]
        scan = raw[pos + 1:pos + 1 + stride]
        pos += stride + 1
        row = bytearray(stride)
        for i, value in enumerate(scan):
            left = row[i - 4] if i >= 4 else 0
            up = previous[i]
            upper_left = previous[i - 4] if i >= 4 else 0
            if filter_type == 0:
                predictor = 0
            elif filter_type == 1:
                predictor = left
            elif filter_type == 2:
                predictor = up
            elif filter_type == 3:
                predictor = (left + up) // 2
            elif filter_type == 4:
                p = left + up - upper_left
                pa, pb, pc = abs(p - left), abs(p - up), abs(p - upper_left)
                predictor = left if pa <= pb and pa <= pc else up if pb <= pc else upper_left
            else:
                raise ValueError("Unsupported PNG filter")
            row[i] = (value + predictor) & 0xff
        pixels[y * stride:(y + 1) * stride] = row
        previous = row
    return width, height, bytes(pixels)


def encode_png_rgba(width, height, pixels):
    """Encode RGBA PNG with filter 0 and deterministic standard-library zlib."""
    stride = width * 4
    if width <= 0 or height <= 0 or len(pixels) != height * stride:
        raise ValueError("Invalid RGBA image buffer")
    raw = b"".join(b"\x00" + pixels[y * stride:(y + 1) * stride]
                   for y in range(height))
    def chunk(kind, payload):
        return (struct.pack(">I", len(payload)) + kind + payload
                + struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))




def verify_archive(z, expected):
    names = z.namelist()
    if len(names) != len(set(names)) or set(names) != expected:
        raise ValueError("Unexpected/missing package entries or duplicate names")
    for name in names:
        if name.startswith("/") or "\\" in name or ".." in Path(name).parts:
            raise ValueError("Unsafe ZIP path: " + name)
        if name.casefold().endswith((".aes", ".pdb", ".mdb")):
            raise ValueError("Forbidden file: " + name)
        if name.casefold().endswith(".dll") and name not in {
            ADDON + "/0Harmony.dll", ADDON + "/ModABCLG1LeadTest.dll"
        }:
            raise ValueError("Non-ABCL DLL in ZIP: " + name)
    if z.read(ADDON + "/0Harmony.dll"):
        raise ValueError("Harmony placeholder must stay empty")


def create(outer_path, expected_sha, output_path):
    if not re.fullmatch("[a-f0-9]{40}", expected_sha):
        raise ValueError("Expected exact forty-character Git commit SHA")
    if output_path.exists():
        raise ValueError("Output exists: refuse in-place overwrite")
    if any(p.lower() in {"streamingassets", "addons"} for p in output_path.resolve().parts):
        raise ValueError("Refuse writing into installed game directories")
    with zipfile.ZipFile(outer_path) as outer:
        if set(outer.namelist()) != {"ABCL_G1_AutoBuilt_TestOnly.zip", "BUILD_INFO.txt"}:
            raise ValueError("Wrong workflow artifact; need two-member G1 Windows L3 ZIP")
        info = outer.read("BUILD_INFO.txt").decode("utf-8-sig")
        match = re.search(r"(?m)^CANDIDATE_SHA=([a-f0-9]{40})\s*$", info)
        hash_match = re.search(r"(?m)^DLL_SHA256=([A-Fa-f0-9]{64})\s*$", info)
        if not match or match.group(1) != expected_sha or not hash_match:
            raise ValueError("G1 candidate SHA or DLL digest not verified")
        original_inner = outer.read("ABCL_G1_AutoBuilt_TestOnly.zip")
    with zipfile.ZipFile(io.BytesIO(original_inner)) as base:
        verify_archive(base, PRECISE_BASE_FILES)
        expected_dll = hash_match.group(1).lower()
        dll_bytes = base.read(ADDON + "/ModABCLG1LeadTest.dll")
        if sha256(dll_bytes) != expected_dll or len(dll_bytes) < 5120:
            raise ValueError("Compiled G1 DLL digest/size mismatch")
        entries = {name: base.read(name) for name in PRECISE_BASE_FILES}
    xml = XML.read_bytes()
    parsed = ET.fromstring(xml)
    assets = {e.attrib.get("ID"): e for e in parsed.findall("GameDBAsset")}
    expected_assets = {
        "ASSET_ABCL_TOXICOLOGY_ROOM_ICON": ("TEXTURE_CUSTOM_SPRITE", "toxicology_room_icon.png"),
        "ASSET_ABCL_TOXICOLOGY_ROOM_ICON_INACTIVE": ("TEXTURE_CUSTOM_SPRITE", "toxicology_room_icon_inactive.png"),
        "ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS": ("TEXTURE", FLOOR_ATLAS_NAME),
    }
    if set(assets) != set(expected_assets):
        raise ValueError("Expected exactly two approved menu sprites and one private floor atlas")
    for asset_id, (asset_type, filename) in expected_assets.items():
        entry = assets[asset_id]
        if entry.findtext("Type") != asset_type or entry.findtext("File") != "MOD_ROOT/Assets/ABCL/" + filename:
            raise ValueError("TO001 GameDBAsset declaration mismatch: " + asset_id)
    new_entries = {ADDON + "/Database/ModAssetListsTO001.xml": xml}
    for name, expected_hash in ART_HASHES.items():
        raw = (ART / name).read_bytes()
        if sha256(raw) != expected_hash:
            raise ValueError("FA approved room icon SHA256 mismatch for " + name)
        if (raw[:8] != b"\x89PNG\r\n\x1a\n" or raw[12:16] != b"IHDR"
                or struct.unpack(">IIBB", raw[16:26]) != (64, 64, 8, 6)):
            raise ValueError("Not the approved 64x64 RGBA sprite: " + name)
        new_entries[ADDON + "/Assets/ABCL/" + name] = raw

    floor_raw = FLOOR_TILE.read_bytes()
    if sha256(floor_raw) != FLOOR_TILE_SHA256:
        raise ValueError("FA approved isometric floor tile SHA256 mismatch")
    if (floor_raw[:8] != b"\x89PNG\r\n\x1a\n" or floor_raw[12:16] != b"IHDR"
            or struct.unpack(">IIBB", floor_raw[16:26]) != (128, 64, 8, 6)):
        raise ValueError("Approved floor tile must be 128x64 RGBA")
    tile_width, tile_height, floor_pixels = decode_png_rgba(floor_raw)
    if (tile_width, tile_height) != (128, 64) or not any(floor_pixels[i + 3] for i in range(0, len(floor_pixels), 4)):
        raise ValueError("Approved floor tile must be non-empty 128x64 RGBA")
    atlas_pixels = bytearray(2048 * 2048 * 4)
    for y in range(64):
        source_start = y * 128 * 4
        target_start = ((1472 + y) * 2048 + 1024) * 4
        atlas_pixels[target_start:target_start + 128 * 4] = floor_pixels[source_start:source_start + 128 * 4]
    atlas_raw = encode_png_rgba(2048, 2048, bytes(atlas_pixels))
    atlas_width, atlas_height, check_pixels = decode_png_rgba(atlas_raw)
    if (atlas_width, atlas_height) != (2048, 2048):
        raise ValueError("Private floor atlas dimensions invalid")
    for y in range(64):
        source_start = y * 128 * 4
        target_start = ((1472 + y) * 2048 + 1024) * 4
        if check_pixels[target_start:target_start + 128 * 4] != floor_pixels[source_start:source_start + 128 * 4]:
            raise ValueError("Private atlas tile 376 does not match approved FA PNG")
    # The atlas buffer was initialized to transparent zeros and only tile 376
    # was copied; no original floor pixels or adjacent tiles can be present.
    new_entries[ADDON + "/Assets/ABCL/" + FLOOR_ATLAS_NAME] = atlas_raw
    readme = (
        "TO-001 / G1 TEST ONLY. Source SHA: " + expected_sha + "\n"
        "Install only in a disposable save with the existing G1 test installer.\n"
        "Open Hospital Management -> Laboratory -> Toxicology Laboratory.\n"
        "Check native-red room icon, gray locked state, hover and menu reopen.\n"
        "Compare original hematology, histology, microbiology and DLC icons.\n"
        "Verify the approved floor tile renders and native room/area overlay colors and CBC remain unchanged.\n"
        "Do NOT click the patient spawn button; no Alpha release.\n"
    )
    new_entries["TO001_TEST_README.txt"] = readme.encode()
    with io.BytesIO() as stream:
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as dest:
            for name, data in sorted({**entries, **new_entries}.items()):
                dest.writestr(name, data)
        package = stream.getvalue()
    with zipfile.ZipFile(io.BytesIO(package)) as check:
        verify_archive(check, set(entries) | set(new_entries))
    manifest = (
        info.rstrip() + "\n"
        "TO001_SOURCE=FA approved room sprites plus direct isometric floor projection\n"
        "TO001_ROOM_ICON_SHA256=" + ART_HASHES["toxicology_room_icon.png"] + "\n"
        "TO001_FLOOR_TILE_SHA256=" + FLOOR_TILE_SHA256 + "\n"
        "TO001_FLOOR_ATLAS_SHA256=" + sha256(atlas_raw) + "\n"
        "TO001_PACKAGE_SHA256=" + sha256(package) + "\n"
        "TO001_RUNTIME_L4=NOT_RUN\n"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as outer:
        outer.writestr("ABCL_G1_TO001_Install_TestOnly.zip", package)
        outer.writestr("BUILD_INFO.txt", manifest)
    print("TO-001 OFFLINE PACKAGE VERIFIED; NO GAMEPLAY L4 CLAIM")
    print("SOURCE_SHA=" + expected_sha)
    print("DLL_SHA256=" + expected_dll)
    print("INNER_PACKAGE_SHA256=" + sha256(package))
    print("OUTER_PACKAGE_SHA256=" + sha256(output_path.read_bytes()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--compiled-artifact", required=True, type=Path)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    create(args.compiled_artifact, args.source_sha, args.output)
