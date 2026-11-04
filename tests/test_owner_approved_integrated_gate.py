"""Offline negative regression tests for the approved-asset package gate."""
import importlib.util
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("owner_gate",
    ROOT/"tools/verify_abcl_owner_integrated.py")
gate=importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def make_objects(standing=True, bench=False):
    root=ET.Element("Database")
    for name, slots in gate.DEVICES.items():
        obj=ET.SubElement(root,"GameDBObject",ID=name)
        ET.SubElement(obj,"AttachedToObject").text=("false" if standing else "true")
        ET.SubElement(obj,"Placement").text="INDOORS"
        ET.SubElement(obj,"TextureRef").text="ASSET_TEX_ABCL_ART001_EQUIPMENT"
        ET.SubElement(obj,"TextureAtlasLayout").text="LAYOUT_16_X_8"
        ET.SubElement(obj,"SpriteShape").text="SHAPE_1_X_1"
        ET.SubElement(obj,"AccessPositions")
        for d,i in zip(("NW","NE","SE","SW"),slots):
            ET.SubElement(obj,"TextureID"+d).text=str(i)
        tags=ET.SubElement(obj,"Tags")
        ET.SubElement(tags,"Tag").text=name.lower()
    if bench:
        ET.SubElement(root,"GameDBObject",ID="OBJECT_ABCL_ART001_WORKBENCH")
    return ET.tostring(root)


class OwnerApprovedPackageGate(unittest.TestCase):
    def test_correct_standalone_objects_accept_without_art_repainting(self):
        gate.verify_device_xml(make_objects())

    def test_rejects_old_tabletop_attached_objects(self):
        with self.assertRaisesRegex(ValueError,"independent floor-standing"):
            gate.verify_device_xml(make_objects(standing=False))

    def test_rejects_obsolete_workbench_reintroduced(self):
        with self.assertRaisesRegex(ValueError,"workbench"):
            gate.verify_device_xml(make_objects(bench=True))

    def test_rejects_native_tag_collision(self):
        node=ET.fromstring(make_objects())
        tags=node.find("./GameDBObject/Tags")
        ET.SubElement(tags,"Tag").text="ui_hematoanalyzer"
        with self.assertRaisesRegex(ValueError,"vanilla clinical tag"):
            gate.verify_device_xml(ET.tostring(node))

    def test_approved_art_hash_contract_has_no_legacy_atlas(self):
        self.assertEqual(gate.APPROVED[gate.ART+"Assets/ABCL/equipment_atlas.png"],
          "b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651")
        self.assertEqual(len(gate.APPROVED),8)
        self.assertNotIn("OBJECT_ABCL_ART001_WORKBENCH",gate.DEVICES)

    def test_does_not_edit_bytes(self):
        import inspect
        source=inspect.getsource(gate)
        self.assertNotIn("ImageDraw",source)
        self.assertNotIn("resize(",source)
        self.assertNotIn("save(",source)
        self.assertNotIn("Copy-Item",source)


if __name__=="__main__":
    unittest.main()
