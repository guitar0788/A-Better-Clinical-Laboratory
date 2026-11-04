"""Offline negative/positive regression for an exact owner R3 UTF-8 wrapper patch."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from patch_integrated_r3_utf8 import patch_entries, rebuild, PACKAGE_ID

def h(x):
    return hashlib.sha256(x).hexdigest()

def fixture():
    installer=b"$M=Get-Content -LiteralPath $Manifest -Raw | ConvertFrom-Json\n[xml]$Strings=Get-Content -LiteralPath $LangFile -Raw\n"
    restore=b"$R=Get-Content -LiteralPath $Receipt -Raw | ConvertFrom-Json\n[xml]$OldXml=Get-Content -LiteralPath $OldAddon -Raw\n"
    files={
        "Install-ABCL-Integrated.ps1":installer,
        "Restore-ABCL-Previous.ps1":restore,
        "ModABCLG1LeadTest/0Harmony.dll":b"",
        "ModABCLG1LeadTest/ModABCLG1LeadTest.dll":b"TEST_ONLY_ABCL_COMPILER_FIXTURE_NOT_AN_EXECUTABLE",
    }
    for i in range(24):
        name=f"ModABCLG1LeadTest/Assets/mock_{i:02d}.bin"
        files[name]=bytes([i])*20
    files["ModABCLG1LeadTest/Assets/mock_00.bin"]=b"\xe4\xb8\xb4\xe5\xba\x8a\xe6\xaf\x92\xe7\x90\x86\xe5\xae\x9e\xe9\xaa\x8c\xe5\xae\xa4"
    compiled="a"*40
    m={
        "package":PACKAGE_ID,
        "G1_compiled_build":{
            "genuine_net35_CLR2":True,
            "commit":compiled,
            "candidate_sha":compiled,
            "dll_sha256":h(files["ModABCLG1LeadTest/ModABCLG1LeadTest.dll"]),
        },
        "file_receipts":{
            name:{"bytes":len(data),"sha256":h(data),"source":"synthetic unit only"}
            for name,data in files.items()
        },
    }
    files["PACKAGE_MANIFEST.json"]=(json.dumps(m,ensure_ascii=False)+"\n").encode()
    return files

class UTF8FixTests(unittest.TestCase):
    def test_patches_only_two_scripts_and_manifest(self):
        old=fixture()
        new=patch_entries(old)
        changed={n for n in old if old[n]!=new[n]}
        self.assertEqual(changed,{"PACKAGE_MANIFEST.json","Install-ABCL-Integrated.ps1","Restore-ABCL-Previous.ps1"})
        for n in (x for x in old if x.startswith("ModABCLG1LeadTest/")):
            self.assertEqual(old[n],new[n])
        for n in ("Install-ABCL-Integrated.ps1","Restore-ABCL-Previous.ps1"):
            self.assertNotIn("Get-Content -LiteralPath $LangFile -Raw",new[n].decode())
            self.assertIn("-Encoding UTF8 -Raw",new[n].decode())
            self.assertEqual(old[n].count(b"Get-Content"),new[n].count(b"Get-Content"))
        m=json.loads(new["PACKAGE_MANIFEST.json"].decode("utf-8"))
        self.assertEqual(m["package"],PACKAGE_ID)
        for n,r in m["file_receipts"].items():
            self.assertEqual((r["bytes"],r["sha256"]),(len(new[n]),h(new[n])))

    def test_refuses_replacing_unrecognized_binary_data(self):
        src=fixture()
        src["ModABCLG1LeadTest/ModABCLG1LeadTest.dll"]=b"tampered"
        with self.assertRaisesRegex(ValueError,"G1 DLL digest mismatch"):
            patch_entries(src)

    def test_rejects_managed_content_tampering(self):
        src=fixture()
        src["ModABCLG1LeadTest/Assets/mock_01.bin"]=b"changed"
        with self.assertRaisesRegex(ValueError,"SHA verification"):
            patch_entries(src)

    def test_refuses_existing_output_or_unknown_zip(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"unknown.zip"
            q=Path(t)/"out.zip"
            p.write_bytes(b"not a reviewed zip")
            with self.assertRaisesRegex(ValueError,"Unreviewed input"):
                rebuild(p,q)
            self.assertFalse(q.exists())
            q.write_bytes(b"protected")
            with self.assertRaisesRegex(ValueError,"Refuse overwriting"):
                rebuild(p,q)
            self.assertEqual(q.read_bytes(),b"protected")

    def test_rejects_wrong_package_identity(self):
        src=fixture()
        m=json.loads(src["PACKAGE_MANIFEST.json"])
        m["package"]="not ABCL"
        src["PACKAGE_MANIFEST.json"]=json.dumps(m).encode()
        with self.assertRaisesRegex(ValueError,"Unknown integrated test package"):
            patch_entries(src)

if __name__=="__main__":
    unittest.main()
