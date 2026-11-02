# ART-001 — FA mass-spectrometer V3 physical art redesign (NW only)

**Status: visual quality NOT approved.** The owner requires smooth antialiased high-quality original Project Hospital-style 2D equipment, not pixel blocks, not a screenshot infographic and not a generic shaded server box.

## Why V2 failed and what V3 genuinely changes

The last owner-unapproved V2 model improved technical 3D enclosure but still resembled a long server box at native size. The display and specimen region were weak relative to the game's native HEM/RIA. A stronger **functional component hierarchy** was required, not more color grading.

V3 keeps the original closed manifold main equipment housing and original ionizer but **physically reconstructs the front operator region**:

- Retires V2's embedded, non-functional blue monitor and duplicated tiny keyboard.
- Builds a recessed analyzer optical chamber with a real top shutter edge, split glass and discrete spectrum readout.
- Introduces a genuinely supported, independently recognizable monitor: machine-fixed supporting ledge, heavy foot, upright stem, swivel hinge, framed LCD, ten luminous graph elements and physically attached two-row keyboard.
- Makes specimen carrier visibly meaningful with seven individually modeled larger blue-capped transparent tubes on a fixed white eight-slot instrument tray. No pasted pixel blocks.
- Changes the ionizer structure with a real inset service strip, anchored insulating collar and several labeled monitored ports.
- Retains physically different rear vent panel, front controls and machine safety edges. The current image shows NW only; no assumption of correctly exported other views.

## Art/technical contract

- Blender source: `tools/art001_mass_redesign_v3.py` operating on existing independently editable FA-only V2 source.
- Real `1024x1024` Cycles original render; LANCZOS smooth downsampling to transparent `128x128`. No nearest neighbor, forced four-color palette, pixel-art preprocessing or copying original-game pixels.
- Source outputs: one new editable `.blend`, high-resolution source PNG, one real NW game-scale PNG, a two-layer OpenRaster source, human-readable preview and SHA256 inventory.
- Source-only GitHub workflow: `.github/workflows/art001-mass-v3-nw.yml`. CI may pass L2 while aesthetic quality remains unacceptable.
- Compare V3 at **actual 1x** beside legally supplied vanilla HEM 248–251 and RIA 252–255 (read-only) and against owner-designated high-detail concept. Do not publish native reference pixels in GitHub or artifact.
- Do not continue generating 8 directions or a second machine until a real NW design is approved by owner. If V3 still fails, fix underlying shape hierarchy and purposefully art-directed 2D shading rather than repeat a machine/preview version cascade.

## Boundaries

Draft PR #14; no new PR. No change to G1, clinical code, GameDB/XML, original equipment tags/IDs, native texture atlas, room/staff/placement or save data. TS owns physical placement, rotations, collisions and L4. No DLC or Workshop compatibility claim; original ART L4 remains 3 PASS / 2 FAIL / 3 BLOCKED. **Never merge, publish or generate an installable game pack from this study.**
