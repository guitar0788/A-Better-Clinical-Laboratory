"""Source-only regression checks for frozen owner-approved TO004 G1 overlay.
The live TO source and installer are separately verified by GitHub CI.
"""
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (ROOT/"tools/build_to004_v3_g1_overlay.py").read_text("utf-8")
GUIDE = (ROOT/"docs/TO004_V3_G1_FOCUSED_L4.md").read_text("utf-8")

class TO004FrozenV3G1(unittest.TestCase):
    def test_frozen_source_and_binary_hashes(self):
        for value in (
            "9130c7a3241315d1b73e8bcfdf4cc2f560cd9804",
            "a0ec4ea41b5d96d4b755c5d244700548a6a2485d6a1d3e1bef73d8dcf09a0847",
            "3461bf9bbb8476d79e869d98f718b887a32ea88f5b0b158f185abc9f6cf85947",
            "1477eb5580e1002c33384f84aaa708dfbe2fb19b09ea01dcd330309295d61457",
            "4454abe727234fd8f8e6a70bcfff2f58860f05dbf3f8351b99951d7725bbad8d",
        ):
            self.assertIn(value, SCRIPT)
            self.assertIn(value, GUIDE)

    def test_resource_only_with_strict_native_menu_registration(self):
        for value in (
            "TEXTURE_CUSTOM_PREFAB_SPRITE","PREFAB",
            "ui_prefab_lab", "GameDBPrefabObject",
            "LayerFloors","LayerWalls","LayerDoors","LayerObjects",
            "GetHash",  # expected not present; see below
        )[:-1]:
            self.assertIn(value, SCRIPT)
        self.assertIn("git", SCRIPT)
        self.assertIn("rev-parse", SCRIPT)
        self.assertIn("source_sha", SCRIPT)
        self.assertIn("ModABCLG1LeadTest/", SCRIPT)
        self.assertNotIn("0Harmony.dll", SCRIPT)
        self.assertNotIn("Harmony.Patch", SCRIPT)
        self.assertNotIn("Recolor", SCRIPT)
        self.assertNotIn("Canvas", SCRIPT)

    def test_focused_l4_without_retesting_accepted_patient_workflow(self):
        for value in (
            "disposable", "rotation", "save", "reload", "CBC", "Workshop",
            "visual", "104×104", "C# binary"
        ):
            self.assertIn(value.lower(), GUIDE.lower())
        self.assertIn("Draft", GUIDE)
        self.assertIn("NOT RUN", GUIDE)
        self.assertNotIn("Download full game DLL", GUIDE)

if __name__ == "__main__":
    unittest.main()
