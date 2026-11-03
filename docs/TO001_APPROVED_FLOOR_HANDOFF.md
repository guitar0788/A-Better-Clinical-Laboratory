# TO-001 — Approved floor glyph: exact room icon projection

**Status (2026-11-03): OWNER VISUAL APPROVED ONLY.** Real Project Hospital runtime L3/L4 and TS integration still required. This approval does **not** extend to earlier independently drawn floor icons, any instrument, or the private renderer.

## Source provenance

The owner approved the room-list Toxicology glyph first. Following multiple rejected floor reimaginings, the owner clarified that the floor icon must be a direct isometric transformation of the already approved room icon. They then approved precisely that projected image.

| Resource | Path | SHA256 / Git blob |
| --- | --- | --- |
| Original approved room vector (unchanged) | `assets/art/to001/toxicology_room_icon.svg` | Git blob `c4a81670a2b0004799513c5b03a61b9239af1f5b` |
| Derived editable native-scale floor vector | `assets/art/to001/toxicology_floor_from_approved_256x128.svg` | SHA256 `76995aef9bb3eb851c28101d0b75200552bc85e91dc28247ebd0e786e6cab4ec` |
| Generated native-floor reference | exported from SVG, 256×128 | SHA256 `a4083e3bef7dab0f9c0d629a42da517a51951729a42884f082eb9d8d5c7e8903` |
| TS-private raster candidate | `assets/art/to001/toxicology_floor_from_approved_128x64.png` | SHA256 `7c0d03ddbd370aca4ddd1a089ff91d814e1c2622659a3d300d844bd9713a8cb4` |

The derived SVG contains one wrapper `<g transform="matrix(3.3 1.2 -2.3 0.75 96 1.6)">`. Its two nested original artwork groups have identical serialized SVG geometry, strokes and colors to the approved original, with no new flask or embedded room zoning panel. It is an editable, non-game-runtime illustration source. A deterministic export script validates both image SHA256 values from the same vector.

## Compatibility and TS integration guardrails

1. **Never** replace or copy over the original `StreamingAssets/Textures/ui/icons.png`, floor tiles, installed vanilla XML, or another Workshop mod’s file. No globally shared resource ID reuse.
2. `ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB` is the only allowed targeted room; preserve the existing exact-room fallback and data registration contract.
3. TS must check whether the private 2048×2048 `LAYOUT_16_X_32` (128×64 cell) floor atlas has verified UV coordinates, transparency, material composition and the correct icon orientation. Do not treat the 256×128 original-game cell and the private 128×64 cell as interchangeably scaled rendering.
4. Maintain native zoning, red/gray states and other original laboratory glyphs; never bake underlying room colors into white artwork.
5. Preserve CBC, G1 patient/test routing, all four DLC and Workshop boundaries. L2 source/art approval is **not** L3/Unity runtime or L4/owner game approval.

**Not changed:** private device tags, instrument workbench, G1 medical records, prefabricated TO rooms, art for any other device, or main. Keep Issue #24 open, PR #14 Draft; no install package, release or auto merge.

## FA private atlas handoff — deterministic source-only L2

Approved original art is unchanged. FA now provides an isolated 2048×2048 RGBA atlas generated from the already approved 128×64 projection with `tools/build_to001_approved_floor_atlas.py` (Pillow 12.3.0). This uses a 16×32 grid. Only tile 376 at column 8, top-origin row 23, pixel rect (1024,1472)–(1152,1536), contains nonzero alpha; the remainder is transparent. The tile bytes are identical to the approved source.

- Input PNG SHA256: `7c0d03ddbd370aca4ddd1a089ff91d814e1c2622659a3d300d844bd9713a8cb4`.
- **Private atlas SHA256: `00bac60d16db5f24ea06759c6add6372f132e45d7bf832c4b81c26ac03e403cd`**.
- Reproducible file: `toxicology_floor_tile_atlas.png`, produced alongside `manifest.json`. GitHub Actions workflow `.github/workflows/to001-approved-private-atlas.yml` exports a **NON-INSTALLABLE** 7-day artifact; source code is retained indefinitely in this branch and can regenerate the atlas without native game files.
- Pure stdlib fail-closed contract tests: `tests/test_to001_private_atlas_source.py`. Both they and the workflow verify that rejected art cannot silently replace the approved visual source.

TS contract: `ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS` for exact `ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB`. TS PR #29 has a separate artless L3 compile at `49475e91...`; it is NOT L3 for this new atlas. FA does not register a new `GameDBAsset`, ship an installation package, modify renderer/UV/material or affect G1 and TO prefab XML. TS must take over asset declaration and native binding only after checking its guarded renderer ownership. Verify L3 and game L4 separately; retain fail-closed behavior for other rooms, 4 DLC and Workshop mods. PR #14 remains Draft; Issue #24 remains open.
