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


def make_svg(device, direction):
    if device not in DEVICES or direction not in DIRECTIONS:
        raise ValueError("Unknown ART-001 asset or direction")
    mirrored = direction in ("NE", "SW")
    rear = direction in ("SE", "SW")
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">']
    if mirrored:
        out.append('<g transform="translate(128 0) scale(-1 1)">')
    out.append('<ellipse cx="64" cy="105" rx="31" ry="3.5" fill="#687b82" opacity=".10"/>')
    # Muted medical enclosure with independent left/right diffuse lighting.
    top = 57 if device == "icp_ms" else 61
    out += [
        polygon('31,76 64,%s 97,76 64,94' % top, '#eaece8'),
        polygon('31,76 64,94 64,102 31,85', '#d0d7d6'),
        polygon('64,94 97,76 97,85 64,102', '#acbbbf'),
        polygon('32,86 64,102 64,105 32,89', '#71848e', "#71848e"),
        polygon('64,102 96,86 96,89 64,105', '#5d7581', "#5d7581"),
        line('M 32,77 L 64,95 L 96,77', '#f9f9f4', 1.25),
    ]
    if device == "icp_ms":
        # Vertical mass-filter unit and authentic benchtop vial carousel.
        out += [
            polygon('46,58 59,51 72,58 59,65', '#edf0eb'),
            polygon('46,58 59,65 59,84 46,77', '#cfd8d8'),
            polygon('59,65 72,58 72,77 59,84', '#aebdc1'),
            polygon('49,65 55,68 55,73 49,70', '#617d88'),
            line('M 49.5,66 L 54,68.5', '#a4c7d0'),
            polygon('75,77 85,71 95,77 85,83', '#a5b5b5'),
        ]
        for j in range(3):
            x = 78 + j*4
            out.append(rectangle(x, 69-(j%2), 2.3, 5.5, '#e8f0ee'))
            out.append(rectangle(x, 68-(j%2), 2.3, 1, '#96aab1'))
            out.append(line('M 64,%s l 5,-2.5' % (69+j*3), '#839da1'))
        if rear:
            out.append(polygon('37,82 51,90 51,96 37,88', '#9babad'))
            for j in range(3):
                out.append(line('M %s,%s l 5,3' % (39+j*3,84+j), '#798d94'))
        else:
            out += [
                polygon('37,82 51,90 51,96 37,88', '#5b7c87'),
                polygon('39,83 48,88 48,91 39,86', '#89b2c0'),
                rectangle(41,93,3,1.4,'#d4d8c4'),
            ]
    else:
        # Lower digestion hood with translucent glass and front/rear service.
        out += [
            polygon('39,69 64,56 89,69 64,83', '#dee1dc'),
            polygon('41,69 64,58 87,69 64,80', '#aebec0'),
            polygon('48,71 64,63 79,71 64,79',
                    '#708f97' if not rear else '#9caeb2'),
        ]
        if rear:
            for j in range(3):
                out.append(line('M %s,%s l 4,-2' % (55+j*4,73+j), '#728b92'))
            out.append(polygon('36,85 50,92 50,96 36,89', '#9aabad'))
        else:
            for j in range(3):
                out.append(rectangle(58+j*4,70+j*.5,2,4.5,'#dce9e8'))
            out += [
                polygon('36,85 50,92 50,96 36,89', '#6d8e9b'),
                line('M 38,87 L 48,92', '#b3d2d7'),
            ]
        out += [
            polygon('79,83 90,78 90,85 79,89', '#8b9ea2'),
            line('M 81,83 L 87,80', '#eff5f0'),
        ]
    if mirrored:
        out.append('</g>')
    out.append('</svg>')
    return ''.join(out)


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
        "schema": "ABCL-ART-001-v2-antialias-review-only",
        "authoring": "original editable SVG; 4x raster supersampling",
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
