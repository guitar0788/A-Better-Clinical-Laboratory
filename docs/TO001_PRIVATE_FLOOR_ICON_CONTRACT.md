# TO-001: exact-room private floor glyph — TS source contract (candidate)

**Status:** TS source candidate only. **NOT installed or L3/L4 approved.** #24 stays NEEDS_FIX. This work is completely separate from the room-list 64×64 UI thumbnail (#24, FA) and relationship/dependency tree (#25).

## Verified native source facts (owner-supplied decompile; do not redistribute original binaries/images)

- `RoomRenderer.Init` reads `TEXTURE_ASSET_FLOOR`, `CreateRoomData` creates a separate `RendererObject("FloorSelectionMarkerIcon", "Materials/floor_room_icons", ...)` per room, and `RenderRooms` writes the glyph mesh UVs with `UpdateIconObject(room, ..., room.m_roomPersistentData.m_roomType.Entry.TextureID, ...)`.
- `TileTextureHelper.GetTileTextureCooridnates` uses a **16-column × 32-row** atlas. Current additive ABCL room is `ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB`, `TextureID=376` (zero-based column **8**, zero-based row **23** from image top). The ordinary UI thumbnail uses a completely separate `IconIndex=850`, which is the native hematology fallback.
- `MapEditorController.sm_instance.CurrentFloorRenderer` exposes the active floor's `MapRenderer`; the private `m_roomRenderer` and `m_roomData` map to `Room` → `RoomData.m_roomIcon.m_gameObject`.
- `RendererObject` sets the per-instance `Renderer.material.mainTexture`. A scoped texture replacement on this *specific existing room-glyph renderer* avoids changing a shared vanilla asset, material, atlas, room metadata or room highlight/zone colors. It has **not** been validated by genuine net35 compilation or gameplay yet.

## TS candidate behavior

`G1ToxicologyPrivateFloorIconAdapter` (in G1 Panel source) runs only on the Unity main thread via `LateUpdate` and only in LOGISTICS scene/mode. At most every 0.75 seconds, it accesses the **current** floor, finds only live renderer entries whose exact native room DB ID matches the ABCL room, and only replaces the individual renderer's `material.mainTexture` when it currently equals the original `TEXTURE_ASSET_FLOOR`. It cannot mutate `IconIndex`, `TextureID`, the underlying tile texture, global UI or room save data.

It requires **all** of:
- private, original `GameDBAsset` ID `ASSET_ABCL_TOXICOLOGY_FLOOR_TILE_ATLAS` registered as a standalone texture;
- loaded `Texture` exactly **2048 × 2048** with a 16 × 32 grid (each cell 128 × 64);
- original floor baseline texture present, original internal fields present, and live matching ABCL room renderers;
- safe, unmodified per-renderer native baseline. If another mod already changed the renderer's texture, this candidate **does not overwrite it**.

When the asset is absent or the view changes, it leaves/reverts to the original texture. If any guarded code fails, it logs once, reverts only owned texture swaps and disables itself. **It never writes a persistent game or original asset field**.

**Not yet packaged:** the required floor-specific private atlas and its XML registration are intentionally absent pending FA artwork and TS asset validation. Current test installations will therefore continue to use the native floor icon. Do not label this as fixed, L3 or L4 PASS.

## FA artwork handoff

Create a **separate editable, original floor glyph**, not the red/gray 64px room-menu thumbnail. Follow the actual original floor-icon style and its alpha/line thickness. A full private **2048×2048 transparent RGBA** atlas is the delivery representation, with artwork **only** in tile **376**: column 8, row 23 from top; pixel rectangle (x=1024..1151, y=1472..1535), dimensions 128×64. All other tiles stay fully transparent. No opaque room-color rectangle; native `RoomRenderer` continues supplying room-zone/access colors. Do not copy any original game tile art into the public repository. Deliver PNG, editable source, a source-only verification and hashes.

**FA does not need to produce this new floor-specific atlas until TS/owner confirm that the private material path compiles and renders safely.** If a genuine L3 cannot bind this exact source ABI, stop rather than create a false native icon replacement.

## Required gates

- [x] Confirm original room floor glyph uses `TextureID`, not `IconIndex`.
- [x] Add scoped, missing-asset-inert candidate and source-only tests.
- [ ] Genuine Windows .NET 3.5 / CLR2 compile and package audit of this candidate.
- [ ] Source-controlled FA atlas contract + private `GameDBAsset` declaration in a dedicated test package.
- [ ] Focused disposable-save L4: ABCL floor icon with 1+ rooms, switch floor/views, save/load, disabled/hover states, remove ABCL while baseline still loads.
- [ ] Regression: original labs, room-zone colors, 4 DLCs and noninterfering Workshop combinations.
- [ ] Owner aesthetic acceptance and no main merge/release until full gates.

**Stop condition:** if the original `RendererObject` material/texture update or version-specific ABI cannot be safely scoped to ABCL, record evidence and mark floor-glyph customization NO-GO; do not patch the original floor atlas.
