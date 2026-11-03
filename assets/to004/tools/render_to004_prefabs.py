#!/usr/bin/env python3
"""Rebuild TO-004 screenshot-derived 104x104 previews from owner-authored editable SVG.

Unlike the retired isometric illustration renderer, this reads only each SVG's
embedded photo layer plus adjustable vector crop. It does not regenerate or
approximate original game objects. Original room prefab XML remains untouched.
"""
from pathlib import Path
import hashlib
import io
import json
import cairosvg
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'art_sources'
OUT=ROOT/'Assets'/'ABCL'/'Prefabs'
MANIFEST=json.loads((ART/'manifest.json').read_text('utf-8'))

for key in ('small','large'):
    source=ART/f'toxicology_{key}.svg'
    raw=cairosvg.svg2png(bytestring=source.read_bytes(),output_width=624,output_height=624)
    im=Image.open(io.BytesIO(raw)).convert('RGBA').resize((104,104),Image.Resampling.LANCZOS)
    target=OUT/f'toxicology_{key}.png'
    im.save(target,optimize=True)
    digest=hashlib.sha256(target.read_bytes()).hexdigest()
    expected=MANIFEST[key]['icon_sha256']
    if digest!=expected:
        raise SystemExit(f'{key}: rendered screenshot thumbnail SHA256 mismatch {digest} != {expected}')
    print(f'{key}: 104x104 RGBA, SHA256 {digest}, PASS')
