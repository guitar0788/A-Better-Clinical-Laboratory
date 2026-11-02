import tempfile
import unittest
from pathlib import Path
from tools.prepare_g1_native_lead_override import prepare, EXAM_ID

SAMPLE = """<Database><GameDBMedicalCondition ID="TRM_LDP">
<DepartmentRef>DPT_INTERNAL_MEDICINE_DEPARTMENT</DepartmentRef>
<Symptoms><GameDBSymptomRules><ProbabilityPercent>100</ProbabilityPercent>
<GameDBSymptomRef>SYM_LEAD_LEVELS_HIGH</GameDBSymptomRef></GameDBSymptomRules></Symptoms>
<Examinations><ExaminationRef>EXM_INTERVIEW</ExaminationRef></Examinations>
<Treatments><TreatmentRef>TRT_HOSPITALIZATION_HIGH_PRIORITY</TreatmentRef>
<TreatmentRef>TRT_CHELATION_THERAPY</TreatmentRef></Treatments>
</GameDBMedicalCondition></Database>"""


class NativeLeadOverrideTests(unittest.TestCase):
    def test_preserves_native_clinical_constraints(self):
        with tempfile.TemporaryDirectory() as d:
            src, dst = Path(d) / "source.xml", Path(d) / "out" / "candidate.xml"
            src.write_text(SAMPLE, encoding="utf8")
            dst.parent.mkdir(parents=True, exist_ok=True)
            result = prepare(src, dst)
            self.assertTrue(result["symptoms_unchanged"])
            self.assertTrue(result["treatments_unchanged"])
            self.assertTrue(result["all_other_native_fields_unchanged"])
            self.assertTrue(result["native_admission_unverified"])
            self.assertFalse(result["gameplay_l4_authorized"])
            self.assertEqual(dst.read_text(encoding="utf8").count(EXAM_ID), 1)
            self.assertEqual(src.read_text(encoding="utf8"), SAMPLE)

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            src, dst = Path(d) / "source.xml", Path(d) / "candidate.xml"
            src.write_text(SAMPLE, encoding="utf8")
            dst.write_text("existing", encoding="utf8")
            with self.assertRaises(FileExistsError):
                prepare(src, dst)
            self.assertEqual(dst.read_text(encoding="utf8"), "existing")

    def test_rejects_output_beside_original_source(self):
        with tempfile.TemporaryDirectory() as d:
            src, dst = Path(d) / "source.xml", Path(d) / "candidate.xml"
            src.write_text(SAMPLE, encoding="utf8")
            with self.assertRaises(ValueError):
                prepare(src, dst)
            self.assertFalse(dst.exists())

    def test_rejects_changed_severity(self):
        with tempfile.TemporaryDirectory() as d:
            src, dst = Path(d) / "source.xml", Path(d) / "out" / "candidate.xml"
            dst.parent.mkdir(parents=True, exist_ok=True)
            src.write_text(SAMPLE.replace("<ProbabilityPercent>100", "<ProbabilityPercent>80"), encoding="utf8")
            with self.assertRaises(ValueError):
                prepare(src, dst)
            self.assertFalse(dst.exists())


if __name__ == "__main__":
    unittest.main()
