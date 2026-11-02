#!/usr/bin/env python3
"""Review-only validation of original ABCL vector art exports; never installs game data."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
SVG_TAGS = {
    "svg", "defs", "linearGradient", "stop", "g", "path", "polygon",
    "rect", "circle", "ellipse", "line",
}
FORBIDDEN = (
    "Assembly-CSharp.dll", "0Harmony.dll", ".aes", ".key",
    "objects_small_atlas.png",
)
DIRECTIONS = ("NW", "NE", "SE", "SW")
EXPECTED_SVG = {
    *(f"{device}_{direction}.svg"
      for device in ("icp_ms", "digestion_station")
      for direction in DIRECTIONS),
    "workbench_icon.svg",
}
EXPECTED_ASSETS = {
    "equipment_atlas.png", "icp_ms_icon.png",
    "digestion_station_icon.png", "workbench_icon.png",
}
EXPECTED_PREVIEWS = {"direction_preview.png", "review_mobile.png"}


def validate_svg_text(data, name="<memory>"):
    """Allow passive authored SVG only; the standard SVG namespace is safe."""
    lowered = data.lower()
    if "<!doctype" in lowered or "<!entity" in lowered:
        raise ValueError(f"DTD/entities are not permitted in {name}")
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ValueError(f"Invalid SVG XML in {name}: {exc}") from exc
    if root.tag != f"{{{SVG_NS}}}svg":
        raise ValueError(f"SVG root must use the standard SVG namespace: {name}")
    expected_viewbox = "0 0 64 64" if name.endswith("workbench_icon.svg") else "0 0 128 128"
    if root.attrib.get("viewBox") != expected_viewbox:
        raise ValueError(f"Invalid SVG viewBox in {name}; expected {expected_viewbox}")

    for element in root.iter():
        if not element.tag.startswith(f"{{{SVG_NS}}}"):
            raise ValueError(f"Foreign XML namespace in {name}")
        local_tag = element.tag.rsplit("}", 1)[-1]
        if local_tag not in SVG_TAGS:
            raise ValueError(f"Unsupported/active SVG element {local_tag} in {name}")
        for attr, value in element.attrib.items():
            attr_name = attr.rsplit("}", 1)[-1].lower()
            val = str(value).strip()
            low = val.lower()
            if attr_name.startswith("on"):
                raise ValueError(f"Event handler attribute in {name}: {attr}")
            if attr_name in ("href", "src") and not val.startswith("#"):
                raise ValueError(f"External SVG reference in {name}: {attr}")
            if any(token in low for token in (
                "javascript:", "data:", "file:", "http://", "https://",
                "@import",
            )):
                raise ValueError(f"External or active reference in {name}: {attr}")
            for target in re.findall(r"url\((.*?)\)", val, flags=re.IGNORECASE):
                target = target.strip().strip("'\"")
                if not target.startswith("#"):
                    raise ValueError(f"Non-local SVG paint reference in {name}: {target}")
    return root


def _check_png(path, size, mode, label):
    from PIL import Image
    with Image.open(path) as image:
        if image.size != size or image.mode != mode:
            raise ValueError(
                f"{label} must be {size[0]}x{size[1]} {mode}; got {image.size} {image.mode}"
            )
        return image.copy()


def verify(root):
    from PIL import Image
    source = root / "Sources" / "ABCL"
    assets = root / "Assets" / "ABCL"
    previews = root / "Previews" / "ABCL"
    files = [p for p in root.rglob("*") if p.is_file()]
    if any(any(token.lower() in p.name.lower() for token in FORBIDDEN)
           or p.suffix.lower() == ".dll" for p in files):
        raise ValueError("Protected game binary, original atlas, or key in export")

    svgs = sorted(source.glob("*.svg"))
    if {p.name for p in svgs} != EXPECTED_SVG:
        raise ValueError(
            f"Expected exactly 8 device views plus workbench icon SVG; got "
            f"{sorted(p.name for p in svgs)}"
        )
    for path in svgs:
        validate_svg_text(path.read_text(encoding="utf-8"), path.name)

    atlas_path = assets / "equipment_atlas.png"
    atlas = _check_png(atlas_path, (2048, 1024), "RGBA", "Object atlas")
    frames = []
    for index in range(8):
        crop = atlas.crop((index * 128, 0, (index + 1) * 128, 128))
        alpha = crop.getchannel("A")
        bbox = alpha.getbbox()
        if not bbox or alpha.getextrema()[0] == 255:
            raise ValueError(f"Missing transparent subject in atlas frame {index}")
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if bbox[3] < 126:
            raise ValueError(f"Frame {index} does not meet the native-cell contact baseline: {bbox}")
        if index < 4:
            if not (100 <= width <= 120 and 100 <= height <= 112):
                raise ValueError(f"Mass-spectrometer footprint out of native reference range: {bbox}")
        else:
            if not (90 <= width <= 110 and 78 <= height <= 90):
                raise ValueError(f"Digestion-workstation footprint out of native reference range: {bbox}")
        if sum(0 < value < 255 for value in alpha.getdata()) < 100:
            raise ValueError(f"Insufficient antialiased edge pixels in frame {index}")
        frames.append(crop.tobytes())
    if len(set(frames)) != 8:
        raise ValueError("All eight directional frames must be distinct")

    for name in EXPECTED_ASSETS - {"equipment_atlas.png"}:
        icon = _check_png(assets / name, (64, 64), "RGBA", "Custom object icon")
        bbox = icon.getchannel("A").getbbox()
        if not bbox or bbox[0] < 2 or bbox[1] < 2 or bbox[2] > 62 or bbox[3] > 62:
            raise ValueError(f"Icon must keep its artwork inside the 60x60 safe area: {name} {bbox}")

    _check_png(previews / "direction_preview.png", (1024, 256), "RGBA", "Native preview")
    _check_png(previews / "review_mobile.png", (1024, 560), "RGBA", "Mobile review preview")

    manifests = list(root.glob("art_manifest.json"))
    if len(manifests) != 1:
        raise ValueError(f"Expected one generated JSON manifest, got {len(manifests)}")
    manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
    if manifest.get("schema") != "ABCL-ART-001-v7-native-bounds-review-only":
        raise ValueError("Unexpected source schema")
    if manifest.get("atlas_layout") != "LAYOUT_16_X_8":
        raise ValueError("Unexpected atlas layout")
    if manifest.get("atlas_size_px") != [2048, 1024] or manifest.get("cell_px") != 128:
        raise ValueError("Atlas manifest dimensions/cell size mismatch")
    if manifest.get("shared_baseline_y_px") != 127:
        raise ValueError("Manifest baseline does not match native-cell contact edge")
    if manifest.get("directions") != list(DIRECTIONS):
        raise ValueError("Unexpected directional ordering")
    if manifest.get("icons") != {
        "icp_ms": "icp_ms_icon.png",
        "digestion_station": "digestion_station_icon.png",
        "workbench": "workbench_icon.png",
    }:
        raise ValueError("Custom icon manifest mismatch")
    all_by_name = {p.name: p for p in files}
    expected_hashes = manifest.get("sha256", {})
    for name, expected_hash in expected_hashes.items():
        path = all_by_name.get(name)
        if path is None or hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash:
            raise ValueError(f"Checksum mismatch or missing file: {name}")
    if set(expected_hashes) != (
        EXPECTED_SVG | EXPECTED_ASSETS | EXPECTED_PREVIEWS
    ):
        raise ValueError("Manifest hash inventory does not match the exact export allowlist")
    if len(files) != 16:
        raise ValueError(f"Unexpected files in review-only export: expected 16, got {len(files)}")

    print("PASS: 8 native-scale directional sprites, 3 safe-area custom icons, 9 safe SVG sources")
    print("PASS: 16x8 RGBA atlas, native baseline/footprint, previews, full SHA256 inventory")
    print("SOURCE ONLY — not a gameplay, placement, animation, staff-pathfinding or L4 verification")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    verify(parser.parse_args().output)
