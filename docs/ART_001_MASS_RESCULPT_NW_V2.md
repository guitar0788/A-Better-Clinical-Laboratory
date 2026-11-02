# ART-001 FA: substantive NW mass-spectrometer resculpt

**Owner visual acceptance: NOT MET. Source-only study, no game package.**

This stage responds to the owner's repeated rejection of pixel art, primitive SVG box silhouettes, bland Blender V1 and arbitrary paint filters. The previous 128px NW smooth test is archived as evidence that technical antialiasing alone cannot solve a poor design.

New work: tools/art001_mass_redesign_v2.py. Unlike previous texture-only filters, this **rebuilds the mass spectrometer's actual original editable geometry**, while reusing only the prior Blender materials, camera rig and untouched second instrument as a non-rendered source baseline.

New shape-specific original content:
- Closed, one-piece custom cross-section enclosure with structural shoulders and molded top, not a stack of generic cubes.
- Larger front analyzer/control surface with recessed blue spectral display, physical lower controller panel, fasteners and sealed sample access.
- Solidly supported autosampler, individually modeled sample vials and blue caps; no floating tray.
- Single vertical ionizer visibly integrated with cabinet, cooling vents and an inset ion port.
- Subdued original white/grey distribution, larger service hatch, mechanically consistent rear and side vents.
- True **1024x1024 source render**, Lanczos reduced to one **128x128 transparent NW RGBA** with many soft alpha levels. No palette reduction, pixel blocks or nearest-neighbor upscaling. Editable Blender source and two-layer OpenRaster artwork are retained.

The CLI workflow .github/workflows/art001-mass-resculpt-nw.yml produces a review-only archive including the editable .blend, high-res original render, native-size output, smooth mobile preview, editable layers and manifest with SHA256 inventory. The resulting image must be **visually inspected and compared at 1x to native HEM/RIA**, not simply presented as visually approved when CI passes.

**Open issues:** This is a materially different first NW silhouette candidate, not the finished game art. The detailed owner concept remains the visual target and the owner retains acceptance authority. Only after one direction looks authentic should FA propagate other directions or offer atlas integration to TS. This review may still require original 2D hand-finishing.

No editing of clinical G1, GameDB IDs, tags, shared object XML, DLC/Workshop files, gameplay rendering hooks, save behavior or installation. PR #14 remains Draft. Historical ART L4 3 PASS / 2 FAIL / 3 BLOCKED remains unchanged. No auto-merge or release.
