#!/usr/bin/env python3
"""ART-001 self-based, standalone instrument XML candidate. NOT INSTALLABLE.

Reads the immutable FA branch; does not draw art, patch clinical G1, change
owner-approved prefabs, original game textures or existing ART-001 objects.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET

FA_SHA = "0e8ff6720402961a102a7788dd6bbfe74e9e1d14"
WORKBENCH = "OBJECT_ABCL_ART001_WORKBENCH"
DEVICES = {
    "OBJECT_ABCL_ART001_ICP_MS": ("abcl_art001_icp_ms", (0, 1, 2, 3),
                                "ASSET_ABCL_ART001_ICON_ICPMS"),
    "OBJECT_ABCL_ART001_DIGESTION": ("abcl_art001_digestion", (4, 5, 6, 7),
                                   "ASSET_ABCL_ART001_ICON_DIGESTION"),
}
DIRECTIONS = ("NW", "NE", "SE", "SW")
FORBIDDEN_TAGS = {
    "hematoanalyzer", "stat_lab_exam", "RIA", "lab_eq_small",
    "lab_analyzer", "ui_hematoanalyzer", "ui_ria",
}
ASSETS = {"ASSET_TEX_ABCL_ART001_EQUIPMENT",
          "ASSET_ABCL_ART001_ICON_ICPMS",
          "ASSET_ABCL_ART001_ICON_DIGESTION",
          "ASSET_ABCL_ART001_ICON_WORKBENCH"}


def check(predicate, why):
    if not predicate:
        raise ValueError(why)


def read_xml(source):
    root = ET.fromstring(source)
    check(root.tag == "Database", "Expected GameDB Database XML root")
    return root


def val(obj, path):
    return (obj.findtext(path) or "").strip()


def transform(original_objects, original_assets, en_strings, zh_strings):
    """Derive two standalone center objects, without editing FA's originals."""
    root = read_xml(original_objects)
    objects = root.findall("GameDBObject")
    ids = [o.get("ID") for o in objects]
    check(len(ids) == 3 and set(ids) == {WORKBENCH, *DEVICES},
          "Unexpected GameDBObject IDs in frozen FA snapshot")
    bench = next(x for x in objects if x.get("ID") == WORKBENCH)
    check(val(bench, "AttachedToObject") == "false"
          and bench.find("AttachmentSlot") is not None,
          "FA snapshot is not the known attachment-only baseline")
    allowed = {x.text for x in bench.findall("AttachmentSlot/AllowedTags/Tag")}
    check(allowed == {v[0] for v in DEVICES.values()},
          "FA workbench allows unexpected attachment tags")
    root.remove(bench)

    report = {}
    for obj in root.findall("GameDBObject"):
        name = obj.get("ID")
        private_tag, slots, icon = DEVICES[name]
        check(val(obj, "AttachedToObject") == "true",
              "Unknown source placement model for " + name)
        check(val(obj, "TextureRef") == "ASSET_TEX_ABCL_ART001_EQUIPMENT"
              and val(obj, "TextureAtlasLayout") == "LAYOUT_16_X_8"
              and val(obj, "SpriteShape") == "SHAPE_1_X_1",
              "Private one-tile atlas contract changed for " + name)
        check(tuple(int(val(obj, "TextureID" + d)) for d in DIRECTIONS) == slots,
              "Four-direction atlas ID mismatch for " + name)
        check(val(obj, "CustomIconAssetRef") == icon,
              "Original private item icon binding changed")
        tags = [x.text for x in obj.findall("Tags/Tag")]
        check(len(set(tags)) == len(tags) and private_tag in tags,
              "Missing/duplicate private device tags")
        check(not (set(tags) & FORBIDDEN_TAGS),
              "Device impersonates vanilla lab/CBC equipment")
        check(obj.find("AttachmentSlot") is None
              and obj.find("ConnectedSlots") is None
              and obj.find("RequiredObjectsInRoom") is None,
              "Unexpected nested/connected slot or room mutation")
        check(val(obj, "PlacedToEdge") == "false"
              and val(obj, "AttachedToWall") == "false"
              and val(obj, "NotInteractable") != "true",
              "Device not eligible for independent indoor placement")
        check(obj.find("AccessPositions") is None,
              "Original device already has custom access positions")
        check(all(obj.find("UseAnimations" + suffix) is not None
                  for suffix in ("", "Start", "End")),
              "Tentative native use-animation references were lost")
        obj.find("AttachedToObject").text = "false"
        placement = obj.find("Placement")
        if placement is None:
            placement = ET.SubElement(obj, "Placement")
        placement.text = "INDOORS"
        access = ET.SubElement(obj, "AccessPositions")
        pos = ET.SubElement(access, "AccessPosition")
        ET.SubElement(pos, "m_x").text = "-1"
        ET.SubElement(pos, "m_y").text = "0"
        report[name] = {
            "native_type": "free-standing indoor center object / one tile",
            "built_in_base": "visual source must include it, NOT validated here",
            "private_tag": private_tag,
            "atlas": dict(zip(DIRECTIONS, slots)),
            "candidate_NW_access": [-1, 0],
            "staff_reach": "UNVERIFIED",
            "animation_contact": "UNVERIFIED",
            "real_game_L4": "NOT_RUN",
        }

    assets = read_xml(original_assets)
    a = assets.findall("GameDBAsset")
    check(len(a) == 4 and {x.get("ID") for x in a} == ASSETS,
          "Source contains unknown assets/overrides")
    for x in list(a):
        if x.get("ID") == "ASSET_ABCL_ART001_ICON_WORKBENCH":
            assets.remove(x)
            continue
        check(val(x, "File").startswith("MOD_ROOT/Assets/ABCL/"),
              "Unexpected original/third-party asset path")
        check(val(x, "Type") in {"TEXTURE_OBJECTS", "TEXTURE_CUSTOM_SPRITE"},
              "Unexpected GameDB asset texture type")

    localized = {}
    for locale, raw in (("en", en_strings), ("zh-Hans", zh_strings)):
        tree = read_xml(raw)
        tables = tree.findall("GameDBStringTable")
        check(len(tables) == 1 and val(tables[0], "LanguageCode") == locale,
              "Unexpected locale/code for " + locale)
        body = tables[0].find("LocalizedStrings")
        check(body is not None, "Missing localized strings")
        entries = body.findall("GameDBLocalizedString")
        keys = [val(x, "LocID") for x in entries]
        check(len(entries) == 6 and len(set(keys)) == 6,
              "Expected 4 instrument labels and 2 bench labels")
        for x in list(entries):
            if val(x, "LocID").startswith(WORKBENCH):
                body.remove(x)
        expected = {k + suffix for k in DEVICES for suffix in ("", "_DESCRIPTION")}
        check({val(x, "LocID") for x in body} == expected,
              "Standalone candidate has orphan/stale localization")
        localized[locale] = tree

    return root, assets, localized, report


