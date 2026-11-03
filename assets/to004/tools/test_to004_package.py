"""TO004 checks include the native-safe test-overlay assembly and source-only guarantees."""
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from package_to004 import build

class PackageCheck(unittest.TestCase):
    def test_can_build_package_and_verify_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'candidate.zip'
            result=build(out,'a'*40)
            self.assertEqual(result['runtime'],8)
            self.assertEqual(result['files'],14)
            self.assertTrue(out.is_file())
            with self.assertRaises(ValueError):build(out,'a'*40)
    def test_missing_or_bad_source_sha(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):build(Path(tmp)/'package.zip','G1')

if __name__=='__main__': unittest.main(verbosity=2)