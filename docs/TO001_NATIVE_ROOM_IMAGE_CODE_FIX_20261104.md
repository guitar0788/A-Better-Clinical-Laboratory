# TS code-only TO-001 native room-icon fix — 2026-11-04

Applies only to the exact `ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB` room button in the native `DepartmentManagementLogisticsHybridController` lists.

- The owner-supplied 64x64 room sprites have **opaque**, already-correct red and gray backgrounds. No pixel/color/source editing is authorized. Pin these assets separately as recorded in governance Draft PR #48.
- The previous UI bridge used runtime lookup by the string `"Image"` and reflected the `sprite` property; this was silent/fail-closed, and the old R3 package used a DLL which was **not** built from the current native-root binding source. This code branch replaces that fragile reflection with a type-safe `UnityEngine.UI.Image` and explicit `UnityEngine.UI.dll` net35 assembly reference.
- Rebind only in `ModEntryPoint.LateUpdate` and only after verifying the exact native button by its stable room ID. The native `UpdateRoomButtons` will continue to write the original `IconIndex` sprite on each Update.
- The source-backed colored image is rendered on an opaque white UI tint **only for this ABCL row**. Other native departments, UI icons, original atlases, DLCs, and Workshop content are not changed.
- If another mod supplies `Image.overrideSprite`, the ABCL bridge fails closed instead of replacing it.
- Add one bounded runtime success log, plus one bounded override-conflict warning, so a later L4 log can distinguish source binding from package/stale-DLL issues.
- **Source-only candidate:** This commit does not modify any bitmap, XML clinical definitions, floor shader, compiled DLL, installer, prefab or original game binary. The packaged R1/R2/R3 versions are rejected as historical test candidates, not evidence that the new source fix works.
- Release gate: genuine net35/CLR2 L3 from this exact new source SHA, package manifest retaining owner-approved image hashes, and then one focused L4 check of room icon + floor. No repeated full G1 clinic tests unless actual clinical code changed.
