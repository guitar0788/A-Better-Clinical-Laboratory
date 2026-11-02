# Official art production guidance for ABCL

Scope: ART-001 and subsequent laboratory equipment. This document supplements `docs/LAB_VISUAL_STANDARD.md`; it does not replace its D011/D012 owner-approved constraints.

## Sources and evidence levels

**Primary, developer-authored:** Oxymoron Games official Project Hospital forum, "Modding tutorial: objects" (roman.oxymoron, 2018-11-20): https://projecthospital.forumotion.com/t1477-modding-tutorial-objects

**Primary, developer responses (same thread):** jan.oxymoron, 2019-06-17 (five UI recolor slots) and 2019-06-24 (ColorSets.xml can change palettes). These are historical statements; validate current installed-game XML before assuming a schema detail is unchanged.

**Reference packs:** The developer links TestMod.zip and HelpfulFiles.zip (Illustrator isometric layers, numbered atlas grids, example XML). Consult read-only and retain attribution; do not upload copyrighted source packs, vanilla textures or DLLs to the public ABCL repository.

No second independent developer-authored art standard with equivalent specificity was confirmed. External generic isometric-art guidance is not evidence of Project Hospital's runtime schema.

## Mandatory vanilla-aligned object art contract

1. Use an **isometric composition grid**, not a retro block-pixel aesthetic. The developer's original tools were Adobe Illustrator and Photoshop; ABCL may use original editable SVG plus headless rasterization if output conforms to the same contract.
2. Draw each object in **NW, NE, SE, SW** order, keeping its physical construction, illumination, footprint and shared baseline coherent across directions. Avoid reimagining a different device per direction.
3. Place each sprite on the correct atlas grid cell. The official tutorial's standard small/tall object atlas is **2048 × 8192**, with **LAYOUT_16_X_64** in its examples. A smaller custom atlas is acceptable only when the exact installed-game renderer has a matching layout/UV path. ABCL's 2048 × 1024, **LAYOUT_16_X_8** has now been confirmed at source level (see the game-code audit below); it is not the same asset as the standard vanilla 16×64 atlas and still requires a separate L4 load/render test.
4. Object taller than one game tile must use the appropriate tall-object texture category. The tutorial says indoor objects cannot exceed **three tiles** in height. Indoor objects wider than one tile must be constructed as **composite objects** with separately defined parts and appropriate offsets.
5. Place PNG textures under `Assets/StreamingAssets/Addons/<ModName>/` and object database XML in its `Database/` directory when constructing an actual installable mod. Use a unique asset reference, correct mod-relative texture path, and distinct texture indices for each direction. The existing ART-001 GitHub workflow produces **non-installable previews only**.
6. Follow the game's corresponding database XML class/type. Start from a comparable game XML definition *as a local read-only schema reference*, then create original, namespaced definitions. Do not copy or publish the original game textures or overwrite original IDs.
7. Custom object icons: **64 × 64 RGBA PNG**, composed within the **inner 60 × 60** region (leave a safe margin). Use supported custom-icon asset references and files; do not assume `IconIndex` alone works in a mod.
8. Recolorable surfaces: developer guidance prescribes hue **300°** on selected surfaces, with `ModColorSets.xml`; historical developer reply confirms **five color slots for objects/decals**. Keep ABCL private color sets and do not rewrite vanilla palettes.
9. Multi-state object animations use directional `AnimationFramesNW/NE/SE/SW` and matching consecutive atlas cells. Do not claim animation from a still image. Character-overlapping assets may require direction-specific front/back textures such as `TextureIDBack*`; establish the correct rendering order from game-backed examples.
10. For multi-tile object seams, the developer suggests slight overlap across part cuts and careful alpha edge treatment to prevent white/black fringe. Any RGB dilation beneath transparent edges must preserve correct intended alpha and atlas separation.
11. Real equipment placement also depends on `AttachmentSlot/AllowedTags`, `ForcesAttachmentOrientation`, `AttachedToObject`, `AccessPositions`, object footprint and actual employee route. Treat artwork, configuration, runtime behavior and gameplay verification as separate gates.
12. Preserve additive ID namespaces, existing clinical G1 functionality and native/DLC/Workshop objects. No automatic merging or distribution of third-party textures.

## Additional original ABCL production recommendations (not claims from Oxymoron)

- For ART-001 tabletop equipment, compare exported silhouettes, feet, contact shadow and controls against owner-supplied *local read-only* native HEM/RIA/table reference sprites. Do not ship screenshots or vanilla texture pixels.
- Prepare side-by-side 1× native and 2× phone review sheets. A review sheet is not proof of correct native in-game scale.
- Run automated checks for dimensional integrity, transparent edges, eight unique source views, atlas indices, XML paths, custom icon padding and asset SHA256; reserve visual quality, contact points, occlusion and placement for human review/L4.
- Model each device's functional mechanical details consistently across four views: access hatch, screen, specimen tray, vents, safety hood and maintenance panel. Keep subdued medical materials and no player-visible ABCL brand.
- Do not add installable placement artifacts until owner accepts visual scale and a bounded L4 check shows corrected placement and rotation.

## Installed-game source audit — atlas, icons, attachment and color rules (2026-11-02)

