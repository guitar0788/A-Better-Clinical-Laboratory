"""R7 source-integrity regression: both independent package gates reject R6."""
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
EXPECTED_SOURCE="a0e5330d7317acb522ed76086817171edcaf5912"
EXPECTED_DLL="605b27bfb2ed5865217c97bb5d083a6e062a8d8d37f157e119418ac4519c5e73"
REJECTED_SOURCE="aada123989f835feb38d8a7d38b1b338e14cc75f"
REJECTED_DLL="72cf86abb5bbb539a5b364aaf314b8f36a4746ca2caab955b191de754ff602c7"

class R7ExactSourceGate(unittest.TestCase):
 def test_builder_and_independent_auditor_agree(self):
  for p in ("tools/build_approved_full_candidate.py","tests/audit_complete_bundle.py"):
   s=(ROOT/p).read_text("utf-8")
   self.assertIn(EXPECTED_SOURCE,s,p)
   self.assertIn(EXPECTED_DLL,s,p)
   self.assertNotIn(REJECTED_SOURCE,s,p)
   self.assertNotIn(REJECTED_DLL,s,p)
 def test_old_r6_is_explicitly_rejected(self):
  p=ROOT/"tests/audit_complete_bundle.py"
  spec=importlib.util.spec_from_file_location("r7_audit",p)
  m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  self.assertEqual(m.EXPECTED_SOURCE,EXPECTED_SOURCE)
  self.assertEqual(m.EXPECTED_DLL,EXPECTED_DLL)
  with self.assertRaisesRegex(ValueError,"stale compiled G1 source"):
   m.audit_bytes({"BUILD_INFO.json":b'{"compiled_g1_source_sha":"'+REJECTED_SOURCE.encode()+b'"}'})
 def test_owner_art_pins_unchanged(self):
  s=(ROOT/"tests/audit_complete_bundle.py").read_text("utf-8")
  self.assertIn("225b2918c448b5d36d1d8582389e8952f2baf1574d0d72935017c81eab7d8199",s)
  self.assertIn("00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd",s)
  self.assertIn("b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651",s)
if __name__=="__main__":unittest.main()
