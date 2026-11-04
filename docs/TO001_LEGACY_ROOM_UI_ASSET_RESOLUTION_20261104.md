# TO-001 legacy room-list icon uses native fallback on missing custom ID

Evidence: original `RoomItemController.Update()` assigns integer `IconIndex` to its `IconController` for the exact room ID. Original `IconController.Update()` converts `SetIcon(customID)` to `IconManager.GetIcon(customID)`; original `IconManager.GetIcon(string)` returns the unrelated vanilla m_iconSprites[0,0] if the custom key is absent. R6 diagnostics confirm the private custom sprite was missing in the game cache.

Earlier G1 implementation correctly prepared SHA-pinned approved red/gray source sprites, then bound them to the native hybrid room list; **but its legacy RoomItemController path still called `icon.SetIcon(assetId)`**, re-entering that confirmed wrong fallback behavior.

This fix also binds the exact SHA-pinned current-state sprite directly to the original `RoomItemController.m_icon` child `UnityEngine.UI.Image`, using the original Unity types through compile-reference-safe component property inspection. Only the target with `m_roomDatabaseID == ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB` is touched. A foreign custom icon ID or a different explicit `Image.overrideSprite` blocks the write; other rooms, game assets, DLC and third-party Mods remain unchanged. No global IconManager mutation or palette edits.

Room-list and private floor fixes need one genuine exact-head net35/CLR2 build plus independent full-archive audit. D016 SHA-pinned owner images and latest 8x6/12x6 XML must remain byte-identical. This is source-level confirmation, not a claim of in-game L4 PASS. Keep Draft and no auto release.
