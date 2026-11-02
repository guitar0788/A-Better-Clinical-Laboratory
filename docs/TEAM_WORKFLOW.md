# TS / FA Development Workflow

**Project:** A Better Clinical Laboratory (ABCL)  
**Version:** 1.1  
**Workstreams:** TS (Technical & Systems) and FA (Fine Arts)  
**Status:** Active governance document; ABCL-D014 adds a tightly scoped owner-approved low-risk auto-merge exception.

This document coordinates work across separate development conversations. A workstream is a persistent responsibility, **not** a permanent chat session or a GitHub account. Chat messages do not automatically synchronize across conversations. Both workstreams must reread repository records rather than assuming that the other conversation received a message.

## 1. Ownership and responsibilities

### TS — Technical & Systems

TS coordinates the technical implementation and integration:

- C# gameplay code, clinical logic, native game interfaces and secure builds.
- Vanilla game, declared DLC and Workshop compatibility and regression testing.
- The canonical plan, approved decisions, Issue/PR coordination and evidence records.
- Integration and technical review of FA deliverables; L3 and L4 test coordination.
- Release preparation, without bypassing the project owner's approval.

TS may review art integration but should not duplicate FA's asset-authoring work. **The repository owner retains final visual acceptance, merge and release authority.**

### FA — Fine Arts

FA owns the original visual resource pipeline:

- Research of the game's device art conventions, scale, perspective and visual quality.
- Original device concepts, editable vector/source art, directional views, texture atlases, previews and necessary animation assets.
- Art generation and validation scripts, source-only preview workflows and visual corrections.
- Precise handoffs that include assets, source hashes, previews, relevant CI results and known limitations.

FA must not independently change G1 clinical logic, patient generation, core native hooks or gameplay interfaces. Any gameplay or resource-registration requirement that crosses that boundary is submitted to TS before implementation.

## 2. Sources of truth and order of investigation

Before starting a task, check in this order:

1. [Canonical development plan](MASTER_PLAN.md): task, existing owner, state and dependencies.
2. [Approved decisions](DECISIONS.md): frozen requirements and previous stop decisions.
3. [Recorded test evidence](TEST_EVIDENCE.md) and existing research: reuse established findings.
4. The relevant Issue, PR, latest commit SHA and Actions results.
5. Original game source only when past evidence is disputed, a critical fact is missing, or implementation requires exact confirmation.

GitHub is authoritative for *saved* work; an unsent chat response or a green CI job is not evidence of a new accepted feature. If records differ, resolve the discrepancy explicitly rather than silently overwriting history. Follow [CONTRIBUTING.md](../CONTRIBUTING.md) and the [release policy](RELEASE_POLICY.md).

## 3. File and branch ownership

| Area | Primary workstream |
| --- | --- |
| Core C#, examinations, treatments, spawner and native/game integration | TS |
| Secure compile, gameplay regression and compatibility checks | TS |
| SVG, original PNG/atlases, art source and visual previews | FA |
| Art export scripts, source-only art preview and validation CI | FA |
| Shared XML registration, object placement, pivots and interaction interfaces | Coordinate through TS before changing |
| Plan, decision log, evidence and release readiness | TS maintains; FA supplies art evidence |

Avoid simultaneous edits to the same file. When a cross-boundary change is required, document the exact affected paths, interface assumptions and accountable workstream before writing code.

Use short-lived task branches and existing scoped PRs. **Do not create a new PR for every small revision.** Only an exact-SHA, TS-approved, safe-path documentation/non-clinical-test PR may auto-merge under [ABCL-D014](DECISIONS.md) and the [low-risk merge policy](AUTO_MERGE_POLICY.md). No automatic core/art/security/CI/governance merge, release, force push to `main`, or untested installable package.

## 4. Current task routing

These are workstream ownership references, not declarations of completion:

- **PR #7 — TS:** G1 clinical implementation and its evidence.
- **PR #14 — FA:** ART-001 original device art, visual review and source preview.
- **PR #15 — FA:** cloud art-source export and contract validation.

The owner and TS must recheck each PR's live state before assigning new work. Do not duplicate an existing task or conflate clinical acceptance with art acceptance.

## 5. Art, gameplay and compatibility gates

Art should match Project Hospital's smooth, detailed, coherent device presentation; a 128×128 native atlas cell is **not** a request for coarse pixel-art styling. Require appropriate scale, perspective, material/shadow detail, directional consistency, attachment geometry, interaction position and staff access. Player-visible equipment names should remain neutral; keep internal IDs namespaced. Use original or properly licensed resources; do not commit or redistribute proprietary game art or plaintext DLLs.

A source-only preview, SVG/PNG contract check or successful Actions run proves **only the checks performed**. It cannot establish in-game placement, rotation, occlusion, pathfinding, staff interaction or save/load behavior. The owner must approve visual quality; real Project Hospital L4 testing is required for gameplay claims.

Preserve vanilla CBC and laboratory behavior. Consider official DLCs and Workshop interoperability. Document intentional vanilla XML overrides and any unsupported third-party combinations per the decision log; do not promise universal compatibility or unqualified save rollback safety.

## 6. Milestones, evidence and handoff format

Work in small, verifiable stages:

**Check existing state → implement a scoped change → validate → commit → report.**

After **each verified stage**, report:

- Task and scope; exact branch and commit SHA.
- PR and Actions run links, with actual pass/fail/pending results.
- Preview location or tangible deliverables, if applicable.
- Evidence level (L1/L2/L3/L4), and what was **not** tested.
- Status: **PASS / NEEDS_FIX / BLOCKED / NOT_TESTED**.
- Next responsible workstream and any dependencies.

Do not describe uncommitted work as saved or a proposed fix as game-verified. TS reviews FA's output for technical integration; the owner remains the final visual approver.

## 7. Chat interruption and continuity

If a conversation appears stuck or exceeds a reasonable interactive interval without visible progress:

1. Preserve the original conversation and its link.
2. Check actual PR changes, commits, Actions, and saved evidence.
3. Avoid blindly replaying possibly completed writes.
4. If necessary, stop the stalled response and continue in the same conversation, or start a replacement conversation with the **same TS/FA role**.
5. Recover only unfinished work from the last verified GitHub checkpoint.

A new chat does not automatically notify the other chat, and neither role can assume background execution after a stalled turn. The owner may relay a short Chinese handoff to FA; public repository governance remains in English.

## 8. Acceptance and release control

The owner approves final visual direction, high-impact merges and releases; TS provides SHA-bound review of qualifying editorial/test-only changes, which may then merge automatically without owner clicks under D014. TS coordinates integration and verifies evidence; FA delivers original, reviewable art. Preserve existing protected-`main`, Verify, security, proprietary-reference handling and release gates. The low-risk exception changes **merge mechanics**, not the approved Alpha scope, G1 medical logic or game acceptance evidence.
