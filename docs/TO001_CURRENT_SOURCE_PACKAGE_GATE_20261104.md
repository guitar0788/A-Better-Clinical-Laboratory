# ABCL R11 — correct original opaque room-list atlas palette

**Current implementation target:** source `80fed52f7d474fce9e7029567b7f81571d7d6905`, true net35/CLR2 G1 DLL SHA-256 `4bc02a4c3d1ee161e712e8119b97f5aaabde1d94ac74ccccf86f712dbee5afc8` (33,280 bytes), authentic Windows Actions [#41833818373](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41833818373), artifact `13324980926`.

## Locked technical decision

The developer's original `StreamingAssets/Textures/ui/icons.png` was inspected with the actual `IconManager` atlas index mapping, not a previously wrong exported glyph sample. Original lab room-list sprites 850, 854, 2868 (and cleaning closet 808) contain their own **opaque red background RGB(201,63,61)** and foreground RGB(242,242,242). Disabled sprites 851/855/2869 contain **opaque gray RGB(153,153,153)**. The original `SegmentItemIconTextTextIconController.UpdateData` merely sets the Sprite; it does not automatically fill a red backdrop for transparent PNGs. The publisher's hue 300° recoloring guidance applies to world materials/objects/tiles, not this room-list icon path.

Owner-provided R10 screenshot documents **menu transparency L4 FAIL**. It is caused by R10's code extracting a transparent glyph from the approved opaque source. R9's code rendered the approved dark red RGB(171,48,62) directly (L4 color FAIL). These two candidate behaviors are rejected and **must not be used**. The owner has declared the independent isometric floor icon **L4 PASS**.

### Current R11 behavior

- Verify the **unchanged, owner-approved** original room-icon red/gray PNG SHA-256 before decoding.
- At runtime only, extract the antialiased shape of the original approved white flask from its known matte; composite onto the exact *baked-in vanilla room-list atlas colors* (red 201,63,61 / disabled gray 153,153,153; white 242). The private UI sprite has 4096/4096 alpha=255; no transparent or dark red background. The original PNG is **never** rewritten or recolored on disk.
- Preserve exact ABCL room row scoping, 22-unit native size, native hybrid/legacy UI support, foreign Mod override fail-closed guards; preserve **unchanged** G1 floor rendering (already owner L4 PASS), room tile 376, both owner-approved standalone devices, 8×6 and 12×6 XML layouts, previous clinical logic and all original/DLC/Workshop files.
- Original Harmony1 1.2.0.1 net35 remains a genuine 113152-byte loader precondition with MIT license; never copy the 0-byte placeholder from isolated G1 L3 test artifact.

### Strict complete ZIP gate

Locally assembled R11 test-only integrated ZIP `ABCL_R11_Full_Test.zip`: 34 entries, SHA-256 `ce0d901ca438c52e8e46529d4c37110c793205db37d5e6d3d3d1e4fa7428fa51`. L2 independent audit PASS; only `ModABCLG1LeadTest.dll` and `BUILD_INFO.json` differ from R10, all other 32 entries byte-identical including 8 owner SHA-frozen sources. Negative gate rejects R10/stale DLL, altered art, missing Harmony1, incorrect room XML or forged old manifest. New exact-head CI and actual net35 L3 PASS.

**No R11 game L4 PASS is claimed.** One focused owner test of the red room-list icon against vanilla and no regression of the known-passing isometric floor icon is required. Keep these gameplay PRs Draft/test-only; no automatic merge to main/release.
