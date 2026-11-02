#!/usr/bin/env python3
"""Fail-closed, owner-reviewed auto-merge of tightly scoped low-risk ABCL PRs.

This runs only from the protected default branch. Never checkout or execute PR
code here. GitHub_TOKEN access is limited to repository merge operations.
"""
import json
import os
import re
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

REPO = "guitar0788/A-Better-Clinical-Laboratory"
OWNER = "guitar0788"
API = "https://api.github.com"
APPROVAL = re.compile(r"^ABCL-TS-AUTOMERGE: ([0-9a-f]{40})$")
BLOCKING_LABELS = {"manual-review", "needs-fix", "blocked", "security-review", "release-review"}
MAX_FILES = 6
MAX_CHANGED_LINES = 180
MAX_PR_SCAN = 30


def low_risk_path(path):
    """Do not auto-merge authoritative plans, medical content, visual assets or CI."""
    if not isinstance(path, str) or ".." in path.split("/"):
        return False
    if path.endswith(".md") and (
        path.startswith("docs/guides/")
        or path.startswith("docs/tutorials/")
        or path.startswith("docs/notes/")
    ):
        return True
    return bool(re.fullmatch(r"tests/test_(?:docs|links|format)_[A-Za-z0-9_]+\.py", path))


def safe_files(files):
    if not files or len(files) > MAX_FILES:
        return False
    if sum(int(f.get("changes", 0)) for f in files) > MAX_CHANGED_LINES:
        return False
    return all(
        low_risk_path(f.get("filename"))
        and f.get("status") in ("added", "modified")
        and isinstance(f.get("patch"), str)
        for f in files
    )


def has_current_owner_approval(comments, sha):
    """Approval is commit-bound; changing the PR head invalidates it."""
    return any(
        c.get("user", {}).get("login") == OWNER
        and APPROVAL.fullmatch((c.get("body") or "").strip())
        and APPROVAL.fullmatch((c.get("body") or "").strip()).group(1) == sha
        for c in comments
    )


def checks_pass(checks, needs_python):
    """Missing/pending/failed mandatory checks are all non-mergeable."""
    by_name = {}
    for check in checks:
        name = check.get("name")
        if name:
            by_name[name] = check
    for name in (("Verify", "CodeRabbit", "Analyze Python") if needs_python else ("Verify", "CodeRabbit")):
        c = by_name.get(name)
        if not c or c.get("status") != "completed" or c.get("conclusion") != "success":
            return False
        if name == "Verify" and c.get("app", {}).get("slug") != "github-actions":
            return False
        if name == "CodeRabbit" and c.get("app", {}).get("slug") != "coderabbitai":
            return False
    for c in checks:
        if c.get("status") != "completed":
            return False
        if c.get("conclusion") not in ("success", "neutral", "skipped"):
            return False
    return True


def no_change_requests(reviews):
    latest = {}
    for review in reviews:
        author = (review.get("user") or {}).get("login")
        state = review.get("state")
        if author and state in ("APPROVED", "CHANGES_REQUESTED", "DISMISSED"):
            latest[author] = state
    return "CHANGES_REQUESTED" not in latest.values()


def preliminary(pr):
    labels = {x.get("name", "").lower() for x in pr.get("labels", [])}
    return (
        pr.get("state") == "open"
        and not pr.get("draft")
        and pr.get("base", {}).get("ref") == "main"
        and pr.get("head", {}).get("repo", {}).get("full_name") == REPO
        and pr.get("user", {}).get("login") == OWNER
        and pr.get("head", {}).get("sha") is not None
        and pr.get("head", {}).get("ref") != "main"
        and pr.get("mergeable") is True
        and not (labels & BLOCKING_LABELS)
    )


