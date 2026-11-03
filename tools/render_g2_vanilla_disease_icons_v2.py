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
    "cadmium_64.png": "eabbbc55405ee75f7c77f5fa810d45e731ec497ed4ea4d3912dbc8fceb6ae3d7",
    "cadmium_32.png": "00a76e5be749f58c6b41942246343349c07e92fc87dc8039ef332d37f6842720",
    "mercury_64.png": "31573926fa10ddca49e40599790829c49c0d8c9ca94f5f52379fbc8906741774",
    "mercury_32.png": "174fb1221357e63658d27f77a296f370c137e1c95cab473d730929e9e4e8ad88",
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
            rgba.putalpha(original.getchannel("A"))
            bbox = rgba.getbbox()
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
                            "mode": "RGBA", "alpha_bounds": list(bbox)}
    record = {
        "status": "V2_ORIGINAL_STYLE_DISEASE_ART_SOURCE_REVIEW_ONLY",
        "only_disease_and_main_symptom_icons": True,
        "exam_icons": "NATIVE_ICON_INDEX_1641_BLOOD_AND_1691_URINE",
        "digestion_machine_icon": "ART001_OWNED_NOT_MEDICALICON",
        "original_game_pixels_included": False,
        "owner_visual_approval": "PENDING",
        "native_game_L4": "NOT_RUN",
        "files": report,
    }
    (output / "V2_SOURCE_REVIEW_MANIFEST.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return record


if __name__ == "__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, required=True)
    args=p.parse_args()
    print(json.dumps(make(args.out), indent=2))
