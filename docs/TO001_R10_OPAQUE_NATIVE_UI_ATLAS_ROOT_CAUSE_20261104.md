# TO-001 R10 FAIL — correct native room icon palette and no transparent layer

**Owner-provided R10 screenshot, 2026-11-04:** the Toxicology Laboratory room-list icon became transparent again. Owner states that purple color keys are the only elements automatically recolored, not alpha-zero background. R9's floor isometric icon was explicitly **L4 PASS** and **must never be changed**; R10 room-list color is **L4 FAIL**.

## Root cause, now supported by original game assets, not guesses

1. `IconManager.LateInit` maps integer atlas index (x = index % 32, y = index / 32) to `StreamingAssets/Textures/ui/icons.png`. A previous purported extraction of native 850/854 used the wrong atlas region, showing transparent foreground-only images. That false sample caused the wrong R10 patch.
2. Correctly sampled vanilla room-list icons **850 (Hematology), 854 (Histology), 2868 (Microbiology), 808 (Cleaning closet)** have opaque red background RGB **(201,63,61)** with antialiased white **(242,242,242)**. Matched disabled icons 851/855/2869 have opaque gray **(153,153,153)**. The colored background is part of the atlas sprite itself; `SegmentItemIconTextTextIconController.UpdateData` does not create a red underlay.
3. Official developer tutorial confirms hue 300° changes the color of scene OBJECT/WALL/TILE textures, not room-list UI sprites. There is no verified purple-key step in the UI adapter.
4. Approved owner source PNGs are fully opaque with dark red RGB(171,48,62) or gray RGB(120,120,120). R9 rendered this matte too dark; R10 incorrectly stripped it to transparent and assumed native UI would fill red. Both were wrong code decisions, not owner artwork defects.

## Correct, code-only bounded fix

- Keep the **exact original SHA-256 owner PNG bytes untouched on disk**. Verify SHA as before, and once per UI icon decode the existing approved flask's antialiased coverage from its known solid backing.
- Create only a private 64×64 runtime UI Sprite using the **exact sampled vanilla room palette (201,63,61 / 153,153,153)** and white glyph 242; every runtime pixel alpha=255. The source PNG remains byte-identical. Do not colorize by a guessed purple key or rely on a nonexistent automatic red underlay.
- Preserve exact RoomId scoping, foreign override guards, 22-unit UI cap, all languages, all instrumentation, and crucially the original **PASS** private floor code, floor tile 376, two standalone instruments and prefab XML.
- Do not inject a copy of any game icon into the public repository. The numerical color values here come from the owner's local reference and the original game atlas; original game assets remain with the player.

## Acceptance and release

Source contract tests, genuine Windows net35/CLR2 compile and complete audit must all pass before any new package. Only **one focused in-game L4 check** of the menu's native-color background and regression-free floor is warranted. The R10 L4 FAIL remains; neither source nor ZIP checks establish native L4. Draft, no release or auto-merge to main.
