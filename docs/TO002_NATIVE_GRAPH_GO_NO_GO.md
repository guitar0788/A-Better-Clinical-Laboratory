# TO-002 — bounded native relationship-diagram engineering verdict

**Date:** 2026-11-03  
**Owner request:** complete TS technical work without damaging the base game, four DLCs or Workshop add-ons.  
**Feature status:** **BLOCKED ON NATIVE L4 ANCHOR AND CLINICAL EDGE EVIDENCE. NO GRAPH NODE IMPLEMENTED.**  
**Code status:** exact-SHA genuinely compiled, source-only safe, read-only test probe.

## Existing facts — no repeated broad research needed

1. Vanilla `DependencyTreePanelController` sets up its close button; it does not provide a GameDB node registration API.
2. Owner-supplied `resources.assets` contains `dep_tree` original **1400×620** RGBA32 texture and Sprite. The original drawing contains **existing boxes and arrows**, with three fixed native laboratory arrows; icon labels are separate Unity UI controls.
3. Thus registering `ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB` cannot insert a fourth laboratory node or a clinically valid fourth arrow.
4. Existing G1 lab-room data and independently approved clinical routes must remain authoritative. No unlabeled shortcut from a guessed outpatient/ward path can be shown as a medical fact.
5. The old combined L4 screenshot shows no Toxicology Laboratory node, as expected: the deployed TS branch was only a read-only probe. No successful post-change hierarchy log is available.

## Source implementation delivered

`src/ABCLTO002ReadOnlyTreeProbe.cs` detects the original visible Dependency Tree and captures once/session, at most 180 transforms/24,000 characters, without UI changes or new files. The exact native `dep_tree` visual is discovered using read-only reflection on either `Image.sprite` **or** `RawImage.texture`. Both work on the original Unity UI component type without adding a static UnityEngine.UI dependency. A valid unique live `RectTransform` yields relative `graphUV` coordinates for existing icons, Text, and TextMeshProUGUI. The record includes native screen/canvas scaling, native texture/rectangle metadata and existing labels.

**Fail-closed:** no matching live original graphic, multiple matches, hidden panel, missing original controller, or incompatible Unity reflection -> **no anchor, no overlay and no native resource change**. The code never allocates a UI node, patches a native method, modifies original textures, installs Harmony, changes a save or edits original GameDB data.

Latest exact source SHA `1fb9ceb5fe947397b9ff0e0a924086cac2e4da7c`. GitHub Actions Verify **41632234805** PASS; CodeQL **41632234552** PASS; genuine Windows .NET 3.5/CLR2 compile PASS with **0 errors and 0 warnings**. Private generated ABCL DLL SHA256 `2D9112B44E38273B221D4FA412785CBC254259992658A6E903D32C8C3C95F217`.

## Go / No-Go for actual node and arrow

**GO only if all are present:**
- One original visible `DependencyTreePanelController` with exactly one matching real `dep_tree` `Image.sprite` or `RawImage.texture` anchor;
- actual live `RectTransform` and Canvas coordinates for the **three vanilla laboratory labels/icons** at representative supported resolutions;
- adequate non-overlapping space for a fourth node and clearly distinguishable line/edge inside the native graph layout;
- observed original ABCL blood-lead sampling/service referral path and proof that the proposed arrow connects semantically correct origin(s) and sink, not a guessed disease pathway;
- all injected visuals are **ABCL-private, reversible and namespaced**; no replacement of original graph pixels, no move of native labels or arrows, no global texture/material alteration and no saved-game mutation;
- explicit Vanilla/DLC/Workshop noninterference check.

**NO-GO / STOP:** any ambiguous anchor, inability to draw the fourth route without changing original arrows/graph meaning, fragile absolute screen coordinates, or unavoidable collision with original/DLC/Workshop UI. If NO-GO, do not implement a decorative fake node or continue repeated speculative patches; record the failed gate and propose a narrowly scoped optional ABCL-only supplementary information view outside the original graph **only after owner approval**.

## Exactly one remaining evidence collection

In **the next already scheduled, visually approved TO/FA combined disposable-save L4**, open the relationship diagram once. Capture the diagnostic's `[ABCL TO-002 TREE STRUCTURE]` entry from `output_log.txt` together with the existing screenshot. **No separate new game installation or repeated patient spawning is justified solely for this diagnostic.** If the runtime anchor is confirmed, TS can author/compile a reversible display patch as a *new* gated candidate. No current source record authorizes presenting #25 as done or releasing its feature.

## TO-001 technical handoff (separate issue #24)

The already compiled per-room floor bridge in Draft #29 isolates material changes to the exact ABCL room and retains native `TextureID`, `IconIndex`, zoning colors and original atlas. Native floor glyph uses a 16×32 atlas grid. The previous joint L4 failed on **art quality, centering and visual weight**, and the revised FA-1 SVG/PNG remains a **source-only candidate awaiting owner visual acceptance**. TS must not recolor or globally stretch original art to hide an aesthetic failure. Re-integrate only after owner approval and exact new art SHA.

**No automatic PR merge, no premature L4, no Alpha claim, no proprietary asset redistribution.**
