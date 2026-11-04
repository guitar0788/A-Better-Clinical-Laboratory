"""Static safety contract for the only supported native R3 installer mode."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "tools" / "Install-ABCL-G1.ps1"

class R3InstallerSafetyTests(unittest.TestCase):
    def test_r3_is_mandatory_and_generic_outpatient_override_is_rejected(self):
        script = INSTALLER.read_text(encoding="utf-8")
        self.assertIn("[switch]$NativeLeadTest", script)
        self.assertIn("if (!$NativeLeadTest)", script)
        self.assertIn("Make-Override", script)
        self.assertIn("'TRM_LDP'", script)
        self.assertNotIn("Diagnoses\\DiagnosesER.xml", script)
        self.assertNotIn("'DIA_CLD'", script)
        self.assertNotIn("Add-PrivateC1Fixture", script)
        self.assertNotIn("DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE", script)
        self.assertIn("R3 native TRM_LDP test mode installed", script)

    def test_both_launchers_select_the_safe_r3_mode(self):
        for name in ("INSTALL_G1.cmd", "INSTALL_G1_R3.cmd"):
            text = (ROOT / "tools" / name).read_text(encoding="utf-8")
            self.assertIn("-NativeLeadTest", text)

    def test_workflow_packages_only_r3_launcher(self):
        workflow = (ROOT / ".github" / "workflows" / "build-g1-candidate.yml").read_text(encoding="utf-8")
        readme = (ROOT / "tools" / "G1_TEST_README.txt").read_text(encoding="utf-8")
        self.assertIn("tools/INSTALL_G1_R3.cmd", workflow)
        self.assertIn("feature/g1-secure-build", workflow)
        self.assertIn("github.actor == 'guitar0788'", workflow)
        self.assertIn("INSTALL_G1_R3.cmd", readme)
        self.assertIn("BUILD_INFO.txt", readme)
        self.assertNotIn("C1 PRIVATE MOBILE GM FIXTURE", readme)
        self.assertNotIn("R2 HISTORY", readme)

    def test_preserves_native_severity_and_treatments(self):
        script = INSTALLER.read_text(encoding="utf-8")
        for clause in ("SYM_LEAD_LEVELS_HIGH", "ProbabilityPercent='100'",
                       "TRT_HOSPITALIZATION_HIGH_PRIORITY", "TRT_CHELATION_THERAPY",
                       "DPT_INTERNAL_MEDICINE_DEPARTMENT",
                       "Existing G1 folder detected; refusal to overwrite"):
            self.assertIn(clause, script)

if __name__ == "__main__":
    unittest.main()
