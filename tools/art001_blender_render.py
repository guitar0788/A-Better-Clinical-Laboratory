#!/usr/bin/env python3
"""Original ABCL lab-device Blender 4.5 study: editable 3D scene and 8 orthographic 128px previews.
Source-only; no game data, addon, native asset, installation or medical logic.
"""
import argparse,hashlib,json,math
from pathlib import Path
import bpy
from mathutils import Vector
from PIL import Image,ImageDraw,ImageFont

DIRECTIONS=("NW","NE","SE","SW")
MODELS=("mass_spectrometer","sample_digestion_workstation")
GAME_WHITE={"light":"#f2f2f2","body":"#e6e6e6","shade":"#cccccc","shadow":"#b3b3b3"}
GROUP,ROOT,MAT={}, {}, {}
CURRENT=None

def color(h):
    f=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    return (*[(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4) for v in f],1)

def make_material(name,hexcode,metallic=0,rough=.42,transparent=False):
    m=bpy.data.materials.new(name);m.use_nodes=True
    m.diffuse_color=color(hexcode)
    nd=m.node_tree.nodes
    p=nd.get("Principled BSDF")
    p.inputs["Base Color"].default_value=color(hexcode)
    p.inputs["Metallic"].default_value=metallic
    p.inputs["Roughness"].default_value=rough
    if transparent:
        mix=nd.new("ShaderNodeMixShader")
        mix.inputs[0].default_value=.46
        clear=nd.new("ShaderNodeBsdfTransparent")
        links=m.node_tree.links;out=nd.get("Material Output")
        links.clear()
        links.new(clear.outputs[0],mix.inputs[1])
        links.new(p.outputs[0],mix.inputs[2])
        links.new(mix.outputs[0],out.inputs["Surface"])
    MAT[name]=m

def register(name,mat):
    ob=bpy.context.object;ob.name=name;ob.parent=ROOT[CURRENT]
    ob.data.materials.append(MAT[mat]);GROUP[CURRENT].append(ob)
    return ob

def bevel(ob,w=.05):
    if w:
        b=ob.modifiers.new("Manufactured soft edge","BEVEL");b.width=w;b.segments=3
        n=ob.modifiers.new("Weighted normals","WEIGHTED_NORMAL");n.keep_sharp=True

def cube(name,xyz,dim,mat,edge=.05):
    bpy.ops.mesh.primitive_cube_add(size=1,location=xyz)
    ob=register(name,mat);ob.dimensions=dim
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    bevel(ob,edge);return ob

def cylinder(name,xyz,r,depth,mat,rotate=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=depth,location=xyz)
    ob=register(name,mat)
    if rotate:ob.rotation_euler=rotate
    bevel(ob,.008)
    for face in ob.data.polygons:face.use_smooth=True

def archline(name,positions,mat,thickness=.05):
    c=bpy.data.curves.new(name,"CURVE");c.dimensions="3D"
    c.bevel_depth=thickness;c.resolution_u=20;c.bevel_resolution=2
    spline=c.splines.new("POLY");spline.points.add(len(positions)-1)
    for p,pos in zip(spline.points,positions):p.co=(*pos,1)
    ob=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(ob)
    ob.parent=ROOT[CURRENT];ob.data.materials.append(MAT[mat])
    GROUP[CURRENT].append(ob)

def caption(text,xyz):
    bpy.ops.object.text_add(location=xyz,rotation=(math.pi/2,0,0))
    ob=register("Manufacturer-neutral " + text,"dark")
    ob.data.body=text;ob.data.size=.077;ob.data.extrude=.001

