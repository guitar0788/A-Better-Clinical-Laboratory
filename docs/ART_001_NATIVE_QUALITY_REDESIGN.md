# ART-001 — native visual quality reset (owner rejection, 2026-11-02)

## Owner-designated visual reference: detailed V8 concept board (2026-11-02)

**FA visual gate: FAIL — current V7/V8/V9/V10 exported sprites do not follow this reference's level of detail.** The owner reposted the earlier blue-and-white ART-001 **concept board** (the board with a full laboratory scene, a large machine render, four orientation panels, icons, and the original-game comparisons) and explicitly challenged the discrepancy. This board is the **appearance target**, not an exported game sprite, an accepted final art resource or an installation package. Its infographic headers, checkmarks, UI, logo and laboratory background are **presentation only** and must never be pasted into native object atlas cells. Do not claim a generated concept image is a functional sprite.

### Physical design benchmark — Mass Spectrometer

- **Major silhouette:** one integrated professional tabletop instrument with a substantial horizontal main enclosure and a **tall ionization module** rising on the rear/side; not separate cuboids loosely stacked on a platform. Front service/display face, rear vent panel and upright module must refer to one consistent mechanical device across NW/NE/SE/SW.
- **Sample interface:** visible fixed cassette/autosampler zone with **blue-capped sample tubes**, machined supports, tray socket, small physical joint/shadow and plausible access clearance, not a floating tray or randomly duplicated vials.
- **Human controls:** believable front/right articulated screen, base/hinge, compact keyboard or control pad; rear and side perspectives show the *same* assembly occluded according to 3D position. Screen geometry cannot become mirrored or float in space.
- **Material:** neutral game-original #F2F2F2 / #E6E6E6 white-shell ladder with #CCCCCC / #B3B3B3 depth, crisp seams, grouped service doors, dark vent slits, restrained blue displays and authored soft bevels. Shell geometry and shading must carry volume, not a thin black outline around flat polygons.

### Physical design benchmark — Sample Digestion Workstation

- **Major silhouette:** broad low-profile enclosed chamber sitting on a substantial **integrated base** and framed by a **continuous curved translucent safety hood** from front to rear, with thick end caps. This is *not* a flat detached lid, open roof or generic white cube.
- **Inside:** credible sample tubes, rack/well plate, heating/sample area **visible through glass where physically exposed**; hidden behind rear opaque casing and side panels when the viewer rotates.
- **Human controls:** side/front mounted compact display, push controls and a small warning label. Ventilation slots and service hatch belong to fixed physical faces; no duplicated front control panel on the back.
- **Glass/material:** layered semi-transparent blue-gray glass with highlights/reflections and visible bevel thickness; cold neutral white outer shell, varied dark gray chassis, sparse non-neon yellow safety accents. No transparent view through opaque structures.

### Mandatory next production method and evidence

1. **STOP promoting procedural V7–V10 studies as 'improvements toward completion'.** These are archived technical experiments. V10 depth sorting fixes one failure mode but remains visually far beneath this design benchmark; a green CI is not an aesthetic PASS.
2. Make an **original, editable layered source** closely matching these machine designs. Use manual layered illustration, carefully authored curves/meshes, or a reproducible real geometry renderer; a new set of tiny polygons from the same procedural architecture is explicitly **not accepted**. The reference composition can guide the design, but do **not** copy full infographic pixels, native sprites, or copyrighted reference art into GitHub. A standalone concept illustration is not a 128px production sprite.
3. Before any atlas packaging, deliver a **single physical model's eight orthographic/isometric turnaround views**, NW/NE/SE/SW for both devices, with a coherent 3D layout, proper front/back/side occlusion, realistic topology and one consistent lighting direction. **Review all eight at actual 128×128**, plus enlarged sheets, against read-only vanilla HEM/RIA cells.
4. Fail the gate if the integrated mass spectrometer collapses into bare boxes, the digestion glass turns into a detached floating roof, parts are visible through opaque panels, or the source loses the concept board's recognisable mechanical features.
5. Preserve the existing ABCL-namespaced XML, static export verifier, safe icon margins, preview workflow, atlas mapping and private workbench interface without arbitrary re-registration. **Do not alter G1 clinical logic or gameplay integration**; TS owns object placement/rotation/staff-contact/L4. No merge, no alpha or installable package before owner art acceptance and later native L4.

**Status: NEEDS FULL ART REDRAW, owner visual acceptance NOT MET.** Owner requested original-game whites, but matching the palette alone is insufficient. No further 'V11 looks better' claim without an actual source export and direct visual evidence.

---


