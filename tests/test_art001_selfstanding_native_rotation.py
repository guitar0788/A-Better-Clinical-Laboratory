"""Native four-direction ART001 operator geometry: positive and negative fixtures."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location(
    "art001_native_rotation", ROOT/"tools/audit_art001_selfstanding_native_rotation.py")
rotation=importlib.util.module_from_spec(spec)
spec.loader.exec_module(rotation)
from test_art001_selfstanding_candidate import synth, module as candidate_module


def tag(obj, name, val):
    ET.SubElement(obj, name).text=str(val)


class NativeOperatorRotation(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/"candidate.xml"
        objects, assets, locales, encode=synth()
        self.original, _, _, _=candidate_module.transform(
            encode(objects), encode(assets),
            encode(locales["en"]), encode(locales["zh-Hans"]))
        # The shared synthetic builder assigns -0.7 to both. The reviewed
        # FA GameDB actually uses -0.65 for the digestion instrument.
        digestion=self.original.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_DIGESTION']")
        digestion.find("UseOffsetXNW").text="-0.65"
        self.refresh()

    def tearDown(self):
        self.tmp.cleanup()

    def refresh(self):
        ET.ElementTree(self.original).write(self.path,encoding="utf-8")

    def device(self,id="OBJECT_ABCL_ART001_ICP_MS"):
        return self.original.find("./GameDBObject[@ID='"+id+"']")

    def fail(self,reason):
        self.refresh()
        with self.assertRaisesRegex(ValueError,reason):
            rotation.validate(self.path)

    def test_all_four_native_positions_and_offsets(self):
        result=rotation.validate(self.path)
        self.assertEqual(result["game_L4"],"NOT_RUN")
        for info in result["objects"].values():
            self.assertEqual(info["native_access_tile_relative_to_device"],{
                "NW":[-1,0],"NE":[0,-1],"SE":[1,0],"SW":[0,1]})
            self.assertEqual(info["actual_usable_room_path"],"NOT_TESTED_L4")
        mass=result["objects"]["OBJECT_ABCL_ART001_ICP_MS"]
        self.assertEqual(mass["expected_use_offsets_from_native_OnPostLoad"],{
            "NW":[-0.7,0.0],"NE":[-0.0,-0.7],
            "SE":[0.7,-0.0],"SW":[0.0,0.7]})

    def test_missing_native_access_slot_rejected(self):
        self.device().remove(self.device().find("AccessPositions"))
        self.fail("Exactly one source operator access tile")

    def test_multi_side_unreviewed_access_slots_rejected(self):
        access=self.device().find("AccessPositions")
        n=ET.SubElement(access,"AccessPosition")
        tag(n,"m_x",1);tag(n,"m_y",0)
        self.fail("Exactly one source operator access tile")

    def test_access_on_own_floor_cell_is_forbidden(self):
        self.device().find("AccessPositions/AccessPosition/m_x").text="0"
        self.fail("Operator access differs from native")

    def test_diagonal_access_rejected(self):
        self.device().find("AccessPositions/AccessPosition/m_y").text="-1"
        self.fail("Operator access differs from native")

    def test_connected_slots_never_reused(self):
        ET.SubElement(self.device(),"ConnectedSlots")
        self.fail("Old tabletop/forced direction")

    def test_wrong_useoffset_xnw_rejected(self):
        self.device().find("UseOffsetXNW").text="0"
        self.fail("FA staff use-offset provenance changed")

    def test_conflicting_explicit_ne_offset_rejected(self):
        tag(self.device(),"UseOffsetXNE","0.3")
        self.fail("Conflicting explicit per-direction")

    def test_explicit_matching_ne_offset_is_valid(self):
        tag(self.device(),"UseOffsetXNE","0.0")
        tag(self.device(),"UseOffsetYNE","-0.7")
        self.refresh()
        self.assertEqual(rotation.validate(self.path)["game_L4"],"NOT_RUN")

    def test_reject_occupied_access_mode_remapped_as_free_slots(self):
        tag(self.device(),"AccessPositionsHaveToBeFree","true")
        self.fail("unexpectedly strict")

    def test_unapproved_atlas_direction_rejected(self):
        self.device().find("TextureIDSW").text="2"
        self.fail("atlas index mismatch")

    def test_float_not_finite_rejected(self):
        self.device().find("UseOffsetXNW").text="NaN"
        self.fail("Non-finite game-object use offset")

    def test_parent_device_cannot_sneak_back_in(self):
        self.device().find("AttachedToObject").text="true"
        self.fail("Floor-standing model")

    def test_invalid_direction_is_not_silently_mapped(self):
        with self.assertRaisesRegex(ValueError,"Unknown"):
            rotation.rotate((-1,0),"S")

if __name__=="__main__":
    unittest.main()
