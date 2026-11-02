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


def _source_sprite(device, direction):
    """Original pixel-art bench-top instruments, designed at a native 128px cell.

    Each direction rotates the control face, upper assembly and visible panel
    rather than merely changing a light or flipping the same 2D box.
    """
    if direction not in DIRECTIONS or device not in DEVICES:
        raise ValueError("Unknown device/direction")
    b = bytearray(CELL * CELL * 4)
    is_ms = device == "icp_ms"
    face_left = direction in ("NW", "SW")
    far_side = direction in ("NW", "NE")
    # Original editable source geometry; final sprite is scale-normalized.
    ellipse(b, CELL, 64, 108, 43, 8, (15, 27, 33, 45))
    # Native-style shaded isometric shell and hard 1px pixel outline.
    top = (194, 226, 227, 255) if is_ms else (242, 222, 174, 255)
    left = (84, 127, 151, 255) if is_ms else (151, 128, 86, 255)
    right = (109, 158, 176, 255) if is_ms else (179, 150, 101, 255)
    dark = (20, 43, 59, 255)
    panel = (35, 62, 77, 255)
    hi = (88, 236, 215, 255) if is_ms else (255, 187, 88, 255)
    silver = (232, 244, 238, 255)

    polygon(b, CELL, [(22, 62), (63, 82), (63, 105), (22, 85)],
            left if face_left else right)
    polygon(b, CELL, [(63, 82), (105, 62), (105, 86), (63, 105)],
            right if face_left else left)
    polygon(b, CELL, [(22, 62), (63, 41), (105, 62), (63, 82)], top)
    line(b, CELL, (22, 86), (63, 106), dark)
    line(b, CELL, (63, 106), (105, 86), dark)
    line(b, CELL, (22, 65), (63, 85), (213, 236, 231, 255))
    line(b, CELL, (64, 85), (104, 65), (224, 239, 227, 255))
    # Two consistent bench-attachment rubber feet.
    rect(b, CELL, 28, 89, 7, 5, dark)
    rect(b, CELL, 92, 88, 7, 5, dark)

    # Front door and status control are on the viewer-facing orientation.
    if face_left:
        polygon(b, CELL, [(27, 67), (54, 81), (54, 99), (27, 85)],
                panel, outline=dark)
        polygon(b, CELL, [(31, 73), (47, 81), (47, 88), (31, 80)],
                (14, 37, 53, 255), outline=(152, 206, 203, 255))
        for i in range(3):
            rect(b, CELL, 32 + i * 4, 86 + i * 2, 2, 2, hi)
        # Vent ribs on the other shell face.
        for i in range(5):
            line(b, CELL, (75, 83 + i * 2), (98, 72 + i * 2),
                 (47, 92, 106, 255))
        line(b, CELL, (30, 69), (48, 78), silver)
    else:
        polygon(b, CELL, [(73, 82), (99, 68), (99, 85), (73, 99)],
                panel, outline=dark)
        polygon(b, CELL, [(80, 82), (95, 74), (95, 81), (80, 89)],
                (14, 37, 53, 255), outline=(152, 206, 203, 255))
        for i in range(3):
            rect(b, CELL, 86 - i * 4, 89 + i * 2, 2, 2, hi)
        for i in range(5):
            line(b, CELL, (27, 72 + i * 2), (51, 83 + i * 2),
                 (47, 92, 106, 255))
        line(b, CELL, (94, 70), (76, 79), silver)

    if is_ms:
        # ICP-MS upper plasma/ionizer unit is substantially taller than the
        # digestion workstation and always has a silver metal exhaust tower.
        shift = (-7 if face_left else 7) + (-3 if far_side else 3)
        cx = 63 + shift
        polygon(b, CELL, [(cx - 18, 35), (cx, 26), (cx + 17, 35),
                           (cx, 44)], (214, 234, 234, 255))
        polygon(b, CELL, [(cx - 18, 35), (cx, 44), (cx, 69),
                           (cx - 18, 60)], (82, 120, 145, 255))
        polygon(b, CELL, [(cx, 44), (cx + 17, 35), (cx + 17, 60),
                           (cx, 69)], (112, 161, 176, 255))
        line(b, CELL, (cx - 18, 36), (cx, 45), silver)
        line(b, CELL, (cx, 45), (cx + 17, 36), silver)
        # Purple ion source core, vent fins, vertical illuminated status bar.
        polygon(b, CELL, [(cx - 11, 44), (cx - 3, 48),
                           (cx - 3, 57), (cx - 11, 53)], (31, 44, 70, 255))
        rect(b, CELL, cx - 8, 48, 2, 4, (188, 141, 241, 255))
        for i in range(4):
            line(b, CELL, (cx + 4, 47 + i * 3),
                 (cx + 12, 43 + i * 3), (45, 83, 107, 255))
        rect(b, CELL, cx + 2, 60, 3, 5, hi)

        # Swivel-fed sample carousel and a small rack of capped vials.
        trayx = 79 if far_side else 43
        trayy = 58 if far_side else 67
        ellipse(b, CELL, trayx, trayy, 13, 5, (32, 62, 79, 255))
        ellipse(b, CELL, trayx, trayy, 9, 3, (179, 208, 207, 255))
        for dx, dy in ((-6, -1), (1, -3), (7, 0)):
            rect(b, CELL, trayx + dx, trayy + dy - 5, 4, 6, silver)
            rect(b, CELL, trayx + dx + 1, trayy + dy - 5, 2, 2, hi)
        line(b, CELL, (cx + (14 if face_left else -14), 58),
             (trayx, trayy - 3), (234, 244, 243, 255))
        line(b, CELL, (cx + (14 if face_left else -14), 59),
             (trayx, trayy - 2), (35, 93, 112, 255))
    else:
        # Digestion station: wide hinged hood, amber transparent reaction
        # chamber, status keypad, pipette tubes and visible safety grille.
        hoodshift = 4 if direction in ("NW", "SE") else -4
        cx = 63 + hoodshift
        polygon(b, CELL, [(cx - 26, 47), (cx, 35), (cx + 28, 47),
                           (cx + 1, 59)], (226, 224, 202, 255))
        polygon(b, CELL, [(cx - 26, 47), (cx + 1, 59),
                           (cx + 1, 70), (cx - 26, 59)], (92, 85, 67, 255))
        polygon(b, CELL, [(cx + 1, 59), (cx + 28, 47),
                           (cx + 28, 59), (cx + 1, 70)], (142, 129, 95, 255))
        # Warm enclosed reaction glass with visible tubes behind it.
        polygon(b, CELL, [(cx - 17, 49), (cx + 1, 57),
                           (cx + 1, 64), (cx - 17, 57)],
                (24, 45, 53, 255), outline=(239, 187, 90, 255))
        for i in range(3):
            x = cx - 12 + i * 5
            rect(b, CELL, x, 53 + i, 2, 5, (248, 153, 53, 255))
            rect(b, CELL, x, 53 + i, 2, 1, (246, 240, 193, 255))
        for i in range(5):
            line(b, CELL, (cx + 8, 59 + i * 2),
                 (cx + 20, 53 + i * 2), (59, 69, 62, 255))
        # Raised central hinge, diagonal amber warning stripe and gauge.
        line(b, CELL, (cx - 19, 45), (cx + 18, 45),
             (252, 192, 78, 255))
        rect(b, CELL, cx + 3, 62, 5, 3, hi)
        rect(b, CELL, cx + 10, 60, 2, 2, (237, 82, 54, 255))
        # Removable sample rack beside the enclosed hood.
        rackx = (30 if far_side else 91)
        for i in range(3):
            x = rackx + i * 5 * (1 if far_side else -1)
            rect(b, CELL, x, 59 + i % 2, 3, 5,
                 (213, 235, 231, 255))
            rect(b, CELL, x, 58 + i % 2, 3, 2, hi)

    # Four visibly distinct orientation cues (not the only difference).
    turn = DIRECTIONS.index(direction)
    for i in range(turn + 1):
        px = 42 + i * 3 if face_left else 80 + i * 3
        pixel(b, CELL, px, 99 if face_left else 92, hi)
    return bytes(b)



