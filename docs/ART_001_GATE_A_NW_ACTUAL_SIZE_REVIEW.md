> **OWNER VISUAL DECISION — 2026-11-03:** Gate A NW previously delivered (`mass_spectrometer_NW_128.png` and layered original SVG/ORA) is **REJECTED, not to be published or staged**. Prior SHA evidence remains for traceability. The existing one-shot art gate prohibits expanding other directions or repeating minor cosmetic variants. The new art-production attempt is **BLOCKED** pending a demonstrably native-quality different approach, separate owner approval and 128px HEM/RIA comparison. Draft PR #14 unchanged for G1/TO and no L4.\n\n# ART-001 — Bounded Gate A: single NW mass-spectrometer visual review (2026-11-03)

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

## Gate A source-quality decision — 2026-11-03 (FA final bounded attempt)

**Result: TECHNICAL SOURCE NO-GO; owner visual judgment still PENDING.** The latest owner turn was "continue"; this is permission to continue **verification**, not evidence of a positive aesthetic sign-off or an exception to the frozen one-shot gate.

FA re-opened the **actual existing** PNG and the full original generated source (not a new image). A fresh independent local Pillow audit confirms:
- Native review RGBA: 128×128, alpha bbox `(6,32,122,126)`, **199 partially-transparent alpha levels**, **3,777 unique visible RGBA values**.
- Exact existing PNG SHA256: `1748c363c3ffac6037bb894a819c54ac12030a9e95ecb378818004f0e99475f2`. Concept SHA256: `4c038eb0aac68d23dd249271532aa12419d36a283a458ff6ceb0f09f7e3081c0`. No local file was replaced or regenerated.
- Smoothness and alpha were **verified**, but these checks are not stylistic acceptance.
- The generated 2D raster retains a long workstation-like built-in base that risks duplicate tabletop surfaces under the ART private-workbench placement contract; whether a source-only removal could preserve correct contact is **NOT PROVEN**.
- The image and algorithmic alpha mask do **not** preserve independently editable physical components, back surfaces, relative 3D coordinates or a reproducible orthographic NW→NE camera. Re-imagining NE with another generative request would violate Gate B identity and the owner's request to stop inconsistent multi-view sheets.

**Gate A fail-closed rule:** do **not** turn the user’s generic "continue" into an affirmative visual approval. Do not begin NE/SW/SE, generate more cosmetic NW variations, put this sprite into GameDB, call L2 complete, run another game test, merge or publish. Continue only via one of two explicitly separated paths:
1. **FA art source restoration** — require a genuinely authorable machine component model/layer source whose topology separates the machine from the lab countertop; then re-open **one NW** visual gate with owner approval *before* attempting NE from the same machine. This would require a substantively new art-production resource/approach, not another automatic filtered version.
2. **TS Alpha fallback research** — existing approved *feasibility assessment only* of reusing vanilla laboratory equipment with additive ABCL analysis. Requires proof of original equipment/procedure coupling, preservation of CBC and all existing departments, adult patients, 4 DLC and Workshop objects, and reversible save compatibility. TS must make a documented GO/NO-GO decision; FA is **not** authorized to change clinical/room/runtime XML, G1, native UI or gamesaves.

**Owner-facing artifact:** `ART001_GateA_technical_verdict.json`, created in the conversation from existing original files (no native art embedded); this report is **not** a committed binary and **not** a GitHub workflow. Current ART-001 branch and PR #14 remain Draft. Historical ART L4 3 PASS / 2 FAIL / 3 BLOCKED unchanged.

**Outcome:** one-shot *image-generation-only* approach is technically exhausted for the frozen four-direction requirements, not proof that an original ABCL equipment mod is impossible. Status should be **BLOCKED on editable physical source + owner visual approval**, not DONE and not a claim of failed G1 medical logic.
