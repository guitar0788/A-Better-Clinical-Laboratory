# ART-001 — native visual quality reset (owner rejection, 2026-11-02)

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
