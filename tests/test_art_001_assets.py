"""Source-only ART-001 smoke tests. No native game runtime is simulated."""
import importlib.util
import json
import subprocess
import sys
import struct
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools" / "generate_art_001.py"
DATA = ROOT / "assets" / "art001" / "Database"


def png_info(path):
    data = Path(path).read_bytes()
    assert data[:8] == bytes((137, 80, 78, 71, 13, 10, 26, 10))
    assert data[12:16] == b"IHDR"
    width, height = struct.unpack(">II", data[16:24])
    return width, height


class Art001ContractTests(unittest.TestCase):
    def test_xml_and_namespacing(self):
        assets = ET.parse(DATA / "ModAssetListsABCL.xml").getroot()
        objects = ET.parse(DATA / "ModObjectsABCL.xml").getroot()
        languages = [
            ET.parse(DATA / "ModStringTableEnABCLArt001.xml").getroot(),
            ET.parse(DATA / "ModStringTableZhHansABCLArt001.xml").getroot(),
        ]
        asset_ids = {x.attrib["ID"] for x in assets}
        self.assertEqual(len(asset_ids), 3)
        self.assertTrue(all(x.startswith("ASSET_") for x in asset_ids))
        self.assertEqual(len(objects), 2)
        ids = set()
        for obj in objects:
            name = obj.attrib["ID"]
            self.assertTrue(name.startswith("OBJECT_ABCL_ART001_"))
            self.assertNotIn(name, ids)
            ids.add(name)
            self.assertEqual(obj.findtext("TextureRef"), "ASSET_TEX_ABCL_ART001_EQUIPMENT")
            self.assertEqual(obj.findtext("TextureAtlasLayout"), "LAYOUT_16_X_8")
            self.assertEqual(obj.findtext("SpriteShape"), "SHAPE_1_X_1")
            self.assertEqual(obj.findtext("AttachedToObject"), "true")
            self.assertNotEqual(obj.findtext("NotInteractable"), "true")
            self.assertIn(obj.findtext("CustomIconAssetRef"), asset_ids)
            self.assertTrue(obj.find("UseAnimations") is not None)
            tags = {x.text for x in obj.findall("Tags/Tag")}
            self.assertIn("ui_equipment", tags)
            self.assertIn("ui_lab_equipment", tags)
            self.assertTrue(any(t.startswith("abcl_art001_") for t in tags))
            self.assertNotIn("hematoanalyzer", tags)
            self.assertNotIn("stat_lab_exam", tags)
        slots = [int(obj.findtext("TextureID" + direction))
                 for obj in objects for direction in ("NW", "NE", "SE", "SW")]
        self.assertEqual(slots, list(range(8)))
        for lang in languages:
            loc = {x.findtext("LocID") for x in lang.findall(".//GameDBLocalizedString")}
            for obj in objects:
                self.assertIn(obj.attrib["ID"], loc)
                self.assertIn(obj.findtext("AbbreviationLocID"), loc)

    def test_procedural_atlas_is_valid_and_all_dirs_distinct(self):
        spec = importlib.util.spec_from_file_location("abcl_art001", GENERATOR)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temp:
            info = module.generate(temp)
            root = Path(temp)
            atlas = root / "Assets" / "ABCL" / "equipment_atlas.png"
            self.assertEqual(png_info(atlas), (2048, 1024))
            self.assertEqual(png_info(root / "Previews" / "ABCL" /
                                      "direction_preview.png"), (1024, 256))
            for name in ("icp_ms_icon.png", "digestion_station_icon.png"):
                self.assertEqual(png_info(root / "Assets" / "ABCL" / name), (64, 64))
            self.assertEqual(info["atlas_layout"], "LAYOUT_16_X_8")
            self.assertEqual(info["shared_pivot_px"], [64, 112])
            self.assertEqual(len(info["sha256"]), 4)
            self.assertEqual(json.loads((root / "art_manifest.json").read_text())
                             ["sha256"], info["sha256"])
            fingerprints = set()
            for device in module.DEVICES:
                for direction in module.DIRECTIONS:
                    result = module.sprite(device, direction)
                    self.assertEqual(len(result), 128 * 128 * 4)
                    self.assertTrue(any(result[i + 3] == 255
                                        for i in range(0, len(result), 4)))
                    fingerprints.add(result)
            self.assertEqual(len(fingerprints), 8)

    def test_offline_stager_is_isolated_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "Art001Proof"
            subprocess.run(
                [sys.executable, str(ROOT / "tools" / "stage_art_001.py"),
                 "--output", str(target)],
                check=True, capture_output=True, text=True,
            )
            self.assertTrue((target / "NOT_FOR_GAME_INSTALL.txt").is_file())
            self.assertTrue((target / "Database" / "ModAddon.xml").is_file())
            self.assertTrue((target / "Assets" / "ABCL" / "equipment_atlas.png").is_file())
            self.assertTrue((target / "Previews" / "ABCL" / "direction_preview.png").is_file())
            self.assertEqual(
                len(list((target / "Database").glob("*.xml"))), 5)
            attempt = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "stage_art_001.py"),
                 "--output", str(target)],
                capture_output=True, text=True,
            )
            self.assertNotEqual(attempt.returncode, 0)
            self.assertIn("Refusing to overwrite", attempt.stderr)

    def test_placement_package_contains_only_allowlisted_original_files(self):
        spec = importlib.util.spec_from_file_location(
            "abcl_art_package", ROOT / "tools" / "build_art001_placement_test.py")
        package = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(package)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            proof = root / "Art001Proof"
            subprocess.run(
                [sys.executable, str(ROOT / "tools" / "stage_art_001.py"),
                 "--output", str(proof)],
                check=True, capture_output=True, text=True,
            )
            out = root / "ABCL-ART001-Placement-TestOnly.zip"
            info = package.build(proof, out, "f" * 40)
            self.assertEqual(info["file_count"], 12)
            self.assertTrue(out.is_file())
            import zipfile
            with zipfile.ZipFile(out) as z:
                names = z.namelist()
                self.assertEqual(len(names), 12)
                self.assertTrue(all(x.startswith("ModABCLArt001Test/") or
                                    x in package.ALLOWED_TOOLS or
                                    x == "BUILD_INFO.txt" for x in names))
                self.assertIn("INSTALL_ART001.cmd", names)
                self.assertNotIn("NOT_FOR_GAME_INSTALL.txt", names)
                self.assertFalse(any("0Harmony" in x or ".dll" in x.lower()
                                     for x in names))
                self.assertIn("SOURCE_SHA=" + "f" * 40,
                              z.read("BUILD_INFO.txt").decode("utf-8"))
            with self.assertRaises(FileExistsError):
                package.build(proof, out, "f" * 40)

    def test_staged_art_does_not_modify_g1(self):
        self.assertFalse((DATA / "ModExaminations.xml").exists())
        self.assertFalse((DATA / "ModDiagnoses.xml").exists())
        self.assertFalse((DATA / "ModDepartments.xml").exists())


if __name__ == "__main__":
    unittest.main()
