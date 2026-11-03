"""CLIN-001 private C1 developer fixture contracts (source/L2 only).

The game-owned diagnosis XML is never embedded in this repository or shipped.
These checks keep the fixture disabled from natural random generation and
confirm the assay is a privately named testing procedure. They do not
certify native gameplay, doctor diagnosis, or save compatibility.
"""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "tools" / "Install-ABCL-G1.ps1"
PANEL = ROOT / "src" / "ABCLG1Panel.cs"
DB = ROOT / "assets" / "g1" / "Database"
CASE_ID = "DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE"
ABCL_SAMPLING = "EXM_ABCL_G1_BLOOD_LEAD_SAMPLING"
ABCL_TESTING = "EXM_ABCL_G1_BLOOD_LEAD_TESTING"


def get_private_case():
    source = INSTALLER.read_text(encoding="utf-8")
    match = re.search(r"\$fragment\.InnerXml\s*=\s*@'\s*\n(.*?)\n'@", source, re.S)
    if not match:
        raise AssertionError("C1 native PowerShell fixture XML missing")
    return ET.fromstring(match.group(1))


class PrivateC1FixtureContract(unittest.TestCase):
    def test_has_private_nonvanilla_identity_and_is_disabled_in_native_pool(self):
        x = get_private_case()
        self.assertEqual(x.tag, "GameDBMedicalCondition")
        self.assertEqual(x.get("ID"), CASE_ID)
        self.assertEqual(x.findtext("AbbreviationLocID"), CASE_ID + "_DESCRIPTION")
        self.assertEqual(x.findtext("DepartmentRef"), "DPT_EMERGENCY")
        self.assertEqual(x.findtext("Disabled"), "true")
        self.assertEqual(x.findtext("OccurrenceRef"), "OCCURRENCE_UNCOMMON")
        self.assertEqual({t.text for t in x.findall("./Tags/Tag")}, {"clinic", "disease"})

    def test_mild_mobile_symptoms_no_original_lead_severe_or_immobile(self):
        x = get_private_case()
        symptoms = x.findall("./Symptoms/GameDBSymptomRules")
        self.assertEqual(len(symptoms), 4)
        self.assertEqual({s.findtext("GameDBSymptomRef") for s in symptoms},
                         {"SYM_ABDOMINAL_PAIN", "SYM_FATIGUE", "SYM_HEADACHE", "SYM_WEAKNESS"})
        for s in symptoms:
            self.assertEqual(s.findtext("DayOfFirstOccurence"), "0")
            self.assertTrue(50 <= int(s.findtext("ProbabilityPercent")) <= 100)
        self.assertNotIn("SYM_LEAD_LEVELS_HIGH", ET.tostring(x, encoding="unicode"))

    def test_private_assay_is_linked_and_no_vanilla_lab_testing_reassigned(self):
        x = get_private_case()
        ids = [e.text for e in x.findall("./Examinations/ExaminationRef")]
        self.assertEqual(ids.count(ABCL_SAMPLING), 1)
        self.assertIn("EXM_INTERVIEW", ids)
        self.assertIn("EXM_ABDOMINAL_PALPATION", ids)
        self.assertFalse(any(v in ids for v in ("EXM_CBC_TESTING", "EXM_CBC_SAMPLING",
                    "EXM_BLOOD_TEST_SAMPLING", "EXM_ABCL_G1_BLOOD_LEAD_TESTING")))
        all_exams = ET.parse(DB / "ModExaminations.xml").getroot()
        samplers = [p for p in all_exams if p.get("ID") == ABCL_SAMPLING]
        self.assertEqual(len(samplers), 1)
        self.assertEqual(samplers[0].findtext("LabTestingExaminationRef"), ABCL_TESTING)

    def test_native_symptom_treatments_are_consistent_and_reviewed(self):
        x = get_private_case()
        treatments = {e.text for e in x.findall("./Treatments/TreatmentRef")}
        self.assertEqual(treatments, {"TRT_REST", "TRT_ANALGESICS", "TRT_HOME_TREATMENT"})
        self.assertEqual(x.findtext("Duration"), "2")
        self.assertGreater(int(x.findtext("InsurancePayment")), 0)
        self.assertTrue(int(x.findtext("IconIndex")) > 0)

    def test_installer_adds_private_case_to_both_original_g1_modes_only_in_staging(self):
        s = INSTALLER.read_text(encoding="utf-8")
        self.assertIn("function Add-PrivateC1Fixture", s)
        self.assertIn("if ($NativeLeadTest)", s)
        self.assertIn("'TRM_LDP'", s)
        self.assertIn("'DIA_CLD'", s)
        self.assertIn("Existing G1 folder detected; refusal to overwrite", s)
        self.assertIn("Add-PrivateC1Fixture (Join-Path $outDb 'ModDiagnoses.xml')", s)
        self.assertLess(s.index("Add-PrivateC1Fixture (Join-Path $outDb 'ModDiagnoses.xml')"),
                        s.index("Move-Item -LiteralPath $stage -Destination $target"))
        self.assertIn("if ($root.SelectSingleNode(\"GameDBMedicalCondition[@ID='$privateId']\"))", s)
        self.assertNotIn("Set-Content -Path $db", s)

    def test_localization_is_fully_bilingual_and_test_labeled(self):
        for f, lang in (("ModStringTableEnABCL.xml", "en"),
                        ("ModStringTableZhHansABCL.xml", "zh-Hans")):
            root = ET.parse(DB / f).getroot()[0]
            self.assertEqual(root.findtext("LanguageCode"), lang)
            values = {n.findtext("LocID"): n.findtext("Text")
                      for n in root.findall("./LocalizedStrings/GameDBLocalizedString")}
            self.assertIn(CASE_ID, values)
            self.assertIn(CASE_ID+"_DESCRIPTION", values)
            self.assertGreater(len(values[CASE_ID].strip()), 5)
            self.assertIn("测试" if lang == "zh-Hans" else "test", values[CASE_ID].lower())

    def test_gm_defaults_to_private_condition_but_guards_real_native_factory(self):
        p = PANEL.read_text(encoding="utf-8")
        self.assertIn('private const string PrivateFixtureId = "'+CASE_ID+'";', p)
        self.assertIn("private string caseId = PrivateFixtureId;", p)
        self.assertIn("condition.Disabled && id != PrivateFixtureId", p)
        self.assertIn("id == PrivateFixtureId", p)
        start = p.index("private void ForceMobilePatient()")
        sub = p[start:]
        self.assertLess(sub.index("if (!condition.Disabled || !properlyLinked)"),
                        sub.index("LopitalEntityFactory.CreateCharacterPatient("))
        self.assertIn("nativePatient.m_state.m_medicalCondition.m_gameDBMedicalCondition.Entry != condition", sub)
        self.assertIn("condition.HasImmobileSymptom()", sub)
        self.assertNotIn("ForceDiagnosis(", sub)

    def test_installer_readme_clearly_explains_new_gm_default_and_no_fake_l4(self):
        readme = (ROOT / "tools" / "G1_TEST_README.txt").read_text(encoding="utf-8")
        self.assertIn("C1 PRIVATE MOBILE GM FIXTURE", readme)
        self.assertIn(CASE_ID, readme)
        self.assertIn("中文超级GM", readme)
        self.assertIn("INSTALL_G1_R3.cmd", readme)
        self.assertIn("No separate GM plugin", readme)
        self.assertIn("CREATION", readme)
        self.assertIn("actual ARRIVAL", readme)
        self.assertIn("Do not claim true C1", readme)
        self.assertIn("original CBC", readme)

    def test_no_new_production_medical_record_or_gm_plugin(self):
        self.assertFalse((DB / "ModDiagnoses.xml").exists())
        self.assertFalse((DB / "ModSymptoms.xml").exists())
        source=(ROOT / "src" / "ABCL.G1.Panel.csproj").read_text(encoding="utf-8")
        self.assertNotIn("BepInEx", source)
        self.assertNotIn("Harmony", source)
        self.assertIn("<TargetFramework>net35</TargetFramework>",source)


if __name__ == "__main__":
    unittest.main()
