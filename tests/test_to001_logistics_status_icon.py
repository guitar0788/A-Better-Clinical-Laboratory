"""TO-001 status-bar adapter: deliberately narrow source-only regression check.

This does not establish success for room zoning, larger icon sizing, or L3/L4.
"""
from pathlib import Path
import unittest

SRC = (Path(__file__).resolve().parents[1] / "src" / "ABCLG1Panel.cs").read_text(encoding="utf-8")


class TO001LogisticsStatusTests(unittest.TestCase):
    def test_status_icon_override_requires_exact_live_abcl_room(self):
        start = SRC.index("private void UpdateExactRoomHoverStatusIcon(")
        end = SRC.index("private void FindHybridRoomRow()", start)
        body = SRC[start:end]
        for key in (
            "ViewModes.LOGISTICS",
            "editor.m_hoverOverObject as Room",
            "hoveredRoom.m_roomPersistentData.m_roomType.Entry.DatabaseID.ToString() != RoomId",
            "panel.m_textStatusBar.activeInHierarchy",
            "panel.m_textStatusBar.GetComponentInChildren<IconController>()",
            "icon.m_customIconAssetID != assetId",
            "icon.SetIcon(assetId)",
        ):
            self.assertIn(key, body)
        self.assertNotIn("SetIcon(850)", body)
        self.assertNotIn("RoomRenderer", body)
        self.assertNotIn("TextureID =", body)
        self.assertNotIn("IconIndex =", body)

    def test_hook_uses_only_existing_private_asset_ready_path(self):
        tick = SRC.split("private void Tick()", 1)[1].split("private void UpdateExactRoomHoverStatusIcon(", 1)[0]
        self.assertIn("GetTextureAsset(ActiveId)", tick)
        self.assertIn("GetTextureAsset(InactiveId)", tick)
        self.assertIn("UpdateExactRoomHoverStatusIcon(assetId);", tick)
        self.assertIn("private void LateUpdate()", SRC)
        self.assertNotIn("Harmony.Patch", SRC)


if __name__ == "__main__":
    unittest.main()
