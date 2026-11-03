"""Source-only guards for the optional G2 cases in the G1 test-only GM panel.

No G2 disease is enabled for random generation, and this is not a C# compile
or in-game test. Actual native validation must use the exact-head net35 build.
"""
from pathlib import Path
import unittest

SOURCE = (Path(__file__).resolve().parents[1] / "src" / "ABCLG1Panel.cs")


class G2GMDispatchContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.method = cls.source[cls.source.index("private void ForceMobilePatient()"):]

    def test_exact_allowlist_and_sampling_ids(self):
        for token in (
            "DIA_ABCL_G2_CADMIUM_EXPOSURE",
            "DIA_ABCL_G2_MERCURY_EXPOSURE",
            "EXM_ABCL_G2_BLOOD_CADMIUM_SAMPLING",
            "EXM_ABCL_G2_URINE_MERCURY_SAMPLING",
            "SYM_ABCL_G2_CADMIUM_ELEVATED",
            "SYM_ABCL_G2_MERCURY_ELEVATED",
        ):
            self.assertIn('"' + token + '"', self.source)
        self.assertIn("id == G2CadmiumId || id == G2MercuryId", self.method)
        self.assertIn("!ValidDisabledG2Case(condition, id)", self.method)
        self.assertIn("condition.Disabled && id != PrivateFixtureId && !isG2",
                      self.method)

    def test_g2_validation_occurs_before_factory_and_blocks_bad_content(self):
        validate = self.source[self.source.index("private bool ValidDisabledG2Case("):
                               self.source.index("private void ForceMobilePatient()")]
        for guard in (
            "!condition.Disabled", "condition.Examinations == null",
            "condition.Symptoms == null", "if (!linked) return false",
            "symptom.PatientMobility == PatientMobility.IMOBILE",
            "symptom.PatientMobility == PatientMobility.INTUBATED",
            "symptom.PatientMobility == PatientMobility.HELICOPTER",
            "symptom.IsMainSymptom && rule.ProbabilityPercent == 100",
        ):
            self.assertIn(guard, validate)
        self.assertLess(self.method.index("!ValidDisabledG2Case(condition, id)"),
                        self.method.index("forceAttempts++"))
        self.assertLess(self.method.index("!ValidDisabledG2Case(condition, id)"),
                        self.method.index("LopitalEntityFactory.CreateCharacterPatient("))

    def test_original_database_id_is_not_compared_directly_to_str(self):
        # Original game source: DatabaseEntry.DatabaseID is ID, not string.
        # ID exposes ToString() but has no ID == string overload.
        src = self.source
        self.assertNotIn("symptom.DatabaseID == expectedMain", src)
        self.assertIn("symptom.DatabaseID != null &&", src)
        self.assertIn("symptom.DatabaseID.ToString() == expectedMain", src)
        self.assertIn("rule.GameDBSymptomRef.Entry", src)

    def test_existing_c1_and_r3_guards_preserved(self):
        for required in (
            'private const string PrivateFixtureId = "DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE";',
            "if (id == PrivateFixtureId)",
            "if (!condition.Disabled || !properlyLinked)",
            "if (condition.HasImmobileSymptom())",
            "Time.realtimeSinceStartup - lastClick < 1.5f",
            "factoryFailed = true;",
            "SpawnNativeLead(lead, insurer)",
        ):
            self.assertIn(required, self.source)
        self.assertNotIn("ForceDiagnosis(", self.source)
        self.assertNotIn("m_immobileSpawnedToday =", self.source)

    def test_case_specific_success_message_is_not_always_blood_lead(self):
        self.assertIn("id == G2CadmiumId ? G2CadmiumSampling", self.method)
        self.assertIn("id == G2MercuryId ? G2MercurySampling", self.method)
        self.assertIn("已关联病例专属采样", self.method)


if __name__ == "__main__":
    unittest.main()
