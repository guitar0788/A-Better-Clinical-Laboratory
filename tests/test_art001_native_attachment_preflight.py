"""Standalone negative-contract tests; no original game code or art is included."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "audit_art001_native_attachment.py"
spec = importlib.util.spec_from_file_location("ts_art_native_preflight", SCRIPT)
auditor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auditor)


def field(parent, name, value):
    ET.SubElement(parent, name).text = str(value)


def build_fixture(path):
    path = Path(path)
    objects = ET.Element("Database")
    workbench = ET.SubElement(objects, "GameDBObject", ID=auditor.WORKBENCH)
    for k, v in (
        ("AttachedToObject", "false"), ("Placement", "INDOORS"),
        ("SpriteShape", "SHAPE_1_X_1"), ("TextureRef", "ASSET_TEX_OBJECTS_SMALL"),
        ("TextureAtlasLayout", "LAYOUT_16_X_64"),
    ):
        field(workbench, k, v)
    for d, i in zip(auditor.DIRECTIONS, (472, 473, 474, 475)):
        field(workbench, "TextureID" + d, i)
    slot = ET.SubElement(workbench, "AttachmentSlot")
    field(slot, "ForcesAttachmentOrientation", "false")
    allowed = ET.SubElement(slot, "AllowedTags")
    for tag, _ in auditor.DEVICES.values():
        field(allowed, "Tag", tag)

    for key, (tag, frames) in auditor.DEVICES.items():
        obj = ET.SubElement(objects, "GameDBObject", ID=key)
        for k, v in (
            ("AttachedToObject", "true"), ("SpriteShape", "SHAPE_1_X_1"),
            ("TextureRef", "ASSET_TEX_ABCL_ART001_EQUIPMENT"),
            ("TextureAtlasLayout", "LAYOUT_16_X_8"),
            ("CustomIconAssetRef", "ASSET_ABCL_ART001_ICON_ICPMS"),
        ):
            field(obj, k, v)
        for d, i in zip(auditor.DIRECTIONS, frames):
            field(obj, "TextureID" + d, i)
        tags = ET.SubElement(obj, "Tags")
        field(tags, "Tag", tag)
        for name in ("UseAnimations", "UseAnimationsStart", "UseAnimationsEnd"):
            field(ET.SubElement(obj, name), "Animation", "stand_ria_use_idle")

    assets = ET.Element("Database")
    for key, kind, filename in (
        ("ASSET_TEX_ABCL_ART001_EQUIPMENT", "TEXTURE_OBJECTS", "equipment_atlas.png"),
        ("ASSET_ABCL_ART001_ICON_ICPMS", "TEXTURE_CUSTOM_SPRITE", "icp_ms_icon.png"),
        ("ASSET_ABCL_ART001_ICON_DIGESTION", "TEXTURE_CUSTOM_SPRITE", "digestion_station_icon.png"),
        ("ASSET_ABCL_ART001_ICON_WORKBENCH", "TEXTURE_CUSTOM_SPRITE", "workbench_icon.png"),
    ):
        node = ET.SubElement(assets, "GameDBAsset", ID=key)
        field(node, "Type", kind)
        field(node, "File", "MOD_ROOT/Assets/ABCL/" + filename)
    ET.ElementTree(objects).write(path / "ModObjectsABCL.xml", encoding="utf-8")
    ET.ElementTree(assets).write(path / "ModAssetListsABCL.xml", encoding="utf-8")
    return objects, assets


class NativeArt001Preflight(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name)
        self.objects, self.assets = build_fixture(self.path)

    def tearDown(self):
        self.temp.cleanup()

    def rewrite(self):
        ET.ElementTree(self.objects).write(
            self.path / "ModObjectsABCL.xml", encoding="utf-8")
        ET.ElementTree(self.assets).write(
            self.path / "ModAssetListsABCL.xml", encoding="utf-8")

    def expect_failure(self, message):
        with self.assertRaisesRegex(ValueError, message):
            auditor.validate(self.path)

    def test_positive_private_contract_carries_explicit_native_limit(self):
        result = auditor.validate(self.path)
        self.assertEqual(result["workbench_capacity_per_tile"], 1)
        self.assertEqual(result["separate_workbench_instances_needed_to_place_both"], 2)
        self.assertIn("NOT_ALLOWED_BLOCKED", result["same_tile_second_device"])
        self.assertEqual(result["native_game_L4"], "NOT_RUN")
        self.assertEqual(set(result["devices"]), set(auditor.DEVICES))

    def test_occupied_table_not_misrepresented_as_two_slots(self):
        result = auditor.validate(self.path)
        self.assertEqual(result["workbench_capacity_per_tile"], 1)
        self.assertNotEqual(result["workbench_capacity_per_tile"], len(result["devices"]))

    def test_vanilla_tag_collision_fails_closed(self):
        child = self.objects.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_ICP_MS']")
        field(child.find("Tags"), "Tag", "hematoanalyzer")
        self.rewrite()
        self.expect_failure("vanilla laboratory tag")

    def test_wrong_parent_allowlist_fails_closed(self):
        allowed = self.objects.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_WORKBENCH']/AttachmentSlot/AllowedTags")
        allowed.find("Tag").text = "stat_lab_exam"
        self.rewrite()
        self.expect_failure("Parent allowed tags")

    def test_forced_rotation_is_rejected(self):
        forced = self.objects.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_WORKBENCH']/AttachmentSlot/ForcesAttachmentOrientation")
        forced.text = "true"
        self.rewrite()
        self.expect_failure("force child orientation")

    def test_spurious_connected_slot_is_rejected(self):
        workbench = self.objects.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_WORKBENCH']")
        ET.SubElement(workbench, "ConnectedSlots")
        self.rewrite()
        self.expect_failure("connected slots")

    def test_wrong_rotation_sprite_id_is_rejected(self):
        digestion = self.objects.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_DIGESTION']")
        digestion.find("TextureIDSW").text = "7"
        self.rewrite()
        self.expect_failure("Native NW/NE/SE/SW")

    def test_original_object_id_overwrite_is_rejected(self):
        obj = self.objects.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_ICP_MS']")
        obj.attrib["ID"] = "OBJECT_RIA"
        self.rewrite()
        self.expect_failure("Do not add/overwrite native")

    def test_second_instrument_cannot_impersonate_first(self):
        digestion = self.objects.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_DIGESTION']")
        field(digestion.find("Tags"), "Tag", "abcl_art001_icp_ms")
        self.rewrite()
        self.expect_failure("exactly one private parent tag")

    def test_no_shared_vanilla_atlas_registration(self):
        obj = self.assets.find("./GameDBAsset[@ID='ASSET_TEX_ABCL_ART001_EQUIPMENT']")
        obj.set("ID", "ASSET_TEX_OBJECTS_SMALL")
        self.rewrite()
        self.expect_failure("shared or original game asset IDs")

    def test_rejects_unbound_child(self):
        child = self.objects.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_ICP_MS']")
        child.find("AttachedToObject").text = "false"
        self.rewrite()
        self.expect_failure("requires a native attachment parent")


if __name__ == "__main__":
    unittest.main()
