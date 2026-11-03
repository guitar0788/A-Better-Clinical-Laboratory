#!/usr/bin/env python3
"""TO-001 FA: native-size WHITE-GLYPH-ONLY original room symbols.

White foreground is identical in normal/disabled resources by design:
the game UI must handle native room color, tint and disabled state.
No game atlas, room-zone RGB, UI state color or clinical resources are altered.
"""
import argparse
import hashlib
import io
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont

FILENAME = ('toxicology_room_icon.png', 'toxicology_room_icon_inactive.png')
NATIVE_GLYPH = '#F2F2F2'
LAB_PALETTE_REFERENCE = {'active': '#C93F3D', 'inactive': '#999999'}
IDS = ('ASSET_ABCL_TOXICOLOGY_ROOM_ICON',
       'ASSET_ABCL_TOXICOLOGY_ROOM_ICON_INACTIVE')
ROOM_ID = 'ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB'
ATLAS_REFERENCE_BBOX = {
    'hematology_850': [20, 14, 44, 49],
    'microbiology_2868': [14, 16, 50, 47],
    'histology_854': [16, 15, 48, 48],
}

def glyph_bbox(image, cutoff=127):
    points = [(x, y) for y in range(64) for x in range(64)
              if image.getpixel((x, y))[3] > cutoff]
    if not points:
        raise ValueError('No visible glyph')
    return (min(x for x, y in points), min(y for x, y in points),
            max(x for x, y in points)+1, max(y for x, y in points)+1)

def rasterize(svg_path):
    source = Path(svg_path).read_bytes()
    root = ET.fromstring(source)
    if root.tag != '{http://www.w3.org/2000/svg}svg' or root.get('viewBox') != '0 0 64 64':
        raise ValueError('Expected original editable 64px SVG')
    if b'#F2F2F2' not in source:
        raise ValueError('Expected neutral-white original LAB foreground')
    if any(color in source.lower() for color in
           (b'#c93f3d', b'#999999', b'#54847f')):
        raise ValueError('Room background/tint must NOT be baked into artwork')
    high = cairosvg.svg2png(bytestring=source, output_width=512, output_height=512)
    with Image.open(io.BytesIO(high)) as image:
        art = image.convert('RGBA').resize((64, 64), Image.Resampling.LANCZOS)
    if any(art.getpixel((x, y))[3] for x in range(64) for y in range(64)
           if x < 2 or y < 2 or x >= 62 or y >= 62):
        raise ValueError('Native Rect(2,2,60,60) cropping unsafe')
    bbox = glyph_bbox(art)
    if not (23 <= bbox[2]-bbox[0] <= 32 and 30 <= bbox[3]-bbox[1] <= 36):
        raise ValueError('Original laboratory glyph visible footprint mismatch: ' + str(bbox))
    if not (17 <= bbox[0] <= 22 and 42 <= bbox[2] <= 47 and
            14 <= bbox[1] <= 19 and 45 <= bbox[3] <= 51):
        raise ValueError('Off-center glyph: ' + str(bbox))
    if art.getpixel((10, 10))[3] or art.getpixel((54, 54))[3]:
        raise ValueError('Background embedded or icon too large')
    if len({p[3] for p in art.getdata() if 0 < p[3] < 255}) < 14:
        raise ValueError('Failed smooth antialiasing contract')
    return art, bbox

def preview(active, disabled, path):
    # RED/GRAY are simulated UI state backdrops in a review sheet ONLY:
    # absolutely neither exported foreground sprite contains these pixels.
    board = Image.new('RGB', (916, 545), '#F1F3F3')
    d = ImageDraw.Draw(board)
    try:
        title = ImageFont.truetype('DejaVuSans.ttf', 23)
        font = ImageFont.truetype('DejaVuSans.ttf', 16)
    except OSError:
        title = ImageFont.load_default()
        font = title
    d.text((26, 18), 'TO-001 | Exact-size white glyph, no baked background',
           font=title, fill='#293D48')
    d.text((26, 56),
           'Original icon masks on simulated vanilla LAB state colors; not a game screenshot',
           font=font, fill='#60717C')
    for i, (icon, back, label) in enumerate(
        ((active, '#C93F3D', 'ACTIVE   (native red preview)'),
         (disabled, '#999999', 'DISABLED   (native gray preview)'))
    ):
        x = 29+i*447
        d.text((x, 103), label, font=font, fill='#384F5D')
        panel = Image.new('RGBA', (64, 64))
        painter = ImageDraw.Draw(panel)
        painter.rounded_rectangle((2, 2, 61, 61), radius=6, fill=back)
        panel.alpha_composite(icon)
        board.paste(panel, (x+8, 160), panel)
        zoom = panel.resize((320, 320), Image.Resampling.LANCZOS)
        board.paste(zoom, (x+104, 137), zoom)
        d.text((x+9, 237), '1x: 64px canvas', font=font, fill='#566D78')
        d.text((x+104, 473), '5x smooth zoom, not pixel art',
               font=font, fill='#566D78')
    d.text((29, 513),
           'Foreground only: actual game UI background/state integration must be verified by TS.',
           font=font, fill='#63727C')
    board.save(path)


