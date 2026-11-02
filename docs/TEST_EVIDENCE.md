# Test Evidence and Claims

Never convert source-level plausibility, a green workflow or third-party examples into an assertion of working gameplay. Each result must identify the tested SHA/package, game build, DLC/Workshop set, environment, steps, expected/actual result, and raw logs/screenshots when available.

## Current evidence baseline (2026-11-01)

| Test | Source and type | Result | Limitation |
| --- | --- | --- | --- |
| G0 disposable CBC in a fourth lab | User's direct in-game report in the predecessor conversation | Reported PASS: fourth room appeared and CBC workflow returned a result | No saved raw output log, game version or reproducible save/load report available here; does not validate G1 |
| G1 independent blood-lead examination | G1 test package/source candidate in predecessor conversation | NOT TESTED / BLOCKED | New test IDs and lead-case flow not demonstrated in actual game |
| G1 patient-spawn panel compilation | Previous Windows installer error screenshot | FAILED / NOT COMPILED | Required legacy C# compiler not found. No genuine game-DLL L3 success recorded |
| G1 GItHub Actions build | Proposed only | NOT RUN | Public repository CI must not assume access to proprietary game references |
| Original-device art acceptance | Not delivered | NOT TESTED | No original interactive equipment approved |
| Four DLC / Workshop / save-load regression | No ABCL L4 matrix | NOT TESTED | Do not claim compatibility or safe uninstall |

## Four evidence levels

- **L1 — unit/logic:** test command, negative cases, results, tested SHA.
- **L2 — data/source/assets:** XML parser, all referenced IDs resolved, room/equipment/medical linkage, atlas/pivots/directions and test failures.
- **L3 — game-compatible build:** real game assembly hashes, compiler/target metadata, exact successful build job and artifact hash. No public upload of game binaries.
- **L4 — gameplay:** human-run test or recorded game run, settings, exact actions, diagnosis/treatment outcome, save/load, baseline regressions, screenshots and output log.

`Verify` initially validates policy files, absence of proprietary compiled artifacts, and any future tracked XML syntax. It **does not** compile a game DLL or run in-game tests.

## L4 case template

```text
Date:
Commit/package SHA256:
Project Hospital build:
DLCs enabled:
Other mods enabled:
Save type (new/existing/disposable):
Scenario and prerequisites:
Steps performed:
Expected:
Actual:
Result (PASS/FAIL/BLOCKED):
Raw log / screenshot references:
Known limitations:
```

## Required G1 gameplay cases

1. New ABCL blood-lead sampling appears for a valid lead-poisoning patient.
2. Sample reaches a staffed ABCL toxicology lab; specialist interacts with an actual required instrument.
3. Lab result returns to the physician and contributes to the diagnostic path.
4. Original CBC still processes at the original hematology lab.
5. Save, close, reopen and reload preserve functioning laboratory tasks and rooms.
6. Test-only spawn controls are off or absent in release configuration.


## ART-001 first owner L4 placement report — 2026-11-02

**Exact tested artifact, as reported by owner**
- Actions artifact ID: `13124027790` (`ABCL-ART001-PLACEMENT-TESTONLY`), Actions run [41408148144](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41408148144).
- Source SHA embedded in the tested package: `1fa723d336f95b27762a202a34aab9c64d003504`.
- This is the original art-only test package, not any later Draft PR #14 commit. The package lacks the later issue-fix changes; do not assign this report to a future candidate.
- Owner supplied a checklist result in chat with no screenshot, matching game log, placement-validation error string, game build, DLC list or additional fault description. **Do not invent those details.**

| # | Owner test item | Actual reported status |
|---|---|---|
| 1 | Game started and entered disposable hospital | **PASS** |
| 2 | Build menu showed both ABCL objects | **PASS** |
| 3 | Equipment names/descriptions displayed normally | **PASS** |
| 4 | Both objects could be placed on a laboratory workbench | **FAIL** |
| 5 | Both objects rendered correctly in all four game rotations | **FAIL** |
| 6 | Scale/occlusion/character-table contact | **BLOCKED** |
| 7 | Nearby staff could still walk normally | **BLOCKED** |
| 8 | Original hematology analyzer and other original equipment unaffected | **BLOCKED** |

**Aggregate:** 3 PASS, 2 FAIL, 3 BLOCKED. **ART-001 L4 placement acceptance = FAIL / NEEDS_FIX.** No staff execution or native procedure routing was attempted. The three blocked items are *not* PASS, and G1 R3's separately accepted patient/CBC test is not substitute evidence for ART-001 item #8 in this run.

**Source-grounded diagnosis after report**
- The staged ART-001 objects declare `AttachedToObject=true` and only `abcl_art001_icp_ms`, `abcl_art001_digestion` (plus generic `ui_*` and `equipment`) tags.
- Vanilla `Lopital.Floor.CanPlaceObject` returns `NOT_ALLOWED_ATTACHMENT_NO_PARENT` without a center/parent table object, and `NOT_ALLOWED_ATTACHMENT_WRONG_PARENT` if that parent has no `AttachmentSlot` or its `AllowedTags` do not match the object tags.
- Vanilla `GameDBObject.AcceptsAttachment` checks for **at least one exact string match** between the parent's `AttachmentSlot.AllowedTags` and the child object's tags.
- The original `OBJECT_TABLE_EQUIPMENT` and `OBJECT_TABLE_SQUERE` tables allow known vanilla tags such as `hematoanalyzer`, `RIA`, `lab_eq_small`, etc. They do **not** list either ART-001 namespaced functional tag, and the object definitions contain none of those allowed tags. Therefore placement onto those unmodified tables will be rejected by original `CanPlaceObject`. This is a verified *contract defect*, not an art-asset loading defect.
- The original equipment-table parent has `ForcesAttachmentOrientation=true`. The source of `Floor.CanPlaceObject` may override the child's direction to match that parent. The owner's four-direction FAIL is retained exactly, but without a screenshot of the rotation UI or a successfully placed object the precise independent rotation behavior is not established.
- Avoid adding general vanilla tags such as `hematoanalyzer`, `RIA` or `lab_eq_small` just to get through `AllowedTags`: this risks altering vanilla procedure equipment resolution, particularly CBC or unrelated Workshop labs. Prefer a dedicated **ABCL-only attachment parent** accepting only the two new tags and not re-registering any vanilla object; verify the changed result in a *new* exact-source candidate before further game testing.

**Next gate:** prepare an additive isolated attachment-parent fix in the ART-001 Draft branch, add static tests that independently model the original AllowedTags/AcceptsAttachment rule and forced-orientation flag, then rebuild and audit one new art-only package. No further owner L4 test is requested at this stage; the already passed R3 clinical patient/ambulance/sampling/chelation sequence is not repeated. Keep Issue #3 open and PR #14 Draft; no merge, release or blanket compatibility claim.
