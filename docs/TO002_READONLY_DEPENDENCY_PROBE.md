# TO-002 — native Dependency tree read-only L4 probe (test-only)

**Status:** Existing read-only probe had genuine L3 proof in Draft PR #32. The **newly expanded exact-Sprite/canvas diagnostic** requires its own exact-commit L2/L3 verification; no L4, no rendered Toxicology Laboratory node.

## Native static asset evidence — 2026-11-03

The owner-provided **original game files only** were inspected offline. Nothing from the game is copied into this repository.

- `ProjectHospital_Data/resources.assets` (from the owner-supplied archive), SHA256 `6aaa7c73b7ef2addc72e8ad91143d1790d36dcd862a5c8d2495cd46fa935d28e`; Unity serialized file version **17** (header). The exact ASCII asset name `dep_tree` appears twice as a **texture record** and a **Sprite record**.
- Serialized `dep_tree` Texture2D name occurs at byte offset **0x4092C**, with following little-endian width/height fields **1400 × 620**.
- The matching `dep_tree` Sprite name occurs at offset **0x78934**; the following floating-point width/height fields also report **1400 × 620**.
- Original `DependencyTreePanelController.cs` contains only `m_closeButton` and a `Start()` click handler calling `gameObject.SetActive(false)`. It does **not** enumerate `GameDBRoomType`, add nodes, or generate edges.

**Inference, not implementation proof:** the original Dependency Tree probably presents a preauthored full-size Sprite, not a dynamic laboratory-node list. The actual scene's relationship-panel component tree, Sprite-to-Image binding, native canvas render mode and screen scaling **still require runtime confirmation**. A screenshot showing the unchanged graph is insufficient to prove the read-only probe fired.

### Narrow engineering decision

Do **not** globally replace original `dep_tree`, mutate original UI prefabs, or distribute modified vanilla pixels. Only consider an *ABCL-owned, reversible child overlay* when the exact `dep_tree` Sprite Image is verified **within the visible native DependencyTreePanelController hierarchy**. Its anchor must be that actual native `RectTransform` and canvas, never a hardcoded screenshot pixel position. Confirm whether scaled layouts and DLC/Workshop UI leave enough space; edge directions must reflect the already accepted G1 routing. If an isolated node/edge cannot be proven safe, record a scoped **NO-GO** rather than patching shared UI.

The new probe logs the exact Sprite name, native source `rect` and texture dimensions, displayed `RectTransform.rect`, world corners, canvas render mode/reference scaling, and current screen dimensions — each within the original 180-item/24KB bounded one-shot read-only capture. It explicitly reports when the exact Sprite was **not** found; do not infer a safe overlay anchor in that case.

## Why this exists
Original game's `DependencyTreePanelController` exposes only a close button; it does not construct graph nodes through a normal GameDB room-type registry. The on-screen diagram is most likely part of a serialized Unity UI hierarchy. An additive ABCL room entry **does not** automatically inject into that graph. Current source lacks evidence for a safe external node-registration API.

## Static background vs. dynamic labels — stronger offline result (2026-11-03)

We inspected `dep_tree` **in memory only** by decoding its first RGBA mip from the owner's `resources.assets.resS`; no proprietary game image bytes are uploaded or committed. Metadata: `dep_tree` Texture2D is **1400×620, RGBA32 (format 4), mipmapped**; the external stream starts at byte **90258120** of `resources.assets.resS`. Its visible content comprises gray/white shaded **boxes and routing arrows**, **not** the hematology/microbiology/histology icons or localized Chinese/English room names shown in the owner's actual game screenshots. The native graph is therefore **composite**: a static underlying flowchart sprite with independently rendered room icons/text, not a complete single flattened UI screenshot.

Important nuance: the static base visibly has **three original laboratory arrow destinations**. A new fourth Toxicology node requires its own clinically sound connection and non-overlapping visual accommodation; cloning a vanilla icon does **not** automatically add a correct arrow or enlarge that fixed layout. Do not overstate the viability of a no-overwrite overlay merely because the words/icons are separate.

The enhanced probe performs a **unique exact-Sprite anchor** check on the *active* visible original panel and reports coordinates of its existing active `RectTransform` descendants in native **graphUV=(u,v)** space by inverting the actual graph transform. It fails closed when zero or multiple `dep_tree` Sprites are present. This is a necessary gate for a later ABCL-only overlay, **not a working overlay or node**.

The next implementation decision requires one existing/next shared L4 `output_log.txt` proving original three lab labels/icons, anchor and scaling. Only design ABCL-owned reversible nodes/edges after that evidence; otherwise record a bounded native-graph NO-GO without modifying original arrows/art or the clinical workflow.

## Bounded, nonintrusive inspection
`ABCLTO002ReadOnlyTreeProbe` runs only in the main hospital scene. Every 2 seconds until the native `DependencyTreePanelController` is actually visible, it does one read-only lookup. At first visible opening in a session it records **at most 180 transforms / 24,000 characters** (names, relative UI positions, bounds, optional local text and Sprite names) in one ordinary game log message starting `[ABCL TO-002 TREE STRUCTURE — READ ONLY / TEST ONLY]`. It then never scans again in that session. No Unity inspector or new player-installed plugin is required; it piggybacks on the existing G1 development panel test DLL. No writes, allocations of game objects, global patches, patient data, graph edits, or game/save changes.

**This does not require a separate immediate owner gameplay test.** Batch it with the next properly packaged, SHA-audited L4 round after TO-001 has its art ready, so the owner opens the relationship graph once during the same test session and can provide `output_log.txt` along with TO-001 screenshots. Do not ask the owner to repeat an entire L4 session only for this diagnostic.

## Stage gate
1. Source-only L2 guard validates one-shot bounded read-only behavior.
2. Genuine net35/CLR2 L3 against owner-authorized encrypted original DLLs; no source-only mock may be counted.
3. Package this test-only probe only in a disposable-save installation; DO NOT ship in public Alpha.
4. Inspect real logged hierarchy before proposing any node/edge. If Unity UI graph is static or an add-on registration cannot be isolated from the original tree, record a precise compatibility NO-GO; do not overwrite original serialized assets or draw fake clinical edges.
5. Only a later owner-accepted L4 could establish a genuine native graph modification.

Separate issues: #24 for room and on-floor icons; #26 for terminology. Preserve G1 clinical routes and all original/DLC/Workshop UI and saves.
