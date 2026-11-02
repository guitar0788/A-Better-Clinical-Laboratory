#!/usr/bin/env python3
"""ART-001 smooth original equipment artwork proof (NOT an installable game addon).

Generate editable SVG sources and antialiased sprites at native 128px cells.
No game-owned bitmap is read or copied. Offline build requires Pillow+CairoSVG.
"""
import argparse
import hashlib
import json
from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont

CELL = 128
DIRECTIONS = ("NW", "NE", "SE", "SW")
DEVICES = ("icp_ms", "digestion_station")


def polygon(points, color, stroke="#8c9395"):
    return ('<polygon points="%s" fill="%s" stroke="%s" '
            'stroke-width=".8" stroke-linejoin="round"/>' %
            (points, color, stroke))


def line(d, color="#869299", width=".8"):
    return ('<path d="%s" fill="none" stroke="%s" '
            'stroke-width="%s" stroke-linejoin="round" '
            'stroke-linecap="round"/>' % (d, color, width))


def rectangle(x, y, w, h, color):
    return '<rect x="%s" y="%s" width="%s" height="%s" fill="%s" rx=".6"/>' % (x, y, w, h, color)



def _enclosure(svg, device):
    """Integrated tabletop analyzer body, authored independently of game art."""
    if device == "icp_ms":
        svg += [
            polygon("26,68 56,51 87,66 57,83", "url(#ivory_top)", "#555c5f"),
            polygon("26,68 57,83 57,105 26,88", "url(#left_face)", "#555c5f"),
            polygon("57,83 87,66 87,88 57,105", "url(#right_face)", "#555c5f"),
            polygon("28,87 57,103 57,109 28,93", "#596a74", "#596a74"),
            polygon("57,103 85,87 85,93 57,109", "#485d68", "#485d68"),
            line("M 27.5,70 L 56.7,86 L 86,68", "#f8f8f1", .9),
            # The upright integrated analyser is part of the enclosure,
            # not a cube resting on a separate blank tabletop.
            polygon("39,48 55,39 72,48 56,58", "#edf0ec", "#626d70"),
            polygon("39,48 56,58 56,91 39,82", "url(#left_face)", "#5e696b"),
            polygon("56,58 72,48 72,82 56,91", "url(#right_face)", "#59666b"),
            line("M 40,49 L 56,59 L 71,50", "#fffefa", 1),
            # Smooth molded trim and drain channels.
            line("M 28.5,74 L 28.5,87 L 55,102", "#f3f5f0", .65),
            line("M 58.5,104 L 85,89", "#bbc7c4", .6),
            rectangle(30,90,3.5,2.5,"#66767a"),
            rectangle(80,90,3,2.5,"#607377"),
        ]
    else:
        svg += [
            # Low enclosed laboratory digestor, unlike tall ICP housing.
            polygon("24,70 63,48 103,69 64,91", "url(#ivory_top)", "#555d62"),
            polygon("24,70 64,91 64,110 24,89", "url(#left_face)", "#626a6d"),
            polygon("64,91 103,69 103,90 64,110", "url(#right_face)", "#5b676e"),
            polygon("25,88 64,109 64,114 25,93", "#5b7180", "#5a6e78"),
            polygon("64,109 102,88 102,93 64,114", "#4e6674", "#4f626c"),
            line("M 25.5,71 L 64,92.5 L 101.5,71", "#fafaf4", 1),
            # Rounded-ish protective upper lid with glass reaction chamber.
            polygon("31,62 63,45 96,62 64,80", "url(#ivory_top)", "#6b7578"),
            polygon("31,62 64,80 64,91 31,74", "#a9b9bc", "#687579"),
            polygon("64,80 96,62 96,74 64,91", "#a5b3b7", "#67757b"),
            line("M 32,63 L 64,81 L 95,63", "#f5f5f0", .9),
            # Rear ventilation slits, distinct service profile.
            line("M 34,75 L 61,90", "#738993", .5),
            line("M 67,89 L 94,75", "#84969a", .5),
            rectangle(32,92,3.8,2.5,"#687a80"),
            rectangle(95,92,3.8,2.5,"#667a80"),
        ]
    return svg


