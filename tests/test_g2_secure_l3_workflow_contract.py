"""Static guard for reviewed protected-main G2 L3 workflow.

This is not a live secrets test or game L3 certification. It ensures no
accidental broadening of the owner-only trusted workflow during review.
"""
from pathlib import Path
import unittest

WORKFLOW = (Path(__file__).resolve().parents[1] / ".github" /
            "workflows" / "auto-build-g2-private-gm-verified.yml")


class G2TrustedBuildWorkflowContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")

    def test_no_untrusted_direct_secrets_trigger(self):
        src = self.source
        self.assertIn("workflow_run:", src)
        self.assertIn("workflows: [Verify]", src)
        self.assertIn("types: [completed]", src)
        self.assertIn("github.event.workflow_run.conclusion == 'success'", src)
        self.assertIn("github.event.workflow_run.event == 'pull_request'", src)
        self.assertIn("github.event.workflow_run.actor.login == 'guitar0788'", src)
        for forbidden in ("pull_request_target:", "repository_dispatch:",
                          "secrets: write", "contents: write",
                          "workflow_dispatch:"):
            self.assertNotIn(forbidden, src)

    def test_exact_branch_and_current_g1_dependency(self):
        src = self.source
        for required in (
            "feature/ts-g2-private-gm-dispatch",
            "pulls/45",
            "pulls/7",
            "$pr.head.sha -ne $env:EVENT_SHA",
            "$g1.head.sha -ne $pr.base.sha",
            "if ($files.Count -ne $pr.changed_files)",
            "src/ABCLG1Panel.cs",
            "tests/test_g1_contract.py",
            "tests/test_g2_private_gm_dispatch.py",
            "docs/G2_PRIVATE_GM_DISPATCH_GATE.md",
        ):
            self.assertIn(required, src)

    def test_inert_compiler_inputs_and_no_original_binaries_in_artifact(self):
        src = self.source
        for required in (
            "71daed7c3aa9e62edf9eea207fd77b2041be52ed",
            "918A1E3FC74AD530AF070C012BB8075DBC3874438FE5BA3C96A8D8AD39A3FCE2",
            "persist-credentials: false",
            "ABCL_G1_AES256_KEY",
            "dotnet restore",
            "dotnet build",
            "CLR2 runtime metadata not found",
            "output/ModABCLG1LeadTest.dll",
            "MEDICAL_ICONS_V3=NOT_PACKAGED",
            "GAMEPLAY_L4=NOT_RUN",
        ):
            self.assertIn(required, src)
        self.assertNotIn("output/Assembly-CSharp.dll", src)
        self.assertNotIn("actions/create-release", src)
        self.assertNotIn("gh pr merge", src)

    def test_no_in_game_success_claim_from_build(self):
        self.assertIn("TEST ONLY", self.source)
        self.assertIn("NOTINSTALLABLE", self.source)
        self.assertIn("CLINICAL_G2_XML=NOT_PACKAGED", self.source)


if __name__ == "__main__":
    unittest.main()