def native_crop_preview(active, disabled, output):
    """Visual L2 proof of exact private IconManager Rect(2,2,60,60) crop.

    Red and gray are ONLY simulated behind the exported transparent glyph.
    No original atlas art or Unity runtime screenshot is written here.
    """
    canvas = Image.new('RGB', (766, 395), '#F1F3F3')
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype('DejaVuSans.ttf', 16)
        heading = ImageFont.truetype('DejaVuSans.ttf', 20)
    except OSError:
        font = heading = ImageFont.load_default()
    draw.text((18, 13), 'TO-001 | Exact 60px native crop test (SOURCE ONLY)',
              fill='#283D48', font=heading)
    for i, (glyph, color, label) in enumerate(
        [(active, '#C93F3D', 'Normal | preview red background'),
         (disabled, '#999999', 'Disabled | preview gray background')]
    ):
        cropped = glyph.crop((2, 2, 62, 62))
        # Original visible white footprint 26x32 within a 60px crop.
        if cropped.getchannel('A').point(lambda v: 255 if v > 127 else 0).getbbox() != (17, 14, 43, 46):
            raise ValueError('Native cropped glyph footprint changed')
        scene = Image.new('RGBA', (60,60), color)
        scene.alpha_composite(cropped)
        x = 18+i*380
        draw.text((x, 72), label, fill='#394B57', font=font)
        canvas.paste(scene.convert('RGB'), (x+4,113))
        enlarged = scene.resize((240,240), Image.Resampling.LANCZOS)
        canvas.paste(enlarged.convert('RGB'), (x+87,106))
        draw.text((x+4,180), 'Actual 60x60', fill='#5A6E78', font=font)
        draw.text((x+87,354), 'Smooth zoom for QA only', fill='#5A6E78', font=font)
    canvas.save(output)

def build(svg, inactive_svg, output):
    output = Path(output).resolve()
    if any(part.lower() in ('streamingassets', 'addons') for part in output.parts):
        raise ValueError('Refuse live game directory')
    output.mkdir(parents=True, exist_ok=True)
    icons = []
    boxes = []
    for filename, source in zip(FILENAME, (svg, inactive_svg)):
        icon, bbox = rasterize(source)
        icon.save(output/filename, optimize=False)
        icons.append(icon)
        boxes.append(bbox)
    # Native active/disabled source icon glyph is F2F2F2 in both states.
    # Deliberately leave panel, zoning, locked tint to TS/native UI logic.
    if icons[0].tobytes() != icons[1].tobytes():
        raise ValueError('State-dependent background color leaked into icon art')
    sheet = output/'to001_native_scale_preview.png'
    preview(*icons, sheet)
    cropped_review = output/'to001_native_60px_crop_preview.png'
    native_crop_preview(*icons, cropped_review)
    paths = [output/x for x in FILENAME]+[sheet, cropped_review]
    manifest = {
        'issue': 24, 'task': 'TO-001',
        'active_asset_id': IDS[0],
        'inactive_candidate_asset_id': IDS[1],
        'room_type': ROOM_ID,
        'format': 'TEXTURE_CUSTOM_SPRITE',
        'native_cell': [64, 64],
        'native_crop': [2, 2, 60, 60],
        'pixel_content': 'white_glyph_only_on_transparent_canvas',
        'foreground_color': NATIVE_GLYPH,
        'preview_only_native_lab_panels': LAB_PALETTE_REFERENCE,
        'vanilla_reference_glyph_bboxes': ATLAS_REFERENCE_BBOX,
        'measured_glyph_bbox': list(boxes[0]),
        'active_and_inactive_glyph_pixels_equal': True,
        'source_files': [Path(svg).name, Path(inactive_svg).name],
        'isolate_native_background': True,
        'no_global_atlas_edits': True,
        'ts_must_verify_background_compositing': True,
        'ui_L4_pass': False,
        'owner_visual_acceptance': False,
        'game_asset_registered_by_this_stage': False,
        'no_g1_changes': True,
        'sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
    }
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print('TO001 FA GLYPH-ONLY L2 SOURCE PASS; UI BACKGROUND AND L4 UNVERIFIED')
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--svg', required=True)
    parser.add_argument('--inactive-svg', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    build(args.svg, args.inactive_svg, args.output)