def _instrument_detail(device, rear):
    svg = []
    if device == "icp_ms":
        if rear:
            svg += [
                polygon("30,72 52,84 52,97 30,85", "#a6b4b6", "#747f83"),
                polygon("62,85 81,75 81,88 62,99", "#9eafb2", "#667e85"),
            ]
            for j in range(5):
                svg.append(line(
                    "M %s,%s l 9,5" % (33+j*2.8,76+j*1.5), "#556c75", .65))
                svg.append(line(
                    "M %s,%s l 7,-4" % (64+j*2.1,90-j*.9), "#526974", .55))
            svg += [
                rectangle(40,93,4.1,1.5,"#4a626d"),
                '<circle cx="48.4" cy="96.2" r=".95" fill="#bcab84"/>',
                line("M 44,43 L 68,55", "#e9edea", .7),
            ]
        else:
            # A legible 14x12 LCD screen and control membrane as in the
            # visual grammar of real original clinical lab equipment.
            svg += [
                polygon("29,73 53,86 53,101 29,88", "#82969c", "#60747d"),
                polygon("32,76 49,85 49,94 32,85", "url(#screen_blue)", "#526c77"),
                line("M 33,77 L 48,85", "#c2d7d8", .7),
                line("M 34,82 L 42,86", "#88c7cc", .55),
                line("M 35,85 L 47,92", "#679eaf", .45),
                rectangle(36,90,2,1.5, "#a4d9cf"),
                rectangle(40,92,2,1.5, "#d9ddc7"),
                line("M 32,87 L 52,98", "#d4ddda", .5),
            ]
        # Narrow, tall ion-source tower with a steel filter and product
        # silhouette continuity. Low-saturation panel status and screws.
        svg += [
            polygon("43,51 55,44 67,51 55,58", "url(#ivory_top)", "#626d71"),
            polygon("43,51 55,58 55,80 43,73", "#d8dfdc", "#6f7d7e"),
            polygon("55,58 67,51 67,73 55,80", "#aebdc1", "#64777d"),
            line("M 44,53 L 54,59 L 65,53", "#fffefa", .8),
            polygon("46.5,59.5 51.7,62 51.7,67.7 46.5,65", "#7c98a0", "#81969e"),
            '<circle cx="49.2" cy="71" r="1.0" fill="#94c6bd"/>',
            '<circle cx="60.3" cy="77" r=".8" fill="#6f8790"/>',
        ]
        for j in range(4):
            svg.append(line(
                "M %s,%s l 5,-2.8" % (58,61+j*2.7), "#69868d", .55))
        # A physical carousel outside the main cabinet footprint.
        svg += [
            polygon("74,74 93,65 108,72 88,82", "#adbfc1", "#52666e"),
            polygon("75,73 93,66 106,72 88,79", "url(#sample_tray)", "#8ca1a2"),
            line("M 75,74 L 88,80 L 105,72", "#f4f6ee", .8),
        ]
        for k in range(5):
            x=78+k*4.5
            y=67+(k%2)*1.2
            svg += [
                rectangle(x,y,2.4,7,"url(#vial_glass)"),
                rectangle(x+.25,y-.9,2,1.6,"#8aa5b0"),
                line("M %s,%s v 4" % (x+.5,y+1), "#fcfdf9", .35),
            ]
        svg += [
            rectangle(86,76,2.7,1.4,"#849ba2"),
            line("M 70,76 Q 74,75 78,72", "#a7bcbd",.9),
        ]
    else:
        if rear:
            # Back of sealed digester has ventilation and power service,
            # not an impossible transparent front window.
            svg += [
                polygon("35,66 64,52 92,65 64,81", "#a6b4b6", "#6d7d80"),
                polygon("31,76 60,92 60,102 31,86", "#9daeb3", "#778a8f"),
            ]
            for j in range(6):
                svg.append(line(
                    "M %s,%s l 7,-3.5" % (48+j*3,69+j*.45), "#617781", .6))
                svg.append(line(
                    "M %s,%s l 4,2.4" % (35+j*3.7,81+j*1.9), "#617780", .55))
            svg += [
                polygon("70,93 97,78 97,84 70,99", "#839a9e", "#607680"),
                '<circle cx="92" cy="86" r=".9" fill="#d3c397"/>',
            ]
        else:
            # Enclosed tempered glass with visible sample tubes.
            svg += [
                polygon("37,62 63,49 88,62 63,76", "#809fa4", "#5c777f"),
                polygon("40,62 63,51 85,62 63,74", "url(#glass_blue)", "#9bafb0"),
                line("M 42,63 L 60,54", "#e1eded", .7),
                line("M 64,72 L 82,63", "#d3e5e3", .6),
                polygon("29,76 60,93 60,103 29,86", "#7d989c", "#5b7780"),
                polygon("32,79 52,90 52,95 32,84", "url(#screen_blue)", "#587681"),
                line("M 33,80 L 51,89", "#b2d6d6", .65),
            ]
            for j in range(6):
                svg += [
                    rectangle(49+j*4.7,62.7+(j%2)*.6,2.4,6,"url(#vial_glass)"),
                    rectangle(49.3+j*4.7,61.5+(j%2)*.6,1.8,1.4,"#9caba5"),
                ]
            svg += [
                rectangle(38,89,3,2,"#d4dfd6"),
                rectangle(43,92,2.5,2,"#c8d1c9"),
            ]
        svg += [
            # Fan grille and a side LED retain identity across all views.
            polygon("73,90 94,78 94,84 73,96", "#8b9fa3", "#647983"),
            line("M 75,90 L 91,81", "#d2ddda",.65),
            '<circle cx="89" cy="87.5" r="1.1" fill="#c0b78b"/>',
            '<circle cx="91.5" cy="86.3" r=".7" fill="#8fb4ad"/>',
        ]
    return ''.join(svg)



