"""Synthetic G1 room and ART001 standalone gate tests; NO original game bytes."""
import importlib.util
import tempfile
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "art001_room_gate", ROOT / "tools/audit_art001_selfstanding_room_boundaries.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

# Independent self-standing source fixture is already negatively tested.
from test_art001_selfstanding_candidate import synth, module as standalone


def element(parent, tag, value):
    ET.SubElement(parent, tag).text = str(value)


def room_fixture():
    root = ET.Element("Database")
    room = ET.SubElement(root, "GameDBRoomType", ID=gate.ROOM_ID)
    filters = ET.SubElement(room, "BuildingModeFilters")
    for tag in ("ui_lab_equipment", "ui_equipment_table", "ui_mobile_cabinet"):
        element(filters, "Tag", tag)
    tags = ET.SubElement(room, "Tags")
    for tag in (gate.PRIVATE_ROOM_TAG, "stat_lab", "lab_specialist_workspace"):
        element(tags, "Tag", tag)
    reqs = ET.SubElement(room, "RequiredEquipment")
    for key in ("ui_hematoanalyzer", "ui_ria", "thermal_cycler", "ui_pc"):
        item = ET.SubElement(reqs, "GameDBRequiredEquipment")
        element(item, "Tag", key)
        element(item, "MinCount", "1")
    return root


class IndependentART001RoomGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name)
        objects, assets, locales, data = synth()
        converted, _, _, report = standalone.transform(
            data(objects), data(assets),
            data(locales["en"]), data(locales["zh-Hans"]))
        self.assertEqual(len(report), 2)
        self.candidate = converted
        self.room = room_fixture()

    def tearDown(self):
        self.tmp.cleanup()

    def files(self):
        c = self.path / "candidate.xml"
        r = self.path / "room.xml"
        ET.ElementTree(self.candidate).write(c, encoding="utf-8")
        ET.ElementTree(self.room).write(r, encoding="utf-8")
        return c, r

    def run_gate(self):
        return gate.verify(*self.files())

    def must_reject(self, reason):
        with self.assertRaisesRegex(ValueError, reason):
            self.run_gate()

    def test_supported_generic_lab_build_menu_but_not_medical_method(self):
        result = self.run_gate()
        self.assertEqual(result["scope"], "SOURCE_ONLY_ROOM_FILTER_GATE")
        self.assertEqual(result["L4"], "NOT_RUN")
        self.assertEqual(result["clinical_assay_dispatch"],
                         "NOT_IMPLEMENTED_FOR_NEW_DEVICES")
        for o in result["devices"].values():
            self.assertEqual(o["native_room_filter_match_source"],
                             ["ui_lab_equipment"])
            self.assertFalse(o["fulfills_existing_G1_required_equipment"])
            self.assertTrue(o["may_appear_in_other_vanilla_lab_build_menus"])

    def test_original_ria_requirement_cannot_be_deleted(self):
        room = self.room.find("GameDBRoomType")
        req = room.find("RequiredEquipment")
        for x in list(req):
            if x.findtext("Tag") == "ui_ria":
                req.remove(x)
        self.must_reject("clinical equipment preconditions")

    def test_vanilla_hematoanalyzer_count_cannot_be_downgraded(self):
        room = self.room.find("GameDBRoomType")
        for x in room.findall("RequiredEquipment/GameDBRequiredEquipment"):
            if x.findtext("Tag") == "ui_hematoanalyzer":
                x.find("MinCount").text = "0"
        self.must_reject("clinical equipment preconditions")

    def test_cannot_require_new_instrument_as_g1_core_equipment_without_approval(self):
        room = self.room.find("GameDBRoomType")
        req = ET.SubElement(room.find("RequiredEquipment"), "GameDBRequiredEquipment")
        element(req, "Tag", "abcl_art001_icp_ms")
        element(req, "MinCount", "1")
        self.must_reject("unexpectedly made mandatory")

    def test_cannot_redefine_vanilla_lab_room_id(self):
        self.room.find("GameDBRoomType").set("ID", "ROOM_TYPE_HEMATOLOGY_LAB")
        self.must_reject("Unexpected G1 room")

    def test_unapproved_generic_ui_filter_deletion_is_blocked(self):
        filters = self.room.find("GameDBRoomType/BuildingModeFilters")
        for x in list(filters):
            if x.text == "ui_lab_equipment":
                filters.remove(x)
        self.must_reject("original UI laboratory-equipment category")

    def test_cannot_drop_original_stat_lab_routing(self):
        tags = self.room.find("GameDBRoomType/Tags")
        for x in list(tags):
            if x.text == "stat_lab":
                tags.remove(x)
        self.must_reject("identity/service routing")

    def test_new_machine_cannot_impersonate_hematoanalyzer(self):
        target = self.candidate.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_ICP_MS']")
        element(target.find("Tags"), "Tag", "ui_hematoanalyzer")
        self.must_reject("impersonates original clinical equipment")

    def test_device_must_retain_native_room_list_category(self):
        target = self.candidate.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_DIGESTION']")
        tags = target.find("Tags")
        for e in list(tags):
            if e.text == "ui_lab_equipment":
                tags.remove(e)
        self.must_reject("native building-category")

    def test_cannot_sneak_workbench_back_in(self):
        ET.SubElement(self.candidate, "GameDBObject", ID=standalone.WORKBENCH)
        self.must_reject("only two standalone ABCL devices")

    def test_parent_relation_cannot_be_reintroduced(self):
        obj = self.candidate.find("./GameDBObject[@ID='OBJECT_ABCL_ART001_ICP_MS']")
        obj.find("AttachedToObject").text = "true"
        self.must_reject("not a native independent indoor object")

    def test_duplicate_required_native_tags_are_rejected(self):
        room = self.room.find("GameDBRoomType")
        req = ET.SubElement(room.find("RequiredEquipment"), "GameDBRequiredEquipment")
        element(req, "Tag", "ui_ria")
        element(req, "MinCount", "1")
        self.must_reject("Duplicate/missing G1 room requirement")


if __name__ == "__main__":
    unittest.main()
