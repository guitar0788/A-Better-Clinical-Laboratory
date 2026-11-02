# ART-001 — original toxicology instruments (source candidate)

**Status:** source and XML candidate, **not an installed or gameplay-validated device**.
Tracked under [ART-001](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/3).
This branch is independent of the still-Draft G1 test harness. The owner's G1 R3
clinical L4 report is accepted for artifact 13117942292; no repeat is required.

## Shipped in this source branch

- A self-contained, originally authored deterministic 2D pixel-sprite generator
  at `tools/generate_art_001.py` (Python standard library only).
- Two prototypes: the ABCL ICP-MS toxicology mass spectrometer and the ABCL
  enclosed sample-digestion workstation.
- Four separately rendered isometric directions per instrument: NW, NE, SE,
  SW. Eight unique atlas tile IDs, shared canvas dimensions and pivots.
- One optional, additive `GameDBAsset` atlas and two local custom icon entries.
- Two ABCL-only `GameDBObject` declarations, based on *structural conventions*
  of original tabletop objects. Native staff animations are only **references
  to vanilla animation names**, not redistributed frames.
- English and Simplified Chinese object names and descriptions.
- `tests/test_art_001_assets.py` for PNG signature/dimensions, unique frames,
  slots, localization, object IDs, collision-safe unique tags and G1 isolation.

## Render source → assets

Run from the repository root:

```sh
python tools/generate_art_001.py --output /path/to/temporary/art001-build
```

Generated outputs are:

```text
art001-build/
  Assets/ABCL/equipment_atlas.png
  Assets/ABCL/icp_ms_icon.png
  Assets/ABCL/digestion_station_icon.png
  Previews/ABCL/direction_preview.png
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

This creates `Art001Proof/Database/` with the two original object entries,
bilingual text, asset references and an art-preview-only addon identity;
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

## Acceptance gates

| Gate | Status |
| --- | --- |
| Original editable source / no copied textures | Source delivered; inspect preview |
| Four directions, atlas, icons, bilingual strings | Automated contract test pending |
| Texture registration/loader, game placement | NOT TESTED |
| Desk anchoring, pivot, occlusion, proportions | NOT TESTED |
| Staff pathfinding, native procedure animation/contact | NOT TESTED |
| Two devices actually participating in ABCL procedures | NOT IMPLEMENTED |
| CBC + DLC/Workshop coexistence and save/reload | NOT TESTED |

**Next permitted integration:** run static tests and review the generated preview;
then make an *isolated disposable-save art loader candidate* and check one
device's native placement/interaction in a single bounded L4 session. Only
after that succeeds should G1 testing tags be intentionally linked to original
ABCL equipment in a new test candidate. Do not call ART-001 complete based on
the sprite generator or green CI alone.
