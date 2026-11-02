"""Synthetic-data tests for G1 native route auditor.

Do not embed proprietary game data or confuse these tests with game L3/L4.
"""
import sys
import tempfile
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from audit_g1_native_route import audit, classify


def add_text(parent, tag, value):
    ET.SubElement(parent, tag).text = value


def room(root, room_id, tag_list):
    item = ET.SubElement(root, "GameDBRoomType", ID=room_id)
    tags = ET.SubElement(item, "Tags")
    for tag in tag_list:
        add_text(tags, "Tag", tag)


def department(root, dept_id, room_list):
    item = ET.SubElement(root, "GameDBDepartment", ID=dept_id)
    allowed = ET.SubElement(item, "RequiredRoomsClinic")
    for room_id in room_list:
        entry = ET.SubElement(allowed, "GameDBDepartmentRoomRequirement")
        add_text(entry, "RoomDatabaseEntryRef", room_id)


def exam(root, exam_id, room_tag, linked=None, fallback=None, qualification=False):
    item = ET.SubElement(root, "GameDBExamination", ID=exam_id)
    proc = ET.SubElement(item, "Procedure")
    required = ET.SubElement(proc, "RequiredRoomTags")
    add_text(required, "Tag", room_tag)
    if fallback:
        add_text(proc, "FallbackLabDepartmentRef", fallback)
    if qualification:
        add_text(proc, "RequiredStatLabQualificationRef",
                 "SKILL_LAB_SPECIALIST_QUALIF_SCIENCE_EDUCATION")
    if linked:
        add_text(item, "LabTestingExaminationRef", linked)


class NativeLabAuditTests(unittest.TestCase):
    def test_missing_patient_room_type_is_not_runtime_proof(self):
        rooms = {
            "OFFICE": ET.fromstring(
                "<GameDBRoomType><Tags><Tag>examinations_basic_equipment</Tag></Tags></GameDBRoomType>"),
            "LAB": ET.fromstring(
                "<GameDBRoomType><Tags><Tag>stat_lab</Tag><Tag>abcl_g1_toxicology_lab</Tag></Tags></GameDBRoomType>"),
        }
        dept = ET.fromstring(
            "<GameDBDepartment><RequiredRoomsClinic><GameDBDepartmentRoomRequirement>"
            "<RoomDatabaseEntryRef>OFFICE</RoomDatabaseEntryRef>"
            "</GameDBDepartmentRoomRequirement></RequiredRoomsClinic></GameDBDepartment>")
        sample = ET.fromstring(
            "<GameDBExamination><Procedure><RequiredRoomTags>"
            "<Tag>examinations_basic_equipment</Tag></RequiredRoomTags></Procedure></GameDBExamination>")
        test = ET.fromstring(
            "<GameDBExamination><Procedure><RequiredRoomTags>"
            "<Tag>abcl_g1_toxicology_lab</Tag></RequiredRoomTags>"
            "<FallbackLabDepartmentRef>DPT_LAB</FallbackLabDepartmentRef>"
            "</Procedure></GameDBExamination>")
        x = classify("DPT_EMERGENCY", dept, rooms, sample, test)
        self.assertTrue(x["sample_type_allowed"])
        self.assertFalse(x["test_type_allowed"])
        self.assertEqual(x["lab_fallback"], "DPT_LAB")
        self.assertIn("vanilla CBC", x["warning"])

    def test_integration_contract_with_synthetic_xml(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base = root / "game"
            addon = root / "addon"
            (base / "Procedures").mkdir(parents=True)
            addon.mkdir()
            rooms = ET.Element("Database")
            room(rooms, "OFFICE", ["examinations_basic_equipment"])
            room(rooms, "HEMATO", ["stat_lab", "hematology_lab"])
            room(rooms, "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB",
                 ["stat_lab", "abcl_g1_toxicology_lab"])
            ET.ElementTree(rooms).write(base / "RoomTypes.xml")
            ET.ElementTree(rooms).write(addon / "ModRoomTypes.xml")
            departments = ET.Element("Database")
            department(departments, "DPT_EMERGENCY", ["OFFICE"])
            department(departments, "DPT_INTERNAL_MEDICINE_DEPARTMENT", ["OFFICE"])
            department(departments, "DPT_LAB", ["HEMATO"])
            ET.ElementTree(departments).write(base / "Departments.xml")
            native_exams = ET.Element("Database")
            exam(native_exams, "EXM_CBC_SAMPLING", "examinations_basic_equipment",
                 linked="EXM_CBC_TESTING")
            exam(native_exams, "EXM_CBC_TESTING", "hematology_lab",
                 fallback="DPT_LAB")
            ET.ElementTree(native_exams).write(base / "Procedures" / "Examinations.xml")
            abcl_exams = ET.Element("Database")
            exam(abcl_exams, "EXM_ABCL_G1_BLOOD_LEAD_SAMPLING",
                 "examinations_basic_equipment",
                 linked="EXM_ABCL_G1_BLOOD_LEAD_TESTING")
            exam(abcl_exams, "EXM_ABCL_G1_BLOOD_LEAD_TESTING",
                 "abcl_g1_toxicology_lab", fallback="DPT_LAB",
                 qualification=True)
            ET.ElementTree(abcl_exams).write(addon / "ModExaminations.xml")
            result = audit(base, addon)
            self.assertTrue(result["lab_fallback_has_test_tag_after_installer"])
            self.assertEqual(result["result"], "STATIC_ROUTE_REVIEW_REQUIRED")
            self.assertEqual(len(result["departments"]), 2)
            for row in result["departments"] + result["vanilla_cbc_control"]:
                self.assertFalse(row["test_type_allowed"])
                self.assertEqual(row["lab_fallback"], "DPT_LAB")


if __name__ == "__main__":
    unittest.main()