def build_mass():
    # All parts are assembled in 3D, so the camera naturally occludes them.
    cube("Solid integrated lower machine plinth",(0,0,.17),(3.8,2.0,.30),"dark",.09)
    cube("Moulded underside",(0,0,.32),(3.66,1.9,.19),"grey",.06)
    cube("Main analyzer cabinet",(-.02,.14,1.02),(3.48,1.55,1.31),"white",.13)
    cube("Top service cover",(-.03,.12,1.72),(3.44,1.56,.13),"light",.06)
    cube("Front lower door",(-.65,-.663,.99),(1.85,.05,.95),"grey",.023)
    cube("Front inset door",(-.65,-.694,.99),(1.72,.017,.83),"white",.017)
    cube("Main screen bezel",(0,-.718,1.24),(.76,.05,.52),"dark",.025)
    cube("Main instrument readout",(0,-.750,1.24),(.64,.012,.40),"display",.015)
    cube("Service lock",(1.05,-.68,.94),(.53,.046,.72),"grey",.029)
    for i in range(8):
        cube("Left chassis real cooling slit "+str(i),(-1.78,-.46+i*.128,1.03),(.019,.074,.42),"dark",.010)
    cube("Rear maintenance cover",(.22,.937,1.16),(1.1,.02,.62),"grey",.020)
    for i in range(7):
        cube("Rear grille "+str(i),(-.18+i*.12,.959,1.19),(.063,.016,.40),"dark",.007)
    # Physically joined tower — ionizer on one side of the main cabinet.
    cube("Integrated ionizer riser",(-1.28,.38,1.79),(.98,.88,.25),"grey",.045)
    cube("Tall ion source enclosure",(-1.29,.39,2.37),(.86,.83,1.18),"white",.095)
    cube("Ionizer sealed top",(-1.29,.39,3.02),(.85,.84,.12),"light",.06)
    cube("Front tower filter frame",(-1.29,-.045,2.38),(.54,.027,.52),"metal",.022)
    cube("Blue dark-tinted service port",(-1.29,-.062,2.39),(.42,.010,.40),"dark",.012)
    for i in range(4):
        cube("Tower vent "+str(i),(-1.29,.816,2.24+i*.122),(.52,.018,.043),"dark",.009)
    # Legitimate autosampler holder, support and seven distinct tubes.
    cube("Supported autosampler underarm",(.63,-.95,.57),(1.80,.49,.15),"metal",.046)
    cube("Instrument specimen rack",(.63,-1.18,.70),(1.72,.50,.17),"dark",.048)
    cube("Machined vial mounting strip",(.63,-1.17,.82),(1.62,.43,.072),"metal",.018)
    for i in range(7):
        x=.02+i*.205
        cylinder("Glass lab vial "+str(i),(x,-1.18,1.01),.060,.30,"vial")
        cylinder("Blue sealed sample cap "+str(i),(x,-1.18,1.19),.073,.065,"blue")
    # Monitor, yoke, screen and keyboard all anchored to machine.
    cube("Monitor foot",(1.58,-.99,.52),(.37,.40,.14),"metal",.039)
    cylinder("Physical monitor stalk",(1.58,-1.00,.80),.056,.60,"metal")
    cube("Monitor swivel head",(1.58,-1.06,1.09),(.27,.17,.15),"grey",.023)
    cube("Monitor frame",(1.58,-1.15,1.43),(.90,.14,.72),"dark",.037)
    cube("Display glass",(1.58,-1.233,1.43),(.75,.011,.57),"display",.018)
    for i in range(8):
        cube("Readout plot "+str(i),(1.28+i*.082,-1.247,1.43+.10*math.sin(i)),(.049,.010,.018),"screen_light",.003)
    cube("Attached keyboard tray",(1.55,-1.45,.44),(.99,.40,.077),"metal",.032)
    for row in range(3):
        for col in range(7):
            cube("Typing cap %d.%d"%(row,col),(1.16+col*.128,-1.58+row*.11,.493),(.100,.077,.019),"keys",.005)
    caption("MASS SPECTROMETER",(-1.42,-.710,.50))

