#!/usr/bin/env python3
"""Original TO-001 Toxicology Laboratory room icon; L2 art review only.

The game crops private custom UI sprites at Rect(2,2,60,60).
This does not modify GameDB, original atlas, clinical G1 or native UI code.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import cairosvg
from PIL import Image, ImageDraw, ImageFont

ID = "ASSET_ABCL_TOXICOLOGY_ROOM_ICON"

def build(svg_path, output):
    output = Path(output).resolve()
    if any(p.lower() in ("streamingassets", "addons") for p in output.parts):
        raise ValueError("Refuse writing into any game directory")
    output.mkdir(parents=True, exist_ok=True)
    source = Path(svg_path).read_bytes()
    root = ET.fromstring(source)
    if root.tag != "{http://www.w3.org/2000/svg}svg":
        raise ValueError("Not SVG")
    png = cairosvg.svg2png(bytestring=source, output_width=512, output_height=512)
    with Image.open(io.BytesIO(png)) as image:
        icon = image.convert("RGBA").resize((64,64), Image.Resampling.LANCZOS)
    # Clear the reserved border. Resampling can spread tiny alpha outside
    # the 60px panel; IconManager crops at (2,2,60,60).
    pen = ImageDraw.Draw(icon)
    for rect in ((0,0,63,1),(0,62,63,63),(0,0,1,63),(62,0,63,63)):
        pen.rectangle(rect, fill=(0,0,0,0))
    bbox = icon.getchannel("A").getbbox()
    if bbox != (2,2,62,62):
        raise ValueError("Unsafe native icon crop: %r" % (bbox,))
    icon_path = output / "toxicology_room_icon.png"
    icon.save(icon_path)
    board = Image.new("RGB",(700,540),"#f0f2f3")
    draw = ImageDraw.Draw(board)
    try:
        title=ImageFont.truetype("DejaVuSans.ttf",23)
        small=ImageFont.truetype("DejaVuSans.ttf",16)
    except OSError:
        title=ImageFont.load_default()
        small=title
    draw.text((28,22),"TO-001 | Toxicology Laboratory",fill="#3b5259",font=title)
    draw.text((28,61),"One original room-type UI icon / smooth 2D / no vanilla sprites",fill="#6d7b83",font=small)
    draw.text((34,111),"64 x 64 actual",font=small,fill="#4b646c")
    draw.text((194,111),"5x smooth screen preview",font=small,fill="#4b646c")
    board.paste(icon,(35,153),icon)
    zoom=icon.resize((300,300),Image.Resampling.LANCZOS)
    board.paste(zoom,(195,134),zoom)
    draw.text((29,483),"SOURCE ONLY | Owner visual acceptance and native-menu L4 pending",font=small,fill="#667780")
    preview=output / "to001_mobile_review.png"
    board.save(preview)
    manifest={
      "issue":24,"task":"TO-001","id":ID,
      "intended_room_type":"ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB",
      "source":Path(svg_path).name,
      "format":"TEXTURE_CUSTOM_SPRITE",
      "resolution":[64,64],"native_crop_rect":[2,2,60,60],
      "source_only":True,"visual_approved":False,
      "l3_tested":False,"l4_tested":False,
      "should_replace_iconindex_850":False,
      "sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                for p in (icon_path,preview)}
    }
    (output / "manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print("TO-001 FA ICON L2 RESOURCE GENERATED; NATIVE UI INTEGRATION NOT DONE")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--svg",required=True)
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    build(args.svg,args.output)
