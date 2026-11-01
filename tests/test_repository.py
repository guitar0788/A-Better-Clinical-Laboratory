"""Real repository-level checks; these do not test Project Hospital gameplay."""
from pathlib import Path
import re
import subprocess
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md",
    "CONTRIBUTING.md",
    "docs/MASTER_PLAN.md",
    "docs/DECISIONS.md",
    "docs/TEST_EVIDENCE.md",
    "docs/RELEASE_POLICY.md",
    ".github/workflows/verify.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/scoped-task.yml",
)
PROPRIETARY_NAMES = {
    "assembly-csharp.dll", "unityengine.dll", "unityengine.coremodule.dll",
    "unityengine.ui.dll", "0harmony.dll"
}
FORBIDDEN_EXTENSIONS = {".dll", ".exe", ".pdb", ".mdb", ".zip", ".7z", ".rar", ".nupkg", ".snupkg"}


def tracked_files():
    completed = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z"],
        capture_output=True, check=True,
    )
    return [ROOT / Path(p.decode("utf-8")) for p in completed.stdout.split(b"\x00") if p]


class RepositoryChecks(unittest.TestCase):
    def test_governance_documents_are_present_and_substantial(self):
        for relative_path in REQUIRED:
            path = ROOT / relative_path
            with self.subTest(file=relative_path):
                self.assertTrue(path.is_file(), "Required governance/CI file missing")
                self.assertGreater(len(path.read_text(encoding="utf-8").strip()), 80)

    def test_plan_tracks_g0_and_g1_separately(self):
        plan = (ROOT / "docs/MASTER_PLAN.md").read_text(encoding="utf-8")
        self.assertIn("G0-001", plan)
        self.assertIn("G1-001", plan)
        self.assertIn("Blocked", plan)
        self.assertIn("two calendar months", plan)

    def test_evidence_does_not_claim_g1_gameplay_pass(self):
        evidence = (ROOT / "docs/TEST_EVIDENCE.md").read_text(encoding="utf-8")
        self.assertIn("NOT TESTED / BLOCKED", evidence)
        self.assertIn("L4", evidence)
        self.assertIn("No public upload", evidence)

    def test_no_proprietary_or_compiled_binary_is_committed(self):
        for path in tracked_files():
            rel = path.relative_to(ROOT).as_posix()
            with self.subTest(file=rel):
                self.assertNotIn(path.name.lower(), PROPRIETARY_NAMES)
                self.assertNotIn(path.suffix.lower(), FORBIDDEN_EXTENSIONS)
                self.assertFalse(rel.startswith(("GameReferences/", "GameManaged/", "LocalGame/")))

    def test_tracked_xml_is_well_formed(self):
        xml_files = [p for p in tracked_files() if p.suffix.lower() == ".xml"]
        for path in xml_files:
            with self.subTest(file=str(path.relative_to(ROOT))):
                ET.parse(path)
        print(f"XML files parsed: {len(xml_files)} (zero means no medical XML has been checked).")

    def test_release_keeps_debug_out(self):
        release = (ROOT / "docs/RELEASE_POLICY.md").read_text(encoding="utf-8").lower()
        self.assertIn("debug patient spawning", release)
        self.assertIn("safe uninstallation is not presumed", release)


if __name__ == "__main__":
    unittest.main()