def build_digestion():
    cube("Laboratory digestion chassis",(0,0,.15),(3.70,2.12,.30),"dark",.087)
    cube("White moulded lower cabinet",(0,0,.50),(3.58,2.00,.67),"white",.12)
    cube("Sealed glass chamber gasket",(0,0,.89),(3.44,1.9,.095),"grey",.04)
    cube("Enclosed sample cavity floor",(0,0,1.01),(3.00,1.45,.09),"dark",.030)
    cube("Stainless carrier plate",(-.12,-.16,1.10),(2.40,.71,.11),"metal",.043)
    for i in range(6):
        x=-1.10+i*.38
        cylinder("Digestion reaction sample "+str(i),(x,-.18,1.32),.083,.38,"vial")
        cylinder("Lab tube collar "+str(i),(x,-.18,1.51),.088,.048,"metal")
    for i in range(4):
        cube("Enclosed heat well "+str(i),(-.81+i*.45,.40,1.12),(.27,.32,.07),"grey",.018)
    # Entire canopy is a genuine curved 3D surface with close-fitting frames.
    # This removes the floating SVG roof and fixes occlusion by solid geometry.
    count=28
    points=[]
    for x in (-1.46,1.46):
        for j in range(count+1):
            a=math.pi*j/count
            points.append((x,.93*math.cos(a),.96+1.0*math.sin(a)))
    faces=[(j,j+1,count+2+j,count+1+j) for j in range(count)]
    mesh=bpy.data.meshes.new("Continuous transparent hood")
    mesh.from_pydata(points,[],faces);mesh.update()
    ob=bpy.data.objects.new("Translucent curved protective glazing",mesh)
    bpy.context.collection.objects.link(ob)
    ob.parent=ROOT[CURRENT];ob.data.materials.append(MAT["glass"])
    GROUP[CURRENT].append(ob)
    for side,x in (("left",-1.53),("right",1.53)):
        arc=[(x,.95*math.cos(math.pi*j/count),.96+1.02*math.sin(math.pi*j/count)) for j in range(count+1)]
        archline("Continuous curved endcap "+side,arc,"metal",.065)
        cube("Endcap fixed foot "+side,(x,0,.95),(.17,1.89,.20),"light",.045)
    archline("Front structural glass sealing",[(-1.5,-.96,.96),(1.5,-.96,.96)],"dark",.051)
    archline("Rear structural glass sealing",[(-1.5,.96,.96),(1.5,.96,.96)],"dark",.051)
    cube("Real instrument control pod",(1.14,-1.02,.54),(.82,.065,.48),"grey",.038)
    cube("Inset controller housing",(1.14,-1.065,.59),(.59,.012,.31),"dark",.021)
    cube("Blue-tinted status LCD",(1.14,-1.075,.60),(.49,.010,.24),"display",.011)
    cylinder("Amber warning lamp",(.88,-1.083,.36),.040,.02,"amber",(math.pi/2,0,0))
    cylinder("Emergency red switch",(1.27,-1.091,.36),.054,.026,"red",(math.pi/2,0,0))
    cube("Rear lower servicing hatch",(0,1.03,.49),(1.90,.023,.38),"grey",.019)
    for i in range(8):
        cube("Rear exhaust strip "+str(i),(-.84+i*.23,1.052,.51),(.095,.014,.22),"dark",.008)
    cube("Side cabinet vent panel",(-1.82,0,.53),(.030,1.10,.36),"grey",.018)
    for i in range(8):
        cube("Side ventilating slit "+str(i),(-1.844,-.44+i*.126,.54),(.017,.066,.19),"dark",.006)
    caption("DIGESTION",(-1.40,-1.03,.40))

def build_scene():
    bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
    sc=bpy.context.scene
    sc.render.engine="CYCLES";sc.cycles.samples=14
    sc.render.resolution_x=384;sc.render.resolution_y=384
    sc.render.resolution_percentage=100
    sc.render.film_transparent=True
    sc.render.image_settings.file_format="PNG"
    sc.render.image_settings.color_mode="RGBA"
    sc.view_settings.view_transform="Standard"
    for args in [
      ("white","#e6e6e6",0,.33),("light","#f2f2f2",0,.28),
      ("grey","#cccccc",0,.35),("metal","#b3b3b3",.60,.31),
      ("dark","#394953",.12,.35),("blue","#3b73a2",.16,.29),
      ("display","#477d9c",.13,.20),("screen_light","#b6dfe7",0,.24),
      ("keys","#d2d9da",0,.48),("amber","#d5b66a",.12,.34),
      ("red","#a75b50",.10,.34)]:make_material(*args)
    make_material("vial","#d4e4ed",.03,.15,True)
    make_material("glass","#adc9d4",.03,.17,True)
    for model in MODELS:
        GROUP[model]=[]
        bpy.ops.object.empty_add(type="PLAIN_AXES")
        ROOT[model]=bpy.context.object
        ROOT[model].name="Editable model "+model
    global CURRENT
    CURRENT=MODELS[0];build_mass()
    CURRENT=MODELS[1];build_digestion()
    for name,pos,energy,diameter in [
       ("Wide key light",(-4,-5,7),530,5),
       ("Soft fill light",(4,2,6),340,4),
       ("Rear silhouette light",(-1,5,5),220,5)]:
        bpy.ops.object.light_add(type="AREA",location=pos)
        obj=bpy.context.object;obj.name=name;obj.data.energy=energy
        obj.data.shape="DISK";obj.data.size=diameter
    bpy.ops.object.camera_add(location=(6,-8,7))
    camera=bpy.context.object
    look=Vector((0,0,1.37))
    camera.rotation_euler=(look-camera.location).to_track_quat("-Z","Y").to_euler()
    camera.data.type="ORTHO";camera.data.ortho_scale=7.8
    sc.camera=camera;sc.world.color=(.67,.67,.67)

