# PR, Issue, and branch lifecycle audit — 2026-11-04

**Repository:** `guitar0788/A-Better-Clinical-Laboratory`
**Authority:** main `docs/MASTER_PLAN.md` and `docs/DECISIONS.md`.
**This is a review document in Draft PR #33, not an approved main-branch change.**

## Exact inventory and why the counts differ

The GitHub REST repository inventory on 2026-11-04 showed **37 git branches**, **23 open pull requests** and **6 open Issues** before this triage. The owner's apparent "23 branches" is the open pull-request count, not the actual branch count.

Four old Draft PRs have since been **closed without merging**; all source branches and historical commits are retained. Post-triage totals: **37 branches / 19 open PRs / 6 open Issues**. Branch inventory is therefore:

| Branch class | Number | Policy |
| --- | ---: | --- |
| Protected `main` | 1 | Keep; no force push or deletion |
| Head branches of 19 currently open PRs | 19 | Keep while PR is active, review-blocked, or needed as a stacked PR base |
| Historical branch of merged PR (PR already merged, branch still exists) | 11 | Eligible for later *reviewed* branch cleanup only; GitHub commits and merged content stay |
| Historical branches of closed *unmerged* PRs | 6 | Preserve until source provenance/archival is confirmed; not automatically delete |
| **Total** | **37** | No branch was deleted by this triage |

## Six genuine top-level Issues — do not fake completion

| Issue | Owner / workstream | Correct lifecycle at this checkpoint |
| --- | --- | --- |
| [#2](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/2) | TS / G1 | **In Progress**: owner-reported R3 core L4 PASS; latest panel and integrated compatibility still have gated follow-up |
| [#3](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/3) | FA + TS / original equipment | **Needs Fix / L4 blocked**: independent hardware art and genuine staff operation not accepted |
| [#4](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/4) | TS / Alpha release | **Backlog**: no approved installable Alpha, four-DLC/Workshop matrix or release gate |
| [#24](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/24) | FA + TS / TO-001 room icon | **In Review**: latest approved visual source; native game floor/UI L4 pending |
| [#25](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/25) | TS / TO-002 dependency graph | **Blocked**: no safe verified additive node/edge API; read-only probe only |
| [#26](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/26) | TS + FA / TO-003 terminology | **In Progress**: G1 source labels checked, complete device/G2 bilingual UI and owner L4 pending |

The completed TO-004 V3 visual/prebuilt-room milestone is tracked in **closed Issue #30**, without incorrectly reopening it just because Draft PR #31/#35 remains unmerged.

## Remaining 19 open PRs — grouped by actual deliverable

| Workstream / dependency | Live PRs | Review gate |
| --- | --- | --- |
| G1 / core and evidence | [#7](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/7), [#23](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/23) | R3 preserved; evidence/main sync and pending panel gate; no release |
| G2 / medically experimental source, icons, GM, trusted L3 | [#43](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/43) → [#44](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/44); [#45](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/45) built on G1 #7; [#46](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/46) | Strict C2 diagnosis remains blocked; V1 ZIP withdrawn; #46 is privileged CI Draft and needs explicit owner review; no G2 L3/L4 |
| ART-001 / visual source and standalone devices | [#14](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/14), [#40](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/40) → [#42](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/42) | Actual FA source pinned; independent 4-direction device interaction/staff L4 pending |
| TO-001 / room menu, logistics and floor | [#28](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/28), [#29](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/29) → [#36](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/36) | Distinct status-bar path and approved floor resource; native game L4 pending |
| TO-002 / read-only graph probe | [#32](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/32) | No graph node implementation and no fake GO |
| TO-003 / G1 language tests | [#27](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/27) | Test-only source; still needs integration into complete bilingual contract |
| TO-004 / V3 prefabs | [#31](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/31), [#35](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/35) | Owner-reported 6/6 V3 room L4; approved source frozen; stage and integration separate |
| Governance / main plan and dependency automation | [#22](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/22), [#33](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/33), [#37](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/37) | #22 Dependabot compatibility; #33 authoritative plan review; #37 D015 not yet approved, C2 unresolved |

The child/parent arrows indicate source dependency, **not permission to auto-merge**. For the G2 code, PR #44 and #45 are siblings from different baselines; they are not one directly mergeable implementation.

## Four archived PRs after exact-source triage

These PRs were closed **without merge** and with explicit GitHub comments, not deleted:

- [#34](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/34): withdrawn combined TO+FA game-test package; owner-reported visual L4 failure. **Do not install old ZIP.**
- [#39](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/39): earlier workbench attachment study superseded by owner's selected integrated-base standalone machines (#40/#42). Its original-engine findings remain useful.
- [#38](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/38): independent GM draft absorbed into current G1 #7. Matching documentation/test Git blobs verified.
- [#41](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/41): disabled C1 GM fixture absorbed into current G1 #7. C# source, docs and core unit-test Git blobs verified.

This is **not a claim that all G1/G2 clinical work has passed game L4**.

## Branches with no open PR

**11 merged-PR branches; cleanup candidates after permission and a ref/lineage check:**
`chore/group-dependabot-actions`,
`chore/security-tooling`,
`ci/automate-g1-verified-net35`,
`ci/conditional-low-risk-automerge`,
`ci/g1-encrypted-public-build`,
`ci/g1-verified-builder`,
`docs/complete-gov-001`,
`docs/mobile-review-guide`,
`docs/project-governance-v1`,
`docs/sync-g1-art-governance`,
`docs/ts-fa-workflow`.

**6 branches for closed/unmerged PRs, preserved as history:**
`ci/art-asset-contract` (#15),
`dependabot/github_actions/actions/checkout-7` (#13),
`feature/ts-tofa-unified-l4` (#34),
`feature/ts-art001-attachment-preflight` (#39),
`feature/clin001-c1-gm-test-harness` (#38),
`feature/clin001-c1-private-mobile-fixture` (#41).

Do **not** delete these six merely to make the branch count smaller; archive or verify that all meaningful code and evidence have an independent permanent home.

## Preventing a recurrence

1. Every top-level Issue represents a unique deliverable/acceptance goal; investigation iterations or CI failures are **comments/commits within existing Issues/PRs**, not new top-level Issues.
2. Prefer **one active PR per independently reviewable change**. A child Draft PR is justified only for a true different codebase/branch dependency (e.g. approved FA art or separately privileged CI).
3. A new candidate that supersedes a failed/withdrawn one must link and close the old Draft PR, with explicit reason and preserved failure evidence. Never label a CI success as L4.
4. Review existing PR head, source SHAs, frozen decisions and the canonical plan **before** opening another branch or Issue.
5. Close a PR as merged only when GitHub says `merged_at` is set. Closing a duplicate without merge must explain where the source was absorbed; do not silently assume it reached `main`.
6. Delete a branch only after its PR is merged, its ref is not the base or head of any active PR, and all unique commits/resource hashes are preserved. The `main` branch is never a cleanup target.
7. Source-only PR closure is not feature completion; keep its parent Issue open until native L3/L4/compatibility gates are met. No core/CI/plan automatic merge beyond D014's narrow approved class.

**Tool limit:** This audit connection supports closing PRs and editing tracked docs but does not expose a branch-delete operation. Hence these branch names are cleanup candidates, not claimed deletions; no history was destroyed.
