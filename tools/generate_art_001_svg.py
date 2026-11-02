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



def _surface_details(device, rear):
    """Additional original, smooth-rendered device detailing at atlas scale.

    Original game art is used for *style and proportions only*: no game
    geometry, textures or pixel rows are copied into this authored source.
    """
    out = [
        # A thin molded shell bevel and recesses at the side of the chassis.
        line('M 32,78 L 63,95 L 63,100', '#f7f8f3', .75),
        line('M 65,95 L 96,78', '#e0e5df', .85),
        line('M 33,84 L 62,100', '#95a4a5', .50),
        line('M 66,100 L 95,85', '#829298', .50),
        # Short instrument feet physically anchored to the same baseline.
        rectangle(39,88.0,4,2.2,'#647982'),
        rectangle(86,88.5,4,2.2,'#506a75'),
        # Miniature screws and a restrained safety marking.
        '<circle cx="34.7" cy="79" r=".70" fill="#748b90"/>',
        '<circle cx="94.2" cy="79" r=".70" fill="#748b90"/>',
        '<path d="M 69,93 l 4,-2 l 0,3 z" fill="#b7b6a3" stroke="#94968b" stroke-width=".28"/>',
    ]
    if device == "icp_ms":
        # Slightly inset anodized sample carousel, not an enormous machine.
        out.extend([
            polygon('75,77 85,71 95,77 85,83','url(#sample_tray)','#6f878d'),
            polygon('75.9,76.7 85,72 93.5,76.8 85,81.8','#d8e1de','#95a7a7'),
            '<ellipse cx="85" cy="76.8" rx="3.5" ry="1.6" fill="#90a7aa" stroke="#687f87" stroke-width=".4"/>',
            # Ionizer upper-unit metallic edges and ventilation ribs.
            line('M 46.6,58.9 L 59.5,65.3 L 71.5,58.8', '#f7f8f5', .8),
            line('M 47,59.6 L 47,76 L 58.5,83.5', '#9ba9aa', .5),
            line('M 59.5,66 L 59.5,83', '#fafbf6', .7),
            rectangle(63.8,70,1,5,'#819ba1'),
            rectangle(65.6,69,1,5,'#8b9da0'),
            rectangle(67.4,68,1,5,'#859a9e'),
            # A thin side-mounted sample holder / small connector lead.
            line('M 74,79 Q 76,75 79,74', '#7c9298', .7),
        ])
        for j in range(4):
            x=76.5+j*4
            out += [
                rectangle(x,68.8+(j%2),2.3,4.4,'url(#vial_glass)'),
                rectangle(x+.15,68.5+(j%2),2,1,'#9aafb5'),
                line('M %s,%s l 0,3.2' %(x+.7,70+j%2), '#fafffb', .45),
            ]
        if rear:
            out += [
                polygon('37.5,81.5 51.5,89.2 51.5,95.5 37.5,88','#aebbb9','#859497'),
                line('M 40,84.2 L 49,89.1', '#718c93',.65),
            ]
            for k in range(5):
                out.append(line('M %s,%s l 4,2.2' %(39+k*1.6,85.2+k*.85),'#779095',.42))
        else:
            out += [
                polygon('37.2,82 51,89.2 51,95 37.2,87.7','url(#panel_dark)','#7b949a'),
                polygon('38.5,82.7 49,88 49,90.4 38.5,85.1','#79a9b1','#a9c2c4'),
                line('M 40,92.0 L 48.5,96.1','#eef1e8',.55),
                rectangle(45,94.7,2.5,1.1,'#b6bda2'),
            ]
    else:
        # Enclosed digester with physical door frame and tiny internal tubes.
        out += [
            polygon('39,69 64,56 89,69 64,83','url(#lid_highlight)','#939fa3'),
            line('M 41,69 L 64,57.7 L 86.8,69','#fafbf5',1),
            line('M 42,71 L 64,82 L 87,70','#bec9c7',.7),
            polygon('48,71 64,63 79,71 64,79',
                    '#6c8d96' if not rear else '#9fadb0','#83989b'),
            # Edge-brightened glass reflection.
            line('M 50,70.6 L 63,64.4','#c5d9d6',.55),
            line('M 63,77.4 L 75,71.5','#d9e4df',.44),
            # Lid hinge and rear access screw caps.
            rectangle(54,61.9,2.6,1.1,'#8f9ea1'),
            rectangle(74,62.3,2.6,1.1,'#919fa1'),
            # Safety-glove interlock indicator.
            '<circle cx="83.5" cy="84.2" r="1" fill="#c4b795" stroke="#8b9391" stroke-width=".38"/>',
        ]
        if rear:
            for j in range(5):
                out.append(line('M %s,%s l 3.8,-1.8' %(56+j*2.2,72+j*.95),'#71878d',.45))
            out.append(line('M 40,88 L 48,92','#7b8d93',.5))
        else:
            for j in range(4):
                x=56+j*3.2
                out += [
                    rectangle(x,69.8+(j%2)*.5,1.8,5.5,'url(#vial_glass)'),
                    rectangle(x+.2,69.4+(j%2)*.5,1.3,.9,'#a8c5c3'),
                ]
            out += [
                polygon('37,84.3 49,91 49,95 37,88.2','url(#panel_dark)','#8e9fa2'),
                line('M 39,86.3 L 46.5,90.7','#bbd4d4',.65),
            ]
        for j in range(4):
            out.append(line('M %s,%s l 2.8,-1.2' %(81+j*1.6,85-j*.8),'#e2e8e2',.42))
    return ''.join(out)


def make_svg(device, direction):
    if device not in DEVICES or direction not in DIRECTIONS:
        raise ValueError("Unknown ART-001 asset or direction")
    mirrored = direction in ("NE", "SW")
    rear = direction in ("SE", "SW")
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">',
           '<defs>',
           '<linearGradient id="sample_tray" x2=".9" y2="1"><stop stop-color="#dbe6e2"/><stop offset="1" stop-color="#8da7ad"/></linearGradient>',
           '<linearGradient id="vial_glass" x2="1" y2=".7"><stop stop-color="#f7faf6" stop-opacity=".96"/><stop offset=".55" stop-color="#b6d0d1" stop-opacity=".77"/><stop offset="1" stop-color="#72919a" stop-opacity=".72"/></linearGradient>',
           '<linearGradient id="lid_highlight" x2=".7" y2="1"><stop stop-color="#f4f5ef"/><stop offset=".62" stop-color="#e1e7e3"/><stop offset="1" stop-color="#a8b8bb"/></linearGradient>',
           '<linearGradient id="panel_dark" x2="1" y2="1"><stop stop-color="#7695a1"/><stop offset="1" stop-color="#475e69"/></linearGradient>',
           '</defs>',
           '<g transform="translate(64 106) scale(1.18) translate(-64 -106)">']
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
    out.append(_surface_details(device, rear))
    if mirrored:
        out.append('</g>')
    out.append('</g>')  # native-scale enlargement, same baseline for all views
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
        "schema": "ABCL-ART-001-v3-detail-review-only",
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
