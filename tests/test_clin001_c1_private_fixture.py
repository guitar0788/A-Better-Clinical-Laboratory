"""Negative regression: retired C1 disabled diagnosis must not return."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "assets/g1/Database"
CASE_ID = "DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE"

class RetiredC1FixtureTests(unittest.TestCase):
    def test_no_private_c1_diagnosis_or_symptom_is_shipped(self):
        for name in ("ModDiagnoses.xml", "ModSymptoms.xml"):
            self.assertFalse((DB / name).exists())
        for name in ("ModStringTableEnABCL.xml", "ModStringTableZhHansABCL.xml"):
            text = (DB / name).read_text(encoding="utf-8")
            self.assertNotIn(CASE_ID, text)

    def test_installer_never_injects_disabled_fixture_or_dia_cld(self):
        script = (ROOT / "tools" / "Install-ABCL-G1.ps1").read_text(encoding="utf-8")
        for forbidden in ("Add-PrivateC1Fixture", CASE_ID, "DiagnosesER.xml", "'DIA_CLD'"):
            self.assertNotIn(forbidden, script)
        self.assertIn("if (!$NativeLeadTest)", script)
        self.assertIn("'TRM_LDP'", script)

    def test_runtime_has_no_super_gm_or_mobile_forced_factory(self):
        source = (ROOT / "src" / "ABCLG1Panel.cs").read_text(encoding="utf-8")
        for forbidden in ("ABCLSuperGmTestPanel", "ForceMobilePatient",
                          "CreateCharacterPatient(", "DIA_CLD", CASE_ID):
            self.assertNotIn(forbidden, source[source.index("private void OnGUI()"):])
        self.assertIn("SpawnNativeLead(lead, insurer)", source)

if __name__ == "__main__":
    unittest.main()
