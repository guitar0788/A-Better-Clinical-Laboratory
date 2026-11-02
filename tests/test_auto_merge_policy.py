"""Offline regression checks for the protected-main low-risk merge gate.

All API behavior is simulated. These tests never make a GitHub merge request.
"""
import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "auto_merge_low_risk.py"
SPEC = importlib.util.spec_from_file_location("abcl_safe_merge", SOURCE)
MERGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MERGE)

SHA = "a" * 40
OTHER_SHA = "b" * 40


def check(name, conclusion="success", app="github-actions"):
    return {
        "name": name, "status": "completed", "conclusion": conclusion,
        "app": {"slug": app}
    }


def eligible_pr():
    return {
        "number": 42, "state": "open", "draft": False, "mergeable": True,
        "base": {"ref": "main"},
        "head": {"sha": SHA, "ref": "docs/example", "repo": {"full_name": MERGE.REPO}},
        "user": {"login": MERGE.OWNER},
        "labels": [{"name": "automerge:low-risk"}],
    }


def safe_doc():
    return {
        "filename": "docs/guides/editor-quickstart.md",
        "status": "added", "changes": 7, "patch": "@@ -0,0 +1,7 @@"
    }


class FakeGitHub:
    def __init__(self, pr=None, files=None, comments=None, checks=None, reviews=None):
        self.pr = pr if pr is not None else eligible_pr()
        self.files = files if files is not None else [safe_doc()]
        self.comments = comments if comments is not None else [
            {"user": {"login": MERGE.OWNER}, "body": "ABCL-TS-AUTOMERGE: " + SHA}
        ]
        self.checks = checks if checks is not None else [
            check("Verify"), check("CodeRabbit", app="coderabbitai")
        ]
        self.reviews = reviews if reviews is not None else []
        self.merges = []

    def get(self, path):
        if path.endswith("/pulls/42"):
            return self.pr
        if path.endswith("/check-runs?per_page=100"):
            return {"check_runs": self.checks}
        raise AssertionError("Unexpected API GET: " + path)

    def get_pages(self, path, limit=100):
        if path.endswith("/files"):
            return self.files
        if path.endswith("/comments"):
            return self.comments
        if path.endswith("/reviews"):
            return self.reviews
        raise AssertionError("Unexpected API GET pages: " + path)

    def request(self, method, path, body=None):
        if method != "PUT" or not path.endswith("/pulls/42/merge"):
            raise AssertionError("Unexpected API mutation")
        self.merges.append(body)
        return {"merged": True, "sha": "c" * 40}


class GateTests(unittest.TestCase):
    def test_safe_paths_are_exactly_limited(self):
        for path in ["docs/notes/README.md", "docs/tutorials/set-up.md",
                     "docs/guides/guide.md", "tests/test_docs_links.py",
                     "tests/test_links_manual.py", "tests/test_format_xml.py"]:
            self.assertTrue(MERGE.low_risk_path(path), path)
        for path in [
            ".github/workflows/verify.yml", "src/ABCLG1Panel.cs",
            "ABCL_G1_refs.aes", "docs/DECISIONS.md", "docs/MASTER_PLAN.md",
            "docs/TEST_EVIDENCE.md", "docs/TEAM_WORKFLOW.md",
            "docs/notes/../DECISIONS.md", "assets/art001/Database/ModObjectsABCL.xml",
            "tests/test_g1_contract.py", "tests/test_auto_merge_policy.py"
        ]:
            self.assertFalse(MERGE.low_risk_path(path), path)

    def test_allowlist_rejects_deleted_binary_and_oversized_file(self):
        self.assertFalse(MERGE.safe_files([{**safe_doc(), "status": "removed"}]))
        self.assertFalse(MERGE.safe_files([{**safe_doc(), "patch": None}]))
        self.assertFalse(MERGE.safe_files([{**safe_doc(), "changes": 181}]))
        self.assertFalse(MERGE.safe_files([safe_doc()] * 7))

    def test_exact_head_sha_approval_is_required(self):
        self.assertTrue(MERGE.has_current_owner_approval(
            [{"user": {"login": MERGE.OWNER}, "body": "ABCL-TS-AUTOMERGE: " + SHA}], SHA))
        self.assertFalse(MERGE.has_current_owner_approval(
            [{"user": {"login": MERGE.OWNER}, "body": "ABCL-TS-AUTOMERGE: " + SHA}], OTHER_SHA))
        self.assertFalse(MERGE.has_current_owner_approval(
            [{"user": {"login": "external-user"}, "body": "ABCL-TS-AUTOMERGE: " + SHA}], SHA))

    def test_pending_verify_and_coderabbit_are_fail_closed(self):
        self.assertFalse(MERGE.checks_pass([check("Verify")], needs_python=False))
        self.assertFalse(MERGE.checks_pass(
            [check("Verify", "failure"), check("CodeRabbit", app="coderabbitai")], False))
        self.assertFalse(MERGE.checks_pass(
            [check("Verify"), check("CodeRabbit", "cancelled", "coderabbitai")], False))
        self.assertFalse(MERGE.checks_pass(
            [check("Verify"), check("CodeRabbit", app="coderabbitai")], True))
        self.assertTrue(MERGE.checks_pass(
            [check("Verify"), check("CodeRabbit", app="coderabbitai"),
             check("Analyze Python")], True))

    def test_blocked_label_and_fork_never_merge(self):
        pr = eligible_pr()
        pr["labels"].append({"name": "manual-review"})
        self.assertFalse(MERGE.preliminary(pr))
        pr = eligible_pr()
        pr["head"]["repo"]["full_name"] = "attacker/fork"
        self.assertFalse(MERGE.preliminary(pr))
        pr = eligible_pr()
        pr["draft"] = True
        self.assertFalse(MERGE.preliminary(pr))

    def test_comment_authorization_works_without_optional_labels(self):
        pr = eligible_pr()
        pr["labels"] = []
        self.assertTrue(MERGE.preliminary(pr))
        gh = FakeGitHub(pr=pr)
        self.assertTrue(MERGE.evaluate_and_merge(gh, 42, expected_sha=SHA))
        self.assertEqual(len(gh.merges), 1)

    def test_merge_only_after_approval_checks_and_revalidation(self):
        gh = FakeGitHub()
        self.assertTrue(MERGE.evaluate_and_merge(gh, 42, expected_sha=SHA))
        self.assertEqual(gh.merges, [{"sha": SHA, "merge_method": "squash"}])
        stale = FakeGitHub()
        self.assertFalse(MERGE.evaluate_and_merge(stale, 42, expected_sha=OTHER_SHA))
        self.assertEqual(stale.merges, [])
        no_approval = FakeGitHub(comments=[])
        self.assertFalse(MERGE.evaluate_and_merge(no_approval, 42))
        self.assertEqual(no_approval.merges, [])
        rejected = FakeGitHub(reviews=[{"user": {"login": "reviewer"}, "state": "CHANGES_REQUESTED"}])
        self.assertFalse(MERGE.evaluate_and_merge(rejected, 42))
        self.assertEqual(rejected.merges, [])

    def test_workflow_never_checks_out_untrusted_pr_code(self):
        workflow = (ROOT / ".github" / "workflows" / "auto-merge-low-risk.yml").read_text()
        self.assertIn("pull_request_target:", workflow)
        self.assertIn("workflow_run:", workflow)
        self.assertIn("ref: main", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("python tools/auto_merge_low_risk.py", workflow)
        self.assertNotIn("pull_request.head.sha", workflow)
        self.assertNotIn("secrets.ABCL_G1_AES256_KEY", workflow)


if __name__ == "__main__":
    unittest.main()
