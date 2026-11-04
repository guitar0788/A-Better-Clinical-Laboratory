# TO-001 R8: UI icon scale and first-frame room marker

Owner's two 2026-11-04 R8 screenshots show the approved red opaque Toxicology room-list icon drawn larger than vanilla neighbors. The floor marker shows native hematology first and the approved private isometric flask only afterward. Both are L4 FAIL for appearance; source art is approved and immutable.

Native DepartmentManagementLogisticsHybridController.CreateRoomButton positions rows at a 26-unit pitch. This patch caps only the target UI Image RectTransform to 24 units; it never edits, recolors or re-encodes the red/gray PNGs.

Native RoomRenderer.CreateRoomData creates every room glyph from vanilla TEXTURE_ASSET_FLOOR, and UpdateIconObject uses room.TextureID=376. The ABCL exact-room per-renderer private atlas swap previously waited up to 0.75 sec before scanning. Remove the delay and call the same scope-guarded pass through Camera.onPreCull on the main camera, after ordinary scene data updates and before draw. No original renderer or shared materials patched; unsubscribe and restore our own materials on disable.

New source tests cover icon size, both UI paths, no delay, callback cleanup and approved art SHA pins. Require genuine exact-head .NET 3.5/CLR2 compilation, audited complete package and one targeted game L4 before any claim of visual success. No changes to original art, independent instruments, floor UV 376, prefabs, clinical rules, saves, DLC, or other Mods.