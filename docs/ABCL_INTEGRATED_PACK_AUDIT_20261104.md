# ABCL refreshed integrated test candidate — 2026-11-04

**Status:** G1 genuine L3 PASS; source/asset archive checks PASS; refreshed combined game L4 NOT RUN. This is a ChatGPT-delivered disposable test package, not an Alpha or GitHub release.

## Exact test package

- File: `ABCL_TEST_R3_20261104.zip`
- Size: **249,639 bytes**
- SHA-256: **`174f5c108294739978489036c6e7bfbe63a5efc5e7e2ed517102fe86f797dd72`**
- 45 files total; 26 files under the active addon.
- Manifest: `PACKAGE_MANIFEST.json`; all 44 other file receipts were rechecked against exact byte count and SHA-256. ZIP CRC test PASS.
- Old links/ZIPs with hashes `e4c2fbc7...` and `f5b191...` are superseded. Use only the R3 filename/hash above.

## Genuine G1 compile (L3)

- PR #7 exact source SHA: `0283e789bbf125b709490bda4c1164c30883fdcd`
- [Protected-main Auto-build Actions #41754602137](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41752846916)
- Artifact ID: **13287840694**
- Genuine Windows .NET Framework 3.5 / CLR2 build: **PASS**
- Compiled ABCL DLL SHA-256: **`c5e8ddeee5dcad5adedfbbf9b42e04af02716f87d1485c3c4a2c976f2a38f373`**
- Exact-head [Verify PASS](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41754570159), [CodeQL PASS](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41754570076), [synthetic R3 installer isolation PASS](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41754570182).

The current DLL contains the native R3 TRM_LDP test path and both TO-001 adapters. The C1/Super-GM class and R2 generic outpatient path are absent. Binary marker scan found no `中文超级GM`, `[ABCL GM TEST ONLY]`, `DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE` or `ForceMobilePatient` strings. The R3 test button remains; it is not a general patient generator.

## Owner L4 findings and source corrections

Owner's 2026-11-04 result for the previous integrated ZIP:

| Item | Owner result |
| --- | --- |
| Install/backup, G1 panel, toxicology room selectable | PASS |
| Two standalone devices visible/placeable, NW/NE/SE/SW | PASS |
| Device scale, perspective and ground contact | PASS |
| TO-004 8x6 / 12x6 prefab placement, rotation and access | PASS |
| TO-004 display names | FAIL — dimensions were appended twice |
| TO-001 room-list and floor icons | FAIL — not assembled in prior package |
| C1/Super-GM generated patient | FAIL — no usable diagnosis/treatment; owner reported broader patient-state impact |
| Staff operation, original CBC, save/reload, rollback | NOT TESTED |

### Super-GM / C1 retirement

Original ILSpy and GameDB inspection showed the C1 fixture's four original symptoms all have `IsMainSymptom=false`; the case had no native main symptom required by diagnosis/treatment UI. The original patient factory also registers a created patient with its insurer, so the old Super-GM was not a side-effect-free preview. The owner reported wider patient-state impact. The current G1 candidate removes the Super-GM class, C1 fixture, C1 localization and generic R2 `DIA_CLD` override. The installer now accepts only explicit R3 native `TRM_LDP` mode and adds the ABCL sampling examination only to an addon-local TRM_LDP copy.

### TO-001 room and floor art

- FA source commit: `cb3a7ab5d03e8677dcb84f486a04bf0ea5f8f622`
- Approved active 64x64 room sprite SHA-256: `acb0042bb006f1f6a85c5b099f1c311ac5268b19944206cb1003b96a7930cb8a`; TS-derived neutral-gray inactive sprite SHA-256: `ebb5b1eec01aef7fc60c0479fd0efb32ebc942cb40a2b1629e06a677f774ba34`
- Approved source tile SHA-256: `7c0d03ddbd370aca4ddd1a089ff91d814e1c2622659a3d300d844bd9713a8cb4`
- Private atlas SHA-256: `00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd` (exact atlas in the approved TO001 stage artifact 13235300478)
- Asset list registers two `TEXTURE_CUSTOM_SPRITE` IDs and one `TEXTURE` private floor atlas. The FA stage originally duplicated the active/inactive PNG; original `IconController` custom-asset path ignores `m_inactive`, so TS derives a separate transparent low-contrast disabled sprite without baking background or area color.
- Current G1 DLL includes exact-room room-menu adapter and private floor renderer. It uses per-renderer material and restores only owned glyph changes; it does not replace the vanilla atlas or write shared material.

Source/asset hashes pass. The refreshed combined game's room-menu, disabled state, floor glyph, zone-color and save/reload L4 remains NOT RUN.

### TO-004 prefab names

Original `MapEditorUIController.CreatePrefabButton` appends the displayed dimensions after the localized name. Therefore the labels must be dimension-free. Updated source head:

`9130c7a3241315d1b73e8bcfdf4cc2f560cd9804`

- EN: `Toxicology Laboratory`
- zh-Hans: `临床毒理实验室`

[TO004 Verify PASS](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41751523720), [source candidate PASS](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41751523693), [CodeQL PASS](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41751523655). Prefab geometry, IDs, sizes, images and frozen V3 source are unchanged. Separate V3 owner L4 remains 6/6 PASS; combined L4 after label correction is NOT RUN. Current-base overlay is Draft PR #47 with Verify/CodeQL PASS.

### ART-001 devices

Owner's L4 items 04-07 confirm both instruments' appearance, placement, four views, size, perspective and ground contact PASS. Staff access/use and the digestion/ICP-MS clinical assay workflow remain NOT TESTED. The test package does not claim that either instrument's clinical workflow is complete.

## Package safety and compatibility checks

| Gate | Result |
| --- | --- |
| ZIP CRC, path inventory, no duplicate entries | PASS |
| Per-file manifest receipts (44 files) | PASS |
| Active addon file count | 26 |
| G1 DLL exact build SHA | PASS |
| Vanilla `0Harmony.dll` sentinel is 0 bytes | PASS; retained intentionally |
| No original Unity/Assembly-CSharp DLLs or decrypted game references | PASS |
| No active G2 diagnosis XML or C1 fixture | PASS |
| TO001 room sprites/floor atlas present with correct IDs and dimensions | PASS |
| TO004 bilingual labels contain no size suffix | PASS |
| Original CBC examination not replaced by addon | PASS at XML/source level |
| PowerShell integrated installer executed on real Windows game path | NOT RUN |
| Refreshed combined in-game L4 | NOT RUN |
| Staff use, CBC in game, save/reload, rollback | NOT TESTED |
| All DLC / Workshop coexistence matrix | NOT TESTED |

**Vanilla sentinel note:** Original `TitleScreenController.cs` checks for an empty `0Harmony.dll` marker before scanning code-mod DLLs and explicitly skips loading that filename. Removing the empty sentinel can prevent the ABCL DLL from being scanned. It is intentionally preserved; it is not a Harmony dependency.

## G2 and remaining scope

G2 Cd/Hg diagnoses and icons are not included in this package. The disabled-case GM dispatcher and its privileged CI proposal were retired after the owner L4 failure. G2 normal diagnostic C2 exclusivity and a genuine playable G2 DLL/L4 remain unproven. TO-002 relationship graph is not implemented. Complete TO-003 UI L4 remains pending.

## Focused next owner test

Use a fresh disposable save. The prior PASS items for device placement and prefab placement/access need not be repeated unless they regress. Retest:

1. Integrated installer, main menu and G1 panel.
2. TO-001 room-list icon, including active/disabled state.
3. TO-001 floor glyph on Toxicology Laboratory; verify other room/zone colors are unchanged.
4. TO-004 8x6 and 12x6 names display exactly once with dimensions; prefab geometry/placement/rotation/access.
5. Staff access and use of both standalone devices.
6. Original CBC.
7. Save, quit, reload.
8. Restore previous ABCL addon.

Do **not** use the removed Super-GM. Do not click the R3 native patient request in this focused UI pass; the historical native route does not need to be replayed.

**No Alpha release. No universal DLC/Workshop compatibility claim.**
