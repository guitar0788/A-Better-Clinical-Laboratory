"""Source-only G1 contract; no gameplay or L3 claim."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "assets/g1/Database"
PANEL = ROOT / "src/ABCLG1Panel.cs"
INSTALLER = ROOT / "tools/Install-ABCL-G1.ps1"

class G1ContractTests(unittest.TestCase):
    def test_only_additive_abcl_owned_database_files(self):
        self.assertEqual({p.name for p in DB.glob("*.xml")}, {
            "ModAddon.xml", "ModRoomTypes.xml", "ModExaminations.xml",
            "ModStringTableEnABCL.xml", "ModStringTableZhHansABCL.xml",
            "ModAssetListsTO001.xml"
        })
        for name in ("ModDepartments.xml", "ModDiagnoses.xml", "ModSymptoms.xml"):
            self.assertFalse((DB / name).exists())

    def test_sampling_route_is_private_and_cbc_is_not_overridden(self):
        ex = ET.parse(DB / "ModExaminations.xml").getroot()
        entries = {x.get("ID"): x for x in ex.findall("GameDBExamination")}
        sample = "EXM_ABCL_G1_BLOOD_LEAD_SAMPLING"
        testing = "EXM_ABCL_G1_BLOOD_LEAD_TESTING"
        self.assertEqual(set(entries), {sample, testing})
        self.assertEqual(entries[sample].findtext("LabTestingExaminationRef"), testing)
        tags = [x.text for x in entries[testing].findall(".//RequiredRoomTags/Tag")]
        self.assertEqual(tags, ["abcl_g1_toxicology_lab"])
        room = ET.parse(DB / "ModRoomTypes.xml").getroot().find("GameDBRoomType")
        self.assertEqual(room.get("ID"), "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB")
        self.assertIn("abcl_g1_toxicology_lab", [x.text for x in room.findall(".//Tags/Tag")])

    def test_only_native_r3_patient_path_remains(self):
        source = PANEL.read_text(encoding="utf-8")
        installer = INSTALLER.read_text(encoding="utf-8")
        for forbidden in ("ABCLSuperGmTestPanel", "superGm", "ForceMobilePatient",
                          "SpawnOne()", "DIA_CLD", "DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE"):
            self.assertNotIn(forbidden, source)
        for forbidden in ("Add-PrivateC1Fixture", "DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE",
                          "DiagnosesER.xml", "'DIA_CLD'"):
            self.assertNotIn(forbidden, installer)
        self.assertIn('GetEntry<GameDBMedicalCondition>("TRM_LDP")', source)
        self.assertIn("SpawnNativeLead(lead, insurer)", source)
        self.assertIn("LopitalEntityFactory.CreateCharacterPatient(", source)
        self.assertIn("PatientMobility.IMOBILE", source)
        self.assertIn("if (!$NativeLeadTest)", installer)
        self.assertIn("'TRM_LDP'", installer)
        self.assertNotIn("DiagnosesER.xml", installer)
        self.assertNotIn("Harmony.Patch", source)

    def test_toxicology_menu_and_floor_assets_are_registered_separately(self):
        assets = ET.parse(DB / "ModAssetListsTO001.xml").getroot()
        rows = {x.get("ID"): x for x in assets.findall("GameDBAsset")}
        self.assertEqual(set(rows), {
            "ASSET_ABCL_TOXICOLOGY_ROOM_ICON",
            "ASSET_ABCL_TOXICOLOGY_ROOM_ICON_INACTIVE",
            "ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS",
        })
        self.assertEqual(rows["ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS"].findtext("Type"), "TEXTURE")
        self.assertEqual(rows["ASSET_ABCL_TOXICOLOGY_ROOM_ICON"].findtext("Type"), "TEXTURE_CUSTOM_SPRITE")
        self.assertIn("toxicology_floor_atlas_private_376.png",
                      rows["ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS"].findtext("File"))
        self.assertIn("G1ToxicologyPrivateFloorIconAdapter", source := PANEL.read_text("utf-8"))
        self.assertIn("to001FloorIcon.LateTick()", source)

if __name__ == "__main__":
    unittest.main()
