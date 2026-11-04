# Test Evidence and Claims

Never convert source-level plausibility, a green workflow or third-party examples into an assertion of working gameplay. Each result must identify the tested SHA/package, game build, DLC/Workshop set, environment, steps, expected/actual result, and raw logs/screenshots when available.

## Current cross-workstream checkpoint (2026-11-02)

This checkpoint supersedes the **status** of the older 2026-11-01 baseline below without deleting or altering its historical evidence.

| Workstream / gate | Evidence | Status and remaining limitations |
| --- | --- | --- |
| TS / G1 R2 laboratory-only fixture | Owner-reported **14/14 real game L4** for test-only fixture on source `7f3c5f29cebd39338df854a1475ceb604dca164f`, [Actions 41377881918](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41377881918). User-reported scenarios included Emergency clinic availability, installed R2 package, native patient arrival, ABCL sampling/analysis and baseline CBC in a disposable test save. | **Owner-reported R2 fixture L4 PASS, not independent log-verified:** exact game build, DLC list, artifact/dll hash, and complete raw logs/screenshots were not preserved in this record; the reported 14/14 is an owner-performed gameplay checklist rather than the 14 unit tests. L3 compilation run link is recorded, but this row is not independent proof of package audit details. R2 is **not** a positive native lead-toxicity case or releasable configuration; later R3 is separate. Re-scope decision: `ABCL-D013`. |
| TS / G1 R3 core clinical flow | Genuine net35/CLR2 compilation [41391983195](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41391983195), source `1a13e8d9ccc41fbf2a86f9c36dcb07b75b477d2b`, test-only artifact `13117942292`; owner report recorded in [Issue #2](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/2) | **Owner-reported L4 PASS:** native TRM_LDP creation, ambulance arrival, Internal Medicine admission, ABCL sampling, staffed toxicology analysis, result returned, chelation, original CBC, save/quit/reload. No independent logs/screenshots, exact game build or DLC list supplied. No all-DLC/Workshop/uninstall/legacy-save acceptance. |
| TS / read-only panel extension | Source `7faf31c6bba34ab58a9e288217d0359956bd2af2`, [Verify 41403021576](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41403021576), CodeQL and Python analysis reported PASS in PR #7 | **Exact-SHA genuine L3/package audit pending**; prior R3 artifact predates read-only Liver TY/ICU/quota diagnostics. After passing L3, require *focused panel display/preflight only*, not repeat of the whole R3 clinical L4. No new compiled success is claimed. |
| FA / ART-001 original devices | [PR #14](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/14), V7–V10 source-only original art preview iterations have been recorded; exact newer asset state must be checked on FA PR #14 | **Owner visual acceptance pending; revised ART-only L4 NOT RUN.** First actual art test remains **3 PASS, 2 FAIL, 3 BLOCKED** (workbench placement and four-direction rotation failed). Preview is not a native screenshot or installable artifact. Decisions `ABCL-D011` and `ABCL-D012` govern art. |
| FA / art export checks | [PR #15](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/15) | Source-only CI scope; no implicit game interaction acceptance, installation or release. |

**Release remains prohibited.** G1 test-only spawn control may not ship in Alpha. The accepted clinical user report does not remove the art, compatibility or release gates.


## 2026-11-04 integration regression and owner-approved art freeze

Direct owner report: the 2026-11-04 complete R1/R2/R3 integrated test packages regressed the room icon UI (looks transparent, should show already-approved opaque red), the floor UI hookup and previously accepted device/prefab experience. **Do not treat the R3 package as L4 PASS.** User supplied `Assets.rar` with five approved PNGs; SHA-256 byte-comparison to R3 ZIP matched **5/5**. Both room-menu source PNGs have alpha 255 for every 64x64 pixel, proving **the package art is not transparent**; real UI display remains broken or loads a different binding. R3 ART machine atlas hash `a5bad4aa...` differs from approved source atlas `b412b384...` and still registers the old three-object attachment workbench; this is a definite packaging regression. Correct standalone source candidate exists in TS Draft PR #42. Exact hashes, file paths, and source/API constraints are frozen in [OWNER_ART_FREEZE_20261104.md](OWNER_ART_FREEZE_20261104.md). No revised Windows package, owner game retest, or new changed-DLL L3 is claimed.

## Historical evidence baseline (2026-11-01; superseded statuses retained)

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