def _digestion_hood_body(rear):
    """A curved protective top, avoiding the previous rectangular tank look."""
    shade = "#9daeb1" if rear else "#57656c"
    out = [
        # An independent original curved shell over the inner heating cavity.
        '<path d="M 32,66 Q 33,55 45,52 L 63,43 Q 74,40 82,48 '
        'L 95,57 Q 99,61 95,67 L 65,83 L 33,68 Z" '
        'fill="url(#hood_shell)" stroke="#6f7b7c" stroke-width=".85" '
        'stroke-linejoin="round"/>',
        line("M 34,64 Q 37,57 46,54 L 64,45 Q 72,44 78,49", "#f3f5ee", .85),
        line("M 36,68 L 65,82 L 94,66", "#c6d3d0", .50),
        '<path d="M 40,65 Q 41,60 49,56 L 63,49 L 81,57 '
        'L 85,63 L 63,76 Z" fill="%s" opacity=".88" '
        'stroke="#71888c" stroke-width=".60"/>' % shade,
    ]
    if rear:
        for k in range(4):
            out.append(line("M %s,%s l 7,-3" % (46+k*6, 64+k*.1),
                            "#73898d", .70))
    else:
        # Front safety glass and glass reflections before micro detail pass.
        out += [
            '<path d="M 44,64 L 63,53 L 79,61 L 63,70 Z" '
            'fill="url(#glass_blue)" stroke="#99b3b5" stroke-width=".45"/>',
            line("M 45,63 L 62,54", "#f3f7f0", .60),
        ]
    return "".join(out)


