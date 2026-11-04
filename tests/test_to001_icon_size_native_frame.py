"""Owner R8 regression — source-only checks, not a native L4 PASS."""
from pathlib import Path
import unittest
S=(Path(__file__).resolve().parents[1]/"src/ABCLG1Panel.cs").read_text("utf-8")
ROOM=S.split("internal sealed class G1ToxicologyRoomIconAdapter",1)[1].split("internal sealed class G1ToxicologyPrivateFloorIconAdapter",1)[0]
FLOOR=S.split("internal sealed class G1ToxicologyPrivateFloorIconAdapter",1)[1]
ENTRY=S.split("public sealed class ModEntryPoint",1)[1].split("private bool HospitalIsReady()",1)[0]
class IconDisplayGate(unittest.TestCase):
 def test_menu_icon_native_size(self):
  self.assertIn("MatchedPrivateRoomIconSide = 34f",ROOM)
  self.assertIn("Mathf.Abs(rect.rect.width - MatchedPrivateRoomIconSide)",ROOM)
  self.assertIn("Mathf.Abs(rect.rect.height - MatchedPrivateRoomIconSide)",ROOM)
  self.assertNotIn("MaxNativeRoomIconSide = 30f",ROOM)
  self.assertIn("FitRoomListIconToNativeRow(targetSegment.m_icon)",ROOM)
  self.assertIn("FitRoomListIconToNativeRow(cachedLegacyImage.gameObject)",ROOM)
  self.assertIn("SetSizeWithCurrentAnchors",ROOM)
 def test_floor_no_delayed_original_marker(self):
  self.assertNotIn("nextScan",FLOOR)
  self.assertIn("if (material.mainTexture != atlas)",FLOOR)
  self.assertIn("room.m_roomPersistentData.m_roomType.Entry.DatabaseID.ToString() != RoomId",FLOOR)
  self.assertNotIn("sharedMaterial.mainTexture =",FLOOR)
 def test_pre_render_hook_lifecycle(self):
  self.assertIn("Camera.onPreCull += BeforeMainCameraCull",ENTRY)
  self.assertIn("Camera.onPreCull -= BeforeMainCameraCull",ENTRY)
  self.assertIn("camera != Camera.main",ENTRY)
  self.assertIn("to001FloorIcon.ReleaseOwned()",ENTRY)
 def test_art_pins_untouched(self):
  for v in ("c2c6c83cb0f8c2ca49dce7184bdd4f71df1c71a20ecf0c38e05337df6a48f62b","eb37ce261299f7df2ac87c61272168f71b5faca5de1578b71a172a8d75e861eb","00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd"):
   self.assertIn(v,S)
if __name__=="__main__":unittest.main()
