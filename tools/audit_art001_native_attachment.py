#!/usr/bin/env python3
"""Read-only native ART-001 placement/rotation preflight.

Consmes the FA art branch's existing additive XML. Does not open Unity, edit
GameDB, generate art, ship game code, or assume L4 completion.

Native evidence: Lopital.Floor.CanPlaceObject(), GameDBObject.AcceptsAttachment(),
Floor.GetForcedOrientation(), ObjectRenderer.GetTextureCoords() in the owner's
unmodified decompiled original game sources (reviewed read-only).
"""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

DIRECTIONS = ("NW", "NE", "SE", "SW")
WORKBENCH = "OBJECT_ABCL_ART001_WORKBENCH"
DEVICES = {
    "OBJECT_ABCL_ART001_ICP_MS": ("abcl_art001_icp_ms", (0, 1, 2, 3)),
    "OBJECT_ABCL_ART001_DIGESTION": ("abcl_art001_digestion", (4, 5, 6, 7)),
}
FORBIDDEN_NATIVE_TAGS = {
    "hematoanalyzer", "stat_lab_exam", "RIA", "lab_eq_small", "lab_analyzer",
}
ORIGINAL_TABLE_IDS = {"OBJECT_TABLE_EQUIPMENT", "OBJECT_TABLE_SQUERE"}
ORIGINAL_DEVICE_IDS = {"OBJECT_HEMATOLOGY_ANALYZER", "OBJECT_RIA"}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def parse(path):
    root = ET.parse(path).getroot()
    require(root.tag == "Database", "Expected GameDB XML Database root")
    return root


def word(node, path):
    v = node.findtext(path)
    return (v or "").strip()


def tags(node, path):
    return [str(e.text or "").strip() for e in node.findall(path)]


