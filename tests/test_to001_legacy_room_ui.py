"""Original RoomItemController / IconController native compatibility.

The original IconController.GetIcon(string) chooses a vanilla placeholder
when no custom ID was registered. Approved local fallback must cover both
hybrid room list and native RoomItemController legacy room list, without
editing any approved PNG or other room.
"""
from pathlib import Path
import unittest
SOURCE=(Path(__file__).resolve().parents[1]/"src/ABCLG1Panel.cs").read_text("utf-8")
ROOM=SOURCE.split("internal sealed class G1ToxicologyRoomIconAdapter",1)[1].split(
 "internal sealed class G1ToxicologyPrivateFloorIconAdapter",1)[0]
class LegacyRoomMenu(unittest.TestCase):
 def test_same_sha_verified_sprite_for_both_native_ui_paths(self):
  self.assertIn("locked ? approvedInactive : approvedActive",ROOM)
  self.assertIn("targetRoomItem.m_roomDatabaseID == RoomId",ROOM)
  self.assertIn("targetRoomItem.m_icon.GetComponent<IconController>()",ROOM)
  self.assertIn("GetComponentsInChildren<UnityEngine.Component>(true)",ROOM)
  self.assertIn('component.GetType().FullName != "UnityEngine.UI.Image"',ROOM)
  self.assertIn("cachedLegacySpriteProperty.SetValue(cachedLegacyImage, sprite, null)",ROOM)
  self.assertNotIn("icon.SetIcon(assetId)",ROOM)
 def test_no_foreign_ui_override_and_no_global_icon_mutations(self):
  self.assertIn("icon.m_customIconAssetID != ActiveId",ROOM)
  self.assertIn("icon.m_customIconAssetID != InactiveId",ROOM)
  self.assertIn("thirdPartyOverride == current",ROOM)
  self.assertIn("cachedLegacyColorProperty.SetValue(cachedLegacyImage, Color.white, null)",ROOM)
  self.assertNotIn("m_customIconSprites[assetId] =",ROOM)
  self.assertNotIn("m_roomType.IconIndex =",ROOM)
 def test_native_floor_view_fixes_remain(self):
  floor=SOURCE.split("internal sealed class G1ToxicologyPrivateFloorIconAdapter",1)[1]
  for view in ("BUILDING","BUILDING_FLOORS","LOGISTICS"):
   self.assertIn("roomView != ViewModes."+view,floor)
  self.assertIn("RoomId",floor)
  self.assertNotIn("sharedMaterial.mainTexture =",floor)
if __name__=="__main__": unittest.main()
