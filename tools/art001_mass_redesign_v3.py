#!/usr/bin/env python3
"""FA ART-001 V3 mass spectrometer: real geometry redesign + native sprite study.

Extends the accepted-as-technical-only V2 source. Changes a SINGLE original
NW mass analyzer into an integrated machine with a genuinely separate, supported
operator LCD, larger real sampling station and distinct inspection bay.

This is not a finished game texture, installable mod, 4-view contract, or L4.
No proprietary game pixels or DLLs are used.
"""
import argparse, hashlib, io, json, math, zipfile
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

import bpy
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont
import art001_mass_redesign_v2 as v2
import art001_blender_render as baseline

DIR = "NW"
NATIVE = 128
HIRES = 1024


def forget_exact(names):
    """Delete geometry only from V2 ART study, never native game data."""
    for name in names:
        o=bpy.data.objects.get(name)
        if o is None:
            raise RuntimeError("Expected previous geometry missing: "+name)
        bpy.data.objects.remove(o, do_unlink=True)


def rebuild_analyzer():
    root=baseline.ROOT[v2.MACHINE]
    forget_exact([
        "Main functional console outer bezel",
        "Instrument computer status window",
        "Controller lower panel",
        *["Spectral peak LED %02d"%i for i in range(8)],
        *["Touchable status dial %02d"%i for i in range(6)],
        "Physical operator keyboard support",
        *["Operator keyboard key %d-%d"%(row,col)
          for row in range(2) for col in range(6)],
    ])
    # Not a generic computer screen: the analyzer bay has actual
    # recessed framed optical windows, a mechanical shutter and datum marks.
    v2.box("Large integrated instrument optical bay outer casing",
           (.50,-.89,1.42),(1.42,.09,.96),"metal",.070)
    v2.box("Mechanical shutter top edge",
           (.50,-.956,1.87),(1.38,.031,.087),"light",.016)
    v2.box("Deep dark optical chamber",
           (.48,-.958,1.46),(1.22,.027,.75),"dark",.048)
    v2.box("Blue-gray glazed analyzer status window",
           (.47,-.978,1.47),(1.10,.012,.64),"display",.035)
    v2.box("Internal vertical optical divider",
           (.68,-.989,1.46),(.036,.015,.55),"metal",.012)
    # A clear, purposeful graph made as part of the physical dark glass.
    heights=[.03,.08,.15,.05,.18,.10,.22,.13,.07,.20]
    for i,h in enumerate(heights):
        v2.box("Optical spectra line %02d"%i,
               (.06+i*.084,-.994,1.32+h),
               (.040,.009,.028),"screen_light",.008)
    # Two clearly different operation modes rather than a strip of LEDs.
    v2.box("Instrument mode fascia",(.42,-.923,.85),
           (1.29,.064,.20),"white",.025)
    for i in range(4):
        b=v2.box("Front mechanical status key %d"%i,
                 (.05+i*.21,-.970,.86),(.12,.024,.075),
                 "blue" if i==0 else "metal",.018)
    for i in range(4):
        v2.box("Front bottom serial service seam %d"%i,
               (-.16+i*.2,-.954,.65),(.090,.020,.012),"grey",.005)

    # Physical independently rotatable LCD: the owner-designated concept
    # shows this outside the main analyzer body, NOT pasted on the front.
    # A bolted ledge and stand ensure it cannot be mistaken for a floating prop.
    v2.box("Integral operator console extension",
           (1.64,-.93,.43),(1.02,.70,.13),"metal",.050)
    v2.box("Monitor swivel steel foot",
           (1.72,-1.04,.59),(.42,.41,.19),"dark",.047)
    v2.tube("Monitor supporting metal column",
            (1.72,-1.06,1.02),.054,.76,"metal")
    v2.box("Monitor articulated hinge",
           (1.72,-1.09,1.38),(.21,.18,.15),"grey",.027)
    v2.box("External analytical display black outer frame",
           (1.71,-1.21,1.74),(.92,.15,.76),"dark",.045)
    v2.box("External analytical LCD softly lit glass",
           (1.71,-1.298,1.74),(.78,.012,.62),"display",.029)
    for i,h in enumerate([.08,.13,.26,.10,.21,.34,.18,.30,.15,.21]):
        v2.box("Operator signal trace %02d"%i,
               (1.36+i*.074,-1.310,1.59+h),
               (.046,.008,.021),"screen_light",.008)
    v2.box("Real keyboard carriage under monitor",
           (1.65,-1.34,.46),(.90,.40,.09),"grey",.038)
    v2.box("Physical QWERTY keyboard inset",
           (1.65,-1.40,.518),(.79,.27,.023),"dark",.015)
    for row in range(2):
        for col in range(6):
            v2.box("Actual keyboard key %d %d"%(row,col),
                   (1.35+col*.119,-1.495+row*.129,.538),
                   (.086,.080,.018),"keys",.006)

    # Keep one 8-slot sampler but make the real equipment rack substantially
    # easier to read at 128px. It remains a fixed original machine component.
    forget_exact([
        *["Sample vial body %d"%i for i in range(8)],
        *["Royal blue vial cap %d"%i for i in range(8)],
        *["Sample label %d"%i for i in range(8)],
    ])
    v2.box("White 8-slot autosampler removable carrier",
           (-.50,-1.12,.835),(1.77,.43,.065),"light",.020)
    for i in range(7):
        x=-1.19+i*.212
        v2.tube("Readable individual glass sample %d"%i,
                (x,-1.165,.998),.071,.27,"vial")
        v2.tube("Readable saturated blue cap %d"%i,
                (x,-1.165,1.151),.090,.077,"blue")
        v2.box("Neutral specimen index label %d"%i,
               (x,-1.24,.975),(.09,.012,.09),"light",.008)
    # Subdivide the otherwise plain ionizer tower and visually join it to
    # the white main enclosure. Faces stay physically genuine for 4-way future.
    v2.box("Ionizer anchored central insulating collar",
           (-1.105,.21,2.25),(.84,.77,.12),"grey",.034)
    v2.box("Ionizer tall side steel service strip",
           (-1.491,-.01,2.77),(.020,.17,.63),"metal",.012)
    for i in range(3):
        v2.box("Ionizer blue monitored port %d"%i,
               (-1.504,-.01,2.66+i*.17),(.011,.090,.067),
               "blue" if i==1 else "dark",.004)
    # Distinct warm caution square: extremely restrained on white cabinet.
    v2.box("Satin caution plate",
           (-1.31,-.841,.63),(.20,.018,.14),"metal",.018)
    # No ABCL project branding on player-visible equipment.
    return root


