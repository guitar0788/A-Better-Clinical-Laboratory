#!/usr/bin/env python3
"""ART-001: reproducible, originally authored ABCL two-device sprite atlas.

No game-owned pixels or third-party textures are read. Uses Python stdlib only.
Run: python tools/generate_art_001.py --output /path/to/art
"""
import argparse
import hashlib
import json
import struct
import zlib
from pathlib import Path

CELL = 128
COLS, ROWS = 16, 8
DIRECTIONS = ("NW", "NE", "SE", "SW")
DEVICES = ("icp_ms", "digestion_station")
INK = (26, 43, 56, 255)
TRANSPARENT = (0, 0, 0, 0)


def pixel(buf, size, x, y, color):
    if 0 <= x < size and 0 <= y < size:
        n = (y * size + x) * 4
        buf[n:n + 4] = bytes(color)


def line(buf, size, a, b, color):
    x0, y0 = a
    x1, y1 = b
    steps = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(steps + 1):
        pixel(buf, size, round(x0 + (x1 - x0) * i / steps),
              round(y0 + (y1 - y0) * i / steps), color)


def polygon(buf, size, points, color, outline=INK):
    ys = [p[1] for p in points]
    for y in range(max(min(ys), 0), min(max(ys) + 1, size)):
        xs = []
        for a, b in zip(points, points[1:] + points[:1]):
            if a[1] == b[1]:
                continue
            if min(a[1], b[1]) <= y < max(a[1], b[1]):
                xs.append(a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1]))
        xs.sort()
        for start, stop in zip(xs[::2], xs[1::2]):
            for x in range(max(round(start), 0), min(round(stop) + 1, size)):
                pixel(buf, size, x, y, color)
    if outline:
        for a, b in zip(points, points[1:] + points[:1]):
            line(buf, size, a, b, outline)


def rect(buf, size, x, y, w, h, color):
    for j in range(y, y + h):
        for i in range(x, x + w):
            pixel(buf, size, i, j, color)


def ellipse(buf, size, cx, cy, rx, ry, color):
    for j in range(max(0, cy - ry), min(size, cy + ry + 1)):
        for i in range(max(0, cx - rx), min(size, cx + rx + 1)):
            if ((i - cx) / rx) ** 2 + ((j - cy) / ry) ** 2 <= 1:
                pixel(buf, size, i, j, color)


def sprite(device, direction):
    b = bytearray(CELL * CELL * 4)
    # Pivots and footprints are shared in all four orientations.
    ellipse(b, CELL, 65, 111, 42, 11, (15, 26, 34, 49))
    is_ms = device == "icp_ms"
    top = (150, 202, 218, 255) if is_ms else (219, 212, 173, 255)
    left = (58, 106, 128, 255) if is_ms else (130, 121, 85, 255)
    right = (89, 148, 164, 255) if is_ms else (165, 154, 113, 255)
    accent = (66, 229, 222, 255) if is_ms else (253, 169, 64, 255)

    # Transparent, 1-tile isometric laboratory bench-top instrument.
    polygon(b, CELL, [(23, 58), (64, 78), (64, 106), (23, 86)], left)
    polygon(b, CELL, [(64, 78), (106, 58), (106, 86), (64, 106)], right)
    polygon(b, CELL, [(23, 58), (64, 37), (106, 58), (64, 78)], top)
    # Structural lip, feet and unique analyzer upper module.
    line(b, CELL, (24, 87), (64, 108), (22, 59, 76, 255))
    line(b, CELL, (64, 108), (106, 87), (22, 59, 76, 255))
    rect(b, CELL, 32, 90, 6, 6, INK)
    rect(b, CELL, 91, 90, 6, 6, INK)

    turn = DIRECTIONS.index(direction)
    # The operator-facing face rotates; no repeated identical directional frame.
    face_left = turn in (0, 3)
    if face_left:
        polygon(b, CELL, [(31, 68), (52, 79), (52, 92), (31, 81)],
                (28, 55, 73, 255), outline=(16, 39, 55, 255))
        for x, y in ((35, 76), (39, 78), (43, 80)):
            rect(b, CELL, x, y, 2, 3, accent)
    else:
        polygon(b, CELL, [(77, 79), (99, 68), (99, 81), (77, 92)],
                (28, 55, 73, 255), outline=(16, 39, 55, 255))
        for x, y in ((83, 82), (87, 80), (91, 78)):
            rect(b, CELL, x, y, 2, 3, accent)

    if is_ms:
        # ICP-MS: sample carousel, metallic analyser and turquoise scan ring.
        polygon(b, CELL, [(48, 52), (64, 44), (81, 52), (64, 60)],
                (41, 70, 94, 255))
        ellipse(b, CELL, 64, 52, 10, 5, (14, 49, 69, 255))
        ellipse(b, CELL, 64, 52, 6, 3, accent)
        for i in range(3):
            x = 47 + (i * 9) + (turn % 2) * 2
            rect(b, CELL, x, 62 - (i % 2) * 3, 4, 5,
                 (217, 238, 236, 255))
            rect(b, CELL, x + 1, 62 - (i % 2) * 3, 2, 2, accent)
        line(b, CELL, (35, 65), (46, 59), (232, 247, 245, 255))
    else:
        # Microwave digestion: upper lid, amber safety glass and tube carousel.
        polygon(b, CELL, [(42, 51), (64, 40), (88, 51), (64, 62)],
                (68, 76, 72, 255))
        polygon(b, CELL, [(49, 51), (64, 44), (81, 51), (64, 58)],
                (38, 57, 64, 255), outline=(236, 199, 101, 255))
        for j in range(3):
            x = 53 + j * 10
            rect(b, CELL, x, 54 + (j % 2), 3, 5, accent)
        rect(b, CELL, 61, 65, 8, 2, (228, 201, 104, 255))
    # Visible turn marker, deliberately different in every orientation.
    indicator = ((45, 63), (77, 62), (76, 69), (45, 69))[turn]
    rect(b, CELL, indicator[0], indicator[1], 3, 2, accent)
    return bytes(b)


