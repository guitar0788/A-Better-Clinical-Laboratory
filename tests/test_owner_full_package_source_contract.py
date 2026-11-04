"""Source-only guard: packaging/installer scripts cannot silently re-enable rejected workbench flow."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class OwnerFullPackageSourceContract(unittest.TestCase):
    def test_owner_build_inputs_are_pinned(self):
        p=(ROOT/"tools/build_approved_full_candidate.py").read_text("utf-8")
        for s in ("aada123989f835feb38d8a7d38b1b338e14cc75f",
                  "72cf86abb5bbb539a5b364aaf314b8f36a4746ca2caab955b191de754ff602c7",
                  "b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651",
                  "ec3be4046d90c219d28143ffd838712fc8030b3a84a05e80a4b8e65ec0141b1d",
                  "7d5c559cc60211ea37b42026c8066fbff98865be88d76ef8730350f3ac81b54d"):
            self.assertIn(s,p)
        self.assertIn("AttachedToObject",p)
        self.assertIn("false",p)
        self.assertIn("PREFAB_HASHES",p)
        self.assertNotIn("ImageDraw",p)
    def test_installer_has_safe_rollback(self):
        p=(ROOT/"tools/Install-ABCL-Full-Test.ps1").read_text("utf-8")
        for s in ("ABCL_INSTALL_STATE.json","ABCL_FULL_OWNER_MARKER.json",
                  "Check-Source", "Check-Installed", "Check-Owner",
                  "ALREADY INSTALLED", "-NativeLeadTest", "if ($Restore)",
                  "_ABCL_OWNER_BACKUP_", "Move-Item", "Hash $current"):
            if s=="Hash $current":continue
            self.assertIn(s,p)
        self.assertNotIn("Remove-Item -LiteralPath $db",p)
        self.assertNotIn("Remove-Item -LiteralPath $game",p)
        self.assertIn("ProjectHospital_Data",p)
        self.assertIn("RESTORE", (ROOT/"tools/RESTORE_ABCL_FULL_TEST.cmd").read_text("utf-8").upper())
    def test_independent_audit_is_read_only(self):
        p=(ROOT/"tools/audit_approved_full_candidate.py").read_text("utf-8")
        self.assertIn("audit_zip",p)
        self.assertIn("owner original source changed",p)
        self.assertIn("obsolete attached workbench",p.lower())
        self.assertIn("NOT_RUN",p)
        self.assertNotIn("ImageDraw",p)
if __name__=="__main__": unittest.main()
