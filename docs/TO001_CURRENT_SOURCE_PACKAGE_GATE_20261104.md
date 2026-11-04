# TO-001 R9 exact-source integrated package gate (2026-11-04)

The owner's approved artwork is frozen under D016, including both red/gray 64px room-list sprites, private isometric floor tile-376 atlas, two preview thumbnails, approved standalone two-device art and new uploaded prefab XMLs. No image or XML bytes were modified in R8.

## Verified real build

- G1 source commit: `9ae13683b63fa849582a72c62b9509c0eb65fe5d`.
- Real Windows net35/CLR2 compilation: https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41819512432 .
- Actual `ModABCLG1LeadTest.dll`: 30,720 bytes, SHA-256 `a096ecfcbeabf49b9cfdae15152cfc46ffa1c3095a8b3ebc75eaa1f743215755`. CLR2 marker `v2.0.50727` verified.
- Authentic Harmony1 1.2.0.1 net35 0Harmony.dll: 113,152 bytes; use original SHA and MIT license, **never the 0-byte sentinel from the standalone isolated G1 CI artifact**.

## Why R8 supersedes R7

Original `RoomRenderer.RenderRooms` supports room glyphs in BUILDING, BUILDING_FLOORS, and LOGISTICS. Previous G1 floor adapter only worked in LOGISTICS, preventing the owner's glyph from appearing in the building-room UI. New source enables exactly those original room-glyph modes. Original `RoomItemController.Update` and `IconController.SetIcon(string)` fall back to a vanilla sprite if custom icon cache lacks the ABCL sprite (confirmed by R6 read-only log). New source applies the already verified red/gray original Sprite to **both** native hybrid and legacy room-list rows, without replacing other Mod assets or shared icon atlases.

## Gates and limitations

This is code-only L3; R5/R6 remain L4 FAIL and R7 lacks gameplay L4 evidence. Both full-bundle builder and independent auditor now reject the previous R6/R7 G1 DLL and source hashes. The local R8 candidate was assembled from the audited R7 with only the new G1 DLL and BUILD_INFO updated. 32 unchanged entries, 8 owner-pinned asset/prefab hashes, two independent floor equipment objects, floor tile 376 and real Harmony1 were checked by a separate offline integrity pass; actual game L4 remains NOT_RUN.

Do not claim in-game icon success without a *single* focused owner room-list/red-background and building-floor/isometric screenshot plus logs. Do not auto-merge or release or change approved artwork, original GameDB, DLC, other Mods or save data.

## 2026-11-04 R8 owner display L4 FAIL / R9 exact replacement

Owner screenshots prove R8 menu icon size over native 26-unit pitch and vanilla hematology-to-private-floor transition. G1 source 9ae13683b63fa849582a72c62b9509c0eb65fe5d caps only the native ABCL room UI rect to 22 (24.2 under 1.1 hover), removes the 750ms floor scan delay, and adds a camera pre-cull exact-room pass without any global shader change or Harmony patch. Genuine Windows net35/CLR2 Actions #41823886803 produced a096ecfcbeabf49b9cfdae15152cfc46ffa1c3095a8b3ebc75eaa1f743215755 (31744 bytes). Independent complete ZIP L2 auditor verified 34 files and 32/32 unchanged members versus R8, frozen owner PNG and prefab hashes and 2 independent devices. Artifact #13318033401. Game R9 L4 is NOT RUN; no release claim.
