"""Static native-route contract; runtime/L3 validation still required."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANEL = (ROOT / "src" / "ABCLG1Panel.cs")


class NativeImmobilePanelContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel = PANEL.read_text(encoding="utf-8")

    def test_r3_only_for_linked_original_condition(self):
        self.assertIn('HasAbclSampling(Database.Instance.GetEntry<GameDBMedicalCondition>("TRM_LDP"))', self.panel)
        self.assertIn("if (IsNativeLeadMode())", self.panel)
        self.assertIn("SpawnNativeLead(lead, insurer)", self.panel)

    def test_native_admission_guards(self):
        for clause in (
            "department.AcceptsOutpatients()",
            "department.AcceptsInpatients()",
            "DiagnosisRandomizerImmobile.Count > 0",
            "Hospital.Instance.HasAnyInpatientDepartment()",
            "m_immobileSpawnedToday > 0",
            "GetFreeAmbulance(false, false)",
            "insurer != null && freeAmbulance",
        ):
            self.assertIn(clause, self.panel)

    def test_original_factory_and_one_attempt(self):
        self.assertIn("r3SpawnAttempted = true;", self.panel)
        self.assertIn("PatientMobility.IMOBILE", self.panel)
        self.assertIn("LopitalEntityFactory.CreateCharacterPatient(", self.panel)
        self.assertIn("floor.AddCharacter(patient);", self.panel)
        self.assertIn("arrival not confirmed", self.panel)
        self.assertNotIn("GetRandomImmobileCompany()", self.panel)

    def test_preserve_r2_outpatient_path(self):
        for clause in (
            'Database.Instance.GetEntry<GameDBMedicalCondition>("DIA_CLD")',
            "PatientMobility.MOBILE",
            "ChooseEligibleOutpatientInsurer()",
            "SpawnOne();",
            "ABCL G1 R2",
        ):
            self.assertIn(clause, self.panel)


if __name__ == "__main__":
    unittest.main()
