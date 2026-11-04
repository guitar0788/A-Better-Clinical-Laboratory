"""Project Hospital native code loader requires a genuine Harmony1 file in each code addon."""
from pathlib import Path
import importlib.util, unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("native_bundle",ROOT/"tests/audit_complete_bundle.py")
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class LoaderContract(unittest.TestCase):
    def test_missing_loader_is_fatal(self):
        with self.assertRaisesRegex(ValueError,"skip G1 code"):
            mod.validate_native_loader({})
    def test_empty_marker_is_fatal(self):
        with self.assertRaisesRegex(ValueError,"official nonempty"):
            mod.validate_native_loader({mod.G1+"0Harmony.dll":b""})
    def test_untrusted_fake_assembly_is_fatal(self):
        with self.assertRaisesRegex(ValueError,"official nonempty"):
            mod.validate_native_loader({mod.G1+"0Harmony.dll":b"MZ"+b"BSJB"+b"HarmonyInstance"+b"0"*20000})
    def test_packager_has_no_silent_skip(self):
        s=(ROOT/"tools/build_approved_full_candidate.py").read_text("utf-8")
        self.assertIn("HARMONY1_SHA=",s)
        self.assertIn("--harmony-dll",s)
        self.assertIn("files[G1+'0Harmony.dll']=real_harmony",s)
        self.assertNotIn("0Harmony.dll' not in files",s)
    def test_license_recorded(self):
        s=(ROOT/"third_party/Harmony-1.2.0.1-LICENSE.txt").read_text("utf-8")
        self.assertIn("Copyright (c) 2017 Andreas Pardeike",s)
if __name__=="__main__":unittest.main()
