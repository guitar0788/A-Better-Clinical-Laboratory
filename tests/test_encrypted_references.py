"""Validate the encrypted G1 reference envelope if a candidate opts in to storing it."""
import hashlib
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ENCRYPTED = ROOT / "ABCL_G1_refs.aes"
SHA256 = "918A1E3FC74AD530AF070C012BB8075DBC3874438FE5BA3C96A8D8AD39A3FCE2"


class EncryptedInputChecks(unittest.TestCase):
    def test_optional_g1_ciphertext_has_expected_exact_hash(self):
        if not ENCRYPTED.exists():
            self.skipTest("Encrypted G1 build input not yet uploaded to this commit.")
        data = ENCRYPTED.read_bytes()
        self.assertGreater(len(data), 36)
        self.assertLess(len(data), 8 * 1024 * 1024)
        self.assertEqual(data[:8], b"ABCLREF1")
        self.assertEqual(hashlib.sha256(data).hexdigest().upper(), SHA256)

    def test_no_key_material_in_repository(self):
        self.assertFalse((ROOT / "ABCL_G1_AES256_GitHub_Secret.txt").exists())
        self.assertFalse((ROOT / "ABCL_G1_Private_Game_References_DoNotPublish.zip").exists())


if __name__ == "__main__":
    unittest.main()