def validate(database: Path) -> dict:
    """Analyze the existing exact FA XML only. Raises on unsafe conflicts.

    Source proof != runtime placement: room-specific access, staff interaction,
    occlusion and saved-game behavior require a later, focused real-game L4.
    """
    database = Path(database)
    objects_root = parse(database / "ModObjectsABCL.xml")
    assets_root = parse(database / "ModAssetListsABCL.xml")
    object_entries = objects_root.findall("GameDBObject")
    asset_entries = assets_root.findall("GameDBAsset")
    objects = {e.get("ID"): e for e in object_entries}
    assets = {e.get("ID"): e for e in asset_entries}
    require(len(objects) == len(object_entries), "Duplicate GameDBObject IDs")
    require(len(assets) == len(asset_entries), "Duplicate GameDBAsset IDs")
    require(set(objects) == {WORKBENCH, *DEVICES},
            "Do not add/overwrite native or unrelated GameDB objects")
    require(all(x.startswith("ASSET_ABCL_ART001_") or x == "ASSET_TEX_ABCL_ART001_EQUIPMENT"
                for x in assets), "Do not define shared or original game asset IDs")
    require(not (set(objects) & (ORIGINAL_TABLE_IDS | ORIGINAL_DEVICE_IDS)),
            "Must never replace original workbench or analyzers")

    parent = objects[WORKBENCH]
    require(word(parent, "AttachedToObject") == "false",
            "Private workbench must itself be a center object")
    require(word(parent, "Placement") == "INDOORS", "Private workbench must be indoors")
    require(word(parent, "SpriteShape") == "SHAPE_1_X_1",
            "Source contract is one occupied native tile per workbench")
    require(word(parent, "TextureRef") == "ASSET_TEX_OBJECTS_SMALL",
            "Review only the original vanilla workbench source reference")
    require(word(parent, "TextureAtlasLayout") == "LAYOUT_16_X_64",
            "Workbench source atlas layout changed")
    require(word(parent, "AttachmentSlot/ForcesAttachmentOrientation") == "false",
            "Parent would force child orientation, contrary to four-view plan")
    require(parent.find("ConnectedSlots") is None,
            "Parent connected slots could force orientation or create another placement path")
    slot = parent.find("AttachmentSlot")
    require(slot is not None, "Workbench must have AttachmentSlot")
    allowed = tags(parent, "AttachmentSlot/AllowedTags/Tag")
    require(len(allowed) == 2 and set(allowed) == set(x[0] for x in DEVICES.values()),
            "Parent allowed tags must match exactly two isolated child tags")
    require(not set(allowed) & FORBIDDEN_NATIVE_TAGS, "Vanilla clinical equipment tag collision")
    require([int(word(parent, "TextureID" + direction)) for direction in DIRECTIONS]
            == [472, 473, 474, 475],
            "Original 4-direction workbench source refs changed")

    require(set(assets) == {
        "ASSET_TEX_ABCL_ART001_EQUIPMENT",
        "ASSET_ABCL_ART001_ICON_ICPMS",
        "ASSET_ABCL_ART001_ICON_DIGESTION",
        "ASSET_ABCL_ART001_ICON_WORKBENCH",
    }, "ART001 must only register one private texture and three private icons")
    atlas = assets["ASSET_TEX_ABCL_ART001_EQUIPMENT"]
    require(word(atlas, "Type") == "TEXTURE_OBJECTS"
            and word(atlas, "File") == "MOD_ROOT/Assets/ABCL/equipment_atlas.png",
            "Native 16x8 object atlas binding was altered")

    diagnostics = {}
    for obj_id, (private_tag, direction_indices) in DEVICES.items():
        obj = objects[obj_id]
        tagset = tags(obj, "Tags/Tag")
        require(len(tagset) == len(set(tagset)), "Duplicate device tag: " + obj_id)
        require(private_tag in tagset and all(t not in tagset
                for t in (set(allowed) - {private_tag})),
                "Each instrument must match exactly one private parent tag: " + obj_id)
        require(not set(tagset) & FORBIDDEN_NATIVE_TAGS,
                "Device impersonates a vanilla laboratory tag: " + obj_id)
        require(word(obj, "AttachedToObject") == "true",
                "Instrument requires a native attachment parent: " + obj_id)
        require(word(obj, "SpriteShape") == "SHAPE_1_X_1",
                "Native equipment contract is a single tile: " + obj_id)
        require(word(obj, "TextureRef") == "ASSET_TEX_ABCL_ART001_EQUIPMENT"
                and word(obj, "TextureAtlasLayout") == "LAYOUT_16_X_8",
                "Unsupported or unowned native 4-view atlas: " + obj_id)
        require([int(word(obj, "TextureID" + d)) for d in DIRECTIONS]
                == list(direction_indices), "Native NW/NE/SE/SW atlas IDs changed: " + obj_id)
        require(obj.find("ConnectedSlots") is None,
                "Unexpected connected-slot forced direction: " + obj_id)
        require(obj.find("AttachmentSlot") is None,
                "Do not introduce nested attachments on a tabletop instrument")
        require(obj.find("RequiredObjectsInRoom") is None,
                "No unverified original-room equipment mutation/requirement")
        require(word(obj, "NotInteractable") != "true",
                "Instrument would be deliberately non-interactable: " + obj_id)
        require(all(obj.find("UseAnimations" + x) is not None
                for x in ("", "Start", "End")),
                "Missing native staff animation refs: " + obj_id)
        require(obj.find("CustomIconAssetRef") is not None,
                "Device private icon missing: " + obj_id)
        diagnostics[obj_id] = {
            "private_tag": private_tag,
            "native_16x8_atlas_slots": dict(zip(DIRECTIONS, direction_indices)),
            "accepted_by_private_parent_source": True,
            "staff_contact": "NOT PROVEN - L4 REQUIRED",
            "real_rotation": "NOT PROVEN - L4 REQUIRED",
        }

    # Critical native source rule (Lopital.Floor.CanPlaceObject):
    # tile.m_attachmentObject is a SINGLE slot, and a second child at the
    # same tile returns NOT_ALLOWED_BLOCKED. AllowedTags is a type ALLOWLIST,
    # not two simultaneous inventory/storage slots.
    return {
        "result": "SOURCE_PREFLIGHT_PASS_NOT_GAME_L4",
        "workbench_id": WORKBENCH,
        "devices": diagnostics,
        "workbench_capacity_per_tile": 1,
        "separate_workbench_instances_needed_to_place_both": 2,
        "same_tile_second_device": "NOT_ALLOWED_BLOCKED (native source)",
        "wrong_parent": "NOT_ALLOWED_ATTACHMENT_NO_PARENT/WRONG_PARENT",
        "allows_rotation_independent_of_parent": True,
        "may_still_be_forced_by_external_connected_slots": True,
        "original_equipment_and_CBC": "UNCHANGED_BY_STAGING_XML; L4 PENDING",
        "four_DLC_and_Workshop": "UNTESTED",
        "native_game_L4": "NOT_RUN",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--art-db", type=Path, required=True)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = validate(args.art_db)
    data = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.exists():
            raise FileExistsError("Never overwrite a previous review report")
        args.output.write_text(data, encoding="utf-8")
    print(data, end="")


if __name__ == "__main__":
    main()
