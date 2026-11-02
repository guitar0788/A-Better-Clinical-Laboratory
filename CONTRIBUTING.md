# Contributing to A Better Clinical Laboratory

This repository is public. Changes are accepted only when they improve a verifiable part of the mod. The [master plan](docs/MASTER_PLAN.md) is the source of truth for scope and status; [decisions](docs/DECISIONS.md) record approved or rejected approaches; [test evidence](docs/TEST_EVIDENCE.md) records what actually ran.

## Workstreams and ownership

Development responsibilities are split between **TS (Technical & Systems)** and **FA (Fine Arts)**. Read the [TS / FA Development Workflow](docs/TEAM_WORKFLOW.md) before coordinating tasks or modifying shared interfaces. The repository owner remains responsible for final acceptance, merging and releasing.

## Before starting any task

1. Check the master plan for an existing task, completion status, and owner.
2. Check the decision log for frozen requirements and rejected implementations.
3. Reuse existing research and test evidence.
4. Reinspect original game code only when a conclusion is disputed, essential evidence is missing, or a feature is about to be implemented.
5. Open or update one scoped Issue. Do not create duplicate research Issues.

## Branches and pull requests

- `main` is the only integration branch. Except for the empty-repository initialization commit, do not push development changes to `main`.
- Use short-lived `feature/<task>`, `fix/<task>`, `art/<task>`, or `docs/<task>` branches.
- Each PR must link a scoped Issue, explain its change and rollback, and list verification at each evidence level.
- Require the `Verify` check for merging once branch protection has been configured. A green `Verify` means repository checks passed, not that a game DLL compiled or the mod worked in-game.
- No force-pushes to `main`, deletion of `main`, or automatic merging of gameplay, art, infrastructure, security, release, planning or evidence PRs. Under **ABCL-D014**, only explicitly TS-approved, low-risk docs/non-clinical tests may auto-merge through the [protected-main allowlist](docs/AUTO_MERGE_POLICY.md) after exact-SHA checks. The owner retains final acceptance of major changes and releases; initial required approvals: zero.
- Record the tested commit SHA. After changes, retest the new SHA; never reuse earlier CI/L4 results.
- Avoid speculative scaffolding, empty test stubs, and broad refactors unrelated to the Issue.

## Issue states and acceptance

Use **Backlog → Ready → In Progress → In Review → Done**; **Blocked** indicates an unresolved dependency. Cancelled items are closed with an explicit reason. Research completion is not feature completion. Close a feature Issue as complete only when its stated acceptance criteria are satisfied; otherwise record the blocker or a separately linked follow-up.

An Issue must state the goal, allowed files, existing evidence, dependencies, test steps, expected result, failure/stop rule, and rollback. Do not assign multiple dependent tasks to active development at once.

## Implementation and compatibility

- Use the original game's supported adult models, employee and clinical AI, laboratory sample workflow, and save structures.
- New IDs are namespaced with `ABCL_`. Document all intentional overrides of existing game IDs, especially `DPT_LAB`, diseases, symptoms, and examinations.
- Add the sampling ↔ testing ↔ room/equipment ↔ symptom/disease relationships as one reviewable change.
- Preserve baseline hematology, microbiology, histology and CBC functionality; test them when a shared definition is overridden.
- A specific incompatibility with a Workshop mod (including HAO) is acceptable only when declared. It does not excuse a broken vanilla game or undocumented save risk.
- Never modify original installed game files. Do not copy proprietary game assemblies or game assets into this repository.
- A C# mod must be compiled against genuine, legally obtained game references with the correct runtime target; .NET 8 or fake-reference tests are not L3 evidence. A private build process must not expose game binaries in logs or public artifacts.
- Test-only patient spawning must be clearly isolated and must not ship enabled in production.
- Do not introduce Harmony hooks unless a precise, game-source-backed requirement and noninterference test justify them.

## Art requirements

Original or properly licensed art only. Four-direction assets must be reviewed for proportions, pivots, occlusion, interaction points and in-game animations. Placeholder assets, screenshots and XML syntax checks are not final art acceptance. Game-visible and usable interaction must be tested at L4.

## Evidence and releases

- **L1:** actual logic tests and negative cases.
- **L2:** XML IDs/references, source contracts, asset validation.
- **L3:** genuine target-framework compilation against legitimate game references, including SHA evidence.
- **L4:** real Project Hospital gameplay: setup, steps, logs/screenshots as relevant, save/load and regression cases.

A passing workflow only covers the tests that actually ran. Use [test evidence](docs/TEST_EVIDENCE.md) for all claims and [release policy](docs/RELEASE_POLICY.md) for Alpha gating. Stop a blocked core feature after one well-scoped, evidence-backed correction attempt; do not turn it into indefinite research.
