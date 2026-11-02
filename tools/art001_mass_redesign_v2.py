#!/usr/bin/env python3
"""ART-001 original mass-spectrometer sculpt, NW first. Source-only FA review.

Physically authored cabinet mesh, curved shell profile, seated controls, sample rack,
real manufacturer-neutral details and a single orthographic game-scale render.
Output is an editable .blend and independently smooth 2D anti-aliased RGBA.
No vanilla/DLC assets, no clinical code, no game package.
"""
import argparse,hashlib,io,json,math,zipfile
from pathlib import Path
from xml.etree.ElementTree import Element,SubElement,tostring

import bpy
from mathutils import Vector
from PIL import Image,ImageChops,ImageDraw,ImageFilter

import art001_blender_render as prior

MACHINE="mass_spectrometer"
CELL=128
STUDIO_RES=1024
PARTS=[]

def object_material(name,material):
    ob=bpy.context.object
    ob.name=name
    ob.parent=prior.ROOT[MACHINE]
    ob.data.materials.clear()
    ob.data.materials.append(prior.MAT[material])
    PARTS.append(ob)
    return ob

def box(name,center,size,material,bevel=.035):
    bpy.ops.mesh.primitive_cube_add(size=1,location=center)
    ob=object_material(name,material)
    ob.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        b=ob.modifiers.new("Subtle hand-built corner roll","BEVEL")
        b.width=bevel;b.segments=3
        n=ob.modifiers.new("Weighted edge normals","WEIGHTED_NORMAL")
        n.keep_sharp=True
    return ob

def tube(name,center,radius,height,material,vertices=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=height,location=center)
    ob=object_material(name,material)
    b=ob.modifiers.new("Manufactured bottle lip","BEVEL")
    b.width=.011;b.segments=3
    for p in ob.data.polygons:p.use_smooth=True
    return ob

def shell_profile(name,outline,y0,y1,material):
    """An original rounded x/z cross-section extruded as one opaque manifold.
    No stacked collection of generic cuboids for the main machine housing.
    Outline is CCW when seen from front; both ends form closed real walls.
    """
    verts=[(x,y,z) for y in (y0,y1) for x,z in outline]
    n=len(outline)
    faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]
    for i in range(n):
        j=(i+1)%n
        faces.append((i,j,j+n,i+n))
    mesh=bpy.data.meshes.new(name+" genuine closed shell")
    mesh.from_pydata(verts,[],faces)
    mesh.update()
    ob=bpy.data.objects.new(name,mesh)
    bpy.context.collection.objects.link(ob)
    ob.parent=prior.ROOT[MACHINE]
    ob.data.materials.append(prior.MAT[material])
    PARTS.append(ob)
    bevel=ob.modifiers.new("Forged 2D-friendly shell perimeter","BEVEL")
    bevel.width=.047;bevel.segments=3
    weighted=ob.modifiers.new("Weighted normals","WEIGHTED_NORMAL")
    weighted.keep_sharp=True
    return ob

def line(name,xyz,material,width=.018):
    cu=bpy.data.curves.new(name,"CURVE")
    cu.dimensions="3D";cu.resolution_u=20
    cu.bevel_depth=width;cu.bevel_resolution=3
    spline=cu.splines.new("POLY")
    spline.points.add(len(xyz)-1)
    for p,coord in zip(spline.points,xyz):p.co=(*coord,1)
    ob=bpy.data.objects.new(name,cu)
    bpy.context.collection.objects.link(ob)
    ob.parent=prior.ROOT[MACHINE]
    cu.materials.append(prior.MAT[material])
    PARTS.append(ob)
    return ob

