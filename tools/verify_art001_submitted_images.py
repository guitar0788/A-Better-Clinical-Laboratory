#!/usr/bin/env python3
"""Validate committed ART-001 *review* images without changing their pixels.

This is a source-integrity gate, not a game L3/L4 or a visual-quality pass.
Do not install the diagnostic atlas or modify G1 / native equipment XML here.
"""
from pathlib import Path
import hashlib
import json
import struct

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "assets/art001/review_20261103"
MANIFEST = REVIEW / "manifest.json"
DIRECTIONS = ("NW", "NE", "SE", "SW")
DEVICES = ("mass_spectrometer", "sample_digestion")


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    from PIL import Image, ImageChops

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["status"] == "APPROVED_FOR_SOURCE_SUBMISSION_ONLY_NOT_RUNTIME_APPROVED"
    assert not manifest["production_XML_modified"]
    assert not manifest["game_installable"]
    assert not manifest["l3_with_new_art"] and not manifest["l4_with_new_art"]
    assert manifest["atlas_layout"] == [16, 8]
    assert manifest["atlas_pixels"] == [2048, 1024]
    assert manifest["native_cell_size"] == [128, 128]
    files = manifest["files"]
    assert len(files) == 11

    expected = {
        "assets/art001/review_20261103/original/mass_spectrometer_four_views.png",
        "assets/art001/review_20261103/original/sample_digestion_four_views.png",
        "assets/art001/review_20261103/diagnostic_equipment_atlas.png",
    }
    for device in DEVICES:
        for direction in DIRECTIONS:
            expected.add(f"assets/art001/review_20261103/frames/{device}_{direction}.png")
    assert {entry["path"] for entry in files} == expected
    for entry in files:
        p = (ROOT / entry["path"]).resolve()
        assert p.is_relative_to(REVIEW.resolve()), entry["path"]
        content = p.read_bytes()
        assert content.startswith(bytes((137, 80, 78, 71, 13, 10, 26, 10)))
        assert sha256(content) == entry["sha256"], entry["path"]
        git_sha = hashlib.sha1(b"blob " + str(len(content)).encode() + bytes((0,)) + content).hexdigest()
        assert git_sha == entry["git_blob_sha1"], entry["path"]
        assert len(content) == entry["bytes"]
        width, height = struct.unpack(">II", content[16:24])
        assert [width, height] == entry["dimensions"]
        with Image.open(p) as image:
            assert image.format == "PNG" and image.mode == "RGBA"
            assert image.size == (width, height)

    frames = []
    for device in DEVICES:
        for direction in DIRECTIONS:
            path = REVIEW / "frames" / f"{device}_{direction}.png"
            with Image.open(path) as im:
                frame = im.convert("RGBA")
            assert frame.size == (128, 128)
            frames.append(frame)
    assert len({sha256(frame.tobytes()) for frame in frames}) == 8

    with Image.open(REVIEW / "diagnostic_equipment_atlas.png") as im:
        atlas = im.convert("RGBA")
    assert atlas.size == (2048, 1024)
    expected_atlas = Image.new("RGBA", atlas.size, (0, 0, 0, 0))
    for index, frame in enumerate(frames):
        expected_atlas.alpha_composite(frame, (128 * index, 0))
    assert ImageChops.difference(expected_atlas, atlas).getbbox() is None
    assert expected_atlas.tobytes() == atlas.tobytes()
    print("PASS ART-001: exact two original PNGs, eight 128px views, private review atlas")
    print("SOURCE SUBMISSION ONLY. No GameDB registration, L3, L4, or compatibility pass.")


if __name__ == "__main__":
    main()
