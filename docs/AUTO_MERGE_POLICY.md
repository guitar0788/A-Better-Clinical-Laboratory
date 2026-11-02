# Conditional auto-merge for low-risk pull requests

**Decision:** ABCL-D014 (owner approved, 2026-11-02)  
**Status:** Takes effect only after this policy and its workflow are merged into protected `main`.  
**Scope:** Repository `guitar0788/A-Better-Clinical-Laboratory` only.

## Why this is deliberately narrow

ABCL has a protected `main`, an ordinary read-only `Verify` check and a proprietary-reference G1 compile path. The project owner does **not** need to click Merge for routine, fully checked editorial tasks. That convenience must not grant permission to change clinical behavior, resource registration, cryptographic inputs, Actions privileges, published versions, or medical and visual acceptance records.

GitHub's built-in `allow_auto_merge` setting was found disabled when this proposal was prepared. The trusted GitHub Actions job performs the final **squash merge through the GitHub API**, not via a repository-wide GitHub auto-merge toggle. It cannot bypass required status checks or branch rules.

## Exact allowlist

Only **added/modified text files** in the following locations are eligible, subject to all other gates:

- `docs/guides/**/*.md`
- `docs/tutorials/**/*.md`
- `docs/notes/**/*.md`
- `tests/test_docs_*.py`, `tests/test_links_*.py`, `tests/test_format_*.py`

A PR must change at most **six files** and **180 diff lines** total. Binary changes and deletions are disallowed. Filenames are evaluated against GitHub's own PR changed-files API, never a PR-authored manifest.

Everything else defaults to **manual, owner-authorized integration**, including:

- `src/`, `assets/`, all original-art, texture and native room/equipment XML.
- `.github/`, `tools/`, build/packaging scripts, Secrets, reference DLLs and cryptographic inputs.
- `docs/MASTER_PLAN.md`, `docs/DECISIONS.md`, `docs/TEST_EVIDENCE.md`, `docs/TEAM_WORKFLOW.md`, `CONTRIBUTING.md`, `README.md`, release policy or compatibility declarations.
- G1 medical/patient/diagnostic code, ART-001 final visual acceptance, compatibility claims, existing saves and release assets.

A PR that mixes safe and restricted files is always **restricted**. FA's artwork or accepted visual decisions never auto-merge.

## Approval and CI conditions (all required)

1. PR is open, **not a draft**, targets `main`, and is authored from this same public repository by `guitar0788`.
2. TS has reviewed the **exact current PR head SHA** and applies label `automerge:low-risk`.
3. TS posts a GitHub PR comment consisting of exactly `ABCL-TS-AUTOMERGE: <40-character-lowercase-head-SHA>`. The comment must be authored by `guitar0788`. A new commit immediately makes an older approval invalid.
4. No `manual-review`, `needs-fix`, `blocked`, `security-review` or `release-review` label.
5. The exact head SHA has successful, completed **GitHub Actions Verify** and **CodeRabbit** checks. For Python tests, **Analyze Python** must also succeed. Any failed, pending or cancelled check blocks merging.
6. No outstanding formal review with **CHANGES_REQUESTED**; GitHub must report that the PR can merge. The workflow rechecks the current head and uses GitHub's atomic expected-SHA merge guard.
7. All file and size restrictions above still hold immediately before merging.

**If any condition is missing, the workflow skips the PR without bypassing policy.** TS can investigate and reapprove a corrected head. No general permission to merge a new feature is implied by a previously attached label.

## How the automation works

- Trusted workflow: `.github/workflows/auto-merge-low-risk.yml` on protected `main`.
- Trusted evaluator: `tools/auto_merge_low_risk.py` checked out from **`main` only**.
- Triggers: TS approval comment or label, PR synchronization/ready state, successful `Verify`, and a two-hour fallback sweep for delayed CodeRabbit checks.
- The merge runner has only GitHub's repository-scoped, short-lived `GITHUB_TOKEN` and the minimum read/write permissions necessary to merge. It never checks out PR code, reads the AES key or starts an encrypted game build.
- GitHub Actions runs created by a `GITHUB_TOKEN`-originated merge may not trigger ordinary `push` workflows. The **source PR head's Verify and review** are therefore the mandatory merge gates; do not invent a post-merge main CI PASS.
- If repository Actions settings or branch rules reject the merge, the operation fails closed; do not turn off protection to force it.

## Responsibilities

**TS** may issue the exact-SHA review comment and label for this restricted class. It performs the final technical review or asks for corrections before approving. The owner does not need to operate GitHub for these approved low-risk merges.

**FA** continues to own art files and art-focused PRs. Any PR with real artwork, game integration, visual acceptance or gameplay evidence remains outside this mechanism.

**The project owner** retains final authority for core changes, security/CI infrastructure, gameplay compatibility claims, DLC/Workshop support, visual acceptance, installation packages and all releases.

## First-time deployment and verification

This change itself is governance/security infrastructure: **PR carrying this file is never auto-merge eligible.** Its required checks and security review must pass before the project owner approves merge into protected `main`.

After activation, validate with a **small docs-only sandbox PR** under `docs/notes/`, record the exact SHA, have TS leave the approval comment and label, and confirm the GitHub Actions run and resulting squash merge. Verify that stale approvals, unknown labels, forks, mixed paths and pending checks do not merge. No clinical L3/L4 test is implied.

All public-facing policy, PR and automation logs remain in English. Do not delete historical branches or rewrite previously approved decisions.
