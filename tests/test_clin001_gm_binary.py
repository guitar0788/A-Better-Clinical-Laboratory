"""Synthetic binary checks: retired GM markers must be absent from current G1 DLL."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from audit_clin001_gm_binary import inspect, GM_LABEL, GM_LOG, C1_ID, R3_TEST_MARKERS

def fake_cli(*names):
    return b"MZ" + bytes(64) + b"BSJB" + bytes(64) + b"".join(
        name.encode("utf-16-le") for name in names)

class TestRetiredGmArtifact(unittest.TestCase):
    def audit(self, data, mode="test"):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "candidate.dll"
            path.write_bytes(data)
            return inspect(path, mode)

    def test_test_candidate_rejects_super_gm_and_c1(self):
        for marker in (GM_LABEL, GM_LOG, C1_ID, "ForceMobilePatient"):
            with self.subTest(marker=marker):
                with self.assertRaisesRegex(ValueError, "Retired C1/Super-GM"):
                    self.audit(fake_cli(marker))

    def test_test_candidate_allows_only_native_r3_test_control(self):
        out = self.audit(fake_cli(*R3_TEST_MARKERS))
        self.assertEqual(out["result"], "RETIRED_GM_MARKER_GATE_PASS")
        self.assertFalse(any(out["retired_gm_markers_present"].values()))

    def test_release_rejects_native_r3_test_controls(self):
        with self.assertRaisesRegex(ValueError, "native R3 test controls"):
            self.audit(fake_cli(*R3_TEST_MARKERS), "release")

    def test_release_without_debug_markers_passes(self):
        out = self.audit(fake_cli("Clinical Toxicology Laboratory"), "release")
        self.assertEqual(out["result"], "RETIRED_GM_MARKER_GATE_PASS")

    def test_malformed_binary_is_not_a_pass(self):
        with self.assertRaisesRegex(ValueError, "PE/CLI"):
            self.audit(b"not a managed assembly")

if __name__ == "__main__":
    unittest.main(verbosity=2)
