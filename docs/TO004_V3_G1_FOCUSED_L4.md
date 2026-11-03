# TO-004 V3 — approved prefab graphics: focused G1 staging / single L4 gate

**Approval date:** 2026-11-03. **Visual gate: PASS (owner).** **Game L4: NOT RUN.**
**Frozen TO source commit:** `a7d399d429b64ad0f41d16c002a18889ae7b00e8`.
**Workstream:** TS (technical integration); TO retains ownership of the frozen art and original room XML. Draft PR #31 remains unmerged.

## Exactly what this stage changes

This is **eight additive resources copied into an already installed, compatible `ModABCLG1LeadTest` G1 test addon**: four GameDB XML files, two owner-authored room XML files, and two approved 104×104 RGBA screenshot thumbnails. The frozen `assets/to004/tools/Install-TO004-Into-G1.ps1` installer refuses to overwrite any pre-existing target file and validates that the G1 toxicology room exists. It edits neither `src/ABCLG1Panel.cs` nor `ModExaminations.xml`, `ModRoomTypes.xml`, the original game database, nor any other addon. This is **not** a new C# binary / full G1 install package. A missing installed compatible G1 test addon is a *stop condition*, not a reason to silently inject a second copy.

**Frozen runtime bytes** (builder compares SHA256 and prohibits any image rewrite):
- `Assets/ABCL/Prefabs/toxicology_small.png` SHA256 `a0ec4ea41b5d96d4b755c5d244700548a6a2485d6a1d3e1bef73d8dcf09a0847`
- `Assets/ABCL/Prefabs/toxicology_large.png` SHA256 `3461bf9bbb8476d79e869d98f718b887a32ea88f5b0b158f185abc9f6cf85947`
- `Prefabs/room_toxicology_small.xml` SHA256 `1477eb5580e1002c33384f84aaa708dfbe2fb19b09ea01dcd330309295d61457`
- `Prefabs/room_toxicology_large.xml` SHA256 `4454abe727234fd8f8e6a70bcfff2f58860f05dbf3f8351b99951d7725bbad8d`

Private tags/IDs `ui_prefab_lab`, `PREFAB_ABCL_TO004_TOXICOLOGY_SMALL`, `PREFAB_ABCL_TO004_TOXICOLOGY_LARGE` and their dedicated `TEXTURE_CUSTOM_PREFAB_SPRITE` assets remain unchanged. The two display names remain `Toxicology Lab - 8 x 6` / `Toxicology Lab - 12 x 6` and corresponding Simplified Chinese. **Original saved outer `m_size` room XML must not be normalized.**

## Build and verification contract

The TS builder `tools/build_to004_v3_g1_overlay.py` checks out and verifies the **literal approved TO commit** (not its moving branch), checks 8 runtime paths and all frozen SHA, four private asset IDs / types / file paths, both native prefab menu entries and layer flags, and calls the original TO candidate packager without modifying approved resources. The resulting ZIP is audited byte-for-byte against the eight sources; it contains **no original DLLs, shared assets, original game data or clinical C# changes**. Workflow builds an overlay and verifies its untouched contents, and separately runs Windows mock installation/uninstallation in a dummy Project Hospital layout. **This is L2 + Windows mock installer validation, not genuine G1 DLL L3 and not gameplay L4.** The G1 executable/DLL must already have been installed from an independently authorized genuine compiled SHA.

## Targeted L4 — one disposable-save session

1. From the **new exact-source Actions artifact**, extract the test-only `ABCL_TO004_TestOnly_Overlay.zip` once, outside the game install. Close the game. Run the packaged `tools/INSTALL_TO004_TEST_ONLY.cmd` and provide the **game root** containing `ProjectHospital_Data` (not `Addons`).
2. Installer must report that exactly **8 additive ABCL files** were installed. If it reports missing G1, old TO004 files or a changed target, **STOP**. Do not delete another Mod, bypass ownership checks, overwrite either approved PNG or manually replace the G1 clinical DLL.
3. Enter a **new disposable save** with this same G1 test addon. Open **Laboratory → Prefabs**. Verify exact EN/ZH native names and visually distinct **8×6** and **12×6** V3 previews. Both were approved offline, but this verifies their actual UI wiring.
4. Place the 8×6 prefab and then the 12×6 on a clean area. Record each room's actual internal footprint, preview/orientation alignment (up to the four supported orientations), equipment and doors/walls. No new FA instrument should appear: these are original owner room layouts.
5. Confirm both room types belong only to `Toxicology Laboratory`; check actual green/red equipment-readiness requirements, lab specialist access and paths. Distinguish a failed room from an unstaffed hospital; do not redo insurance/lead patient spawning.
6. Compare original Hematology/Microbiology/Histology prefab list and original CBC usability; confirm their objects/icons are not replaced. With enabled DLCs/Workshop, record exactly which combinations were actually tested; do not claim untested combinations.
7. Save the disposable test hospital, exit and reload **without changing the addon installation**, verify both prefabs remain intact and no missing object/type warnings.
8. If any item fails, stop on **the first failing step**. Record screenshot + exact error/log and source/package SHA. Do not run all steps again to reproduce an already recorded failure. Only if needed, capture `output_log.txt` or `Player.log`.

**Acceptance:** UI thumbnails/labels, both placements/rotations, original object layers and sizes, room readiness/path, vanilla lab noninterference and one save/reload all pass. Only this owner gameplay report can advance #30 beyond *visual approved / L4 pending*.

## Removal / rollback

Close game and retire the disposable test save first. Use the same frozen package's `tools/UNINSTALL_TO004_TEST_ONLY.cmd` to remove **only eight SHA-matching TO004 files**. It refuses changed files and does not remove G1 or any vanilla/Workshop assets. **Do not load a save containing newly added prefabs after removing those resource definitions**.

## Hard boundaries

PR #31 **Draft**, no merge/release; no FA-1/FA-2 art changes, no native relation-tree edits or G1 clinical logic. If a necessary G1 variant is absent, stop and check the already authorized genuine G1 build; don't silently overwrite an installed G1 test addon or re-run accepted full lead-patient/CBC exercises.
