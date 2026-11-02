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


def _stroke(buf, points, color):
    for p, q in zip(points, points[1:]):
        line(buf, CELL, p, q, color)


def sprite(device, direction):
    """Eight original directional laboratory sprites with native-style material cues.

    Dimensions intentionally remain smaller than the 128-px cell. Four
    directions share the same geometric origin, heights, panel semantics and
    visual weight; only surfaces and perspective reveal change with view.
    """
    if direction not in DIRECTIONS or device not in DEVICES:
        raise ValueError("Unknown device/direction")
    buf = bytearray(CELL * CELL * 4)
    control_left = direction in ("NW", "SW")
    back_view = direction in ("NW", "NE")

    # A restrained medical-laboratory palette drawn independently of game art.
    edge = (87, 94, 99, 255)
    edge_light = (150, 159, 161, 255)
    shell_top = (228, 228, 221, 255)
    shell_left = (190, 198, 197, 255)
    shell_right = (204, 209, 203, 255)
    side_shadow = (155, 165, 168, 255)
    rim = (245, 243, 234, 255)
    seam = (116, 126, 132, 255)
    dark = (66, 80, 88, 255)
    display = (80, 104, 109, 255)
    indicator = (126, 172, 159, 255)
    feet = (77, 85, 90, 255)

    # A thin, consistent footprint on the laboratory instrument workbench.
    # No broad floor shadow: attachment renderer and parent desk own placement.
    if device == "icp_ms":
        # Compact clinical trace-metal analyzer: a two-level cabinet with a
        # recognisable mass-filter column, capped sample rack and exhaust.
        polygon(buf, CELL, [(34, 82), (63, 68), (94, 83), (64, 99)],
                shell_top, outline=edge)
        polygon(buf, CELL, [(34, 82), (64, 99), (64, 108), (34, 91)],
                shell_left if control_left else side_shadow, outline=edge)
        polygon(buf, CELL, [(64, 99), (94, 83), (94, 93), (64, 108)],
                shell_right if control_left else shell_left, outline=edge)
        _stroke(buf, [(35, 83), (64, 99), (93, 84)], rim)
        # Small separate upright analyzer module, not a giant stacked cube.
        cx = (58 if control_left else 69) + (-2 if back_view else 2)
        polygon(buf, CELL,
                [(cx - 11, 67), (cx + 1, 61), (cx + 13, 67), (cx + 1, 73)],
                shell_top, outline=edge)
        polygon(buf, CELL,
                [(cx - 11, 67), (cx + 1, 73), (cx + 1, 94), (cx - 11, 88)],
                shell_left, outline=edge)
        polygon(buf, CELL,
                [(cx + 1, 73), (cx + 13, 67), (cx + 13, 88), (cx + 1, 94)],
                side_shadow, outline=edge)
        line(buf, CELL, (cx - 10, 70), (cx, 75), rim)
        # Vertical filter ventilation and a muted status indicator.
        for n in range(3):
            line(buf, CELL,
                 (cx + 5, 76 + n * 4), (cx + 10, 73 + n * 4), seam)
        rect(buf, CELL, cx - 6, 79, 2, 4, display)
        rect(buf, CELL, cx - 6, 83, 2, 2, indicator)

        # Detachable sample tray: its projected location reverses with view.
        tx = 80 if control_left else 48
        ty = 82 if back_view else 90
        polygon(buf, CELL,
                [(tx - 10, ty), (tx, ty - 5), (tx + 11, ty),
                 (tx + 1, ty + 5)], side_shadow, outline=seam)
        for dx, dy in ((-5, -1), (0, -3), (5, -1)):
            rect(buf, CELL, tx + dx, ty + dy - 5, 3, 6, rim)
            line(buf, CELL, (tx + dx, ty + dy - 5),
                 (tx + dx + 2, ty + dy - 5), display)
        # Front-facing NW/NE views show the control panel; opposite SW/SE
        # views show rear power/ventilation service panels like vanilla gear.
        if back_view and control_left:
            polygon(buf, CELL, [(38, 86), (52, 93), (52, 100), (38, 93)],
                    display, outline=seam)
            for n in range(3):
                pixel(buf, CELL, 40 + 3 * n, 96 + n, indicator)
        elif back_view:
            polygon(buf, CELL, [(76, 93), (89, 86), (89, 93), (76, 100)],
                    display, outline=seam)
            for n in range(3):
                pixel(buf, CELL, 83 + 2 * n, 96 - n, indicator)
        elif control_left:
            polygon(buf, CELL, [(38, 87), (54, 95), (54, 102), (38, 94)],
                    side_shadow, outline=seam)
            for n in range(4):
                line(buf, CELL, (41, 89 + n * 2),
                     (50, 94 + n * 2), dark)
            rect(buf, CELL, 51, 99, 2, 2, feet)
        else:
            polygon(buf, CELL, [(74, 95), (90, 87), (90, 94), (74, 102)],
                    side_shadow, outline=seam)
            for n in range(4):
                line(buf, CELL, (78, 99 - n * 2),
                     (87, 94 - n * 2), dark)
            rect(buf, CELL, 75, 99, 2, 2, feet)
        # A sliver of physical supports, not a large block floating in air.
        rect(buf, CELL, 40, 95, 4, 3, feet)
        rect(buf, CELL, 83, 96, 4, 3, feet)
    else:
        # A lower, wider sample-digestion workstation. Original instrument
        # silhouette is deliberately dissimilar from the mass spectrometer.
        polygon(buf, CELL, [(32, 80), (63, 65), (96, 81), (64, 97)],
                shell_top, outline=edge)
        polygon(buf, CELL, [(32, 80), (64, 97), (64, 105), (32, 88)],
                shell_left if control_left else side_shadow, outline=edge)
        polygon(buf, CELL, [(64, 97), (96, 81), (96, 89), (64, 105)],
                shell_right if control_left else shell_left, outline=edge)
        line(buf, CELL, (34, 80), (64, 96), rim)
        line(buf, CELL, (65, 96), (94, 82), rim)

        # Trapezoidal hinged hood, transparent safety observation window.
        cx = 63 + (-3 if control_left else 3)
        polygon(buf, CELL,
                [(cx - 21, 76), (cx, 65), (cx + 22, 76), (cx, 88)],
                (215, 216, 205, 255), outline=edge)
        polygon(buf, CELL,
                [(cx - 18, 75), (cx, 66), (cx + 18, 75), (cx, 84)],
                (174, 189, 188, 255), outline=seam)
        if back_view:
            # Safe, visible front glass and tiny capped reaction vials.
            polygon(buf, CELL,
                    [(cx - 12, 75), (cx, 69), (cx + 11, 75), (cx, 81)],
                    (74, 92, 98, 255), outline=edge_light)
            for n in range(3):
                yy = 74 + (n % 2)
                x = cx - 5 + n * 4
                pixel(buf, CELL, x, yy, (178, 156, 116, 255))
                pixel(buf, CELL, x, yy + 1, (174, 171, 140, 255))
        else:
            # Rear cover: horizontal louvres instead of an impossible
            # four-direction window, with a single quiet safety marker.
            polygon(buf, CELL,
                    [(cx - 12, 75), (cx, 69), (cx + 11, 75), (cx, 81)],
                    (157, 173, 175, 255), outline=edge_light)
            for n in range(4):
                line(buf, CELL, (cx - 6 + n * 3, 74 + n),
                     (cx - 2 + n * 3, 72 + n), seam)
            pixel(buf, CELL, cx + 7, 76, (177, 158, 126, 255))
        _stroke(buf, [(cx - 19, 76), (cx, 85), (cx + 19, 76)], rim)

        # NW/NE: front keypad/inspection; SW/SE: rear grilles and service
        # panel. Keep the same housing across all four views.
        if back_view and control_left:
            polygon(buf, CELL, [(37, 84), (54, 93), (54, 99), (37, 90)],
                    (115, 132, 137, 255), outline=seam)
            rect(buf, CELL, 40, 89, 7, 3, display)
            pixel(buf, CELL, 49, 98, indicator)
        elif back_view:
            polygon(buf, CELL, [(75, 93), (91, 85), (91, 91), (75, 99)],
                    (115, 132, 137, 255), outline=seam)
            rect(buf, CELL, 81, 89, 7, 3, display)
            pixel(buf, CELL, 84, 94, indicator)
        elif control_left:
            polygon(buf, CELL, [(37, 84), (54, 93), (54, 99), (37, 90)],
                    side_shadow, outline=seam)
            for n in range(3):
                line(buf, CELL, (41, 88 + n * 2),
                     (49, 92 + n * 2), dark)
        else:
            polygon(buf, CELL, [(75, 93), (91, 85), (91, 91), (75, 99)],
                    side_shadow, outline=seam)
            for n in range(3):
                line(buf, CELL, (79, 94 - n * 2),
                     (87, 90 - n * 2), dark)
        # Low-profile sample-well cassette, visible beside the hood.
        x = 80 if back_view else 47
        y = 88 if back_view else 91
        for n in range(3):
            rect(buf, CELL, x - 5 + n * 4, y - (n % 2), 2, 3, rim)
        rect(buf, CELL, 39, 93, 4, 3, feet)
        rect(buf, CELL, 86, 93, 4, 3, feet)

    # A 128px atlas cell gives renderer compatibility, not visual scale.
    # Bounds: ~65px wide, <=50px high. All views share baseline y <= 108.
    return bytes(buf)


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
    # Original device icons, derived solely from the editable sprite source.
    for dev in DEVICES:
        original = sprite(dev, "SE")
        icon = bytearray(64 * 64 * 4)
        for y in range(64):
            for x in range(64):
                start = ((y * 2) * CELL + x * 2) * 4
                end = (y * 64 + x) * 4
                icon[end:end + 4] = original[start:start + 4]
        name = dev + "_icon.png"
        hashes[name] = write_png(root / "Assets" / "ABCL" / name, 64, 64, icon)
    hashes["direction_preview.png"] = write_png(
        root / "Previews" / "ABCL" / "direction_preview.png",
        8 * CELL, 2 * CELL, preview)
    manifest = {
        "schema": "ABCL-ART-001-v1-vanilla-style", "authoring": "Original procedural pixel art",
        "atlas_layout": "LAYOUT_16_X_8", "sprite_shape": "SHAPE_1_X_1",
        "atlas_size_px": [width, height], "cell_px": CELL,
        "directions": list(DIRECTIONS),
        "sprites": slots, "shared_pivot_px": [64, 112],
        "collision": "1x1; dedicated private attachment parent",
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
