# Test Evidence and Claims

Never convert source-level plausibility, a green workflow or third-party examples into an assertion of working gameplay. Each result must identify the tested SHA/package, game build, DLC/Workshop set, environment, steps, expected/actual result, and raw logs/screenshots when available.

## Toxicology icon first-frame and instrument-requirement L4 follow-up — 2026-11-04

**Owner screenshots:** `IMG_9655.jpeg`, `IMG_9657.jpeg`, `IMG_9658.jpeg`. The owner reports that both the room-list icon and floor graphic initially show a vanilla hematology glyph and only *then* change to the dedicated Toxicology glyph; two independent mass spectrometer/digestion machines are *not* mandatory and the toxicology room still copies the vanilla hematology equipment requirements. The owner did not provide an exact package SHA in this screenshot turn, so these observations must not be attributed to a specific later build without confirmation. The previous explicit `RestoreFix` checklist (7 PASS / 1 FAIL, exact SHA recorded below) remains separately authoritative for that earlier package.

**Native source root cause:** original `GameDBRoomType` supports only numeric `IconIndex` and `TextureID`, not a `CustomIconAssetRef`. Vanilla department room controls draw the integer `IconIndex` in `UpdateRoomButton`, while the separate ABCL private Sprite adapter updates only afterward. The existing toxicology room used vanilla hematology indices `850` and `376`. Original supplied `StreamingAssets/Textures/ui/icons.png` entries `3070/3071` and `Textures/tiles_4096_atlas.png` tile `491` are fully transparent and not referenced by original/DLC `IconIndex`/`TextureID` declarations. The fallback is now private-room-only `3070/3071` and `491`; the approved original icon/floor design is still supplied by private assets. **No shared original atlas was patched.** An initial blank frame is possible; whether the previously observed wrong-icon flash disappears is **new game L4 NOT RUN**.

**Equipment source root cause:** previous `ModRoomTypes.xml` required `ui_hematoanalyzer`, `ui_ria`, and `thermal_cycler`, but did not require the two private machines. The previous G1 blood-lead lab analysis still used `hematoanalyzer`; fixing room readiness alone would have broken the actual clinical route. Current G1 Draft PR #7 explicitly requires `abcl_art001_digestion` and `abcl_art001_icp_ms` with MinCount=1 each, removes those three **toxicology room** old mandatory tags, and uses the matching private tags in the blood-lead procedure in order: `stat_lab_exam` → digestion → ICP-MS → biohazard disposal → hand hygiene. These exact private object tags were verified in the previously packaged two standalone GameDB objects from owner-submitted FA Draft #14/TS Draft #42. The original CBC, DPT_LAB clinic rooms and all Workshop files are not changed by the overlay. This *does not* establish in-game staff equipment use or result return.

**Test-only ZIP:** `ABCL_TO001_Equipment_And_Icon_Fix_20261104.zip`, SHA256 `332dd92ecc8f89549a0b71a3de608de88f89418c97539d2d4a4d260240311482`, 46 members, all 45 receipt SHA256 values checked, all XML well formed, 2 standalone instrument IDs/tags cross-matched to room requirements and G1 exam steps. Four source changes: `ModRoomTypes.xml`, `ModExaminations.xml`, `ModAssetListsTO001.xml`, and private floor image remapped from tile376 to tile491; private PNG is generated from the same approved FA pixels, not redrawn. G1 C# source Git blob `63bbb4f79e14d6ac35b6fc825c8aefd29b69edb5` remains **identical** to the genuinely compiled prior build from SHA `24d77f2f8ebac16aa9cc54e53cd55efabdc9e26e` ([Windows net35/CLR2 #41772460864](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41772460864)), DLL SHA256 `f32929f9ddad0b1bd8a04e62ce4b4b7bd765604f27106cd29f5c90703b74a149`. The current G1 overlay source `7daad9f9a34338395e12f5eb675faed3d508868d` passed [Verify #41774655575](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41774655575), [CodeQL #41774655353](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41774655353), and [R3 installer isolation #41774655461](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41774655461). This is XML/asset L2 and an unchanged genuine G1 C# L3; **not new gameplay L4**.

**V3 prefab boundary:** original owner-accepted 8×6 and 12×6 prefab XML/previews remain byte-identical and do **not** contain the two new machine objects. Both machines must be added manually after prefab placement to make the room meet the new mandatory equipment rules. A prefab layout V4 requires separate authoring/visual approval, and the historical V3 PASS does **not** prove the new readiness requirement.

**Focused owner L4 still required:** initial correct icon without vanilla wrong-symbol flash; private floor glyph/no wrong-symbol flash/zone colors; exact two mandatory machine counts and room ready only after placement; G1 blood-lead preparation→ICP-MS technician behavior/result (if no legitimate available clinical case, mark NOT TESTED/BLOCKED, do not force GM). Existing historical normal CBC/save/rollback PASS is not automatically invalidated, but changing the toxicology room validity and medical procedure requires focused new L4 before release.

---

## TO-001 room-list icon — latest owner L4 and exact-source repair (2026-11-04)

**Owner-tested package:** `ABCL_TEST_R3_20261104_RestoreFix.zip`, exact ZIP SHA256 `01400d176d180c6ad71da96b398a8ffd170223441a3e2975c6571478d87381c0`. Owner's explicit result: **7 PASS / 1 FAIL / 0 BLOCKED**. No game build, DLC set or other Workshop-mod list was supplied.

