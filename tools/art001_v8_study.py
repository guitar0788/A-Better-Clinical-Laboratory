#!/usr/bin/env python3
"""ART-001 V8 independently authored four-view isometric device study.

Original 3D-consistent vector geometry; produces editable SVGs, native 128px
previews and a phone contact sheet. NOT a GameDB export or an installable addon.
No vanilla textures, game DLLs, or external art assets are used.
"""
import argparse
import hashlib
import json
import math
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

import cairosvg
from PIL import Image, ImageDraw, ImageFont

CELL = 128
DIRECTIONS = ("NW", "NE", "SE", "SW")
MACHINES = ("mass_spectrometer", "digestion_workstation")


class Scene:
    def __init__(self, turn):
        self.turn = turn
        self.parts = []
        self.angle = math.radians(turn * 90)
        self.cs, self.sn = math.cos(self.angle), math.sin(self.angle)

    def point(self, x, y, z):
        xx = self.cs * x - self.sn * y
        yy = self.sn * x + self.cs * y
        return (64 + (xx - yy) * .93, 100 + (xx + yy) * .43 - z * .92)

    def poly(self, pts, fill, stroke="#677780", width=.64, extra=""):
        coords = " ".join("%.2f,%.2f" % self.point(*p) for p in pts)
        self.parts.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" %s/>' %
                          (coords, fill, stroke, width, extra))

    def rule(self, pts, color, width=.65, opacity=1):
        coords = " ".join("%.2f,%.2f" % self.point(*p) for p in pts)
        self.parts.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" opacity="%s" stroke-linecap="round" stroke-linejoin="round"/>' %
                          (coords, color, width, opacity))

    def dot(self, x, y, z, r, color):
        sx, sy = self.point(x, y, z)
        self.parts.append('<circle cx="%.2f" cy="%.2f" r="%s" fill="%s"/>' % (sx, sy, r, color))

    def visible(self, axis, side):
        # Both a camera-visible side and its actual physical identity are
        # selected after a 90-degree spatial rotation; no SVG mirroring.
        nx, ny = ((side, 0) if axis == "x" else (0, side))
        return (self.cs * nx - self.sn * ny + self.sn * nx + self.cs * ny) > .25

    def face(self, axis, side, fixed, a0, a1, z0, z1, fill, stroke="#69757c", width=.55):
        if not self.visible(axis, side):
            return
        if axis == "x":
            p = [(fixed, a0, z0), (fixed, a1, z0),
                 (fixed, a1, z1), (fixed, a0, z1)]
        else:
            p = [(a0, fixed, z0), (a1, fixed, z0),
                 (a1, fixed, z1), (a0, fixed, z1)]
        self.poly(p, fill, stroke, width)

    def box(self, x0, x1, y0, y1, z0, z1, tone="shell"):
        palette = {
            "shell": ("url(#top)", "url(#bright)", "url(#cool)"),
            "steel": ("url(#steel_top)", "url(#steel_bright)", "url(#steel_dark)"),
            "base": ("#9eabb0", "#82939c", "#617783"),
            "dark": ("#7f919a", "#526a74", "#435865"),
        }
        top, bright, dark = palette[tone]
        self.face("x", -1, x0, y0, y1, z0, z1, bright)
        self.face("y", -1, y0, x0, x1, z0, z1, bright)
        self.face("x", 1, x1, y0, y1, z0, z1, dark)
        self.face("y", 1, y1, x0, x1, z0, z1, dark)
        self.poly([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1),
                   (x0, y1, z1)], top, "#65737a", .74)
        # Edge glint makes shell thickness readable at 128 native pixels.
        self.rule([(x0 + 1, y0 + 1, z1 + .2),
                   (x1 - 1, y0 + 1, z1 + .2)], "#fffefa", .58)

    def vent(self, axis, side, fixed, a0, a1, z0, z1):
        self.face(axis, side, fixed, a0, a1, z0, z1, "#899ba4", "#637880")
        n = 5
        for i in range(n):
            zz = z0 + 1.7 + (z1-z0-3.4)*(i+.5)/n
            if axis == "x":
                self.rule([(fixed, a0+1, zz), (fixed, a1-1, zz)], "#536975", .65)
            else:
                self.rule([(a0+1, fixed, zz), (a1-1, fixed, zz)], "#536975", .65)

    def status(self, axis, side, fixed, a0, a1, z0, z1):
        self.face(axis, side, fixed, a0, a1, z0, z1, "#344f5c", "#edf6f4", .85)
        # Distinct screen bezel, line plot, power and safety control.
        self.face(axis, side, fixed, a0+1.3, a1-1.3, z0+1.4, z1-1.5, "url(#screen)", "#7da4b2", .32)
        for u, h in ((.19,.2),(.36,.48),(.54,.31),(.71,.78),(.84,.45)):
            xx=a0+(a1-a0)*u
            if axis=="x":
                self.dot(fixed,xx,z0+2+(z1-z0-4)*h,.52,"#cbe8e5")
            else:
                self.dot(xx,fixed,z0+2+(z1-z0-4)*h,.52,"#cbe8e5")

    def body_trim(self, x0,x1,y0,y1,z):
        self.rule([(x0,y1,z),(x1,y1,z)], "#f5f6ee", .86)
        self.rule([(x1,y0,z),(x1,y1,z)], "#d2e2df", .82)
        self.rule([(x0,y0,z),(x0,y1,z)], "#dfe8e5", .65)

    def mass(self):
        # Real physical sub-assemblies are laid out in a consistent local
        # coordinate system, then the entire machine is rotated in 3D.
        self.box(-31, 27, -19, 19, 0, 5, "base")
        self.box(-29, 25, -18, 17, 5, 44, "shell")
        self.body_trim(-29,25,-18,17,43)
        # Two independent cabinet seams and a low kick plate.
        self.rule([(-29,17,8),(25,17,8)],"#718b96",1.3)
        self.vent("x", 1, 25, -13, 6, 12, 25)
        self.vent("y", -1, -18, -21, 4, 10, 27)
        # Front operator face, placed on physical +Y surface.
        self.status("y",1,17,-18,-1,21,37)
        self.face("y",1,17,-18,-1,15,18,"#a5b6bf")
        for k in range(4):
            self.dot(-17+4*k,17,12,.74,("#bdd4c2" if k==0 else "#9daeb4"))
        # Distinct power cassette on x-right side.
        self.face("x",1,25,-10,5,28,36,"#d3dcda","#75868d")
        self.rule([(25,-9,30),(25,3,30)],"#7b9298",.9)
        # Tall ion-source housing — part of the SAME machine in every view.
        self.box(-27,-8,-16,4,44,67,"steel")
        self.box(-25,-10,-14,2,67,70,"shell")
        self.vent("y", 1, 4, -24, -11, 52, 61)
        self.face("x", 1, -8, -9, 0, 51, 61, "#68848c")
        self.dot(-8,-4,62,1.15,"#c7d2aa")
        # Bolted service cover and narrow warm warning label.
        self.face("y", 1, 17, 7, 19, 12, 18, "#dfc777", "#6e787d")
        # Physical cassette ramp in front of the cabinet.
        self.box(1, 28, 17, 28, 17, 21, "steel")
        self.box(2, 26, 18, 27, 21, 24, "dark")
        for k in range(5):
            x=4+k*4.3
            self.box(x,x+2.4,20,23,24,31,"shell")
            self.box(x+.25,x+2.2,20.4,22.5,31,32.4,"dark")
        # No elliptical ground shadow: scene represents a tabletop asset.

    def digestion(self):
        self.box(-28,28,-20,20,0,4,"base")
        self.box(-27,27,-19,19,4,25,"shell")
        self.body_trim(-27,27,-19,19,24)
        self.vent("x",-1,-27,-11,7,8,20)
        self.vent("y",-1,-19,-19,13,8,17)
        self.status("y",1,19,-23,-9,7,18)
        self.dot(-6,19,12,1.15,"#c5c7aa")
        self.dot(-3,19,12,1.15,"#c6a78c")
        # Lab digestor has a short arched protective hood, not a
        # rectangular cube: surface is described by seven cross sections.
        roof=[]
        for i in range(9):
            x=-22+i*5.4
            z=31 + 9*math.sqrt(max(0,1-((x-0)/28)**2))
            roof.append((x,z))
        # Back shell and vertical lower trim; stainless ridges catch light.
        self.poly([(x,-16,z) for x,z in roof]+[(x,15,z) for x,z in reversed(roof)],
                  "url(#roof)","#657780",.69)
        for x,z in roof[1::2]:
            self.rule([(x,-16,z),(x,15,z)],"#e9efeb",.55,.75)
        # Single continuous safety glass cassette physically on +Y,
        # visible only from operator/front directions.
        self.face("y",1,19,-21,17,25,33,"#91aeb5","#f3f7f0",.88)
        self.face("y",1,19,-19,15,26,32,"url(#glass)","#a7cccf",.36)
        # A clear interior: heating wells and stainless racks on top.
        self.box(-16,15,-10,8,25,27,"dark")
        for x in (-11,-4,3,10):
            self.box(x,x+2.9,-4,2.0,27,31,"steel")
        # Only one real rear hatch, not a mirrored fake front panel.
        self.face("y",-1,-19,-16,13,6,20,"#bcc7c7")
        self.vent("y",-1,-19,-12,10,9,18)
        self.face("x",1,27,-13,8,10,18,"#899ba1")
        self.dot(27,3,15,.86,"#d3bd7d")
        self.dot(27,0,15,.8,"#a0d5b6")
        self.body_trim(-27,27,-19,19,5)


