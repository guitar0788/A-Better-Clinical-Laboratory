# ART-001 — original toxicology instruments (source candidate)

**Status:** source and XML candidate, **not an installed or gameplay-validated device**.
Tracked under [ART-001](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/3).
This branch is independent of the still-Draft G1 test harness. The owner's G1 R3
clinical L4 report is accepted for artifact 13117942292; no repeat is required.

## Shipped in this source branch

- A self-contained, originally authored smooth SVG generator
  at `tools/generate_art_001_svg.py` (CairoSVG + Pillow in cloud CI).
- Two original prototypes: a mass spectrometer and an enclosed
  sample-digestion workstation; player-visible names are unbranded.
- Four separately rendered isometric directions per instrument: NW, NE, SE,
  SW. Eight unique atlas tile IDs, shared canvas dimensions and pivots.
- One optional, additive `GameDBAsset` atlas and three original custom icon entries
  (two instruments plus the private workbench).
- Three private `GameDBObject` declarations: two attached devices and one
  private instrument workbench, based on *structural conventions* of original tabletop objects. Native staff animations are only **references
  to vanilla animation names**, not redistributed frames.
- English and Simplified Chinese object names and descriptions.
- `tests/test_art_001_assets.py` for PNG signature/dimensions, unique frames,
  slots, localization, object IDs, collision-safe unique tags and G1 isolation.

## Render source → assets

Run from the repository root:

```sh
python tools/generate_art_001_svg.py --output /path/to/temporary/art001-build
```

Generated outputs are:

```text
art001-build/
  Assets/ABCL/equipment_atlas.png
  Assets/ABCL/icp_ms_icon.png
  Assets/ABCL/digestion_station_icon.png
  Assets/ABCL/workbench_icon.png
  Sources/ABCL/ (8 device SVGs + workbench_icon.svg)
  Previews/ABCL/direction_preview.png
  Previews/ABCL/review_mobile.png
  art_manifest.json
```

**Source of truth** is the generator, not the generated PNG. The manifest
contains reproducible SHA256 hashes and atlas mappings. No game assets are read.

## Create an offline review folder (NOT a game installer)

To generate a self-contained disposable review layout without touching the
live game installation:

```sh
python tools/stage_art_001.py --output /path/to/new/Art001Proof
```

This creates `Art001Proof/Database/` with the two original device entries,
private workbench, private ModColorSets.xml, bilingual text, asset references
and an art-preview-only addon identity;
`Art001Proof/Assets/ABCL/` holds the generated atlas/icons. A preview image
is at `Art001Proof/Previews/ABCL/direction_preview.png`. The stager refuses
to overwrite an existing directory or write into any `StreamingAssets` /
`Addons` directory. It is a **resource-layout review fixture**, not a tested
loader or an approved installable Mod.

The new devices carry `ui_lab_equipment` so the existing lab room's build
filter can discover them *if* an addon loader accepts the fixture. Their
functional tags are still isolated and deliberately do not claim to satisfy
the G1 lab-procedure requirements.

## Game format — grounded technical contract

The user's original game sources show:

- `GameDBAsset` with `Type=TEXTURE_OBJECTS` or
  `TEXTURE_CUSTOM_SPRITE`, `File=MOD_ROOT/...` for addon assets.
- `GameDBObject` supports `TextureRef`, `TextureAtlasLayout`,
  `SpriteShape`, `TextureIDNW/NE/SE/SW`, `CustomIconAssetRef`,
  `AttachedToObject`, `UseAnimations`, `Tags`, and `Cost`.
- Original game `TextureAtlasLayout` enum includes `LAYOUT_16_X_8`.
  Its object-renderer source has a coordinate handler for 16×8. **Do not use**
  `LAYOUT_8_X_8`: the renderer returns null for that enum, despite its
  presence in the enum definition.
- This atlas uses 16 columns × 8 rows, with 128×128 px per cell, yielding a
  2048×1024 RGBA atlas; at full decode it is roughly 8 MiB. Two devices
  share one atlas rather than separate 2048×8192 vanilla-size sheets.

This is an author-created representation of the required structure; it does
not include any original game texture, sprite or original DLL.

## Tags, interaction and compatibility

- The staged objects deliberately use **new ABCL-only functional tags**
  `abcl_art001_icp_ms` and `abcl_art001_digestion`.
- They do **not** impersonate the original `hematoanalyzer`,
  `stat_lab_exam`, or other vanilla process-equipment tags. This prevents
  unintended rerouting of CBC or unrelated Workshop labs during staging.
