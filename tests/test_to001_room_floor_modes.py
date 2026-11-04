"""TO-001 native RoomRenderer view-mode contract (L2; owner L4 pending).

The original RoomRenderer.RenderRooms draws glyphs in BUILDING, BUILDING_FLOORS
and LOGISTICS (only game/no-walls/doctor modes are excluded).
"""
from pathlib import Path
import unittest
S=(Path(__file__).resolve().parents[1]/"src/ABCLG1Panel.cs").read_text(encoding="utf-8")
F=S.split("internal sealed class G1ToxicologyPrivateFloorIconAdapter",1)[1]

class FloorViewModes(unittest.TestCase):
 def test_all_vanilla_room_overlay_modes_included(self):
  for mode in ("BUILDING","BUILDING_FLOORS","LOGISTICS"):
   self.assertIn("roomView != ViewModes."+mode,F)
  self.assertIn("does not display room glyphs",F)
  self.assertNotIn("m_currentMode != ViewModes.LOGISTICS",F)

 def test_game_modes_fail_closed_and_do_not_touch_shared_atlas(self):
  self.assertIn("RestoreOwned();",F)
  self.assertIn("room.m_roomPersistentData.m_roomType.Entry.DatabaseID.ToString() != RoomId",F)
  self.assertIn("material.mainTexture = atlas;",F)
  self.assertNotIn("sharedMaterial.mainTexture =",F)
  self.assertNotIn("Harmony.Patch",F)

 def test_owner_original_tile_and_compiled_abi_unchanged(self):
  self.assertIn("00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd",F)
  self.assertIn("2048, 2048",F)
  self.assertIn("Texture previouslyOwnedAtlas = privateAtlas;",F)
  self.assertIn("private readonly Dictionary<Renderer, Texture> owned",F)

if __name__=="__main__":
 unittest.main()
