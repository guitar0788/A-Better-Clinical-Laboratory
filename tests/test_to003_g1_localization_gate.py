"""TO-003: verify professional bilingual, self-contained G1 UI copy.

Source-only/L2 validation. Does not claim runtime localization, clinical behavior
or owner visual acceptance. Test-only spawn panels are deliberately out of scope.
"""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "assets" / "g1" / "Database"
ROOM = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB"
EXAMS = (
    "EXM_ABCL_G1_BLOOD_LEAD_SAMPLING",
    "EXM_ABCL_G1_BLOOD_LEAD_TESTING",
)
FIELDS = (ROOM,) + EXAMS


def localized(path):
    root = ET.parse(path).getroot()
    table = root.find("GameDBStringTable")
    assert table is not None
    return table.findtext("LanguageCode"), {
        entry.findtext("LocID"): entry.findtext("Text") or ""
        for entry in table.findall("./LocalizedStrings/GameDBLocalizedString")
    }


class TO003G1LocalizationGate(unittest.TestCase):
    def test_room_and_exams_have_complete_bilingual_copy(self):
        en_lang, en = localized(DB / "ModStringTableEnABCL.xml")
        zh_lang, zh = localized(DB / "ModStringTableZhHansABCL.xml")
        self.assertEqual(en_lang, "en")
        self.assertEqual(zh_lang, "zh-Hans")
        self.assertEqual(set(en), set(zh))
        self.assertEqual(set(en), {key for field in FIELDS for key in (field, field + "_DESCRIPTION")})
        for dictionary in (en, zh):
            for field in FIELDS:
                title, detail = dictionary[field].strip(), dictionary[field + "_DESCRIPTION"].strip()
                self.assertTrue(title and detail, field)
                self.assertNotEqual(title.casefold(), detail.casefold())
                self.assertLessEqual(len(title), 48, field + " title exceeds review budget")
                self.assertLessEqual(len(detail), 110, field + " description exceeds review budget")
                for value in (title, detail):
                    self.assertFalse(re.search(r"\b(?:placeholder|todo|tbd|testonly|g1|abcl)\b", value, re.I))
                    self.assertNotIn("XXX", value.upper())

    def test_g1_copy_matches_actual_workflow_not_unimplemented_methods(self):
        _, en = localized(DB / "ModStringTableEnABCL.xml")
        _, zh = localized(DB / "ModStringTableZhHansABCL.xml")
        self.assertEqual(en[ROOM], "Toxicology Laboratory")
        self.assertEqual(zh[ROOM], "临床毒理实验室")
        self.assertIn("whole-blood", en[EXAMS[1] + "_DESCRIPTION"])
        self.assertIn("血铅", zh[EXAMS[1]])
        for strings in (en, zh):
            # No unimplemented numeric results or named assay technology promised.
            for value in strings.values():
                self.assertFalse(re.search(r"ICP[- ]?MS|mass spectrom|质谱|实时数值", value, re.I))

    def test_localization_ids_match_real_room_and_exam_entries(self):
        room = ET.parse(DB / "ModRoomTypes.xml").getroot().find("GameDBRoomType")
        self.assertEqual(room.get("ID"), ROOM)
        self.assertEqual(room.findtext("AbbreviationLocID"), ROOM + "_DESCRIPTION")
        exams = ET.parse(DB / "ModExaminations.xml").getroot()
        self.assertEqual({e.get("ID") for e in exams.findall("GameDBExamination")}, set(EXAMS))
        for exam in exams.findall("GameDBExamination"):
            self.assertEqual(exam.findtext("AbbreviationLocID"), exam.get("ID") + "_DESCRIPTION")


if __name__ == "__main__":
    unittest.main()
