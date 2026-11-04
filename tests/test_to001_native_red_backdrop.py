"""R9 owner screenshot: native room-list red-background composition.

Confirmed native icons.png #850/#854 are white RGBA sprites with transparent
background; ABCL approved PNG is SHA-pinned opaque RGB(171,48,62). We render
only the preserved white flask in memory over the ORIGINAL native UI red,
without rewriting PNGs or touching the already-passing floor glyph.
"""
from pathlib import Path
import unittest
S=(Path(__file__).resolve().parents[1]/"src/ABCLG1Panel.cs").read_text("utf-8")
RES=S.split("internal sealed class G1ApprovedPrivateTexture",1)[1].split(
 "// TO-001: optional additive UI-only adapter.",1)[0]
ROOM=S.split("internal sealed class G1ToxicologyRoomIconAdapter",1)[1].split(
 "internal sealed class G1ToxicologyPrivateFloorIconAdapter",1)[0]
FLOOR=S.split("internal sealed class G1ToxicologyPrivateFloorIconAdapter",1)[1]

class NativePaletteContract(unittest.TestCase):
 def test_bytes_and_approved_sha_are_unchanged(self):
  for h in ("225b2918c448b5d36d1d8582389e8952f2baf1574d0d72935017c81eab7d8199",
            "50c17ea8ba8b42b28295564f594713069a31c9e48fa05f3a6b623a36851b6490"):
   self.assertIn(h,ROOM)
  self.assertNotIn("File.WriteAllBytes",S)
  self.assertNotIn("Texture2D.SetPixels(",S)
  self.assertNotIn("GetRoomSprite()",S)
 def test_native_white_gray_overlay_does_not_embed_red_backdrop(self):
  self.assertIn("new Color32(171, 48, 62, 255)",RES)
  self.assertIn("new Color32(120, 120, 120, 255)",RES)
  self.assertIn("nativeGlyphChannel = disabled ? (byte)77 : (byte)242",RES)
  self.assertIn("approvedSource.GetPixels32()",RES)
  self.assertIn("glyph.SetPixels32(overlay)",RES)
  self.assertIn("new Color32(nativeGlyphChannel,",RES)
  self.assertIn("GetNativeRoomGlyphSprite()",RES)
  self.assertIn("visiblePixels < 20 || visiblePixels > 2048",RES)
 def test_both_native_room_ui_paths_use_derived_sprite(self):
  self.assertIn("GetNativeRoomGlyphSprite()",ROOM)
  self.assertIn("FitRoomListIconToNativeRow(targetSegment.m_icon)",ROOM)
  self.assertIn("FitRoomListIconToNativeRow(cachedLegacyImage.gameObject)",ROOM)
  self.assertIn("cachedSpriteProperty.SetValue(cachedSegmentImage, sprite, null)",ROOM)
  self.assertIn("cachedLegacySpriteProperty.SetValue(cachedLegacyImage, sprite, null)",ROOM)
  self.assertNotIn("sharedMaterial",ROOM)
 def test_floor_l4_pass_not_regressed(self):
  self.assertIn("G1ApprovedPrivateTexture(\"toxicology_floor_atlas_private_376.png\"",FLOOR)
  self.assertIn("00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd",FLOOR)
  self.assertIn("roomView != ViewModes.BUILDING",FLOOR)
  self.assertIn("roomView != ViewModes.BUILDING_FLOORS",FLOOR)
  self.assertIn("material.mainTexture = atlas;",FLOOR)
if __name__=="__main__": unittest.main()
