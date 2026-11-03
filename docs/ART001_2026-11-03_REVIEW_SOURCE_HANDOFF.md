# ART-001 — Owner-approved source submission, not game acceptance (2026-11-03)

**Repository:** guitar0788/A-Better-Clinical-Laboratory  
**Branch:** `feature/art-001-two-devices`  
**Issue:** #3 · **Draft PR:** #14  

## Owner's authorization

The owner explicitly approved **submitting** the two images produced in the preceding art-design turn after the 128×128 technical assessment. This permission means *preserve and store those exact images*; it does **not** authorize redesigning them, modifying GameDB object definitions, integrating directly into G1, installing a test package or merging the PR. Earlier rejected V7–V10 art and the ART-only L4 failures remain historical evidence, not PASS.

## Source and private proof

| Item | Exact file | SHA256 |
| --- | --- | --- |
| Mass spectrometer original four-view sheet | `assets/art001/review_20261103/original/mass_spectrometer_four_views.png` | `81f50e232cc275cf4939597f0170f7fde155ae28010b67976c42d6dd5c5e38ae` |
| Sample digestion original four-view sheet | `assets/art001/review_20261103/original/sample_digestion_four_views.png` | `a3edefd91d6eedc119856e3efaac613ba14ad4ae1c149a6a882fde70b5e9f708` |
| Diagnostic 2048×1024 atlas only | `assets/art001/review_20261103/diagnostic_equipment_atlas.png` | `b412b384056f1bc6e036175a4780523fb667959447d253f3b9778f1ee1d6f651` |

Both original sheets are 1254×1254 transparent PNGs, preserved **byte-for-byte**. Eight derived 128×128 transparent RGBA PNGs are in `frames/`, indexed 0–3 (mass NW, NE, SE, SW) and 4–7 (digestion NW, NE, SE, SW), using a 16×8 atlas layout with the remaining slots transparent. Their exact Git blob hashes and SHA256 values are recorded in `assets/art001/review_20261103/manifest.json`.

This package is an **art-source archive and diagnostic atlas**. The original game assets were only read for comparison and are not uploaded, copied or bundled. The diagnostic atlas is deliberately **not** saved under the production `Assets/ABCL/equipment_atlas.png` or referenced in `ModAssetListsABCL.xml`.

## TS integration boundaries and open blockers

The currently staged `OBJECT_ABCL_ART001_ICP_MS` and `OBJECT_ABCL_ART001_DIGESTION` definitions are tabletop attachments (`AttachedToObject=true`). Both submitted images depict substantial **self-supporting cabinets / full bases**. Do not force these images on top of the existing `OBJECT_ABCL_ART001_WORKBENCH`: this risks clipped bases, floating graphics and bad animation/occlusion anchors. TS should first independently assess **floor-standing original object** feasibility with the original structural rules, renderer footprint, object collision, player interactions and staff pathfinding, without modifying original or other mods' content.

The image-gen sheets are illustrated four-view concepts, not confirmed coherent 3D rotational exports and **not layered/3D editable original model files**. Before game art acceptance, TS / FA must assess each direction's physical continuity, real-size silhouette, visible alpha fringe, rotation, user-facing art quality, staff contact, stand-alone placement and save/reload. A separate exact-source L3 and disposable-save L4 remain required.

Historical ART-only L4: **3 PASS / 2 FAIL / 3 BLOCKED**; no completed L4 on the newly submitted art.

**Unchanged:** G1 medical logic, TO prefab XML, original three labs/CBC, all vanilla/DLC/Workshop files, original art hashes, custom tags and existing draft PR structure. Keep PR #14 **Draft**; no auto-merge, published package or medical edits from this FA source-only submission.
