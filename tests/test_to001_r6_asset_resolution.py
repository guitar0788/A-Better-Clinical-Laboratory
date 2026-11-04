"""R6 log regression: confirmed G1 loads, native icon preflight rejects one asset."""
from pathlib import Path
import unittest
SRC=(Path(__file__).resolve().parents[1]/"src/ABCLG1Panel.cs").read_text("utf-8")
class PrivateArt(unittest.TestCase):
 def test_exact_source_pins(self):
  for sha in ("225b2918c448b5d36d1d8582389e8952f2baf1574d0d72935017c81eab7d8199","50c17ea8ba8b42b28295564f594713069a31c9e48fa05f3a6b623a36851b6490","00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd"):self.assertIn(sha,SRC)
  self.assertIn("SHA256.Create()",SRC)
  self.assertIn("File.ReadAllBytes(path)",SRC)
  self.assertIn("request.LoadImageIntoTexture(local)",SRC)
  self.assertNotIn("Texture2D.SetPixels(",SRC)
 def test_state_and_floor_isolation(self):
  room=SRC.split("internal sealed class G1ToxicologyRoomIconAdapter",1)[1].split("internal sealed class G1ToxicologyPrivateFloorIconAdapter",1)[0]
  floor=SRC.split("internal sealed class G1ToxicologyPrivateFloorIconAdapter",1)[1]
  self.assertIn("GetTextureAsset(assetId)",room)
  self.assertIn("locked ? approvedInactive : approvedActive",room)
  self.assertNotIn("GetTextureAsset(ActiveId) == null ||",room)
  self.assertIn("approvedFloor.GetTexture()",floor)
  self.assertIn("room.m_roomPersistentData.m_roomType.Entry.DatabaseID.ToString() != RoomId",floor)
  self.assertIn("material.mainTexture = atlas",floor)
  self.assertNotIn("sharedMaterial",floor)
  self.assertNotIn("Harmony.Patch",floor)
if __name__=="__main__":unittest.main()
