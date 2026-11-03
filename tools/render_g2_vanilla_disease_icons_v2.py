#!/usr/bin/env python3
"""Generate only two ABCL-owned vanilla-style disease icon pairs, for review.

NO original game artwork, no glossy drawing, no lab-machine/exam icons,
no DLL, no installation or L4 claim. The exact SVG silhouettes are
fully editable and rendered as white RGBA with transparent surroundings.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/g2/disease_icons_v2"
EXPECTED = {
    "cadmium_64.png": "b93bc9e188146aa392e48585eeb2c162efa167ab836f0b2532b0feedc94c3a48",
    "cadmium_32.png": "81561399b2a88921a01741dae978c7f223f24ba03e82d1d8c516ddb19bc9d774",
    "mercury_64.png": "bd5d12d9edc5f1fce126687cdbcedd54ad81e4802c913e8d7104d03a8b7e3afc",
    "mercury_32.png": "8613ea09713ea577feb6d9bb507dc0ebfd05dd0727f43b21cdb35896db93201d",
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def make(output: Path):
    import cairosvg
    from PIL import Image

    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError("Refuse replacing previously reviewed sprite files")
    if any(part.lower() in {"projecthospital_data", "streamingassets", "addons"}
           for part in output.parts):
        raise ValueError("Never render directly into an installed game")
    output.mkdir(parents=True)
    report = {}
    for element in ("cadmium", "mercury"):
        data = (SOURCE / f"{element}.svg").read_bytes()
        root = ET.fromstring(data)
        if root.attrib.get("viewBox") != "0 0 64 64":
            raise ValueError("Original reference cell must be 64x64")
        xml = data.decode("utf-8")
        if any(x in xml.lower() for x in ("<lineargradient","<radialgradient",
                                         "<image","<filter","base64,")):
            raise ValueError("No raster/gradient/3D/borrowed game pixels allowed")
        for color in ("#FFFFFF",):
            if color not in xml:
                raise ValueError("All shapes must be flat white")
        for size in (64, 32):
            render = cairosvg.svg2png(bytestring=data,
                                     output_width=size * 4,
                                     output_height=size * 4)
            original = Image.open(io.BytesIO(render)).convert("RGBA")
            original = original.resize((size, size), Image.Resampling.LANCZOS)
            rgba = Image.new("RGBA", (size, size), (255, 255, 255, 0))
            # Remove sub-5 alpha LANCZOS ringing, which otherwise connects
            # separate glyph components at tiny native UI sizes.
            rgba.putalpha(original.getchannel("A").point(
                lambda alpha: 0 if alpha < 5 else alpha))
            bbox = rgba.getbbox()
            if bbox is None:
                raise ValueError("Blank medical pictogram")
            mask = rgba.getchannel("A")
            occupied_rows = [y for y in range(size)
                if mask.crop((0, y, size, y + 1)).getbbox()]
            empty_rows = set(range(min(occupied_rows), max(occupied_rows) + 1)) - set(occupied_rows)
            mid = size // 2
            # Hard source/PNG contract: a *literal* empty horizontal strip
            # must separate Cd/Hg lettering from the material symbol at
            # native 64x64 and 32x32, not only in an enlarged preview.
            gap = [y for y in range(mid, size) if y in empty_rows]
            gap_before = [y for y in range(mid - 1, -1, -1) if y in empty_rows]
            strip = []
            for y in range(mid - 1, -1, -1):
                if y in empty_rows: strip.insert(0, y)
                else: break
            for y in range(mid, size):
                if y in empty_rows: strip.append(y)
                else: break
            minimum = 8 if size == 64 else 4
            if len(strip) < minimum:
                raise ValueError("Chemical letters touch the pictogram; native-size gap too small")
            if size == 64:
                if not (8 <= bbox[0] < bbox[2] <= 56 and
                        8 <= bbox[1] < bbox[3] <= 57):
                    raise ValueError("64px glyph does not fit vanilla icon proportions")
            else:
                if not (3 <= bbox[0] < bbox[2] <= 28 and
                        3 <= bbox[1] < bbox[3] <= 30):
                    raise ValueError("32px glyph is clipped or oversized")
            name = f"{element}_{size}.png"
            p = output / name
            rgba.save(p, optimize=True)
            digest = sha(p.read_bytes())
            if digest != EXPECTED[name]:
                raise ValueError(f"Frozen reviewed {name} changed: {digest}")
            report[name] = {"sha256": digest, "size": size,
                            "mode": "RGBA", "alpha_bounds": list(bbox), "letter_material_empty_rows": len(strip)}
    record = {
        "status": "V3_CHEMICAL_LETTERS_SEPARATED_SOURCE_REVIEW_ONLY",
        "only_disease_and_main_symptom_icons": True,
        "exam_icons": "NATIVE_ICON_INDEX_1641_BLOOD_AND_1691_URINE",
        "digestion_machine_icon": "ART001_OWNED_NOT_MEDICALICON",
        "original_game_pixels_included": False,
        "owner_visual_approval": "PENDING",
        "native_game_L4": "NOT_RUN",
        "letter_material_separation": "32px >= 4 fully transparent rows; 64px >= 8 fully transparent rows",
        "files": report,
    }
    (output / "V3_SOURCE_REVIEW_MANIFEST.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return record


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    args=p.parse_args()
    print(json.dumps(make(args.out), indent=2))
