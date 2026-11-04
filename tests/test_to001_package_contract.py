"""TO-001 offline packager safety tests; no gameplay L4 claim."""
from pathlib import Path
import hashlib
import importlib.util
import io
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools" / "assemble_to001_test_only.py"
SPEC = importlib.util.spec_from_file_location("to001_packager", PATH)
pack = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pack)
SHA = "1" * 40
MOCK_DLL = b"MZ" + b"x" * 6000


def fake_actions_artifact(path, sha=SHA, tamper=False):
    with io.BytesIO() as buf:
        with zipfile.ZipFile(buf, "w") as inner:
            for name in sorted(pack.PRECISE_BASE_FILES):
                blob = (b"" if name.endswith("0Harmony.dll")
                        else MOCK_DLL if name.endswith("ModABCLG1LeadTest.dll")
                        else b"test-only offline fixture")
                inner.writestr(name, blob)
        packed = buf.getvalue()
    declared_hash = hashlib.sha256(MOCK_DLL).hexdigest()
    if tamper:
        declared_hash = "f" * 64
    with zipfile.ZipFile(path, "w") as outer:
        outer.writestr("ABCL_G1_AutoBuilt_TestOnly.zip", packed)
        outer.writestr("BUILD_INFO.txt",
                       "G1 TEST ONLY\nCANDIDATE_SHA=" + sha +
                       "\nDLL_SHA256=" + declared_hash + "\n")


class TO001OfflinePackagingTests(unittest.TestCase):
    def test_additive_room_and_floor_assets_are_packaged(self):
        with tempfile.TemporaryDirectory() as temp:
            artifact = Path(temp) / "g1_actions.zip"
            output = Path(temp) / "to001.zip"
            fake_actions_artifact(artifact)
            pack.create(artifact, SHA, output)
            with zipfile.ZipFile(output) as outer:
                self.assertEqual(set(outer.namelist()),
                                 {"ABCL_G1_TO001_Install_TestOnly.zip", "BUILD_INFO.txt"})
                info = outer.read("BUILD_INFO.txt").decode()
                self.assertIn("TO001_FLOOR_TILE_SHA256=" + pack.FLOOR_TILE_SHA256, info)
                self.assertIn("TO001_INACTIVE_ROOM_ICON_SHA256=" + pack.ART_HASHES["toxicology_room_icon_inactive.png"], info)
                self.assertIn("TO001_FLOOR_ATLAS_SHA256=", info)
                self.assertIn("TO001_RUNTIME_L4=NOT_RUN", info)
                with zipfile.ZipFile(io.BytesIO(outer.read(
                        "ABCL_G1_TO001_Install_TestOnly.zip"))) as inner:
                    self.assertEqual(len(inner.namelist()), 15)
                    self.assertEqual(inner.read(pack.ADDON + "/ModABCLG1LeadTest.dll"), MOCK_DLL)
                    self.assertEqual(inner.read(pack.ADDON + "/0Harmony.dll"), b"")
                    for filename in pack.ART_HASHES:
                        self.assertTrue(inner.read(pack.ADDON + "/Assets/ABCL/" + filename))
                    atlas_path = pack.ADDON + "/Assets/ABCL/" + pack.FLOOR_ATLAS_NAME
                    atlas = inner.read(atlas_path)
                    aw, ah, atlas_pixels = pack.decode_png_rgba(atlas)
                    fw, fh, floor_pixels = pack.decode_png_rgba(pack.FLOOR_TILE.read_bytes())
                    self.assertEqual((aw, ah), (2048, 2048))
                    self.assertEqual((fw, fh), (128, 64))
                    for y in range(64):
                        source_start = y * 128 * 4
                        target_start = ((1472 + y) * 2048 + 1024) * 4
                        self.assertEqual(
                            atlas_pixels[target_start:target_start + 128 * 4],
                            floor_pixels[source_start:source_start + 128 * 4])
                    xml = inner.read(pack.ADDON + "/Database/ModAssetListsTO001.xml")
                    self.assertIn(b"TEXTURE_CUSTOM_SPRITE", xml)
                    self.assertIn(b"ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS", xml)
                    self.assertNotIn("Assembly-CSharp.dll", " ".join(inner.namelist()))

    def test_refuses_wrong_exact_sha_or_modified_dll(self):
        with tempfile.TemporaryDirectory() as temp:
            artifact = Path(temp) / "g1_actions.zip"
            output = Path(temp) / "to001.zip"
            fake_actions_artifact(artifact)
            with self.assertRaisesRegex(ValueError, "G1 candidate SHA"):
                pack.create(artifact, "2" * 40, output)
            fake_actions_artifact(artifact, tamper=True)
            with self.assertRaisesRegex(ValueError, "DLL digest"):
                pack.create(artifact, SHA, output)
            self.assertFalse(output.exists())

    def test_refuses_overwriting_existing_package(self):
        with tempfile.TemporaryDirectory() as temp:
            artifact = Path(temp) / "g1_actions.zip"
            output = Path(temp) / "to001.zip"
            fake_actions_artifact(artifact)
            output.write_bytes(b"protected")
            with self.assertRaisesRegex(ValueError, "Output exists"):
                pack.create(artifact, SHA, output)
            self.assertEqual(output.read_bytes(), b"protected")


if __name__ == "__main__":
    unittest.main()
