"""R6 log regression: confirmed G1 loads, native icon preflight rejects one asset."""
from pathlib import Path
import unittest
SRC=(Path(__file__).resolve().parents[1]/"src/ABCLG1Panel.cs").read_text("utf-8")
class PrivateArt(unittest.TestCase):
 def test_exact_source_pins(self):
  for sha in ("c2c6c83cb0f8c2ca49dce7184bdd4f71df1c71a20ecf0c38e05337df6a48f62b","eb37ce261299f7df2ac87c61272168f71b5faca5de1578b71a172a8d75e861eb","00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd"):self.assertIn(sha,SRC)
  self.assertIn("SHA256.Create()",SRC)
  self.assertIn("File.ReadAllBytes(path)",SRC)
  self.assertIn("loadImage.Invoke(request",SRC)
  self.assertIn('Assembly.Load("UnityEngine.UnityWebRequestWWWModule")',SRC)
  self.assertNotIn("new WWW(",SRC)
  self.assertNotIn("Texture2D.SetPixels(",SRC)
 def test_state_and_floor_isolation(self):
  room=SRC.split("internal sealed class G1ToxicologyRoomIconAdapter",1)[1].split("internal sealed class G1ToxicologyPrivateFloorIconAdapter",1)[0]
  floor=SRC.split("internal sealed class G1ToxicologyPrivateFloorIconAdapter",1)[1]
  self.assertIn("GetTextureAsset(assetId)",room)
  self.assertIn('GetField("m_customIconSprites"',room)
  self.assertIn("nativeCache.TryGetValue(assetId, out sprite)",room)
  self.assertIn("IconRegistered=",room)
  self.assertIn("locked ? approvedInactive : approvedActive",room)
  self.assertNotIn("GetTextureAsset(ActiveId) == null ||",room)
  self.assertIn("approvedFloor.GetTexture()",floor)
  self.assertIn("room.m_roomPersistentData.m_roomType.Entry.DatabaseID.ToString() != RoomId",floor)
  self.assertIn("material.mainTexture = atlas",floor)
  self.assertNotIn("sharedMaterial.mainTexture =",floor)
  self.assertNotIn("Harmony.Patch",floor)
if __name__=="__main__":unittest.main()
