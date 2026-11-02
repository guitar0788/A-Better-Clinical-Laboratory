#!/usr/bin/env python3
"""ART-001 art-only manually directed 2D ink/tones over original V3 NW 1024px.

One actual original game's *style study*, NOT original game pixels: hand-placed
mechanical strokes, local cabinet linework, screen graphics, vial highlights;
continuous anti-aliased paint source; editable layered OpenRaster; no install.
"""
import argparse,hashlib,io,json,zipfile
from pathlib import Path
from xml.etree.ElementTree import Element,SubElement,tostring
import numpy as np
from PIL import Image,ImageChops,ImageDraw,ImageFilter,ImageFont

def encode(im):
    s=io.BytesIO();im.save(s,format="PNG");return s.getvalue()

def hand_detailed_layer(alpha):
    img=Image.new("RGBA",(1024,1024));d=ImageDraw.Draw(img)
    dark=(61,65,68,215);steel=(176,187,193,205)
    white=(246,248,246,195);cyan=(154,200,211,240)
    # Original authored high-resolution manual curves following the actual
    # physical front/upper shell. Not a geometry/SVG/block generator.
    for points,color,width in [
      ([(276,398),(340,369),(422,332)],dark,5),
      ([(425,335),(506,369),(576,398),(651,432)],(103,107,110,120),4),
      ([(273,404),(314,388),(344,376)],white,6),
      ([(511,386),(579,417),(620,435)],white,4),
      ([(263,451),(369,484),(369,589)],dark,5),
      ([(276,463),(351,487)],white,5),
      ([(390,468),(395,497),(396,576)],(97,103,107,160),4),
      ([(325,182),(375,202),(422,184)],dark,4),
      ([(334,201),(336,299)],dark,5),
      ([(341,216),(347,289)],white,3),
      ([(341,320),(405,346),(443,332)],dark,5),
      ([(423,595),(430,595),(440,589),(450,592),(460,568),
        (470,590),(486,578),(493,595),(508,576),(521,590)],cyan,6),
      ([(424,599),(530,599)],(111,175,197,155),3),
      ([(555,508),(564,503),(570,507),(580,490),
        (588,500),(599,479),(613,495),(625,488)],cyan,5),
      ([(227,606),(308,632),(421,671)],white,6),
      ([(237,618),(305,638),(412,681)],(82,87,91,156),4),
    ]:d.line(points,fill=color,width=width,joint="curve")
    d.rounded_rectangle((339,264,346,273),radius=1,fill=(100,169,137,235))
    d.ellipse((631,460,641,470),fill=(108,192,163,235))
    d.rounded_rectangle((278,507,286,515),radius=1,fill=steel)
    for x,y in [(256,552),(283,559),(309,567),(335,574),
                 (360,585),(387,589),(416,599)]:
        d.arc((x-7,y-5,x+7,y+5),195,320,fill=(187,218,233,245),width=3)
        d.line([(x-6,y+14),(x-4,y+24)],fill=(235,239,237,165),width=3)
    for i in range(5):
        x=693+i*10
        d.line([(x,574-i*4),(x,622-i*4)],fill=(180,190,193,175),width=3)
    for row in range(2):
        for col in range(6):
            x=541+col*16-row*3;y=765+row*14+col*6
            d.line([(x,y),(x+7,y+2)],fill=white,width=2)
    img.putalpha(ImageChops.multiply(img.getchannel("A"),
                   alpha.filter(ImageFilter.MaxFilter(5))))
    return img

def neutral_paint(original):
    rgba=np.array(original,dtype=np.uint8)
    rgb=rgba[:,:,:3].astype(np.float32)
    lumin=rgb @ np.array([.2126,.7152,.0722],np.float32)
    neutral=(rgba[:,:,3]>12)&((rgb.max(2)-rgb.min(2))<24)&(lumin>105)
    strength=(np.clip((lumin-112)/110,.1,.8)*.45)
    new=rgb+(237-rgb)*(.22*strength[:,:,None])
    rgb[neutral]=new[neutral]
    rgba[:,:,:3]=np.clip(np.rint(rgb),0,255).astype(np.uint8)
    return Image.fromarray(rgba,"RGBA")

def contour(original):
    opacity=original.getchannel("A")
    outer=opacity.filter(ImageFilter.MaxFilter(7))
    rim=ImageChops.subtract(outer,opacity).filter(ImageFilter.GaussianBlur(.75))
    rim=rim.point(lambda v:round(v*.84))
    ink=Image.new("RGBA",(1024,1024),(46,49,51,0))
    ink.putalpha(rim)
    return ink

