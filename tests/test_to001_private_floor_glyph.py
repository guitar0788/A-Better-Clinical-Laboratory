"""L2 source gate for TO-001 private floor-glyph candidate.

Important: this check does NOT prove net35 ABI or in-game rendering.
The private FA atlas is deliberately unregistered until L3 + art gate.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "src" / "ABCLG1Panel.cs").read_text("utf-8")
ROOM = ET.parse(ROOT / "assets/g1/Database/ModRoomTypes.xml").getroot().find("GameDBRoomType")


class TO001PrivateFloorGlyphTests(unittest.TestCase):
    def test_uses_original_floor_texture_channel_without_mutating_room_database(self):
        self.assertEqual(ROOM.get("ID"), "ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB")
        self.assertEqual(ROOM.findtext("TextureID"), "376")
        self.assertEqual(ROOM.findtext("IconIndex"), "850")
        self.assertIn("G1ToxicologyPrivateFloorIconAdapter", SOURCE)
        bridge = SOURCE.split("internal sealed class G1ToxicologyPrivateFloorIconAdapter", 1)[1]
        for token in (
            'PrivateFloorAtlasId = "ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS"',
            'GetField("m_roomRenderer"',
            'GetField("m_roomData"',
            "ViewModes.LOGISTICS",
            "MapEditorController.sm_instance.CurrentFloorRenderer",
            "room.m_roomPersistentData.m_roomType.Entry.DatabaseID.ToString() != RoomId",
            "renderer",  # underlying renderer is accessed via room glyph GameObject
            'GetTextureAsset(floorAsset.Value)',
            "atlas.width != 2048 || atlas.height != 2048",
            "material.mainTexture != baseline",
            "material.mainTexture = atlas",
            "RestoreOwned();",
            "Time.unscaledTime + 0.75f",
        ):
            self.assertIn(token, bridge, token)
        for forbidden in ("Harmony.Patch", "sharedMaterial", "roomType.TextureID =", "roomType.IconIndex =",
                          "GameObject.Find", "DestroyImmediate", "Save(", "SetIcon(850)"):
            self.assertNotIn(forbidden, bridge, forbidden)

    def test_missing_artist_asset_has_no_live_behavior_and_no_accidental_mod_copy(self):
        db = ROOT / "assets/g1/Database/ModAssetListsTO001.xml"
        xml = ET.parse(db).getroot()
        assets = [x.get("ID") for x in xml.findall("GameDBAsset")]
        self.assertNotIn("ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS", assets)
        self.assertIn('GetEntry<GameDBAsset>(PrivateFloorAtlasId) == null', SOURCE)
        # Source-only candidate: delivering a new atlas requires a distinct,
        # source-controlled FA and L3 package gate, not an undocumented swap.
        self.assertFalse((ROOT / "assets/g1/Assets/ABCL/toxicology_floor_tile_atlas.png").exists())


if __name__ == "__main__":
    unittest.main()