def write_png(path, width, height, rgba):
    if len(rgba) != width * height * 4:
        raise ValueError("RGBA size mismatch")
    signature = bytes((137, 80, 78, 71, 13, 10, 26, 10))
    def chunk(tag, payload):
        data = tag + payload
        return (struct.pack(">I", len(payload)) + data +
                struct.pack(">I", zlib.crc32(data) & 0xffffffff))
    stride = width * 4
    scanlines = bytearray()
    for y in range(height):
        scanlines.append(0)
        scanlines.extend(rgba[y * stride:(y + 1) * stride])
    data = (signature + chunk(b"IHDR", struct.pack(">IIBBBBB",
            width, height, 8, 6, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(bytes(scanlines), 9)) +
            chunk(b"IEND", b""))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return hashlib.sha256(data).hexdigest()


def generate(root):
    root = Path(root)
    width, height = COLS * CELL, ROWS * CELL
    atlas = bytearray(width * height * 4)
    hashes = {}
    slots = {}
    for dev_i, dev in enumerate(DEVICES):
        slots[dev] = {}
        for j, direction in enumerate(DIRECTIONS):
            slot = dev_i * 4 + j
            tile = sprite(dev, direction)
            for y in range(CELL):
                dst = (y * width + slot * CELL) * 4
                src = y * CELL * 4
                atlas[dst:dst + CELL * 4] = tile[src:src + CELL * 4]
            slots[dev][direction] = slot
    hashes["equipment_atlas.png"] = write_png(
        root / "Assets" / "ABCL" / "equipment_atlas.png", width, height, atlas)
    # Compact four-direction preview; it is not a loader texture.
    preview = bytearray(8 * CELL * 2 * CELL * 4)
    for row, dev in enumerate(DEVICES):
        for col, direction in enumerate(DIRECTIONS):
            tile = sprite(dev, direction)
            for y in range(CELL):
                dst = ((row * CELL + y) * (8 * CELL) + col * 2 * CELL) * 4
                src = y * CELL * 4
                preview[dst:dst + CELL * 4] = tile[src:src + CELL * 4]
    hashes["direction_preview.png"] = write_png(
        root / "Previews" / "ABCL" / "direction_preview.png",
        8 * CELL, 2 * CELL, preview)
    manifest = {
        "schema": "ABCL-ART-001-v0", "authoring": "Original procedural pixel art",
        "atlas_layout": "LAYOUT_16_X_8", "sprite_shape": "SHAPE_1_X_1",
        "atlas_size_px": [width, height], "cell_px": CELL,
        "directions": list(DIRECTIONS),
        "sprites": slots, "shared_pivot_px": [64, 112],
        "collision": "1x1 tile; existing attachment table required",
        "ownership": "ABCL original art; no vanilla/DLC/Workshop textures copied",
        "sha256": hashes
    }
    path = root / "art_manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = generate(args.output)
    print(json.dumps(result["sha256"], sort_keys=True))


if __name__ == "__main__":
    main()
