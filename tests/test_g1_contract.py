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
            "ModStringTableEnABCL.xml", "ModStringTableZhHansABCL.xml",
            "ModAssetListsTO001.xml"
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

    def test_r2_fixture_is_mobile_and_test_only(self):
        """R2 isolates native outpatient lab flow from severe lead admission."""
        script = (ROOT / "src/ABCLG1Panel.cs").read_text(encoding="utf-8")
        installer = (ROOT / "tools/Install-ABCL-G1.ps1").read_text(encoding="utf-8")
        self.assertIn("DIA_CLD", script)
        self.assertIn("PatientMobility.MOBILE", script)
        # R3 deliberately adds an IMOBILE route; isolate the historical R2 method.
        r2_method = script.split("private void SpawnOne()", 1)[1]
        self.assertNotIn("PatientMobility.IMOBILE", r2_method)
        self.assertIn("AcceptsOutpatients()", script)
        self.assertIn("m_patientsSpawnedToday > 0", script)
        self.assertIn("m_gameDBInsuranceCompany.IsValid", script)
        self.assertNotIn("m_gameDBInsuranceCompany != null", script)
        self.assertIn("EXM_ABCL_G1_BLOOD_LEAD_SAMPLING", script)
        self.assertIn("DIA_CLD", installer)
        self.assertIn("DiagnosesER.xml", installer)
        # R3 opt-in branch may mention genuine lead; the default R2 branch must not.
        default_r2 = installer.split("# Previously accepted R2 disposable clinic fixture is still the default.", 1)[1].split("Move-Item -LiteralPath $stage", 1)[0]
        self.assertIn("DIA_CLD", default_r2)
        self.assertNotIn("TRM_LDP", default_r2)
        self.assertNotIn("SYM_LEAD_LEVELS_HIGH", default_r2)
        self.assertIn("original game files unchanged", installer.lower())

    def test_test_panel_is_not_implicitly_alpha_enabled(self):
        script = (ROOT / "src/ABCLG1Panel.cs").read_text(encoding="utf-8")
        self.assertIn("CreateCharacterPatient", script)
        self.assertIn("DIA_CLD", script)
        self.assertIn("PatientMobility.MOBILE", script)
        r2_method = script.split("private void SpawnOne()", 1)[1]
        self.assertNotIn("PatientMobility.IMOBILE", r2_method)
        self.assertIn("private void SpawnOne()", script)
        self.assertNotIn("Harmony.Patch", script)
        doc = (ROOT / "docs/G1_BUILD.md").read_text(encoding="utf-8")
        self.assertIn("NOT RUN", doc)
        self.assertIn("never", doc.lower())


    def test_r3_installer_is_explicit_and_r2_default_is_preserved(self):
        installer = (ROOT / "tools/Install-ABCL-G1.ps1").read_text(encoding="utf-8")
        r3_cmd = (ROOT / "tools/INSTALL_G1_R3.cmd").read_text(encoding="utf-8")
        r2_cmd = (ROOT / "tools/INSTALL_G1.cmd").read_text(encoding="utf-8")
        self.assertIn("[switch]$NativeLeadTest", installer)
        self.assertIn("-NativeLeadTest", r3_cmd)
        self.assertNotIn("-NativeLeadTest", r2_cmd)
        self.assertIn("R3 native TRM_LDP test mode installed", installer)
        self.assertNotIn("OFFLINE REVIEW only", installer)

if __name__ == "__main__":
    unittest.main()