def _lab_color(r, g, b, a):
    """Muted cool/neutral medical equipment palette; keep visible highlights."""
    if not a:
        return (0, 0, 0, 0)
    lum = (r * 30 + g * 59 + b * 11) // 100
    # De-emphasize bright red, orange, cyan and purple accents. Preserve
    # luminance and a little chroma so both devices remain distinguishable.
    return (
        min(255, (lum * 81 + r * 19) // 100 + 2),
        min(255, (lum * 83 + g * 17) // 100 + 4),
        min(255, (lum * 82 + b * 18) // 100 + 9),
        a,
    )


def sprite(device, direction):
    """Compact bench instrument inside the same native 128px atlas cell.

    The old 84px-wide, 80px-tall source was visually as large as an entire
    workbench in the owner L4 photos. Scale about 70% in width and 57% in
    height; align feet near y=110 in every direction. This preserves 16x8
    atlas indices, internal tags and vanilla object rendering semantics.
    """
    source = _source_sprite(device, direction)
    out = bytearray(CELL * CELL * 4)
    # Same pivot and baseline across all orientations.
    width = 62 if device == "icp_ms" else 64
    height = 50 if device == "icp_ms" else 44
    left = (CELL - width) // 2
    top = 109 - height
    # Original authored source content including tower and feet, excluding
    # the intentionally faint ground-shadow pixels at the very bottom.
    src_x0, src_x1 = 20, 108
    src_y0, src_y1 = 24, 107
    for y in range(height):
        sy = src_y0 + (y * (src_y1 - src_y0)) // max(height - 1, 1)
        for x in range(width):
            sx = src_x0 + (x * (src_x1 - src_x0)) // max(width - 1, 1)
            start = (sy * CELL + sx) * 4
            col = _lab_color(*source[start:start + 4])
            dest = ((top + y) * CELL + left + x) * 4
            out[dest:dest + 4] = bytes(col)
    return bytes(out)


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
