"""Source-only G1 validation; does not claim game compilation or gameplay."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "assets/g1/Database"

class G1ContractTests(unittest.TestCase):
    def test_only_abcl_owned_data_files_are_committed(self):
        self.assertEqual({p.name for p in DB.glob("*.xml")}, {
            "ModAddon.xml", "ModRoomTypes.xml", "ModExaminations.xml",
            "ModStringTableEnABCL.xml", "ModStringTableZhHansABCL.xml"
        })
        self.assertFalse((DB / "ModDepartments.xml").exists())
        self.assertFalse((DB / "ModDiagnoses.xml").exists())
        self.assertFalse((DB / "ModSymptoms.xml").exists())

    def test_new_exam_ref_and_room_route(self):
        ex = ET.parse(DB / "ModExaminations.xml").getroot()
        entries = {x.get("ID"):x for x in ex.findall("GameDBExamination")}
        sampling = "EXM_ABCL_G1_BLOOD_LEAD_SAMPLING"
        testing = "EXM_ABCL_G1_BLOOD_LEAD_TESTING"
        self.assertEqual(set(entries), {sampling, testing})
        self.assertEqual(entries[sampling].findtext("LabTestingExaminationRef"), testing)
        tags = [x.text for x in entries[testing].findall(".//RequiredRoomTags/Tag")]
        self.assertEqual(tags, ["abcl_g1_toxicology_lab"])
        rooms = ET.parse(DB / "ModRoomTypes.xml").getroot()
        room = rooms.find("GameDBRoomType")
        self.assertEqual(room.get("ID"), "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB")
        self.assertIn("abcl_g1_toxicology_lab", [t.text for t in room.findall(".//Tags/Tag")])

    def test_lead_case_uses_native_immobile_ambulance_route(self):
        """TRM_LDP's required original high-lead symptom is IMOBILE.

        Contract-only: this never pretends to prove ambulance arrival in-game.
        """
        script = (ROOT / "src/ABCLG1Panel.cs").read_text(encoding="utf-8")
        self.assertIn("PatientMobility.IMOBILE", script)
        self.assertNotIn("lead, PatientMobility.MOBILE", script)
        self.assertIn("HasAnyInpatientDepartment()", script)
        self.assertIn("GetRandomDepartmentWithDiagnoses(PatientMobility.IMOBILE)", script)
        self.assertIn("GetAmbulanceCount() < 1", script)
        self.assertIn("m_immobileSpawnedToday <= 0", script)
        self.assertIn("insurer.m_gameDBInsuranceCompany.Entry", script)
        self.assertIn("queued for native ambulance arrival", script)

    def test_test_panel_is_not_implicitly_alpha_enabled(self):
        script = (ROOT / "src/ABCLG1Panel.cs").read_text(encoding="utf-8")
        self.assertIn("CreateCharacterPatient", script)
        self.assertIn("TRM_LDP", script)
        self.assertIn("private void SpawnOne()", script)
        self.assertNotIn("Harmony.Patch", script)
        doc = (ROOT / "docs/G1_BUILD.md").read_text(encoding="utf-8")
        self.assertIn("NOT RUN", doc)
        self.assertIn("never", doc.lower())

if __name__ == "__main__":
    unittest.main()
