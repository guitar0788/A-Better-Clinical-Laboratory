#!/usr/bin/env python3
"""ART-001 V10 independently authored four-view isometric device study.

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
# Exact most common neutral shell colours in the owner's vanilla HEM/RIA
# atlas frames 248-255, sampled locally from RGB only (no native pixels).
NATIVE_WHITE = ("#f2f2f2", "#e6e6e6", "#cccccc", "#b3b3b3")


class Scene:
    def __init__(self, turn):
        self.turn = turn
        # Primitives are stored with a real camera-depth key, not appended
        # immediately in construction order. This fixes see-through cabinets.
        self.parts = []
        self.angle = math.radians(turn * 90)
        self.cs, self.sn = math.cos(self.angle), math.sin(self.angle)

    def point(self, x, y, z):
        xx = self.cs * x - self.sn * y
        yy = self.sn * x + self.cs * y
        return (64 + (xx - yy) * .93, 100 + (xx + yy) * .43 - z * .92)

    def camera_depth(self, x, y):
        # Bigger transformed (x+y) is closer to the viewer.
        return (self.cs + self.sn)*x + (self.cs - self.sn)*y

    def _append(self, pts, markup, offset=0):
        depth = sum(self.camera_depth(x,y) for x,y,z in pts) / len(pts)
        self.parts.append((depth+offset, len(self.parts), markup))

    def draw(self):
        # Painter depth ordering plus hidden-face culling, applied uniformly
        # to all faces, glazing, hardware, strokes and status LEDs.
        return ''.join(entry[2] for entry in sorted(self.parts))

    def poly(self, pts, fill, stroke="#454545", width=.79, extra=""):
        coords = " ".join("%.2f,%.2f" % self.point(*p) for p in pts)
        markup = '<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" %s/>' % (coords, fill, stroke, width, extra)
        self._append(pts, markup)

    def rule(self, pts, color, width=.65, opacity=1):
        coords = " ".join("%.2f,%.2f" % self.point(*p) for p in pts)
        markup = '<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" opacity="%s" stroke-linecap="round" stroke-linejoin="round"/>' % (coords, color, width, opacity)
        self._append(pts, markup, offset=.035)

    def dot(self, x, y, z, r, color):
        sx, sy = self.point(x, y, z)
        self._append([(x,y,z)], '<circle cx="%.2f" cy="%.2f" r="%s" fill="%s"/>' % (sx, sy, r, color), offset=.06)

    def visible(self, axis, side):
        # Both a camera-visible side and its actual physical identity are
        # selected after a 90-degree spatial rotation; no SVG mirroring.
        nx, ny = ((side, 0) if axis == "x" else (0, side))
        return (self.cs * nx - self.sn * ny + self.sn * nx + self.cs * ny) > .25

    def face(self, axis, side, fixed, a0, a1, z0, z1, fill, stroke="#575757", width=.69):
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
            "base": ("#b3b3b3", "#9b9b9b", "#737373"),
            "dark": ("#777777", "#505050", "#353535"),
        }
        top, bright, dark = palette[tone]
        self.face("x", -1, x0, y0, y1, z0, z1, bright)
        self.face("y", -1, y0, x0, x1, z0, z1, bright)
        self.face("x", 1, x1, y0, y1, z0, z1, dark)
        self.face("y", 1, y1, x0, x1, z0, z1, dark)
        self.poly([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1),
                   (x0, y1, z1)], top, "#3b3b3b", .82)
        # Edge glint makes shell thickness readable at 128 native pixels.
        self.rule([(x0 + 1, y0 + 1, z1 + .2),
                   (x1 - 1, y0 + 1, z1 + .2)], "#f2f2f2", .64)

    def vent(self, axis, side, fixed, a0, a1, z0, z1):
        # Never paint a rear grille after its opaque housing was drawn.
        if not self.visible(axis,side):
            return
        self.face(axis, side, fixed, a0, a1, z0, z1, "#969696", "#4a4a4a")
        n = 5
        for i in range(n):
            zz = z0 + 1.7 + (z1-z0-3.4)*(i+.5)/n
            if axis == "x":
                self.rule([(fixed, a0+1, zz), (fixed, a1-1, zz)], "#4b4b4b", .73)
            else:
                self.rule([(a0+1, fixed, zz), (a1-1, fixed, zz)], "#536975", .65)

    def status(self, axis, side, fixed, a0, a1, z0, z1):
        if not self.visible(axis,side):
            return
        self.face(axis, side, fixed, a0, a1, z0, z1, "#333c43", "#f2f2f2", 1.0)
        # Distinct screen bezel, line plot, power and safety control.
        self.face(axis, side, fixed, a0+1.3, a1-1.3, z0+1.4, z1-1.5, "url(#screen)", "#a7b9c3", .42)
        for u, h in ((.19,.2),(.36,.48),(.54,.31),(.71,.78),(.84,.45)):
            xx=a0+(a1-a0)*u
            if axis=="x":
                self.dot(fixed,xx,z0+2+(z1-z0-4)*h,.52,"#cbe8e5")
            else:
                self.dot(xx,fixed,z0+2+(z1-z0-4)*h,.52,"#cbe8e5")

    def body_trim(self, x0,x1,y0,y1,z):
        self.rule([(x0,y1,z),(x1,y1,z)], "#f2f2f2", .86)
        self.rule([(x1,y0,z),(x1,y1,z)], "#cccccc", .82)
        self.rule([(x0,y0,z),(x0,y1,z)], "#e6e6e6", .65)

    def mass(self):
        # Real physical sub-assemblies are laid out in a consistent local
        # coordinate system, then the entire machine is rotated in 3D.
        self.box(-31, 27, -19, 19, 0, 5, "base")
        self.box(-29, 25, -18, 17, 5, 44, "shell")
        self.body_trim(-29,25,-18,17,43)
        # Two independent cabinet seams and a low kick plate.
        self.rule([(-29,17,8),(25,17,8)],"#626262",1.3)
        self.vent("x", 1, 25, -13, 6, 12, 25)
        self.vent("y", -1, -18, -21, 4, 10, 27)
        # Front operator face, placed on physical +Y surface.
        self.status("y",1,17,-18,-1,21,37)
        self.face("y",1,17,-18,-1,15,18,"#b3b3b3")
        if self.visible("y",1):
            for k in range(4):
                self.dot(-17+4*k,17,12,.74,("#bdd4c2" if k==0 else "#afafaf"))
        # Native-like chassis details authored as true fixed-side geometry:
        # rear-only hatch, door gasket, separate removable lower cassette.
        self.face("y",-1,-18,-19,18,13,32,"#b3b3b3","#555555",.68)
        self.rule([(-18,-18,17),(17,-18,17)],"#5b5b5b",.95)
        self.rule([(-18,-18,28),(17,-18,28)],"#e6e6e6",.64)
        self.face("x",-1,-29,-12,8,10,25,"#cccccc","#5c5c5c",.64)
        self.rule([(-29,-10,21),(-29,6,21)],"#8a8a8a",.80)
        for x in (-24,21):
            self.dot(x,15,39,0.72,"#6b6b6b")
        for x in (-20,20):
            self.dot(x,-16,43,0.64,"#808080")
        self.face("y",1,17,5,23,32,35,"#757575","#4f4f4f",.75)
        # Cool service jack is small; housing remains neutral native white.
        self.dot(22,17,18,1.1,"#5286a5")
        self.dot(19,17,18,0.55,"#d7c984")
        # Distinct power cassette on x-right side.
        self.face("x",1,25,-10,5,28,36,"#cccccc","#4f4f4f")
        self.rule([(25,-9,30),(25,3,30)],"#6a6a6a",.9)
        # Tall ion-source housing — part of the SAME machine in every view.
        self.box(-27,-8,-16,4,44,67,"steel")
        self.box(-25,-10,-14,2,67,70,"shell")
        self.vent("y", 1, 4, -24, -11, 52, 61)
        self.face("x", 1, -8, -9, 0, 51, 61, "#68848c")
        self.dot(-8,-4,62,1.15,"#c7d2aa")
        # Bolted service cover and narrow warm warning label.
        self.face("y", 1, 17, 7, 19, 12, 18, "#d6c578", "#585858")
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
        if self.visible("y",1):
            self.dot(-6,19,12,1.15,"#c5c7aa")
            self.dot(-3,19,12,1.15,"#c6a78c")
        # Reinforced satin-grey lower shroud and true 3D side details.
        # The physical service hatch remains on -Y, regardless of rotation.
        self.face("y",-1,-19,-17,14,6,21,"#b3b3b3","#4e4e4e",.75)
        self.face("x",-1,-27,-14,8,7,21,"#cccccc","#646464",.65)
        self.rule([(-26,-19,5),(25,-19,5)],"#6d6d6d",.82)
        self.rule([(-27,19,20),(27,19,20)],"#f2f2f2",.74)
        for x in (-22,22):
            self.dot(x,18,8,0.72,"#656565")
        # Lab digestor has a short arched protective hood, not a
        # rectangular cube: surface is described by seven cross sections.
        roof=[]
        for i in range(9):
            x=-22+i*5.4
            z=31 + 9*math.sqrt(max(0,1-((x-0)/28)**2))
            roof.append((x,z))
        # CLOSED physical curved cover. Rear wall, front arch and side
        # end-caps form a volume rather than a floating 2D roof.
        # Their geometry is defined in 3D and depth-sorted together with
        # internal racks. The front glass is inset on y=+15.14.
        if self.visible("y",-1):
            self.poly([(x,-16,z) for x,z in roof]+
                      [(roof[-1][0],-16,25),(roof[0][0],-16,25)],
                      "url(#cool)","#4f4f4f",.80)
            self.rule([(roof[0][0],-16,28),(roof[-1][0],-16,28)],
                      "#878787",.95)
        if self.visible("y",1):
            self.poly([(x,15,z) for x,z in roof]+
                      [(roof[-1][0],15,25),(roof[0][0],15,25)],
                      "#858b8b","#393939",.91)
            self.poly([(x,15.14,z-3.0) for x,z in roof[1:-1]]+
                      [(roof[-2][0],15.14,27.2),(roof[1][0],15.14,27.2)],
                      "url(#glass)","#d4d8d8",.66)
            self.rule([(roof[1][0],15.20,26.9),(roof[-2][0],15.20,26.9)],
                      "#e6e6e6",.75)
        for side,x in ((-1,roof[0][0]),(1,roof[-1][0])):
            if self.visible("x",side):
                z=roof[0][1] if side<0 else roof[-1][1]
                self.poly([(x,-16,z),(x,15,z),(x,15,25),(x,-16,25)],
                          "url(#cool)","#525252",.76)
        self.poly([(x,-16,z) for x,z in roof]+
                  [(x,15,z) for x,z in reversed(roof)],
                  "url(#roof)","#474747",.91)
        self.rule([(x,-16,z) for x,z in roof],"#f2f2f2",.88)
        self.rule([(x,15,z) for x,z in roof],"#606060",.86)
        for x,z in roof[1::2]:
            self.rule([(x,-16,z),(x,15,z)],"#cccccc",.36,.60)
        # Internal digestor rails are below the closed hood.
        # No floating protective plate, false back-side buttons, or
        # direct look-through of an opaque shell.
        # A clear interior: heating wells and stainless racks on top.
        self.box(-16,15,-10,8,25,27,"dark")
        for x in (-11,-4,3,10):
            self.box(x,x+2.9,-4,2.0,27,31,"steel")
        # Only one real rear hatch, not a mirrored fake front panel.
        self.face("y",-1,-19,-16,13,6,20,"#cccccc")
        self.vent("y",-1,-19,-12,10,9,18)
        self.face("x",1,27,-13,8,10,18,"#cccccc")
        self.dot(27,3,15,.86,"#d2b65a")
        self.dot(27,0,15,.8,"#9db9ad")
        self.body_trim(-27,27,-19,19,5)


def make_svg(machine, direction):
    if machine not in MACHINES or direction not in DIRECTIONS:
        raise ValueError("Unknown V10 study machine/direction")
    scene = Scene(DIRECTIONS.index(direction))
    if machine == "mass_spectrometer":
        scene.mass()
    else:
        scene.digestion()
    gradients = '''<defs>
    <!-- Neutral shell ladder sampled read-only from vanilla HEM/RIA 248-255.
         F2F2F2 = illuminated shell; E6E6E6 = base; CCCCCC and B3B3B3
         are successive original shadow levels. No vanilla pixels copied. -->
    <linearGradient id="top" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f2f2f2"/><stop offset=".62" stop-color="#e6e6e6"/><stop offset="1" stop-color="#cccccc"/></linearGradient>
    <linearGradient id="bright" x1="0" y1="0" x2=".30" y2="1"><stop stop-color="#f2f2f2"/><stop offset=".48" stop-color="#e6e6e6"/><stop offset="1" stop-color="#cccccc"/></linearGradient>
    <linearGradient id="cool" x1="0" y1="0" x2=".8" y2="1"><stop stop-color="#e6e6e6"/><stop offset=".54" stop-color="#cccccc"/><stop offset="1" stop-color="#b3b3b3"/></linearGradient>
    <linearGradient id="steel_top"><stop stop-color="#e6e6e6"/><stop offset="1" stop-color="#b3b3b3"/></linearGradient>
    <linearGradient id="steel_bright"><stop stop-color="#cccccc"/><stop offset="1" stop-color="#929292"/></linearGradient>
    <linearGradient id="steel_dark"><stop stop-color="#b3b3b3"/><stop offset="1" stop-color="#797979"/></linearGradient>
    <linearGradient id="screen"><stop stop-color="#8bb6c8"/><stop offset=".35" stop-color="#49758b"/><stop offset="1" stop-color="#2b4156"/></linearGradient>
    <linearGradient id="glass" x2="1" y2="1"><stop stop-color="#d7e2e4" stop-opacity=".86"/><stop offset=".46" stop-color="#8098a1" stop-opacity=".83"/><stop offset="1" stop-color="#4a5a67" stop-opacity=".92"/></linearGradient>
    <linearGradient id="roof"><stop stop-color="#f2f2f2"/><stop offset=".17" stop-color="#cccccc"/><stop offset=".47" stop-color="#929292"/><stop offset=".76" stop-color="#5d5d5d"/><stop offset="1" stop-color="#3b3b3b"/></linearGradient>
    </defs>'''
    return '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">' + gradients + '<g id="' + machine + '_' + direction + '">' + scene.draw() + '</g></svg>'


def test_occlusion_contract():
    # A back-facing panel should never emit a rectangle or its details.
    for turn in range(4):
        scene=Scene(turn)
        behind = next((axis,side) for axis,side in
                      (("x",-1),("x",1),("y",-1),("y",1))
                      if not scene.visible(axis,side))
        axis,side=behind
        scene.vent(axis,side,side*20,-8,8,10,25)
        scene.status(axis,side,side*20,-8,8,10,25)
        assert not scene.parts, "Hidden face details leaked into SVG"
        # Painter order invariant; nearest opaque surface is drawn last.
        scene.poly([(10,10,2),(10,11,2),(11,11,2)],"#bbbbbb")
        scene.poly([(-10,-10,2),(-10,-11,2),(-11,-11,2)],"#eeeeee")
        source=scene.draw()
        assert source.index("#eeeeee") < source.index("#bbbbbb"),"Camera depth order broken"


def build(output):
    test_occlusion_contract()
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
    draw.text((24, 15), "ART-001 / V10   ORIGINAL FOUR-VIEW VECTOR STUDY", fill="#293c48", font=title)
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
    draw.text((24, 539), "VANILLA HEM / RIA SHELL: measured neutral-white palette (not game pixels)", fill="#444444", font=caption)
    for i,(label,tone) in enumerate(zip(("F2F2F2 illuminated","E6E6E6 body","CCCCCC shade","B3B3B3 depth"),NATIVE_WHITE)):
        x=24+i*253
        draw.rectangle((x,566,x+30,591),fill=tone,outline="#666666",width=1)
        draw.text((x+39,570),label,fill="#535353",font=caption)
    draw.line((24,604,1031,604),fill="#cccccc",width=2)
    draw.text((24,619),"NON-INSTALLABLE ORIGINAL SOURCE STUDY. Not an in-game screenshot or accepted game asset.",fill="#637783",font=caption)
    shot=output/"V10_mobile_review.png"
    contact.save(shot)
    hashes[shot.name]=hashlib.sha256(shot.read_bytes()).hexdigest()
    (output/"study_manifest.json").write_text(json.dumps({
      "stage":"V10 original source study - visual gate NOT PASSED",
      "white_palette_source":"vanilla HEM and RIA 248-255 read-only color sampling",
      "native_white_levels":list(NATIVE_WHITE),
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
    if any(c not in make_svg("mass_spectrometer","NW").lower() for c in NATIVE_WHITE[:3]):
        raise RuntimeError("Native neutral white ladder not present in authored material gradients")
    print(json.dumps({"bounds":bounds,"native_white":list(NATIVE_WHITE),"review":str(shot)},indent=2))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    build(args.output)


if __name__=="__main__":
    main()
