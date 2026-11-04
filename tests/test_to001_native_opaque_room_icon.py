"""TO-001 R10 failure: original room UI atlas is OPAQUE RED, not transparent.

Evidence: user-supplied vanilla StreamingAssets/Textures/ui/icons.png
correctly indexed with IconManager mapping: 850/854/2868 have 201,63,61 red
and 851/855/2869 have 153 grey. Hue 300-degree object textures are unrelated.
Only the runtime sprite is composited; D016 approved art SHA is untouched.
"""
from pathlib import Path
import unittest
SOURCE=(Path(__file__).resolve().parents[1]/"src/ABCLG1Panel.cs").read_text("utf-8")
ROOM=SOURCE.split("internal sealed class G1ToxicologyRoomIconAdapter",1)[1].split(
 "internal sealed class G1ToxicologyPrivateFloorIconAdapter",1)[0]
APPROVED=SOURCE.split("internal sealed class G1ApprovedPrivateTexture",1)[1].split(
 "// TO-001: optional additive UI-only adapter.",1)[0]
FLOOR=SOURCE.split("internal sealed class G1ToxicologyPrivateFloorIconAdapter",1)[1]
class NativeUIRoomAtlas(unittest.TestCase):
 def test_active_original_native_color_is_baked_in(self):
  self.assertIn("new Color32(201, 63, 61, 255)", APPROVED)
  self.assertIn("new Color32(153, 153, 153, 255)", APPROVED)
  self.assertIn("const float nativeWhite = 242f", APPROVED)
  self.assertIn("new Color32(171, 48, 62, 255)", APPROVED)
  self.assertIn("new Color32(120, 120, 120, 255)", APPROVED)
  self.assertIn("nativeStyled[i] = new Color32(", APPROVED)
  self.assertIn("255); // never transparent", APPROVED)
  self.assertNotIn("byte alpha = ", APPROVED)
  self.assertNotIn("nativeGlyphChannel", APPROVED)
 def test_exact_owner_source_remains_pinned_and_no_write(self):
  for h in ("225b2918c448b5d36d1d8582389e8952f2baf1574d0d72935017c81eab7d8199",
            "50c17ea8ba8b42b28295564f594713069a31c9e48fa05f3a6b623a36851b6490"):
   self.assertIn(h,ROOM)
  self.assertIn("SHA256.Create()",APPROVED)
  self.assertNotIn("File.WriteAllBytes",SOURCE)
  self.assertNotIn("File.WriteAllText",APPROVED)
 def test_only_exact_room_uses_native_paletted_sprite(self):
  self.assertIn("GetNativeRoomGlyphSprite()",ROOM)
  self.assertIn("IsExactNativeRoomButton(targetButtonRoot)",ROOM)
  self.assertIn("targetRoomItem.m_roomDatabaseID == RoomId",ROOM)
  self.assertIn("FitRoomListIconToNativeRow(targetSegment.m_icon)",ROOM)
  self.assertIn("FitRoomListIconToNativeRow(cachedLegacyImage.gameObject)",ROOM)
  self.assertIn("cachedSpriteProperty.SetValue(cachedSegmentImage, sprite, null)",ROOM)
  self.assertNotIn("m_customIconSprites[assetId] =",ROOM)
 def test_floor_l4_pass_unmodified(self):
  self.assertIn("00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd",FLOOR)
  for mode in ("BUILDING","BUILDING_FLOORS","LOGISTICS"):
   self.assertIn("roomView != ViewModes."+mode,FLOOR)
  self.assertIn("material.mainTexture = atlas",FLOOR)
  self.assertNotIn("sharedMaterial.mainTexture =",FLOOR)
 def test_rejected_old_opaque_dark_and_transparent_versions_are_not_reintroduced(self):
  self.assertNotIn("nativeGlyphChannel",APPROVED)
  self.assertNotIn("new Color32(nativeGlyphChannel,",APPROVED)
  self.assertNotIn("ownedSprite",APPROVED)
if __name__=="__main__":unittest.main()
