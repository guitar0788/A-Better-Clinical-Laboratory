#!/usr/bin/env python3
"""FA-1 / TO-001: purpose-authored room/floor visuals, no native asset copying.

MENU: 64x64 original analytic flask. FLOOR: independent 256x128 isometric
illustration of the same flask, downsampled to the TS private 128x64 tile.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
from xml.etree import ElementTree as ET

import cairosvg
from PIL import Image, ImageDraw, ImageFont

NS = '{http://www.w3.org/2000/svg}'
RECT = (1024, 1472, 1152, 1536)


def raster(path, size):
    raw = Path(path).read_bytes()
    if any(q in raw.lower() for q in (b'<script', b'<image', b'<use', b'href=', b'url(', b'javascript:')):
        raise ValueError('External or executable SVG resources are forbidden')
    tree = ET.fromstring(raw)
    if tree.tag != NS+'svg' or tree.get('viewBox') != '0 0 %s %s' % size:
        raise ValueError('Wrong original vector viewBox')
    if b'#F2F2F2' not in raw:
        raise ValueError('Expected native white only')
    if any(c in raw.lower() for c in (b'#c93f3d', b'#999999', b'#54847f')):
        raise ValueError('Native zone color must not be baked into glyph')
    hi = cairosvg.svg2png(bytestring=raw, output_width=size[0]*4, output_height=size[1]*4)
    with Image.open(io.BytesIO(hi)) as image:
        return image.convert('RGBA').resize(size, Image.Resampling.LANCZOS)


def build(room_svg, out):
    room_svg = Path(room_svg).resolve()
    floor_svg = room_svg.with_name('toxicology_floor_glyph.svg')
    out = Path(out).resolve()
    if any(p.lower() in ('streamingassets', 'addons') for p in out.parts):
        raise ValueError('Refuse original game/install directories')
    room, floor = raster(room_svg, (64, 64)), raster(floor_svg, (256, 128))
    b = lambda img: img.getchannel('A').point(lambda v: 255 if v > 127 else 0).getbbox()
    if b(room) != (19, 15, 45, 50) or b(floor) != (61, 11, 196, 121):
        raise ValueError('Original-size drawing footprint changed')
    private = floor.resize((128, 64), Image.Resampling.LANCZOS)
    if b(private) != (31, 6, 98, 61):
        raise ValueError('TS private atlas footprint mismatch')
    atlas = Image.new('RGBA', (2048, 2048), (0, 0, 0, 0))
    atlas.paste(private, RECT[:2])
    out.mkdir(parents=True, exist_ok=True)
    for name, img in (('toxicology_floor_glyph_256x128.png', floor),
                      ('toxicology_floor_glyph_128x64.png', private),
                      ('toxicology_floor_atlas_private_376.png', atlas)):
        img.save(out/name)
    review = Image.new('RGB', (750, 420), '#eff1f3')
    d = ImageDraw.Draw(review)
    try:
        font = ImageFont.truetype('DejaVuSans.ttf', 16)
        heading = ImageFont.truetype('DejaVuSans.ttf', 22)
    except OSError:
        font = heading = ImageFont.load_default()
    d.text((20, 20), 'FA-1 TO-001 | native menu / oblique floor', font=heading, fill='#263b48')
    d.text((20, 58), 'Simulated UI backdrops ONLY; not embedded in private source sprites.', font=font, fill='#47616f')
    menu_preview = Image.new('RGBA', (64, 64), '#c93f3d')
    menu_preview.alpha_composite(room)
    floor_preview = Image.new('RGBA', (256, 128), '#697880')
    floor_preview.alpha_composite(floor)
    d.text((30, 110), 'MENU / 64x64', font=font, fill='#394b55')
    d.text((280, 110), 'FLOOR / 256x128', font=font, fill='#394b55')
    review.paste(menu_preview.convert('RGB'), (30, 150))
    review.paste(menu_preview.resize((160, 160), Image.Resampling.LANCZOS).convert('RGB'), (101, 150))
    review.paste(floor_preview.convert('RGB'), (280, 150))
    review.paste(floor_preview.resize((360, 180), Image.Resampling.LANCZOS).convert('RGB'), (275, 227))
    preview = out/'TO001_original_size_art_review.png'
    review.save(preview)
    paths = [out/n for n in ('toxicology_floor_glyph_256x128.png',
                             'toxicology_floor_glyph_128x64.png',
                             'toxicology_floor_atlas_private_376.png')] + [preview]
    manifest = {
        'issue': 24, 'stage': 'FA_L2_ONLY',
        'room_source': 'assets/art/to001/toxicology_room_icon.svg',
        'floor_source': 'assets/art/to001/toxicology_floor_glyph.svg',
        'separate_surface_art': True, 'same_flask_motif': True,
        'native_room_size': [64, 64], 'vanilla_floor_cell': [256, 128],
        'native_floor_bbox': list(b(floor)), 'private_floor_bbox': list(b(private)),
        'ts_private_atlas': [2048, 2048], 'ts_grid': [16, 32],
        'tile_376_rect': list(RECT), 'no_baked_room_color': True,
        'no_native_game_asset_copy': True, 'non_installable': True,
        'game_L3': False, 'game_L4': False, 'owner_visual_approved': False,
        'sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in (room_svg, floor_svg)}
    }
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print('FA L2 source-only: authored distinct native room/floor surfaces')
    return manifest


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--room-svg', required=True)
    p.add_argument('--output', required=True)
    a = p.parse_args()
    build(a.room_svg, a.output)