**Gate: FAIL / redesign required.** The owner compared the generated V7 mobile review to the original Project Hospital objects and rejected it. The formerly green Verify/CodeQL/export checks prove only technical source integrity, not art quality. The V7 geometry generator is a historical prototype, not an accepted visual base for another minor colour or edge edit.

## Binding references and preserved work

- The authoritative task state is `docs/MASTER_PLAN.md`; decisions `ABCL-D011`/`ABCL-D012` and `docs/LAB_VISUAL_STANDARD.md` remain binding. Official object tutorial and installed-game findings are in `docs/OFFICIAL_ART_GUIDANCE.md`.
- Inspect the owner's legally supplied vanilla `objects_small_atlas.png` **read-only**: hematology analyzer frames 248–251, RIA frames 252–255, bench frames 472–475, at their native **128 × 128** cell scale. These are references, never an export or GitHub deliverable.
- Preserve current additive ABCL GameDBObject IDs, private workbench/attachment allowlist, official source-derived atlas choices (`LAYOUT_16_X_8`, 2048 × 1024), neutral bilingual UI names, safe 64 × 64 icons, validated load paths and separate G1 clinical logic. A new artist must not rebuild them.
- `tools/verify_art_exports.py` and its review-only workflow test export/security/atlas integrity. **They cannot pass or overrule a human visual FAIL**. Keep installation-package generation on hold.

## Why V7 failed (observed in actual V7 review and native references)

1. Mass spectrometer: overly narrow modular tower, thin blue linework, repeated simple rectangular control areas and a floating-looking side tray. It does not read as a richly surfaced, practical native lab machine.
2. Digestion station: flat beveled box with a generic blue window and tiny identical controls. Original RIA has a stronger shaped shell, large curved hood and differentiated lower control face; V7's rear views remove the functional work area rather than showing a credible same-machine back.
3. Both: predominantly flat uniform cool-gray fills and fine outlines, few believable specular bands, softened material transitions, purposeful mechanical joints or integrated contact shadows. Native devices have much more convincing volume, small accents and complex functional surfaces.
4. NW/NE/SE/SW use mirroring too readily; directional features change sides without demonstrating one consistent 3D mechanical layout. A full physical 4-view turnaround is required.
5. The preview places fake ground ellipses beneath tabletop equipment. That presentation is not evidence of bench height, perspective or native attachment contact. Compare actual sprite silhouettes **without** preview-stage shadows at 1× first.

## Production workflow (no local desktop art software required)

**Checkpoint A — design specification and side-by-side review, no installer:** make a reference-derived shape sheet for each machine: silhouette, front operational face, sample flow, doors, service rear and top. Establish consistent four-way geometry and the color/material hierarchy. A separately marked concept visual may be generated to explore the design, but is **not** a sprite or approved game texture.

**Checkpoint B — original authored art:** commission or manually author layered, editable 2D/raster or SVG art with carefully shaded cabinets, weighted edges, crisp physical parts, restrained reflections and small controls. Avoid continuing the polygon-block procedural generator as the sole art process. Source should preserve editable layers and distinct physical views. Never trace or redistribute native pixels.

**Checkpoint C — mandatory true-scale comparison:** review native equipment and the new original sprites at **1× 128px**, and optionally 4× nearest-neighbor for inspection; 2× antialiased phone sheets are supplementary only. Check silhouette hierarchy, shading, surface count, readable small details, source consistency, bench-relative height and all four cardinal directions. Reject or revise before export automation or L4.

**Checkpoint D — compatibility export:** once approved visually, export exact NW/NE/SE/SW indexed cells, safe-area UI icons, full SHA256 manifest, original file list, passive source validation and existing review-only workflow. Ensure native and Workshop IDs/tags remain isolated.

**Checkpoint E — bounded art-only L4 (only after C and D):** one disposable-save test for private bench placement, four direction change, sprite pivot and bench contact, employee occlusion/walkability, and coexistence with vanilla hematology analyzer/RIA. Do **not** repeat the already accepted G1 R3 clinical patient test.

## Explicit acceptance and stop

- [ ] Owner approves the two individually legible machine designs relative to original HEM and RIA at 1×; both visibly exceed V7's flat schematic quality.
- [ ] Four directions remain mechanically consistent and materially detailed; no directional fake mirrors.
- [ ] Correct 128px native cell / attachment envelope and clear absence of invented ground-plane shadows.
- [ ] All original file, GameDB and noninterference checks pass; no copyrighted game assets, keys or DLLs in GitHub.
- [ ] Exact-SHA in-game art-only L4 placement, rotation, contact and noninterference tests pass.

Until these pass: keep ART-001 **NEEDS FULL VISUAL REDESIGN**, Issue #3 OPEN, PR #14 Draft, no merge, no release, no validated-install package. Historical L4 remains **3 PASS / 2 FAIL / 3 BLOCKED**.