| Focused L4 checkpoint | Actual owner result |
| --- | --- |
| Toxicology Laboratory dedicated room-list icon | **FAIL** |
| Isometric floor glyph and original zone colors | **PASS** |
| Both 8×6 / 12×6 prefab names and previews | **PASS** |
| Laboratory staff pathing and room readiness | **PASS** |
| Vanilla hematology and original CBC | **PASS** |
| Ordinary patients diagnosed/treated normally, without GM | **PASS** |
| Temporary save, exit and reload | **PASS** |
| Restore previous ABCL after game exit | **PASS** |

This later user report supersedes only the corresponding status of the earlier mixed 8 PASS / 1 FAIL / 4 NOT TESTED report; it does not erase that earlier exact-SHA evidence. **Do not repeat these seven passed scenarios simply to validate a private room-list icon code change.** No game-wide/DLC/Workshop compatibility claim is inferred.

**Original-game code evidence:** the owner's ILSpy `DepartmentManagementLogisticsHybridController.CreateRoomButton()` places `BuildingModeButtonController` on the Button child of each **root** room-button prefab. Vanilla `UpdateRoomButton(root,...)` independently resolves `SegmentItemIconTextTextIconController` from that same root. The earlier ABCL adapter erroneously resolved `BuildingModeButtonController` *starting from the segment component*, requiring an unproved ancestor relationship. The fixed adapter walks the four original `m_roomButtons*` root collections, verifies exact private RoomId `ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB`, gets the icon segment from the root, and revalidates its cached root on department switching. No original shared `IconIndex`, other room, palette/material, medical treatment or shared GameDB entry is changed.

**Source and genuine build:** current [Draft PR #7](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/7) exact source SHA `24d77f2f8ebac16aa9cc54e53cd55efabdc9e26e`. [Verify](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41772427098), [CodeQL](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41772427088), [Windows R3 installer isolation smoke](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41772427092) and **genuine Windows net35/CLR2 compile** [#41772460864](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41772460864) all **PASS**. Artifact `13295238120`, new ABCL DLL SHA256 `f32929f9ddad0b1bd8a04e62ce4b4b7bd765604f27106cd29f5c90703b74a149`.

**Chat-delivered focused package:** `ABCL_TO001_RoomIcon_Fix.zip`, SHA256 `c3f846cc199661df98737de1133b75c971b9645c8f5838b19d12c26a97fba522`. Repacked from exact `ABCL_TEST_R3_20261104_UTF8Fix.zip` (SHA256 `d0f96ecca6f7df1f05cc5b4a29ad56dea145ee2824647d49ecd669670e69b7c2`). Of the 26 game-addon files only the ABCL-produced DLL changes; two test-note files and the SHA manifest also change. ZIP CRC, all XML parsing and manifest file receipts **PASS**. Windows PowerShell 5.1 explicit UTF-8 install and guarded rollback are unchanged.

**New candidate targeted room-list icon game L4: NOT TESTED.** Next owner check only the dedicated row icon in the active lab department and that it does not leak to other department room-list icons; test locked/unlocked state if available. Parent Issue #24 and core PR #7 remain open/Draft pending this result. No additional standalone equipment or general patient/GM run is needed.

---

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

### Integrated installer UTF-8 decoding regression (2026-11-04)

**Owner-provided evidence:** first installation attempt of `ABCL_TEST_R3_20261104_RestoreFix.zip` (SHA256 `01400d176d180c6ad71da96b398a8ffd170223441a3e2975c6571478d87381c0`) on Windows showed `Install-ABCL-Integrated.ps1:71` rejecting the Chinese TO-004 string-table XML as malformed. The original XML was independently parsed as valid UTF-8; `Get-Content -Raw` in Windows PowerShell 5.1 had applied system ANSI decoding to a BOM-less UTF-8 file, turning the two `临床毒理实验室` texts into mojibake. This occurred in installer preflight before moving any ABCL folder.

**Exact fix and package:** both install and restore scripts now use `-Encoding UTF8 -Raw` for all JSON/XML `Get-Content` reads; package owner ID, previous-backup location, G1 DLL and **all 26 game addon files** remain byte-identical. Rebuilt chat-delivered `ABCL_TEST_R3_20261104_UTF8Fix.zip`, SHA256 **`d0f96ecca6f7df1f05cc5b4a29ad56dea145ee2824647d49ecd669670e69b7c2`**, has 46 ZIP entries and passes XML parsing, CRC, per-file SHA256 receipt, exact ABCL compiled DLL SHA and change-scope audit. Source patcher is `tools/patch_integrated_r3_utf8.py` in [Draft PR #47](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/47). Real Windows PowerShell 5.1 BOM-less Chinese XML parse, patch tamper-negative tests and synthetic rollback [Actions #41771255628](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41771255628) **PASS**, current PR #47 exact head `40f087359b5ef9413d7134aacf35fa937f7984e2`; [Verify](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41771255445) and [CodeQL](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41771255668) PASS. **Owner full-game installation and L4 on this hotfix: NOT TESTED.** This is an installer-only regression, not justification for rerunning medical G1 R3 or reopening the retired Super-GM route.

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
