"""Source-only gate for approved, exact-room private floor atlas."""
import hashlib, importlib.util, shutil, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def mod():
    spec=importlib.util.spec_from_file_location("atlas",ROOT/"tools/build_to001_approved_floor_atlas.py")
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m
class TestApprovedPrivateAtlas(unittest.TestCase):
    def test_exact_source_identity_and_coordinates(self):
        m=mod()
        self.assertEqual(m.TILE,376)
        self.assertEqual(m.RECT,(1024,1472,1152,1536))
        self.assertEqual((m.ATLAS_W,m.ATLAS_H),(2048,2048))
        source=(ROOT/"assets/art/to001/toxicology_floor_from_approved_128x64.png").read_bytes()
        vector=(ROOT/"assets/art/to001/toxicology_floor_from_approved_256x128.svg").read_bytes()
        self.assertEqual(m.sha(source),m.SOURCE_SHA)
        self.assertEqual(m.sha(vector),m.VECTOR_SHA)
        room=(ROOT/"assets/art/to001/toxicology_room_icon.svg").read_bytes()
        self.assertEqual(hashlib.sha1(b"blob "+str(len(room)).encode()+b"\x00"+room).hexdigest(),m.ROOM_BLOB)
    def test_rejected_sources_and_live_package_absent(self):
        self.assertFalse((ROOT/"assets/art/to001/toxicology_floor_glyph.svg").exists())
        self.assertFalse((ROOT/"assets/g1/Assets/ABCL/toxicology_floor_tile_atlas.png").exists())
    def test_modified_art_fails_closed(self):
        m=mod()
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);d=r/"assets/art/to001";d.mkdir(parents=True)
            for filename in ("toxicology_floor_from_approved_128x64.png",
                             "toxicology_floor_from_approved_256x128.svg",
                             "toxicology_room_icon.svg"):
                shutil.copyfile(ROOT/"assets/art/to001"/filename,d/filename)
            target=d/"toxicology_floor_from_approved_128x64.png"
            target.write_bytes(target.read_bytes()+b"invalid")
            with self.assertRaisesRegex(ValueError,"Not the owner-approved"):
                m.build(r,r/"output")
            self.assertFalse((r/"output").exists())
if __name__=="__main__": unittest.main()
