"""G1 bilingual medical terminology and ID-preservation checks (source only)."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "assets" / "g1" / "Database"
FILES = {"en": DB / "ModStringTableEnABCL.xml",
         "zh-Hans": DB / "ModStringTableZhHansABCL.xml"}
ROOM = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB"
SAMPLE = "EXM_ABCL_G1_BLOOD_LEAD_SAMPLING"
ANALYSIS = "EXM_ABCL_G1_BLOOD_LEAD_TESTING"
IDS = {x for name in (ROOM, SAMPLE, ANALYSIS) for x in (name, name + "_DESCRIPTION")}

def get_texts(path, lang):
    table = ET.parse(path).getroot().find("GameDBStringTable")
    if table is None or table.findtext("LanguageCode") != lang:
        raise AssertionError("Unexpected language table")
    rows = table.findall("./LocalizedStrings/GameDBLocalizedString")
    keys = [x.findtext("LocID") for x in rows]
    if len(keys) != len(set(keys)):
        raise AssertionError("Duplicate LocID")
    return {x.findtext("LocID"): x.findtext("Text") for x in rows}

class G1MedicalLocalizationTests(unittest.TestCase):
    def test_parallel_nonbranded_localization_without_private_debug_case(self):
        for lang, path in FILES.items():
            strings = get_texts(path, lang)
            self.assertEqual(set(strings), IDS)
            for locid, value in strings.items():
                self.assertTrue(value and value.strip() == value)
                self.assertFalse(re.search(r"\\b(?:ABCL|G1|test|fixture|debug)\\b", value, re.I))
                self.assertNotIn("测试", value)
                self.assertNotIn("占位", value)
                if locid.endswith("_DESCRIPTION"):
                    self.assertGreaterEqual(len(value), 10)
                    self.assertLessEqual(len(value), 100)
                else:
                    self.assertGreaterEqual(len(value), 3)
                    self.assertLessEqual(len(value), 40)

    def test_medical_specificity_without_numeric_engine_claim(self):
        en = get_texts(FILES["en"], "en")
        zh = get_texts(FILES["zh-Hans"], "zh-Hans")
        self.assertIn("Toxicology", en[ROOM])
        self.assertIn("Blood", en[SAMPLE])
        self.assertIn("lead", en[ANALYSIS].lower())
        self.assertIn("毒理", zh[ROOM])
        self.assertIn("采集", zh[SAMPLE])
        self.assertIn("血铅", zh[ANALYSIS])
        for strings in (en, zh):
            self.assertFalse(any("µg/dL" in value or "μg/dL" in value for value in strings.values()))

    def test_display_locids_match_existing_room_and_exam_ids(self):
        room = ET.parse(DB / "ModRoomTypes.xml").getroot().find("GameDBRoomType")
        self.assertEqual(room.get("ID"), ROOM)
        self.assertEqual(room.findtext("AbbreviationLocID"), ROOM + "_DESCRIPTION")
        exams = ET.parse(DB / "ModExaminations.xml").getroot()
        self.assertEqual({x.get("ID") for x in exams.findall("GameDBExamination")}, {SAMPLE, ANALYSIS})
        for exam in exams.findall("GameDBExamination"):
            self.assertEqual(exam.findtext("AbbreviationLocID"), exam.get("ID") + "_DESCRIPTION")

if __name__ == "__main__":
    unittest.main()
