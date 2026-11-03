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