def setup():
    v2.make_scene()
    rebuild_analyzer()
    # A critical actual-image finding in first V3 CI output: the operator
    # screen was hidden below the analyzer hood and looked like another
    # dark stripe. Raise the entire LCD and hinge while physically extending
    # the same support column, so it is a legible separate machine component
    # at native scale (not a fake pasted 2D floating monitor).
    screen_names=[
        "External analytical display black outer frame",
        "External analytical LCD softly lit glass",
        *["Operator signal trace %02d"%i for i in range(10)]
    ]
    for name in screen_names:
        ob=bpy.data.objects.get(name)
        if ob is None:raise RuntimeError("Missing component "+name)
        ob.location.z += .70
    hinge=bpy.data.objects["Monitor articulated hinge"]
    hinge.location.z += .70
    column=bpy.data.objects["Monitor supporting metal column"]
    column.location.z += .35
    column.dimensions.z = 1.46
    # Original authored ionizer port was under-specified in the 128px
    # image. Make its blue inspection strip physically legible.
    v2.box("Ionizer dedicated blue optical condition bar",
           (-1.13,-.127,2.93),(.16,.013,.55),"display",.017)
    v2.box("Ionizer optical strip protective edging",
           (-1.13,-.139,3.22),(.26,.016,.037),"metal",.010)
    scene=bpy.context.scene
    scene.render.resolution_x=HIRES
    scene.render.resolution_y=HIRES
    scene.render.resolution_percentage=100
    scene.cycles.samples=36
    scene.camera.data.ortho_scale=6.60
    # Brighter balanced grey-white than V2's PBR-muddy gray without forcing
    # any four-tone quantization or removing natural high-res shading.
    scene.view_settings.view_transform="Standard"
    scene.view_settings.look="Medium High Contrast"
    return scene


def native_scale(img_path):
    with Image.open(img_path) as src: im=src.convert("RGBA")
    assert im.size == (HIRES,HIRES)
    bbox=im.getchannel("A").getbbox()
    if bbox is None:raise ValueError("New art is completely transparent")
    source=im.crop(bbox)
    factor=min(114/source.width,110/source.height)
    native=source.resize((max(1,round(source.width*factor)),
                          max(1,round(source.height*factor))),
                         Image.Resampling.LANCZOS)
    tile=Image.new("RGBA",(NATIVE,NATIVE),(0,0,0,0))
    tile.alpha_composite(native,((NATIVE-native.width)//2,
                                 125-native.height))
    return tile


