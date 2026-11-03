"""Pure synthetic source gates for two self-standing ABCL-only equipment types."""
import importlib.util
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

SCRIPT = Path(__file__).resolve().parents[1] / "tools/stage_art001_selfstanding_candidate.py"
spec = importlib.util.spec_from_file_location("art001_selfstanding", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def put(parent, name, value):
    ET.SubElement(parent, name).text = str(value)


def synth():
    objects = ET.Element("Database")
    bench = ET.SubElement(objects, "GameDBObject", ID=module.WORKBENCH)
    put(bench, "AttachedToObject", "false")
    slot = ET.SubElement(bench, "AttachmentSlot")
    allowed = ET.SubElement(slot, "AllowedTags")
    for tag, _, _ in module.DEVICES.values():
        put(allowed, "Tag", tag)

    for key, (tag, slots, icon) in module.DEVICES.items():
        obj = ET.SubElement(objects, "GameDBObject", ID=key)
        for k, v in [
            ("AttachedToObject", "true"), ("TextureRef", "ASSET_TEX_ABCL_ART001_EQUIPMENT"),
            ("TextureAtlasLayout", "LAYOUT_16_X_8"), ("SpriteShape", "SHAPE_1_X_1"),
            ("CustomIconAssetRef", icon), ("PlacedToEdge", "false"),
            ("AttachedToWall", "false"), ("UseOffsetXNW", "-0.7")
        ]:
            put(obj, k, v)
        for direction, num in zip(module.DIRECTIONS, slots):
            put(obj, "TextureID" + direction, num)
        tags = ET.SubElement(obj, "Tags")
        put(tags, "Tag", "ui_equipment")
        put(tags, "Tag", "ui_lab_equipment")
        put(tags, "Tag", tag)
        for x in ("", "Start", "End"):
            put(ET.SubElement(obj, "UseAnimations" + x), "Animation", "use_equipment_low")

    assets = ET.Element("Database")
    for key in module.ASSETS:
        row = ET.SubElement(assets, "GameDBAsset", ID=key)
        if key == "ASSET_TEX_ABCL_ART001_EQUIPMENT":
            put(row, "Type", "TEXTURE_OBJECTS")
            put(row, "File", "MOD_ROOT/Assets/ABCL/equipment_atlas.png")
        else:
            put(row, "Type", "TEXTURE_CUSTOM_SPRITE")
            put(row, "File", "MOD_ROOT/Assets/ABCL/" + key + ".png")

    locales = {}
    for lang in ("en", "zh-Hans"):
        root = ET.Element("Database")
        table = ET.SubElement(root, "GameDBStringTable", ID="L_" + lang)
        put(table, "LanguageCode", lang)
        strs = ET.SubElement(table, "LocalizedStrings")
        for key in [module.WORKBENCH, *module.DEVICES]:
            for suffix in ("", "_DESCRIPTION"):
                row = ET.SubElement(strs, "GameDBLocalizedString")
                put(row, "LocID", key + suffix)
                put(row, "Text", key + suffix)
        locales[lang] = root
    def data(x): return ET.tostring(x, encoding="utf-8")
    return objects, assets, locales, data


class IndependentDevices(unittest.TestCase):
    def setUp(self):
        self.o, self.a, self.l, self.data = synth()

    def call(self):
        return module.transform(
            self.data(self.o), self.data(self.a),
            self.data(self.l["en"]), self.data(self.l["zh-Hans"]))

    def fails(self, needle):
        with self.assertRaisesRegex(ValueError, needle):
            self.call()

    def test_independent_cabinet_device_positive_and_no_workbench(self):
        source_before = self.data(self.o)
        objects, assets, loc, report = self.call()
        self.assertEqual(self.data(self.o), source_before)
        self.assertEqual({x.get("ID") for x in objects}, set(module.DEVICES))
        self.assertEqual(len(assets.findall("GameDBAsset")), 3)
        self.assertNotIn(module.WORKBENCH, self.data(objects).decode("utf-8"))
        self.assertNotIn("ASSET_TEX_OBJECTS_SMALL", self.data(objects).decode("utf-8"))
        self.assertNotIn("OBJECT_TABLE_EQUIPMENT", self.data(objects).decode("utf-8"))
        for obj in objects:
            self.assertEqual(obj.findtext("AttachedToObject"), "false")
            self.assertEqual(obj.findtext("Placement"), "INDOORS")
            self.assertEqual(obj.findtext("SpriteShape"), "SHAPE_1_X_1")
            self.assertEqual(obj.findtext("AccessPositions/AccessPosition/m_x"), "-1")
            self.assertIsNone(obj.find("AttachmentSlot"))
        self.assertEqual(len(loc["en"].findall(".//GameDBLocalizedString")), 4)
        self.assertEqual(len(report), 2)
        self.assertTrue(all(v["staff_reach"] == "UNVERIFIED" for v in report.values()))

    def test_reject_vanilla_CBC_and_RIA_tag_collision(self):
        child = self.o.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_ICP_MS']")
        put(child.find("Tags"), "Tag", "hematoanalyzer")
        self.fails("impersonates vanilla")

    def test_reject_invalid_parent_tags(self):
        node = self.o.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_WORKBENCH']")
        node.find("AttachmentSlot/AllowedTags/Tag").text = "ui_ria"
        self.fails("unexpected attachment")

    def test_reject_changed_source_model_not_attached(self):
        self.o.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_ICP_MS']/AttachedToObject").text = "false"
        self.fails("Unknown source placement")

    def test_reject_invalid_layout(self):
        self.o.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_ICP_MS']/TextureAtlasLayout").text = "LAYOUT_8_X_8"
        self.fails("Private one-tile atlas")

    def test_reject_wrong_direction(self):
        self.o.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_DIGESTION']/TextureIDSE").text = "9"
        self.fails("Four-direction atlas")

    def test_reject_wrong_private_icon(self):
        self.o.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_DIGESTION']/CustomIconAssetRef").text = "ASSET_ABCL_ART001_ICON_WORKBENCH"
        self.fails("private item icon")

    def test_reject_vanilla_resource_reference(self):
        self.a.find("./GameDBAsset[@ID='ASSET_TEX_ABCL_ART001_EQUIPMENT']/File").text = "MOD_ROOT/Textures/objects_small_atlas.png"
        self.fails("original/third-party")

    def test_reject_duplicate_clinical_object_or_ID(self):
        ET.SubElement(self.o, "GameDBObject", ID="OBJECT_HEMATOLOGY_ANALYZER")
        self.fails("Unexpected GameDBObject IDs")

    def test_reject_forced_connected_slot(self):
        child = self.o.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_ICP_MS']")
        ET.SubElement(child, "ConnectedSlots")
        self.fails("Unexpected nested/connected")

    def test_reject_non_interactable_variant(self):
        child = self.o.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_ICP_MS']")
        put(child, "NotInteractable", "true")
        self.fails("not eligible for independent")

    def test_reject_malformed_localized_resource(self):
        self.l["zh-Hans"].find(".//LanguageCode").text = "en"
        self.fails("Unexpected locale")

if __name__ == "__main__":
    unittest.main()
