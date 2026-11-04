# TO-004 — test-only additive overlay and source gate

**GitHub branch:** `feature/to004-toxicology-prefabs` / Draft PR #31. **Issue:** #30.

The prefab contracts use vanilla `GameDBPrefabObject` with `PrefabAssetRef` linked to a private `GameDBAsset` of type `PREFAB`; image assets are private `TEXTURE_CUSTOM_PREFAB_SPRITE` (104×104 RGBA). The original `PrefabManager.LoadDevPrefabAssets` and `StreamingAssetManager.CreatePrefabSprites` have these paths. Both use the existing Laboratory menu filter `ui_prefab_lab`. No new DLL or Harmony patch is needed.

Source assets under `assets/to004/`: two original XML room layouts, four additive XML database entries / tables, two original transparent icons, two editable SVGs and a deterministic source renderer.

The *G1 test-only overlay artifact* is a **14-file ZIP**: eight runtime additive files, four safe install/rollback helper scripts, one `TO004_BUILD_INFO.json`, and one `TO004_TEST_README.txt`. It is **not** a standalone G1 installer because it intentionally excludes G1's private toxin-room definition and clinical DLL. It never includes proprietary game DLLs, decryption material or assets copied from the base game. Existing G1 remains independently built and tested.

To reproduce and test from the repository source tree:

```sh
python -m pip install Pillow==11.3.0
python -m unittest discover -s assets/to004/tests -p 'test_*.py' -v
python -m unittest discover -s assets/to004/tools -p 'test_*.py' -v
python assets/to004/tools/package_to004.py --source-sha <exact-40-hex-commit> --output /tmp/ABCL_TO004_TestOnly_Overlay.zip
```

The GitHub `pull_request` workflow runs the commands automatically, with source checkout pinned to the exact head SHA, then uploads a source-matched test-only artifact. The asset registration XML is already in Draft PR #31; this scope only adds reproducible packaging and guarded installation to avoid manual ZIP composition.

**Blocked until actual L4:** 8×6 and 12×6 menu presence, previews, rotation, placement, staff routes, room readiness, save/load, vanilla + DLC + Workshop noninterference, owner visual sign-off. Previous G1 R3 clinical acceptance should not be repeated solely for a prefab change.