def _material_finish(device, rear):
    """Extra authored housing fit/finish at final game cell dimensions.

    All geometry is original. Native RIA/hematology sprites were used as
    visual references for subdued panels, moulded seams and service access,
    never as source geometry or pixels.
    """
    out = []
    # One restrained molded rim, chassis seam and soft left/right
    # illumination. Shadows are sub-pixel in the final 128px output.
    if device == "icp_ms":
        out += [
            line("M 27,69 L 57,84 L 86,68", "#f9faf6", .68),
            line("M 28.5,70 L 28.5,87 L 56.5,104", "#bac5c4", .45),
            line("M 58.5,104 L 85,88", "#a4b5b7", .50),
            line("M 30,89 L 57,104 L 57,107", "#9bb0b4", .35),
            # Tall side module: filter-service split and metallic gasket.
            line("M 39.8,51.5 L 39.8,80.5", "#edf0ea", .68),
            line("M 40.4,69 L 54,76", "#aebdc0", .45),
            line("M 57,58.5 L 57,89", "#f8faf6", .55),
            '<circle cx="42.4" cy="51.6" r=".54" fill="#72848b"/>',
            '<circle cx="67" cy="53" r=".48" fill="#72848b"/>',
            # Thin horizontal status slot: meaningful controls, not neon.
            polygon("37,98 48,104 48,105.4 37,99.3","#dce4e1","#869ba0"),
            rectangle(41,96.3,1.9,1.4,"#b4cebd"),
            rectangle(45,98.7,1.9,1.2,"#a7b8ae"),
        ]
        if rear:
            out += [
                # Back utility socket and pressure label.
                polygon("67,93 78,87 78,91.5 67,97.5","#5b727a","#758c92"),
                line("M 70,93 L 74,91", "#d3dcd7", .38),
                '<circle cx="81.2" cy="86.2" r=".65" fill="#d0c8af"/>',
            ]
        else:
            out += [
                # LCD glass specular reflection over lit original front.
                polygon("33.1,76.9 39,80 39,81.5 33.1,78.4","#c5e4e3","#95c1bf"),
                line("M 35,88.5 L 45,94", "#d4e3de", .40),
                '<circle cx="45.3" cy="98.3" r=".7" fill="#a8c4b6"/>',
            ]
        # Five sample vials stand in a curved carousel rather than
        # floating independently above the chassis.
        out += [
            line("M 76,74 L 89,81 L 105,73", "#edf1eb", .50),
            line("M 74,73 L 83,69", "#7b989f", .40),
        ]
    else:
        out += [
            # Continuous enclosure seams and a smooth safety-lid latch.
            line("M 26,71 L 64,92.5 L 101,72", "#fcfaf3", .75),
            line("M 24.5,88.8 L 63,110", "#9aaeb1", .46),
            line("M 65,109.8 L 101,89", "#899ba0", .46),
            line("M 32,63.3 L 63.8,81 L 95,63.5", "#fafbf4", .60),
            line("M 34,74 L 61,88.8", "#d4dfdc", .55),
            polygon("62,78.2 66,76.3 70,78.2 66,80.5",
                    "#dce2de","#76878c"),
            rectangle(61.2,80.6,5.4,1.8,"#657d86"),
            '<circle cx="37.6" cy="76.7" r=".65" fill="#6d8085"/>',
            '<circle cx="95" cy="76.7" r=".65" fill="#72848b"/>',
            # A small main power switch on the lower rear cabinet.
            polygon("74,94 83,89 83,92.5 74,97.2",
                    "#788e93","#65777f"),
            '<circle cx="79.9" cy="92" r=".7" fill="#a5c5b1"/>',
        ]
        if rear:
            out += [
                polygon("45,86 55,91 55,93 45,88",
                        "#e1e9e4","#a1b4b8"),
                '<circle cx="88" cy="82.6" r=".68" fill="#b1c7c2"/>',
            ]
        else:
            out += [
                # Condensation on the inspection glass, not a painted box.
                line("M 48,62 L 61,56", "#e0efea", .45),
                line("M 53,72 L 62,76.2", "#bdd8d3", .40),
                line("M 37,80 L 48,86", "#b3cfd2", .42),
                rectangle(42,96,2.4,1.2,"#bdc7b7"),
            ]
    return "".join(out)


