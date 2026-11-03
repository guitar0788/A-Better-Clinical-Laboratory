"""TO-001: source-only native UI, original-art and noninterference contract.

This test is L2 only: exact in-game behavior requires native Windows L3 and L4.
"""
from pathlib import Path
import re
import struct
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "assets" / "g1" / "Database"
ASSETS = ROOT / "assets" / "g1" / "Assets" / "ABCL"
ACTIVE = "ASSET_ABCL_TOXICOLOGY_ROOM_ICON"
INACTIVE = "ASSET_ABCL_TOXICOLOGY_ROOM_ICON_INACTIVE"
ROOM_ID = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB"


class TO001NativeRoomIconTests(unittest.TestCase):
    def test_private_icon_assets_are_additive_and_native_loader_compatible(self):
        xml = ET.parse(DB / "ModAssetListsTO001.xml").getroot()
        assets = {x.get("ID"): x for x in xml.findall("GameDBAsset")}
        self.assertEqual(set(assets), {ACTIVE, INACTIVE})
        for key, entry in assets.items():
            self.assertEqual(entry.findtext("Type"), "TEXTURE_CUSTOM_SPRITE")
            file_path = entry.findtext("File")
            self.assertTrue(file_path.startswith("MOD_ROOT/Assets/ABCL/"))
            self.assertNotIn("..", file_path)
            png = ASSETS / Path(file_path).name
            self.assertTrue(png.is_file())
            payload = png.read_bytes()
            self.assertEqual(payload[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(payload[12:16], b"IHDR")
            w, h, depth, color = struct.unpack(">IIBB", payload[16:26])
            self.assertEqual((w, h, depth, color), (64, 64, 8, 6))
            self.assertGreater(len(payload), 300)

    def test_never_changes_vanilla_room_indices_or_zone_colors(self):
        room = ET.parse(DB / "ModRoomTypes.xml").getroot().find("GameDBRoomType")
        self.assertEqual(room.get("ID"), ROOM_ID)
        self.assertEqual(room.findtext("IconIndex"), "850")
        self.assertEqual(room.findtext("TextureID"), "376")
        self.assertEqual(room.findtext("AccessRights"), "STAFF")
        self.assertFalse((DB / "DLCRoomTypes.xml").exists())
        self.assertFalse((DB / "RoomTypes.xml").exists())

    def test_exact_room_no_global_sprite_patch_and_correct_update_order(self):
        source = (ROOT / "src" / "ABCLG1Panel.cs").read_text(encoding="utf-8")
        adapter = source.split("internal sealed class G1ToxicologyRoomIconAdapter", 1)[1]
        self.assertIn('RoomId = "' + ROOM_ID + '"', adapter)
        self.assertIn('ActiveId = "' + ACTIVE + '"', adapter)
        self.assertIn('InactiveId = "' + INACTIVE + '"', adapter)
        self.assertIn('private void LateUpdate()', source)
        self.assertIn('targetSegment.m_icon.GetComponent("Image")', adapter)
        self.assertIn('cachedSegmentImage.GetType().GetProperty("sprite"', adapter)
        self.assertIn("private PropertyInfo cachedSpriteProperty;", source)
        self.assertIn("cachedSegmentImage.gameObject != targetSegment.m_icon", adapter)
        self.assertNotIn("using UnityEngine.UI;", source)
        self.assertIn("targetRoomItem.m_icon.GetComponent<IconController>()", adapter)
        self.assertIn("RoomButtonItemId.GetValue(button)", adapter)
        self.assertIn("BuildingModeItemType.ROOM", adapter)
        self.assertIn("RoomButtonItemId.GetValue(button) as string", adapter)
        self.assertIn("id == RoomId", adapter)
        self.assertIn("item.m_roomDatabaseID == RoomId", adapter)
        self.assertIn("InsuranceManager.Instance.IsRoomLocked(targetRoom)", adapter)
        self.assertIn("cachedSpriteProperty.PropertyType == typeof(Sprite)", adapter)
        self.assertIn("(cachedSpriteProperty.GetValue(cachedSegmentImage, null) as Sprite) != sprite", adapter)
        self.assertIn("cachedSpriteProperty.SetValue(cachedSegmentImage, sprite, null)", adapter)
        self.assertIn("GetTextureAsset(ActiveId)", adapter)
        self.assertIn("GetTextureAsset(InactiveId)", adapter)
        self.assertIn("Time.unscaledTime + 0.75f", adapter)
        self.assertNotIn("Harmony.Patch", source)
        self.assertNotIn("SetIcon(850)", adapter)
        self.assertNotIn("m_roomType.IconIndex =", source)
        self.assertNotIn("UISettings.Instance.", adapter)
        self.assertNotIn("RoomRenderer", adapter)
        # Do not use global per-frame scene-wide RoomItemController enumeration.
        self.assertNotIn("FindObjectsOfType<RoomItemController>", adapter)
        self.assertNotIn("FindObjectsOfType<IconController>", adapter)
        self.assertNotIn("Image.color =", adapter)
        self.assertNotIn("Save(", adapter)

    def test_g1_clinical_contracts_and_localization_not_replaced(self):
        examinations = ET.parse(DB / "ModExaminations.xml").getroot()
        exam_ids = {x.get("ID") for x in examinations.findall("GameDBExamination")}
        self.assertEqual(exam_ids, {
            "EXM_ABCL_G1_BLOOD_LEAD_SAMPLING",
            "EXM_ABCL_G1_BLOOD_LEAD_TESTING",
        })
        self.assertNotIn("0Harmony", (ROOT / "src" / "ABCLG1Panel.cs").read_text("utf-8"))


if __name__ == "__main__":
    unittest.main()
