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
