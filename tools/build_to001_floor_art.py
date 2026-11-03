#!/usr/bin/env python3
"""TO-001 FA original floor glyph; source-only, no game installation.

A 2048x2048 16x32 private atlas with one original white symbol in tile 376.
Never rewrite the game's TEXTURE_ASSET_FLOOR, its atlas, UI colors, or G1 logic.
"""
import argparse, hashlib, io, json
from pathlib import Path
import xml.etree.ElementTree as ET
import cairosvg
from PIL import Image, ImageDraw, ImageFont

ATLAS_SIZE=(2048,2048)
GRID=(16,32)
CELL_SIZE=(128,64)
TILE_ID=376
TILE_COL=TILE_ID%GRID[0]
TILE_ROW=TILE_ID//GRID[0]
TILE_BOX=(TILE_COL*128,TILE_ROW*64,(TILE_COL+1)*128,(TILE_ROW+1)*64)
ASSET_ID='ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS'
ROOM_ID='ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB'

def render_original_glyph(svgfile):
    data=Path(svgfile).read_bytes()
    low=data.lower()
    if any(s in low for s in (b'<script',b'<image',b'<use',b'href=',b'url(')):
        raise ValueError('External resource references are prohibited')
    root=ET.fromstring(data)
    if root.tag!='{http://www.w3.org/2000/svg}svg' or root.get('viewBox')!='0 0 128 64':
        raise ValueError('Expected editable 128x64 original SVG')
    if any(s in low for s in (b'#c93f3d',b'#999999',b'#54847f')):
        raise ValueError('No room UI/zone background color may be embedded')
    hi=cairosvg.svg2png(bytestring=data,output_width=512,output_height=256)
    with Image.open(io.BytesIO(hi)) as im:
        glyph=im.convert('RGBA').resize(CELL_SIZE,Image.Resampling.LANCZOS)
    alpha=glyph.getchannel('A')
    bb=alpha.point(lambda v:255 if v>127 else 0).getbbox()
    if not bb or bb[0]<6 or bb[1]<6 or bb[2]>121 or bb[3]>58:
        raise ValueError('Floor glyph clipped or too close to a cell edge: %r'%(bb,))
    if not (15<=bb[2]-bb[0]<=105 and 14<=bb[3]-bb[1]<=54):
        raise ValueError('Floor glyph size outside safe bounds')
    if len({a for a in alpha.getdata() if 0<a<255})<20:
        raise ValueError('Antialiased alpha required')
    if glyph.getpixel((0,0))[3] or glyph.getpixel((127,63))[3]:
        raise ValueError('Floor glyph edge bleed')
    return glyph,bb

def build(svgfile,dest):
    dest=Path(dest).resolve()
    if any(p.lower() in ('streamingassets','addons') for p in dest.parts):
        raise ValueError('Never write to live game directories')
    dest.mkdir(parents=True,exist_ok=True)
    glyph,bb=render_original_glyph(svgfile)
    atlas=Image.new('RGBA',ATLAS_SIZE,(0,0,0,0))
    atlas.paste(glyph,TILE_BOX[:2])
    outside=atlas.getchannel('A')
    ImageDraw.Draw(outside).rectangle(
        (TILE_BOX[0],TILE_BOX[1],TILE_BOX[2]-1,TILE_BOX[3]-1),fill=0)
    if outside.getbbox():
        raise ValueError('Atlas nontransparent outside tile 376')
    atlaspath=dest/'toxicology_floor_atlas_private_376.png'
    atlas.save(atlaspath,optimize=True)
    tilepath=dest/'toxicology_floor_glyph_128x64.png'
    glyph.save(tilepath,optimize=True)
    board=Image.new('RGB',(930,460),'#EDF0F2')
    d=ImageDraw.Draw(board)
    try:
        title=ImageFont.truetype('DejaVuSans.ttf',23)
        small=ImageFont.truetype('DejaVuSans.ttf',16)
    except OSError:
        title=small=ImageFont.load_default()
    d.text((24,22),'TO-001 | original floor glyph: exact 128 x 64 tile',font=title,fill='#304856')
    d.text((24,62),'Private 2048 x 2048 atlas, 16 x 32; ONLY cell 376 has artwork',font=small,fill='#607884')
    d.text((30,118),'1x native 128 x 64',font=small,fill='#415766')
    d.text((270,118),'4x smooth zoom (not in-game)',font=small,fill='#415766')
    native=Image.new('RGBA',CELL_SIZE,'#818A90')
    native.alpha_composite(glyph)
    board.paste(native.convert('RGB'),(35,172))
    zoom=native.resize((512,256),Image.Resampling.LANCZOS)
    board.paste(zoom.convert('RGB'),(274,155))
    d.text((24,432),'Source-only L2, no native texture/zone tint, UI adapter, L3 or L4 changes.',
           font=small,fill='#647783')
    preview=dest/'to001_floor_native_size_review.png'
    board.save(preview)
    manifest={
        'task':'TO-001','issue':24,'status':'FA_L2_SOURCE_ONLY',
        'private_asset_id':ASSET_ID,'room_type':ROOM_ID,
        'native_texture_type':'TEXTURE_ASSET_FLOOR',
        'atlas_size':list(ATLAS_SIZE),'grid':list(GRID),
        'tile_id':TILE_ID,'tile_column':TILE_COL,'tile_row_from_top':TILE_ROW,
        'tile_dimensions':list(CELL_SIZE),'tile_rect':list(TILE_BOX),
        'original_glyph_bbox':list(bb),'source_svg':Path(svgfile).name,
        'transparent_outside_tile_376':True,
        'room_zone_tint_not_baked':True,'source_only':True,
        'registered_in_gamedb':False,'owner_visual_approved':False,
        'l3_verified_with_this_asset':False,'game_l4_verified':False,
        'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
          for p in (atlaspath,tilepath,preview)}
    }
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('FA TO001 FLOOR ART SOURCE-ONLY PASS (L2); NO L3/L4')
    return manifest

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--svg',required=True)
    p.add_argument('--output',required=True)
    args=p.parse_args()
    build(args.svg,args.output)
