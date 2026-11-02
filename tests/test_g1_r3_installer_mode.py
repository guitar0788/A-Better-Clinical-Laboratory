"""Static safety contract for R3 installer mode; does not claim game runtime success."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "tools" / "Install-ABCL-G1.ps1"


class R3InstallerSafetyTests(unittest.TestCase):
    def test_default_remains_r2_and_lead_explicit(self):
        script = INSTALLER.read_text(encoding="utf-8")
        self.assertIn("[switch]$NativeLeadTest", script)
        self.assertIn("if ($NativeLeadTest)", script)
        self.assertIn("Diagnoses\\DiagnosesINTERN.xml", script)
        self.assertIn("Diagnoses\\DiagnosesER.xml", script)
        self.assertIn("'TRM_LDP'", script)
        self.assertIn("'DIA_CLD'", script)
        self.assertIn("R3 native TRM_LDP test mode installed", script)

    def test_r3_launcher_is_included_in_test_artifact(self):
        workflow = (ROOT / ".github" / "workflows" / "build-g1-candidate.yml").read_text(encoding="utf-8")
        readme = (ROOT / "tools" / "G1_TEST_README.txt").read_text(encoding="utf-8")
        launcher = ROOT / "tools" / "INSTALL_G1_R3.cmd"
        self.assertTrue(launcher.is_file())
        self.assertIn("tools/INSTALL_G1_R3.cmd", workflow)
        package_line = next(line for line in workflow.splitlines() if "Copy-Item $packageFiles" in line)
        self.assertIn("INSTALL_G1_R3.cmd", workflow)
        self.assertIn("feature/g1-secure-build", workflow)
        self.assertIn("github.actor == 'guitar0788'", workflow)
        self.assertNotIn("INSTALL_G1.cmd", package_line)
        self.assertIn("INSTALL_G1_R3.cmd", readme)
        self.assertIn("BUILD_INFO.txt", readme)
        self.assertNotIn("OFFLINE REVIEW ONLY", readme)

    def test_preserves_native_severity_and_treatments(self):
        script = INSTALLER.read_text(encoding="utf-8")
        self.assertIn("SYM_LEAD_LEVELS_HIGH", script)
        self.assertIn("ProbabilityPercent='100'", script)
        self.assertIn("TRT_HOSPITALIZATION_HIGH_PRIORITY", script)
        self.assertIn("TRT_CHELATION_THERAPY", script)
        self.assertIn("DPT_INTERNAL_MEDICINE_DEPARTMENT", script)
        self.assertIn("Existing G1 folder detected; refusal to overwrite", script)


if __name__ == "__main__":
    unittest.main()
