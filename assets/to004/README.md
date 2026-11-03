# TO-004 — Toxicology Laboratory prefab room candidates

**DRAFT / NOT MERGEABLE.** See [Issue #30](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/30). This branch is independent of the current TS G1 and FA ART branches.

## Owner-original inputs
| Room | Original filename | Room bounds | Saved outer m_size | SHA256 |
| --- | --- | --- | --- | --- |
| Small | Toxicology Laboratory Map8x6.xml | 8×6 | 10×7 | `1477eb5580e1002c33384f84aaa708dfbe2fb19b09ea01dcd330309295d61457` |
| Large | Toxicology Laboratory Map12x6.xml | 12×6 | 13×7 | `4454abe727234fd8f8e6a70bcfff2f58860f05dbf3f8351b99951d7725bbad8d` |

The prefab XMLs must remain byte-for-byte unchanged. Both reference `ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB` from draft G1, and original-game equipment only. No ART-001 prototype devices are embedded. Game-runtime L4 not performed.

## Native addon route
`PrefabManager.LoadDevPrefabAssets` loads `GameDBAsset` with `Type=PREFAB` and `MOD_ROOT` paths; `GameDBPrefabObject` exposes `PrefabAssetRef`, `DisplayedSizeX/Y`, `Cost`, `CustomIconAssetRef` and `ui_prefab_lab` tags. Original hematology-small/large are 25000/30000, used here as an initial **price baseline**, not a verified bill of materials.

The overlay's root directory is `assets/to004/` in the repository. Once art and tests are complete, copy its `Database/`, `Prefabs/` and `Assets/` structure **inside the existing G1 addon staging folder**, without modifying the original game's database or making a standalone addon that lacks G1.

## Pending binary/media and gates
The standalone TO-004 handoff prepared in the TO chat contains two **104×104 original PNG layout illustrations**, generated editable SVGs, a source-only Python renderer, test-only installation/rollback helpers, manifest and six passing L2 checks. **The PNGs and editable SVG source are not yet committed to this GitHub branch.** Consequently its current references to `Assets/ABCL/Prefabs/toxicology_small.png` and `toxicology_large.png` are unresolved; **do not merge or install this branch directly**.

Once PNG sources are committed and G1 staging packaging is updated, run exact-source L2, real game loading/menu/placement/rotation/readiness L4, CBC regression, save/load, and declared DLC/Workshop combinations. This branch must remain Draft until owner visual approval and a focused L4 pass. Do not repeat the previously accepted full G1 clinical patient journey solely for a prefab change.

No original-game artwork, DLLs, decrypted dependencies, secrets, or launch-ready Alpha are present.
