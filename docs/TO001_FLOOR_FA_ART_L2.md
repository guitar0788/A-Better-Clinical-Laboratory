# TO-001 — Menu and floor share one original icon source

**2026-11-03 FA correction.** The user rejected the separately authored floor icon with its detached square badge. That source and generated standalone binary have been deliberately removed from the Draft PR #14 working tree. Previous Actions L2 only proved atlas placement and must not be cited as art acceptance.

## Actual original game evidence (read-only)

The owner-supplied vanilla files show the **same visual motif** at two technical render surfaces, not necessarily the same PNG/atlas: Hematology menu IconIndex **850** and floor TextureID **376** are both paired test tubes; Microbiology **2868/377** both represent a microbe; Histology **854/378** both represent a molecular structure. The original menu atlas is StreamingAssets/Textures/ui/icons.png (64x64 icons). The original floor atlas is StreamingAssets/Textures/tiles_4096_atlas.png (**4096x4096**, 16x32 = **256x128** original pixels per cell). The earlier FA claim that the original floor atlas was 2048x2048 was wrong. TS PR #29 instead uses a **private** 2048x2048/16x32 atlas, yielding **128x64** private cells; equivalent UV topology but smaller original-pixel resolution. Native L4 visual appearance remains unverified.

## One editable source, two output formats

- Only canonical authored Toxicology motif: assets/art/to001/toxicology_room_icon.svg. The existing 64x64 transparent menu art remains unchanged.
- tools/build_to001_floor_art.py reads the same original SVG groups and applies a deterministic isometric affine view. It does **not** paint new equipment, badges, small squares, logos or a second freehand flask.
- In the source-only FA Actions artifact (not the repository's committed runtime resources): derived_floor_glyph_editable.svg, toxicology_floor_glyph_128x64.png, toxicology_floor_atlas_private_376.png, TO001_shared_symbol_review.png and manifest.json.
- Private atlas tile 376 occupies (1024,1472)-(1152,1536) in 2048x2048; all other pixels zero alpha. Floor sprite contains white original motif only, with no native zone-color panel.
- Review preview uses **simulated** menu-red and neutral-gray backdrops solely to make the small white glyph visible. It is not an actual game screenshot.
- The CI checks original source SHA, original projection, no stale independently designed floor SVG/PNG, exact tile coverage and file hashes. No original game pixels are committed to GitHub.

## TS boundary

TS PR #29 compiled the floor renderer on Windows at source 49475e91... before this new derived floor artwork existed. That previous L3 pass is **not** L3 for this texture. Before integration, TS must verify original room glyph ownership, material/UV lifecycle, same-room-only substitution, transparent background composition, disabled/hover state and restoration when changing floors/view modes. Current Issue #24 stays OPEN pending owner visual acceptance and real L4 for both menu and floor, vanilla lab icons, all official DLC and relevant Workshop assets.

No G1 medical changes, original atlas changes, vanilla IconIndex/TextureID changes, untested installation packages, TO-002 art, automatic merge or release.