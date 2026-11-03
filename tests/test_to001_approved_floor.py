"""TO-001 exact projected-floor visual asset: pure stdlib contract (no L3/L4)."""
import hashlib
from pathlib import Path
import struct
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "assets/art/to001/toxicology_room_icon.svg"
DERIVED = ROOT / "assets/art/to001/toxicology_floor_from_approved_256x128.svg"
PNG = ROOT / "assets/art/to001/toxicology_floor_from_approved_128x64.png"
NS = "{http://www.w3.org/2000/svg}"
EXPECTED = {
    "room_blob": "c4a81670a2b0004799513c5b03a61b9239af1f5b",
    "floor_svg": "76995aef9bb3eb851c28101d0b75200552bc85e91dc28247ebd0e786e6cab4ec",
    "floor_png": "7c0d03ddbd370aca4ddd1a089ff91d814e1c2622659a3d300d844bd9713a8cb4",
}

class ApprovedFloorGlyphTests(unittest.TestCase):
    def test_is_exact_original_flask_geometry_only(self):
        data = SRC.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()
        self.assertEqual(blob, EXPECTED["room_blob"])
        self.assertEqual(hashlib.sha256(DERIVED.read_bytes()).hexdigest(), EXPECTED["floor_svg"])
        original = ET.fromstring(data)
        derived = ET.parse(DERIVED).getroot()
        self.assertEqual(derived.get("viewBox"), "0 0 256 128")
        source_groups = [x for x in original if x.tag == NS+"g"]
        target = [x for x in derived if x.tag == NS+"g"]
        self.assertEqual(len(source_groups), 2)
        self.assertEqual(len(target), 1)
        self.assertEqual(target[0].get("transform"), "matrix(3.3 1.2 -2.3 0.75 96 1.6)")
        self.assertEqual(len(list(target[0])), 2)
        for old, new in zip(source_groups, list(target[0])):
            self.assertEqual(ET.tostring(old), ET.tostring(new))

    def test_private_png_exact_and_no_bad_prior_art(self):
        data = PNG.read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), EXPECTED["floor_png"])
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(struct.unpack(">II", data[16:24]), (128,64))
        self.assertEqual(data[25], 6)  # PNG true-color RGBA
        self.assertFalse((ROOT/"assets/art/to001/toxicology_floor_glyph.svg").exists())

if __name__ == "__main__":
    unittest.main()
