# FA owner visual acceptance — 2026-11-03

Repository: `guitar0788/A-Better-Clinical-Laboratory`  
Branch: `feature/art-001-two-devices`  
Issues: #3 / #24; Draft PR: #14

This is the **owner's binding, independent** visual result; it does not claim game L4.

| Resource | Owner decision | Exact treatment |
| --- | --- | --- |
| TO-001 dedicated room-list normal/disabled glyph | **VISUAL APPROVED** | Keep approved committed SVG/PNG bytes; no regeneration or changes. The UI native red/gray backdrops remain TS/runtime-owned and unproven. |
| TO-001 floor/zoning glyph | **VISUAL REJECTED / NEEDS_FIX** | Do not register, package, install, or copy the rejected source to any private atlas. Retire its obsolete source-only workflow from the active branch. Historical Git commits preserve the rejected vector and tests. |
| ART-001 mass spectrometer NW | **VISUAL REJECTED / NEEDS_FIX** | The owner-delivered previous 128x128 PNG + layered source are not approved. They are offline review attachments, **not** to be staged as production assets. Do not proceed to NE/SE/SW. |
| ART-001 digestion instrument and workbench | **BLOCKED** | Wait for NW approval and direction-identity gate. |

## Frozen approved room art

- `assets/art/to001/toxicology_room_icon.svg` — Git blob `c4a81670a2b0004799513c5b03a61b9239af1f5b`
- `assets/art/to001/toxicology_room_icon_inactive.svg` — keep current active-branch bytes
- `assets/art/to001/toxicology_room_icon.png` and `toxicology_room_icon_inactive.png` — existing Git blob `149bc34ebe68194d13054d91564c28700b5311ab`; two states share the exact same transparent-white glyph by design.
- Native original reference measurements: HEM room icon 24x35px; MIC 36x31px; HIST 32x33px; accepted Toxicology glyph 26x35px in a 64x64 cell.
- Previous [TO-001 original-source validation](https://github.com/guitar0788/A-Better-Clinical-Laboratory/actions/runs/41605312367) PASS was **source-only**; never equate it to native UI/disabled-state L4.

## Protected boundaries

This acceptance record is additive governance and removal of an **unapproved art experiment**, not a clinical change. No edits to G1 medical XML, TO prefabricated room XML, original textures/atlases, other Workshop mods, or private attachment parent/tags. Neither alpha release nor game package authorized. Keep PR #14 Draft; no auto-merge.

## Further work

- Floor and NW are **not approved** merely because another prototype has been drawn locally; art preview quality and owner acceptance remain separate gates.
- Reject an unconvincing 128px proof locally rather than asking the owner to reinstall the mod. Compare privately with native originals; do not upload copyrighted game pixels.
- The NW design must be one **compact tabletop device**, with believable integrated ion source, sample rack, controls, lighting and stable four-view source design; no built-in laboratory desk/double counter.
- TS integrates only **approved** files after source and runtime compatibility checks; the approved TO-001 room icon should not be conflated with its rejected floor counterpart.

## Follow-up rejection — floor N3 (2026-11-03, owner feedback)

The owner explicitly replied **"地面仍然不合格"** (floor icon still unacceptable). This rejects the newer offline TO-001 floor N3 review candidate in addition to all earlier floor variants. It is **NOT** an approval, a request to reinstall the game, or authorization to merge. No user L4 is requested.

A side-by-side read-only comparison of owner's original floor tiles `tiles_376.png`, `tiles_377.png`, `tiles_378.png` (256×128 per cropped cell) with `toxicology_floor_mask_256x128_N3.png` confirms the substantive error:

- The original three floor sprites are simple, near-white **mostly filled silhouettes** without internal outlined laboratory-glass icons or secondary inset lines. They differ in footprint/structure but share that sparse filled graphic language.
- N3 is a **hollow, multi-stroke flask diagram with interior details**; even a matching cell size, clean transparency and edge-safe bbox cannot make it stylistically equivalent.
- Measured opaque-pixel coverage of full 256×128 cells: original tiles 376 ~8.7%, 377 ~13.9%, 378 ~8.6%; N3 ~9.0%. Similar overall coverage demonstrates that the mismatch is **contour/fill/negative-space design**, not simply canvas scaling. These are measurements of owner's read-only game assets and rejected candidate; **no native pixels are committed**.

**Disposition:** Mark N3 `VISUAL FAIL / REJECTED`; do not reuse its SVG/PNGs in the current TS private atlas or submit a further incremental line-thickness/scale tweak. A future floor proposal must change the art *method*, first show one native-style filled silhouette with 1× baseline comparison, and require owner visual approval **before** any asset commit or native adapter test. The accepted 64×64 room-menu glyph is unaffected and remains locked at SVG Git blob `c4a81670a2b0004799513c5b03a61b9239af1f5b` and PNG blob `149bc34ebe68194d13054d91564c28700b5311ab`. All previous art is retained as historical/offline evidence. Issue #24 stays open; PR #14 stays Draft.