def sculpt_mass():
    # One integrated body, markedly deeper/taller than the rejected long thin tube.
    # Main silhouette has purposeful rounded shoulders and a protected lower skirting.
    box("Continuous enclosed lower steel plinth",(0,0,.16),(3.34,1.97,.26),"dark",.10)
    box("Grey gasket around protected underside",(0,0,.315),(3.20,1.90,.080),"metal",.024)
    shell_profile("Unified white spectrometer instrument shell",
       [(-1.56,.34),(1.42,.34),(1.57,.46),(1.57,1.80),
        (1.49,2.05),(1.32,2.14),(-1.30,2.14),(-1.50,1.96),(-1.56,1.76)],
       -.81,.82,"white")
    # Chassis front: wide strong dark analyser window set IN a real flush lip.
    box("Continuous molded front equipment face",(0,-.833,1.13),(2.70,.055,1.27),"grey",.056)
    box("Slim top front white shoulder",(0,-.874,1.91),(2.65,.048,.17),"light",.024)
    # Left sealed cassette cover; right operational face and a larger readable LCD.
    box("Removable sealed sample intake door",(-.91,-.873,1.30),(.86,.047,.88),"white",.038)
    box("Left side service seal",(-.91,-.904,1.31),(.67,.016,.66),"grey",.017)
    box("Ion source viewing insert",(-.91,-.924,1.43),(.30,.022,.36),"metal",.023)
    box("Depth-set blue ion filter",(-.91,-.945,1.43),(.21,.010,.29),"display",.014)
    box("Main functional console outer bezel",(.51,-.886,1.42),(1.31,.070,.84),"dark",.063)
    box("Instrument computer status window",(.51,-.936,1.46),(1.09,.013,.66),"display",.034)
    # Screen has proper function: vivid graph, gentle hardware buttons, line chart.
    for n,(dx,dz) in enumerate([(0,0),(.08,.06),(.18,-.02),(.29,.17),(.43,.03),(.54,.22),(.66,.08),(.78,.19)]):
        box("Spectral peak LED %02d"%n,(.04+dx,-.947,1.31+dz),
            (.049,.010,.024),"screen_light",.008)
    box("Controller lower panel",(.51,-.892,.82),(1.28,.055,.21),"grey",.024)
    for i in range(6):
        tube("Touchable status dial %02d"%i, (.15+i*.137,-.921,.816),.027,.018,
             "blue" if i==0 else "metal",20).rotation_euler=(math.pi/2,0,0)
    # Tall integrated upstream source occupies a permanent corner of the body
    # with support feet and realistic rear profile (not floating on top).
    box("Welded ionizer interface riser",(-1.10,.35,2.16),(.94,.85,.19),"metal",.052)
    shell_profile("Single molded high-voltage ion source tower",
      [(-1.49,2.20),(-.69,2.20),(-.67,2.33),(-.67,3.21),
       (-.76,3.33),(-1.37,3.33),(-1.50,3.19)],
      -.05,.74,"white")
    box("Ion source side ventilation cover",(-1.51,.27,2.81),(.033,.55,.57),"grey",.020)
    for k in range(5):
        box("Ionizer rear thermal exhaust %d"%k,(-1.529,.09+k*.105,2.85),(.014,.050,.29),"dark",.009)
    box("Ion filter recess under true bezel",(-1.10,-.076,2.89),(.48,.032,.63),"metal",.033)
    box("Ion source dark optical cartridge",(-1.10,-.104,2.89),(.32,.011,.45),"dark",.013)
    box("Ion source top service plate",(-1.10,.31,3.35),(.74,.83,.055),"light",.027)
    # Complete mechanical autosampler with rigid visible supports (not pasted
    # blue pixels or a floating object in front of an opaque side).
    box("Fixed sampler carriage lower arm",(-.50,-1.00,.50),(2.08,.43,.13),"metal",.033)
    box("Integrated sample receiver tray",(-.51,-1.12,.62),(1.86,.52,.16),"dark",.044)
    box("Single stainless microtiter plate",(-.51,-1.13,.74),(1.78,.44,.095),"metal",.028)
    for i in range(8):
        x=-1.20+i*.194
        tube("Sample vial body %d"%i,(x,-1.16,.91),.060,.22,"vial")
        tube("Royal blue vial cap %d"%i,(x,-1.16,1.035),.073,.057,"blue")
        # Printed narrow sticker at one face acts as a style-appropriate label.
        box("Sample label %d"%i,(x,-1.225,.890),(.067,.006,.06),"light",.006)
    # Separate service gaskets and dark precise ventilation holes for same
    # exterior anatomy, never duplicated to the rear in the 4-view series.
    for i in range(6):
        box("Right housing rear louvre %02d"%i,(1.588,-.45+i*.150,1.23),
            (.015,.084,.56),"dark",.009)
    box("Rear original service hatch",(.45,.833,1.31),(1.17,.029,.70),"grey",.020)
    for i in range(8):
        box("Rear filter slot %02d"%i,(-.03+i*.13,.850,1.31),(.072,.012,.44),"dark",.007)
    # Art-directed anchor seams on top and side emphasize panel anatomy.
    line("Top white housing split",[(.65,-.71,2.15),(.65,.64,2.15)],"metal",.012)
    line("Side full-length service seam",[(1.565,-.68,.54),(1.565,.60,.54)],"grey",.013)
    # Real front-mounted keyboard panel: restrained and legible at 128px.
    box("Physical operator keyboard support",(1.07,-1.02,.43),(.97,.36,.10),"metal",.035)
    for row in range(2):
        for col in range(6):
            box("Operator keyboard key %d-%d"%(row,col),
                (.70+col*.13,-1.17+row*.11,.493),
                (.094,.078,.016),"keys",.006)

