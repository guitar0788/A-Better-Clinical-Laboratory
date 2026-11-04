# TO-001: Original room marker view modes, 2026-11-04

## Original evidence, not image speculation

The owner's uploaded `dll_ilspy.zip` contains `RoomRenderer.cs`. In `RenderRooms`, line 62, the native room folder returns only if the floor render mode is not NORMAL or the view is GAME_NO_WALLS, GAME_WALLS, or DOCTOR_MODE. It actively calls `UpdateIconObject(room, roomIcon, roomType.TextureID, ...)` on line 119 for valid room overlays. `ViewModeController.SwitchMode` separately defines BUILDING, BUILDING_FLOORS and LOGISTICS. Both BUILDING modes show room glyphs, not just LOGISTICS.

The previous ABCL G1 `G1ToxicologyPrivateFloorIconAdapter.Tick()` explicitly rejected every mode other than LOGISTICS. Therefore the approved private tile-376 isometric flask could not appear in a building/room-allocation view, even if its SHA/asset resolution succeeded. That logic itself was defective.

## Change

Allow the exact per-room floor glyph override in BUILDING, BUILDING_FLOORS and LOGISTICS. Continue to fail closed and restore our own texture outside native room-overlay modes. Keep original room `TextureID=376`, owner-approved 2048px atlas SHA, vanilla material/tint and color, collision protection and room-identity filter. There is no global texture registration or sharedMaterial edit.

No changes to: approved room-list red/gray icon bitmaps, floor isometric artwork, equipment artwork, two independent floor devices, both latest prefab XMLs, game original source, DLCs, third-party Mods or medical logic. All earlier R6 screenshot failures remain genuine L4 FAIL; this is an L2 source correction to be compiled in exact-head Windows net35 and audited in a single full package before focused L4.

The menu room-list icon is a **separate UI path** and remains L4 unverified after R7; this floor-mode fix does not assert it passes.
