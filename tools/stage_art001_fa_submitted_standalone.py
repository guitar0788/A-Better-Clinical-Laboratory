#!/usr/bin/env python3
"""Exact FA ART-001 sprite -> ABCL self-standing source integration (test only).

No game files are changed; no vanilla/DLC/Workshop bytes or G1 DLLs are shipped.
FA's original source and the eight 128x128 frames are never altered/redrawn.
Only the *staged* private atlas is byte-copied and optional 64px UI previews
are derived by fixed 2:1 resampling from the submitted native NW frame.

This creates a self-contained directory of GameDB proposals, NOT an installer.
Owner visual acceptance, native loader and gameplay L4 are separate gates.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
from xml.etree import ElementTree as ET

FA_SHA = "cb3a7ab5d03e8677dcb84f486a04bf0ea5f8f622"
FA_REL = Path("assets/art001/review_20261103")
EXPECTED_SHEETS = {
    "mass_spectrometer_four_views.png":
        "81f50e232cc275cf4939597f0170f7fde155ae28010b67976c42d6dd5c5e38ae",
    "sample_digestion_four_views.png":
        "a3edefd91d6eedc119856e3efaac613ba14ad4ae1c149a6a882fde70b5e9f708",
}
ATLAS_SHA = "b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651"
DEVICE_NAMES = ("mass_spectrometer", "sample_digestion")
DIRECTIONS = ("NW", "NE", "SE", "SW")
STAGED_XML = (
    "ModObjectsABCL.xml", "ModAssetListsABCL.xml",
    "ModStringTableEnABCLArt001.xml", "ModStringTableZhHansABCLArt001.xml",
)
ROOT = Path(__file__).resolve().parents[1]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(ok: bool, why: str) -> None:
    if not ok:
        raise ValueError(why)


def is_under_game(path: Path) -> bool:
    return any(p.casefold() in {"addons", "streamingassets", "projecthospital_data"}
               for p in path.parts)


def check_manifest(fa: Path) -> tuple[dict, dict]:
    from PIL import Image

    fa = fa.resolve(strict=True)
    actual = subprocess.check_output(
        ["git", "-C", str(fa), "rev-parse", "HEAD"], text=True).strip()
    require(actual == FA_SHA, "FA source is not the literal owner-submitted commit")

    src = fa / FA_REL
    manifest = json.loads((src / "manifest.json").read_text("utf-8"))
    require(manifest["status"] == "APPROVED_FOR_SOURCE_SUBMISSION_ONLY_NOT_RUNTIME_APPROVED",
            "FA source approval may not be reinterpreted as game acceptance")
    require(manifest["atlas_layout"] == [16, 8]
            and manifest["atlas_pixels"] == [2048, 1024]
            and manifest["native_cell_size"] == [128, 128],
            "Changed original GameDB atlas contract")
    require(manifest["production_XML_modified"] is False
            and manifest["game_installable"] is False
            and manifest["l3_with_new_art"] is False
            and manifest["l4_with_new_art"] is False,
            "FA source handoff was improperly promoted without review")

    allowed = {
        str(FA_REL / "diagnostic_equipment_atlas.png"),
        *(str(FA_REL / "original" / n) for n in EXPECTED_SHEETS),
        *(str(FA_REL / "frames" / f"{d}_{r}.png")
          for d in DEVICE_NAMES for r in DIRECTIONS),
    }
    files = manifest["files"]
    require(len(files) == 11 and {e["path"] for e in files} == allowed,
            "Submitted art manifest path set differs from the approved source")
    actual_sha = {}
    for entry in files:
        rel = Path(entry["path"])
        source_file = (fa / rel).resolve(strict=True)
        require(source_file.is_relative_to(src.resolve())
                and source_file.is_file() and not source_file.is_symlink(),
                "Manifest file escaped original FA source or became a symlink")
        raw = source_file.read_bytes()
        require(digest(raw) == entry["sha256"] and len(raw) == entry["bytes"],
                "Owner-approved FA art bytes changed: " + str(rel))
        require(hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
                == entry["git_blob_sha1"], "Original Git blob differs: " + str(rel))
        with Image.open(source_file) as image:
            require(image.format == "PNG" and image.mode == "RGBA"
                    and list(image.size) == entry["dimensions"],
                    "Invalid submitted PNG dimensions/transparency: " + str(rel))
        actual_sha[str(rel)] = digest(raw)

    for name, expected in EXPECTED_SHEETS.items():
        require(actual_sha[str(FA_REL / "original" / name)] == expected,
                "Original FA 1254 image has changed")
    require(actual_sha[str(FA_REL / "diagnostic_equipment_atlas.png")] == ATLAS_SHA,
            "Original FA 2048x1024 atlas changed")
    require(manifest["atlas_indices"] == {
        f"{device}_{direction}": i * 4 + j
        for i, device in enumerate(DEVICE_NAMES)
        for j, direction in enumerate(DIRECTIONS)
    }, "Submitted directional index order changed")
    return manifest, actual_sha


def analyze_and_derive_icons(fa: Path, dest: Path) -> dict:
    from PIL import Image, ImageChops

    source = fa / FA_REL
    assets = dest / "Assets" / "ABCL"
    assets.mkdir(parents=True, exist_ok=True)
    original_atlas = source / "diagnostic_equipment_atlas.png"
    # A literal copy is crucial: never reconstruct or redraw approved pixels.
    shutil.copyfile(original_atlas, assets / "equipment_atlas.png")
    require(digest((assets / "equipment_atlas.png").read_bytes()) == ATLAS_SHA,
            "Staged native object atlas does not equal approved FA bytes")
    frame_report = {}
    with Image.open(original_atlas) as im:
        atlas = im.convert("RGBA")
    blank = Image.new("RGBA", atlas.size, (0, 0, 0, 0))
    for index, (device, direction) in enumerate(
            (x for d in DEVICE_NAMES for x in ((d, r) for r in DIRECTIONS))):
        frame_file = source / "frames" / f"{device}_{direction}.png"
        with Image.open(frame_file) as im:
            frame = im.convert("RGBA")
        require(frame.size == (128, 128), "Invalid actual GameDB frame size")
        blank.alpha_composite(frame, (index * 128, 0))
        alpha = frame.getchannel("A")
        bbox = alpha.getbbox()
        require(bbox is not None, "Empty native FA frame")
        # The source artwork has known alpha-fringe and mechanical continuity
        # risks. Record them without repainting or pretending they are fixed.
        hist = alpha.histogram()
        fringe = sum(hist[1:8])
        frame_report[f"{device}_{direction}"] = {
            "file_sha256": digest(frame_file.read_bytes()),
            "alpha_bbox": list(bbox),
            "fractional_alpha_pixels_1_to_7": fringe,
            "identity": "UNREVIEWED_MECHANICAL_FOUR_WAY_COHERENCE",
            "foot_contact": "UNTESTED",
        }
    require(atlas.tobytes() == blank.tobytes(),
            "Private FA diagnostic atlas differs from 8 original native frames")

    # 64px build-menu thumbnails derived 1:1 from the submitted NW frame,
    # never painted anew. Their appearance is *not* owner approved yet.
    for device, icon_file in (
        ("mass_spectrometer", "icp_ms_icon.png"),
        ("sample_digestion", "digestion_station_icon.png"),
    ):
        with Image.open(source / "frames" / f"{device}_NW.png") as im:
            image = im.convert("RGBA")
            image = image.resize((64, 64), Image.Resampling.LANCZOS)
        image.save(assets / icon_file, format="PNG")

    return {
        "atlas": ATLAS_SHA, "submitted_frames": frame_report,
        "derived_64px_NW_build_icons": {
            name: digest((assets / name).read_bytes())
            for name in ("icp_ms_icon.png", "digestion_station_icon.png")
        },
        "derived_icons_owner_visual_approval": "NOT_REQUESTED_OR_GRANTED",
        "art_source_changed": False,
    }


def stage(fa: Path, output: Path) -> dict:
    fa = Path(fa).resolve(strict=True)
    output = Path(output).resolve()
    require(not output.exists(), "Will not overwrite an earlier staged candidate")
    require(not is_under_game(output), "Refusing to write to an installed game/Addon folder")
    manifest, inventory = check_manifest(fa)

    # Import the already regression-verified PR #40 XML transformation, not
    # the prior table-mounted source. This gives TWO independent center objects.
    spec = importlib.util.spec_from_file_location(
        "selfstanding_gate", ROOT / "tools" / "stage_art001_selfstanding_candidate.py")
    require(spec is not None and spec.loader is not None, "Missing independent-source gate")
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    paths = {
        "objects": fa / "assets/art001/Database/ModObjectsABCL.xml",
        "assets": fa / "assets/art001/Database/ModAssetListsABCL.xml",
        "en": fa / "assets/art001/Database/ModStringTableEnABCLArt001.xml",
        "zh": fa / "assets/art001/Database/ModStringTableZhHansABCLArt001.xml",
    }
    require(all(path.is_file() and not path.is_symlink() for path in paths.values()),
            "FA source GameDB XML missing or unsafe")
    original = {key: path.read_bytes() for key, path in paths.items()}
    objects, assets, locales, native_summary = old.transform(
        original["objects"], original["assets"], original["en"], original["zh"])
    require(len(objects.findall("GameDBObject")) == 2,
            "Derived candidate unexpectedly includes a workbench")
    require(len(assets.findall("GameDBAsset")) == 3,
            "Derived candidate has missing/unapproved game assets")

    output.mkdir(parents=True)
    dbout = output / "Database"
    dbout.mkdir()
    out = {
        "ModObjectsABCL.xml": objects,
        "ModAssetListsABCL.xml": assets,
        "ModStringTableEnABCLArt001.xml": locales["en"],
        "ModStringTableZhHansABCLArt001.xml": locales["zh-Hans"],
    }
    for filename, tree in out.items():
        (dbout / filename).write_bytes(
            ET.tostring(tree, encoding="utf-8", xml_declaration=True))
    art = analyze_and_derive_icons(fa, output)
    require(all((output / "Assets" / "ABCL" / f).is_file()
                for f in ("equipment_atlas.png", "icp_ms_icon.png",
                          "digestion_station_icon.png")), "Missing private game textures")
    files = {
        str(p.relative_to(output)).replace("\\", "/"): digest(p.read_bytes())
        for p in output.rglob("*") if p.is_file()
    }
    record = {
        "status": "G1_RESOURCE_OVERLAY_CANDIDATE_L2_ONLY_NOT_INSTALLABLE",
        "frozen_FA_sha": FA_SHA,
        "existing_TS_independent_center_object_gate": "PR40",
        "original_FA_manifest_hashes_verified": len(inventory),
        "original_FA_xml_sha256": {k: digest(v) for k, v in original.items()},
        "generated_runtime_XML_and_asset_sha256": files,
        "artwork": art,
        "native_objects": native_summary,
        "retains_all_original_vanilla_and_CBC_tags_untouched": True,
        "G1_source_or_DLL_modified": False,
        "TO004_V3_owner_approved_resources_modified": False,
        "new_clinical_instrument_method": "NOT_IMPLEMENTED",
        "independent_game_L4": "NOT_RUN",
        "four_DLC_Workshop": "NOT_TESTED",
        "warnings": [
            "Do not install attached and standalone objects with the same IDs together",
            "Only FA art *submission* accepted; in-game visual quality and 4-view mechanical coherence NOT APPROVED",
            "Derived build-menu icons require separate visual review",
            "The native staff access offset and one-tile cabinet footprint are provisional",
        ],
    }
    (output / "ART001_TS_INTEGRATION_MANIFEST.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fa-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    options = parser.parse_args()
    print(json.dumps(stage(options.fa_root, options.output),
                     indent=2, ensure_ascii=False))
