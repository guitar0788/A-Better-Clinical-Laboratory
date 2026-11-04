#!/usr/bin/env python3
"""Independent ABCL ART-001 device visibility/readiness *source-only* audit.

The G1 room and the two new machine objects are read-only. Source evidence
does NOT prove actual build-menu, staff path, room readiness or clinical use.
"""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOM_ID = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB"
PRIVATE_ROOM_TAG = "abcl_g1_toxicology_lab"
EXPECTED_DEVICES = {
    "OBJECT_ABCL_ART001_ICP_MS": "abcl_art001_icp_ms",
    "OBJECT_ABCL_ART001_DIGESTION": "abcl_art001_digestion",
}
NATIVE_CLINICAL_TAGS = {
    "hematoanalyzer", "stat_lab_exam", "ui_hematoanalyzer", "ui_ria",
    "RIA", "thermal_cycler", "ui_pc", "ui_print", "ui_glassware",
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def strings(parent, query):
    return [(item.text or "").strip() for item in parent.findall(query)]


def verify(candidate: Path, g1_room: Path) -> dict:
    objs = ET.parse(candidate).getroot()
    rooms = ET.parse(g1_room).getroot()
    require(objs.tag == "Database" and rooms.tag == "Database", "Invalid GameDB root")
    entries = objs.findall("GameDBObject")
    by_id = {e.get("ID"): e for e in entries}
    require(len(entries) == 2 and set(by_id) == set(EXPECTED_DEVICES),
            "Expected only two standalone ABCL devices; no legacy workbench")
    room_defs = rooms.findall("GameDBRoomType")
    require(len(room_defs) == 1 and room_defs[0].get("ID") == ROOM_ID,
            "Unexpected G1 room; original/toxicology room ownership must be preserved")
    room = room_defs[0]
    tags = strings(room, "Tags/Tag")
    require(PRIVATE_ROOM_TAG in tags and "stat_lab" in tags,
            "G1 original lab identity/service routing changed")
    filters = strings(room, "BuildingModeFilters/Tag")
    require(len(filters) == len(set(filters)) and "ui_lab_equipment" in filters,
            "G1 needs its original UI laboratory-equipment category")

    requirements = {}
    for item in room.findall("RequiredEquipment/GameDBRequiredEquipment"):
        key = (item.findtext("Tag") or "").strip()
        require(key and key not in requirements, "Duplicate/missing G1 room requirement")
        count_text = item.findtext("MinCount")
        require(count_text is not None and int(count_text) >= 0,
                "Invalid G1 room requirement minimum")
        requirements[key] = int(count_text)
    require(requirements.get("ui_hematoanalyzer", -1) == 1
            and requirements.get("ui_ria", -1) == 1,
            "Original G1 R3 clinical equipment preconditions must remain intact")
    require(requirements.get("thermal_cycler", -1) == 1,
            "Original G1 lab thermal-cycler requirement unexpectedly changed")
    require(all(not x.startswith("abcl_art001_") for x in requirements),
            "Unapproved new private equipment unexpectedly made mandatory")

    decisions = {}
    for key, private_tag in EXPECTED_DEVICES.items():
        o = by_id[key]
        obj_tags = strings(o, "Tags/Tag")
        require(len(obj_tags) == len(set(obj_tags))
                and private_tag in obj_tags and "ui_lab_equipment" in obj_tags
                and "ui_equipment" in obj_tags,
                "Missing private function or native building-category tag: " + key)
        require(not set(obj_tags).intersection(NATIVE_CLINICAL_TAGS),
                "New device impersonates original clinical equipment: " + key)
        require(o.findtext("AttachedToObject") == "false"
                and o.findtext("Placement") == "INDOORS",
                "Device is not a native independent indoor object")
        require(o.find("AttachmentSlot") is None, "Device unexpectedly needs a parent")
        require(o.findtext("SpriteShape") == "SHAPE_1_X_1",
                "Native single-cell model assumptions changed")
        eligible = set(obj_tags).intersection(filters)
        require("ui_lab_equipment" in eligible,
                "Device is not discoverable by existing G1 lab build-mode filter")
        require(not set(obj_tags).intersection(requirements),
                "Device accidentally satisfies vanilla/preapproved R3 room prerequisites")
        decisions[key] = {
            "native_room_filter_match_source": sorted(eligible),
            "private_function_tag": private_tag,
            "standalone_candidate": True,
            "fulfills_existing_G1_required_equipment": False,
            "actually_placeable": "L4_NOT_RUN",
            "staff_operable": "L4_NOT_RUN",
            "may_appear_in_other_vanilla_lab_build_menus": True,
        }

    return {
        "scope": "SOURCE_ONLY_ROOM_FILTER_GATE",
        "original_G1_room_id": ROOM_ID,
        "required_hematoanalyzer_and_ria": "UNCHANGED",
        "testable_build_filter": "ui_lab_equipment",
        "note": "Generic native build category may be shared with vanilla labs; "
                "not proof of Toxicology-only menu isolation.",
        "devices": decisions,
        "clinical_assay_dispatch": "NOT_IMPLEMENTED_FOR_NEW_DEVICES",
        "original_CBC_and_lab_gameplay": "NOT_TESTED_BY_SOURCE_GATE",
        "four_DLC_Workshop": "UNTESTED",
        "L4": "NOT_RUN",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--g1-room", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.candidate, args.g1_room)
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.exists():
            raise FileExistsError("Will not overwrite previous source gate")
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")
