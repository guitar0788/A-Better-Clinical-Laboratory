#!/usr/bin/env python3
"""Independent 32/64px alpha-gap audit for the revised native disease pictograms.

Never reads original game assets. Rejects any 32px sprite whose chemical
letters visually connect with the symbol below, including tiny alpha fringes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

EXPECTED = {
    "cadmium_64.png": "b93bc9e188146aa392e48585eeb2c162efa167ab836f0b2532b0feedc94c3a48",
    "cadmium_32.png": "81561399b2a88921a01741dae978c7f223f24ba03e82d1d8c516ddb19bc9d774",
    "mercury_64.png": "bd5d12d9edc5f1fce126687cdbcedd54ad81e4802c913e8d7104d03a8b7e3afc",
    "mercury_32.png": "8613ea09713ea577feb6d9bb507dc0ebfd05dd0727f43b21cdb35896db93201d",
}


def gap_rows(image: Image.Image) -> list[int]:
    size = image.width
    if image.size != (size, size) or image.mode != "RGBA" or size not in (32, 64):
        raise ValueError("Not a native 32/64 RGBA icon")
    alpha = image.getchannel("A")
    active = [y for y in range(size)
              if alpha.crop((0, y, size, y + 1)).getbbox()]
    if not active:
        raise ValueError("Empty disease pictogram")
    y_min, y_max = min(active), max(active)
    if y_min >= size // 2 or y_max <= size // 2:
        raise ValueError("Both chemical letters and material symbol must be present")
    empty = set(range(y_min, y_max + 1)) - set(active)
    mid = size // 2
    strip = []
    for y in range(mid-1, y_min-1, -1):
        if y in empty:
            strip.insert(0, y)
        else:
            break
    for y in range(mid, y_max+1):
        if y in empty:
            strip.append(y)
        else:
            break
    required = 8 if size == 64 else 4
    if len(strip) < required:
        raise ValueError("Cd/Hg label contacts pictogram or leaves less than "
                         + str(required) + " transparent rows")
    return strip


def verify(folder: Path) -> dict:
    folder = Path(folder)
    manifest = json.loads((folder / "V3_SOURCE_REVIEW_MANIFEST.json").read_text("utf-8"))
    if manifest["status"] != "V3_CHEMICAL_LETTERS_SEPARATED_SOURCE_REVIEW_ONLY":
        raise ValueError("Not a V3 owner-reviewed source candidate")
    if set(manifest["files"]) != set(EXPECTED):
        raise ValueError("Unexpected or missing private disease icons")
    report = {}
    for name, expected in EXPECTED.items():
        raw = (folder/name).read_bytes()
        actual = hashlib.sha256(raw).hexdigest()
        if actual != expected or manifest["files"][name]["sha256"] != expected:
            raise ValueError("Icon source hash mismatch: "+name)
        with Image.open(folder/name) as img:
            rgba = img.convert("RGBA")
            if img.mode != "RGBA" or img.size not in ((32, 32), (64, 64)):
                raise ValueError("Invalid game-native medical sprite size/mode: "+name)
            if any((r, g, b) != (255, 255, 255) for r, g, b, a in rgba.getdata() if a):
                raise ValueError("Nonwhite or shaded medical icon: "+name)
            blank_strip = gap_rows(rgba)
            if manifest["files"][name]["letter_material_empty_rows"] != len(blank_strip):
                raise ValueError("Rendering and independent spacing auditors disagree")
            # Deliberate negative regression: a 1px opaque vertical bridge must
            # cause rejection even though all original SVG/vector IDs are valid.
            tampered = rgba.copy()
            d = ImageDraw.Draw(tampered)
            d.line((rgba.width//2, blank_strip[0]-1,
                    rgba.width//2, blank_strip[-1]+1),
                   fill=(255,255,255,255), width=1)
            try:
                gap_rows(tampered)
            except ValueError:
                pass
            else:
                raise AssertionError("Negative contact-bridge test did not fail: "+name)
            report[name] = {
                "size":rgba.width,
                "sha256":actual,
                "fully_transparent_separation_rows":blank_strip,
                "deliberate_bridge_negative_test":"REJECTED_AS_EXPECTED",
            }
    return {
        "status":"FOUR_NATIVE_V3_ICONS_REPRODUCIBLE_AND_DETACHED",
        "checks":report,
        "visual_owner_game_L4":"NOT_RUN",
        "old_V1_L4_package":"WITHDRAWN_DO_NOT_INSTALL",
    }


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--icons",type=Path,required=True)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=verify(args.icons)
    print(json.dumps(result,indent=2))
    if args.output:
        if args.output.exists():
            raise FileExistsError("Do not overwrite earlier gate evidence")
        args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
