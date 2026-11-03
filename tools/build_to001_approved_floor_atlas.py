#!/usr/bin/env python3
"""Build a non-installable private 16x32 atlas from approved TO-001 floor art."""
import argparse, hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOM_ID = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB"
ASSET_ID = "ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS"
SOURCE_SHA = "7c0d03ddbd370aca4ddd1a089ff91d814e1c2622659a3d300d844bd9713a8cb4"
VECTOR_SHA = "76995aef9bb3eb851c28101d0b75200552bc85e91dc28247ebd0e786e6cab4ec"
ROOM_BLOB = "c4a81670a2b0004799513c5b03a61b9239af1f5b"
ATLAS_SHA = "00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd"
COLUMNS, ROWS, TILE = 16, 32, 376
CELL_W, CELL_H = 128, 64
ATLAS_W, ATLAS_H = 2048, 2048
RECT = (TILE % COLUMNS * CELL_W, TILE // COLUMNS * CELL_H,
        (TILE % COLUMNS + 1) * CELL_W, (TILE // COLUMNS + 1) * CELL_H)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def build(root, output):
    from PIL import Image, ImageDraw
    root = Path(root).resolve()
    art = (root / "assets/art/to001/toxicology_floor_from_approved_128x64.png").read_bytes()
    vector = (root / "assets/art/to001/toxicology_floor_from_approved_256x128.svg").read_bytes()
    room = (root / "assets/art/to001/toxicology_room_icon.svg").read_bytes()
    if sha(art) != SOURCE_SHA or sha(vector) != VECTOR_SHA:
        raise ValueError("Not the owner-approved projected floor source")
    git_blob = hashlib.sha1(b"blob " + str(len(room)).encode() + b"\x00" + room).hexdigest()
    if git_blob != ROOM_BLOB:
        raise ValueError("Approved room icon was modified")
    from io import BytesIO
    with Image.open(BytesIO(art)) as img:
        tile = img.convert("RGBA")
    if tile.size != (CELL_W, CELL_H) or not tile.getbbox():
        raise ValueError("Invalid private tile")
    for r,g,b,a in tile.getdata():
        # Ignore subvisible RGB fringing from Lanczos; preserve source pixels.
        if a and (max(r,g,b)-min(r,g,b) > 1 or (a >= 16 and min(r,g,b) < 228)):
            raise ValueError("Zone tint/background embedded in floor art")
    atlas = Image.new("RGBA", (ATLAS_W, ATLAS_H), (0,0,0,0))
    atlas.paste(tile, RECT[:2])
    if atlas.crop(RECT).tobytes() != tile.tobytes():
        raise ValueError("Tile 376 changed")
    outside = atlas.getchannel("A")
    ImageDraw.Draw(outside).rectangle((RECT[0],RECT[1],RECT[2]-1,RECT[3]-1),fill=0)
    if outside.getbbox() is not None:
        raise ValueError("Non-transparent pixels outside tile 376")
    output = Path(output).resolve()
    if any(s.lower() in ("streamingassets","addons") for s in output.parts):
        raise ValueError("Refusing to write inside the game installation")
    output.mkdir(parents=True, exist_ok=True)
    out = output/"toxicology_floor_tile_atlas.png"
    atlas.save(out)
    if sha(out.read_bytes()) != ATLAS_SHA:
        raise ValueError("Non-reproducible private atlas output")
    manifest = {
        "gate":"FA_L2_SOURCE_ONLY","target_room":ROOM_ID,"asset_id_for_TS":ASSET_ID,
        "grid":[COLUMNS,ROWS],"atlas_size":[ATLAS_W,ATLAS_H],
        "tile_index":TILE,"tile_rect":list(RECT),
        "source_sha256":SOURCE_SHA,"floor_vector_sha256":VECTOR_SHA,
        "room_git_blob":ROOM_BLOB,"atlas_sha256":ATLAS_SHA,
        "no_other_nontransparent_tiles":True,"no_baked_zone_color":True,
        "game_db_registered":False,"installable":False,"L3":False,"L4":False
    }
    (output/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print("FA L2 PASS: approved tile 376; atlas SHA256 "+ATLAS_SHA)
    return manifest

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    build(a.root,a.output)
