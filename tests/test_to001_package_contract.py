"""TO-001 offline packager safety tests. Synthetic archives test ZIP policy only.

These tests do NOT simulate or claim Windows .NET L3 or gameplay L4.
"""
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
MOCK_DLL = b"MZ" + b"x" * 6000   # synthetic placeholder: never a real game assembly


def fake_actions_artifact(path, sha=SHA, tamper=False):
    with io.BytesIO() as buf:
        with zipfile.ZipFile(buf, "w") as inner:
            for name in sorted(pack.PRECISE_BASE_FILES):
                blob = (
                    b"" if name.endswith("0Harmony.dll")
                    else MOCK_DLL if name.endswith("ModABCLG1LeadTest.dll")
                    else b"test-only offline fixture"
                )
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
    def test_additive_expected_assets_and_preserved_core_files(self):
        with tempfile.TemporaryDirectory() as temp:
            artifact = Path(temp) / "g1_actions.zip"
            output = Path(temp) / "to001.zip"
            fake_actions_artifact(artifact)
            pack.create(artifact, SHA, output)
            with zipfile.ZipFile(output) as outer:
                self.assertEqual(set(outer.namelist()),
                                 {"ABCL_G1_TO001_Install_TestOnly.zip", "BUILD_INFO.txt"})
                self.assertIn("TO001_RUNTIME_L4=NOT_RUN",
                              outer.read("BUILD_INFO.txt").decode())
                with zipfile.ZipFile(io.BytesIO(outer.read(
                        "ABCL_G1_TO001_Install_TestOnly.zip"))) as inner:
                    self.assertEqual(len(inner.namelist()), 14)
                    self.assertEqual(inner.read(pack.ADDON + "/ModABCLG1LeadTest.dll"), MOCK_DLL)
                    self.assertEqual(inner.read(pack.ADDON + "/0Harmony.dll"), b"")
                    for filename in pack.ART_HASHES:
                        self.assertTrue(inner.read(pack.ADDON + "/Assets/ABCL/" + filename))
                    self.assertIn(b"TEXTURE_CUSTOM_SPRITE",
                                  inner.read(pack.ADDON + "/Database/ModAssetListsTO001.xml"))
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
