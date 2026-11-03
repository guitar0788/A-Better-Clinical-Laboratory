#!/usr/bin/env python3
"""Stage exact owner-approved TO-001 room and isometric floor artwork, source-only.

It consumes FA's immutable Git commit, checks the approved asset hashes and
builds a private 16 x 32 transparent atlas. It NEVER edits the G1 clinical
code, any owner-approved art, vanilla game files, or third-party addons.
The output is NOT an installable Mod or a game L4 claim.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import xml.etree.ElementTree as ET

FA_COMMIT = "d56b89962c0664fb37fc39113caed92892a335cc"
APPROVED_ROOM_SVG_BLOB = "c4a81670a2b0004799513c5b03a61b9239af1f5b"
APPROVED_ROOM_PNG_BLOB = "149bc34ebe68194d13054d91564c28700b5311ab"
APPROVED_FLOOR_SVG_SHA256 = "76995aef9bb3eb851c28101d0b75200552bc85e91dc28247ebd0e786e6cab4ec"
APPROVED_FLOOR_PNG_SHA256 = "7c0d03ddbd370aca4ddd1a089ff91d814e1c2622659a3d300d844bd9713a8cb4"
ROOM_ID = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB"
ATLAS_ID = "ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS"
ATLAS_NAME = "toxicology_floor_atlas_private_376.png"
ATLAS_SIZE = (2048, 2048)
CELL_SIZE = (128, 64)
TILE_ID = 376
TILE_COLUMNS = 16
TILE_ROWS = 32
ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ORIGINAL_ASSETS = {
    "ASSET_ABCL_TOXICOLOGY_ROOM_ICON": "toxicology_room_icon.png",
    "ASSET_ABCL_TOXICOLOGY_ROOM_ICON_INACTIVE": "toxicology_room_icon_inactive.png",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blobsha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def png_size_rgba(data: bytes, width: int, height: int) -> None:
    if (data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR"
        or struct.unpack(">IIBB", data[16:26]) != (width, height, 8, 6)):
        raise ValueError("Approved image must be exact native-size RGBA PNG")


def stage(fa_root: Path, output: Path) -> dict:
    from PIL import Image

    fa_root = fa_root.resolve(strict=True)
    output = output.resolve()
    if output.exists():
        raise FileExistsError("Refuse overwriting previous art stage or installed game files")
    if any(p.lower() in {"addons", "streamingassets", "projecthospital_data"}
           for p in output.parts):
        raise ValueError("Do not create staged resources under the live game")
    if subprocess.check_output(
        ["git", "-C", str(fa_root), "rev-parse", "HEAD"], text=True
    ).strip() != FA_COMMIT:
        raise ValueError("FA checkout is not the frozen approved commit")

    art = fa_root / "assets" / "art" / "to001"
    data = {}
    for name in ("toxicology_room_icon.svg",
                 "toxicology_room_icon.png",
                 "toxicology_room_icon_inactive.png",
                 "toxicology_floor_from_approved_256x128.svg",
                 "toxicology_floor_from_approved_128x64.png"):
        path = art / name
        if not path.is_file() or path.is_symlink():
            raise ValueError("Missing/unsafe frozen source: " + name)
        data[name] = path.read_bytes()

    if blobsha(data["toxicology_room_icon.svg"]) != APPROVED_ROOM_SVG_BLOB:
        raise ValueError("Approved room glyph source changed")
    for name in ("toxicology_room_icon.png", "toxicology_room_icon_inactive.png"):
        if blobsha(data[name]) != APPROVED_ROOM_PNG_BLOB:
            raise ValueError("Approved native room icon PNG changed: " + name)
        png_size_rgba(data[name], 64, 64)
    if sha256(data["toxicology_floor_from_approved_256x128.svg"]) != APPROVED_FLOOR_SVG_SHA256:
        raise ValueError("Approved floor projection source changed")
    floor_data = data["toxicology_floor_from_approved_128x64.png"]
    if sha256(floor_data) != APPROVED_FLOOR_PNG_SHA256:
        raise ValueError("Approved floor PNG has changed")
    png_size_rgba(floor_data, *CELL_SIZE)

    # Preserve FA's own structural vector check. A mere hash-equivalent image
    # does not grant permission to redraw the approved room glyph.
    import importlib.util
    validator = fa_root / "tools" / "export_to001_floor_from_approved.py"
    spec = importlib.util.spec_from_file_location("approved_floor_export", validator)
    if spec is None or spec.loader is None:
        raise ValueError("Approved source verifier is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.verify_vector(art / "toxicology_room_icon.svg",
                         art / "toxicology_floor_from_approved_256x128.svg")

    base = ET.parse(ROOT / "assets/g1/Database/ModAssetListsTO001.xml").getroot()
    existing = {e.get("ID"): e for e in base.findall("GameDBAsset")}
    if set(existing) != set(EXPECTED_ORIGINAL_ASSETS):
        raise ValueError("Original private TO-001 menu asset IDs changed")
    for asset_id, name in EXPECTED_ORIGINAL_ASSETS.items():
        e = existing[asset_id]
        if (e.findtext("Type") != "TEXTURE_CUSTOM_SPRITE"
            or e.findtext("File") != "MOD_ROOT/Assets/ABCL/" + name):
            raise ValueError("Native room icon asset declaration changed")

    # These are separate game UI assets: never use the 64x64 menu Sprite as
    # a floor Texture, never globally replace the original 376/377/378 atlas.
    e = ET.SubElement(base, "GameDBAsset", ID=ATLAS_ID)
    ET.SubElement(e, "Type").text = "TEXTURE"
    ET.SubElement(e, "File").text = "MOD_ROOT/Assets/ABCL/" + ATLAS_NAME

    with Image.open(art / "toxicology_floor_from_approved_128x64.png") as original:
        floor = original.convert("RGBA")
    if floor.size != CELL_SIZE or floor.getbbox() is None:
        raise ValueError("Approved native floor tile missing/empty")
    atlas = Image.new("RGBA", ATLAS_SIZE, (0, 0, 0, 0))
    col, row_from_top = TILE_ID % TILE_COLUMNS, TILE_ID // TILE_COLUMNS
    x, y = col * CELL_SIZE[0], row_from_top * CELL_SIZE[1]
    atlas.paste(floor, (x, y))
    # This is a private isolated atlas, never the original floor texture.
    # A bounding box must reside exclusively in tile 376.
    bbox = atlas.getbbox()
    if (bbox is None or bbox[0] < x or bbox[1] < y
        or bbox[2] > x + CELL_SIZE[0] or bbox[3] > y + CELL_SIZE[1]):
        raise ValueError("Private glyph leaked into a native neighboring tile")

    output.mkdir(parents=True)
    db_dir = output / "Database"
    images_dir = output / "Assets" / "ABCL"
    db_dir.mkdir()
    images_dir.mkdir(parents=True)
    (db_dir / "ModAssetListsTO001.xml").write_bytes(
        ET.tostring(base, encoding="utf-8", xml_declaration=True))
    for filename in EXPECTED_ORIGINAL_ASSETS.values():
        (images_dir / filename).write_bytes(data[filename])
    atlas.save(images_dir / ATLAS_NAME, format="PNG")
    png_size_rgba((images_dir / ATLAS_NAME).read_bytes(), *ATLAS_SIZE)
    manifest = {
        "stage": "SOURCE_ONLY / FA VISUAL APPROVED / TS NATIVE L4 NOT_RUN",
        "fa_source_sha": FA_COMMIT,
        "room_glyph_git_blob": APPROVED_ROOM_SVG_BLOB,
        "approved_private_floor_png_sha256": APPROVED_FLOOR_PNG_SHA256,
        "atlas_tile_id": TILE_ID,
        "tile_col": col,
        "tile_row_top": row_from_top,
        "tile_rect_top_origin": [x, y, *CELL_SIZE],
        "room_id_unchanged": ROOM_ID,
        "files_sha256": {
            str(p.relative_to(output)).replace("\\", "/"): sha256(p.read_bytes())
            for p in sorted(output.rglob("*")) if p.is_file()
        },
        "original_base_game_assets_included": False,
        "G1_patient_or_diagnosis_modified": False,
        "native_game_L4": "NOT_RUN",
    }
    (output / "TO001_STAGE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fa-root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    print(json.dumps(stage(args.fa_root, args.output), indent=2))


if __name__ == "__main__":
    main()
