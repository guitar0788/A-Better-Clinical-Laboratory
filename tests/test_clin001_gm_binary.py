"""Synthetic binary-marker checks: no proprietary assembly bytes embedded."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1] / "tools"))
from audit_clin001_gm_binary import (inspect, GM_LABEL, GM_LOG,
                                    LEGACY_TEST_BUTTON)


def fake_cli(*names):
    # Stand-in for PE/CLI bytes; these tests do not compile or ship a DLL.
    return b"MZ" + bytes(64) + b"BSJB" + bytes(64) + b"".join(
        name.encode("utf-16-le") for name in names)


class TestGmBuiltArtifact(unittest.TestCase):
    def audit(self, data, mode):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"candidate.dll"
            path.write_bytes(data)
            return inspect(path,mode)

    def test_dev_candidate_requires_chinese_ui_and_log(self):
        out=self.audit(fake_cli(GM_LABEL, GM_LOG),"test")
        self.assertTrue(out["gm_markers_present"][GM_LABEL])

    def test_dev_candidate_rejects_gm_ui_missing(self):
        with self.assertRaisesRegex(ValueError,"missing Chinese"):
            self.audit(fake_cli(GM_LOG),"test")

    def test_release_rejects_chinese_gm(self):
        with self.assertRaisesRegex(ValueError,"prohibited debug"):
            self.audit(fake_cli(GM_LABEL,GM_LOG),"release")

    def test_release_rejects_legacy_g1_debug_spawn(self):
        with self.assertRaisesRegex(ValueError,"prohibited debug"):
            self.audit(fake_cli(LEGACY_TEST_BUTTON),"release")

    def test_release_without_debug_markers_passes(self):
        out=self.audit(fake_cli("Clinical Toxicology Laboratory"),"release")
        self.assertEqual(out["result"],"BINARY_MARKER_GATE_PASS")

    def test_malformed_binary_is_not_a_pass(self):
        with self.assertRaisesRegex(ValueError,"PE/CLI"):
            self.audit(b"not a managed assembly","test")


if __name__=="__main__":
    unittest.main(verbosity=2)
