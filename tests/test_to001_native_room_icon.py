"""TO-001 additive menu/floor icon source contract; native game L4 still required."""
from pathlib import Path
import hashlib
import struct
import unittest
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "assets" / "g1" / "Database"
ASSETS = ROOT / "assets" / "g1" / "Assets" / "ABCL"
FLOOR_SOURCE = ROOT / "assets" / "g1" / "Source" / "TO001" / "toxicology_floor_from_approved_128x64.png"
ACTIVE = "ASSET_ABCL_TOXICOLOGY_ROOM_ICON"
INACTIVE = "ASSET_ABCL_TOXICOLOGY_ROOM_ICON_INACTIVE"
FLOOR = "ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS"
ROOM_ID = "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB"

class TO001NativeRoomIconTests(unittest.TestCase):
    def test_approved_menu_and_floor_assets_are_additive(self):
        xml = ET.parse(DB / "ModAssetListsTO001.xml").getroot()
        assets = {x.get("ID"): x for x in xml.findall("GameDBAsset")}
        self.assertEqual(set(assets), {ACTIVE, INACTIVE, FLOOR})
        for key in (ACTIVE, INACTIVE):
            entry = assets[key]
            self.assertEqual(entry.findtext("Type"), "TEXTURE_CUSTOM_SPRITE")
            file_path = entry.findtext("File")
            self.assertEqual(file_path, "MOD_ROOT/Assets/ABCL/" + key.replace(
                "ASSET_ABCL_TOXICOLOGY_ROOM_ICON", "toxicology_room_icon").replace(
                "_INACTIVE", "_inactive") + ".png")
            payload = (ASSETS / Path(file_path).name).read_bytes()
            self.assertEqual(payload[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(payload[12:16], b"IHDR")
            self.assertEqual(struct.unpack(">IIBB", payload[16:26]), (64, 64, 8, 6))
            expected_hash = ("acb0042bb006f1f6a85c5b099f1c311ac5268b19944206cb1003b96a7930cb8a"
                             if key == ACTIVE else
                             "ebb5b1eec01aef7fc60c0479fd0efb32ebc942cb40a2b1629e06a677f774ba34")
            self.assertEqual(hashlib.sha256(payload).hexdigest(), expected_hash)
        self.assertNotEqual(hashlib.sha256((ASSETS / "toxicology_room_icon.png").read_bytes()).digest(),
                            hashlib.sha256((ASSETS / "toxicology_room_icon_inactive.png").read_bytes()).digest())
        floor = assets[FLOOR]
        self.assertEqual(floor.findtext("Type"), "TEXTURE")
        self.assertEqual(floor.findtext("File"),
                         "MOD_ROOT/Assets/ABCL/toxicology_floor_atlas_private_376.png")
        raw = FLOOR_SOURCE.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         "7c0d03ddbd370aca4ddd1a089ff91d814e1c2622659a3d300d844bd9713a8cb4")
        self.assertEqual(struct.unpack(">IIBB", raw[16:26]), (128, 64, 8, 6))

    def test_never_changes_vanilla_room_indices_or_zone_colors(self):
        room = ET.parse(DB / "ModRoomTypes.xml").getroot().find("GameDBRoomType")
        self.assertEqual(room.get("ID"), ROOM_ID)
        self.assertEqual(room.findtext("IconIndex"), "850")
        self.assertEqual(room.findtext("TextureID"), "376")
        self.assertEqual(room.findtext("AccessRights"), "STAFF")
        self.assertFalse((DB / "DLCRoomTypes.xml").exists())
        self.assertFalse((DB / "RoomTypes.xml").exists())

    def test_exact_room_menu_adapter_is_scoped_and_non_destructive(self):
        source = (ROOT / "src" / "ABCLG1Panel.cs").read_text(encoding="utf-8")
        adapter = source.split("internal sealed class G1ToxicologyRoomIconAdapter", 1)[1].split(
            "internal sealed class G1ToxicologyPrivateFloorIconAdapter", 1)[0]
        self.assertIn('RoomId = "' + ROOM_ID + '"', adapter)
        self.assertIn('ActiveId = "' + ACTIVE + '"', adapter)
        self.assertIn('InactiveId = "' + INACTIVE + '"', adapter)
        self.assertIn("private void LateUpdate()", source)
        self.assertIn("GetTextureAsset(ActiveId)", adapter)
        self.assertIn("GetTextureAsset(InactiveId)", adapter)
        self.assertIn("targetRoomItem.m_icon.GetComponent<IconController>()", adapter)
        self.assertIn("InsuranceManager.Instance.IsRoomLocked(targetRoom)", adapter)
        self.assertNotIn("SetIcon(850)", adapter)
        self.assertNotIn("m_roomType.IconIndex =", source)
        self.assertNotIn("FindObjectsOfType<RoomItemController>", adapter)
        self.assertNotIn("Harmony.Patch", source)

    def test_floor_adapter_targets_only_abcl_room_and_private_atlas(self):
        source = (ROOT / "src" / "ABCLG1Panel.cs").read_text(encoding="utf-8")
        adapter = source.split("internal sealed class G1ToxicologyPrivateFloorIconAdapter", 1)[1]
        self.assertIn('RoomId = "' + ROOM_ID + '"', adapter)
        self.assertIn('PrivateFloorAtlasId = "' + FLOOR + '"', adapter)
        self.assertIn("GetTextureAsset(PrivateFloorAtlasId)", adapter)
        self.assertIn("atlas.width != 2048 || atlas.height != 2048", adapter)
        self.assertIn("room.m_roomPersistentData.m_roomType.Entry.DatabaseID.ToString() != RoomId", adapter)
        self.assertIn("Renderer glyph", adapter)
        self.assertIn("Material material = glyph.material", adapter)
        self.assertNotIn("sharedMaterial.mainTexture =", adapter)
        self.assertIn("RestoreOwned()", adapter)
        self.assertIn("conflicts.Contains(glyph)", adapter)
        self.assertIn("to001FloorIcon.LateTick()", source)
        # The native IconController custom-asset path ignores m_inactive; the
        # private inactive sprite must therefore be a distinct no-background derivative.
        sys.path.insert(0, str(ROOT / "tools"))
        import assemble_to001_test_only as pack
        aw, ah, active_pixels = pack.decode_png_rgba((ASSETS / "toxicology_room_icon.png").read_bytes())
        iw, ih, inactive_pixels = pack.decode_png_rgba((ASSETS / "toxicology_room_icon_inactive.png").read_bytes())
        self.assertEqual((aw, ah, iw, ih), (64, 64, 64, 64))
        self.assertNotEqual(active_pixels, inactive_pixels)
        for i in range(0, len(active_pixels), 4):
            if active_pixels[i + 3]:
                self.assertEqual(inactive_pixels[i:i+3], bytes((145, 145, 145)))
                self.assertLessEqual(inactive_pixels[i+3], active_pixels[i+3])
            else:
                self.assertEqual(inactive_pixels[i+3], 0)

    def test_g1_clinical_contracts_and_localization_are_not_replaced(self):
        exams = ET.parse(DB / "ModExaminations.xml").getroot()
        ids = {x.get("ID") for x in exams.findall("GameDBExamination")}
        self.assertEqual(ids, {
            "EXM_ABCL_G1_BLOOD_LEAD_SAMPLING",
            "EXM_ABCL_G1_BLOOD_LEAD_TESTING",
        })
        self.assertNotIn("0Harmony", (ROOT / "src" / "ABCLG1Panel.cs").read_text("utf-8"))

if __name__ == "__main__":
    unittest.main()