def make_scene():
    prior.build_scene()
    root=prior.ROOT[MACHINE]
    bpy.ops.object.select_all(action="DESELECT")
    # Remove only the old mass art. The other machine and technical pipeline
    # remain untouched and cannot be accidentally shipped.
    to_delete=[ob for ob in bpy.data.objects if ob.parent==root]
    for ob in to_delete:bpy.data.objects.remove(ob,do_unlink=True)
    prior.CURRENT=MACHINE
    sculpt_mass()
    # Keep the second experiment hidden; save source as isolated editable
    # study but leave original Github source unchanged.
    for ob in bpy.data.objects:
        if ob.parent==prior.ROOT["sample_digestion_workstation"]:
            ob.hide_render=True
    root.location=(0,0,0)
    root.rotation_euler.z=0
    scene=bpy.context.scene
    scene.render.resolution_x=STUDIO_RES
    scene.render.resolution_y=STUDIO_RES
    scene.render.resolution_percentage=100
    scene.render.engine="CYCLES"
    scene.cycles.samples=32
    scene.render.film_transparent=True
    scene.view_settings.view_transform="Standard"
    scene.camera.data.ortho_scale=6.2
    # The camera and all areas remain the same for future camera rotations.
    return scene

def make_nw(image):
    with Image.open(image) as im:rgba=im.convert("RGBA")
    rect=rgba.getchannel("A").getbbox()
    if not rect:raise ValueError("Empty render")
    crop=rgba.crop(rect)
    ratio=min(114/crop.width,110/crop.height)
    crop=crop.resize((max(1,round(crop.width*ratio)),
                     max(1,round(crop.height*ratio))),Image.Resampling.LANCZOS)
    sprite=Image.new("RGBA",(CELL,CELL))
    sprite.alpha_composite(crop,((CELL-crop.width)//2,125-crop.height))
    return sprite

def paintfinish(native):
    # The correctly shadowed mesh stays continuous-color. This is *not*
    # four-band palette reduction and does not create pixel-art outlines.
    layer=Image.new("RGBA",(CELL,CELL),(0,0,0,0))
    al=native.getchannel("A")
    edge=ImageChops.subtract(al,al.filter(ImageFilter.MinFilter(3)))
    edge=edge.filter(ImageFilter.GaussianBlur(.40))
    edge=edge.point(lambda a:round(a*.34))
    layer.putalpha(edge)
    # Dark blue graphite, same restrained contour role as vanilla:
    tinted=Image.new("RGBA",(CELL,CELL),(40,45,49,0))
    tinted.putalpha(edge)
    return tinted,Image.alpha_composite(native,tinted)

def as_png(im):
    b=io.BytesIO();im.save(b,format="PNG",optimize=True);return b.getvalue()

def output(out,original,ink,finished,blend):
    img=out/"mass_spectrometer_NW_V2_smooth_original_128.png"
    finished.save(img)
    ora=out/"mass_spectrometer_NW_V2_editable_layers.ora"
    root=Element("image",{"w":"128","h":"128","version":"0.0.3",
         "name":"ART-001 authored physical model smooth paint review"})
    st=SubElement(root,"stack")
    for name,p in [("Soft 2D silhouette","data/edge.png"),
                   ("High-resolution cabinet rendering","data/base.png")]:
        SubElement(st,"layer",{"name":name,"src":p,"visibility":"visible",
           "opacity":"1.0","composite-op":"svg:src-over","x":"0","y":"0"})
    with zipfile.ZipFile(ora,"w") as z:
        z.writestr("mimetype","image/openraster",compress_type=zipfile.ZIP_STORED)
        z.writestr("stack.xml",tostring(root))
        z.writestr("data/edge.png",as_png(ink))
        z.writestr("data/base.png",as_png(original))
        z.writestr("mergedimage.png",as_png(finished))
    from PIL import ImageFont
    board=Image.new("RGB",(800,558),(239,241,244))
    draw=ImageDraw.Draw(board)
    try:
        title=ImageFont.truetype("DejaVuSans.ttf",22)
        small=ImageFont.truetype("DejaVuSans.ttf",16)
    except OSError:
        title=ImageFont.load_default();small=title
    draw.text((22,18),"FA / ART-001  —  RESCULPTED NW STUDY",font=title,fill="#334854")
    draw.text((22,55),"One authored 3D cabinet / continuous shade / smooth anti-alias",font=small,fill="#596c76")
    draw.text((36,108),"1x native 128px",font=small,fill="#53636b")
    draw.text((222,108),"3x smooth inspection (not pixel art)",font=small,fill="#53636b")
    board.paste(finished,(34,154),finished)
    large=finished.resize((384,384),Image.Resampling.LANCZOS)
    board.paste(large,(226,132),large)
    draw.line((22,528,779,528),fill="#c1cad0",width=1)
    draw.text((22,534),"SOURCE-ONLY. VISUAL QUALITY NOT ACCEPTED; NO GAME INSTALL / L4.",
              font=small,fill="#687983")
    contact=out/"NW_V2_smooth_review.png"
    board.save(contact)
    m={"stage":"MASS-ORIGINAL-3D-SCULPT-V2-NW",
       "source_only":True,"not_installable":True,"visual_approved":False,
       "game_l4":False,"direction":"NW","cell":[128,128],
       "true_source_render_px":[STUDIO_RES,STUDIO_RES],
       "scale":"Lanczos continuous antialias",
       "quantized_palette":False,"nearest_neighbor":False,
       "original_mesh_parts":len(PARTS),
       "sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in (img,ora,contact,blend,out/"original_NW_1024.png")}}
    (out/"manifest.json").write_text(json.dumps(m,indent=2)+"\n")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    out=args.output.resolve()
    if any(x.lower() in ("addons","streamingassets") for x in out.parts):
        raise ValueError("Never write inside a game installation")
    out.mkdir(parents=True,exist_ok=True)
    make_scene()
    src=out/"ART001_Mass_Resculpt_Editable.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(src))
    raw=out/"original_NW_1024.png"
    bpy.context.scene.render.filepath=str(raw)
    bpy.ops.render.render(write_still=True)
    base=make_nw(raw)
    ink,finished=paintfinish(base)
    output(out,base,ink,finished,src)
    print("FA V2 ORIGINAL PHYSICAL CABINET RESCULPT: SOURCE-ONLY L2",flush=True)
if __name__=="__main__":main()
