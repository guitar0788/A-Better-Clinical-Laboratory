#!/usr/bin/env python3
"""Report static G1 room-tag eligibility against a private, local game database.

Do not commit game XML or use this report as proof of gameplay (L4).
"""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

PATIENT_DEPARTMENTS = ("DPT_EMERGENCY", "DPT_INTERNAL_MEDICINE_DEPARTMENT")
LAB_DEPARTMENT = "DPT_LAB"
ABCL_ROOM = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB"
ABCL_SAMPLE = "EXM_ABCL_G1_BLOOD_LEAD_SAMPLING"
ABCL_TEST = "EXM_ABCL_G1_BLOOD_LEAD_TESTING"


def entries(path):
    return {item.get("ID"): item for item in ET.parse(str(path)).getroot()
            if item.get("ID")}


def tags(item, path="./Tags/Tag"):
    return [node.text for node in item.findall(path) if node.text]


def allowed_room_types(department):
    groups = ("RequiredRoomsClinic", "RequiredRoomsHospitalization",
              "SharedRoomsHospitalization")
    return [node.text for group in groups
            for node in department.findall(
                "./%s/GameDBDepartmentRoomRequirement/RoomDatabaseEntryRef" % group)
            if node.text]


def classify(department_id, department, rooms, sample, test):
    available = {tag for room_id in allowed_room_types(department)
                 if room_id in rooms for tag in tags(rooms[room_id])}
    sampling_tags = tags(sample, "./Procedure/RequiredRoomTags/Tag")
    testing_tags = tags(test, "./Procedure/RequiredRoomTags/Tag")
    sample_allowed = bool(available.intersection(sampling_tags))
    test_allowed = bool(available.intersection(testing_tags))
    return {
        "department": department_id,
        "sample_tags": sampling_tags,
        "test_tags": testing_tags,
        "sample_type_allowed": sample_allowed,
        "test_type_allowed": test_allowed,
        "lab_fallback": test.findtext("./Procedure/FallbackLabDepartmentRef"),
        "warning": ("Source-level NOT_AVAILABLE_DEPARTMENT branch is possible; "
                    "the vanilla CBC may produce the same result"
                    if not sample_allowed or not test_allowed else
                    "Static room-type check passes; runtime dispatch still unverified"),
    }


def audit(game_db, addon_db):
    departments = entries(game_db / "Departments.xml")
    rooms = entries(game_db / "RoomTypes.xml")
    rooms.update(entries(addon_db / "ModRoomTypes.xml"))
    base_exams = entries(game_db / "Procedures" / "Examinations.xml")
    custom = entries(addon_db / "ModExaminations.xml")
    if ABCL_SAMPLE not in custom or ABCL_TEST not in custom:
        raise ValueError("ABCL sampling/testing pair missing")
    if custom[ABCL_SAMPLE].findtext("LabTestingExaminationRef") != ABCL_TEST:
        raise ValueError("ABCL sampling/testing pair is disconnected")
    if ABCL_ROOM not in rooms:
        raise ValueError("ABCL room ID missing")
    room_tags = tags(rooms[ABCL_ROOM])
    test_tags = tags(custom[ABCL_TEST], "./Procedure/RequiredRoomTags/Tag")
    if "stat_lab" not in room_tags or "abcl_g1_toxicology_lab" not in room_tags:
        raise ValueError("ABCL room lacks dedicated native stat-lab tags")
    if "abcl_g1_toxicology_lab" not in test_tags:
        raise ValueError("ABCL examination lost dedicated routing tag")
    if custom[ABCL_TEST].findtext("./Procedure/FallbackLabDepartmentRef") != LAB_DEPARTMENT:
        raise ValueError("ABCL lab test lacks DPT_LAB fallback")
    if custom[ABCL_TEST].findtext("./Procedure/RequiredStatLabQualificationRef") != "SKILL_LAB_SPECIALIST_QUALIF_SCIENCE_EDUCATION":
        raise ValueError("ABCL examination does not require vanilla lab specialist skill")

    lab_allowed_rooms = set(allowed_room_types(departments[LAB_DEPARTMENT]))
    # The test-only installer appends this optional room to DPT_LAB at install time.
    lab_allowed_rooms.add(ABCL_ROOM)
    lab_tags = {t for room in lab_allowed_rooms if room in rooms
                for t in tags(rooms[room])}
    if not lab_tags.intersection(test_tags):
        raise ValueError("DPT_LAB fallback cannot have a room matching the G1 test")

    result = {
        "purpose": "offline XML/source-path diagnostic; NOT L3 or L4",
        "abcl_room": ABCL_ROOM,
        "abcl_has_stat_lab": True,
        "lab_fallback_has_test_tag_after_installer": True,
        "departments": [],
        "vanilla_cbc_control": [],
        "result": "STATIC_ROUTE_REVIEW_REQUIRED",
    }
    for department_id in PATIENT_DEPARTMENTS:
        if department_id not in departments:
            raise ValueError("Missing game department: " + department_id)
        department = departments[department_id]
        result["departments"].append(
            classify(department_id, department, rooms,
                     custom[ABCL_SAMPLE], custom[ABCL_TEST]))
        result["vanilla_cbc_control"].append(
            classify(department_id, department, rooms,
                     base_exams["EXM_CBC_SAMPLING"], base_exams["EXM_CBC_TESTING"]))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-db", type=Path, required=True,
                        help="Local game's StreamingAssets/Database path (never uploaded)")
    parser.add_argument("--addon-db", type=Path,
                        default=Path(__file__).resolve().parents[1] /
                        "assets/g1/Database")
    args = parser.parse_args()
    print(json.dumps(audit(args.game_db, args.addon_db), indent=2,
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