def fine_2d_finish(base):
    # Deliberate soft outline, made from the actual alpha geometry. Do NOT
    # translate a sharp low-res 128px source to fake pixel art.
    alpha=base.getchannel("A")
    perimeter=ImageChops.subtract(alpha,alpha.filter(ImageFilter.MinFilter(3)))
    perimeter=perimeter.filter(ImageFilter.GaussianBlur(.36))
    perimeter=perimeter.point(lambda v:round(v*.43))
    ink=Image.new("RGBA",base.size,(42,46,49,0))
    ink.putalpha(perimeter)
    return ink,Image.alpha_composite(base,ink)


def pngbytes(im):
    b=io.BytesIO();im.save(b,format="PNG");return b.getvalue()


def pack(out,source,base,ink,done,editable):
    image=out/"mass_spectrometer_NW_V3_original_smooth_128.png"
    done.save(image)
    layers=out/"mass_spectrometer_NW_V3_editable.ora"
    root=Element("image",{"w":"128","h":"128","name":"ART001 V3 original studio source","version":"0.0.3"})
    stack=SubElement(root,"stack")
    for label,src in [("Natural clean shell and mechanical components","data/shell.png"),
                      ("Soft art-directed 2D ink","data/ink.png")][::-1]:
        SubElement(stack,"layer",{"name":label,"src":src,"visibility":"visible",
                                  "opacity":"1.0","composite-op":"svg:src-over",
                                  "x":"0","y":"0"})
    with zipfile.ZipFile(layers,"w") as z:
        z.writestr("mimetype","image/openraster",compress_type=zipfile.ZIP_STORED)
        z.writestr("stack.xml",tostring(root))
        z.writestr("data/shell.png",pngbytes(base))
        z.writestr("data/ink.png",pngbytes(ink))
        z.writestr("mergedimage.png",pngbytes(done))
    board=Image.new("RGB",(944,542),(242,244,245))
    d=ImageDraw.Draw(board)
    try:
        title=ImageFont.truetype("DejaVuSans.ttf",23)
        regular=ImageFont.truetype("DejaVuSans.ttf",17)
    except OSError:
        title=ImageFont.load_default()
        regular=title
    d.text((24,17),"FA / ART-001 | NW Physical Redesign V3",font=title,fill=(43,55,64))
    d.text((24,54),"Integrated analyzer + real supported LCD + original specimen rack",font=regular,fill=(82,94,102))
    d.text((36,101),"128px 1x",font=regular,fill=(54,69,77))
    board.paste(done,(35,148),done)
    d.text((218,101),"Smooth detail review / NOT nearest-neighbor",font=regular,fill=(54,69,77))
    enlarged=done.resize((432,432),Image.Resampling.LANCZOS)
    board.paste(enlarged,(225,102),enlarged)
    d.line((24,520,917,520),fill=(184,199,209),width=1)
    d.text((24,522),"SOURCE-ONLY · OWNER VISUAL REVIEW NOT PASSED · NOT INSTALLABLE",
           font=regular,fill=(99,108,116))
    preview=out/"NW_V3_visual_review.png"
    board.save(preview)
    paths=(source,image,layers,preview,editable)
    manifest={
      "stage":"ART001-MASS-V3-STRUCTURAL-REDESIGN-NW",
      "source_only":True,"not_installable":True,
      "owner_visual_approved":False,"game_l4_tested":False,
      "direction":"NW","cell":[128,128],
      "source_render":[HIRES,HIRES],
      "sampler_vials":7,"has_physical_operator_lcd":True,
      "not_pixel_art":True,"palette_quantized":False,
      "sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    return manifest


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    out=args.output.resolve()
    if any(x.lower() in ("addons","streamingassets") for x in out.parts):
        raise ValueError("Refuse writing in any original game directories")
    out.mkdir(parents=True,exist_ok=True)
    setup()
    editable=out/"ART001_V3_mass_3D_editable.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(editable))
    hires=out/"NW_original_studio_1024.png"
    bpy.context.scene.render.filepath=str(hires)
    bpy.ops.render.render(write_still=True)
    base=native_scale(hires)
    ink,finish=fine_2d_finish(base)
    m=pack(out,hires,base,ink,finish,editable)
    if len(m["sha256"])!=5:raise RuntimeError("Incomplete review files")
    print("ART-001 V3: revised physical instrument / smooth NW source review only",flush=True)


if __name__=="__main__":
    main()