def stage(fa_root, output):
    fa_root = Path(fa_root).resolve(strict=True)
    output = Path(output).resolve()
    check(not output.exists(), "Refuse overwrite of previous candidate")
    check(not any(part.lower() in {"streamingassets", "addons", "projecthospital_data"}
                  for part in output.parts), "Never stage into the live game")
    head = subprocess.check_output(
        ["git", "-C", str(fa_root), "rev-parse", "HEAD"], text=True).strip()
    check(head == FA_SHA, "Refuse mutable/unreviewed FA art source commit")
    db = fa_root / "assets/art001/Database"
    files = {
        "objects": db / "ModObjectsABCL.xml",
        "assets": db / "ModAssetListsABCL.xml",
        "en": db / "ModStringTableEnABCLArt001.xml",
        "zh": db / "ModStringTableZhHansABCLArt001.xml",
    }
    for key, p in files.items():
        check(p.is_file() and not p.is_symlink(), "Missing original FA XML: " + key)
    inputs = {k: p.read_bytes() for k, p in files.items()}
    objects, assets, localized, report = transform(
        inputs["objects"], inputs["assets"], inputs["en"], inputs["zh"])
    output.mkdir(parents=True)
    db_out = output / "Database"
    db_out.mkdir()
    generated = {
        "ModObjectsABCLSelfStandingCandidate.xml": objects,
        "ModAssetListsABCLSelfStandingCandidate.xml": assets,
        "ModStringTableEnABCLSelfStandingCandidate.xml": localized["en"],
        "ModStringTableZhHansABCLSelfStandingCandidate.xml": localized["zh-Hans"],
    }
    for filename, tree in generated.items():
        (db_out / filename).write_bytes(
            ET.tostring(tree, encoding="utf-8", xml_declaration=True))
    digest = lambda data: hashlib.sha256(data).hexdigest()
    manifest = {
        "status": "SOURCE_ONLY_NOT_INSTALLABLE",
        "frozen_FA_commit": FA_SHA,
        "source_sha256": {k: digest(v) for k, v in inputs.items()},
        "candidate_sha256": {
            n: digest((db_out / n).read_bytes()) for n in generated},
        "device_objects": report,
        "separate_workbench_needed": False,
        "workbench_object_included": False,
        "G1_current_hematoanalyzer_and_RIA_requirements": "UNCHANGED",
        "FA_latest_two_1254px_4view_images": "NOT IN PUBLIC BRANCH",
        "native_game_L4": "NOT_RUN",
        "new_assay_device_binding": "NOT_IMPLEMENTED",
        "approved_TO004_prefabs": "UNCHANGED",
        "D011_tabletop_decision": "REQUIRES OWNER APPROVAL BEFORE REAL IMPLEMENTATION",
    }
    (output / "SELFSTANDING_SOURCE_GATE.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fa-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(stage(args.fa_root, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
