"""G1 bilingual player-facing medical terminology and ID-preservation checks.

Source-level only: this is not a medical gameplay or translation L4 test.
The internal ABCL namespace stays private; room, procedure and description
display text stays neutral, concise and professionally meaningful.
"""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "assets" / "g1" / "Database"
FILES = {
    "en": DB / "ModStringTableEnABCL.xml",
    "zh-Hans": DB / "ModStringTableZhHansABCL.xml",
}
ROOM = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB"
SAMPLE = "EXM_ABCL_G1_BLOOD_LEAD_SAMPLING"
ANALYSIS = "EXM_ABCL_G1_BLOOD_LEAD_TESTING"
IDS = {entry for name in (ROOM, SAMPLE, ANALYSIS) for entry in (name, name + "_DESCRIPTION")}


def get_texts(path, lang):
    tree = ET.parse(path).getroot()
    table = tree.find("GameDBStringTable")
    if table is None or table.findtext("LanguageCode") != lang:
        raise AssertionError("Unexpected or missing GameDBStringTable language")
    rows = table.findall("./LocalizedStrings/GameDBLocalizedString")
    keys = [row.findtext("LocID") for row in rows]
    if len(keys) != len(set(keys)):
        raise AssertionError("Duplicate LocID in " + str(path))
    return {row.findtext("LocID"): row.findtext("Text") for row in rows}


class G1MedicalLocalizationTests(unittest.TestCase):
    def test_complete_parallel_nonbranded_localization(self):
        for lang, path in FILES.items():
            with self.subTest(language=lang):
                strings = get_texts(path, lang)
                self.assertEqual(set(strings), IDS)
                for locid, content in strings.items():
                    self.assertTrue(locid.startswith(("ROOM_TYPE_ABCL_", "EXM_ABCL_")))
                    self.assertIsInstance(content, str)
                    self.assertEqual(content.strip(), content)
                    self.assertFalse(re.search(r"\b(?:ABCL|G1|test|fixture|debug)\b", content, re.I))
                    self.assertNotIn("测试", content)
                    self.assertNotIn("占位", content)
                    self.assertNotIn("一次性", content)
                    if locid.endswith("_DESCRIPTION"):
                        self.assertGreaterEqual(len(content), 10)
                        self.assertLessEqual(len(content), 100)
                    else:
                        self.assertGreaterEqual(len(content), 3)
                        self.assertLessEqual(len(content), 40)

    def test_medical_specificity_without_claiming_numeric_engine(self):
        en = get_texts(FILES["en"], "en")
        zh = get_texts(FILES["zh-Hans"], "zh-Hans")
        self.assertIn("Toxicology", en[ROOM])
        self.assertIn("Blood", en[SAMPLE])
        self.assertIn("lead", en[ANALYSIS].lower())
        self.assertIn("毒理", zh[ROOM])
        self.assertIn("采集", zh[SAMPLE])
        self.assertIn("血铅", zh[ANALYSIS])
        # Current clinical engine returns examination outcomes, not a numeric BLL.
        for strings in (en, zh):
            self.assertFalse(any("µg/dL" in text for text in strings.values()))
            self.assertFalse(any("μg/dL" in text for text in strings.values()))

    def test_display_locids_match_existing_room_and_exam_ids(self):
        room = ET.parse(DB / "ModRoomTypes.xml").getroot().find("GameDBRoomType")
        self.assertEqual(room.attrib.get("ID"), ROOM)
        self.assertEqual(room.findtext("AbbreviationLocID"), ROOM + "_DESCRIPTION")
        exams = ET.parse(DB / "ModExaminations.xml").getroot()
        self.assertEqual({exam.attrib.get("ID") for exam in exams.findall("GameDBExamination")}, {SAMPLE, ANALYSIS})
        for exam in exams.findall("GameDBExamination"):
            self.assertEqual(exam.findtext("AbbreviationLocID"), exam.attrib["ID"] + "_DESCRIPTION")


if __name__ == "__main__":
    unittest.main()