def make_svg(device, direction):
    """Original, smooth 2D isometric equipment with four coherent views."""
    if device not in DEVICES or direction not in DIRECTIONS:
        raise ValueError("Unknown ART-001 asset or direction")
    mirrored = direction in ("NE", "SW")
    rear = direction in ("SE", "SW")
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">',
           '<defs>',
           '<linearGradient id="ivory_top" x2="1" y2=".8"><stop stop-color="#f9f9f5"/><stop offset=".5" stop-color="#e6e9e5"/><stop offset="1" stop-color="#d7dcd9"/></linearGradient>',
           '<linearGradient id="left_face" x2=".45" y2="1"><stop stop-color="#e9eeea"/><stop offset="1" stop-color="#bcc7c8"/></linearGradient>',
           '<linearGradient id="right_face" x2=".8" y2="1"><stop stop-color="#d7dedd"/><stop offset="1" stop-color="#9cabb1"/></linearGradient>',
           '<linearGradient id="screen_blue" x2=".7" y2="1"><stop stop-color="#6c9fae"/><stop offset="1" stop-color="#3b6479"/></linearGradient>',
           '<linearGradient id="glass_blue" x2="1" y2=".7"><stop stop-color="#a7c6c5" stop-opacity=".93"/><stop offset=".55" stop-color="#7398a2" stop-opacity=".95"/><stop offset="1" stop-color="#456c79"/></linearGradient>',
           '<linearGradient id="vial_glass" x2="1" y2=".7"><stop stop-color="#f7faf6" stop-opacity=".98"/><stop offset=".48" stop-color="#bdd1d4" stop-opacity=".83"/><stop offset="1" stop-color="#8ca9af" stop-opacity=".87"/></linearGradient>',
           '<linearGradient id="sample_tray" x2=".9" y2="1"><stop stop-color="#e0e6de"/><stop offset=".7" stop-color="#bacacc"/><stop offset="1" stop-color="#85989f"/></linearGradient>',
           '<linearGradient id="hood_shell" x2=".65" y2="1"><stop stop-color="#eceeeb"/><stop offset=".45" stop-color="#c2cbcb"/><stop offset="1" stop-color="#778a90"/></linearGradient>',
           '</defs>']
    # The native renderer maps the complete 128x128 cell onto a 1x1
    # object quad. Align authored contact shadows/feet with the bottom edge.
    # Targets are measured from the supplied vanilla sprites: HEM NW
    # bbox=(7,20,126,128), RIA NW bbox=(8,43,108,127).
    # Apply device-specific enlargement around the common current baseline
    # (y=117) so the mass spectrometer matches HEM scale and the lower
    # digestion unit matches RIA scale without changing its physical design.
    sx, sy = ((1.20, 1.55) if device == "icp_ms" else (1.16, 1.273))
    svg.append('<g transform="translate(64 127) scale(%s %s) translate(-64 -117)">' % (sx, sy))
    # Existing authored geometry is kept intact inside the new native-cell
    # registration transform; no geometry is re-created per direction.
    svg.append('<g transform="translate(0 18.5) scale(1 .835)">')
    if mirrored:
        svg.append('<g transform="translate(128 0) scale(-1 1)">')
    svg += [
        '<ellipse cx="64" cy="111" rx="42" ry="6" fill="#637783" opacity=".11"/>'
    ]
    svg.extend(_enclosure([], device))
    if device == "digestion_station":
        svg.append(_digestion_hood_body(rear))
    svg.append(_instrument_detail(device, rear))
    svg.append(_material_finish(device, rear))
    if mirrored:
        svg.append('</g>')
    svg.append('</g>')  # original art coordinate transform
    svg.append('</g>')  # native cell baseline / scale correction
    svg.append('</svg>')
    return ''.join(svg)


def image_hash(path, image):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG", optimize=True)
    return hashlib.sha256(path.read_bytes()).hexdigest()




def dilate_transparent_rgb(image, radius=2):
    """Bleed nearest visible RGB beneath transparent pixels without changing alpha.

    Applied per 128px cell before atlas assembly so linear texture filtering
    cannot pull black transparent RGB into antialiased edges or leak colours
    between neighbouring atlas cells.
    """
    if radius < 0:
        raise ValueError("radius must be non-negative")
    rgba = image.convert("RGBA")
    width, height = rgba.size
    source = list(rgba.getdata())
    output = source.copy()
    radius_sq = radius * radius
    for y in range(height):
        for x in range(width):
            index = y * width + x
            if source[index][3] != 0:
                continue
            nearest = None
            nearest_distance = radius_sq + 1
            for dy in range(-radius, radius + 1):
                ny = y + dy
                if ny < 0 or ny >= height:
                    continue
                for dx in range(-radius, radius + 1):
                    distance = dx * dx + dy * dy
                    if distance == 0 or distance > radius_sq or distance > nearest_distance:
                        continue
                    nx = x + dx
                    if nx < 0 or nx >= width:
                        continue
                    candidate = source[ny * width + nx]
                    if candidate[3] == 0:
                        continue
                    nearest = candidate
                    nearest_distance = distance
            if nearest is not None:
                output[index] = (nearest[0], nearest[1], nearest[2], 0)
    rgba.putdata(output)
    return rgba