def ora(path,layers,merged):
    root=Element("image",{"w":"128","h":"128","version":"0.0.3",
                          "name":"ART001 original illustrated NW"})
    group=SubElement(root,"stack")
    for label,name,_ in reversed(layers):
        SubElement(group,"layer",{"name":label,"src":"data/"+name,
            "visibility":"visible","opacity":"1.0",
            "composite-op":"svg:src-over","x":"0","y":"0"})
    with zipfile.ZipFile(path,"w") as z:
        z.writestr("mimetype","image/openraster",compress_type=zipfile.ZIP_STORED)
        z.writestr("stack.xml",tostring(root))
        for label,name,im in layers:z.writestr("data/"+name,encode(im))
        z.writestr("mergedimage.png",encode(merged))

def build(srcfile,baseline,out):
    out=Path(out).resolve()
    if any(a.lower() in ("streamingassets","addons") for a in out.parts):
        raise ValueError("Never write inside an installed game directory")
    out.mkdir(parents=True,exist_ok=True)
    original=Image.open(srcfile).convert("RGBA")
    if original.size!=(1024,1024):
        raise ValueError("Require genuine original 1024px art source")
    neutral=neutral_paint(original);rim=contour(original)
    details=hand_detailed_layer(original.getchannel("A"))
    combined=Image.alpha_composite(Image.alpha_composite(rim,neutral),details)
    bounds=combined.getchannel("A").getbbox()
    if bounds is None:raise ValueError("Empty output")
    factor=min(112/(bounds[2]-bounds[0]),102/(bounds[3]-bounds[1]))
    w=round((bounds[2]-bounds[0])*factor)
    h=round((bounds[3]-bounds[1])*factor)
    def resize_art(layer):
        im=layer.crop(bounds).resize((w,h),Image.Resampling.LANCZOS)
        board=Image.new("RGBA",(128,128))
        board.alpha_composite(im,((128-w)//2,122-h))
        return board
    layers=[
       ("Continuous neutral-white cabinet painting","body.png",resize_art(neutral)),
       ("Original silhouette outline","outline.png",resize_art(rim)),
       ("Precisely positioned mechanical detail","mechanics.png",resize_art(details))]
    merged=Image.alpha_composite(
        Image.alpha_composite(layers[0][2],layers[1][2]),layers[2][2])
    sprite=out/"mass_spectrometer_NW_illustrated_128.png";merged.save(sprite)
    editable=out/"mass_spectrometer_NW_layered_art.ora"
    ora(editable,layers,merged)
    # Keep independently editable high-res illustration layers for professional
    # refinement: no original game sprite is inside this artifact.
    neutral.save(out/"NW_bodypaint_1024.png")
    rim.save(out/"NW_contour_1024.png")
    details.save(out/"NW_mechanical_ink_1024.png")
    old=Image.open(baseline).convert("RGBA")
    if old.size!=(128,128):raise ValueError("Comparison V3 must be 128px")
    preview=Image.new("RGB",(900,630),"#f0f2f4")
    draw=ImageDraw.Draw(preview)
    try:
        large=ImageFont.truetype("DejaVuSans.ttf",26)
        small=ImageFont.truetype("DejaVuSans.ttf",18)
    except OSError:large=ImageFont.load_default();small=large
    draw.text((24,20),"ART-001 | NW illustrated 2D style study",font=large,fill="#304453")
    draw.text((24,61),"Original source / smooth 128px / editable 2D ink / NOT game-ready",
              font=small,fill="#60727d")
    for i,(im,label) in enumerate([
       (old,"Previous V3: direct 3D render"),
       (merged,"New: original illustrated 2D paint")]):
        x=40+i*432
        draw.text((x,121),label,font=small,fill="#334f60")
        preview.paste(im,(x,164),im)
        zoom=im.resize((356,356),Image.Resampling.LANCZOS)
        preview.paste(zoom,(x,270),zoom)
    draw.text((24,606),"REVIEW ONLY | NO VANILLA ART | VISUAL GATE NOT PASSED",
              font=small,fill="#697784")
    picture=out/"NW_V3_vs_illustrated_mobile.png";preview.save(picture)
    items=[sprite,editable,picture]+list(out.glob("NW_*_1024.png"))
    manifest={
      "source":"ABCL original authored Blender V3 NW 1024px",
      "owner_visual_approved":False,"not_installable":True,
      "game_L4":False,"native_cell":[128,128],
      "filter":"Lanczos continuous alpha and shading; manual detail source",
      "native_bbox":merged.getchannel("A").getbbox(),
      "layers":3,
      "sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in items}}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print("ART001 NW illustration source-only PASS",flush=True)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True)
    p.add_argument("--baseline",required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    build(a.source,a.baseline,a.output)