- The original vanilla animations `use_equipment_low` and
  `stand_ria_use_*` are referenced as tentative contact candidates. Actual
  animation origin/offsets, supported attachment-slot/desk positions, occlusion,
  staff pathfinding and placement need visual/game verification.
- The current G1 examination and laboratory definitions are **untouched**.
  Its verified workflow still uses native equipment, not these objects.
- Do not copy this staging Database into `StreamingAssets/Addons` until a
  separate native asset-loader and interaction review authorizes the exact
  package. Do not automatically install or publish it, and do not remove
  equipment from saves containing these candidates.

## Source-backed native loader audit and preview evidence (2026-11-02)

The original game assemblies and game database were inspected **read-only**
from the owner's previously supplied `dll_ilspy.zip` and `StreamingAssets.zip`.
Findings relevant to the staged XML (not gameplay evidence):

- `GameDBAsset` supports `Type` and `File`; `GameDBAsset.OnLoad` uses
  `Database.sm_currentDirectory` as its root. `Database.ReadFiles` assigns
  the mod root path before iterating its `Database/` XML files.
- `StreamingAssetManager.LoadTextures` resolves `MOD_ROOT/...` from
  `GameDBAsset.RootPath` and recognizes both `TEXTURE_OBJECTS` and
  `TEXTURE_CUSTOM_SPRITE`. Thus the source file-reference form and asset
  types are grounded in the real loader. This is not proof the test object
  can be placed or interacted with.
- `ObjectRenderer.GetTextureCoords` directly supports
  `LAYOUT_16_X_8`, mapping IDs to a 16×8 atlas. Its `LAYOUT_8_X_8`
  branch returns null, so the candidate correctly avoids that layout.
- `ObjectsAttachments.xml` provides native analogs:
  `OBJECT_HEMATOLOGY_ANALYZER` uses `AttachedToObject=true`,
  `UseOffsetXNW=-0.7`, `use_equipment_low`, and tags
  `equipment/ui_equipment/hematoanalyzer`; `OBJECT_RIA` uses the same
  attachment mode, `UseOffsetXNW=-0.9`, and `stand_ria_use_*`
  animations. These are conventions the ABCL prototype mirrors.
  **Do not infer four-direction animation contact from XML alone.**
- The ART-001 functional equipment tags are new and **do not** satisfy
  vanilla `hematoanalyzer` / `stat_lab_exam`. No original treatment or
  diagnostic equipment is re-registered, and the R3 patient test build is
  unaffected.

The first generated preview (source `66dab800...`) was inspected and
**rejected as visually insufficient**: both machines read as generic boxes,
and direction changes were too subtle. The source was revised with an
upright ICP-MS plasma/ionizer tower, sample carousel, vials, side vents,
status panels, and a separate enclosed amber sample-digestion chamber,
reaction tubes and control gauges. Each orientation now changes structural
visibility, control-face direction and upper assembly position.

**Verified refined preview source:** `c5cefcccc28083ef06ef0ff12b638ce2dfb9b4c8`.

- [Successful original-preview build](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41407436693):
  uploaded preview-only artifact `13124281121`.
- Downloaded, extracted and visually inspected the actual
  `Previews/ABCL/direction_preview.png`, 1024×256 RGBA. It contains
  two independently distinguishable instruments and NW/NE/SE/SW frames.
  The shared atlas is 2048×1024 RGBA; the individual icons are 64×64 RGBA.
- Downloaded artifact ZIP SHA256:
  `c3d7d0551d1d1d90ea02f0b2d723caf9db5cfdc97b2537f4c663064444021c85`.
- Refined atlas SHA256:
  `fa0b2e0bea72ab71b94d2752599bfc66fb642c0a64b748ca358ba9a2479e9249`.
- The source preview has passed Verify, CodeQL and Analyze Python; the
  dedicated preview workflow also completed successfully.

**Limit:** visual inspection of a transparent PNG is *offline-only*.
Real in-game sprite scale, layering, placement, pathfinding, desk attachment,
character contact, inventory tags and save/load remain untested. Do not
ship the preview artifact as a game mod or mark ART-001 complete.

## Approved source/package checkpoint, not a gameplay release

The art-only placement-test candidate was built by
[Actions run 41408148144](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41408148144)
against source `1fa723d336f95b27762a202a34aab9c64d003504`.