def make_workbench_icon_svg():
    """Original 64px isometric workbench icon; no vanilla pixels are copied."""
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
      <defs>
        <linearGradient id="bench_top" x2=".8" y2="1">
          <stop stop-color="#f1f3ef"/><stop offset="1" stop-color="#c9d2d0"/>
        </linearGradient>
        <linearGradient id="bench_side" x2="0" y2="1">
          <stop stop-color="#c2ccca"/><stop offset="1" stop-color="#84969b"/>
        </linearGradient>
      </defs>
      <ellipse cx="32" cy="53" rx="20" ry="3.2" fill="#6e8188" opacity=".14"/>
      <path d="M9 23 L31 11 L55 23 L33 36 Z" fill="url(#bench_top)" stroke="#65747a" stroke-width="1.15" stroke-linejoin="round"/>
      <path d="M9 23 L33 36 L33 41 L9 28 Z" fill="#b5c1c1" stroke="#65747a" stroke-width=".9"/>
      <path d="M33 36 L55 23 L55 28 L33 41 Z" fill="url(#bench_side)" stroke="#65747a" stroke-width=".9"/>
      <path d="M14 29 L14 46 L18 49 L18 32" fill="#aab8b8" stroke="#687b80" stroke-width=".85"/>
      <path d="M48 28 L48 44 L44 47 L44 31" fill="#94a5a8" stroke="#687b80" stroke-width=".85"/>
      <path d="M18 45 L44 45 L48 43" fill="none" stroke="#6b7d82" stroke-width="1.7" stroke-linecap="round"/>
      <path d="M17 31 L32 39 L47 31" fill="none" stroke="#f9faf5" stroke-width=".8"/>
      <rect x="26" y="21" width="12" height="2.2" rx=".7" fill="#9aadb0" opacity=".8"/>
      <circle cx="47" cy="25" r="1.1" fill="#9db7ad"/>
    </svg>'''


def _icon_canvas(svg):
    """Render artwork inside the game's 60x60 safe area of a 64px icon."""
    rendered = Image.open(BytesIO(cairosvg.svg2png(
        bytestring=svg.encode("utf-8"), output_width=256,
        output_height=256))).convert("RGBA")
    inner = rendered.resize((60, 60), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    canvas.alpha_composite(inner, (2, 2))
    return dilate_transparent_rgb(canvas, radius=2)


def generate(root):
    root = Path(root)
    atlas = Image.new("RGBA", (2048, 1024), (0, 0, 0, 0))
    preview = Image.new("RGBA", (1024, 256), (250, 250, 247, 255))
    # Separate enlarged review sheet for phone screens. This is explicitly
    # 2x display scaling, NOT an additional native texture or game bitmap.
    mobile = Image.new("RGBA", (1024, 752), (249, 249, 246, 255))
    draw = ImageDraw.Draw(mobile)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 20)
        small_font = ImageFont.truetype("DejaVuSans.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
        small_font = font
    draw.text((24, 8), "Mass Spectrometer", fill=(59, 72, 79), font=font)
    draw.text((555, 12), "NW / NE / SE / SW  |  2x review",
              fill=(109, 122, 127), font=small_font)
    draw.text((24, 282), "Sample Digestion Workstation", fill=(59, 72, 79), font=font)
    draw.text((24, 573), "CUSTOM UI ICONS  |  64x64 RGBA  |  60x60 SAFE AREA",
              fill=(59, 72, 79), font=small_font)
    draw.text((24, 731), "SOURCE 128x128 PER VIEW  |  NOT AN IN-GAME SCREENSHOT",
              fill=(119, 128, 129), font=small_font)
    slots = {}
    hashes = {}
    for di, device in enumerate(DEVICES):
        slots[device] = {}
        for ri, direction in enumerate(DIRECTIONS):
            svg = make_svg(device, direction)
            svg_file = root / "Sources" / "ABCL" / (device + "_" + direction + ".svg")
            svg_file.parent.mkdir(parents=True, exist_ok=True)
            svg_file.write_text(svg, encoding="utf-8")
            hashes[svg_file.name] = hashlib.sha256(svg.encode("utf-8")).hexdigest()
            rendered = Image.open(BytesIO(cairosvg.svg2png(
                bytestring=svg.encode("utf-8"), output_width=512,
                output_height=512))).convert("RGBA")
            tile = rendered.resize((CELL, CELL), Image.Resampling.LANCZOS)
            tile = dilate_transparent_rgb(tile, radius=2)
            idx = di*4+ri
            # paste preserves RGB beneath zero-alpha pixels for texture filtering.
            atlas.paste(tile, (idx*CELL, 0))
            preview.alpha_composite(tile, (ri*256+64, di*CELL))
            scaled = tile.resize((216, 216), Image.Resampling.LANCZOS)
            px = ri * 256 + 20
            py = (42 if di == 0 else 314)
            mobile.alpha_composite(scaled, (px, py))
            draw.text((ri * 256 + 113, py + 216),
                      direction, fill=(64, 77, 84), font=small_font)
            slots[device][direction] = idx
    hashes["equipment_atlas.png"] = image_hash(
        root/"Assets"/"ABCL"/"equipment_atlas.png", atlas)
    hashes["direction_preview.png"] = image_hash(
        root/"Previews"/"ABCL"/"direction_preview.png", preview)
    for di, device in enumerate(DEVICES):
        tile = atlas.crop((di*4*CELL, 0, (di*4+1)*CELL, CELL))
        icon = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        icon.paste(tile.resize((60, 60), Image.Resampling.LANCZOS), (2, 2))
        icon = dilate_transparent_rgb(icon, radius=2)
        icon_x = 24 + di * 334
        mobile.alpha_composite(icon.resize((96, 96), Image.Resampling.LANCZOS),
                               (icon_x, 602))
        icon_label = ("Mass Spectrometer" if di == 0 else "Digestion Station")
        draw.text((icon_x + 108, 642), icon_label,
                  fill=(59, 72, 79), font=small_font)
        hashes[device+"_icon.png"] = image_hash(
            root/"Assets"/"ABCL"/(device+"_icon.png"), icon)
    workbench_svg = make_workbench_icon_svg()
    icon_source = root/"Sources"/"ABCL"/"workbench_icon.svg"
    icon_source.parent.mkdir(parents=True, exist_ok=True)
    icon_source.write_text(workbench_svg, encoding="utf-8")
    hashes["workbench_icon.svg"] = hashlib.sha256(
        workbench_svg.encode("utf-8")).hexdigest()
    workbench_icon = _icon_canvas(workbench_svg)
    hashes["workbench_icon.png"] = image_hash(
        root/"Assets"/"ABCL"/"workbench_icon.png", workbench_icon)
    mobile.alpha_composite(
        workbench_icon.resize((96, 96), Image.Resampling.LANCZOS),
        (692, 602))
    draw.text((800, 642), "Instrument Workbench",
              fill=(59, 72, 79), font=small_font)
    hashes["review_mobile.png"] = image_hash(
        root/"Previews"/"ABCL"/"review_mobile.png", mobile)
    manifest = {
        "schema": "ABCL-ART-001-v7-native-bounds-review-only",
        "authoring": "original editable SVG; 4x supersampled, Lanczos",
        "atlas_layout": "LAYOUT_16_X_8",
        "atlas_size_px": [2048,1024], "cell_px": CELL,
        "directions": list(DIRECTIONS), "sprites": slots,
        "icons": {"icp_ms":"icp_ms_icon.png",
                  "digestion_station":"digestion_station_icon.png",
                  "workbench":"workbench_icon.png"},
        "shared_baseline_y_px": 127,
        "alpha_edge_rgb_bleed_px": 2,
        "mobile_review_size_px": [1024, 752],
        "mobile_review_includes_custom_icons": True,
        "sha256": hashes
    }
    (root/"art_manifest.json").write_text(
        json.dumps(manifest, indent=2)+"\n", encoding="utf-8")
    return manifest


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args=parser.parse_args()
    print(generate(args.output)["sha256"]["equipment_atlas.png"])


if __name__ == "__main__":
    main()
