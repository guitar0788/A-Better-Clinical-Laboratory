# ART-001 — Anti-aliased original-style laboratory equipment rework

**State:** original-art concept and *editable SVG source prototype*; **NOT visually accepted**, **NOT installed**, **NOT a game-ready replacement**. Tracking: Issue #3, Draft PR #14. Decisions D011/D012 apply to all subsequent laboratory equipment.

## Original game evidence (read-only; owner-provided files)

- The original graphics are inside `StreamingAssets/Textures/objects_small_atlas.png` (2048×8192, 16 columns × 64 rows; each atlas cell is 128×128).
- The original `StreamingAssets/Database/Objects/ObjectsAttachments.xml` contains `OBJECT_HEMATOLOGY_ANALYZER` with slots 248/249/250/251 and `OBJECT_RIA` with slots 252/253/254/255.
- The equipment workbench `OBJECT_TABLE_EQUIPMENT` in `Objects.xml` uses slots 472/473/474/475, `ASSET_TEX_OBJECTS_SMALL`, `LAYOUT_16_X_64`, and has an attachment slot which accepts vanilla functional tags.
- Original bitmap alpha-bound measurements (not physical-object geometry) demonstrate that earlier arbitrary `<=65×51px` constraints were unjustified: HEM NW alpha bounding box is (7,20,126,128); RIA NW is (8,43,108,127). Both include shaded margins/contact effects. Shadows, orientation and renderer offset make direct pixel bounding boxes inappropriate as placement proof.
- The original bitmaps exhibit antialiased edge pixels, soft shading and detail. The formerly shipped procedural rectangular/pixel-block `tools/generate_art_001.py` was visually rejected by the owner.

**Copyright boundary:** Original assets above are used solely for local visual analysis and reference. They are **not copied** into ART-001's new sprites, GitHub, or a user-installable package.

## New editable-source direction

`tools/generate_art_001_svg.py` is a standalone review-only original SVG art generator. It produces eight editable four-view source SVGs, one shared transparent 2048×1024 PNG atlas with 128×128 cells, and small original icons. It rasterizes SVG at 4× size with CairoSVG and downsamples using Pillow Lanczos, rather than writing flat aliased pixels. Directional pairs are mirrored/edited variants with distinct front/back service geometry. No game's original pixel data is ingested.

`tests/test_art_001_svg.py` tests source isolation, four direction slots, native atlas format, non-copied original asset names, partial-alpha antialiasing and nonidentical frames. The *ordinary* Verify job skips renderer-dependent checks if Pillow/CairoSVG are not installed; the dedicated preview workflow installs the renderer and must execute all of them.

The old art-only **installable** placement package workflow is paused. `.github/workflows/art-001-preview.yml` exports only a preview/source artifact named `ABCL-ART001-ANTIALIASED-REVIEW-NOT-INSTALLABLE`. No original clinical G1 code is changed.

## Visual concept vs production assets

A non-pixelated isometric concept sheet is provided privately to the owner as a **design reference only**. It is not an original-game screenshot, a four-frame deterministic animation source, or an approved packed texture. Some concept panels show larger cabinet equipment than the small benchtop devices requested; this is a review concern rather than evidence of acceptance.

The actual SVG prototype, although anti-aliased, is still a first source-pass and may not yet match the full material complexity of the original HEM/RIA artwork. **Do not package it for user L4 until the owner approves the art scale and appearance and the generated atlas has been compared at native in-game size.**

## Acceptance gates

- [x] Find actual original GameDBObject XML and sprite IDs without redistributing their bitmap data.
- [x] Preserve private ABCL technical IDs, unbranded player-facing English/Chinese labels.
- [x] Create original editable SVG authoring pipeline with supersampled antialiasing.
- [ ] Exact branch-head renderer + Verify/CodeQL all pass, and exported preview hash is audited.
- [ ] Owner accepts new art as visually consistent with native hospital laboratory equipment.
- [ ] Dedicated private workbench visual integration and correct native attachment pivot/rotation.
- [ ] One new art-only disposable-save L4 with proper placement, four views, contact, occlusion, pathfinding, vanilla-equipment coexistence.
- [ ] Native staff use/procedure interaction through isolated ABCL tags.

Historical first ART L4 remains **3 PASS / 2 FAIL / 3 BLOCKED**; G1 R3 clinical success remains separate and is not repeated.
