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

    def test_liver_ty_icu_and_ambulance_progression_is_visible(self):
        for clause in (
            'Entry.NameLocID != "IN_COM_CCC"',
            'Database.Instance.GetEntry<GameDBDepartment>("DPT_ICU")',
            "icu.AcceptsInpatients()",
            "IsInsuranceObjectivePassed(liverTy, 3)",
            "IsInsuranceObjectivePassed(liverTy, 4)",
            "m_ambulancesUnlocked",
            "m_currentImmobilePatients",
            "m_immobileSpawnedToday",
            "Liver TY (肝泰保险) contracted:",
            "Liver TY ICU hospitalization objective (#4):",
            "Liver TY one-ambulance objective (#5):",
        ):
            self.assertIn(clause, self.panel)

    def test_native_insurer_selection_is_not_hardcoded_to_liver_ty(self):
        start = self.panel.index("private InsuranceCompany ChooseEligibleImmobileInsurer()")
        end = self.panel.index("private InsuranceCompany FindLiverTyInsurance()", start)
        selection = self.panel[start:end]
        self.assertNotIn("IN_COM_CCC", selection)
        self.assertIn("company.m_immobileSpawnedToday > 0", selection)

    def test_preflight_diagnostics_are_read_only(self):
        start = self.panel.index("private bool CheckNativeLeadPreflight(")
        end = self.panel.index("private void SpawnNativeLead(", start)
        preflight = self.panel[start:end]
        for forbidden in (
            "CalculatePatientCounts(",
            "ProcessReward(",
            "m_currentImmobilePatients =",
            "m_immobileSpawnedToday =",
            "ContractInsuranceCompany(",
        ):
            self.assertNotIn(forbidden, preflight)

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
