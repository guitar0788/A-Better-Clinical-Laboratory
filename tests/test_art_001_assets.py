"""ART-001 source/XML contract tests. No native game runtime is simulated."""
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    from PIL import Image
    import cairosvg  # noqa: F401
    VECTOR_DEPS_AVAILABLE = True
except ImportError:
    Image = None
    VECTOR_DEPS_AVAILABLE = False

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools" / "generate_art_001_svg.py"
DATA = ROOT / "assets" / "art001" / "Database"


def load_generator():
    spec = importlib.util.spec_from_file_location("abcl_art001_svg", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Art001ContractTests(unittest.TestCase):
    def test_xml_assets_icons_palette_and_namespacing(self):
        assets = ET.parse(DATA / "ModAssetListsABCL.xml").getroot()
        objects = ET.parse(DATA / "ModObjectsABCL.xml").getroot()
        colors = ET.parse(DATA / "ModColorSets.xml").getroot()
        languages = [
            ET.parse(DATA / "ModStringTableEnABCLArt001.xml").getroot(),
            ET.parse(DATA / "ModStringTableZhHansABCLArt001.xml").getroot(),
        ]
        asset_map = {x.attrib["ID"]: x for x in assets}
        self.assertEqual(len(asset_map), 4)
        self.assertTrue(all(x.startswith("ASSET_") for x in asset_map))
        self.assertEqual(asset_map["ASSET_TEX_ABCL_ART001_EQUIPMENT"].findtext("Type"),
                         "TEXTURE_OBJECTS")
        self.assertEqual(asset_map["ASSET_TEX_ABCL_ART001_EQUIPMENT"].findtext("File"),
                         "MOD_ROOT/Assets/ABCL/equipment_atlas.png")
        icon_ids = {
            "ASSET_ABCL_ART001_ICON_ICPMS",
            "ASSET_ABCL_ART001_ICON_DIGESTION",
            "ASSET_ABCL_ART001_ICON_WORKBENCH",
        }
        self.assertTrue(icon_ids.issubset(asset_map))
        for icon_id in icon_ids:
            self.assertEqual(asset_map[icon_id].findtext("Type"),
                             "TEXTURE_CUSTOM_SPRITE")
            self.assertTrue(asset_map[icon_id].findtext("File").startswith(
                "MOD_ROOT/Assets/ABCL/"))

        self.assertEqual(len(objects), 3)
        workbench = objects.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_WORKBENCH']")
        self.assertIsNotNone(workbench)
        self.assertEqual(workbench.findtext("TextureRef"), "ASSET_TEX_OBJECTS_SMALL")
        self.assertEqual(workbench.findtext("TextureAtlasLayout"), "LAYOUT_16_X_64")
        self.assertEqual(workbench.findtext("AttachedToObject"), "false")
        self.assertEqual(workbench.findtext("Placement"), "INDOORS")
        self.assertEqual(workbench.findtext("AttachmentSlot/HeightOffset"), "0.9")
        self.assertEqual(workbench.findtext("AttachmentSlot/ForcesAttachmentOrientation"),
                         "false")
        self.assertEqual(
            {x.text for x in workbench.findall("AttachmentSlot/AllowedTags/Tag")},
            {"abcl_art001_icp_ms", "abcl_art001_digestion"},
        )
        self.assertEqual(workbench.findtext("CustomIconAssetRef"),
                         "ASSET_ABCL_ART001_ICON_WORKBENCH")
        self.assertIsNone(workbench.find("IconIndex"))
        self.assertEqual(workbench.findtext("ColorSetRef"),
                         "COLOR_SET_ABCL_ART001_WORKBENCH")

        device_objs = [obj for obj in objects if obj is not workbench]
        self.assertEqual(len(device_objs), 2)
        ids = set()
        for obj in objects:
            name = obj.attrib["ID"]
            self.assertTrue(name.startswith("OBJECT_ABCL_ART001_"))
            self.assertNotIn(name, ids)
            ids.add(name)
            self.assertIn(obj.findtext("CustomIconAssetRef"), asset_map)
            self.assertIsNone(obj.find("IconIndex"))

        allowed = {x.text for x in workbench.findall("AttachmentSlot/AllowedTags/Tag")}
        for obj in device_objs:
            self.assertEqual(obj.findtext("TextureRef"), "ASSET_TEX_ABCL_ART001_EQUIPMENT")
            self.assertEqual(obj.findtext("TextureAtlasLayout"), "LAYOUT_16_X_8")
            self.assertEqual(obj.findtext("SpriteShape"), "SHAPE_1_X_1")
            self.assertEqual(obj.findtext("AttachedToObject"), "true")
            self.assertNotEqual(obj.findtext("NotInteractable"), "true")
            self.assertTrue(obj.find("UseAnimationsStart") is not None)
            self.assertTrue(obj.find("UseAnimations") is not None)
            self.assertTrue(obj.find("UseAnimationsEnd") is not None)
            tags = {x.text for x in obj.findall("Tags/Tag")}
            self.assertIn("ui_equipment", tags)
            self.assertIn("ui_lab_equipment", tags)
            private_tags = {t for t in tags if t.startswith("abcl_art001_")}
            self.assertTrue(private_tags)
            self.assertTrue(private_tags & allowed)
            self.assertFalse(tags & {
                "hematoanalyzer", "stat_lab_exam", "RIA", "lab_eq_small",
                "lab_analyzer",
            })
            self.assertEqual(obj.findtext("ColorSetRef"), None)
            # Static machine sprites have no separate behind-character layer
            # or multi-state animation frames; vanilla HEM/RIA use the same
            # single-layer, static-object atlas convention.
            for direction in ("NW", "NE", "SE", "SW"):
                self.assertIsNone(obj.find("TextureIDBack" + direction))
                self.assertIsNone(obj.find("AnimationFrames" + direction))

        slots = [
            int(obj.findtext("TextureID" + direction))
            for obj in device_objs
            for direction in ("NW", "NE", "SE", "SW")
        ]
        self.assertEqual(slots, list(range(8)))
        workbench_slots = [
            int(workbench.findtext("TextureID" + direction))
            for direction in ("NW", "NE", "SE", "SW")
        ]
        self.assertEqual(workbench_slots, [472, 473, 474, 475])

        color_sets = colors.findall("GameDBColorSet")
        self.assertEqual([x.get("ID") for x in color_sets],
                         ["COLOR_SET_ABCL_ART001_WORKBENCH"])
        palette = color_sets[0].findall("./Colors/GameDBColor")
        self.assertEqual(len(palette), 5)
        for color in palette:
            for channel in ("R", "G", "B"):
                value = int(color.findtext(channel))
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, 255)

        for lang in languages:
            loc = {
                x.findtext("LocID")
                for x in lang.findall(".//GameDBLocalizedString")
            }
            for obj in objects:
                self.assertIn(obj.attrib["ID"], loc)
                self.assertIn(obj.findtext("AbbreviationLocID"), loc)

    def test_attachment_parent_is_private_and_is_not_a_vanilla_patch(self):
        objects = ET.parse(DATA / "ModObjectsABCL.xml").getroot()
        ids = {x.get("ID") for x in objects}
        self.assertEqual(ids, {
            "OBJECT_ABCL_ART001_WORKBENCH",
            "OBJECT_ABCL_ART001_ICP_MS",
            "OBJECT_ABCL_ART001_DIGESTION",
        })
        parent = objects.find(
            "./GameDBObject[@ID='OBJECT_ABCL_ART001_WORKBENCH']")
        allowed = {
            x.text for x in parent.findall("AttachmentSlot/AllowedTags/Tag")
        }
        self.assertEqual(allowed, {
            "abcl_art001_icp_ms", "abcl_art001_digestion"
        })
        for vanilla in (
            "OBJECT_TABLE_EQUIPMENT", "OBJECT_TABLE_SQUERE",
            "OBJECT_HEMATOLOGY_ANALYZER", "OBJECT_RIA",
        ):
            self.assertNotIn(vanilla, ids)
        self.assertEqual(
            parent.findtext("AttachmentSlot/ForcesAttachmentOrientation"),
            "false",
        )
        self.assertIsNone(parent.find("RequiredObjectsInRoom"))

    @unittest.skipUnless(VECTOR_DEPS_AVAILABLE,
                         "CairoSVG/Pillow are installed by the cloud art-preview workflow")
    def test_svg_atlas_native_bounds_and_custom_icon_safe_area(self):
        generator = load_generator()
        with tempfile.TemporaryDirectory() as temp:
            info = generator.generate(temp)
            root = Path(temp)
            atlas_path = root / "Assets" / "ABCL" / "equipment_atlas.png"
            with Image.open(atlas_path) as atlas:
                self.assertEqual(atlas.size, (2048, 1024))
                self.assertEqual(atlas.mode, "RGBA")
                self.assertEqual(hashlib.sha256(atlas_path.read_bytes()).hexdigest(),
                                 info["sha256"]["equipment_atlas.png"])
                for index in range(8):
                    tile = atlas.crop((index * 128, 0, (index + 1) * 128, 128))
                    bbox = tile.getchannel("A").getbbox()
                    self.assertIsNotNone(bbox)
                    self.assertGreaterEqual(bbox[3], 126,
                                            ("contact baseline", index, bbox))
                    if index < 4:
                        self.assertGreaterEqual(bbox[2] - bbox[0], 100)
                        self.assertLessEqual(bbox[2] - bbox[0], 120)
                        self.assertGreaterEqual(bbox[3] - bbox[1], 100)
                        self.assertLessEqual(bbox[3] - bbox[1], 112)
                    else:
                        self.assertGreaterEqual(bbox[2] - bbox[0], 90)
                        self.assertLessEqual(bbox[2] - bbox[0], 110)
                        self.assertGreaterEqual(bbox[3] - bbox[1], 78)
                        self.assertLessEqual(bbox[3] - bbox[1], 90)
                    alpha = tile.getchannel("A")
                    self.assertGreater(
                        sum(0 < value < 255 for value in alpha.getdata()), 100
                    )
            self.assertEqual(info["atlas_layout"], "LAYOUT_16_X_8")
            self.assertEqual(info["shared_baseline_y_px"], 127)
            self.assertEqual(info["schema"], "ABCL-ART-001-v7-native-bounds-review-only")
            self.assertEqual(len(list((root / "Sources" / "ABCL").glob("*.svg"))), 9)

            for icon_name in (
                "icp_ms_icon.png", "digestion_station_icon.png",
                "workbench_icon.png",
            ):
                icon_path = root / "Assets" / "ABCL" / icon_name
                with Image.open(icon_path) as icon:
                    self.assertEqual(icon.size, (64, 64))
                    self.assertEqual(icon.mode, "RGBA")
                    bbox = icon.getchannel("A").getbbox()
                    self.assertIsNotNone(bbox)
                    self.assertGreaterEqual(bbox[0], 2)
                    self.assertGreaterEqual(bbox[1], 2)
                    self.assertLessEqual(bbox[2], 62)
                    self.assertLessEqual(bbox[3], 62)
                self.assertEqual(
                    hashlib.sha256(icon_path.read_bytes()).hexdigest(),
                    info["sha256"][icon_name],
                )
            self.assertEqual(
                Image.open(root / "Previews" / "ABCL" /
                           "direction_preview.png").size, (1024, 256)
            )
            self.assertEqual(
                Image.open(root / "Previews" / "ABCL" /
                           "review_mobile.png").size, (1024, 560)
            )

    @unittest.skipUnless(VECTOR_DEPS_AVAILABLE,
                         "CairoSVG/Pillow are installed by the cloud art-preview workflow")
    def test_offline_stager_uses_active_svg_source_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "Art001Proof"
            subprocess.run(
                [sys.executable, str(ROOT / "tools" / "stage_art_001.py"),
                 "--output", str(target)],
                check=True, capture_output=True, text=True,
            )
            self.assertTrue((target / "NOT_FOR_GAME_INSTALL.txt").is_file())
            self.assertTrue((target / "Database" / "ModAddon.xml").is_file())
            self.assertTrue((target / "Database" / "ModColorSets.xml").is_file())
            self.assertTrue((target / "Assets" / "ABCL" /
                             "equipment_atlas.png").is_file())
            self.assertTrue((target / "Assets" / "ABCL" /
                             "workbench_icon.png").is_file())
            self.assertTrue((target / "Previews" / "ABCL" /
                             "direction_preview.png").is_file())
            self.assertEqual(len(list((target / "Database").glob("*.xml"))), 6)
            attempt = subprocess.run(
                [sys.executable, str(ROOT / "tools" / "stage_art_001.py"),
                 "--output", str(target)],
                capture_output=True, text=True,
            )
            self.assertNotEqual(attempt.returncode, 0)
            self.assertIn("Refusing to overwrite", attempt.stderr)

    @unittest.skipUnless(VECTOR_DEPS_AVAILABLE,
                         "CairoSVG/Pillow are installed by the cloud art-preview workflow")
    def test_placement_package_builder_is_allowlisted_and_not_published(self):
        spec = importlib.util.spec_from_file_location(
            "abcl_art_package",
            ROOT / "tools" / "build_art001_placement_test.py",
        )
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
            self.assertEqual(info["file_count"], 14)
            self.assertTrue(out.is_file())
            import zipfile
            with zipfile.ZipFile(out) as archive:
                names = archive.namelist()
                self.assertEqual(len(names), 14)
                self.assertTrue(all(
                    x.startswith("ModABCLArt001Test/") or
                    x in package.ALLOWED_TOOLS or
                    x == "BUILD_INFO.txt" for x in names
                ))
                self.assertTrue(any(x.endswith("/ModColorSets.xml") for x in names))
                self.assertTrue(any(x.endswith("/workbench_icon.png") for x in names))
                self.assertIn("INSTALL_ART001.cmd", names)
                self.assertNotIn("NOT_FOR_GAME_INSTALL.txt", names)
                self.assertFalse(any(
                    "0Harmony" in x or ".dll" in x.lower() for x in names
                ))
                self.assertIn("SOURCE_SHA=" + "f" * 40,
                              archive.read("BUILD_INFO.txt").decode("utf-8"))
            with self.assertRaises(FileExistsError):
                package.build(proof, out, "f" * 40)

    def test_player_visible_names_are_unbranded(self):
        for file_name in (
            "ModStringTableEnABCLArt001.xml",
            "ModStringTableZhHansABCLArt001.xml",
        ):
            root = ET.parse(DATA / file_name).getroot()
            for node in root.findall(".//GameDBLocalizedString/Text"):
                self.assertNotIn("ABCL", node.text or "")
                self.assertNotIn("原创", node.text or "")
        en = ET.parse(DATA / "ModStringTableEnABCLArt001.xml").getroot()
        labels = {
            node.findtext("LocID"): node.findtext("Text")
            for node in en.findall(".//GameDBLocalizedString")
        }
        self.assertEqual(labels["OBJECT_ABCL_ART001_ICP_MS"], "Mass Spectrometer")
        self.assertEqual(labels["OBJECT_ABCL_ART001_WORKBENCH"], "Instrument Workbench")

    def test_staged_art_does_not_modify_g1(self):
        self.assertFalse((DATA / "ModExaminations.xml").exists())
        self.assertFalse((DATA / "ModDiagnoses.xml").exists())
        self.assertFalse((DATA / "ModDepartments.xml").exists())


if __name__ == "__main__":
    unittest.main()
