# Test Evidence and Claims

Never convert source-level plausibility, a green workflow or third-party examples into an assertion of working gameplay. Each result must identify the tested SHA/package, game build, DLC/Workshop set, environment, steps, expected/actual result, and raw logs/screenshots when available.

## Current cross-workstream checkpoint (2026-11-02)

This checkpoint supersedes the **status** of the older 2026-11-01 baseline below without deleting or altering its historical evidence.

| Workstream / gate | Evidence | Status and remaining limitations |
| --- | --- | --- |
| TS / G1 R2 laboratory-only fixture | Owner-reported **14/14 real game L4** for test-only fixture on source `7f3c5f29cebd39338df854a1475ceb604dca164f`, [Actions 41377881918](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41377881918). User-reported scenarios included Emergency clinic availability, installed R2 package, native patient arrival, ABCL sampling/analysis and baseline CBC in a disposable test save. | **Owner-reported R2 fixture L4 PASS, not independent log-verified:** exact game build, DLC list, artifact/dll hash, and complete raw logs/screenshots were not preserved in this record; the reported 14/14 is an owner-performed gameplay checklist rather than the 14 unit tests. L3 compilation run link is recorded, but this row is not independent proof of package audit details. R2 is **not** a positive native lead-toxicity case or releasable configuration; later R3 is separate. Re-scope decision: `ABCL-D013`. |
| TS / G1 R3 core clinical flow | Genuine net35/CLR2 compilation [41391983195](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41391983195), source `1a13e8d9ccc41fbf2a86f9c36dcb07b75b477d2b`, test-only artifact `13117942292`; owner report recorded in [Issue #2](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/2) | **Owner-reported L4 PASS:** native TRM_LDP creation, ambulance arrival, Internal Medicine admission, ABCL sampling, staffed toxicology analysis, result returned, chelation, original CBC, save/quit/reload. No independent logs/screenshots, exact game build or DLC list supplied. No all-DLC/Workshop/uninstall/legacy-save acceptance. |
| TS / protected-main G1 auto-build / packaging | [PR #19](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/19) merged as `82a23174c1ad0af23e75036f5112660560f07c42`; protected-main **push Verify** [41495795717](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41495795717) SUCCESS **for main merge** `82a23174c1ad0af23e75036f5112660560f07c42`, which triggered the first auto-build; the **independent PR #7 candidate Verify** [41460295218](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41460295218) SUCCESS for candidate `aa3e7b163b05f78b24ca5fdfeba4baba07953012` and the protected job independently re-authorized that current PR SHA before Windows [auto-build 41495833103](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41495833103) SUCCESS; artifact `13165179364`. [Independent binary, ZIP and reference-hash audit](G1_AUTO_BUILD_L3_EVIDENCE.md). | **L3 PASS:** genuine Windows `net35`/CLR2 build 0 warnings/errors; ABCL DLL `39db73bd3707700c7aa2adda6004b67408dcea98b271ebf1af241f4288ed8500` (14,848 bytes, `v2.0.50727`); outer artifact SHA256 `3669cc2584890e8839d7b34d230e140716a18d07fcb6b81b2fc0542ca9ca2190`; 10 expected package entries and no plaintext game DLLs / key files. A second complete [Windows auto L3 run 41499553588](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41499553588) SUCCESS for exact PR #7 head `ecd6cc66868fa0ef31320b79eebb0040b8f3f3e8`, artifact `13168800066` outer SHA256 `08fa312951028ddff4997f2991b75bcced426befd6b88f5567dff5592bedceb7`, inner ZIP SHA256 `1543b1f03fcd9512ddf9f6f3363f2936c71eafede25bf8d5163bc4e3fc72fec6`; same 14,848-byte DLL hash as first run, verified eight packaging inputs and no proprietary binaries/keys. Third exact-head [Windows auto L3 run 41548682348](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41548682348) SUCCESS for `63aa4c5ea067e58e2b79e2d1d1a233791224dbd8`; `Verify`, `CodeQL`, `Analyze Python` PASS; produced artifact `13190690403` (outer ZIP SHA256 `f780e9b03c8682ac9c2720c55e0989e45da58c8dd0777789617245bfd4aec716`, inner installer ZIP SHA256 `8240bc06cc933025baff3e06e9cd12f010090dca589dfd586e88469958095578`) and **identical** managed DLL SHA256 `39db73bd3707700c7aa2adda6004b67408dcea98b271ebf1af241f4288ed8500` (14,848 B). The exact updated English and Simplified Chinese clinical labels/descriptions are inside audited five XML files; 10 expected inner entries, zero proprietary game DLLs/Secrets. **Does not prove L4**, DLC compatibility, or Alpha. |
| TS / read-only panel extension | The diagnostic-panel implementation compiled as source `aa3e7b163b05f78b24ca5fdfeba4baba07953012` by [Windows run 41495833103](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41495833103). Later PR #7 README update and protected-main conflict resolution preserved its C# source blob; **preceding exact PR #7 head** `ecd6cc66868fa0ef31320b79eebb0040b8f3f3e8` independently passed a second [Windows run 41499553588](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41499553588) with the same managed `net35` DLL SHA256 `39db73bd3707700c7aa2adda6004b67408dcea98b271ebf1af241f4288ed8500`, newer exact SHA in `BUILD_INFO.txt`, and corrected panel-only test instructions. The latest `63aa4c5ea067e58e2b79e2d1d1a233791224dbd8` changed only the ABCL-owned bilingual **visible** labels/descriptions and added tests validating namespace-safe LocIDs; actual [Windows L3 41548682348](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41548682348) PASS with the **same unchanged DLL hash** and updated XML in packaged artifact `13190690403`. | **Current exact-head L3 and bilingual package audit PASS, panel-only L4 NOT RUN.** Validate only Liver TY / ICU objectives, ambulance inventory, configured-vs-live IMOBILE quota read-only status and no side effects in a disposable save. Do **not** re-run R3 clinical patient/ambulance/CBC/save-load for this read-only change; unsupported DLC/Workshop and release remain unaccepted. |
| FA / ART-001 original devices | [PR #14](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/14), V7–V10 source-only original art preview iterations have been recorded; exact newer asset state must be checked on FA PR #14 | **Owner visual acceptance pending; revised ART-only L4 NOT RUN.** First actual art test remains **3 PASS, 2 FAIL, 3 BLOCKED** (workbench placement and four-direction rotation failed). Preview is not a native screenshot or installable artifact. Decisions `ABCL-D011` and `ABCL-D012` govern art. |
| TS + FA / TO-001 private Toxicology room icon | [Issue #24](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/24); FA active/inactive original 64×64 glyphs from source `5c739b4e1cba7eb8d8e81b5d0f823de2f2077973` pinned to G1 private PNG blobs (native lab colors red `#C93F3D`, gray `#999999`, white `#F2F2F2`). TS exact source `851b3059bed871d38844cffff7310de995bb2019`, Verify/CodeQL/Python source tests PASS; original game-reference [net35/CLR2 Windows build 41566322905](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41566322905) **SUCCESS, 0 warnings/errors**, ABCL DLL `7b13e698024c660f40257b713535b9b2b23354289301e3b1d1bbf41476112f2e` (19,456 bytes). First complete 14-entry UI-only test ZIP (combined original G1 compiled DLL + private PNGs + 2 name-spaced GameDBAsset XML + installer) independently inspected and hashed SHA256 `a30e9f3f6854ee502dd5aea3028ed95dde5e553df4ad6ebf2e0fe0e3f64f81eb`, not a release. | **L2 + genuine L3 + test-package file audit PASS; L4 NOT RUN.** The engine's numeric IconIndex 850 remains fallback; no global atlas/DLC/XML overrides or room zoning/access color changes. Exact ABCL lab row adaptation handles both `RoomItemController` and constantly redrawn `DepartmentManagementLogisticsHybridController` row via bounded LateUpdate. Owner must observe normal + unavailable state, reopen, map zone colors, original lab icons, CBC and at least claimed DLC/mod set in a disposable save. Do not merge Draft G1/art PRs or publish until L4 and visual approval. |
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
