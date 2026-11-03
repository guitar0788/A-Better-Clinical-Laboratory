# ART-001 — Bounded Gate A: single NW mass-spectrometer visual review (2026-11-03)

**STATUS: HOLD — OWNER VISUAL APPROVAL NOT RECEIVED. NOT a game-ready asset.** This is the *one* owner-authorized final NW appearance attempt under [the binding one-shot gate](ART_001_ONE_SHOT_VISUAL_GATE.md). Do not expand to NE, SW or SE, change object XML, initiate L3/L4, automatically merge or release.

## Source provenance, actual artifacts, and verification

The current visual is an **AI-generated single-view original concept PNG** (1254×1254 RGB with white background) produced in this FA chat on 2026-11-03. It is **not** a component-editable 3D/2D scene and not a set of real four-direction sprites. Neither the original generated concept nor its derived binaries are committed to GitHub as of this review; they are shared as **conversation attachments**, with these exact filenames:

- `NW_original_generated_concept.png` — original 1254×1254 RGB concept, SHA256 **4c038eb0aac68d23dd249271532aa12419d36a283a458ff6ceb0f09f7e3081c0**.
- `mass_spectrometer_NW_concept_extracted_master.png` — independent raster foreground extraction, original resolution, transparent RGBA source, SHA256 **fc08f63df71bfa592c13ff261ce79485826cf482164ec142434d6a84e3a23eba**. The alpha mask is editable separately; **machine components are not**.
- `mass_spectrometer_NW_review_128.png` — the **actual 128×128 transparent RGBA review** created from the full-resolution image by antialiased Lanczos downsampling, SHA256 **1748c363c3ffac6037bb894a819c54ac12030a9e95ecb378818004f0e99475f2**; alpha bbox **(6,32,122,126)** (Python/Pillow exclusive end). Exact native sprite count: **one NW study only**.
- `NW_GateA_actual_size_preview.png` — actual 1× native scale plus smooth enlarged checkerboard preview; **not** a production object sprite.
- `NW_editable_alpha_mask.png` and `GateA_manifest.json` — source mask and measurement/provenance inventory.

Local extraction/format checks: native cell 128×128, transparent background, **199 distinct fractional-alpha values**, **3,777 unique visible RGBA values**. This is smooth, antialiased 2D raster, **not 4-color or nearest-neighbor pixel art**. Mask derivation from an opaque generated concept is lossy and may need edge refinement. This report is a **local visual/source check**, not a GitHub Actions PASS, L2 resource contract PASS, L3 DLL test or L4 game test.

Vanilla original `objects_small_atlas.png` was opened **read-only** from the owner's local game archive; original HEM cells 248–251, RIA 252–255 and tabletop 472–475 were inspected privately. Native sprites and proprietary source pixels are **not included** in this report, GitHub, or the conversation review archive.

## Measured native-scale comparison and visual gate

- Vanilla HEM 248/249 spans approximately 119–120px wide by 107px high, with alpha touching bottom y=128; vanilla RIA 252/253 spans ~100px wide by 84px high. Different native silhouettes are intentional; there is **no fixed universal art bounding box**.
- Candidate actual alpha bounds **x=6–122, y=32–126** = **116×94 px**. Its baseline has been aligned near the native bottom, but the **wide, flat machine silhouette** is proportionally different from the original HEM equipment. Size alone **does not prove table fit**.
- **Passable direction cues in the single concept:** integrated vertical ion-source tower, blue-capped supported specimen rack, separate monitor and keyboard, neutral white/gray housing and smooth outlines are all recognizable.
- **Blocking art/contract issues:** the generated picture depicts a giant continuous countertop/bench-like lower plinth, even though existing ART-001 workbench attachment and game tables have their own native object/placement contract; this may become a *double countertop*. At 1× the keyboard, vents and some specimen details become tiny, and gradients/line thickness are visibly more illustration-like than native hand-authored HEM/RIA. The monitor, rack and tower positions **cannot be reconstructed reliably in NE** from a one-image generative source.
- There is **no physically persistent editable source model and no proof that it is exactly the same machine from more than one camera direction**. A single AI image, even converted into a genuine transparent native-size PNG, **cannot satisfy the full Gate A source/editability or Gate B directional-identity requirement**.

**Disposition:** Gate A image-extraction evidence exists; actual native-scale concept must be presented for **owner aesthetic judgment**. **Do not mark Gate A PASS**, and **do not fabricate new orientations**. If owner rejects the single native-scale design, the agreed one-shot rule is to **stop this generation route** rather than make indefinite versions, and have TS assess the separately approved vanilla-equipment Alpha fallback for feasibility only. This is not authorization to remove new instruments from the final product.

## Ownership and compatibility

FA owns visual originality and the single-direction art candidate. TS owns the main authority plan, actual GameDB asset registration, source-proof interop, workbench collision/attachment, rotation, vanilla patients, 4 DLC/Workshop safety, and eventual L3/L4. Preserve **PR #14 Draft** and historical art **L4 3 PASS / 2 FAIL / 3 BLOCKED**. No G1 medical changes, native atlas copying, installable package, merge or release.

**There is no new automated workflow run attached to this documentation-only review.** A green earlier ART-001 workflow does not validate this new generated concept cutout.
