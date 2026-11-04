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
        self.assertIn("      issues: write", REPORT)
        self.assertIn("      pull-requests: read", REPORT)
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
