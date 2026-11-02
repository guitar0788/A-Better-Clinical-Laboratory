#!/usr/bin/env python3
"""ART-001 smooth 2D studio finish, from the ORIGINAL ABCL editable Blender scene.

The output is one NW game-size transparent raster, not pixel art.
No block geometry generation, palette quantization or nearest-neighbor scaling.
Never imports native game textures. Does not write a game-installable atlas.
"""
import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

import bpy
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

CELL = 128
RENDER = 768


def render_original(blend_file, highres):
    bpy.ops.wm.open_mainfile(filepath=str(blend_file))
    target = bpy.data.objects["Editable model mass_spectrometer"]
    other = bpy.data.objects["Editable model sample_digestion_workstation"]
    for ob in bpy.data.objects:
        if ob.parent == target:
            ob.hide_render = False
        if ob.parent == other:
            ob.hide_render = True
    target.location = (0, 0, 0)
    target.rotation_euler.z = 0
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 32
    scene.render.resolution_x = RENDER
    scene.render.resolution_y = RENDER
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.filepath = str(highres)
    bpy.ops.render.render(write_still=True)
    if not highres.exists():
        raise RuntimeError("Cloud render produced no source image")


def smooth_source(source_image):
    with Image.open(source_image) as im:
        rgba = im.convert("RGBA")
    if rgba.size != (RENDER, RENDER):
        raise ValueError("Requires a genuine 768px source, not an upscaled 128px sprite")
    bounds = rgba.getchannel("A").getbbox()
    if not bounds:
        raise ValueError("Source has no opaque geometry")
    crop = rgba.crop(bounds)
    factor = min(116 / crop.width, 108 / crop.height)
    target = (max(1, round(crop.width*factor)), max(1, round(crop.height*factor)))
    # Genuine supersampling: 768px -> 128px. Pillow RGBA LANCZOS
    # filters transparency in premultiplied-alpha space.
    crop = crop.resize(target, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    canvas.alpha_composite(crop, ((CELL-target[0])//2, 125-target[1]))
    return canvas


def color_and_edge(base):
    # Per-pixel linear soft tonal adjustment, not N-band quantization.
    # Modify neutral material areas gently; blue control details stay blue.
    pixels = bytearray(base.tobytes())
    for i in range(0, len(pixels), 4):
        r,g,b,a = pixels[i:i+4]
        if a > 0 and max(r,g,b)-min(r,g,b) < 24 and min(r,g,b) > 95:
            # Slightly lift clean white cabinet while retaining gradient
            # continuity and each original shading variation.
            for index in (0,1,2):
                v = pixels[i+index]
                pixels[i+index] = min(246, round(v + (242-v)*0.13))
    toned = Image.frombytes("RGBA", (CELL,CELL), bytes(pixels))
    al = toned.getchannel("A")
    # Soft inner contour, NOT 1px pixel staircase; zero where transparent.
    inner = ImageChops.subtract(al, al.filter(ImageFilter.MinFilter(3)))
    inner = inner.filter(ImageFilter.GaussianBlur(0.52))
    inner = inner.point(lambda v: round(v*0.47))
    ink = Image.new("RGBA", (CELL,CELL), (49,54,57,0))
    ink.putalpha(inner)
    finished = Image.alpha_composite(toned, ink)
    return toned, ink, finished


def png_bytes(im):
    b=io.BytesIO()
    im.save(b, "PNG", optimize=True)
    return b.getvalue()


def package(out, base, ink, finished):
    out.mkdir(parents=True, exist_ok=True)
    png=out/"mass_spectrometer_NW_smooth_antialiased_128.png"
    finished.save(png)
    ora=out/"mass_spectrometer_NW_smooth_layers.ora"
    root=Element("image", {"w":"128","h":"128","name":"NW Smooth Original Art Review","version":"0.0.3"})
    stack=SubElement(root, "stack")
    for name,src in [("Continuous tone original studio paint","data/base.png"),
                     ("Soft contour 2D finish","data/soft-edge.png")][::-1]:
        SubElement(stack, "layer", {"name":name,"src":src,
                    "visibility":"visible","opacity":"1.0",
                    "composite-op":"svg:src-over","x":"0","y":"0"})
    with zipfile.ZipFile(ora, "w") as z:
        z.writestr("mimetype", "image/openraster",compress_type=zipfile.ZIP_STORED)
        z.writestr("stack.xml",tostring(root))
        z.writestr("data/base.png",png_bytes(base))
        z.writestr("data/soft-edge.png",png_bytes(ink))
        z.writestr("mergedimage.png",png_bytes(finished))
    sheet = Image.new("RGB",(820,610),(236,239,242))
    d=ImageDraw.Draw(sheet)
    try:
        font=ImageFont.truetype("DejaVuSans.ttf",20)
        small=ImageFont.truetype("DejaVuSans.ttf",15)
    except OSError:
        font=ImageFont.load_default()
        small=font
    d.text((24,20),"ART-001  /  NW SMOOTH 2D REVIEW",font=font,fill=(39,53,63))
    d.text((24,56),"Original 768px source / Lanczos to 128px / continuous shading",font=small,fill=(70,85,95))
    # Show the same source at native size and smooth enlarged size.
    # Never show nearest-neighbor blocks as a fake artistic improvement.
    d.text((30,114),"Native 128 x 128",font=small,fill=(57,65,72))
    d.text((214,114),"4x smooth view - visual inspection only",font=small,fill=(57,65,72))
    sheet.paste(finished,(30,156),finished)
    smooth_zoom=finished.resize((430,430),Image.Resampling.LANCZOS)
    sheet.paste(smooth_zoom,(224,118),smooth_zoom)
    d.text((28,576),"SOURCE ONLY / NOT A GAME PACKAGE / OWNER VISUAL GATE OPEN",
           font=small,fill=(85,91,95))
    preview=out/"NW_smooth_mobile_preview.png"
    # Do not crop final output; prevent preview extension below canvas.
    sheet.save(preview)
    checks={
       "stage":"NW-SMOOTH-128-V1",
       "original_768px_render":True,
       "resampler":"Lanczos",
       "quantized_palette":False,
       "pixel_nearest_neighbor":False,
       "owner_visual_approved":False,
       "game_l4":False,"not_installable":True,
       "sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in (png,ora,preview)}
    }
    (out/"manifest.json").write_text(json.dumps(checks,indent=2)+"\n",encoding="utf-8")
    return checks


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--blend",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    out=args.output.resolve()
    if any(x.lower() in ("streamingassets","addons") for x in out.parts):
        raise ValueError("Refuse writing to game directory")
    out.mkdir(parents=True,exist_ok=True)
    raw=out/"NW_original_768px_renderer_input.png"
    render_original(args.blend.resolve(),raw)
    base,ink,finished=color_and_edge(smooth_source(raw))
    report=package(out,base,ink,finished)
    # Raw input is original generated Blender art; safe review provenance.
    report["source_render_sha256"]=hashlib.sha256(raw.read_bytes()).hexdigest()
    (out/"manifest.json").write_text(json.dumps(report,indent=2)+"\n")
    print("NW SMOOTH SOURCE REVIEW READY - NOT A VISUAL OR L4 PASS",flush=True)

if __name__=="__main__":
    main()
