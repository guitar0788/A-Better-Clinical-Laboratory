# TO-001 — Native room-list red backing, R9 owner screenshot

## R9 L4 observation

The owner confirms the **floor isometric flask L4 PASS** on R9. Preserve it and do not rework floor art or renderer. The room-list icon is visible and size-correct but the red backing is **darker** than the original hematology/microbiology icons; this appearance is R9 L4 FAIL. Do not redraw or recolor the owner-approved 64x64 PNG.

## Original asset and code evidence

- Original shipped `StreamingAssets/Textures/ui/icons.png`, e.g. glyph atlas positions 850/854 and 2868: white/gray pixels have alpha and surrounding alpha=0. The game displays the original prefab's red background behind the transparent glyph.
- The approved original toxicology active source PNG is **opaque at all 4096 pixels**, solid red background RGB(171,48,62) and white flask (SHA-256 `225b2918c448b5d36d1d8582389e8952f2baf1574d0d72935017c81eab7d8199`). Disabled is opaque gray RGB(120,120,120) (SHA-256 `50c17ea8ba8b42b28295564f594713069a31c9e48fa05f3a6b623a36851b6490`). A direct `UnityEngine.UI.Image.sprite` replacement paints the baked dark red **over** the existing vanilla red. A white image tint cannot lighten baked red.
- Native `SegmentItemIconTextTextIconController.UpdateData` sets only the sprite, leaving the prefab's backing. It overwrites each frame; existing ABCL LateUpdate corrects only the exact Toxicology room row.

## Code-only corrective behavior

- Leave the **exact approved source bytes unchanged** and verify SHA-256 as before. For only those two 64x64 room-icon files, recover the original antialiased white flask alpha coverage at runtime from the known solid background, and create a cached, transparent overlay sprite in RAM. Active foreground uses the native atlas white RGB(242); inactive uses native gray RGB(77). No on-disk files generated, recolored, exported or replaced.
- Let the native UI backdrop (already used for vanilla labs) show through. Do not add guessed or baked-in color values to the room row; only the target sprite and existing white Image tint are used. The 22-unit native row scale remains unchanged.
- Existing third-party `overrideSprite`/custom icon conflict guards remain; no global icon atlas or other Mod is modified. The **floor L4 PASS code path and every approved art/prefab XML/device file remain unchanged**.

## Gates

Offline source regressions and genuine Windows .NET 3.5/CLR2 exact-head compile must pass before creating an integrated test ZIP. A single targeted owner L4 check of the room-list red against vanilla and no regression in floor glyph is required to mark complete; `Verify`/ZIP/compile alone are not native L4. Keep Draft, do not merge/release before evidence.