def make_svg(machine, direction):
    if machine not in MACHINES or direction not in DIRECTIONS:
        raise ValueError("Unknown V8 study machine/direction")
    scene = Scene(DIRECTIONS.index(direction))
    if machine == "mass_spectrometer":
        scene.mass()
    else:
        scene.digestion()
    gradients = '''<defs>
    <linearGradient id="top" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fafbf7"/><stop offset=".57" stop-color="#e8eeeb"/><stop offset="1" stop-color="#c5d0d1"/></linearGradient>
    <linearGradient id="bright" x1="0" y1="0" x2=".42" y2="1"><stop stop-color="#eef2ee"/><stop offset=".47" stop-color="#d5dedb"/><stop offset="1" stop-color="#a6b8ba"/></linearGradient>
    <linearGradient id="cool" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#d1dcdb"/><stop offset=".42" stop-color="#a9bac0"/><stop offset="1" stop-color="#81979e"/></linearGradient>
    <linearGradient id="steel_top"><stop stop-color="#edf2ee"/><stop offset="1" stop-color="#a9bac0"/></linearGradient>
    <linearGradient id="steel_bright"><stop stop-color="#dce5e3"/><stop offset="1" stop-color="#849aa3"/></linearGradient>
    <linearGradient id="steel_dark"><stop stop-color="#a7b8bc"/><stop offset="1" stop-color="#677b86"/></linearGradient>
    <linearGradient id="screen"><stop stop-color="#83b7c0"/><stop offset=".35" stop-color="#537e92"/><stop offset="1" stop-color="#293d58"/></linearGradient>
    <linearGradient id="glass" x2="1" y2="1"><stop stop-color="#d9ece8" stop-opacity=".92"/><stop offset=".46" stop-color="#8facb3" stop-opacity=".73"/><stop offset="1" stop-color="#476c82" stop-opacity=".85"/></linearGradient>
    <linearGradient id="roof"><stop stop-color="#f8faf5"/><stop offset=".28" stop-color="#d1dcda"/><stop offset=".75" stop-color="#9fb0b6"/><stop offset="1" stop-color="#667b83"/></linearGradient>
    </defs>'''
    return '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">' + gradients + '<g id="' + machine + '_' + direction + '">' + ''.join(scene.parts) + '</g></svg>'


