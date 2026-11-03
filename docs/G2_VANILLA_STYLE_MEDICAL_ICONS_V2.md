# G2 medical icons — V2 correction after owner rejection

**Status: visual correction produced for owner preview; not yet approved / not installable / no game L4.** This is a **child PR of experimental G2 Draft #43**, not a release.

## Rejected art and reference evidence

On 2026-11-04 the owner explicitly rejected all eight earlier `MedicalIcons` PNGs **before testing**. The old combined ZIP is **WITHDRAWN, DO NOT INSTALL**. We preserve its SHA and failure report as history; no silent replacement of the earlier test package.

A read-only inspection of the original game `StreamingAssets/Textures/ui/icons.png` confirms a **2048×6144 RGBA sheet / 64×64 cells**; original medical diagnosis symbols (including the native toxic skull `IconIndex=1203`, neutral droplet `1169`, blood sampling `1641`, and urine sampling `1691`) are **small, flat, predominantly white medical pictograms**, not realistic shaded organs, glassware or machines. Original game artwork remains private read-only reference; do not publish/copy it into this repository.

## V2 change implemented

The two newly generated **assessment** diseases and their two private main symptoms now share just **two original icon glyph families**, each with a white transparent `64×64` and `32×32` RGBA asset:

- **Cadmium exposure assessment / 镉暴露评估** — `Cd` and three simple metal ingots. Original editable source `assets/g2/disease_icons_v2/cadmium.svg`.
- **Mercury exposure assessment / 汞暴露评估** — `Hg` and a compact liquid droplet. Original editable source `assets/g2/disease_icons_v2/mercury.svg`.

No shadows, gradients, hospital equipment or disease-skull icon are present. Shapes are drawn with original vector paths, not copied from the game. The Python renderer `tools/render_g2_vanilla_disease_icons_v2.py` makes **exact 64px and 32px transparent PNGs**, enforces consistent pure-white strokes, original-like alpha bounds and frozen source digests, and refuses installation paths. The PNG output is a **review artifact** until the owner approves actual 1:1 native-size appearance.

### Asset ownership corrected in the clinical builder

- `ModAssetListsG2.xml` now defines exactly **4** custom medical textures: two per disease and shared with its private main symptom. No `METALS_EXAM` or `DIGESTION` image asset is registered as a disease icon.
- G2 blood cadmium sampling/testing uses the **original** blood icon convention `IconIndex=1641`; G2 urine mercury uses original urine convention `1691`. Private `CustomIconBig/SmallAssetRef` fields are removed from examination entries to avoid duplicate or inappropriate disease images.
- G2 disease/main symptom fallback is changed from **1203 toxic skull** (misleading for exposure) to **1169 neutral original droplet**. Its appearance in any specific game UI still needs actual evidence; source-only checks do not guarantee custom icon preference over fallback.
- The sample digestion **device/build-menu art is owned by ART-001**, not G2 medical icons. The previously submitted FA independent four-direction device source and TO-004 owner-approved prefabs are unchanged.

### Hard gates

1. Source-only GitHub CI must generate four exact art PNGs, compare SHA256, check true 64/32 alpha and overlay XML IDs, original exam index and lack of old skull fallback.
2. The owner evaluates the two disease designs and 32px readability from the produced actual-size preview. **No assumption that V2 is accepted just because it was built.**
3. Only after explicit owner approval may TS replace the rejected icon assets inside a **new, explicitly versioned** unified G2 test package. Do not reuse the withdrawn old ZIP or overwrite unknown existing Mod files.
4. New diagnosis manual/forced confirmation bypass (C2) and actual private ICP-MS/digestion clinical L4 remain separate BLOCKED/NOT RUN gates. Do not claim game compatibility without a disposable-save L4.

**This draft does not merge main, release Alpha or modify original / DLC / third-party assets.**
