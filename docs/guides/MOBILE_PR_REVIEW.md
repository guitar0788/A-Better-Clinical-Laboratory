# Reviewing ABCL pull requests from a phone

This short guide is for contributors using the GitHub mobile app or a mobile browser. It explains how to distinguish source checks from genuine Project Hospital gameplay evidence.

## Find the exact work being reviewed

Open the pull request and use **Commits** to copy the latest full 40-character SHA. If the branch changes, previous CI or game test results must not be attributed to the new source without checking the exact SHA.

Use **Files changed** to see whether the work touches clinical code, original artwork, shared XML or only documentation. The pull request title alone does not establish its scope.

## Read the Checks tab

**Verify** validates repository contracts and relevant source/tests. A passing result is not a real game build. The **G1 Windows net35/CLR2 build** is separate L3 evidence, with an Actions run and test-only artifact. A preview-only art workflow is likewise not an installable game package.

A completed **CodeRabbit** review is useful but does not establish that all visual, native interaction or DLC/Workshop compatibility concerns have been resolved.

## Read the evidence

Before describing a result as accepted, inspect the relevant section of `docs/TEST_EVIDENCE.md` and record the tested SHA, run ID, exact scope, limitations and any required L4 gameplay steps.

An approved static preview never substitutes for the owner's in-game visual approval. A previously accepted core G1 clinical test does not need to be repeated only because a read-only diagnostic panel or art preview layout changed.

## Ordinary low-risk handoffs

TS may approve truly minor documentation/non-clinical test changes by commenting `ABCL-TS-AUTOMERGE: <full-head-sha>` on the PR. A protected-main workflow handles eligible merges after exact-head checks pass; it does not merge code, art, medical definitions, governance or releases. See `docs/AUTO_MERGE_POLICY.md` for the full exclusion list.

If a merge is not automatic, **do not disable branch protection**. Check the current SHA, review state, CI conclusions and allowed file paths. Important changes still require owner authorization.
