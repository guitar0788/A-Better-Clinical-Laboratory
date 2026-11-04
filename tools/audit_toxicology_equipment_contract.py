#!/usr/bin/env python3
"""Fail-closed static audit of integrated ABCL toxicology room and lab tags.

Checks only the ABCL addon. Never alters a game, installed mod, original XML
or original artwork. No actual gameplay / patient L4 claim.
"""
import argparse
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET

ROOM = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB"
TEST = "EXM_ABCL_G1_BLOOD_LEAD_TESTING"
INSTRUMENTS = {
    "OBJECT_ABCL_ART001_DIGESTION": "abcl_art001_digestion",
    "OBJECT_ABCL_ART001_ICP_MS": "abcl_art001_icp_ms",
}
FORBIDDEN_ROOM = {"ui_hematoanalyzer", "ui_ria", "thermal_cycler"}
EXPECTED_STEPS = [
    "stat_lab_exam", "abcl_art001_digestion", "abcl_art001_icp_ms",
    "biohazard_trash", "clean_hands"
]

def check(ok, message):
    if not ok:
        raise ValueError(message)

def audit(path: Path):
    path = path.resolve(strict=True)
    db = path / "Database"
    room_db = ET.parse(db / "ModRoomTypes.xml").getroot()
    rooms = [x for x in room_db.findall("GameDBRoomType") if x.get("ID") == ROOM]
    check(len(rooms) == 1, "Expected one owned Toxicology Lab room type")
    room = rooms[0]
    check(room.findtext("IconIndex") == "3070" and room.findtext("TextureID") == "491",
          "Room must use isolated blank fallback slots (not vanilla hematology icons)")
    reqs = room.findall("./RequiredEquipment/GameDBRequiredEquipment")
    requirements = {x.findtext("Tag"): int(x.findtext("MinCount", "-1")) for x in reqs}
    check(len(reqs) == len(requirements), "Duplicate required equipment tag")
    for tag in INSTRUMENTS.values():
        check(requirements.get(tag) == 1, "Private instrument missing mandatory MinCount=1: " + tag)
    check(not (FORBIDDEN_ROOM & requirements.keys()), "Copied vanilla hematology requirements found")
    for t in ("ui_pc", "ui_print", "ui_glassware", "ui_lab_sink", "ui_biohazard_bin"):
        check(requirements.get(t) == 1, "Missing core laboratory support equipment: " + t)

    objects = ET.parse(db / "ModObjectsABCL.xml").getroot()
    ids = Counter(x.get("ID") for x in objects.findall("GameDBObject"))
    check(set(ids) == set(INSTRUMENTS) and all(n == 1 for n in ids.values()),
          "Expected exactly two private standalone instruments, no workbench or duplicates")
    for obj in objects.findall("GameDBObject"):
        name = obj.get("ID")
        tags = [x.text for x in obj.findall("./Tags/Tag")]
        check(tags.count(INSTRUMENTS[name]) == 1, "Private equipment tag missing/nonunique: " + name)
        check(obj.findtext("AttachedToObject") == "false" and obj.findtext("Placement") == "INDOORS",
              "Equipment lost its approved independent-placement contract: " + name)
        check(not (set(tags) & FORBIDDEN_ROOM), "Private equipment impersonates vanilla lab")

    exam_db = ET.parse(db / "ModExaminations.xml").getroot()
    entries = [e for e in exam_db.findall("GameDBExamination") if e.get("ID") == TEST]
    check(len(entries) == 1, "Expected one private G1 blood-lead analysis")
    lab = entries[0]
    steps = lab.findall("./Procedure/RequiredEquipmentList/RequiredEquipment")
    tags = [x.findtext("Tag") for x in steps]
    check(tags == EXPECTED_STEPS, "G1 lead procedure still targets old or missing equipment")
    check(lab.findtext("./Procedure/RequiredRoomTags/Tag") == "abcl_g1_toxicology_lab",
          "G1 procedure could route into a vanilla CBC room")

    room_assets = ET.parse(db / "ModAssetListsTO001.xml").getroot()
    atlas = [x for x in room_assets.findall("GameDBAsset")
             if x.get("ID") == "ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS"]
    check(len(atlas) == 1 and
          atlas[0].findtext("File") == "MOD_ROOT/Assets/ABCL/toxicology_floor_atlas_private_491.png",
          "Private floor texture must match TextureID=491")
    check((path / "Assets" / "ABCL" / "toxicology_floor_atlas_private_491.png").is_file(),
          "Private floor atlas not bundled")
    check(not (db / "RoomTypes.xml").exists() and not (db / "Examinations.xml").exists(),
          "Accidental core game database replacements in addon")
    return {
        "status": "L2_OFFLINE_CONTRACT_PASS",
        "room": ROOM, "required_devices": sorted(INSTRUMENTS.values()),
        "procedure_steps": tags,
        "original_CBC_examination_replaced": False,
        "game_L4": "NOT_RUN",
        "prefabs_V3": "UNCHANGED; add both instruments after prefab placement until V4 integration",
    }

if __name__ == "__main__":
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument("addon_root", type=Path)
    print(json.dumps(audit(parser.parse_args().addon_root), indent=2))
