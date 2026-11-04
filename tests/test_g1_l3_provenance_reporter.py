"""Source-only checks for protected-main G1 compile provenance reporting.

This does not compile or test Project Hospital. It verifies the reporter
cannot publish a guessed DLL hash or read the game's encrypted references.
"""
from pathlib import Path
import unittest

WORKFLOW = (Path(__file__).resolve().parents[1] /
            ".github/workflows/auto-build-g1-verified.yml")
TEXT = WORKFLOW.read_text(encoding="utf-8")
AUTHORIZE = TEXT.split("\n  authorize:", 1)[1].split("\n  build:", 1)[0]
BUILD = TEXT.split("\n  build:", 1)[1].split("\n  report:", 1)[0]
REPORT = TEXT.split("\n  report:", 1)[1]


class G1ProvenanceReporterPolicy(unittest.TestCase):
    def test_real_build_must_succeed_before_reporting(self):
        self.assertIn("needs: [authorize, build]", REPORT)
        self.assertIn("needs.authorize.outputs.allowed == 'true'", REPORT)
        self.assertIn("needs.build.result == 'success'", REPORT)
        self.assertIn("id: build_info", BUILD)
        self.assertIn('dll_sha256: ${{ steps.build_info.outputs.dll_sha256 }}', BUILD)
        self.assertIn('"dll_sha256=$hash" >> $env:GITHUB_OUTPUT', BUILD)
        self.assertLess(BUILD.index("Compile isolated project against genuine net35"),
                        BUILD.index("id: build_info"))
        self.assertLess(BUILD.index("id: build_info"),
                        BUILD.index("uses: actions/upload-artifact@v4"))
        self.assertIn("SOURCE_SHA: ${{ needs.authorize.outputs.sha }}", REPORT)
        self.assertIn("DLL_SHA256: ${{ needs.build.outputs.dll_sha256 }}", REPORT)

    def test_reporter_cannot_access_game_keys_or_mutate_repository(self):
        self.assertIn("      pull-requests: write", REPORT)
        self.assertNotIn("      issues: write", REPORT)
        self.assertIn("      pull-requests: write", REPORT)
        self.assertIn("      contents: read", REPORT)
        self.assertNotIn("      contents: write", REPORT)
        self.assertNotIn("ABCL_G1_AES256_KEY", REPORT)
        self.assertNotIn("ABCL_G1_refs.aes", REPORT)
        self.assertNotIn("dotnet build", REPORT)
        self.assertNotIn("      issues: write", AUTHORIZE)
        self.assertNotIn("      issues: write", BUILD)

    def test_never_report_stale_or_unknown_dll(self):
        self.assertIn("PR 7 moved or changed owner", REPORT)
        self.assertIn("$pr.head.sha -ne $env:SOURCE_SHA", REPORT)
        self.assertIn("$pr.user.login -ne 'guitar0788'", REPORT)
        self.assertIn("$pr.head.ref -ne 'feature/g1-secure-build'", REPORT)
        self.assertIn("$env:SOURCE_SHA -cnotmatch '^[0-9a-f]{40}$'", REPORT)
        self.assertIn("$env:DLL_SHA256 -cnotmatch '^[0-9A-Fa-f]{64}$'", REPORT)
        self.assertIn("ABCL-G1-EXACT-L3-PROVENANCE", REPORT)
        self.assertIn("Complete owner-integrated 34-file bundle: **NOT AUDITED**", REPORT)
        self.assertIn("gameplay L4: **NOT RUN**", REPORT)
        self.assertIn("0-byte Harmony placeholder", REPORT)

    def test_authorized_failed_windows_stage_is_reported_without_fabricated_dll(self):
        self.assertIn("always() && !cancelled() && needs.authorize.result == 'success'", REPORT)
        self.assertIn("needs.authorize.outputs.allowed == 'true'", REPORT)
        self.assertIn("needs.build.result == 'failure'", REPORT)
        self.assertIn("      actions: read", REPORT)
        self.assertIn("BUILD_RESULT: ${{ needs.build.result }}", REPORT)
        self.assertIn("$env:BUILD_RESULT -notin @('success','failure')", REPORT)
        self.assertIn("if ($env:BUILD_RESULT -eq 'success')", REPORT)
        self.assertIn('actions/runs/$env:RUN_ID/jobs?per_page=100', REPORT)
        self.assertIn("No independently confirmed failed Windows build job", REPORT)
        self.assertIn("Failed stage: $stage", REPORT)
        self.assertIn("G1 authorized Windows build job: FAILED (L3 compile status not established)", REPORT)
        self.assertIn("No verified DLL SHA", REPORT)
        self.assertIn("Project Hospital gameplay L4: **NOT RUN**", REPORT)
        self.assertNotIn("ABCL_G1_AES256_KEY", REPORT)
        self.assertNotIn("ABCL_G1_refs.aes", REPORT)

    def test_http403_pr_comment_denial_retains_exact_l3_summary(self):
        self.assertIn("      pull-requests: write", REPORT)
        self.assertNotIn("      issues: write", REPORT)
        self.assertIn("GITHUB_STEP_SUMMARY", REPORT)
        self.assertIn("Add-Content -LiteralPath $env:GITHUB_STEP_SUMMARY -Value $body", REPORT)
        self.assertIn("if ($statusCode -ne 403) { throw }", REPORT)
        self.assertIn("::warning::PR provenance comment HTTP 403", REPORT)
        self.assertIn("existing marker comment (if any) was not updated", REPORT)
        self.assertIn("may describe an older source SHA", REPORT)
        self.assertIn("inspect the exact run Actions summary", REPORT)
        self.assertNotIn("Actions summary and artifact.", REPORT)
        self.assertIn("PR 7 moved or changed owner", REPORT)
        self.assertIn("if ($env:BUILD_RESULT -eq 'success')", REPORT)
        self.assertNotIn("ABCL_G1_AES256_KEY", REPORT)
        self.assertNotIn("ABCL_G1_refs.aes", REPORT)

    def test_reporter_is_non_releasing_and_does_not_write_new_comments_each_run(self):
        self.assertIn("issues/7/comments?per_page=100", REPORT)
        self.assertIn("issues/comments/$($old.id)", REPORT)
        self.assertIn("$comment.user.login -eq 'github-actions[bot]'", REPORT)
        self.assertIn("while (-not [string]::IsNullOrEmpty($nextPage))", REPORT)
        self.assertIn("-ResponseHeadersVariable responseHeaders", REPORT)
        self.assertIn("responseHeaders['Link']", REPORT)
        self.assertIn('rel="next"', REPORT)
        self.assertIn("$old=$comment", REPORT)
        self.assertNotIn("releases: write", REPORT)
        self.assertNotIn("git push", REPORT)


if __name__ == "__main__":
    unittest.main()
