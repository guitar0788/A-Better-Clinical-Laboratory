"""ART-001 FA exact-source integration contract; no game DLL, no installer."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
F = ROOT / "tools" / "stage_art001_fa_submitted_standalone.py"
spec=importlib.util.spec_from_file_location("abcl_fa_join",F)
join=importlib.util.module_from_spec(spec)
spec.loader.exec_module(join)

try:
    from PIL import Image
except ImportError:
    Image=None


class FAIntegrationSourceTests(unittest.TestCase):
    def test_exact_approved_submit_snapshot_and_art_hashes(self):
        self.assertEqual(join.FA_SHA,"cb3a7ab5d03e8677dcb84f486a04bf0ea5f8f622")
        self.assertEqual(join.ATLAS_SHA,
                         "b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651")
        self.assertEqual(len(join.EXPECTED_SHEETS),2)
        self.assertEqual(len(join.DIRECTIONS),4)

    def test_native_atlas_and_no_dangerous_source_mutations(self):
        script=F.read_text("utf-8")
        for required in ("old.transform(","shutil.copyfile","original_FA_manifest_hashes_verified",
                         "derived_icons_owner_visual_approval","independent_game_L4",
                         "G1_source_or_DLL_modified","NOT_INSTALLABLE"):
            self.assertIn(required,script)
        self.assertNotIn("Overwrite-G1",script)
        self.assertNotIn("0Harmony.dll",script)
        self.assertNotIn("Assembly-CSharp.dll",script)
        self.assertNotIn("TRT_",script)
        self.assertTrue(join.is_under_game(Path("/p/StreamingAssets/Addons/new")))
        self.assertFalse(join.is_under_game(Path("/tmp/art001/fa_staging")))

    def test_frozen_nonproduction_manifest_gate_name(self):
        self.assertEqual(str(join.FA_REL),"assets/art001/review_20261103")

    @unittest.skipUnless(Image is not None, "Pillow runs on ART-only CI, not baseline Verify")
    def test_copy_approved_rgba_atlas_and_derive_only_icons(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            fa=root/"fa"
            source=fa/join.FA_REL
            (source/"frames").mkdir(parents=True)
            from hashlib import sha256
            # Source-like 16x8 alpha images for pure geometry test. Never
            # uploads this fixture or pretends these are original FA sprites.
            atlas=Image.new("RGBA",(2048,1024),(0,0,0,0))
            for i,(device,direction) in enumerate(
                ( (d,r) for d in join.DEVICE_NAMES for r in join.DIRECTIONS )
            ):
                rgba=(220-i*3,170+i*4,140,240)
                tile=Image.new("RGBA",(128,128),(0,0,0,0))
                for x in range(30,90):
                    for y in range(25,105):
                        tile.putpixel((x,y),rgba)
                tile.save(source/"frames"/f"{device}_{direction}.png")
                atlas.alpha_composite(tile,(128*i,0))
            # Dependency-only logic can consume the same fake immutable bytes;
            # never test against approved hash via monkeypatch for production.
            atlas.save(source/"diagnostic_equipment_atlas.png")
            orig=join.ATLAS_SHA
            try:
                join.ATLAS_SHA=sha256((source/"diagnostic_equipment_atlas.png").read_bytes()).hexdigest()
                output=root/"output"
                data=join.analyze_and_derive_icons(fa,output)
                self.assertEqual(data["atlas"],join.ATLAS_SHA)
                self.assertEqual(len(data["submitted_frames"]),8)
                self.assertEqual(data["derived_icons_owner_visual_approval"],
                                 "NOT_REQUESTED_OR_GRANTED")
                self.assertEqual((output/"Assets/ABCL/equipment_atlas.png").read_bytes(),
                                 (source/"diagnostic_equipment_atlas.png").read_bytes())
                for filename in ("icp_ms_icon.png","digestion_station_icon.png"):
                    with Image.open(output/"Assets/ABCL"/filename) as im:
                        self.assertEqual(im.size,(64,64))
                        self.assertEqual(im.mode,"RGBA")
            finally:
                join.ATLAS_SHA=orig


if __name__=="__main__":
    unittest.main()
