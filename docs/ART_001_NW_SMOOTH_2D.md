# ART-001 NW smooth 2D source proof

**Owner visual gate remains FAIL.** The previously shown NW pixel-style paintover and previous V7-V10 / Blender V1 art do not meet the owner's Project Hospital 2D standard.

The owner explicitly requests **smooth, detailed, antialiased original 2D—not pixel art**. This source-only generator is a targeted correction to the rejected processing method:

- Reopen the original editable ABCL Blender source; render only the mass spectrometer NW at genuine 768x768 resolution, not upscale a 128px sprite.
- Smooth Lanczos reduction to a transparent 128x128 output, with natural antialiased alpha. Keep intermediate tonal values; do not reduce shades to an artificial four-color palette.
- Retain a gentle editable contour as a separate OpenRaster layer. Preview enlarged using Lanczos rather than nearest-neighbor.
- New art-only sources: tools/art001_smooth_nw.py and .github/workflows/art001-smooth-nw.yml.
- Deliver original high-res render, native-size PNG, editable OpenRaster layers, smooth mobile preview, SHA256 manifest. Source-only review artifact; NOT installable.

**Remaining limitation:** the existing machine's overall form still needs substantial artistic redesign to match the owner's detailed concept board and vanilla HEM/RIA. Process improvements cannot substitute for human visual acceptance. This is **not** declared a completed art asset.

Do not modify G1 clinical code, private attachment, GameDB IDs, XML registrations or original game files. No GameDB atlas replacement, no DLC/Workshop compatibility assumption, no L4, no merge, no release. TS owns integration; FA stays on Draft PR #14.