def build(output):
    output = Path(output)
    source = output / "Sources"
    tiles = output / "Native128"
    source.mkdir(parents=True, exist_ok=True)
    tiles.mkdir(parents=True, exist_ok=True)
    contact = Image.new("RGB", (1056, 664), "#f6f6f3")
    draw = ImageDraw.Draw(contact)
    try:
        title = ImageFont.truetype("DejaVuSans.ttf", 22)
        caption = ImageFont.truetype("DejaVuSans.ttf", 15)
    except OSError:
        title = ImageFont.load_default()
        caption = title
    draw.text((24, 15), "ART-001 / V8   ORIGINAL FOUR-VIEW VECTOR STUDY", fill="#293c48", font=title)
    draw.text((24, 49), "No native game textures | 128px actual study cells | Visual approval pending", fill="#68777d", font=caption)
    hashes={}
    bounds={}
    for di,machine in enumerate(MACHINES):
        top=101+di*256
        draw.text((24,top-20), "MASS SPECTROMETER" if di==0 else "SAMPLE DIGESTION WORKSTATION",fill="#334a57",font=caption)
        for i,direction in enumerate(DIRECTIONS):
            content=make_svg(machine,direction)
            path=source/(machine+"_"+direction+".svg")
            path.write_text(content,encoding="utf-8")
            hashes[path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
            png=cairosvg.svg2png(bytestring=content.encode("utf-8"),output_width=512,output_height=512)
            im=Image.open(BytesIO(png)).convert("RGBA").resize((CELL,CELL),Image.Resampling.LANCZOS)
            bounds[path.stem]=im.getchannel("A").getbbox()
            tile=tiles/(machine+"_"+direction+".png")
            im.save(tile)
            hashes[tile.name]=hashlib.sha256(tile.read_bytes()).hexdigest()
            x=24+i*256
            # Native pixels shown at 1x inside a 128-cell, then an independent
            # enlarged comparison; no invented floor or workbench footprint.
            contact.paste(im,(x,top+11),im)
            doubled=im.resize((112,112),Image.Resampling.NEAREST)
            contact.paste(doubled,(x+132,top+18),doubled)
            draw.text((x+48,top+149),direction+" | 1x",fill="#47606b",font=caption)
            draw.text((x+133,top+149),"zoom",fill="#789099",font=caption)
    draw.line((24,604,1031,604),fill="#d5dddd",width=2)
    draw.text((24,619),"NON-INSTALLABLE ORIGINAL SOURCE STUDY. Not an in-game screenshot or accepted game asset.",fill="#637783",font=caption)
    shot=output/"V8_mobile_review.png"
    contact.save(shot)
    hashes[shot.name]=hashlib.sha256(shot.read_bytes()).hexdigest()
    (output/"study_manifest.json").write_text(json.dumps({
      "stage":"V8 original source study - visual gate NOT PASSED",
      "directions":list(DIRECTIONS),
      "machines":list(MACHINES),
      "cell":[128,128],
      "bounds":bounds,
      "file_sha256":hashes,
      "not_installable":True,
      "has_vanilla_pixels":False
    },indent=2)+"\n",encoding="utf-8")
    if len(bounds)!=8 or len({hashes[m+"_"+d+".png"] for m in MACHINES for d in DIRECTIONS})!=8:
        raise RuntimeError("Eight distinct physical orientations required")
    print(json.dumps({"bounds":bounds,"review":str(shot)},indent=2))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    build(args.output)


if __name__=="__main__":
    main()
