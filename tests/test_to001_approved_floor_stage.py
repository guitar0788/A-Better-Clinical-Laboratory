"""Owner-approved TO001 floor stage: source-only/negative acceptance contracts.

This is NOT a Unity L3 or gameplay L4 verification.
"""
from pathlib import Path
import ast
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
BUILDER=ROOT/"tools/stage_to001_approved_floor.py"
SOURCE=BUILDER.read_text("utf-8")
G1_ROOMS=ET.parse(ROOT/"assets/g1/Database/ModRoomTypes.xml").getroot()
ORIGINAL_ASSET=ET.parse(ROOT/"assets/g1/Database/ModAssetListsTO001.xml").getroot()

class ApprovedTO001FloorStageTests(unittest.TestCase):
    def test_exact_approval_pins_and_blob_verification(self):
        ast.parse(SOURCE, filename=str(BUILDER))
        for required in (
            "d56b89962c0664fb37fc39113caed92892a335cc",
            "c4a81670a2b0004799513c5b03a61b9239af1f5b",
            "149bc34ebe68194d13054d91564c28700b5311ab",
            "76995aef9bb3eb851c28101d0b75200552bc85e91dc28247ebd0e786e6cab4ec",
            "7c0d03ddbd370aca4ddd1a089ff91d814e1c2622659a3d300d844bd9713a8cb4",
            "module.verify_vector(",
            "Approved room glyph source changed",
            "Approved floor PNG has changed",
        ):
            self.assertIn(required, SOURCE)
        self.assertIn("Refuse overwriting previous art stage", SOURCE)

    def test_private_atlas_grid_and_runtime_asset_are_isolated(self):
        for required in (
            "ATLAS_SIZE = (2048, 2048)",
            "CELL_SIZE = (128, 64)",
            "TILE_ID = 376",
            "TILE_COLUMNS = 16",
            "TILE_ROWS = 32",
            'ATLAS_ID = "ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS"',
            'ET.SubElement(e, "Type").text = "TEXTURE"',
            "atlas.paste(floor, (x, y))",
            "original_base_game_assets_included",
            '"native_game_L4": "NOT_RUN"',
        ):
            self.assertIn(required, SOURCE)
        self.assertNotIn("StreamingAssets/Textures/", SOURCE)
        self.assertNotIn("sharedMaterial.mainTexture =", SOURCE)
        self.assertNotIn("GameDBMedicalCondition", SOURCE)

    def test_never_change_base_room_fallback_or_original_menu_ids(self):
        room=G1_ROOMS.find("GameDBRoomType")
        self.assertEqual(room.get("ID"),"ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB")
        self.assertEqual(room.findtext("TextureID"),"376")
        self.assertEqual(room.findtext("IconIndex"),"850")
        assets={x.get("ID"):x for x in ORIGINAL_ASSET.findall("GameDBAsset")}
        self.assertEqual(set(assets),{
            "ASSET_ABCL_TOXICOLOGY_ROOM_ICON",
            "ASSET_ABCL_TOXICOLOGY_ROOM_ICON_INACTIVE",
        })
        self.assertFalse((ROOT/"assets/g1/Database/ModDiagnoses.xml").exists())

    def test_output_is_not_installer_or_release(self):
        self.assertNotIn("Install-ABCL-G1.ps1", SOURCE)
        self.assertNotIn("ModABCLG1LeadTest.dll", SOURCE)
        self.assertNotIn("0Harmony.dll", SOURCE)
        self.assertIn("Do not create staged resources under the live game", SOURCE)
        self.assertIn("Refuse overwriting previous art stage", SOURCE)

if __name__=="__main__":
    unittest.main()
