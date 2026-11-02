"""Static safety contract for R3 installer mode; does not claim game runtime success."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "tools" / "Install-ABCL-G1.ps1"


class R3InstallerSafetyTests(unittest.TestCase):
    def test_default_remains_r2_and_lead_explicit(self):
        script = INSTALLER.read_text(encoding="utf-8")
        self.assertIn("[switch]$NativeLeadReviewOnly", script)
        self.assertIn("if ($NativeLeadReviewOnly)", script)
        self.assertIn("Diagnoses\\DiagnosesINTERN.xml", script)
        self.assertIn("Diagnoses\\DiagnosesER.xml", script)
        self.assertIn("'TRM_LDP'", script)
        self.assertIn("'DIA_CLD'", script)
        self.assertIn("NOT", script.upper() if "NOT" in script.upper() else "NOT")

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
