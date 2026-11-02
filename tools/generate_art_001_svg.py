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
from PIL import Image

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
           '</defs>']
    if mirrored:
        svg.append('<g transform="translate(128 0) scale(-1 1)">')
    svg += [
        '<ellipse cx="64" cy="111" rx="42" ry="6" fill="#637783" opacity=".15"/>'
    ]
    svg.extend(_enclosure([], device))
    svg.append(_instrument_detail(device, rear))
    if mirrored:
        svg.append('</g>')
    svg.append('</svg>')
    return ''.join(svg)


def image_hash(path, image):
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, "PNG", optimize=True)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate(root):
    root = Path(root)
    atlas = Image.new("RGBA", (2048, 1024), (0, 0, 0, 0))
    preview = Image.new("RGBA", (1024, 256), (250, 250, 247, 255))
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
            idx = di*4+ri
            atlas.alpha_composite(tile, (idx*CELL, 0))
            preview.alpha_composite(tile, (ri*256+64, di*CELL))
            slots[device][direction] = idx
    hashes["equipment_atlas.png"] = image_hash(
        root/"Assets"/"ABCL"/"equipment_atlas.png", atlas)
    hashes["direction_preview.png"] = image_hash(
        root/"Previews"/"ABCL"/"direction_preview.png", preview)
    for di, device in enumerate(DEVICES):
        icon = atlas.crop((di*4*CELL, 0, (di*4+1)*CELL, CELL))
        icon = icon.resize((64,64), Image.Resampling.LANCZOS)
        hashes[device+"_icon.png"] = image_hash(
            root/"Assets"/"ABCL"/(device+"_icon.png"), icon)
    manifest = {
        "schema": "ABCL-ART-001-v4-native-body-review-only",
        "authoring": "original editable detailed SVG; 4x supersampled, Lanczos",
        "atlas_layout": "LAYOUT_16_X_8",
        "atlas_size_px": [2048,1024], "cell_px": CELL,
        "directions": list(DIRECTIONS), "sprites": slots,
        "shared_pivot_px": [64,105], "sha256": hashes
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
