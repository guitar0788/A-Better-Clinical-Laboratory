#!/usr/bin/env python3
"""FA TO-001 original Toxicology Laboratory room icons, active + inactive.

Original Project Hospital TS source audit:
  active LAB icon background #C93F3D; inactive #999999;
  glyph #F2F2F2; native sprite crop Rect(2,2,60,60) within a 64px source.
No native game pixels are embedded. This is resource-only, not L3/L4.
"""
import argparse
import hashlib
import io
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ACTIVE_ID = "ASSET_ABCL_TOXICOLOGY_ROOM_ICON"
INACTIVE_ID = "ASSET_ABCL_TOXICOLOGY_ROOM_ICON_INACTIVE"  # Candidate, not runtime behavior.
ROOM_ID = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB"
PALETTE = {"active":"#C93F3D","inactive":"#999999","glyph":"#F2F2F2"}


def rasterize(svg_path, expected_panel):
    source=Path(svg_path).read_bytes()
    root=ET.fromstring(source)
    if root.tag!="{http://www.w3.org/2000/svg}svg":
        raise ValueError("Not an original SVG")
    if root.get("viewBox")!="0 0 64 64":
        raise ValueError("SVG must have 64px native viewBox")
    if expected_panel.lower().encode() not in source.lower():
        raise ValueError("Native LAB palette missing from SVG")
    if b"#f2f2f2" not in source.lower():
        raise ValueError("Original LAB white glyph not found")
    hires=cairosvg.svg2png(bytestring=source,output_width=512,output_height=512)
    with Image.open(io.BytesIO(hires)) as image:
        art=image.convert("RGBA").resize((64,64),Image.Resampling.LANCZOS)
    # Native IconManager crops Rect(2,2,60,60); make that contract explicit.
    canvas=ImageDraw.Draw(art)
    for rect in ((0,0,63,1),(0,62,63,63),(0,0,1,63),(62,0,63,63)):
        canvas.rectangle(rect,fill=(0,0,0,0))
    if art.getchannel("A").getbbox()!=(2,2,62,62):
        raise ValueError("64px 2px border has incorrect alpha bounds")
    expected=tuple(bytes.fromhex(expected_panel[1:]))
    if art.getpixel((11,11))!=(*expected,255):
        raise ValueError("LAB UI swatch did not survive 512->64px render")
    alevels={a for a in art.getchannel("A").getdata() if 0<a<255}
    if len(alevels)<10:
        raise ValueError("Icon is not smoothly antialiased")
    return art


def preview(active,inactive,path):
    board=Image.new("RGB",(900,570),"#F0F2F3")
    d=ImageDraw.Draw(board)
    try:
        title=ImageFont.truetype("DejaVuSans.ttf",25)
        small=ImageFont.truetype("DejaVuSans.ttf",17)
    except OSError:
        title=ImageFont.load_default()
        small=title
    d.text((26,20),"TO-001 | Toxicology Laboratory room icon",font=title,fill="#354B53")
    d.text((26,59),"Original lab colors: #C93F3D active / #999999 inactive",font=small,fill="#687A83")
    d.text((48,114),"ACTIVE / LAB room",font=small,fill="#394E57")
    d.text((495,114),"INACTIVE / TS review candidate",font=small,fill="#394E57")
    for x,icon in ((45,active),(495,inactive)):
        board.paste(icon,(x,155),icon)
        large=icon.resize((296,296),Image.Resampling.LANCZOS)
        board.paste(large,(x+92,144),large)
    d.text((26,472),"Native 64x64 RGBA | 2px crop | original analytical-flask glyph",font=small,fill="#65777F")
    d.text((26,504),"SOURCE ONLY | owner visual acceptance and room-menu L3/L4 pending",font=small,fill="#65777F")
    board.save(path)


def build(svg_path,output,inactive_svg_path=None):
    svg_path=Path(svg_path)
    if inactive_svg_path is None:
        inactive_svg_path=svg_path.with_name("toxicology_room_icon_inactive.svg")
    inactive_svg_path=Path(inactive_svg_path)
    output=Path(output).resolve()
    if any(p.lower() in ("streamingassets","addons") for p in output.parts):
        raise ValueError("Refuse live game directory")
    output.mkdir(parents=True,exist_ok=True)
    active=rasterize(svg_path,PALETTE["active"])
    inactive=rasterize(inactive_svg_path,PALETTE["inactive"])
    active_png=output/"toxicology_room_icon.png"
    inactive_png=output/"toxicology_room_icon_inactive.png"
    active.save(active_png,optimize=False)
    inactive.save(inactive_png,optimize=False)
    review=output/"to001_mobile_review.png"
    preview(active,inactive,review)
    manifest={
      "issue":24,"task":"TO-001",
      "active_asset_id":ACTIVE_ID,
      "inactive_candidate_asset_id":INACTIVE_ID,
      "inactive_switching_proven":False,
      "intended_room_type":ROOM_ID,
      "format":"TEXTURE_CUSTOM_SPRITE",
      "native_active_panel":PALETTE["active"],
      "native_inactive_panel":PALETTE["inactive"],
      "native_glyph":PALETTE["glyph"],
      "resolution":[64,64],
      "native_crop_rect":[2,2,60,60],
      "sources":[svg_path.name,inactive_svg_path.name],
      "source_only":True,"owner_visual_approved":False,
      "game_asset_registered":False,"native_room_ui_adapted":False,
      "l3_tested":False,"l4_tested":False,
      "no_iconindex_850_override":True,
      "no_global_zone_color_override":True,
      "sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                for p in (active_png,inactive_png,review)}
    }
    (output/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print("TO-001 FA native LAB red/gray original art L2 built; NOT UI L3/L4")
    return manifest


if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--svg",required=True)
    p.add_argument("--inactive-svg")
    p.add_argument("--output",required=True)
    args=p.parse_args()
    build(args.svg,args.output,args.inactive_svg)
