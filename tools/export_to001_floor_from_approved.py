#!/usr/bin/env python3
"""TO-001 exact approved SVG projection export (offline only, never installs into game)."""
import argparse
import hashlib
import io
from pathlib import Path
import xml.etree.ElementTree as ET

APPROVED_BLOB = "c4a81670a2b0004799513c5b03a61b9239af1f5b"
NATIVE_SHA256 = "a4083e3bef7dab0f9c0d629a42da517a51951729a42884f082eb9d8d5c7e8903"
PRIVATE_SHA256 = "7c0d03ddbd370aca4ddd1a089ff91d814e1c2622659a3d300d844bd9713a8cb4"
MATRIX = "matrix(3.3 1.2 -2.3 0.75 96 1.6)"
ROOT = Path(__file__).resolve().parents[1]
NS = "{http://www.w3.org/2000/svg}"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def verify_vector(src, floor):
    original = src.read_bytes()
    git_sha = hashlib.sha1(b"blob " + str(len(original)).encode() + b"\x00" + original).hexdigest()
    if git_sha != APPROVED_BLOB:
        raise ValueError("The room-list icon has changed since owner approval")
    a = ET.fromstring(original)
    b = ET.fromstring(floor.read_bytes())
    orig_groups = [x for x in a if x.tag == NS + "g"]
    outer = [x for x in b if x.tag == NS + "g"]
    if b.get("viewBox") != "0 0 256 128" or len(orig_groups) != 2 or len(outer) != 1:
        raise ValueError("Unexpected floor vector structure")
    if outer[0].get("transform") != MATRIX:
        raise ValueError("Different floor perspective")
    if len(list(outer[0])) != 2:
        raise ValueError("Floor vector includes unexpected artwork")
    for orig, child in zip(orig_groups, list(outer[0])):
        if ET.tostring(orig) != ET.tostring(child):
            raise ValueError("Approved icon geometry or styling was redrawn")


def export(output):
    from PIL import Image
    import cairosvg

    src = ROOT / "assets/art/to001/toxicology_room_icon.svg"
    floor = ROOT / "assets/art/to001/toxicology_floor_from_approved_256x128.svg"
    verify_vector(src, floor)
    high = cairosvg.svg2png(bytestring=floor.read_bytes(), output_width=1024, output_height=512)
    with Image.open(io.BytesIO(high)) as image:
        native = image.convert("RGBA").resize((256,128),Image.Resampling.LANCZOS)
    private = native.resize((128,64),Image.Resampling.LANCZOS)
    artifacts = {}
    for name, im, expected in (
        ("toxicology_floor_from_approved_256x128.png", native, NATIVE_SHA256),
        ("toxicology_floor_from_approved_128x64.png", private, PRIVATE_SHA256),
    ):
        b = io.BytesIO()
        im.save(b, format="PNG")
        data = b.getvalue()
        if sha256(data) != expected:
            raise ValueError("Not the owner-approved asset bytes: " + name)
        artifacts[name] = data
    output = Path(output).resolve()
    if any(s.lower() in {"streamingassets", "addons"} for s in output.parts):
        raise ValueError("Refusing to write into a live game/addon installation")
    output.mkdir(parents=True, exist_ok=True)
    for name,data in artifacts.items():
        (output/name).write_bytes(data)
    current_private = ROOT / "assets/art/to001/toxicology_floor_from_approved_128x64.png"
    if current_private.read_bytes() != artifacts[current_private.name]:
        raise ValueError("Committed private PNG differs from approved export")
    print("PASS: owner-approved floor SVG and exact 256x128 / 128x64 PNG bytes; source-only")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    export(args.output)
