# TO-001 — TS staging from owner-approved isometric flask (not yet game L4)

**Status:** Owner approved the FA room-list glyph and its **exact direct isometric floor projection** on 2026-11-03. This approval **does not certify** actual game render, DPI, zoning tint or another method of drawing the flask.

## What was actually implemented

The new build-only `tools/stage_to001_approved_floor.py` consumes **immutable FA source SHA `d56b89962c0664fb37fc39113caed92892a335cc`** from Draft PR #14 and checks all of the following byte-for-byte:

- approved room-list glyph SVG original Git blob `c4a81670a2b0004799513c5b03a61b9239af1f5b`;
- both approved 64×64 RGBA menu PNG blobs `149bc34ebe68194d13054d91564c28700b5311ab`;
- approved direct projected 256×128 editable SVG SHA256 `76995aef9bb3eb851c28101d0b75200552bc85e91dc28247ebd0e786e6cab4ec`;
- approved 128×64 original transparent floor PNG SHA256 `7c0d03ddbd370aca4ddd1a089ff91d814e1c2622659a3d300d844bd9713a8cb4`;
- the original FA structural validation `verify_vector()` proves the two approved SVG groups are unchanged beneath exactly one approved perspective matrix.

On source approval, TS places that exact 128×64 PNG (no resize, geometry alteration or new icon) into one **new private 2048×2048 transparent RGBA atlas**, 16 columns × 32 rows, **tile 376** only: `x=1024..1151`, `y=1472..1535` from the top. A separately generated `ModAssetListsTO001.xml` adds only the namespaced `ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS` `TEXTURE` entry, leaving the two original 64×64 menu sprite IDs untouched. The script outputs a SHA256 inventory. It NEVER writes to the installed game. It creates no proprietary original resource or DLL.

## Interface and compatibility constraints

- TS's earlier reviewed/compiled `G1ToxicologyPrivateFloorIconAdapter` remains isolated to **`ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB`** in LOGISTICS view; it only swaps the existing exact room's own Renderer.material texture when the native original texture is still present; other rooms and other Mods cannot be globally repainted. A changed/unknown native renderer is left alone.
- The G1 room keeps `TextureID=376`, `IconIndex=850`, original zoning palette and native room/color rules. Original floor atlas/image files and three vanilla lab icons are never replaced.
- This staging is **source-only L2**, not a new G1 compiled DLL, an installed mod or runtime acceptance. G1 clinical examinations, insurers, patient generator, original CBC, TO-004 V3 approved prefabs and DLCs/Workshop are outside this change.

## Required next gates

1. [ ] Independent pinned-source FA checkout and TS staging job **PASS**; record exact TS HEAD, hashes of atlas/XML and verify 512 isolated tiles.
2. [ ] Genuine exact-HEAD G1 TS .NET 3.5 / CLR2 L3 compilation against owner-authorized encrypted references (the previous bridge's L3 is prior-source evidence only).
3. [ ] In an **already planned one-session, disposable-save L4**, verify ABCL floor icon placement, color, scale, disabled/hover states, original hematology/microbiology/histology, private-room switch, save/reload and optionally enabled DLC/Workshop combinations. The already accepted TO-004 V3 room prefabs are not redrawn or retested from scratch.
4. [ ] Keep Issue #24 OPEN, original FA PR #14 Draft and TS integration PR Draft. No merge or Alpha without actual game evidence.

**Stop rule:** If genuine native renderer ABI, verified background/texture ownership or exact alpha representation fails, revert the ABCL-only opt-in adapter and record a bounded compatibility NO-GO instead of changing original game assets.
