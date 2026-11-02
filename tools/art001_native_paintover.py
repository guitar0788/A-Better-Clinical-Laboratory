#!/usr/bin/env python3
"""Original 128px NW raster paintover of ABCL's Blender source: visual-only."""
import argparse,io,zipfile,hashlib,json
from pathlib import Path
from xml.etree.ElementTree import Element,SubElement,tostring
import numpy as np
from PIL import Image,ImageDraw,ImageFilter,ImageChops
def paint(source,destination):
    source=Image.open(source).convert("RGBA")
    if source.size!=(128,128):raise ValueError("Expected original ABCL 128px study")
    dst=Path(destination).resolve()
    if any(p.lower() in ("addons","streamingassets") for p in dst.parts):raise ValueError("No live game files")
    dst.mkdir(parents=True,exist_ok=True)
    px=np.asarray(source).copy()
    rgb=px[:,:,:3].astype(float);a=px[:,:,3]
    l=.2126*rgb[:,:,0]+.7152*rgb[:,:,1]+.0722*rgb[:,:,2]
    c=rgb.max(2)-rgb.min(2)
    neutral=(a>0)&(c<19)&(l>112)
    index=np.select([l>=221,l>=195,l>=155],[0,1,2],default=3)
    white=np.array([[242,242,242],[230,230,230],[204,204,204],[179,179,179]],dtype=np.uint8)
    px[neutral,:3]=white[index[neutral]]
    blue=(a>0)&(~neutral)&(rgb[:,:,2]>rgb[:,:,0]*1.12)&(l>=45)
    levels=np.select([l>=140,l>=100,l>=65],[0,1,2],default=3)
    colors=np.array([[150,185,200],[103,152,175],[65,110,138],[41,72,91]],dtype=np.uint8)
    px[blue,:3]=colors[levels[blue]]
    base=Image.fromarray(px,"RGBA")
    visible=source.getchannel("A").point(lambda v:255 if v>92 else 0)
    rim=ImageChops.subtract(visible,visible.filter(ImageFilter.MinFilter(3)))
    ink=Image.new("RGBA",(128,128),(39,45,49,0));ink.putalpha(rim)
    control=Image.new("RGBA",(128,128),(0,0,0,0))
    d=ImageDraw.Draw(control)
    d.rounded_rectangle((45,85,60,96),radius=1,fill=(54,81,101,238),outline=(37,45,52,250))
    d.line([(47,92),(50,91),(52,93),(55,88),(58,89)],fill=(159,218,223,255))
    d.rounded_rectangle((72,89,84,101),radius=1,fill=(47,72,90,245),outline=(34,43,50,255))
    d.line([(74,97),(76,95),(78,97),(80,94),(82,95)],fill=(161,205,216,255))
    d.line([(42,108),(66,110)],fill=(54,62,66,225),width=2)
    for j in range(6):
        x=43+j*4;y=100+j//4
        d.rounded_rectangle((x,y+3,x+3,y+9),radius=1,fill=(221,235,238,205),outline=(72,85,91,224))
        d.ellipse((x-1,y+1,x+3,y+4),fill=(57,116,177,255),outline=(34,65,101,240))
        d.point((x,y+2),fill=(140,190,215,245))
    d.line([(20,79),(21,100),(36,105)],fill=(102,107,112,160))
    d.rectangle((24,91,31,94),fill=(72,80,84,215))
    d.line([(25,92),(29,92)],fill=(180,180,175,225))
    d.line([(70,109),(85,112)],fill=(54,60,65,190))
    control.putalpha(ImageChops.multiply(control.getchannel("A"),visible.filter(ImageFilter.MaxFilter(3))))
    glint=Image.new("RGBA",(128,128),(0,0,0,0));d=ImageDraw.Draw(glint)
    d.line([(28,19),(36,16),(43,19)],fill=(255,255,255,150))
    d.line([(19,52),(32,47),(45,49)],fill=(250,250,248,110))
    d.line([(58,50),(71,54),(94,61)],fill=(255,255,255,90))
    glint.putalpha(ImageChops.multiply(glint.getchannel("A"),visible))
    layers=[("Original authored 3D base","base.png",base),("Ink contour","contour.png",ink),
       ("Front control paint","controls.png",control),("Neutral highlights","glints.png",glint)]
    final=base
    for _,__,layer in layers[1:]:final=Image.alpha_composite(final,layer)
    png=dst/"mass_spectrometer_NW_original_128.png";final.save(png)
    ora=dst/"mass_spectrometer_NW_editable_layers.ora"
    root=Element("image",{"w":"128","h":"128","name":"ART001 NW art-only review","version":"0.0.3"})
    stack=SubElement(root,"stack")
    for label,file,layer in reversed(layers):
        SubElement(stack,"layer",{"name":label,"src":"data/"+file,"visibility":"visible","opacity":"1.0","composite-op":"svg:src-over","x":"0","y":"0"})
    with zipfile.ZipFile(ora,"w") as z:
        z.writestr("mimetype","image/openraster",compress_type=zipfile.ZIP_STORED)
        z.writestr("stack.xml",tostring(root))
        for label,file,layer in layers:
            tmp=io.BytesIO();layer.save(tmp,"PNG");z.writestr("data/"+file,tmp.getvalue())
        tmp=io.BytesIO();final.save(tmp,"PNG");z.writestr("mergedimage.png",tmp.getvalue())
    m={"source":"original ABCL Blender, NOT vanilla",
      "visual_accepted":False,"game_l4":False,"not_installable":True,
      "direction":"NW","cell":[128,128],
      "sha256":{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (png,ora)}}
    (dst/"manifest.json").write_text(json.dumps(m,indent=2)+"\n")
    print("One original NW source-only raster art sprite delivered")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True);p.add_argument("--output",required=True)
    a=p.parse_args();paint(a.source,a.output)
