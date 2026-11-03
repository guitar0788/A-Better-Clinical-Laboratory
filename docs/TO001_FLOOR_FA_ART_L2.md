# FA TO-001 — Independent Toxicology Floor Glyph (L2 source-only review)

**Status:** Original FA floor art candidate only; NOT a registered game asset or game-visible fix. Issue #24 stays OPEN, PR #14 stays Draft. This work never changes G1 medical code, base-game atlases, native floor room colors, vanilla/DLC XML, or Workshop assets.

## Why a distinct source is required

[TS Draft PR #29](https://github.com/guitar0788/A-Better-Clinical-Laboratory/pull/29) established the real native floor glyph is rendered using `RoomRenderer.RenderRooms`, `GameDBRoomType.TextureID=376`, `TileTextureHelper` and `TEXTURE_ASSET_FLOOR`. That is a **different path** from the 64×64 room-menu custom icon (`IconIndex=850`). Retinting or resizing the room-list art will never replace the on-floor/zoning symbol.

TS exact source `49475e91cabb2fa361c85e28d2f29ee0b7510c17` has genuine Windows net35/CLR2 **L3 build PASS** recorded in [Actions #41588842602](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41588842602). **This earlier package did NOT contain a private floor atlas**, so it does not prove the new sprite can render, compose with native zone tint, or safely coexist with other mods. The new artwork must not be automatically packaged.

## New original FA deliverable

- `assets/art/to001/floor/toxicology_floor_glyph.svg`: independently editable original **128×64** artwork — one isometric analytical flask, linked chemistry motif and small sensor. This **is not a scale-up of the 64px menu SVG**. Neutral-white `#F2F2F2` strokes only; completely transparent backing. No original game pixels copied. Real native floor-icon style still needs owner **L4 visual** comparison because its original full floor atlas is not distributed here.
- `tools/build_to001_floor_art.py`: deterministic high-resolution CairoSVG vector rasterization (512×256) and Lanczos reduction to original **128×64 RGBA**. Builds a new **2048×2048 RGBA** private 16×32 texture. Writes only tile index **376** (zero-based column **8**, row from image top **23**; exact atlas rectangle `[1024,1472,1152,1536)`); all other cells have **zero alpha**. No red/gray or room/zone color in the PNG.
- `.github/workflows/to001-floor-art-review.yml`: isolated source-only artwork verification; checks exact tile dimensions/cell position, no other tile with content, source manifest SHA256, transparency and no compiled DLL/keys. It uploads only a **NOT-INSTALLABLE review artifact**.
- Generated review (not source-controlled native asset declaration): `toxicology_floor_glyph_128x64.png`, `toxicology_floor_atlas_private_376.png`, `to001_floor_native_size_review.png`, `manifest.json`. Preview uses a **simulated neutral-gray background**, not an original-game screenshot.

## Compatibility and TS handoff

FA gives TS one review-only candidate with manifest ID `ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS` for exact room `ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB`. **No GameDBAsset XML is added by FA.** TS must only register/use it in a **new, separately audited L3+L4 test package** after validating scoped `RoomData.m_roomIcon` renderer ownership, matching atlas UVs, texture lifecycle, fail-closed replacement, and restore-on-view/floor-change. Never overwrite native shared `floor_room_icons`, assign an unproven global index, force a zone color, or modify `TextureID=376` on unrelated rooms.

A real owner L4 must check: room-list icon **and** on-floor glyph separately, current and adjacent floors, view switching, multiple Toxicology rooms, normal/disabled/hover, reopening, save/reload, original hematology/microbiology/histology, four official DLCs and noninterfering Workshop mods. A green FA L2 or earlier TS L3 is **not** L4.

TO-002 relationship chart artwork remains out of scope until TS confirms that separate screen's actual resource specifications. G1 and TO-003 were not edited.

**Disposition:** source-only art candidate available; TS technical integration pending, user visual approval pending, no merge/release.
