"""No-regression contract for the exact ABCL native hybrid UI image bridge.

This is offline evidence ONLY; it cannot claim native net35 compilation or
Project Hospital runtime UI acceptance. Owner artwork is frozen in PR #48.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ApprovedRoomBindingContract(unittest.TestCase):
    def test_direct_ui_component_and_build_reference(self):
        source = (ROOT / "src" / "ABCLG1Panel.cs").read_text("utf-8")
        proj = (ROOT / "src" / "ABCL.G1.Panel.csproj").read_text("utf-8")
        self.assertIn("using UnityEngine.UI;", source)
        self.assertIn('<Reference Include="UnityEngine.UI">', proj)
        self.assertIn("UnityEngine.UI.dll", proj)
        self.assertNotIn('GetComponent("Image")', source)
        self.assertNotIn("cachedSpriteProperty", source)

    def test_exact_scoped_row_and_owned_sprite_only(self):
        source = (ROOT / "src" / "ABCLG1Panel.cs").read_text("utf-8")
        adapter = source.split("internal sealed class G1ToxicologyRoomIconAdapter", 1)[1].split(
            "internal sealed class G1ToxicologyPrivateFloorIconAdapter", 1)[0]
        self.assertIn("IsExactNativeRoomButton(targetButtonRoot)", adapter)
        self.assertIn("targetSegment.m_icon.GetComponent<Image>()", adapter)
        self.assertIn("cachedSegmentImage.overrideSprite == null", adapter)
        self.assertIn("cachedSegmentImage.color = Color.white", adapter)
        self.assertIn("cachedSegmentImage.sprite = sprite", adapter)
        self.assertIn('private bool loggedHybridBind;', adapter)
        self.assertNotIn("IconIndex =", adapter)
        self.assertNotIn("sharedMaterial", adapter)
        self.assertNotIn("SetIcon(850)", adapter)
        self.assertNotIn("SetIcon(3070)", adapter)

    def test_never_rewrites_owner_art_or_native_floor(self):
        source = (ROOT / "src" / "ABCLG1Panel.cs").read_text("utf-8")
        adapter = source.split("internal sealed class G1ToxicologyRoomIconAdapter", 1)[1].split(
            "internal sealed class G1ToxicologyPrivateFloorIconAdapter", 1)[0]
        self.assertNotIn("Texture2D.SetPixel", adapter)
        self.assertNotIn("Texture2D.SetPixels", adapter)
        self.assertNotIn("Graphics.Blit(", adapter)
        self.assertNotIn("new Sprite(", adapter)


if __name__ == "__main__":
    unittest.main()
