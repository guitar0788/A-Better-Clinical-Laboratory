# TO-001 — Dedicated Toxicology Laboratory room-draw icon (FA delivery)

**Issue:** [#24](https://github.com/guitar0788/A-Better-Clinical-Laboratory/issues/24). **Status:** FA original room-icon resource delivered for owner visual review; **NOT** yet accepted, registered in the game, or verified in L4.

## Original artwork

- Editable source: `assets/art/to001/toxicology_room_icon.svg`.
- True final source PNG: `assets/art/to001/toxicology_room_icon.png` (64×64 RGBA; a strict 2px transparent boundary, crop-safe at `Rect(2,2,60,60)`).
- Source-to-PNG regeneration: `tools/build_to001_icon.py`. It rasterizes at 512×512 using CairoSVG, smooth Lanczos downsampling to 64×64, reserves the native cropped margin, emits a mobile-friendly source-only review sheet and SHA256 manifest.
- New source-only CI: `.github/workflows/to001-icon-preview.yml`; verifies actual committed icon pixels against regenerated SVG, format, 2px margin, alpha and namespaced IDs.
- Art direction: a **single clinical analytical flask with a molecular-analysis mark**, white flat non-pixel glyph over a restrained teal-green panel. This is intentionally distinct from vanilla hematology's twin test tubes; no text, developer branding, "test" badge or copyrighted native artwork. Vanilla `StreamingAssets/Textures/ui/icons.png` was consulted **read-only** for UI style and icon sizes; it is **not copied or embedded**.

## TS integration handoff — not done here

The existing TS source audit in Issue #24 shows:
1. `GameDBRoomType.IconIndex` is numeric only, and the Toxicology room currently uses **850**, already the hematology room's original/DLC icon. Do **not** overwrite 850 or invent `CustomIconAssetRef` in the room type XML.
2. `IconManager.LateInit` supports namespaced `GameDBAsset` entries of `TEXTURE_CUSTOM_SPRITE`; `IconController.SetIcon(string)` supports the named sprite. The **native room menu row uses `SetIcon(int)`**, so a private asset by itself **does not** display in the room-draw menu.
3. Proposed exact-resource ID: **`ASSET_ABCL_TOXICOLOGY_ROOM_ICON`**, target room ID **`ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB`**. When TS has confirmed the legal asset declaration and a collision-safe UI event/lifecycle scope, copy the PNG into a packaged **ABCL-private Assets** path and declare only that asset. Do not add clinical-equipment tags or alter the current G1 logic. No game XML or runtime changes are committed in this FA art delivery.
4. TS's proposed Harmony-free, exact-row-scoped adapter is *only a design*: it has not passed true net35 L3 nor native-menu L4. Before adding UI code, validate room-menu lifecycle and fail-closed behavior if the sprite is missing. Existing 850 hematology icon is the fallback only.
5. Final owner-visible acceptance: only the Toxicology room row changes; native hematology/microbiology/histology and Infectious Diseases DLC rows stay untouched, and compatible Workshop items remain unchanged. Test first entry, closing/reopening the room menu, save/load and menu performance in a disposable save.

## Gates and responsibilities

| Gate | Current state |
| --- | --- |
| FA original icon and editable source | **Delivered, pending visual acceptance** |
| 64×64 smooth RGBA and exact 2px crop contract | **Implemented; CI source proof required** |
| GameDBAsset private registration | **TS NOT IMPLEMENTED** |
| Exact-room native row adapter and net35 L3 | **TS NOT IMPLEMENTED** |
| Real room-selection icon L4, vanilla/DLC/Workshop noninterference | **NOT TESTED** |

Keep Issue #24 **OPEN** until verified game-menu L4 and owner acceptance. Leave Draft PR #14 and clinical PR #7 unmerged. No installable build/release or original-game file overwrite is authorized by this art-only resource.
