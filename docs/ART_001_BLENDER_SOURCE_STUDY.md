# ART-001 Blender source-stage handoff (FA)

**Gate:** Experimental visual redesign, **not yet visually accepted**. The owner rejected V7–V10 geometric SVG studies and selected the detailed earlier concept board as the design target. Do not treat that generated illustration as actual source artwork, and do not copy its UI/background into a native equipment sprite.

## New source pipeline

- **Editable source code:** `tools/art001_blender_render.py`.
- **Editable original 3D asset:** `Sources/ART001_original_editable_3D.blend` within the CI review artifact; editable in Blender but no local installation is required to view PNGs.
- **Cloud-only CI:** `.github/workflows/art001-blender-review.yml`, using Python 3.11, pinned Blender Foundation `bpy==4.5.15`, Cycles CPU and Pillow.
- **Outputs:** eight unique original 128×128 RGBA views and `Previews/ART001_Blender_review.png` with four directions for two new instruments, plus SHA256 manifest. **Review only; no production atlas or installer.**
- **Original devices:** a mechanically integrated horizontal mass spectrometer with vertical ionizer, physically supported blue-capped specimen rack, mounted screen/keyboard and distinct service faces; a digestion workstation with continuous curved 3D glass hood, endcap frames, real enclosed sample racks and front/rear different panels.
- **Palette:** game-inspired neutral housing `#F2F2F2` / `#E6E6E6` / `#CCCCCC` / `#B3B3B3`, restrained cool-blue display and sample highlights.
- **View consistency:** rotate one physical model around Z by 90° for NW/NE/SE/SW; keep one fixed orthographic camera and consistent lighting, without SVG mirroring and without hand-imagined hidden parts. Blender calculates real mesh visibility, transparent glass and specular shading.

## Boundaries

No original-game texture or proprietary DLL is imported, bundled or redistributed. G1 medical logic, the ART-001 private-workbench/attachment rules, XML object registrations, vanilla/DLC/Workshop resource IDs and all installation workflows remain unchanged. TS owns game placement, rotation interface, medical workflow, collision and L4. The historical art L4 remains 3 PASS / 2 FAIL / 3 BLOCKED.

## Stage gates

- [ ] Headless Blender renders genuine eight 128×128 study views in GitHub Actions with a source .blend and hashed manifest.
- [ ] FA inspects the **actual** downloaded cloud artifact for silhouette, curved hood, color and occlusion rather than trusting green CI.
- [ ] Owner visually compares real PNG studies to the high-detail concept board and native HEM/RIA references. Source-only success is not aesthetic acceptance.
- [ ] If accepted visually, only then design a TS-reviewed game atlas and isolated ART-only L4; no merge, release, or installable package beforehand.

The first cloud build may fail due to headless runtime version issues; report the exact failure and fix it on **Draft PR #14**, rather than claiming Blender worked without evidence.