def tile(path):
    with Image.open(path) as original:
        img=original.convert("RGBA")
    bb=img.getchannel("A").getbbox()
    if not bb:raise RuntimeError("Blender rendered an empty direction frame")
    cropped=img.crop(bb)
    sc=min(116/cropped.width,110/cropped.height,1.4)
    cropped=cropped.resize((max(1,int(cropped.width*sc)),max(1,int(cropped.height*sc))),Image.Resampling.LANCZOS)
    cell=Image.new("RGBA",(128,128),(0,0,0,0))
    cell.alpha_composite(cropped,((128-cropped.width)//2,126-cropped.height))
    return cell

def run(out):
    out.mkdir(parents=True,exist_ok=True)
    build_scene()
    (out/"Sources").mkdir(exist_ok=True)
    blend=out/"Sources"/"ART001_original_editable_3D.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    sheet=Image.new("RGB",(1144,714),"#f5f6f3")
    draw=ImageDraw.Draw(sheet)
    try:
        big=ImageFont.truetype("DejaVuSans.ttf",24)
        normal=ImageFont.truetype("DejaVuSans.ttf",16)
    except OSError:big=ImageFont.load_default();normal=big
    draw.text((18,13),"ART-001  /  REAL BLENDER 3D SOURCE STUDY",font=big,fill="#253746")
    draw.text((18,48),"Original 3D mesh / normal shading / glass / 4 orthographic views / NOT game-ready",font=normal,fill="#596f80")
    sha={};boxes={}
    for row,m in enumerate(MODELS):
        for k in MODELS:
            for ob in GROUP[k]:ob.hide_render=(k!=m)
        draw.text((18,83+row*284),m.replace("_"," ").upper(),font=big,fill="#3b4e5b")
        for n,direction in enumerate(DIRECTIONS):
            ROOT[m].rotation_euler.z=n*math.pi/2
            temp=out/"temp-render.png"
            bpy.context.scene.render.filepath=str(temp)
            bpy.ops.render.render(write_still=True)
            t=tile(temp)
            path=out/"Native128"/(m+"_"+direction+".png")
            path.parent.mkdir(exist_ok=True)
            t.save(path)
            sha[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
            boxes[path.stem]=t.getchannel("A").getbbox()
            x=18+n*281;y=128+row*284
            sheet.paste(t,(x,y),t)
            zoom=t.resize((158,158),Image.Resampling.NEAREST)
            sheet.paste(zoom,(x+118,y-8),zoom)
            draw.text((x+22,y+144),direction+" 128px | 1x",font=normal,fill="#5c6d77")
    (out/"temp-render.png").unlink(missing_ok=True)
    draw.line((18,662,1126,662),fill="#bfcbd0",width=2)
    draw.text((18,682),"SOURCE-ONLY | NOT INSTALLABLE | no G1, no game XML, no gameplay or L4 acceptance",font=normal,fill="#687a85")
    output=out/"Previews"/"ART001_Blender_review.png"
    output.parent.mkdir(exist_ok=True);sheet.save(output)
    sha[output.name]=hashlib.sha256(output.read_bytes()).hexdigest()
    sha[blend.name]=hashlib.sha256(blend.read_bytes()).hexdigest()
    if len(boxes)!=8 or len({sha[m+"_"+d+".png"] for m in MODELS for d in DIRECTIONS})!=8:
        raise RuntimeError("No unique original art in eight directions")
    (out/"art_manifest.json").write_text(json.dumps({
      "schema":"ABCL-ART001-BLENDER-V1-REVIEW-ONLY",
      "source_only":True,"not_installable":True,"l4_tested":False,
      "models":list(MODELS),"directions":list(DIRECTIONS),
      "blender":bpy.app.version_string,"white_palette":GAME_WHITE,
      "cell":[128,128],"bounds":boxes,"sha256":sha
    },indent=2)+"\n")
    print("PASS: Blender editable .blend + eight unique 128px studies",flush=True)

def main():
    p=argparse.ArgumentParser();p.add_argument("--output",required=True,type=Path)
    out=p.parse_args().output.resolve()
    if any(x.lower() in ("streamingassets","addons") for x in out.parts):
        raise ValueError("Refusing to write inside a live game installation")
    run(out)
if __name__=="__main__":main()
