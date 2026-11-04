"""R13 fail-closed bundle gate: reject R12 and earlier until genuine L3."""
from pathlib import Path
import importlib.util, unittest
ROOT=Path(__file__).resolve().parents[1]
SOURCE="9511fc9da495c0c015f383c4950666bff776176e"
DLL=None  # No genuine R13 Windows compiler evidence recorded yet
STALE=[
 ("62450307ae36b5104f3a3634d0612592f743afff","15aef1736dfd70f34d9fede073140360c754f5c7d9d10eac3639e54d78012f9c"),
 ("80fed52f7d474fce9e7029567b7f81571d7d6905","4bc02a4c3d1ee161e712e8119b97f5aaabde1d94ac74ccccf86f712dbee5afc8"),
 ("991657743adde647e3249a4815e2b642c9d84490","653086e366ef818277cf66970bfb7e3ba22d9970ca07dc5febd61b3c9ecdc7a2"),
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
   self.assertIn("EXPECTED_DLL=None",data)
   for old_sha,old_dll in STALE:
    self.assertNotIn(old_sha,data)
    self.assertNotIn(old_dll,data)
 def test_previous_binaries_fail_source_gate(self):
  path=ROOT/"tests/audit_complete_bundle.py"
  spec=importlib.util.spec_from_file_location("exact_audit",path)
  audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
  self.assertEqual(audit.EXPECTED_SOURCE,SOURCE)
  self.assertEqual(audit.EXPECTED_DLL,DLL)
  self.assertIsNone(audit.EXPECTED_DLL)
  for old_sha,old_dll in STALE:
   with self.assertRaises(ValueError):
    audit.audit_bytes({"BUILD_INFO.json":(
     '{"compiled_g1_source_sha":"'+old_sha+'","dll_sha256":"'+old_dll+'"}'
     ).encode("utf-8")})
 def test_artwork_sha_pins_never_changed(self):
  s=(ROOT/"tests/audit_complete_bundle.py").read_text("utf-8")
  for sha in (
   "c2c6c83cb0f8c2ca49dce7184bdd4f71df1c71a20ecf0c38e05337df6a48f62b",
   "eb37ce261299f7df2ac87c61272168f71b5faca5de1578b71a172a8d75e861eb",
   "00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd",
   "b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651"):
   self.assertIn(sha,s)
if __name__=="__main__":unittest.main()