The downloaded test artifact `13124027790` was independently extracted and
verified: outer SHA256 `c634eac32d86ca6023af26197ba57e019e927b46ce911f6482b05b5e17980cbf`,
inner placement-only ZIP SHA256
`f39086a685c2ca557cec32e1538d874b4661792a5f68d3f7f8af7ee887b0196a`.
The inner ZIP has exactly 12 allowlisted files, contains both original objects,
texture atlas, two icons, bilingual strings, BUILD_INFO, isolated installer,
and no game DLLs, AES key or G1 clinical code. Its installer only creates
`StreamingAssets/Addons/ModABCLArt001Test` and refuses overwrite.

**This artifact is eligible for a single controlled disposable-save ART-001
placement/rotation L4, not for Alpha or independent staff laboratory interaction
acceptance.** [See the separate single-pass protocol](ART_001_SINGLE_PASS_L4.md).
The R3 clinical-path test need not be repeated.

## First ART-001 owner L4 — FAIL / NEEDS_FIX (2026-11-02)

The owner tested source `1fa723d336f95b27762a202a34aab9c64d003504`,
artifact `13124027790`, and reported: game start **PASS**, menu entries
**PASS**, names/descriptions **PASS**, placement on lab workbench **FAIL**,
four-direction rotation **FAIL**, scale/occlusion/character contact
**BLOCKED**, nearby staff walking **BLOCKED**, vanilla hematology and
other equipment noninterference **BLOCKED**. No screenshot/log or precise
UI error was supplied. **The original package failed L4 and must not be
reported as accepted.**

Original `Lopital.Floor.CanPlaceObject` checks
`AttachedToObject` against the current tile's center/parent object:
missing parent => `NOT_ALLOWED_ATTACHMENT_NO_PARENT`, parent without
`AttachmentSlot` or without an accepted tag =>
`NOT_ALLOWED_ATTACHMENT_WRONG_PARENT`. Original
`GameDBObject.AcceptsAttachment` is an exact membership check over the
parent's `AttachmentSlot.AllowedTags`. The vanilla
`OBJECT_TABLE_EQUIPMENT` and `OBJECT_TABLE_SQUERE` allowed-tag lists
omit both `abcl_art001_icp_ms` and `abcl_art001_digestion`; the first
candidate did not carry any compatible vanilla tag. This explains rejection
on original vanilla benches without assuming a missing texture.

**Source corrective candidate:** add only
`OBJECT_ABCL_ART001_WORKBENCH`, with an original installed-game
`ASSET_TEX_OBJECTS_SMALL` reference (no texture duplication), a private
attachment slot allowing only the two ART-001 tags, and
`ForcesAttachmentOrientation=false`. This leaves unmodified vanilla
tables and all vanilla procedure-routing tags. Use two private benches for
two private devices. The new source has static tests; actual loading,
placement, rotation and employee interactions remain **NOT TESTED**.

The forced-orientation property of vanilla tables is an additional possible
constraint on rotating attached devices, but the report lacks enough
observable detail to establish an independent four-direction rendering
defect. Keep reported rotation status **FAIL** until a corrected native
single-pass observation.

Do not request a new user L4 until the corrected source passes the
exact-source package gate and its asset manifest is independently audited.
The successful G1 R3 clinical test (artifact `13117942292`) is unaffected
and must not be repeated.

## Native-style visual redesign after owner rejection (2026-11-02)

The owner rejected the previous oversized/boxy equipment and asked that all
future laboratory expansions avoid visible ABCL branding. The approved rule
is `ABCL-D011` / `docs/LAB_VISUAL_STANDARD.md`.

The first simplified scaled-source candidate was itself rejected in offline
review: despite a neutral palette, the devices had no readable detailed
geometry. The procedural source was rewritten to draw an upright compact
mass-spectrometer analysis column/sample rack and a separate low-profile
digestion unit with safety hood and sample wells. Both draw front panels in
NW/NE and distinct rear ventilation/service covers in SW/SE.

Offline inspected source `af82f65eae54cae02bb1e8e1adf077620ec581a8`;
exact-source test candidate `82182ceb7ad99d1ac59289ec7d5b78305e7a76da`
adds a >100 visible-pixel pairwise-difference regression, without changing
artwork. Verify 17 tests (one existing skip), CodeQL, Analyze Python, preview
and standalone package workflow all PASS. Current full source/package audit
is recorded in `docs/TEST_EVIDENCE.md`; user-visible strings have no project
branding while resource identifiers remain namespaced.

