"""Exact ABCL full-bundle source gate: R10 verified net35, reject R6/R7/R8."""
from pathlib import Path
import importlib.util, unittest
ROOT=Path(__file__).resolve().parents[1]
SOURCE="991657743adde647e3249a4815e2b642c9d84490"
DLL="653086e366ef818277cf66970bfb7e3ba22d9970ca07dc5febd61b3c9ecdc7a2"
STALE=[
 ("9ae13683b63fa849582a72c62b9509c0eb65fe5d","a096ecfcbeabf49b9cfdae15152cfc46ffa1c3095a8b3ebc75eaa1f743215755"),
 ("d73b2302b896c8cf58c3230ddaa5663e02285b53","51e4bb2c49a550c591f5908dbe765409a9a2a86d0e664421059840525804ef8b"),
 ("a0e5330d7317acb522ed76086817171edcaf5912","605b27bfb2ed5865217c97bb5d083a6e062a8d8d37f157e119418ac4519c5e73"),
 ("aada123989f835feb38d8a7d38b1b338e14cc75f","72cf86abb5bbb539a5b364aaf314b8f36a4746ca2caab955b191de754ff602c7"),
]
class CurrentSourceGate(unittest.TestCase):
 def test_compiler_and_two_independent_package_gates_agree(self):
  for p in ("tools/build_approved_full_candidate.py","tests/audit_complete_bundle.py"):
   data=(ROOT/p).read_text("utf-8")
   self.assertIn(SOURCE,data)
   self.assertIn(DLL,data)
   for old_sha,old_dll in STALE:
    self.assertNotIn(old_sha,data)
    self.assertNotIn(old_dll,data)
 def test_previous_binaries_fail_source_gate(self):
  path=ROOT/"tests/audit_complete_bundle.py"
  spec=importlib.util.spec_from_file_location("exact_audit",path)
  audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
  self.assertEqual(audit.EXPECTED_SOURCE,SOURCE)
  self.assertEqual(audit.EXPECTED_DLL,DLL)
  for old_sha,old_dll in STALE:
   with self.assertRaises(ValueError):
    audit.audit_bytes({"BUILD_INFO.json":(
     '{"compiled_g1_source_sha":"'+old_sha+'","dll_sha256":"'+old_dll+'"}'
     ).encode("utf-8")})
 def test_artwork_sha_pins_never_changed(self):
  s=(ROOT/"tests/audit_complete_bundle.py").read_text("utf-8")
  for sha in (
   "225b2918c448b5d36d1d8582389e8952f2baf1574d0d72935017c81eab7d8199",
   "50c17ea8ba8b42b28295564f594713069a31c9e48fa05f3a6b623a36851b6490",
   "00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd",
   "b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651"):
   self.assertIn(sha,s)
if __name__=="__main__":unittest.main()
