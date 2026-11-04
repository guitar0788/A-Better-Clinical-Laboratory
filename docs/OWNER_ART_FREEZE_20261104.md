# 2026-11-04 Owner-approved art and native integration freeze

**Authority:** direct owner acceptance on 2026-11-04, following the invalid 2026-11-04 R1/R2/R3 integrated-test packages. This record amends D011/D012 for these exact two freestanding instruments; it supersedes prior status text treating the exact approved images as awaiting visual approval. It does **not** establish native gameplay L4 acceptance or a releasable package.

## Frozen untouched artwork — owner-supplied Assets.rar

The five images below were extracted and SHA-256 compared byte-for-byte against **ABCL_Full_Integrated_Test_20261104_R3_Corrected.zip**. All 5 matched. The PNGs are **already correct** and must not be repainted, resized, recolored, redrawn, or exchanged for placeholder art:

| Exact path under `Assets/` | Dimensions | SHA-256 |
| --- | --- | --- |
| `ABCL/toxicology_room_icon.png` | 64x64 | `225b2918c448b5d36d1d8582389e8952f2baf1574d0d72935017c81eab7d8199` |
| `ABCL/toxicology_room_icon_inactive.png` | 64x64 | `50c17ea8ba8b42b28295564f594713069a31c9e48fa05f3a6b623a36851b6490` |
| `ABCL/toxicology_floor_atlas_private_376.png` | 2048x2048 | `00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd` |
| `ABCL/Prefabs/toxicology_small.png` | 104x104 | `a0ec4ea41b5d96d4b755c5d244700548a6a2485d6a1d3e1bef73d8dcf09a0847` |
| `ABCL/Prefabs/toxicology_large.png` | 104x104 | `3461bf9bbb8476d79e869d98f718b887a32ea88f5b0b158f185abc9f6cf85947` |

**Verified alpha:** both supplied 64x64 room-list icons have 4096/4096 pixels with alpha=255. The active icon has a solid red background and white flask; the inactive icon has a solid gray background. A transparent-looking native room list therefore means the correct resource was not reliably loaded/bound/drawn. Do **not** "fix" this by altering the owner image. The floor image's transparency outside the glyph is intentional and must not be replaced by a red button.

## Frozen freestanding instrument art

The owner additionally **approved the two four-view instrument artworks already submitted around midday**, with their integrated bases. They are **floor-standing objects**, not attachments to a separate table. Preserve the original source images and directional sprites on FA Draft PR #14 (reviewed source commit `cb3a7ab5d03e8677dcb84f486a04bf0ea5f8f622`):

- `assets/art001/review_20261103/original/mass_spectrometer_four_views.png` SHA-256 `81f50e232cc275cf4939597f0170f7fde155ae28010b67976c42d6dd5c5e38ae`.
- `assets/art001/review_20261103/original/sample_digestion_four_views.png` SHA-256 `a3edefd91d6eedc119856e3efaac613ba14ad4ae1c149a6a882fde70b5e9f708`.
- Approved-source eight-frame diagnostic atlas `assets/art001/review_20261103/diagnostic_equipment_atlas.png` SHA-256 `b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651`.

**Use TS Draft PR #42's independently staged floor-object definitions as the engineering starting point:** the two ABCL equipment objects must have `AttachedToObject=false`, `Placement=INDOORS`, correct private 4-direction indices and tags. Do not package or register `OBJECT_ABCL_ART001_WORKBENCH`, and do not reinstate the previously rejected three-object attachment setup. This explicitly amends the tabletop/optional dedicated-parent assumption in D011 for these two devices only.

## Reproducible evidence of bad integration, not bad images

- The 2026-11-04 R3 ZIP contains exactly the **same five SHA-256 artwork files** as the user's supplied RAR. Reported in-game wrong appearance is therefore a **runtime/UI binding, install-state or packaging-version issue**, not a reason to modify their pixels.
- R3's installed ART asset is **not** the approved new atlas: `ModABCLArt001Test/Assets/ABCL/equipment_atlas.png` SHA-256 `a5bad4aae0c41b5775586bba358f1c3a5c42cc099a8e28b41c1e174e485559c3`, versus approved `b412b384...`; its `ModObjectsABCL.xml` still includes the workbench and `AttachedToObject=true`. This is a source/packaging regression.
- Original `DepartmentManagementLogisticsHybridController.UpdateRoomButtons` resets the row's `Image.sprite` using `IconIndex` on each update. ABCL's exact-room UI bridge must be verified after native updates, for the correct private asset ID, correct `Image` target, alpha/tint and state; no global icon atlas overwrite.
- The original `RoomRenderer` uses a separate `TextureID` floor path. Preserve approved private floor tile **376** and native logistics color semantics; do not bake a substitute red background into the floor atlas.
- The reuploaded prefab XML files are pinned separately: 8x6 `ec3be4046d90c219d28143ffd838712fc8030b3a84a05e80a4b8e65ec0141b1d`, 12x6 `7d5c559cc60211ea37b42026c8066fbff98865be88d76ef8730350f3ac81b54d`. Preview image acceptance does **not** assert those thumbnails depict every object in these updated XML layouts.

## Acceptance and hard stop

1. Before building, enforce exact asset SHA-256, source art identity, XML object placement and prefab ID/preview integrity. Never substitute an older "approved" sprite or a redesigned icon.
2. Preserve other mods and the original game files, XML, icons and CBC; use only ABCL-owned namespaces; no global shared material/palette mutation.
3. Separate source L2 validation, genuine changed-DLL net35/CLR2 L3 compilation, package-file audit and actual game L4. Never treat source tests or owner *visual* acceptance as runtime success.
4. R1/R2/R3 integrated ZIPs are **rejected test baselines**; do not reissue them with superficial image swaps. No new owner install request until a single complete integrated candidate passes the offline gate.
5. No source-art changes, merges or Alpha release are authorized by this record. The owner has explicitly said the bug is **code/integration**, not art.