**Current output is a source preview, not a native in-game acceptance.**
The earlier owner L4 remains 3 PASS / 2 FAIL / 3 BLOCKED. The new private
workbench, actual sprite size/contact, animations and staff pathfinding
still require one focused art-only L4 after owner visual approval. No G1
patient-generation regression is justified by this art change.

## Acceptance gates

| Gate | Status |
| --- | --- |
| Original editable source / no copied textures | Source delivered; inspect preview |
| Four directions, atlas, icons, bilingual strings | Source tests PASS; native four-direction FAIL (first L4) |
| Texture registration/loader, game placement | Menu entry PASS; vanilla bench placement FAIL; private parent source fix pending L4 |
| Desk anchoring, pivot, occlusion, proportions | Placement FAIL; scale/occlusion/contact BLOCKED |
| Staff pathfinding, native procedure animation/contact | BLOCKED / NOT TESTED |
| Two devices actually participating in ABCL procedures | NOT IMPLEMENTED |
| CBC + DLC/Workshop coexistence and save/reload | Original equipment noninterference BLOCKED in this L4; wider combinations NOT TESTED |

**Next permitted integration:** run static tests and review the generated preview;
then make an *isolated disposable-save art loader candidate* and check one
device's native placement/interaction in a single bounded L4 session. Only
after that succeeds should G1 testing tags be intentionally linked to original
ABCL equipment in a new test candidate. Do not call ART-001 complete based on
the sprite generator or green CI alone.

## Non-pixel-art visual concept direction — 2026-11-02

The owner explicitly rejected the earlier procedural pixel-block style and
requested direct study of actual Project Hospital laboratory sprites. The
user-provided original-game archives were used to extract **read-only style
references** from `StreamingAssets/Textures/objects_small_atlas.png`:

- `OBJECT_HEMATOLOGY_ANALYZER`: atlas 16 x 64, tile IDs 248-251;
- `OBJECT_RIA`: tile IDs 252-255;
- `OBJECT_TABLE_EQUIPMENT`: tile IDs 472-475.

Each atlas cell is 128x128. Original-game references show fine anti-aliased
isometric medical devices with soft tonal transitions, subdued light-gray and
slate surfaces, detailed distinct front and rear faces, and believable table
contact. These game-owned sprites are **study references only**, not resources
to copy or redistribute in the Mod.

An original smooth-isometric visual **concept sheet** was generated for a mass
spectrometer, sample-digestion workstation and instrument workbench, in four
notional views each. It is a **style exploration**, not a game sprite atlas:
not guaranteed to have consistent pixel-aligned pivots, directions,
transparency, equipment worktop scale, sprite footprint or original-engine
contact offsets. Any check-mark claims rendered on a concept sheet are
illustrative and do NOT establish gameplay or scale verification.

**Development gate:** the active source generator is now tools/generate_art_001_svg.py; offline staging uses the same generator. The previous pixel generator is deprecated and no longer called by active preview or staging. V7 native-cell bounds, custom icon safe areas and the private five-slot workbench palette pass source/preview contracts. This does not equal owner visual acceptance or L4. Review the exact v7 mobile sheet against vanilla HEM/RIA; only after owner acceptance may a separate ART-only test package be considered. Historical first L4 remains 3 PASS, 2 FAIL, 3 BLOCKED; keep PR #14 Draft.


## V7 active-source checkpoint — 2026-11-02

The active source of truth is now tools/generate_art_001_svg.py. The offline staging script imports that same generator; the rejected pixel generator tools/generate_art_001.py is retained only for historical audit and is explicitly deprecated. The v7 source calibrates the ICP-MS and digestion sprites against the native HEM/RIA alpha bounds, aligns both bottom edges with row 127 of the 128px cell, adds a third custom workbench icon with the official 60×60 safe area, and adds a private five-color ModColorSets.xml without changing a vanilla palette.

The exact preview artifact 13139014729 is preview-only and non-installable. It contains 16 files: 9 SVG sources, one 2048×1024 atlas, 3 64×64 icons, 2 previews and a manifest. Exact ZIP SHA256 3641e7a0939dfa3da641da137ca01216ef3cb79de925f8dc2f8070bc0ccb85bd; atlas SHA256 13a54b445d2ede60d14bfcc69b5eb23adfb4045558091c79e1743a9c5174afb1. The historical first owner L4 remains 3 PASS / 2 FAIL / 3 BLOCKED. No v7 in-game placement, rotation, contact, occlusion, staff route, save/load or vanilla equipment coexistence has been tested. G1 R3 clinical L4 remains accepted and must not be repeated for ART-001.