This is source-derived evidence from the owner's previously supplied, read-only
game archives. No DLL or original atlas pixels were committed or uploaded.
The inspected Assembly-CSharp.dll SHA256 was
`1120d899fb74d16f31115c5c27325edbd1154b68e9419e6b7ea03cc3d43b6f24`;
the local vanilla objects atlas SHA256 was
`4b4af1dcb092f39487fe14a7e8cb93d06048c151276f6f7891e41ef2efc9fc16`.

### Custom atlas layout is supported by code, not yet by L4

- The real `TextureAtlasLayout` enum includes `LAYOUT_16_X_8`.
- `ObjectRenderer.GetTextureCoords` has an explicit `LAYOUT_16_X_8`
  branch and calls `TileTextureHelper.GetObjectTextureCooridnates16x8`.
- The helper uses X step `1/16` and Y step `1/8`; with 128px cells,
  the corresponding texture is 2048×1024. The generated IDs 0–7 occupy
  the first eight cells of its top atlas row.
- The same renderer's `LAYOUT_8_X_8` branch returns no coordinates; do not
  substitute that superficially similar enum.
- `StreamingAssetManager.LoadCoreData` queues both `TEXTURE_OBJECTS` and
  `TEXTURE_CUSTOM_SPRITE`; `LoadTextures` resolves the add-on
  `MOD_ROOT` asset path and loads the referenced image. `Database.ReadFiles`
  sets the add-on root and recursively reads XML under its Database folder.
  No fixed 2048×8192 check was found in these paths.
- Therefore the current custom 16×8 atlas has a real source-level loader and
  UV contract. This **does not prove** the actual mod loads, the sprite
  appears at correct scale, or all game builds support it. Keep exact-SHA
  L4 loading/rendering as a separate gate.

### Native object / attachment contracts

- Vanilla `OBJECT_HEMATOLOGY_ANALYZER` uses
  `AttachedToObject=true`, `LAYOUT_16_X_64`, 1×1 shape,
  `UseOffsetXNW=-0.7`, and `use_equipment_low` for its character-use
  animation. Vanilla `OBJECT_RIA` likewise uses attached-object mode,
  `UseOffsetXNW=-0.9`, and `stand_ria_use_*`.
- Both native objects omit `AccessPositions`, `TextureIDBack*` and
  `AnimationFramesNW/NE/SE/SW`. In `Floor.CanPlaceObject`, a null
  AccessPositions array takes the default direction-specific use-position
  path. ART-001 follows this native static-device convention; staff access
  and character contact remain untested.
- `Floor.CanPlaceObject` rejects an attached object if there is no center
  parent, no parent AttachmentSlot, or `AcceptsAttachment` rejects its tags.
  `GameDBObject.AcceptsAttachment` performs exact membership against
  the parent's `AttachmentSlot.AllowedTags`. The private workbench's
  two-item allowlist therefore has a source-backed reason; it does not widen
  vanilla table allowlists.
- `MapEditorUIController` reads the parent slot's `HeightOffset` and
  `DepthOffset`; if `ForcesAttachmentOrientation=true`, it forces the
  child orientation to the parent. The private workbench uses false to permit
  NW/NE/SE/SW child rotations. This predicts editor behavior only; the first
  owner L4 failed placement and rotation, and the corrected candidate has
  not yet been tested in game.
- Devices remain single-layer static sprites. No `TextureIDBack*` is added
  because there is no separate character-overlap layer in their current
  design. If future art intersects a worker silhouette, reassess depth layers
  against the actual renderer rather than adding back textures speculatively.

### Custom icons and palette

- The official guide prescribes 64×64 RGBA custom icons with the artwork
  confined to the inner 60×60 area. V7 pads all three icons with a 2px
  transparent border and tests the alpha bounds.
- The official guide prescribes hue 300° on recolorable texture faces and
  `ModColorSets.xml`; the developer response confirms the object/decals
  palette is limited to five slots. V7 gives the native-texture private
  workbench its own five-color palette ID. The two original SVG device
  textures use a fixed authored palette and do not claim in-game recoloring.
- The private palette duplicates a restrained five-option neutral set under
  a new ID; no vanilla ColorSet is edited or replaced. Actual in-game tint
  behavior remains an L4 visual check.

### Size, composition and occlusion

- The two new devices use `SHAPE_1_X_1`; no multi-tile composite is
  currently required. Their measured V7 alpha bounds fit within a single
  128×128 atlas cell and their bottoms now reach the final cell row.
- The tutorial's three-tile indoor height cap and composite-object rule still
  apply if later equipment grows beyond one tile in footprint/height.
- Static four-view frames do not need AnimationFrames state counts. Character
  use animations are references to existing native animation names, not
  proof of exact contact poses or worker task routing.

## ART-001 decision

Existing review-only generator and its private atlas remain unchanged. Do not change native atlas layout or XML attachment semantics from a documentation-only study. A future contract revision must first compare the official tutorial's full atlas format with the original installed game's corresponding asset-loader references, then make changes on the art branch and test them separately. Historical first owner L4 stays **3 PASS / 2 FAIL / 3 BLOCKED**. G1 R3 clinical L4 is not repeated for appearance-only changes.
