# Test Evidence and Claims

Never convert source-level plausibility, a green workflow or third-party examples into an assertion of working gameplay. Each result must identify the tested SHA/package, game build, DLC/Workshop set, environment, steps, expected/actual result, and raw logs/screenshots when available.

## Latest owner L4 and corrected integration checkpoint (2026-11-04)

**Package actually tested by owner:** `ABCL_G1_ART_TO004_TEST_20261104_G1-22db2f.zip`, SHA256 `e4c2fbc77af26aeee71736062ced7fc4e5198b7e1184c79fe2e3b6b53ad2e7ca`. Owner's exact checklist: **PASS 8 / FAIL 1 / BLOCKED 0 / NOT TESTED 4**. The recorded FAIL was item 08 (prefab menu/preview/name). The photos additionally document diagnosis/treatment failure after a Super-GM-created patient, and the owner separately reported missing TO-001 menu/floor icons and effects on other patients. These independent observed defects are **not** silently converted into PASS or folded into the score.

| Exact checklist item | Owner result | Scope and outstanding evidence |
| --- | --- | --- |
| 01 Install and back up prior ABCL | PASS | Owner-tested package only |
| 02 Game loads and G1 panel visible | PASS | Owner-tested package only |
| 03 Toxicology room selectable; requirements | PASS | Owner-tested package only |
| 04 Two standalone machines appear and place | PASS | Owner-tested package only |
| 05 ICP-MS all NW/NE/SE/SW views | PASS | Owner-tested package only |
| 06 Digestion station all NW/NE/SE/SW views | PASS | Owner-tested package only |
| 07 Device scale/perspective/ground contact | PASS | Owner-tested package only |
| 08 Two prefab menu names/previews | FAIL | Vanilla appends dimensions; localized text duplicated them |
| 09 Prefab placement, rotation and access | PASS | Owner-tested package only |
| 10 Staff pathing and room readiness | NOT TESTED | Remains open |
| 11 Vanilla hematology and CBC | NOT TESTED | Remains open |
| 12 Disposable save / exit / reload | NOT TESTED | Remains open |
| 13 Restore previous ABCL after game exit | NOT TESTED | Remains open |
| Extra: GM-created patient and noninterference | FAIL / reported side effects | The C1 fixture had no native main symptom; original factory also registered patient with insurer. Retired from current test candidate. |
| Extra: TO-001 room and floor icons | MISSING IN TESTED BUILD | New assets integrated, **not** retested in game |

**Precise source remediation:** the C1 test condition used four original symptoms with `IsMainSymptom=false` and thus lacked a valid main symptom for native diagnostic/treatment presentation. The generic test `DIA_CLD` override could also affect ordinary patients sharing that diagnosis. The current G1 test source has removed Super-GM/C1 and the generic R2 override; only preflighted native `TRM_LDP` R3 remains. G2 Cd/Hg cases are **not** included in the refreshed package.

**New exact G1 L3:** current [Draft PR #7](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/7) head `32fd883c99a62a207cf6b4be0dbfd6bd5b6be809` genuine Windows net35/CLR2 build [Actions #41752846916](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41752846916), artifact ID `13286912693`, ABCL-only DLL SHA256 `c02cbb8cbfaa6a32a1887d52378537e5c9a78168f3d2078e31ac0e84f18fbe0a`. Verify, CodeQL and synthetic R3 installer isolation passed. No proprietary original assemblies were included in the package.

**TO-004 naming correction:** [source SHA `9130c7a3241315d1b73e8bcfdf4cc2f560cd9804`](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/31); both EN/zh-Hans names omit embedded width/height because vanilla adds the size once. Source, CodeQL, and Windows mock overlay validation passed in [Draft PR #47](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/47). The owner-approved original two prefab geometry/preview files and eight device frames were preserved.

**Restoration correction and synthetic proof:** the initial integrated R3 wrapper `ABCL_TEST_R3_20261104.zip` had a mismatched package owner identifier in `Restore-ABCL-Previous.ps1`; its rollback path was invalid. A corrected and independently hash-audited test archive `ABCL_TEST_R3_20261104_RestoreFix.zip` has SHA256 `01400d176d180c6ad71da96b398a8ffd170223441a3e2975c6571478d87381c0`, with all **26 addon files byte-identical** to the G1 R3 integration candidate. The exact restore script has been committed in PR #47, Git blob `e244c53f0c32f7ecf4e8692c03d66cac441839a4`. [Windows synthetic backup/restore tests](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41754984759) cover successful replacement, absence of a prior version, wrong owner receipt, missing backup, corrupted managed file and preservation of an unrelated Workshop test folder. **This is a Windows mock PASS only**, not actual game L4 or an assurance about real saved games.

**Combined new candidate L4: NOT RUN.** Do not start patient-generation testing for the retired Super-GM. Native staff work, CBC, original patient noninterference, save/load, restored prior ABCL, game build, DLC set and Workshop matrix remain unverified for the current candidate. Alpha release remains prohibited.

---

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
