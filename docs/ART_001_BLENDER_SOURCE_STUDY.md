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

## Owner rejection — rendering style does not match vanilla (2026-11-02)

**Visual verdict: FAIL / NOT ACCEPTED.** The owner compared the actual Blender 4.5.15 cloud-rendered 8-view output to original Project Hospital HEM/RIA sprites, and found it conspicuously foreign to the game's art style. This overrides any implied acceptance from successful 3D occlusion, Blender CI or correct white RGB values.

FA compared the *actual downloaded PNGs* to the user's read-only original texture excerpts:

| At actual 128px game-cell scale | Original HEM/RIA | Blender V1 | Required correction |
| --- | --- | --- | --- |
| Rendering language | Compact, hand-tuned **2D game sprites**, deliberately stepped/dark silhouette edges, simplified tonal regions and local highlights | Smooth PBR/Cycles lighting, softly bevelled mesh, tiny floating-looking 3D features | Keep Blender only for object geometry/perspective; do **not** take its direct PBR render as final game art. Rework to a controlled **2D paintover / sprite stylization** at actual target resolution. |
| Color *distribution* | Strong flat neutral white broad regions, discrete grey outlines, short high-contrast blue/control accents | Correct white swatches but gray diffuse microshading and dark bluish machine base dominate | Restrict broad cabinet panels to vanilla-like #F2F2F2/#E6E6E6/#CCCCCC/#B3B3B3 with discrete intentional dark edges; no muddy PBR diffuse gradients. |
| Shape hierarchy | Native HEM has dominant one-piece body, large front operator feature and clear integrated sample-carrier silhouette; RIA has cohesive low opaque curved cover | Long rectangular mass-spectrometer bar, a small detached-feeling side monitor, uniformly thin details; large shiny translucent glass dome over digestion station | Rebuild **distinctive silhouette** before detailing. HEM and RIA are scale/style references, not shapes to clone; device must remain original and physically plausible. |
| Pixel legibility | Main controls, sample carriers and equipment edges purposefully exaggerated for tiny native cell | Too many thin modeled lines, keyboards and grilles alias/downsample into noise or vanish | Author prominent controls and shadow bands for **128×128 first**. Test in a vanilla lab scene, not only a magnified white preview sheet. |
| Shadows/contact | Native authored shadow/outline relationships sit in the full sprite and table context | Floating, crisp neutral background proof; no verified contact and Blender glossy depth | Explicit 2D local shadow, controlled outline weight and table-relative baseline, subject to later TS-owned L4 placement gate. |

**Do not start Blender V2 by merely changing lights, render samples, camera, or gray levels.** A source pipeline is proven technically, but its current *art direction* is rejected. Next FA deliverable is a **single fully revised 128px equipment sprite** with actual manual/illustrative raster finish and a native-reference 1× comparison. If it still reads foreign to the game, stop there rather than generating four or eight polished-looking but unusable orientations. Only after owner accepts the first sprite should FA propagate the editable physical model and painted style across the other seven directions and prepare a new noninstallable source artifact.

**Technical isolation:** Preserve the real .blend model and workflow for geometry reference. Do not rewrite G1 medical logic or art registration/attachment API. Do not distribute original HEM/RIA pixels or the earlier generated concept board as native assets. PR #14 stays Draft, no merge/release/installer and no new game L4. No claims about DLC/Workshop interoperability from Blender CI.

## V11 presentation-board provenance gate

The subsequently generated V11 multi-panel image is **concept presentation only**. It is not eight independent editable 128×128 RGBA game sprites, is not extracted from the Blender source, and has not passed the native HEM/RIA same-scale review. Its embedded PR/CI claims are decorative text and **not verified GitHub evidence**. Never stage this board into GameDB, label it as exported artwork, or use it as L2/L4 proof. Next FA task remains producing and inspecting **one genuine original 128×128 transparent equipment sprite** before any eight-view expansion. The owner's earlier V8 reference remains the quality target. Visual gate: FAIL; no installable output.
