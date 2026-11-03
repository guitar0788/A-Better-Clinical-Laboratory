"""TO+FA integrated pre-L4 source contracts, no gameplay pass asserted."""
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
BUILDER=(ROOT/"tools/build_tofa_unified_l4.py").read_text(encoding="utf-8")
INSTALL=(ROOT/"tools/Install-TOFA-Unified.ps1").read_text(encoding="utf-8")
WORKFLOW=(ROOT/".github/workflows/build-tofa-unified-l4.yml").read_text(encoding="utf-8")
CORE=(ROOT/"src/ABCLG1Panel.cs").read_text(encoding="utf-8")
CS=(ROOT/"src/ABCL.G1.Panel.csproj").read_text(encoding="utf-8")

class TOFAUnifiedContract(unittest.TestCase):
    def test_exact_external_branch_commit_pins(self):
        for sha in ("cafcc32d9eb21b1f7e5df39a7f7f443d3ebf1da7",
                    "eac88c04f6d585e987b921938b76e3a3a4d4d1b0"):
            self.assertIn(sha,BUILDER)
            self.assertIn(sha,WORKFLOW)
        self.assertIn("github.sha",WORKFLOW)
        self.assertIn("Exact-head Verify PASS",WORKFLOW)
        self.assertIn("ABCL_G1_AES256_KEY",WORKFLOW)
        self.assertNotIn("secrets.ABCL_G1_AES256_KEY",BUILDER)

    def test_both_addons_are_in_one_package_without_vanilla_overwrites(self):
        for piece in ("ModABCLG1LeadTest/","ModABCLArt001Test/",
                      "ModAssetListsTO004.xml","ModPrefabObjectsTO004.xml",
                      "ModObjectsABCL.xml","ModColorSets.xml",
                      "TOFA_L4_CHECKLIST.txt","RESTORE_TOFA_PREVIOUS.cmd",
                      "ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS"):
            self.assertIn(piece,BUILDER)
        room=ET.parse(ROOT/"assets/g1/Database/ModRoomTypes.xml").getroot().find("GameDBRoomType")
        self.assertEqual(room.findtext("TextureID"),"376")
        self.assertEqual(room.findtext("IconIndex"),"850")
        self.assertNotIn("GameDBAsset ID=\"ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS\"", 
                         (ROOT/"assets/g1/Database/ModAssetListsTO001.xml").read_text("utf-8"))

    def test_single_install_and_rollback_scope(self):
        for piece in ("BUILD_INFO.json","Get-FileHash","Move-Item","_TOFA_PREVIOUS_ABCL_TEST_ONLY",
                      "ProjectHospital_Data\\StreamingAssets\\Addons",
                      "if ($Restore)","Check-Owned","Install-ABCL-G1.ps1"):
            self.assertIn(piece,INSTALL)
        self.assertNotIn("Remove-Item -LiteralPath $gameDb",INSTALL)
        self.assertIn("original assets", 
            (ROOT/"tools/TOFA_L4_CHECKLIST.txt").read_text("utf-8").lower())

    def test_tree_probe_and_floor_bridge_both_included(self):
        self.assertIn("G1ToxicologyPrivateFloorIconAdapter",CORE)
        self.assertIn("ABCLTO002ReadOnlyTreeProbe",CORE)
        self.assertIn('<Compile Include="ABCLTO002ReadOnlyTreeProbe.cs" />',CS)
        probe=(ROOT/"src/ABCLTO002ReadOnlyTreeProbe.cs").read_text("utf-8")
        self.assertIn("DependencyTreePanelController",probe)
        self.assertNotIn("Harmony.Patch",probe)

if __name__=="__main__":
    unittest.main()