class GitHub:
    def __init__(self, token):
        if not token:
            raise ValueError("GitHub token missing")
        self.token = token

    def request(self, method, path, body=None):
        url = API + path
        headers = {
            "Authorization": "Bearer " + self.token,
            "Accept": "application/vnd.github+json",
            "User-Agent": "ABCL-approved-low-risk-automerge",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        payload = None if body is None else json.dumps(body).encode("utf-8")
        req = Request(url, data=payload, method=method, headers=headers)
        try:
            with urlopen(req, timeout=18) as r:
                data = r.read()
            return json.loads(data.decode("utf-8")) if data else {}
        except HTTPError as e:
            detail = e.read(500).decode("utf-8", errors="replace")
            raise RuntimeError("%s %s returned HTTP %s: %s" % (method, path, e.code, detail)) from e

    def get(self, path):
        return self.request("GET", path)

    def get_pages(self, path, limit=100):
        all_items = []
        for page in range(1, 4):
            sep = "&" if "?" in path else "?"
            items = self.get("%s%sper_page=100&page=%d" % (path, sep, page))
            if not isinstance(items, list):
                raise ValueError("Unexpected GitHub list payload")
            all_items.extend(items)
            if len(items) < 100 or len(all_items) >= limit:
                break
        return all_items[:limit]


def evaluate_and_merge(gh, number, expected_sha=None):
    pr = gh.get("/repos/%s/pulls/%d" % (REPO, number))
    sha = pr.get("head", {}).get("sha")
    if expected_sha and expected_sha != sha:
        print("SKIP PR #%d: Verify SHA is no longer the current head" % number)
        return False
    if not preliminary(pr):
        print("SKIP PR #%d: not owner-approved, safe, current or mergeable" % number)
        return False

    files = gh.get_pages("/repos/%s/pulls/%d/files" % (REPO, number), limit=MAX_FILES + 1)
    if not safe_files(files):
        print("SKIP PR #%d: paths, binary changes or size require human review" % number)
        return False

    comments = gh.get_pages("/repos/%s/issues/%d/comments" % (REPO, number), limit=300)
    if not has_current_owner_approval(comments, sha):
        print("SKIP PR #%d: no exact-SHA TS approval comment" % number)
        return False

    data = gh.get("/repos/%s/commits/%s/check-runs?per_page=100" % (REPO, sha))
    checks = data.get("check_runs", [])
    needs_python = any(f["filename"].endswith(".py") for f in files)
    if not checks_pass(checks, needs_python):
        print("SKIP PR #%d: Verify / CodeRabbit / CodeQL checks pending or failed" % number)
        return False
    reviews = gh.get_pages("/repos/%s/pulls/%d/reviews" % (REPO, number))
    if not no_change_requests(reviews):
        print("SKIP PR #%d: changes requested" % number)
        return False

    # Revalidate the exact head immediately before merge. GitHub also enforces
    # this SHA atomically and applies the existing protected-main rules.
    latest = gh.get("/repos/%s/pulls/%d" % (REPO, number))
    if latest.get("head", {}).get("sha") != sha or not preliminary(latest):
        print("SKIP PR #%d: changed while evaluating" % number)
        return False
    print("MERGE PR #%d: owner-approved SHA %s; %d safe file(s)" % (number, sha, len(files)))
    response = gh.request("PUT", "/repos/%s/pulls/%d/merge" % (REPO, number), {
        "sha": sha, "merge_method": "squash"
    })
    if not response.get("merged"):
        raise RuntimeError("GitHub did not confirm merge for PR #%d" % number)
    print("MERGED PR #%d: %s" % (number, response.get("sha")))
    return True


def candidates(event_name, event):
    if event_name == "pull_request_target":
        pr = event.get("pull_request") or {}
        return [(pr.get("number"), None)] if pr.get("number") else []
    if event_name == "issue_comment":
        issue = event.get("issue") or {}
        comment = event.get("comment") or {}
        if not issue.get("pull_request") or comment.get("user", {}).get("login") != OWNER:
            return []
        if not APPROVAL.fullmatch((comment.get("body") or "").strip()):
            return []
        return [(issue.get("number"), None)]
    if event_name == "workflow_run":
        run = event.get("workflow_run") or {}
        if run.get("name") != "Verify" or run.get("conclusion") != "success":
            return []
        if run.get("event") != "pull_request" or run.get("head_repository", {}).get("full_name") != REPO:
            return []
        sha = run.get("head_sha")
        return [(pr["number"], sha) for pr in (run.get("pull_requests") or []) if pr.get("number")]
    return []


def main():
    if os.environ.get("GITHUB_REPOSITORY") != REPO:
        raise RuntimeError("Unexpected target repository")
    with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as f:
        event = json.load(f)
    gh = GitHub(os.environ.get("GH_TOKEN"))
    event_name = os.environ["GITHUB_EVENT_NAME"]
    pending = candidates(event_name, event)
    if event_name == "schedule":
        prs = gh.get_pages("/repos/%s/pulls?state=open" % REPO, limit=MAX_PR_SCAN)
        pending = [(pr.get("number"), None) for pr in prs if pr.get("number")]
    seen = set()
    for number, sha in pending:
        if number and number not in seen:
            seen.add(number)
            evaluate_and_merge(gh, int(number), sha)


if __name__ == "__main__":
    main()
