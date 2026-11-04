"""Regression contract: unsafe C1/Super-GM is retired from G1."""
from pathlib import Path
import hashlib
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
TRUSTED_PROJECT_GIT_BLOB = "71daed7c3aa9e62edf9eea207fd77b2041be52ed"

class GMContract(unittest.TestCase):
    def test_pinned_project_hash_not_modified(self):
        raw = (SRC / "ABCL.G1.Panel.csproj").read_bytes()
        blob = b"blob " + str(len(raw)).encode("ascii") + b"\x00" + raw
        self.assertEqual(hashlib.sha1(blob).hexdigest(), TRUSTED_PROJECT_GIT_BLOB)
        project = ET.fromstring(raw)
        include = {x.get("Include") for x in project.findall(".//Compile")}
        self.assertEqual(include, {"ABCLG1Panel.cs"})

    def test_no_super_gm_or_private_c1_runtime(self):
        text = (SRC / "ABCLG1Panel.cs").read_text(encoding="utf-8")
        for forbidden in ("ABCLSuperGmTestPanel", "中文超级GM", "[ABCL GM TEST ONLY]",
                          "ForceMobilePatient", "DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE",
                          "private string caseId", "superGm.Draw"):
            self.assertNotIn(forbidden, text)
        self.assertIn("SpawnNativeLead(lead, insurer)", text)
        self.assertIn("LopitalEntityFactory.CreateCharacterPatient(", text)

    def test_no_c1_or_generic_outpatient_diagnosis_in_installer_or_localization(self):
        installer = (ROOT / "tools" / "Install-ABCL-G1.ps1").read_text(encoding="utf-8")
        for forbidden in ("DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE", "Add-PrivateC1Fixture",
                          "DiagnosesER.xml", "'DIA_CLD'"):
            self.assertNotIn(forbidden, installer)
        for name in ("ModStringTableEnABCL.xml", "ModStringTableZhHansABCL.xml"):
            text = (ROOT / "assets/g1/Database" / name).read_text(encoding="utf-8")
            self.assertNotIn("DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE", text)

    def test_native_r3_panel_remains_one_attempt(self):
        source = (SRC / "ABCLG1Panel.cs").read_text(encoding="utf-8")
        self.assertIn("r3SpawnAttempted = true;", source)
        self.assertIn("PatientMobility.IMOBILE", source)
        self.assertIn("CheckNativeLeadPreflight", source)
        self.assertIn("REQUEST ONE NATIVE LEAD PATIENT", source)
        self.assertNotIn("ForceDiagnosis(", source)
        self.assertNotIn("m_immobileSpawnedToday =", source)

if __name__ == "__main__":
    unittest.main(verbosity=2)
