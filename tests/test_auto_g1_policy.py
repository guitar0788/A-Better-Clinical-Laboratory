"""Static guardrails for the owner-only verified G1 build workflow.

These tests do not assert successful net35 compilation or gameplay. They prevent
casual regressions in the privileged CI boundary.
"""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "auto-build-g1-verified.yml"


class TestAutoG1BuildPolicy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_only_after_verify_and_bound_to_g1_branch_or_initial_main_merge(self):
        self.assertIn("workflow_run:", self.text)
        self.assertIn("workflows: [Verify]", self.text)
        self.assertIn("types: [completed]", self.text)
        self.assertIn("branches: [feature/g1-secure-build, main]", self.text)
        self.assertNotIn("pull_request_target:", self.text)
        self.assertIn("workflow_run.conclusion == 'success'", self.text)
        self.assertIn("workflow_run.head_repository.full_name == github.repository", self.text)
        self.assertIn("workflow_run.actor.login == 'guitar0788'", self.text)

    def test_least_privilege_read_access_for_authorization_only(self):
        before_jobs, jobs = self.text.split("\n", 1)[0], self.text
        workflow_permissions = jobs.split("permissions:", 1)[1].split("concurrency:", 1)[0]
        self.assertIn("contents: read", workflow_permissions)
        self.assertNotIn("pull-requests:", workflow_permissions)
        self.assertNotIn("checks:", workflow_permissions)
        authorize = jobs.split("  authorize:", 1)[1].split("  build:", 1)[0]
        self.assertIn("    permissions:", authorize)
        self.assertIn("      contents: read", authorize)
        self.assertIn("      pull-requests: read", authorize)
        self.assertIn("      checks: read", authorize)
        build = jobs.split("  build:", 1)[1]
        self.assertNotIn("    permissions:", build)
        self.assertNotIn("contents: write", self.text)

    def test_exact_current_owner_pr_precedes_secret_access(self):
        gate = self.text.index("Authorize latest owner-controlled G1 PR head before decrypt")
        checkout = self.text.index("Checkout exact approved source")
        isolate = self.text.index("Copy the pinned G1 project")
        restore = self.text.index("Restore trusted package before")
        decrypt = self.text.index("Decrypt owner-authorized references")
        self.assertLess(gate, checkout)
        self.assertLess(isolate, restore)
        self.assertLess(restore, decrypt)
        self.assertIn("/pulls/7", self.text)
        self.assertIn("pr.head.sha -ne $sha", self.text)
        self.assertIn("stale", self.text.lower())

    def test_unrelated_main_verify_skips_before_pr_lookup(self):
        main_guard = self.text.index("if ($run.head_branch -eq 'main') {")
        changed_workflow_test = self.text.index("if (@($commit.files")
        clean_skip = self.text.index("Unrelated main Verify; no G1 build necessary.")
        pr_lookup = self.text.index('"/pulls/7"') if '"/pulls/7"' in self.text else self.text.index('/pulls/7')
        self.assertLess(main_guard, changed_workflow_test)
        self.assertLess(changed_workflow_test, clean_skip)
        self.assertLess(clean_skip, pr_lookup)
        self.assertIn('"allowed=false" >> $env:GITHUB_OUTPUT', self.text)

    def test_authorized_g1_checkout_contains_all_packaging_inputs_before_decryption(self):
        checkout = self.text.index("Checkout exact approved source")
        preflight = self.text.index("Audit exact G1 checkout and eight packaged source files before decrypt")
        decrypt = self.text.index("Decrypt owner-authorized references")
        self.assertLess(checkout, preflight)
        self.assertLess(preflight, decrypt)
        self.assertIn("EXPECTED_G1_SHA: ${{ needs.authorize.outputs.sha }}", self.text)
        self.assertIn("git rev-parse HEAD", self.text)
        self.assertIn("Test-Path -LiteralPath $path -PathType Leaf", self.text)
        for required in (
            "assets/g1/Database/ModAddon.xml",
            "assets/g1/Database/ModExaminations.xml",
            "assets/g1/Database/ModRoomTypes.xml",
            "assets/g1/Database/ModStringTableEnABCL.xml",
            "assets/g1/Database/ModStringTableZhHansABCL.xml",
            "tools/Install-ABCL-G1.ps1",
            "tools/INSTALL_G1_R3.cmd",
            "tools/G1_TEST_README.txt",
        ):
            self.assertIn(required, self.text)

    def test_stale_g1_runs_cancel_and_revalidate_before_sensitive_stages(self):
        self.assertIn("cancel-in-progress: true", self.text)
        self.assertNotIn("cancel-in-progress: false", self.text)
        authorize = self.text.index("Authorize latest owner-controlled G1 PR head before decrypt")
        checkout = self.text.index("Checkout exact approved source")
        first_recheck = self.text.index("Reject superseded G1 PR before decrypt")
        decrypt = self.text.index("Decrypt owner-authorized references in temporary runner storage")
        compile_step = self.text.index("Compile isolated project against genuine net35 game references")
        package = self.text.index("Create ABCL-only test artifact")
        second_recheck = self.text.index("Reject superseded G1 PR before test artifact upload")
        upload = self.text.index("uses: actions/upload-artifact@v4")
        self.assertLess(authorize, checkout)
        self.assertLess(checkout, first_recheck)
        self.assertLess(first_recheck, decrypt)
        self.assertLess(decrypt, compile_step)
        self.assertLess(package, second_recheck)
        self.assertLess(second_recheck, upload)
        for block in (
            self.text[first_recheck:decrypt],
            self.text[second_recheck:upload],
        ):
            self.assertIn("EXPECTED_G1_SHA: ${{ needs.authorize.outputs.sha }}", block)
            self.assertIn("pr.head.sha -ne $env:EXPECTED_G1_SHA", block)
            self.assertIn("pr.state -ne 'open'", block)
            self.assertIn("pr.user.login -ne 'guitar0788'", block)
            self.assertIn("pr.head.ref -ne 'feature/g1-secure-build'", block)
            self.assertIn("pr.base.ref -ne 'main'", block)

    def test_pinned_isolated_project_without_untrusted_msbuild_hooks(self):
        self.assertIn("71daed7c3aa9e62edf9eea207fd77b2041be52ed", self.text)
        self.assertIn("git hash-object -- src/ABCL.G1.Panel.csproj", self.text)
        self.assertIn("Join-Path $env:RUNNER_TEMP 'abcl-isolated-src'", self.text)
        self.assertIn('dotnet build "$env:ABCL_G1_ISOLATED_PROJECT"', self.text)
        self.assertNotIn("dotnet build src/ABCL.G1.Panel.csproj", self.text)
        self.assertIn("persist-credentials: false", self.text)

    def test_no_release_or_vanilla_binaries_published(self):
        self.assertIn("ABCL-G1-AutoBuilt-TestOnly", self.text)
        self.assertIn("ABCL_G1_AES256_KEY", self.text)
        self.assertIn("REF_SHA256:", self.text)
        self.assertIn("0Harmony.dll", self.text)
        self.assertIn("Forbidden original game reference in test artifact.", self.text)
        self.assertNotIn("softprops/action-gh-release", self.text)
        self.assertNotIn("releases: write", self.text)
        self.assertNotIn("contents: write", self.text)


if __name__ == "__main__":
    unittest.main()
