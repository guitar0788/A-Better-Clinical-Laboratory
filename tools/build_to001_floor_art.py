#!/usr/bin/env python3
"""TO-001: derive floor art from the EXISTING original room-menu SVG.

The vanilla game has separate atlas paths but consistent icon motifs.
This FA tool never draws an additional floor glyph, detached badge or sensor.
Review-only source L2, no runtime registration/installation.
"""
import argparse,copy,hashlib,io,json
from pathlib import Path
from xml.etree import ElementTree as ET
import cairosvg
from PIL import Image,ImageDraw,ImageFont

NS="{http://www.w3.org/2000/svg}"
RECT=(1024,1472,1152,1536)
SIZE=(128,64)
# 64x64 room icon to 128x64 private floor tile, isometric projection only.
MATRIX=(2.4,-0.32,0.7,1.02,-35.2,9.6)

def build(room_svg,out):
    out=Path(out).resolve()
    if any(p.lower() in ("streamingassets","addons") for p in out.parts):
        raise ValueError("Refuse writing in original game folders")
    raw=Path(room_svg).read_bytes()
    if any(v in raw.lower() for v in (b"<script",b"<image",b"<use",b"href=",b"url(",b"javascript:")):
        raise ValueError("Unsafe SVG input")
    root=ET.fromstring(raw)
    if root.tag!=NS+"svg" or root.get("viewBox")!="0 0 64 64":
        raise ValueError("Must use the exact original 64px room SVG")
    source_groups=[e for e in root if e.tag==NS+"g"]
    if not source_groups: raise ValueError("Room icon has no drawable vector groups")
    target=ET.Element(NS+"svg",{"viewBox":"0 0 128 64","width":"128","height":"64"})
    ET.SubElement(target,NS+"title").text="Floor glyph projected from existing room icon"
    transform=ET.SubElement(target,NS+"g",{
        "transform":"matrix("+" ".join(str(v) for v in MATRIX)+")"})
    for group in source_groups: transform.append(copy.deepcopy(group))
    svg=ET.tostring(target,encoding="utf-8",xml_declaration=True)
    hi=cairosvg.svg2png(bytestring=svg,output_width=1024,output_height=512)
    with Image.open(io.BytesIO(hi)) as source:
        tile=source.convert("RGBA").resize(SIZE,Image.Resampling.LANCZOS)
    bbox=tile.getchannel("A").point(lambda v:255 if v>127 else 0).getbbox()
    if bbox!=(40,14,105,52):raise ValueError("Projected source art changed "+str(bbox))
    for point in ((0,0),(127,63),(10,10),(112,53)):
        if tile.getpixel(point)[3]!=0:raise ValueError("Private floor tile edge clipped")
    out.mkdir(parents=True,exist_ok=True)
    svgout=out/"derived_floor_glyph_editable.svg"
    svgout.write_bytes(svg)
    pngout=out/"toxicology_floor_glyph_128x64.png"
    tile.save(pngout)
    atlas=Image.new("RGBA",(2048,2048),(0,0,0,0))
    atlas.paste(tile,RECT[:2])
    a=atlas.getchannel("A")
    ImageDraw.Draw(a).rectangle((1024,1472,1151,1535),fill=0)
    if a.getbbox():raise ValueError("Nontransparent private floor atlas outside tile 376")
    atlasout=out/"toxicology_floor_atlas_private_376.png"
    atlas.save(atlasout)
    # Simulated backgrounds ONLY in the preview, never in the icon PNG or atlas.
    board=Image.new("RGB",(720,480),"#EEF0F2")
    d=ImageDraw.Draw(board)
    try:
        f=ImageFont.truetype("DejaVuSans.ttf",17)
        h=ImageFont.truetype("DejaVuSans.ttf",23)
    except OSError:
        f=h=ImageFont.load_default()
    d.text((20,18),"TO-001 | ONE source, two native surfaces",font=h,fill="#354C55")
    d.text((20,58),"Same original flask and molecules; floor is projected, not redrawn",font=f,fill="#516774")
    room_png=cairosvg.svg2png(bytestring=raw,output_width=512,output_height=512)
    with Image.open(io.BytesIO(room_png)) as im:
        room=im.convert("RGBA").resize((64,64),Image.Resampling.LANCZOS)
    d.text((30,114),"MENU: 64x64",font=f,fill="#354C55")
    d.text((285,114),"FLOOR: 128x64",font=f,fill="#354C55")
    left=Image.new("RGBA",(64,64),"#C93F3D")
    left.alpha_composite(room)
    right=Image.new("RGBA",SIZE,"#68747A")
    right.alpha_composite(tile)
    board.paste(left,(35,160))
    board.paste(right,(280,160))
    board.paste(left.resize((160,160),Image.Resampling.LANCZOS),(36,240))
    board.paste(right.resize((320,160),Image.Resampling.LANCZOS),(281,240))
    d.text((24,441),"Source-only. Backgrounds simulated, not baked into game sprites.",
           font=f,fill="#596E79")
    preview=out/"TO001_shared_symbol_review.png"
    board.save(preview)
    paths=(svgout,pngout,atlasout,preview)
    manifest={
      "issue":24,"stage":"FA_L2_ONLY",
      "one_source_svg":"assets/art/to001/toxicology_room_icon.svg",
      "one_source_sha256":hashlib.sha256(raw).hexdigest(),
      "floor_derived_from_room_svg":True,"extra_floor_badges":False,
      "vanilla_floor_atlas_size":[4096,4096],
      "private_atlas_size":[2048,2048],"private_grid":[16,32],
      "tile_376_rect":list(RECT),"native_private_tile":list(SIZE),
      "visible_bbox":list(bbox),"private_atlas_only_tile_376":True,
      "no_baked_room_color":True,"not_installable":True,
      "gamedb_registered":False,"l3":False,"l4":False,"visual_approved":False,
      "sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print("FA L2: shared original visual motif; TS L3/L4 pending")
    return manifest

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--room-svg",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    build(a.room_svg,a.output)
